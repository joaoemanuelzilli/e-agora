"""Backtest point-in-time de fatores para ranquear ações brasileiras (painel mensal 2017-01 a 2026-09).

Uso:
  python pipeline/tests/factor_backtest.py [--sp DIR_SCRATCH] [--cache DIR_CACHE] [--from-stage fund|prices|panel|analysis]

Estágios (cada um grava cache em --cache e é reaproveitado se existir; --from-stage força a refazer dali em diante):
  fund      DFP 2015–2025 + ITR 2016–2026 brutos da CVM -> fundamentos por período (versão original do período, sem
            reapresentações do ano seguinte), LTM por aritmética de acumulados (serve a exercícios fora de dezembro).
  prices    COTAHIST (por ISIN, corte em lacunas > 45 dias) + desdobramentos/grupamentos/bonificações B3 (split_events /
            adjust de pipeline/market.py, mais detecção de razões "redondas") + proventos em dinheiro B3 -> índice de
            retorno total diário; ADTV; Ibovespa; CDI mensal (BCB SGS 4391).
  panel     painel mensal point-in-time (defasagem 45 d trimestre / 90 d anual), universo ADTV 3m >= R$ 5 mi, 14 fatores,
            blocos do painel e retornos futuros 1/3/6/12 meses.
  analysis  IC de Spearman (média, IC-IR, t Newey-West, % positivos, decaimento), quintis Q5−Q1, compostos (painel,
            pesos iguais, otimizado 2017–2022 testado 2023–2026, regime de crise), bootstrap de pesos.
Saídas: data/tests/factor_backtest.json, data/tests/factor_backtest.md
"""
import argparse
import json
import math
import os
import re
import sys
import time
import zipfile
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
import cvm  # noqa: E402  (funções de extração padronizada; o arquivo original não é alterado)
import market  # noqa: E402  (split_events / adjust)

DEFAULT_SP = "/tmp/claude-1000/-home-joaoemanuel-git-e-agora/cd238de5-f094-4d2e-ba5c-c5e5bf8d2192/scratchpad"
OUT_DIR = ROOT / "data" / "tests"
PANEL_START, PANEL_END = pd.Timestamp("2017-01-31"), pd.Timestamp("2026-09-30")
IS_END = pd.Timestamp("2022-12-31")  # amostra de estimação dos pesos; fora da amostra: retornos de 2023-01 em diante
OOS_START = pd.Timestamp("2022-12-20")  # 1ª formação fora da amostra (fim de dez/2022 -> retorno de jan/2023)
LAG_Q, LAG_A = 45, 90
ADTV_MIN = 5e6
HORIZONS = (1, 3, 6, 12)
STAGES = ["fund", "prices", "panel", "analysis"]
DOCS = ["DRE", "BPA", "BPP", "DFC_MI", "DFC_MD", "DVA"]
FIN_SUBSECTORS = {"Intermediários Financeiros", "Previdência e Seguros", "Serviços Financeiros Diversos"}
FIN_EXTRA = {"ITSA"}  # holding de participações (resultado = equivalência): sem EBITDA/margem significativos
UNIT_COMPOSITION = {"ENGI11": (1, 4), "IGTI11": (1, 2), "ALUP11": (1, 2), "BPAC11": (1, 2), "SAPR11": (1, 4),
                    "TAEE11": (1, 2), "KLBN11": (1, 4), "SANB11": (1, 1), "BRBI11": (1, 2)}


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def fnum(s):
    try:
        return float(str(s).replace(".", "").replace(",", "."))
    except Exception:
        return None


def finite(x):
    return x is not None and isinstance(x, (int, float, np.floating)) and math.isfinite(x)


# =====================================================================================================================
# 1) Fundamentos point-in-time (CVM bruto)
# =====================================================================================================================
def ticker_cnpj_map(sp, tickers):
    fca = pd.read_csv(Path(sp) / "work" / "fca_vm.csv", sep=";", dtype=str)
    t2c = dict(zip(fca.Codigo_Negociacao, fca.CNPJ_Companhia))
    t2c.update(cvm.EXTRA_CNPJ)
    det = json.load(open(Path(sp) / "raw" / "b3" / "details.json"))
    for tk in tickers:
        if tk not in t2c:
            c = (det.get(tk[:4]) or {}).get("cnpj")
            if c and len(c) == 14:
                t2c[tk] = f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"
    return {tk: t2c[tk] for tk in tickers if tk in t2c}


def _read_member(z, name, cnpjs):
    if name not in z.namelist():
        return None
    parts = []
    with z.open(name) as fh:
        for ch in pd.read_csv(fh, sep=";", encoding="latin1", dtype=str, chunksize=300_000,
                              usecols=lambda c: c in cvm.USECOLS or c.startswith("QT_")):
            ch = ch[ch.CNPJ_CIA.isin(cnpjs)]
            if len(ch):
                parts.append(ch)
    return pd.concat(parts, ignore_index=True) if parts else None


def _load_zip(args):
    zp, kind, y, cnpjs = args
    out = {}
    with zipfile.ZipFile(zp) as z:
        for doc in DOCS:
            for basis in ("con", "ind"):
                df = _read_member(z, f"{kind}_cia_aberta_{doc}_{basis}_{y}.csv", cnpjs)
                if df is not None and len(df):
                    out[(kind, doc, basis)] = df
        cc = _read_member(z, f"{kind}_cia_aberta_composicao_capital_{y}.csv", cnpjs)
        if cc is not None and len(cc):
            out[(kind, "CAP", "-")] = cc
    return kind, y, out


def load_store(sp, cnpjs, workers=4):
    raw = Path(sp) / "raw" / "cvm"
    jobs = [(raw / f"dfp_cia_aberta_{y}.zip", "dfp", y, set(cnpjs)) for y in range(2015, 2026)]
    jobs += [(raw / f"itr_cia_aberta_{y}.zip", "itr", y, set(cnpjs)) for y in range(2016, 2027)]
    jobs = [j for j in jobs if j[0].exists()]
    acc = {}
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for kind, y, out in ex.map(_load_zip, jobs):
            for k, df in out.items():
                acc.setdefault(k, []).append(df)
            log("cvm lido", kind, y)
    store = {}
    for k, parts in acc.items():
        df = pd.concat(parts, ignore_index=True)
        df["VERSAO"] = pd.to_numeric(df["VERSAO"], errors="coerce")
        if "DS_CONTA" in df:
            df["DS_CONTA"] = df["DS_CONTA"].fillna("")
        if "VL_CONTA" in df:
            df["VL_RAW"] = pd.to_numeric(df["VL_CONTA"], errors="coerce")
            scale = np.where(df["ESCALA_MOEDA"].str.upper().str.startswith("MIL"), 1e-3, 1e-6)
            df["VL"] = df["VL_RAW"] * scale
        if k[1] != "CAP":
            df = cvm.latest_version(df)
        store[k] = df
    return store


def _eps(dre_rows):
    """Lucro básico por ação (R$/ação, valor bruto) por classe: {'ON': x, 'PN': y, ...}."""
    out = {}
    sub = dre_rows[dre_rows.CD_CONTA.str.startswith("3.99.01.")]
    for r in sub.itertuples():
        lab = (r.DS_CONTA or "").strip().upper()
        lab = re.sub(r"[^A-Z]", "", lab) or r.CD_CONTA
        if pd.notna(r.VL_RAW):
            out[lab] = float(r.VL_RAW)
    return out


def company_periods(g):
    """g: {(kind, doc, basis): df} de um CNPJ -> {DT_REFER: registro com fluxos acumulados no exercício e balanço}."""
    recs = {}
    ftype = None
    for kind in ("dfp", "itr"):
        for dt in sorted(set().union(*[set(g[(kind, "DRE", b)].DT_REFER.unique()) for b in ("con", "ind") if (kind, "DRE", b) in g] or [set()])):
            basis = "con" if (kind, "DRE", "con") in g and (g[(kind, "DRE", "con")].DT_REFER == dt).any() else "ind"
            dre_all = g[(kind, "DRE", basis)]
            dre = dre_all[(dre_all.DT_REFER == dt) & (dre_all.ORDEM_EXERC == "ÚLTIMO")]
            if not len(dre):
                continue
            ini = dre.DT_INI_EXERC.dropna()
            fy_start = ini.min() if len(ini) else None
            dre_ytd = dre[dre.DT_INI_EXERC == fy_start] if fy_start else dre
            tabs = {"DRE": cvm.tab_from(dre_ytd)}
            for doc in ("BPA", "BPP", "DFC_MI", "DFC_MD", "DVA"):
                df = g.get((kind, doc, basis))
                if df is None:
                    continue
                sub = df[(df.DT_REFER == dt) & (df.ORDEM_EXERC == "ÚLTIMO")]
                if len(sub):
                    tabs[doc] = cvm.tab_from(sub)
            if "DFC_MI" not in tabs and "DFC_MD" in tabs:
                tabs["DFC_MI"] = tabs["DFC_MD"]
            ft = cvm.fin_type(tabs["DRE"])
            ftype = ft or ftype
            # fluxos também na outra base (bancos: ITR individual x DFP consolidada) para o LTM usar uma base só
            alt = {}
            ob = "ind" if basis == "con" else "con"
            if (kind, "DRE", ob) in g:
                d2 = g[(kind, "DRE", ob)]
                d2 = d2[(d2.DT_REFER == dt) & (d2.ORDEM_EXERC == "ÚLTIMO")]
                if len(d2):
                    i2 = d2.DT_INI_EXERC.dropna()
                    d2 = d2[d2.DT_INI_EXERC == i2.min()] if len(i2) else d2
                    t2 = {"DRE": cvm.tab_from(d2)}
                    for doc in ("DFC_MI", "DFC_MD", "DVA"):
                        df = g.get((kind, doc, ob))
                        if df is not None:
                            sub = df[(df.DT_REFER == dt) & (df.ORDEM_EXERC == "ÚLTIMO")]
                            if len(sub):
                                t2[doc] = cvm.tab_from(sub)
                    if "DFC_MI" not in t2 and "DFC_MD" in t2:
                        t2["DFC_MI"] = t2["DFC_MD"]
                    alt[ob] = t2
            recs[dt] = {"kind": kind, "dt": dt, "fy_start": fy_start, "basis": basis, "tabs": tabs, "alt": alt, "eps": _eps(dre_ytd), "ft": ft}
    def fix_ctrl(f):
        ni, ct, mn = f.get("net_income"), f.get("ni_controlling"), f.get("ni_minority")
        if finite(ni) and finite(ct) and abs(ct) < 1e-6 and abs(ni) > 1:  # atribuição trocada/zerada no arquivo original
            f["ni_controlling"] = ni if not finite(mn) or abs(mn - ni) <= 0.02 * abs(ni) + 0.5 else ni - mn
        return {k: (float(v) if finite(v) else None) for k, v in f.items()}
    out = {}
    for dt, r in recs.items():
        f, b = cvm.flows_bs(r["tabs"], ftype)
        by_basis = {r["basis"]: fix_ctrl(f)}
        for ob, t2 in r["alt"].items():
            f2 = cvm.extract_flows(t2.get("DRE", {}), t2.get("DFC_MI", {}), t2.get("DVA", {}), ftype)
            by_basis[ob] = fix_ctrl(f2)
        out[dt] = {"kind": r["kind"], "fy_start": r["fy_start"], "basis": r["basis"], "eps": r["eps"],
                   "ytd": by_basis[r["basis"]], "ytd_by_basis": by_basis,
                   "bs": {k: (float(v) if finite(v) else None) for k, v in b.items()}}
    return out, ftype


def add_ltm(periods):
    """LTM(T) = acumulado(T) + exercício anterior − acumulado(T − 1 ano); no fechamento do exercício, LTM = exercício."""
    for dt, p in periods.items():
        if p["kind"] == "dfp":
            p["ltm"] = dict(p["ytd"])
            p["ltm_eps"] = dict(p["eps"])
            continue
        p["ltm"], p["ltm_eps"] = None, None
        if not p["fy_start"]:
            continue
        prev_fy = (pd.Timestamp(p["fy_start"]) - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        t = pd.Timestamp(dt)
        prev_dt = (t - pd.DateOffset(years=1)).strftime("%Y-%m-%d")
        fy, py = periods.get(prev_fy), periods.get(prev_dt)
        if py is None:  # fim de mês com dia diferente (fevereiro etc.)
            cands = [k for k in periods if periods[k]["kind"] == "itr" and abs((pd.Timestamp(k) - (t - pd.DateOffset(years=1))).days) <= 3]
            py = periods[cands[0]] if cands else None
        if fy is None or fy["kind"] != "dfp" or py is None:
            continue
        basis = next((b for b in (p["basis"], "ind" if p["basis"] == "con" else "con")
                      if all(b in (x.get("ytd_by_basis") or {}) for x in (p, fy, py))), None)
        if basis is None:  # sem as três peças na mesma base: não mistura consolidado com individual
            continue
        ya, yb, yc = p["ytd_by_basis"][basis], fy["ytd_by_basis"][basis], py["ytd_by_basis"][basis]
        ltm = {}
        for k, a in ya.items():
            b, c = yb.get(k), yc.get(k)
            ltm[k] = a + b - c if all(finite(x) for x in (a, b, c)) else None
        p["ltm"] = ltm
        p["ltm_basis"] = basis
        p["ltm_eps"] = {k: p["eps"][k] + fy["eps"][k] - py["eps"][k] for k in p["eps"] if k in fy["eps"] and k in py["eps"]}
    return periods


def shares_history_cvm(cap, sup_issuer):
    """Ações em circulação por DT_REFER (composição do capital CVM, 2020+), com a mesma detecção de escala do cvm.py."""
    if cap is None or not len(cap):
        return []
    cs = cap.sort_values(["DT_REFER", "VERSAO"]).copy()
    for c_ in ["QT_ACAO_ORDIN_CAP_INTEGR", "QT_ACAO_PREF_CAP_INTEGR", "QT_ACAO_TOTAL_CAP_INTEGR", "QT_ACAO_ORDIN_TESOURO",
               "QT_ACAO_PREF_TESOURO", "QT_ACAO_TOTAL_TESOURO"]:
        cs[c_] = pd.to_numeric(cs[c_], errors="coerce")
    hist = []
    for dt, gg in cs.groupby("DT_REFER"):
        r = gg.iloc[-1]
        tot = r.QT_ACAO_TOTAL_CAP_INTEGR
        tes = r.QT_ACAO_TOTAL_TESOURO if np.isfinite(r.QT_ACAO_TOTAL_TESOURO) else 0.0
        if tot and np.isfinite(tot):
            hist.append({"date": dt, "total": float(tot), "treasury": float(tes), "outstanding": float(tot - tes)})
    b3_total = fnum((sup_issuer or {}).get("totalNumberShares", "0")) or 0.0
    scale = 1.0
    if hist and b3_total:
        r = b3_total / hist[-1]["total"]
        scale = 1000.0 if 300 < r < 30000 else 1.0
    for h in hist:
        for kk in ("total", "treasury", "outstanding"):
            h[kk] *= scale
    if hist and b3_total and scale == 1000.0:
        last = hist[-1]
        if last["total"] and last["treasury"] / last["total"] > 0.25:
            for h in hist:
                h["treasury"] /= 1000.0
                h["outstanding"] = h["total"] - h["treasury"]
    return hist


def stage_fund(sp, cache, tickers):
    t2c = ticker_cnpj_map(sp, tickers)
    sup = json.load(open(Path(sp) / "raw" / "b3" / "supplement.json"))
    cnpjs = sorted(set(t2c.values()))
    log("fundamentos: tickers com CNPJ", len(t2c), "de", len(tickers), "| CNPJs", len(cnpjs))
    store = load_store(sp, cnpjs)
    by_cnpj = {}
    for k, df in store.items():
        for cn, gg in df.groupby("CNPJ_CIA"):
            by_cnpj.setdefault(cn, {})[k] = gg
    fund = {}
    for tk, cn in t2c.items():
        g = by_cnpj.get(cn)
        if not g:
            continue
        g_fin = {k: v for k, v in g.items() if k[1] != "CAP"}
        if not g_fin:
            continue
        periods, ftype = company_periods(g_fin)
        periods = add_ltm(periods)
        caps = [g[k] for k in (("dfp", "CAP", "-"), ("itr", "CAP", "-")) if k in g]
        cap = pd.concat(caps, ignore_index=True) if caps else None
        fund[tk] = {"cnpj": cn, "ftype": ftype, "periods": periods, "shares": shares_history_cvm(cap, sup.get(tk[:4]))}
    pd.to_pickle(fund, Path(cache) / "fund.pkl")
    log("fundamentos: empresas", len(fund))
    return fund


# =====================================================================================================================
# 2) Preços: retorno total diário ajustado por eventos, volume, Ibovespa, CDI
# =====================================================================================================================
NICE = [2, 3, 4, 5, 8, 10, 20, 25, 50, 100]
MANUAL_SPLITS = {}  # {ticker: [(data_com, multiplicador)]} para eventos ausentes em B3 e Yahoo (nenhum necessário hoje)
CLASS_BY_SUFFIX = {"3": ["ON"], "4": ["PN", "PNA"], "5": ["PNA"], "6": ["PNB"], "11": ["UNT"]}


def dividend_rows(sp, cache, issuer):
    for d in (Path(sp) / "raw" / "b3" / "dividends", Path(cache).parent / "dividends", Path(cache) / "dividends"):
        p = d / f"{issuer}.json"
        if p.exists():
            return json.load(open(p)).get("rows") or [], True
    return [], False


def fetch_missing_dividends(sp, cache, issuers):
    """Baixa o histórico de proventos B3 (mesma API de pipeline/dividends.py) dos emissores sem arquivo local."""
    import dividends as dv
    sup = json.load(open(Path(sp) / "raw" / "b3" / "supplement.json"))
    det = json.load(open(Path(sp) / "raw" / "b3" / "details.json"))
    out = Path(cache) / "dividends"
    out.mkdir(parents=True, exist_ok=True)
    for iss in issuers:
        if dividend_rows(sp, cache, iss)[1]:
            continue
        s = sup.get(iss) or {}
        used, rows = dv.history(dv.name_variants(s.get("tradingName"), det.get(iss)))
        json.dump({"name": used, "rows": rows}, open(out / f"{iss}.json", "w"), ensure_ascii=False)
        log("proventos baixados", iss, len(rows))


def fetch_yahoo_splits(cache, tickers):
    """Histórico completo de desdobramentos/grupamentos/bonificações (Yahoo, eventos 'split'), com cache local.
    O suplemento da B3 só traz o evento mais recente de cada tipo por ISIN (ex.: BBDC sem as bonificações 2015–2021)."""
    from urllib.request import Request, urlopen
    p = Path(cache) / "yahoo_splits.json"
    data = json.load(open(p)) if p.exists() else {}
    for tk in tickers:
        if tk in data:
            continue
        url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}.SA?period1=1420070400&period2=1793000000"
               f"&interval=1d&events=split")
        ev = None
        for attempt in range(3):
            try:
                with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r:
                    d = json.loads(r.read().decode())
                res = (d.get("chart") or {}).get("result") or [{}]
                ev = [[datetime.fromtimestamp(int(k), tz=timezone.utc).strftime("%Y-%m-%d"), float(v["numerator"]), float(v["denominator"])]
                      for k, v in ((res[0].get("events") or {}).get("splits") or {}).items()]
                break
            except Exception:
                time.sleep(1.5 * (attempt + 1))
        if ev is not None:
            data[tk] = sorted(ev)
            json.dump(data, open(p, "w"))
    return data


def merge_events(b3_events, yahoo, index):
    """Eventos B3 + Yahoo (data-com = pregão anterior ao ex-dia); duplicatas (±7 dias, fator ±3%) ficam com a B3."""
    evs = list(b3_events)
    for ds, num, den in yahoo or []:
        if not num or not den:
            continue
        mult = num / den
        if abs(mult - 1) < 1e-6:
            continue
        ex = pd.Timestamp(ds)
        prior = index[index < ex]
        if not len(prior):
            continue
        dcom = prior[-1]
        if any(abs((d - dcom).days) <= 7 and abs(m / mult - 1) < 0.03 for d, m in evs):
            continue
        evs.append((dcom, mult))
    return sorted(evs)


def class_dividends(rows, ticker):
    """[(data_com, valor por ação/unit)] da classe negociada; units: linha UNT ou composição ON + k·PN."""
    def parse(r):
        d = pd.to_datetime(r.get("lastDatePriorEx"), format="%d/%m/%Y", errors="coerce")
        v = fnum(r.get("valueCash"))
        q = fnum(r.get("quotedPerShares")) or 1.0
        return d, (v / q if v is not None and q else None)
    suffix = ticker[4:]
    agg = {}
    seen = set()
    for r in rows:
        key = (r.get("typeStock"), r.get("lastDatePriorEx"), r.get("corporateAction"), r.get("valueCash"), r.get("dateApproval"))
        if key in seen:
            continue
        seen.add(key)
        d, v = parse(r)
        if pd.isna(d) or v is None or v <= 0:
            continue
        agg.setdefault(r.get("typeStock"), {}).setdefault(d, 0.0)
        agg[r.get("typeStock")][d] += v
    if suffix == "11":
        out = dict(agg.get("UNT", {}))
        n_on, n_pn = UNIT_COMPOSITION.get(ticker, (1, 2))
        pn = agg.get("PN") or agg.get("PNA") or {}
        for d, v in (agg.get("ON") or {}).items():
            if d not in out:
                out[d] = n_on * v + n_pn * pn.get(d, 0.0)
        return sorted(out.items())
    for cls in CLASS_BY_SUFFIX.get(suffix, ["ON"]):
        if cls in agg:
            return sorted(agg[cls].items())
    return []


def stage_prices(sp, cache, tickers):
    df = pd.read_csv(Path(sp) / "work" / "cotahist.csv.gz", parse_dates=["date"])
    sup = json.load(open(Path(sp) / "raw" / "b3" / "supplement.json"))
    idx = json.load(open(Path(sp) / "raw" / "b3" / "indices.json"))
    ibov = pd.Series({pd.Timestamp(d): v for d, v in idx["IBOV"]}).sort_index()
    ibov = ibov[~ibov.index.duplicated()]
    fetch_missing_dividends(sp, cache, sorted({t[:4] for t in tickers}))
    latest_isin = df[df.date >= "2026-09-01"].sort_values("date").groupby("ticker")["isin"].last()
    ysplits = fetch_yahoo_splits(cache, tickers)
    per, issues = {}, {}
    for tk in tickers:
        if tk not in latest_isin.index:
            issues[tk] = "sem negociação em 2026-09+"
            continue
        isin = latest_isin[tk]
        s = df[df["isin"] == isin].sort_values(["date", "volume"]).drop_duplicates("date", keep="last").set_index("date")
        fat = s["fatcot"].replace(0, 1).astype(float)
        for c in ("open", "high", "low", "close", "avg"):
            s[c] = s[c] / fat
        gaps = s.index.to_series().diff().dt.days
        big_gap = gaps[gaps > 45]
        if len(big_gap):
            s = s[s.index >= big_gap.index[-1]]
        if len(s) < 60:
            issues[tk] = "menos de 60 pregões"
            continue
        evs = merge_events(market.split_events(sup.get(tk[:4]), isin), ysplits.get(tk), s.index)
        close_adj = market.adjust(s["close"], evs)
        rets = close_adj.pct_change().dropna()
        extra = []
        for d, r_ in rets[rets.abs() > 0.35].items():  # desdobramentos/grupamentos ausentes na lista B3 (como market.py)
            ratio = 1 + r_
            for m in NICE:
                for mult in (m, 1 / m):
                    if abs(ratio * mult - 1) < 0.08:
                        extra.append((s.index[s.index.get_loc(d) - 1], mult))
        evs = sorted(evs + extra + [(pd.Timestamp(d), m) for d, m in MANUAL_SPLITS.get(tk, [])])
        # restituição de capital em ações (ex.: BRAP4 entregou ações da Vale em 12/2021): ajuste neutro no ex-dia
        neutral = []
        for e in (sup.get(tk[:4]) or {}).get("stockDividends") or []:
            if e.get("isinCode") == isin and e.get("label") == "REST CAP ACOES":
                dcom = market.ptdate(e["lastDatePrior"])
                after = s.index[s.index > dcom]
                before = s.index[s.index <= dcom]
                if len(after) and len(before):
                    neutral.append((before[-1], float(s["close"].loc[before[-1]] / s["close"].loc[after[0]])))
        adj_evs = sorted(evs + neutral)
        close_adj = market.adjust(s["close"], adj_evs)
        rows, _ = dividend_rows(sp, cache, tk[:4])
        divs = class_dividends(rows, tk)
        dps = pd.Series(0.0, index=s.index)
        div_list = []
        for dc, v in divs:
            later = s.index[s.index > dc]
            if not len(later) or dc < s.index[0]:
                continue
            f = 1.0
            for dcom, mult in adj_evs:
                if dcom >= dc:
                    f *= mult
            dps.loc[later[0]] += v / f
            div_list.append((dc, v / f))
        prev = close_adj.shift(1)
        r = ((close_adj + dps) / prev - 1).iloc[1:]
        tr = pd.concat([pd.Series([1.0], index=[s.index[0]]), (1 + r).cumprod()])
        weird = r[r.abs() > 0.35]
        per[tk] = {"isin": isin, "close": s["close"].astype(float), "adj": close_adj.astype(float), "tr": tr.astype(float),
                   "volume": s["volume"].astype(float), "events": evs, "adj_events": adj_evs, "divs": div_list, "weird": [(d.strftime("%Y-%m-%d"), float(x)) for d, x in weird.items()]}
    cdi = fetch_cdi(cache)
    out = {"per": per, "ibov": ibov, "cdi": cdi, "issues": issues}
    pd.to_pickle(out, Path(cache) / "prices.pkl")
    log("preços: tickers", len(per), "| problemas", issues)
    return out


def fetch_cdi(cache):
    """CDI mensal (% a.m., BCB SGS 4391); cache local. Sem rede: None (Sharpe vira retorno/vol sem taxa livre)."""
    p = Path(cache) / "cdi_4391.json"
    if not p.exists():
        try:
            from urllib.request import Request, urlopen
            url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4391/dados?formato=json&dataInicial=01/01/2015&dataFinal=31/12/2026"
            with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r:
                json.dump(json.loads(r.read().decode()), open(p, "w"))
        except Exception as e:
            log("CDI indisponível:", e)
            return None
    d = json.load(open(p))
    s = pd.Series({pd.Timestamp(datetime.strptime(x["data"], "%d/%m/%Y")) + pd.offsets.MonthEnd(0): float(x["valor"]) / 100 for x in d})
    return s.sort_index()


# =====================================================================================================================
# 3) Painel mensal point-in-time
# =====================================================================================================================
FACTORS = ["ep", "bp", "ebitda_ev", "dy", "roe", "roic", "gross_margin", "piotroski", "altman", "nd_ebitda",
           "mom_12_1", "vol_1y", "beta_2y", "size"]
SIGN = {"ep": 1, "bp": 1, "ebitda_ev": 1, "dy": 1, "roe": 1, "roic": 1, "gross_margin": 1, "piotroski": 1, "altman": 1,
        "nd_ebitda": -1, "mom_12_1": 1, "vol_1y": -1, "beta_2y": -1, "size": -1}
LABEL = {"ep": "E/P", "bp": "B/P", "ebitda_ev": "EBITDA/EV", "dy": "DY 12m", "roe": "ROE", "roic": "ROIC",
         "gross_margin": "Margem bruta", "piotroski": "Piotroski F", "altman": "Altman Z″ (EM)", "nd_ebitda": "Dív. líq./EBITDA",
         "mom_12_1": "Momentum 12-1", "vol_1y": "Volatilidade 1a", "beta_2y": "Beta 2a", "size": "Tamanho (log mcap)"}
GROUP = {"ep": "valor", "bp": "valor", "ebitda_ev": "valor", "dy": "valor", "roe": "qualidade", "roic": "qualidade",
         "gross_margin": "qualidade", "piotroski": "qualidade", "altman": "solidez", "nd_ebitda": "solidez",
         "mom_12_1": "momentum", "vol_1y": "baixo risco", "beta_2y": "baixo risco", "size": "tamanho"}
NONFIN_ONLY = {"ebitda_ev", "roic", "gross_margin", "piotroski", "altman", "nd_ebitda"}


def month_grid(ibov):
    s = ibov[ibov.index >= "2015-12-01"]
    return list(s.groupby(s.index.to_period("M")).apply(lambda x: x.index[-1]))


def _period_index(periods):
    rows = []
    for dt, p in periods.items():
        lag = LAG_A if p["kind"] == "dfp" else LAG_Q
        rows.append((pd.Timestamp(dt) + pd.Timedelta(days=lag), pd.Timestamp(dt), dt))
    return sorted(rows, key=lambda x: x[1])


def _year_before(periods, dt):
    t = pd.Timestamp(dt) - pd.DateOffset(years=1)
    k = t.strftime("%Y-%m-%d")
    if k in periods:
        return periods[k]
    for kk in periods:
        if abs((pd.Timestamp(kk) - t).days) <= 3:
            return periods[kk]
    return None


def shares_at(hist, events, d, impl=None):
    """Ações em circulação na base de cotação da data d. Registro CVM (2020+) <= d ajustado por eventos posteriores;
    antes do 1º registro: retroprojeção pelos eventos B3 × correção de emissões/recompras via LPA (lucro / LPA básico)."""
    if not hist:
        return None
    best = None
    for h in hist:
        if pd.Timestamp(h["date"]) <= d:
            best = h
    if best is not None:
        n = best["outstanding"]
        b = pd.Timestamp(best["date"])
        for dcom, mult in events:
            if b <= dcom < d:
                n *= mult
        return n
    first = hist[0]
    b = pd.Timestamp(first["date"])
    n = first["outstanding"]
    for dcom, mult in events:
        if d <= dcom < b:
            n /= mult
    if impl is not None and len(impl):
        r = impl[impl.index <= d]
        r = r.iloc[-1] if len(r) else impl.iloc[0]
        n *= r
    return n


def fix_share_scale(hist, b3_total, events):
    """Escala por registro (unidades x milhares) escolhida contra a referência B3 atual retroprojetada pelos eventos;
    a CVM mistura escalas entre anos (ex.: BBDC 2020 em milhares, 2021+ em unidades)."""
    out = []
    for h in hist:
        if not h["total"] or h["total"] <= 0:
            continue
        d = pd.Timestamp(h["date"])
        ref = b3_total
        for dcom, mult in events:
            if dcom >= d:
                ref /= mult
        # o registro pode já refletir evento ocorrido entre o fim do período e a entrega (ex.: IRBR3 2022 após grupamento)
        k_post = 1.0
        for dcom, mult in events:
            if d < dcom <= d + pd.Timedelta(days=150):
                k_post *= mult
        cands = [(s_, k) for s_ in (1e-3, 1e-2, 0.1, 1.0, 10.0, 100.0, 1e3) for k in ({1.0, k_post})]  # LAVV3 2T26: 10×
        best, kb = (1.0, 1.0) if not ref else min(cands, key=lambda c: abs(math.log(h["total"] * c[0] / c[1] / ref)))
        best = best / kb
        tot, tre = h["total"] * best, h["treasury"] * best
        if tot > 0 and tre / tot > 0.25:
            tre = tre / 1000 if tre / 1000 / tot <= 0.25 else 0.0
        out.append({"date": h["date"], "total": tot, "treasury": tre, "outstanding": tot - tre})
    return out


def implied_share_ratio(f, sup_iss, events, hist, first_px):
    """Razão (ações implícitas pelo LPA) / (retroprojeção por eventos) nos períodos anteriores ao 1º registro CVM.
    Usada só quando estável (mediana móvel de 3 períodos) e com desvio > 15% (limites 0,5–1,25)."""
    if not hist:
        return None
    b0 = pd.Timestamp(hist[0]["date"])
    on = fnum((sup_iss or {}).get("numberCommonShares", "0")) or 0.0
    pn = fnum((sup_iss or {}).get("numberPreferredShares", "0")) or 0.0
    w_on = on / (on + pn) if on + pn > 0 else 1.0
    pts = {}
    for dt, p in f["periods"].items():
        d = pd.Timestamp(dt)
        if d > b0 + pd.Timedelta(days=370) or d < first_px + pd.Timedelta(days=200):  # antes do IPO/1º pregão: ruído
            continue
        eps = p["eps"]
        ni = p["ytd"].get("ni_controlling")
        e_on = eps.get("ON")
        e_pn = next((eps[k] for k in ("PN", "PNA", "PNB") if k in eps), None)
        if e_on is None and e_pn is None:
            continue
        e = (w_on * (e_on if e_on is not None else e_pn) + (1 - w_on) * (e_pn if e_pn is not None else e_on))
        if not finite(ni) or not finite(e) or abs(e) < 0.02 or abs(ni) < 5:
            continue
        n_impl = ni * 1e6 / e
        n_back = shares_at(hist, events, d)
        if n_back and n_impl > 0:
            pts[d] = n_impl / n_back
    if len(pts) < 3:
        return None
    s = pd.Series(pts).sort_index()
    # normaliza pela razão observada perto do 1º registro (onde a retroprojeção é exata)
    near = s[(s.index >= b0 - pd.Timedelta(days=200)) & (s.index <= b0 + pd.Timedelta(days=370))]
    base = float(near.median()) if len(near) else 1.0
    s = (s / base).rolling(3, center=True, min_periods=2).median()
    s = s[s.index < b0]
    # só desvios grandes (follow-on, fusão, recompras relevantes); > 1,25 ou < 0,5 tende a ser artefato do LPA
    s = s.where(((s - 1).abs() > 0.15) & (s <= 1.25) & (s >= 0.5), 1.0)
    return s if len(s) else None


def stage_panel(sp, cache, tickers, fund, prices):
    sup = json.load(open(Path(sp) / "raw" / "b3" / "supplement.json"))
    det = json.load(open(Path(sp) / "raw" / "b3" / "details.json"))
    ibov = prices["ibov"]
    grid = month_grid(ibov)
    ib_d = ibov.pct_change()
    ib_m = pd.Series([ibov[ibov.index <= g].iloc[-1] for g in grid], index=grid)
    rows = []
    share_fix = {}
    for tk in tickers:
        px = prices["per"].get(tk)
        if px is None:
            continue
        f = fund.get(tk)
        iss = tk[:4]
        ic = (det.get(iss) or {}).get("industryClassification") or ""
        parts = [x.strip() for x in ic.split("/")]
        sector, subsector = (parts[0] if parts else None), (parts[1] if len(parts) > 1 else None)
        is_fin = bool((f or {}).get("ftype")) or subsector in FIN_SUBSECTORS or iss in FIN_EXTRA
        per_unit = cvm.UNITS.get(tk, 1)
        tr, adj, close, volu = px["tr"], px["adj"], px["close"], px["volume"]
        # retornos diários alinhados ao calendário do Ibovespa
        r_d = tr.pct_change().reindex(ib_d.index)
        both = r_d.notna() & ib_d.notna()
        x, y = r_d.where(both), ib_d.where(both)
        n504 = both.astype(float).rolling(504, min_periods=1).sum()
        sx, sy = x.fillna(0).rolling(504, min_periods=1).sum(), y.fillna(0).rolling(504, min_periods=1).sum()
        sxy, syy = (x * y).fillna(0).rolling(504, min_periods=1).sum(), (y * y).fillna(0).rolling(504, min_periods=1).sum()
        beta = ((sxy - sx * sy / n504) / (syy - sy * sy / n504)).where(n504 >= 250)
        vol = r_d.rolling(252, min_periods=180).std() * math.sqrt(252)
        dv = pd.Series(volu.values, index=volu.index).reindex(ib_d.index).fillna(0.0)
        adtv = dv.rolling(63, min_periods=20).mean()
        divs = pd.Series({d: v for d, v in px["divs"]}) if px["divs"] else pd.Series(dtype=float)
        if len(divs):
            divs = divs.groupby(level=0).sum().sort_index()
        plist = _period_index(f["periods"]) if f else []
        b3_total = fnum((sup.get(iss) or {}).get("totalNumberShares", "0")) or 0.0
        sh_hist = fix_share_scale(f["shares"], b3_total, px["events"]) if f else []
        impl = implied_share_ratio(f, sup.get(iss), px["events"], sh_hist, tr.index[0]) if f else None
        if impl is not None:
            share_fix[tk] = {d.strftime("%Y-%m-%d"): round(float(v), 3) for d, v in impl.items() if v != 1.0}
        tr_idx = tr.index
        for gi, g in enumerate(grid):
            pos = tr_idx.searchsorted(g, side="right") - 1
            if pos < 0:
                continue
            last_trade = tr_idx[pos]
            row = {"date": g, "ticker": tk, "issuer": iss, "sector": sector, "is_fin": is_fin,
                   "stale_days": int((g - last_trade).days), "tr": float(tr.iloc[pos]),
                   "adtv": float(adtv.get(g, np.nan)) if g in adtv.index else np.nan,
                   "vol_1y": float(vol.get(g, np.nan)) if g in vol.index else np.nan,
                   "beta_2y": float(beta.get(g, np.nan)) if g in beta.index else np.nan}
            close_t, adj_t = float(close.iloc[pos]), float(adj.iloc[pos])
            # dividendos 12m (data-com em (t-365, t]) / preço, na mesma base ajustada
            if len(divs):
                dd = divs[(divs.index > g - pd.Timedelta(days=365)) & (divs.index <= g)]
                row["dy"] = float(dd.sum() / adj_t) if adj_t > 0 else np.nan
            else:
                row["dy"] = 0.0 if (tr.index[0] <= g - pd.Timedelta(days=365)) else np.nan
            if tr.index[0] > g - pd.Timedelta(days=330):
                row["dy"] = np.nan  # histórico curto demais para DY 12m
            # fundamentos disponíveis em g
            fa = None
            for av, pe, dt in plist:
                if av <= g and f["periods"][dt]["ltm"] is not None:
                    fa = dt
            n_sh = shares_at(sh_hist, px["events"], g, impl) if f else None
            mcap = close_t * n_sh / per_unit / 1e6 if n_sh else np.nan
            row["mcap"] = mcap
            row["size"] = math.log(mcap) if finite(mcap) and mcap > 0 else np.nan
            if fa is not None and pd.Timestamp(fa) >= g - pd.Timedelta(days=550) and finite(mcap) and mcap > 0:
                p = f["periods"][fa]
                L, B = p["ltm"], p["bs"]
                p1 = _year_before(f["periods"], fa)
                L1 = (p1 or {}).get("ltm") or {}
                B1 = (p1 or {}).get("bs") or {}
                row["fund_period"] = fa
                ni, eq = L.get("ni_controlling"), B.get("equity_controlling")
                row["ep"] = ni / mcap if finite(ni) else np.nan
                row["bp"] = eq / mcap if finite(eq) else np.nan
                eq1 = B1.get("equity_controlling")
                eq_avg = (eq + eq1) / 2 if finite(eq) and finite(eq1) and eq1 > 0 else eq
                row["roe"] = ni / eq_avg if finite(ni) and finite(eq_avg) and eq_avg > 0 else np.nan
                # ROE médio 5 anos (exercícios publicados até g) para o bloco qualidade do painel
                fys = [(pe, dt) for av, pe, dt in plist if av <= g and f["periods"][dt]["kind"] == "dfp"][-5:]
                roes = []
                for pe, dt in fys:
                    q = f["periods"][dt]
                    q1 = _year_before(f["periods"], dt)
                    e0 = q["bs"].get("equity_controlling")
                    e1 = (q1 or {}).get("bs", {}).get("equity_controlling") if q1 else None
                    ea = (e0 + e1) / 2 if finite(e0) and finite(e1) and e1 > 0 else e0
                    n_ = q["ytd"].get("ni_controlling")
                    if finite(n_) and finite(ea) and ea > 0:
                        roes.append(n_ / ea)
                row["roe_5y"] = float(np.mean(roes)) if len(roes) >= 3 else np.nan
                if not is_fin:
                    nd, mino, eb = B.get("net_debt"), B.get("minority") or 0.0, L.get("ebitda")
                    ev = mcap + nd + (mino if finite(mino) else 0.0) if finite(nd) else np.nan
                    row["ebitda_ev"] = eb / ev if finite(eb) and finite(ev) and ev > 0 else np.nan
                    if finite(nd) and finite(eb):
                        row["nd_ebitda"] = nd / eb if eb > 0 else (99.0 if nd > 0 else np.nan)
                    ebit, eqt = L.get("ebit"), B.get("equity")
                    icap = eqt + nd if finite(eqt) and finite(nd) else np.nan
                    row["roic"] = ebit * (1 - 0.34) / icap if finite(ebit) and finite(icap) and icap > 0 else np.nan
                    gp, rev = L.get("gross_profit"), L.get("revenue")
                    row["gross_margin"] = gp / rev if finite(gp) and finite(rev) and rev > 0 else np.nan
                    ta = B.get("total_assets")
                    if finite(ta) and ta > 0:
                        ca, cl = B.get("current_assets") or 0.0, B.get("current_liab") or 0.0
                        re_ = B.get("retained") or 0.0
                        eqv = eqt if finite(eqt) else 0.0
                        tl = ta - eqv
                        x1, x2 = (ca - cl) / ta, re_ / ta
                        x3 = (ebit if finite(ebit) else 0.0) / ta
                        x4 = eqv / tl if tl > 0 else 0.0
                        row["altman"] = 3.25 + 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4
                    ta1 = B1.get("total_assets")
                    ni1 = L1.get("ni_controlling")
                    if finite(ta) and ta > 0 and finite(ta1) and ta1 > 0 and finite(ni) and finite(ni1):
                        cfo = L.get("cfo") or 0.0
                        roa, roa1 = ni / ta, ni1 / ta1
                        sig = [roa > 0, cfo > 0, roa > roa1, cfo / ta > roa,
                               (B.get("lt_debt") or 0.0) / ta <= (B1.get("lt_debt") or 0.0) / ta1,
                               (B.get("current_assets") or 0.0) / (B.get("current_liab") or 1.0) > (B1.get("current_assets") or 0.0) / (B1.get("current_liab") or 1.0)]
                        d0, d1 = pd.Timestamp(fa), pd.Timestamp(p1_date(fa))
                        n0 = shares_at(sh_hist, px["events"], d0, impl)
                        n1 = shares_at(sh_hist, px["events"], d1, impl)
                        mult_between = 1.0
                        for dcom, mult in px["events"]:
                            if d1 <= dcom < d0:
                                mult_between *= mult
                        sig.append(bool(n0 <= n1 * mult_between * 1.01) if n0 and n1 else True)
                        gm = (L.get("gross_profit") or 0.0) / (L.get("revenue") or 1.0)
                        gm1 = (L1.get("gross_profit") or 0.0) / (L1.get("revenue") or 1.0)
                        sig.append(gm > gm1)
                        sig.append((L.get("revenue") or 0.0) / ta > (L1.get("revenue") or 0.0) / ta1)
                        row["piotroski"] = float(sum(bool(s_) for s_ in sig))
            # preço: momentum 12-1, retorno do mês (sobrerreação) e retornos futuros
            def tr_at(k):
                j = gi + k
                if j < 0 or j >= len(grid):
                    return np.nan
                pp = tr_idx.searchsorted(grid[j], side="right") - 1
                if pp < 0 or (grid[j] - tr_idx[pp]).days > 10:
                    return np.nan
                return float(tr.iloc[pp])
            t0 = row["tr"] if row["stale_days"] <= 10 else np.nan
            row["mom_12_1"] = tr_at(-1) / tr_at(-12) - 1
            row["ret_1m_past"] = t0 / tr_at(-1) - 1
            row["ibov_1m_past"] = float(ib_m.iloc[gi] / ib_m.iloc[gi - 1] - 1) if gi >= 1 else np.nan
            for h in HORIZONS:
                j = gi + h
                if j < len(grid):
                    pp = tr_idx.searchsorted(grid[j], side="right") - 1
                    row[f"fwd_{h}m"] = float(tr.iloc[pp]) / t0 - 1 if pp >= 0 and pp > pos - 1 else np.nan
                else:
                    row[f"fwd_{h}m"] = np.nan
            rows.append(row)
    panel = pd.DataFrame(rows)
    ibm = pd.DataFrame({"date": grid, "ibov": ib_m.values})
    for h in HORIZONS:
        ibm[f"ibov_fwd_{h}m"] = ib_m.shift(-h).values / ib_m.values - 1
    ibm["ibov_3m_past"] = ib_m.values / ib_m.shift(3).values - 1
    out = {"panel": panel, "ibov_m": ibm, "share_fix": share_fix}
    pd.to_pickle(out, Path(cache) / "panel.pkl")
    log("painel: linhas", len(panel), "| tickers", panel.ticker.nunique(), "| correções de ações (LPA)", len(share_fix))
    return out


def p1_date(dt):
    return (pd.Timestamp(dt) - pd.DateOffset(years=1)).strftime("%Y-%m-%d")


# =====================================================================================================================
# 4) Análise: IC, quintis, decaimento, compostos, otimização fora da amostra, crise, bootstrap
# =====================================================================================================================
PANEL_W = {"valor": 0.30, "upside": 0.10, "qualidade": 0.20, "solidez": 0.15, "sobrerreacao": 0.10, "probabilidade": 0.15}
BLOCKS = {"valor": ["ep", "bp", "ebitda_ev", "dy"], "qualidade": ["roe", "roic", "gross_margin", "piotroski"],
          "solidez": ["altman", "nd_ebitda"], "momentum": ["mom_12_1"], "baixo_risco": ["vol_1y", "beta_2y"], "tamanho": ["size"]}
EXTRA_BLOCKS = ["upside_hist", "reversao_1m"]


def winsor_z(s, lo=0.025, hi=0.975):
    """z-score transversal com winsorização 2,5/97,5% e corte em ±3 (como o zscore do painel, robusto a outliers)."""
    x = s.astype(float)
    if x.notna().sum() < 5:
        return x * np.nan
    a, b = x.quantile(lo), x.quantile(hi)
    x = x.clip(a, b)
    sd = x.std(ddof=0)
    if not sd or not np.isfinite(sd):
        return x * 0.0
    return ((x - x.mean()) / sd).clip(-3, 3)


def nw_t(x, lags):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 8:
        return np.nan
    e = x - x.mean()
    s = e @ e / n
    for l in range(1, min(lags, n - 1) + 1):
        s += 2 * (1 - l / (lags + 1)) * (e[l:] @ e[:-l]) / n
    return float(x.mean() / math.sqrt(s / n)) if s > 0 else np.nan


def ic_series(df, col, ret, min_n=20):
    out = {}
    for d, g in df[["date", col, ret]].dropna().groupby("date"):
        if len(g) >= min_n and g[col].nunique() > 2:
            out[d] = float(g[col].rank().corr(g[ret].rank()))
    return pd.Series(out, dtype=float).sort_index()


def ic_stats(s, h):
    s = s.dropna()
    if len(s) < 8:
        return None
    return {"n_meses": int(len(s)), "ic_medio": float(s.mean()), "ic_dp": float(s.std()), "ic_ir": float(s.mean() / s.std()) if s.std() > 0 else None,
            "t_nw": nw_t(s.values, h + 2), "pct_positivo": float((s > 0).mean())}


def quintile_returns(df, col, ret="fwd_1m", q=5, min_n=20):
    rows = {}
    for d, g in df[["date", col, ret]].dropna().groupby("date"):
        if len(g) < min_n or g[col].nunique() < q:
            continue
        b = pd.qcut(g[col].rank(method="first"), q, labels=False) + 1
        rows[d] = g.groupby(b)[ret].mean()
    return pd.DataFrame(rows).T.sort_index()


def perf(r, rf=None, periods=12):
    """Métricas de uma série mensal de retornos (decimal)."""
    r = r.dropna()
    if len(r) < 6:
        return None
    eq = (1 + r).cumprod()
    dd = float((eq / eq.cummax() - 1).min())
    ann = float(eq.iloc[-1] ** (periods / len(r)) - 1)
    vol = float(r.std() * math.sqrt(periods))
    ex = r - (rf.reindex(r.index).fillna(0.0) if rf is not None else 0.0)
    sharpe = float(ex.mean() / ex.std() * math.sqrt(periods)) if ex.std() > 0 else None
    return {"n_meses": int(len(r)), "retorno_anual": ann, "media_mensal": float(r.mean()), "vol_anual": vol, "sharpe": sharpe,
            "max_drawdown": dd, "pct_meses_positivos": float((r > 0).mean())}


def max_icir_weights(icmat, shrink=0.5, few=False):
    """w >= 0, soma 1, maximizando IC médio / dp do IC do composto (Σ dos ICs encolhida para a diagonal)."""
    from scipy.optimize import minimize
    m = icmat.dropna()
    if len(m) < 12:
        return None
    mu = m.mean().values
    S = m.cov().values
    S = shrink * np.diag(np.diag(S)) + (1 - shrink) * S
    k = len(mu)
    def neg(w):  # noqa: E306
        v = w @ S @ w
        return -(w @ mu) / math.sqrt(v) if v > 0 else 0.0
    best = None
    mu_pos = np.clip(mu, 1e-6, None)
    starts = [np.ones(k) / k, mu_pos / mu_pos.sum()] + ([] if few else [np.eye(k)[i] * 0.7 + 0.3 / k for i in range(k)])
    for x0 in starts:
        res = minimize(neg, x0, method="SLSQP", bounds=[(0, 1)] * k, constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}],
                       options={"maxiter": 500, "ftol": 1e-10})
        if res.success and (best is None or res.fun < best.fun):
            best = res
    if best is None:
        return None
    w = np.clip(best.x, 0, None)
    w[w < 1e-4] = 0
    return pd.Series(w / w.sum(), index=m.columns)


def composite(df, weights, cols):
    """Média ponderada dos z disponíveis, renormalizando os pesos por ação (como o escore do painel)."""
    W = pd.Series(weights, dtype=float).reindex(cols).fillna(0.0)
    Z = df[cols]
    num = (Z * W).sum(axis=1, min_count=1)
    den = (Z.notna() * W).sum(axis=1)
    out = num / den.replace(0, np.nan)
    out[den < 0.5 * W.sum()] = np.nan  # exige ao menos metade do peso disponível
    return out


REC_CANDIDATES = [f for f in FACTORS if f != "size"]  # tamanho fora: é o fator mais contaminado pelo viés de sobrevivência


def rec_weights(Ms, idx=None):
    """Regra recomendada: peso ∝ max(0, IC-IR médio nos horizontes 1/3/12m). Contínua (sem corte duro), sem inverter a
    covariância dos ICs; fora da amostra, regras simples assim generalizaram tão bem ou melhor que o máximo IC-IR."""
    sub = {h: (M.dropna() if idx is None else M.iloc[idx].dropna()) for h, M in Ms.items()}
    cols = list(next(iter(sub.values())).columns)
    icir = pd.Series(0.0, index=cols)
    for h, M in sub.items():
        icir += (M.mean() / M.std().replace(0, np.nan)).fillna(0) / len(sub)
    w = icir.clip(lower=0)
    return w / w.sum() if w.sum() > 0 else None


def block_bootstrap_idx(n, block, rng):
    idx = []
    while len(idx) < n:
        s = rng.integers(0, n)
        idx.extend(range(s, min(s + block, n)))
    return np.array(idx[:n])


def stage_analysis(sp, cache, panel_out, prices):
    pn = panel_out["panel"].copy()
    ibm = panel_out["ibov_m"].set_index("date")
    cdi = prices.get("cdi")
    # --------------------------------------------------------------- blocos derivados por ticker (histórico próprio)
    pn = pn.sort_values(["ticker", "date"])
    ups = []
    for m in ("ep", "bp", "ebitda_ev"):
        pos = pn[m].where(pn[m] > 0)
        med = pos.groupby(pn.ticker).transform(lambda x: x.shift(1).rolling(60, min_periods=24).median())
        ups.append((pn[m] / med - 1).where((pn[m] > 0) & (med > 0)))
    pn["upside_hist"] = pd.concat(ups, axis=1).mean(axis=1)
    pn["reversao_1m"] = -(pn["ret_1m_past"] - pn["beta_2y"].fillna(1.0) * pn["ibov_1m_past"])
    pn["prob_proxy"] = np.log1p(pn["upside_hist"].clip(lower=-0.95)) / pn["vol_1y"]
    pn["quality_panel"] = pn["roe_5y"] + (pn["piotroski"].fillna(4.5) - 4.5) / 9
    pn["solidez_panel"] = (-(pn["nd_ebitda"].fillna(2.5)) + pn["altman"].fillna(5.0) / 3).where(~pn["is_fin"])
    # --------------------------------------------------------------- universo point-in-time
    u = pn[(pn.adtv >= ADTV_MIN) & (pn.stale_days <= 7) & (pn.date >= PANEL_START) & (pn.date <= PANEL_END)].copy()
    u = u.sort_values("adtv").drop_duplicates(["date", "issuer"], keep="last").sort_values(["date", "ticker"])
    for f in FACTORS:
        u["o_" + f] = SIGN[f] * u[f]
        u["z_" + f] = u.groupby("date")["o_" + f].transform(winsor_z)
    for b, fs in BLOCKS.items():
        u["b_" + b] = u[["z_" + f for f in fs]].mean(axis=1)
        u["zb_" + b] = u.groupby("date")["b_" + b].transform(winsor_z)
    for b in EXTRA_BLOCKS:
        u["zb_" + b] = u.groupby("date")[b].transform(winsor_z)
    # blocos do painel (proxies documentadas)
    u["p_valor"] = u[["z_ep", "z_ebitda_ev", "z_dy"]].mean(axis=1)
    pan = {"valor": "p_valor", "upside": "upside_hist", "qualidade": "quality_panel", "solidez": "solidez_panel",
           "sobrerreacao": "reversao_1m", "probabilidade": "prob_proxy"}
    for k, c in pan.items():
        u["zp_" + k] = u.groupby("date")[c].transform(winsor_z)
    months = sorted(u.date.unique())
    crisis = set(ibm.index[ibm["ibov_3m_past"] <= -0.10])  # formação após Ibovespa <= -10% em 3 meses
    log("análise: meses", len(months), "| nomes/mês", round(u.groupby("date").size().mean(), 1))
    is_mask = lambda d, h: (d + pd.DateOffset(months=h)) <= IS_END + pd.Timedelta(days=5)
    oos_mask = lambda d: d >= OOS_START
    # --------------------------------------------------------------- IC por fator × horizonte
    res = {"factors": {}, "ic_monthly": {}, "quintiles": {}, "decay": {}}
    ic_1m = {}
    for f in FACTORS + ["upside_hist", "reversao_1m", "prob_proxy"]:
        col = "o_" + f if f in FACTORS else f
        lab = LABEL.get(f, {"upside_hist": "Upside p/ múltiplo histórico (proxy)", "reversao_1m": "Reversão 1m residual (proxy sobrerreação)",
                            "prob_proxy": "ln(1+upside hist)/vol (proxy probabilidade)"}.get(f))
        entry = {"label": lab, "grupo": GROUP.get(f, "proxy painel"), "sinal_esperado": SIGN.get(f, 1),
                 "cobertura_media": float(u.groupby("date")[col].apply(lambda x: x.notna().mean()).mean()), "horizontes": {}}
        for h in HORIZONS:
            s = ic_series(u, col, f"fwd_{h}m")
            st = ic_stats(s, h)
            if st is None:
                continue
            s_is = s[[is_mask(d, h) for d in s.index]]
            s_oos = s[[oos_mask(d) for d in s.index]]
            st["in_sample_2017_2022"] = ic_stats(s_is, h)
            st["fora_amostra_2023_2026"] = ic_stats(s_oos, h)
            st["crise"] = ic_stats(s[[d in crisis for d in s.index]], h)
            st["normal"] = ic_stats(s[[d not in crisis for d in s.index]], h)
            entry["horizontes"][f"{h}m"] = st
            res["ic_monthly"].setdefault(f, {})[f"{h}m"] = {d.strftime("%Y-%m"): round(v, 4) for d, v in s.items()}
            if h == 1:
                ic_1m[f] = s
        qr = quintile_returns(u, col, "fwd_1m")
        if len(qr):
            sp_ = qr[5] - qr[1]
            entry["quintis_1m"] = {"retorno_medio_mensal_por_quintil": {str(int(k)): float(v) for k, v in qr.mean().items()},
                                   "spread_q5_q1": {"anual": float(sp_.mean() * 12), "vol_anual": float(sp_.std() * math.sqrt(12)),
                                                    "sharpe": float(sp_.mean() / sp_.std() * math.sqrt(12)) if sp_.std() > 0 else None,
                                                    "t_nw": nw_t(sp_.values, 3), "pct_meses_positivos": float((sp_ > 0).mean()),
                                                    "max_drawdown": perf(sp_)["max_drawdown"] if perf(sp_) else None},
                                   "monotonia_spearman": float(pd.Series(qr.mean().values).corr(pd.Series(range(1, 6)), method="spearman"))}
            for h in (3, 6, 12):
                qh = quintile_returns(u, col, f"fwd_{h}m")
                if len(qh):
                    sh = qh[5] - qh[1]
                    entry["quintis_1m"][f"spread_q5_q1_{h}m"] = {"anualizado": float(sh.mean() * 12 / h), "t_nw": nw_t(sh.values, h + 2)}
            res["quintiles"][f] = {d.strftime("%Y-%m"): round(float(v), 5) for d, v in sp_.items()}
        res["factors"][f] = entry
    # --------------------------------------------------------------- decaimento: IC do fator em t com retorno do mês t+k
    R = pn.pivot_table(index="date", columns="ticker", values="fwd_1m")
    for f in FACTORS + ["upside_hist", "reversao_1m"]:
        col = "o_" + f if f in FACTORS else f
        Fm = u.pivot_table(index="date", columns="ticker", values=col)
        dec = []
        for k in range(0, 12):
            Rk = R.shift(-k).reindex(index=Fm.index, columns=Fm.columns)
            ics = []
            for d in Fm.index:
                x, y = Fm.loc[d], Rk.loc[d]
                ok = x.notna() & y.notna()
                if ok.sum() >= 20:
                    ics.append(x[ok].rank().corr(y[ok].rank()))
            dec.append({"defasagem_meses": k, "ic_medio": float(np.nanmean(ics)) if ics else None,
                        "t": float(np.nanmean(ics) / (np.nanstd(ics) / math.sqrt(len(ics)))) if len(ics) > 8 else None})
        res["decay"][f] = dec
    log("análise: ICs e decaimento ok")
    # --------------------------------------------------------------- compostos
    zf = ["z_" + f for f in FACTORS]
    zb = ["zb_" + b for b in BLOCKS]
    zbx = zb + ["zb_" + b for b in EXTRA_BLOCKS]
    u["c_painel_proxy"] = composite(u, {"zp_" + k: w for k, w in PANEL_W.items()}, ["zp_" + k for k in PANEL_W])
    ren = {k: PANEL_W[k] for k in ("valor", "upside", "qualidade", "solidez")}
    u["c_painel_renorm"] = composite(u, {"zp_" + k: w for k, w in ren.items()}, ["zp_" + k for k in ren])
    u["c_iguais_fatores"] = composite(u, {c: 1.0 for c in zf}, zf)
    u["c_iguais_blocos"] = composite(u, {c: 1.0 for c in zb}, zb)
    # IC mensal (1m) de cada fator/bloco para a otimização
    def icmat(cols, h=1, mask=None):
        m = {}
        for c in cols:
            s = ic_series(u, c, f"fwd_{h}m")
            m[c] = s
        M = pd.DataFrame(m).sort_index()
        if mask is not None:
            M = M[[mask(d) for d in M.index]]
        return M
    is1 = lambda d: is_mask(d, 1)
    M_f_is = icmat(zf, 1, is1)
    M_b_is = icmat(zb, 1, is1)
    M_bx_is = icmat(zbx, 1, is1)
    w_f = max_icir_weights(M_f_is)
    w_b = max_icir_weights(M_b_is)
    w_bx = max_icir_weights(M_bx_is)
    icir_is = (M_f_is.mean() / M_f_is.std()).clip(lower=0)
    w_simple = icir_is / icir_is.sum() if icir_is.sum() > 0 else None
    u["c_otim_fatores"] = composite(u, w_f.to_dict(), zf) if w_f is not None else np.nan
    u["c_otim_blocos"] = composite(u, w_b.to_dict(), zb) if w_b is not None else np.nan
    u["c_otim_blocos_proxies"] = composite(u, w_bx.to_dict(), zbx) if w_bx is not None else np.nan
    u["c_icir_simples"] = composite(u, w_simple.to_dict(), zf) if w_simple is not None else np.nan
    # regra recomendada: média dos pesos de máx. IC-IR (blocos) nos horizontes 1, 3 e 12 meses, estimada em 2017–2022
    zrec = ["z_" + f for f in REC_CANDIDATES]
    Ms_is = {h: icmat(zrec, h, lambda d, h=h: is_mask(d, h)) for h in (1, 3, 12)}
    w_rec_is = rec_weights(Ms_is)
    u["c_recomendado_regra"] = composite(u, w_rec_is.to_dict(), zrec) if w_rec_is is not None else np.nan
    # regime de crise: meses de formação com Ibovespa <= -10% nos 3 meses anteriores
    u["crise"] = u.date.isin(crisis)
    crisis_months = sorted(d for d in months if d in crisis)
    # pesos de crise: IC-IR em meses de crise (amostra inteira; poucos meses -> só referência) com horizonte 3m
    M_b_cr = icmat(zb, 3, lambda d: d in crisis)
    w_cr = max_icir_weights(M_b_cr, shrink=0.8) if len(M_b_cr.dropna()) >= 6 else None
    if w_cr is None and len(M_b_cr.dropna()):
        mu = M_b_cr.mean().clip(lower=0)
        w_cr = mu / mu.sum() if mu.sum() > 0 else None
    u["c_crise_blocos"] = composite(u, w_cr.to_dict(), zb) if w_cr is not None else np.nan
    comps = ["c_painel_proxy", "c_painel_renorm", "c_iguais_fatores", "c_iguais_blocos", "c_icir_simples", "c_otim_fatores",
             "c_otim_blocos", "c_otim_blocos_proxies", "c_recomendado_regra", "c_crise_blocos"]
    comp_label = {"c_painel_proxy": "Pesos atuais do painel (proxies p/ upside, sobrerreação, probabilidade)",
                  "c_painel_renorm": "Pesos atuais do painel renormalizados (valor, upside, qualidade, solidez)",
                  "c_iguais_fatores": "Pesos iguais (14 fatores)", "c_iguais_blocos": "Pesos iguais (6 blocos)",
                  "c_icir_simples": "Pesos ∝ IC-IR 1m positivo (2017–2022)",
                  "c_otim_fatores": "Máx. IC-IR, 14 fatores (2017–2022)", "c_otim_blocos": "Máx. IC-IR, 6 blocos (2017–2022)",
                  "c_otim_blocos_proxies": "Máx. IC-IR, 6 blocos + upside hist. + reversão 1m (2017–2022)",
                  "c_recomendado_regra": "Regra recomendada (peso ∝ IC-IR positivo médio 1/3/12m, 13 fatores, sem tamanho), estimada em 2017–2022",
                  "c_crise_blocos": "Pesos de crise (IC-IR 3m nos meses de crise, amostra inteira — referência)"}
    ew = u.groupby("date")["fwd_1m"].mean()
    ibov_1m = ibm["ibov_fwd_1m"]
    rf = cdi
    periods = {"in_sample_2017_2022": lambda d: d < OOS_START, "fora_amostra_2023_2026": oos_mask,
               "completo": lambda d: True, "crise": lambda d: d in crisis}
    res["composites"] = {}
    res["composite_series"] = {}
    for c in comps:
        e = {"descricao": comp_label[c], "ic": {}, "carteiras": {}}
        for h in HORIZONS:
            s = ic_series(u, c, f"fwd_{h}m")
            e["ic"][f"{h}m"] = {k: ic_stats(s[[fn(d) and (k != "in_sample_2017_2022" or is_mask(d, h)) for d in s.index]], h)
                               for k, fn in periods.items()}
        qr = quintile_returns(u, c, "fwd_1m")
        if not len(qr):
            continue
        q5, q1 = qr[5], qr[1]
        ls = q5 - q1
        exc = q5 - ew.reindex(q5.index)
        for k, fn in periods.items():
            idx = [d for d in q5.index if fn(d)]
            if not idx:
                continue
            e["carteiras"][k] = {"top_quintil": perf(q5.loc[idx], rf), "long_short_q5_q1": perf(ls.loc[idx]),
                                 "excesso_vs_universo_ew": {"media_anual": float(exc.loc[idx].mean() * 12),
                                                           "t_nw": nw_t(exc.loc[idx].values, 3),
                                                           "pct_meses_acima": float((exc.loc[idx] > 0).mean())},
                                 "universo_ew": perf(ew.reindex(idx), rf), "ibov": perf(ibov_1m.reindex(idx), rf)}
        # giro mensal do top quintil
        tops = {}
        for d, g in u[["date", "ticker", c]].dropna().groupby("date"):
            if len(g) >= 20:
                tops[d] = set(g.nlargest(max(1, len(g) // 5), c).ticker)
        ds = sorted(tops)
        e["giro_mensal_top_quintil"] = float(np.mean([1 - len(tops[a] & tops[b]) / max(1, len(tops[b])) for a, b in zip(ds[:-1], ds[1:])])) if len(ds) > 1 else None
        res["composites"][c] = e
        res["composite_series"][c] = {"q5": {d.strftime("%Y-%m"): round(float(v), 5) for d, v in q5.items()},
                                      "q1": {d.strftime("%Y-%m"): round(float(v), 5) for d, v in q1.items()}}
    res["composite_series"]["universo_ew"] = {d.strftime("%Y-%m"): round(float(v), 5) for d, v in ew.items()}
    res["composite_series"]["ibov"] = {d.strftime("%Y-%m"): round(float(v), 5) for d, v in ibov_1m.reindex(months).items() if np.isfinite(v)}
    res["weights"] = {"otim_fatores_2017_2022": w_f.round(4).to_dict() if w_f is not None else None,
                      "otim_blocos_2017_2022": w_b.round(4).to_dict() if w_b is not None else None,
                      "otim_blocos_proxies_2017_2022": w_bx.round(4).to_dict() if w_bx is not None else None,
                      "icir_simples_2017_2022": w_simple.round(4).to_dict() if w_simple is not None else None,
                      "crise_blocos": w_cr.round(4).to_dict() if w_cr is not None else None,
                      "recomendado_regra_2017_2022": w_rec_is.round(4).to_dict() if w_rec_is is not None else None}
    log("análise: compostos ok")
    # --------------------------------------------------------------- bootstrap dos pesos (amostra inteira, blocos de 6 meses)
    rng = np.random.default_rng(20261026)
    M_b_all = icmat(zb, 1).dropna()
    M_bx_all = icmat(zbx, 1).dropna()
    M_f_all = icmat(zf, 1).dropna()
    boot = {}
    for name, M in (("blocos", M_b_all), ("blocos_proxies", M_bx_all), ("fatores", M_f_all)):
        point = max_icir_weights(M)
        draws = []
        for _ in range(200):
            ii = block_bootstrap_idx(len(M), 6, rng)
            w = max_icir_weights(M.iloc[ii].reset_index(drop=True))
            if w is not None:
                draws.append(w)
        D = pd.DataFrame(draws)
        boot[name] = {"ponto_amostra_inteira": point.round(4).to_dict() if point is not None else None,
                      "mediana": D.median().round(4).to_dict(), "p05": D.quantile(0.05).round(4).to_dict(),
                      "p95": D.quantile(0.95).round(4).to_dict(), "prob_peso_positivo": (D > 0.01).mean().round(3).to_dict(), "n_boot": int(len(D))}
        if name == "fatores":
            G = pd.DataFrame({g: D[[c for c in D.columns if GROUP.get(c[2:]) == g.replace("_", " ")]].sum(axis=1)
                              for g in ("valor", "qualidade", "solidez", "momentum", "baixo_risco", "tamanho")})
            boot[name]["por_grupo"] = {"mediana": G.median().round(4).to_dict(), "p05": G.quantile(0.05).round(4).to_dict(),
                                       "p95": G.quantile(0.95).round(4).to_dict()}
    Ms_all = {h: icmat(zrec, h) for h in (1, 3, 12)}
    common = sorted(set.intersection(*[set(M.dropna().index) for M in Ms_all.values()]))
    Ms_all = {h: M.loc[common] for h, M in Ms_all.items()}
    point = rec_weights(Ms_all)
    draws = []
    for _ in range(1000):
        ii = block_bootstrap_idx(len(common), 12, rng)
        w = rec_weights(Ms_all, ii)
        if w is not None:
            draws.append(w)
    D = pd.DataFrame(draws).fillna(0.0)
    grp = lambda X: pd.DataFrame({g: X[[c for c in X.columns if GROUP.get(c[2:]) == g]].sum(axis=1)
                                  for g in ("valor", "qualidade", "solidez", "momentum", "baixo risco")})
    G, Gp = grp(D), grp(point.to_frame().T)
    boot["recomendado_regra"] = {"ponto_amostra_inteira": point.round(4).to_dict(), "mediana": D.median().round(4).to_dict(),
                                 "p05": D.quantile(0.05).round(4).to_dict(), "p95": D.quantile(0.95).round(4).to_dict(),
                                 "prob_peso_positivo": (D > 0.01).mean().round(3).to_dict(), "n_boot": int(len(D)),
                                 "meses": len(common), "bloco_bootstrap_meses": 12,
                                 "candidatos": REC_CANDIDATES,
                                 "por_grupo": {"ponto": Gp.iloc[0].round(4).to_dict(), "mediana": G.median().round(4).to_dict(),
                                               "p05": G.quantile(0.05).round(4).to_dict(), "p95": G.quantile(0.95).round(4).to_dict(),
                                               "prob_peso_positivo": (G > 0.01).mean().round(3).to_dict()}}
    res["bootstrap"] = boot
    # composto recomendado: pesos de blocos (amostra inteira) arredondados; IC-IR fora da amostra dos pesos 2017–2022
    res["ic_bloco_amostra_inteira"] = {c[3:]: ic_stats(icmat([c], 1)[c], 1) for c in zbx}
    res["meta"] = {"meses": len(months), "primeiro_mes": months[0].strftime("%Y-%m"), "ultimo_mes": months[-1].strftime("%Y-%m"),
                   "nomes_por_mes": {"media": float(u.groupby("date").size().mean()), "min": int(u.groupby("date").size().min()),
                                     "max": int(u.groupby("date").size().max())},
                   "nomes_por_ano": {str(k): float(v) for k, v in (u.groupby(u.date.dt.year).size() / u.groupby(u.date.dt.year).date.nunique()).items()},
                   "meses_crise": [d.strftime("%Y-%m") for d in crisis_months],
                   "ultimo_retorno_parcial": "o mês 2026-10 vai até 23/10/2026 (último pregão no COTAHIST)"}
    res["_u"] = u  # (removido antes de gravar)
    return res


# =====================================================================================================================
# 5) Saídas
# =====================================================================================================================
def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else round(float(o), 6)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, pd.Timestamp):
        return o.strftime("%Y-%m-%d")
    return o


def _g(d, *ks):
    for k in ks:
        if d is None:
            return None
        d = d.get(k) if isinstance(d, dict) else None
    return d


def _p(x, d=1, sign=False):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{x * 100:+.{d}f}%" if sign else f"{x * 100:.{d}f}%"


def _n(x, d=3, sign=False):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{x:+.{d}f}" if sign else f"{x:.{d}f}"


BLOCK_LABEL = {"valor": "Valor (E/P, B/P, EBITDA/EV, DY)", "qualidade": "Qualidade (ROE, ROIC, margem bruta, Piotroski)",
               "solidez": "Solidez (Altman Z″, dív. líq./EBITDA)", "momentum": "Momentum 12-1", "baixo_risco": "Baixo risco (vol 1a, beta 2a)",
               "tamanho": "Tamanho (small caps)", "upside_hist": "Upside p/ múltiplo histórico (proxy de upside)",
               "reversao_1m": "Reversão residual 1m (proxy de sobrerreação)"}


def render_md(res):
    F, C, B, M = res["factors"], res["composites"], res["bootstrap"], res["meta"]
    L = []
    w = L.append
    rec = B["recomendado_regra"]
    blocks = list(BLOCKS)
    def fic(f, h, k=None):
        e = _g(F, f, "horizontes", f"{h}m")
        return _g(e, k) if k else e
    n_oos = _g(C, "c_iguais_blocos", "carteiras", "fora_amostra_2023_2026", "top_quintil", "n_meses") or 0
    cm = [pd.Period(x, "M") for x in M["meses_crise"]]
    n_ep = sum(1 for i, x in enumerate(cm) if i == 0 or (x - cm[i - 1]).n > 2)
    ep_txt = {1: "um episódio", 2: "dois episódios", 3: "três episódios", 4: "quatro episódios"}.get(n_ep, f"{n_ep} episódios")
    nmin, nmax = M["nomes_por_mes"]["min"], M["nomes_por_mes"]["max"]
    fixes = sorted(k for k, v in (M.get("correcoes_acoes_por_lpa") or {}).items() if v)
    # --------------------------------------------------------------------------- cabeçalho e conclusões
    w("# Backtest de fatores — ações brasileiras, painel mensal point-in-time 2017-01 a 2026-09")
    w("")
    w(f"Gerado por `pipeline/tests/factor_backtest.py` em {M.get('gerado_em', '')}. Dados completos (ICs mensais, spreads, séries dos "
      f"compostos, bootstrap) em `data/tests/factor_backtest.json`. {M['meses']} meses de formação ({M['primeiro_mes']} a {M['ultimo_mes']}), "
      f"média de {M['nomes_por_mes']['media']:.0f} ações por mês (mín. {M['nomes_por_mes']['min']}, máx. {M['nomes_por_mes']['max']}). "
      "IC = correlação de Spearman entre o fator (orientado no sinal esperado) e o retorno total futuro; t com erros de Newey-West "
      "(defasagens = horizonte + 2).")
    w("")
    w("## Conclusões")
    w("")
    strong, weak, null = [], [], []
    for f in FACTORS:
        ts = [fic(f, h, "t_nw") for h in HORIZONS]
        ics = [fic(f, h, "ic_medio") for h in HORIZONS]
        oos12 = _g(fic(f, 12), "fora_amostra_2023_2026", "ic_medio")
        is12 = _g(fic(f, 12), "in_sample_2017_2022", "ic_medio")
        best_t = max([t for t in ts if t is not None] or [0])
        if best_t >= 2 and (oos12 or 0) > 0 and (is12 or 0) > 0:
            strong.append(f)
        elif sum(1 for x in ics if (x or 0) > 0) >= 3 and best_t >= 1.0:
            weak.append(f)
        else:
            null.append(f)
    def lst(fs, h=12):
        return "; ".join(f"{LABEL[f]} (IC {h}m {_n(fic(f, h, 'ic_medio'))}, t {_n(fic(f, h, 't_nw'), 2)})" for f in fs) or "nenhum"
    w(f"1. **Funcionaram (t ≥ 2 em algum horizonte e IC 12m positivo dentro e fora da amostra):** {lst(strong)}. "
      "O sinal mais robusto é **valor**: barato por lucro, patrimônio e EBITDA paga em todos os horizontes, cresce com o horizonte e "
      "se mantém em 2023–2026.")
    w(f"2. **Positivos mas fracos (IC > 0 em 3+ horizontes e t entre 1 e 2):** {lst(weak, 1)}.")
    w(f"3. **Sem efeito ou contrários:** {lst(null, 1)}.")
    up, rv = F.get("upside_hist", {}), F.get("reversao_1m", {})
    w(f"4. **Proxies dos blocos sem histórico do painel não funcionaram em meses normais.** Upside até o múltiplo histórico da própria "
      f"ação: IC 1m {_n(_g(up, 'horizontes', '1m', 'ic_medio'))} (t {_n(_g(up, 'horizontes', '1m', 't_nw'), 2)}), 6m "
      f"{_n(_g(up, 'horizontes', '6m', 'ic_medio'))} (t {_n(_g(up, 'horizontes', '6m', 't_nw'), 2)}): ações baratas contra o próprio "
      f"passado continuam caindo. Sobrerreação (comprar quem caiu mais que o beta prevê no mês): IC 1m "
      f"{_n(_g(rv, 'horizontes', '1m', 'ic_medio'))} (t {_n(_g(rv, 'horizontes', '1m', 't_nw'), 2)}), 12m "
      f"{_n(_g(rv, 'horizontes', '12m', 'ic_medio'))} (t {_n(_g(rv, 'horizontes', '12m', 't_nw'), 2)}). O retorno residual "
      f"tem continuação, não reversão. Só nos meses de crise o sinal vira: IC 1m {_n(_g(rv, 'horizontes', '1m', 'crise', 'ic_medio'))} "
      f"em {_g(rv, 'horizontes', '1m', 'crise', 'n_meses')} meses, amostra pequena demais para concluir.")
    cr = C.get("c_painel_renorm", {}).get("carteiras", {})
    co = C.get("c_otim_blocos", {}).get("carteiras", {})
    ci = C.get("c_iguais_blocos", {}).get("carteiras", {})
    crr = C.get("c_recomendado_regra", {}).get("carteiras", {})
    w(f"5. **Fora da amostra, pesos otimizados não batem regras simples.** O máximo IC-IR estimado em 2017–2022 (blocos) teve excesso "
      f"sobre o universo de {_p(_g(co, 'in_sample_2017_2022', 'excesso_vs_universo_ew', 'media_anual'), sign=True)} a.a. dentro da amostra e "
      f"{_p(_g(co, 'fora_amostra_2023_2026', 'excesso_vs_universo_ew', 'media_anual'), sign=True)} a.a. fora dela. Pesos iguais por bloco ficaram "
      f"em {_p(_g(ci, 'fora_amostra_2023_2026', 'excesso_vs_universo_ew', 'media_anual'), sign=True)} e os pesos atuais do painel renormalizados "
      f"em {_p(_g(cr, 'fora_amostra_2023_2026', 'excesso_vs_universo_ew', 'media_anual'), sign=True)} "
      f"(IC 12m fora da amostra {_n(_g(C, 'c_painel_renorm', 'ic', '12m', 'fora_amostra_2023_2026', 'ic_medio'))}). "
      f"A regra recomendada, estimada só com 2017–2022, entregou {_p(_g(crr, 'fora_amostra_2023_2026', 'excesso_vs_universo_ew', 'media_anual'), sign=True)} "
      f"(IC 1m {_n(_g(C, 'c_recomendado_regra', 'ic', '1m', 'fora_amostra_2023_2026', 'ic_medio'))}, IC 12m "
      f"{_n(_g(C, 'c_recomendado_regra', 'ic', '12m', 'fora_amostra_2023_2026', 'ic_medio'))}). Com {n_oos} meses fora da amostra, nenhuma dessas diferenças "
      "é estatisticamente distinguível. A escolha tem de ser por robustez, não pelo melhor número.")
    crisis_f = sorted(FACTORS, key=lambda f: -(_g(fic(f, 3), "crise", "ic_medio") or -9))
    w(f"6. **Regime de crise** (formação após Ibovespa ≤ −10% em 3 meses; {len(M['meses_crise'])} meses: {', '.join(M['meses_crise'])}; "
      f"{ep_txt} independentes). Valor (B/P, EBITDA/EV) e momentum ficam mais fortes. Baixo risco **inverte**: as ações de beta e "
      "volatilidade altas lideram a recuperação. IC 3m em crise: "
      + "; ".join(f"{LABEL[f]} {_n(_g(fic(f, 3), 'crise', 'ic_medio'))}" for f in crisis_f[:4]) + "; ... "
      + "; ".join(f"{LABEL[f]} {_n(_g(fic(f, 3), 'crise', 'ic_medio'))}" for f in crisis_f[-3:]) + ".")
    w("")
    # --------------------------------------------------------------------------- pesos recomendados
    w("## Pesos recomendados")
    w("")
    w("A regra dá a cada fator peso proporcional ao seu IC-IR positivo, na média dos horizontes de 1, 3 e 12 meses. Fatores de IC-IR médio "
      "≤ 0 ficam com zero. São 13 candidatos: tamanho fica fora porque é o fator mais contaminado pelo viés de sobrevivência. A regra não "
      "inverte a covariância dos ICs nem usa corte duro. Fora da amostra, esquemas simples como este generalizaram tão bem ou melhor que o "
      "máximo IC-IR, que concentrou peso em momentum e perdeu força em 2023–2026. Os números são medianas de "
      f"{rec['n_boot']} reamostragens em blocos de 12 meses da amostra inteira ({rec['meses']} meses com os três horizontes). O intervalo é "
      "o de 90% (p5–p95), e o peso recomendado é a mediana normalizada e arredondada para 5%. A mesma regra estimada só com 2017–2022 está "
      "na tabela de compostos, com o resultado fora da amostra.")
    w("")
    pg = rec["por_grupo"]
    groups = ["valor", "qualidade", "solidez", "momentum", "baixo risco"]
    gm = pd.Series(pg["mediana"]).reindex(groups).fillna(0)
    gm = gm / gm.sum()
    gr = (gm / 0.05).round() * 0.05
    gr = gr / gr.sum()
    w("| Bloco | Peso recomendado | Mediana bootstrap | IC 90% | P(peso > 1%) | Estimativa pontual |")
    w("|---|---:|---:|---:|---:|---:|")
    glab = {"valor": "Valor", "qualidade": "Qualidade", "solidez": "Solidez", "momentum": "Momentum 12-1", "baixo risco": "Baixo risco"}
    for g in groups:
        w(f"| {glab[g]} | **{_p(gr[g], 0)}** | {_p(pg['mediana'].get(g), 0)} | {_p(pg['p05'].get(g), 0)} – {_p(pg['p95'].get(g), 0)} | "
          f"{_n(pg['prob_peso_positivo'].get(g), 2)} | {_p(pg['ponto'].get(g), 0)} |")
    w("")
    w("Por fator (mediana [p5–p95], P(peso > 1%)): " + "; ".join(
        f"{LABEL[f]} {_p(rec['mediana'].get('z_' + f), 0)} [{_p(rec['p05'].get('z_' + f), 0)}–{_p(rec['p95'].get('z_' + f), 0)}], "
        f"{_n(rec['prob_peso_positivo'].get('z_' + f), 2)}" for f in REC_CANDIDATES
        if (rec['prob_peso_positivo'].get('z_' + f) or 0) >= 0.2) + ". Os demais ficam com peso zero na maioria das reamostragens.")
    w("")
    bx = B.get("blocos_proxies", {})
    w("Tradução para o painel (hoje valor 30%, qualidade 20%, solidez 15%, upside 10%, sobrerreação 10%, probabilidade 15%):")
    w("")
    w(f"- **Valor** deve ser o maior bloco: {_p(gr['valor'], 0)} recomendado, intervalo {_p(pg['p05'].get('valor'), 0)}–{_p(pg['p95'].get('valor'), 0)}. "
      "Upside (DCF) e probabilidade (Monte Carlo) derivam do mesmo valor justo e, na prática, são valor de novo. Sem histórico para "
      "testá-los, o prudente é tratá-los como parte do bloco valor, sem somar peso.")
    w(f"- **Qualidade** {_p(gr['qualidade'], 0)} e **solidez** {_p(gr['solidez'], 0)}. Os sinais que sobrevivem são ROE, Piotroski e dívida "
      "líquida/EBITDA, todos fracos (t de 1 a 2). Margem bruta e Altman Z″ têm IC ≈ 0 e podem sair dos blocos.")
    w(f"- **Momentum** {_p(gr['momentum'], 0)} e **baixo risco** {_p(gr['baixo risco'], 0)} não existem no painel e entram pela evidência. O "
      "momentum perdeu força fora da amostra no horizonte de 1m, mas segue positivo em 12m. Os dois estão inflados pelo viés de sobrevivência, "
      "e baixo risco inverte em crises.")
    w(f"- **Sobrerreação**: o proxy mensal tem IC negativo significativo, e com os proxies no otimizador o bootstrap dá peso mediano "
      f"{_p(_g(bx, 'mediana', 'zb_reversao_1m'), 0)} a ela e {_p(_g(bx, 'mediana', 'zb_upside_hist'), 0)} ao upside histórico. A recomendação é "
      "0% a 5% fora de crises.")
    wc = res["weights"].get("crise_blocos") or {}
    w(f"- **Em crise**, os pesos de referência (IC-IR 3m nos {len(M['meses_crise'])} meses de crise, blocos) são "
      + ", ".join(f"{b.replace('_', ' ')} {_p(wc.get('zb_' + b), 0)}" for b in blocks)
      + f". Indicam mais valor e momentum e zero em baixo risco, mas vêm de {ep_txt} e não servem como estimativa.")
    w("")
    # --------------------------------------------------------------------------- tabela de ICs
    w("## IC por fator e horizonte (amostra inteira)")
    w("")
    w("IC médio, com o t de Newey-West entre parênteses. IC-IR = média/dp do IC mensal. Q5−Q1 = carteira long-short mensal, igualmente "
      "ponderada, do quintil mais atrativo menos o menos atrativo (retorno total, anualizado ×12).")
    w("")
    w("| Fator (sinal) | 1m | 3m | 6m | 12m | IC-IR 1m | % meses IC>0 (1m) | Q5−Q1 a.a. | Sharpe Q5−Q1 | Q5−Q1 12m a.a. |")
    w("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for f in FACTORS + ["upside_hist", "reversao_1m", "prob_proxy"]:
        e = F.get(f)
        if not e:
            continue
        cells = [f"{_n(_g(e, 'horizontes', f'{h}m', 'ic_medio'))} ({_n(_g(e, 'horizontes', f'{h}m', 't_nw'), 1)})" for h in HORIZONS]
        q = _g(e, "quintis_1m", "spread_q5_q1") or {}
        sgn = "+" if e["sinal_esperado"] > 0 else "−"
        w(f"| {e['label']} ({sgn}) | " + " | ".join(cells) + f" | {_n(_g(e, 'horizontes', '1m', 'ic_ir'), 2)} | "
          f"{_p(_g(e, 'horizontes', '1m', 'pct_positivo'), 0)} | {_p(q.get('anual'), 1, True)} | {_n(q.get('sharpe'), 2)} | "
          f"{_p(_g(e, 'quintis_1m', 'spread_q5_q1_12m', 'anualizado'), 1, True)} |")
    w("")
    # --------------------------------------------------------------------------- IS x OOS x crise
    w("## Estabilidade: dentro × fora da amostra e crise × normal")
    w("")
    w("| Fator | IC 1m 2017–22 | IC 1m 2023–26 | IC 12m 2017–22 | IC 12m 2023–26 | IC 3m crise | IC 3m normal | % crise IC>0 (3m) |")
    w("|---|---:|---:|---:|---:|---:|---:|---:|")
    for f in FACTORS + ["upside_hist", "reversao_1m"]:
        e = F.get(f)
        if not e:
            continue
        h1, h12, h3 = _g(e, "horizontes", "1m"), _g(e, "horizontes", "12m"), _g(e, "horizontes", "3m")
        w(f"| {e['label']} | {_n(_g(h1, 'in_sample_2017_2022', 'ic_medio'))} | {_n(_g(h1, 'fora_amostra_2023_2026', 'ic_medio'))} | "
          f"{_n(_g(h12, 'in_sample_2017_2022', 'ic_medio'))} | {_n(_g(h12, 'fora_amostra_2023_2026', 'ic_medio'))} | "
          f"{_n(_g(h3, 'crise', 'ic_medio'))} | {_n(_g(h3, 'normal', 'ic_medio'))} | {_p(_g(h3, 'crise', 'pct_positivo'), 0)} |")
    w("")
    # --------------------------------------------------------------------------- decaimento
    w("## Decaimento do sinal")
    w("")
    w("IC médio entre o fator em t e o retorno do mês t+k → t+k+1. Mede por quanto tempo uma leitura do fator continua informativa.")
    w("")
    lags = [0, 1, 2, 3, 6, 9, 11]
    w("| Fator | " + " | ".join(f"k={k}" for k in lags) + " |")
    w("|---|" + "---:|" * len(lags))
    for f, dec in res["decay"].items():
        dd = {x["defasagem_meses"]: x["ic_medio"] for x in dec}
        w(f"| {F[f]['label']} | " + " | ".join(_n(dd.get(k)) for k in lags) + " |")
    w("")
    # --------------------------------------------------------------------------- compostos
    w("## Compostos: dentro (2017–2022) e fora da amostra (2023–2026)")
    w("")
    w("Carteira = quintil superior do escore, igualmente ponderada, rebalanceamento mensal, retorno total, sem custos. Sharpe do quintil "
      "superior sobre o CDI; Sharpe da long-short sem taxa livre. Excesso = quintil superior menos a média igualmente ponderada do "
      "universo (t Newey-West). No mesmo período, o universo igualmente ponderado rendeu "
      f"{_p(_g(C, 'c_iguais_blocos', 'carteiras', 'in_sample_2017_2022', 'universo_ew', 'retorno_anual'))} a.a. em 2017–2022 e "
      f"{_p(_g(C, 'c_iguais_blocos', 'carteiras', 'fora_amostra_2023_2026', 'universo_ew', 'retorno_anual'))} a.a. em 2023–2026. O Ibovespa (sem "
      f"proventos) rendeu {_p(_g(C, 'c_iguais_blocos', 'carteiras', 'in_sample_2017_2022', 'ibov', 'retorno_anual'))} e "
      f"{_p(_g(C, 'c_iguais_blocos', 'carteiras', 'fora_amostra_2023_2026', 'ibov', 'retorno_anual'))}.")
    w("")
    w("| Composto | Período | Q5 a.a. | Vol | Sharpe | Máx. DD | Excesso a.a. (t) | L/S a.a. | Sharpe L/S | IC 1m (t) | IC 12m | Giro/mês |")
    w("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for c, e in C.items():
        for per, lab in (("in_sample_2017_2022", "2017–22"), ("fora_amostra_2023_2026", "2023–26"), ("crise", "crise")):
            cw = _g(e, "carteiras", per)
            if not cw:
                continue
            t5, ls, ex = cw["top_quintil"] or {}, cw["long_short_q5_q1"] or {}, cw["excesso_vs_universo_ew"]
            ic1, ic12 = _g(e, "ic", "1m", per) or {}, _g(e, "ic", "12m", per) or {}
            w(f"| {e['descricao']} | {lab} | {_p(t5.get('retorno_anual'))} | {_p(t5.get('vol_anual'), 0)} | {_n(t5.get('sharpe'), 2)} | "
              f"{_p(t5.get('max_drawdown'), 0)} | {_p(ex.get('media_anual'), 1, True)} ({_n(ex.get('t_nw'), 1)}) | {_p(ls.get('retorno_anual'), 1, True)} | "
              f"{_n(ls.get('sharpe'), 2)} | {_n(ic1.get('ic_medio'))} ({_n(ic1.get('t_nw'), 1)}) | {_n(ic12.get('ic_medio'))} | "
              f"{_p(e.get('giro_mensal_top_quintil'), 0)} |")
    w("")
    w("Pesos estimados em 2017–2022 (usados fora da amostra):")
    w("")
    for k, v in res["weights"].items():
        if v:
            w(f"- `{k}`: " + ", ".join(f"{kk.split('_', 1)[1]} {_p(vv, 0)}" for kk, vv in sorted(v.items(), key=lambda kv: -kv[1]) if vv > 0.005))
    w("")
    fb_ = B.get("fatores", {})
    if fb_:
        w("Bootstrap no nível dos 14 fatores, amostra inteira, IC-IR 1m, agregado por grupo (mediana [p5–p95]): "
          + "; ".join(f"{g} {_p(fb_['por_grupo']['mediana'][g], 0)} [{_p(fb_['por_grupo']['p05'][g], 0)}–{_p(fb_['por_grupo']['p95'][g], 0)}]"
                      for g in fb_["por_grupo"]["mediana"]) + ".")
        w("")
    # --------------------------------------------------------------------------- método e vieses
    w("## Método")
    w("")
    w("- **Preços**: COTAHIST oficial da B3 (lote padrão, à vista), série por ISIN (cobre troca de código), corte na última lacuna > 45 dias. "
      "Os ajustes usam `split_events`/`adjust` de `pipeline/market.py` sobre o suplemento B3, mais o histórico do Yahoo (o suplemento só "
      "guarda o evento mais recente de cada tipo por ISIN; sem isso faltariam, por exemplo, as bonificações anuais do Bradesco 2015–2021) e "
      "a detecção de razões redondas. Restituição de capital em ações (BRAP4, 12/2021) recebe ajuste neutro. **Retorno total**: proventos "
      "em dinheiro da B3 (histórico por evento), na classe negociada (units: linha UNT ou composição), reinvestidos no ex-dia.")
    w(f"- **Fundamentos**: DFP 2015–2025 e ITR 2016–2026 brutos da CVM, extraídos com as funções de `pipeline/cvm.py`. Usa o arquivo "
      f"original de cada período, sem a reapresentação do ano seguinte, e a última versão entregue daquele período. O LTM sai da "
      f"aritmética dos acumulados (YTD + exercício anterior − YTD de um ano antes), que funciona para exercícios fora de dezembro (CAML3, SMTO3). "
      f"Defasagem de {LAG_Q} dias para ITR e {LAG_A} dias para DFP. Os dados ficam velhos demais (descartados) após 18 meses.")
    w("- **Ações em circulação**: composição do capital da CVM (2020+), com escala corrigida registro a registro contra a contagem atual da "
      "B3 retroprojetada pelos eventos. Antes de 2020, retroprojeção pelos eventos, corrigida por emissões e recompras grandes (> 15%) "
      f"inferidas do lucro por ação básico ({', '.join(fixes) if fixes else 'nenhuma'}).")
    w(f"- **Universo**: os {M.get('universo_base', '')}. Formação no último pregão do mês. Ações com último negócio há mais de 7 dias são excluídas.")
    w("- **Fatores**: E/P = lucro LTM dos controladores / valor de mercado. B/P = PL dos controladores / valor de mercado. EBITDA/EV, com "
      "EV = valor de mercado + dívida líquida (com arrendamentos) + minoritários. DY = proventos com data-com nos últimos 12 meses / preço. "
      "ROE sobre PL médio. ROIC = EBIT×(1−34%)/(PL + dívida líquida). Margem bruta LTM. Piotroski F com os 9 sinais LTM contra LTM de um "
      "ano antes (como `pipeline/build.py`). Altman Z″ mercados emergentes = 3,25 + 6,56·X1 + 3,26·X2 + 6,72·X3 + 1,05·X4. Dívida "
      "líquida/EBITDA (EBITDA ≤ 0 com dívida = pior). Momentum 12-1. Volatilidade de 252 pregões. Beta diário de 504 pregões contra o "
      "Ibovespa. Log do valor de mercado. Bancos, seguradoras, B3 e Itaúsa ficam fora dos fatores de EBITDA, ROIC, margem, Piotroski, "
      "Altman e alavancagem.")
    w("- **Compostos**: z-score transversal winsorizado (2,5%/97,5%, corte ±3). O escore pondera os z disponíveis e renormaliza os pesos "
      "por ação, como o escore do painel. Proxies do painel: valor = média z(E/P, EBITDA/EV, DY), no lugar da TIR implícita. Upside = "
      "desconto dos múltiplos (E/P, B/P, EBITDA/EV) contra a mediana de 60 meses da própria ação. Qualidade = ROE médio de 5 exercícios + "
      "(Piotroski − 4,5)/9. Solidez = −dív. líq./EBITDA + Altman/3, como no painel. Sobrerreação = −(retorno do mês − beta × Ibovespa). "
      "Probabilidade = ln(1 + upside)/volatilidade.")
    w("")
    w("## Vieses e limitações")
    w("")
    w("- **Sobrevivência e seleção**: o universo são as ações líquidas de out/2026. Empresas que quebraram, foram compradas ou perderam "
      "liquidez em 2017–2026 não entram. Pior: uma small cap de 2017 só está aqui se sobreviveu e cresceu, o que infla retornos passados de "
      "small caps e de ações com momentum. Os números de tamanho, momentum e baixo risco devem ser lidos com desconto. O nível de retorno "
      "do universo (a.a.) é otimista. Diferenças entre fatores e ICs sofrem menos, mas também sofrem.")
    w(f"- **Poucos anos**: {M['meses']} meses, cerca de {M['meses'] // 12} anos e um único ciclo de juros. Fora da amostra são {n_oos} meses. "
      f"Crise são {len(M['meses_crise'])} meses de {ep_txt}. Com IC-IR mensal de ~0,15–0,25, t ≈ 2 exige ~100 meses: quase todos os "
      "fatores estão no limiar da significância, e os intervalos dos pesos são largos.")
    w(f"- **Universo pequeno**: {nmin} a {nmax} nomes por mês, quintis de {nmin // 5} a {nmax // 5} ações. Os spreads Q5−Q1 são ruidosos e não descontam custos. "
      "O giro mensal do quintil superior aparece na tabela.")
    w("- **Dados**: a última versão de cada ITR/DFP pode conter correções feitas depois da data de corte (viés pequeno). Ações antes de "
      "2020 são estimadas. Proventos e eventos dependem de B3/Yahoo. O mês 2026-10 é parcial (até 23/10). O retorno do Ibovespa é só de "
      "preço. Upside DCF, probabilidade Monte Carlo e sobrerreação do dia da eleição não têm histórico e foram testados só por proxies.")
    w("- **Múltiplas comparações**: 14 fatores × 4 horizontes. Alguns t ≈ 2 surgem por acaso. Pesos de crise são ilustrativos.")
    w("")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sp", default=os.environ.get("EAGORA_SP", DEFAULT_SP), help="diretório com work/ e raw/ (scratchpad)")
    ap.add_argument("--cache", default=None, help="diretório de cache (default: <sp>/quant/q1/cache)")
    ap.add_argument("--from-stage", choices=STAGES, default=None, help="refaz a partir deste estágio")
    a = ap.parse_args()
    sp = a.sp
    cache = Path(a.cache or Path(sp) / "quant" / "q1" / "cache")
    cache.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    q = json.load(open(ROOT / "data" / "market" / "quotes.json"))
    # universo original de 147 tickers; entradas marcadas "extra" (acrescentadas depois ao painel ao vivo) ficam fora
    tickers = [k for k in q if k != "fetched_at" and not (q[k] or {}).get("extra")]
    redo = set(STAGES[STAGES.index(a.from_stage):]) if a.from_stage else set()
    fund = pd.read_pickle(cache / "fund.pkl") if (cache / "fund.pkl").exists() and "fund" not in redo else stage_fund(sp, cache, tickers)
    prices = pd.read_pickle(cache / "prices.pkl") if (cache / "prices.pkl").exists() and "prices" not in redo else stage_prices(sp, cache, tickers)
    if (cache / "panel.pkl").exists() and not redo & {"fund", "prices", "panel"}:
        panel = pd.read_pickle(cache / "panel.pkl")
    else:
        panel = stage_panel(sp, cache, tickers, fund, prices)
    res = stage_analysis(sp, cache, panel, prices)
    u = res.pop("_u")
    u.to_pickle(cache / "universe_scored.pkl")
    res["meta"].update({
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "universo_base": f"{len(tickers)} tickers de data/market/quotes.json (universo líquido atual, sem as entradas 'extra') filtrados por ADTV 3m >= R$ 5 mi na data; 1 classe por emissor (maior ADTV)",
        "tickers": tickers,
        "defasagens": {"trimestral_itr_dias": LAG_Q, "anual_dfp_dias": LAG_A},
        "retornos": "retorno total (proventos em dinheiro B3 reinvestidos no ex-dia; desdobramentos, grupamentos e bonificações B3 + Yahoo + razões redondas), fim de mês a fim de mês",
        "correcoes_acoes_por_lpa": {k: v for k, v in (panel.get("share_fix") or {}).items() if v},
        "problemas_precos": prices.get("issues"),
        "saltos_nao_explicados_35pct": {k: v["weird"] for k, v in prices["per"].items() if v["weird"]},
    })
    json.dump(clean(res), open(OUT_DIR / "factor_backtest.json", "w"), ensure_ascii=False, indent=1)
    (OUT_DIR / "factor_backtest.md").write_text(render_md(res))
    log("gravado:", OUT_DIR / "factor_backtest.json", "e", OUT_DIR / "factor_backtest.md")


if __name__ == "__main__":
    main()

"""Estudo de crashes 2016–2026: o que previu a recuperação das ações brasileiras depois de choques de mercado,
e aplicação ao choque de 26/10/2026 (ranking "regime de crise" das 59 empresas da cobertura).

Uso:
    python pipeline/tests/crash_study.py [cotahist_csv_gz] [dir_raw_b3]
    (padrão: $EAGORA_RAW/work/cotahist.csv.gz e $EAGORA_RAW/raw/b3, EAGORA_RAW = scratchpad da sessão)

Entradas: COTAHIST diário não ajustado; eventos B3 (supplement.json, desdobramentos/grupamentos/bonificações);
Ibovespa diário (indices.json); setores B3 (details.json); fundamentos CVM data/hist/{TICKER}.json;
choque de hoje data/market/{TICKER}.json (stats.today) e data/market/_market.json; cobertura research/_coverage.json;
valuation data/app/overview.json (só referência, não entra no modelo).

Saídas: data/tests/crash_study.json, data/tests/crash_study.md

Método (resumo):
  * Episódios: todos os dias com Ibovespa ≤ −4% desde 2016 (exceto 02/02/2016, sem 1 ano de histórico prévio no
    COTAHIST) + 31/10/2022 (pós-eleição). Dias a ≤ 45 dias corridos um do outro formam um "cluster" (crise).
  * Universo principal: ações com fundamentos CVM em data/hist (sobreviventes de 2026), 1 classe por emissor (a mais
    líquida), negociadas no dia do choque, presença ≥ 90% nos 63 pregões anteriores e ADTV ≥ R$ 1 mi.
  * Características pré-choque (até t−1): beta e beta de baixa diários (até 504 pregões), DL/EBITDA, E/P, B/P, ROE
    (CVM point-in-time: trimestre +45 dias, ano +90 dias), tamanho (log valor de mercado), liquidez (log ADTV 63d),
    momentum 12−1, exportadora, financeira, estatal (point-in-time).
  * Queda do dia: resíduo contra o beta (r0 − β_baixa·r_m) e contra fatores (resíduo da regressão cross-section de r0
    em beta, alavancagem, tamanho e dummies setoriais — mesma especificação de pipeline/market.py).
  * Retornos futuros 1/3/6/12 meses (21/63/126/252 pregões) a partir do fechamento do dia do choque e a partir do fundo
    do episódio (mínima do Ibovespa em [t0, t0+63]). Retornos de preço (sem proventos).
  * Regressões cross-section por episódio (OLS, erros HC3), agregadas à Fama-MacBeth por dia e por cluster
    (a inferência honesta é a por cluster: os dias da Covid têm janelas futuras quase idênticas).
  * Estratégias de cesta (quintis, peso igual, compra no fechamento do choque) vs Ibovespa, com drawdown.
  * Reversão: estrutura a termo do coeficiente do resíduo φ(h) para h = 1…252 pregões.
  * Viés de sobrevivência: modelo só de mercado no universo amplo (todas as ações do COTAHIST, inclusive deslistadas)
    vs o subconjunto de sobreviventes.
  * Validação fora da amostra: deixa-um-cluster-de-fora (LOCO).
  * Hoje: mesmas características com dados até 23/10/2026 e o retorno de hoje (stats.today.chg); coeficientes
    FM por cluster com encolhimento (b·max(0, 1 − 1/t²)); intervalo = dispersão entre clusters + ruído idiossincrático.
"""
import json
import math
import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as sps

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
import market as mk  # noqa: E402  (split_events, adjust, STATE, TODAY, LAST_CLOSE)

RAW = Path(os.environ.get("EAGORA_RAW", "/tmp/claude-1000/-home-joaoemanuel-git-e-agora/cd238de5-f094-4d2e-ba5c-c5e5bf8d2192/scratchpad"))
OUT = ROOT / "data" / "tests"
H = {"1m": 21, "3m": 63, "6m": 126, "12m": 252}
PHI_H = [1, 2, 3, 5, 10, 21, 42, 63, 126, 189, 252]
CRASH_THR = -0.04
EXTRA_DAYS = {"2022-10-31": "Pós-eleição: Lula eleito (Ibovespa +1,3%, estatais −8% a −10%)"}
LABELS = {
    "2016-02-02": "Petróleo/China (sem histórico prévio no COTAHIST: excluído)",
    "2017-05-18": "Joesley Day (delação JBS/Temer)",
    "2018-05-28": "Greve dos caminhoneiros",
    "2020-02-26": "Covid: primeiro dia após o Carnaval",
    "2020-03-05": "Covid", "2020-03-06": "Covid", "2020-03-09": "Covid + guerra de preços do petróleo",
    "2020-03-11": "Covid: OMS declara pandemia", "2020-03-12": "Covid: circuit breakers", "2020-03-16": "Covid: circuit breaker",
    "2020-03-18": "Covid: circuit breaker", "2020-03-23": "Covid: fundo do Ibovespa", "2020-03-27": "Covid",
    "2020-04-24": "Demissão de Moro (dentro da janela da Covid)",
    "2020-10-28": "Segunda onda da Covid na Europa",
    "2021-02-22": "Intervenção na Petrobras (troca do CEO)",
    "2025-12-05": "Candidatura de Flávio Bolsonaro (eleição 2026)",
}
CLUSTER_NAMES = {"2017-05": "Joesley 2017", "2018-05": "Greve 2018", "2020-02": "Covid 2020", "2020-10": "2ª onda 2020",
                 "2021-02": "Petrobras 2021", "2022-10": "Eleição 2022", "2025-12": "Flávio 2025"}
POLITICAL = {"Joesley 2017", "Petrobras 2021", "Eleição 2022", "Flávio 2025"}
ELECTORAL = {"Eleição 2022", "Flávio 2025"}
# exportadoras: Materiais Básicos (exceto domésticas), petróleo E&P/integrada (distribuidoras não) e lista explícita
EXPORTER_TK = {"EMBJ3", "EMBR3", "WEGE3", "SUZB3", "KLBN11", "BEEF3", "MBRF3", "MRFG3", "BRFS3", "JBSS3", "SLCE3", "SMTO3", "TUPY3",
               "PETR3", "PETR4", "PRIO3", "RECV3", "BRAV3", "RRRP3", "ENAT3"}
DOMESTIC_MAT = {"DXCO3", "RANI3"}  # Materiais Básicos com receita essencialmente doméstica
# estatais point-in-time: (ticker, controle estatal até)
STATE_UNTIL = {"AXIA3": "2022-06-14", "ELET3": "2022-06-14", "ELET6": "2022-06-14", "SBSP3": "2024-07-22",
               "CPLE3": "2023-08-10", "CPLE6": "2023-08-10", "VBBR3": "2019-07-24", "BRDT3": "2019-07-24"}
STATE_ALWAYS = set(mk.STATE) - {"BRAP4"}  # Bradespar não é estatal
DAY0_COLS = ["beta", "lev_c", "log_mcap", "exporter", "financial", "state", "utility", "consumo"]  # = market.py xsec
FWD_COLS = ["beta", "resid", "value", "roe", "lev", "size", "mom", "exporter", "financial", "state"]  # E/P entra via 'value' (E/P ≈ B/P·ROE)
FWD_COLS_EP = ["beta", "resid", "ep", "bp", "roe", "lev", "size", "mom", "exporter", "financial", "state"]  # robustez
Z_COLS = ["ep", "bp", "roe", "lev", "size", "mom", "liq"]
DUMMIES = ("exporter", "financial", "state", "consumo", "utility")
UNI_COLS = ["beta", "resid", "resid_b", "r0", "ep", "bp", "value", "roe", "lev", "size", "liq", "mom", "exporter", "financial", "state", "consumo", "utility"]
SCORE_COLS = ["resid", "beta", "value", "roe", "lev", "size", "mom", "exporter", "state"]
REGIMES = {  # pesos por cluster na média de Fama-MacBeth; definidos pela natureza do choque, não pelo resultado
    "todos": lambda c: 1.0,
    "recomendado": lambda c: 2.0 if c in POLITICAL else 1.0,
    "politico": lambda c: 1.0 if c in POLITICAL else 0.0,
    "eleitoral": lambda c: 1.0 if c in ELECTORAL else 0.0,
    "panico": lambda c: 0.0 if c in POLITICAL else 1.0,
}


# ---------------------------------------------------------------------------------------------- utilidades
def fnum(x):
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) else float(x)


def rnd(x, n=4):
    if x is None:
        return None
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return round(x, n) if np.isfinite(x) else None


def rank_normal(s):
    """Escore normal pelos postos (robusto a outliers); NaN -> 0 (neutro)."""
    s = pd.Series(s, dtype=float)
    out = pd.Series(0.0, index=s.index)
    m = s.notna()
    if m.sum() >= 5:
        r = s[m].rank()
        out[m] = sps.norm.ppf((r - 0.5) / m.sum())
    return out


def winsor(s, p=0.01):
    s = pd.Series(s, dtype=float)
    lo, hi = s.quantile(p), s.quantile(1 - p)
    return s.clip(lo, hi)


def ols_hc3(y, X, names):
    """OLS com erros robustos HC3; descarta colunas constantes (exceto o intercepto)."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    keep = [0] + [j for j in range(1, X.shape[1]) if np.nanstd(X[:, j]) > 1e-12]
    Xk = X[:, keep]
    n, p = Xk.shape
    out = {nm: (np.nan, np.nan) for nm in names}
    if n <= p + 2:
        return out, np.nan, np.nan, None
    XtXi = np.linalg.pinv(Xk.T @ Xk)
    b = XtXi @ Xk.T @ y
    e = y - Xk @ b
    h = np.einsum("ij,jk,ik->i", Xk, XtXi, Xk)
    w = (e / np.clip(1 - h, 1e-6, None)) ** 2
    V = XtXi @ (Xk.T * w) @ Xk @ XtXi
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    sst = ((y - y.mean()) ** 2).sum()
    r2 = 1 - (e ** 2).sum() / sst if sst > 0 else np.nan
    for j, col in enumerate(keep):
        out[names[col]] = (float(b[j]), float(se[j]))
    return out, float(r2), float(np.std(e, ddof=p)), e


def slopes(Y, x):
    """Inclinação OLS coluna a coluna (com NaN) de Y (T×N) em x (T)."""
    M = ~np.isnan(Y)
    X = np.where(M, x[:, None], np.nan)
    n = M.sum(0)
    with np.errstate(invalid="ignore", divide="ignore"):
        mx, my = np.nanmean(X, 0), np.nanmean(Y, 0)
        cov = np.nansum((X - mx) * (Y - my), 0)
        var = np.nansum((X - mx) ** 2, 0)
        b = cov / var
    return b, n


def clean(o):
    """Converte numpy/NaN para tipos JSON."""
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.bool_, bool)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        return float(o) if np.isfinite(o) else None
    if isinstance(o, pd.Timestamp):
        return o.strftime("%Y-%m-%d")
    return o


def max_dd(path):
    p = np.asarray(path, float)
    p = p[np.isfinite(p)]
    if len(p) == 0:
        return None
    p = np.concatenate([[1.0], p])
    return float((p / np.maximum.accumulate(p) - 1).min())


# ---------------------------------------------------------------------------------------------- dados
def tk_class(tk):
    return tk[4:]


def load_panel(cot_path, sup):
    """Painel ajustado (desdobramentos/grupamentos B3 + razões 'redondas'), por segmento de ISIN e costurado em cadeias:
    renomeações trocam o ISIN (CCRO3→MOTV3, ELET3→AXIA3, ARZZ3→AZZA3, BRDT3→VBBR3, EMBR3→EMBJ3, TRPL4→ISAE4,
    NATU3→NTCO3→NATU3). Um segmento que termina é ligado ao segmento da mesma classe que começa até 7 dias depois com
    preço contínuo (razão 1:1 ± 20%); a cadeia é indexada pelo ISIN mais recente."""
    df = pd.read_csv(cot_path, usecols=["date", "ticker", "close", "volume", "fatcot", "isin"], parse_dates=["date"])
    df = df[df["isin"].str[6:9].isin(["ACN", "CDA", "UNT"]) & df["ticker"].str[4:].isin(["3", "4", "5", "6", "7", "8", "11"])].copy()
    df["close"] = df["close"] / df["fatcot"].clip(lower=1)
    df = df.sort_values("date").drop_duplicates(["isin", "date"], keep="last")
    close = df.pivot(index="date", columns="isin", values="close").sort_index()
    vol = df.pivot(index="date", columns="isin", values="volume").reindex(close.index)
    cal = close.index
    last_tk = df.groupby("isin")["ticker"].last()
    nice = [2, 3, 4, 5, 8, 10, 20, 25, 50, 100]
    seg_adj, seg_raw, seg_tk, seg_isin, seg_ev = {}, {}, {}, {}, {}
    for isin in close.columns:
        s = close[isin].dropna()
        if len(s) < 20:
            continue
        tk = last_tk[isin]
        evs = mk.split_events(sup.get(tk[:4]), isin) if sup.get(tk[:4]) else []
        a = mk.adjust(s, evs)
        r = a.pct_change(fill_method=None).dropna()
        extra = []
        for d, r_ in r[r.abs() > 0.35].items():  # eventos ausentes da lista B3: razão "redonda" no salto (como market.py)
            ratio = 1 + r_
            for m_ in nice:
                for mult in (m_, 1 / m_):
                    if abs(ratio * mult - 1) < 0.08:
                        extra.append((s.index[s.index.get_loc(d) - 1], mult))
        if extra:
            evs = sorted(evs + extra)
            a = mk.adjust(s, evs)
        gaps = s.index.to_series().diff().dt.days
        cuts = [s.index[0]] + list(gaps[gaps > 45].index) + [None]
        segs = []
        for i in range(len(cuts) - 1):
            m = (s.index >= cuts[i]) & ((s.index < cuts[i + 1]) if cuts[i + 1] is not None else True)
            segs.append(m)
        for i, m in enumerate(segs):
            key = isin if i == len(segs) - 1 else f"{isin}#{i}"
            seg_adj[key], seg_raw[key], seg_tk[key], seg_isin[key], seg_ev[key] = a[m], s[m], tk, isin, evs
    first = {k: v.index[0] for k, v in seg_adj.items()}
    last = {k: v.index[-1] for k, v in seg_adj.items()}
    end_cut = cal[-1] - pd.Timedelta(days=30)
    cand = []
    for k_old, d_end in last.items():
        if d_end >= end_cut:
            continue
        for k_new, d0 in first.items():
            if k_new == k_old or not (d_end < d0 <= d_end + pd.Timedelta(days=7)):
                continue
            if tk_class(seg_tk[k_old]) != tk_class(seg_tk[k_new]):
                continue
            ratio = seg_raw[k_new].iloc[0] / seg_raw[k_old].iloc[-1]
            if not 0.8 < ratio < 1.25:
                continue
            v_old = vol[seg_isin[k_old]].reindex(seg_raw[k_old].index[-20:]).fillna(0).mean()
            v_new = vol[seg_isin[k_new]].reindex(seg_raw[k_new].index[:20]).fillna(0).mean()
            if v_old <= 0 or v_new <= 0 or not 0.2 < v_new / v_old < 5:
                continue
            cand.append((abs(math.log(ratio)), k_old, k_new, ratio))
    succ, pred = {}, {}
    for fit, k_old, k_new, ratio in sorted(cand):
        if k_old in succ or k_new in pred:
            continue
        succ[k_old], pred[k_new] = k_new, k_old
    # cadeias: do segmento terminal para trás
    P_cols, R_cols, V_cols, chain_tk, chain_ev, chains = {}, {}, {}, {}, {}, {}
    vol_seg = {}
    for key in seg_adj:
        isin = seg_isin[key]
        vol_seg[key] = vol[isin].reindex(seg_adj[key].index)
    for key in seg_adj:
        if key in succ:
            continue
        chain = [key]
        while chain[0] in pred:
            chain.insert(0, pred[chain[0]])
        adj_s = seg_adj[chain[-1]].copy()
        raw_s = seg_raw[chain[-1]].copy()
        vol_s = vol_seg[chain[-1]].copy()
        evs = list(seg_ev[chain[-1]])
        for i in range(len(chain) - 2, -1, -1):
            old, new = chain[i], chain[i + 1]
            target_last = adj_s.iloc[0] * seg_raw[old].iloc[-1] / seg_raw[new].iloc[0]
            scaled = seg_adj[old] * (target_last / seg_adj[old].iloc[-1])
            adj_s = pd.concat([scaled, adj_s])
            raw_s = pd.concat([seg_raw[old], raw_s])
            vol_s = pd.concat([vol_seg[old], vol_s])
            if seg_isin[old] != seg_isin[chain[-1]]:
                evs += [e for e in seg_ev[old] if e[0] < seg_adj[old].index[-1]]
        if len(adj_s) < 60:
            continue
        P_cols[key], R_cols[key], V_cols[key] = adj_s, raw_s, vol_s
        chain_tk[key], chain_ev[key] = seg_tk[chain[-1]], sorted(set(evs))
        if len(chain) > 1:
            chains[key] = [f"{seg_tk[c]}:{c}" for c in chain]
    P = pd.DataFrame(P_cols).reindex(cal)
    R_raw = pd.DataFrame(R_cols).reindex(cal)
    V = pd.DataFrame(V_cols).reindex(cal)
    last_tk = pd.Series(chain_tk)
    rec = df[df.date >= "2026-09-01"].groupby("ticker")["isin"].last()
    recent = rec[rec.isin(P.columns)]
    return P, R_raw, V, last_tk, recent, chain_ev, chains


def load_hist():
    out = {}
    for f in sorted((ROOT / "data" / "hist").glob("*.json")):
        out[f.stem] = json.load(open(f))
    return out


def qend(k):
    y, q = int(k[:4]), int(k[-1])
    return pd.Timestamp(year=y, month=q * 3, day=1) + pd.offsets.MonthEnd(0)


def fund_pit(hh, d):
    """Fundamentos disponíveis em d: fluxo LTM (4 trimestres, +45d; 4T +90d) ou último ano (+90d); balanço mais recente
    disponível (trimestral +45d ou anual +90d)."""
    fl, fl_end = None, None
    for k in hh.get("annual") or {}:
        y = int(k[2:])
        end = pd.Timestamp(year=y, month=12, day=31)
        if end + pd.Timedelta(days=90) <= d and (fl_end is None or end > fl_end):
            a = hh["annual"][k]
            fl, fl_end = {f: a.get(f) for f in ("ni_controlling", "ebitda", "revenue")}, end
    qk = sorted(hh.get("quarterly") or {}, key=lambda x: (int(x[:4]), int(x[-1])))
    av = [k for k in qk if qend(k) + pd.Timedelta(days=90 if k.endswith("Q4") else 45) <= d]
    if len(av) >= 4:
        last4 = av[-4:]
        ends = [qend(k) for k in last4]
        if (ends[-1] - ends[0]).days < 300 and (fl_end is None or ends[-1] > fl_end):
            f = {}
            for fld in ("ni_controlling", "ebitda", "revenue"):
                vals = [hh["quarterly"][k].get(fld) for k in last4]
                f[fld] = sum(vals) if all(v is not None for v in vals) else None
            fl, fl_end = f, ends[-1]
    bal, bal_end = None, None
    for k, a in (hh.get("annual") or {}).items():
        end = pd.Timestamp(year=int(k[2:]), month=12, day=31)
        if end + pd.Timedelta(days=90) <= d and (bal_end is None or end > bal_end):
            bal, bal_end = a, end
    for k, b in (hh.get("balance_quarterly") or {}).items():
        end = qend(k)
        if end + pd.Timedelta(days=45) <= d and (bal_end is None or end > bal_end):
            bal, bal_end = b, end
    if fl is None or bal is None:
        return None
    return {**fl, "equity_controlling": bal.get("equity_controlling"), "net_debt": bal.get("net_debt"),
            "flow_end": fl_end.strftime("%Y-%m-%d"), "bal_end": bal_end.strftime("%Y-%m-%d")}


def share_records(hh, events):
    """shares_history com escala corrigida registro a registro contra o total atual da B3 (há anos em milhares)."""
    cur = (hh.get("shares") or {}).get("outstanding")
    recs = []
    for r in hh.get("shares_history") or []:
        d = pd.Timestamp(r["date"])
        n = r.get("outstanding")
        if not n or n <= 0:
            continue
        if cur:
            mult_after = np.prod([m for dc, m in events if dc >= d]) if events else 1.0
            ratio = cur / (n * mult_after)
            if 300 < ratio < 30000:
                n *= 1000.0
            elif ratio > 30000 or ratio < 0.02:
                continue
        recs.append((d, float(n)))
    return sorted(recs), cur


def shares_at(recs, cur, events, d):
    prior = [r for r in recs if r[0] <= d]
    if prior:
        b, n = prior[-1]
        for dc, m in events:
            if b <= dc < d:
                n *= m
        return n
    if recs:
        b, n = recs[0]
        for dc, m in events:
            if d <= dc < b:
                n /= m
        return n
    if cur:
        n = cur
        for dc, m in events:
            if dc >= d:
                n /= m
        return n
    return None


def sector_of(det, tk):
    ic = ((det.get(tk[:4]) or {}).get("industryClassification") or "")
    parts = [x.strip() for x in ic.split("/")]
    return parts[0] if parts and parts[0] else None


def is_exporter(setor, tk):
    s = (setor or "").replace(",", ".")
    return (s == "Materiais Básicos" and tk not in DOMESTIC_MAT) or tk in EXPORTER_TK


def is_state(tk, d):
    if tk in STATE_ALWAYS:
        return True
    u = STATE_UNTIL.get(tk)
    return bool(u and d <= pd.Timestamp(u))


# ---------------------------------------------------------------------------------------------- características
def market_chars(P, V, mret, k, isins):
    """Características de mercado com dados até o índice k−1 (k = dia do choque)."""
    lo = max(1, k - 504)
    win = P.iloc[lo - 1:k][isins]
    R = win.ffill().pct_change(fill_method=None).iloc[1:]
    traded = win.iloc[1:].notna()
    m = mret.iloc[lo:k].values
    Y = R.values
    b_all, n_all = slopes(Y, m)
    dn = m < 0
    b_dn, n_dn = slopes(Y[dn], m[dn])
    started = traded.cumsum() > 0
    pres_win = (traded.sum() / started.sum().clip(lower=1)).values
    last63 = P.iloc[max(0, k - 63):k][isins]
    pres63 = last63.notna().mean().values
    adtv = V.iloc[max(0, k - 63):k][isins].fillna(0).mean().values
    Pf = P.iloc[:k][isins].ffill()
    p_1 = Pf.iloc[k - 22].values if k >= 22 else np.full(len(isins), np.nan)
    p_12 = Pf.iloc[k - 253].values if k >= 253 else np.full(len(isins), np.nan)
    vol1y = R.iloc[-252:].std().values * math.sqrt(252)
    df = pd.DataFrame({"beta_all": b_all, "n_beta": n_all, "beta": b_dn, "n_dn": n_dn, "pres_win": pres_win, "pres63": pres63,
                       "adtv": adtv, "mom": p_1 / p_12 - 1, "vol1y": vol1y}, index=isins)
    df.loc[(df.n_beta < 200) | (df.pres_win < 0.8), ["beta_all", "beta"]] = np.nan
    df.loc[df.n_dn < 80, "beta"] = df.loc[df.n_dn < 80, "beta_all"]
    return df


def fund_chars(hist, tk, d, raw_close, events):
    hh = hist.get(tk)
    if hh is None:
        return {}
    f = fund_pit(hh, d)
    recs, cur = share_records(hh, events)
    n = shares_at(recs, cur, events, d)
    per_unit = hh.get("shares_per_unit") or 1
    out = {"is_fin": bool(hh.get("is_financial"))}
    if n and raw_close and raw_close > 0:
        out["mcap"] = raw_close * n / per_unit / 1e6
    if f and out.get("mcap"):
        mc = out["mcap"]
        ni, eq, eb, nd = f.get("ni_controlling"), f.get("equity_controlling"), f.get("ebitda"), f.get("net_debt")
        out["ep"] = ni / mc if ni is not None else None
        out["bp"] = eq / mc if eq is not None else None
        out["roe"] = ni / eq if ni is not None and eq and eq > 0 else None
        if not out["is_fin"] and nd is not None and eb is not None:
            out["lev"] = nd / eb if eb > 0 else (8.0 if nd > 0 else -2.0)
        out["flow_end"], out["bal_end"] = f["flow_end"], f["bal_end"]
    return out


def day0_model(X):
    """Regressão cross-section da queda do dia (especificação de market.py): resíduo contra fatores."""
    Z = X.copy()
    Z["lev_c"] = Z["lev"].clip(-2, 8)
    Z["lev_c"] = Z["lev_c"].fillna(Z["lev_c"].median())
    Z["log_mcap"] = np.log(Z["mcap"].where(Z["mcap"] > 0))
    Z["log_mcap"] = Z["log_mcap"].fillna(Z["log_mcap"].median())
    A = np.column_stack([np.ones(len(Z))] + [Z[c].astype(float).values for c in DAY0_COLS])
    res, r2, _, e = ols_hc3(Z["r0"].values, A, ["const"] + DAY0_COLS)
    fitted = Z["r0"].values - e if e is not None else np.full(len(Z), np.nan)
    return pd.Series(e, index=Z.index), pd.Series(fitted, index=Z.index), res, r2


def build_cross_section(k, d, P, R_raw, V, mret, rm0, isin_tk, hist, det, events, r0_override=None, min_adtv=1e6):
    """Seção cruzada do universo principal no choque de índice k (data d)."""
    isins = [i for i in isin_tk if i in P.columns]
    mc = market_chars(P, V, mret, k, isins)
    rows = []
    for isin in isins:
        tk = isin_tk[isin]
        if r0_override is not None:
            if tk not in r0_override:
                continue
            r0 = r0_override[tk]
            p_prev = P[isin].iloc[:k].dropna()
            if not len(p_prev) or (P.index[k - 1] - p_prev.index[-1]).days > 7:
                continue
            raw_prev = R_raw[isin].iloc[:k].dropna().iloc[-1]
        else:
            p0 = P[isin].iloc[k]
            p_prev = P[isin].iloc[:k].dropna()
            if not np.isfinite(p0) or not len(p_prev) or (d - p_prev.index[-1]).days > 7:
                continue
            r0 = p0 / p_prev.iloc[-1] - 1
            raw_prev = R_raw[isin].iloc[:k].dropna().iloc[-1]
        c = mc.loc[isin]
        if not np.isfinite(c.beta) or c.pres63 < 0.9 or c.adtv < min_adtv:
            continue
        fc = fund_chars(hist, tk, d, raw_prev, events.get(isin, []))
        setor = sector_of(det, tk)
        rows.append({"isin": isin, "ticker": tk, "issuer": isin[2:6], "r0": r0, "beta": float(np.clip(c.beta, -0.5, 3.0)),
                     "beta_all": c.beta_all, "adtv": c.adtv, "mom": c.mom, "vol1y": c.vol1y,
                     "mcap": fc.get("mcap"), "ep": fc.get("ep"), "bp": fc.get("bp"), "roe": fc.get("roe"), "lev": fc.get("lev"),
                     "flow_end": fc.get("flow_end"), "bal_end": fc.get("bal_end"),
                     "setor": setor, "exporter": float(is_exporter(setor, tk)), "financial": float(bool(fc.get("is_fin")) or (setor == "Financeiro")),
                     "state": float(is_state(tk, d)), "utility": float(setor == "Utilidade Pública"), "consumo": float(setor == "Consumo Cíclico")})
    X = pd.DataFrame(rows)
    if X.empty:
        return X
    X = X.sort_values("adtv", ascending=False).drop_duplicates("issuer", keep="first").set_index("ticker")
    X["resid_b"] = X["r0"] - X["beta"] * rm0
    e, fitted, res, r2 = day0_model(X)
    X["resid"] = e
    X["day0_fitted"] = fitted
    X.attrs["day0"] = {"r2": r2, "coef": {k_: rnd(v[0]) for k_, v in res.items()}, "t": {k_: rnd(v[0] / v[1], 2) if v[1] else None for k_, v in res.items()}}
    X["size"] = np.log(X["mcap"].where(X["mcap"] > 0))
    X["liq"] = np.log(X["adtv"].where(X["adtv"] > 0))
    for c_ in Z_COLS:
        X[c_ + "_z"] = rank_normal(X[c_]).values
    X["lev_z"] = rank_normal(X["lev"].clip(-2, 8)).values
    X["value"] = X["ep_z"] + X["bp_z"]
    X.loc[X["ep"].isna() & X["bp"].isna(), "value"] = np.nan
    X["value_z"] = rank_normal(X["value"]).values
    return X


def design(X, cols, resid_col="resid"):
    mats, names = [np.ones(len(X))], ["const"]
    for c in cols:
        if c == "beta":
            v = X["beta"].values
        elif c == "resid":
            v = winsor(X[resid_col]).values
        elif c in ("resid_b", "r0"):
            v = winsor(X[c]).values
        elif c in DUMMIES:
            v = X[c].values
        else:
            v = X[c + "_z"].values
        mats.append(np.asarray(v, float))
        names.append(c)
    return np.column_stack(mats), names


# ---------------------------------------------------------------------------------------------- agregação
def fm(df_coef, clusters, min_n=2):
    """Fama-MacBeth: média dos coeficientes por dia (ingênuo) e por cluster (inferência honesta)."""
    out = {}
    cl = pd.Series(clusters, index=df_coef.index)
    by_c = df_coef.groupby(cl).mean()
    for col in df_coef.columns:
        d_ = df_coef[col].dropna()
        c_ = by_c[col].dropna()
        o = {}
        if len(d_) >= min_n:
            o["days"] = {"mean": rnd(d_.mean(), 5), "t": rnd(d_.mean() / (d_.std(ddof=1) / math.sqrt(len(d_))), 2) if d_.std(ddof=1) > 0 else None, "n": int(len(d_))}
        if len(c_) >= min_n:
            sd = c_.std(ddof=1)
            o["clusters"] = {"mean": rnd(c_.mean(), 5), "se": rnd(sd / math.sqrt(len(c_)), 5), "t": rnd(c_.mean() / (sd / math.sqrt(len(c_))), 2) if sd > 0 else None,
                             "n": int(len(c_)), "pct_pos": rnd((c_ > 0).mean(), 2), "per_cluster": {k: rnd(v, 5) for k, v in c_.items()}}
        out[col] = o
    return out


def shrink(mean, t):
    """Encolhimento positivo de James-Stein por coeficiente: b·max(0, 1 − 1/t²)."""
    if mean is None or t is None or not np.isfinite(t) or abs(t) <= 1:
        return 0.0
    return float(mean) * max(0.0, 1 - 1 / (t * t))


def wfm(byc, wfun):
    """Fama-MacBeth ponderado por cluster: {coluna: (média, t, n_clusters)}."""
    w = np.array([wfun(c) for c in byc.index], float)
    out = {}
    for col in byc.columns:
        v = byc[col].values.astype(float)
        m = np.isfinite(v) & (w > 0)
        n = int(m.sum())
        if n == 0:
            out[col] = (np.nan, np.nan, 0)
            continue
        ww = w[m] / w[m].sum()
        mean = float((ww * v[m]).sum())
        t = np.nan
        if n >= 2:
            se = math.sqrt(float((ww ** 2 * (v[m] - mean) ** 2).sum()) * n / (n - 1))
            t = mean / se if se > 0 else np.nan
        out[col] = (mean, t, n)
    return out


def wmean(series, wfun):
    w = np.array([wfun(c) for c in series.index], float)
    m = (w > 0) & np.isfinite(series.values)
    return float((series.values[m] * w[m]).sum() / w[m].sum()) if m.any() else np.nan


def spearman(a, b):
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 8 or np.std(a[m]) == 0 or np.std(b[m]) == 0:
        return np.nan
    return float(sps.spearmanr(a[m], b[m]).correlation)


# ---------------------------------------------------------------------------------------------- principal
def main(cot_path=None, raw_b3=None):
    cot_path = Path(cot_path or RAW / "work" / "cotahist.csv.gz")
    raw_b3 = Path(raw_b3 or RAW / "raw" / "b3")
    OUT.mkdir(parents=True, exist_ok=True)
    sup = json.load(open(raw_b3 / "supplement.json"))
    det = json.load(open(raw_b3 / "details.json"))
    idx = json.load(open(raw_b3 / "indices.json"))
    hist = load_hist()
    cov_rows = json.load(open(ROOT / "research" / "_coverage.json"))["coverage"]
    cov = [r["ticker"] for r in cov_rows]
    overview = json.load(open(ROOT / "data" / "app" / "overview.json"))
    ov = {c["ticker"]: c for c in overview["companies"]}
    mkt = json.load(open(ROOT / "data" / "market" / "_market.json"))
    print("carregando COTAHIST…", flush=True)
    P, R_raw, V, last_tk, recent, events, chains = load_panel(cot_path, sup)
    print("cadeias costuradas:", len(chains), "|", "; ".join(" → ".join(c.split(":")[0] for c in v) for v in list(chains.values())[:60]), flush=True)
    cal = P.index
    ibov = pd.Series({pd.Timestamp(d): v for d, v in idx["IBOV"]}).sort_index()
    ibov = ibov[~ibov.index.duplicated()].reindex(cal).ffill()
    mret = ibov.pct_change(fill_method=None)
    print("painel:", P.shape, cal[0].date(), cal[-1].date(), flush=True)

    # universo principal: tickers com fundamentos CVM -> ISIN atual
    isin_tk = {}
    for tk in hist:
        if tk in recent.index and recent[tk] in P.columns:
            isin_tk[recent[tk]] = tk

    # episódios
    r_all = mret[mret.index >= "2016-01-01"]
    crash_days = [d for d, v in r_all.items() if v <= CRASH_THR]
    listing = [{"date": d.strftime("%Y-%m-%d"), "ibov_ret": rnd(mret[d]), "label": LABELS.get(d.strftime("%Y-%m-%d"), ""),
                "used": d >= pd.Timestamp("2017-01-01")} for d in crash_days]
    ep_days = sorted([d for d in crash_days if d >= pd.Timestamp("2017-01-01")] + [pd.Timestamp(x) for x in EXTRA_DAYS])
    clusters, last, cid = [], None, None
    for d in ep_days:
        if last is None or (d - last).days > 45:
            cid = CLUSTER_NAMES.get(d.strftime("%Y-%m"), d.strftime("%Y-%m"))
        clusters.append(cid)
        last = d
    ep_cluster = dict(zip(ep_days, clusters))

    # ------------------------------------------------------------------ seções cruzadas históricas
    secs, ep_meta = {}, []
    Pf_all = P.ffill()
    for d in ep_days:
        k = cal.get_loc(d)
        X = build_cross_section(k, d, P, R_raw, V, mret, mret.iloc[k], isin_tk, hist, det, events)
        kt = int(np.argmin(ibov.iloc[k:k + 64].values)) + k
        for hn, h in H.items():
            for base, kk in (("t0", k), ("trough", kt)):
                if kk + h < len(cal):
                    X[f"f_{base}_{hn}"] = (Pf_all[X["isin"]].iloc[kk + h].values / Pf_all[X["isin"]].iloc[kk].values - 1)
                else:
                    X[f"f_{base}_{hn}"] = np.nan
        for h in PHI_H:
            X[f"phi_{h}"] = Pf_all[X["isin"]].iloc[k + h].values / Pf_all[X["isin"]].iloc[k].values - 1 if k + h < len(cal) else np.nan
        # retorno até o fundo e delistagem dentro de 12m
        X["to_trough"] = Pf_all[X["isin"]].iloc[kt].values / Pf_all[X["isin"]].iloc[k].values - 1
        last_obs = P[X["isin"]].iloc[k:k + 253].notna()[::-1].idxmax()
        X["stopped_12m"] = [(last_obs[i] < cal[min(k + 252, len(cal) - 1)] - pd.Timedelta(days=10)) for i in X["isin"]]
        X.attrs["k"], X.attrs["kt"] = k, kt
        secs[d] = X
        ib = {hn: rnd(ibov.iloc[k + h] / ibov.iloc[k] - 1) if k + h < len(cal) else None for hn, h in H.items()}
        ibt = {hn: rnd(ibov.iloc[kt + h] / ibov.iloc[kt] - 1) if kt + h < len(cal) else None for hn, h in H.items()}
        ew = {hn: rnd(np.nanmean(X[f"f_t0_{hn}"])) for hn in H}
        ep_meta.append({"date": d.strftime("%Y-%m-%d"), "label": LABELS.get(d.strftime("%Y-%m-%d")) or EXTRA_DAYS.get(d.strftime("%Y-%m-%d"), ""),
                        "cluster": ep_cluster[d], "ibov_ret": rnd(mret.iloc[k]), "n_stocks": int(len(X)), "n_fund": int(X["ep"].notna().sum()),
                        "trough_date": cal[kt].strftime("%Y-%m-%d"), "trough_lag": int(kt - k), "ibov_t0_to_trough": rnd(ibov.iloc[kt] / ibov.iloc[k] - 1),
                        "ibov_fwd": ib, "ibov_fwd_from_trough": ibt, "ew_universe_fwd": ew,
                        "cross_sd_r0": rnd(X["r0"].std()), "cross_sd_resid": rnd(X["resid"].std()), "day0_model": X.attrs["day0"],
                        "fund_dates": {"flow_end_mode": X["flow_end"].mode().iloc[0] if X["flow_end"].notna().any() else None,
                                       "bal_end_mode": X["bal_end"].mode().iloc[0] if X["bal_end"].notna().any() else None}})
        print(d.date(), ep_cluster[d], "n=", len(X), "r2 day0=", round(X.attrs["day0"]["r2"], 3), flush=True)

    days_idx = [d.strftime("%Y-%m-%d") for d in ep_days]
    cl_series = [ep_cluster[d] for d in ep_days]

    # ------------------------------------------------------------------ regressões cross-section (multivariada)
    def run_reg(base, cols, hn, resid_col="resid", subset=None):
        rows, r2s, sds = {}, [], []
        for d in ep_days:
            X = secs[d]
            if subset is not None:
                X = X[subset(X)]
            y = X[f"f_{base}_{hn}"]
            m = y.notna()
            if m.sum() < 25:
                continue
            Xm = X[m]
            A, names = design(Xm, cols, resid_col)
            res, r2, sd, _ = ols_hc3(winsor(y[m]).values, A, names)
            rows[d.strftime("%Y-%m-%d")] = {k_: v[0] for k_, v in res.items()}
            rows[d.strftime("%Y-%m-%d") + "_t"] = {k_: (v[0] / v[1] if v[1] else np.nan) for k_, v in res.items()}
            r2s.append(r2)
            sds.append(sd)
        coef = pd.DataFrame({k_: v for k_, v in rows.items() if not k_.endswith("_t")}).T
        tt = pd.DataFrame({k_[:-2]: v for k_, v in rows.items() if k_.endswith("_t")}).T
        cls = [ep_cluster[pd.Timestamp(x)] for x in coef.index]
        return coef, tt, cls, (float(np.nanmean(r2s)) if r2s else None), (float(np.nanmean(sds)) if sds else None)

    regs = {}
    coef_store = {}
    for base in ("t0", "trough"):
        regs[base] = {}
        for hn in H:
            coef, tt, cls, r2m, sdm = run_reg(base, FWD_COLS, hn)
            if coef.empty:
                continue
            coef_store[(base, hn)] = (coef, cls, sdm)
            regs[base][hn] = {"n_episodes": int(len(coef)), "n_clusters": int(len(set(cls))), "avg_r2": rnd(r2m, 3), "avg_resid_sd": rnd(sdm),
                              "fm": fm(coef, cls),
                              "per_episode": {d: {"coef": {k_: rnd(v, 4) for k_, v in coef.loc[d].items()},
                                                  "t_hc3": {k_: rnd(v, 2) for k_, v in tt.loc[d].items()}} for d in coef.index}}

    regs["t0_ep_bp"] = {}
    for hn in H:
        coef, tt, cls, r2m, sdm = run_reg("t0", FWD_COLS_EP, hn)
        if not coef.empty:
            regs["t0_ep_bp"][hn] = {"n_episodes": int(len(coef)), "avg_r2": rnd(r2m, 3), "fm": fm(coef, cls)}

    # ------------------------------------------------------------------ univariado (inclinação e IC de Spearman)
    univ = {}
    for base in ("t0", "trough"):
        univ[base] = {}
        for hn in H:
            ics, sl = {c: {} for c in UNI_COLS}, {c: {} for c in UNI_COLS}
            for d in ep_days:
                X = secs[d]
                y = X[f"f_{base}_{hn}"]
                m = y.notna()
                if m.sum() < 25:
                    continue
                for c in UNI_COLS:
                    A, names = design(X[m], [c] if c not in ("resid_b", "r0") else [c])
                    res, _, _, _ = ols_hc3(winsor(y[m]).values, A, names)
                    sl[c][d.strftime("%Y-%m-%d")] = res[c][0]
                    raw = X[m][c].astype(float).values if c not in ("lev",) else X[m]["lev"].clip(-2, 8).astype(float).values
                    ics[c][d.strftime("%Y-%m-%d")] = spearman(raw, y[m].values)
            ic_df = pd.DataFrame(ics)
            sl_df = pd.DataFrame(sl)
            if ic_df.empty:
                continue
            cls = [ep_cluster[pd.Timestamp(x)] for x in ic_df.index]
            univ[base][hn] = {"ic": fm(ic_df, cls), "slope": fm(sl_df, cls)}

    # ------------------------------------------------------------------ reversão: φ(h)
    phi = {}
    phi_b = {}
    for h in PHI_H:
        rows, rows_b = {}, {}
        for d in ep_days:
            X = secs[d]
            y = X[f"phi_{h}"]
            m = y.notna()
            if m.sum() < 25:
                continue
            A, names = design(X[m], ["beta", "resid"])
            res, _, _, _ = ols_hc3(winsor(y[m]).values, A, names)
            rows[d.strftime("%Y-%m-%d")] = {"phi": res["resid"][0], "t": res["resid"][0] / res["resid"][1] if res["resid"][1] else np.nan}
            A, names = design(X[m], ["beta", "resid_b"])
            res, _, _, _ = ols_hc3(winsor(y[m]).values, A, names)
            rows_b[d.strftime("%Y-%m-%d")] = {"phi": res["resid_b"][0]}
        dfp = pd.DataFrame(rows).T
        dfb = pd.DataFrame(rows_b).T
        cls = [ep_cluster[pd.Timestamp(x)] for x in dfp.index]
        phi[h] = fm(dfp[["phi"]], cls)["phi"]
        phi_b[h] = fm(dfb[["phi"]], [ep_cluster[pd.Timestamp(x)] for x in dfb.index])["phi"]

    # caminho do quintil de maior resíduo negativo vs universo (peso igual), por cluster
    qpath = {}
    for d in ep_days:
        X = secs[d]
        k = X.attrs["k"]
        n_av = min(252, len(cal) - 1 - k)
        sub = Pf_all[X["isin"]].iloc[k:k + n_av + 1]
        rel = sub / sub.iloc[0]
        q = pd.qcut(X["resid"].rank(method="first"), 5, labels=False)
        lo = rel.loc[:, (q == 0).values].mean(1).values
        hi = rel.loc[:, (q == 4).values].mean(1).values
        allm = rel.mean(1).values
        qpath[d] = {"q1_minus_all": lo - allm, "q1_minus_q5": lo - hi}
    path_by_cluster = {}
    for c in sorted(set(cl_series), key=lambda x: cl_series.index(x)):
        ds = [d for d in ep_days if ep_cluster[d] == c]
        L = min(len(qpath[d]["q1_minus_all"]) for d in ds)
        path_by_cluster[c] = np.mean([qpath[d]["q1_minus_all"][:L] for d in ds], axis=0)
    Lmin = min(len(v) for v in path_by_cluster.values())
    avg_path = np.mean([v[:Lmin] for v in path_by_cluster.values()], axis=0)
    sel_days = [0, 1, 2, 5, 10, 21, 42, 63, 126, 189, 252]
    qpath_out = {"avg_q1_minus_all": {str(t): rnd(avg_path[t]) for t in sel_days if t < Lmin},
                 "per_cluster": {c: {str(t): rnd(v[t]) for t in sel_days if t < len(v)} for c, v in path_by_cluster.items()},
                 "peak_day": int(np.argmax(avg_path)), "peak_value": rnd(avg_path.max())}

    # ------------------------------------------------------------------ estratégias de cesta
    strat_defs = {
        "resid_neg": ("Quintil de maior resíduo negativo (contra fatores)", lambda X: X["resid"], "low", None),
        "resid_b_neg": ("Quintil de maior resíduo negativo (contra beta)", lambda X: X["resid_b"], "low", None),
        "fall_abs": ("Maior queda absoluta no dia", lambda X: X["r0"], "low", None),
        "cheap": ("Mais barato (E/P + B/P)", lambda X: X["ep_z"] + X["bp_z"], "high", lambda X: X["ep"].notna()),
        "quality": ("Maior qualidade (ROE)", lambda X: X["roe"], "high", lambda X: X["roe"].notna()),
        "low_lev": ("Menor alavancagem (DL/EBITDA, não financeiras)", lambda X: X["lev"], "low", lambda X: X["lev"].notna()),
        "high_beta": ("Maior beta de baixa", lambda X: X["beta"], "high", None),
        "low_beta": ("Menor beta de baixa", lambda X: X["beta"], "low", None),
    }
    strat = {}
    for key, (label, fn, side, filt) in strat_defs.items():
        per = {}
        for d in ep_days:
            X = secs[d]
            if filt is not None:
                X = X[filt(X)]
            s = fn(X).astype(float)
            q = pd.qcut(s.rank(method="first"), 5, labels=False)
            pick = X[(q == 0) if side == "low" else (q == 4)]
            other = X[(q == 4) if side == "low" else (q == 0)]
            k = secs[d].attrs["k"]
            n_av = min(252, len(cal) - 1 - k)
            sub = Pf_all[pick["isin"]].iloc[k:k + n_av + 1]
            path = (sub / sub.iloc[0]).mean(1).values
            sub_o = Pf_all[other["isin"]].iloc[k:k + n_av + 1]
            path_o = (sub_o / sub_o.iloc[0]).mean(1).values
            ib = (ibov.iloc[k:k + n_av + 1] / ibov.iloc[k]).values
            row = {"n": int(len(pick)), "members": sorted(pick.index.tolist())}
            for hn, h in H.items():
                if h <= n_av:
                    row[f"ret_{hn}"] = rnd(path[h] - 1)
                    row[f"ibov_{hn}"] = rnd(ib[h] - 1)
                    row[f"excess_{hn}"] = rnd(path[h] - ib[h])
                    row[f"ls_{hn}"] = rnd(path[h] - path_o[h])
            row["mdd_12m"] = rnd(max_dd(path[1:]))
            row["ibov_mdd_12m"] = rnd(max_dd(ib[1:]))
            row["min_ret_path"] = rnd(path.min() - 1)
            per[d.strftime("%Y-%m-%d")] = row
        agg = {}
        dfp = pd.DataFrame(per).T
        cls = [ep_cluster[pd.Timestamp(x)] for x in dfp.index]
        for col in [c for c in dfp.columns if c.startswith(("ret_", "excess_", "ls_", "ibov_", "mdd", "min_"))]:
            v = pd.to_numeric(dfp[col], errors="coerce")
            byc = v.groupby(cls).mean().dropna()
            agg[col] = {"mean_clusters": rnd(byc.mean()), "pct_pos_clusters": rnd((byc > 0).mean(), 2) if col.startswith(("excess", "ls")) else None,
                        "per_cluster": {k_: rnd(x) for k_, x in byc.items()}, "mean_days": rnd(v.mean())}
        strat[key] = {"label": label, "aggregate": agg, "per_episode": per}

    # ------------------------------------------------------------------ viés de sobrevivência: universo amplo
    alive = P[P.index >= "2026-09-01"].notna().any()
    surv = {}
    rows_b, rows_s = {}, {}
    nonsurv_gap = {}
    for d in ep_days:
        k = cal.get_loc(d)
        pres = P.iloc[max(0, k - 63):k].notna().mean()
        cols = [c for c in P.columns if pres[c] >= 0.9 and np.isfinite(P[c].iloc[k])]
        mc = market_chars(P, V, mret, k, cols)
        mc = mc[np.isfinite(mc.beta)]
        mc["issuer"] = [c[2:6] for c in mc.index]
        mc = mc.sort_values("adtv", ascending=False).drop_duplicates("issuer").head(150)
        prev = Pf_all[mc.index].iloc[k - 1].values
        mc["r0"] = Pf_all[mc.index].iloc[k].values / prev - 1
        mc["resid_b"] = mc["r0"] - mc["beta"].clip(-0.5, 3) * mret.iloc[k]
        mc["beta"] = mc["beta"].clip(-0.5, 3)
        mc["mom_z"] = rank_normal(mc["mom"]).values
        mc["liq_z"] = rank_normal(np.log(mc["adtv"].clip(lower=1))).values
        mc["surv"] = [bool(alive.get(c, False)) for c in mc.index]  # ainda negociada em set–out/2026
        h = H["6m"]
        if k + h >= len(cal):
            continue
        y = pd.Series(Pf_all[mc.index].iloc[k + h].values / Pf_all[mc.index].iloc[k].values - 1, index=mc.index)
        nonsurv_gap[d.strftime("%Y-%m-%d")] = {"n": int(len(mc)), "n_surv": int(mc.surv.sum()),
                                               "mean_6m_surv": rnd(y[mc.surv].mean()), "mean_6m_nonsurv": rnd(y[~mc.surv].mean())}
        for tag, sub in (("broad", mc), ("surv", mc[mc.surv])):
            ys = y[sub.index]
            A = np.column_stack([np.ones(len(sub)), sub["beta"].values, winsor(sub["resid_b"]).values, sub["mom_z"].values, sub["liq_z"].values])
            res, _, _, _ = ols_hc3(winsor(ys).values, A, ["const", "beta", "resid_b", "mom", "liq"])
            (rows_b if tag == "broad" else rows_s)[d.strftime("%Y-%m-%d")] = {k_: v[0] for k_, v in res.items()}
    cb, cs_ = pd.DataFrame(rows_b).T, pd.DataFrame(rows_s).T
    surv = {"horizon": "6m", "model": "r_6m ~ beta_baixa + resid_beta + momentum + liquidez (top 150 emissores por ADTV, inclui deslistadas)",
            "broad": fm(cb, [ep_cluster[pd.Timestamp(x)] for x in cb.index]),
            "survivors_only": fm(cs_, [ep_cluster[pd.Timestamp(x)] for x in cs_.index]),
            "return_gap": nonsurv_gap}

    # ------------------------------------------------------------------ validação LOCO do modelo combinado (6m e 12m)
    loco = {}
    for hn in ("3m", "6m", "12m"):
        coef, cls, _ = coef_store[("t0", hn)]
        res_c, res_r = {}, {}
        byc_all = coef.groupby(cls).mean()
        for c in sorted(set(cls)):
            train = coef[[x != c for x in cls]]
            tcls = [x for x in cls if x != c]
            fmt = fm(train, tcls)
            b = {nm: shrink((fmt[nm].get("clusters") or {}).get("mean"), (fmt[nm].get("clusters") or {}).get("t")) for nm in coef.columns}
            st_r = wfm(byc_all.drop(index=c), REGIMES["recomendado"])
            b_r = {nm: shrink(st_r[nm][0], st_r[nm][1]) for nm in coef.columns}
            ics, spreads, ics_r, spreads_r = [], [], [], []
            for d in [pd.Timestamp(x) for x, cc in zip(coef.index, cls) if cc == c]:
                X = secs[d]
                y = X[f"f_t0_{hn}"]
                m = y.notna()
                A, names = design(X[m], FWD_COLS)
                for bb, li, ls in ((b, ics, spreads), (b_r, ics_r, spreads_r)):
                    pred = A @ np.array([bb.get(nm, 0.0) if nm != "const" else 0.0 for nm in names])
                    li.append(spearman(pred, y[m].values))
                    q = pd.qcut(pd.Series(pred).rank(method="first"), 5, labels=False).values
                    ls.append(float(np.mean(y[m].values[q == 4]) - np.mean(y[m].values[q == 0])))
            res_c[c] = {"ic": rnd(np.nanmean(ics), 3), "q5_minus_q1": rnd(np.nanmean(spreads))}
            res_r[c] = {"ic": rnd(np.nanmean(ics_r), 3), "q5_minus_q1": rnd(np.nanmean(spreads_r))}
        loco[hn] = {}
        for tag, rc in (("todos", res_c), ("recomendado", res_r)):
            loco[hn][tag] = {"per_cluster": rc, "mean_ic": rnd(np.nanmean([v["ic"] for v in rc.values() if v["ic"] is not None]), 3),
                             "mean_q5_q1": rnd(np.nanmean([v["q5_minus_q1"] for v in rc.values() if v["q5_minus_q1"] is not None])),
                             "pct_clusters_ic_pos": rnd(np.mean([(v["ic"] or 0) > 0 for v in rc.values()]), 2),
                             "mean_ic_political": rnd(np.nanmean([v["ic"] for k_, v in rc.items() if k_ in POLITICAL and v["ic"] is not None]), 3)}

    # ------------------------------------------------------------------ hoje (26/10/2026)
    rm0_today = mkt["ibov_today"]["chg"]
    r0_today, today_ref = {}, {}
    for tk in hist:
        f = ROOT / "data" / "market" / f"{tk}.json"
        if f.exists():
            st = json.load(open(f)).get("stats") or {}
            t_ = st.get("today") or {}
            if t_.get("chg") is not None:
                r0_today[tk] = float(t_["chg"])
                today_ref[tk] = {"beta_down_3y": st.get("beta_down_3y"), "residual_mkt": t_.get("residual"), "xsec_residual_mkt": t_.get("xsec_residual")}
    k_today = len(cal)
    P_ext = pd.concat([P, pd.DataFrame(index=[mk.TODAY], columns=P.columns, dtype=float)])
    R_ext = pd.concat([R_raw, pd.DataFrame(index=[mk.TODAY], columns=R_raw.columns, dtype=float)])
    V_ext = pd.concat([V, pd.DataFrame(index=[mk.TODAY], columns=V.columns, dtype=float)])
    m_ext = pd.concat([mret, pd.Series([rm0_today], index=[mk.TODAY])])
    # prioriza a classe da cobertura no desempate por emissor
    isin_tk_today = dict(isin_tk)
    XT = build_cross_section(k_today, mk.TODAY, P_ext, R_ext, V_ext, m_ext, rm0_today, isin_tk_today, hist, det, events, r0_override=r0_today, min_adtv=0)
    for tk in cov:
        if tk not in XT.index:
            print("aviso: cobertura fora da seção cruzada de hoje:", tk)
    # se a classe da cobertura perdeu o desempate (BBDC4 x BBDC3), reconstrói com a classe da cobertura
    lost = [tk for tk in cov if tk not in XT.index and tk in hist]
    if lost:
        drop_iss = {recent[t][2:6] for t in lost if t in recent.index}
        keep = {i: t for i, t in isin_tk.items() if i[2:6] not in drop_iss or t in lost}
        XT = build_cross_section(k_today, mk.TODAY, P_ext, R_ext, V_ext, m_ext, rm0_today, keep, hist, det, events, r0_override=r0_today, min_adtv=0)
    print("hoje: n=", len(XT), "day0 r2=", round(XT.attrs["day0"]["r2"], 3), flush=True)
    resid_rng = pd.concat([secs[d]["resid"] for d in ep_days])
    lo_r, hi_r = float(resid_rng.quantile(0.005)), float(resid_rng.quantile(0.995))

    def cl_mean(key, hn):
        v = pd.Series({m_["date"]: m_[key][hn] for m_ in ep_meta if m_[key][hn] is not None}, dtype=float)
        return v.groupby([ep_cluster[pd.Timestamp(x)] for x in v.index]).mean()

    ibov_cl = {hn: cl_mean("ibov_fwd", hn) for hn in H}
    ew_cl = {hn: cl_mean("ew_universe_fwd", hn) for hn in H}
    ibov_fwd_cl = {hn: {"by_regime": {rg: rnd(wmean(ibov_cl[hn], f)) for rg, f in REGIMES.items()},
                        "ew_universe_by_regime": {rg: rnd(wmean(ew_cl[hn], f)) for rg, f in REGIMES.items()},
                        "per_cluster": {c: rnd(v) for c, v in ibov_cl[hn].items()},
                        "ew_per_cluster": {c: rnd(v) for c, v in ew_cl[hn].items()}} for hn in H}

    XTc = XT.copy()
    XTc["resid"] = XTc["resid"].clip(lo_r, hi_r)
    A, names = design(XTc, FWD_COLS)
    A[:, names.index("resid")] = XTc["resid"].values  # resíduo de hoje cortado na faixa histórica (não winsorizado de novo)
    Ac = A - A.mean(axis=0, keepdims=True)  # componente relativo: desvio em relação à média da seção cruzada de hoje
    Ac[:, 0] = 0.0
    preds, model_used = {}, {}
    for hn in ("3m", "6m", "12m"):
        coef, cls, sdm = coef_store[("t0", hn)]
        byc = coef.groupby(cls).mean()
        mods = {}
        for rg, wf in REGIMES.items():
            stt = wfm(byc, wf)
            central = rg in ("todos", "recomendado")
            b = {nm: (shrink(stt[nm][0], stt[nm][1]) if central else (stt[nm][0] if np.isfinite(stt[nm][0]) else 0.0)) for nm in names}
            b["const"] = 0.0
            lvl = wmean(ew_cl[hn], wf)
            mods[rg] = {"b": b, "level": lvl, "ibov": wmean(ibov_cl[hn], wf),
                        "stats": {nm: {"mean": rnd(stt[nm][0], 5), "t": rnd(stt[nm][1], 2), "n": stt[nm][2], "used": rnd(b[nm], 5)} for nm in names if nm != "const"}}
        # cenários por cluster (coeficientes brutos do cluster + nível do cluster) -> dispersão do intervalo
        scen = {}
        for c in byc.index:
            bc = np.nan_to_num(byc.loc[c, names].values.astype(float))
            bc[0] = 0.0
            scen[c] = ew_cl[hn].get(c, np.nan) + Ac @ bc
        scen = pd.DataFrame(scen, index=XTc.index)
        rel_scen = scen.sub(pd.Series({c: ibov_cl[hn].get(c, np.nan) for c in scen.columns}), axis=1)
        out = {}
        for rg, md in mods.items():
            bvec = np.array([md["b"][nm] for nm in names])
            out[rg] = pd.Series(md["level"] + Ac @ bvec, index=XTc.index)
        sd_scen = scen.std(axis=1, ddof=1)
        sd_rel = rel_scen.std(axis=1, ddof=1)
        mu = out["recomendado"]
        sd_pred = np.sqrt(sd_scen ** 2 + (sdm or 0) ** 2)
        sd_pred_rel = np.sqrt(sd_rel ** 2 + (sdm or 0) ** 2)
        bvec = np.array([mods["recomendado"]["b"][nm] for nm in names])
        contrib = {nm: pd.Series(Ac[:, j] * bvec[j], index=XTc.index) for j, nm in enumerate(names) if nm != "const"}
        preds[hn] = {"mu": mu, "regimes": out, "lo80": mu - 1.2816 * sd_pred, "hi80": mu + 1.2816 * sd_pred,
                     "rel": mu - mods["recomendado"]["ibov"], "rel_lo80": mu - mods["recomendado"]["ibov"] - 1.2816 * sd_pred_rel,
                     "rel_hi80": mu - mods["recomendado"]["ibov"] + 1.2816 * sd_pred_rel, "scen": scen, "contrib": contrib}
        model_used[hn] = {rg: {"level_ew": rnd(md["level"]), "ibov": rnd(md["ibov"]), "coef": md["stats"]} for rg, md in mods.items()}
        model_used[hn]["resid_sd"] = rnd(sdm)

    # pesos recomendados do escore composto (z): IC de Spearman univariado médio de 3m e 6m a partir do choque, FM ponderado
    # (crises políticas com peso 2), encolhido por max(0, 1 − 1/t²) e normalizado para soma |w| = 1
    ic6 = pd.DataFrame({c: (univ["t0"]["6m"]["ic"].get(c, {}).get("clusters") or {}).get("per_cluster", {}) for c in SCORE_COLS})
    ic3 = pd.DataFrame({c: (univ["t0"]["3m"]["ic"].get(c, {}).get("clusters") or {}).get("per_cluster", {}) for c in SCORE_COLS})
    w_tab, raw_w = {}, {}
    for c in SCORE_COLS:
        row = {}
        for rg, wf in REGIMES.items():
            st6 = wfm(ic6[[c]], wf)[c]
            row[f"ic6_{rg}"] = rnd(st6[0], 3)
            row[f"t6_{rg}"] = rnd(st6[1], 2)
        st3 = wfm(ic3[[c]], REGIMES["recomendado"])[c]
        row["ic3_recomendado"], row["t3_recomendado"] = rnd(st3[0], 3), rnd(st3[1], 2)
        icb = pd.concat([ic3[c], ic6[c]], axis=1).mean(axis=1, skipna=True).to_frame(c)  # IC médio 3m–6m por crise
        st = wfm(icb, REGIMES["recomendado"])[c]
        row["ic36_recomendado"], row["t36_recomendado"] = rnd(st[0], 3), rnd(st[1], 2)
        raw_w[c] = shrink(st[0], st[1])
        w_tab[c] = row
    tot = sum(abs(v) for v in raw_w.values()) or 1.0
    weights = {c: rnd(v / tot, 3) for c, v in raw_w.items()}
    for c in w_tab:
        w_tab[c]["weight"] = weights[c]

    def zcol(c):
        if c in ("resid", "beta"):
            return rank_normal(XT[c])
        if c in DUMMIES:
            v = XT[c].astype(float)
            return (v - v.mean()) / (v.std() or 1.0)
        return XT[c + "_z"]
    score = sum(weights[c] * zcol(c) for c in weights if weights[c])
    score = score if isinstance(score, pd.Series) else pd.Series(0.0, index=XT.index)

    rank_rows = []
    for tk in cov:
        if tk not in XT.index:
            continue
        x = XT.loc[tk]
        row = {"ticker": tk, "name": ov.get(tk, {}).get("name"), "group": ov.get(tk, {}).get("group"), "setor": x["setor"],
               "r0_today": rnd(x["r0"]), "beta_down": rnd(x["beta"], 3), "resid_beta": rnd(x["resid_b"]), "resid_factor": rnd(x["resid"]),
               "resid_factor_mkt_json": rnd((today_ref.get(tk) or {}).get("xsec_residual_mkt")),
               "ep": rnd(x["ep"]), "bp": rnd(x["bp"]), "roe": rnd(x["roe"]), "nd_ebitda": rnd(x["lev"], 2), "mcap_mn": rnd(x["mcap"], 0),
               "adtv_mn": rnd(x["adtv"] / 1e6, 1), "mom_12_1": rnd(x["mom"]), "state": bool(x["state"]), "exporter": bool(x["exporter"]),
               "financial": bool(x["financial"]), "fund_dates": [x["flow_end"], x["bal_end"]],
               "value_z": rnd(x["value_z"], 2), "mom_z": rnd(x["mom_z"], 2), "size_z": rnd(x["size_z"], 2)}
        for hn in ("3m", "6m", "12m"):
            p_ = preds[hn]
            row[f"exp_{hn}"] = rnd(p_["mu"][tk])
            row[f"lo80_{hn}"], row[f"hi80_{hn}"] = rnd(p_["lo80"][tk]), rnd(p_["hi80"][tk])
            row[f"exp_{hn}_vs_ibov"] = rnd(p_["rel"][tk])
            row[f"lo80_{hn}_vs_ibov"], row[f"hi80_{hn}_vs_ibov"] = rnd(p_["rel_lo80"][tk]), rnd(p_["rel_hi80"][tk])
            row[f"regimes_{hn}"] = {rg: rnd(v[tk]) for rg, v in p_["regimes"].items()}
            row[f"scenarios_{hn}"] = {c: rnd(v) for c, v in p_["scen"].loc[tk].items()}
        row["contrib_6m"] = {nm: rnd(v[tk]) for nm, v in preds["6m"]["contrib"].items()}
        row["crisis_score_z"] = rnd(score[tk], 3)
        o = ov.get(tk, {})
        row["valuation_ref"] = {"upside": o.get("upside"), "irr_implied": o.get("irr_implied"), "rank_multifator": o.get("rank")}
        rank_rows.append(row)
    for hn in ("6m", "12m"):
        for i, r in enumerate(sorted(rank_rows, key=lambda r: -(r[f"exp_{hn}"] if r[f"exp_{hn}"] is not None else -9)), 1):
            r[f"rank_{hn}"] = i
    rank_rows.sort(key=lambda r: -(r["exp_3m"] if r["exp_3m"] is not None else -9))  # ranking principal: 3m (melhor LOCO)
    for i, r in enumerate(rank_rows, 1):
        r["rank_crisis"] = i
    for key in ("crisis_score_z",):
        for i, r in enumerate(sorted(rank_rows, key=lambda r: -(r[key] if r[key] is not None else -9)), 1):
            r["rank_score_z"] = i
    for rg in ("panico", "eleitoral"):
        for i, r in enumerate(sorted(rank_rows, key=lambda r: -(r["regimes_3m"][rg] if r["regimes_3m"][rg] is not None else -9)), 1):
            r[f"rank_{rg}"] = i
    rk = pd.DataFrame([{k_: r[k_] for k_ in ("rank_crisis", "rank_6m", "rank_12m", "rank_score_z", "rank_panico", "rank_eleitoral")} for r in rank_rows])
    rank_corr = {c: rnd(sps.spearmanr(rk["rank_crisis"], rk[c]).correlation, 2) for c in rk.columns if c != "rank_crisis"}

    # correlação do resíduo de hoje com o de _market.json
    cmp_ = XT.join(pd.DataFrame(today_ref).T, how="left")
    corr_resid = spearman(cmp_["resid"].astype(float).values, pd.to_numeric(cmp_["xsec_residual_mkt"], errors="coerce").values)
    cov_set = [t for t in cov if t in XT.index]

    today_out = {"date": mk.TODAY.strftime("%Y-%m-%d"), "ibov_chg": rm0_today, "n_cross_section": int(len(XT)),
                 "day0_model": XT.attrs["day0"], "resid_hist_clip": [rnd(lo_r), rnd(hi_r)], "spearman_resid_vs_market_json": rnd(corr_resid, 3),
                 "cross_sd_r0": rnd(XT["r0"].std()), "cross_sd_resid": rnd(XT["resid"].std()),
                 "coverage_mean_resid": rnd(XT.loc[cov_set, "resid"].mean()), "coverage_share_resid_below_hist": rnd((XT.loc[cov_set, "resid"] < lo_r).mean(), 2),
                 "regimes": {k_: sorted(c for c in sorted(set(cl_series)) if f(c) > 0) for k_, f in REGIMES.items()},
                 "regime_weights": {k_: {c: f(c) for c in sorted(set(cl_series))} for k_, f in REGIMES.items()},
                 "ibov_fwd_hist": ibov_fwd_cl, "model": model_used, "weights_score_z": weights, "weights_table": w_tab,
                 "ranking_horizon": "3m", "rank_spearman_vs_3m": rank_corr, "ranking": rank_rows}

    result = {"generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "method": __doc__.strip().split("Método (resumo):")[1].strip(),
              "inputs": {"cotahist": str(cot_path), "raw_b3": str(raw_b3), "panel": [cal[0].strftime("%Y-%m-%d"), cal[-1].strftime("%Y-%m-%d")],
                         "n_isins": int(P.shape[1])},
              "stitched_chains": chains,
              "crash_days_le_4pct": listing, "episodes": ep_meta, "clusters": sorted(set(cl_series), key=lambda x: cl_series.index(x)),
              "regressions": regs, "univariate": univ, "reversal": {"phi_factor_resid": {str(k_): v for k_, v in phi.items()},
                                                                    "phi_beta_resid": {str(k_): v for k_, v in phi_b.items()},
                                                                    "q1_resid_path": qpath_out},
              "strategies": {k_: {"label": v["label"], "aggregate": v["aggregate"], "per_episode": v["per_episode"]} for k_, v in strat.items()},
              "survivorship": surv, "loco": loco, "today": today_out}
    result = clean(result)
    json.dump(result, open(OUT / "crash_study.json", "w"), ensure_ascii=False, indent=1)
    write_md(result)
    print("ok:", OUT / "crash_study.json")


# ---------------------------------------------------------------------------------------------- relatório
def pct(x, n=1):
    return "—" if x is None else f"{x * 100:+.{n}f}%".replace(".", ",")


def num(x, n=2):
    return "—" if x is None else f"{x:.{n}f}".replace(".", ",")


def gx(d, *keys):
    for k in keys:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def regime_stat(per_cluster, rg):
    if not per_cluster:
        return None, None
    ser = pd.DataFrame({"v": pd.Series(per_cluster, dtype=float)})
    m, t, _ = wfm(ser, REGIMES[rg])["v"]
    return (m if np.isfinite(m) else None), (t if t is not None and np.isfinite(t) else None)


def ic_pc(R, base, h, c):
    return gx(R, "univariate", base, h, "ic", c, "clusters", "per_cluster") or {}


NAMES = {"beta": "Beta de baixa", "resid": "Resíduo do dia (fatores)", "resid_b": "Resíduo do dia (beta)", "r0": "Retorno do dia",
         "ep": "E/P", "bp": "B/P", "value": "Valor (E/P+B/P)", "roe": "ROE", "lev": "DL/EBITDA", "size": "Tamanho (log VM)",
         "liq": "Liquidez (log ADTV)", "mom": "Momentum 12−1", "exporter": "Exportadora", "financial": "Financeira", "state": "Estatal",
         "consumo": "Consumo cíclico", "utility": "Utilidade pública", "const": "Intercepto"}


def write_md(R):
    T = R["today"]
    cls = R["clusters"]
    S = R["strategies"]
    L = []
    A = L.append
    ib = T["ibov_fwd_hist"]
    phi = R["reversal"]["phi_factor_resid"]
    qp = R["reversal"]["q1_resid_path"]["avg_q1_minus_all"]
    agg = lambda k, c: gx(S, k, "aggregate", c, "mean_clusters")
    pcl = lambda k, c: gx(S, k, "aggregate", c, "per_cluster") or {}
    ppos = lambda k, c: gx(S, k, "aggregate", c, "pct_pos_clusters")
    ics = {c: {h: ic_pc(R, "t0", h, c) for h in H} for c in UNI_COLS}
    ict = {c: {h: ic_pc(R, "trough", h, c) for h in H} for c in UNI_COLS}
    rs = lambda c, h, rg: regime_stat(ics[c][h], rg)[0]
    lo3 = R["loco"]["3m"]["recomendado"]
    lo12 = R["loco"]["12m"]["recomendado"]
    sv = R["survivorship"]
    W = T["weights_score_z"]
    wt = T["weights_table"]
    n_days = len(R["episodes"])
    of_n = lambda frac: "—" if frac is None else f"{int(round(frac * len(cls)))} de {len(cls)}"
    neg_n = lambda c, h: sum(1 for v in ics[c][h].values() if v is not None and v < 0)
    first_of = {}
    for e in R["episodes"]:
        first_of.setdefault(e["cluster"], e)
    lags = [e["trough_lag"] for e in first_of.values()]
    top = T["ranking"][:10]
    w_in = {c: v for c, v in W.items() if c != "exporter" and v}
    tot_in = sum(abs(v) for v in w_in.values()) or 1
    w_ele_raw = {c: (wt[c].get("ic6_eleitoral") or 0) for c in wt}
    tot_ele = sum(abs(v) for v in w_ele_raw.values()) or 1

    A("# Estudo de crashes 2016–2026: o que previu a recuperação das ações brasileiras\n")
    A(f"Gerado em {R['generated_at']} por `pipeline/tests/crash_study.py` (reexecutável; ~1 min). Dados completos, por episódio e por ação, em `data/tests/crash_study.json`. "
      "Retornos de preço ajustados por desdobramentos/grupamentos (sem proventos). Estudo quantitativo, não é recomendação.\n")

    # ------------------------------------------------------------------ conclusões
    A("## Conclusões\n")
    A(f"1. **Amostra.** {n_days} dias de choque em {len(cls)} crises (2017–2025): todos os pregões com Ibovespa ≤ −4% desde 2017 "
      f"(16; o de 02/02/2016 ficou de fora por não ter um ano de histórico no COTAHIST) mais o pós-eleição de 31/10/2022. "
      f"São {min(e['n_stocks'] for e in R['episodes'])}–{max(e['n_stocks'] for e in R['episodes'])} ações por episódio, todas com fundamentos CVM point-in-time. "
      "A inferência honesta é por crise (n = 7, ou 6 em 12m), porque os 11 dias da Covid compartilham a mesma janela futura.")
    A(f"2. **Mercado.** Depois dos choques, o Ibovespa subiu em média {pct(gx(ib, '3m', 'by_regime', 'todos'))} em 3m, {pct(gx(ib, '6m', 'by_regime', 'todos'))} em 6m e "
      f"{pct(gx(ib, '12m', 'by_regime', 'todos'))} em 12m (média por crise). Nas crises de pânico o 6m foi {pct(gx(ib, '6m', 'by_regime', 'panico'))}; nas duas eleitorais "
      f"(2022 e dez/2025), {pct(gx(ib, '6m', 'by_regime', 'eleitoral'))}, com o universo de ações (peso igual) em {pct(gx(ib, '6m', 'ew_universe_by_regime', 'eleitoral'))}.")
    A("3. **O que previu a recuperação, comprando no fechamento do dia do choque:**")
    A(f"   - **A sobrerreação idiossincrática reverte, mas devagar.** O resíduo da queda contra fatores (beta, alavancagem, tamanho e setor) tem coeficiente φ de "
      f"{num(gx(phi, '5', 'clusters', 'mean'))} em 5 pregões (t {num(gx(phi, '5', 'clusters', 't'), 1)}), {num(gx(phi, '21', 'clusters', 'mean'))} em 1m, "
      f"{num(gx(phi, '63', 'clusters', 'mean'))} em 3m (t {num(gx(phi, '63', 'clusters', 't'), 1)}) e {num(gx(phi, '126', 'clusters', 'mean'))} em 6m "
      f"(t {num(gx(phi, '126', 'clusters', 't'), 1)}). Em média, cerca de 2/3 da queda \"excessiva\" volta em 3 meses e toda ela em 6 meses (φ ≤ −1: os perdedores passam a ganhar). Quase nada volta na primeira semana. "
      f"O IC de Spearman é {num(rs('resid', '3m', 'todos'), 3)} em 3m e {num(rs('resid', '6m', 'todos'), 3)} em 6m, negativo em {neg_n('resid', '6m')} das {len(cls)} crises em 6m. "
      f"A cesta do quintil de resíduo mais negativo bateu o universo em {pct(qp.get('63'))} em 3m e {pct(qp.get('126'))} em 6m. "
      f"A exceção é dez/2025 (Flávio), em que os perdedores continuaram perdendo ({pct(pcl('resid_neg', 'excess_6m').get('Flávio 2025'))} contra o Ibovespa em 6m).")
    A(f"   - **O beta depende do regime.** Nos pânicos (greve 2018, Covid, 2ª onda), beta alto foi o melhor preditor (IC 6m {num(rs('beta', '6m', 'panico'), 2)}). "
      f"Nos choques eleitorais foi o pior (IC {num(rs('beta', '6m', 'eleitoral'), 2)}). A cesta de beta alto superou o Ibovespa em {pct(agg('high_beta', 'excess_6m'))} em 6m na média, "
      f"mas perdeu {pct(pcl('high_beta', 'excess_6m').get('Eleição 2022'))} em 2022 e {pct(pcl('high_beta', 'excess_6m').get('Flávio 2025'))} em 2025, com drawdown "
      f"de 12m de {pct(agg('high_beta', 'mdd_12m'))} contra {pct(agg('high_beta', 'ibov_mdd_12m'))} do índice. \"Comprar a maior queda absoluta\" "
      f"({pct(agg('fall_abs', 'excess_6m'))} em 6m, {pct(pcl('fall_abs', 'excess_6m').get('Flávio 2025'))} em 2025) tem o mesmo perfil.")
    A(f"   - **Valor (E/P + B/P) ajuda em geral, e mais nas crises políticas.** IC 6m de {num(rs('value', '6m', 'todos'), 3)} em todas as crises, "
      f"{num(rs('value', '6m', 'politico'), 3)} nas políticas e {num(rs('value', '6m', 'eleitoral'), 3)} nas eleitorais. Só o B/P tem IC 12m de {num(rs('bp', '12m', 'todos'), 2)}. "
      f"A cesta barata ficou {pct(agg('cheap', 'excess_12m'))} acima do Ibovespa em 12m, com excesso positivo em 6m em {of_n(ppos('cheap', 'excess_6m'))} crises. "
      "Na regressão conjunta, o E/P perde força para B/P e ROE (E/P ≈ B/P × ROE), por isso o modelo usa o composto.")
    A(f"   - **Exportadoras (hedge cambial)** superaram em quase todas as crises: +{num(gx(R, 'regressions', 't0', '3m', 'fm', 'exporter', 'clusters', 'mean') * 100, 1)} p.p. "
      f"em 3m na regressão conjunta (t {num(gx(R, 'regressions', 't0', '3m', 'fm', 'exporter', 'clusters', 't'), 1)}). Exceções no IC de 6m: {', '.join(k for k, v in ics['exporter']['6m'].items() if v is not None and v < 0) or 'nenhuma'}.")
    A(f"   - **Qualidade e baixa alavancagem não protegem na recuperação.** A cesta de ROE alto rendeu {pct(agg('quality', 'excess_6m'))} contra o Ibovespa em 6m "
      f"(positiva em {of_n(ppos('quality', 'excess_6m'))} crises) e a de DL/EBITDA baixa, {pct(agg('low_lev', 'excess_6m'))}. Nos choques eleitorais, porém, "
      f"o ROE teve IC {num(rs('roe', '6m', 'eleitoral'), 2)} e as estatais {num(rs('state', '6m', 'eleitoral'), 2)}: é nesse regime que qualidade e o desconto político pagam.")
    A(f"   - **Momentum 12−1** tem IC 6m de {num(rs('mom', '6m', 'todos'), 3)}, concentrado nos pânicos ({num(rs('mom', '6m', 'panico'), 2)}). "
      f"**Tamanho:** small caps recuperam mais em 12m (IC {num(rs('size', '12m', 'todos'), 3)}), exceto nas eleições, em que as grandes foram melhor ({num(rs('size', '6m', 'eleitoral'), 2)}).")
    A(f"   - **A partir do fundo do episódio** (não observável em tempo real) lidera o \"junk rally\": beta (IC 1m {num(regime_stat(ict['beta']['1m'], 'todos')[0], 2)}), "
      f"DL/EBITDA alta ({num(regime_stat(ict['lev']['1m'], 'todos')[0], 2)}), ROE baixo ({num(regime_stat(ict['roe']['1m'], 'todos')[0], 2)}) e B/P alto "
      f"({num(regime_stat(ict['bp']['6m'], 'todos')[0], 2)} em 6m). Comprar beta só compensa se o fundo já passou. O fundo do Ibovespa veio de {min(lags)} a {max(lags)} pregões depois do primeiro dia de cada crise (na Covid, em 23/03/2020).")
    A(f"4. **Viés de sobrevivência é pequeno nos sinais de mercado.** No universo amplo (top 150 por ADTV, inclui deslistadas) o beta tem coeficiente "
      f"{num(gx(sv, 'broad', 'beta', 'clusters', 'mean'), 3)}, o resíduo {num(gx(sv, 'broad', 'resid_b', 'clusters', 'mean'), 2)} e o momentum {num(gx(sv, 'broad', 'mom', 'clusters', 'mean'), 3)}. "
      f"Só entre sobreviventes: {num(gx(sv, 'survivors_only', 'beta', 'clusters', 'mean'), 3)}, {num(gx(sv, 'survivors_only', 'resid_b', 'clusters', 'mean'), 2)} e "
      f"{num(gx(sv, 'survivors_only', 'mom', 'clusters', 'mean'), 3)}. Os fundamentos só existem para sobreviventes, então isso não pode ser testado para eles.")
    A(f"5. **Fora da amostra (deixa uma crise de fora),** o modelo combinado com pesos de regime tem IC médio de {num(lo3['mean_ic'], 3)} em 3m (positivo em "
      f"{of_n(lo3['pct_clusters_ic_pos'])} crises; 2022: {num(gx(lo3, 'per_cluster', 'Eleição 2022', 'ic'), 2)}, 2025: {num(gx(lo3, 'per_cluster', 'Flávio 2025', 'ic'), 2)}) e de {num(lo12['mean_ic'], 3)} em 12m. O spread Q5−Q1 é {pct(lo3['mean_q5_q1'])} em 3m. "
      f"Em 6m o modelo é fraco ({num(R['loco']['6m']['recomendado']['mean_ic'], 3)}), por isso o ranking usa 3m.")
    A(f"6. **Hoje (Ibovespa {pct(T['ibov_chg'])}) é um choque eleitoral com magnitude de pânico.** A queda contra fatores tem R² de {num(T['day0_model']['r2'])}: "
      f"o beta explica a maior parte (coeficiente {num(T['day0_model']['coef'].get('beta'), 3)} por unidade de beta) e as exportadoras caíram "
      f"{num(T['day0_model']['coef'].get('exporter') * 100, 0)} p.p. menos. O resíduo de hoje foi limitado à faixa histórica "
      f"[{pct(T['resid_hist_clip'][0])}, {pct(T['resid_hist_clip'][1])}] ({pct(T['coverage_share_resid_below_hist'], 0).lstrip('+')} da cobertura está abaixo dela). "
      "Como os dois regimes discordam em beta, ROE, alavancagem e tamanho, o modelo recomendado dá peso 2 às crises políticas, encolhe cada coeficiente por max(0, 1 − 1/t²) "
      "e fica com o que é robusto aos dois: reversão do resíduo, valor, momentum e exportadoras.\n")

    # ------------------------------------------------------------------ pesos
    A("## Pesos recomendados para o regime atual\n")
    A("Escore composto em z (postos normalizados na seção cruzada de hoje). Os pesos vêm do IC de Spearman médio de 3m e 6m a partir do choque, por crise, com Fama-MacBeth ponderado "
      "(crises políticas com peso 2), encolhimento max(0, 1 − 1/t²) e normalização Σ|w| = 1. Peso negativo no resíduo significa que quanto mais a ação caiu além do previsto pelos fatores, melhor.\n")
    A("| Característica | IC 6m todas | IC 6m pânico | IC 6m políticas | IC 6m eleitorais | IC 3m–6m recom. | t | **Peso** | Peso nas 59 (sem exportadora) | Indicativo eleitoral |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for c, r in wt.items():
        win = (w_in.get(c, 0) / tot_in) if c in w_in else 0.0
        A(f"| {NAMES.get(c, c)} | {num(r.get('ic6_todos'), 3)} | {num(r.get('ic6_panico'), 3)} | {num(r.get('ic6_politico'), 3)} | {num(r.get('ic6_eleitoral'), 3)} | "
          f"{num(r.get('ic36_recomendado'), 3)} | {num(r.get('t36_recomendado'), 1)} | **{num(W.get(c), 2)}** | {num(win, 2)} | {num(w_ele_raw[c] / tot_ele, 2)} |")
    A("\nA coluna \"indicativo eleitoral\" usa só 2022 e 2025 (n = 2, sem significância), como cenário de estresse caso o choque vire uma reprecificação duradoura de regime, "
      "a exemplo de 2022 e de dez/2025. Nesse cenário o beta pesa contra, e ROE, estatais e tamanho pesam a favor. Beta, ROE, DL/EBITDA, tamanho e estatal ficam com peso zero no "
      "central porque o sinal se inverte entre regimes.\n")

    # ------------------------------------------------------------------ ranking
    A("## Ranking \"regime de crise\" das 59 empresas (26/10/2026)\n")
    m3 = T["model"]["3m"]["recomendado"]
    A(f"Retorno esperado = retorno médio do universo depois dos choques (3m: {pct(m3['level_ew'])}; Ibovespa {pct(m3['ibov'])}, pesos de regime) mais Σ coeficiente × (característica − média de hoje). "
      "Os coeficientes são Fama-MacBeth por crise, com pesos de regime e encolhimento. O intervalo de 80% combina a dispersão entre crises (aplicando os coeficientes de cada crise) com "
      f"o ruído idiossincrático (σ 3m = {pct(T['model']['3m']['resid_sd'])}). Os cenários \"pânico\" e \"eleitoral\" aplicam os coeficientes médios desses regimes, sem encolhimento. "
      f"Correlação de postos do ranking 3m com o de 6m: {num(T['rank_spearman_vs_3m'].get('rank_6m'), 2)}; com o de 12m: {num(T['rank_spearman_vs_3m'].get('rank_12m'), 2)}; "
      f"com o escore z: {num(T['rank_spearman_vs_3m'].get('rank_score_z'), 2)}; com o cenário eleitoral: {num(T['rank_spearman_vs_3m'].get('rank_eleitoral'), 2)}.\n")
    A("### Top 10\n")
    A("| # | Ticker | Queda hoje | Resíduo fatores | Beta | Valor (z) | Esperado 3m | IC 80% 3m | vs Ibov 3m | Esperado 6m | Esperado 12m | Pânico 3m | Eleitoral 3m | Escore z (pos.) |\n|---:|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|")
    for r in top:
        A(f"| {r['rank_crisis']} | {r['ticker']} | {pct(r['r0_today'])} | {pct(r['resid_factor'])} | {num(r['beta_down'])} | {num(r.get('value_z'))} | "
          f"{pct(r['exp_3m'])} | {pct(r['lo80_3m'], 0)} a {pct(r['hi80_3m'], 0)} | {pct(r['exp_3m_vs_ibov'])} | {pct(r['exp_6m'])} | {pct(r['exp_12m'])} | "
          f"{pct(r['regimes_3m']['panico'])} | {pct(r['regimes_3m']['eleitoral'])} | {num(r['crisis_score_z'])} ({r['rank_score_z']}) |")
    A("\n### Todas as 59\n")
    A("| # | Ticker | Grupo | Queda hoje | Resíduo fatores | Beta | E/P | B/P | ROE | DL/EBITDA | Mom. 12−1 | Esp. 3m | IC 80% 3m | Esp. 6m | Esp. 12m | Eleitoral 3m | Escore z |\n|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|")
    for r in T["ranking"]:
        A(f"| {r['rank_crisis']} | {r['ticker']} | {r.get('group') or ''} | {pct(r['r0_today'])} | {pct(r['resid_factor'])} | {num(r['beta_down'])} | {pct(r['ep'])} | {num(r['bp'])} | "
          f"{pct(r['roe'])} | {num(r['nd_ebitda'], 1)} | {pct(r['mom_12_1'], 0)} | {pct(r['exp_3m'])} | {pct(r['lo80_3m'], 0)} a {pct(r['hi80_3m'], 0)} | {pct(r['exp_6m'])} | "
          f"{pct(r['exp_12m'])} | {pct(r['regimes_3m']['eleitoral'])} | {num(r['crisis_score_z'])} |")
    A("\nCoeficientes usados (3m, recomendado; t ponderado por crise; \"usado\" = encolhido):\n")
    A("| Variável | Média | t | Usado | Pânico | Eleitoral |\n|---|---:|---:|---:|---:|---:|")
    for c in FWD_COLS:
        st = m3["coef"].get(c, {})
        A(f"| {NAMES.get(c, c)} | {num(st.get('mean'), 4)} | {num(st.get('t'), 1)} | {num(st.get('used'), 4)} | "
          f"{num(gx(T, 'model', '3m', 'panico', 'coef', c, 'mean'), 4)} | {num(gx(T, 'model', '3m', 'eleitoral', 'coef', c, 'mean'), 4)} |")

    # ------------------------------------------------------------------ episódios
    A("\n## Episódios\n")
    A("Dias com Ibovespa ≤ −4% desde 2016 (o COTAHIST começa em 04/01/2016):\n")
    A("| Data | Ibovespa | Evento | Usado |\n|---|---:|---|---|")
    for e in R["crash_days_le_4pct"]:
        A(f"| {e['date']} | {pct(e['ibov_ret'])} | {e['label']} | {'sim' if e['used'] else 'não'} |")
    A("\nEpisódios analisados (inclui 31/10/2022). Fundo = mínima do Ibovespa em [t0, t0+63 pregões]. R² = regressão cross-section da queda do dia contra fatores.\n")
    A("| Data | Crise | Ibov dia | N | Fundo | Ibov até fundo | Ibov 1m | 3m | 6m | 12m | Universo 6m | R² queda |\n|---|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|")
    for e in R["episodes"]:
        f = e["ibov_fwd"]
        A(f"| {e['date']} | {e['cluster']} | {pct(e['ibov_ret'])} | {e['n_stocks']} | {e['trough_date']} | {pct(e['ibov_t0_to_trough'])} | {pct(f['1m'])} | {pct(f['3m'])} | "
          f"{pct(f['6m'])} | {pct(f['12m'])} | {pct(e['ew_universe_fwd']['6m'])} | {num(e['day0_model']['r2'])} |")

    # ------------------------------------------------------------------ IC por regime
    A("\n## O que previu a recuperação: IC de Spearman univariado por regime\n")
    A("Média por crise (t entre parênteses, só para \"todas\"). Regimes definidos pela natureza do choque: políticas = Joesley 2017, Petrobras 2021, Eleição 2022 e Flávio 2025; "
      "eleitorais = 2022 e 2025; pânico = greve 2018, Covid 2020 e 2ª onda 2020.\n")
    A("| Característica | 1m | 3m | 6m | 12m | 6m pânico | 6m políticas | 6m eleitorais | Do fundo 1m | Do fundo 6m |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for c in UNI_COLS:
        cells = []
        for h in H:
            m_, t_ = regime_stat(ics[c][h], "todos")
            cells.append(f"{num(m_, 3)} ({num(t_, 1)})" if m_ is not None else "—")
        A(f"| {NAMES.get(c, c)} | " + " | ".join(cells) + f" | {num(rs(c, '6m', 'panico'), 3)} | {num(rs(c, '6m', 'politico'), 3)} | {num(rs(c, '6m', 'eleitoral'), 3)} | "
          f"{num(regime_stat(ict[c]['1m'], 'todos')[0], 3)} | {num(regime_stat(ict[c]['6m'], 'todos')[0], 3)} |")
    A("\nIC 6m por crise:\n")
    A("| Característica | " + " | ".join(cls) + " |\n|---|" + "---:|" * len(cls))
    for c in UNI_COLS:
        A(f"| {NAMES.get(c, c)} | " + " | ".join(num(ics[c]['6m'].get(k), 3) for k in cls) + " |")

    # ------------------------------------------------------------------ regressões
    for base, title in (("t0", "a partir do dia do choque"), ("trough", "a partir do fundo do episódio")):
        A(f"\n## Regressão multivariada {title} (Fama-MacBeth por crise)\n")
        A("Coeficiente médio por crise (t). OLS por episódio com erros HC3; beta e resíduo em unidades de retorno; demais características em escore normal de postos; "
          "dummies 0/1; retorno futuro winsorizado a 1%/99%.\n")
        hs = [h for h in H if h in R["regressions"][base]]
        A("| Variável | " + " | ".join(hs) + " |\n|---|" + "---:|" * len(hs))
        for c in ["const"] + FWD_COLS:
            cells = []
            for h in hs:
                o = gx(R, "regressions", base, h, "fm", c, "clusters") or {}
                cells.append(f"{num(o.get('mean'), 3)} ({num(o.get('t'), 1)})" if o else "—")
            A(f"| {NAMES.get(c, c)} | " + " | ".join(cells) + " |")
        A("| R² médio | " + " | ".join(num(R["regressions"][base][h]["avg_r2"]) for h in hs) + " |")
        A("| Episódios / crises | " + " | ".join(f"{R['regressions'][base][h]['n_episodes']} / {R['regressions'][base][h]['n_clusters']}" for h in hs) + " |")
    A("\nRobustez com E/P e B/P separados (a partir do choque): " + "; ".join(
        f"{h}: E/P {num(gx(R, 'regressions', 't0_ep_bp', h, 'fm', 'ep', 'clusters', 'mean'), 3)} (t {num(gx(R, 'regressions', 't0_ep_bp', h, 'fm', 'ep', 'clusters', 't'), 1)}), "
        f"B/P {num(gx(R, 'regressions', 't0_ep_bp', h, 'fm', 'bp', 'clusters', 'mean'), 3)} (t {num(gx(R, 'regressions', 't0_ep_bp', h, 'fm', 'bp', 'clusters', 't'), 1)}), "
        f"ROE {num(gx(R, 'regressions', 't0_ep_bp', h, 'fm', 'roe', 'clusters', 'mean'), 3)} (t {num(gx(R, 'regressions', 't0_ep_bp', h, 'fm', 'roe', 'clusters', 't'), 1)})"
        for h in ("3m", "6m", "12m")) + ".")

    # ------------------------------------------------------------------ reversão
    A("\n## A sobrerreação reverte? Em quanto tempo?\n")
    A("r(t0→t0+h) = a + b·beta + φ(h)·resíduo, por episódio, com Fama-MacBeth por crise. φ = −1 é reversão total; φ = 0, nenhuma.\n")
    A("| h (pregões) | φ resíduo fatores | t | % crises com φ < 0 | φ resíduo beta |\n|---:|---:|---:|---:|---:|")
    for h, o in phi.items():
        c = o.get("clusters") or {}
        cb = gx(R, "reversal", "phi_beta_resid", h, "clusters") or {}
        A(f"| {h} | {num(c.get('mean'), 3)} | {num(c.get('t'), 1)} | {num(1 - c['pct_pos'], 2) if c.get('pct_pos') is not None else '—'} | {num(cb.get('mean'), 3)} |")
    qpp = R["reversal"]["q1_resid_path"]
    A("\nCesta do quintil de resíduo mais negativo menos o universo (peso igual, acumulado, em pregões):\n")
    A("| Crise | " + " | ".join(qpp["avg_q1_minus_all"].keys()) + " |\n|---|" + "---:|" * len(qpp["avg_q1_minus_all"]))
    A("| **Média** | " + " | ".join(pct(v) for v in qpp["avg_q1_minus_all"].values()) + " |")
    for c, v in qpp["per_cluster"].items():
        A(f"| {c} | " + " | ".join(pct(v.get(t)) for t in qpp["avg_q1_minus_all"].keys()) + " |")

    # ------------------------------------------------------------------ estratégias
    A("\n## Estratégias: cesta comprada no fechamento do dia do choque (quintil, peso igual) vs Ibovespa\n")
    A("Média por crise (cada crise pesa 1). Excesso = cesta − Ibovespa; L/S = quintil escolhido − quintil oposto; MDD = drawdown máximo em 12 meses.\n")
    A("| Estratégia | 1m | 3m | 6m | 12m | Excesso 3m | Excesso 6m | Excesso 12m | % crises excesso 6m > 0 | L/S 6m | MDD 12m | MDD Ibov |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for k, s_ in S.items():
        A(f"| {s_['label']} | {pct(agg(k, 'ret_1m'))} | {pct(agg(k, 'ret_3m'))} | {pct(agg(k, 'ret_6m'))} | {pct(agg(k, 'ret_12m'))} | {pct(agg(k, 'excess_3m'))} | "
          f"{pct(agg(k, 'excess_6m'))} | {pct(agg(k, 'excess_12m'))} | {num(ppos(k, 'excess_6m'), 2)} | {pct(agg(k, 'ls_6m'))} | {pct(agg(k, 'mdd_12m'))} | {pct(agg(k, 'ibov_mdd_12m'))} |")
    A("\nExcesso de 6m por crise:\n")
    A("| Estratégia | " + " | ".join(cls) + " |\n|---|" + "---:|" * len(cls))
    for k, s_ in S.items():
        A(f"| {s_['label']} | " + " | ".join(pct(pcl(k, 'excess_6m').get(c)) for c in cls) + " |")

    # ------------------------------------------------------------------ sobrevivência e LOCO
    A("\n## Viés de sobrevivência\n")
    A(f"Modelo: {sv['model']}. Coeficientes Fama-MacBeth por crise (t):\n")
    A("| Variável | Universo amplo | Só sobreviventes (negociadas em set–out/2026) |\n|---|---:|---:|")
    for c in ("const", "beta", "resid_b", "mom", "liq"):
        b = gx(sv, "broad", c, "clusters") or {}
        s_ = gx(sv, "survivors_only", c, "clusters") or {}
        A(f"| {NAMES.get(c, c)} | {num(b.get('mean'), 3)} ({num(b.get('t'), 1)}) | {num(s_.get('mean'), 3)} ({num(s_.get('t'), 1)}) |")
    A("\n| Episódio | N amplo | N sobreviventes | 6m sobreviventes | 6m não sobreviventes |\n|---|---:|---:|---:|---:|")
    for d, g in sv["return_gap"].items():
        A(f"| {d} | {g['n']} | {g['n_surv']} | {pct(g['mean_6m_surv'])} | {pct(g['mean_6m_nonsurv'])} |")
    A("\n## Validação fora da amostra (deixa uma crise de fora)\n")
    A("O modelo é treinado nas outras crises (FM com encolhimento) e aplicado à seção cruzada da crise deixada de fora.\n")
    A("| Horizonte | Pesos | IC médio | IC médio nas políticas | Q5−Q1 médio | % crises IC > 0 |\n|---|---|---:|---:|---:|---:|")
    for h, o in R["loco"].items():
        for tag, v in o.items():
            A(f"| {h} | {tag} | {num(v['mean_ic'], 3)} | {num(v['mean_ic_political'], 3)} | {pct(v['mean_q5_q1'])} | {num(v['pct_clusters_ic_pos'], 2)} |")
    A("\n| Crise | " + " | ".join(f"{h} recom." for h in R["loco"]) + " |\n|---|" + "---:|" * len(R["loco"]))
    for c in cls:
        A(f"| {c} | " + " | ".join(f"IC {num(gx(R['loco'][h], 'recomendado', 'per_cluster', c, 'ic'), 2)} / {pct(gx(R['loco'][h], 'recomendado', 'per_cluster', c, 'q5_minus_q1'))}" for h in R["loco"]) + " |")

    # ------------------------------------------------------------------ limitações
    A("\n## Limitações\n")
    A("- **Poucos episódios independentes.** São 7 crises (6 com 12m), apenas 2 eleitorais e 3 de pânico. Os t por crise têm 3–6 graus de liberdade e os 11 dias da Covid contam como um "
      "evento só (o t \"por dia\" no JSON é ingênuo). A classificação dos regimes (político/eleitoral/pânico) e o peso 2 das crises políticas são escolhas a priori, não estimadas.")
    A("- **Hoje está fora da amostra em magnitude.** O Ibovespa caiu −14,8%, só comparável a 12 e 16/03/2020, e 59 ações caíram ≥ 20%. O resíduo foi limitado à faixa histórica "
      "e a extrapolação linear de φ para quedas desse tamanho não é testada.")
    A("- **Sobrevivência.** Os fundamentos (E/P, B/P, ROE, DL/EBITDA) existem só para empresas listadas hoje (`data/hist`). O teste no universo amplo, que inclui deslistadas, cobre só "
      "sinais de mercado. Uma deslistagem é tratada como saída pelo último preço.")
    A("- **Retorno de preço, sem proventos.** Isso subestima valor e ações de dividendo alto em ~DY por ano. Os efeitos de E/P e B/P provavelmente estão subestimados.")
    A("- **Fundamentos point-in-time com defasagem fixa** (45 dias para trimestres, 90 dias para o anual). Na Covid isso usa o FY2018, porque o FY2019 só entra em 30/03/2020. "
      "Em 31/10/2022 usa o fluxo do FY2021 com o balanço do 2T22 (o ITR na base começa em 2022). O valor de mercado histórico vem da série de ações da CVM, "
      "corrigida de escala e recuada por desdobramentos.")
    A("- **Classificações manuais.** Exportadora = Materiais Básicos (exceto Dexco/Irani), petróleo E&P/integrada e uma lista explícita, sem distribuidoras. Estatal é point-in-time "
      "(Eletrobras até 06/2022, Sabesp até 07/2024, Copel até 08/2023, BR Distribuidora até 07/2019). Setores seguem a classificação atual da B3.")
    A("- **Costura de ISINs** em renomeações, por continuidade de preço 1:1 ± 20%, mesma classe e volume compatível (lista em `stitched_chains`). Pode errar em papéis ilíquidos "
      "fora do universo principal.")
    A("- **Os retornos de hoje são uma foto intradiária** (`data/market/*.json`, stats.today) e o ranking muda com o fechamento. O valuation (`data/app/overview.json`) não entra no modelo, só como referência "
      "no JSON: este ranking é uma sobreposição de regime de crise, não um ranking de valor justo.")
    A("- **Intervalos largos.** O intervalo de 80% é dominado pela trajetória do mercado (o nível vem da média pós-choque, que vai de −10% a +50% entre crises). "
      "O ranking relativo é mais confiável do que o nível do retorno esperado.")
    open(OUT / "crash_study.md", "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main(*sys.argv[1:3])

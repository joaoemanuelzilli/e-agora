"""Mercado e quant: preços ajustados (B3 oficial), risco, decomposição da queda, event study, múltiplos históricos e fatores.

Uso: python pipeline/market.py <cotahist_csv_gz> <dir_raw_b3> <quotes_json>
Saídas: data/market/{TICKER}.json, data/market/_market.json, data/market/quotes.json
"""
import json
import math
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "market"
TODAY = pd.Timestamp("2026-10-26")
LAST_CLOSE = pd.Timestamp("2026-10-23")
PRE_RALLY = pd.Timestamp("2026-08-14")  # mínima do Ibovespa antes do rali eleitoral (166,9 mil)
ELECTIONS = [  # dia útil seguinte ao resultado da eleição presidencial
    ("1998-10-05", "FHC reeleito (1º turno)"), ("2002-10-28", "Lula eleito"), ("2006-10-30", "Lula reeleito"),
    ("2010-11-01", "Dilma eleita"), ("2014-10-27", "Dilma reeleita"), ("2018-10-29", "Bolsonaro eleito"),
    ("2022-10-31", "Lula eleito"),
]
STATE = {"BBAS3", "BRSR6", "PETR3", "PETR4", "SAPR11", "CSMG3", "CMIG4", "BBSE3", "CXSE3", "BRAP4", "IRBR3"}


def ptdate(s):
    return pd.Timestamp(datetime.strptime(s, "%d/%m/%Y"))


def fnum(s):
    return float(str(s).replace(".", "").replace(",", "."))


def split_events(sup, isin):
    """Eventos que mudam a quantidade de ações: [(data_com, multiplicador_de_ações)]."""
    ev = []
    for e in (sup or {}).get("stockDividends") or []:
        if e.get("isinCode") != isin:
            continue
        lab = e.get("label", "")
        f = fnum(e["factor"])
        if lab in ("BONIFICACAO", "DESDOBRAMENTO"):
            mult = 1 + f / 100
        elif lab == "GRUPAMENTO":
            mult = f
        else:
            continue
        if mult > 0 and abs(mult - 1) > 1e-9:
            ev.append((ptdate(e["lastDatePrior"]), mult))
    agg = {}
    for d, m in ev:
        agg[d] = agg.get(d, 1.0) * m
    return sorted((d, m) for d, m in agg.items() if abs(m - 1) > 1e-9)


def adjust(series, events):
    """Ajusta preços anteriores ao ex-evento: preço × 1/multiplicador. series indexada por data."""
    adj = series.copy().astype(float)
    for dcom, mult in events:
        adj.loc[adj.index <= dcom] = adj.loc[adj.index <= dcom] / mult
    return adj


def ols(y, x):
    x1 = np.column_stack([np.ones(len(x)), x])
    b, *_ = np.linalg.lstsq(x1, y, rcond=None)
    res = y - x1 @ b
    return b, res


def fwd(series, d0, days):
    s = series[series.index >= d0]
    if len(s) <= days:
        return None
    return float(s.iloc[days] / s.iloc[0] - 1)


def main(cot_path, raw_b3, quotes_json):
    OUT.mkdir(parents=True, exist_ok=True)
    sup = json.load(open(Path(raw_b3) / "supplement.json"))
    det = json.load(open(Path(raw_b3) / "details.json"))
    idx = json.load(open(Path(raw_b3) / "indices.json"))
    q = json.load(open(quotes_json))
    rows = q["rows"]
    quotes = {r["ticker"]: {**(r.get("quote") or {}), "name": r["name"], "indices": r["indices"]} for r in rows}
    json.dump({"fetched_at": q["fetched_at"], **quotes}, open(OUT / "quotes.json", "w"), ensure_ascii=False)
    cov = {r["ticker"] for r in json.load(open(ROOT / "research" / "_coverage.json"))["coverage"]}

    df = pd.read_csv(cot_path, parse_dates=["date"])
    ibov = pd.Series({pd.Timestamp(d): v for d, v in idx["IBOV"]}).sort_index()
    ibov = ibov[~ibov.index.duplicated()]
    ib_today = quotes.get("IBOV", {}).get("price")
    ibov_chg_today = None
    # IBOV ao vivo vem do fetch separado (quotes não traz índice); usa API B3 se disponível
    try:
        from urllib.request import Request, urlopen
        with urlopen(Request("https://cotacao.b3.com.br/mds/api/v1/instrumentQuotation/IBOV", headers={"User-Agent": "Mozilla/5.0"}), timeout=15) as r:
            d = json.loads(r.read().decode())
        s = d["Trad"][0]["scty"]["SctyQtn"]
        ib_today, ibov_chg_today = s["curPrc"], s["prcFlcn"] / 100
    except Exception:
        pass
    ib_ret = ibov.pct_change().dropna()

    # ------------------------------------------------ séries por ticker (via ISIN, cobre troca de código)
    latest_isin = df[df.date >= "2026-09-01"].sort_values("date").groupby("ticker")["isin"].last()
    per = {}
    for tk in quotes:
        if tk not in latest_isin.index:
            continue
        isin = latest_isin[tk]
        s = df[df["isin"] == isin].sort_values("date").drop_duplicates("date", keep="last").set_index("date")
        if len(s) < 60:
            continue
        # corta no último buraco > 45 dias (ex.: NATU3 relistada em 2025)
        gaps = s.index.to_series().diff().dt.days
        big_gap = gaps[gaps > 45]
        if len(big_gap):
            s = s[s.index >= big_gap.index[-1]]
        if len(s) < 60:
            continue
        issuer = tk[:4]
        evs = split_events(sup.get(issuer), isin)
        close_adj = adjust(s["close"], evs)
        rets = close_adj.pct_change().dropna()
        # desdobramentos/grupamentos ausentes na lista da B3: razão "redonda" no salto
        nice = [2, 3, 4, 5, 8, 10, 20, 25, 50, 100]
        extra = []
        for d, r_ in rets[rets.abs() > 0.35].items():
            ratio = 1 + r_
            for m in nice:
                for mult in (m, 1 / m):
                    if abs(ratio * mult - 1) < 0.08:
                        prev_d = s.index[s.index.get_loc(d) - 1]
                        extra.append((prev_d, mult))
        if extra:
            evs = sorted(evs + extra)
            close_adj = adjust(s["close"], evs)
            rets = close_adj.pct_change().dropna()
        weird = rets[rets.abs() > 0.35]
        per[tk] = {"isin": isin, "raw": s, "adj": close_adj, "events": evs, "weird": weird}

    # ------------------------------------------------ estatísticas de risco e decomposição da queda
    stats = {}
    for tk, p in per.items():
        a = p["adj"]
        r = a.pct_change().dropna()
        j = pd.concat([r.rename("s"), ib_ret.rename("m")], axis=1, join="inner").dropna()
        j2 = j[j.index > LAST_CLOSE - pd.Timedelta(days=730)]
        j3 = j[j.index > LAST_CLOSE - pd.Timedelta(days=1095)]
        if len(j2) < 120:
            continue
        b2, res2 = ols(j2.s.values, j2.m.values)
        wk = pd.concat([a.resample("W-FRI").last().pct_change().rename("s"), ibov.resample("W-FRI").last().pct_change().rename("m")], axis=1, sort=True).dropna()
        wk = wk[wk.index > LAST_CLOSE - pd.Timedelta(days=1095)]
        bw, _ = ols(wk.s.values, wk.m.values) if len(wk) > 50 else (np.array([np.nan, np.nan]), None)
        dn = j3[j3.m < 0]
        bd, _ = ols(dn.s.values, dn.m.values) if len(dn) > 60 else (np.array([np.nan, np.nan]), None)
        cr = j[j.m <= -0.03]
        bc, _ = ols(cr.s.values, cr.m.values) if len(cr) >= 8 else (np.array([np.nan, np.nan]), None)
        idio = float(np.std(res2) * math.sqrt(252))
        vol1y = float(r[r.index > LAST_CLOSE - pd.Timedelta(days=365)].std() * math.sqrt(252))
        hi52 = float(a[a.index > LAST_CLOSE - pd.Timedelta(days=365)].max())
        a10 = a[a.index > LAST_CLOSE - pd.Timedelta(days=3650)]
        dd = (a10 / a10.cummax() - 1).min()
        qt = quotes.get(tk) or {}
        px_now, chg_now = qt.get("price"), (qt.get("chg_pct") or 0) / 100
        last_px = float(a.iloc[-1])
        def ret_since(days):
            s0 = a[a.index <= LAST_CLOSE - pd.Timedelta(days=days)]
            return float(last_px / s0.iloc[-1] - 1) if len(s0) else None
        ytd0 = a[a.index <= pd.Timestamp("2025-12-31")]
        mom = None
        s252 = a[a.index <= LAST_CLOSE - pd.Timedelta(days=365)]
        s21 = a[a.index <= LAST_CLOSE - pd.Timedelta(days=30)]
        if len(s252) and len(s21):
            mom = float(s21.iloc[-1] / s252.iloc[-1] - 1)
        vol3m = p["raw"]["volume"][p["raw"].index > LAST_CLOSE - pd.Timedelta(days=95)].mean() / 1e6
        pre_rally = a[a.index <= PRE_RALLY]
        pr_px = float(pre_rally.iloc[-1]) if len(pre_rally) else None
        beta_use = bd[1] if np.isfinite(bd[1]) else b2[1]
        exp = beta_use * ibov_chg_today if ibov_chg_today is not None else None
        stats[tk] = {
            "beta_2y_daily": float(b2[1]), "beta_3y_weekly": float(bw[1]) if np.isfinite(bw[1]) else None,
            "beta_down_3y": float(bd[1]) if np.isfinite(bd[1]) else None, "beta_crash_10y": float(bc[1]) if np.isfinite(bc[1]) else None,
            "n_crash_days": int(len(cr)), "idio_vol": idio, "vol_1y": vol1y, "max_dd_10y": float(dd),
            "high_52w_pre": hi52, "dist_high_now": (px_now / hi52 - 1) if px_now else None,
            "ret_ytd_pre": float(last_px / ytd0.iloc[-1] - 1) if len(ytd0) else None,
            "ret_12m_pre": ret_since(365), "ret_36m_pre": ret_since(1095), "mom_12_1": mom, "adtv_3m_mn": float(vol3m),
            "price_pre_rally": pr_px, "rally_to_2310": (last_px / pr_px - 1) if pr_px else None,
            "now_vs_pre_rally": (px_now / pr_px - 1) if pr_px and px_now else None,
            "today": {"chg": chg_now, "price": px_now, "prev_close": qt.get("prev_close"), "expected_beta": exp,
                      "residual": (chg_now - exp) if exp is not None else None,
                      "z_idio": ((chg_now - exp) / (idio / math.sqrt(252))) if exp is not None and idio > 0 else None},
            "split_events": [(d.strftime("%Y-%m-%d"), m) for d, m in p["events"]],
            "price_jumps_unexplained": [(d.strftime("%Y-%m-%d"), float(v)) for d, v in p["weird"].items()],
        }

    # ------------------------------------------------ regressão cross-section da queda de hoje
    sect = {}
    for tk in quotes:
        d_ = det.get(tk[:4]) or {}
        ic = d_.get("industryClassification") or ""
        parts = [x.strip() for x in ic.split("/")]
        sect[tk] = {"setor": parts[0] if parts else None, "subsetor": parts[1] if len(parts) > 1 else None, "segmento": parts[2] if len(parts) > 2 else None}
    xs = []
    for tk, st in stats.items():
        h = ROOT / "data" / "hist" / f"{tk}.json"
        lev, mcap = None, None
        if h.exists():
            hh = json.load(open(h))
            ltm = hh.get("ltm") or {}
            bal = hh.get("balance") or {}
            if not hh.get("is_financial") and ltm.get("ebitda") and ltm["ebitda"] > 0 and bal.get("net_debt") is not None:
                lev = bal["net_debt"] / ltm["ebitda"]
            sh = (hh.get("shares") or {}).get("outstanding")
            if sh and st["today"]["prev_close"]:
                mcap = st["today"]["prev_close"] * sh / (hh.get("shares_per_unit") or 1) / 1e6
        s_ = sect.get(tk, {})
        exporter = s_.get("setor") in ("Materiais Básicos", "Petróleo, Gás e Biocombustíveis") or tk in ("EMBJ3", "WEGE3", "SUZB3", "KLBN11", "BEEF3", "MBRF3", "SLCE3")
        xs.append({"ticker": tk, "y": st["today"]["chg"], "beta": st["beta_down_3y"] if st["beta_down_3y"] is not None else st["beta_2y_daily"],
                   "lev": lev, "log_mcap": math.log(mcap) if mcap else None, "exporter": 1.0 if exporter else 0.0,
                   "financial": 1.0 if s_.get("setor") == "Financeiro" else 0.0, "state": 1.0 if tk in STATE else 0.0,
                   "utility": 1.0 if s_.get("setor") == "Utilidade Pública" else 0.0,
                   "consumo": 1.0 if s_.get("setor") == "Consumo Cíclico" else 0.0, "mom": st["mom_12_1"]})
    X = pd.DataFrame(xs).set_index("ticker")
    X["lev_c"] = X["lev"].clip(-2, 8).fillna(X["lev"].median())
    X["log_mcap"] = X["log_mcap"].fillna(X["log_mcap"].median())
    X["mom"] = X["mom"].fillna(0)
    cols = ["beta", "lev_c", "log_mcap", "exporter", "financial", "state", "utility", "consumo"]
    Xm = X.dropna(subset=["y", "beta"])
    A = np.column_stack([np.ones(len(Xm))] + [Xm[c].values for c in cols])
    coef, *_ = np.linalg.lstsq(A, Xm.y.values, rcond=None)
    pred = A @ coef
    resid = Xm.y.values - pred
    sst = ((Xm.y - Xm.y.mean()) ** 2).sum()
    r2 = 1 - (resid ** 2).sum() / sst
    s2 = (resid ** 2).sum() / (len(Xm) - len(cols) - 1)
    cov_b = s2 * np.linalg.inv(A.T @ A)
    tstats = coef / np.sqrt(np.diag(cov_b))
    # só beta
    A1 = np.column_stack([np.ones(len(Xm)), Xm.beta.values])
    c1, *_ = np.linalg.lstsq(A1, Xm.y.values, rcond=None)
    r2_beta = 1 - ((Xm.y.values - A1 @ c1) ** 2).sum() / sst
    xsec = {"n": int(len(Xm)), "r2": float(r2), "r2_beta_only": float(r2_beta),
            "coef": dict(zip(["const"] + cols, map(float, coef))), "t": dict(zip(["const"] + cols, map(float, tstats))),
            "points": [{"ticker": t, "actual": float(a), "predicted": float(p_), "residual": float(a - p_)} for t, a, p_ in zip(Xm.index, Xm.y.values, pred)]}
    for pnt in xsec["points"]:
        if pnt["ticker"] in stats:
            stats[pnt["ticker"]]["today"]["xsec_predicted"] = pnt["predicted"]
            stats[pnt["ticker"]]["today"]["xsec_residual"] = pnt["residual"]

    # ------------------------------------------------ event study (mercado)
    worst = ib_ret.nsmallest(20)
    crash_rows = []
    for d, v in worst.items():
        crash_rows.append({"date": d.strftime("%Y-%m-%d"), "ret": float(v), **{k: fwd(ibov, d, n) for k, n in (("f1m", 21), ("f3m", 63), ("f6m", 126), ("f12m", 252))}})
    big = ib_ret[ib_ret <= -0.05]
    agg = {k: [] for k in ("f1m", "f3m", "f6m", "f12m")}
    for d in big.index:
        for k, n in (("f1m", 21), ("f3m", 63), ("f6m", 126), ("f12m", 252)):
            x = fwd(ibov, d, n)
            if x is not None:
                agg[k].append(x)
    crash_stats = {k: {"n": len(v), "mean": float(np.mean(v)) if v else None, "median": float(np.median(v)) if v else None,
                       "pct_pos": float(np.mean(np.array(v) > 0)) if v else None, "p10": float(np.percentile(v, 10)) if v else None,
                       "p90": float(np.percentile(v, 90)) if v else None} for k, v in agg.items()}
    elect = []
    for ds, label in ELECTIONS:
        d = pd.Timestamp(ds)
        s = ibov[ibov.index >= d]
        prev = ibov[ibov.index < d]
        if len(s) and len(prev):
            elect.append({"date": ds, "label": label, "ret_d1": float(s.iloc[0] / prev.iloc[-1] - 1),
                          **{k: fwd(ibov, d, n) for k, n in (("f1m", 21), ("f3m", 63), ("f6m", 126), ("f12m", 252))}})
    # drawdowns > 25% e recuperação
    dd_eps = []
    peak_v, peak_d, in_dd, trough_v, trough_d = ibov.iloc[0], ibov.index[0], False, None, None
    for d, v in ibov.items():
        if v >= peak_v:
            if in_dd and trough_v / peak_v - 1 <= -0.25:
                dd_eps.append({"peak": peak_d.strftime("%Y-%m-%d"), "trough": trough_d.strftime("%Y-%m-%d"), "depth": float(trough_v / peak_v - 1),
                               "recovered": d.strftime("%Y-%m-%d"), "days_to_recover": int((d - trough_d).days)})
            peak_v, peak_d, in_dd, trough_v, trough_d = v, d, False, None, None
        else:
            if not in_dd or v < trough_v:
                trough_v, trough_d = v, d
            in_dd = True
    rally_after = {}
    for e in dd_eps:
        rally_after[e["trough"]] = fwd(ibov, pd.Timestamp(e["trough"]), 252)
    ibov_w = ibov.resample("W-FRI").last().dropna()
    market = {
        "ibov_today": {"price": ib_today, "chg": ibov_chg_today, "prev_close": float(ibov.iloc[-1]), "rank_since_1998": int((ib_ret < (ibov_chg_today or 0)).sum()) + 1 if ibov_chg_today else None,
                       "pre_rally": float(ibov[ibov.index <= PRE_RALLY].iloc[-1]), "pre_rally_date": PRE_RALLY.strftime("%Y-%m-%d")},
        "ibov_daily_return_stats": {"mean": float(ib_ret.mean()), "std": float(ib_ret.std()), "n": int(len(ib_ret)),
                                    "z_today": float((ibov_chg_today - ib_ret.mean()) / ib_ret.std()) if ibov_chg_today else None},
        "worst_days": crash_rows, "crash_forward_stats": crash_stats, "crash_threshold": -0.05, "elections": elect,
        "drawdowns_25": [{**e, "fwd12m_from_trough": rally_after.get(e["trough"])} for e in dd_eps],
        "ibov_weekly": [[d.strftime("%Y-%m-%d"), round(float(v), 2)] for d, v in ibov_w.items()],
        "indices_last": {k: (v[-1] if v else None) for k, v in idx.items()},
        "xsec": xsec, "sectors": sect,
    }
    # trajetórias pós-choque (base 100 no fechamento do dia do choque), episódios separados por >= 60 dias
    def path(d0, n=252):
        s = ibov[ibov.index >= d0]
        if len(s) < 10:
            return None
        s = s.iloc[: n + 1]
        return [round(float(v / s.iloc[0] * 100), 2) for v in s.values]
    episodes, last_d = [], None
    for d, v in ib_ret[ib_ret <= -0.07].sort_index().items():
        if last_d is None or (d - last_d).days > 60:
            pth = path(d)
            if pth and len(pth) > 200:
                episodes.append({"date": d.strftime("%Y-%m-%d"), "ret": float(v), "path": pth})
        last_d = d
    market["crash_paths"] = episodes
    market["election_paths"] = [{"date": e["date"], "label": e["label"], "path": path(pd.Timestamp(e["date"]) - pd.Timedelta(days=1))} for e in elect]
    # retorno diário: histograma para mostrar quão extremo é hoje
    h_counts, h_edges = np.histogram(ib_ret.clip(-0.2, 0.2), bins=80)
    market["ibov_return_hist"] = {"counts": h_counts.tolist(), "edges": h_edges.tolist()}
    json.dump(market, open(OUT / "_market.json", "w"), ensure_ascii=False)

    # ------------------------------------------------ por ticker: séries, múltiplos históricos, proventos
    for tk, p in per.items():
        if tk not in stats:
            continue
        a, raw = p["adj"], p["raw"]
        h_path = ROOT / "data" / "hist" / f"{tk}.json"
        hh = json.load(open(h_path)) if h_path.exists() else None
        d3 = a[a.index > LAST_CLOSE - pd.Timedelta(days=3 * 365)]
        w10 = a.resample("W-FRI").last().dropna()
        doc = {"ticker": tk, "isin": p["isin"], "sector": sect.get(tk), "stats": stats[tk],
               "daily_3y": [[d.strftime("%Y-%m-%d"), round(float(v), 4)] for d, v in d3.items()],
               "weekly_10y": [[d.strftime("%Y-%m-%d"), round(float(v), 4)] for d, v in w10.items()],
               "ibov_daily_3y": [[d.strftime("%Y-%m-%d"), round(float(v), 2)] for d, v in ibov[ibov.index > LAST_CLOSE - pd.Timedelta(days=3 * 365)].items()]}
        # event study da ação nos crashes do período disponível
        evs = []
        for d, v in ib_ret[(ib_ret <= -0.07) & (ib_ret.index >= a.index[0])].items():
            r_s = a.pct_change().get(d)
            evs.append({"date": d.strftime("%Y-%m-%d"), "ibov": float(v), "stock_d0": float(r_s) if r_s is not None and np.isfinite(r_s) else None,
                        **{k: fwd(a, d, n) for k, n in (("f1m", 21), ("f3m", 63), ("f6m", 126), ("f12m", 252))},
                        **{"ibov_" + k: fwd(ibov, d, n) for k, n in (("f1m", 21), ("f3m", 63), ("f6m", 126), ("f12m", 252))}})
        doc["crash_events"] = evs
        # proventos B3 (12m) por ação desta classe
        divs = []
        for e in (sup.get(tk[:4]) or {}).get("cashDividends") or []:
            if e.get("isinCode") == p["isin"]:
                divs.append({"data_com": e["lastDatePrior"], "pagamento": e.get("paymentDate"), "tipo": e.get("label"), "valor": fnum(e["rate"]), "ref": e.get("relatedTo")})
        doc["dividends_b3"] = divs
        if hh:
            doc["multiples_history"] = multiples_history(hh, raw, p["events"], quotes.get(tk))
            doc["dps_history"] = dps_history(hh, a, p["events"])
        json.dump(doc, open(OUT / f"{tk}.json", "w"), ensure_ascii=False)
    warn = {tk: st["price_jumps_unexplained"] for tk, st in stats.items() if st["price_jumps_unexplained"] and tk in cov}
    print("tickers:", len(stats), "| R² xsec:", round(r2, 3), "| R² só beta:", round(r2_beta, 3), "| IBOV hoje:", ibov_chg_today)
    print("saltos não explicados (cobertura):", json.dumps(warn)[:1500])


def shares_at(hh, d, events):
    """Ações em circulação (base da época) na data d: último registro CVM ≤ d, ajustado por eventos entre o registro e d."""
    hist = hh.get("shares_history") or []
    best = None
    for h in hist:
        if pd.Timestamp(h["date"]) <= d:
            best = h
    if best is None and hist:
        best = hist[0]
    if best is None:
        return None
    n = best["outstanding"]
    for dcom, mult in events:
        if pd.Timestamp(best["date"]) < dcom < d:
            n *= mult
    return n


def fundamentals_at(hh, d):
    """LTM disponível na data d (defasagem de publicação: 45d trimestre, 90d anual)."""
    best = None
    for k, q in (hh.get("quarterly") or {}).items():
        y, qq = int(k[:4]), int(k[-1])
        qend = pd.Timestamp(year=y, month=qq * 3, day=1) + pd.offsets.MonthEnd(0)
        lag = 90 if qq == 4 else 45
        if qend + pd.Timedelta(days=lag) <= d:
            if best is None or qend > best[0]:
                best = (qend, k)
    ann = None
    for k in hh.get("annual") or {}:
        y = int(k[2:])
        if pd.Timestamp(year=y, month=12, day=31) + pd.Timedelta(days=90) <= d:
            ann = k if ann is None or int(k[2:]) > int(ann[2:]) else ann
    if best is not None:
        qend, k = best
        keys = sorted(hh["quarterly"], key=lambda x: (int(x[:4]), int(x[-1])))
        i = keys.index(k)
        if i >= 3:
            last4 = keys[i - 3:i + 1]
            ok = all(pd.Timestamp(year=int(a[:4]), month=int(a[-1]) * 3, day=1) + pd.offsets.MonthEnd(0) >= qend - pd.Timedelta(days=370) for a in last4)
            if ok:
                f = {}
                for fld in ("ni_controlling", "ebitda", "revenue", "dividends_paid"):
                    vals = [hh["quarterly"][a].get(fld) for a in last4]
                    f[fld] = sum(vals) if all(v is not None for v in vals) else None
                bq = (hh.get("balance_quarterly") or {}).get(k) or ({} if qq_is4(k) else {})
                if not bq and qq_is4(k):
                    bq = hh["annual"].get(f"FY{k[:4]}") or {}
                f.update({b: bq.get(b) for b in ("equity_controlling", "net_debt", "minority")})
                return f
    if ann:
        a = hh["annual"][ann]
        return {f: a.get(f) for f in ("ni_controlling", "ebitda", "revenue", "dividends_paid", "equity_controlling", "net_debt", "minority")}
    return None


def qq_is4(k):
    return k.endswith("Q4")


def multiples_history(hh, raw, events, q):
    out = []
    per_unit = hh.get("shares_per_unit") or 1
    months = raw["close"].resample("ME").last().dropna()
    months = months[months.index >= pd.Timestamp("2016-01-01")]
    for d, px in months.items():
        n = shares_at(hh, d, events)
        f = fundamentals_at(hh, d)
        if not n or not f:
            continue
        mcap = px * n / per_unit / 1e6
        row = {"date": d.strftime("%Y-%m-%d"), "mcap": round(mcap, 1)}
        ni, eq, eb = f.get("ni_controlling"), f.get("equity_controlling"), f.get("ebitda")
        row["pe"] = round(mcap / ni, 2) if ni and ni > 0 else None
        row["pbv"] = round(mcap / eq, 3) if eq and eq > 0 else None
        if not hh.get("is_financial") and eb and eb > 0 and f.get("net_debt") is not None:
            row["ev_ebitda"] = round((mcap + f["net_debt"] + (f.get("minority") or 0)) / eb, 2)
        dv = f.get("dividends_paid")
        row["dy"] = round(-dv / mcap, 4) if dv is not None and mcap > 0 else None
        out.append(row)
    # ponto de hoje (preço ao vivo)
    if q and q.get("price"):
        d = TODAY
        n = (hh.get("shares") or {}).get("outstanding")
        f = fundamentals_at(hh, d)
        if n and f:
            mcap = q["price"] * n / per_unit / 1e6
            row = {"date": d.strftime("%Y-%m-%d"), "mcap": round(mcap, 1), "live": True}
            ni, eq, eb = f.get("ni_controlling"), f.get("equity_controlling"), f.get("ebitda")
            row["pe"] = round(mcap / ni, 2) if ni and ni > 0 else None
            row["pbv"] = round(mcap / eq, 3) if eq and eq > 0 else None
            if not hh.get("is_financial") and eb and eb > 0 and f.get("net_debt") is not None:
                row["ev_ebitda"] = round((mcap + f["net_debt"] + (f.get("minority") or 0)) / eb, 2)
            dv = f.get("dividends_paid")
            row["dy"] = round(-dv / mcap, 4) if dv is not None and mcap > 0 else None
            out.append(row)
    stats = {}
    for k in ("pe", "pbv", "ev_ebitda", "dy"):
        hist_vals = np.array([r[k] for r in out if r.get(k) is not None and not r.get("live")], dtype=float)
        if k == "pe":
            hist_vals = hist_vals[(hist_vals > 0) & (hist_vals < 80)]
        if k == "ev_ebitda":
            hist_vals = hist_vals[(hist_vals > 0) & (hist_vals < 60)]
        if len(hist_vals) < 12:
            continue
        for win, nm in ((len(hist_vals), "all"), (60, "5y")):
            hv = hist_vals[-win:]
            cur = out[-1].get(k) if out and out[-1].get("live") else None
            stats[f"{k}_{nm}"] = {"mean": float(hv.mean()), "median": float(np.median(hv)), "std": float(hv.std()),
                                  "p10": float(np.percentile(hv, 10)), "p90": float(np.percentile(hv, 90)), "n": int(len(hv)),
                                  "current": cur, "z": float((cur - hv.mean()) / hv.std()) if cur is not None and hv.std() > 0 else None,
                                  "pctile": float((hv < cur).mean()) if cur is not None else None}
    return {"series": out, "stats": stats}


def dps_history(hh, adj, events):
    rows = []
    for k, a in sorted((hh.get("annual") or {}).items(), key=lambda kv: int(kv[0][2:])):
        y = int(k[2:])
        d = pd.Timestamp(year=y, month=12, day=31)
        n = shares_at(hh, d, events)
        dv = a.get("dividends_paid")
        ni = a.get("ni_controlling")
        if not n or dv is None:
            continue
        mult_after = 1.0
        for dcom, mult in events:
            if dcom > d:
                mult_after *= mult
        dps = -dv * 1e6 / n / mult_after  # em base de ações atual
        yr = adj[(adj.index.year == y)]
        rows.append({"year": y, "dividends_mn": -dv, "dps_adj": round(dps, 4), "payout": round(-dv / ni, 4) if ni and ni > 0 else None,
                     "dy_avg_price": round(dps / float(yr.mean()), 4) if len(yr) else None})
    return rows


if __name__ == "__main__":
    main(*sys.argv[1:4])

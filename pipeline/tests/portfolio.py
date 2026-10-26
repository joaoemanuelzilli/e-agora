#!/usr/bin/env python3
"""Carteiras pós-choque (26/10/2026): covariância Ledoit-Wolf, otimizações com limites, risco ex-ante,
estresses, Monte Carlo por bootstrap, backtest de "comprar no crash" (2017 e 2020) e Kelly fracionado.

Uso:
    .venv/bin/python pipeline/tests/portfolio.py [--sp <scratchpad>] [--paths 10000] [--offline]

Entradas: data/app/overview.json, data/app/companies/*.json, data/market/*.json, research/*.json,
          <sp>/work/cotahist.csv.gz, <sp>/raw/b3/{indices,supplement}.json,
          BCB SGS 1 (dólar comercial; cache em data/tests/cache/sgs1_usdbrl.json).
Saídas:   data/tests/portfolio.json, data/tests/portfolio.md

Convenções: retornos simples; preços ajustados só por eventos societários (desdobramento, grupamento,
bonificação), como em pipeline/market.py (sem reinvestimento de proventos); Ibovespa é índice de retorno total.
"""
import argparse
import json
import math
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
from market import adjust, split_events  # noqa: E402  (mesma lógica de ajuste do pipeline)

OUT = ROOT / "data" / "tests"
CACHE = OUT / "cache"
SP_DEFAULT = Path("/tmp/claude-1000/-home-joaoemanuel-git-e-agora/cd238de5-f094-4d2e-ba5c-c5e5bf8d2192/scratchpad")

TODAY = pd.Timestamp("2026-10-26")
LAST_CLOSE = pd.Timestamp("2026-10-23")
HIST_START = pd.Timestamp("2016-01-01")
COV_DAYS = 1095                      # janela de 3 anos (dias corridos), como em market.py
W_MAX, SECTOR_MAX = 0.20, 0.40
DI_LONG = 0.155                      # DI longo após o choque (~15,5%)
DI_SHOCK, FX_SHOCK, IBOV_DOWN, IBOV_UP = 0.03, 0.20, -0.20, 0.30
HORIZONS = {"3m": 63, "6m": 126, "12m": 252}
MC_DAYS, MC_BLOCK = 252, 21
CRASHES = [  # (data do choque, data de referência pré-choque, rótulo)
    ("2017-05-18", "2017-05-17", "Joesley Day (delação JBS/Temer)"),
    ("2020-03-16", "2020-02-21", "Covid-19 (circuit breakers de março)"),
]
# códigos antigos do mesmo emissor (troca de ticker/ISIN) para alongar o histórico de retornos
PREDECESSORS = {"MOTV3": [("CCRO3", "BRCCROACNOR2")], "AZZA3": [("ARZZ3", "BRARZZACNOR3")],
                "NATU3": [("NTCO3", "BRNTCOACNOR5")]}
METHODS = {"ew": "Pesos iguais", "iv": "Inverso da volatilidade", "rp": "Paridade de risco",
           "mv": "Mínima variância", "ms_tir": "Máximo Sharpe (TIR − CDI)", "ms_up": "Máximo Sharpe (upside anualizado 3a)"}


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def r4(x, d=4):
    if x is None:
        return None
    try:
        xf = float(x)
    except (TypeError, ValueError):
        return x
    return round(xf, d) if math.isfinite(xf) else None


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return r4(o, 6)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, pd.Timestamp):
        return o.strftime("%Y-%m-%d")
    return o


# ============================================================================ dados
def load_fx(offline):
    """Dólar comercial (SGS 1) diário; usa cache e completa pela API do BCB se possível."""
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / "sgs1_usdbrl.json"
    rows = json.load(open(path))["dados"] if path.exists() else []
    last = pd.to_datetime(rows[-1]["data"], dayfirst=True) if rows else None
    if not offline and (last is None or last < TODAY):
        try:
            a = (last + pd.Timedelta(days=1)).strftime("%d/%m/%Y") if last is not None else "01/01/2015"
            url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json&dataInicial={a}&dataFinal={TODAY:%d/%m/%Y}"
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r:
                new = json.loads(r.read().decode())
            if new:
                rows += new
                json.dump({"serie": "BCB SGS 1 - dolar comercial venda (R$/US$)", "dados": rows}, open(path, "w"))
        except Exception as e:  # noqa: BLE001
            log("aviso: câmbio não atualizado:", e)
    if not rows:
        return None
    s = pd.Series({pd.to_datetime(r["data"], dayfirst=True): float(r["valor"]) for r in rows}).sort_index()
    return s[~s.index.duplicated()]


def adjusted(close, sup_issuer, isin):
    """Mesmo ajuste de pipeline/market.py: eventos B3 + razões 'redondas' em saltos > 35% sem evento."""
    evs = split_events(sup_issuer, isin)
    adj = adjust(close, evs)
    rets = adj.pct_change().dropna()
    nice, extra = [2, 3, 4, 5, 8, 10, 20, 25, 50, 100], []
    for d, r_ in rets[rets.abs() > 0.35].items():
        ratio = 1 + r_
        for m in nice:
            for mult in (m, 1 / m):
                if abs(ratio * mult - 1) < 0.08:
                    extra.append((close.index[close.index.get_loc(d) - 1], mult))
    if extra:
        adj = adjust(close, sorted(evs + extra))
    return adj


def isin_segments(groups, isin, sup_issuer):
    """Séries ajustadas de um ISIN, quebradas em buracos > 45 dias (retornos não atravessam o buraco)."""
    if isin not in groups:
        return []
    s = groups[isin].sort_values("date").drop_duplicates("date", keep="last").set_index("date")
    gaps = s.index.to_series().diff().dt.days
    cuts = [s.index[0]] + list(gaps[gaps > 45].index)
    segs = []
    for k, c0 in enumerate(cuts):
        part = s[s.index >= c0]
        if k + 1 < len(cuts):
            part = part[part.index < cuts[k + 1]]
        if len(part) >= 20:
            segs.append((adjusted(part["close"], sup_issuer, isin), part["volume"]))
    return segs


def load_prices(sp, market_docs):
    """Retornos diários ajustados (2016–2026) e volume financeiro por ticker, a partir do COTAHIST."""
    sup = json.load(open(sp / "raw" / "b3" / "supplement.json"))
    df = pd.read_csv(sp / "work" / "cotahist.csv.gz", usecols=["date", "ticker", "close", "volume", "isin"],
                     parse_dates=["date"], dtype={"ticker": str, "isin": str})
    need = {doc["isin"] for doc in market_docs.values()} | {i for v in PREDECESSORS.values() for _, i in v}
    df = df[df["isin"].isin(need)]
    groups = {k: g for k, g in df.groupby("isin")}
    rets, vols, first_obs = {}, {}, {}
    for tk, doc in market_docs.items():
        segs = isin_segments(groups, doc["isin"], sup.get(tk[:4]))
        own_r = [a.pct_change().dropna() for a, _ in segs]
        r = pd.concat(own_r).sort_index() if own_r else pd.Series(dtype=float)
        v = pd.concat([vv for _, vv in segs]).sort_index() if segs else pd.Series(dtype=float)
        for ptk, pisin in PREDECESSORS.get(tk, []):
            for a, vv in isin_segments(groups, pisin, sup.get(ptk[:4])):
                pr = a.pct_change().dropna()
                pr = pr[~pr.index.isin(r.index)]
                r = pd.concat([r, pr]).sort_index()
                v = pd.concat([v, vv[~vv.index.isin(v.index)]]).sort_index()
        r = r[~r.index.duplicated()]
        rets[tk], vols[tk] = r, v[~v.index.duplicated()]
        first_obs[tk] = r.index.min() if len(r) else None
    return rets, vols


def load_market_docs():
    docs = {}
    for f in sorted((ROOT / "data" / "market").glob("*.json")):
        if f.name.startswith("_") or f.stem in ("dividends", "quotes"):
            continue
        d = json.load(open(f))
        if "isin" not in d:
            continue
        mh = (d.get("multiples_history") or {}).get("series") or []
        docs[d["ticker"]] = {"isin": d["isin"], "sector": d.get("sector") or {}, "stats": d.get("stats") or {},
                             "mult": [m for m in mh if not m.get("live")]}
    return docs


# ============================================================================ estatística
def ols(y, x):
    X = np.column_stack([np.ones(len(x)), x])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return b, y - X @ b


def ledoit_wolf_cc(X):
    """Ledoit & Wolf (2004, 'Honey, I shrunk...'): alvo de correlação constante. X: T×N."""
    X = np.asarray(X, float)
    T, N = X.shape
    Xc = X - X.mean(0)
    S = Xc.T @ Xc / T
    var = np.diag(S).copy()
    sd = np.sqrt(var)
    rbar = ((S / np.outer(sd, sd)).sum() - N) / (N * (N - 1))
    F = rbar * np.outer(sd, sd)
    np.fill_diagonal(F, var)
    X2 = Xc ** 2
    pi_mat = X2.T @ X2 / T - S ** 2
    theta = (Xc ** 3).T @ Xc / T - var[:, None] * S
    off = np.outer(1 / sd, sd) * theta
    np.fill_diagonal(off, 0.0)
    rho = np.trace(pi_mat) + rbar * off.sum()
    gamma = ((F - S) ** 2).sum()
    delta = float(max(0.0, min(1.0, (pi_mat.sum() - rho) / gamma / T)))
    return delta * F + (1 - delta) * S, delta, float(rbar), S


def impute(R, rm, rng):
    """Completa retornos ausentes com beta×Ibovespa + resíduo sorteado do próprio papel."""
    out, n_imp = R.copy(), {}
    for c in R.columns:
        y = R[c]
        ok = y.notna() & rm.notna()
        miss = y.isna() & rm.notna()
        n_imp[c] = int(miss.sum())
        if not miss.any():
            continue
        b, res = ols(y[ok].values, rm[ok].values)
        out.loc[miss, c] = b[1] * rm[miss].values + rng.choice(res, size=int(miss.sum()))
    return out, n_imp


# ============================================================================ otimização
def max_investable(groups_idx, ub):
    return sum(min(SECTOR_MAX, ub[g].sum()) for g in groups_idx)


def solve(n, budget, groups_idx, ub, obj, jac=None, x0s=None):
    cons = [{"type": "eq", "fun": lambda w: w.sum() - budget, "jac": lambda w: np.ones_like(w)}]
    for g in groups_idx:
        mask = np.zeros(n)
        mask[g] = 1.0
        cons.append({"type": "ineq", "fun": (lambda w, m=mask: SECTOR_MAX - m @ w), "jac": (lambda w, m=mask: -m)})
    best = None
    for x0 in x0s or [np.full(n, budget / n)]:
        res = minimize(obj, np.clip(x0, 0, ub), jac=jac, bounds=list(zip(np.zeros(n), ub)), constraints=cons,
                       method="SLSQP", options={"maxiter": 2000, "ftol": 1e-14})
        w = np.clip(res.x, 0, ub)
        feas = abs(w.sum() - budget) < 1e-6 and all(w[g].sum() <= SECTOR_MAX + 1e-6 for g in groups_idx)
        val = obj(w) if not isinstance(obj(w), tuple) else obj(w)[0]
        if feas and (best is None or val < best[1]):
            best = (w, val)
    if best is None:
        raise RuntimeError("otimização sem solução viável")
    w = best[0]
    w[w < 1e-6] = 0.0
    return w * budget / w.sum()


def build_portfolio(method, Sig, mu_tir, mu_up, groups_idx, budget, vols):
    n = len(vols)
    ub = np.full(n, W_MAX)
    proj = lambda t: solve(n, budget, groups_idx, ub, lambda w: ((w - t) ** 2).sum(), lambda w: 2 * (w - t), [t])  # noqa: E731
    ew = proj(np.full(n, budget / n))
    iv_t = (1 / vols) / (1 / vols).sum() * budget
    iv = proj(iv_t)
    if method == "ew":
        return ew
    if method == "iv":
        return iv
    if method == "mv":
        return solve(n, budget, groups_idx, ub, lambda w: w @ Sig @ w * 100, lambda w: 200 * Sig @ w, [ew, iv])
    if method == "rp":
        def f(w):
            s = Sig @ w
            rc = w * s / (w @ s)
            return 1e3 * ((rc - 1 / n) ** 2).sum()
        return solve(n, budget, groups_idx, ub, f, None, [iv, ew])
    mu = mu_tir if method == "ms_tir" else mu_up
    ub_m = np.where(np.isfinite(mu), W_MAX, 0.0)
    mu0 = np.nan_to_num(mu, nan=0.0)

    def f(w):
        v = math.sqrt(max(w @ Sig @ w, 1e-12))
        return -(w @ mu0) / v

    def g(w):
        s = Sig @ w
        v = math.sqrt(max(w @ s, 1e-12))
        return -(mu0 / v - (w @ mu0) * s / v ** 3)
    order = np.argsort(-np.where(np.isfinite(mu), mu / vols, -np.inf))
    greedy = np.zeros(n)
    left = budget
    for i in order:
        take = min(W_MAX, left)
        greedy[i] = take
        left -= take
        if left <= 1e-9:
            break
    x0s = [np.minimum(ew, ub_m), np.minimum(iv, ub_m), greedy]
    if max_investable(groups_idx, ub_m) + 1e-9 < budget:
        raise RuntimeError("universo com retorno definido não comporta o orçamento")
    return solve(n, budget, groups_idx, ub_m, f, g, x0s)


# ============================================================================ estresse por ação
def ddm_pv(e, r):
    g = e["g"]
    roe_T = max(e["roe_T"], g + 0.02)
    flows = np.array(e["div"], float)
    flows[0] *= e["f26"]
    pv = float(np.sum(flows / (1 + r) ** np.array(e["taus"], float)))
    tv = e["ni_last"] * (1 + g) * (1 - g / roe_T) / (r - g)
    return pv + tv / (1 + r) ** e["tau_T"]


DI_EARN_YEARS = 3  # o lucro fica menor por 3 anos (ciclo de juros), valor presente sobre o valor de mercado


def di_stress(c, comp_doc, research_doc, d_fallback):
    """+300 bp: canal de lucro (VP de 3 anos de 3 × sensibilidade/100 bp, ÷ valor de mercado)
    × canal de duration (DDM do motor reprecificado a r + 3 p.p.)."""
    e = c.get("engine") or {}
    irr = c.get("irr_implied")
    dur_eff, r_used, note = None, None, []
    if e.get("div") and irr and e.get("ni_last", 0) > 0:
        r_used = max(irr, DI_LONG)  # piso: taxa exigida não fica abaixo do DI longo
        p0, p1 = ddm_pv(e, r_used), ddm_pv(e, r_used + DI_SHOCK)
        if p0 > 0 and p1 > 0:
            dur_eff = p1 / p0 - 1
        if irr < DI_LONG:
            note.append(f"TIR {irr:.1%} < DI longo: duration calculada a {DI_LONG:.1%}")
    if dur_eff is None:
        dur_eff = d_fallback
        note.append("sem DDM utilizável: duration mediana do universo")
    sens = ((research_doc or {}).get("rate_sensitivity") or {}).get("ni_impact_per_100bp_cdi_mn")
    ni_fwd = None
    pj = (comp_doc or {}).get("projections") or {}
    nic = pj.get("ni_controlling") or pj.get("net_income")
    if nic and len(nic) > 1 and nic[1] and nic[1] > 0:
        ni_fwd = nic[1]
    elif c.get("pe_fwd") and c.get("mcap"):
        ni_fwd = c["mcap"] / c["pe_fwd"]
    r_pv = r_used if r_used else max(DI_LONG, 0.20)
    annuity = sum(1 / (1 + r_pv + DI_SHOCK) ** k for k in range(1, DI_EARN_YEARS + 1))
    if sens is None:
        earn = 0.0
        note.append("sensibilidade de lucro não divulgada (banco/sem dado): canal de lucro = 0")
    else:
        earn = float(np.clip(DI_SHOCK * 100 * sens * annuity / c["mcap"], -0.6, 0.3))
    total = (1 + earn) * (1 + dur_eff) - 1
    return {"di_earn": earn, "di_duration": dur_eff, "di_rate_used": r_used, "di_total": total,
            "duration_years": -dur_eff / DI_SHOCK, "ni_sens_100bp_mn": sens, "ni_fwd_mn": ni_fwd,
            "ni_hit_pct_fwd": (DI_SHOCK * 100 * sens / ni_fwd) if (sens is not None and ni_fwd) else None,
            "di_note": "; ".join(note)}


# ============================================================================ métricas
def stationary_idx(pool, n_paths, horizon, L, rng):
    """Bootstrap estacionário (Politis-Romano), circular dentro de cada segmento contíguo do pool:
    ao fim de um segmento o bloco volta ao início do mesmo segmento, o que mantém a amostragem
    uniforme (sem o viés de super-amostrar o fim de cada janela)."""
    pool = np.asarray(pool)
    m = len(pool)
    brk = np.r_[0, np.flatnonzero(np.diff(pool) != 1) + 1, m]
    seg_start, seg_end = np.empty(m, dtype=np.int64), np.empty(m, dtype=np.int64)
    for a, b in zip(brk[:-1], brk[1:]):
        seg_start[a:b], seg_end[a:b] = a, b - 1
    pos = np.empty((n_paths, horizon), dtype=np.int64)
    pos[:, 0] = rng.integers(0, m, n_paths)
    jump = rng.random((n_paths, horizon)) < 1.0 / L
    newp = rng.integers(0, m, (n_paths, horizon))
    for t in range(1, horizon):
        p = pos[:, t - 1]
        nxt = np.where(p == seg_end[p], seg_start[p], p + 1)
        pos[:, t] = np.where(jump[:, t], newp[:, t], nxt)
    return pool[pos]


def dist_summary(x, bins=None):
    q = [1, 5, 10, 25, 50, 75, 90, 95, 99]
    out = {"mean": float(np.mean(x)), "std": float(np.std(x)), **{f"p{k}": float(np.percentile(x, k)) for k in q}}
    if bins is not None:
        c, _ = np.histogram(np.clip(x, bins[0], bins[-1]), bins=bins)
        out["hist_counts"] = c.tolist()
    return out


def var_cvar(x, a=0.05):
    q = np.percentile(x, 100 * a)
    return float(-q), float(-x[x <= q].mean())


# ============================================================================ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sp", default=str(SP_DEFAULT))
    ap.add_argument("--paths", type=int, default=10000)
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--seed", type=int, default=20261026)
    args = ap.parse_args()
    sp = Path(args.sp)
    rng = np.random.default_rng(args.seed)
    OUT.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------------- universo e fundamentos
    ov = json.load(open(ROOT / "data" / "app" / "overview.json"))
    C = {c["ticker"]: c for c in ov["companies"]}
    U = [c["ticker"] for c in ov["companies"]]
    OPP = list(ov["opportunities"])
    cdi = (1 + float(ov["macro"]["cdi"][-1]["valor"]) / 100) ** 252 - 1
    cdi_d = (1 + cdi) ** (1 / 252) - 1
    ib_today = ov["market"]["ibov_today"]
    comp_docs = {t: json.load(open(ROOT / "data" / "app" / "companies" / f"{t}.json")) for t in U}
    res_docs = {t: (json.load(open(ROOT / "research" / f"{t}.json")) if (ROOT / "research" / f"{t}.json").exists() else {}) for t in U}
    log(f"universo {len(U)} | oportunidades {OPP} | CDI {cdi:.4f}")

    # ---------------------------------------------------------------- preços
    mdocs = load_market_docs()
    rets, vols_fin = load_prices(sp, mdocs)
    idx = json.load(open(sp / "raw" / "b3" / "indices.json"))
    ibov = pd.Series({pd.Timestamp(d): v for d, v in idx["IBOV"]}).sort_index()
    ibov = ibov[~ibov.index.duplicated()]
    cal = ibov.index[(ibov.index >= HIST_START) & (ibov.index <= LAST_CLOSE)]
    rm_all = ibov.pct_change().reindex(cal)
    log("séries:", len(rets), "| calendário", cal[0].date(), "→", cal[-1].date())

    # checagem contra data/market/{T}.json (daily_3y)
    chk = []
    for t in U:
        d3 = json.load(open(ROOT / "data" / "market" / f"{t}.json"))["daily_3y"]
        s3 = pd.Series({pd.Timestamp(d): v for d, v in d3}).pct_change().dropna()
        j = pd.concat([s3.rename("a"), rets[t].rename("b")], axis=1, join="inner").dropna()
        chk.append(float((j.a - j.b).abs().max()) if len(j) else None)
    log("máx. |dif| de retorno vs daily_3y:", max(x for x in chk if x is not None))

    R_all = pd.DataFrame({t: rets[t].reindex(cal) for t in U})
    R_fill, n_imp_all = impute(R_all, rm_all, rng)
    w3 = cal > LAST_CLOSE - pd.Timedelta(days=COV_DAYS)
    R3_obs = R_all[w3]
    R3 = R_fill[w3]
    n_imp3 = {t: int(R3_obs[t].isna().sum()) for t in U}
    rm3 = rm_all[w3]

    # ---------------------------------------------------------------- covariância 3a (LW)
    Sig_d, delta, rbar, S_d = ledoit_wolf_cc(R3.values)
    Sig = Sig_d * 252
    vol = np.sqrt(np.diag(Sig))
    corr = Sig / np.outer(vol, vol)
    eig_min_sample = float(np.linalg.eigvalsh(S_d * 252).min())
    log(f"LW: delta={delta:.3f} rbar={rbar:.3f} | vol mediana {np.median(vol):.3f}")

    # betas (3a, observados)
    beta, beta_dn, beta_up = {}, {}, {}
    for t in U:
        j = pd.concat([R3_obs[t].rename("s"), rm3.rename("m")], axis=1).dropna()
        beta[t] = float(np.cov(j.s, j.m)[0, 1] / j.m.var())
        dn, up = j[j.m < 0], j[j.m > 0]
        beta_dn[t] = float(ols(dn.s.values, dn.m.values)[0][1])
        beta_up[t] = float(ols(up.s.values, up.m.values)[0][1])
    ib_vol3 = float(rm3.std() * math.sqrt(252))

    # câmbio: betas semanais 3a (parcial com Ibovespa constante e total/co-movimento)
    fx = load_fx(args.offline)
    fxb = {}
    fx_today = None
    if fx is not None:
        fx_today = float(fx.loc[TODAY] / fx[fx.index < TODAY].iloc[-1] - 1) if TODAY in fx.index else None
        wk_fx = fx[fx.index <= LAST_CLOSE].resample("W-FRI").last().pct_change()
        wk_m = ibov[ibov.index <= LAST_CLOSE].resample("W-FRI").last().pct_change()
        for t in U + ["IBOV"]:
            px = (1 + (rets[t] if t != "IBOV" else ibov.pct_change()).reindex(cal).fillna(0)).cumprod()
            obs = (rets[t] if t != "IBOV" else ibov.pct_change()).reindex(cal).notna()
            px = px.where(obs)
            ws = px.resample("W-FRI").last().pct_change()
            j = pd.concat([ws.rename("s"), wk_m.rename("m"), wk_fx.rename("x")], axis=1, sort=True).dropna()
            j = j[j.index > LAST_CLOSE - pd.Timedelta(days=COV_DAYS)]
            tot = float(np.cov(j.s, j.x)[0, 1] / j.x.var())
            if t == "IBOV":
                fxb[t] = {"fx_beta_total": tot, "fx_beta_partial": None, "n_weeks": int(len(j))}
                continue
            X = np.column_stack([np.ones(len(j)), j.m.values, j.x.values])
            b, *_ = np.linalg.lstsq(X, j.s.values, rcond=None)
            fxb[t] = {"fx_beta_total": tot, "fx_beta_partial": float(b[2]), "n_weeks": int(len(j))}
    log("câmbio hoje:", fx_today)

    # ---------------------------------------------------------------- vetores por ação
    mu_tir = np.array([(C[t]["irr_implied"] - cdi) if C[t].get("irr_implied") is not None else np.nan for t in U])
    mu_up = np.array([((1 + C[t]["upside"]) ** (1 / 3) - 1) if C[t].get("upside") is not None else np.nan for t in U])
    today_r = {t: C[t]["price_ref"] / C[t]["prev_close"] - 1 for t in U}
    ib_chg = ib_today["chg"]
    # duration de reserva = mediana dos que têm DDM
    tmp = []
    for t in U:
        e = C[t].get("engine") or {}
        if e.get("div") and C[t].get("irr_implied") and e.get("ni_last", 0) > 0:
            r_ = max(C[t]["irr_implied"], DI_LONG)
            p0, p1 = ddm_pv(e, r_), ddm_pv(e, r_ + DI_SHOCK)
            if p0 > 0 and p1 > 0:
                tmp.append(p1 / p0 - 1)
    d_fallback = float(np.median(tmp))
    stock = {}
    for i, t in enumerate(U):
        c = C[t]
        di = di_stress(c, comp_docs[t], res_docs[t], d_fallback)
        fb = fxb.get(t, {})
        stock[t] = {
            "ticker": t, "name": c.get("name"), "setor": c["sector"]["setor"], "subsetor": c["sector"]["subsetor"],
            "segmento": c["sector"]["segmento"], "opportunity": t in OPP, "price": c["price_ref"], "prev_close": c["prev_close"],
            "ret_today": today_r[t], "fair_value": c.get("fair_value"), "upside": c.get("upside"), "irr": c.get("irr_implied"),
            "mu_tir": mu_tir[i], "mu_up": mu_up[i], "vol": vol[i], "beta": beta[t], "beta_down": beta_dn[t], "beta_up": beta_up[t],
            "beta_down_market_json": c.get("beta"), "nd_ebitda": c.get("nd_ebitda"), "mcap": c.get("mcap"), "adtv": c.get("adtv"),
            "imputed_days_3y": n_imp3[t], "imputed_days_10y": n_imp_all[t],
            "stress": {
                "ibov_m20": beta_dn[t] * IBOV_DOWN,
                "ibov_m20_beta_hoje": today_r[t] / ib_chg * IBOV_DOWN,
                "ibov_p30": beta_up[t] * IBOV_UP,
                "di_p300": di["di_total"],
                "usd_p20_puro": fb.get("fx_beta_partial", np.nan) * FX_SHOCK if fb else None,
                "usd_p20_comov": fb.get("fx_beta_total", np.nan) * FX_SHOCK if fb else None,
            },
            "di_detail": di, "fx_detail": fb,
        }

    # ---------------------------------------------------------------- carteiras
    def groups_for(names, level):
        lab = [stock[t][level] for t in names]
        return [np.array([k for k, x in enumerate(lab) if x == g]) for g in sorted(set(lab))]

    specs = [
        ("op7_b3", OPP, "setor", f"{len(OPP)} oportunidades · setor B3 ≤ 40% (excedente em CDI)"),
        ("op7_sub", OPP, "subsetor", f"{len(OPP)} oportunidades · subsetor B3 ≤ 40%"),
        ("u59", U, "setor", "Universo de 59 · setor B3 ≤ 40%"),
    ]
    sel = {t: i for i, t in enumerate(U)}
    ports = []
    R_hist = R_fill.values  # 2016–2026 completo
    for pid, names, level, label in specs:
        ii = np.array([sel[t] for t in names])
        Sg = Sig[np.ix_(ii, ii)]
        grp = groups_for(names, level)
        budget = min(1.0, max_investable(grp, np.full(len(ii), W_MAX)))
        for m in METHODS:
            w_sub = build_portfolio(m, Sg, mu_tir[ii], mu_up[ii], grp, budget, vol[ii])
            w = np.zeros(len(U))
            w[ii] = w_sub
            ports.append({"id": f"{pid}_{m}", "universe": pid, "method": m, "label": f"{label} · {METHODS[m]}",
                          "sector_rule": level, "budget": budget, "w": w})
    log("carteiras:", len(ports))

    # recomendada: núcleo das 7 oportunidades (50% máx. Sharpe TIR + 50% paridade de risco, setor B3 ≤ 40%) + CDI;
    # alternativa: máx. Sharpe (TIR) do universo de 59 dimensionado por meio Kelly, resto em CDI
    def find(pid):
        return next(p for p in ports if p["id"] == pid)

    def add(pid, w, label, universe="blend"):
        ports.append({"id": pid, "universe": universe, "method": "blend", "label": label, "sector_rule": "setor",
                      "budget": float(w.sum()), "w": w})
    add("rec_op7_core", 0.5 * find("op7_b3_ms_tir")["w"] + 0.5 * find("op7_b3_rp")["w"],
        f"Recomendada · {len(OPP)} oportunidades (50% máx. Sharpe TIR + 50% paridade de risco), setor B3 ≤ 40%, excedente em CDI", "op7_b3")
    w_ms = find("u59_ms_tir")["w"]
    k_half = float(min(1.0, (np.nansum(w_ms * mu_tir) / (w_ms @ Sig @ w_ms)) / 2))
    add("alt_u59_halfkelly", k_half * w_ms, f"Alternativa · máx. Sharpe (TIR) do universo de 59 × meio Kelly ({k_half:.0%}), resto em CDI", "u59")

    # ---------------------------------------------------------------- métricas ex-ante, estresses, MC
    beta_v = np.array([beta[t] for t in U])
    bdn_v = np.array([beta_dn[t] for t in U])
    bup_v = np.array([beta_up[t] for t in U])
    st_keys = list(stock[U[0]]["stress"].keys())
    st_mat = {k: np.array([np.nan if stock[t]["stress"][k] is None else stock[t]["stress"][k] for t in U], float) for k in st_keys}
    adtv_v = np.array([C[t].get("adtv") or np.nan for t in U])
    setor_v = np.array([stock[t]["setor"] for t in U])
    sub_v = np.array([stock[t]["subsetor"] for t in U])
    today_v = np.array([today_r[t] for t in U])

    # pools do bootstrap: todos os dias 2016–2026 e "crise" = decil superior da vol. realizada 21d do Ibovespa
    rv21 = rm_all.rolling(21).std() * math.sqrt(252)
    thr = float(rv21.quantile(0.90))
    crisis_mask = (rv21 >= thr).values
    pool_all = np.arange(len(cal))[1:]
    pool_cr = np.arange(len(cal))[crisis_mask]
    crisis_segments = []
    if len(pool_cr):
        start = prev = pool_cr[0]
        for k in pool_cr[1:]:
            if k != prev + 1:
                crisis_segments.append((cal[start], cal[prev]))
                start = k
            prev = k
        crisis_segments.append((cal[start], cal[prev]))
    idx_all = stationary_idx(pool_all, args.paths, MC_DAYS, MC_BLOCK, rng)
    idx_cr = stationary_idx(pool_cr, args.paths, MC_DAYS, MC_BLOCK, rng)
    bins = np.round(np.arange(-0.8, 1.6001, 0.05), 4)
    mu_tot_stock = np.array([C[t]["irr_implied"] if C[t].get("irr_implied") is not None else cdi for t in U])
    tgt = (1 + mu_tot_stock) ** (1 / 252) - 1                 # deriva diária = TIR de dono (CDI se ausente)
    shift_all = tgt - R_hist[pool_all].mean(0)                 # troca a média 2016–2026 pela TIR
    shift_cr = tgt - R_hist[pool_cr].mean(0)                   # troca a média dos dias de crise pela TIR
    SHOCK_DAYS = 63                                            # regime "choque": 3 meses de crise + 9 meses normais
    log(f"bootstrap: {len(pool_all)} dias, crise {len(pool_cr)} dias (vol21 ≥ {thr:.1%})")

    def evaluate(p):
        w = p["w"]
        cash = 1 - w.sum()
        inv = w.sum()
        v = float(math.sqrt(w @ Sig @ w))
        ex_tir = float(np.nansum(w * mu_tir))
        ex_up = float(np.nansum(w * mu_up))
        s1m = v * math.sqrt(21 / 252)
        m1m = (cdi + ex_tir) / 12
        rc = w * (Sig @ w) / (v ** 2) if v > 0 else w * 0
        wn = w / inv
        hhi = float((wn ** 2).sum())
        div_ratio = float((w * vol).sum() / v) if v > 0 else None
        rp_series = R_hist @ w + cash * cdi_d
        lr = np.log1p(rp_series[1:])
        r21 = np.exp(pd.Series(lr).rolling(21).sum().dropna().values) - 1  # janelas de 21 d sobrepostas 2016–2026
        rs_cr_tir = (R_hist + shift_cr) @ w + cash * cdi_d
        r21_cr = np.expm1(np.log1p(rs_cr_tir[idx_cr[:, :21]]).sum(1))     # 1º mês de trajetórias de crise (deriva TIR)
        vh, ch = var_cvar(r21)
        vc, cc = var_cvar(r21_cr)
        sectors = {}
        for s_, x in zip(setor_v, w):
            if x > 0:
                sectors[s_] = sectors.get(s_, 0) + float(x)
        subs = {}
        for s_, x in zip(sub_v, w):
            if x > 0:
                subs[s_] = subs.get(s_, 0) + float(x)
        aum = 100.0  # R$ mi
        liq = w * aum / (0.2 * adtv_v)
        stress = {k: float(np.nansum(w * st_mat[k])) for k in st_keys}
        metrics = {
            "invested": inv, "cash_cdi": cash, "n_names": int((w > 0).sum()), "vol": v, "vol_crisis_hist": None,
            "beta": float(w @ beta_v), "beta_down": float(w @ bdn_v), "beta_up": float(w @ bup_v),
            "exp_excess_tir": ex_tir, "exp_total_tir": cdi + ex_tir, "sharpe_tir": ex_tir / v if v else None,
            "exp_excess_up": ex_up, "sharpe_up": ex_up / v if v else None,
            "var95_1m_param": float(-(m1m - norm.ppf(0.95) * s1m)), "cvar95_1m_param": float(-(m1m - s1m * norm.pdf(norm.ppf(0.95)) / 0.05)),
            "var95_1m_hist": vh, "cvar95_1m_hist": ch, "var95_1m_crisis": vc, "cvar95_1m_crisis": cc,
            "hhi": hhi, "n_eff": 1 / hhi, "max_w": float(w.max()), "top3": float(np.sort(w)[-3:].sum()),
            "max_rc": float(rc.max()), "div_ratio": div_ratio,
            "ret_today_exante": float(w @ today_v), "ret_today_pred_beta_down": float(w @ bdn_v) * ib_chg,
            "days_to_liquidate_max_100mn": float(np.nanmax(np.where(w > 0, liq, np.nan))),
        }
        metrics["vol_crisis_hist"] = float(np.std(rp_series[crisis_mask]) * math.sqrt(252))
        # Monte Carlo 1 ano
        mc = {}
        rs = R_hist @ w + cash * cdi_d
        rs_tir = (R_hist + shift_all) @ w + cash * cdi_d
        regimes = {
            "normal_hist": np.log1p(rs[idx_all]),
            "normal_tir": np.log1p(rs_tir[idx_all]),
            "crise_tir": np.log1p(rs_cr_tir[idx_cr]),
            "choque_tir": np.concatenate([np.log1p(rs_cr_tir[idx_cr[:, :SHOCK_DAYS]]), np.log1p(rs_tir[idx_all[:, SHOCK_DAYS:]])], 1),
            "crise_hist": np.log1p(rs[idx_cr]),
        }
        for nm, paths in regimes.items():
            tot = np.expm1(paths.sum(1))
            cum = np.cumsum(paths, 1)
            mdd = np.expm1((cum - np.maximum.accumulate(np.maximum(cum, 0), 1)).min(1))
            d_ = dist_summary(tot, bins)
            d_.update({"p_loss": float((tot < 0).mean()), "p_below_cdi": float((tot < cdi).mean()),
                       "p_loss_20": float((tot < -0.2).mean()), "p_gain_30": float((tot > 0.3).mean()),
                       "mdd_median": float(np.median(mdd)), "mdd_p5": float(np.percentile(mdd, 5)),
                       "p_dd_25": float((mdd < -0.25).mean())})
            if nm in ("normal_tir", "choque_tir"):
                fan = np.expm1(cum[:, 20::21])
                d_["fan_months"] = list(range(1, fan.shape[1] + 1))
                d_["fan"] = {f"p{k}": np.percentile(fan, k, axis=0).tolist() for k in (5, 25, 50, 75, 95)}
            # Kelly numérico: fração f na carteira e (1 − f) em CDI, máx E[log]
            grid = np.arange(0, 3.001, 0.01)
            el = [np.mean(np.log(np.maximum(1 + cdi + f * (tot - cdi), 1e-9))) for f in grid]
            d_["kelly_full"] = float(grid[int(np.argmax(el))])
            mc[nm] = d_
        kelly_an = ex_tir / v ** 2 if v else None
        kelly = {"analytic_full": kelly_an, "analytic_half": kelly_an / 2 if kelly_an else None, "analytic_quarter": kelly_an / 4 if kelly_an else None,
                 "bootstrap_full_normal_tir": mc["normal_tir"]["kelly_full"], "bootstrap_full_choque_tir": mc["choque_tir"]["kelly_full"],
                 "bootstrap_full_crise_tir": mc["crise_tir"]["kelly_full"]}
        weights = [{"ticker": t, "w": float(x), "setor": stock[t]["setor"], "subsetor": stock[t]["subsetor"], "rc": float(rc[k]),
                    "irr": C[t].get("irr_implied"), "upside": C[t].get("upside")} for k, (t, x) in enumerate(zip(U, w)) if x > 1e-6]
        weights.sort(key=lambda r: -r["w"])
        return {"id": p["id"], "universe": p["universe"], "method": p["method"], "label": p["label"], "sector_rule": p["sector_rule"],
                "weights": weights, "metrics": metrics, "sectors": dict(sorted(sectors.items(), key=lambda kv: -kv[1])),
                "subsectors": dict(sorted(subs.items(), key=lambda kv: -kv[1])), "stress": stress, "mc": mc, "kelly": kelly}

    results = [evaluate(p) for p in ports]
    log("métricas ok")

    # ---------------------------------------------------------------- backtest: comprar no crash
    bt = crash_backtest(mdocs, rets, vols_fin, ibov, cal)
    log("backtest ok")

    # ---------------------------------------------------------------- saída
    rec = next(r for r in results if r["id"] == "rec_op7_core")
    out = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "as_of": TODAY.strftime("%Y-%m-%d"),
        "params": {"cdi": cdi, "di_long": DI_LONG, "w_max": W_MAX, "sector_max": SECTOR_MAX, "cov_window": f"{(cal[w3][0]).date()} a {LAST_CLOSE.date()} (diário)",
                   "cov_obs": int(w3.sum()), "lw_shrinkage": delta, "lw_target": "correlação constante", "lw_rbar": rbar,
                   "sample_cov_min_eig": eig_min_sample, "ibov_vol_3y": ib_vol3, "ibov_today": ib_chg, "usd_today": fx_today,
                   "shocks": {"ibov_down": IBOV_DOWN, "ibov_up": IBOV_UP, "di": DI_SHOCK, "usd": FX_SHOCK},
                   "mc": {"paths": args.paths, "days": MC_DAYS, "mean_block": MC_BLOCK, "seed": args.seed, "crisis_vol21_threshold": thr,
                          "crisis_days": int(len(pool_cr)), "crisis_segments": [[a.strftime("%Y-%m-%d"), b.strftime("%Y-%m-%d")] for a, b in crisis_segments],
                          "bins": bins.tolist()},
                   "di_duration_fallback": d_fallback,
                   "ibov_usd_p20_comov": (fxb.get("IBOV", {}).get("fx_beta_total") or float("nan")) * FX_SHOCK,
                   "notes": ["Retorno esperado = TIR de dono − CDI (alternativa: (1+upside)^(1/3) − 1).",
                             "Betas de 3 anos diários; beta de baixa/alta = OLS só nos dias de queda/alta do Ibovespa.",
                             "DI +300 bp = (1 + canal de lucro) × (1 + canal de duration) − 1. Lucro: valor presente de 3 anos de 3 × sensibilidade do lucro por 100 bp de CDI (research/{T}.json) ÷ valor de mercado; bancos sem dado = 0. Duration: DDM do motor (mesmos fluxos da TIR de dono) reprecificado a r + 3 p.p., r = max(TIR, DI longo 15,5%).",
                             "Dólar +20%: 'puro' = beta cambial semanal (3a) com Ibovespa constante; 'comov' = beta univariado (inclui a queda típica da bolsa quando o dólar sobe).",
                             "Monte Carlo: bootstrap estacionário (bloco médio 21 d) de retornos diários 2016–2026; 'crise' sorteia só dias com vol. 21d do Ibovespa no decil superior; 'tir' troca a média histórica de cada ação pela TIR de dono.",
                             "Ausências de histórico (ex.: MOTV3 entre CCRO3 e MOTV3) preenchidas com beta × Ibovespa + resíduo sorteado."]},
        "universe": [stock[t] for t in U],
        "covariance": {"tickers": U, "vol": vol.tolist(), "corr": np.round(corr, 3).tolist(), "shrinkage": delta},
        "portfolios": results,
        "recommended": {"id": rec["id"], "label": rec["label"], "weights": rec["weights"], "metrics": rec["metrics"], "stress": rec["stress"],
                        "weights_equity_sleeve": [{"ticker": x["ticker"], "w": x["w"] / rec["metrics"]["invested"]} for x in rec["weights"]],
                        "sizing": sizing(rec)},
        "stress_long": [{"portfolio": r["id"], "scenario": k, "value": v} for r in results for k, v in r["stress"].items()],
        "backtest": bt,
    }
    out["universe"] = jsonable(out["universe"])
    json.dump(jsonable(out), open(OUT / "portfolio.json", "w"), ensure_ascii=False)
    (OUT / "portfolio.md").write_text(render_md(out, results, stock, U, OPP, cdi), encoding="utf-8")
    log("gravado:", OUT / "portfolio.json", OUT / "portfolio.md")


# ============================================================================ dimensionamento
def sizing(r):
    """Exposição em ações sugerida = meio Kelly (fração da carteira-alvo × parcela investida), por regime."""
    inv, k = r["metrics"]["invested"], r["kelly"]
    half = {"choque_3m": k["bootstrap_full_choque_tir"] / 2, "normal_bootstrap": k["bootstrap_full_normal_tir"] / 2,
            "analitico": (k["analytic_full"] or 0) / 2, "crise_ano": k["bootstrap_full_crise_tir"] / 2}
    eq = {nm: min(1.0, f) * inv for nm, f in half.items()}
    return {"half_kelly_fraction_of_target": half, "equity_exposure": eq, "target_equity": inv,
            "entry_equity": eq["choque_3m"], "full_equity_if_vol_normalizes": min(inv, max(eq["normal_bootstrap"], eq["analitico"])),
            "rule": "começar no meio Kelly do regime de choque e subir até o meio Kelly normal/analítico (teto = parcela investida da carteira-alvo) quando a vol. 21d do Ibovespa sair do decil superior"}


# ============================================================================ backtest
def ibov_episodes(ibov, thr=-0.05, gap=60):
    """Episódios de queda diária ≤ −5% do Ibovespa desde 1998 (≥ 60 dias entre episódios) e retornos seguintes."""
    cal, r = ibov.index, ibov.pct_change()
    eps, last = [], None
    for d, v in r[r <= thr].items():
        if last is None or (d - last).days > gap:
            i0 = cal.get_loc(d)
            eps.append({"date": d.strftime("%Y-%m-%d"), "ret": float(v),
                        **{f"f{h}": (float(ibov.iloc[i0 + n] / ibov.iloc[i0] - 1) if i0 + n < len(cal) else None) for h, n in HORIZONS.items()}})
        last = d
    summ = {}
    for h in HORIZONS:
        x = np.array([e[f"f{h}"] for e in eps if e[f"f{h}"] is not None])
        summ[h] = {"n": int(len(x)), "median": float(np.median(x)), "mean": float(x.mean()), "pct_pos": float((x > 0).mean()), "min": float(x.min()), "max": float(x.max())}
    return {"episodes": eps, "summary": summ}


def crash_backtest(mdocs, rets, vols_fin, ibov, cal_unused):
    cal = ibov.index
    ib_r = ibov.pct_change()
    events = []
    for d_s, ref_s, label in CRASHES:
        d, ref = pd.Timestamp(d_s), pd.Timestamp(ref_s)
        i0 = cal.get_loc(d)
        rows = []
        for t, doc in mdocs.items():
            r = rets.get(t)
            if r is None or d not in r.index or r.index.min() > ref - pd.Timedelta(days=120):
                continue
            span = cal[(cal > ref) & (cal <= cal[min(i0 + 252, len(cal) - 1)])]
            rr = r.reindex(cal[(cal >= r.index.min())]).fillna(0.0)
            px = (1 + rr).cumprod()
            if ref not in px.index:
                continue
            v = vols_fin[t]
            adtv = float(v[(v.index < d) & (v.index >= d - pd.Timedelta(days=95))].mean() / 1e6) if len(v) else 0.0
            if not np.isfinite(adtv) or adtv < 10:
                continue
            drop = float(px[d] / px[ref] - 1)
            day = float(r.get(d, np.nan))
            me = [m for m in doc["mult"] if pd.Timestamp(m["date"]) < d.replace(day=1)]
            pe = pbv = dy = None
            if me:
                m = me[-1]
                pm = pd.Timestamp(m["date"])
                pref = px[px.index <= pm]
                scale = float(px[d] / pref.iloc[-1]) if len(pref) else None
                if scale:  # múltiplos do fim do mês anterior levados ao preço do dia do choque; fora da faixa = erro de unidade
                    pe = m["pe"] * scale if m.get("pe") and m["pe"] > 0 else None
                    pe = pe if pe is not None and 1.0 <= pe <= 60.0 else None
                    pbv = m["pbv"] * scale if m.get("pbv") and m["pbv"] > 0 else None
                    pbv = pbv if pbv is not None and 0.1 <= pbv <= 20.0 else None
                dy = m.get("dy") if m.get("dy") is not None and 0.0 <= m.get("dy") <= 0.15 else 0.0
            fw = {}
            path = []
            for h, n in HORIZONS.items():
                if i0 + n < len(cal):
                    fw[h] = float(px[cal[i0 + n]] / px[d] - 1 + (dy or 0) * n / 252)
            if i0 + 252 < len(cal):
                path = (px[cal[i0:i0 + 253]] / px[d]).values.tolist()
            rows.append({"ticker": t, "setor": doc["sector"].get("setor"), "adtv": adtv, "drop": drop, "day": day, "pe": pe, "pbv": pbv,
                         "ey": 1 / pe if pe else None, "dy": dy, **{f"f{h}": fw.get(h) for h in HORIZONS}, "_path": path})
        df = pd.DataFrame(rows)
        q_drop = df["drop"].quantile(1 / 3)
        q_drop_hi = df["drop"].quantile(2 / 3)
        ey_ok = df["ey"].notna()
        q_ey = df.loc[ey_ok, "ey"].quantile(2 / 3)
        df["score"] = np.nan
        sub = df[ey_ok]
        df.loc[ey_ok, "score"] = sub["drop"].rank(pct=True, ascending=False) + sub["ey"].rank(pct=True)
        q_sc = df["score"].quantile(0.8)
        baskets = {
            "todas": df.index,
            "mais_caidas": df.index[df["drop"] <= q_drop],
            "menos_caidas": df.index[df["drop"] >= q_drop_hi],
            "mais_baratas": df.index[ey_ok & (df["ey"] >= q_ey)],
            "caidas_e_baratas": df.index[df["score"] >= q_sc],
        }
        ibf = {h: float(ibov[cal[i0 + n]] / ibov[d] - 1) for h, n in HORIZONS.items() if i0 + n < len(cal)}
        ib_path = (ibov[cal[i0:i0 + 253]] / ibov[d]).values.tolist()
        bk = []
        for nm, ix in baskets.items():
            b = df.loc[ix]
            rec = {"name": nm, "n": int(len(b)), "tickers": b.sort_values("drop")["ticker"].tolist(),
                   "drop_mean": float(b["drop"].mean()), "pe_median": float(b["pe"].median()) if b["pe"].notna().any() else None}
            for h in HORIZONS:
                x = b[f"f{h}"].dropna()
                if len(x):
                    rec[f"ret_{h}"] = float(x.mean())
                    rec[f"median_{h}"] = float(x.median())
                    rec[f"excess_{h}"] = float(x.mean() - ibf[h])
                    rec[f"hit_{h}"] = float((x > ibf[h]).mean())
            paths = [p for p in b["_path"] if len(p) == 253]
            if paths:
                pm = np.mean(np.array(paths), 0)
                rec["path"] = np.round(pm, 4).tolist()
                rec["max_dd_12m"] = float((pm / np.maximum.accumulate(pm) - 1).min())
            bk.append(rec)
        # regressão cross-section: retorno 12m ~ queda + L/P
        xs = df.dropna(subset=["f12m"])
        b_drop = float(np.polyfit(xs["drop"], xs["f12m"], 1)[0]) if len(xs) > 10 else None
        xe = xs[xs["ey"].notna()]
        b_ey = float(np.polyfit(xe["ey"], xe["f12m"], 1)[0]) if len(xe) > 10 else None
        rank_ic = {}
        for h in HORIZONS:
            z = df.dropna(subset=[f"f{h}"])
            rank_ic[f"drop_{h}"] = float(z["drop"].rank().corr(z[f"f{h}"].rank()))
            ze = z[z["ey"].notna()]
            rank_ic[f"ey_{h}"] = float(ze["ey"].rank().corr(ze[f"f{h}"].rank()))
        events.append({"date": d_s, "ref_date": ref_s, "label": label, "n_universe": int(len(df)),
                       "ibov_drop": float(ibov[d] / ibov[ref] - 1), "ibov_day": float(ib_r[d]), "ibov_fwd": ibf, "ibov_path": np.round(ib_path, 4).tolist(),
                       "baskets": bk, "slope_f12m_on_drop": b_drop, "slope_f12m_on_ey": b_ey, "rank_ic": rank_ic,
                       "stocks": df.drop(columns=["_path"]).to_dict("records")})
    return {"ibov_crash_episodes": ibov_episodes(ibov),
            "universe_rule": "tickers de data/market com histórico na data, ADTV 3m ≥ R$ 10 mi (viés de sobrevivência: lista atual)",
            "dividends": "retornos de preço + DY 12m na data × prazo (aprox.)", "events": events}


# ============================================================================ relatório
def pct(x, d=1):
    return "—" if x is None or (isinstance(x, float) and not math.isfinite(x)) else f"{x * 100:.{d}f}%".replace(".", ",")


def num(x, d=2):
    return "—" if x is None or (isinstance(x, float) and not math.isfinite(x)) else f"{x:.{d}f}".replace(".", ",")


def wfmt(weights, k=8):
    txt = " · ".join(f"{w['ticker']} {w['w'] * 100:.0f}".replace(".", ",") for w in weights[:k])
    return txt + (f" … (+{len(weights) - k})" if len(weights) > k else "")


def render_md(out, results, stock, U, OPP, cdi):
    P = out["params"]
    by = {r["id"]: r for r in results}
    rec = out["recommended"]
    m, st, sz = rec["metrics"], rec["stress"], rec["sizing"]
    rmc = by[rec["id"]]["mc"]
    alt = by["alt_u59_halfkelly"]
    bt = out["backtest"]
    n_cc = sum(1 for t in OPP if stock[t]["setor"] == "Consumo Cíclico")
    L = []
    L.append("# Carteiras pós-choque — 26/10/2026\n")
    L.append(f"Gerado por `pipeline/tests/portfolio.py` em {out['generated_at']} (dados: `data/app/overview.json`, preços B3 ajustados 2016–2026, "
             f"câmbio BCB). Ibovespa {pct(P['ibov_today'])} no dia, dólar {pct(P['usd_today'])}, CDI {pct(cdi, 2)}, DI longo ~{pct(P['di_long'])}. "
             f"Limites: {pct(P['w_max'], 0)} por ação e {pct(P['sector_max'], 0)} por setor B3. Estudo quantitativo com finalidade informativa; "
             "não é recomendação de investimento.\n")

    # ------------------------------------------------------------ resumo
    L.append("## Resumo\n")
    L.append(f"- **Carteira recomendada (alvo):** {wfmt(rec['weights'])} (% do capital) + **{pct(m['cash_cdi'], 0)} em CDI**. "
             f"São as {len(OPP)} oportunidades do estudo, com pesos de 50% máximo Sharpe (TIR − CDI) e 50% paridade de risco. "
             f"{n_cc} das {len(OPP)} são Consumo Cíclico, então o limite de 40% por setor só permite investir {pct(m['invested'], 0)}; o resto fica no CDI.")
    L.append(f"- **Tamanho (Kelly fracionado):** meio Kelly dá {pct(sz['equity_exposure']['choque_3m'], 0)} do capital em ações no regime de choque "
             f"(3 meses de volatilidade de crise) e {pct(sz['equity_exposure']['normal_bootstrap'], 0)}–{pct(sz['equity_exposure']['analitico'], 0)} "
             f"no regime normal. Sugestão: entrar com ~{pct(sz['entry_equity'], 0)} e subir até {pct(sz['full_equity_if_vol_normalizes'], 0)} "
             "quando a volatilidade normalizar.")
    L.append(f"- **Risco ex-ante (carteira-alvo):** vol {pct(m['vol'])} a.a., beta {num(m['beta'])} (beta de baixa {num(m['beta_down'])}), "
             f"retorno esperado {pct(m['exp_total_tir'])} a.a. ({pct(m['exp_excess_tir'])} acima do CDI), Sharpe {num(m['sharpe_tir'])}. "
             f"VaR 95% de 1 mês: {pct(m['var95_1m_param'])} (normal) e {pct(m['var95_1m_crisis'])} no regime de crise; "
             f"CVaR {pct(m['cvar95_1m_hist'])} no histórico 2016–2026 e {pct(m['cvar95_1m_crisis'])} na crise. "
             f"N efetivo {num(m['n_eff'], 1)}; BEEF3 responde por {pct(rec['weights'][0]['rc'], 0)} do risco.")
    L.append(f"- **Estresses (carteira-alvo):** Ibovespa −20% → {pct(st['ibov_m20'])} pelo beta de baixa, ou {pct(st['ibov_m20_beta_hoje'])} "
             f"repetindo a reação de hoje; DI +300 bp → {pct(st['di_p300'])}; dólar +20% → {pct(st['usd_p20_puro'])} no canal cambial puro "
             f"e {pct(st['usd_p20_comov'])} com o co-movimento histórico da bolsa. Na reversão (Ibovespa +30%), {pct(st['ibov_p30'])}. "
             f"No pregão de hoje a carteira teria rendido {pct(m['ret_today_exante'])}; o beta de baixa previa {pct(m['ret_today_pred_beta_down'])}.")
    nt, ch = rmc["normal_tir"], rmc["choque_tir"]
    L.append(f"- **Monte Carlo 1 ano (deriva = TIR):** no regime normal, mediana {pct(nt['p50'])}, p5 {pct(nt['p5'])}, P(perda) {pct(nt['p_loss'], 0)} "
             f"e P(abaixo do CDI) {pct(nt['p_below_cdi'], 0)}. Com 3 meses de choque, mediana {pct(ch['p50'])}, p5 {pct(ch['p5'])}, "
             f"P(perda) {pct(ch['p_loss'], 0)} e drawdown mediano {pct(ch['mdd_median'])}.")
    am = alt["metrics"]
    L.append(f"- **Alternativa totalmente diversificável:** o máximo Sharpe do universo de 59 ({wfmt(by['u59_ms_tir']['weights'])}) "
             f"tem Sharpe {num(by['u59_ms_tir']['metrics']['sharpe_tir'])}, mas inclui nomes fora das oportunidades (BBAS3, HAPV3, BRSR6). "
             f"Dimensionado a meio Kelly ({pct(am['invested'], 0)} em ações), fica com risco parecido (vol {pct(am['vol'])}, Ibovespa −20% → "
             f"{pct(alt['stress']['ibov_m20'])}).")
    evs = bt["events"]
    parts = []
    for ev in evs:
        bb = {x["name"]: x for x in ev["baskets"]}
        mc_, mb_ = bb["mais_caidas"], bb["mais_baratas"]
        parts.append(f"em {ev['date']}, as mais caídas subiram {pct(mc_.get('ret_3m'))} em 3m (mediana {pct(mc_.get('median_3m'))}; "
                     f"{pct(mc_.get('hit_3m'), 0)} acima do índice), contra {pct(ev['ibov_fwd']['3m'])} do Ibovespa. Em 12m, a mediana delas foi "
                     f"{pct(mc_.get('median_12m'))}, contra {pct(ev['ibov_fwd']['12m'])} do índice, e a das mais baratas por P/L {pct(mb_.get('median_12m'))}. "
                     f"Depois da compra, o drawdown chegou a {pct(min(x.get('max_dd_12m', 0) for x in ev['baskets']))}")
    es = bt["ibov_crash_episodes"]["summary"]["12m"]
    e2020 = next((e["f12m"] for e in bt["ibov_crash_episodes"]["episodes"] if e["date"] == "2020-02-26"), None)
    L.append(f"- **Histórico de crashes:** {'; '.join(parts)}. A reversão das mais caídas é forte e ampla nos primeiros 3–6 meses "
             f"(correlação de ranking entre a queda e o retorno de 3m: {num(evs[0]['rank_ic']['drop_3m'])} e {num(evs[1]['rank_ic']['drop_3m'])}), "
             "mas em 12 meses a vantagem da ação mediana diminui ou some. O P/L baixo, isolado, bateu o índice em 2017 e perdeu em 2020. "
             f"Nos {es['n']} episódios de queda diária ≤ −5% do Ibovespa desde 1998, comprar no 1º dia rendeu mediana de {pct(es['median'])} em 12m "
             f"({pct(es['pct_pos'], 0)} positivos). Em 2020, comprar em 26/02 rendeu {pct(e2020)}, contra {pct(evs[1]['ibov_fwd']['12m'])} comprando em 16/03. "
             "O risco de entrar cedo justifica a entrada escalonada.\n")

    # ------------------------------------------------------------ recomendada
    L.append("## Carteira recomendada\n")
    L.append(f"**{rec['label']}**\n")
    L.append("| Ação | % capital | % das ações | Setor / subsetor | TIR | Upside | Contrib. risco | Beta baixa | DI +300 | Dólar +20% puro |\n|---|---:|---:|---|---:|---:|---:|---:|---:|---:|")
    for w, ws in zip(rec["weights"], rec["weights_equity_sleeve"]):
        s_ = stock[w["ticker"]]
        L.append(f"| {w['ticker']} | {pct(w['w'])} | {pct(ws['w'])} | {s_['setor']} / {s_['subsetor']} | {pct(w['irr'])} | {pct(w['upside'])} | {pct(w['rc'])} | "
                 f"{num(s_['beta_down'])} | {pct(s_['stress']['di_p300'])} | {pct(s_['stress']['usd_p20_puro'])} |")
    L.append(f"| CDI | {pct(m['cash_cdi'])} | — | caixa | {pct(cdi, 2)} | — | 0% | 0 | 0% | 0% |\n")
    L.append("Dimensionamento por Kelly (fração da carteira-alvo; exposição resultante em ações):\n")
    L.append("| Regime | Kelly cheio | Meio Kelly | Ações / capital |\n|---|---:|---:|---:|")
    kk = by[rec["id"]]["kelly"]
    for nm, full in (("analitico", kk["analytic_full"]), ("normal_bootstrap", kk["bootstrap_full_normal_tir"]),
                     ("choque_3m", kk["bootstrap_full_choque_tir"]), ("crise_ano", kk["bootstrap_full_crise_tir"])):
        L.append(f"| {nm} | {num(full)} | {num(sz['half_kelly_fraction_of_target'][nm])} | {pct(sz['equity_exposure'][nm], 0)} |")
    L.append(f"\nRegra: {sz['rule']}.\n")

    # ------------------------------------------------------------ todas as carteiras
    L.append("## Carteiras testadas\n")
    L.append(f"`op7_b3` = {len(OPP)} oportunidades com setor B3 ≤ 40% (máximo investível 60%, resto em CDI); `op7_sub` = {len(OPP)} oportunidades com subsetor B3 ≤ 40% "
             "(incorporação ≤ 40%, 100% investido); `u59` = universo de 59 com setor B3 ≤ 40%.\n")
    L.append("| Carteira | Pesos (% do capital) |\n|---|---|")
    for r in results:
        L.append(f"| {r['id']} | {wfmt(r['weights'])}{' + CDI ' + str(round(r['metrics']['cash_cdi'] * 100)) if r['metrics']['cash_cdi'] > 1e-6 else ''} |")
    L.append("")
    L.append("| Carteira | Invest. | Nomes | Vol | Beta | Beta baixa | E[exc.] TIR | Sharpe TIR | Sharpe upside | VaR95 1m normal | VaR95 1m crise | CVaR95 1m hist. | CVaR95 1m crise | N efetivo | Máx. contrib. risco |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in results:
        mm = r["metrics"]
        L.append(f"| {r['id']} | {pct(mm['invested'], 0)} | {mm['n_names']} | {pct(mm['vol'])} | {num(mm['beta'])} | {num(mm['beta_down'])} | {pct(mm['exp_excess_tir'])} | "
                 f"{num(mm['sharpe_tir'])} | {num(mm['sharpe_up'])} | {pct(mm['var95_1m_param'])} | {pct(mm['var95_1m_crisis'])} | {pct(mm['cvar95_1m_hist'])} | "
                 f"{pct(mm['cvar95_1m_crisis'])} | {num(mm['n_eff'], 1)} | {pct(mm['max_rc'], 0)} |")
    L.append("")
    L.append("Exposição setorial (setor B3, % do capital):\n")
    L.append("| Carteira | Setores |\n|---|---|")
    for r in results:
        L.append(f"| {r['id']} | " + " · ".join(f"{k} {v * 100:.0f}" for k, v in r["sectors"].items()) + " |")
    L.append("")

    # ------------------------------------------------------------ estresses
    L.append("## Estresses (choque instantâneo, % do capital)\n")
    L.append("| Carteira | Ibov −20% (beta baixa) | Ibov −20% (reação de hoje) | DI +300 bp | Dólar +20% puro | Dólar +20% c/ co-mov. | Ibov +30% (beta alta) |\n|---|---:|---:|---:|---:|---:|---:|")
    for r in results:
        s_ = r["stress"]
        L.append(f"| {r['id']} | {pct(s_['ibov_m20'])} | {pct(s_['ibov_m20_beta_hoje'])} | {pct(s_['di_p300'])} | {pct(s_['usd_p20_puro'])} | {pct(s_['usd_p20_comov'])} | {pct(s_['ibov_p30'])} |")
    L.append(f"| Ibovespa (referência) | −20,0% | −20,0% | — | — | {pct(P['ibov_usd_p20_comov'])} | +30,0% |\n")
    L.append("A coluna \"reação de hoje\" usa a razão entre a queda de cada ação e a do Ibovespa em 26/10. Como o universo foi escolhido justamente por ter caído ≥ 20%, "
             "essa razão superestima o beta. Ainda assim, ela mostra que em choques políticos os nomes domésticos se movem perto do dobro do índice.\n")

    # ------------------------------------------------------------ Monte Carlo
    L.append("## Monte Carlo de 1 ano (bootstrap estacionário, 10 mil trajetórias)\n")
    L.append("Regimes: `normal_hist` = dias de 2016–2026 com a média histórica; `normal_tir` = mesmos dias com a média de cada ação trocada pela TIR de dono; "
             "`choque_tir` = 3 meses sorteados dos dias de crise e 9 meses normais; `crise_tir` = o ano todo em dias de crise "
             f"(vol 21d do Ibovespa ≥ {pct(P['mc']['crisis_vol21_threshold'])}: {P['mc']['crisis_days']} dias, em 2016, 2017, 2018, 2020, 2021, 2022 e out/2026); "
             "`crise_hist` = dias de crise com a média que tiveram.\n")
    L.append("| Carteira | Regime | Média | p5 | p25 | p50 | p75 | p95 | P(perda) | P(< CDI) | DD mediano | P(DD > 25%) | Kelly cheio |\n|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for pid in (rec["id"], "alt_u59_halfkelly", "op7_b3_ms_tir", "op7_sub_ms_tir", "u59_ms_tir", "u59_rp", "u59_mv"):
        r = by[pid]
        for k in ("normal_hist", "normal_tir", "choque_tir", "crise_tir", "crise_hist"):
            d = r["mc"][k]
            L.append(f"| {pid} | {k} | {pct(d['mean'])} | {pct(d['p5'])} | {pct(d['p25'])} | {pct(d['p50'])} | {pct(d['p75'])} | {pct(d['p95'])} | {pct(d['p_loss'], 0)} | "
                     f"{pct(d['p_below_cdi'], 0)} | {pct(d['mdd_median'])} | {pct(d['p_dd_25'], 0)} | {num(d['kelly_full'])} |")
    L.append("")

    # ------------------------------------------------------------ backtest
    L.append("## Backtest ilustrativo: comprar no crash\n")
    L.append(f"Regra: {bt['universe_rule']}. Retornos: {bt['dividends']}. Cestas com pesos iguais, compradas no fechamento do dia do choque. "
             "\"Mais caídas\" = terço com maior queda desde a data de referência; \"mais baratas\" = terço com maior L/P (P/L do fim do mês anterior levado ao preço do choque); "
             "\"caídas e baratas\" = quintil superior da soma dos dois rankings.\n")
    for ev in evs:
        L.append(f"### {ev['date']} — {ev['label']}\n")
        L.append(f"Universo de {ev['n_universe']} ações. O Ibovespa caiu {pct(ev['ibov_drop'])} entre {ev['ref_date']} e o fechamento do choque "
                 f"({pct(ev['ibov_day'])} no dia) e depois subiu {pct(ev['ibov_fwd'].get('3m'))} em 3m, {pct(ev['ibov_fwd'].get('6m'))} em 6m e {pct(ev['ibov_fwd'].get('12m'))} em 12m.\n")
        L.append("| Cesta | N | Queda média | P/L mediano | 3m | 6m | 12m | Mediana 12m | Excesso 12m | % > Ibov 12m | DD máx. 12m |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for b in ev["baskets"]:
            L.append(f"| {b['name']} | {b['n']} | {pct(b['drop_mean'])} | {num(b['pe_median'], 1)} | {pct(b.get('ret_3m'))} | {pct(b.get('ret_6m'))} | {pct(b.get('ret_12m'))} | "
                     f"{pct(b.get('median_12m'))} | {pct(b.get('excess_12m'))} | {pct(b.get('hit_12m'), 0)} | {pct(b.get('max_dd_12m'))} |")
        ic = ev["rank_ic"]
        L.append(f"\nCorrelação de ranking (Spearman) entre a queda e o retorno seguinte: 3m {num(ic['drop_3m'])}, 6m {num(ic['drop_6m'])}, 12m {num(ic['drop_12m'])} "
                 f"(negativo = as mais caídas sobem mais). Entre o L/P e o retorno: 3m {num(ic['ey_3m'])}, 12m {num(ic['ey_12m'])}.\n")
    ep = bt["ibov_crash_episodes"]
    L.append("### Ibovespa após quedas diárias ≤ −5% (episódios com ≥ 60 dias de intervalo, desde 1998)\n")
    L.append("| Data | Queda no dia | 3m | 6m | 12m |\n|---|---:|---:|---:|---:|")
    for e in ep["episodes"]:
        L.append(f"| {e['date']} | {pct(e['ret'])} | {pct(e['f3m'])} | {pct(e['f6m'])} | {pct(e['f12m'])} |")
    L.append("| **mediana** | | " + " | ".join(f"**{pct(ep['summary'][h]['median'])}** ({pct(ep['summary'][h]['pct_pos'], 0)} > 0)" for h in HORIZONS) + " |\n")

    # ------------------------------------------------------------ por ação
    L.append("## Sensibilidades por ação\n")
    L.append("★ = oportunidade. Duration = queda do DDM com +3 p.p. na taxa ÷ 3 p.p. Lucro DI = efeito do canal de lucro sobre o preço.\n")
    L.append("| Ação | Setor | Vol | Beta | Beta baixa | Beta alta | Hoje | TIR − CDI | Upside a.a. 3a | Ibov −20% | DI +300 | Lucro DI | Duration (anos) | Beta câmbio puro | Dólar +20% puro |\n"
             "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for t in U:
        s_ = stock[t]
        L.append(f"| {t}{' ★' if s_['opportunity'] else ''} | {s_['setor']} | {pct(s_['vol'])} | {num(s_['beta'])} | {num(s_['beta_down'])} | {num(s_['beta_up'])} | {pct(s_['ret_today'])} | "
                 f"{pct(s_['mu_tir'])} | {pct(s_['mu_up'])} | {pct(s_['stress']['ibov_m20'])} | {pct(s_['stress']['di_p300'])} | {pct(s_['di_detail']['di_earn'])} | "
                 f"{num(s_['di_detail']['duration_years'], 1)} | {num((s_['fx_detail'] or {}).get('fx_beta_partial'))} | {pct(s_['stress']['usd_p20_puro'])} |")
    L.append("")

    # ------------------------------------------------------------ método
    L.append("## Método e ressalvas\n")
    L.append(f"- Covariância: {P['cov_window']}, {P['cov_obs']} observações diárias, Ledoit-Wolf com alvo de correlação constante "
             f"(intensidade {num(P['lw_shrinkage'], 3)}, correlação média {num(P['lw_rbar'], 3)}), anualizada × 252. Vol 3a do Ibovespa: {pct(P['ibov_vol_3y'])}.")
    L.append("- Otimização: SLSQP, long-only, 20% por ação e 40% por setor. Pesos iguais e inverso da volatilidade são projetados no conjunto viável. "
             "A paridade de risco minimiza o desvio das contribuições de risco em relação a 1/N, com limites. "
             "Máximo Sharpe usa várias partidas; holdings sem TIR (SIMH3, CSAN3) ficam de fora da versão TIR.")
    for n_ in P["notes"]:
        L.append(f"- {n_}")
    L.append("- A TIR de dono é a taxa implícita no preço sob as projeções do estudo (horizonte longo), não uma previsão de 12 meses. "
             "O Sharpe ex-ante herda os erros dessas projeções; por isso a recomendação mistura máximo Sharpe com paridade de risco e não usa o máximo Sharpe puro.")
    L.append("- Backtest: só 2 eventos, preços sem reinvestimento de proventos (DY aproximado; valores fora de 0–15% descartados) e P/L histórico com erros de unidade "
             "em alguns tickers (P/L fora de 1–60 descartado). Há viés de sobrevivência, porque o universo é a lista atual. É ilustrativo, não estatisticamente conclusivo.")
    L.append("- Estresses são lineares e instantâneos, sem efeitos de segunda ordem (liquidez, chamadas de margem, rebaixamentos).")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()

"""Motor de projeção e valuation (Ke 25%).

Uso:
  python pipeline/model.py TICKER [TICKER ...]   -> imprime resumo e grava data/model/{TICKER}.json
  python pipeline/model.py --all                 -> roda todos os research/*.json (holdings por último)

Lê research/{TICKER}.json (premissas) + data/hist/{TICKER}.json (CVM). Preço: API oficial B3 (ao vivo),
com fallback para data/market/quotes.json. Fórmulas: docs/model-spec.md.
"""
import json
import math
import os
import sys
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
KE = 0.25
TAX_SHIELD = 0.34
VAL_DATE = date(2026, 10, 26)
YEARS = [2026, 2027, 2028, 2029, 2030]
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
N_MC = 5000


# ------------------------------------------------------------------ utilitários
def yf(d0, d1):
    return (d1 - d0).days / 365.25


def arr(x, n=5, default=0.0):
    if x is None:
        return np.full(n, default, dtype=float)
    if isinstance(x, (int, float)):
        return np.full(n, float(x))
    a = np.array([default if v is None else v for v in x], dtype=float)
    if len(a) < n:
        a = np.concatenate([a, np.full(n - len(a), a[-1] if len(a) else default)])
    return a[:n]


def num(x, default=0.0):
    try:
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return default
        return float(x)
    except Exception:
        return default


_quote_cache = {}


# Pesos do blend por setor onde as duas baterias de teste concordam (data/tests/robustness.md e alt_methods.md):
# incorporadoras — FCFF oscila com terreno, recebíveis e juros capitalizados, então DCF ≤ 20% e o lado do acionista domina;
# bancos — valor = ROE contra Ke sobre o PL, P/L sai (redundante com o DDM e distorcido por provisões/JCP).
# Nos demais setores as baterias divergem e fica o padrão 50/25/25. Premissa com valuation_weights próprio prevalece (EZTC3).
_HOMEBUILDERS = ("CURY3", "CYRE3", "DIRR3", "EZTC3", "JHSF3", "MDNE3", "MRVE3", "PLPL3", "TEND3")
_BANKS = ("BBAS3", "BBDC4", "BBDC3", "BRSR6", "BPAC11")
SECTOR_WEIGHTS = {**{t: {"ddm": 0.5, "pe": 0.3, "dcf": 0.2} for t in _HOMEBUILDERS},
                  **{t: {"ddm": 0.6, "pbv": 0.4} for t in _BANKS}}


def live_quote(ticker):
    if ticker in _quote_cache:
        return _quote_cache[ticker]
    q = None
    if os.environ.get("EAGORA_SNAPSHOT") == "1":  # rodada final: foto de valuation (quotes_val) ou a do dia do crash
        for name in ("quotes_val.json", "quotes.json"):
            snap = ROOT / "data" / "market" / name
            if not snap.exists():
                continue
            sq = json.load(open(snap)).get(ticker)
            if sq and sq.get("price"):
                q = {"price": sq["price"], "chg_pct": sq.get("chg_pct"), "prev_close": sq.get("prev_close"), "ts": sq.get("ts"), "source": "B3 (foto do estudo)"}
                _quote_cache[ticker] = q
                return q
    try:
        with urlopen(Request(f"https://cotacao.b3.com.br/mds/api/v1/instrumentQuotation/{ticker}", headers={"User-Agent": UA}), timeout=15) as r:
            d = json.loads(r.read().decode())
        if d.get("BizSts", {}).get("cd") == "OK":
            s = d["Trad"][0]["scty"]["SctyQtn"]
            q = {"price": s["curPrc"], "chg_pct": s.get("prcFlcn"), "ts": d["Msg"]["dtTm"], "source": "B3 ao vivo"}
            if s.get("prcFlcn") is not None:
                q["prev_close"] = s["curPrc"] / (1 + s["prcFlcn"] / 100)
    except Exception:
        q = None
    if q is None:
        snap = ROOT / "data" / "market" / "quotes.json"
        if snap.exists():
            q = json.load(open(snap)).get(ticker)
    _quote_cache[ticker] = q
    return q


def shares_info(hist, prem):
    sh = hist.get("shares") or {}
    ov = (prem.get("overrides") or {}).get("base") or {}
    total = num(sh.get("outstanding")) / 1e6
    on, pn = num(sh.get("on")) / 1e6, num(sh.get("pn")) / 1e6
    if ov.get("shares_outstanding_mn"):
        f = num(ov["shares_outstanding_mn"]) / total if total else 1.0
        total, on, pn = num(ov["shares_outstanding_mn"]), on * f, pn * f
    return {"outstanding_mn": total, "on_mn": on, "pn_mn": pn,
            "per_unit": prem.get("shares_per_unit") or hist.get("shares_per_unit") or 1}


def market_cap(prem, hist, sh, price_main):
    """Market cap (R$ mi) usando as classes listadas quando houver ON/PN com preços diferentes."""
    classes = prem.get("listed_classes") or []
    main = prem["ticker"]
    if len(classes) >= 2 and sh["on_mn"] > 0 and sh["pn_mn"] > 0:
        px = {}
        for c in classes:
            q = live_quote(c["ticker"]) if c["ticker"] != main else {"price": price_main}
            if q and q.get("price"):
                px[c["class"].upper()[:2]] = q["price"]
        if "ON" in px and "PN" in px:
            return px["ON"] * sh["on_mn"] + px["PN"] * sh["pn_mn"]
    return price_main / sh["per_unit"] * sh["outstanding_mn"]


# ------------------------------------------------------------------ projeção industrial
def project_industrial(prem, hist, shifts=None):
    p = prem["projection"]
    sh = shifts or {}
    ov = (prem.get("overrides") or {}).get("base") or {}
    fy = hist["annual"]["FY2025"]
    bal = hist["balance"]
    rev0 = num(ov.get("revenue_2025"), num(fy.get("revenue")))
    g = arr(p.get("revenue_growth")) + sh.get("revenue_growth_shift", 0.0)
    m = arr(p.get("ebitda_margin")) + sh.get("ebitda_margin_shift", 0.0)
    da = arr(p.get("da_pct_revenue"))
    cx = arr(p.get("capex_pct_revenue")) + sh.get("capex_pct_shift", 0.0)
    nwc = num(p.get("nwc_pct_revenue"))
    kd = arr(p.get("cost_of_net_debt"))
    of = arr(p.get("other_financial"))
    tx = arr(p.get("tax_rate"), default=0.3)
    mino = num(p.get("minority_share_ni"))
    po = arr(p.get("payout"))
    bb = arr(p.get("buyback_mn"))
    iss = arr(p.get("equity_issuance_mn"))
    nd_base = num(ov.get("net_debt"), num(bal.get("net_debt")))
    eq_base = num(ov.get("equity_controlling"), num(bal.get("equity_controlling")))
    eq_fy = num(ov.get("equity_controlling_2025"), num(fy.get("equity_controlling"), eq_base))
    bdate = date.fromisoformat(ov.get("balance_date") or bal.get("date") or "2026-06-30")
    f26 = max(0.0, min(1.0, yf(bdate, date(2026, 12, 31))))
    n = 5
    rev = np.zeros(n); ebitda = np.zeros(n); dep = np.zeros(n); ebit = np.zeros(n); fin = np.zeros(n)
    ebt = np.zeros(n); tax = np.zeros(n); ni = np.zeros(n); nic = np.zeros(n); capex = np.zeros(n)
    dnwc = np.zeros(n); fcff = np.zeros(n); div = np.zeros(n); nd = np.zeros(n); eq = np.zeros(n)
    prev_rev, prev_nd, prev_eq = rev0, nd_base, eq_base
    for i in range(n):
        rev[i] = prev_rev * (1 + g[i])
        ebitda[i] = rev[i] * m[i]
        dep[i] = rev[i] * da[i]
        ebit[i] = ebitda[i] - dep[i]
        fin[i] = -kd[i] * prev_nd + of[i]
        ebt[i] = ebit[i] + fin[i]
        tax[i] = max(0.0, ebt[i]) * tx[i]
        ni[i] = ebt[i] - tax[i]
        nic[i] = ni[i] * (1 - mino)
        capex[i] = rev[i] * cx[i]
        dnwc[i] = nwc * (rev[i] - prev_rev)
        fcff[i] = ebit[i] * (1 - tx[i]) + dep[i] - capex[i] - dnwc[i]
        div[i] = max(0.0, nic[i]) * po[i]
        cf_pre = ebitda[i] - tax[i] + fin[i] - capex[i] - dnwc[i] - (ni[i] - nic[i]) * po[i]
        frac = f26 if i == 0 else 1.0
        nd[i] = prev_nd - frac * cf_pre + frac * (div[i] + bb[i] - iss[i])
        eq[i] = prev_eq + frac * (nic[i] - div[i] - bb[i] + iss[i])
        prev_rev, prev_nd, prev_eq = rev[i], nd[i], eq[i]
    eq_start = np.concatenate([[eq_fy], eq[:-1]])
    roe = nic / np.where((eq_start + eq) / 2 > 0, (eq_start + eq) / 2, np.nan)
    nd_start = np.concatenate([[nd_base], nd[:-1]])
    ic = (eq_start + eq) / 2 + (nd_start + nd) / 2 + num(bal.get("minority"))
    roic = ebit * (1 - tx) / np.where(ic > 0, ic, np.nan)
    return dict(rev0=rev0, revenue=rev, ebitda=ebitda, d_and_a=dep, ebit=ebit, fin_result=fin, ebt=ebt, taxes=tax,
                net_income=ni, ni_controlling=nic, capex=capex, d_nwc=dnwc, fcff=fcff, dividends=div, net_debt=nd,
                equity=eq, roe=roe, roic=roic, tax_rate=tx, payout=po, growth=g, margin=m,
                nd_base=nd_base, eq_base=eq_base, eq_fy=eq_fy, base_date=bdate, f26=f26)


def project_financial(prem, hist, shifts=None):
    fp = prem.get("financial_projection") or {}
    sh = shifts or {}
    ov = (prem.get("overrides") or {}).get("base") or {}
    fy = hist["annual"]["FY2025"]
    bal = hist["balance"]
    ni0 = num(ov.get("ni_controlling_2025"), num(fy.get("ni_controlling")))
    eq_fy = num(ov.get("equity_controlling_2025"), num(fy.get("equity_controlling")))
    eq_base = num(ov.get("equity_controlling"), num(bal.get("equity_controlling"), eq_fy))
    po = arr(fp.get("payout") or (prem.get("projection") or {}).get("payout"))
    roe_in = fp.get("roe")
    gr_in = fp.get("ni_growth")
    roe_shift = sh.get("ebitda_margin_shift", 0.0) * 1.0 + sh.get("roe_shift", 0.0)
    gshift = sh.get("revenue_growth_shift", 0.0)
    bdate = date.fromisoformat(ov.get("balance_date") or bal.get("date") or "2026-06-30")
    f26 = max(0.0, min(1.0, yf(bdate, date(2026, 12, 31))))
    n = 5
    ni = np.zeros(n); div = np.zeros(n); eq = np.zeros(n)
    prev_eq, prev_ni = eq_fy, ni0
    for i in range(n):
        if gr_in is not None and roe_in is None:
            ni[i] = prev_ni * (1 + arr(gr_in)[i] + gshift)
        else:
            ni[i] = (arr(roe_in)[i] + roe_shift) * prev_eq * (1 + gshift * 0.5)
        div[i] = max(0.0, ni[i]) * po[i]
        eq[i] = prev_eq + ni[i] - div[i]
        prev_eq, prev_ni = eq[i], ni[i]
    eq_start = np.concatenate([[eq_fy], eq[:-1]])
    roe = ni / ((eq_start + eq) / 2)
    return dict(ni0=ni0, net_income=ni, ni_controlling=ni, dividends=div, equity=eq, roe=roe, payout=po,
                eq_fy=eq_fy, eq_base=eq_base, base_date=bdate, f26=f26, growth=np.diff(np.concatenate([[ni0], ni])) / np.abs(np.concatenate([[ni0], ni[:-1]])))


# ------------------------------------------------------------------ valuation
def timings(base_date, f26):
    t_mid26 = date.fromordinal(base_date.toordinal() + int((date(2026, 12, 31) - base_date).days / 2))
    taus = [yf(VAL_DATE, t_mid26)] + [yf(VAL_DATE, date(y, 7, 1)) for y in YEARS[1:]]
    return np.array(taus), yf(VAL_DATE, date(2030, 12, 31))


def ddm_value(div, ni_last, f26, taus, tau_T, ke, g, roe_T):
    roe_T = max(roe_T, g + 0.02)
    flows = div.copy()
    flows[0] *= f26
    pv = float(np.sum(flows / (1 + ke) ** taus))
    tv = ni_last * (1 + g) * (1 - g / roe_T) / (ke - g) if ke > g else float("nan")
    return pv + tv / (1 + ke) ** tau_T, pv, tv


def dcf_value(pr, f26, taus, tau_T, wacc, g, roic_T):
    roic_T = max(roic_T, g + 0.02)
    flows = pr["fcff"].copy()
    flows[0] *= f26
    pv = float(np.sum(flows / (1 + wacc) ** taus))
    nopat = pr["ebit"][-1] * (1 - pr["tax_rate"][-1])
    tv = nopat * (1 + g) * (1 - g / roic_T) / (wacc - g) if wacc > g else float("nan")
    return pv + tv / (1 + wacc) ** tau_T, pv, tv


def irr_bisect(fn, lo, hi, target, it=80):
    """Acha r tal que fn(r) = target, com fn decrescente em r."""
    flo, fhi = fn(lo), fn(hi)
    if not (np.isfinite(flo) and np.isfinite(fhi)):
        return None
    if flo < target or fhi > target:
        return None  # sem raiz no intervalo (ex.: lucro terminal negativo): TIR não definida
    for _ in range(it):
        mid = (lo + hi) / 2
        if fn(mid) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def value_company(prem, hist, ke=KE, shifts=None, price=None, mcap=None, detail=True, mcap_now=None):
    tpl = prem.get("template", "industrial")
    term = prem.get("terminal") or {}
    g = num(term.get("g"), 0.05) + (shifts or {}).get("terminal_g_shift", 0.0)
    sh = shares_info(hist, prem)
    n_sh = sh["outstanding_mn"]
    tm = prem.get("target_multiples") or {}
    adj = prem.get("adjustments") or {}
    bal = hist["balance"]
    out = {"template": tpl}
    if tpl == "financial":
        pr = project_financial(prem, hist, shifts)
    else:
        pr = project_industrial(prem, hist, shifts)
    taus, tau_T = timings(pr["base_date"], pr["f26"])
    roe_T = num(term.get("roe"), float(np.nanmean(pr["roe"][-2:])) if np.isfinite(np.nanmean(pr["roe"][-2:])) else 0.15)
    eq_ddm, pv_div, tv_eq = ddm_value(pr["dividends"], pr["ni_controlling"][-1], pr["f26"], taus, tau_T, ke, g, roe_T)
    eps = pr["ni_controlling"] / n_sh
    dps = pr["dividends"] / n_sh
    bvps = pr["equity"] / n_sh
    vals = {}
    vals["ddm"] = eq_ddm / n_sh
    if tpl != "financial":
        w = prem.get("wacc") or {}
        kd = num(w.get("kd_pre_tax"), 0.155)
        wd = w.get("target_debt_weight")
        if wd is None:
            pre_mcap = mcap if mcap else None
            wd = max(0.0, min(0.6, pr["nd_base"] / (pr["nd_base"] + pre_mcap))) if pre_mcap and pr["nd_base"] > 0 else 0.0
        wacc = (1 - wd) * ke + wd * kd * (1 - TAX_SHIELD)
        roic_T = num(term.get("roic"), float(np.nanmean(pr["roic"][-2:])) if np.isfinite(np.nanmean(pr["roic"][-2:])) else wacc)
        ev, pv_f, tv_f = dcf_value(pr, pr["f26"], taus, tau_T, wacc, g, roic_T)
        minority_v = num(adj.get("minority_value"), num(bal.get("minority")))
        eq_dcf = ev - pr["nd_base"] - minority_v + num(adj.get("non_operating_assets")) - num(adj.get("other_debt_like"))
        vals["dcf"] = eq_dcf / n_sh
        out["dcf"] = {"wacc": wacc, "kd": kd, "wd": wd, "ev": ev, "pv_explicit": pv_f, "tv": tv_f,
                      "pv_tv": tv_f / (1 + wacc) ** tau_T, "tv_share": (tv_f / (1 + wacc) ** tau_T) / ev if ev else None,
                      "equity": eq_dcf, "minority_value": minority_v, "roic_T": roic_T,
                      "implied_exit_ev_ebitda": tv_f / pr["ebitda"][-1] if pr["ebitda"][-1] else None}
        # múltiplos
        mv = []
        if tm.get("pe") and eps[1] > 0:
            vals["pe"] = tm["pe"] * eps[1]
            mv.append(vals["pe"])
        if tm.get("ev_ebitda") and pr["ebitda"][1] > 0:
            eqm = tm["ev_ebitda"] * pr["ebitda"][1] - pr["net_debt"][0] - minority_v + num(adj.get("non_operating_assets")) - num(adj.get("other_debt_like"))
            vals["ev_ebitda"] = eqm / n_sh
            mv.append(vals["ev_ebitda"])
        vals["multiples"] = float(np.mean(mv)) if mv else None
    else:
        mv = []
        if tm.get("pe") and eps[1] > 0:
            vals["pe"] = tm["pe"] * eps[1]
            mv.append(vals["pe"])
        if tm.get("pbv"):
            vals["pbv"] = tm["pbv"] * bvps[0]
            mv.append(vals["pbv"])
        vals["multiples"] = float(np.mean(mv)) if mv else None
        out["justified_pbv"] = (roe_T - g) / (ke - g)
    # referências
    ltm = hist.get("ltm") or {}
    eps_ltm = num(ltm.get("ni_controlling"), num(hist["annual"]["FY2025"].get("ni_controlling"))) / n_sh
    ovb = (prem.get("overrides") or {}).get("base") or {}
    bv_now = num(ovb.get("equity_controlling"), num(bal.get("equity_controlling"))) / n_sh
    vals["graham"] = math.sqrt(22.5 * eps_ltm * bv_now) if eps_ltm > 0 and bv_now > 0 else None
    vals["bazin"] = dps[1] / 0.06 if dps[1] > 0 else None
    # blend
    weights = prem.get("valuation_weights") or SECTOR_WEIGHTS.get(prem.get("ticker") or hist.get("ticker")) or (
        {"ddm": 0.5, "multiples": 0.5} if tpl == "financial" else {"dcf": 0.5, "ddm": 0.25, "multiples": 0.25})
    tot, acc = 0.0, 0.0
    for k, wgt in weights.items():
        x = vals.get(k)
        if x is not None and np.isfinite(x):
            acc += wgt * max(0.0, x)
            tot += wgt
    fair = acc / tot if tot else None
    unit = sh["per_unit"]
    out.update({"fair_value_share": fair, "fair_value": fair * unit if fair is not None else None, "values_share": vals,
                "values": {k: (x * unit if x is not None else None) for k, x in vals.items()}, "weights": weights,
                "g": g, "roe_T": roe_T, "ke": ke, "proj": pr, "eps": eps, "dps": dps, "bvps": bvps, "taus": taus, "tau_T": tau_T,
                "shares": sh, "ddm": {"equity": eq_ddm, "pv_div": pv_div, "tv": tv_eq}})
    out["pe_target"] = tm.get("pe")
    # retornos ao preço de mercado
    if price:
        p_sh = price / unit
        out["upside"] = fair / p_sh - 1 if fair else None
        f26 = pr["f26"]
        def pv_eq(r):
            if r <= g + 1e-4:
                return float("inf")
            v, _, _ = ddm_value(pr["dividends"], pr["ni_controlling"][-1], f26, taus, tau_T, r, g, roe_T)
            return v / n_sh
        out["irr_implied"] = irr_bisect(pv_eq, g + 0.002, 3.0, p_sh)
        pe_exit = tm.get("pe")
        if pe_exit and eps[1] > 0 and eps[3] > 0:
            t_exit = yf(VAL_DATE, date(2028, 12, 31))
            def pv3(r):
                fl = dps[:3].copy()
                fl[0] *= f26
                return float(np.sum(fl / (1 + r) ** taus[:3]) + pe_exit * eps[3] / (1 + r) ** t_exit)
            out["irr_3y"] = irr_bisect(pv3, -0.9, 5.0, p_sh)
            out["exit_price_2028"] = pe_exit * eps[3] * unit
        out["dy"] = (dps[:3] / p_sh).tolist()
        out["pe_fwd"] = p_sh / eps[1] if eps[1] > 0 else None
        out["pe_ltm"] = p_sh / eps_ltm if eps_ltm > 0 else None
        out["pbv_now"] = p_sh / bv_now if bv_now > 0 else None
        mc_now = mcap_now or mcap
        if tpl != "financial" and mc_now:
            ev_now = mc_now + pr["nd_base"] + out["dcf"]["minority_value"]
            out["ev_now"] = ev_now
            ebitda_ltm = num(ltm.get("ebitda"))
            out["ev_ebitda_ltm"] = ev_now / ebitda_ltm if ebitda_ltm > 0 else None
            out["ev_ebitda_fwd"] = ev_now / pr["ebitda"][1] if pr["ebitda"][1] > 0 else None
    return out


def value_holding(prem, hist, models, price=None, ke=None):
    ke = KE if ke is None else ke
    so = prem.get("sotp") or {}
    sh = shares_info(hist, prem)
    term = prem.get("terminal") or {}
    g = num(term.get("g"), 0.05)
    comps, nav_fair, nav_mkt = [], 0.0, 0.0
    for c in so.get("components", []):
        stake = num(c.get("stake"), 1.0)
        tk = c.get("ticker")
        v_fair = v_mkt = None
        if c.get("method") == "fixed" or not tk:
            v_fair = v_mkt = num(c.get("value_mn"))
        else:
            q = live_quote(tk)
            if q and q.get("price"):
                mh = ROOT / "data" / "hist" / f"{tk}.json"
                n = None
                if tk in models and (models[tk].get("shares") or {}).get("outstanding_mn"):
                    msh = models[tk]["shares"]  # respeita overrides de ações do modelo da controlada
                    n = msh["outstanding_mn"] / (msh.get("per_unit") or 1)
                elif mh.exists():
                    hh = json.load(open(mh))
                    n = num((hh.get("shares") or {}).get("outstanding")) / 1e6 / (hh.get("shares_per_unit") or 1)
                if not n and c.get("shares_mn"):
                    n = num(c["shares_mn"])
                if n:
                    v_mkt = q["price"] * n
            if c.get("method") == "fair" and tk in models and models[tk].get("fair_value") is not None:
                m = models[tk]
                v_fair = m["fair_value_share"] * m["shares"]["outstanding_mn"]
            else:
                v_fair = v_mkt if v_mkt is not None else num(c.get("value_mn"))
            if v_mkt is None:
                v_mkt = num(c.get("value_mn"), v_fair or 0.0)
        comps.append({"name": c.get("name"), "ticker": tk, "stake": stake, "method": c.get("method"),
                      "value_fair_100": v_fair, "value_mkt_100": v_mkt,
                      "contrib_fair": stake * (v_fair or 0.0), "contrib_mkt": stake * (v_mkt or 0.0)})
        nav_fair += stake * (v_fair or 0.0)
        nav_mkt += stake * (v_mkt or 0.0)
    hnd = num(so.get("holding_net_debt_mn"))
    hcost = num(so.get("holding_cost_mn"))
    cap_cost = hcost / (ke - g) if ke > g else 0.0
    eq_fair = nav_fair - hnd - cap_cost
    eq_mkt = nav_mkt - hnd - cap_cost
    n_sh = sh["outstanding_mn"]
    unit = sh["per_unit"]
    out = {"template": "holding", "components": comps, "nav_fair": nav_fair, "nav_mkt": nav_mkt, "holding_net_debt": hnd,
           "holding_cost_capitalized": cap_cost, "holding_cost_mn": hcost, "equity_fair": eq_fair, "equity_mkt": eq_mkt,
           "fair_value_share": eq_fair / n_sh, "fair_value": eq_fair / n_sh * unit, "nav_mkt_share": eq_mkt / n_sh * unit,
           "shares": sh, "values": {"sotp": eq_fair / n_sh * unit, "nav_market": eq_mkt / n_sh * unit}, "weights": {"sotp": 1.0}, "ke": ke, "g": g}
    if price:
        out["upside"] = out["fair_value"] / price - 1
        out["discount_to_nav_mkt"] = 1 - price / out["nav_mkt_share"] if out["nav_mkt_share"] > 0 else None
    return out


# ------------------------------------------------------------------ análises adicionais
def scenarios(prem, hist, price, mcap):
    sc = prem.get("scenarios") or {}
    res = {}
    for name in ("bear", "bull"):
        s = sc.get(name) or {}
        r = value_company(prem, hist, shifts=s, price=price, mcap=mcap)
        res[name] = {"fair_value": r["fair_value"], "probability": num(s.get("probability"), 0.25 if name == "bear" else 0.2),
                     "narrative": s.get("narrative"), "upside": r.get("upside")}
    return res


def sensitivity(prem, hist, price, mcap):
    kes = [0.20, 0.225, 0.25, 0.275, 0.30]
    gs = [-0.02, -0.01, 0.0, 0.01, 0.02]
    grid = [[value_company(prem, hist, ke=k, shifts={"terminal_g_shift": dg}, mcap=mcap)["fair_value"] for dg in gs] for k in kes]
    gsh = [-0.04, -0.02, 0.0, 0.02, 0.04]
    msh = [-0.03, -0.015, 0.0, 0.015, 0.03]
    grid2 = [[value_company(prem, hist, shifts={"revenue_growth_shift": a, "ebitda_margin_shift": b}, mcap=mcap)["fair_value"] for b in msh] for a in gsh]
    base_g = num((prem.get("terminal") or {}).get("g"), 0.05)
    return {"ke_axis": kes, "g_axis": [base_g + d for d in gs], "ke_g": grid,
            "growth_shift_axis": gsh, "margin_shift_axis": msh, "growth_margin": grid2}


def monte_carlo(prem, hist, price, mcap, n=N_MC, seed=7):
    u = prem.get("uncertainty") or {}
    sd_g, sd_m = num(u.get("revenue_growth_sd"), 0.03), num(u.get("ebitda_margin_sd"), 0.015)
    sd_T, sd_c = num(u.get("terminal_g_sd"), 0.0075), num(u.get("capex_pct_sd"), 0.005)
    rng = np.random.default_rng(seed)
    z1 = rng.standard_normal(n)
    z2 = 0.5 * z1 + math.sqrt(1 - 0.25) * rng.standard_normal(n)
    eg, em = z1 * sd_g, z2 * sd_m
    eT = np.clip(rng.standard_normal(n) * sd_T, -0.03, 0.015)
    ec = rng.standard_normal(n) * sd_c
    out = np.empty(n)
    for i in range(n):
        r = value_company(prem, hist, shifts={"revenue_growth_shift": eg[i], "ebitda_margin_shift": em[i], "terminal_g_shift": eT[i], "capex_pct_shift": ec[i]}, mcap=mcap)
        out[i] = r["fair_value"] if r["fair_value"] is not None else np.nan
    out = out[np.isfinite(out)]
    pct = {f"p{p}": float(np.percentile(out, p)) for p in (5, 10, 25, 50, 75, 90, 95)}
    lo, hi = np.percentile(out, 1), np.percentile(out, 99)
    hist_counts, edges = np.histogram(np.clip(out, lo, hi), bins=40)
    return {"n": int(len(out)), "mean": float(out.mean()), "std": float(out.std()), **pct,
            "prob_above_price": float((out > price).mean()) if price else None,
            "hist": {"counts": hist_counts.tolist(), "edges": edges.tolist()},
            "samples": np.sort(rng.choice(out, size=min(400, len(out)), replace=False)).round(4).tolist(),
            "params": {"revenue_growth_sd": sd_g, "ebitda_margin_sd": sd_m, "terminal_g_sd": sd_T, "capex_pct_sd": sd_c, "corr_growth_margin": 0.5}}


def reverse_dcf(prem, hist, price, mcap):
    """Deslocamento constante de crescimento de receita que faz o valor justo = preço."""
    if not price:
        return None
    f = lambda s: value_company(prem, hist, shifts={"revenue_growth_shift": s}, mcap=mcap)["fair_value"] or 0.0
    lo, hi = -0.40, 0.60
    if f(lo) > price:
        return {"growth_shift": lo, "bounded": True}
    if f(hi) < price:
        return {"growth_shift": hi, "bounded": True}
    for _ in range(50):
        mid = (lo + hi) / 2
        if f(mid) < price:
            lo = mid
        else:
            hi = mid
    s = (lo + hi) / 2
    base = arr(prem.get("projection", {}).get("revenue_growth")) if prem.get("template") != "financial" else arr((prem.get("financial_projection") or {}).get("roe"))
    return {"growth_shift": s, "implied_avg_growth": float(np.mean(base + s)), "base_avg_growth": float(np.mean(base)), "bounded": False}


# ------------------------------------------------------------------ execução
def jsonable(o):
    if isinstance(o, dict):
        return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, np.ndarray):
        return [jsonable(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else round(float(o), 6)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, date):
        return o.isoformat()
    return o


def run(ticker, models, write=True, quiet=False, mc=True):
    prem = json.load(open(ROOT / "research" / f"{ticker}.json"))
    hist = json.load(open(ROOT / "data" / "hist" / f"{ticker}.json"))
    q = live_quote(ticker) or {}
    price = q.get("price")
    sh = shares_info(hist, prem)
    tpl = prem.get("template", "industrial")
    if tpl == "holding":
        res = value_holding(prem, hist, models, price=price)
        res["mcap"] = price / sh["per_unit"] * sh["outstanding_mn"] if price else None
    else:
        prev = q.get("prev_close")
        mcap_pre = market_cap(prem, hist, sh, prev) if prev else None
        mcap = market_cap(prem, hist, sh, price) if price else None
        res = value_company(prem, hist, price=price, mcap=mcap_pre or mcap, mcap_now=mcap)
        res["mcap"] = mcap
        res["mcap_pre_election"] = mcap_pre
        if price:
            res["scenarios"] = scenarios(prem, hist, price, mcap_pre or mcap)
            pb = res["scenarios"]
            p_bear, p_bull = pb["bear"]["probability"], pb["bull"]["probability"]
            res["scenarios"]["base"] = {"fair_value": res["fair_value"], "probability": 1 - p_bear - p_bull, "upside": res.get("upside")}
            fvs = [pb["bear"]["fair_value"], res["fair_value"], pb["bull"]["fair_value"]]
            ps = [p_bear, 1 - p_bear - p_bull, p_bull]
            res["scenarios"]["expected_fair_value"] = float(sum(f * p for f, p in zip(fvs, ps) if f is not None))
            res["sensitivity"] = sensitivity(prem, hist, price, mcap_pre or mcap)
            res["reverse_dcf"] = reverse_dcf(prem, hist, price, mcap_pre or mcap)
            if mc:
                res["monte_carlo"] = monte_carlo(prem, hist, price, mcap_pre or mcap)
    res["ticker"] = ticker
    res["price"] = price
    res["quote"] = q
    res["valuation_date"] = VAL_DATE.isoformat()
    models[ticker] = res
    if write:
        (ROOT / "data" / "model").mkdir(parents=True, exist_ok=True)
        json.dump(jsonable(res), open(ROOT / "data" / "model" / f"{ticker}.json", "w"), ensure_ascii=False)
    if not quiet:
        summary(ticker, res)
    return res


def fmt(x, pct=False, d=2):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{x*100:.1f}%" if pct else f"{x:,.{d}f}"


def summary(tk, r):
    print(f"\n=== {tk} [{r['template']}]  preço {fmt(r.get('price'))}  valor justo {fmt(r.get('fair_value'))}  upside {fmt(r.get('upside'), True)}")
    if r["template"] == "holding":
        for c in r["components"]:
            print(f"   {c['name'][:28]:28s} {c['stake']*100:5.1f}%  justo100 {fmt(c['value_fair_100'],d=0)}  mkt100 {fmt(c['value_mkt_100'],d=0)}")
        print(f"   NAV justo {fmt(r['nav_fair'],d=0)}  NAV mercado {fmt(r['nav_mkt'],d=0)}  DL holding {fmt(r['holding_net_debt'],d=0)}  desconto vs NAV mkt {fmt(r.get('discount_to_nav_mkt'), True)}")
        return
    v = r["values"]
    print("   métodos:", {k: fmt(x) for k, x in v.items()})
    print(f"   TIR implícita {fmt(r.get('irr_implied'), True)} | TIR 3a {fmt(r.get('irr_3y'), True)} | DY 26-28 {[fmt(x, True) for x in r.get('dy', [])]}")
    pr = r["proj"]
    print("   ROE:", [fmt(x, True) for x in pr["roe"]], " LL:", [fmt(x, d=0) for x in pr["ni_controlling"]])
    if r["template"] != "financial":
        d = r["dcf"]
        print(f"   WACC {fmt(d['wacc'], True)}  EV {fmt(d['ev'], d=0)}  TV% {fmt(d['tv_share'], True)}  EV/EBITDA saída {fmt(d['implied_exit_ev_ebitda'], d=1)}x  ROIC_T {fmt(d['roic_T'], True)}")
        print("   Receita:", [fmt(x, d=0) for x in pr["revenue"]], " EBITDA:", [fmt(x, d=0) for x in pr["ebitda"]])
        print("   DL/EBITDA:", [fmt(nd / e, d=1) if e else "—" for nd, e in zip(pr["net_debt"], pr["ebitda"])], " FCFF:", [fmt(x, d=0) for x in pr["fcff"]])
        print(f"   P/L LTM {fmt(r.get('pe_ltm'), d=1)}x  P/L 27E {fmt(r.get('pe_fwd'), d=1)}x  EV/EBITDA LTM {fmt(r.get('ev_ebitda_ltm'), d=1)}x  P/VP {fmt(r.get('pbv_now'), d=2)}x")
    else:
        print(f"   P/VP justo (Gordon) {fmt(r.get('justified_pbv'), d=2)}x  P/L 27E {fmt(r.get('pe_fwd'), d=1)}x  P/VP {fmt(r.get('pbv_now'), d=2)}x")
    if "monte_carlo" in r:
        m = r["monte_carlo"]
        print(f"   Monte Carlo: p10 {fmt(m['p10'])}  p50 {fmt(m['p50'])}  p90 {fmt(m['p90'])}  P(valor>preço) {fmt(m['prob_above_price'], True)}")
    if "scenarios" in r:
        s = r["scenarios"]
        print(f"   Cenários: bear {fmt(s['bear']['fair_value'])}  base {fmt(r['fair_value'])}  bull {fmt(s['bull']['fair_value'])}  esperado {fmt(s['expected_fair_value'])}")


def main(args):
    models = {}
    if args and args[0] == "--all":
        prems = sorted(p.stem for p in (ROOT / "research").glob("*.json") if not p.stem.startswith("_"))
        order = []
        for t in prems:
            try:
                tpl = json.load(open(ROOT / "research" / f"{t}.json")).get("template")
            except Exception as e:
                print("JSON inválido:", t, e)
                continue
            order.append((tpl == "holding", t))
        for _, t in sorted(order):
            try:
                run(t, models, quiet="--quiet" in args)
            except Exception as e:
                print("ERRO", t, repr(e))
    else:
        tks = [a for a in args if not a.startswith("--")]
        for t in tks:
            prem = json.load(open(ROOT / "research" / f"{t}.json"))
            if prem.get("template") == "holding":
                for c in (prem.get("sotp") or {}).get("components", []):
                    tk = c.get("ticker")
                    if c.get("method") == "fair" and tk and (ROOT / "research" / f"{tk}.json").exists() and tk not in models:
                        try:
                            run(tk, models, write=False, quiet=True, mc=False)
                        except Exception as e:
                            print("aviso: não consegui avaliar", tk, e)
            run(t, models, mc="--no-mc" not in args)


if __name__ == "__main__":
    main(sys.argv[1:])

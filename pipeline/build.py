"""Monta os dados do app (data/app/*) a partir de hist (CVM), market (B3), model (valuation) e research (premissas).

Uso: python pipeline/build.py
"""
import json
import math
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "data" / "app"
KE = 0.25
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def load(p):
    try:
        return json.load(open(p))
    except Exception:
        return None


def f(x):
    try:
        x = float(x)
        return x if math.isfinite(x) else None
    except Exception:
        return None


def r(x, d=4):
    x = f(x)
    return None if x is None else round(x, d)


def get_json(url):
    try:
        with urlopen(Request(url, headers={"User-Agent": UA}), timeout=20) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


# ------------------------------------------------------------------ quant
def piotroski(h):
    a = h.get("annual") or {}
    if h.get("is_financial") or "FY2025" not in a or "FY2024" not in a:
        return None
    c, p = a["FY2025"], a["FY2024"]
    def g(d, k):
        return f(d.get(k))
    sig = {}
    ta_c, ta_p = g(c, "total_assets"), g(p, "total_assets")
    ni_c, ni_p = g(c, "ni_controlling"), g(p, "ni_controlling")
    cfo_c = g(c, "cfo")
    if None in (ta_c, ta_p, ni_c, ni_p) or not ta_c or not ta_p:
        return None
    roa_c, roa_p = ni_c / ta_c, ni_p / ta_p
    sig["ROA positivo"] = roa_c > 0
    sig["FCO positivo"] = (cfo_c or 0) > 0
    sig["ROA crescente"] = roa_c > roa_p
    sig["FCO > lucro (accruals)"] = (cfo_c or 0) / ta_c > roa_c
    lev_c = (g(c, "lt_debt") or 0) / ta_c
    lev_p = (g(p, "lt_debt") or 0) / ta_p
    sig["Alavancagem LP caindo"] = lev_c <= lev_p
    cr_c = (g(c, "current_assets") or 0) / (g(c, "current_liab") or 1)
    cr_p = (g(p, "current_assets") or 0) / (g(p, "current_liab") or 1)
    sig["Liquidez corrente subindo"] = cr_c > cr_p
    sh = h.get("shares_history") or []
    s25 = [x["outstanding"] for x in sh if x["date"].startswith("2025-12")]
    s24 = [x["outstanding"] for x in sh if x["date"].startswith("2024-12")]
    sig["Sem emissão de ações"] = (s25[-1] <= s24[-1] * 1.01) if s25 and s24 else True
    gm_c = (g(c, "gross_profit") or 0) / (g(c, "revenue") or 1)
    gm_p = (g(p, "gross_profit") or 0) / (g(p, "revenue") or 1)
    sig["Margem bruta subindo"] = gm_c > gm_p
    at_c = (g(c, "revenue") or 0) / ta_c
    at_p = (g(p, "revenue") or 0) / ta_p
    sig["Giro do ativo subindo"] = at_c > at_p
    return {"score": int(sum(sig.values())), "signals": sig}


def altman(h):
    if h.get("is_financial"):
        return None
    b = h.get("balance") or {}
    ltm = h.get("ltm") or {}
    ta = f(b.get("total_assets"))
    if not ta:
        return None
    ca, cl = f(b.get("current_assets")) or 0, f(b.get("current_liab")) or 0
    re_ = f(b.get("retained")) or 0
    ebit = f(ltm.get("ebit")) or 0
    eq = f(b.get("equity")) or 0
    tl = ta - eq
    x1, x2, x3, x4 = (ca - cl) / ta, re_ / ta, ebit / ta, eq / tl if tl > 0 else 0
    z = 3.25 + 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4
    zone = "segura" if z > 5.85 else ("cinzenta" if z > 4.35 else "risco")
    return {"z": round(z, 2), "zone": zone, "x": [round(x1, 3), round(x2, 3), round(x3, 3), round(x4, 3)]}


def zscore(vals):
    a = np.array([np.nan if v is None else v for v in vals], dtype=float)
    m, s = np.nanmean(a), np.nanstd(a)
    out = (a - m) / s if s and np.isfinite(s) and s > 0 else np.zeros_like(a)
    out = np.clip(out, -3, 3)
    return [None if not np.isfinite(x) else float(x) for x in out]


# ------------------------------------------------------------------ montagem
def series_hist(h):
    a = h.get("annual") or {}
    years = sorted(a, key=lambda k: int(k[2:]))
    out = {"years": [int(y[2:]) for y in years]}
    for k in ("revenue", "ebitda", "ebit", "ni_controlling", "net_debt", "equity_controlling", "capex", "cfo", "dividends_paid",
              "gross_profit", "d_and_a", "fin_result", "total_assets", "gross_debt", "cash_total", "leases"):
        out[k] = [r(a[y].get(k), 2) for y in years]
    for k in ("ebitda_margin", "net_margin", "roe", "roic", "nd_ebitda", "payout", "gross_margin"):
        out[k] = [r((a[y].get("ratios") or {}).get(k)) for y in years]
    out["fcf"] = [r((f(a[y].get("cfo")) or 0) + (f(a[y].get("capex")) or 0), 2) if a[y].get("cfo") is not None else None for y in years]
    q = h.get("quarterly") or {}
    qk = sorted(q, key=lambda k: (int(k[:4]), int(k[-1])))[-12:]
    out["quarterly"] = {"periods": [f"{k[-1]}T{k[2:4]}" for k in qk],
                        **{k: [r(q[p].get(k), 2) for p in qk] for k in ("revenue", "ebitda", "ni_controlling")}}
    return out


def projections(m):
    pr = m.get("proj") or {}
    if not pr:
        return None
    keys = ("revenue", "ebitda", "ebit", "d_and_a", "fin_result", "taxes", "net_income", "ni_controlling", "capex", "d_nwc", "fcff",
            "dividends", "net_debt", "equity", "roe", "roic", "growth", "margin", "payout")
    out = {"years": [2026, 2027, 2028, 2029, 2030]}
    for k in keys:
        if k in pr and isinstance(pr[k], list):
            out[k] = [r(x, 4) for x in pr[k]]
    out["eps"] = [r(x, 4) for x in (m.get("eps") or [])]
    out["dps"] = [r(x, 4) for x in (m.get("dps") or [])]
    out["bvps"] = [r(x, 4) for x in (m.get("bvps") or [])]
    if out.get("net_debt") and out.get("ebitda"):
        out["nd_ebitda"] = [r(nd / e) if nd is not None and e else None for nd, e in zip(out["net_debt"], out["ebitda"])]
    return out


def engine(m):
    """Entradas compactas para o motor TS recalcular valor justo (Ke) e TIR com preço ao vivo."""
    if not m or m.get("template") == "holding":
        return {"template": "holding", "fair_value": m.get("fair_value") if m else None,
                "nav_mkt_share": m.get("nav_mkt_share") if m else None}
    pr = m.get("proj") or {}
    sh = m.get("shares") or {}
    e = {"template": m.get("template"), "ke_base": KE, "g": m.get("g"), "roe_T": m.get("roe_T"),
         "f26": pr.get("f26"), "taus": m.get("taus"), "tau_T": m.get("tau_T"),
         "div": pr.get("dividends"), "ni_last": (pr.get("ni_controlling") or [None])[-1],
         "eps": m.get("eps"), "dps": m.get("dps"), "n_sh": sh.get("outstanding_mn"), "per_unit": sh.get("per_unit"),
         "values_share": m.get("values_share"), "weights": m.get("weights"), "pe_target": None}
    if m.get("template") != "financial":
        d = m.get("dcf") or {}
        e.update({"fcff": pr.get("fcff"), "nopat_last": (pr.get("ebit") or [0])[-1] * (1 - (pr.get("tax_rate") or [0.3])[-1]),
                  "roic_T": d.get("roic_T"), "kd": d.get("kd"), "wd": d.get("wd"), "nd_base": pr.get("nd_base"),
                  "minority_value": d.get("minority_value"), "eq_bridge_extra": (d.get("equity") or 0) - ((d.get("ev") or 0) - (pr.get("nd_base") or 0) - (d.get("minority_value") or 0))})
    return e


def mc_quantiles(m):
    mc = (m or {}).get("monte_carlo") or {}
    smp = mc.get("samples")
    if not smp:
        return None
    return [round(float(x), 4) for x in np.percentile(np.array(smp, dtype=float), np.linspace(0, 100, 101))]


def main():
    APP.mkdir(parents=True, exist_ok=True)
    (APP / "companies").mkdir(exist_ok=True)
    cov = load(ROOT / "research" / "_coverage.json")["coverage"]
    mk = load(ROOT / "data" / "market" / "_market.json")
    quotes = load(ROOT / "data" / "market" / "quotes.json") or {}
    rows = []
    docs = []
    for c in cov:
        tk = c["ticker"]
        h = load(ROOT / "data" / "hist" / f"{tk}.json") or {}
        m = load(ROOT / "data" / "model" / f"{tk}.json")
        rs = load(ROOT / "research" / f"{tk}.json")
        mt = load(ROOT / "data" / "market" / f"{tk}.json") or {}
        note = (ROOT / "research" / "notes" / f"{tk}.md")
        st = mt.get("stats") or {}
        pz = piotroski(h) if h else None
        az = altman(h) if h else None
        ltm = h.get("ltm") or {}
        cov_int = None
        if not h.get("is_financial") and ltm.get("ebit") is not None and ltm.get("fin_expense"):
            cov_int = f(ltm["ebit"]) / abs(f(ltm["fin_expense"])) if f(ltm["fin_expense"]) else None
        hist5 = (h.get("annual") or {})
        roe5 = [((hist5.get(f"FY{y}") or {}).get("ratios") or {}).get("roe") for y in range(2021, 2026)]
        roe5 = [x for x in roe5 if x is not None]
        val = m or {}
        proj = projections(val) if m else None
        row = {
            "ticker": tk, "name": c["name"], "group": c["group"], "sector": (mt.get("sector") or {}),
            "template": (rs or {}).get("template") or ("financial" if h.get("is_financial") else "industrial"),
            "has_model": bool(m and m.get("fair_value") is not None), "has_research": rs is not None,
            "price_ref": val.get("price") or (quotes.get(tk) or {}).get("price"),
            "prev_close": (quotes.get(tk) or {}).get("prev_close") or c.get("prev_close_2310"),
            "chg_snapshot": (quotes.get(tk) or {}).get("chg_pct"),
            "fair_value": r(val.get("fair_value")), "upside": r(val.get("upside")),
            "irr_implied": r(val.get("irr_implied")), "irr_3y": r(val.get("irr_3y")),
            "dy": [r(x) for x in (val.get("dy") or [])],
            "roe_3y": (proj or {}).get("roe", [None] * 3)[:3] if proj else None,
            "pe_fwd": r(val.get("pe_fwd"), 2), "pe_ltm": r(val.get("pe_ltm"), 2), "pbv": r(val.get("pbv_now"), 3),
            "ev_ebitda_fwd": r(val.get("ev_ebitda_fwd"), 2), "ev_ebitda_ltm": r(val.get("ev_ebitda_ltm"), 2),
            "prob_mc": r((val.get("monte_carlo") or {}).get("prob_above_price")),
            "mc_p10": r((val.get("monte_carlo") or {}).get("p10")), "mc_p90": r((val.get("monte_carlo") or {}).get("p90")),
            "mcap": r(val.get("mcap"), 1), "adtv": r(st.get("adtv_3m_mn"), 1),
            "beta": r(st.get("beta_down_3y") or st.get("beta_2y_daily"), 3),
            "today": st.get("today"), "mom_12_1": r(st.get("mom_12_1")), "ret_12m_pre": r(st.get("ret_12m_pre")),
            "vol_1y": r(st.get("vol_1y")), "max_dd_10y": r(st.get("max_dd_10y")),
            "price_pre_rally": r(st.get("price_pre_rally")), "rally_to_2310": r(st.get("rally_to_2310")), "now_vs_pre_rally": r(st.get("now_vs_pre_rally")),
            "piotroski": pz["score"] if pz else None, "altman": az, "interest_cov": r(cov_int, 2),
            "nd_ebitda": r(((h.get("ltm") or {}).get("ratios") or {}).get("nd_ebitda"), 2),
            "roe_avg_5y": r(float(np.mean(roe5)) if roe5 else None),
            "summary": (rs or {}).get("summary"), "confidence": (rs or {}).get("confidence"),
            "spark": [x[1] for x in (mt.get("daily_3y") or [])[-260:][::5]] + ([val.get("price")] if val.get("price") else []),
            "engine": engine(m) if m else None,
            "mc_q": mc_quantiles(m),
            "per_unit": (val.get("shares") or {}).get("per_unit") or h.get("shares_per_unit") or 1,
            "listed_classes": (rs or {}).get("listed_classes"),
        }
        rows.append(row)
        doc = {"generated_at": datetime.now().isoformat(timespec="seconds"), "ke": KE, "row": row,
               "profile": {"cnpj": h.get("cnpj"), "cvm_code": h.get("cvm_code"), "sector_cvm": h.get("sector_cvm"),
                           "latest_quarter": h.get("latest_quarter_label"), "balance_date": h.get("balance_date"),
                           "shares": h.get("shares"), "fin_type": h.get("fin_type")},
               "history": series_hist(h) if h else None, "ltm": h.get("ltm"), "ltm_label": h.get("ltm_label"),
               "balance": h.get("balance"), "growth": h.get("growth"),
               "projections": proj, "valuation": {k: val.get(k) for k in (
                   "fair_value", "fair_value_share", "values", "values_share", "weights", "upside", "irr_implied", "irr_3y",
                   "exit_price_2028", "dcf", "ddm", "justified_pbv", "scenarios", "sensitivity", "reverse_dcf", "monte_carlo",
                   "pe_fwd", "pe_ltm", "pbv_now", "ev_now", "ev_ebitda_ltm", "ev_ebitda_fwd", "dy", "mcap", "mcap_pre_election",
                   "g", "roe_T", "ke", "components", "nav_fair", "nav_mkt", "holding_net_debt", "holding_cost_capitalized",
                   "nav_mkt_share", "discount_to_nav_mkt", "template")} if m else None,
               "market": {k: mt.get(k) for k in ("stats", "daily_3y", "weekly_10y", "ibov_daily_3y", "crash_events",
                                                  "multiples_history", "dps_history", "dividends_b3", "sector")},
               "quant": {"piotroski": pz, "altman": az, "interest_cov": r(cov_int, 2)},
               "research": rs, "notes_md": note.read_text() if note.exists() else None,
               "report": load(ROOT / "research" / "reports" / f"{tk}.json")}
        docs.append(doc)
    # escores quant (z-scores dentro da cobertura)
    z_val = zscore([x["irr_implied"] for x in rows])
    z_up = zscore([x["upside"] for x in rows])
    z_q = zscore([((x["roe_avg_5y"] or 0) + ((x["piotroski"] or 4.5) - 4.5) / 9) if x["roe_avg_5y"] is not None else None for x in rows])
    z_s = zscore([(-(x["nd_ebitda"] if x["nd_ebitda"] is not None else 2.5) + ((x["altman"] or {}).get("z") or 5) / 3) if x["template"] != "financial" else None for x in rows])
    z_o = zscore([-(x["today"] or {}).get("xsec_residual") if (x["today"] or {}).get("xsec_residual") is not None else None for x in rows])
    z_p = zscore([x["prob_mc"] for x in rows])
    for i, x in enumerate(rows):
        comp = {"valor": z_val[i], "upside": z_up[i], "qualidade": z_q[i], "solidez": z_s[i], "sobrerreacao": z_o[i], "probabilidade": z_p[i]}
        w = {"valor": 0.30, "upside": 0.10, "qualidade": 0.20, "solidez": 0.15, "sobrerreacao": 0.10, "probabilidade": 0.15}
        tot = sum(w[k] for k, v in comp.items() if v is not None)
        x["scores"] = comp
        x["score"] = round(sum(w[k] * v for k, v in comp.items() if v is not None) / tot, 3) if tot else None
    ranked = sorted([x for x in rows if x["score"] is not None], key=lambda x: -x["score"])
    for i, x in enumerate(ranked):
        x["rank"] = i + 1
    for doc in docs:  # row é o mesmo objeto: já contém escores e ranking
        json.dump(doc, open(APP / "companies" / f"{doc['row']['ticker']}.json", "w"), ensure_ascii=False, separators=(",", ":"))
    # oportunidades: TIR de dono >= 20%, P(valor > preço) >= 45% no Monte Carlo, fora da zona de risco do
    # Altman Z'' e confiança do analista diferente de "baixa"; ordenadas pelo escore multifator (top 8)
    def low_conf(x):
        c = (x.get("confidence") or "").lower().strip()
        return c.startswith("baixa") and not c.startswith("baixa-m") and not c.startswith("baixa a m")
    opp = [x for x in ranked if (x["irr_implied"] or -1) >= 0.20 and (x["prob_mc"] or 0) >= 0.45
           and ((x["altman"] or {}).get("zone") != "risco") and not low_conf(x)][:8]
    # relatórios são documentos datados: se existirem, a lista fica congelada nas empresas com relatório
    reported = {p.stem for p in (ROOT / "research" / "reports").glob("*.json") if not p.stem.startswith("_")}
    if reported:
        opp = [x for x in ranked if x["ticker"] in reported]
    # macro ao vivo no build (o app também atualiza em tempo real)
    def sgs(code, n=1):
        d = get_json(f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados/ultimos/{n}?formato=json")
        return d
    macro = {"selic": sgs(432), "cdi": sgs(12), "ipca12m": sgs(13522), "ptax": sgs(1)}
    sectors = {}
    for x in mk["xsec"]["points"]:
        s = (mk["sectors"].get(x["ticker"]) or {}).get("setor") or "Outros"
        sectors.setdefault(s, []).append(x["actual"])
    sector_stats = sorted([{"setor": k, "n": len(v), "median": float(np.median(v)), "mean": float(np.mean(v))} for k, v in sectors.items()], key=lambda d: d["median"])
    overview = {"generated_at": datetime.now().isoformat(timespec="seconds"), "ke": KE, "valuation_date": "2026-10-26",
                "companies": rows, "opportunities": [x["ticker"] for x in opp],
                "opportunity_rule": "TIR de dono ≥ 20%, P(valor justo > preço) ≥ 45% no Monte Carlo, fora da zona de risco do Altman Z″ e confiança do analista diferente de baixa; ordenadas pelo escore multifator. Seleção feita com os preços das 12h55 de 26/10/2026.",
                "market": {k: mk.get(k) for k in ("ibov_today", "ibov_daily_return_stats", "worst_days", "crash_forward_stats", "crash_threshold",
                                                   "elections", "drawdowns_25", "ibov_weekly", "ibov_return_hist", "indices_last", "crash_paths", "election_paths")},
                "xsec": mk["xsec"], "sectors": mk["sectors"], "sector_stats": sector_stats, "macro": macro,
                "coverage_rule": load(ROOT / "research" / "_coverage.json")["rule"]}
    json.dump(overview, open(APP / "overview.json", "w"), ensure_ascii=False, separators=(",", ":"))
    print("empresas:", len(rows), "| com modelo:", sum(1 for x in rows if x["has_model"]), "| oportunidades:", overview["opportunities"])


if __name__ == "__main__":
    main()

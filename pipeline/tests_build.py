"""Junta os resultados das baterias de teste (data/tests/*) em data/app/tests.json (página /testes) e
data/app/portfolio.json (carteira recomendada para a página /investir). Só entra o que os gráficos usam.

Uso: python pipeline/tests_build.py
"""
import json
import re
from datetime import datetime
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "data" / "tests"
APP = ROOT / "data" / "app"


def load(p):
    try:
        return json.load(open(p))
    except Exception:
        return None


def text(p):
    try:
        return Path(p).read_text()
    except Exception:
        return None


def r(x, d=4):
    return None if x is None else round(float(x), d)


def verdict(md):
    if not md:
        return None
    for line in md.splitlines():
        if re.search(r"veredito", line, re.I):
            v = re.sub(r"[#*_`>]", "", line).split(":", 1)[-1].strip()
            return v[:160] if v else None
    return None


def review(ov):
    base = load(T / "baseline_pre_review.json") or {"empresas": {}}
    now = {c["ticker"]: c for c in ov["companies"]}
    out = []
    for tk, b in sorted(base["empresas"].items()):
        md = text(ROOT / "research" / "review" / f"{tk}.md")
        a = now.get(tk, {})
        out.append({
            "ticker": tk, "verdict": verdict(md), "has_review": md is not None,
            "changed": (ROOT / "research" / "review" / f"{tk}.orig.json").exists(),
            "before": {"fair": b.get("fair_value"), "irr": b.get("irr_implied"), "upside": b.get("upside"), "rank": b.get("rank")},
            "after": {"fair": a.get("fair_value"), "irr": a.get("irr_implied"), "upside": a.get("upside"), "rank": a.get("rank")},
        })
    return out


FACTOR_SHORT = {"upside_hist": "Upside histórico (proxy)", "reversao_1m": "Sobrerreação (proxy)", "prob_proxy": "Probabilidade (proxy)",
                "size": "Tamanho", "altman": "Altman Z″"}
COMP_SHORT = {"c_painel_proxy": "Pesos antigos do painel", "c_painel_renorm": "Painel renormalizado", "c_iguais_fatores": "Iguais, 14 fatores",
              "c_iguais_blocos": "Iguais, 6 blocos", "c_icir_simples": "∝ IC-IR de 1 mês", "c_otim_fatores": "Otimizado, 14 fatores",
              "c_otim_blocos": "Otimizado, 6 blocos", "c_otim_blocos_proxies": "Otimizado, blocos + proxies",
              "c_recomendado_regra": "Regra ∝ IC-IR (recomendada)", "c_crise_blocos": "Pesos de crise"}


def factor():
    f = load(T / "factor_backtest.json")
    if not f:
        return None
    ic = []
    for k, v in f["factors"].items():
        h = v.get("horizontes") or {}
        row = {"key": k, "label": FACTOR_SHORT.get(k, v.get("label")), "grupo": v.get("grupo"), "h": {}}
        for hz in ("1m", "3m", "6m", "12m"):
            x = h.get(hz) or {}
            row["h"][hz] = {"ic": r(x.get("ic_medio")), "t": r(x.get("t_nw"), 2)}
        x12 = h.get("12m") or {}
        row["is12"] = r((x12.get("in_sample_2017_2022") or {}).get("ic_medio"))
        row["oos12"] = r((x12.get("fora_amostra_2023_2026") or {}).get("ic_medio"))
        row["crise"] = r(((h.get("3m") or {}).get("crise") or {}).get("ic_medio"))
        ic.append(row)
    comps = []
    for k, v in f["composites"].items():
        cart = v.get("carteiras") or {}
        def exc(per):
            return r(((cart.get(per) or {}).get("excesso_vs_universo_ew") or {}).get("media_anual"))
        comps.append({"key": k, "label": COMP_SHORT.get(k, v.get("descricao")), "desc": v.get("descricao"),
                      "is": exc("in_sample_2017_2022"), "oos": exc("fora_amostra_2023_2026")})
    bl = (f.get("bootstrap") or {}).get("blocos") or {}
    names = {"zb_valor": "Valor", "zb_qualidade": "Qualidade", "zb_solidez": "Solidez", "zb_momentum": "Momentum",
             "zb_baixo_risco": "Baixo risco", "zb_tamanho": "Tamanho"}
    boot = [{"key": k, "label": lab, "median": r((bl.get("mediana") or {}).get(k)), "p05": r((bl.get("p05") or {}).get(k)),
             "p95": r((bl.get("p95") or {}).get(k)), "prob_pos": r((bl.get("prob_peso_positivo") or {}).get(k))} for k, lab in names.items()]
    meta = f.get("meta") or {}
    return {"ic": ic, "composites": comps, "bootstrap": boot,
            "meta": {"meses": meta.get("meses"), "de": meta.get("primeiro_mes"), "ate": meta.get("ultimo_mes")}}


CRASH_LABELS = {"beta": "Beta de baixa", "resid": "Resíduo da queda", "r0": "Queda do dia", "value": "Valor (E/P + B/P)",
                "ep": "E/P", "bp": "B/P", "roe": "ROE", "lev": "Alavancagem", "size": "Tamanho", "liq": "Liquidez",
                "mom": "Momentum 12-1", "exporter": "Exportadora", "financial": "Financeira", "state": "Estatal",
                "consumo": "Consumo", "utility": "Utility"}


def crash():
    c = load(T / "crash_study.json")
    if not c:
        return None
    u = ((c.get("univariate") or {}).get("t0") or {}).get("6m", {}).get("ic") or {}
    regimes = (c.get("today") or {}).get("regimes") or {}
    clusters = c.get("clusters") or []
    rows = []
    for k, lab in CRASH_LABELS.items():
        pc = ((u.get(k) or {}).get("clusters") or {}).get("per_cluster") or {}
        if not pc:
            continue
        reg = {}
        for name in ("panico", "eleitoral", "politico", "todos"):
            vals = [pc[cl] for cl in regimes.get(name, []) if pc.get(cl) is not None]
            reg[name] = r(mean(vals)) if vals else None
        rows.append({"key": k, "label": lab, "per_cluster": {cl: r(pc.get(cl)) for cl in clusters}, **reg})
    rk = (c.get("today") or {}).get("ranking") or []
    ranking = [{"ticker": x["ticker"], "exp": r(x.get("exp_3m")), "lo": r(x.get("lo80_3m")), "hi": r(x.get("hi80_3m")),
                "vs_ibov": r(x.get("exp_3m_vs_ibov"))} for x in rk[:15]]
    return {"clusters": clusters, "regimes": regimes, "ic6": rows, "ranking": ranking,
            "weights": (c.get("today") or {}).get("weights_score_z")}


GRID_SHORT = {"pesos": "Pesos do blend", "ke": "Ke de 20% a 30%", "g": "Perpetuidade ±2 p.p.", "multiplos": "Múltiplos-alvo ±30%",
              "margem_cresc": "Margem e crescimento ±2 p.p.", "kd": "Custo da dívida +300 bp", "conjunta": "Todas as grades juntas",
              "mc15": "Monte Carlo, desvios ×1,5"}


def robust():
    rb = load(T / "robustness.json")
    if not rb:
        return None
    grids = []
    for k, g in (rb.get("grids") or {}).items():
        s = g.get("summary") or {}
        grids.append({"key": k, "label": GRID_SHORT.get(k, g.get("label")), "n": s.get("n"),
                      "sp_irr": r((s.get("spearman_irr") or {}).get("median"), 3), "sp_up": r((s.get("spearman_up") or {}).get("median"), 3),
                      "sp_up_min": r((s.get("spearman_up") or {}).get("min"), 3), "top7_up": r(s.get("overlap7_up_mean"), 3),
                      "top7_irr": r(s.get("overlap7_irr_mean"), 3), "kept": r((s.get("opportunities") or {}).get("kept_mean"), 2)})
    price = {c["ticker"]: c.get("price") for c in rb.get("companies") or []}
    joint = [x for x in rb.get("long") or [] if x.get("grid") == "conjunta"]
    joint = sorted(joint, key=lambda x: -(x.get("top7_irr") or 0))
    jrows = [{"ticker": x["ticker"], "price": price.get(x["ticker"]), "p5": r(x.get("fair_p5")), "p50": r(x.get("fair_p50")),
              "p95": r(x.get("fair_p95")), "top7_irr": r(x.get("top7_irr"), 3), "top7_up": r(x.get("top7_up"), 3)}
             for x in joint if (x.get("top7_irr") or 0) >= 0.05 or (x.get("top7_up") or 0) >= 0.05]
    return {"grids": grids, "joint": jrows[:16]}


METHOD_SHORT = {"dcf": "DCF (estudo)", "apv": "APV", "eva": "EVA", "ddm": "DDM (estudo)", "ddm_adj": "DDM com emissões",
                "fcfe": "FCFE", "rim": "Lucro residual (RIM)", "pe_just": "P/L justificado", "pbv_just": "P/VP justificado",
                "peers_adj": "Pares ajustados ao Ke", "multiples": "Múltiplos-alvo (estudo)", "peers": "Pares (mediana)",
                "hist": "Histórico de 5 anos", "sotp_new": "Soma das partes"}
SCHEME_LABELS = {"estudo": "Pesos do estudo", "estudo_sem_multiplos": "Sem múltiplos-alvo", "proposto": "Proposta por classe",
                 "proposto_sem_mercado": "Proposta só com intrínsecos", "igual_todos": "Peso igual em todos os métodos"}


def alt():
    a = load(T / "alt_methods.json")
    if not a:
        return None
    bias = [{"key": k, "label": METHOD_SHORT.get(k, v.get("label")), "n": v.get("n"), "median": r(v.get("median_vs_study_fair")),
             "p25": r(v.get("p25_vs_study_fair")), "p75": r(v.get("p75_vs_study_fair"))} for k, v in (a.get("bias") or {}).items()]
    schemes = [{"key": k, "label": SCHEME_LABELS.get(k, k), "median_upside": r(v.get("median_upside")),
                "n_pos": v.get("n_upside_positive"), "opps": v.get("opportunities_by_rule")} for k, v in (a.get("rankings") or {}).items()]
    return {"bias": bias, "schemes": schemes}


STRESS_LABELS = {"ibov_m20": "Ibovespa −20% (beta de baixa)", "ibov_m20_beta_hoje": "Ibovespa −20% (reação de hoje)",
                 "ibov_p30": "Ibovespa +30%", "di_p300": "DI +300 bp", "usd_p20_puro": "Dólar +20%, canal cambial",
                 "usd_p20_comov": "Dólar +20%, com a bolsa"}


def portfolio():
    p = load(T / "portfolio.json")
    if not p:
        return None
    rec = p.get("recommended") or {}
    m = rec.get("metrics") or {}
    return {"generated_at": p.get("generated_at"), "label": rec.get("label"),
            "weights": [{"ticker": w["ticker"], "w": r(w.get("w")), "irr": r(w.get("irr")), "rc": r(w.get("rc"))} for w in rec.get("weights") or []],
            "sleeve": [{"ticker": w["ticker"], "w": r(w.get("w"))} for w in rec.get("weights_equity_sleeve") or []],
            "metrics": {k: r(m.get(k)) for k in ("invested", "cash_cdi", "vol", "beta", "beta_down", "exp_total_tir", "exp_excess_tir",
                                                 "sharpe_tir", "var95_1m_param")},
            "sizing": rec.get("sizing"),
            "stress": [{"key": k, "label": STRESS_LABELS.get(k, k), "value": r(v)} for k, v in (rec.get("stress") or {}).items()],
            "cdi": r((p.get("params") or {}).get("cdi"))}


def consensus(ov):
    now = {c["ticker"]: c for c in ov["companies"]}
    out = []
    for g in (1, 2, 3):
        d = load(T / "consensus" / f"grupo{g}.json")
        for e in (d or {}).get("empresas") or []:
            tk = e.get("ticker")
            c = now.get(tk) or {}
            cons = e.get("consenso_mediano")
            fair = c.get("fair_value")
            if tk and cons:
                out.append({"ticker": tk, "price": c.get("price_ref"), "fair": r(fair), "consensus": r(cons),
                            "n": e.get("n_analistas"), "gap": r(fair / cons - 1) if fair and cons else None})
    return sorted(out, key=lambda x: (x["gap"] is None, x["gap"] or 0))


def suite():
    s = load(T / "test_results.json")
    if not s:
        return None
    return {"generated_at": s.get("generated_at"), "totals": s.get("totals"), "blocks": s.get("blocks"), "next_build": s.get("next_build")}


def main():
    ov = load(APP / "overview.json") or {"companies": []}
    port = portfolio()
    out = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "baseline_opportunities": (load(T / "baseline_pre_review.json") or {}).get("opportunities"),
        "opportunities": ov.get("opportunities"), "dropped": ov.get("opportunities_dropped"),
        "review": review(ov), "factor": factor(), "crash": crash(), "robust": robust(), "alt": alt(), "portfolio": port,
        "consensus": consensus(ov), "suite": suite(),
        "md": {k: text(T / f"{k}.md") for k in ("factor_backtest", "crash_study", "robustness", "portfolio", "alt_methods", "test_report")},
        "consensus_md": [x for x in (text(T / "consensus" / f"grupo{i}.md") for i in (1, 2, 3)) if x],
    }
    json.dump(out, open(APP / "tests.json", "w"), ensure_ascii=False, separators=(",", ":"), default=str)
    if port:
        json.dump(port, open(APP / "portfolio.json", "w"), ensure_ascii=False, separators=(",", ":"), default=str)
    size = (APP / "tests.json").stat().st_size / 1024
    print(f"tests.json {size:.0f} KB | revisões {sum(1 for x in out['review'] if x['has_review'])} | alteradas {sum(1 for x in out['review'] if x['changed'])}",
          "| baterias:", [k for k in ("factor", "crash", "robust", "alt", "portfolio", "suite") if out[k]], "| consenso:", len(out["consensus"]))


if __name__ == "__main__":
    main()

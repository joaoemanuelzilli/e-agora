#!/usr/bin/env python3
"""Checagens da regra de decisão (revisão de 17/11/2026). Lê a foto atual (data/app/overview.json) e o motor do estudo.

  1. Elegibilidade: lista de acompanhamento × elegíveis para compra à meta (TIR de dono >= Ke e preço <= preço-teto).
  2. Sensibilidade da regra aos cortes: TIR mínima × chance mínima no Monte Carlo × tamanho da lista.
  3. Efeito do preço: TIR de dono com as MESMAS projeções ao preço de antes (fechamento de 23/10) e de depois (foto de
     28/10). Mede só o efeito mecânico do preço; não separa mudança dos negócios.
  4. Sensibilidades-chave das selecionadas: margem EBITDA −2 p.p., crescimento −2 p.p., e IR de 17% na Vitru.
  5. Ponte da data de avaliação: convenção antiga (stub inteiro descontado em 26/10, com prazo negativo) × atual
     (balanço levado a 28/10 pela ponte de caixa; só fluxos posteriores entram no DCF, no DDM e na TIR).

Uso:    .venv/bin/python pipeline/tests/decision_checks.py
Saídas: data/tests/decision_checks.json e data/tests/decision_checks.md (nada fora de data/tests/ é gravado).
"""
import copy
import json
import os
import statistics as st
import sys
import warnings
from datetime import date, datetime
from pathlib import Path

import numpy as np

os.environ["EAGORA_SNAPSHOT"] = "1"
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
import model as M  # noqa: E402

warnings.filterwarnings("ignore")
OUT = ROOT / "data" / "tests"
KE = M.KE


def pc(x, d=1):
    return "n/d" if x is None else f"{x * 100:.{d}f}%".replace(".", ",")


def brl(x, d=2):
    return "n/d" if x is None else f"R$ {x:.{d}f}".replace(".", ",")


def low_conf(c):
    c = (c or "").lower().strip()
    return c.startswith("baixa") and not c.startswith("baixa-m") and not c.startswith("baixa a m")


def load(t):
    return json.load(open(ROOT / "research" / f"{t}.json")), json.load(open(ROOT / "data" / "hist" / f"{t}.json"))


def value(t, row, price=None, prem=None, shifts=None):
    p0, hist = load(t)
    prem = prem or p0
    sh = M.shares_info(hist, prem)
    px = price if price is not None else row["price_ref"]
    mcap_pre = M.market_cap(prem, hist, sh, row["prev_close"]) if row.get("prev_close") else None
    mcap_now = M.market_cap(prem, hist, sh, px)
    return M.value_company(prem, hist, shifts=shifts, price=px, mcap=mcap_pre or mcap_now, mcap_now=mcap_now, detail=False)


class legacy_timing:
    """Convenção anterior à revisão: avaliação em 26/10, stub inteiro (balanço-base → 31/12) descontado no meio do stub."""

    def __enter__(self):
        self.keep = (M.VAL_DATE, M.stub_elapsed, M.timings)
        M.VAL_DATE = date(2026, 10, 26)
        M.stub_elapsed = lambda bdate: 0.0

        def timings(base_date, f26):
            mid = date.fromordinal(base_date.toordinal() + int((date(2026, 12, 31) - base_date).days / 2))
            taus = [M.yf(M.VAL_DATE, mid)] + [M.yf(M.VAL_DATE, date(y, 7, 1)) for y in M.YEARS[1:]]
            return np.array(taus), M.yf(M.VAL_DATE, date(2030, 12, 31))
        M.timings = timings

    def __exit__(self, *a):
        M.VAL_DATE, M.stub_elapsed, M.timings = self.keep


def main():
    ov = json.load(open(ROOT / "data" / "app" / "overview.json"))
    rows = {c["ticker"]: c for c in ov["companies"]}
    opp = ov["opportunities"]
    ranked = sorted([c for c in rows.values() if c.get("score") is not None], key=lambda c: -c["score"])
    out = {"generated_at": datetime.now().isoformat(timespec="seconds"), "ke": KE, "valuation_date": M.VAL_DATE.isoformat()}

    # 1) elegibilidade
    elig = []
    for t in opp:
        c = rows[t]
        ok = (c["irr_implied"] or -1) >= KE and c.get("ceiling") is not None and c["price_ref"] <= c["ceiling"]
        elig.append({"ticker": t, "price": c["price_ref"], "ceiling": c.get("ceiling"), "irr": c["irr_implied"], "prob_mc": c["prob_mc"],
                     "fair_value": c["fair_value"], "ddm": None, "eligible": bool(ok),
                     "margin_to_ceiling": (c["ceiling"] / c["price_ref"] - 1) if c.get("ceiling") else None})
    ge_ke = sorted([(t, c["irr_implied"]) for t, c in rows.items() if (c["irr_implied"] or -1) >= KE], key=lambda x: -x[1])
    out["eligibility"] = {"watchlist": opp, "eligible": [e["ticker"] for e in elig if e["eligible"]], "rows": elig,
                          "irr_ge_ke_universe": [{"ticker": t, "irr": i, "in_watchlist": t in opp,
                                                  "reason_out": None if t in opp else ("confiança baixa" if low_conf(rows[t].get("confidence")) else "fora pelos demais filtros ou pelo escore")}
                                                 for t, i in ge_ke]}

    # 2) sensibilidade da regra
    def select(irr_min, prob_min, n):
        ok = [c["ticker"] for c in ranked if (c["irr_implied"] or -1) >= irr_min and (c["prob_mc"] or 0) >= prob_min
              and (c.get("altman") or {}).get("zone") != "risco" and not low_conf(c.get("confidence"))]
        return ok, (ok if n is None else ok[:n])
    grid = []
    for irr_min in (0.18, 0.20, 0.22, 0.25):
        for prob_min in (0.35, 0.45, 0.55, 0.65):
            passed, _ = select(irr_min, prob_min, None)
            grid.append({"irr_min": irr_min, "prob_min": prob_min, "n_pass": len(passed), "tickers": passed,
                         "kept_of_watchlist": len(set(passed) & set(opp))})
    sizes = {str(n): select(0.20, 0.45, n)[1] for n in (5, 6, 8)}
    out["rule_sensitivity"] = {"grid": grid, "by_list_size_at_base_cuts": sizes, "base": {"irr_min": 0.20, "prob_min": 0.45, "n": 8}}

    # 3) efeito do preço (mesmas projeções)
    pre, post = {}, {}
    for t, c in rows.items():
        if c["template"] == "holding" or c["irr_implied"] is None or not c.get("prev_close"):
            continue
        pre[t] = value(t, c, price=c["prev_close"]).get("irr_implied")
        post[t] = c["irr_implied"]
    pv = [x for x in pre.values() if x is not None]
    qv = [post[t] for t in pre if pre[t] is not None]
    chg = [c["price_ref"] / c["prev_close"] - 1 for c in rows.values() if c.get("prev_close") and c.get("price_ref")]
    out["price_effect"] = {"n": len(pv), "median_price_change": st.median(chg), "irr_median_pre": st.median(pv), "irr_median_post": st.median(qv),
                           "n_ge_25_pre": sum(x >= 0.25 for x in pv), "n_ge_25_post": sum(x >= 0.25 for x in qv),
                           "n_ge_20_pre": sum(x >= 0.20 for x in pv), "n_ge_20_post": sum(x >= 0.20 for x in qv),
                           "watchlist": {t: {"pre": pre.get(t), "post": post.get(t)} for t in opp},
                           "note": "Mesmas projeções, trocando só o preço (fechamento de 23/10 × foto de 28/10). Efeito mecânico do preço, não decomposição causal."}

    # 4) sensibilidades-chave
    sens = []
    for t in opp:
        c = rows[t]
        base = value(t, c)
        m2 = value(t, c, shifts={"ebitda_margin_shift": -0.02})
        g2 = value(t, c, shifts={"revenue_growth_shift": -0.02})
        sens.append({"ticker": t, "price": c["price_ref"], "irr_base": base.get("irr_implied"), "fv_base": base.get("fair_value"),
                     "irr_margin_m2pp": m2.get("irr_implied"), "fv_margin_m2pp": m2.get("fair_value"),
                     "irr_growth_m2pp": g2.get("irr_implied"), "fv_growth_m2pp": g2.get("fair_value"),
                     "margin_base_2027": float(base["proj"]["margin"][1]) if "margin" in base["proj"] else None})
    out["key_sensitivities"] = {"rows": sens}
    if "VTRU3" in rows:
        prem, _ = load("VTRU3")
        p17 = copy.deepcopy(prem)
        p17["projection"]["tax_rate"] = [0.17] * 5
        b, v = value("VTRU3", rows["VTRU3"]), value("VTRU3", rows["VTRU3"], prem=p17)
        out["key_sensitivities"]["vtru_tax_17"] = {"tax_base": prem["projection"]["tax_rate"], "payout_base": prem["projection"].get("payout"),
                                                    "fv_base": b["fair_value"], "fv": v["fair_value"], "irr_base": b["irr_implied"], "irr": v["irr_implied"]}

    # 5) ponte da data de avaliação
    new = {t: value(t, c) for t, c in rows.items() if c["template"] != "holding"}
    with legacy_timing():
        old = {t: value(t, c) for t, c in rows.items() if c["template"] != "holding"}
    dfv = [new[t]["fair_value"] / old[t]["fair_value"] - 1 for t in new if old[t].get("fair_value") and new[t].get("fair_value")]
    dirr = [new[t]["irr_implied"] - old[t]["irr_implied"] for t in new if old[t].get("irr_implied") is not None and new[t].get("irr_implied") is not None]
    oi = [x["irr_implied"] for x in old.values() if x.get("irr_implied") is not None]
    ni = [x["irr_implied"] for x in new.values() if x.get("irr_implied") is not None]
    out["valuation_date_bridge"] = {
        "n": len(dfv), "fair_value_change_median": st.median(dfv), "fair_value_change_min": min(dfv), "fair_value_change_max": max(dfv),
        "irr_change_median": st.median(dirr), "irr_change_min": min(dirr), "irr_median_old": st.median(oi), "irr_median_new": st.median(ni),
        "n_ge_25_old": sum(x >= 0.25 for x in oi), "n_ge_25_new": sum(x >= 0.25 for x in ni),
        "n_ge_20_old": sum(x >= 0.20 for x in oi), "n_ge_20_new": sum(x >= 0.20 for x in ni),
        "watchlist": {t: {"fv_old": old[t]["fair_value"], "fv_new": new[t]["fair_value"], "irr_old": old[t]["irr_implied"], "irr_new": new[t]["irr_implied"],
                          "first_tau_old": float(old[t]["taus"][0]), "first_tau_new": float(new[t]["taus"][0])} for t in opp},
        "note": "Antiga: avaliação em 26/10 e stub de 2026 inteiro descontado no meio do stub (prazo negativo de −0,07 ano para balanço de 30/06). "
                "Atual: avaliação em 28/10; a parte do stub já decorrida vira ponte de dívida líquida e patrimônio (caixa gerado menos proventos pagos), "
                "e só os fluxos posteriores entram no DCF, no DDM e na TIR. Hipótese: fluxos uniformes dentro do stub."}

    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(OUT / "decision_checks.json", "w"), ensure_ascii=False, indent=1, default=float)

    L = []
    A = L.append
    A("# Checagens da regra de decisão")
    A("")
    A(f"Gerado em {out['generated_at'][:10]} sobre a foto de preços de 28/10/2026 (Ke = {pc(KE, 0)}). Script: `pipeline/tests/decision_checks.py`.")
    A("")
    A("## 1. Lista de acompanhamento e elegíveis para compra")
    A("")
    A("A regra original (TIR ≥ 20%, chance ≥ 45%, Altman fora de risco, confiança diferente de baixa; 8 primeiras pelo escore) define a **lista de "
      "acompanhamento**. É **elegível para compra à meta** quem, dentro dela, tem TIR de dono ≥ Ke e preço ≤ preço-teto (o menor entre o DDM a Ke e o valor justo).")
    A("")
    A("| Ação | Preço | Preço-teto | Folga até o teto | TIR de dono | Chance MC | Situação |")
    A("|---|---:|---:|---:|---:|---:|---|")
    for e in elig:
        A(f"| {e['ticker']} | {brl(e['price'])} | {brl(e['ceiling'])} | {pc(e['margin_to_ceiling'])} | {pc(e['irr'])} | {pc(e['prob_mc'], 0)} | "
          f"{'elegível à meta' if e['eligible'] else 'acompanhamento (acima do teto)'} |")
    A("")
    A(f"No universo, {len(ge_ke)} empresas têm TIR ≥ {pc(KE, 0)}: " + ", ".join(f"{t} ({pc(i)})" for t, i in ge_ke) + ". "
      + "; ".join(f"{x['ticker']} fica fora da lista por {x['reason_out']}" for x in out["eligibility"]["irr_ge_ke_universe"] if not x["in_watchlist"]) + ".")
    A("")
    A("## 2. Sensibilidade da regra aos cortes")
    A("")
    A("Quantas empresas passam nos quatro filtros para cada par de cortes (Altman e confiança mantidos; sem limite de tamanho). Entre parênteses, quantas das 8 da lista atual continuam.")
    A("")
    A("| TIR mínima | Chance ≥ 35% | Chance ≥ 45% | Chance ≥ 55% | Chance ≥ 65% |")
    A("|---|---:|---:|---:|---:|")
    for irr_min in (0.18, 0.20, 0.22, 0.25):
        cells = [next(g for g in grid if g["irr_min"] == irr_min and g["prob_min"] == p) for p in (0.35, 0.45, 0.55, 0.65)]
        A(f"| {pc(irr_min, 0)} | " + " | ".join(f"{g['n_pass']} ({g['kept_of_watchlist']})" for g in cells) + " |")
    A("")
    A("Com os cortes-base (20% e 45%), o tamanho da lista decide quem entra: " + "; ".join(f"{n} nomes: {', '.join(v)}" for n, v in sizes.items()) + ".")
    A("")
    pe = out["price_effect"]
    A("## 3. Efeito do preço na TIR (mesmas projeções)")
    A("")
    A(f"Queda mediana de preço na cobertura entre o fechamento de 23/10 e a foto de 28/10: {pc(pe['median_price_change'])}. "
      f"TIR de dono mediana ({pe['n']} empresas): {pc(pe['irr_median_pre'])} → {pc(pe['irr_median_post'])}. "
      f"Empresas com TIR ≥ 25%: {pe['n_ge_25_pre']} → {pe['n_ge_25_post']}; com TIR ≥ 20%: {pe['n_ge_20_pre']} → {pe['n_ge_20_post']}.")
    A("")
    A("| Ação | TIR ao preço de 23/10 | TIR ao preço de 28/10 |")
    A("|---|---:|---:|")
    for t in opp:
        A(f"| {t} | {pc(pe['watchlist'][t]['pre'])} | {pc(pe['watchlist'][t]['post'])} |")
    A("")
    A("É o efeito mecânico do preço com projeções fixas. Não mede quanto os negócios mudaram com juros, câmbio, demanda ou regulação.")
    A("")
    A("## 4. Sensibilidades-chave das selecionadas")
    A("")
    A("Choques aplicados aos cinco anos de projeção, um de cada vez, com o preço da foto. São sensibilidades condicionais, não previsões.")
    A("")
    A("| Ação | TIR base | Margem EBITDA −2 p.p. | Crescimento −2 p.p. | Valor justo base | VJ com margem −2 p.p. |")
    A("|---|---:|---:|---:|---:|---:|")
    for s_ in sens:
        A(f"| {s_['ticker']} | {pc(s_['irr_base'])} | {pc(s_['irr_margin_m2pp'])} | {pc(s_['irr_growth_m2pp'])} | {brl(s_['fv_base'])} | {brl(s_['fv_margin_m2pp'])} |")
    A("")
    v17 = out["key_sensitivities"].get("vtru_tax_17")
    if v17:
        A(f"**Vitru com IR de 17% nos cinco anos** (base: {', '.join(pc(x, 0) for x in v17['tax_base'])}; payout de "
          f"{', '.join(pc(x, 0) for x in (v17['payout_base'] or []))}): valor justo {brl(v17['fv_base'])} → {brl(v17['fv'])}; "
          f"TIR {pc(v17['irr_base'])} → {pc(v17['irr'])}. A classificação acima de 25% depende do benefício fiscal projetado.")
        A("")
    vb = out["valuation_date_bridge"]
    A("## 5. Ponte da data de avaliação")
    A("")
    A(vb["note"])
    A("")
    pp = lambda x: f"{x * 100:+.2f}".replace(".", ",") + " p.p."
    A(f"Efeito nas {vb['n']} empresas com modelo próprio: valor justo {pc(vb['fair_value_change_median'])} na mediana (de {pc(vb['fair_value_change_min'])} a "
      f"{pc(vb['fair_value_change_max'])}); TIR de dono {pp(vb['irr_change_median'])} na mediana (mínimo {pp(vb['irr_change_min'])}). "
      f"TIR mediana {pc(vb['irr_median_old'])} → {pc(vb['irr_median_new'])}; empresas com TIR ≥ 25%: {vb['n_ge_25_old']} → {vb['n_ge_25_new']}; ≥ 20%: {vb['n_ge_20_old']} → {vb['n_ge_20_new']}.")
    A("")
    A("| Ação | Valor justo antigo → atual | TIR antiga → atual | 1º prazo de desconto antigo → atual (anos) |")
    A("|---|---:|---:|---:|")
    for t in opp:
        w = vb["watchlist"][t]
        A(f"| {t} | {brl(w['fv_old'])} → {brl(w['fv_new'])} | {pc(w['irr_old'], 2)} → {pc(w['irr_new'], 2)} | {f"{w['first_tau_old']:+.3f} → {w['first_tau_new']:+.3f}".replace(".", ",")} |")
    A("")
    (OUT / "decision_checks.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("gravado:", OUT / "decision_checks.json", OUT / "decision_checks.md")
    print("elegíveis:", out["eligibility"]["eligible"], "| TIR mediana pré/pós:", round(pe["irr_median_pre"], 4), round(pe["irr_median_post"], 4),
          "| ≥25%:", pe["n_ge_25_pre"], "→", pe["n_ge_25_post"])


if __name__ == "__main__":
    main()

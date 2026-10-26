"""(4) Saídas do modelo (data/model/*.json) e dos dados do app (data/app/*.json)."""
import json
import math

import pytest

import pyref
from conftest import APP, MODEL, RESEARCH, fails, load, overview

OV = overview()
ROWS = {c["ticker"]: c for c in OV["companies"]}
TICKERS = list(ROWS)
NON_HOLDING = [t for t in TICKERS if ROWS[t]["template"] != "holding"]
INDUSTRIAL = [t for t in TICKERS if ROWS[t]["template"] == "industrial"]
IRR_RANGE = (-0.50, 3.00)
PROJ_KEYS = ("revenue", "ebitda", "ni_controlling", "dividends", "net_debt", "equity", "eps", "dps")


def Mo(t):
    return load(MODEL / f"{t}.json")


def finite(x):
    return isinstance(x, (int, float)) and math.isfinite(x)


def rel_close(a, b, rel=0.005, abs_=5e-5):
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) <= rel * abs(b) + abs_


@pytest.mark.parametrize("t", TICKERS)
def test_valor_justo_finito_e_positivo(t):
    m, c = Mo(t), ROWS[t]
    assert finite(m.get("fair_value")) and m["fair_value"] > 0, f"data/model fair_value = {m.get('fair_value')}"
    assert finite(c.get("fair_value")) and c["fair_value"] > 0 and c["has_model"], f"overview fair_value = {c.get('fair_value')}"
    for k, v in (m.get("values") or {}).items():
        assert v is None or finite(v), f"método {k} = {v}"


@pytest.mark.parametrize("t", TICKERS)
def test_pesos_somam_1(t):
    w = Mo(t).get("weights") or {}
    assert w and all(x >= 0 for x in w.values()), f"pesos {w}"
    assert abs(sum(w.values()) - 1) < 1e-6, f"pesos {w} somam {sum(w.values()):.6f}"
    vals = Mo(t).get("values_share") or Mo(t).get("values") or {}
    usable = [k for k in w if finite(vals.get(k))]
    assert usable, f"nenhum método com peso tem valor: pesos {w}, valores {vals}"


@pytest.mark.parametrize("t", NON_HOLDING)
def test_tir_no_intervalo(t):
    m, c = Mo(t), ROWS[t]
    bad = []
    for src, d in (("data/model", m), ("overview", c)):
        for k in ("irr_implied", "irr_3y"):
            x = d.get(k)
            if x is not None and not (IRR_RANGE[0] <= x <= IRR_RANGE[1]):
                bad.append(f"{src} {k} = {x:.4f} fora de [−50%, 300%]")
    if m.get("irr_implied") is None:
        ddm = (m.get("values_share") or {}).get("ddm")
        if ddm is None or ddm > 0:  # sem raiz só é aceitável com DDM ≤ 0 (lucro terminal negativo)
            bad.append("TIR implícita ausente")
    assert not bad, fails(bad)


@pytest.mark.parametrize("t", NON_HOLDING)
def test_tir_nao_fica_presa_no_limite_da_bissecao(t):
    """A bisseção devolve o limite do intervalo quando não há raiz: o número exibido não é uma TIR."""
    m = Mo(t)
    g = m.get("g")
    bad = []
    r = m.get("irr_implied")
    if r is not None and (abs(r - (g + 0.002)) < 1e-6 or abs(r - 3.0) < 1e-6):
        ddm = (m.get("values_share") or {}).get("ddm")
        bad.append(f"irr_implied = {r:.4f} = limite (g + 0,2 p.p. = {g + 0.002:.4f} ou 300%); DDM/ação {ddm}, "
                   f"LL 2030E {(m.get('proj') or {}).get('ni_controlling', [None])[-1]}")
    r3 = m.get("irr_3y")
    if r3 is not None and (abs(r3 + 0.9) < 1e-6 or abs(r3 - 5.0) < 1e-6):
        bad.append(f"irr_3y = {r3:.4f} = limite (−90% ou 500%)")
    assert not bad, fails(bad)


@pytest.mark.parametrize("t", NON_HOLDING)
def test_projecoes_com_5_anos(t):
    d = load(APP / "companies" / f"{t}.json")
    pr = d.get("projections") or {}
    assert pr.get("years") == [2026, 2027, 2028, 2029, 2030], f"anos {pr.get('years')}"
    keys = PROJ_KEYS if ROWS[t]["template"] == "industrial" else ("ni_controlling", "dividends", "equity", "eps", "dps", "roe")
    bad = [f"{k}: {len(pr.get(k) or [])} posições" for k in keys if len(pr.get(k) or []) != 5]
    bad += [f"{k}: valores não finitos" for k in keys if any(not finite(x) for x in pr.get(k) or [])]
    mp = Mo(t).get("proj") or {}
    bad += [f"data/model proj.{k}: {len(mp.get(k) or [])} posições" for k in ("ni_controlling", "dividends", "equity") if len(mp.get(k) or []) != 5]
    assert not bad, fails(bad)


@pytest.mark.parametrize("t", NON_HOLDING)
def test_monte_carlo_quantis_ordenados(t):
    mc = Mo(t).get("monte_carlo") or {}
    assert mc, "sem Monte Carlo"
    q = [mc.get(k) for k in ("p5", "p10", "p25", "p50", "p75", "p90", "p95")]
    assert all(finite(x) for x in q), f"quantis {q}"
    assert all(a <= b for a, b in zip(q, q[1:])), f"p5..p95 fora de ordem: {q}"
    assert mc.get("n", 0) >= 4500, f"só {mc.get('n')} simulações válidas de 5.000"
    p = mc.get("prob_above_price")
    assert p is None or 0 <= p <= 1, f"P(valor > preço) = {p}"
    mq = ROWS[t].get("mc_q") or []
    assert len(mq) == 101 and all(a <= b for a, b in zip(mq, mq[1:])), "mc_q (101 quantis do painel) ausente ou fora de ordem"
    fv = Mo(t)["fair_value"]
    assert mc["p5"] <= fv <= mc["p95"], f"valor justo base {fv:.4f} fora de [p5 {mc['p5']:.4f}, p95 {mc['p95']:.4f}]"


def leverage_justified(t):
    prem = load(RESEARCH / f"{t}.json")
    txt = json.dumps([prem.get("debt_profile"), (prem.get("overrides") or {}).get("notes")], ensure_ascii=False).lower()
    return "dl/ebitda" in txt and ("10x" in txt or "10 x" in txt)


@pytest.mark.parametrize("t", INDUSTRIAL)
def test_dl_ebitda_projetada_abaixo_de_10x(t):
    """DL/EBITDA projetada < 10x (e EBITDA > 0 com DL > 0), salvo justificativa em research/{T}.json."""
    pr = load(APP / "companies" / f"{t}.json").get("projections") or {}
    bad = []
    for y, e, n in zip(pr.get("years") or [], pr.get("ebitda") or [], pr.get("net_debt") or []):
        if e is None or n is None:
            continue
        if e <= 0 and n > 0:
            bad.append(f"{y}E: EBITDA {e:,.0f} ≤ 0 com DL {n:,.0f}")
        elif e > 0 and n / e >= 10:
            bad.append(f"{y}E: DL/EBITDA {n / e:.1f}x")
    if bad and leverage_justified(t):
        pytest.xfail("alavancagem justificada em research/" + t + ".json: " + "; ".join(bad))
    assert not bad, fails(bad)


@pytest.mark.parametrize("t", NON_HOLDING)
def test_cenarios_coerentes(t):
    sc = Mo(t).get("scenarios") or {}
    assert sc, "sem cenários"
    ps = [sc[k]["probability"] for k in ("bear", "base", "bull")]
    fv = [sc[k]["fair_value"] for k in ("bear", "base", "bull")]
    assert all(0 <= p <= 1 for p in ps) and abs(sum(ps) - 1) < 1e-6, f"probabilidades bear/base/bull {ps}"
    assert fv[0] <= fv[1] + 1e-9 and fv[1] <= fv[2] + 1e-9, f"valor justo bear {fv[0]} / base {fv[1]} / bull {fv[2]}"
    exp = sum(p * f for p, f in zip(ps, fv))
    assert abs(sc["expected_fair_value"] - exp) < 1e-3 * max(1, abs(exp)), f"valor esperado {sc['expected_fair_value']} × Σp·v {exp}"


@pytest.mark.parametrize("t", NON_HOLDING)
def test_sensibilidade_decrescente_no_ke(t):
    s = Mo(t).get("sensitivity") or {}
    col = [row[2] for row in s.get("ke_g") or []]  # g base
    assert len(col) == 5 and all(finite(x) for x in col), f"grade Ke×g {s.get('ke_g')}"
    assert all(b <= a + 1e-9 for a, b in zip(col, col[1:])), f"valor justo não cai com o Ke: {dict(zip(s.get('ke_axis'), col))}"
    assert abs(col[2] - Mo(t)["fair_value"]) < 1e-4 * max(1, Mo(t)["fair_value"]), f"centro da grade {col[2]} ≠ valor justo {Mo(t)['fair_value']}"


@pytest.mark.parametrize("t", TICKERS)
def test_upside_coerente_com_preco(t):
    m, c = Mo(t), ROWS[t]
    p = m.get("price")
    assert p and p > 0, f"preço {p}"
    exp = m["fair_value"] / p - 1
    assert abs(m["upside"] - exp) < 1e-4, f"upside {m['upside']} × valor/preço − 1 = {exp}"
    assert c.get("price_ref") == p, f"overview price_ref {c.get('price_ref')} × data/model price {p}"


@pytest.mark.parametrize("t", TICKERS)
def test_app_em_dia_com_o_modelo(t):
    """data/app/overview.json foi montado a partir do data/model atual (senão: rodar pipeline/build.py)."""
    m, c = Mo(t), ROWS[t]
    bad = []
    for k in ("fair_value", "upside", "irr_implied", "irr_3y"):
        a, b = c.get(k), m.get(k)
        b = None if b is None else round(b, 4)
        if (a is None) != (b is None) or (a is not None and abs(a - b) > 1.5e-4 + 1e-4 * abs(b)):
            bad.append(f"{k}: app {a} × modelo {b}")
    if bad:
        bad.append(f"data/model/{t}.json mais novo que overview.json ({OV['generated_at']})")
    assert not bad, fails(bad)


REF25 = pyref.reference([0.25])["0.25"]


@pytest.mark.parametrize("t", TICKERS)
def test_modelo_reproduzivel_a_partir_das_premissas(t):
    """model.py (Ke 25%, foto de preços) com research + hist atuais reproduz data/model/{T}.json."""
    r, m = REF25[t], Mo(t)
    assert "error" not in r, r.get("error")
    bad = [f"{k}: recalculado {r[k]} × gravado {m.get(k)}" for k in ("fair_value", "irr_implied", "irr_3y") if not rel_close(r[k], m.get(k))]
    assert not bad, fails(bad)


LOW = ("baixa",)


def test_oportunidades_seguem_a_regra_de_selecao():
    """As oportunidades publicadas têm relatório e ainda cumprem a regra (TIR ≥ 20%, P ≥ 45%, Altman fora de risco, confiança ≠ baixa)."""
    opp = OV.get("opportunities") or []
    assert opp, "sem oportunidades"
    bad = []
    for t in opp:
        c = ROWS.get(t)
        if not c:
            bad.append(f"{t}: fora da lista de empresas")
            continue
        if not (RESEARCH / "reports" / f"{t}.json").exists():
            bad.append(f"{t}: sem research/reports/{t}.json")
        m = Mo(t)
        irr, prob = m.get("irr_implied"), (m.get("monte_carlo") or {}).get("prob_above_price")
        conf = (c.get("confidence") or "").lower()
        if irr is None or irr < 0.20:
            bad.append(f"{t}: TIR implícita {irr} < 20% (modelo atual)")
        if prob is None or prob < 0.45:
            bad.append(f"{t}: P(valor > preço) {prob} < 45% (modelo atual)")
        if (c.get("altman") or {}).get("zone") == "risco":
            bad.append(f"{t}: Altman Z'' na zona de risco")
        if conf.startswith(LOW) and not conf.startswith(("baixa-m", "baixa a m")):
            bad.append(f"{t}: confiança '{c.get('confidence')}'")
    assert not bad, fails(bad)

"""Regra de decisão v2 e convenção de datas (revisão de 17/11/2026)."""
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
OV = json.load(open(ROOT / "data" / "app" / "overview.json"))
ROWS = {c["ticker"]: c for c in OV["companies"]}
KE = OV["ke"]


def test_data_de_avaliacao_e_a_da_foto_de_precos():
    assert OV["valuation_date"] == "2026-10-28"


@pytest.mark.parametrize("t", sorted(t for t, c in ROWS.items() if (c.get("engine") or {}).get("taus")))
def test_nenhum_fluxo_e_descontado_com_prazo_negativo(t):
    e = ROWS[t]["engine"]
    assert min(e["taus"]) >= 0, f"{t}: prazo de desconto negativo {min(e['taus']):.4f} (fluxo anterior à data de avaliação)"
    assert 0 <= e["f26"] <= 1, f"{t}: fração do stub de 2026 fora de [0, 1]"


def test_elegiveis_sao_subconjunto_da_lista_e_cumprem_a_meta():
    opp, elig = OV["opportunities"], OV["eligible"]
    assert set(elig) <= set(opp)
    for t in opp:
        c = ROWS[t]
        ok = c["irr_implied"] >= KE and c["ceiling"] is not None and c["price_ref"] <= c["ceiling"]
        assert (t in elig) == ok, f"{t}: elegibilidade inconsistente (TIR {c['irr_implied']}, preço {c['price_ref']}, teto {c['ceiling']})"


@pytest.mark.parametrize("t", sorted(OV["opportunities"]))
def test_teto_nao_supera_o_valor_justo(t):
    c = ROWS[t]
    assert c["ceiling"] is not None and c["ceiling"] <= c["fair_value"] + 1e-6


@pytest.mark.parametrize("t", sorted(t for t, c in ROWS.items() if c.get("mc_q") and c.get("prob_mc") is not None))
def test_quantis_do_painel_reproduzem_a_probabilidade_do_monte_carlo(t):
    c = ROWS[t]
    q, p = c["mc_q"], c["price_ref"]
    if p <= q[0]:
        est = 1.0
    elif p >= q[-1]:
        est = 0.0
    else:
        i = next(k for k in range(1, len(q)) if q[k] >= p)
        est = 1 - (i - 1 + (p - q[i - 1]) / ((q[i] - q[i - 1]) or 1)) / (len(q) - 1)
    assert abs(est - c["prob_mc"]) <= 0.01, f"{t}: quantis {est:.4f} × Monte Carlo {c['prob_mc']:.4f}"

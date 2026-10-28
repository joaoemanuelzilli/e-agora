"""(3) Integridade dos dados de mercado (data/market/*.json): preços, betas, datas, múltiplos históricos e proventos."""
import math
from datetime import date

import pytest

from conftest import MARKET, coverage, fails, load, market_tickers

TICKERS = market_tickers()
COV = set(coverage())
TODAY = "2026-10-26"
JUMP = 0.35
BETA_RANGE = (0.0, 3.0)        # betas usados no estudo (diário 2a, semanal 3a, de queda 3a)
CRASH_BETA_RANGE = (-0.5, 3.5)  # beta em dias de crash (exibido na página da empresa)


def P(t):
    return pytest.param(t, id=t + ("" if t in COV else "~fora"))


def M(t):
    return load(MARKET / f"{t}.json")


def split_dates(m):
    return [d for d, _ in (m.get("stats") or {}).get("split_events") or []]


def ordered(dates):
    return all(a < b for a, b in zip(dates, dates[1:]))


@pytest.mark.parametrize("t", [P(t) for t in TICKERS])
def test_series_com_datas_ordenadas_e_precos_positivos(t):
    m = M(t)
    bad = []
    for key in ("daily_3y", "weekly_10y", "ibov_daily_3y"):
        s = m.get(key) or []
        ds = [d for d, _ in s]
        if not ordered(ds):
            bad.append(f"{key}: datas fora de ordem ou repetidas")
        if any(d > TODAY for d in ds):
            bad.append(f"{key}: datas futuras {[d for d in ds if d > TODAY][:3]}")
        nonpos = [(d, v) for d, v in s if v is None or not v > 0]
        if nonpos:
            bad.append(f"{key}: preços ≤ 0 {nonpos[:3]}")
    if len(m.get("daily_3y") or []) < 120:
        bad.append(f"daily_3y com {len(m.get('daily_3y') or [])} pregões")
    assert not bad, fails(bad)


@pytest.mark.parametrize("t", [P(t) for t in TICKERS])
def test_sem_saltos_diarios_nao_explicados(t):
    """Retorno diário |r| > 35% na série ajustada só é aceito se houver evento societário (B3) a até 3 dias."""
    m = M(t)
    s = m.get("daily_3y") or []
    ev = [date.fromisoformat(d) for d in split_dates(m)]
    bad = []
    for (d0, v0), (d1, v1) in zip(s, s[1:]):
        r = v1 / v0 - 1
        if abs(r) > JUMP and not any(abs((date.fromisoformat(d1) - e).days) <= 3 for e in ev):
            bad.append(f"{d1}: {r:+.1%} ({v0} → {v1})")
    first = s[0][0] if s else "9999-12-31"
    for d, r in (m.get("stats") or {}).get("price_jumps_unexplained") or []:
        if d >= first:
            continue  # já avaliado acima na série de 3 anos
        bad.append(f"{d}: {r:+.1%} (fora da janela de 3 anos, marcado pelo pipeline como não explicado)")
    assert not bad, fails(bad)


@pytest.mark.parametrize("t", [P(t) for t in TICKERS])
def test_betas_plausiveis(t):
    st = M(t).get("stats") or {}
    bad = []
    for k in ("beta_2y_daily", "beta_3y_weekly", "beta_down_3y"):
        b = st.get(k)
        if b is None:
            continue
        if not (math.isfinite(b) and BETA_RANGE[0] <= b <= BETA_RANGE[1]):
            bad.append(f"{k} = {b:.2f} fora de [{BETA_RANGE[0]}, {BETA_RANGE[1]}]")
    b = st.get("beta_crash_10y")
    if b is not None and not (CRASH_BETA_RANGE[0] <= b <= CRASH_BETA_RANGE[1]):
        bad.append(f"beta_crash_10y = {b:.2f} fora de [{CRASH_BETA_RANGE[0]}, {CRASH_BETA_RANGE[1]}] com só {st.get('n_crash_days')} dias de crash")
    if st.get("beta_2y_daily") is None:
        bad.append("sem beta diário de 2 anos")
    assert not bad, fails(bad)


@pytest.mark.parametrize("t", [P(t) for t in TICKERS])
def test_multiplos_historicos_datas_ordenadas(t):
    ser = (M(t).get("multiples_history") or {}).get("series") or []
    ds = [r["date"] for r in ser]
    bad = []
    if not ordered(ds):
        bad.append("datas fora de ordem: " + " → ".join(ds[-3:]))
    fut = [d for d in ds if d > TODAY]
    if fut:
        bad.append(f"pontos com data futura {fut} (mês corrente rotulado no fim do mês)")
    assert not bad, fails(bad)


@pytest.mark.parametrize("t", [P(t) for t in TICKERS])
def test_multiplos_historicos_plausiveis(t):
    """Valor de mercado mensal sem saltos > 3× não explicados; P/L > 0,5x; DY < 50% (detecta quebra de escala de ações)."""
    m = M(t)
    ser = [r for r in (m.get("multiples_history") or {}).get("series") or [] if not r.get("live")]
    ev = split_dates(m)
    bad = []
    for a, b in zip(ser, ser[1:]):
        if a.get("mcap") and b.get("mcap"):
            r = b["mcap"] / a["mcap"]
            if (r > 3 or r < 1 / 3) and not any(a["date"] < d <= b["date"] for d in ev):
                bad.append(f"valor de mercado {a['date']} {a['mcap']:,.1f} → {b['date']} {b['mcap']:,.1f} (×{r:,.3g})")
    pe = [r for r in ser if r.get("pe") is not None and 0 < r["pe"] < 0.5]
    if pe:
        bad.append(f"{len(pe)} meses com P/L < 0,5x (ex.: {pe[0]['date']} {pe[0]['pe']}x)")
    dy = [r for r in ser if r.get("dy") is not None and r["dy"] > 0.5]
    if dy:
        bad.append(f"{len(dy)} meses com DY > 50% (ex.: {dy[0]['date']} {dy[0]['dy']:.0%})")
    dps = [r for r in m.get("dps_history") or [] if r.get("dy_avg_price") is not None and r["dy_avg_price"] > 0.5]
    if dps:
        bad.append(f"dps_history: DY médio > 50% em {[(r['year'], r['dy_avg_price']) for r in dps][:4]}")
    assert not bad, fails(bad, 6)


def test_cotacoes_da_foto_coerentes():
    """quotes.json: preço e fechamento anterior > 0 e variação = preço/anterior − 1 para as empresas da cobertura."""
    q = load(MARKET / "quotes.json")
    bad = []
    for t in coverage():
        x = q.get(t) or {}
        p, pc, ch = x.get("price"), x.get("prev_close"), x.get("chg_pct")
        if not (p and p > 0 and pc and pc > 0):
            bad.append(f"{t}: preço {p} / anterior {pc}")
            continue
        if ch is not None and abs((p / pc - 1) * 100 - ch) > 0.05:
            bad.append(f"{t}: variação {ch:.2f}% × {(p / pc - 1) * 100:.2f}%")
    assert not bad, fails(bad)


DIV = load(MARKET / "dividends.json")


@pytest.mark.parametrize("e", [pytest.param(e, id=e["ticker"]) for e in DIV["empresas"]])
def test_proventos_nao_negativos(e):
    """dividends.json: valores ≥ 0 (eventos, anos, TTM, a pagar, projeção), datas válidas e ordenadas, DY TTM < 50%."""
    bad = []
    ev = e.get("eventos") or []
    for x in ev:
        v = x.get("valor")
        if v is None or not v >= 0:
            bad.append(f"evento {x.get('dc')}: valor {v}")
        try:
            date.fromisoformat(x["dc"])
        except Exception:
            bad.append(f"evento com data-com inválida {x.get('dc')}")
    if [x["dc"] for x in ev] != sorted(x["dc"] for x in ev):
        bad.append("eventos fora de ordem de data-com")
    for a in e.get("annual") or []:
        if not a.get("total", 0) >= 0:
            bad.append(f"ano {a.get('ano')}: total {a.get('total')}")
    for a in e.get("a_pagar") or []:
        if a.get("valor") is None or a["valor"] < 0:
            bad.append(f"a pagar {a.get('pagamento')}: valor {a.get('valor')}")
    for x in e.get("proj_dps") or []:
        if x is not None and x < 0:
            bad.append(f"DPA projetado {x}")
    ttm = e.get("ttm") or {}
    if (ttm.get("total") or 0) < 0:
        bad.append(f"TTM {ttm.get('total')}")
    if ttm.get("dy") is not None and ttm["dy"] > 0.5:
        bad.append(f"DY TTM {ttm['dy']:.0%}")
    assert not bad, fails(bad)


def test_proventos_cobrem_toda_a_cobertura():
    got = {e["ticker"] for e in DIV["empresas"]}
    assert got == set(coverage()), f"faltam {sorted(set(coverage()) - got)}; sobram {sorted(got - set(coverage()))}"

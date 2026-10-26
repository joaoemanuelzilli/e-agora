"""(2) Integridade das demonstrações da CVM padronizadas (data/hist/*.json)."""
import math

import pytest

from conftest import HIST, MARKET, RESEARCH, SUPPLEMENT, coverage, fails, hist_tickers, load, qkey

TICKERS = hist_tickers()
COV = set(coverage())
FLOW_LTM = ("revenue", "ebit", "ebitda", "ni_controlling", "net_income", "d_and_a", "cfo")

# Limitações de dados documentadas pelo analista em research/{T}.json (overrides.notes): xfail, não falha nova.
KNOWN = {
    ("HAPV3", "ltm"): "IFRS 17 no ITR 2026: 3.01 do 6M26 não é comparável ao DFP 2025; base sobrescrita em research/HAPV3.json (overrides)",
}


def params(check):
    out = []
    for t in TICKERS:
        reason = KNOWN.get((t, check))
        marks = [pytest.mark.xfail(reason=reason, strict=False)] if reason else []
        out.append(pytest.param(t, id=t + ("" if t in COV else "~fora"), marks=marks))
    return out


def H(t):
    return load(HIST / f"{t}.json")


def periods_bs(h):
    """Balanços padronizados: anuais, trimestrais (ITR) e o balanço-base."""
    out = [(k, v) for k, v in (h.get("annual") or {}).items()]
    out += [(k, v) for k, v in (h.get("balance_quarterly") or {}).items()]
    if h.get("balance"):
        out.append(("balanço-base " + str(h["balance"].get("date")), h["balance"]))
    return out


def num(x):
    return x if isinstance(x, (int, float)) and math.isfinite(x) else None


@pytest.mark.parametrize("t", params("identity"))
def test_ativo_igual_passivo_mais_pl(t):
    """Ativo total = passivo circulante + não circulante + PL (1%); e, nas linhas brutas, conta 1 (BPA) = conta 2 (BPP)."""
    h = H(t)
    bad = []
    if not h.get("is_financial"):
        for k, b in periods_bs(h):
            ta, cl, ncl, eq = (num(b.get(x)) for x in ("total_assets", "current_liab", "noncurrent_liab", "equity"))
            if None in (ta, cl, ncl, eq):
                continue
            gap = ta - (cl + ncl + eq)
            if abs(gap) > 0.01 * abs(ta):
                bad.append(f"{k}: ativo {ta:,.1f} × passivo+PL {cl + ncl + eq:,.1f} ({gap / ta:+.1%})")
    raw = h.get("raw") or {}
    if raw.get("BPA") and raw.get("BPP"):
        a = {r[0]: r[2:] for r in raw["BPA"]["rows"]}
        p = {r[0]: r[2:] for r in raw["BPP"]["rows"]}
        for i, per in enumerate(raw["BPA"]["periods"]):
            va, vp = (a.get("1") or [None] * 9)[i], (p.get("2") or [None] * 9)[i]
            if va is not None and vp is not None and abs(va - vp) > 0.01 * abs(va):
                bad.append(f"bruto {per}: conta 1 {va:,.1f} × conta 2 {vp:,.1f}")
    assert not bad, fails(bad)


def last4(lq):
    y, q = qkey(lq)
    out = []
    for _ in range(4):
        out.append(f"{y}Q{q}")
        q -= 1
        if q == 0:
            y, q = y - 1, 4
    return out[::-1]


@pytest.mark.parametrize("t", params("ltm"))
def test_soma_4_trimestres_igual_ltm(t):
    """Σ dos 4 trimestres até o último ITR ≈ LTM (1% + R$ 1 mi) para receita, EBIT, EBITDA, lucro, D&A e FCO."""
    h = H(t)
    lq, ltm, q = h.get("latest_quarter"), h.get("ltm"), h.get("quarterly") or {}
    if not lq or not ltm:
        pytest.skip("sem ITR/LTM")
    ks = last4(lq)
    missing = [k for k in ks if k not in q]
    assert not missing, f"{h.get('ltm_label')}: trimestres ausentes {missing}"
    bad = []
    for f in FLOW_LTM:
        vals = [num(q[k].get(f)) for k in ks]
        L = num(ltm.get(f))
        if L is None or any(v is None for v in vals):
            continue
        s = sum(vals)
        if abs(s - L) > 0.01 * abs(L) + 1.0:
            bad.append(f"{f}: Σ{'+'.join(k[2:] for k in ks)} = {s:,.1f} × LTM {L:,.1f} ({(s - L) / abs(L or 1):+.1%})")
    assert not bad, fails(bad)


def b3n(s):
    return float(str(s or "0").replace(".", "") or 0)


@pytest.mark.parametrize("t", params("shares"))
def test_acoes_coerentes_com_b3(t):
    """Ações = total da B3 (suplemento oficial); em circulação = total × (1 − tesouraria); ON + PN = circulação; CVM ≈ B3."""
    if not SUPPLEMENT.exists():
        pytest.skip(f"suplemento B3 não encontrado em {SUPPLEMENT} (defina B3_SUPPLEMENT)")
    h = H(t)
    sh = h.get("shares") or {}
    sp = load(SUPPLEMENT).get(t[:4]) or {}
    b3 = b3n(sp.get("totalNumberShares"))
    assert sh, "sem bloco 'shares'"
    assert b3 > 0, f"emissor {t[:4]} sem totalNumberShares no suplemento da B3"
    bad = []
    if abs((sh.get("total") or 0) - b3) > 0.001 * b3:
        bad.append(f"total {sh.get('total'):,.0f} × B3 {b3:,.0f}")
    tr = sh.get("treasury_ratio")
    if tr is None or not (0 <= tr < 0.25):
        bad.append(f"fração em tesouraria {tr}")
    else:
        exp = b3 * (1 - tr)
        if abs((sh.get("outstanding") or 0) - exp) > 0.001 * exp:
            bad.append(f"em circulação {sh.get('outstanding'):,.0f} × B3×(1−tes.) {exp:,.0f}")
    on, pn, out = sh.get("on") or 0, sh.get("pn") or 0, sh.get("outstanding") or 0
    if out and abs(on + pn - out) > 0.005 * out:
        bad.append(f"ON {on:,.0f} + PN {pn:,.0f} ≠ circulação {out:,.0f}")
    bv = sh.get("b3_vs_cvm")
    hs = h.get("shares_history") or []
    m = split_mult(t, hs[-1]["date"], "2026-10-26") if hs else 1.0  # desdobramentos depois do último ITR
    if bv is not None and abs(bv / m - 1) > 0.10:
        bad.append(f"B3/CVM (último ITR, escala {sh.get('cvm_scale')}) = {bv:.4f} (eventos B3 posteriores ×{m:.4g}): "
                   f"quantidade da B3 difere >10% da CVM {sh.get('cvm_outstanding'):,.0f}")
    assert not bad, fails(bad)


def split_mult(t, d0, d1):
    mp = MARKET / f"{t}.json"
    if not mp.exists():
        return 1.0
    m = 1.0
    for d, k in (load(mp).get("stats") or {}).get("split_events") or []:
        if d0 < d <= d1:
            m *= k
    return m


@pytest.mark.parametrize("t", params("shares_hist"))
def test_historico_de_acoes_sem_quebra_de_escala(t):
    """shares_history (CVM): variação entre registros consecutivos ≤ 3× salvo desdobramento/grupamento/bonificação da B3."""
    hs = H(t).get("shares_history") or []
    bad = []
    for a, b in zip(hs, hs[1:]):
        if not a.get("total") or not b.get("total"):
            continue
        r = b["total"] / a["total"]
        if 1 / 3 <= r <= 3:
            continue
        m = split_mult(t, a["date"], b["date"])
        if abs(r / m - 1) <= 0.2:
            continue
        bad.append(f"{a['date']}→{b['date']}: {a['total']:,.0f} → {b['total']:,.0f} (×{r:,.4g})")
    assert not bad, fails(bad, 6)


@pytest.mark.parametrize("t", params("net_debt"))
def test_divida_liquida_bruta_menos_caixa_mais_arrendamentos(t):
    """DL = dívida bruta − caixa e aplicações + arrendamentos; bruta = CP + LP + outras linhas; caixa = disp. + aplic. CP + LP."""
    h = H(t)
    if h.get("is_financial"):
        pytest.skip("financeira: DL não se aplica")
    bad = []
    for k, b in periods_bs(h):
        g, c, l, nd, ndx = (num(b.get(x)) for x in ("gross_debt", "cash_total", "leases", "net_debt", "net_debt_ex_leases"))
        if nd is None:
            continue
        if None in (g, c, l):
            bad.append(f"{k}: componentes ausentes (bruta {g}, caixa {c}, arrend. {l})")
            continue
        if abs(nd - (g - c + l)) > 0.05:
            bad.append(f"{k}: DL {nd:,.2f} × {g:,.2f} − {c:,.2f} + {l:,.2f} = {g - c + l:,.2f}")
        if ndx is not None and abs(ndx - (g - c)) > 0.05:
            bad.append(f"{k}: DL ex-arrend. {ndx:,.2f} × {g - c:,.2f}")
        gd = sum(num(b.get(x)) or 0 for x in ("st_debt", "lt_debt", "debt_other_lines"))
        if abs(gd - g) > 0.05:
            bad.append(f"{k}: bruta {g:,.2f} × CP+LP+outras {gd:,.2f}")
        ct = sum(num(b.get(x)) or 0 for x in ("cash", "st_investments", "lt_investments"))
        if abs(ct - c) > 0.05:
            bad.append(f"{k}: caixa total {c:,.2f} × soma {ct:,.2f}")
    assert not bad, fails(bad)


@pytest.mark.parametrize("t", params("signs"))
def test_sinais_receita_positiva_e_da_nao_negativa(t):
    """Receita > 0 e D&A ≥ 0 em todos os anos, trimestres e no LTM; ativo total > 0."""
    h = H(t)
    bad = []
    rows = [(k, v) for k, v in (h.get("annual") or {}).items()] + [(k, v) for k, v in sorted((h.get("quarterly") or {}).items(), key=lambda kv: qkey(kv[0]))]
    if h.get("ltm"):
        rows.append((h.get("ltm_label") or "LTM", h["ltm"]))
    for k, a in rows:
        rv, da = num(a.get("revenue")), num(a.get("d_and_a"))
        if rv is not None and rv <= 0:
            bad.append(f"{k}: receita {rv:,.2f}")
        if da is not None and da < 0:
            bad.append(f"{k}: D&A {da:,.2f}")
    for k, b in periods_bs(h):
        ta = num(b.get("total_assets"))
        if ta is not None and ta <= 0:
            bad.append(f"{k}: ativo total {ta}")
    assert not bad, fails(bad)


@pytest.mark.parametrize("t", params("years"))
def test_sem_anos_ou_trimestres_faltantes(t):
    """Anos contíguos até FY2025 (sem DRE zerada), trimestres contíguos até o último ITR (2T26 ou 3T26)."""
    h = H(t)
    a = h.get("annual") or {}
    ys = sorted(int(k[2:]) for k in a)
    bad = []
    assert ys, "sem anos"
    holes = [y for y in range(ys[0], ys[-1] + 1) if y not in ys]
    if holes:
        bad.append(f"anos ausentes {holes}")
    if ys[-1] != 2025:
        bad.append(f"último ano {ys[-1]} (esperado FY2025)")
    for y in ys:
        d = a[f"FY{y}"]
        if all((num(d.get(k)) or 0) == 0 for k in ("revenue", "ebit", "net_income", "ni_controlling")):
            bad.append(f"FY{y}: DRE zerada (receita, EBIT e lucro = 0)")
    q = h.get("quarterly") or {}
    ks = sorted(q, key=qkey)
    if ks:
        y, qq = qkey(ks[0])
        miss = []
        while (y, qq) <= qkey(ks[-1]):
            if f"{y}Q{qq}" not in q:
                miss.append(f"{y}Q{qq}")
            qq += 1
            if qq == 5:
                y, qq = y + 1, 1
        if miss:
            bad.append(f"trimestres ausentes {miss}")
    if h.get("latest_quarter") not in ("2026Q2", "2026Q3"):
        bad.append(f"último ITR {h.get('latest_quarter')} (esperado 2T26 ou 3T26)")
    if t in COV and not h.get("ltm"):
        bad.append("sem LTM")
    assert not bad, fails(bad)


def test_cobertura_tem_todos_os_artefatos():
    """As 59 empresas da cobertura têm hist (CVM), mercado, premissas e modelo."""
    miss = []
    for t in coverage():
        for p in (HIST / f"{t}.json", MARKET / f"{t}.json", RESEARCH / f"{t}.json", HIST.parent / "model" / f"{t}.json"):
            if not p.exists():
                miss.append(str(p.relative_to(HIST.parents[1])))
    assert len(coverage()) == 59, f"cobertura com {len(coverage())} empresas"
    assert not miss, fails(miss)

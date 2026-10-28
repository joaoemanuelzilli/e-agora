#!/usr/bin/env python3
"""Métodos alternativos de valuation a Ke 25% e teste de pesos por template/setor (59 empresas, 26/10/2026).

Reavalia todas as empresas com o motor do estudo (`pipeline/model.py`, importado SEM alteração) a partir das
premissas atuais de `research/{T}.json`, do histórico CVM (`data/hist`) e da foto de preços do estudo
(`data/market/quotes.json`, EAGORA_SNAPSHOT=1). Revisores podem mudar premissas: basta rodar de novo.

Métodos acrescentados (todos por ação/unit, comparáveis ao preço):
  (a) RIM / Ohlson (lucro residual): V = PL_base + Σ (LL_t − c_t·PL_{t−1}) descontado a Ke, com o ROE de 2030 convergindo
      linearmente ao ROE terminal das premissas em 10 anos (2031–2040) e perpetuidade do lucro residual a g.
  (b) EVA: EV = CI_0 + Σ (NOPAT_t − c_t·CI_{t−1}) a WACC (CI evolui pelo investimento líquido: capex − D&A + ΔCG), com
      fade do ROIC de 2030 ao ROIC terminal em 10 anos; ponte para o equity igual à do DCF.
  (c) APV: Ku (Harris–Pringle) = (1 − wd)·Ke + wd·Kd com a mesma alavancagem do WACC do estudo; FCFF e perpetuidade a Ku;
      + VP do benefício fiscal da dívida líquida PROJETADA (34%, ou a alíquota efetiva se < 20%: RET, SUDENE, prejuízo).
  (d) FCFE explícito: LL + D&A − capex − ΔCG + Δdívida, com a dívida líquida do balanço-base crescendo com a receita
      (juros e LL recalculados), descontado a Ke; perpetuidade LL·(1+g)·(1 − g/ROE_T)/(Ke − g).
  (e) P/L e P/VP justificados (Gordon, ROE terminal): P/VP = (ROE_T − g)/(Ke − g) × VPA atual;
      P/L = (1 − g/ROE_T)/(Ke − g) × LPA 12m à frente.
  (f) Múltiplos de mercado: mediana dos pares da cobertura (P/L 2027E, EV/EBITDA 2027E, P/VP atuais) e mediana de
      5 anos da própria ação (P/L, EV/EBITDA, P/VP LTM, `multiples_history.stats`) aplicadas às métricas da empresa.
Bancos: RIM, DDM, P/L e P/VP justificados e múltiplos (sem FCFF/EVA/APV/FCFE: dívida é matéria-prima).
Holdings: SOTP recalculado com o novo valor justo das controladas avaliadas pelo motor; P/VP histórico como referência.

Compara com DCF/DDM/múltiplos do estudo (dispersão, viés sistemático, divergências e causas), aplica pesos propostos
por classe (template/setor) e mostra o efeito em valor justo, upside, ranking (upside e escore multifator do
build.py) e nas 7 oportunidades. Checagens: RIM com a perpetuidade do DDM reproduz o DDM (identidade de clean surplus)
e EVA com a perpetuidade do DCF reproduz o EV do DCF.

Uso:   .venv/bin/python pipeline/tests/alt_methods.py
Saídas: data/tests/alt_methods.json e data/tests/alt_methods.md (nada fora de data/tests/ é gravado).
"""
import json
import math
import os
import sys
import warnings
from datetime import date, datetime
from pathlib import Path

import numpy as np

os.environ["EAGORA_SNAPSHOT"] = "1"  # mesma foto de preços do estudo
sys.dont_write_bytecode = True       # não grava .pyc em pipeline/__pycache__ (fora de pipeline/tests/)
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
import model as M  # noqa: E402  (motor do estudo, sem alterações)

OUT_JSON = ROOT / "data" / "tests" / "alt_methods.json"
OUT_MD = ROOT / "data" / "tests" / "alt_methods.md"
KE = M.KE
TAX_STAT = M.TAX_SHIELD
VAL = M.VAL_DATE
FADE_N = 10
FADE_YEARS = list(range(2031, 2031 + FADE_N))
FADE_TAUS = np.array([M.yf(VAL, date(y, 7, 1)) for y in FADE_YEARS])
W26 = M.yf(VAL, date(2026, 12, 31))  # LPA 12m à frente = W26·LPA26 + (1 − W26)·LPA27
TS_MIN_EFFECTIVE = 0.20
PEER_GROUP_FALLBACK = {"G04_moda_consumo", "G11_utilities"}
MULT_BOUNDS = {"pe": (0.0, 60.0), "ev_ebitda": (0.0, 40.0), "pbv": (0.0, 20.0)}
FACTOR_W = {"valor": 0.30, "upside": 0.10, "qualidade": 0.20, "solidez": 0.15, "sobrerreacao": 0.10, "probabilidade": 0.15}

LABEL = {"dcf": "DCF-FCFF (estudo)", "ddm": "DDM (estudo)", "ddm_adj": "DDM c/ emissões e recompras", "multiples": "Múltiplos-alvo (estudo)",
         "rim": "RIM/Ohlson (fade ROE)", "eva": "EVA (fade ROIC)", "apv": "APV", "fcfe": "FCFE (DL ∝ receita)",
         "pe_just": "P/L justificado", "pbv_just": "P/VP justificado", "peers": "Pares (mediana)",
         "hist": "Histórico 5a (mediana)", "peers_adj": "Pares ajustados ao Ke 25%", "sotp": "SOTP (estudo)",
         "sotp_new": "SOTP (controladas c/ pesos novos)", "nav_market": "NAV a mercado"}
INTRINSIC = ["dcf", "apv", "eva", "ddm", "ddm_adj", "fcfe", "rim", "pe_just", "pbv_just"]
RELATIVE_ADJ = ["peers_adj"]
MARKET = ["multiples", "peers", "hist"]
ALL_METHODS = INTRINSIC + RELATIVE_ADJ + MARKET

# ------------------------------------------------------------------ classes e pesos propostos
CLASS_BY_GROUP = {
    "G01_locacao": "locacao", "G03_varejo_massa": "varejo_consumo", "G04_moda_consumo": "varejo_consumo",
    "G05_alimentar_farma": "varejo_consumo", "G06_incorp_media_alta": "incorporadora", "G07_incorp_mcmv": "incorporadora",
    "G09_educacao_saude": "servicos_tecnologia", "G11_utilities": "infra_utilities", "G10_financeiro": "servicos_tecnologia",
}
CLASS_OVERRIDE = {
    "ECOR3": "infra_utilities", "MOTV3": "infra_utilities", "RAIL3": "infra_utilities", "ORVR3": "infra_utilities",
    "ALOS3": "renda_imobiliaria", "IGTI11": "renda_imobiliaria", "MULT3": "renda_imobiliaria",
    "VBBR3": "ciclico_commodity", "BEEF3": "ciclico_commodity", "TTEN3": "ciclico_commodity",
    "SMFT3": "servicos_tecnologia", "CVCB3": "servicos_tecnologia", "TOTS3": "servicos_tecnologia",
    "INTB3": "servicos_tecnologia", "GGPS3": "servicos_tecnologia", "B3SA3": "servicos_tecnologia",
}
WEIGHTS = {
    "banco": {"rim": 0.50, "ddm": 0.25, "pbv_just": 0.25},
    "incorporadora": {"rim": 0.45, "fcfe": 0.20, "peers_adj": 0.15, "dcf": 0.10, "pbv_just": 0.10},
    "infra_utilities": {"apv": 0.40, "dcf": 0.20, "fcfe": 0.20, "ddm_adj": 0.20},
    "renda_imobiliaria": {"apv": 0.35, "dcf": 0.35, "fcfe": 0.15, "ddm_adj": 0.15},
    "locacao": {"eva": 0.30, "apv": 0.25, "dcf": 0.25, "fcfe": 0.20},
    "varejo_consumo": {"dcf": 0.35, "fcfe": 0.20, "peers_adj": 0.25, "pe_just": 0.20},
    "servicos_tecnologia": {"dcf": 0.40, "fcfe": 0.20, "eva": 0.20, "pe_just": 0.20},
    "ciclico_commodity": {"dcf": 0.45, "fcfe": 0.30, "ddm_adj": 0.25},
    "holding": {"sotp_new": 1.0},
}
CLASS_LABEL = {
    "banco": "Bancos", "incorporadora": "Incorporadoras", "infra_utilities": "Infraestrutura e utilities",
    "renda_imobiliaria": "Shoppings (renda imobiliária)", "locacao": "Locação (capital intensivo)",
    "varejo_consumo": "Varejo e consumo", "servicos_tecnologia": "Serviços, saúde, educação e tecnologia",
    "ciclico_commodity": "Cíclicas / commodities", "holding": "Holdings (SOTP)",
}
CLASS_WHY = {
    "banco": "Dívida é matéria-prima (não há FCFF/EV); o valor vem do spread ROE − Ke sobre o capital regulatório. "
             "RIM ancora no PL (Basileia) e independe da política de payout; DDM complementa (dividendo limitado pelo capital); "
             "P/VP justificado = RIM em estado estacionário. Múltiplos de mercado embutem Ke implícito < 25% e ficam como referência.",
    "incorporadora": "Estoque/terreno e recebíveis SÃO o capital de giro: FCFF oscila com landbank e repasses, e o lucro (POC) mede melhor "
                     "a criação de valor. RIM sobre o PL (estoque a custo) é o método natural, com P/VP justificado como âncora e FCFE "
                     "(dívida SFH/cessões no fluxo do acionista); DCF com peso baixo porque o FCFF ignora o other_financial (juros "
                     "capitalizados, custo de cessões); pares MCMV/média-alta são homogêneos (ajustados ao Ke 25%).",
    "infra_utilities": "Ativos de vida longa, fluxos previsíveis e alavancagem que muda ao longo da concessão (amortização, ciclos de capex): "
                       "o APV separa valor operacional (Ku) do benefício fiscal da dívida projetada, sem supor wd constante; "
                       "DCF-WACC como contraparte; DDM/FCFE (40%) porque, com Ke fixo e ROIC < WACC, o EV fica abaixo da dívida e só o "
                       "lado do acionista (responsabilidade limitada) dá valor positivo.",
    "renda_imobiliaria": "NOI estável e alavancagem estrutural (CRI/debêntures) → DCF/APV; PL a custo histórico subavalia as "
                         "propriedades, então RIM/P/VP ficam fora; DDM/FCFE capturam a distribuição recorrente.",
    "locacao": "Valor = (ROIC − WACC) × crescimento da frota: EVA explicita o spread e sua convergência; dívida é estrutural "
               "e cíclica (APV); DCF como base; FCFE (estrutura de capital constante) evita penalizar a retenção.",
    "varejo_consumo": "Ciclo curto, margens que revertem à média e arrendamentos IFRS-16: a perpetuidade do DCF é frágil e os "
                      "pares carregam a leitura do ciclo — mas reescalados ao Ke 25% (Gordon, pela TIR implícita de cada par); P/L "
                      "justificado mantém o múltiplo coerente com o Ke; FCFE evita penalizar a retenção.",
    "servicos_tecnologia": "Asset-light/crescimento: DCF como base; EVA expõe a convergência do ROIC; FCFE (estrutura de capital constante) "
                           "e P/L justificado como checagens do lado do acionista.",
    "ciclico_commodity": "Lucro cíclico e alavancagem alta: DCF com o ciclo projetado explicitamente; FCFE/DDM do lado do acionista. "
                         "Múltiplos (históricos ou de pares) não normalizam o ciclo a Ke 25% e o PL é comprimido (BEEF3): ficam como referência.",
    "holding": "SOTP é o único método coerente; recalculado com o valor justo novo das controladas avaliadas pelo motor.",
}


def classify(t, tpl, group):
    if tpl == "financial":
        return "banco"
    if tpl == "holding":
        return "holding"
    return CLASS_OVERRIDE.get(t) or CLASS_BY_GROUP.get(group) or "servicos_tecnologia"


# ------------------------------------------------------------------ utilitários
def load(p):
    with open(p) as fh:
        return json.load(fh)


def fnum(x):
    try:
        x = float(x)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def pos(x):
    x = fnum(x)
    return x if x is not None and x > 0 else None


def median(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)) if xs else None


def zscore(vals):  # igual ao build.py
    a = np.array([np.nan if v is None else v for v in vals], dtype=float)
    m, s = np.nanmean(a), np.nanstd(a)
    out = (a - m) / s if s and np.isfinite(s) and s > 0 else np.zeros_like(a)
    out = np.clip(out, -3, 3)
    return [None if not np.isfinite(x) else float(x) for x in out]


def spearman(a, b):
    # pares com valor ausente (ex.: holding sem TIR, empresa sem P(MC)) ficam de fora
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None and np.isfinite(x) and np.isfinite(y)]
    if len(pairs) < 3:
        return float("nan")
    a2, b2 = zip(*pairs)
    ra = np.argsort(np.argsort(a2)).astype(float)
    rb = np.argsort(np.argsort(b2)).astype(float)
    return float(np.corrcoef(ra, rb)[0, 1])


def blend(vals, weights):
    """Mesma regra do motor: média ponderada de max(0, valor) renormalizada sobre os métodos disponíveis."""
    tot, acc, used = 0.0, 0.0, {}
    for k, w in weights.items():
        x = fnum(vals.get(k))
        if x is not None:
            acc += w * max(0.0, x)
            tot += w
            used[k] = w
    if not tot:
        return None, {}
    return acc / tot, {k: w / tot for k, w in used.items()}


# ------------------------------------------------------------------ motor do estudo
def seed_missing_quotes(cov):
    """Componentes de holdings fora da foto de preços (ex.: AMOB3, PASS3) fariam o motor buscar cotação ao vivo, que pode
    falhar e zerar o componente. Para reprodutibilidade, semeia o cache de cotações do motor (só em memória) com o preço
    implícito no último data/model/{holding}.json gravado pelo próprio motor."""
    snap = load(ROOT / "data" / "market" / "quotes.json")
    seeded = {}
    for c in cov:
        prem = load(ROOT / "research" / f"{c['ticker']}.json")
        if prem.get("template") != "holding":
            continue
        stored = {x.get("ticker"): x for x in (load(ROOT / "data" / "model" / f"{c['ticker']}.json").get("components") or [])}
        for comp in (prem.get("sotp") or {}).get("components", []):
            tk = comp.get("ticker")
            if not tk or comp.get("method") != "market" or tk in snap or tk in M._quote_cache:
                continue
            hp = ROOT / "data" / "hist" / f"{tk}.json"
            n = None
            if hp.exists():
                hh = load(hp)
                n = M.num((hh.get("shares") or {}).get("outstanding")) / 1e6 / (hh.get("shares_per_unit") or 1)
            if not n and comp.get("shares_mn"):
                n = M.num(comp["shares_mn"])
            v = fnum((stored.get(tk) or {}).get("value_mkt_100"))
            if n and v:
                M._quote_cache[tk] = {"price": v / n, "source": "semeado de data/model (última rodada do motor)"}
                seeded[tk] = round(v / n, 4)
    return seeded


def run_engine(cov):
    models, ctx = {}, {}
    prems = {c["ticker"]: load(ROOT / "research" / f"{c['ticker']}.json") for c in cov}
    order = sorted(cov, key=lambda c: (prems[c["ticker"]].get("template") == "holding", c["ticker"]))
    for c in order:
        t = c["ticker"]
        prem = prems[t]
        hist = load(ROOT / "data" / "hist" / f"{t}.json")
        q = M.live_quote(t) or {}
        price = q.get("price")
        sh = M.shares_info(hist, prem)
        mpre = mnow = None
        if prem.get("template") == "holding":
            r = M.value_holding(prem, hist, models, price=price)
        else:
            prev = q.get("prev_close")
            mpre = M.market_cap(prem, hist, sh, prev) if prev else None
            mnow = M.market_cap(prem, hist, sh, price) if price else None
            r = M.value_company(prem, hist, price=price, mcap=mpre or mnow, mcap_now=mnow)
        r["price"] = price
        models[t] = r
        ctx[t] = {"prem": prem, "hist": hist, "price": price, "mcap_pre": mpre, "mcap_now": mnow, "cov": c}
    return models, ctx


# ------------------------------------------------------------------ (a) RIM / Ohlson
def rim_value(B0, ni, B, f26, taus, s0, tau_T, ke, g, roe_lr, tv_engine=None):
    """Lucro residual (Edwards–Bell–Ohlson) com encargo de capital exato no espaçamento de meio de período do motor.

    V = B0·(1+Ke)^(−s0) + Σ_{2026–30} RI_t·(1+Ke)^(−τ_t) + VC_2030·(1+Ke)^(−τ_T) − PL_2030·(1+Ke)^(−τ_2030),
    RI_t = LL_t − c_t·PL_{t−1}, c_t = (1+Ke)^(τ_t − τ_{t−1}) − 1. VC_2030 = valor de continuação do equity em 31/12/2030 na
    mesma convenção da perpetuidade do motor (fluxos de fim de ano): com a perpetuidade do DDM do estudo, V ≡ DDM (identidade de
    clean surplus). Com fade: VC = PL_2030 + Σ_{2031–40} (ROE_t − Ke)·PL_{t−1}/(1+Ke)^k + perpetuidade do RI a g, com ROE_2031 =
    LL_2030·(1+g)/PL_2030 (continuação do estudo) convergindo linear ao ROE terminal e reinvestimento de g/ROE_T do lucro.
    """
    if B0 is None or B0 <= 0:
        return None
    taus = np.asarray(taus, dtype=float)
    s = np.concatenate([[s0], taus])
    c = (1 + ke) ** np.diff(s) - 1
    b_prev = np.concatenate([[B0], B[:-1]])
    ni_eff = np.array(ni, dtype=float)
    ni_eff[0] *= f26
    ri = ni_eff - c * b_prev
    d = (1 + ke) ** (-taus)
    d_T = (1 + ke) ** (-tau_T)
    pv_book = B0 * (1 + ke) ** (-s0)
    pv_ri = float(np.sum(ri * d))
    B_T = B[-1]
    roe_30 = ni[-1] * (1 + g) / B_T if B_T > 0 else roe_lr
    v_engine = pv_book + pv_ri + tv_engine * d_T - B_T * d[-1] if tv_engine is not None else None
    # Fade só corrói retorno EXCEDENTE (ROE de continuação > ROE terminal). Abaixo disso o PL costuma carregar ágio/intangíveis
    # e o ROE terminal das premissas vale para o investimento novo: usa-se a perpetuidade do próprio estudo.
    fade = B_T > 0 and roe_30 >= roe_lr
    cv_ri = None
    if fade:
        b, cv_ri = B_T, 0.0
        for k in range(FADE_N):  # 2031 = roe_30 … 2040 = roe_lr
            roe_k = roe_30 + (roe_lr - roe_30) * k / (FADE_N - 1)
            cv_ri += (roe_k - ke) * b / (1 + ke) ** (k + 1)
            b *= 1 + roe_k * g / roe_lr
        cv_ri += (roe_lr - ke) * b / (ke - g) / (1 + ke) ** FADE_N
        value = pv_book + pv_ri + (B_T + cv_ri) * d_T - B_T * d[-1]
    else:
        value = v_engine if v_engine is not None else pv_book + pv_ri
    cv_eq = (B_T + cv_ri) if fade else tv_engine
    return {"value_mn": value, "fade_applied": bool(fade), "pv_book": pv_book, "pv_ri_2026_30": pv_ri,
            "continuing_value_equity_2030": cv_eq, "continuing_value_engine_2030": tv_engine,
            "pv_terminal_net_of_book": value - pv_book - pv_ri, "roe_2031_start": roe_30, "roe_lr": roe_lr,
            "book_share_of_value": pv_book / value if value else None, "value_engine_tv_mn": v_engine}


# ------------------------------------------------------------------ (b) EVA
def eva_value(pr, r, minority_book, s0):
    w = r["dcf"]["wacc"]
    g = r["g"]
    f26 = pr["f26"]
    taus = np.asarray(r["taus"], dtype=float)
    nopat = pr["ebit"] * (1 - pr["tax_rate"])
    netinv = pr["capex"] - pr["d_and_a"] + pr["d_nwc"]
    nop, inv = nopat.copy(), netinv.copy()
    nop[0] *= f26
    inv[0] *= f26
    ic0 = pr["eq_base"] + pr["nd_base"] + minority_book
    ic = ic0 + np.cumsum(inv)
    ic_prev = np.concatenate([[ic0], ic[:-1]])
    s = np.concatenate([[s0], taus])
    c = (1 + w) ** np.diff(s) - 1
    eva = nop - c * ic_prev
    d = (1 + w) ** (-taus)
    pv_ic0 = ic0 * (1 + w) ** (-s0)
    pv_eva = float(np.sum(eva * d))
    roic_lr = max(r["dcf"]["roic_T"], g + 0.02)
    ic_T = ic[-1]
    roic_30 = nopat[-1] * (1 + g) / ic_T if ic_T > 0 else roic_lr  # ROIC 2031 na continuação do estudo
    d_T = (1 + w) ** (-r["tau_T"])
    ev_chk = pv_ic0 + pv_eva + r["dcf"]["tv"] * d_T - ic_T * d[-1]  # ≡ EV do DCF (identidade)
    fade = ic_T > 0 and roic_30 >= roic_lr  # mesma regra do RIM: só o retorno excedente converge
    cv_eva = None
    if fade:
        k_ic, cv_eva = ic_T, 0.0
        for k in range(FADE_N):  # investimento líquido = g/ROIC_T do NOPAT, como na perpetuidade do estudo
            roic_k = roic_30 + (roic_lr - roic_30) * k / (FADE_N - 1)
            cv_eva += (roic_k - w) * k_ic / (1 + w) ** (k + 1)
            k_ic *= 1 + roic_k * g / roic_lr
        cv_eva += (roic_lr - w) * k_ic / (w - g) / (1 + w) ** FADE_N
        ev = pv_ic0 + pv_eva + (ic_T + cv_eva) * d_T - ic_T * d[-1]
    else:
        ev = ev_chk
    pv_fade = ev - ev_chk
    pv_tv = (ic_T + cv_eva) if fade else r["dcf"]["tv"]
    return {"ev_mn": ev, "fade_applied": bool(fade), "ev_engine_tv_mn": ev_chk, "ic0": ic0, "pv_ic0": pv_ic0, "pv_eva_2026_30": pv_eva,
            "fade_effect_on_ev": pv_fade, "continuing_value_ev_2030": pv_tv, "roic_2031_start": roic_30, "roic_lr": roic_lr,
            "wacc": w, "eva": eva.tolist(), "roic_minus_wacc_2030": roic_30 - w}


# ------------------------------------------------------------------ (c) APV
def apv_value(pr, r, prem):
    d = r["dcf"]
    g = r["g"]
    f26 = pr["f26"]
    taus = np.asarray(r["taus"], dtype=float)
    tau_T = r["tau_T"]
    wd, kd = d["wd"], d["kd"]
    cnd = M.arr((prem.get("projection") or {}).get("cost_of_net_debt"))
    kd_hp = kd
    if cnd.max() > 0.05 and kd > cnd.max() + 0.04:  # Kd "grossed-up" para anular o benefício fiscal (RET)
        kd_hp = float(cnd.mean())
    ku = (1 - wd) * KE + wd * kd_hp
    flows = pr["fcff"].copy()
    flows[0] *= f26
    pv_u = float(np.sum(flows / (1 + ku) ** taus))
    roic_T = max(d["roic_T"], g + 0.02)
    nopat_T = pr["ebit"][-1] * (1 - pr["tax_rate"][-1])
    tv_u = nopat_T * (1 + g) * (1 - g / roic_T) / (ku - g)
    pv_tv_u = tv_u / (1 + ku) ** tau_T
    tx = pr["tax_rate"]
    tau_ts = np.where(tx >= TS_MIN_EFFECTIVE, TAX_STAT, np.maximum(tx, 0.0))
    nd_prev = np.concatenate([[pr["nd_base"]], pr["net_debt"][:-1]])
    ts = tau_ts * cnd * np.maximum(nd_prev, 0.0) * (pr["ebt"] > 0)
    ts_flows = ts.copy()
    ts_flows[0] *= f26
    pv_ts = float(np.sum(ts_flows / (1 + ku) ** taus))
    ts_T = tau_ts[-1] * cnd[-1] * max(pr["net_debt"][-1], 0.0) * (1 + g) * (pr["ebt"][-1] > 0)
    pv_tv_ts = ts_T / (ku - g) / (1 + ku) ** tau_T
    ev = pv_u + pv_tv_u + pv_ts + pv_tv_ts
    return {"ev_mn": ev, "ku": ku, "kd_used": kd_hp, "wd": wd, "pv_unlevered": pv_u + pv_tv_u, "pv_tax_shield": pv_ts + pv_tv_ts,
            "tax_shield_share_ev": (pv_ts + pv_tv_ts) / ev if ev else None, "tau_ts_2030": float(tau_ts[-1]),
            "nd_2030": float(pr["net_debt"][-1]), "nd_base": float(pr["nd_base"]),
            "nd_ebitda_base": float(pr["nd_base"] / pr["ebitda"][0]) if pr["ebitda"][0] > 0 else None,
            "nd_ebitda_2030": float(pr["net_debt"][-1] / pr["ebitda"][-1]) if pr["ebitda"][-1] > 0 else None}


# ------------------------------------------------------------------ (d) FCFE explícito
def fcfe_value(pr, r, prem):
    p = prem.get("projection") or {}
    g = r["g"]
    f26 = pr["f26"]
    taus = np.asarray(r["taus"], dtype=float)
    kd = M.arr(p.get("cost_of_net_debt"))
    of = M.arr(p.get("other_financial"))
    mino = M.num(p.get("minority_share_ni"))
    tx = pr["tax_rate"]
    nd0, eb, rev = pr["nd_base"], pr["ebitda"], pr["revenue"]
    # estrutura de capital constante em relação ao porte: DL acompanha a receita (não o EBITDA, para não realavancar em
    # recuperação de margem); caixa líquido fica constante (não é distribuído nem investido)
    lev = nd0 / eb[0] if nd0 > 0 and eb[0] > 0 else None
    nd = nd0 * rev / rev[0] if nd0 > 0 and rev[0] > 0 else np.full(5, nd0)
    nd_prev = np.concatenate([[nd0], nd[:-1]])
    fin = -kd * nd_prev + of
    ebt = pr["ebit"] + fin
    tax = np.maximum(ebt, 0.0) * tx
    ni = ebt - tax
    ni_c = ni * (1 - mino)
    fcfe_tot = ni + pr["d_and_a"] - pr["capex"] - pr["d_nwc"] + (nd - nd_prev)
    flows = fcfe_tot * (1 - mino)
    fl = flows.copy()
    fl[0] *= f26
    pv = float(np.sum(fl / (1 + KE) ** taus))
    roe_T = max(r["roe_T"], g + 0.02)
    tv = ni_c[-1] * (1 + g) * (1 - g / roe_T) / (KE - g)
    pv_tv = tv / (1 + KE) ** r["tau_T"]
    div = pr["dividends"]
    return {"value_mn": pv + pv_tv, "pv_explicit": pv, "pv_tv": pv_tv, "nd_ebitda_2026": lev,
            "nd_ebitda_2030": float(nd[-1] / eb[-1]) if eb[-1] > 0 else None,
            "fcfe": flows.tolist(), "ni_controlling_recomputed": ni_c.tolist(),
            "fcfe_over_dividends_2027_30": float(np.sum(flows[1:]) / np.sum(div[1:])) if np.sum(div[1:]) > 0 else None,
            "payout_avg_2027_30": float(np.mean(pr["payout"][1:]))}


# ------------------------------------------------------------------ (e) múltiplos justificados
def justified(r, eq_base, n_sh):
    g = r["g"]
    roe_T = max(r["roe_T"], g + 0.02)
    pbv_m = (roe_T - g) / (KE - g)
    pe_m = (1 - g / roe_T) / (KE - g)
    eps = r["eps"]
    eps_ntm = W26 * eps[0] + (1 - W26) * eps[1]
    bv = eq_base / n_sh
    return {"pbv_mult": pbv_m, "pe_mult_ntm": pe_m, "eps_ntm": eps_ntm, "bvps_base": bv, "roe_T": roe_T, "g": g,
            "pe_value_share": pe_m * eps_ntm if eps_ntm > 0 else None,
            "pbv_value_share": pbv_m * bv if bv > 0 else None}


def ke_implied_from_pe(pe, g, roe_T, trailing):
    """Ke que torna um P/L coerente com Gordon: P/L_fwd = (1 − g/ROE)/(Ke − g); trailing multiplica por (1+g)."""
    if not pe or pe <= 0:
        return None
    roe_T = max(roe_T, g + 0.02)
    return g + (1 - g / roe_T) * ((1 + g) if trailing else 1.0) / pe


# ------------------------------------------------------------------ (f) pares e históricos
def peer_set(t, info):
    me = info[t]
    if me["template"] == "holding":
        return None, []
    cands = [u for u in info if u != t and info[u]["template"] == me["template"]]
    steps = [
        ("grupo do estudo ∩ segmento B3", lambda x: x["group"] == me["group"] and x["segmento"] == me["segmento"], 2),
        ("segmento B3", lambda x: x["segmento"] == me["segmento"], 2),
        ("setor/subsetor B3", lambda x: (x["setor"], x["subsetor"]) == (me["setor"], me["subsetor"]), 2),
        ("grupo do estudo", lambda x: x["group"] == me["group"] and me["group"] in PEER_GROUP_FALLBACK, 2),
        ("segmento B3 (1 par)", lambda x: x["segmento"] == me["segmento"], 1),
    ]
    for name, pred, nmin in steps:
        s = [u for u in cands if pred(info[u])]
        if len(s) >= nmin:
            return name, sorted(s)
    return None, []


def clean_mult(k, x):
    x = fnum(x)
    lo, hi = MULT_BOUNDS[k]
    return x if x is not None and lo < x <= hi else None


def ke_adj_factor(m):
    """Gordon: múltiplo ∝ 1/(k − g). Reescala o múltiplo de mercado do par, cujo k é a TIR implícita no preço de hoje
    (DDM do estudo, i.e. o custo de capital implícito), para Ke 25%: fator = (k − g)/(Ke − g)."""
    k, g = fnum(m.get("irr_implied")), fnum(m.get("g"))
    if k is None or g is None:
        return None
    k = min(max(k, g + 0.02), 0.60)
    return (k - g) / (KE - g)


# ------------------------------------------------------------------ por empresa
def company_alt(t, r, cx):
    prem, hist = cx["prem"], cx["hist"]
    tpl = r["template"]
    sh = r["shares"]
    n_sh, unit = sh["outstanding_mn"], sh["per_unit"] or 1
    pr = r["proj"]
    g, roe_T = r["g"], r["roe_T"]
    s0 = M.yf(VAL, pr["base_date"])
    taus, tau_T = r["taus"], r["tau_T"]
    adj = prem.get("adjustments") or {}
    bal = hist["balance"]
    out = {"values_share": {}, "detail": {}, "checks": {}}
    vs = out["values_share"]
    # estudo
    for k in ("dcf", "ddm", "multiples", "pe", "ev_ebitda", "pbv"):
        if r["values_share"].get(k) is not None:
            out.setdefault("study_values_share", {})[k] = r["values_share"][k]
    # (a) RIM
    roe_lr = max(roe_T, g + 0.02)
    tv_eq = r["ddm"]["tv"]
    rim = rim_value(pr["eq_base"], pr["ni_controlling"], pr["equity"], pr["f26"], taus, s0, tau_T, KE, g, roe_lr, tv_engine=tv_eq)
    if rim:
        vs["rim"] = rim["value_mn"] / n_sh
        out["detail"]["rim"] = rim
        # checagem: DDM com distribuições totais (dividendos + recompras − emissões) do motor
        p = prem.get("projection") or {}
        dist = pr["dividends"].copy()
        if tpl != "financial":
            dist = dist + M.arr(p.get("buyback_mn")) - M.arr(p.get("equity_issuance_mn"))
        fl = dist.copy()
        fl[0] *= pr["f26"]
        ddm_tot = float(np.sum(fl / (1 + KE) ** np.asarray(taus))) + tv_eq / (1 + KE) ** tau_T
        out["checks"]["rim_engine_tv_vs_ddm_total"] = rim["value_engine_tv_mn"] / ddm_tot - 1 if ddm_tot else None
        out["checks"]["ddm_total_vs_ddm_study"] = ddm_tot / r["ddm"]["equity"] - 1 if r["ddm"]["equity"] else None
        vs["ddm_adj"] = ddm_tot / n_sh
        out["detail"]["capital_flows"] = {
            "buyback_mn_2026_30": float(np.sum(M.arr(p.get("buyback_mn")))) if tpl != "financial" else 0.0,
            "equity_issuance_mn_2026_30": float(np.sum(M.arr(p.get("equity_issuance_mn")))) if tpl != "financial" else 0.0,
            "ddm_with_buyback_issuance_share": ddm_tot / n_sh,
            "ddm_total_vs_ddm_study": out["checks"]["ddm_total_vs_ddm_study"]}
    # (e) justificados
    js = justified(r, pr["eq_base"], n_sh)
    out["detail"]["justified"] = js
    if js["pe_value_share"] is not None:
        vs["pe_just"] = js["pe_value_share"]
    if js["pbv_value_share"] is not None:
        vs["pbv_just"] = js["pbv_value_share"]
    tm = prem.get("target_multiples") or {}
    out["detail"]["ke_implied"] = {"target_pe_fwd": ke_implied_from_pe(tm.get("pe"), g, roe_T, trailing=False)}
    if tpl != "financial":
        minority_book = M.num(bal.get("minority"))
        minority_v = r["dcf"]["minority_value"]
        bridge = -pr["nd_base"] - minority_v + M.num(adj.get("non_operating_assets")) - M.num(adj.get("other_debt_like"))
        out["detail"]["bridge_mn"] = bridge
        # (b) EVA
        ev = eva_value(pr, r, minority_book, s0)
        vs["eva"] = (ev["ev_mn"] + bridge) / n_sh
        out["detail"]["eva"] = ev
        out["checks"]["eva_engine_tv_vs_dcf_ev"] = ev["ev_engine_tv_mn"] / r["dcf"]["ev"] - 1 if r["dcf"]["ev"] else None
        # (c) APV
        ap = apv_value(pr, r, prem)
        vs["apv"] = (ap["ev_mn"] + bridge) / n_sh
        out["detail"]["apv"] = ap
        # (d) FCFE
        fc = fcfe_value(pr, r, prem)
        vs["fcfe"] = fc["value_mn"] / n_sh
        out["detail"]["fcfe"] = fc
        # diagnósticos para divergências
        ni_c = pr["ni_controlling"]
        of = M.arr((prem.get("projection") or {}).get("other_financial"))
        of_at = float(np.sum(of[1:] * (1 - pr["tax_rate"][1:])))
        out["detail"]["diag"] = {
            "other_fin_over_ni_2027_30": of_at / float(np.sum(ni_c[1:])) if np.sum(ni_c[1:]) > 0 else None,
            "other_fin_mn_avg_2027_30": float(np.mean(of[1:])),
            "tv_share_dcf": r["dcf"].get("tv_share"),
            "fcff_conversion_2027_30": float(np.sum(pr["fcff"][1:]) / np.sum(ni_c[1:])) if np.sum(ni_c[1:]) > 0 else None,
            "roic_2030": float(pr["roic"][-1]) if np.isfinite(pr["roic"][-1]) else None, "roic_T": r["dcf"]["roic_T"],
            "roe_2030": float(pr["roe"][-1]) if np.isfinite(pr["roe"][-1]) else None, "roe_T": roe_T,
            "wacc": r["dcf"]["wacc"], "wd": r["dcf"]["wd"], "g": g}
    else:
        out["detail"]["diag"] = {"roe_2030": float(pr["roe"][-1]), "roe_T": roe_T, "g": g}
    return out


def market_multiples_now(r):
    return {"pe": clean_mult("pe", r.get("pe_fwd")), "ev_ebitda": clean_mult("ev_ebitda", r.get("ev_ebitda_fwd")),
            "pbv": clean_mult("pbv", r.get("pbv_now"))}


def apply_multiples(r, cx, mults, basis):
    """Valor por ação implícito por múltiplos. basis='fwd' (pares: LPA/EBITDA 2027E, VPA atual) ou 'ltm' (histórico)."""
    hist = cx["hist"]
    pr = r["proj"]
    n_sh = r["shares"]["outstanding_mn"]
    tpl = r["template"]
    bal = hist["balance"]
    ltm = hist.get("ltm") or {}
    res = {}
    bv = pr["eq_base"] / n_sh
    if basis == "fwd":
        eps = r["eps"][1]
        ebitda = pr["ebitda"][1] if tpl != "financial" else None
        nd, mino = pr.get("nd_base"), (r.get("dcf") or {}).get("minority_value")
    else:
        eps = M.num(ltm.get("ni_controlling"), M.num(hist["annual"]["FY2025"].get("ni_controlling"))) / n_sh
        ebitda = fnum(ltm.get("ebitda")) if tpl != "financial" else None
        nd, mino = fnum(bal.get("net_debt")), M.num(bal.get("minority"))
    if mults.get("pe") and eps > 0:
        res["pe"] = mults["pe"] * eps
    if mults.get("ev_ebitda") and ebitda and ebitda > 0 and nd is not None:
        res["ev_ebitda"] = (mults["ev_ebitda"] * ebitda - nd - (mino or 0.0)) / n_sh
    if mults.get("pbv") and bv > 0:
        res["pbv"] = mults["pbv"] * bv
    keys = ("pe", "pbv") if tpl == "financial" else ("pe", "ev_ebitda")
    use = [res[k] for k in keys if res.get(k) is not None]
    res["combined"] = float(np.mean(use)) if use else None
    return res


HIST_BOUNDS = {"pe": (1.0, 80.0), "pbv": (0.05, 20.0), "ev_ebitda": (1.0, 60.0)}


def hist_multiples(t):
    """Mediana de 5 anos (60 meses) da própria ação, recalculada da série `multiples_history` com filtro de qualidade:
    descarta meses com valor de mercado fora de [1/50; 50]× o atual (erros de unidade de ações na série, ex.: BBDC4 e
    TTEN3 2021–24 com P/L 0,01) e múltiplos fora de faixas plausíveis. Exige ≥ 24 meses válidos."""
    mt = load(ROOT / "data" / "market" / f"{t}.json")
    mh = mt.get("multiples_history") or {}
    st = mh.get("stats") or {}
    ser = mh.get("series") or []
    live = [x for x in ser if x.get("live")]
    hist = [x for x in ser if not x.get("live")][-60:]
    ref = (live[-1] if live else (hist[-1] if hist else {})).get("mcap")
    out = {"source_stats_median": {k: fnum((st.get(f"{k}_5y") or {}).get("median")) for k in ("pe", "ev_ebitda", "pbv")}}
    for k in ("pe", "ev_ebitda", "pbv"):
        lo, hi = HIST_BOUNDS[k]
        vals = [x[k] for x in hist if x.get(k) is not None and lo <= x[k] <= hi and x.get("mcap") and ref
                and ref / 50 <= x["mcap"] <= ref * 50]
        out[f"{k}_n"] = len(vals)
        out[f"{k}_current"] = fnum((st.get(f"{k}_5y") or {}).get("current"))
        if len(vals) >= 24:
            out[k] = float(np.median(vals))
            out[f"{k}_mean"] = float(np.mean(vals))
    out["months_dropped_quality"] = sum(1 for x in hist if not (x.get("mcap") and ref and ref / 50 <= x["mcap"] <= ref * 50))
    return out, mt.get("sector") or {}


# ------------------------------------------------------------------ diagnóstico de divergências
def dispersion(vals, keys):
    xs = [vals.get(k) for k in keys if fnum(vals.get(k)) is not None]
    p = [x for x in xs if x > 0]
    res = {"n": len(xs), "n_nonpositive": len(xs) - len(p)}
    if len(p) >= 2:
        lg = np.log(p)
        res.update({"std_log": float(np.std(lg)), "max_over_min": float(max(p) / min(p)),
                    "cv": float(np.std(p) / np.mean(p)), "median": float(np.median(p))})
    return res


def reasons_for(t, vals, det, diag, tpl):
    """Causas prováveis das divergências entre métodos (regras com magnitude)."""
    rs = []
    intr = [vals.get(k) for k in INTRINSIC if pos(vals.get(k))]
    mkt = [vals.get(k) for k in MARKET if pos(vals.get(k))]
    if intr and mkt:
        ratio = float(np.median(mkt) / np.median(intr))
        if ratio > 1.8:
            ki = (det.get("ke_implied") or {})
            parts = []
            if ki.get("hist_pe_ltm"):
                parts.append(f"P/L histórico embute Ke ≈ {ki['hist_pe_ltm']*100:.0f}%")
            if ki.get("target_pe_fwd"):
                parts.append(f"P/L-alvo embute Ke ≈ {ki['target_pe_fwd']*100:.0f}%")
            rs.append((math.log(ratio), f"múltiplos de mercado {br(ratio, 1)}× a mediana intrínseca"
                       + (f" ({'; '.join(parts)} vs 25%)" if parts else "")))
        elif ratio < 0.55:
            rs.append((-math.log(ratio), f"múltiplos de mercado {br(ratio)}× a mediana intrínseca (pares/histórico deprimidos)"))
    dcf, rim, ddm, fcfe, apv, eva = (vals.get(k) for k in ("dcf", "rim", "ddm", "fcfe", "apv", "eva"))
    if tpl != "financial":
        conv = diag.get("fcff_conversion_2027_30")
        if pos(rim) and dcf is not None and conv is not None and dcf < 0.6 * rim and conv < 0.7:
            rs.append((math.log(rim / max(dcf, 0.05 * rim)), f"FCFF baixo frente ao lucro (FCFF/LL 2027–30 = {conv*100:.0f}%: capex/ΔCG) → DCF ≪ métodos de lucro"))
        if pos(rim) and dcf is not None and conv is not None and dcf > 1.6 * rim and conv > 1.1:
            rs.append((math.log(dcf / rim), f"FCFF acima do lucro (FCFF/LL 2027–30 = {conv*100:.0f}%) → DCF ≫ RIM/DDM"))
        ofs = diag.get("other_fin_over_ni_2027_30")
        if ofs is not None and abs(ofs) > 0.15 and pos(dcf) and pos(fcfe) and abs(math.log(dcf / fcfe)) > 0.15:
            rs.append((abs(math.log(dcf / fcfe)) + 0.1, f"other_financial (R$ {br(diag.get('other_fin_mn_avg_2027_30', 0), 0)} mi/ano, {ofs*100:+.0f}% do LL) "
                       "entra no LL (DDM/RIM/FCFE) mas não no FCFF do DCF"))
        if dcf is not None and dcf <= 0 and any(pos(x) for x in (ddm, fcfe, rim)):
            rs.append((1.5, f"EV a WACC {diag.get('wacc', 0)*100:.0f}% abaixo da dívida (ROIC 2030 {(diag.get('roic_2030') or 0)*100:.0f}%): DCF/APV ≤ 0, "
                       "mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada"))
        tvs = diag.get("tv_share_dcf")
        if tvs is not None and tvs > 0.75:
            rs.append((0.3 + tvs - 0.75, f"DCF dependente da perpetuidade (TV = {tvs*100:.0f}% do EV"
                       + (": fluxos explícitos negativos)" if tvs > 1 else ")")))
        if pos(apv) and pos(dcf) and abs(math.log(apv / dcf)) > 0.2:
            ap = det.get("apv") or {}
            nd30 = ap.get("nd_ebitda_2030")
            rs.append((abs(math.log(apv / dcf)), f"APV/DCF = {br(apv/dcf)}: dívida projetada (DL/EBITDA {br(ap.get('nd_ebitda_base'), 1)}x → "
                       f"{br(nd30, 1)}x em 2030) ≠ peso-alvo wd = {ap.get('wd', 0)*100:.0f}% do WACC"))
        if pos(eva) and pos(dcf) and abs(math.log(eva / dcf)) > 0.2:
            e = det.get("eva") or {}
            rs.append((abs(math.log(eva / dcf)), f"EVA/DCF = {br(eva/dcf)}: ROIC 2031 (continuação) {e.get('roic_2031_start', 0)*100:.0f}% converge ao ROIC terminal "
                       f"{e.get('roic_lr', 0)*100:.0f}% (WACC {e.get('wacc', 0)*100:.0f}%) em vez de persistir"))
        if pos(fcfe) and pos(ddm) and fcfe / ddm > 1.3:
            fc = det.get("fcfe") or {}
            rs.append((math.log(fcfe / ddm), f"FCFE/DDM = {br(fcfe/ddm)}: payout médio {fc.get('payout_avg_2027_30', 0)*100:.0f}% retém caixa que rende Kd·(1−t) < Ke"))
        if pos(fcfe) and pos(ddm) and fcfe / ddm < 0.7:
            rs.append((math.log(ddm / fcfe), f"FCFE/DDM = {br(fcfe/ddm)}: dividendos projetados acima do FCFE (desalavancagem cessa ou dívida financia o payout)"))
    cf = det.get("capital_flows") or {}
    dch = cf.get("ddm_total_vs_ddm_study")
    if dch is not None and abs(dch) > 0.1:
        what = (f"emissão de ações de R$ {br(cf.get('equity_issuance_mn_2026_30'), 0)} mi" if (cf.get("equity_issuance_mn_2026_30") or 0) > 0
                else f"recompra de R$ {br(cf.get('buyback_mn_2026_30'), 0)} mi")
        rs.append((abs(math.log(1 + dch)) + 0.2, f"DDM do estudo ignora a {what} projetada (dividendo cresce com o capital novo, ações fixas): "
                   f"com ela o DDM seria {pc(dch)}; o RIM (clean surplus) já a desconta"))
    rr = det.get("rim") or {}
    if pos(rim) and pos(ddm) and rr.get("fade_applied") and abs(math.log(rim / ddm)) > 0.2:
        rs.append((abs(math.log(rim / ddm)), f"RIM/DDM = {br(rim/ddm)}: ROE de 2031 na continuação ({rr.get('roe_2031_start', 0)*100:.0f}%) converge ao ROE terminal {rr.get('roe_lr', 0)*100:.0f}% em 10 anos"))
    neg = [LABEL[k] for k in ALL_METHODS if fnum(vals.get(k)) is not None and vals[k] <= 0]
    if neg and not (fnum(dcf) is not None and dcf <= 0):
        rs.append((1.0, "valor ≤ 0 em: " + ", ".join(neg)))
    rs.sort(key=lambda x: -x[0])
    return [s for _, s in rs[:3]]


# ------------------------------------------------------------------ principal
def main():
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    cov_doc = load(ROOT / "research" / "_coverage.json")
    cov = cov_doc["coverage"]
    mk = load(ROOT / "data" / "market" / "_market.json")
    overview = load(ROOT / "data" / "app" / "overview.json")
    ov_rows = {x["ticker"]: x for x in overview["companies"]}
    opp7 = list(overview.get("opportunities") or [])
    seeded = seed_missing_quotes(cov)
    models, ctx = run_engine(cov)
    tickers = [c["ticker"] for c in cov]

    # metadados, múltiplos de mercado atuais e históricos
    info, cur_mult, hist_m = {}, {}, {}
    for t in tickers:
        r, cx = models[t], ctx[t]
        hm, sec = hist_multiples(t)
        sec = sec or mk["sectors"].get(t) or {}
        info[t] = {"group": cx["cov"]["group"], "template": r["template"], "setor": sec.get("setor"),
                   "subsetor": sec.get("subsetor"), "segmento": sec.get("segmento")}
        hist_m[t] = hm
        if r["template"] != "holding":
            cur_mult[t] = market_multiples_now(r)

    comp = {}
    for t in tickers:
        r, cx = models[t], ctx[t]
        tpl = r["template"]
        unit = (r.get("shares") or {}).get("per_unit") or 1
        price = cx["price"]
        cls = classify(t, tpl, info[t]["group"])
        row = {"ticker": t, "name": cx["prem"].get("name"), "group": info[t]["group"], "class": cls, "template": tpl,
               "sector": {k: info[t][k] for k in ("setor", "subsetor", "segmento")}, "price": price, "per_unit": unit,
               "study": {"fair_value": r.get("fair_value"), "upside": r.get("upside"), "weights": r.get("weights"),
                         "irr_implied": r.get("irr_implied")},
               "values": {}, "detail": {}, "checks": {}}
        if tpl == "holding":
            row["values"]["sotp"] = r["values"]["sotp"]
            row["values"]["nav_market"] = r["values"]["nav_market"]
            hm = hist_m[t]
            n_sh = r["shares"]["outstanding_mn"]
            hh = cx["hist"]
            bv = M.num(hh["balance"].get("equity_controlling")) / n_sh
            eps_ltm = M.num((hh.get("ltm") or {}).get("ni_controlling")) / n_sh
            hv = {}
            if hm.get("pbv") and bv > 0:
                hv["pbv"] = hm["pbv"] * bv * unit
            if hm.get("pe") and eps_ltm > 0:
                hv["pe"] = hm["pe"] * eps_ltm * unit
            row["detail"]["hist"] = {"multiples_5y_median": hm, "implied_per_unit": hv}
            if hv:
                row["values"]["hist"] = float(np.mean(list(hv.values())))
            row["detail"]["sotp"] = {"nav_fair": r["nav_fair"], "nav_mkt": r["nav_mkt"], "holding_net_debt": r["holding_net_debt"],
                                     "holding_cost_capitalized": r["holding_cost_capitalized"],
                                     "discount_to_nav_mkt": r.get("discount_to_nav_mkt")}
            comp[t] = row
            continue
        a = company_alt(t, r, cx)
        for k, v in a["values_share"].items():
            row["values"][k] = v * unit if v is not None else None
        for k in ("dcf", "ddm", "multiples"):
            if r["values_share"].get(k) is not None:
                row["values"][k] = r["values_share"][k] * unit
        row["study"]["values"] = {k: (v * unit if v is not None else None) for k, v in r["values_share"].items()}
        row["detail"].update(a["detail"])
        row["checks"].update(a["checks"])
        # (f) pares
        pname, peers = peer_set(t, info)
        pm, pm_adj = {}, {}
        for k in ("pe", "ev_ebitda", "pbv"):
            pm[k] = median([cur_mult[u][k] for u in peers if u in cur_mult])
            adj = []
            for u in peers:
                x, fac = (cur_mult.get(u) or {}).get(k), ke_adj_factor(models[u])
                if x is not None and fac is not None:
                    adj.append(x * fac)
            pm_adj[k] = median(adj)
        pv = apply_multiples(r, cx, pm, "fwd") if peers else {}
        # ajuste Gordon só vale para múltiplos de equity (P/L, P/VP); EV/EBITDA não escala com (k − g) do acionista
        pva = apply_multiples(r, cx, {"pe": pm_adj.get("pe"), "pbv": pm_adj.get("pbv") if r["template"] == "financial" else None}, "fwd") if peers else {}
        row["detail"]["peers"] = {"rule": pname, "peers": peers, "median_multiples": pm, "median_multiples_ke25": pm_adj,
                                  "peer_irr_implied": {u: models[u].get("irr_implied") for u in peers},
                                  "own_multiples_now": cur_mult.get(t),
                                  "implied_per_unit": {k: (v * unit if v is not None else None) for k, v in pv.items()},
                                  "implied_per_unit_ke25": {k: (v * unit if v is not None else None) for k, v in pva.items()}}
        if pv.get("combined") is not None:
            row["values"]["peers"] = pv["combined"] * unit
        if pva.get("combined") is not None:
            row["values"]["peers_adj"] = pva["combined"] * unit
        # (f) histórico próprio
        hm = hist_m[t]
        hvals = apply_multiples(r, cx, {k: hm.get(k) for k in ("pe", "ev_ebitda", "pbv")}, "ltm") if hm else {}
        row["detail"]["hist"] = {"multiples_5y_median": hm,
                                 "implied_per_unit": {k: (v * unit if v is not None else None) for k, v in hvals.items()}}
        if hvals.get("combined") is not None:
            row["values"]["hist"] = hvals["combined"] * unit
        row["detail"]["ke_implied"]["hist_pe_ltm"] = ke_implied_from_pe(hm.get("pe"), r["g"], r["roe_T"], trailing=True)
        row["detail"]["ke_implied"]["market_irr_today"] = r.get("irr_implied")
        comp[t] = row

    # ---------------------------------------------------------------- pesos propostos (e alternativos)
    def weights_for(t, scheme):
        row = comp[t]
        cls = row["class"]
        if scheme == "estudo":
            if row["template"] == "holding":
                return {"sotp": 1.0}
            return row["study"]["weights"]
        if scheme == "estudo_sem_multiplos":
            if row["template"] == "holding":
                return {"sotp_new": 1.0}
            return {k: v for k, v in row["study"]["weights"].items() if k != "multiples"}
        if scheme == "proposto":
            return WEIGHTS[cls]
        if scheme == "proposto_sem_mercado":
            w = {k: v for k, v in WEIGHTS[cls].items() if k not in MARKET + RELATIVE_ADJ}
            return w or WEIGHTS[cls]
        if scheme == "igual_todos":
            if row["template"] == "holding":
                return {"sotp_new": 1.0}
            return {k: 1.0 for k in ALL_METHODS}
        raise ValueError(scheme)

    schemes = ["estudo", "estudo_sem_multiplos", "proposto", "proposto_sem_mercado", "igual_todos"]
    fair = {s: {} for s in schemes}
    used_w = {s: {} for s in schemes}
    # 1) não-holdings
    for s in schemes:
        for t in tickers:
            if comp[t]["template"] == "holding":
                continue
            if s == "estudo":
                fair[s][t] = comp[t]["study"]["fair_value"]
                used_w[s][t] = comp[t]["study"]["weights"]
            else:
                fair[s][t], used_w[s][t] = blend(comp[t]["values"], weights_for(t, s))
    # 2) holdings: SOTP com as controladas no valor justo do esquema
    for s in schemes:
        for t in tickers:
            if comp[t]["template"] != "holding":
                continue
            if s == "estudo":
                fair[s][t] = comp[t]["study"]["fair_value"]
                used_w[s][t] = {"sotp": 1.0}
                continue
            mods = {}
            for u, m in models.items():
                if u in fair[s] and comp[u]["template"] != "holding" and fair[s][u] is not None:
                    unit_u = m["shares"]["per_unit"] or 1
                    mods[u] = {**m, "fair_value": fair[s][u], "fair_value_share": fair[s][u] / unit_u}
                else:
                    mods[u] = m
            rh = M.value_holding(ctx[t]["prem"], ctx[t]["hist"], mods, price=ctx[t]["price"])
            comp[t]["values"][f"sotp_{s}"] = rh["fair_value"]
            if s == "proposto":
                comp[t]["values"]["sotp_new"] = rh["fair_value"]
                comp[t]["detail"]["sotp"]["components_new"] = [
                    {"name": c["name"], "ticker": c["ticker"], "stake": c["stake"], "method": c["method"],
                     "value_fair_100": c["value_fair_100"]} for c in rh["components"]]
            fair[s][t], used_w[s][t] = rh["fair_value"], {"sotp_new": 1.0}

    # ---------------------------------------------------------------- probabilidade (Monte Carlo do motor reescalado) e escore
    stored = {t: load(ROOT / "data" / "model" / f"{t}.json") for t in tickers}

    def prob_mc(t, fv):
        m = stored[t]
        mc = m.get("monte_carlo") or {}
        smp = np.array(mc.get("samples") or [], dtype=float)
        price = comp[t]["price"]
        if not len(smp) or not m.get("fair_value") or fv is None or not price:
            return None
        base_fv = comp[t]["study"]["fair_value"]
        p_ref = mc.get("prob_above_price")
        # números aleatórios comuns: P(estudo) gravada + variação da amostra quando o valor justo é reescalado
        p_s = float(np.mean(smp * (fv / m["fair_value"]) > price))
        p_b = float(np.mean(smp * (base_fv / m["fair_value"]) > price))
        if p_ref is None:
            return p_s
        return float(min(1.0, max(0.0, p_ref + p_s - p_b)))

    res = {s: {} for s in schemes}
    for s in schemes:
        rows = []
        for t in tickers:
            fv = fair[s][t]
            price = comp[t]["price"]
            up = fv / price - 1 if fv is not None and price else None
            rows.append({"ticker": t, "fair": fv, "upside": up, "irr": comp[t]["study"]["irr_implied"],
                         "prob": prob_mc(t, fv) if comp[t]["template"] != "holding" else None})
        z_val = zscore([x["irr"] for x in rows])
        z_up = zscore([x["upside"] for x in rows])
        z_p = zscore([x["prob"] for x in rows])
        for i, x in enumerate(rows):
            sc = (ov_rows.get(x["ticker"]) or {}).get("scores") or {}
            f = {"valor": z_val[i], "upside": z_up[i], "qualidade": sc.get("qualidade"), "solidez": sc.get("solidez"),
                 "sobrerreacao": sc.get("sobrerreacao"), "probabilidade": z_p[i]}
            tot = sum(FACTOR_W[k] for k, v in f.items() if v is not None)
            x["score"] = sum(FACTOR_W[k] * v for k, v in f.items() if v is not None) / tot if tot else None
        for key, rk in (("score", "rank_score"), ("upside", "rank_upside")):
            ranked = sorted([x for x in rows if x[key] is not None], key=lambda x: -x[key])
            for i, x in enumerate(ranked):
                x[rk] = i + 1

        def low_conf(t):
            c = (ctx[t]["prem"].get("confidence") or "").lower().strip()
            return c.startswith("baixa") and not c.startswith("baixa-m") and not c.startswith("baixa a m")

        for x in rows:
            ov = ov_rows.get(x["ticker"]) or {}
            x["passes_rule"] = bool((x["irr"] or -1) >= 0.20 and (x["prob"] or 0) >= 0.45
                                    and ((ov.get("altman") or {}).get("zone") != "risco") and not low_conf(x["ticker"]))
        res[s] = {x["ticker"]: x for x in rows}

    # ---------------------------------------------------------------- viés sistemático e dispersão
    bias = {}
    for k in ALL_METHODS + ["sotp_new"]:
        rr, rd, ups, above = [], [], [], 0
        for t in tickers:
            v = fnum(comp[t]["values"].get(k))
            fs = pos(comp[t]["study"]["fair_value"])
            if v is None or fs is None:
                continue
            rr.append(v / fs)
            above += v > fs
            dcf = pos(comp[t]["values"].get("dcf"))
            if dcf and k != "dcf":
                rd.append(v / dcf)
            if comp[t]["price"]:
                ups.append(v / comp[t]["price"] - 1)
        if not rr:
            continue
        lr = np.log([max(x, 1e-3) for x in rr])
        bias[k] = {"label": LABEL[k], "n": len(rr), "median_vs_study_fair": float(np.median(rr)) - 1,
                   "p25_vs_study_fair": float(np.percentile(rr, 25)) - 1, "p75_vs_study_fair": float(np.percentile(rr, 75)) - 1,
                   "geo_mean_vs_study_fair": float(np.exp(np.mean(lr))) - 1,
                   "median_vs_dcf": (float(np.median(rd)) - 1) if rd else None,
                   "share_above_study_fair": above / len(rr), "median_upside_vs_price": float(np.median(ups)) if ups else None}

    for t in tickers:
        row = comp[t]
        if row["template"] == "holding":
            continue
        v = row["values"]
        row["dispersion"] = {"all": dispersion(v, ALL_METHODS), "intrinsic": dispersion(v, INTRINSIC),
                             "market": dispersion(v, MARKET)}
        mi, mm = row["dispersion"]["intrinsic"].get("median"), row["dispersion"]["market"].get("median")
        row["dispersion"]["market_over_intrinsic"] = mm / mi if mi and mm else None
        row["divergence_reasons"] = reasons_for(t, v, row["detail"], row["detail"].get("diag") or {}, row["template"])
    div_rank = sorted([t for t in tickers if comp[t]["template"] != "holding" and comp[t]["dispersion"]["all"].get("std_log") is not None],
                      key=lambda t: -comp[t]["dispersion"]["all"]["std_log"])

    # participação da perna de múltiplos-alvo no valor justo do estudo
    for t in tickers:
        row = comp[t]
        if row["template"] == "holding":
            continue
        w = row["study"]["weights"] or {}
        parts = {k: wk * max(0.0, row["values"][k]) for k, wk in w.items() if fnum(row["values"].get(k)) is not None}
        tot = sum(parts.values())
        row["study"]["multiples_share_of_fair"] = parts.get("multiples", 0.0) / tot if tot else None

    # ---------------------------------------------------------------- consolidação por empresa
    for t in tickers:
        row = comp[t]
        row["schemes"] = {}
        for s in schemes:
            x = res[s][t]
            row["schemes"][s] = {"fair_value": x["fair"], "upside": x["upside"], "weights_used": used_w[s].get(t),
                                 "prob_mc": x["prob"], "score": x["score"], "rank_score": x.get("rank_score"),
                                 "rank_upside": x.get("rank_upside"), "passes_opportunity_rule": x["passes_rule"]}
        row["proposed"] = row["schemes"]["proposto"]

    # ---------------------------------------------------------------- resumo dos rankings / oportunidades
    def ranking_summary(s):
        a = [res["estudo"][t]["score"] for t in tickers]
        b = [res[s][t]["score"] for t in tickers]
        ua = [res["estudo"][t]["upside"] for t in tickers]
        ub = [res[s][t]["upside"] for t in tickers]
        top_s = [x["ticker"] for x in sorted(res[s].values(), key=lambda x: -(x["score"] if x["score"] is not None else -9))]
        top_u = [x["ticker"] for x in sorted(res[s].values(), key=lambda x: -(x["upside"] if x["upside"] is not None else -9))]
        rule = [t for t in top_s if res[s][t]["passes_rule"]][:8]
        return {"spearman_score_vs_study": spearman(a, b), "spearman_upside_vs_study": spearman(ua, ub),
                "median_upside": float(np.median([x for x in ub if x is not None])),
                "n_upside_positive": int(sum(1 for x in ub if x is not None and x > 0)),
                "top10_score": top_s[:10], "top10_upside": top_u[:10], "opportunities_by_rule": rule,
                "frozen7": {t: {"rank_score": res[s][t].get("rank_score"), "rank_upside": res[s][t].get("rank_upside"),
                                "upside": res[s][t]["upside"], "fair_value": res[s][t]["fair"], "prob_mc": res[s][t]["prob"],
                                "passes_rule": res[s][t]["passes_rule"]} for t in opp7}}

    rankings = {s: ranking_summary(s) for s in schemes}
    class_members = {}
    for t in tickers:
        class_members.setdefault(comp[t]["class"], []).append(t)
    class_effect = {}
    for cls, ts in class_members.items():
        d = [comp[t]["proposed"]["fair_value"] / comp[t]["study"]["fair_value"] - 1 for t in ts
             if pos(comp[t]["study"]["fair_value"]) and comp[t]["proposed"]["fair_value"] is not None]
        class_effect[cls] = {"n": len(ts), "median_change_fair": float(np.median(d)) if d else None,
                             "median_upside_study": float(np.median([comp[t]["study"]["upside"] for t in ts if comp[t]["study"]["upside"] is not None])),
                             "median_upside_proposed": float(np.median([comp[t]["proposed"]["upside"] for t in ts if comp[t]["proposed"]["upside"] is not None]))}
    checks = {
        "quotes_seeded_for_holdings": seeded,
        "rim_engine_tv_vs_ddm_total_max_abs_industrial": max(abs(comp[t]["checks"]["rim_engine_tv_vs_ddm_total"]) for t in tickers
                                                             if comp[t]["template"] == "industrial" and comp[t]["checks"].get("rim_engine_tv_vs_ddm_total") is not None),
        "rim_engine_tv_vs_ddm_total_banks": {t: comp[t]["checks"].get("rim_engine_tv_vs_ddm_total") for t in tickers if comp[t]["template"] == "financial"},
        "eva_engine_tv_vs_dcf_ev_max_abs": max(abs(comp[t]["checks"]["eva_engine_tv_vs_dcf_ev"]) for t in tickers
                                               if comp[t]["checks"].get("eva_engine_tv_vs_dcf_ev") is not None),
        "stored_vs_engine_fair": {t: (stored[t].get("fair_value") / comp[t]["study"]["fair_value"] - 1)
                                  for t in tickers if pos(stored[t].get("fair_value")) and pos(comp[t]["study"]["fair_value"])
                                  and abs(stored[t]["fair_value"] / comp[t]["study"]["fair_value"] - 1) > 0.001},
    }
    nh = [t for t in tickers if comp[t]["template"] != "holding"]

    def med_ratio(k, base):
        rr = [comp[t]["values"][k] / comp[t]["values"][base] for t in nh
              if pos(comp[t]["values"].get(k)) and pos(comp[t]["values"].get(base))]
        return {"median": float(np.median(rr)) if rr else None, "n": len(rr)}

    def med_of(xs):
        xs = [x for x in xs if x is not None]
        return float(np.median(xs)) if xs else None

    stats = {
        "agreement_vs_ddm": {k: med_ratio(k, "ddm") for k in ("rim", "fcfe", "pe_just", "pbv_just", "peers_adj", "dcf", "multiples", "peers", "hist")},
        "agreement_vs_dcf": {k: med_ratio(k, "dcf") for k in ("apv", "eva", "fcfe", "rim", "multiples", "peers", "hist")},
        "multiples_share_of_study_fair": {
            "all": med_of([comp[t]["study"].get("multiples_share_of_fair") for t in nh]),
            "industrial": med_of([comp[t]["study"].get("multiples_share_of_fair") for t in nh if comp[t]["template"] == "industrial"]),
            "financial": med_of([comp[t]["study"].get("multiples_share_of_fair") for t in nh if comp[t]["template"] == "financial"])},
        "dcf_nonpositive": [t for t in nh if comp[t]["template"] == "industrial" and (fnum(comp[t]["values"].get("dcf")) or 0) <= 0],
        "apv_nonpositive": [t for t in nh if comp[t]["template"] == "industrial" and (fnum(comp[t]["values"].get("apv")) or 0) <= 0],
        "dcf_nonpositive_equity_positive": [t for t in nh if comp[t]["template"] == "industrial" and (fnum(comp[t]["values"].get("dcf")) or 0) <= 0
                                            and any(pos(comp[t]["values"].get(k)) for k in ("ddm", "fcfe", "rim"))],
        "ke_implied_median": {
            "market_irr_today": med_of([comp[t]["detail"]["ke_implied"].get("market_irr_today") for t in nh]),
            "target_pe": med_of([comp[t]["detail"]["ke_implied"].get("target_pe_fwd") for t in nh]),
            "hist_pe": med_of([comp[t]["detail"]["ke_implied"].get("hist_pe_ltm") for t in nh])},
        "fade_applied": {"rim": [t for t in nh if (comp[t]["detail"].get("rim") or {}).get("fade_applied")],
                         "eva": [t for t in nh if (comp[t]["detail"].get("eva") or {}).get("fade_applied")]},
        "other_financial_material": {t: comp[t]["detail"]["diag"].get("other_fin_over_ni_2027_30") for t in nh
                                     if comp[t]["template"] == "industrial" and abs(comp[t]["detail"]["diag"].get("other_fin_over_ni_2027_30") or 0) > 0.15},
        "median_change_fair_proposed": med_of([comp[t]["proposed"]["fair_value"] / comp[t]["study"]["fair_value"] - 1 for t in tickers
                                               if pos(comp[t]["study"]["fair_value"]) and comp[t]["proposed"]["fair_value"] is not None]),
        "hist_series_quality_dropped": {t: comp[t]["detail"]["hist"]["multiples_5y_median"].get("months_dropped_quality") for t in nh
                                        if (comp[t]["detail"]["hist"]["multiples_5y_median"].get("months_dropped_quality") or 0) >= 6},
        "rank_moves_upside": sorted([(t, (res["estudo"][t].get("rank_upside") or 0) - (res["proposto"][t].get("rank_upside") or 0)) for t in tickers],
                                    key=lambda x: -abs(x[1]))[:10],
    }
    doc = {
        "generated_at": datetime.now().isoformat(timespec="seconds"), "valuation_date": VAL.isoformat(), "ke": KE, "stats": stats,
        "params": {"fade_years": FADE_YEARS, "roe_fade_target": "terminal.roe das premissas (roe_T do motor)",
                   "roic_fade_target": "terminal.roic (roic_T do motor)", "tax_shield_rate": f"{TAX_STAT} se alíquota efetiva ≥ {TS_MIN_EFFECTIVE}, senão a efetiva",
                   "ku": "Harris–Pringle: (1 − wd)·Ke + wd·Kd, wd e Kd do WACC do estudo (Kd 'grossed-up' de RET → custo da DL projetado)",
                   "fcfe_debt_policy": "DL cresce com a receita a partir da DL do balanço-base (estrutura de capital constante em relação ao porte); caixa líquido mantido constante",
                   "eps_ntm_weight_2026": W26, "peer_multiples": "P/L 2027E, EV/EBITDA 2027E e P/VP atuais (foto do estudo), mediana",
                   "hist_multiples": "mediana 5 anos LTM (multiples_history.stats *_5y), n ≥ 24 meses",
                   "multiple_bounds": MULT_BOUNDS, "prob_mc": "P(valor > preço) do Monte Carlo do motor, amostra reescalada pelo novo valor justo (números aleatórios comuns)",
                   "score": "escore multifator do build.py (mesmos pesos); qualidade/solidez/sobrerreação do overview; valor, upside e probabilidade recalculados"},
        "methods": LABEL, "weights_by_class": WEIGHTS, "class_label": CLASS_LABEL, "class_rationale": CLASS_WHY,
        "class_members": class_members, "class_effect": class_effect, "bias": bias,
        "divergence_top": [{"ticker": t, "std_log": comp[t]["dispersion"]["all"]["std_log"],
                            "max_over_min": comp[t]["dispersion"]["all"]["max_over_min"],
                            "market_over_intrinsic": comp[t]["dispersion"]["market_over_intrinsic"],
                            "reasons": comp[t]["divergence_reasons"]} for t in div_rank[:15]],
        "rankings": rankings, "opportunities_frozen": opp7, "checks": checks, "companies": comp,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as fh:
        json.dump(M.jsonable(doc), fh, ensure_ascii=False, indent=1)
    write_md(doc, tickers, div_rank)
    print(f"ok: {OUT_JSON.relative_to(ROOT)} e {OUT_MD.relative_to(ROOT)} | empresas {len(tickers)}")
    for s in schemes:
        rs = rankings[s]
        print(f"  {s:22s} upside mediano {rs['median_upside']*100:6.1f}% | upside>0: {rs['n_upside_positive']:2d} | "
              f"Spearman escore {rs['spearman_score_vs_study']:.2f} | regra: {rs['opportunities_by_rule']}")
    print("  checagens:", {k: v for k, v in checks.items() if k != "stored_vs_engine_fair"}, "| defasagem gravado×motor:", checks["stored_vs_engine_fair"])


# ------------------------------------------------------------------ relatório
def br(x, d=2):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return "—"
    s = f"{x:,.{d}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def pc(x, d=0, sign=True):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return "—"
    s = f"{x*100:+.{d}f}%" if sign else f"{x*100:.{d}f}%"
    return s.replace(".", ",")


def write_md(doc, tickers, div_rank):
    comp, rk, bias, st = doc["companies"], doc["rankings"], doc["bias"], doc["stats"]
    rs, rp = rk["estudo"], rk["proposto"]
    L = []
    A = L.append
    ag, agd = st["agreement_vs_ddm"], st["agreement_vs_dcf"]
    ki = st["ke_implied_median"]
    ce = doc["class_effect"]
    opp = doc["opportunities_frozen"]
    keep_s = [t for t in opp if rs["frozen7"][t]["passes_rule"]]
    keep_p = [t for t in opp if rp["frozen7"][t]["passes_rule"]]
    lost_s = [t for t in opp if t not in keep_s]
    lost_p = [t for t in keep_s if t not in keep_p]
    new_p = [t for t in rp["opportunities_by_rule"] if t not in opp]

    def x_(v, d=2):
        return f"{br(v, d)}×" if v is not None else "—"

    A("# Métodos alternativos de valuation e novos pesos (Ke 25%)")
    A("")
    A(f"*Gerado em {doc['generated_at']} por `pipeline/tests/alt_methods.py`. Motor `pipeline/model.py` importado sem alterações, "
      "premissas lidas de `research/` no momento da execução (os revisores seguem ajustando; rode de novo para atualizar), preços da "
      "foto do estudo. Valores por ação/unit, comparáveis ao preço. Dados completos em `data/tests/alt_methods.json`.*")
    A("")
    A("## Resumo")
    A("")
    A(f"1. **Os métodos intrínsecos alternativos confirmam DCF e DDM.** Mediana por empresa em relação ao DDM: RIM {x_(ag['rim']['median'])}, "
      f"P/L justificado {x_(ag['pe_just']['median'])}, P/VP justificado {x_(ag['pbv_just']['median'])}, FCFE {x_(ag['fcfe']['median'])}, "
      f"pares ajustados ao Ke {x_(ag['peers_adj']['median'])}. Em relação ao DCF: APV {x_(agd['apv']['median'])} e EVA {x_(agd['eva']['median'])}. "
      f"RIM ≡ DDM e EVA ≡ DCF são identidades quando a perpetuidade é a mesma (erro máximo {doc['checks']['rim_engine_tv_vs_ddm_total_max_abs_industrial']:.0e} e "
      f"{doc['checks']['eva_engine_tv_vs_dcf_ev_max_abs']:.0e}, relativo). As diferenças vêm só do fade do retorno excedente "
      f"(RIM em {len(st['fade_applied']['rim'])} empresas, EVA em {len(st['fade_applied']['eva'])}) e da política de dívida (APV e FCFE).")
    A(f"2. **O viés está nos métodos de mercado.** Na mediana, os múltiplos-alvo do estudo ficam {x_(agd['multiples']['median'])} o DCF, os pares "
      f"{x_(agd['peers']['median'])} e a mediana histórica de 5 anos {x_(agd['hist']['median'])}. Eles embutem Ke de cerca de {pc(ki['target_pe'], 0, False)} "
      f"(P/L-alvo) e {pc(ki['hist_pe'], 0, False)} (P/L histórico), e o preço de hoje embute uma TIR de dono mediana de {pc(ki['market_irr_today'], 0, False)}: "
      f"nenhum deles está em 25%. Com 25% de peso, a perna de múltiplos-alvo responde, na mediana, por {pc(st['multiples_share_of_study_fair']['industrial'], 0, False)} "
      f"do valor justo industrial do estudo. Nos bancos, com 50% de peso, responde por {pc(st['multiples_share_of_study_fair']['financial'], 0, False)}.")
    A(f"3. **Onde e por que divergem.** (i) Alavancagem com Ke fixo: {len(st['dcf_nonpositive'])} das 53 industriais têm DCF ≤ 0 (EV abaixo da dívida, com "
      f"ROIC < WACC), mas {len(st['dcf_nonpositive_equity_positive'])} delas têm DDM/FCFE/RIM > 0. Um Ke de 25% que não sobe com a alavancagem viola "
      f"Modigliani-Miller, e o acionista tem responsabilidade limitada (utilities, concessões, locadoras, MGLU3, ASAI3). "
      f"(ii) `other_financial` entra no lucro, mas não no FCFF ({', '.join(st['other_financial_material'])}): no caso de TEND3/PLPL3/MRVE3, "
      f"juros capitalizados e custo de cessões inflam o DCF frente ao RIM/FCFE. (iii) Payout baixo: o FCFE supera o DDM em "
      f"{pc(ag['fcfe']['median'] - 1 if ag['fcfe']['median'] else None)} na mediana, porque o caixa retido rende Kd·(1−t) < Ke. "
      f"(iv) PL com ágio (HAPV3, AZZA3, ALOS3) tira o sentido do P/VP. Detalhes por empresa na tabela de divergências.")
    A(f"4. **Pesos recomendados.** Cada classe usa os métodos coerentes com Ke 25% (tabela abaixo): RIM nos bancos e incorporadoras, APV/DCF "
      f"mais o lado do acionista em infraestrutura, EVA/APV em locação, e DCF com pares ajustados ao Ke no varejo. Múltiplos de mercado brutos "
      f"(alvo, pares e histórico) ficam como referência relativa e saem do valor justo.")
    A(f"5. **Efeito.** O valor justo muda {pc(st['median_change_fair_proposed'])} na mediana (infraestrutura {pc(ce['infra_utilities']['median_change_fair'])}, "
      f"shoppings {pc(ce['renda_imobiliaria']['median_change_fair'])}, serviços {pc(ce['servicos_tecnologia']['median_change_fair'])}, bancos "
      f"{pc(ce['banco']['median_change_fair'])}, varejo {pc(ce['varejo_consumo']['median_change_fair'])}, incorporadoras {pc(ce['incorporadora']['median_change_fair'])}, "
      f"locação {pc(ce['locacao']['median_change_fair'])}, cíclicas {pc(ce['ciclico_commodity']['median_change_fair'])}). O upside mediano das 59 passa de "
      f"{pc(rs['median_upside'])} para {pc(rp['median_upside'])}, e empresas com upside > 0: {rs['n_upside_positive']} → {rp['n_upside_positive']}. "
      f"Quase toda a queda vem de retirar os múltiplos-alvo: o esquema \"estudo sem múltiplos\" já dá {pc(rk['estudo_sem_multiplos']['median_upside'])}. "
      f"O ranking quase não muda (Spearman do escore multifator {br(rp['spearman_score_vs_study'])}; do upside {br(rp['spearman_upside_vs_study'])}), porque o "
      f"upside pesa só 10% do escore e a TIR de dono (30%), a qualidade e a solidez não dependem dos pesos.")
    A(f"6. **As 7 oportunidades.** Com as premissas revisadas de agora, o estudo recalculado mantém {len(keep_s)} das 7 pela regra "
      f"({', '.join(keep_s)}){'; ' + ', '.join(lost_s) + ' já ficam abaixo de P(MC) 45%' if lost_s else ''}. Com os pesos propostos, ficam {len(keep_p)}: "
      + ", ".join(f"{t} (upside {pc(rp['frozen7'][t]['upside'])})" for t in keep_p)
      + (f". Saem {', '.join(f'{t} (P(MC) {pc(rp['frozen7'][t]['prob_mc'], 0, False)})' for t in lost_p)}" if lost_p else "")
      + (f". Entram pela regra: {', '.join(new_p)}" if new_p else ". Nenhuma empresa nova entra")
      + ". Os rankings das oportunidades mudam pouco (tabela abaixo).")
    A("")
    A("## Métodos e convenções")
    A("")
    A("| Método | Definição | Bancos | Holdings |")
    A("|---|---|---|---|")
    A("| RIM/Ohlson | PL_base·(1+Ke)^(−s0) + Σ(LL_t − c_t·PL_{t−1}) a Ke. Se o ROE de 2031 na continuação do estudo (LL₂₀₃₀·(1+g)/PL₂₀₃₀) supera o ROE terminal, ele converge a este em 10 anos (2031–40), reinvestindo g/ROE_T do lucro, com perpetuidade do lucro residual a g. Caso contrário, usa a perpetuidade do estudo | sim | — |")
    A("| EVA | CI₀ + Σ(NOPAT_t − c_t·CI_{t−1}) a WACC; CI = PL + DL + minoritários, evolui por capex − D&A + ΔCG; mesmo fade do ROIC ao ROIC terminal; mesma ponte EV → equity do DCF | — | — |")
    A("| APV | FCFF e perpetuidade (value driver) a Ku = (1−wd)·Ke + wd·Kd (Harris–Pringle, com wd/Kd do WACC do estudo; Kd ajustado ao RET → custo da DL projetado) + VP a Ku do benefício fiscal da DL projetada (34%, ou a alíquota efetiva se < 20%) | — | — |")
    A("| FCFE | LL + D&A − capex − ΔCG + ΔDL, com a DL do balanço-base crescendo com a receita (juros e LL recalculados; caixa líquido constante), a Ke; perpetuidade LL·(1+g)·(1−g/ROE_T)/(Ke−g) | ≡ DDM | — |")
    A("| DDM c/ emissões e recompras | DDM do estudo com o fluxo líquido ao acionista (dividendos + recompras − emissões projetadas); ≡ RIM sem fade | ≡ DDM | — |")
    A("| P/L justificado | (1 − g/ROE_T)/(Ke − g) × LPA 12m à frente (2T26 + 2027E ponderados) | sim | — |")
    A("| P/VP justificado | (ROE_T − g)/(Ke − g) × VPA do balanço-base | sim | — |")
    A("| Pares | mediana dos pares da cobertura (grupo ∩ segmento B3 → segmento → subsetor → grupo [moda/consumo, utilities] → 1 par do segmento) de P/L 2027E e EV/EBITDA 2027E atuais (bancos: P/L e P/VP) | sim | — |")
    A("| Pares ajustados ao Ke | P/L de cada par × (k_par − g)/(25% − g), com k_par = TIR implícita no preço de hoje (Gordon), mediana × LPA 2027E (bancos: também P/VP) | sim | — |")
    A("| Histórico | mediana de 60 meses da própria ação (P/L e EV/EBITDA LTM; bancos P/L e P/VP) × métricas LTM; filtra meses com erro de unidade de ações | sim | P/VP, P/L |")
    A("| SOTP | SOTP do estudo recalculado com o valor justo novo das controladas avaliadas pelo motor (MOVI3, VAMO3, RAIL3) | — | sim |")
    A("")
    A("Todos os fluxos seguem o calendário do motor: stub de 2026 após o balanço-base, meio de período e perpetuidade em 31/12/2030. "
      "O encargo de capital do RIM e do EVA usa o espaçamento exato entre fluxos. É isso que torna RIM ≡ DDM e EVA ≡ DCF quando a perpetuidade é a mesma.")
    A("")
    A("## Viés sistemático por método")
    A("")
    A("| Método | n | Mediana vs valor justo do estudo | P25 / P75 | Mediana vs DCF | % acima do estudo | Upside mediano vs preço |")
    A("|---|---|---|---|---|---|---|")
    for k in ALL_METHODS + ["sotp_new"]:
        b = bias.get(k)
        if not b:
            continue
        A(f"| {b['label']} | {b['n']} | {pc(b['median_vs_study_fair'])} | {pc(b['p25_vs_study_fair'])} / {pc(b['p75_vs_study_fair'])} | "
          f"{pc(b['median_vs_dcf'])} | {pc(b['share_above_study_fair'], 0, False)} | {pc(b['median_upside_vs_price'])} |")
    A("")
    A("O valor justo do estudo já inclui 25% (bancos: 50%) de múltiplos-alvo; por isso os intrínsecos aparecem abaixo dele e próximos do DCF/DDM.")
    A("")
    A("## Onde os métodos divergem mais (e por quê)")
    A("")
    A("Dispersão = desvio-padrão do log dos valores positivos de todos os métodos. Ke implícito no P/L histórico = Ke que torna a mediana "
      "de 5 anos do P/L (LTM, Gordon com ROE e g terminais) coerente; TIR hoje = TIR de dono implícita no preço (DDM do estudo).")
    A("")
    A("| # | Empresa | Classe | σ log | Máx/mín | Mercado/intrínseco | Ke impl. P/L hist. | TIR hoje | Causas principais |")
    A("|---|---|---|---|---|---|---|---|---|")
    for i, t in enumerate(div_rank[:15]):
        c = comp[t]
        d = c["dispersion"]
        kk = c["detail"].get("ke_implied") or {}
        A(f"| {i+1} | {t} | {CLASS_LABEL[c['class']]} | {br(d['all']['std_log'])} | {br(d['all']['max_over_min'], 1)}× | "
          f"{x_(d['market_over_intrinsic'])} | {pc(kk.get('hist_pe_ltm'), 0, False)} | {pc(kk.get('market_irr_today'), 0, False)} | "
          f"{'; '.join(c['divergence_reasons']) or '—'} |")
    A("")
    A("## Pesos propostos por classe")
    A("")
    A("| Classe | Empresas | Pesos | Justificativa |")
    A("|---|---|---|---|")
    for cls, w in WEIGHTS.items():
        ms = doc["class_members"].get(cls, [])
        A(f"| {CLASS_LABEL[cls]} | {', '.join(ms)} | {', '.join(f'{LABEL[k]} {v*100:.0f}%' for k, v in w.items())} | {CLASS_WHY[cls]} |")
    A("")
    A("Princípios: (1) só entram métodos coerentes com Ke 25%; múltiplos de mercado brutos embutem o Ke implícito do mercado e viram referência; "
      "(2) para bancos não existe FCFF/EV; (3) o FCFE substitui o DDM onde o payout é baixo e discricionário; (4) o APV entra onde a alavancagem "
      "muda ou difere do wd do WACC. Pesos do estudo, para comparação: industrial DCF 50% / DDM 25% / múltiplos-alvo 25%; bancos DDM 50% / múltiplos 50%; "
      "holdings SOTP 100% (EZTC3 com 70/10/20). A agregação é a do motor: média de max(0, valor), renormalizada nos métodos disponíveis.")
    A("")
    A("### Efeito por classe")
    A("")
    A("| Classe | n | Δ mediano do valor justo | Upside mediano estudo | Upside mediano proposto |")
    A("|---|---|---|---|---|")
    for cls in WEIGHTS:
        e = ce.get(cls)
        if e:
            A(f"| {CLASS_LABEL[cls]} | {e['n']} | {pc(e['median_change_fair'])} | {pc(e['median_upside_study'])} | {pc(e['median_upside_proposed'])} |")
    A("")
    A("### Esquemas comparados")
    A("")
    A("| Esquema | Upside mediano | Upside > 0 | Spearman escore vs estudo | Spearman upside vs estudo | Oportunidades pela regra (top 8 por escore) |")
    A("|---|---|---|---|---|---|")
    names = {"estudo": "Estudo (recalculado agora)", "estudo_sem_multiplos": "Estudo sem múltiplos-alvo (DCF/DDM renormalizados)",
             "proposto": "**Proposto por classe**", "proposto_sem_mercado": "Proposto sem pares ajustados (só intrínsecos)",
             "igual_todos": "Peso igual em todos os métodos (inclui mercado bruto)"}
    for s_, r_ in rk.items():
        A(f"| {names[s_]} | {pc(r_['median_upside'])} | {r_['n_upside_positive']} | {br(r_['spearman_score_vs_study'])} | {br(r_['spearman_upside_vs_study'])} | "
          f"{', '.join(r_['opportunities_by_rule']) or '—'} |")
    A("")
    A("Top 10 do escore multifator: estudo " + ", ".join(rs["top10_score"]) + "; proposto " + ", ".join(rp["top10_score"]) + ".")
    A("")
    mv = [(t, d) for t, d in st["rank_moves_upside"] if d]
    if mv:
        A("Maiores mudanças no ranking por upside (posições; + = sobe): " + ", ".join(f"{t} {d:+d}" for t, d in mv) + ".")
        A("")
    A("## As 7 oportunidades")
    A("")
    A("| Empresa | Preço | Valor justo estudo → proposto | Upside estudo → proposto | Rank escore | Rank upside | P(MC) estudo → proposto | Regra (proposto) |")
    A("|---|---|---|---|---|---|---|---|")
    for t in opp:
        a, b = rs["frozen7"][t], rp["frozen7"][t]
        A(f"| {t} | {br(comp[t]['price'])} | {br(a['fair_value'])} → {br(b['fair_value'])} | {pc(a['upside'])} → {pc(b['upside'])} | "
          f"{a['rank_score']} → {b['rank_score']} | {a['rank_upside']} → {b['rank_upside']} | {pc(a['prob_mc'], 0, False)} → {pc(b['prob_mc'], 0, False)} | "
          f"{'passa' if b['passes_rule'] else 'não passa'} |")
    A("")
    A("Regra do estudo (build.py): TIR de dono ≥ 20%, P(valor justo > preço) ≥ 45%, Altman fora da zona de risco e confiança diferente de baixa. "
      "A TIR, o Altman e a confiança não mudam com os pesos; a probabilidade reescala a amostra do Monte Carlo do motor pelo novo valor justo.")
    A("")
    for t in opp:
        c = comp[t]
        v = c["values"]
        A(f"- **{t}** ({CLASS_LABEL[c['class']]}): " + ", ".join(f"{LABEL[k]} {br(v.get(k))}" for k in ALL_METHODS if v.get(k) is not None)
          + (f". Divergências: {'; '.join(c['divergence_reasons'])}." if c.get("divergence_reasons") else "."))
    A("")
    A("## Para os revisores (achados que afetam o estudo)")
    A("")
    A("- **Múltiplos-alvo incoerentes com Ke 25%**: o P/L-alvo mediano embute Ke de ~" + pc(ki["target_pe"], 0, False)
      + ". Para manter os múltiplos no blend, use os justificados (Gordon a 25%) ou os pares ajustados pela TIR implícita.")
    A("- **DCF × `other_financial`**: o FCFF exclui `other_financial`, mas o lucro (DDM/RIM/FCFE) inclui. Onde ele é material ("
      + ", ".join(f"{t} {pc(v, 0)} do LL" for t, v in st["other_financial_material"].items())
      + "), trate o item como ajuste debt-like ou como fluxo operacional, para não inflar (ou deprimir) o DCF.")
    iss = {t: comp[t]["detail"]["capital_flows"] for t in tickers if comp[t]["template"] != "holding"
           and abs((comp[t]["detail"].get("capital_flows") or {}).get("ddm_total_vs_ddm_study") or 0) > 0.02}
    if iss:
        A("- **DDM × emissão/recompra projetada**: o DDM do motor desconta só dividendos, com o número de ações fixo; o capital novo aumenta o lucro "
          "e o dividendo sem diluir. " + "; ".join(f"{t}: emissão R$ {br(v['equity_issuance_mn_2026_30'], 0)} mi, recompra R$ {br(v['buyback_mn_2026_30'], 0)} mi → DDM "
          f"{pc(v['ddm_total_vs_ddm_study'])} com o fluxo de capital" for t, v in iss.items())
          + ". Corrija no DDM (fluxo líquido ao acionista) ou ajuste o número de ações.")
    A("- **wd do WACC × dívida projetada**: em " + str(len(st["dcf_nonpositive"])) + " industriais o DCF dá equity ≤ 0. Com Ke fixo, o wd-alvo precisa "
      "ser coerente com a alavancagem a que 25% se refere; senão DCF e DDM medem coisas diferentes (ver APV/DCF e FCFE/DDM no JSON).")
    A("- **Série de múltiplos históricos**: " + ", ".join(f"{t} ({n} meses descartados)" for t, n in st["hist_series_quality_dropped"].items())
      + ". Esses meses têm erro de unidade de ações em `multiples_history` (P/L 0,01, P/VP 0,001), e as medianas de `stats` ficam inválidas.")
    A("- **Holdings**: componentes \"market\" fora da foto de preços (" + (", ".join(doc["checks"]["quotes_seeded_for_holdings"]) or "nenhum")
      + ") forçam cotação ao vivo, que falha de forma intermitente e zera o componente. Aqui o cache foi semeado com o último `data/model` do motor.")
    A("- **HAPV3**: o PL de R$ 48 bi é quase todo ágio da fusão e o preço implica P/VP de 0,05×. P/VP e RIM com fade não fazem sentido ali; o fade só corrói retorno excedente.")
    A("")
    A("## Tabela completa (59)")
    A("")
    A("Valores por ação/unit (R$). Rank = escore multifator do build.py recalculado; ↑ = rank por upside. Ordem: rank proposto.")
    A("")
    A("| Empresa | Classe | Preço | DCF | DDM | Múlt. | RIM | EVA | APV | FCFE | P/L j | P/VP j | Pares Ke | Pares | Hist. | Justo estudo | Justo proposto | Upside estudo | Upside proposto | Rank | ↑ Rank |")
    A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    order = sorted(tickers, key=lambda t: (comp[t]["proposed"]["rank_score"] or 99))
    keys = ("dcf", "ddm", "multiples", "rim", "eva", "apv", "fcfe", "pe_just", "pbv_just", "peers_adj", "peers", "hist")
    for t in order:
        c = comp[t]
        v = c["values"]
        a, b = c["schemes"]["estudo"], c["schemes"]["proposto"]
        mid = " | ".join(br(v.get(k)) for k in keys)
        A(f"| {t} | {CLASS_LABEL[c['class']]} | {br(c['price'])} | {mid} | {br(a['fair_value'])} | {br(b['fair_value'])} | {pc(a['upside'])} | {pc(b['upside'])} | "
          f"{a['rank_score']} → {b['rank_score']} | {a['rank_upside']} → {b['rank_upside']} |")
    A("")
    A("Holdings: SOTP do estudo e SOTP recalculado nas colunas \"Justo\"; \"Hist.\" = P/VP/P/L históricos consolidados (só referência).")
    A("")
    A("## Limitações")
    A("")
    A("- RIM, EVA, APV e FCFE usam as mesmas projeções do estudo: mudam a lente (âncora em PL/CI, fade, estrutura de capital, política de dívida), "
      "não os drivers operacionais. Divergências grandes apontam premissas a revisar, não erros de método.")
    A("- O APV ignora custos de dificuldade financeira, relevantes para as alavancadas (MGLU3, CVCB3, AZZA3, ECOR3), e trata o benefício fiscal com o risco do ativo (Harris–Pringle).")
    A("- O FCFE com estrutura de capital constante supõe rolar e ampliar a dívida na proporção da receita. Para quem precisa desalavancar (covenants), superestima o fluxo do acionista.")
    A("- Pares: a cobertura tem só 1 a 4 pares por segmento, e os múltiplos são da foto pós-queda. VBBR3, B3SA3, TOTS3, INTB3, GGPS3, BEEF3, TTEN3, SMFT3 e CVCB3 não têm par na cobertura. "
      "O ajuste ao Ke usa a TIR implícita de cada par (DDM do estudo) e vale só para múltiplos de equity.")
    A("- P(valor > preço) nos esquemas novos reescala a amostra do Monte Carlo do motor, sem refazer as 5.000 simulações; a TIR implícita, o Altman e a confiança não mudam com os pesos.")
    A("- Bancos ficam sem FCFF/EVA/APV, e o FCFE coincide com o DDM porque o PL projetado é o capital exigido.")
    with open(OUT_MD, "w") as fh:
        fh.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()

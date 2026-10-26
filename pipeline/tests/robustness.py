#!/usr/bin/env python3
"""Teste de robustez do valuation (59 empresas, 26/10/2026): pesos do blend e premissas.

Reavalia todas as empresas com o motor `pipeline/model.py` (importado, SEM alteração; as premissas de
`research/{T}.json` são copiadas em memória e perturbadas) e mede a estabilidade do valor justo e dos rankings
por TIR implícita (dividendos + perpetuidade) e por upside. Preços: foto `data/market/quotes.json`
(EAGORA_SNAPSHOT=1). As premissas são lidas na hora: rode de novo após revisões para refletir a versão atual.

Grades (uma dimensão de cada vez; demais premissas na base de cada empresa):
  pesos         {DCF, DDM, múltiplos} em passos de 0,1 com soma 1 (66 vetores). Bancos: {DDM = DCF+DDM, múltiplos}
                (o "intrínseco" do banco é o DDM), o que dá os 11 vetores {DDM, múltiplos} do template financeiro.
  ke            Ke de 20% a 30%, passo 1 p.p. (11)
  g             g terminal −2 a +2 p.p. (5)
  multiplos     múltiplos-alvo (P/L, EV/EBITDA, P/VP) −30% a +30%, passo 10% (7)
  margem_cresc  choque aditivo na margem EBITDA × no crescimento de receita, −2 a +2 p.p. cada (25)
  kd            Kd +300 bp: só no WACC, só no resultado financeiro (cost_of_net_debt) e nos dois (3)
  mc15          Monte Carlo com desvios ×1,5 (sorteios independentes por empresa; cada sorteio é uma combinação)
  conjunta      amostra aleatória do produto cartesiano pesos × Ke × g × múltiplos × margem × crescimento × Kd
Métricas: Spearman dos rankings vs base, frequência no top 7 / top 15, p5–p95 do valor justo, lista robusta
(top 7 em ≥ 50% e ≥ 80% das combinações), dependência das 7 oportunidades atuais (regra do build.py reproduzida
com P(valor justo > preço) recalculada por Monte Carlo idêntico ao do motor) e impacto de pesos propostos por setor.

Uso:
  .venv/bin/python pipeline/tests/robustness.py [--quick] [--n-joint N] [--n-mc15 N] [--n-mc N] [--workers N]
Saídas: data/tests/robustness.json (por empresa e por grade, formato para gráfico) e data/tests/robustness.md.
"""
import argparse
import hashlib
import json
import math
import os
import sys
import time
import warnings
import zlib
from datetime import datetime
from multiprocessing import get_context
from pathlib import Path

import numpy as np
from scipy.stats import rankdata, spearmanr

os.environ["EAGORA_SNAPSHOT"] = "1"  # foto de preços do estudo, sem rede
warnings.filterwarnings("ignore", category=RuntimeWarning)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
import model as M  # noqa: E402  motor de valuation (não alterado)
import build as B  # noqa: E402  zscore do escore multifator (mesma função do app)

OUT_JSON = ROOT / "data" / "tests" / "robustness.json"
OUT_MD = ROOT / "data" / "tests" / "robustness.md"
KE0 = M.KE
SEED_ENGINE = 7  # semente do Monte Carlo do motor
SCORE_W = {"valor": 0.30, "upside": 0.10, "qualidade": 0.20, "solidez": 0.15, "sobrerreacao": 0.10, "probabilidade": 0.15}
METHOD_KEYS = ("dcf", "ddm", "pe", "ev_ebitda", "pbv", "multiples")

W_GRID = [(round(a / 10, 1), round(b / 10, 1), round((10 - a - b) / 10, 1)) for a in range(11) for b in range(11 - a)]
KE_GRID = [round(0.20 + 0.01 * i, 2) for i in range(11)]
G_GRID = [-0.02, -0.01, 0.0, 0.01, 0.02]
MULT_GRID = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]
SHOCK_GRID = [-0.02, -0.01, 0.0, 0.01, 0.02]
KD_SHOCK = 0.03
KD_MODES = ["wacc", "pnl", "both"]
GRID_LABEL = {
    "pesos": "Pesos do blend {DCF, DDM, múltiplos} (passo 0,1)",
    "ke": "Ke 20–30% (passo 1 p.p.)",
    "g": "g terminal −2 a +2 p.p.",
    "multiplos": "Múltiplos-alvo −30% a +30%",
    "margem_cresc": "Margem EBITDA × crescimento ±2 p.p.",
    "kd": "Kd +300 bp (WACC / resultado financeiro / ambos)",
    "mc15": "Monte Carlo com desvios ×1,5",
    "conjunta": "Amostra conjunta de todas as grades",
}
DET_GRIDS = ["pesos", "ke", "g", "multiplos", "margem_cresc", "kd"]

# ------------------------------------------------------------------ pesos propostos por setor
# Chaves do motor: dcf, ddm, multiples (média P/L e EV/EBITDA ou P/L e P/VP), pe, ev_ebitda, pbv (bancos).
PROPOSED = {
    "bancos": {
        "tickers": ["BBAS3", "BBDC4", "BRSR6", "BPAC11"],
        "weights": {"ddm": 0.6, "pbv": 0.4},
        "why": "Valor de banco = ROE contra Ke sobre o PL. O DDM já é o fluxo do acionista (dividendo limitado pelo capital "
               "regulatório) e sua perpetuidade é o P/VP de Gordon (ROE−g)/(Ke−g); o P/VP-alvo é a âncora de mercado. "
               "O P/L sai: é redundante com o DDM (ambos lucro) e distorcido pelo ciclo de provisões e pelo JCP.",
    },
    "utilities": {
        "tickers": ["ALUP11", "AURE3", "CPLE3", "ENGI11", "EQTL3", "SBSP3"],
        "weights": {"ddm": 0.8, "multiples": 0.2},
        "why": "Retorno regulado e payout por política. Com DL de cerca de 50% do EV, o patrimônio do DCF (EV − DL) é a "
               "diferença de dois números grandes e sai negativo a Ke 25% nas 6 empresas: o motor trunca em zero e "
               "mantém o peso, então o DCF vira só um corte. O DCF fica como checagem (ROIC < WACC). O DDM desconta direto "
               "o fluxo do acionista após o serviço da dívida e foi o método menos disperso do setor.",
    },
    "concessoes": {
        "tickers": ["ECOR3", "MOTV3", "RAIL3", "ORVR3"],
        "weights": {"ddm": 0.8, "multiples": 0.2},
        "why": "Concessões rodoviárias, ferroviárias e ambientais com alavancagem de projeto de cerca de 50% do EV. O retorno "
               "do acionista é o dividendo após a dívida, e o DCF dá patrimônio residual negativo em ECOR3, MOTV3 e RAIL3. "
               "Os múltiplos ficam com 20% como âncora de mercado.",
    },
    "incorporadoras": {
        "tickers": ["CURY3", "CYRE3", "DIRR3", "EZTC3", "JHSF3", "MDNE3", "MRVE3", "PLPL3", "TEND3"],
        "weights": {"ddm": 0.5, "pe": 0.3, "dcf": 0.2},
        "why": "P/VP-ROE: no motor, a perpetuidade do DDM é PL×(ROE−g)/(Ke−g), o mesmo que P/VP justo × VPA. O P/L é o "
               "múltiplo de mercado do setor. EV/EBITDA sai porque há juros capitalizados no custo e a DL inclui "
               "financiamento à produção (capital de giro). O FCFF oscila com terreno e recebíveis "
               "(nwc de 0,6–1,5× a receita), daí só 20% de DCF.",
    },
    "varejo": {
        "tickers": ["CEAB3", "LREN3", "SBFG3", "MGLU3", "ASAI3", "GMAT3", "PGMN3", "RADL3", "AZZA3", "ALPA4",
                    "VIVA3", "VULC3", "NATU3"],
        "weights": {"ddm": 0.5, "multiples": 0.3, "dcf": 0.2},
        "why": "Muitos comparáveis listados e ciclo de margem e de giro: os múltiplos (P/L e EV/EBITDA IFRS-16) sobem para 30% "
               "(o padrão é 25%). Não vão além porque embutem custo de capital de cerca de 12%, e a 40% sozinhos põem LREN3 e "
               "SBFG3 na lista (ver sensibilidade). O DCF cai para 20%: o arrendamento IFRS-16 entra na DL (cerca de 40% do EV) "
               "e o DCF é o método mais disperso do setor. O DDM, coerente com o Ke 25%, fica com 50%.",
    },
    "locadoras": {
        "tickers": ["RENT3", "MOVI3", "VAMO3"],
        "weights": {"ddm": 0.7, "multiples": 0.3},
        "why": "O capex de frota é sobretudo crescimento e a DL passa de 70% do EV: o FCFF é negativo no horizonte "
               "explícito e o patrimônio do DCF fica ≤ 0 (MOVI3, VAMO3), daí DCF fora do blend. O dividendo reflete a "
               "geração depois da frota. O mercado precifica por P/L e EV/EBITDA, que ficam com 30%.",
    },
    "shoppings": {
        "tickers": ["ALOS3", "IGTI11", "MULT3"],
        "weights": {"ddm": 0.5, "dcf": 0.3, "multiples": 0.2},
        "why": "Ativos reais de vida longa, payout alto e alavancagem moderada (DL de cerca de 25% do EV). DCF e DDM convergem no "
               "nível (diferença de 5–16%), mas o DDM é menos disperso (0,65 contra 1,00), daí 50/30. Os múltiplos-alvo (P/L de "
               "9,5–12x) valem 2,5× o DDM porque embutem custo de capital muito abaixo de 25%; ficam com 20%.",
    },
}
DEFAULT_IND = {"dcf": 0.5, "ddm": 0.25, "multiples": 0.25}
# sensibilidade da proposta às escolhas mais discutíveis (demais setores na proposta)
VARIANTS = {
    "varejo DDM 60 / Múlt 20 / DCF 20": {"varejo": {"ddm": 0.6, "multiples": 0.2, "dcf": 0.2}},
    "varejo DDM 50 / Múlt 30 / DCF 20 (proposta)": {},
    "varejo DDM 40 / Múlt 40 / DCF 20": {"varejo": {"ddm": 0.4, "multiples": 0.4, "dcf": 0.2}},
    "incorporadoras no padrão 50/25/25": {"incorporadoras": {"dcf": 0.5, "ddm": 0.25, "multiples": 0.25}},
    "demais com DCF 30 / DDM 45 / Múlt 25": {"demais": {"dcf": 0.3, "ddm": 0.45, "multiples": 0.25}},
}

# ------------------------------------------------------------------ estado global (herdado pelos workers via fork)
COMPS = {}
ORDER = []   # tickers na ordem do overview
NONH = []    # não holdings
HOLD = []    # holdings (SOTP)
IDX = {}
STATIC = {}  # campos do escore que não dependem do valuation


def _load_json_retry(p, tries=5):
    last = None
    for _ in range(tries):
        try:
            raw = p.read_bytes()
            return json.loads(raw), raw
        except Exception as e:  # revisor gravando o arquivo neste instante
            last = e
            time.sleep(0.5)
    raise last


def load_universe():
    ov = json.load(open(ROOT / "data" / "app" / "overview.json"))
    rows = {x["ticker"]: x for x in ov["companies"]}
    for t in [x["ticker"] for x in ov["companies"]]:
        pp = ROOT / "research" / f"{t}.json"
        prem, raw = _load_json_retry(pp)
        hist = json.load(open(ROOT / "data" / "hist" / f"{t}.json"))
        q = M.live_quote(t) or {}
        price, prev = q.get("price"), q.get("prev_close")
        tpl = prem.get("template", "industrial")
        sh = M.shares_info(hist, prem)
        mcap = mcap_pre = None
        if tpl != "holding":
            mcap = M.market_cap(prem, hist, sh, price) if price else None
            mcap_pre = M.market_cap(prem, hist, sh, prev) if prev else None
        COMPS[t] = dict(ticker=t, prem=prem, hist=hist, price=price, tpl=tpl, mcap=mcap, mcap_pre=mcap_pre or mcap,
                        shares=sh, row=rows[t], sha1=hashlib.sha1(raw).hexdigest()[:12],
                        mtime=datetime.fromtimestamp(pp.stat().st_mtime).isoformat(timespec="seconds"))
        ORDER.append(t)
        (HOLD if tpl == "holding" else NONH).append(t)
    for i, t in enumerate(ORDER):
        IDX[t] = i
        row = COMPS[t]["row"]
        sc = row.get("scores") or {}
        conf = (COMPS[t]["prem"].get("confidence") or "").lower().strip()
        STATIC[t] = {"qualidade": sc.get("qualidade"), "solidez": sc.get("solidez"), "sobrerreacao": sc.get("sobrerreacao"),
                     "zone": (row.get("altman") or {}).get("zone"),
                     "low_conf": conf.startswith("baixa") and not conf.startswith("baixa-m") and not conf.startswith("baixa a m")}
    return ov


def bucket_of(t):
    for b, d in PROPOSED.items():
        if t in d["tickers"]:
            return b
    return "holdings" if COMPS[t]["tpl"] == "holding" else "demais"


def proposed_weights(t):
    b = bucket_of(t)
    if b in PROPOSED:
        return dict(PROPOSED[b]["weights"])
    if b == "holdings":
        return None
    return dict(DEFAULT_IND) if COMPS[t]["tpl"] != "financial" else {"ddm": 0.5, "multiples": 0.5}


# ------------------------------------------------------------------ motor sob perturbação
def weights_for(tpl, w3):
    wd, wq, wm = w3
    if tpl == "financial":
        return {"ddm": round(wd + wq, 1), "multiples": wm}
    return {"dcf": wd, "ddm": wq, "multiples": wm}


def variant_prem(prem, tpl, weights=None, mult=1.0, kd=0.0, kd_mode="both"):
    """Cópia rasa das premissas com as perturbações (nunca grava em disco)."""
    p = dict(prem)
    if weights is not None:
        p["valuation_weights"] = weights
    if mult != 1.0:
        tm = dict(prem.get("target_multiples") or {})
        for k in ("pe", "ev_ebitda", "pbv"):
            if isinstance(tm.get(k), (int, float)) and tm.get(k):
                tm[k] = tm[k] * mult
        p["target_multiples"] = tm
    if kd and tpl not in ("financial", "holding"):
        if kd_mode in ("both", "pnl"):
            pj = dict(prem.get("projection") or {})
            pj["cost_of_net_debt"] = (M.arr(pj.get("cost_of_net_debt")) + kd).tolist()
            p["projection"] = pj
        if kd_mode in ("both", "wacc"):
            w = dict(prem.get("wacc") or {})
            w["kd_pre_tax"] = M.num(w.get("kd_pre_tax"), 0.155) + kd
            p["wacc"] = w
    return p


def company_weights(t, st):
    c = COMPS[t]
    if st.get("w3") is not None:
        return weights_for(c["tpl"], st["w3"])
    if st.get("wmap") is not None and t in st["wmap"]:
        return st["wmap"][t]
    return None


def holding_fair(c, models, ke, dg):
    """SOTP do motor (value_holding) com o custo de holding recapitalizado a (Ke − g) do cenário."""
    r = M.value_holding(c["prem"], c["hist"], models, price=c["price"])
    hcost = M.num((c["prem"].get("sotp") or {}).get("holding_cost_mn"))
    g1 = r["g"] + dg
    cap = hcost / (ke - g1) if ke > g1 else 0.0
    eq = r["nav_fair"] - r["holding_net_debt"] - cap
    return eq / r["shares"]["outstanding_mn"] * r["shares"]["per_unit"]


def _f(x):
    try:
        x = float(x)
        return x if math.isfinite(x) else np.nan
    except Exception:
        return np.nan


def eval_state(st):
    """Avalia as 59 empresas num estado de premissas. Retorna fair, upside, irr (n) e valores por método (n×3)."""
    ke = st.get("ke", KE0)
    dg, dm, dgr = st.get("dg", 0.0), st.get("dm", 0.0), st.get("dgr", 0.0)
    shifts = {}
    if dg:
        shifts["terminal_g_shift"] = dg
    if dm:
        shifts["ebitda_margin_shift"] = dm
    if dgr:
        shifts["revenue_growth_shift"] = dgr
    n = len(ORDER)
    fair, up, irr = np.full(n, np.nan), np.full(n, np.nan), np.full(n, np.nan)
    meth = np.full((n, 3), np.nan)
    models = {}
    for t in NONH:
        c = COMPS[t]
        i = IDX[t]
        try:
            p = variant_prem(c["prem"], c["tpl"], company_weights(t, st), st.get("mult", 1.0), st.get("kd", 0.0),
                             st.get("kd_mode", "both"))
            r = M.value_company(p, c["hist"], ke=ke, shifts=shifts or None, price=c["price"], mcap=c["mcap_pre"],
                                mcap_now=c["mcap"])
        except Exception:
            continue
        models[t] = r
        fair[i], up[i], irr[i] = _f(r.get("fair_value")), _f(r.get("upside")), _f(r.get("irr_implied"))
        v = r.get("values") or {}
        meth[i] = [_f(v.get("dcf")), _f(v.get("ddm")), _f(v.get("multiples"))]
    for t in HOLD:
        c = COMPS[t]
        i = IDX[t]
        try:
            fv = holding_fair(c, models, ke, dg)
        except Exception:
            continue
        fair[i] = fv
        up[i] = fv / c["price"] - 1 if c["price"] else np.nan
    return fair, up, irr, meth


def mc_draws(prem, n, seed, scale):
    """Mesmos sorteios do monte_carlo() do motor (ordem das chamadas ao gerador preservada)."""
    u = prem.get("uncertainty") or {}
    sd_g, sd_m = M.num(u.get("revenue_growth_sd"), 0.03) * scale, M.num(u.get("ebitda_margin_sd"), 0.015) * scale
    sd_T, sd_c = M.num(u.get("terminal_g_sd"), 0.0075) * scale, M.num(u.get("capex_pct_sd"), 0.005) * scale
    rng = np.random.default_rng(seed)
    z1 = rng.standard_normal(n)
    z2 = 0.5 * z1 + math.sqrt(1 - 0.25) * rng.standard_normal(n)
    eg, em = z1 * sd_g, z2 * sd_m
    eT = np.clip(rng.standard_normal(n) * sd_T, -0.03, 0.015)
    ec = rng.standard_normal(n) * sd_c
    return eg, em, eT, ec


def mc_values_worker(args):
    """Valores por método em cada sorteio (Monte Carlo do motor) → P(valor > preço) para qualquer vetor de pesos."""
    t, scale, n, seed = args
    c = COMPS[t]
    eg, em, eT, ec = mc_draws(c["prem"], n, seed, scale)
    V = {k: np.full(n, np.nan) for k in METHOD_KEYS}
    for j in range(n):
        try:
            r = M.value_company(c["prem"], c["hist"], shifts={"revenue_growth_shift": eg[j], "ebitda_margin_shift": em[j],
                                "terminal_g_shift": eT[j], "capex_pct_shift": ec[j]}, mcap=c["mcap_pre"])
        except Exception:
            continue
        v = r.get("values") or {}
        for k in METHOD_KEYS:
            V[k][j] = _f(v.get(k))
    return t, V


def mc_prob_worker(args):
    """P(valor justo > preço) num estado de premissas, com o Monte Carlo do motor (5.000 sorteios, semente 7)."""
    st, t, n = args
    c = COMPS[t]
    eg, em, eT, ec = mc_draws(c["prem"], n, SEED_ENGINE, 1.0)
    p = variant_prem(c["prem"], c["tpl"], company_weights(t, st), st.get("mult", 1.0), st.get("kd", 0.0), st.get("kd_mode", "both"))
    ke = st.get("ke", KE0)
    out = np.full(n, np.nan)
    for j in range(n):
        try:
            r = M.value_company(p, c["hist"], ke=ke, shifts={"revenue_growth_shift": eg[j] + st.get("dgr", 0.0),
                                "ebitda_margin_shift": em[j] + st.get("dm", 0.0), "terminal_g_shift": eT[j] + st.get("dg", 0.0),
                                "capex_pct_shift": ec[j]}, mcap=c["mcap_pre"])
            out[j] = _f(r.get("fair_value"))
        except Exception:
            pass
    out = out[np.isfinite(out)]
    return float((out > c["price"]).mean()) if len(out) and c["price"] else np.nan


def mc_rank_worker(args):
    """Sorteios com desvios ×1,5 (semente própria por empresa) com preço: valor justo, upside e TIR por sorteio."""
    t, n, seed = args
    c = COMPS[t]
    eg, em, eT, ec = mc_draws(c["prem"], n, seed, 1.5)
    fair, up, irr, fvs = (np.full(n, np.nan) for _ in range(4))
    for j in range(n):
        try:
            r = M.value_company(c["prem"], c["hist"], shifts={"revenue_growth_shift": eg[j], "ebitda_margin_shift": em[j],
                                "terminal_g_shift": eT[j], "capex_pct_shift": ec[j]}, price=c["price"], mcap=c["mcap_pre"],
                                mcap_now=c["mcap"])
        except Exception:
            continue
        fair[j], up[j], irr[j], fvs[j] = _f(r.get("fair_value")), _f(r.get("upside")), _f(r.get("irr_implied")), _f(r.get("fair_value_share"))
    return t, fair, up, irr, fvs


def blend(V, weights):
    """Blend idêntico ao do motor: Σ w·max(0, v) / Σ w sobre métodos disponíveis (vetorizado nos sorteios)."""
    acc, tot = 0.0, 0.0
    for k, w in weights.items():
        x = V.get(k)
        if x is None:
            continue
        ok = np.isfinite(x)
        acc = acc + np.where(ok, w * np.maximum(0.0, np.nan_to_num(x)), 0.0)
        tot = tot + np.where(ok, w, 0.0)
    tot = np.asarray(tot, dtype=float)
    return np.where(tot > 0, np.asarray(acc, dtype=float) / np.where(tot > 0, tot, 1.0), np.nan)


def prob_from_values(V, weights, price):
    f = blend(V, weights)
    f = f[np.isfinite(f)]
    return float((f > price).mean()) if len(f) and price else np.nan


# ------------------------------------------------------------------ métricas
def rank_desc(x):
    x = np.asarray(x, dtype=float)
    out = np.full(x.shape, np.nan)
    ok = np.isfinite(x)
    if ok.any():
        out[ok] = rankdata(-x[ok], method="min")
    return out


def spear(a, b):
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3 or np.nanstd(a[ok]) == 0 or np.nanstd(b[ok]) == 0:
        return np.nan
    if np.allclose(a[ok], b[ok]):
        return 1.0
    return float(spearmanr(a[ok], b[ok]).statistic)


def topk(x, k):
    r = rank_desc(x)
    return set(np.where(r <= k)[0].tolist())


def score_rule(irr, up, prob):
    """Escore multifator e regra de oportunidades do build.py (z-scores na cobertura)."""
    def lst(a):
        return [None if not np.isfinite(x) else round(float(x), 4) for x in a]
    z_val, z_up, z_p = B.zscore(lst(irr)), B.zscore(lst(up)), B.zscore(lst(prob))
    n = len(ORDER)
    score = np.full(n, np.nan)
    for i, t in enumerate(ORDER):
        s = STATIC[t]
        comp = {"valor": z_val[i], "upside": z_up[i], "qualidade": s["qualidade"], "solidez": s["solidez"],
                "sobrerreacao": s["sobrerreacao"], "probabilidade": z_p[i]}
        tot = sum(SCORE_W[k] for k, v in comp.items() if v is not None)
        if tot:
            score[i] = round(sum(SCORE_W[k] * v for k, v in comp.items() if v is not None) / tot, 3)
    ranked = sorted([i for i in range(n) if np.isfinite(score[i])], key=lambda i: -score[i])
    rank = np.full(n, np.nan)
    for k, i in enumerate(ranked):
        rank[i] = k + 1
    sel = [i for i in ranked if (irr[i] if np.isfinite(irr[i]) else -1) >= 0.20 and (prob[i] if np.isfinite(prob[i]) else 0) >= 0.45
           and STATIC[ORDER[i]]["zone"] != "risco" and not STATIC[ORDER[i]]["low_conf"]][:8]
    return score, rank, sel


def q(a, p):
    a = np.asarray(a, dtype=float)
    a = a[np.isfinite(a)]
    return float(np.percentile(a, p)) if len(a) else None


def rnd(x, d=4):
    if x is None:
        return None
    try:
        x = float(x)
    except Exception:
        return None
    return round(x, d) if math.isfinite(x) else None


def grid_metrics(F, U, I, base):
    """F/U/I: cenários × empresas. Retorna métricas por cenário e por empresa."""
    S = F.shape[0]
    RI = np.vstack([rank_desc(I[s]) for s in range(S)])
    RU = np.vstack([rank_desc(U[s]) for s in range(S)])
    b7i, b7u = topk(base["irr"], 7), topk(base["up"], 7)
    per_s = {"spearman_irr": [], "spearman_up": [], "overlap7_irr": [], "overlap7_up": [], "top7_irr": [], "top7_up": []}
    for s in range(S):
        per_s["spearman_irr"].append(spear(base["irr"], I[s]))
        per_s["spearman_up"].append(spear(base["up"], U[s]))
        t7i, t7u = set(np.where(RI[s] <= 7)[0].tolist()), set(np.where(RU[s] <= 7)[0].tolist())
        per_s["overlap7_irr"].append(len(t7i & b7i) / 7)
        per_s["overlap7_up"].append(len(t7u & b7u) / 7)
        per_s["top7_irr"].append([ORDER[i] for i in sorted(t7i, key=lambda i: RI[s][i])])
        per_s["top7_up"].append([ORDER[i] for i in sorted(t7u, key=lambda i: RU[s][i])])
    per_c = {}
    for i, t in enumerate(ORDER):
        ri, ru = RI[:, i], RU[:, i]
        has_i = np.isfinite(ri).any()
        per_c[t] = {
            "top7_irr": rnd(np.mean(ri <= 7)) if has_i else None, "top15_irr": rnd(np.mean(ri <= 15)) if has_i else None,
            "top7_up": rnd(np.mean(ru <= 7)), "top15_up": rnd(np.mean(ru <= 15)),
            "fair_p5": rnd(q(F[:, i], 5)), "fair_p50": rnd(q(F[:, i], 50)), "fair_p95": rnd(q(F[:, i], 95)),
            "up_p5": rnd(q(U[:, i], 5)), "up_p50": rnd(q(U[:, i], 50)), "up_p95": rnd(q(U[:, i], 95)),
            "irr_p5": rnd(q(I[:, i], 5)), "irr_p50": rnd(q(I[:, i], 50)), "irr_p95": rnd(q(I[:, i], 95)),
            "rank_irr_best": rnd(np.nanmin(ri), 0) if has_i else None, "rank_irr_worst": rnd(np.nanmax(ri), 0) if has_i else None,
            "rank_up_best": rnd(np.nanmin(ru), 0), "rank_up_worst": rnd(np.nanmax(ru), 0),
            "rank_up_p50": rnd(q(ru, 50), 1), "rank_irr_p50": rnd(q(ri, 50), 1) if has_i else None,
        }
    def summ(v):
        v = np.array(v, dtype=float)
        v = v[np.isfinite(v)]
        if not len(v):
            return None
        return {"min": rnd(v.min()), "p5": rnd(np.percentile(v, 5)), "median": rnd(np.median(v)), "mean": rnd(v.mean())}
    summary = {"n": int(S), "spearman_irr": summ(per_s["spearman_irr"]), "spearman_up": summ(per_s["spearman_up"]),
               "overlap7_irr_mean": rnd(np.mean(per_s["overlap7_irr"])), "overlap7_up_mean": rnd(np.mean(per_s["overlap7_up"]))}
    for metric in ("irr", "up"):
        for thr, lab in ((0.5, "ge50"), (0.8, "ge80")):
            key = f"top7_{metric}"
            lst = [t for t in ORDER if per_c[t][key] is not None and per_c[t][key] >= thr - 1e-12]
            summary[f"robust_{metric}_{lab}"] = sorted(lst, key=lambda t: -per_c[t][key])
    return per_s, per_c, summary, RI, RU


def opp_metrics(sel_lists, current):
    """sel_lists: listas (índices) selecionadas pela regra em cada cenário."""
    cur = set(IDX[t] for t in current)
    kept = [len(set(s[:7]) & cur) for s in sel_lists]
    freq = {t: rnd(np.mean([IDX[t] in s[:7] for s in sel_lists])) for t in ORDER}
    freq = {t: v for t, v in freq.items() if v and v > 0}
    return {"kept_mean": rnd(np.mean(kept)), "kept_min": int(min(kept)), "kept_dist": {str(k): int(kept.count(k)) for k in range(8)},
            "identical_share": rnd(np.mean([set(s[:7]) == cur for s in sel_lists])),
            "freq_selected": dict(sorted(freq.items(), key=lambda kv: -kv[1]))}


# ------------------------------------------------------------------ cenários
def oat_states():
    g = {}
    g["pesos"] = [({"w_dcf": w[0], "w_ddm": w[1], "w_mult": w[2]}, {"w3": w}) for w in W_GRID]
    g["ke"] = [({"ke": k}, {"ke": k}) for k in KE_GRID]
    g["g"] = [({"dg": d}, {"dg": d}) for d in G_GRID]
    g["multiplos"] = [({"mult": m}, {"mult": m}) for m in MULT_GRID]
    g["margem_cresc"] = [({"dm": a, "dgr": b}, {"dm": a, "dgr": b}) for a in SHOCK_GRID for b in SHOCK_GRID]
    g["kd"] = [({"kd": KD_SHOCK, "kd_mode": m}, {"kd": KD_SHOCK, "kd_mode": m}) for m in KD_MODES]
    return g


def joint_states(n, seed=20261026):
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        w = W_GRID[rng.integers(len(W_GRID))]
        st = {"w3": w, "ke": KE_GRID[rng.integers(len(KE_GRID))], "dg": G_GRID[rng.integers(5)], "mult": MULT_GRID[rng.integers(7)],
              "dm": SHOCK_GRID[rng.integers(5)], "dgr": SHOCK_GRID[rng.integers(5)], "kd": KD_SHOCK if rng.integers(2) else 0.0,
              "kd_mode": "both"}
        out.append(({"w_dcf": w[0], "w_ddm": w[1], "w_mult": w[2], "ke": st["ke"], "dg": st["dg"], "mult": st["mult"],
                     "dm": st["dm"], "dgr": st["dgr"], "kd": st["kd"]}, st))
    return out


def seed_for(t):
    return 20261026 + zlib.crc32(t.encode()) % 100000


# ------------------------------------------------------------------ relatório
def pct(x, d=0):
    return "—" if x is None or (isinstance(x, float) and not math.isfinite(x)) else f"{x * 100:.{d}f}%".replace(".", ",")


def num(x, d=2):
    return "—" if x is None or (isinstance(x, float) and not math.isfinite(x)) else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fr(x):
    return "—" if x is None else f"{x:.2f}".replace(".", ",")


def lst_txt(lst):
    return ", ".join(lst) if lst else "nenhuma"


def ri(x):
    return "—" if x is None else str(int(x))


def cond_txt(by, name):
    """Condição de peso em que a empresa é selecionada em ≥ 50% dos vetores (marginal no peso indicado)."""
    lv = [(float(k), v) for k, v in by.items()]
    allv = [l for l, _ in lv]
    ok = [l for l, v in lv if v is not None and v >= 0.5]
    f1 = lambda x: f"{x:.1f}".replace(".", ",")
    if not ok:
        return f"nenhum {name}"
    if len(ok) == len(lv):
        return f"qualquer {name}"
    lo, hi = min(ok), max(ok)
    contiguous = all((l in ok) == (lo <= l <= hi) for l in allv)
    if lo == hi:
        return f"{name} = {f1(lo)}"
    if contiguous and hi == max(allv):
        return f"{name} ≥ {f1(lo)}"
    if contiguous and lo == min(allv):
        return f"{name} ≤ {f1(hi)}"
    if contiguous:
        return f"{name} entre {f1(lo)} e {f1(hi)}"
    return f"{name} entre {f1(lo)} e {f1(hi)}, irregular"


def lst_e(lst):
    lst = list(lst)
    return "nenhuma" if not lst else lst[0] if len(lst) == 1 else ", ".join(lst[:-1]) + " e " + lst[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="menos sorteios (teste rápido)")
    ap.add_argument("--n-joint", type=int, default=3000)
    ap.add_argument("--n-mc15", type=int, default=2000)
    ap.add_argument("--n-mc", type=int, default=M.N_MC, help="sorteios do MC de P(valor>preço) (motor: 5.000)")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    a = ap.parse_args()
    if a.quick:
        a.n_joint, a.n_mc15, a.n_mc = 300, 200, 1000
    t0 = time.time()
    ov = load_universe()
    n = len(ORDER)
    current_opp = list(ov.get("opportunities") or [])
    print(f"universo: {n} empresas ({len(HOLD)} holdings) | oportunidades atuais: {current_opp}", flush=True)

    # ---------------- base (motor, premissas atuais)
    bF, bU, bI, bMeth = eval_state({})
    base = {"fair": bF, "up": bU, "irr": bI}
    ctx = get_context("fork")
    with ctx.Pool(a.workers) as pool:
        # ---------------- grades determinísticas
        grids = oat_states()
        flat = [(g, p, st) for g in DET_GRIDS for (p, st) in grids[g]]
        res = pool.map(eval_state, [st for _, _, st in flat], chunksize=2)
        print(f"grades determinísticas: {len(flat)} cenários  [{time.time() - t0:.0f}s]", flush=True)
        # ---------------- amostra conjunta
        js = joint_states(a.n_joint)
        res_j = pool.map(eval_state, [st for _, st in js], chunksize=8)
        print(f"amostra conjunta: {len(js)} combinações  [{time.time() - t0:.0f}s]", flush=True)
        # ---------------- MC do motor (valores por método por sorteio): desvios ×1 e ×1,5
        mcv = dict(pool.map(mc_values_worker, [(t, 1.0, a.n_mc, SEED_ENGINE) for t in NONH]))
        mcv15 = dict(pool.map(mc_values_worker, [(t, 1.5, a.n_mc, SEED_ENGINE) for t in NONH]))
        print(f"MC por método (×1 e ×1,5): {a.n_mc} sorteios  [{time.time() - t0:.0f}s]", flush=True)
        # ---------------- MC ×1,5 com TIR (ranking por sorteio, sementes independentes)
        mcr = pool.map(mc_rank_worker, [(t, a.n_mc15, seed_for(t)) for t in NONH])
        print(f"MC ×1,5 com TIR: {a.n_mc15} sorteios  [{time.time() - t0:.0f}s]", flush=True)
        # ---------------- P(valor > preço) nas grades não-peso (para escore e regra de oportunidades)
        nw = [(k, (g, p, st)) for k, (g, p, st) in enumerate(flat) if g != "pesos"]
        tasks = [(st, t, a.n_mc) for _, (g, p, st) in nw for t in NONH]
        probs_flat = pool.map(mc_prob_worker, tasks, chunksize=4)
        print(f"P(MC) nas grades de premissas: {len(nw)} cenários  [{time.time() - t0:.0f}s]", flush=True)

    # ---------------- P(MC) base reproduzida e checagem contra o app
    base_w = {t: (COMPS[t]["prem"].get("valuation_weights") or ({"ddm": 0.5, "multiples": 0.5} if COMPS[t]["tpl"] == "financial" else DEFAULT_IND)) for t in NONH}
    b_prob = np.full(n, np.nan)
    b_prob15 = np.full(n, np.nan)
    for t in NONH:
        b_prob[IDX[t]] = prob_from_values(mcv[t], base_w[t], COMPS[t]["price"])
        b_prob15[IDX[t]] = prob_from_values(mcv15[t], base_w[t], COMPS[t]["price"])
    b_score, b_rank, b_sel = score_rule(bI, bU, b_prob)
    rows = {t: COMPS[t]["row"] for t in ORDER}
    check, prob_check = [], []
    for t in ORDER:
        r = rows[t]
        i = IDX[t]
        d_fv = (bF[i] / r["fair_value"] - 1) if r.get("fair_value") else None
        if d_fv is None or abs(d_fv) > 5e-4:
            check.append({"ticker": t, "fair_engine": rnd(bF[i]), "fair_overview": r.get("fair_value"), "diff": rnd(d_fv),
                          "irr_engine": rnd(bI[i]), "irr_overview": r.get("irr_implied"), "research_mtime": COMPS[t]["mtime"]})
        elif r.get("prob_mc") is not None and abs(b_prob[i] - r["prob_mc"]) > 6e-4:
            prob_check.append({"ticker": t, "prob_engine": rnd(b_prob[i]), "prob_overview": r.get("prob_mc")})
    changed = {d["ticker"] for d in check}
    score_diff = [abs(b_score[IDX[t]] - rows[t]["score"]) for t in ORDER
                  if rows[t].get("score") is not None and np.isfinite(b_score[IDX[t]]) and t not in changed]

    # ---------------- métricas por grade
    out_grids = {}
    per_company_grid = {t: {} for t in ORDER}
    opp_by_grid = {}
    prob_state = {}
    # probabilidade por cenário (pesos: re-blend exato dos sorteios do motor; demais: MC re-rodado)
    pi = 0
    for k, (g, p, st) in enumerate(flat):
        pr = np.full(n, np.nan)
        if g == "pesos":
            for t in NONH:
                pr[IDX[t]] = prob_from_values(mcv[t], weights_for(COMPS[t]["tpl"], st["w3"]), COMPS[t]["price"])
        else:
            for t in NONH:
                pr[IDX[t]] = probs_flat[pi]
                pi += 1
        prob_state[k] = pr
    for g in DET_GRIDS:
        ks = [k for k, (gg, _, _) in enumerate(flat) if gg == g]
        F = np.vstack([res[k][0] for k in ks])
        U = np.vstack([res[k][1] for k in ks])
        I = np.vstack([res[k][2] for k in ks])
        per_s, per_c, summ, RI, RU = grid_metrics(F, U, I, base)
        sels, scores_g, sranks = [], [], []
        for k in ks:
            sc, rk, sel = score_rule(res[k][2], res[k][1], prob_state[k])
            sels.append(sel)
            scores_g.append(sc)
            sranks.append(rk)
        om = opp_metrics(sels, current_opp)
        sp_score = [spear(b_score, s) for s in scores_g]
        summ["spearman_score"] = {"min": rnd(np.nanmin(sp_score)), "median": rnd(np.nanmedian(sp_score))}
        summ["opportunities"] = om
        opp_by_grid[g] = om
        P = np.vstack([prob_state[k] for k in ks])
        out_grids[g] = {
            "label": GRID_LABEL[g], "params": [flat[k][1] for k in ks], **{kk: [rnd(x) for x in vv] if kk.startswith(("spearman", "overlap")) else vv for kk, vv in per_s.items()},
            "selected_opportunities": [[ORDER[i] for i in s] for s in sels],
            "spearman_score": [rnd(x) for x in sp_score],
            "summary": summ,
            "matrix": {"fair": [[rnd(x) for x in row] for row in F], "upside": [[rnd(x) for x in row] for row in U],
                       "irr": [[rnd(x) for x in row] for row in I], "rank_irr": [[rnd(x, 0) for x in row] for row in RI],
                       "rank_up": [[rnd(x, 0) for x in row] for row in RU], "prob_mc": [[rnd(x) for x in row] for row in P],
                       "score": [[rnd(x, 3) for x in row] for row in scores_g], "rank_score": [[rnd(x, 0) for x in row] for row in sranks]},
        }
        for t in ORDER:
            per_company_grid[t][g] = per_c[t]
            per_company_grid[t][g]["opp_selected"] = rnd(np.mean([IDX[t] in s[:7] for s in sels]))

    # ---------------- amostra conjunta
    FJ = np.vstack([r[0] for r in res_j])
    UJ = np.vstack([r[1] for r in res_j])
    IJ = np.vstack([r[2] for r in res_j])
    MJ = np.stack([r[3] for r in res_j])  # cenários × empresas × {dcf, ddm, múltiplos}
    per_s, per_c, summ, _, _ = grid_metrics(FJ, UJ, IJ, base)
    out_grids["conjunta"] = {"label": GRID_LABEL["conjunta"], "params": [p for p, _ in js],
                             "spearman_irr": [rnd(x) for x in per_s["spearman_irr"]], "spearman_up": [rnd(x) for x in per_s["spearman_up"]],
                             "overlap7_irr": [rnd(x) for x in per_s["overlap7_irr"]], "overlap7_up": [rnd(x) for x in per_s["overlap7_up"]],
                             "summary": summ}
    for t in ORDER:
        per_company_grid[t]["conjunta"] = per_c[t]

    # ---------------- MC ×1,5 (ranking por sorteio)
    N15 = a.n_mc15
    F15, U15, I15 = np.full((N15, n), np.nan), np.full((N15, n), np.nan), np.full((N15, n), np.nan)
    fvs15 = {}
    for t, f, u, ir, fvs in mcr:
        F15[:, IDX[t]], U15[:, IDX[t]], I15[:, IDX[t]] = f, u, ir
        fvs15[t] = fvs
    for t in HOLD:
        c = COMPS[t]
        for j in range(N15):
            models = {s: {"fair_value": F15[j, IDX[s]], "fair_value_share": fvs15[s][j], "shares": COMPS[s]["shares"]}
                      for s in NONH if np.isfinite(F15[j, IDX[s]])}
            try:
                fv = holding_fair(c, models, KE0, 0.0)
                F15[j, IDX[t]] = fv
                U15[j, IDX[t]] = fv / c["price"] - 1
            except Exception:
                pass
    per_s, per_c, summ, _, _ = grid_metrics(F15, U15, I15, base)
    sc15, rk15, sel15 = score_rule(bI, bU, b_prob15)
    summ["opportunities_prob_x1_5"] = {"selected": [ORDER[i] for i in sel15], "prob_x1_5": {ORDER[i]: rnd(b_prob15[i]) for i in range(n) if np.isfinite(b_prob15[i])}}
    out_grids["mc15"] = {"label": GRID_LABEL["mc15"], "params": {"n_draws": N15, "sd_scale": 1.5, "seeds": "independentes por empresa (crc32 do ticker)",
                                                               "terminal_g_clip": [-0.03, 0.015]},
                         "spearman_irr": [rnd(x) for x in per_s["spearman_irr"]], "spearman_up": [rnd(x) for x in per_s["spearman_up"]],
                         "overlap7_irr": [rnd(x) for x in per_s["overlap7_irr"]], "overlap7_up": [rnd(x) for x in per_s["overlap7_up"]],
                         "summary": summ}
    for t in ORDER:
        per_company_grid[t]["mc15"] = per_c[t]
        per_company_grid[t]["mc15"]["prob_above_price_x1_5"] = rnd(b_prob15[IDX[t]])

    # ---------------- dependência das oportunidades em relação aos pesos (detalhe)
    ks_w = [k for k, (gg, _, _) in enumerate(flat) if gg == "pesos"]
    opp_detail = {}
    watch = list(dict.fromkeys(current_opp + [t for t, v in opp_by_grid["pesos"]["freq_selected"].items()]))
    for t in watch:
        i = IDX[t]
        sel_flags = []
        probs_t, ups_t = [], []
        for k in ks_w:
            _, _, sel = score_rule(res[k][2], res[k][1], prob_state[k])
            sel_flags.append(i in sel[:7])
            probs_t.append(prob_state[k][i])
            ups_t.append(res[k][1][i])
        by_mult = {}
        for wm in sorted(set(w[2] for w in W_GRID)):
            idx = [j for j, w in enumerate(W_GRID) if w[2] == wm]
            by_mult[f"{wm:.1f}"] = rnd(np.mean([sel_flags[j] for j in idx]))
        by_dcf = {}
        for wd in sorted(set(w[0] for w in W_GRID)):
            idx = [j for j, w in enumerate(W_GRID) if w[0] == wd]
            by_dcf[f"{wd:.1f}"] = rnd(np.mean([sel_flags[j] for j in idx]))
        opp_detail[t] = {"current": t in current_opp, "selected_share": rnd(np.mean(sel_flags)),
                         "prob_min": rnd(np.nanmin(probs_t)), "prob_max": rnd(np.nanmax(probs_t)),
                         "up_min": rnd(np.nanmin(ups_t)), "up_max": rnd(np.nanmax(ups_t)),
                         "selected_by_w_mult": by_mult, "selected_by_w_dcf": by_dcf,
                         "ternary": [{"w_dcf": W_GRID[j][0], "w_ddm": W_GRID[j][1], "w_mult": W_GRID[j][2], "selected": bool(sel_flags[j]),
                                      "prob": rnd(probs_t[j]), "upside": rnd(ups_t[j])} for j in range(len(W_GRID))]}

    # ---------------- pesos propostos por setor
    wmap = {t: proposed_weights(t) for t in NONH}
    pF, pU, pI, pMeth = eval_state({"wmap": wmap})
    p_prob = np.full(n, np.nan)
    for t in NONH:
        p_prob[IDX[t]] = prob_from_values(mcv[t], wmap[t], COMPS[t]["price"])
    p_score, p_rank, p_sel = score_rule(pI, pU, p_prob)
    bRU, pRU = rank_desc(bU), rank_desc(pU)
    prop_rows = []
    for t in ORDER:
        i = IDX[t]
        prop_rows.append({"ticker": t, "bucket": bucket_of(t), "weights_base": base_w.get(t) or {"sotp": 1.0},
                          "weights_proposed": wmap.get(t) or {"sotp": 1.0},
                          "fair_base": rnd(bF[i]), "fair_proposed": rnd(pF[i]), "fair_change": rnd(pF[i] / bF[i] - 1) if bF[i] else None,
                          "up_base": rnd(bU[i]), "up_proposed": rnd(pU[i]), "rank_up_base": rnd(bRU[i], 0), "rank_up_proposed": rnd(pRU[i], 0),
                          "prob_base": rnd(b_prob[i]), "prob_proposed": rnd(p_prob[i]),
                          "score_base": rnd(b_score[i], 3), "score_proposed": rnd(p_score[i], 3),
                          "rank_score_base": rnd(b_rank[i], 0), "rank_score_proposed": rnd(p_rank[i], 0),
                          "selected_base": i in b_sel[:7], "selected_proposed": i in p_sel[:7]})
    # diagnóstico por setor: sinal do DCF, múltiplos/DDM, DL/EV e dispersão de cada método na amostra conjunta
    diag = {}
    for b in list(PROPOSED) + ["demais"]:
        tks = [t for t in NONH if bucket_of(t) == b]
        if not tks:
            continue
        ii = [IDX[t] for t in tks]
        dcf, ddm, mul = bMeth[ii, 0], bMeth[ii, 1], bMeth[ii, 2]
        nd_ev = []
        for t in tks:
            c = COMPS[t]
            if c["tpl"] == "financial" or not c["mcap"]:
                continue
            ndb = M.num(((c["prem"].get("overrides") or {}).get("base") or {}).get("net_debt"), M.num(c["hist"]["balance"].get("net_debt")))
            nd_ev.append(ndb / (ndb + c["mcap"]) if ndb + c["mcap"] > 0 else np.nan)
        disp = {}
        for mi, mname in enumerate(("dcf", "ddm", "multiples")):
            vals = []
            for i in ii:
                x = MJ[:, i, mi]
                x = x[np.isfinite(x)]
                if len(x) and np.median(x) > 0:
                    vals.append((np.percentile(x, 95) - np.percentile(x, 5)) / abs(np.median(x)))
                elif len(x):
                    vals.append(np.nan)
            disp[mname] = rnd(np.nanmedian(vals)) if vals and np.isfinite(np.nanmedian(vals)) else None
        # pesos de mínima dispersão (p95−p5)/p50 do blend na amostra conjunta (diagnóstico, não recomendação)
        best = None
        for w in W_GRID:
            disp_w = []
            for t, i in zip(tks, ii):
                wd = weights_for(COMPS[t]["tpl"], w)
                Vj = {"dcf": MJ[:, i, 0], "ddm": MJ[:, i, 1], "multiples": MJ[:, i, 2]}
                f = blend(Vj, wd)
                f = f[np.isfinite(f)]
                if len(f) and np.median(f) > 0:
                    disp_w.append((np.percentile(f, 95) - np.percentile(f, 5)) / np.median(f))
            if disp_w:
                m_ = float(np.median(disp_w))
                if best is None or m_ < best[1] - 1e-12:
                    best = (w, m_)
        diag[b] = {"tickers": tks, "dcf_negative": int(np.sum(dcf < 0)), "n": len(tks),
                   "median_mult_over_ddm": rnd(np.nanmedian(mul / ddm)), "median_dcf_over_ddm": rnd(np.nanmedian(dcf / ddm)),
                   "median_nd_over_ev": rnd(np.nanmedian(nd_ev)) if nd_ev else None,
                   "dispersion_joint_p95_p5_over_p50": disp,
                   "min_dispersion_weights": {"w_dcf": best[0][0], "w_ddm": best[0][1], "w_mult": best[0][2], "dispersion": rnd(best[1])} if best else None}
    # impacto de um setor por vez (demais setores na base)
    by_bucket = {}
    base_sel7 = set(ORDER[i] for i in b_sel[:7])
    for bname in PROPOSED:
        wm1 = {t: wmap[t] for t in NONH if bucket_of(t) == bname}
        F1, U1, I1, _ = eval_state({"wmap": wm1})
        p1 = b_prob.copy()
        for t in wm1:
            p1[IDX[t]] = prob_from_values(mcv[t], wm1[t], COMPS[t]["price"])
        _, _, sel1 = score_rule(I1, U1, p1)
        s7 = [ORDER[i] for i in sel1[:7]]
        by_bucket[bname] = {"spearman_up_vs_base": rnd(spear(bU, U1)), "rule_top7": s7,
                            "enter": [t for t in s7 if t not in base_sel7], "leave": [t for t in ORDER if t in base_sel7 and t not in s7],
                            "fair_change_median": rnd(np.nanmedian([F1[IDX[t]] / bF[IDX[t]] - 1 for t in wm1 if bF[IDX[t]]]))}
    variants = {}
    for vname, ovr in VARIANTS.items():
        wmv = {t: (dict(ovr[bucket_of(t)]) if bucket_of(t) in ovr else wmap[t]) for t in NONH}
        Fv, Uv, Iv, _ = eval_state({"wmap": wmv})
        pv = np.full(n, np.nan)
        for t in NONH:
            pv[IDX[t]] = prob_from_values(mcv[t], wmv[t], COMPS[t]["price"])
        _, _, selv = score_rule(Iv, Uv, pv)
        rv = rank_desc(Uv)
        variants[vname] = {"override": ovr, "rule_top7": [ORDER[i] for i in selv[:7]], "spearman_up_vs_base": rnd(spear(bU, Uv)),
                           "top7_up": [ORDER[i] for i in sorted(topk(Uv, 7), key=lambda i: rv[i])],
                           "prob": {t: rnd(pv[IDX[t]]) for t in ("CEAB3", "LREN3", "SBFG3", "DIRR3", "COGN3", "PGMN3") if t in IDX}}
    proposed = {
        "variants": variants,
        "by_bucket": by_bucket,
        "buckets": {b: {"tickers": d["tickers"], "weights": d["weights"], "why": d["why"]} for b, d in PROPOSED.items()},
        "default": {"weights": DEFAULT_IND, "tickers": [t for t in NONH if bucket_of(t) == "demais"],
                    "why": "Educação, saúde, serviços, tecnologia, proteína, agro, combustíveis e turismo: mantém o padrão da especificação (50/25/25)."},
        "rows": prop_rows,
        "spearman_up_vs_base": rnd(spear(bU, pU)), "spearman_score_vs_base": rnd(spear(b_score, p_score)),
        "top7_up_base": [ORDER[i] for i in sorted(topk(bU, 7), key=lambda i: bRU[i])],
        "top7_up_proposed": [ORDER[i] for i in sorted(topk(pU, 7), key=lambda i: pRU[i])],
        "top15_up_base": [ORDER[i] for i in sorted(topk(bU, 15), key=lambda i: bRU[i])],
        "top15_up_proposed": [ORDER[i] for i in sorted(topk(pU, 15), key=lambda i: pRU[i])],
        "opportunities_base_rule": [ORDER[i] for i in b_sel], "opportunities_proposed_rule": [ORDER[i] for i in p_sel],
        "diagnostics_by_bucket": diag,
    }

    # ---------------- lista robusta consolidada
    def robust(grid, metric, thr):
        return [t for t in ORDER if (per_company_grid[t][grid].get(f"top7_{metric}") or 0) >= thr - 1e-12]
    robust_lists = {"definition": "top 7 em ≥ 50% / ≥ 80% das combinações; headline = amostra conjunta (todas as grades ao mesmo tempo)"}
    for g in DET_GRIDS + ["mc15", "conjunta"]:
        robust_lists[g] = {f"{m}_{lab}": sorted(robust(g, m, thr), key=lambda t: -(per_company_grid[t][g].get(f"top7_{m}") or 0))
                           for m in ("irr", "up") for thr, lab in ((0.5, "ge50"), (0.8, "ge80"))}
    allg = DET_GRIDS + ["mc15", "conjunta"]
    for m in ("irr", "up"):
        for thr, lab in ((0.5, "ge50"), (0.8, "ge80")):
            robust_lists.setdefault("todas_as_grades", {})[f"{m}_{lab}"] = [
                t for t in ORDER if all((per_company_grid[t][g].get(f"top7_{m}") or 0) >= thr - 1e-12 for g in allg)]

    # ---------------- JSON
    bRI = rank_desc(bI)
    companies = []
    long = []
    for t in ORDER:
        c = COMPS[t]
        i = IDX[t]
        r = rows[t]
        companies.append({
            "ticker": t, "name": r.get("name"), "group": r.get("group"), "bucket": bucket_of(t), "template": c["tpl"],
            "price": c["price"], "research_mtime": c["mtime"], "research_sha1": c["sha1"],
            "base": {"fair": rnd(bF[i]), "upside": rnd(bU[i]), "irr": rnd(bI[i]), "rank_irr": rnd(bRI[i], 0), "rank_up": rnd(bRU[i], 0),
                     "prob_mc": rnd(b_prob[i]), "score": rnd(b_score[i], 3), "rank_score": rnd(b_rank[i], 0),
                     "selected_rule": i in b_sel[:7], "values": {"dcf": rnd(bMeth[i, 0]), "ddm": rnd(bMeth[i, 1]), "multiples": rnd(bMeth[i, 2])},
                     "weights": base_w.get(t) or {"sotp": 1.0}},
            "overview": {"fair_value": r.get("fair_value"), "upside": r.get("upside"), "irr_implied": r.get("irr_implied"),
                         "score": r.get("score"), "rank": r.get("rank"), "prob_mc": r.get("prob_mc"), "opportunity": t in current_opp},
            "grids": per_company_grid[t],
            "opportunity_vs_weights": opp_detail.get(t),
        })
        for g, d in per_company_grid[t].items():
            long.append({"ticker": t, "grid": g, **d})
    out = {
        "meta": {"generated_at": datetime.now().isoformat(timespec="seconds"), "valuation_date": M.VAL_DATE.isoformat(), "ke_base": KE0,
                 "prices": "data/market/quotes.json (EAGORA_SNAPSHOT=1)", "engine": "pipeline/model.py (importado, sem alteração)",
                 "n_companies": n, "n_holdings": len(HOLD), "current_opportunities": current_opp,
                 "overview_generated_at": ov.get("generated_at"), "runtime_s": None,
                 "settings": {"n_joint": a.n_joint, "n_mc15": a.n_mc15, "n_mc_prob": a.n_mc, "quick": a.quick,
                              "weights_grid": "66 vetores {dcf, ddm, múltiplos} passo 0,1; bancos {ddm = dcf+ddm, múltiplos}",
                              "ke_grid": KE_GRID, "g_shift_grid": G_GRID, "multiples_scale_grid": MULT_GRID,
                              "margin_shift_grid": SHOCK_GRID, "growth_shift_grid": SHOCK_GRID, "kd_shock": KD_SHOCK, "kd_modes": KD_MODES},
                 "ranking": "rank 1 = maior TIR implícita / maior upside; holdings (SOTP) sem TIR ficam fora do ranking por TIR",
                 "base_check": {"divergences_vs_overview": check, "prob_divergences_vs_overview": prob_check,
                                "prob_exact_engine_mc": a.n_mc == M.N_MC,
                                "score_max_abs_diff": rnd(max(score_diff) if score_diff else None, 3),
                                "rule_selection_now": [ORDER[i] for i in b_sel],
                                "prob_near_cutoff": {ORDER[i]: rnd(b_prob[i]) for i in range(n)
                                                     if np.isfinite(b_prob[i]) and abs(b_prob[i] - 0.45) <= 0.05 and np.isfinite(bI[i]) and bI[i] >= 0.20}},
                 "method_stats": {"dcf_negative": [ORDER[i] for i in range(n) if np.isfinite(bMeth[i, 0]) and bMeth[i, 0] < 0],
                                  "median_mult_over_ddm": rnd(np.nanmedian([bMeth[i, 2] / bMeth[i, 1] for i in range(n)
                                                                           if np.isfinite(bMeth[i, 2]) and np.isfinite(bMeth[i, 1]) and bMeth[i, 1] > 0])),
                                  "median_dcf_over_ddm": rnd(np.nanmedian([bMeth[i, 0] / bMeth[i, 1] for i in range(n)
                                                                          if np.isfinite(bMeth[i, 0]) and np.isfinite(bMeth[i, 1]) and bMeth[i, 1] > 0]))},
                 "research_versions": {t: {"mtime": COMPS[t]["mtime"], "sha1": COMPS[t]["sha1"]} for t in ORDER}},
        "tickers": ORDER,
        "base": {"fair": [rnd(x) for x in bF], "upside": [rnd(x) for x in bU], "irr": [rnd(x) for x in bI],
                 "rank_irr": [rnd(x, 0) for x in bRI], "rank_up": [rnd(x, 0) for x in bRU], "prob_mc": [rnd(x) for x in b_prob],
                 "score": [rnd(x, 3) for x in b_score], "rank_score": [rnd(x, 0) for x in b_rank],
                 "top7_irr": [ORDER[i] for i in sorted(topk(bI, 7), key=lambda i: bRI[i])],
                 "top15_irr": [ORDER[i] for i in sorted(topk(bI, 15), key=lambda i: bRI[i])],
                 "top7_up": [ORDER[i] for i in sorted(topk(bU, 7), key=lambda i: bRU[i])],
                 "top15_up": [ORDER[i] for i in sorted(topk(bU, 15), key=lambda i: bRU[i])]},
        "grids": out_grids,
        "companies": companies,
        "long": long,
        "robust_lists": robust_lists,
        "opportunities_vs_weights": {"current": current_opp, "summary": opp_by_grid["pesos"], "by_grid": opp_by_grid, "detail": opp_detail,
                                     "mc_sd_x1_5": out_grids["mc15"]["summary"]["opportunities_prob_x1_5"]["selected"]},
        "proposed_weights": proposed,
    }
    out["meta"]["runtime_s"] = round(time.time() - t0, 1)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(OUT_JSON, "w"), ensure_ascii=False, separators=(",", ":"))
    write_md(out)
    print(f"ok: {OUT_JSON.relative_to(ROOT)} e {OUT_MD.relative_to(ROOT)}  [{time.time() - t0:.0f}s]")


def write_md(o):
    """Relatório em Markdown a partir do JSON (todas as tabelas são geradas)."""
    T = o["tickers"]
    comp = {c["ticker"]: c for c in o["companies"]}
    G = o["grids"]
    rl = o["robust_lists"]
    cur = o["meta"]["current_opportunities"]
    L = []
    L.append("# Robustez do valuation: pesos do blend e premissas (26/10/2026)")
    L.append("")
    L.append(f"Gerado em {o['meta']['generated_at']} por `pipeline/tests/robustness.py`, com o motor `pipeline/model.py` sem "
             f"alteração e a foto de preços `data/market/quotes.json`. São {o['meta']['n_companies']} empresas "
             f"({o['meta']['n_holdings']} holdings por SOTP). Ke base de 25%. Dados para gráfico: `data/tests/robustness.json`.")
    L.append("")
    # ---- resumo
    sj = G["conjunta"]["summary"]
    L.append("## Resumo")
    L.append("")
    L.append(f"- **A TIR implícita não depende dos pesos, do Ke nem dos múltiplos.** Ela é a taxa que zera o DDM ao preço de hoje, "
             f"então só muda com g, margem, crescimento, Kd e Monte Carlo. O ranking por TIR é estável: Spearman mediano de "
             f"{fr(sj['spearman_irr']['median'])} (mínimo {fr(sj['spearman_irr']['min'])}) na amostra conjunta de {num(sj['n'], 0)} combinações.")
    sw = G["pesos"]["summary"]
    ms = o["meta"]["method_stats"]
    L.append(f"- **No ranking por upside, a ordem geral resiste aos pesos, mas o topo não.** Nas 66 combinações de pesos, o Spearman "
             f"mediano é {fr(sw['spearman_up']['median'])} (mínimo {fr(sw['spearman_up']['min'])}), porém só "
             f"{pct(sw['overlap7_up_mean'])} do top 7 por upside se mantém em média. Na amostra conjunta, o Spearman mediano é "
             f"{fr(sj['spearman_up']['median'])} (mínimo {fr(sj['spearman_up']['min'])}). Causa: na mediana, os múltiplos-alvo valem "
             f"{fr(ms['median_mult_over_ddm'])}× o DDM a Ke 25%, e {len(ms['dcf_negative'])} empresas têm DCF negativo, que o motor "
             f"trunca em zero sem tirar o peso.")
    L.append(f"- **Lista robusta por TIR** (top 7 na amostra conjunta): ≥ 80%: {lst_txt(rl['conjunta']['irr_ge80'])}; "
             f"≥ 50%: {lst_txt(rl['conjunta']['irr_ge50'])}.")
    L.append(f"- **Lista robusta por upside** (top 7 na amostra conjunta): ≥ 80%: {lst_txt(rl['conjunta']['up_ge80'])}; "
             f"≥ 50%: {lst_txt(rl['conjunta']['up_ge50'])}.")
    core_i = [t for t in rl["conjunta"]["irr_ge50"] if t in rl["conjunta"]["up_ge50"]]
    L.append(f"- **Núcleo robusto** (top 7 por TIR e por upside em ≥ 50% da amostra conjunta): {lst_txt(core_i)}. "
             f"Em todas as grades ao mesmo tempo (≥ 50% em cada uma): TIR {lst_txt(rl['todas_as_grades']['irr_ge50'])}; "
             f"upside {lst_txt(rl['todas_as_grades']['up_ge50'])}.")
    ow = o["opportunities_vs_weights"]["summary"]
    det = o["opportunities_vs_weights"]["detail"]
    sel_now = o["meta"]["base_check"]["rule_selection_now"]
    out_now = [t for t in cur if t not in sel_now]
    L.append(f"- **As 7 oportunidades atuais ({', '.join(cur)}) dependem dos pesos e já das revisões.** Com as premissas revisadas e os "
             f"pesos atuais, a regra do `build.py` seleciona {len(sel_now[:7])} ({lst_txt(sel_now[:7])})"
             + (f"; {lst_e(out_now)} {'ficou' if len(out_now) == 1 else 'ficaram'} fora pelos filtros de P(MC) ≥ 45% ou TIR ≥ 20%" if out_now else "")
             + f". Nos 66 vetores de pesos (upside, P(MC) e escore recalculados), a regra mantém em média {num(ow['kept_mean'], 1)} das 7 "
             f"(mínimo {ow['kept_min']}) e a lista sai idêntica em {pct(ow['identical_share'])}. Fração de vetores com cada empresa selecionada: "
             + "; ".join(f"{t} {pct(det[t]['selected_share'])}"
                         + ("" if det[t]["selected_share"] in (0, 1) else f" ({cond_txt(det[t]['selected_by_w_mult'], 'w_múlt')}; {cond_txt(det[t]['selected_by_w_dcf'], 'w_DCF')})")
                         for t in cur if t in det) + ".")
    pw = o["proposed_weights"]
    vv = pw["variants"]
    L.append(f"- **Pesos propostos por setor:** o Spearman do upside contra a base fica em {fr(pw['spearman_up_vs_base'])} e o do escore em "
             f"{fr(pw['spearman_score_vs_base'])}. A regra passa a selecionar {lst_txt(pw['opportunities_proposed_rule'][:7])}, "
             f"contra {lst_txt(pw['opportunities_base_rule'][:7])} hoje. O peso dos múltiplos no varejo decide a cauda da lista: "
             + "; ".join(f"{k}: {lst_txt(d['rule_top7'])}" for k, d in vv.items() if k.startswith("varejo")) + ".")
    L.append("")
    # ---- base
    bc = o["meta"]["base_check"]
    L.append("## Base e reprodução")
    L.append("")
    dv = bc["divergences_vs_overview"]
    L.append(f"A base é o motor rodado agora com as premissas atuais. Ele reproduz o `overview.json` ({o['meta']['overview_generated_at']}) "
             f"em valor justo e TIR, exceto em {len(dv)} empresas cujas premissas (ou cuja controlada) mudaram depois do build: "
             + (", ".join(f"{d['ticker']} ({num(d['fair_overview'])} → {num(d['fair_engine'])})" for d in dv) or "nenhuma") + ". "
             + ((("A P(MC) recalculada bate com a do app em todas as empresas sem mudança de premissa. " if not bc["prob_divergences_vs_overview"]
                  else f"A P(MC) difere da do app em {len(bc['prob_divergences_vs_overview'])} empresas sem mudança no valor justo "
                       f"(revisão de desvios em `uncertainty`): " + ", ".join(f"{d['ticker']} {pct(d['prob_overview'], 1)} → {pct(d['prob_engine'], 1)}" for d in bc["prob_divergences_vs_overview"]) + ". "))
                if bc["prob_exact_engine_mc"] else "Esta rodada usou menos sorteios que o motor, então a P(MC) difere por ruído amostral. ")
             + f"Com as premissas atuais, a regra de oportunidades seleciona {lst_txt(bc['rule_selection_now'])}.")
    near = bc.get("prob_near_cutoff") or {}
    if near:
        L.append("")
        L.append("Com TIR ≥ 20% e P(MC) a até 5 p.p. do corte de 45%: " + ", ".join(f"{t} ({pct(v, 1)})" for t, v in near.items())
                 + ". Para essas empresas, a seleção depende de detalhes (sorteios, pesos, revisões).")
    L.append("")
    b = o["base"]
    L.append(f"Top 7 da base por TIR: {lst_txt(b['top7_irr'])}. Top 7 por upside: {lst_txt(b['top7_up'])}.")
    L.append("")
    # ---- estabilidade por grade
    L.append("## Estabilidade do ranking por grade")
    L.append("")
    L.append("Spearman de cada combinação contra a base (mediana / mínimo), fração média do top 7 da base que continua no top 7 e "
             "número médio de oportunidades atuais que a regra mantém (de 7).")
    L.append("")
    L.append("| Grade | Combinações | Spearman TIR | Spearman upside | Spearman escore | Top 7 TIR mantido | Top 7 upside mantido | Oportunidades mantidas |")
    L.append("|---|---:|---|---|---|---:|---:|---:|")
    for g in DET_GRIDS + ["mc15", "conjunta"]:
        s = G[g]["summary"]
        si, su = s["spearman_irr"], s["spearman_up"]
        ss = s.get("spearman_score")
        oo = s.get("opportunities")
        inv = " (invariante)" if g in ("pesos", "ke", "multiplos") else ""
        L.append(f"| {GRID_LABEL[g]} | {s['n']} | {fr(si['median'])} / {fr(si['min'])}{inv} | {fr(su['median'])} / {fr(su['min'])} | "
                 f"{(fr(ss['median']) + ' / ' + fr(ss['min'])) if ss else '—'} | {pct(s['overlap7_irr_mean'])} | {pct(s['overlap7_up_mean'])} | "
                 f"{num(oo['kept_mean'], 1) if oo else '—'} |")
    L.append("")
    L.append("Na amostra conjunta e no MC ×1,5, o escore e a regra não são recalculados, porque exigiriam um Monte Carlo por combinação. "
             "Nas grades determinísticas, P(MC) é recalculada com o Monte Carlo do motor (5.000 sorteios, semente 7).")
    L.append("")
    # ---- frequência no top 7 / top 15
    L.append("## Frequência no top 7 e no top 15 por empresa")
    L.append("")
    L.append("Frequências na amostra conjunta (C), na grade de pesos (P) e no Monte Carlo ×1,5 (MC). A faixa p5–p95 do valor justo é a da "
             "amostra conjunta. A tabela lista as empresas que aparecem no top 15 da base ou em pelo menos 5% das combinações; as demais estão no JSON.")
    L.append("")
    L.append("| Empresa | Preço | VJ base | VJ p5–p95 (C) | TIR base (rank) | Upside base (rank) | Top 7 TIR C | Top 15 TIR C | Top 7 TIR MC | Top 7 upside C | Top 15 upside C | Top 7 upside P | Top 7 upside MC | Regra (pesos) |")
    L.append("|---|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    def keyf(t):
        c = comp[t]["grids"]["conjunta"]
        return -((c["top7_irr"] or 0) + (c["top7_up"] or 0) + 0.5 * ((c["top15_irr"] or 0) + (c["top15_up"] or 0)))
    shown = [t for t in T if (comp[t]["base"]["rank_irr"] or 99) <= 15 or (comp[t]["base"]["rank_up"] or 99) <= 15
             or (comp[t]["grids"]["conjunta"]["top15_irr"] or 0) >= 0.05 or (comp[t]["grids"]["conjunta"]["top15_up"] or 0) >= 0.05]
    for t in sorted(shown, key=keyf):
        c = comp[t]
        gj, gp, gm = c["grids"]["conjunta"], c["grids"]["pesos"], c["grids"]["mc15"]
        bb = c["base"]
        star = " ★" if t in cur else ""
        L.append(f"| {t}{star} | {num(c['price'])} | {num(bb['fair'])} | {num(gj['fair_p5'])}–{num(gj['fair_p95'])} | "
                 f"{pct(bb['irr'], 1)} ({ri(bb['rank_irr'])}) | {pct(bb['upside'])} ({ri(bb['rank_up'])}) | "
                 f"{pct(gj['top7_irr'])} | {pct(gj['top15_irr'])} | {pct(gm['top7_irr'])} | {pct(gj['top7_up'])} | {pct(gj['top15_up'])} | "
                 f"{pct(gp['top7_up'])} | {pct(gm['top7_up'])} | {pct(gp.get('opp_selected'))} |")
    L.append("")
    L.append("★ = oportunidade atual. A coluna “Regra (pesos)” dá a fração das 66 combinações de pesos em que a regra do app (TIR ≥ 20%, P(MC) ≥ 45%, "
             "Altman fora de risco, confiança não baixa, ordem pelo escore) põe a empresa entre as 7.")
    L.append("")
    L.append("### Faixa p5–p95 do valor justo por grade (todas as empresas)")
    L.append("")
    L.append("| Empresa | Preço | VJ base | Pesos | Ke | g | Múltiplos | Margem × cresc. | Kd | MC ×1,5 | Conjunta |")
    L.append("|---|---:|---:|---|---|---|---|---|---|---|---|")
    for t in sorted(T, key=lambda t: (comp[t]["base"]["rank_up"] or 99)):
        c = comp[t]
        cells = []
        for g in DET_GRIDS + ["mc15", "conjunta"]:
            d = c["grids"][g]
            cells.append(f"{num(d['fair_p5'])}–{num(d['fair_p95'])}")
        L.append(f"| {t} | {num(c['price'])} | {num(c['base']['fair'])} | " + " | ".join(cells) + " |")
    L.append("")
    # ---- lista robusta
    L.append("## Lista robusta")
    L.append("")
    L.append("Empresas no top 7 em pelo menos 80% ou 50% das combinações de cada grade.")
    L.append("")
    L.append("| Grade | TIR ≥ 80% | TIR ≥ 50% | Upside ≥ 80% | Upside ≥ 50% |")
    L.append("|---|---|---|---|---|")
    for g in DET_GRIDS + ["mc15", "conjunta", "todas_as_grades"]:
        d = rl[g]
        lab = GRID_LABEL.get(g, "Em todas as grades ao mesmo tempo")
        L.append(f"| {lab} | {lst_txt(d['irr_ge80'])} | {lst_txt(d['irr_ge50'])} | {lst_txt(d['up_ge80'])} | {lst_txt(d['up_ge50'])} |")
    L.append("")
    # ---- oportunidades x pesos
    L.append("## As 7 oportunidades atuais e os pesos")
    L.append("")
    L.append("Para cada um dos 66 vetores de pesos, o teste recalcula o upside, a P(valor justo > preço) e o escore e reaplica a regra do `build.py`. "
             "A P(MC) sai do mesmo Monte Carlo do motor, com os valores por método guardados em cada sorteio e o blend refeito. "
             "A TIR e os demais fatores do escore não dependem dos pesos.")
    L.append("")
    L.append("| Empresa | Selecionada (% dos pesos) | Condição (≥ 50% dos vetores) | P(MC) mín–máx | Upside mín–máx | Seleção por w_múlt = 0; 0,1; …; 1 | Seleção por w_DCF = 0; 0,1; …; 1 |")
    L.append("|---|---:|---|---|---|---|---|")
    for t, d in sorted(det.items(), key=lambda kv: (not kv[1]["current"], -(kv[1]["selected_share"] or 0))):
        star = " ★" if d["current"] else ""
        bm = " ".join(pct(v) for v in d["selected_by_w_mult"].values())
        bd = " ".join(pct(v) for v in d["selected_by_w_dcf"].values())
        cond = f"{cond_txt(d['selected_by_w_mult'], 'w_múlt')}; {cond_txt(d['selected_by_w_dcf'], 'w_DCF')}"
        L.append(f"| {t}{star} | {pct(d['selected_share'])} | {cond} | {pct(d['prob_min'])}–{pct(d['prob_max'])} | {pct(d['up_min'])}–{pct(d['up_max'])} | {bm} | {bd} |")
    L.append("")
    dist = ow["kept_dist"]
    L.append("Quantas das 7 atuais a regra mantém, em número de combinações: " + ", ".join(f"{k} mantidas: {v}" for k, v in dist.items() if v) + ".")
    L.append("")
    og = o["opportunities_vs_weights"]["by_grid"]
    L.append("Seleção pela regra nas demais grades (fração de combinações em que cada empresa está entre as 7):")
    L.append("")
    for g in DET_GRIDS:
        fs = og[g]["freq_selected"]
        L.append(f"- {GRID_LABEL[g]}: " + ", ".join(f"{t} {pct(v)}" for t, v in fs.items()) + f" (lista idêntica em {pct(og[g]['identical_share'])}).")
    L.append(f"- Monte Carlo com desvios ×1,5 (P(MC) recalculada com os pesos da base): {lst_txt(o['opportunities_vs_weights']['mc_sd_x1_5'])}.")
    L.append("")
    # ---- pesos propostos
    L.append("## Pesos propostos por setor")
    L.append("")
    L.append("| Setor | Empresas | Pesos | Justificativa |")
    L.append("|---|---|---|---|")
    def wtxt(w):
        names = {"dcf": "DCF", "ddm": "DDM", "multiples": "Múltiplos", "pe": "P/L", "ev_ebitda": "EV/EBITDA", "pbv": "P/VP"}
        return " / ".join(f"{names.get(k, k)} {int(round(v * 100))}%" for k, v in w.items())
    for bname, d in pw["buckets"].items():
        L.append(f"| {bname} | {', '.join(d['tickers'])} | {wtxt(d['weights'])} | {d['why']} |")
    L.append(f"| demais | {', '.join(pw['default']['tickers'])} | {wtxt(pw['default']['weights'])} | {pw['default']['why']} |")
    L.append("")
    L.append("Diagnóstico por setor, com base nos valores da base e na amostra conjunta. A dispersão é (p95 − p5) / p50 de cada método "
             "sob Ke, g, múltiplos, margem, crescimento e Kd. Os pesos de mínima dispersão minimizam a dispersão mediana do blend no setor. "
             "São só uma checagem, porque payout, capex e capital de giro não são choques da grade e o DDM e o DCF dependem deles.")
    L.append("")
    L.append("| Setor | n | DCF < 0 | Múltiplos/DDM (mediana) | DCF/DDM (mediana) | DL/EV mercado | Dispersão DCF | Dispersão DDM | Dispersão múltiplos | Pesos de mínima dispersão |")
    L.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for bname, d in pw["diagnostics_by_bucket"].items():
        ds = d["dispersion_joint_p95_p5_over_p50"]
        mw = d["min_dispersion_weights"]
        L.append(f"| {bname} | {d['n']} | {d['dcf_negative']} | {fr(d['median_mult_over_ddm'])} | {fr(d['median_dcf_over_ddm'])} | {pct(d['median_nd_over_ev'])} | "
                 f"{fr(ds['dcf'])} | {fr(ds['ddm'])} | {fr(ds['multiples'])} | "
                 f"{('DCF ' + str(mw['w_dcf']) + ' / DDM ' + str(mw['w_ddm']) + ' / Múlt ' + str(mw['w_mult'])) if mw else '—'} |")
    L.append("")
    L.append("Impacto dos pesos propostos (empresas cujo rank por upside ou cuja seleção muda, além do top 15 de cada lado):")
    L.append("")
    L.append("| Empresa | Setor | VJ base → proposto | Δ VJ | Upside base → proposto | Rank upside | P(MC) base → proposta | Rank escore | Regra |")
    L.append("|---|---|---|---:|---|---|---|---|---|")
    pr_rows = [r for r in pw["rows"] if (r["rank_up_base"] or 99) <= 15 or (r["rank_up_proposed"] or 99) <= 15
               or r["selected_base"] != r["selected_proposed"]]
    for r in sorted(pr_rows, key=lambda r: r["rank_up_proposed"] or 99):
        sel = ("entra" if r["selected_proposed"] and not r["selected_base"] else "sai" if r["selected_base"] and not r["selected_proposed"]
               else "mantém" if r["selected_base"] else "—")
        L.append(f"| {r['ticker']} | {r['bucket']} | {num(r['fair_base'])} → {num(r['fair_proposed'])} | {pct(r['fair_change'])} | "
                 f"{pct(r['up_base'])} → {pct(r['up_proposed'])} | {ri(r['rank_up_base'])} → {ri(r['rank_up_proposed'])} | "
                 f"{pct(r['prob_base'])} → {pct(r['prob_proposed'])} | "
                 f"{ri(r['rank_score_base'])} → {ri(r['rank_score_proposed'])} | {sel} |")
    L.append("")
    L.append(f"Top 7 por upside: base {lst_txt(pw['top7_up_base'])}; proposto {lst_txt(pw['top7_up_proposed'])}. "
             f"Regra de oportunidades: base {lst_txt(pw['opportunities_base_rule'][:7])}; proposto {lst_txt(pw['opportunities_proposed_rule'][:7])}.")
    L.append("")
    L.append("Decomposição, aplicando os pesos propostos a um setor por vez (os demais ficam na base):")
    L.append("")
    L.append("| Setor alterado | Δ VJ mediano do setor | Spearman upside vs base | Entram na regra | Saem da regra |")
    L.append("|---|---:|---:|---|---|")
    for bname, d in pw["by_bucket"].items():
        L.append(f"| {bname} | {pct(d['fair_change_median'])} | {fr(d['spearman_up_vs_base'])} | {lst_txt(d['enter'])} | {lst_txt(d['leave'])} |")
    L.append("")
    L.append("Sensibilidade da proposta às escolhas mais discutíveis (os demais setores ficam na proposta):")
    L.append("")
    L.append("| Variante | Regra (7) | Top 7 upside | Spearman upside vs base | P(MC): CEAB3 / LREN3 / SBFG3 / DIRR3 / COGN3 |")
    L.append("|---|---|---|---:|---|")
    for vname, d in pw["variants"].items():
        pp = d["prob"]
        L.append(f"| {vname} | {lst_txt(d['rule_top7'])} | {lst_txt(d['top7_up'])} | {fr(d['spearman_up_vs_base'])} | "
                 + " / ".join(pct(pp.get(t)) for t in ("CEAB3", "LREN3", "SBFG3", "DIRR3", "COGN3")) + " |")
    L.append("")
    # ---- achados
    L.append("## Achados sobre o motor e limitações")
    L.append("")
    L.append(f"- **DCF negativo entra como zero e mantém o peso** (`max(0, x)` no blend). Isso ocorre em {len(ms['dcf_negative'])} empresas "
             f"({', '.join(ms['dcf_negative'])}): cada 10 p.p. de peso no DCF corta cerca de 10% do valor justo, sem informação nova. "
             "Melhor seria tirar o método do blend quando o patrimônio do DCF for negativo, ou trocá-lo pelo DDM.")
    L.append(f"- **Os múltiplos-alvo não são coerentes com Ke 25%.** Um P/L de 9–12x com g 5% e ROE 17% equivale a um custo de capital próprio "
             f"de cerca de 11–13%. A P/L justa a Ke 25%, g 5% e ROE 15–20% fica em 3,5–4x. Na mediana, o valor por múltiplos é "
             f"{fr(ms['median_mult_over_ddm'])}× o do DDM. Por isso o peso dos múltiplos é o principal motor do upside, e os pesos "
             "propostos limitam os múltiplos a 20–40%.")
    L.append("- **O DCF é o método mais disperso** (tabela de diagnóstico). Com o patrimônio residual EV − DL, um erro pequeno no EV vira um "
             "erro grande no valor por ação quando a DL é grande. O peso padrão de 50% no DCF é a maior fonte de fragilidade do valor justo "
             "nos setores alavancados.")
    L.append("- **Holding com controlada de valor justo zero:** `value_holding` testa `models[tk].get('fair_value')` pela verdade do valor, "
             "então 0,0 vira o valor de mercado da controlada. Isso afeta SIMH3 quando MOVI3 ou VAMO3 chegam a zero, por exemplo com peso 100% no DCF.")
    kdg = o["grids"]["kd"]
    kdi = [k for k, p in enumerate(kdg["params"]) if p.get("kd_mode") == "both"]
    if kdi:
        irr_kd = kdg["matrix"]["irr"][kdi[0]]
        lost = [t for t in cur if (o["base"]["irr"][T.index(t)] or 0) >= 0.20 and (irr_kd[T.index(t)] or 0) < 0.20]
        if lost:
            L.append(f"- **Kd +300 bp derruba a TIR de {lst_e(lost)} para menos de 20%** ("
                     + ", ".join(f"{t} {pct(o['base']['irr'][T.index(t)], 1)} → {pct(irr_kd[T.index(t)], 1)}" for t in lost)
                     + "), e a regra os exclui. O corte de TIR de 20% é uma aresta para empresas alavancadas sob estresse de juros.")
    mg = o["grids"]["margem_cresc"]
    km = [k for k, p in enumerate(mg["params"]) if p.get("dm") == -0.02 and p.get("dgr") == 0.0]
    if km and "BEEF3" in T:
        ib = T.index("BEEF3")
        L.append("- **Choque de ±2 p.p. de margem é desproporcional em negócios de margem fina** (BEEF3 cerca de 8,5%, ASAI3, GMAT3 e VBBR3 com 4–6%): "
                 f"em BEEF3, −2 p.p. levam a TIR de {pct(o['base']['irr'][ib], 1)} a {pct(mg['matrix']['irr'][km[0]][ib], 1)} e o upside de "
                 f"{pct(o['base']['upside'][ib])} a {pct(mg['matrix']['upside'][km[0]][ib])}. Isso explica boa parte da faixa p5–p95 larga desses "
                 "nomes na amostra conjunta.")
    L.append("- **Kd +300 bp nos bancos:** o template financeiro não tem custo de dívida, então esses choques não mudam bancos. Margem ±2 p.p. vira ROE ±2 p.p. "
             "no template financeiro, que é a convenção do motor.")
    L.append("- Na amostra conjunta e no MC ×1,5, a regra de oportunidades não é recalculada (P(MC) exigiria um Monte Carlo por combinação). "
             "No MC ×1,5, os sorteios são independentes entre empresas, o caso conservador para a estabilidade do ranking.")
    L.append("")
    L.append("## Como reproduzir")
    L.append("")
    L.append("```bash")
    L.append(".venv/bin/python pipeline/tests/robustness.py            # completo")
    L.append(".venv/bin/python pipeline/tests/robustness.py --quick    # rápido (menos sorteios)")
    L.append("```")
    L.append("")
    st = o["meta"]["settings"]
    L.append(f"Parâmetros desta rodada: amostra conjunta de {num(st['n_joint'], 0)} combinações, MC ×1,5 com {num(st['n_mc15'], 0)} "
             f"sorteios por empresa e P(MC) com {num(st['n_mc_prob'], 0)} sorteios. Tempo: {num(o['meta']['runtime_s'], 0)} s.")
    OUT_MD.write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()

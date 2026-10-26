"""Referência Python (pipeline/model.py) para os testes de paridade do motor TS (lib/valuation.ts).

Uso: python tests/pyref.py 0.20 0.25 0.30
Saída (stdout): {"<ke>": {"<TICKER>": {"fair_value", "irr_implied", "irr_3y"}}}

- Preço = companies[].price_ref de data/app/overview.json (o mesmo usado no lado TS).
- Market cap pré-eleição/atual = os gravados em data/model/{T}.json (mesmas entradas do WACC da rodada do estudo).
- Holdings: controladas "fair" reavaliadas no mesmo Ke e custo de holding capitalizado a (Ke − g)
  (model.KE é trocado temporariamente, pois value_holding usa a constante do módulo).
- Cotações: EAGORA_SNAPSHOT=1 (foto do estudo). Componentes "market" de holdings sem cotação na foto
  recebem o preço implícito gravado no modelo, para o teste não depender da rede.
"""
import json
import os
import sys
from pathlib import Path

os.environ["EAGORA_SNAPSHOT"] = "1"
sys.dont_write_bytecode = True  # não grava __pycache__ em pipeline/ (fora de tests/)
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline"))
import model as M  # noqa: E402
import build as B  # noqa: E402  (só funções; main() fica sob __main__)


def load(p):
    with open(p) as fh:
        return json.load(fh)


def _clean(x):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return x if x == x and abs(x) != float("inf") else None


def overview():
    return load(ROOT / "data" / "app" / "overview.json")


def price_of(tk, ov=None):
    ov = ov or overview()
    for c in ov["companies"]:
        if c["ticker"] == tk:
            return c.get("price_ref")
    return None


def value_industrial(tk, ke, price):
    prem = load(ROOT / "research" / f"{tk}.json")
    hist = load(ROOT / "data" / "hist" / f"{tk}.json")
    mj = load(ROOT / "data" / "model" / f"{tk}.json")
    mcap_pre, mcap = mj.get("mcap_pre_election"), mj.get("mcap")
    return M.value_company(prem, hist, ke=ke, price=price, mcap=mcap_pre or mcap, mcap_now=mcap)


def _seed_market_quotes(prem, models):
    """Componentes 'market' sem cotação na foto: preço implícito do modelo gravado (sem rede)."""
    snap = load(ROOT / "data" / "market" / "quotes.json")
    stored = load(ROOT / "data" / "model" / f"{prem['ticker']}.json")
    by_tk = {c.get("ticker"): c for c in stored.get("components", [])}
    for c in (prem.get("sotp") or {}).get("components", []):
        tk = c.get("ticker")
        if not tk or c.get("method") == "fixed" or (snap.get(tk) or {}).get("price"):
            continue
        n = None
        if tk in models and (models[tk].get("shares") or {}).get("outstanding_mn"):
            msh = models[tk]["shares"]
            n = msh["outstanding_mn"] / (msh.get("per_unit") or 1)
        elif (ROOT / "data" / "hist" / f"{tk}.json").exists():
            hh = load(ROOT / "data" / "hist" / f"{tk}.json")
            n = M.num((hh.get("shares") or {}).get("outstanding")) / 1e6 / (hh.get("shares_per_unit") or 1)
        if not n and c.get("shares_mn"):
            n = M.num(c["shares_mn"])
        v = (by_tk.get(tk) or {}).get("value_mkt_100")
        if n and v:
            M._quote_cache[tk] = {"price": v / n, "source": "implícito no modelo gravado"}


def value_holding(tk, ke, price, ov):
    prem = load(ROOT / "research" / f"{tk}.json")
    hist = load(ROOT / "data" / "hist" / f"{tk}.json")
    models = {}
    for c in (prem.get("sotp") or {}).get("components", []):
        sub = c.get("ticker")
        if c.get("method") == "fair" and sub and (ROOT / "research" / f"{sub}.json").exists():
            models[sub] = value_industrial(sub, ke, price_of(sub, ov))
    _seed_market_quotes(prem, models)
    old = M.KE
    M.KE = ke
    try:
        return M.value_holding(prem, hist, models, price=price)
    finally:
        M.KE = old


def engines_from_model(ov):
    """Motor TS reconstruído do data/model atual (build.engine), para comparar entradas coerentes
    quando data/app ainda não foi remontado depois de uma revisão do modelo."""
    out = {}
    for c in ov["companies"]:
        mp = ROOT / "data" / "model" / f"{c['ticker']}.json"
        if mp.exists():
            out[c["ticker"]] = B.engine(load(mp))
    return out


def reference(kes):
    ov = overview()
    out = {"_engines_from_model": engines_from_model(ov)}
    for ke in kes:
        res = {}
        for c in ov["companies"]:
            tk, price = c["ticker"], c.get("price_ref")
            try:
                if c["template"] == "holding":
                    r = value_holding(tk, ke, price, ov)
                else:
                    r = value_industrial(tk, ke, price)
                res[tk] = {"fair_value": _clean(r.get("fair_value")), "irr_implied": _clean(r.get("irr_implied")),
                           "irr_3y": _clean(r.get("irr_3y"))}
            except Exception as e:  # o teste mostra o erro como falha daquela empresa
                res[tk] = {"error": repr(e)}
        out[str(ke)] = res
    return out


if __name__ == "__main__":
    kes = [float(a) for a in sys.argv[1:]] or [0.20, 0.25, 0.30]
    json.dump(reference(kes), sys.stdout)

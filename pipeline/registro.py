"""Congela as recomendações do estudo numa data, para medir depois se foram boas decisões.

Grava data/registro/{id}.json com: as oportunidades (preço de referência = fechamento oficial da B3, preço-teto,
compra forte, valor justo, TIR, chance, peso na carteira do estudo), a alocação sugerida, os benchmarks
(Ibovespa, Small Caps, CDI) e a foto de todas as empresas cobertas, para comparar a seleção com o resto.

Uso: python pipeline/registro.py <id> <ceilings.json> <ibov_fech> <smll_fech> <cdi_aa>
     ceilings.json = {TICKER: {teto, compra_forte, vj}} calculado com lib/valuation.ts (mesmo motor do site)
"""
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "data" / "app"


def official_prev_close(tk):
    """Fechamento oficial do pregão anterior = preço de agora / (1 + variação do dia)."""
    for attempt in range(3):
        try:
            with urlopen(Request(f"https://cotacao.b3.com.br/mds/api/v1/instrumentQuotation/{tk}", headers={"User-Agent": "Mozilla/5.0"}), timeout=20) as r:
                d = json.loads(r.read().decode())
            q = d["Trad"][0]["scty"]["SctyQtn"]
            c, f = q.get("curPrc"), q.get("prcFlcn")
            return tk, round(c / (1 + f / 100), 2) if c and f is not None else None
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    return tk, None


def r(x, d=4):
    return None if x is None else round(float(x), d)


def main(rid, ceil_path, ibov, smll, cdi):
    ov = json.load(open(APP / "overview.json"))
    port = json.load(open(APP / "portfolio.json"))
    ext = json.load(open(ROOT / "data" / "external" / "analise_aprofundada_2810.json"))
    qv = json.load(open(ROOT / "data" / "market" / "quotes_val.json"))
    ceil = json.load(open(ceil_path))
    rows = {c["ticker"]: c for c in ov["companies"]}
    with ThreadPoolExecutor(max_workers=8) as ex:
        closes = dict(ex.map(official_prev_close, list(rows)))
    w = {x["ticker"]: x["w"] for x in port.get("weights") or []}
    invested = (port.get("metrics") or {}).get("invested") or sum(w.values())
    extd = {e["ticker"]: e for e in ext["empresas"]}
    recs = []
    for i, t in enumerate(ov["opportunities"]):
        c = rows[t]
        doc = json.load(open(APP / "companies" / f"{t}.json"))
        px = closes.get(t) or c["price_ref"]
        cl = ceil.get(t) or {}
        teto, forte = cl.get("teto"), cl.get("compra_forte")
        situacao = "compra forte" if forte and px <= forte else ("na faixa de compra" if teto and px <= teto else "acima do teto")
        e = extd.get(t)
        recs.append({
            "rank": i + 1, "ticker": t, "nome": c["name"], "setor": (c.get("sector") or {}).get("subsetor"),
            "preco_ref": px, "preco_foto_17h06": c["price_ref"], "teto": r(teto, 2), "compra_forte": r(forte, 2),
            "valor_justo": r(c["fair_value"], 2), "upside": r(c["fair_value"] / px - 1) if c["fair_value"] and px else None,
            "tir_dono": r(c["irr_implied"]), "tir_3a": r(c["irr_3y"]), "chance_valor_acima": r(c["prob_mc"]),
            "peso_capital": r(w.get(t)), "peso_acoes": r(w.get(t) / invested) if w.get(t) and invested else None,
            "situacao": situacao, "confianca": (c.get("confidence") or "").split(" ")[0].rstrip(":—,"),
            "segunda_analise": {"decisao": e["decisao"], "sinal": e["sinal"], "valor_justo": e.get("valor_justo")} if e else None,
            "tese": ((doc.get("report") or {}).get("headline")),
        })
    universo = [{"ticker": t, "preco_ref": closes.get(t) or c["price_ref"], "valor_justo": r(c["fair_value"], 2),
                 "tir_dono": r(c["irr_implied"]), "chance_valor_acima": r(c["prob_mc"]), "selecionada": t in ov["opportunities"]}
                for t, c in rows.items()]
    sz = port.get("sizing") or {}
    out = {
        "id": rid,
        "titulo": "Carteira recomendada pelo estudo",
        "data_ref": "2026-10-28",
        "preco_ref": "Fechamento oficial da B3 em 28/10/2026",
        "registrado_em": datetime.now().isoformat(timespec="minutes"),
        "ke": ov.get("ke", 0.25),
        "regra": ov.get("opportunity_rule"),
        "benchmarks": {"IBOV": ibov, "SMLL": smll, "CDI_aa": cdi},
        "carteira": {"acoes": r(invested), "cdi": r(1 - invested), "entrada_sugerida": r(sz.get("entry_equity")),
                     "acoes_vol_normal": r(sz.get("full_equity_if_vol_normalizes")), "metodo": port.get("label"),
                     "retorno_esperado": r((port.get("metrics") or {}).get("exp_total_tir")), "vol": r((port.get("metrics") or {}).get("vol"))},
        "recomendacoes": recs,
        "universo": universo,
        "como_avaliar": [
            "Retorno de cada ação = preço de agora ÷ preço de referência − 1, somado aos proventos com data-com no período.",
            "Carteira = soma dos pesos × retornos das ações + parcela em CDI corrigida pelo CDI do período.",
            "Comparar com o Ibovespa, o Small Caps e o CDI do mesmo período, e com a mediana das empresas não selecionadas.",
            "Ação que perdeu a tese: ver os gatilhos de saída do relatório de cada uma.",
        ],
        "aviso": "Estudo quantitativo com finalidade informativa; não é recomendação de investimento.",
        "fontes": {"cotacoes_val": qv.get("label"), "segunda_analise": f"{ext['autor']}, {ext['data']}"},
    }
    (ROOT / "data" / "registro").mkdir(exist_ok=True)
    json.dump(out, open(ROOT / "data" / "registro" / f"{rid}.json", "w"), ensure_ascii=False, indent=1)
    miss = [t for t in rows if not closes.get(t)]
    print(f"registro {rid}: {len(recs)} recomendações, {len(universo)} empresas | sem fechamento oficial: {miss}")
    for x in recs:
        print(f"  {x['rank']} {x['ticker']:6} ref {x['preco_ref']:>7} (foto {x['preco_foto_17h06']}) teto {x['teto']} VJ {x['valor_justo']} peso {x['peso_capital']} {x['situacao']}")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], float(a[2]), float(a[3]), float(a[4]))

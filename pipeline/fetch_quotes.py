"""Foto de preços para o valuation (separada da foto do dia do crash, que fica em data/market/quotes.json).

Busca na API oficial da B3 a cotação de todas as empresas cobertas, das controladas listadas citadas nas holdings
e do Ibovespa, e grava data/market/quotes_val.json. Rodar depois do fechamento para usar o preço de fechamento.

Uso: python pipeline/fetch_quotes.py "Fechamento de 28/10/2026"
"""
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0"}


def quote(tk):
    for attempt in range(4):
        try:
            with urlopen(Request(f"https://cotacao.b3.com.br/mds/api/v1/instrumentQuotation/{tk}", headers=UA), timeout=20) as r:
                d = json.loads(r.read().decode())
            if (d.get("BizSts") or {}).get("cd") != "OK":
                return tk, None
            t = d["Trad"][0]["scty"]
            q = t["SctyQtn"]
            px, ch = q.get("curPrc"), q.get("prcFlcn")
            prev = px / (1 + ch / 100) if px and ch is not None and ch > -100 else None
            return tk, {"price": px, "chg_pct": ch, "prev_close": round(prev, 4) if prev else None, "ts": d["Msg"]["dtTm"], "name": t.get("desc")}
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    return tk, None


def main(label):
    cov = [c["ticker"] for c in json.load(open(ROOT / "research" / "_coverage.json"))["coverage"]]
    extra = set()
    for p in (ROOT / "research").glob("*.json"):
        if p.stem.startswith("_"):
            continue
        try:
            so = json.load(open(p)).get("sotp") or {}
        except Exception:
            continue
        for c in so.get("components") or []:
            if c.get("ticker"):
                extra.add(c["ticker"])
    tickers = sorted(set(cov) | extra | {"IBOV"})
    with ThreadPoolExecutor(max_workers=8) as ex:
        res = dict(ex.map(quote, tickers))
    missing = [t for t, v in res.items() if not v or not v.get("price")]
    out = {"fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "label": label, "fonte": "B3 instrumentQuotation (oficial)"}
    out.update({t: v for t, v in res.items() if v and v.get("price")})
    json.dump(out, open(ROOT / "data" / "market" / "quotes_val.json", "w"), ensure_ascii=False, indent=1)
    print(f"quotes_val.json: {len(out) - 3} cotações | sem preço: {missing}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Foto de valuation")

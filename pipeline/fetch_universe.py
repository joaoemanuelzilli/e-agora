"""Universo (IBOV + IBrX-100 + SMLL) e variação do dia via API oficial da B3.

Uso: python pipeline/fetch_universe.py <dir_raw_b3> <saida_json>
"""
import base64
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
INDICES = ["IBOV", "IBXX", "SMLL"]


def get_json(url, tries=3):
    for i in range(tries):
        try:
            with urlopen(Request(url, headers={"User-Agent": UA}), timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            time.sleep(1 + i)
    return None


def index_portfolio(idx):
    payload = json.dumps({"language": "pt-br", "pageNumber": 1, "pageSize": 200, "index": idx, "segment": "1"})
    p = base64.b64encode(payload.encode()).decode()
    data = get_json(f"https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetPortfolioDay/{p}")
    return data.get("results", []) if data else []


def quote(ticker):
    d = get_json(f"https://cotacao.b3.com.br/mds/api/v1/instrumentQuotation/{ticker}")
    if not d or d.get("BizSts", {}).get("cd") != "OK":
        return ticker, None
    t = d["Trad"][0]
    q = t["scty"]["SctyQtn"]
    return ticker, {
        "price": q.get("curPrc"),
        "chg_pct": q.get("prcFlcn"),
        "open": q.get("opngPric"),
        "low": q.get("minPric"),
        "high": q.get("maxPric"),
        "avg": q.get("avrgPric"),
        "trades": t.get("ttlQty"),
        "desc": t["scty"].get("desc"),
        "ts": d.get("Msg", {}).get("dtTm"),
    }


def main(raw_dir, out_path):
    universe = {}
    for idx in INDICES:
        rows = index_portfolio(idx)
        json.dump(rows, open(f"{raw_dir}/idx_{idx}.json", "w"), ensure_ascii=False)
        for r in rows:
            tk = r["cod"].strip()
            u = universe.setdefault(tk, {"ticker": tk, "name": r["asset"].strip(), "type": r["type"].strip(), "indices": {}})
            u["indices"][idx] = float(r["part"].replace(".", "").replace(",", "."))
    with ThreadPoolExecutor(max_workers=12) as ex:
        for tk, q in ex.map(quote, list(universe)):
            universe[tk]["quote"] = q
    rows = []
    for u in universe.values():
        q = u.get("quote")
        if q and q.get("price") and q.get("chg_pct") is not None:
            q["prev_close"] = round(q["price"] / (1 + q["chg_pct"] / 100), 4)
        rows.append(u)
    rows.sort(key=lambda r: (r.get("quote") or {}).get("chg_pct", 0) or 0)
    json.dump({"fetched_at": time.strftime("%Y-%m-%d %H:%M:%S"), "rows": rows}, open(out_path, "w"), ensure_ascii=False, indent=1)
    ok = sum(1 for r in rows if r.get("quote"))
    print(f"universe={len(rows)} quotes_ok={ok}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

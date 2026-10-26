"""Dados oficiais B3: proventos/eventos por emissor e histórico diário de índices.

Uso: python pipeline/b3_fetch.py <universe_json> <out_dir>
"""
import base64
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def get_json(url, tries=4):
    for i in range(tries):
        try:
            with urlopen(Request(url, headers={"User-Agent": UA}), timeout=40) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            time.sleep(1.5 * (i + 1))
    return None


def b64(obj):
    return base64.b64encode(json.dumps(obj).encode()).decode()


def supplement(issuer):
    url = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetListedSupplementCompany/" + b64(
        {"issuingCompany": issuer, "language": "pt-br"})
    d = get_json(url)
    return issuer, (d[0] if isinstance(d, list) and d else None)


def index_year(idx, year, tries=6):
    url = "https://sistemaswebb3-listados.b3.com.br/indexStatisticsProxy/IndexCall/GetPortfolioDay/" + b64(
        {"index": idx, "language": "pt-br", "year": str(year)})
    d = None
    for i in range(tries):  # a API às vezes devolve vazio: tenta de novo
        d = get_json(url)
        if d and d.get("results"):
            break
        time.sleep(1.5 * (i + 1))
    rows = []
    if not d or not d.get("results"):
        return rows
    for r in d["results"]:
        day = r["day"]
        for m in range(1, 13):
            val = r.get(f"rateValue{m}")
            if val:
                rows.append((f"{year}-{m:02d}-{day:02d}", float(val.replace(".", "").replace(",", "."))))
    return rows


def main(universe_json, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows = json.load(open(universe_json))["rows"]
    issuers = sorted({r["ticker"][:4] for r in rows})
    with ThreadPoolExecutor(max_workers=8) as ex:
        sup = dict(ex.map(supplement, issuers))
    json.dump(sup, open(out / "supplement.json", "w"), ensure_ascii=False)
    print("supplement ok:", sum(1 for v in sup.values() if v), "/", len(issuers))
    idx = {}
    for name in ("IBOV", "SMLL", "IFNC", "IMOB", "ICON", "IEEX"):
        start = 1998 if name == "IBOV" else 2008
        with ThreadPoolExecutor(max_workers=6) as ex:
            parts = list(ex.map(lambda y: index_year(name, y), range(start, 2027)))
        idx[name] = sorted(p for part in parts for p in part)
        print(name, len(idx[name]), idx[name][0] if idx[name] else None, idx[name][-1] if idx[name] else None)
    json.dump(idx, open(out / "indices.json", "w"))


if __name__ == "__main__":
    main(*sys.argv[1:3])

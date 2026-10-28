"""Inclui na cobertura (research/_coverage.json) os tickers com premissas prontas em research/.

Uso: python pipeline/coverage_add.py <universe_adtv.csv> <universe_quotes.json> [GRUPO=TICKER,TICKER ...]
Lê nome, queda às 11h39, preço e índices da foto do universo de 26/10. Cria PETR3/BBDC3 a partir das premissas da
outra classe quando só uma existir (mesma companhia, mesmas premissas).
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DUP = {"PETR3": "PETR4", "BBDC3": "BBDC4"}


def main(adtv_csv, quotes_json, *groups):
    covp = ROOT / "research" / "_coverage.json"
    cov = json.load(open(covp))
    have = {c["ticker"] for c in cov["coverage"]}
    adtv = {r["ticker"]: r for r in csv.DictReader(open(adtv_csv))}
    q = {r["ticker"]: r for r in json.load(open(quotes_json))["rows"]}
    group_of = {}
    for g in groups:
        name, tks = g.split("=", 1)
        for t in tks.split(","):
            group_of[t] = name
    # cópias de classe
    for t, src in DUP.items():
        sp, tp = ROOT / "research" / f"{src}.json", ROOT / "research" / f"{t}.json"
        if sp.exists() and not tp.exists() and t in group_of:
            d = json.load(open(sp))
            d["ticker"] = t
            d["copied_from"] = src
            json.dump(d, open(tp, "w"), ensure_ascii=False, indent=2)
            note = ROOT / "research" / "notes" / f"{src}.md"
            if note.exists():
                (ROOT / "research" / "notes" / f"{t}.md").write_text(f"*Mesmas premissas de {src} (mesma companhia, outra classe de ação).*\n\n" + note.read_text())
    added, missing = [], []
    for t, g in group_of.items():
        if t in have:
            continue
        if not (ROOT / "research" / f"{t}.json").exists():
            missing.append(t)
            continue
        a, r = adtv.get(t) or {}, q.get(t) or {}
        quote = r.get("quote") or {}
        cov["coverage"].append({
            "ticker": t, "name": r.get("name") or a.get("name") or t, "group": g,
            "chg_pct_1139": round(float(a["chg"]), 2) if a.get("chg") else None,
            "price_1139": quote.get("price"), "prev_close_2310": quote.get("prev_close"),
            "adtv_3m_mn": round(float(a["adtv"]), 1) if a.get("adtv") else None,
            "indices": [k for k in (r.get("indices") or {})] or (a.get("idx") or "").split(","), "round": 2,
        })
        added.append(t)
    cov["rule"] = ("1ª rodada (26/10): queda ≥ 20% no dia e ADTV 3m ≥ R$ 20 mi; ampliação (28/10): demais ações do universo "
                   "IBOV+IBrX100+SMLL com ADTV 3m ≥ R$ 10 mi e dados da CVM")
    json.dump(cov, open(covp, "w"), ensure_ascii=False, indent=1)
    print(f"cobertura: {len(cov['coverage'])} | incluídas {len(added)} | sem premissas: {missing}")


if __name__ == "__main__":
    main(*sys.argv[1:])

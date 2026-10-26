"""Junta os resultados das baterias de teste (data/tests/*) em data/app/tests.json para a página /testes.

Uso: python pipeline/tests_build.py
"""
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "data" / "tests"


def load(p):
    try:
        return json.load(open(p))
    except Exception:
        return None


def text(p):
    try:
        return Path(p).read_text()
    except Exception:
        return None


def verdict(md):
    if not md:
        return None
    for line in md.splitlines():
        if re.search(r"veredito", line, re.I):
            v = re.sub(r"[#*_`>]", "", line).split(":", 1)[-1].strip()
            return v[:160] if v else None
    return None


def main():
    ov = load(ROOT / "data" / "app" / "overview.json") or {"companies": []}
    base = load(T / "baseline_pre_review.json") or {"empresas": {}}
    now = {c["ticker"]: c for c in ov["companies"]}
    review = []
    for tk, b in sorted(base["empresas"].items()):
        md = text(ROOT / "research" / "review" / f"{tk}.md")
        a = now.get(tk, {})
        review.append({
            "ticker": tk, "verdict": verdict(md), "has_review": md is not None,
            "changed": (ROOT / "research" / "review" / f"{tk}.orig.json").exists(),
            "before": {"fair": b.get("fair_value"), "irr": b.get("irr_implied"), "upside": b.get("upside"), "rank": b.get("rank")},
            "after": {"fair": a.get("fair_value"), "irr": a.get("irr_implied"), "upside": a.get("upside"), "rank": a.get("rank")},
            "md": md,
        })
    out = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "baseline_opportunities": base.get("opportunities"),
        "opportunities": ov.get("opportunities"),
        "review": review,
        "factor_backtest": load(T / "factor_backtest.json"),
        "crash_study": load(T / "crash_study.json"),
        "robustness": load(T / "robustness.json"),
        "portfolio": load(T / "portfolio.json"),
        "alt_methods": load(T / "alt_methods.json"),
        "consensus": [x for x in (load(T / "consensus" / f"grupo{i}.json") for i in (1, 2, 3)) if x],
        "md": {k: text(T / f"{k}.md") for k in ("factor_backtest", "crash_study", "robustness", "portfolio", "alt_methods", "test_report")},
        "consensus_md": [x for x in (text(T / "consensus" / f"grupo{i}.md") for i in (1, 2, 3)) if x],
    }
    json.dump(out, open(ROOT / "data" / "app" / "tests.json", "w"), ensure_ascii=False, separators=(",", ":"), default=str)
    have = [k for k in ("factor_backtest", "crash_study", "robustness", "portfolio", "alt_methods") if out[k]]
    print("tests.json:", "revisões", sum(1 for r in review if r["has_review"]), "| alteradas", sum(1 for r in review if r["changed"]),
          "| baterias:", have, "| consenso:", len(out["consensus"]), "| relatório de testes:", bool(out["md"]["test_report"]))


if __name__ == "__main__":
    main()

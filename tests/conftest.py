"""Fixtures e utilitários compartilhados pelos testes pytest (não altera nada fora de tests/ e data/tests/)."""
import json
import os
import sys
from functools import lru_cache
from pathlib import Path

sys.dont_write_bytecode = True  # não grava __pycache__ em pipeline/ ao importar o motor
os.environ.setdefault("EAGORA_SNAPSHOT", "1")  # cotações = foto do estudo (sem rede)

ROOT = Path(__file__).resolve().parents[1]
HIST = ROOT / "data" / "hist"
MARKET = ROOT / "data" / "market"
MODEL = ROOT / "data" / "model"
APP = ROOT / "data" / "app"
RESEARCH = ROOT / "research"
# suplemento oficial da B3 (ações emitidas): fora do repositório; caminho configurável
DEFAULT_SUPPLEMENT = "/tmp/claude-1000/-home-joaoemanuel-git-e-agora/cd238de5-f094-4d2e-ba5c-c5e5bf8d2192/scratchpad/raw/b3/supplement.json"
SUPPLEMENT = Path(os.environ.get("B3_SUPPLEMENT", DEFAULT_SUPPLEMENT))


@lru_cache(maxsize=None)
def load(path):
    with open(path) as fh:
        return json.load(fh)


def coverage():
    return [c["ticker"] for c in load(RESEARCH / "_coverage.json")["coverage"]]


def hist_tickers():
    return sorted(p.stem for p in HIST.glob("*.json"))


def market_tickers():
    return sorted(p.stem for p in MARKET.glob("*.json") if not p.stem.startswith("_") and p.stem not in ("quotes", "dividends"))


def overview():
    return load(APP / "overview.json")


def qkey(k):
    return int(k[:4]), int(k[-1])


def fails(problems, limit=12):
    """Mensagem de falha compacta com evidência (primeiros itens + total)."""
    head = "; ".join(map(str, problems[:limit]))
    more = f" … (+{len(problems) - limit})" if len(problems) > limit else ""
    return f"{len(problems)} problema(s): {head}{more}"

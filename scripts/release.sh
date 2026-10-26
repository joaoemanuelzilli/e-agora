#!/usr/bin/env bash
# Integra resultados e publica, tudo na mesma foto de preços (13h02 de 26/10/2026):
# modelo -> dividendos (histórico B3 em cache) -> dados do app -> baterias de teste -> resumo dos testes -> build -> git -> Vercel.
# Uso: bash scripts/release.sh "mensagem do commit"   (BATTERIES=0 pula as baterias; SUITE=1 roda também a suíte de testes)
set -euo pipefail
cd "$(dirname "$0")/.."
SP=${SP:-/tmp/claude-1000/-home-joaoemanuel-git-e-agora/cd238de5-f094-4d2e-ba5c-c5e5bf8d2192/scratchpad}
MSG=${1:-"Atualiza estudo e testes"}
export EAGORA_SNAPSHOT=1
.venv/bin/python -I -W ignore pipeline/model.py --all --quiet
.venv/bin/python -I pipeline/dividends.py "$SP/raw/b3" > /dev/null
.venv/bin/python -I pipeline/build.py
if [ "${BATTERIES:-1}" = "1" ]; then
  # as baterias leem data/app/overview.json e as premissas; rodam em paralelo
  .venv/bin/python -I pipeline/tests/portfolio.py --offline > "$SP/batt_portfolio.log" 2>&1 &
  .venv/bin/python -I pipeline/tests/robustness.py > "$SP/batt_robustness.log" 2>&1 &
  .venv/bin/python -I pipeline/tests/alt_methods.py > "$SP/batt_alt.log" 2>&1 &
  .venv/bin/python -I pipeline/tests/crash_study.py "$SP/work/cotahist.csv.gz" "$SP/raw/b3" > "$SP/batt_crash.log" 2>&1 &
  wait
fi
if [ "${SUITE:-0}" = "1" ]; then
  ISOLATED=1 bash tests/run_all.sh > "$SP/suite.log" 2>&1 || true
fi
.venv/bin/python -I pipeline/tests_build.py
rm -rf .next && npx next build > "$SP/build.log" 2>&1 || { tail -30 "$SP/build.log"; exit 1; }
grep -E "Generating static pages.*\)" "$SP/build.log" | tail -1
git add -A
git commit -q -m "$MSG" || echo "nada para commitar"
git push -q origin main
vercel deploy --prod --yes 2>&1 | grep -E "Aliased|readyState" | head -2

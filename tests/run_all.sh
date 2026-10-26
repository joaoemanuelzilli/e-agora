#!/usr/bin/env bash
# Suíte completa de testes do estudo:
#   1) pytest  — integridade CVM (data/hist), mercado (data/market) e saídas do modelo (data/model, data/app)
#   2) node    — paridade do motor TS (lib/valuation.ts) com o Python (pipeline/model.py) em Ke 20/25/30%
#   3) next build
#   4) next start -p 3300 + rotas (páginas, 59 empresas, relatórios, APIs ao vivo); derruba só o servidor iniciado aqui
#   5) relatório em data/tests/test_report.md (+ data/tests/test_results.json; saídas brutas em data/tests/raw/)
# Uso: bash tests/run_all.sh
#   variáveis: PYTHON, PORT=3300, SKIP_BUILD=1 (reusa .next), B3_SUPPLEMENT=<supplement.json da B3>,
#   ISOLATED=1 (build e servidor numa cópia temporária do projeto, sem tocar no .next/ compartilhado — útil quando
#   outro `next start` está servindo o .next do repositório; node_modules entra por hard link quando possível)
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PY="${PYTHON:-$ROOT/.venv/bin/python}"
PORT="${PORT:-3300}"
OUT="$ROOT/data/tests/raw"
mkdir -p "$OUT"
export PYTHONDONTWRITEBYTECODE=1 EAGORA_SNAPSHOT=1 NEXT_TELEMETRY_DISABLED=1
STARTED_AT="$(date -Iseconds)"
step() { printf '\n== %s\n' "$*"; }

step "1/5 pytest: CVM, mercado e modelo"
"$PY" -W ignore -m pytest tests -q -p no:cacheprovider -o junit_family=xunit2 --junitxml="$OUT/pytest.xml" > "$OUT/pytest.log" 2>&1
PYTEST_RC=$?
tail -n 1 "$OUT/pytest.log"

step "2/5 node --test: paridade do motor TS × Python"
node --test --test-reporter=spec --test-reporter-destination="$OUT/node_engine.log" \
  --test-reporter=junit --test-reporter-destination="$OUT/node_engine.xml" tests/engine_parity.test.mjs
ENGINE_RC=$?
grep -E "^ℹ (tests|pass|fail|skipped)" "$OUT/node_engine.log" | tr '\n' ' '; echo

APP_DIR="$ROOT"
if [ "${ISOLATED:-0}" = "1" ]; then
  APP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/eagora-app.XXXXXX")" || { echo "mktemp falhou"; exit 2; }
  tar -C "$ROOT" --exclude=./node_modules --exclude=./.next --exclude=./.git --exclude=./.venv --exclude=./data/tests -cf - . | tar -C "$APP_DIR" -xf -
  cp -al "$ROOT/node_modules" "$APP_DIR/node_modules" 2>/dev/null || cp -a "$ROOT/node_modules" "$APP_DIR/node_modules"
  echo "ISOLATED=1: build e servidor em $APP_DIR"
fi

step "3/5 next build"
if [ "${SKIP_BUILD:-0}" = "1" ] && [ -f "$APP_DIR/.next/BUILD_ID" ]; then
  echo "SKIP_BUILD=1: usando o build existente (.next/BUILD_ID $(cat "$APP_DIR/.next/BUILD_ID"))" | tee "$OUT/next_build.log"
  BUILD_RC=0
else
  (cd "$APP_DIR" && npx next build) > "$OUT/next_build.log" 2>&1
  BUILD_RC=$?
fi
tail -n 4 "$OUT/next_build.log"
echo "next build: código de saída $BUILD_RC"

step "4/5 next start -p $PORT + rotas"
# quem escuta na porta (ss; o lsof pode não enxergar sockets em ambientes com /proc restrito)
port_busy() { ss -Hltn "sport = :$1" 2>/dev/null | grep -q . || { command -v lsof >/dev/null && [ -n "$(lsof -t -iTCP:"$1" -sTCP:LISTEN 2>/dev/null)" ]; }; }
ROUTES_RC=1
SERVER_STOPPED=1
rm -f "$OUT/node_routes.xml" "$OUT/node_routes.log"
if [ "$BUILD_RC" -ne 0 ]; then
  echo "build falhou: rotas não testadas" | tee "$OUT/node_routes.log"
elif port_busy "$PORT"; then
  echo "porta $PORT ocupada por um processo que esta suíte não iniciou: rotas não testadas" | tee "$OUT/node_routes.log"
  ROUTES_RC=3
else
  # grupo de processos próprio (setsid): no fim derruba npx → sh → next-server juntos, e só eles
  setsid bash -c 'cd "$1" && exec npx next start -p "$2"' _ "$APP_DIR" "$PORT" > "$OUT/next_start.log" 2>&1 &
  SERVER_PID=$!
  PGID="$SERVER_PID"  # setsid sem fork: o próprio processo vira líder do novo grupo (kill -- -PGID não atinge esta suíte)
  # espera o servidor responder (curl faz as novas tentativas; sem sleep)
  if curl -s -o /dev/null --retry 90 --retry-delay 1 --retry-connrefused --max-time 60 "http://localhost:$PORT/"; then
    BASE_URL="http://localhost:$PORT" node --test --test-reporter=spec --test-reporter-destination="$OUT/node_routes.log" \
      --test-reporter=junit --test-reporter-destination="$OUT/node_routes.xml" tests/app_routes.test.mjs
    ROUTES_RC=$?
    grep -E "^ℹ (tests|pass|fail|skipped)" "$OUT/node_routes.log" | tr '\n' ' '; echo
  else
    echo "servidor não respondeu em http://localhost:$PORT" | tee "$OUT/node_routes.log"
  fi
  # encerra só o que foi iniciado aqui (o grupo do setsid) e confirma pela porta
  [ -n "$PGID" ] && kill -TERM -- "-$PGID" 2>/dev/null
  wait "$SERVER_PID" 2>/dev/null
  timeout 20 bash -c "while ss -Hltn 'sport = :$PORT' 2>/dev/null | grep -q .; do :; done"
  if port_busy "$PORT" && [ -n "$PGID" ]; then kill -KILL -- "-$PGID" 2>/dev/null; timeout 10 bash -c "while ss -Hltn 'sport = :$PORT' 2>/dev/null | grep -q .; do :; done"; fi
  if port_busy "$PORT"; then echo "AVISO: porta $PORT ainda ocupada"; SERVER_STOPPED=0; else echo "servidor da porta $PORT encerrado (grupo $PGID)"; fi
fi

# só apaga a cópia depois que o servidor caiu (senão ele continuaria servindo de um diretório removido)
if [ "$APP_DIR" != "$ROOT" ] && [ "$SERVER_STOPPED" = 1 ]; then rm -rf "$APP_DIR"; fi

step "5/5 relatório"
"$PY" -I tests/make_report.py --started "$STARTED_AT" --pytest-rc "$PYTEST_RC" --engine-rc "$ENGINE_RC" \
  --build-rc "$BUILD_RC" --routes-rc "$ROUTES_RC"

[ "$PYTEST_RC" -eq 0 ] && [ "$ENGINE_RC" -eq 0 ] && [ "$BUILD_RC" -eq 0 ] && [ "$ROUTES_RC" -eq 0 ]

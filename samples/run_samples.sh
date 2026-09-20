#!/usr/bin/env bash
# Run every code sample against the local mock API.
#
# Usage:
#   ./samples/run_samples.sh
#
# The API version comes from SZLAK_API_VERSION (default 2.0).

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${SZLAK_PORT:-8420}"
VERSION="${SZLAK_API_VERSION:-2.0}"

echo "Starting Szlak mock API v${VERSION} on port ${PORT}"
SZLAK_API_VERSION="$VERSION" SZLAK_PORT="$PORT" \
  python3 "$ROOT/mock-api/server.py" > /tmp/szlak-server.log 2>&1 &
SERVER_PID=$!

cleanup() { kill "$SERVER_PID" 2>/dev/null || true; }
trap cleanup EXIT

for _ in $(seq 1 40); do
  if python3 -c "
import urllib.request,sys
try:
    urllib.request.urlopen('http://127.0.0.1:${PORT}/health', timeout=1)
except Exception:
    sys.exit(1)
" 2>/dev/null; then
    break
  fi
  sleep 0.25
done

echo

PASS=0
FAIL=0
FAILED_SAMPLES=()

for sample in "$ROOT"/samples/*.py; do
  name="$(basename "$sample")"
  printf '=== %s ' "$name"
  printf '%.0s=' $(seq 1 $((50 - ${#name})))
  echo

  if python3 "$sample"; then
    echo "--- PASS"
    PASS=$((PASS + 1))
  else
    echo "--- FAIL"
    FAIL=$((FAIL + 1))
    FAILED_SAMPLES+=("$name")
  fi
  echo
done

echo "=================================================="
echo "  ${PASS} passed, ${FAIL} failed"
if [ "$FAIL" -gt 0 ]; then
  echo "  Failing: ${FAILED_SAMPLES[*]}"
fi
echo "=================================================="

[ "$FAIL" -eq 0 ]

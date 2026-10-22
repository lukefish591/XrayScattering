#!/usr/bin/env bash
# Build the static Pyodide Panel app into web/dist (not committed).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ -x "$ROOT/.venv/bin/python" ]]; then
  exec "$ROOT/.venv/bin/python" -m app.build_static
fi
exec python3 -m app.build_static

#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  ./setup_original.sh
fi

source .venv/bin/activate
pytest -q test_original.py || true
cat log_original.txt
cat time_original.txt
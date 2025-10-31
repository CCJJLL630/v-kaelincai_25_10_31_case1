#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  ./setup_optimized.sh
fi

source .venv/bin/activate
pytest -q test_optimized.py
cat log_optimized.txt
cat time_optimized.txt
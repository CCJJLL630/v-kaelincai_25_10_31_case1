#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python -m venv "$SCRIPT_DIR/.venv"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/.venv/bin/activate"
pip install --upgrade pip
pip install -r "$SCRIPT_DIR/requirements_optimized.txt"
echo "Environment ready in $SCRIPT_DIR/.venv"

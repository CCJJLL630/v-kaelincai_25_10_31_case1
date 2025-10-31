#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/log_optimized.txt"
TIME_FILE="${SCRIPT_DIR}/time_optimized.txt"
VENV_DIR="${SCRIPT_DIR}/.venv_optimized"

if [[ -d "${VENV_DIR}" ]]; then
  PYTHON_BIN="${VENV_DIR}/bin/python"
else
  PYTHON_BIN="python"
fi

export PROJECT_DIR="${SCRIPT_DIR}"

"${PYTHON_BIN}" - <<'PY'
import json
import os
import subprocess
import sys
import time
from pathlib import Path

script_dir = Path(os.environ["PROJECT_DIR"])
log_file = script_dir / "log_optimized.txt"
time_file = script_dir / "time_optimized.txt"
pytest_args = [sys.executable, "-m", "pytest", "test_optimized.py", "-q"]

start = time.perf_counter()
proc = subprocess.run(pytest_args, cwd=script_dir, capture_output=True, text=True)
elapsed = time.perf_counter() - start

log_payload = "# pytest output for Project B\n" + proc.stdout + proc.stderr
log_file.write_text(log_payload)

time_summary = f"elapsed_seconds: {elapsed:.6f}\npytest_exit_code: {proc.returncode}\n"
time_file.write_text(time_summary)

if proc.returncode != 0:
    sys.exit(proc.returncode)
PY

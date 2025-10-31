#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/log_original.txt"
TIME_FILE="${SCRIPT_DIR}/time_original.txt"
VENV_DIR="${SCRIPT_DIR}/.venv_original"

if [[ -d "${VENV_DIR}" ]]; then
  PYTHON_BIN="${VENV_DIR}/bin/python"
else
  PYTHON_BIN="python"
fi

export PROJECT_DIR="${SCRIPT_DIR}"

"${PYTHON_BIN}" - <<'PY'
import os
import subprocess
import sys
import time
from pathlib import Path

script_dir = Path(os.environ["PROJECT_DIR"])
log_file = script_dir / "log_original.txt"
time_file = script_dir / "time_original.txt"
pytest_args = [sys.executable, "-m", "pytest", "test_original.py", "-q"]

start = time.perf_counter()
proc = subprocess.run(pytest_args, cwd=script_dir, capture_output=True, text=True)
elapsed = time.perf_counter() - start

log_payload = (
    "# pytest output for Project A (expected failure)\n" + proc.stdout + proc.stderr
)
log_file.write_text(log_payload)

time_summary = (
    f"elapsed_seconds: {elapsed:.6f}\n"
    f"pytest_exit_code: {proc.returncode}\n"
    "note: Non-zero exit code is expected because the bug is still present.\n"
)
time_file.write_text(time_summary)

# Always exit successfully so automation can continue.
PY

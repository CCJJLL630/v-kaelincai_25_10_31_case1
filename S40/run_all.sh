#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pushd "$ROOT_DIR/Project_A_Faulty" >/dev/null
bash run_original.sh || true
popd >/dev/null

pushd "$ROOT_DIR/Project_B_Optimized" >/dev/null
bash run_optimized.sh
popd >/dev/null

python - <<'PY'
from pathlib import Path
import json
import textwrap

root = Path(__file__).resolve().parent
report_path = root / "compare_report.md"

def read_time(path: Path) -> dict:
    data = {"status": "unknown", "elapsed_seconds": "n/a", "timestamp": "n/a"}
    if path.exists():
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                if "=" not in line:
                    continue
                key, value = line.strip().split("=", 1)
                data[key] = value
    return data

faulty = read_time(root / "Project_A_Faulty" / "time_original.txt")
optimized = read_time(root / "Project_B_Optimized" / "time_optimized.txt")

content = f"""# Comparison Report

## Execution Summary

- Project A status: {faulty.get('status', 'unknown')} (elapsed {faulty.get('elapsed_seconds', 'n/a')} s)
- Project B status: {optimized.get('status', 'unknown')} (elapsed {optimized.get('elapsed_seconds', 'n/a')} s)

Further analysis available in README.
"""

report_path.write_text(textwrap.dedent(content), encoding="utf-8")
PY

echo "Comparison report generated at $ROOT_DIR/compare_report.md"

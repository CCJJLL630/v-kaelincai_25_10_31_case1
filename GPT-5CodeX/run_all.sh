#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${ROOT_DIR}/Project_A_Faulty/run_original.sh"
bash "${ROOT_DIR}/Project_B_Optimized/run_optimized.sh"

python - <<'PY'
import json
import math
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
project_a = root / "Project_A_Faulty"
project_b = root / "Project_B_Optimized"
report_path = root / "compare_report.md"

def parse_time_file(path: Path) -> dict:
    data = {"elapsed_seconds": math.nan, "pytest_exit_code": None}
    if not path.exists():
        return data
    for line in path.read_text().splitlines():
        if line.startswith("elapsed_seconds"):
            try:
                data["elapsed_seconds"] = float(line.split(":", 1)[1].strip())
            except ValueError:
                data["elapsed_seconds"] = math.nan
        elif line.startswith("pytest_exit_code"):
            try:
                data["pytest_exit_code"] = int(line.split(":", 1)[1].strip())
            except ValueError:
                data["pytest_exit_code"] = None
    return data

sys.path.insert(0, str(project_a))
sys.path.insert(0, str(project_b))

import original_code  # type: ignore
import optimized_code  # type: ignore

cases = json.loads((root / "test_data.json").read_text())["test_cases"]

results = []
for case in cases:
    payload = case["input"]["payload"]
    weights = case["input"]["weights"]
    expected = float(case["expected_output"])

    faulty_output = original_code.compute_insight_score(payload, weights)
    optimized_output = optimized_code.compute_insight_score(payload, weights)

    faulty_error = abs(faulty_output - expected)
    optimized_error = abs(optimized_output - expected)

    tolerance = max(1e-6, abs(expected) * 1e-6)
    results.append(
        {
            "name": case["name"],
            "expected": expected,
            "faulty_output": faulty_output,
            "optimized_output": optimized_output,
            "faulty_pass": faulty_error <= tolerance,
            "optimized_pass": optimized_error <= tolerance,
            "bug_type": case["bug_type"],
        }
    )

faulty_accuracy = sum(r["faulty_pass"] for r in results) / len(results)
optimized_accuracy = sum(r["optimized_pass"] for r in results) / len(results)

faulty_errors = sum(abs(r["expected"] - r["faulty_output"]) for r in results) / len(results)
optimized_errors = sum(abs(r["expected"] - r["optimized_output"]) for r in results) / len(results)

a_time = parse_time_file(project_a / "time_original.txt")
b_time = parse_time_file(project_b / "time_optimized.txt")

lines = [
    "# Comparison Report",
    "",
    "| Metric | Project A (Faulty) | Project B (Optimized) |",
    "| --- | --- | --- |",
    f"| Accuracy | {faulty_accuracy:.2%} | {optimized_accuracy:.2%} |",
    f"| Mean Absolute Error | {faulty_errors:.6f} | {optimized_errors:.6f} |",
    f"| pytest exit code | {a_time['pytest_exit_code']} | {b_time['pytest_exit_code']} |",
    f"| Execution time (s) | {a_time['elapsed_seconds']:.6f} | {b_time['elapsed_seconds']:.6f} |",
    "",
    "## Test Outcomes",
    "",
    "| Test Case | Bug Type | Expected | Faulty Output | Optimized Output | Faulty Pass | Optimized Pass |",
    "| --- | --- | --- | --- | --- | --- | --- |",
]
for row in results:
    lines.append(
        f"| {row['name']} | {row['bug_type']} | {row['expected']:.6f} | "
        f"{row['faulty_output']:.6f} | {row['optimized_output']:.6f} | "
        f"{('Yes' if row['faulty_pass'] else 'No')} | {('Yes' if row['optimized_pass'] else 'No')} |"
    )

lines.extend(
    [
        "",
        "## Observations",
        "",
        "- Project B restores accumulator correctness and normalizes nested collections.",
        "- Cached weight lookups and iterative traversal reduce recursion depth risk and redundant dictionary access.",
        "- Project A retains the documented bug, which causes major accuracy loss on nested payloads.",
    ]
)

report_path.write_text("\n".join(lines))
PY

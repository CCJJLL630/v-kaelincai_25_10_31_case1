#!/usr/bin/env bash
set -euo pipefail

echo "Running Project A (Faulty)"
pushd Project_A_Faulty >/dev/null
./run_original.sh || true
popd >/dev/null

echo "Running Project B (Optimized)"
pushd Project_B_Optimized >/dev/null
./run_optimized.sh
popd >/dev/null

python <<'PYCODE'
import json
from pathlib import Path

def parse_metrics(folder: Path, time_file: str, log_file: str):
    runtime = None
    time_path = folder / time_file
    if time_path.exists():
        content = time_path.read_text(encoding="utf-8").strip()
        if "=" in content:
            try:
                runtime = float(content.split("=")[-1])
            except ValueError:
                runtime = None
    log_path = folder / log_file
    total = 0
    errors = 0
    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#"):
                continue
            total += 1
            if any(keyword in line for keyword in ["FAIL", "Error", "Exception", "matches_expected=False", "NoException"]):
                errors += 1
    accuracy = None
    if total:
        accuracy = (total - errors) / total
    return runtime, errors, total, accuracy

a_runtime, a_errors, a_total, a_accuracy = parse_metrics(Path("Project_A_Faulty"), "time_original.txt", "log_original.txt")
b_runtime, b_errors, b_total, b_accuracy = parse_metrics(Path("Project_B_Optimized"), "time_optimized.txt", "log_optimized.txt")

def format_val(value):
    if value is None:
        return "TBD"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)

improvement_runtime = None
if a_runtime is not None and b_runtime is not None:
    improvement_runtime = a_runtime - b_runtime

improvement_accuracy = None
if a_accuracy is not None and b_accuracy is not None:
    improvement_accuracy = b_accuracy - a_accuracy

report_lines = Path("compare_report.md").read_text(encoding="utf-8").splitlines()

def replace_line(lines, metric, a_val, b_val, improve):
    new_lines = []
    for line in lines:
        if line.startswith(f"| {metric} |"):
            new_lines.append(
                f"| {metric} | {format_val(a_val)} | {format_val(b_val)} | {format_val(improve)} |"
            )
        else:
            new_lines.append(line)
    return new_lines

report_lines = replace_line(report_lines, "Accuracy", a_accuracy, b_accuracy, improvement_accuracy)
report_lines = replace_line(report_lines, "Average Runtime (s)", a_runtime, b_runtime, improvement_runtime)
report_lines = replace_line(report_lines, "Error Count", a_errors if a_total else None, b_errors if b_total else None, (a_errors - b_errors) if a_total and b_total else None)
report_lines = replace_line(report_lines, "Edge-case Success Rate", "TBD", "TBD", "TBD")

Path("compare_report.md").write_text("\n".join(report_lines), encoding="utf-8")

PYCODE
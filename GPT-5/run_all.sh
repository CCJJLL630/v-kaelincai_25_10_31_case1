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
        content = time_path.read_text(encoding='utf-8').strip()
        if '=' in content:
            try:
                runtime = float(content.split('=')[-1])
            except ValueError:
                runtime = None
    log_path = folder / log_file
    total = 0
    errors = 0
    edge_success = 0
    edge_total = 0
    for line in log_path.read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'): continue
        total += 1
        name, rest = line.split(':', 1)
        is_edge = any(tag in name for tag in ['edge', 'vulnerability', 'invalid', 'complex'])
        if is_edge:
            edge_total += 1
        failed = any(keyword in rest for keyword in ['FAIL', 'Error', 'Exception', 'matches_expected=False', 'NoException'])
        if failed:
            errors += 1
        else:
            if is_edge:
                edge_success += 1
    accuracy = (total - errors) / total if total else None
    edge_rate = edge_success / edge_total if edge_total else None
    return runtime, errors, total, accuracy, edge_rate

metrics_a = parse_metrics(Path('Project_A_Faulty'), 'time_original.txt', 'log_original.txt')
metrics_b = parse_metrics(Path('Project_B_Optimized'), 'time_optimized.txt', 'log_optimized.txt')
(a_runtime, a_errors, a_total, a_accuracy, a_edge) = metrics_a
(b_runtime, b_errors, b_total, b_accuracy, b_edge) = metrics_b

compare = Path('compare_report.md').read_text(encoding='utf-8').splitlines()

def fmt(v):
    if v is None: return 'TBD'
    if isinstance(v, float): return f"{v:.4f}"
    return str(v)

improv_runtime = a_runtime - b_runtime if a_runtime is not None and b_runtime is not None else None
improv_accuracy = (b_accuracy - a_accuracy) if a_accuracy is not None and b_accuracy is not None else None
improv_errors = (a_errors - b_errors) if a_total and b_total else None
improv_edge = (b_edge - a_edge) if a_edge is not None and b_edge is not None else None

replacement = {
    'Accuracy': (a_accuracy, b_accuracy, improv_accuracy),
    'Average Runtime (s)': (a_runtime, b_runtime, improv_runtime),
    'Error Count': (a_errors if a_total else None, b_errors if b_total else None, improv_errors),
    'Edge-case Success Rate': (a_edge, b_edge, improv_edge),
}

updated = []
for line in compare:
    if line.startswith('| ') and '|' in line[2:]:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) > 2:
            metric = parts[1]
            if metric in replacement:
                a_val, b_val, imp = replacement[metric]
                line = f"| {metric} | {fmt(a_val)} | {fmt(b_val)} | {fmt(imp)} |"
    updated.append(line)

Path('compare_report.md').write_text('\n'.join(updated), encoding='utf-8')
print('Comparison updated.')
PYCODE

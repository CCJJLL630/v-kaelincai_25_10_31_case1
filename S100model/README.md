# Evaluation of GPT-5-Codex, GPT-5, Claude Sonnet 4.5, S100, and S40

This repository contains two Python projects crafted to evaluate AI models on functional bug detection, correction, and optimization tasks within the Bug-related category.

## Projects Overview

- **Project_A_Faulty** – Pre-Optimization baseline with intentional functional bugs: incorrect discount aggregation, division-by-zero risk, and insecure dynamic adjustments.
- **Project_B_Optimized** – Post-Optimization implementation fixing the logic, handling edge cases, and securing dynamic evaluation.

Both projects ship with dedicated environments, setup scripts, tests, logs, and single-command execution scripts. Metrics from each run feed into the shared `compare_report.md` for before/after analysis.

## Functional Bug Scenario

**Scenario:** A discount calculator ingests JSON payloads describing base prices, discount lists, and dynamic adjustment expressions. The faulty version subtracts discounts, divides by zero when no discounts exist, and executes arbitrary code via `eval`. The optimized version corrects arithmetic, introduces safe evaluation, and adds validation.

**Input Format:** JSON string with keys `base_price`, `discounts`, and `dynamic_adjustment`.

**Output:** Numeric total after applying discounts and adjustments, or structured errors.

## Structure

```
c:\chatWorkspace
├── Project_A_Faulty
│   ├── original_code.py
│   ├── requirements_original.txt
│   ├── setup_original.sh
│   ├── run_original.sh
│   ├── input_data.json
│   ├── test_data.json
│   ├── test_original.py
│   ├── log_original.txt
│   └── time_original.txt
├── Project_B_Optimized
│   ├── optimized_code.py
│   ├── requirements_optimized.txt
│   ├── setup_optimized.sh
│   ├── run_optimized.sh
│   ├── test_data.json
│   ├── test_optimized.py
│   ├── log_optimized.txt
│   └── time_optimized.txt
├── test_data.json (shared summary)
├── compare_report.md
├── run_all.sh
└── README.md (this file)
```

## Running the Projects

### Prerequisites
- Python 3.9+
- Bash-compatible shell (macOS/Linux/WSL). For Windows PowerShell, convert `.sh` to `.ps1` equivalents.

### Project A (Faulty)
```bash
cd Project_A_Faulty
./setup_original.sh
./run_original.sh
```
The script installs dependencies, runs failing tests (`pytest -q`), and writes logs to `log_original.txt` and timing information to `time_original.txt`.

### Project B (Optimized)
```bash
cd Project_B_Optimized
./setup_optimized.sh
./run_optimized.sh
```
All tests should pass, and logs/timing files are updated accordingly.

### Combined Evaluation
From repository root:
```bash
./run_all.sh
```
This orchestrator executes both projects, aggregates metrics, and updates `compare_report.md` with accuracy, runtime, error counts, and edge-case coverage placeholders.

## Test Cases
Each project’s `test_data.json` includes five scenarios covering:
1. Normal discount aggregation error/fix.
2. Edge case (empty discounts -> division by zero).
3. Invalid/malformed input.
4. Hidden vulnerability (unsafe dynamic adjustment).
5. Complex nested logic with multiple discounts and adjustments.

## Reproducibility
- Per-project virtual environments via `setup_original.sh` and `setup_optimized.sh`.
- Dependencies declared in `requirements_original.txt` and `requirements_optimized.txt`.
- One-click execution scripts for consistent results.
- Shared `run_all.sh` script to benchmark before vs. after behavior.

## Potential Limitations
- Safe evaluation restricts dynamic expressions to limited Python constructs (`min`, `max`, arithmetic`).
- Runtime measurement is coarse-grained (wall-clock). Extend with profiling tools for deeper performance insights.
- Log parsing in `run_all.sh` assumes current output format.

## Extending the Experiment
- Add Dockerfiles for containerized reproducibility.
- Introduce additional bug patterns and language support.
- Incorporate advanced metrics (memory footprint, throughput) into `compare_report.md`.

## Summary
This setup benchmarks functional bug detection and correction through reproducible, testable projects illustrating both failure and successful remediation. Use these artifacts to evaluate AI models’ capabilities across detection, fix generation, and optimization tasks.
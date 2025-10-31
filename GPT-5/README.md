# Evaluation of GPT-5-Codex, GPT-5, Claude Sonnet 4.5, S100, and S40

This repository contains two Python projects crafted to evaluate AI models on functional bug detection, correction, and optimization tasks within the Bug-related category.

## Projects Overview
- **Project_A_Faulty** – Pre-Optimization baseline with intentional functional bugs: incorrect discount aggregation, division-by-zero risk, and insecure dynamic adjustments.
- **Project_B_Optimized** – Post-Optimization implementation fixing the logic, handling edge cases, and securing dynamic evaluation.

## Functional Bug Scenario
A discount calculator ingests JSON payloads describing base prices, discount lists, and dynamic adjustment expressions. The faulty version subtracts discounts, divides by zero when no discounts exist, and executes arbitrary code via `eval`. The optimized version corrects arithmetic, introduces safe evaluation, and adds validation.

### Input Format
JSON string with keys `base_price`, `discounts`, and `dynamic_adjustment`.

### Output
Numeric total after applying discounts and adjustments, or controlled exceptions.

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
└── README.md
```

## Running the Projects (Bash)
```bash
cd Project_A_Faulty
./setup_original.sh
./run_original.sh

cd ../Project_B_Optimized
./setup_optimized.sh
./run_optimized.sh

cd ..
./run_all.sh
```
`compare_report.md` will update with accuracy, runtime, error counts, and edge-case success rate.

## Test Cases
Each project’s `test_data.json` includes five scenarios covering:
1. Normal discount aggregation error/fix.
2. Edge case (empty discounts -> division by zero vs. safe handling).
3. Invalid/malformed input.
4. Hidden vulnerability (unsafe dynamic adjustment vs. safe rejection).
5. Complex nested logic with multiple discounts and adjustments.

## Reproducibility
- Per-project virtual environments via setup scripts.
- Explicit dependency lists (`requirements_original.txt`, `requirements_optimized.txt`).
- Single-command execution scripts for consistency.
- Aggregated comparison via `run_all.sh`.

## Potential Limitations
- Safe evaluation restricts dynamic expressions to limited constructs (`min`, `max`, arithmetic`).
- Runtime measurement is coarse (wall-clock). For deeper performance analysis add profiling.
- Log parsing assumes current output format.

## Extending the Experiment
- Add Dockerfiles for containerized reproducibility.
- Introduce performance benchmarks (memory, throughput).
- Add CI workflow for automated execution.

## Summary
This setup benchmarks functional bug detection and correction through reproducible, testable projects illustrating both failure and successful remediation. Use these artifacts to evaluate AI models’ capabilities across detection, fix generation, and optimization tasks.

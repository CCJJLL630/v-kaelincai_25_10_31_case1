# Evaluation of GPT-5-Codex, GPT-5, Claude Sonnet 4.5, S100, and S40 on Bug-related – Functional Bug Detection, Correction, and Optimization

## Overview

This workspace contains two parallel Python projects that model the lifecycle of a
functional bug: the **faulty** pre-optimization implementation and the
**optimized** post-fix implementation. Both projects process nested student
assessment data and compute weighted grade summaries. The original code fails to
handle nested structures and untrusted payloads, while the optimized version
introduces resilient parsing, validation, and performance improvements.

```
Project_A_Faulty/      # Pre-optimization reference with intentional bug
Project_B_Optimized/   # Corrected and optimized implementation
```

## Functional Bug Scenario

- **Bug type:** Incorrect handling of nested / malformed inputs leading to
  `TypeError` and inaccurate grade calculations.
- **Input format:** JSON payload containing students, assignments, weights, and
  nested score collections.
- **Output format:** Mapping of student names to weighted final grade rounded to
  two decimals.
- **Intended improvement:** Ensure the system tolerates nested iterables, string
  numerics, dictionary payloads, and malformed scores while improving runtime by
  avoiding repeated recursion/aggregation.

## Project A – Pre-Optimization

*Primary script:* `Project_A_Faulty/original_code.py`

- Naively sums score lists without flattening or validation.
- Crashes with `TypeError` when encountering nested collections, strings, or
  dictionaries.
- Tests (`test_original.py`) include expected failures to demonstrate the bug
  and a strict `xfail` that documents the desired outcome.

### Running Project A

1. (Optional) Set up the environment:
   ```bash
   cd Project_A_Faulty
   bash setup_original.sh
   ```
2. Execute the regression suite (continues even if failures occur):
   ```bash
   bash run_original.sh
   ```
3. Review `log_original.txt` for pytest output and `time_original.txt` for the
   recorded runtime and exit code.

## Project B – Post-Optimization

*Primary script:* `Project_B_Optimized/optimized_code.py`

- Iteratively flattens nested iterables using a deque (non-recursive BFS).
- Sanitizes data, coerces numeric strings, clamps untrusted payloads, and skips
  invalid entries.
- Uses streaming aggregation (constant memory) for better performance on large
  datasets.
- Comprehensive tests (`test_optimized.py`) verify correctness across normal,
  edge, malformed, and vulnerability scenarios.

### Running Project B

1. (Optional) create and activate the environment:
   ```bash
   cd Project_B_Optimized
   bash setup_optimized.sh
   ```
2. Execute the validated suite:
   ```bash
   bash run_optimized.sh
   ```
3. Inspect `log_optimized.txt` and `time_optimized.txt` for outcomes and timing.

## One-Click Evaluation

At the repository root:

```bash
bash run_all.sh
```

The script orchestrates both projects, tolerates the expected failure in Project
A, and regenerates `compare_report.md` with a summary of pass/fail and timing
statistics.

## Test Data

- Shared scenarios are listed in `test_data.json` at the root and replicated in
  each project directory.
- Coverage includes normal inputs, nested structures, malformed strings, hidden
  dictionary payloads (vulnerability simulation), and missing assignments.

## Reproducibility Notes

- Requirements are pinned (`pytest==8.1.1`).
- Shell scripts assume a POSIX shell; on Windows, run via WSL, Git Bash, or
  adapt commands for PowerShell.
- Logs and performance reports are generated deterministically by the automation
  scripts after each run.

## Limitations

- Performance measurements are lightweight; adjust the dataset or wrap
  collection in benchmarking tools for more granular profiling.
- The optimized implementation clamps scores to `<= 100` for safety; adjust the
  policy if the business rules differ.
- Dockerfiles are not included but can be added following the setup scripts.

## How to Extend the Experiment

- Add new scenarios in `test_data.json` and mirror them in the respective test
  modules to simulate unexpected data shapes.
- Integrate property-based testing (e.g., via Hypothesis) for fuzzing nested
  structures.
- Expand logging and metrics collection to cover memory footprint or
  distribution analysis.

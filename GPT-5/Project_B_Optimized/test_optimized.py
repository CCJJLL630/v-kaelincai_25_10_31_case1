"""Automated validation for optimized discount processor."""
from __future__ import annotations
import json, time, pytest
from optimized_code import DiscountProcessorError, apply_discounts

def _to_json(raw_input):
    if isinstance(raw_input, dict):
        return json.dumps(raw_input)
    return raw_input

def test_all_cases_pass():
    with open("test_data.json", "r", encoding="utf-8") as fh:
        cases = json.load(fh)
    results = []
    start = time.perf_counter()
    for case in cases:
        data = _to_json(case["input"])
        expected = case.get("expected_output")
        expected_exc = case.get("expected_exception")
        try:
            output = apply_discounts(data)
        except Exception as exc:  # noqa: BLE001
            outcome = expected_exc is not None and isinstance(exc, (DiscountProcessorError, json.JSONDecodeError))
        else:
            if expected_exc is not None:
                outcome = False
            else:
                outcome = expected is not None and abs(output - expected) < 1e-6
        results.append((case["name"], outcome))
    elapsed = time.perf_counter() - start
    with open("log_optimized.txt", "w", encoding="utf-8") as log_file:
        for name, outcome in results:
            log_file.write(f"{name}: {'PASS' if outcome else 'FAIL'}\n")
    with open("time_optimized.txt", "w", encoding="utf-8") as time_file:
        time_file.write(f"runtime_seconds={elapsed:.6f}\n")
    assert all(outcome for _, outcome in results)

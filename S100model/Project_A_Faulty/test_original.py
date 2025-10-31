"""Tests illustrating faults in the pre-optimization implementation."""

from __future__ import annotations

import json
import time

import pytest

from original_code import apply_discounts


def _to_json(raw_input):
    if isinstance(raw_input, dict):
        return json.dumps(raw_input)
    return raw_input


def test_faulty_behavior_records_failures():
    with open("test_data.json", "r", encoding="utf-8") as fh:
        cases = json.load(fh)

    results = []
    start = time.perf_counter()
    for case in cases:
        data = _to_json(case["input"])
        try:
            output = apply_discounts(data)
        except Exception as exc:  # noqa: BLE001
            results.append((case["name"], type(exc).__name__, False))
        else:
            results.append((case["name"], output, output == case.get("expected_output")))
    elapsed = time.perf_counter() - start

    with open("log_original.txt", "w", encoding="utf-8") as log_file:
        for name, info, matches in results:
            log_file.write(f"{name}: {info} (matches_expected={matches})\n")

    with open("time_original.txt", "w", encoding="utf-8") as time_file:
        time_file.write(f"runtime_seconds={elapsed:.6f}\n")

    assert any(not match for _, _, match in results)
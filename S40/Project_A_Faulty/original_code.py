"""Faulty implementation for computing student grade summaries.

This module intentionally contains a functional bug. It assumes that the score
lists are flat sequences of numeric values. In reality, the input mixes nested
lists, string numbers, dictionaries, and potentially malicious payloads. The
current implementation attempts to sum the values directly, which raises a
TypeError and makes the system unusable for real customer data.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any


def load_student_data(path: Path | None = None) -> Dict[str, Any]:
    """Load the sample student dataset from the JSON input file."""

    if path is None:
        path = Path(__file__).resolve().parent / "input_data.json"
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def compute_weighted_grades(payload: Dict[str, Any]) -> Dict[str, float]:
    """Compute weighted averages for each student.

    BUG: The implementation expects every score to be a numeric scalar. When
    nested collections or non-numeric payloads appear, `sum(scores)` will raise
    a TypeError. Even if the code did not throw, the result would be incorrect
    because the algorithm counts invalid scores instead of rejecting them.
    """

    results: Dict[str, float] = {}
    for student in payload.get("students", []):
        weights_total = 0.0
        weighted_sum = 0.0
        for assignment in student.get("assignments", []):
            weight = float(assignment.get("weight", 1.0))
            scores = assignment.get("scores", [])
            if not scores:
                # Empty scores still count toward the weight but contribution is zero.
                weights_total += weight
                continue

            # BUG: `scores` can be nested lists or contain strings/dicts.
            assignment_total = sum(scores)
            assignment_avg = assignment_total / len(scores)
            weights_total += weight
            weighted_sum += assignment_avg * weight

        results[student["name"]] = round(weighted_sum / weights_total, 2) if weights_total else 0.0
    return results


def main() -> Dict[str, float]:
    """Entry point used by the CLI and manual debugging."""

    payload = load_student_data()
    return compute_weighted_grades(payload)


if __name__ == "__main__":  # pragma: no cover
    report = main()
    print(json.dumps(report, indent=2))

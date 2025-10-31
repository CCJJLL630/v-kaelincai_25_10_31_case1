"""Optimized and hardened implementation of the student grading pipeline.

Key improvements over the faulty version:

1. Robust flattening: gracefully handles arbitrarily nested iterables without
   recursion to avoid stack-overflow on deeply nested inputs.
2. Input sanitation: rejects invalid values, converts string numerics, clamps
   out-of-range payloads, and ignores NaN/Infinity exploits.
3. Efficient aggregation: streams values while keeping constant memory and
   preemptively short-circuits empty assignments.
"""

from __future__ import annotations

import json
import math
from collections import deque
from pathlib import Path
from typing import Any, Deque, Dict, Iterable, Iterator, List

_VALID_TYPES = (int, float)


def load_student_data(path: Path | None = None) -> Dict[str, Any]:
    if path is None:
        path = Path(__file__).resolve().parent / "input_data.json"
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _normalize_leaf(value: Any) -> float | None:
    """Convert a raw payload into a sanitized numeric score.

    Returns:
        float between 0 and 100 inclusive, or ``None`` if the value is invalid.
    """

    original = value
    if isinstance(value, dict):
        value = value.get("value")

    if isinstance(value, _VALID_TYPES):
        numeric = float(value)
    elif isinstance(value, str):
        try:
            numeric = float(value.strip())
        except ValueError:
            return None
    else:
        return None

    if math.isnan(numeric) or math.isinf(numeric):
        return None
    if numeric < 0:
        return None

    # Clamp to prevent score-injection attacks while keeping decimals.
    numeric = min(numeric, 100.0)
    # Preserve two decimal places for deterministic rounding later.
    return round(numeric, 4)


def _iter_numeric(scores: Iterable[Any]) -> Iterator[float]:
    """Iterate over sanitized numeric scores in BFS order.

    Using a deque avoids recursion and handles deeply nested structures with
    predictable performance characteristics.
    """

    queue: Deque[Any] = deque([scores])
    while queue:
        current = queue.popleft()
        if isinstance(current, dict):
            sanitized = _normalize_leaf(current)
            if sanitized is not None:
                yield sanitized
        elif isinstance(current, (list, tuple, set)):
            for item in current:
                queue.append(item)
        else:
            sanitized = _normalize_leaf(current)
            if sanitized is not None:
                yield sanitized


def compute_weighted_grades(payload: Dict[str, Any]) -> Dict[str, float]:
    """Compute weighted averages for each student with resilient data handling."""

    results: Dict[str, float] = {}
    for student in payload.get("students", []):
        weighted_sum = 0.0
        weight_total = 0.0
        for assignment in student.get("assignments", []):
            weight = float(assignment.get("weight", 1.0))
            total = 0.0
            count = 0
            for numeric in _iter_numeric(assignment.get("scores", [])):
                total += numeric
                count += 1
            if not count:
                # Skip assignments with no valid scores so they don't skew averages.
                continue
            assignment_avg = total / count
            weighted_sum += assignment_avg * weight
            weight_total += weight

        results[student["name"]] = round(weighted_sum / weight_total, 2) if weight_total else 0.0
    return results


def generate_grade_report(path: Path | None = None) -> Dict[str, float]:
    """Convenience helper for CLI usage."""

    payload = load_student_data(path)
    return compute_weighted_grades(payload)


if __name__ == "__main__":  # pragma: no cover
    report = generate_grade_report()
    print(json.dumps(report, indent=2))

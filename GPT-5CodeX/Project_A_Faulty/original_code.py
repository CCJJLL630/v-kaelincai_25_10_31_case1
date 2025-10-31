"""Faulty implementation of the insight score computation.

The function is expected to walk a nested payload structure and combine values
according to a type-specific weight map. This version contains two major issues:
1. Accumulator Reset Bug: whenever children are encountered, the outer total is
   replaced by the recursive call, discarding work done so far.
2. Collection Handling Bug: list and dict values are coerced incorrectly,
   leading to wrong magnitudes and missing nested numbers.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List
import json

Payload = List[Dict[str, Any]]
WeightMap = Dict[str, float]


def compute_insight_score(payload: Payload, weight_lookup: WeightMap) -> float:
    """Compute a weighted score for the payload.

    BUG: The running total is reset whenever children are processed, losing the
    contributions already accumulated. Additionally, list values contribute their
    length instead of their numeric contents and dict values ignore nested
    structures. Hidden invalid values propagate silently as zeros.
    """

    total = 0.0
    for item in payload:
        weight = weight_lookup.get(item.get("type"), 1.0)
        value = item.get("value", 0)

        if isinstance(value, list):
            # BUG: list magnitude should sum numeric content, not the length.
            total += weight * len(value)
        elif isinstance(value, dict):
            # BUG: dict magnitude requires recursive traversal with weights; this
            # simplistic sum ignores nested structures.
            total += weight * sum(v for v in value.values() if isinstance(v, (int, float)))
        elif isinstance(value, (int, float)):
            total += weight * value
        else:
            try:
                total += weight * float(value)
            except (TypeError, ValueError):
                total += 0

        children = item.get("children")
        if children:
            # BUG: the accumulator is overwritten instead of being increased.
            total = compute_insight_score(children, weight_lookup)
    return total


def load_input(path: Path) -> tuple[Payload, WeightMap]:
    data = json.loads(path.read_text())
    return data.get("payload", []), data.get("weights", {})


def main() -> None:
    payload_path = Path(__file__).with_name("input_data.json")
    payload, weights = load_input(payload_path)
    score = compute_insight_score(payload, weights)
    print(f"Faulty insight score: {score}")


if __name__ == "__main__":
    main()

"""Optimized and corrected implementation of the insight score computation.

Fixes applied compared to the faulty version:
- Preserves the running total while traversing nested children.
- Normalizes list, dict, and string values recursively instead of using
  incorrect heuristics.
- Uses an iterative traversal and cached weight lookups to avoid redundant
  recursion and dictionary hits on large payloads.
"""
from __future__ import annotations

from collections.abc import Sequence
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Mapping
import json

Payload = List[Dict[str, Any]]
WeightMap = Mapping[str, float]


def _normalize_value(value: Any) -> float:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return 0.0
    if isinstance(value, list):
        return sum(_normalize_value(item) for item in value)
    if isinstance(value, dict):
        return sum(_normalize_value(item) for item in value.values())
    return 0.0


def compute_insight_score(payload: Sequence[Dict[str, Any]], weight_lookup: WeightMap) -> float:
    if not payload:
        return 0.0

    @lru_cache(maxsize=None)
    def resolve_weight(event_type: str) -> float:
        return float(weight_lookup.get(event_type, 1.0))

    total = 0.0
    stack: List[Sequence[Dict[str, Any]]] = [payload]

    while stack:
        items = stack.pop()
        if not isinstance(items, Sequence) or isinstance(items, (str, bytes)):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            event_type = item.get("type", "")
            weight = resolve_weight(event_type)
            total += weight * _normalize_value(item.get("value"))
            children = item.get("children")
            if isinstance(children, Sequence) and not isinstance(children, (str, bytes)):
                stack.append(children)
    return total


def load_input(path: Path) -> tuple[Payload, Dict[str, float]]:
    data = json.loads(path.read_text())
    weights = {k: float(v) for k, v in data.get("weights", {}).items()}
    return data.get("payload", []), weights


def main() -> None:
    payload_path = Path(__file__).with_name("input_data.json")
    payload, weights = load_input(payload_path)
    score = compute_insight_score(payload, weights)
    print(f"Optimized insight score: {score}")


if __name__ == "__main__":
    main()

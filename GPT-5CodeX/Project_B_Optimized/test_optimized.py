import json
from pathlib import Path

import pytest

from optimized_code import compute_insight_score

ROOT = Path(__file__).resolve().parents[1]
TEST_DATA = json.loads((ROOT / "test_data.json").read_text())
CASES = TEST_DATA["test_cases"]


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_optimized_score(case):
    payload = case["input"]["payload"]
    weights = case["input"]["weights"]
    expected = case["expected_output"]
    result = compute_insight_score(payload, weights)
    assert result == pytest.approx(expected, rel=1e-6)


def test_handles_large_depth():
    payload = [
        {
            "type": "click",
            "value": list(range(25)),
            "children": [
                {
                    "type": "view",
                    "value": [str(i) for i in range(10)],
                    "children": [
                        {"type": "purchase", "value": {"leaf": 3}}
                    ],
                }
            ],
        }
    ]
    weights = {"click": 1.25, "view": 0.5, "purchase": 2.0}
    # Expected result: click -> sum(range(25)) = 300,
    # view -> sum(str(i)) = 45,
    # purchase -> 3.
    expected = 1.25 * 300 + 0.5 * 45 + 2.0 * 3
    result = compute_insight_score(payload, weights)
    assert result == pytest.approx(expected, rel=1e-9)

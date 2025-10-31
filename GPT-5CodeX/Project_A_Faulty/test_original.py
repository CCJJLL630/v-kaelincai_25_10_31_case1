import json
from pathlib import Path

import pytest

from original_code import compute_insight_score

ROOT = Path(__file__).resolve().parents[1]
TEST_DATA = json.loads((ROOT / "test_data.json").read_text())
CASES = TEST_DATA["test_cases"]


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_faulty_score(case):
    payload = case["input"]["payload"]
    weights = case["input"]["weights"]
    expected = case["expected_output"]
    result = compute_insight_score(payload, weights)
    assert result == pytest.approx(expected), (
        "Faulty implementation diverged from expected output. "
        "This failure is intentional and highlights the functional bug."
    )


def test_returns_float():
    case = CASES[1]
    payload = case["input"]["payload"]
    weights = case["input"]["weights"]
    result = compute_insight_score(payload, weights)
    assert isinstance(result, float)

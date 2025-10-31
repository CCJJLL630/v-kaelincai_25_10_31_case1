"""Pytest suite that demonstrates the failure in the faulty implementation."""

from __future__ import annotations

from pathlib import Path

import pytest

from original_code import compute_weighted_grades, load_student_data


def test_basic_numeric_scores_work():
    """Sanity check with clean, flat numeric scores."""

    payload = {
        "students": [
            {
                "name": "Test",
                "assignments": [
                    {"name": "Quiz", "weight": 1.0, "scores": [70, 80, 90]},
                    {"name": "Project", "weight": 1.0, "scores": [88, 92]},
                ],
            }
        ]
    }

    report = compute_weighted_grades(payload)
    assert pytest.approx(report["Test"], rel=1e-3) == 85.0


def test_nested_scores_trigger_failure():
    """Real dataset contains nested structures which break the implementation."""

    payload = load_student_data()
    with pytest.raises(TypeError):
        compute_weighted_grades(payload)


def test_string_scores_trigger_failure():
    payload = {
        "students": [
            {
                "name": "Mal",
                "assignments": [
                    {"name": "Quiz", "weight": 1.0, "scores": ["99", 100, 98]},
                ],
            }
        ]
    }

    with pytest.raises(TypeError):
        compute_weighted_grades(payload)


def test_dictionary_payload_triggers_failure():
    payload = {
        "students": [
            {
                "name": "Injected",
                "assignments": [
                    {"name": "Exploit", "weight": 1.0, "scores": [{"value": "101"}]},
                ],
            }
        ]
    }

    with pytest.raises(TypeError):
        compute_weighted_grades(payload)


def test_missing_assignments_defaults_to_zero():
    payload = {"students": [{"name": "Empty", "assignments": []}]}
    report = compute_weighted_grades(payload)
    assert report["Empty"] == 0.0


@pytest.mark.xfail(strict=True, reason="Bug remains unfixed in Project A")
def test_expected_final_scores_for_reference_dataset():
    payload = load_student_data()
    report = compute_weighted_grades(payload)
    # Once the bug is fixed, the grade for Alice should match 93.73.
    assert pytest.approx(report["Alice"], rel=1e-3) == 93.73

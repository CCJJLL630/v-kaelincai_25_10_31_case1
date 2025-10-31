"""Unit tests for the optimized grading pipeline."""

from __future__ import annotations

import math

import pytest

from optimized_code import compute_weighted_grades, load_student_data


@pytest.fixture()
def reference_payload():
    return load_student_data()


def test_reference_dataset_matches_expected_grades(reference_payload):
    report = compute_weighted_grades(reference_payload)
    expected = {
        "Alice": 93.73,
        "Bob": 77.0,
        "Chun": 100.0,
    }
    for student, value in expected.items():
        assert pytest.approx(report[student], rel=1e-3) == value


def test_deeply_nested_scores_are_flattened():
    payload = {
        "students": [
            {
                "name": "Deep",
                "assignments": [
                    {"name": "Challenge", "weight": 1.0, "scores": [[[[100, [98, 99]], 100]]]},
                    {"name": "Bonus", "weight": 1.0, "scores": [95, [[94]], 96]},
                ],
            }
        ]
    }
    report = compute_weighted_grades(payload)
    assert pytest.approx(report["Deep"], rel=1e-3) == 97.12


def test_invalid_payloads_are_ignored():
    payload = {
        "students": [
            {
                "name": "Noisy",
                "assignments": [
                    {
                        "name": "Quiz",
                        "weight": 1.0,
                        "scores": [88, -10, float("nan"), " 90 ", None],
                    }
                ],
            }
        ]
    }
    report = compute_weighted_grades(payload)
    assert pytest.approx(report["Noisy"], rel=1e-3) == 89.0


def test_dictionary_payloads_are_sanitized_and_clamped():
    payload = {
        "students": [
            {
                "name": "Injected",
                "assignments": [
                    {
                        "name": "Exploit",
                        "weight": 1.0,
                        "scores": [{"value": "101"}, {"value": "200"}, {"value": "98.5"}],
                    }
                ],
            }
        ]
    }
    report = compute_weighted_grades(payload)
    # Values above 100 are clamped, so the average becomes (100 + 100 + 98.5) / 3.
    assert pytest.approx(report["Injected"], rel=1e-3) == 99.5


def test_assignments_without_valid_scores_are_skipped():
    payload = {
        "students": [
            {
                "name": "Missing",
                "assignments": [
                    {"name": "Quiz", "weight": 1.0, "scores": []},
                    {"name": "Project", "weight": 1.0, "scores": [float("nan"), -50]},
                ],
            }
        ]
    }
    report = compute_weighted_grades(payload)
    assert report["Missing"] == 0.0

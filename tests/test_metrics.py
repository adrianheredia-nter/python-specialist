"""Unit tests for the KPI and statistics helpers."""
# pylint: disable=missing-function-docstring,redefined-outer-name

import pandas as pd
import pytest

from student_analytics.config import MATH, READING, WRITING
from student_analytics.metrics import (
    compute_kpis,
    describe_scores,
    pass_rate,
    passed_all,
    passed_by_subject,
)


@pytest.fixture
def scores():
    return pd.DataFrame(
        {
            "gender": ["female", "male", "female", "male"],
            MATH: [50, 49, 80, 90],
            READING: [60, 70, 40, 90],
            WRITING: [70, 80, 90, 50],
        }
    )


def test_passed_all_needs_the_three_subjects(scores):
    # 49 in math or 40 in reading is enough to fail
    assert passed_all(scores).tolist() == [True, False, False, True]


def test_pass_rate(scores):
    assert pass_rate(scores) == pytest.approx(50.0)


def test_pass_rate_on_empty_data(scores):
    assert pass_rate(scores.iloc[0:0]) == 0.0


def test_compute_kpis(scores):
    kpis = compute_kpis(scores)
    assert kpis[MATH] == pytest.approx(67.25)
    assert kpis[READING] == pytest.approx(65.0)
    assert kpis[WRITING] == pytest.approx(72.5)
    assert kpis["students"] == 4
    assert kpis["pass_rate"] == pytest.approx(50.0)


def test_describe_scores(scores):
    stats = describe_scores(scores)
    assert list(stats.index) == ["Math", "Reading", "Writing"]
    assert list(stats.columns) == ["Mean", "Median", "Std. dev.", "Max", "Min"]
    assert stats.loc["Math", "Median"] == pytest.approx(65.0)
    assert stats.loc["Reading", "Max"] == 90
    assert stats.loc["Writing", "Min"] == 50
    assert stats.loc["Math", "Std. dev."] == pytest.approx(scores[MATH].std())


def test_passed_by_subject(scores):
    result = passed_by_subject(scores).set_index(["Subject", "Result"])["Students"]
    assert result[("Math", "Passed")] == 3
    assert result[("Math", "Failed")] == 1
    assert result[("Reading", "Passed")] == 3
    assert result[("Writing", "Passed")] == 4
    assert result[("Writing", "Failed")] == 0

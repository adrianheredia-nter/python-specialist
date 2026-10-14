"""Unit tests for the sidebar filter logic."""
# pylint: disable=missing-function-docstring

import pandas as pd

from student_analytics.config import GENDER, TEST_PREP
from student_analytics.filters import apply_filters


def make_df():
    return pd.DataFrame(
        {
            GENDER: ["female", "male", "female", "male"],
            TEST_PREP: ["none", "completed", "completed", "none"],
        }
    )


def test_no_selection_returns_everything():
    df = make_df()
    assert len(apply_filters(df, {GENDER: [], TEST_PREP: []})) == 4


def test_single_filter():
    result = apply_filters(make_df(), {GENDER: ["female"]})
    assert result[GENDER].unique().tolist() == ["female"]
    assert len(result) == 2


def test_filters_are_combined():
    result = apply_filters(make_df(), {GENDER: ["female"], TEST_PREP: ["completed"]})
    assert result.index.tolist() == [2]


def test_several_values_in_one_filter():
    result = apply_filters(make_df(), {GENDER: ["female", "male"], TEST_PREP: ["none"]})
    assert result.index.tolist() == [0, 3]

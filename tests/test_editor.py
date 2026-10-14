"""Unit tests for applying data editor changes."""
# pylint: disable=missing-function-docstring

import pandas as pd

from student_analytics.editor import apply_editor_changes


def make_df():
    return pd.DataFrame({"gender": ["female", "male", "female"], "math score": [10, 20, 30]})


def test_no_changes_keeps_data():
    df = make_df()
    pd.testing.assert_frame_equal(apply_editor_changes(df, {}), df)


def test_edit_a_cell():
    result = apply_editor_changes(make_df(), {"edited_rows": {1: {"math score": 99}}})
    assert result["math score"].tolist() == [10, 99, 30]


def test_delete_rows():
    result = apply_editor_changes(make_df(), {"deleted_rows": [0, 2]})
    assert result["math score"].tolist() == [20]
    assert result.index.tolist() == [0]


def test_add_row_ignores_unknown_keys():
    changes = {"added_rows": [{"_index": 7, "gender": "male", "math score": 55}]}
    result = apply_editor_changes(make_df(), changes)
    assert len(result) == 4
    assert result.iloc[-1].to_dict() == {"gender": "male", "math score": 55}


def test_edit_and_delete_use_original_positions():
    changes = {"edited_rows": {2: {"math score": 31}}, "deleted_rows": [0]}
    result = apply_editor_changes(make_df(), changes)
    assert result["math score"].tolist() == [20, 31]


def test_original_dataframe_is_not_modified():
    df = make_df()
    apply_editor_changes(df, {"edited_rows": {0: {"math score": 0}}, "deleted_rows": [1]})
    assert df["math score"].tolist() == [10, 20, 30]

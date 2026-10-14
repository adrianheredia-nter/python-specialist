"""Helpers for the data editor page."""

import pandas as pd
import streamlit as st

from student_analytics.config import (
    CATEGORY_COLUMNS,
    COLUMN_LABELS,
    MAX_SCORE,
    MIN_SCORE,
    SCORE_COLUMNS,
)


def apply_editor_changes(df: pd.DataFrame, changes: dict) -> pd.DataFrame:
    """Apply the changes reported by st.data_editor to a copy of df.

    The editor gives row positions, not index labels. Edits and deletions
    refer to the rows that were on screen, so they go first. New rows go last.
    """
    result = df.copy()

    for position, values in changes.get("edited_rows", {}).items():
        label = result.index[int(position)]
        for column, value in values.items():
            result.at[label, column] = value

    deleted = changes.get("deleted_rows", [])
    if deleted:
        result = result.drop(index=result.index[deleted])

    # Keep only real columns, the editor can add an "_index" key
    added = [
        {key: value for key, value in row.items() if key in result.columns}
        for row in changes.get("added_rows", [])
    ]
    added = [row for row in added if row]
    if added:
        result = pd.concat([result, pd.DataFrame(added)], ignore_index=True)

    return result.reset_index(drop=True)


def column_config(original: pd.DataFrame) -> dict:
    """Editor columns with validation.

    Categories can only take values that exist in the original dataset and
    scores must be whole numbers between 0 and 100.
    """
    config = {}
    for column in CATEGORY_COLUMNS:
        config[column] = st.column_config.SelectboxColumn(
            COLUMN_LABELS[column],
            options=sorted(original[column].dropna().unique().tolist()),
            required=True,
        )
    for column in SCORE_COLUMNS:
        config[column] = st.column_config.NumberColumn(
            COLUMN_LABELS[column],
            min_value=MIN_SCORE,
            max_value=MAX_SCORE,
            step=1,
            format="%d",
            required=True,
        )
    return config

"""Sidebar filters shared by the dashboard and the charts page."""

import pandas as pd
import streamlit as st

from student_analytics.config import COLUMN_LABELS, GENDER, GROUP, PARENT_EDUCATION, TEST_PREP

FILTER_COLUMNS = [GENDER, GROUP, PARENT_EDUCATION, TEST_PREP]


def filter_key(column: str) -> str:
    """Session state key where the selection for a column is saved."""
    return f"filter_{column}"


def _widget_key(column: str) -> str:
    return f"_{filter_key(column)}"


def init_filters() -> None:
    """Start every filter empty, which means no filtering."""
    for column in FILTER_COLUMNS:
        st.session_state.setdefault(filter_key(column), [])


def _save_selection(column: str) -> None:
    # Streamlit drops widget state when the widget is not on screen,
    # so the selection is copied to a key we own.
    st.session_state[filter_key(column)] = st.session_state[_widget_key(column)]


def _clear_filters() -> None:
    for column in FILTER_COLUMNS:
        st.session_state[filter_key(column)] = []
        st.session_state[_widget_key(column)] = []


def get_selections() -> dict:
    """Current filter values as {column: [selected values]}."""
    init_filters()
    return {column: st.session_state[filter_key(column)] for column in FILTER_COLUMNS}


def apply_filters(df: pd.DataFrame, selections: dict) -> pd.DataFrame:
    """Keep the rows that match every non empty selection."""
    mask = pd.Series(True, index=df.index)
    for column, values in selections.items():
        if values:
            mask &= df[column].isin(values)
    return df[mask]


def render_sidebar_filters(df: pd.DataFrame) -> None:
    """Draw one multiselect per filter. Options come from the data itself."""
    init_filters()
    st.sidebar.header("Filters")
    for column in FILTER_COLUMNS:
        options = sorted(df[column].dropna().unique().tolist())
        # An edit can remove a value, so drop saved values that are gone
        saved = [value for value in st.session_state[filter_key(column)] if value in options]
        st.session_state[filter_key(column)] = saved
        st.session_state[_widget_key(column)] = saved
        st.sidebar.multiselect(
            COLUMN_LABELS[column],
            options,
            key=_widget_key(column),
            on_change=_save_selection,
            args=(column,),
            placeholder="All",
        )
    st.sidebar.button("Clear filters", on_click=_clear_filters, width="stretch")
    st.sidebar.caption("Empty filter means all values.")


def filtered_data(df: pd.DataFrame) -> pd.DataFrame:
    """Render the sidebar and return the filtered rows."""
    render_sidebar_filters(df)
    return apply_filters(df, get_selections())

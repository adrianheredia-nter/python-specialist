"""Page 1: general overview with filters, KPIs and the filtered data."""

import pandas as pd
import streamlit as st

from student_analytics.charts import score_distribution_box
from student_analytics.config import MATH, READING, WRITING
from student_analytics.data import get_data
from student_analytics.filters import filtered_data
from student_analytics.metrics import compute_kpis, describe_scores


def _delta(value: float, reference: float, suffix: str = "") -> str | None:
    # Only show the difference when the filters change the numbers
    diff = value - reference
    return None if abs(diff) < 0.005 else f"{diff:+.2f}{suffix} vs all"


def show_kpis(df: pd.DataFrame, full_df: pd.DataFrame) -> None:
    """Five metric cards. The delta compares against the whole dataset."""
    kpis = compute_kpis(df)
    reference = compute_kpis(full_df)
    cards = [
        ("Avg. math", MATH),
        ("Avg. reading", READING),
        ("Avg. writing", WRITING),
    ]
    columns = st.columns(5)
    for column, (label, key) in zip(columns, cards):
        column.metric(label, f"{kpis[key]:.2f}", _delta(kpis[key], reference[key]))
    columns[3].metric("Students", kpis["students"])
    columns[4].metric(
        "Passed all 3",
        f"{kpis['pass_rate']:.1f}%",
        _delta(kpis["pass_rate"], reference["pass_rate"], " pts"),
        help="Score of 50 or more in math, reading and writing.",
    )


def show_statistics(df: pd.DataFrame) -> None:
    """Descriptive statistics, hidden in an expander by default."""
    with st.expander("Statistical analysis", expanded=False):
        st.dataframe(describe_scores(df).round(2), width="stretch")
        st.plotly_chart(score_distribution_box(df), width="stretch")
        st.caption(
            "The box shows the middle 50% of the scores. "
            "The line inside is the median and the dots are outliers."
        )


def main() -> None:
    """Render the dashboard page."""
    st.title("Students Performance Dashboard")
    full_df = get_data()
    df = filtered_data(full_df)

    if df.empty:
        st.warning("No students match the selected filters.")
        return

    show_kpis(df, full_df)

    st.subheader(f"Filtered data ({len(df)} of {len(full_df)} students)")
    st.dataframe(df, width="stretch")

    show_statistics(df)


main()

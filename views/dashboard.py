"""Page 1: general overview of the dataset."""

import streamlit as st

from student_analytics.data import get_data


def main() -> None:
    """Render the dashboard page."""
    st.title("Students Performance Dashboard")
    df = get_data()
    st.dataframe(df, width="stretch")


main()

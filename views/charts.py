"""Page 2: every chart asked in the exam except the statistics one."""

import matplotlib.pyplot as plt
import streamlit as st

from student_analytics import charts
from student_analytics.data import get_data
from student_analytics.filters import filtered_data


def main() -> None:
    """Render the charts page. Filters from the sidebar apply here too."""
    st.title("Charts")
    full_df = get_data()
    df = filtered_data(full_df)

    st.caption(f"Showing {len(df)} of {len(full_df)} students.")
    if df.empty:
        st.warning("Nothing to plot. Try removing some filters.")
        return

    left, right = st.columns(2)
    with left:
        st.subheader("Math by gender")
        fig = charts.math_by_gender_bar(df)
        st.pyplot(fig)
        plt.close(fig)
    with right:
        st.subheader("Reading by parental education")
        st.altair_chart(charts.reading_by_education_chart(df), width="stretch")

    left, right = st.columns(2)
    with left:
        st.subheader("Test preparation")
        st.plotly_chart(charts.test_prep_pie(df), width="stretch")
    with right:
        st.subheader("Passed students")
        st.plotly_chart(charts.passed_by_subject_bar(df), width="stretch")

    st.subheader("Correlation between scores")
    left, right = st.columns([3, 1])
    with left:
        st.plotly_chart(charts.score_correlation_scatter(df), width="stretch")
    with right:
        st.plotly_chart(charts.correlation_heatmap(df), width="stretch")
        st.caption("Values close to 1 mean the scores move together.")


main()

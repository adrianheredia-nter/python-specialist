"""Dataset loading and session state setup."""

import pandas as pd
import streamlit as st

from student_analytics.config import DATA_PATH

DATA_KEY = "students_df"


@st.cache_data(show_spinner=False)
def load_dataset(path=DATA_PATH) -> pd.DataFrame:
    """Read the original CSV. Streamlit caches the result between reruns."""
    return pd.read_csv(path)


def init_session_state() -> None:
    """Load the dataset into the session the first time the app runs.

    The working copy lives in st.session_state, so edits survive page changes.
    A browser refresh starts a new session and brings back the original data.
    """
    if DATA_KEY not in st.session_state:
        with st.spinner("Loading students dataset..."):
            st.session_state[DATA_KEY] = load_dataset().copy()
        st.toast(f"Dataset loaded: {len(st.session_state[DATA_KEY])} students")


def get_data() -> pd.DataFrame:
    """Return the working copy of the dataset for the current session."""
    init_session_state()
    return st.session_state[DATA_KEY]


def set_data(df: pd.DataFrame) -> None:
    """Replace the working copy of the dataset."""
    st.session_state[DATA_KEY] = df


def reset_data() -> None:
    """Throw away the session changes and go back to the original CSV."""
    st.session_state[DATA_KEY] = load_dataset().copy()

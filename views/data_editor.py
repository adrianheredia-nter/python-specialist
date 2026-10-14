"""Page 3: edit the dataset during the session."""

import streamlit as st

from student_analytics.data import get_data, load_dataset, reset_data, set_data
from student_analytics.editor import apply_editor_changes, column_config

VERSION_KEY = "editor_version"
SAVED_KEY = "editor_saved"


def _editor_key() -> str:
    # A new key gives a fresh editor after every save. Without it the
    # editor would apply the same pending changes twice.
    return f"students_editor_{st.session_state[VERSION_KEY]}"


def _save_changes() -> None:
    changes = st.session_state[_editor_key()]
    set_data(apply_editor_changes(get_data(), changes))
    st.session_state[VERSION_KEY] += 1
    st.session_state[SAVED_KEY] = True


def _restore_original() -> None:
    reset_data()
    st.session_state[VERSION_KEY] += 1
    st.toast("Original dataset restored")


def main() -> None:
    """Render the editor page."""
    st.session_state.setdefault(VERSION_KEY, 0)

    st.title("Data editor")
    st.write(
        "Edit any cell, add rows at the bottom or select rows and delete them. "
        "Changes are applied right away to the dashboard and the charts."
    )
    st.info(
        "Changes only last for this session. Refresh the browser or press the "
        "button below to get the original data back."
    )

    if st.session_state.pop(SAVED_KEY, False):
        st.toast("Changes saved")

    df = get_data()
    st.data_editor(
        df,
        key=_editor_key(),
        num_rows="dynamic",
        column_config=column_config(load_dataset()),
        on_change=_save_changes,
        width="stretch",
        height=500,
    )
    st.caption(f"{len(df)} students in the current session.")

    st.button("Restore original data", on_click=_restore_original, icon="↩️")


main()

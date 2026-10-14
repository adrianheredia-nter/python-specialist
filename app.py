"""Entry point. Run with: streamlit run app.py"""

import streamlit as st

from student_analytics.data import init_session_state

st.set_page_config(page_title="Students Performance", page_icon="📊", layout="wide")

# Load the data once per session, before any page is rendered
init_session_state()

pages = [
    st.Page("views/dashboard.py", title="Dashboard", icon="🏠", default=True),
    st.Page("views/charts.py", title="Charts", icon="📈"),
]

st.navigation(pages).run()

"""Smoke tests that run the real pages with Streamlit's AppTest."""
# pylint: disable=missing-function-docstring

from pathlib import Path

from streamlit.testing.v1 import AppTest

from student_analytics.config import GENDER
from student_analytics.data import DATA_KEY

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def run_app(page: str | None = None) -> AppTest:
    at = AppTest.from_file(APP, default_timeout=30).run()
    if page:
        at.switch_page(page).run()
    assert not at.exception
    return at


def test_dashboard_shows_kpis():
    at = run_app()
    labels = [metric.label for metric in at.metric]
    assert labels == ["Avg. math", "Avg. reading", "Avg. writing", "Students", "Passed all 3"]
    assert at.metric[3].value == "1000"
    assert at.metric[4].value == "81.2%"


def test_filter_updates_kpis():
    at = run_app()
    at.sidebar.multiselect[0].select("female").run()
    assert not at.exception
    students = at.metric[3].value
    expected = (at.session_state[DATA_KEY][GENDER] == "female").sum()
    assert students == str(expected)


def test_charts_page_renders():
    at = run_app("views/charts.py")
    subheaders = [item.value for item in at.subheader]
    assert "Math by gender" in subheaders
    assert "Correlation between scores" in subheaders


def test_editor_page_renders():
    at = run_app("views/data_editor.py")
    assert at.title[0].value == "Data editor"
    assert any("1000 students" in item.value for item in at.caption)

"""KPIs and descriptive statistics. Pure pandas, no Streamlit here."""

import pandas as pd

from student_analytics.config import PASS_MARK, SCORE_COLUMNS, SUBJECT_LABELS


def passed_all(df: pd.DataFrame) -> pd.Series:
    """True for students with 50 or more in math, reading and writing."""
    return (df[SCORE_COLUMNS] >= PASS_MARK).all(axis=1)


def pass_rate(df: pd.DataFrame) -> float:
    """Percentage of students that passed the three subjects."""
    if df.empty:
        return 0.0
    return float(passed_all(df).mean() * 100)


def compute_kpis(df: pd.DataFrame) -> dict:
    """Averages per subject, number of students and pass rate."""
    kpis = {column: float(df[column].mean()) for column in SCORE_COLUMNS}
    kpis["students"] = len(df)
    kpis["pass_rate"] = pass_rate(df)
    return kpis

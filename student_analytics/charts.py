"""Chart builders. Each function gets a DataFrame and returns a figure."""

import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px

from student_analytics.config import (
    COLUMN_LABELS,
    EDUCATION_ORDER,
    GENDER,
    LUNCH,
    MATH,
    PARENT_EDUCATION,
    READING,
    SCORE_COLUMNS,
    SUBJECT_LABELS,
    TEST_PREP,
    WRITING,
)
from student_analytics.metrics import mean_by, passed_by_subject, scores_long

SUBJECT_COLORS = {"Math": "#4C78A8", "Reading": "#F58518", "Writing": "#54A24B"}
GENDER_COLORS = {"female": "#E45756", "male": "#4C78A8"}
RESULT_COLORS = {"Passed": "#54A24B", "Failed": "#E45756"}


def math_by_gender_bar(df):
    """Matplotlib bar chart with the average math score per gender."""
    means = mean_by(df, GENDER, MATH)
    colors = [GENDER_COLORS.get(gender, "#999999") for gender in means[GENDER]]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(means[GENDER].str.capitalize(), means[MATH], color=colors, edgecolor="black")
    ax.bar_label(bars, fmt="%.1f", padding=3)
    ax.set_title("Average math score by gender", fontweight="bold")
    ax.set_xlabel("Gender")
    ax.set_ylabel("Average math score")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


def reading_by_education_chart(df):
    """Altair horizontal bars: average reading score per parental education.

    Education levels keep their natural order, so the trend is easy to read.
    Hovering a bar highlights it and shows the exact values.
    """
    data = df.groupby(PARENT_EDUCATION, as_index=False).agg(
        avg_reading=(READING, "mean"), students=(READING, "size")
    )
    hover = alt.selection_point(on="pointerover", fields=[PARENT_EDUCATION], empty=False)
    label = COLUMN_LABELS[PARENT_EDUCATION]

    bars = (
        alt.Chart(data)
        .mark_bar(cornerRadiusEnd=4)
        .encode(
            x=alt.X("avg_reading:Q", title="Average reading score", scale=alt.Scale(domain=[0, 100])),
            y=alt.Y(f"{PARENT_EDUCATION}:N", title=label, sort=EDUCATION_ORDER),
            color=alt.condition(hover, alt.value("#F58518"), alt.value("#4C78A8")),
            tooltip=[
                alt.Tooltip(f"{PARENT_EDUCATION}:N", title=label),
                alt.Tooltip("avg_reading:Q", title="Avg. reading", format=".2f"),
                alt.Tooltip("students:Q", title="Students"),
            ],
        )
        .add_params(hover)
    )
    text = bars.mark_text(align="left", dx=4).encode(
        text=alt.Text("avg_reading:Q", format=".1f"), color=alt.value("black")
    )
    return (bars + text).properties(
        title="Average reading score by parental education", height=320
    )


def test_prep_pie(df):
    """Plotly pie chart with students who completed the preparation course or not."""
    counts = df[TEST_PREP].value_counts().rename_axis("Course").reset_index(name="Students")
    fig = px.pie(
        counts,
        names="Course",
        values="Students",
        color="Course",
        color_discrete_map={"completed": "#54A24B", "none": "#BAB0AC"},
        hole=0.35,
        title="Test preparation course",
    )
    fig.update_traces(textinfo="percent+label+value")
    return fig


def passed_by_subject_bar(df):
    """Plotly grouped bars with passed and failed students per subject."""
    fig = px.bar(
        passed_by_subject(df),
        x="Subject",
        y="Students",
        color="Result",
        barmode="group",
        text="Students",
        color_discrete_map=RESULT_COLORS,
        title="Passed and failed students by subject (pass mark 50)",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis_title="Students", xaxis_title=None)
    return fig


def score_correlation_scatter(df):
    """Plotly scatter: math vs reading, sized by writing and colored by gender."""
    fig = px.scatter(
        df.dropna(subset=SCORE_COLUMNS),
        x=MATH,
        y=READING,
        size=WRITING,
        color=GENDER,
        color_discrete_map=GENDER_COLORS,
        hover_data=[LUNCH, PARENT_EDUCATION, TEST_PREP],
        labels=COLUMN_LABELS,
        size_max=12,
        opacity=0.7,
        title="Math vs reading score (size = writing score)",
    )
    return fig


def correlation_heatmap(df):
    """Plotly heatmap with the Pearson correlation between the three scores."""
    corr = df[SCORE_COLUMNS].corr().rename(index=SUBJECT_LABELS, columns=SUBJECT_LABELS)
    fig = px.imshow(
        corr,
        text_auto=".2f",
        zmin=-1,
        zmax=1,
        color_continuous_scale="RdBu_r",
        title="Correlation between scores",
    )
    return fig


def score_distribution_box(df):
    """Plotly box plot with the score distribution of each subject."""
    fig = px.box(
        scores_long(df),
        x="Subject",
        y="Score",
        color="Subject",
        color_discrete_map=SUBJECT_COLORS,
        points="outliers",
        title="Score distribution by subject",
    )
    fig.update_layout(showlegend=False, yaxis_range=[0, 105])
    return fig

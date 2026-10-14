"""Chart builders. Each function gets a DataFrame and returns a figure."""

import plotly.express as px

from student_analytics.metrics import scores_long

SUBJECT_COLORS = {"Math": "#4C78A8", "Reading": "#F58518", "Writing": "#54A24B"}


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

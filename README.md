# python-specialist

Streamlit app to explore the Students Performance dataset. It covers the Python Specialist ordinary exam: filters, KPIs, statistics, charts and a data editor.

The dataset has 1000 students with their math, reading and writing scores. It also includes gender, group, parental education, lunch and test preparation.

## Requirements

- Python 3.10 or newer
- The packages in `requirements.txt`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

Use `requirements.txt` instead if you only want to run the app.

## Run

```bash
streamlit run app.py
```

The app opens at http://localhost:8501.

## Pages

**Dashboard**

- Sidebar filters by gender, group, parental education and test preparation. They can be combined.
- Filter options are read from the data. Selections are kept while you move between pages.
- KPIs: average math, reading and writing, number of students and percentage that passed all three.
- Table with the filtered students.
- "Statistical analysis" expander with mean, median, standard deviation, min and max, plus a box plot.

**Charts**

- Average math score by gender (Matplotlib).
- Average reading score by parental education (Altair).
- Students with and without test preparation (Plotly pie).
- Passed students per subject (Plotly).
- Math vs reading scatter. Point size is the writing score and color is the gender. The hover shows lunch, parental education and test preparation.
- Correlation heatmap between the three scores.

The sidebar filters also apply here.

**Data editor**

- Edit any cell with `st.data_editor`. Categories use dropdowns and scores only accept 0 to 100.
- Add rows at the bottom or select rows and delete them.
- Changes update the dashboard and the charts right away.
- "Restore original data" reloads the CSV.

Changes live in `st.session_state` only. The CSV file is never modified, so refreshing the browser brings back the original data.

## Pass rule

A student passes a subject with a score of 50 or more. "Passed all 3" means 50 or more in math, reading and writing. The value is `PASS_MARK` in `student_analytics/config.py`.

## Project structure

```
app.py                     entry point and navigation
views/
  dashboard.py             filters, KPIs, table and statistics
  charts.py                all the charts
  data_editor.py           editable table
student_analytics/
  config.py                paths, column names and constants
  data.py                  cached CSV load and session state
  filters.py               sidebar filters
  metrics.py               KPIs and statistics
  charts.py                chart builders
  editor.py                applies the data editor changes
data/StudentsPerformance.csv
tests/
```

Pages only draw things. The logic lives in `student_analytics`, so it can be tested without running Streamlit.

## Tests

```bash
pytest
pylint app.py student_analytics views tests
```

`tests/test_app.py` runs the real pages with Streamlit's `AppTest`. The other files test filters, metrics and the editor logic.

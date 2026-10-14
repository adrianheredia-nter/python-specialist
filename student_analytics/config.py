"""Constants shared across the app: paths, column names and labels."""

from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "StudentsPerformance.csv"

# Dataset columns
GENDER = "gender"
GROUP = "race/ethnicity"
PARENT_EDUCATION = "parental level of education"
LUNCH = "lunch"
TEST_PREP = "test preparation course"
MATH = "math score"
READING = "reading score"
WRITING = "writing score"

SCORE_COLUMNS = [MATH, READING, WRITING]
CATEGORY_COLUMNS = [GENDER, GROUP, PARENT_EDUCATION, LUNCH, TEST_PREP]

SUBJECT_LABELS = {MATH: "Math", READING: "Reading", WRITING: "Writing"}

COLUMN_LABELS = {
    GENDER: "Gender",
    GROUP: "Group",
    PARENT_EDUCATION: "Parental education",
    LUNCH: "Lunch",
    TEST_PREP: "Test preparation",
    MATH: "Math score",
    READING: "Reading score",
    WRITING: "Writing score",
}

# A student passes a subject with a score of 50 or more
PASS_MARK = 50
MIN_SCORE = 0
MAX_SCORE = 100

# Natural order for the parents' education level, lowest to highest
EDUCATION_ORDER = [
    "some high school",
    "high school",
    "some college",
    "associate's degree",
    "bachelor's degree",
    "master's degree",
]

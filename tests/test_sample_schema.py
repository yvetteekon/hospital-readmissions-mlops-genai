from pathlib import Path

import pandas as pd

SAMPLE = Path("tests/data/hospital_readmissions_sample.csv")
REQUIRED = {
    "age",
    "time_in_hospital",
    "n_lab_procedures",
    "n_procedures",
    "n_medications",
    "n_outpatient",
    "n_inpatient",
    "n_emergency",
    "medical_specialty",
    "diag_1",
    "diag_2",
    "diag_3",
    "glucose_test",
    "A1Ctest",
    "change",
    "diabetes_med",
    "readmitted",
}

def test_sample_exists():
    assert SAMPLE.exists()

def test_sample_has_required_columns():
    df = pd.read_csv(SAMPLE)
    assert REQUIRED.issubset(df.columns)

def test_sample_is_small():
    df = pd.read_csv(SAMPLE)
    assert 5 <= len(df) <= 100
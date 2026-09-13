from pathlib import Path

import pandas as pd
from great_expectations.dataset import PandasDataset

SAMPLE = Path("tests/data/hospital_readmissions_sample.csv")
REQUIRED = [
    "age", "time_in_hospital", "n_lab_procedures", "n_procedures",
    "n_medications", "n_outpatient", "n_inpatient", "n_emergency",
    "medical_specialty", "diag_1", "diag_2", "diag_3",
    "glucose_test", "A1Ctest", "change", "diabetes_med", "readmitted",
]

def main() -> None:
    df = PandasDataset(pd.read_csv(SAMPLE))
    assert df.expect_table_columns_to_match_set(REQUIRED).success
    assert df.expect_column_values_to_not_be_null("readmitted").success
    assert df.expect_column_values_to_be_in_set("readmitted", ["yes", "no"]).success
    assert df.expect_column_values_to_be_in_set(
        "age",
        ["[40-50)", "[50-60)", "[60-70)", "[70-80)", "[80-90)", "[90-100)"],
    ).success
    assert df.expect_column_values_to_be_between(
        "time_in_hospital", min_value=1, max_value=14
    ).success

if __name__ == "__main__":
    main()
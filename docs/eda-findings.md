# EDA findings

Source: `notebooks/01 exploratory data analysis.ipynb`  
Notebooks stay on `chore/exploration-eda`. This file is what `develop` should carry.

## Dataset

- **File:** `data/raw/hospital_readmissions.csv`
- **N:** 25,000 patient encounters
- **Target:** `readmitted` (`yes` / `no`)

| Column | Role |
|--------|------|
| `age` | Age band: `[40-50)` … `[90-100)` |
| `time_in_hospital` | Length of stay (days) |
| `n_lab_procedures` | Lab procedures during stay |
| `n_procedures` | Other procedures during stay |
| `n_medications` | Distinct medications |
| `n_outpatient` | Outpatient visits in prior year |
| `n_inpatient` | Inpatient visits in prior year |
| `n_emergency` | Emergency visits in prior year |
| `medical_specialty` | Attending specialty |
| `diag_1`, `diag_2`, `diag_3` | Primary / secondary / tertiary diagnosis group |
| `glucose_test`, `A1Ctest` | `no` / `normal` / `high` |
| `change` | Medication change (`yes` / `no`) |
| `diabetes_med` | On diabetes medication (`yes` / `no`) |

Derived in EDA only: `n_diabetes_diag` = count of `Diabetes` among `diag_1`–`diag_3` (0–3).

## Problem size

About **1 in 2 patients** was readmitted (analysis of 25,000 patients). Classes are close to balanced (~47% / 53%).

Figure: `reports/figures/target distribution.png`

## Key insight 1 — primary diagnosis by age

Heatmap of `diag_1` within each age band (`reports/figures/primary diagnosis by age group.png`):

- Ages **50 and above:** **Circulatory** is the most common primary diagnosis
- Ages **under 50:** **Other** is the most common primary diagnosis

## Key insight 2 — diabetes diagnosis vs readmission

A patient can have 0–3 diabetes diagnoses across `diag_1`, `diag_2`, and `diag_3`.

Hypothesis test at α = 0.05:

- **H0:** diabetes diagnosis is not correlated with readmission
- **H1:** diabetes diagnosis is correlated with readmission
- **p-value for `n_diabetes_diag` = 0.53** (> 0.05)

**Decision:** accept H0. Diabetes diagnosis count is not a targeting rule.

## Feature distributions

Utilization counts (`n_outpatient`, `n_inpatient`, `n_emergency`) are mostly 0 with a long tail. Typical stay is ~4 days, ~16 medications, ~43 lab procedures.

`Missing` is a real level for specialty and diagnoses — keep those rows.

## Carry into modeling

- Keep original predictors; `n_diabetes_diag` is optional
- Ordinal-encode `age`, `glucose_test`, `A1Ctest`
- One-hot encode specialty, diagnoses, `change`, `diabetes_med`
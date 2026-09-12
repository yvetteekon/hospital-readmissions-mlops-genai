# EDA and model findings

Short summary of decisions from exploratory analysis and post-model evaluation. Notebooks stay on `chore/exploration-eda`. This file is what `develop` should carry forward.

## Target

- **Outcome:** 30-day hospital readmission (`readmitted`)
- **Positive class:** patient was readmitted
- **Task:** binary classification used for **risk ranking and outreach prioritization**, not as a standalone clinical decision

Overall readmission rate in the evaluation set is about **47%**.

## Key features

Strongest SHAP drivers of predicted risk:

| Rank | Feature | Mean \|SHAP\| | Direction |
|------|---------|---------------|-----------|
| 1 | `n_inpatient` | 0.32 | More prior inpatient visits → higher risk |
| 2 | `n_outpatient` | 0.10 | More outpatient visits → higher risk |
| 3 | `n_procedures` | 0.07 | More procedures → higher risk |

Utilization history dominates age, diagnoses, and medication counts. High `n_emergency` can also raise risk for some patients, but it is not in the top 3 by average importance.

**Implication:** prioritize follow-up for patients with heavy prior inpatient use, then outpatient / procedure volume.

## Metric choice

| Metric | Role in this project |
|--------|----------------------|
| ROC-AUC | Overall ranking quality |
| Precision–Recall | More relevant than ROC because we care about the readmitted class and outreach cost |
| F0.5 | Precision-leaning operating point when follow-up capacity is limited |
| F2 | Recall-leaning; in this model it flagged nearly everyone, so it is not operationally useful |
| Queue rate | Share of patients flagged at a threshold |
| Lift / gain / deciles | How well ranking concentrates true readmissions |

**Decision:** do not optimize for F2. High recall required flagging ~87–99% of patients. Prefer a **capacity-aware threshold** or F0.5.

Example threshold comparison (training/evaluation run):

| Objective | Threshold | Precision | Recall | Queue rate |
|-----------|-----------|-----------|--------|------------|
| F0.5 | 0.47 | 0.61 | 0.50 | 38% |
| F1 | 0.35 | 0.49 | 0.92 | 87% |
| F2 | 0.26 | 0.47 | 1.00 | 99% |

Recommended starting point: **threshold ≈ 0.47 (F0.5)** or “flag the top ~40% by predicted probability.”

Use `predict_proba` for ROC, PR, gain, and lift. Use hard `predict` labels only after a threshold is chosen.

## Threshold and decile takeaway

- Ranking power is **modest**.
- Peak KS was around the **top 40%** of patients (about deciles 1–4).
- At the top 50%, the model captured about 50% of readmissions — close to random selection.
- Beyond 40–50% outreach, extra contacts add little.

**Gain:** the curve stays near the random diagonal; the useful part is the top 40%.

**Lift:** highest among the very top-ranked patients (about 2.1 at the extreme top), then declines toward 1.0. Top 20% ≈ 1.45 lift; top 40% ≈ 1.28; top 50% ≈ 1.22.

**Practical rule:** focus care-management resources on the **highest-risk ~40%**. Do not treat the score as a precise individual diagnosis.

## What to build next

- Scoring pipeline should output **probability**, decile/rank, and top contributing features.
- Streamlit MVP: score a patient, show risk band, show `n_inpatient` / `n_outpatient` / `n_procedures`.
- Later GenAI/RAG can reuse these findings as knowledge docs, not as a second model.
# Patch Report: Step 10.3 - Dataset Selection Rationale

## Purpose

This patch adds a clear explanation of why the project uses the University of Liverpool DataCat / PLOS ONE public dog growth dataset instead of choosing a random Kaggle dog dataset.

The goal is to make the data-source decision easier to defend during the final project review.

---

## Files Changed

```text
README.md
HOW_TO_RUN.md
DATA_SOURCES.md
PROJECT_BRIEF.md
COURSE_TOPIC_MAPPING.md
docs/real_data_source_notes.md
docs/dataset_selection_rationale.md
PATCH_REPORT_STEP10_3_DATASET_SELECTION_RATIONALE.md
```

---

## What Was Added

- Added a dedicated dataset-selection rationale document.
- Explained that Kaggle is useful for dataset discovery, but not every dog dataset fits a growth-monitoring task.
- Clarified why the selected Liverpool DataCat / PLOS ONE dataset is a better fit for age/bodyweight growth modelling.
- Strengthened the honest project boundary: real public dog growth data foundation + Cane Corso product context.
- Added future direction for a Cane Corso-specific longitudinal dataset.
- Fixed run-command wording for the practical workflow in documentation.
- Updated notebook count/review order and project structure references where needed.

---

## Responsible Interpretation

This patch does not change the modelling logic or claim that the project is trained on private real Cane Corso veterinary data.

Correct interpretation:

```text
The project uses real public dog-growth data and applies the workflow to a Cane Corso Growth Intelligence concept.
```

Incorrect interpretation:

```text
The project proves a veterinary or breed-specific conclusion for all Cane Corso dogs.
```

---

## Validation Notes

This is a documentation and project-explanation patch. It does not require retraining the models.

Recommended local checks after applying:

```powershell
python src/create_time_series_features.py
python src/run_growth_assessment.py
git status
```

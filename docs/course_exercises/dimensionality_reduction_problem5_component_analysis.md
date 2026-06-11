# Problem 5 — Analyze and Visualize the Components

This document strengthens the most important requirement from the Dimensionality Reduction exercise: **analyze and visualize the components**.

## Original exercise intent

The exercise asks the student to:

- pick the best model or representation from the previous problem;
- inspect several SVD components;
- identify high-positive and high-negative terms;
- inspect example records with high values on each component;
- decide whether a component looks like a meaningful semantic axis;
- create at least two visualizations;
- explain whether visible clusters are real, useful, misleading, or caused by unrelated metadata.

## Project-safe adaptation

The original exercise uses a fake-job dataset. This repository stays lightweight and does not include external Kaggle data. The same method is adapted to a tiny Cane Corso growth-note sample:

- job postings become growth-monitoring notes;
- fake-job clusters become abnormal/risk growth-note groups;
- company/industry metadata becomes age, measurement, status, and wording effects;
- SVD components become latent semantic axes in growth text.

## Generated evidence

| Requirement | Evidence file |
|---|---|
| Top positive and low/opposite-loading terms | `reports/course_exercises/dimensionality_reduction_problem5_component_terms.csv` |
| Example records with high component values | `reports/course_exercises/dimensionality_reduction_problem5_component_examples.csv` |
| At least two visualization coordinate sets | `reports/course_exercises/dimensionality_reduction_problem5_visualization_coordinates.csv` |
| Written interpretation of clusters and misleading views | `reports/course_exercises/dimensionality_reduction_problem5_visualization_interpretation.md` |
| Notebook implementation | `notebooks/06_1_dimensionality_reduction_exercise_project_alignment.ipynb` |

## Why this matters

Problem 5 is where dimensionality reduction stops being only a transformation and becomes an interpretable ML tool. The model should not only produce components; the student must inspect whether the components make sense.

For this project, the safest conclusion is:

> Component analysis is useful for understanding growth-note language, but visual clusters should not be treated as biological proof until validated on real, larger Cane Corso growth records.

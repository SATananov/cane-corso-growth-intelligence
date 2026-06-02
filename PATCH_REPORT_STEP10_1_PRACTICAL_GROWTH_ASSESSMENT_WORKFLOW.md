# Patch Report — Step 10.1 Practical Growth Assessment Workflow

## Purpose

Step 10.1 adds a small applied workflow after the Feature Engineering and Time Series lecture.

The project now demonstrates a practical path:

```text
owner-style measurements -> engineered features -> reference comparison -> report
```

This makes the project more functional while still keeping the tone appropriate for a student who is learning the material step by step.

## Added Files

```text
data/input/example_new_cane_corso_measurements.csv
src/run_growth_assessment.py
data/processed/example_growth_assessment_features.csv
reports/example_growth_assessment_report.md
reports/figures/practical_growth_assessment_weight_trend.png
reports/figures/practical_growth_assessment_velocity_signal.png
docs/practical_growth_assessment_workflow.md
notebooks/05_1_practical_growth_assessment_workflow.ipynb
PATCH_REPORT_STEP10_1_PRACTICAL_GROWTH_ASSESSMENT_WORKFLOW.md
```

## Updated Files

```text
README.md
HOW_TO_RUN.md
COURSE_TOPIC_MAPPING.md
docs/math_foundation.md
```

## Mathematical Concepts Used

- consecutive differences;
- growth velocity;
- rolling average;
- weight-to-height ratio;
- z-score comparison;
- normalized Euclidean distance.

## Functional Value

The project can now be used as a simple educational growth-monitoring workflow. A user can provide repeated measurements and receive an automatically generated report with mathematical signals and figures.

## Safety Boundary

The workflow does not provide veterinary diagnosis, treatment advice, breed certification, pedigree proof, or official growth judgement. It is a learning and monitoring aid only.

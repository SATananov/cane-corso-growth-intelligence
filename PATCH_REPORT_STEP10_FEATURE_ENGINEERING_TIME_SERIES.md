# Patch Report — Step 10 Feature Engineering and Time Series

## Purpose

This step adds the next course topic to Cane Corso Growth Intelligence:

```text
Feature Engineering and Time Series
```

The update is designed to look professional, but still learning-oriented. The notebook explains the mathematical ideas clearly instead of pretending to be a finished production veterinary system.

## Added Files

```text
notebooks/05_feature_engineering_time_series_growth.ipynb
docs/feature_engineering_time_series_notes.md
src/create_time_series_features.py
data/processed/cane_corso_time_series_features.csv
reports/figures/time_series_weight_trajectory.png
reports/figures/time_series_growth_velocity.png
reports/figures/time_series_rolling_weight_average.png
reports/figures/feature_engineering_correlation_matrix.png
PATCH_REPORT_STEP10_FEATURE_ENGINEERING_TIME_SERIES.md
```

## Updated Files

```text
README.md
HOW_TO_RUN.md
COURSE_TOPIC_MAPPING.md
docs/math_foundation.md
```

## Mathematical Ideas Covered

The new notebook explains and applies:

- ordered records as a simple time series;
- lag features;
- weight gain and height gain;
- growth velocity;
- body proportion ratio;
- rolling average;
- z-score signal;
- correlation check between engineered features.

## Learning Tone

The notebook intentionally includes sections such as:

- learning objective;
- formulas before code;
- interpretation for the project;
- learning reflection;
- limitations and responsible use.

This keeps the work appropriate for a student project while still showing serious mathematical understanding.

## Responsible Boundaries

The step does not claim to provide veterinary diagnosis, medical advice, pedigree proof or breed certification. It describes the outputs as educational growth-monitoring signals only.

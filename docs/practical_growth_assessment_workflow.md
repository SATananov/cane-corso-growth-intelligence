# Practical Growth Assessment Workflow

This document explains the applied layer added in Step 10.1.

The goal is to show that the course project is not only a collection of notebooks. It can also be used as a small practical workflow:

```text
new Cane Corso measurements -> feature engineering -> mathematical signals -> readable report
```

## Input

The example owner-style input file is:

```text
data/input/example_new_cane_corso_measurements.csv
```

Each row represents one measurement over time:

```text
dog_id, dog_name, sex, age_months, weight_kg, height_cm, activity_level
```

This is intentionally simple because the project is still a learning project. A real product would need stronger validation, more real data, veterinary review and better user interface.

## Mathematical Features

The workflow uses the same mathematical ideas from the Feature Engineering and Time Series lecture.

### Difference feature

```text
weight_gain(t) = weight(t) - weight(t-1)
```

This shows the absolute change between two consecutive measurements.

### Growth velocity

```text
growth_velocity(t) = weight_gain(t) / delta_age(t)
```

This converts growth into a rate of change per month.

### Ratio feature

```text
weight_to_height_ratio(t) = weight_kg(t) / height_cm(t)
```

This is a simple proportion signal. In this project it is used only for learning and monitoring, not as a medical score.

### Rolling mean

```text
rolling_mean_3(t) = average(x(t), x(t-1), x(t-2))
```

The rolling mean smooths short-term movement and makes the trend easier to interpret.

### Z-score signal

```text
z = (latest_velocity - reference_mean_velocity) / reference_standard_deviation
```

The z-score helps describe whether the latest growth velocity is close to or far from the reference growth velocity distribution.

## Reference Comparison

The latest record is compared with the existing project reference features in:

```text
data/processed/cane_corso_time_series_features.csv
```

The workflow also calculates a simple normalized Euclidean distance:

```text
distance = sqrt(sum((x_latest_scaled - x_reference_scaled)^2))
```

This does not prove health status. It only gives a mathematical similarity signal inside the educational dataset.

## Outputs

Running the script creates:

```text
data/processed/example_growth_assessment_features.csv
reports/example_growth_assessment_report.md
reports/figures/practical_growth_assessment_weight_trend.png
reports/figures/practical_growth_assessment_velocity_signal.png
```

## How to Run

From the project root:

```powershell
& ".\.venv\Scripts\python.exe" "srcun_growth_assessment.py"
```

Optional notebook walkthrough:

```text
notebooks/05_1_practical_growth_assessment_workflow.ipynb
```

## Responsible Use

This workflow is educational. It does not diagnose disease, prescribe treatment, replace veterinary care, certify Cane Corso quality, or prove pedigree. It only demonstrates how machine learning feature engineering can be connected to a practical growth-monitoring use case.

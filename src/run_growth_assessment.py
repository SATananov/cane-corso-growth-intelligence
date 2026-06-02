"""Practical Cane Corso growth assessment workflow.

This script is part of the learning project. It does not diagnose health,
recommend treatment, certify breed quality, or replace veterinary judgement.
It converts a small owner-style measurement file into engineered growth
features, compares the latest record with the project reference sample, and
writes a readable educational report.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "input" / "example_new_cane_corso_measurements.csv"
REFERENCE_PATH = PROJECT_ROOT / "data" / "processed" / "cane_corso_time_series_features.csv"
OUTPUT_FEATURES_PATH = PROJECT_ROOT / "data" / "processed" / "example_growth_assessment_features.csv"
REPORT_PATH = PROJECT_ROOT / "reports" / "example_growth_assessment_report.md"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
WEIGHT_FIGURE_PATH = FIGURES_DIR / "practical_growth_assessment_weight_trend.png"
VELOCITY_FIGURE_PATH = FIGURES_DIR / "practical_growth_assessment_velocity_signal.png"

REQUIRED_INPUT_COLUMNS = {
    "dog_id",
    "dog_name",
    "sex",
    "age_months",
    "weight_kg",
    "height_cm",
    "activity_level",
}

FEATURE_COLUMNS_FOR_DISTANCE = [
    "age_months",
    "weight_kg",
    "height_cm",
    "growth_velocity_kg_per_month",
    "weight_to_height_ratio",
]


@dataclass
class AssessmentResult:
    dog_name: str
    latest_age_months: float
    latest_weight_kg: float
    latest_height_cm: float
    latest_growth_velocity: float
    reference_velocity_mean: float
    reference_velocity_std: float
    velocity_z_score: float
    expected_weight_at_age: float
    weight_deviation_percent: float
    nearest_profile_distance: float
    practical_signal: str
    interpretation_points: List[str]


def load_measurements(input_path: Path = INPUT_PATH) -> pd.DataFrame:
    """Load owner-style measurement records and validate required columns."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    data = pd.read_csv(input_path)
    missing = REQUIRED_INPUT_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"Input file is missing required columns: {sorted(missing)}")

    data = data.copy()
    data["age_months"] = pd.to_numeric(data["age_months"], errors="raise")
    data["weight_kg"] = pd.to_numeric(data["weight_kg"], errors="raise")
    data["height_cm"] = pd.to_numeric(data["height_cm"], errors="raise")
    data = data.sort_values(["dog_id", "age_months"]).reset_index(drop=True)
    return data


def engineer_time_series_features(data: pd.DataFrame) -> pd.DataFrame:
    """Create practical time-series features from consecutive measurements."""
    features = data.copy().sort_values(["dog_id", "age_months"]).reset_index(drop=True)
    grouped = features.groupby("dog_id", sort=False)

    features["previous_age_months"] = grouped["age_months"].shift(1)
    features["previous_weight_kg"] = grouped["weight_kg"].shift(1)
    features["previous_height_cm"] = grouped["height_cm"].shift(1)

    features["delta_age_months"] = features["age_months"] - features["previous_age_months"]
    features["weight_gain_kg"] = features["weight_kg"] - features["previous_weight_kg"]
    features["height_gain_cm"] = features["height_cm"] - features["previous_height_cm"]

    features["growth_velocity_kg_per_month"] = features["weight_gain_kg"] / features["delta_age_months"]
    features["height_velocity_cm_per_month"] = features["height_gain_cm"] / features["delta_age_months"]
    features["weight_to_height_ratio"] = features["weight_kg"] / features["height_cm"]

    features["rolling_weight_mean_3"] = grouped["weight_kg"].transform(lambda values: values.rolling(3, min_periods=1).mean())
    features["rolling_growth_velocity_3"] = grouped["growth_velocity_kg_per_month"].transform(
        lambda values: values.rolling(3, min_periods=1).mean()
    )

    features["growth_phase"] = pd.cut(
        features["age_months"],
        bins=[0, 6, 12, 18, 36],
        labels=["early_growth", "adolescent_growth", "young_adult", "adult_monitoring"],
        include_lowest=True,
    ).astype(str)

    return features


def _safe_standard_deviation(values: pd.Series) -> float:
    std = float(values.std(ddof=0))
    return std if std > 0 else 1.0


def _reference_subset(reference: pd.DataFrame, latest: pd.Series) -> pd.DataFrame:
    sex = str(latest.get("sex", "")).lower()
    same_sex = reference[reference["sex"].astype(str).str.lower() == sex]
    return same_sex if len(same_sex) >= 5 else reference


def _expected_weight_at_age(reference_subset: pd.DataFrame, age_months: float) -> float:
    reference = reference_subset.copy()
    reference["age_distance"] = (reference["age_months"] - age_months).abs()
    closest_distance = reference["age_distance"].min()
    closest_records = reference[reference["age_distance"] == closest_distance]
    return float(closest_records["weight_kg"].mean())


def _nearest_profile_distance(reference_subset: pd.DataFrame, latest: pd.Series) -> float:
    complete_reference = reference_subset.dropna(subset=FEATURE_COLUMNS_FOR_DISTANCE).copy()
    if complete_reference.empty:
        return 0.0

    means = complete_reference[FEATURE_COLUMNS_FOR_DISTANCE].mean()
    stds = complete_reference[FEATURE_COLUMNS_FOR_DISTANCE].std(ddof=0).replace(0, 1)

    reference_scaled = (complete_reference[FEATURE_COLUMNS_FOR_DISTANCE] - means) / stds
    latest_vector = latest[FEATURE_COLUMNS_FOR_DISTANCE].astype(float)
    latest_scaled = (latest_vector - means) / stds
    distances = ((reference_scaled - latest_scaled) ** 2).sum(axis=1) ** 0.5
    return float(distances.min())


def assess_latest_record(features: pd.DataFrame, reference: pd.DataFrame) -> AssessmentResult:
    """Create a simple educational assessment from the latest measurement."""
    latest = features.sort_values("age_months").iloc[-1]
    reference_subset = _reference_subset(reference, latest)

    velocity_reference = reference_subset["growth_velocity_kg_per_month"].dropna()
    reference_velocity_mean = float(velocity_reference.mean())
    reference_velocity_std = _safe_standard_deviation(velocity_reference)

    latest_velocity = float(latest["growth_velocity_kg_per_month"])
    velocity_z_score = (latest_velocity - reference_velocity_mean) / reference_velocity_std

    expected_weight = _expected_weight_at_age(reference_subset, float(latest["age_months"]))
    weight_deviation_percent = ((float(latest["weight_kg"]) - expected_weight) / expected_weight) * 100
    nearest_distance = _nearest_profile_distance(reference_subset, latest)

    interpretation_points: List[str] = []

    if abs(velocity_z_score) < 1:
        velocity_signal = "within_reference_learning_band"
        interpretation_points.append(
            "The latest growth velocity is within one standard deviation of the reference mean."
        )
    elif velocity_z_score >= 1:
        velocity_signal = "above_reference_learning_band"
        interpretation_points.append(
            "The latest growth velocity is above the reference band and deserves careful trend review."
        )
    else:
        velocity_signal = "below_reference_learning_band"
        interpretation_points.append(
            "The latest growth velocity is below the reference band and deserves careful trend review."
        )

    if abs(weight_deviation_percent) <= 15:
        weight_signal = "weight_close_to_age_reference"
        interpretation_points.append(
            "The latest weight is reasonably close to the nearest age-based reference records."
        )
    elif weight_deviation_percent > 15:
        weight_signal = "weight_above_age_reference"
        interpretation_points.append(
            "The latest weight is noticeably above the nearest age-based reference records."
        )
    else:
        weight_signal = "weight_below_age_reference"
        interpretation_points.append(
            "The latest weight is noticeably below the nearest age-based reference records."
        )

    if velocity_signal == "within_reference_learning_band" and weight_signal == "weight_close_to_age_reference":
        practical_signal = "monitoring_signal_stable_in_learning_context"
    else:
        practical_signal = "monitoring_signal_review_trend_in_learning_context"

    return AssessmentResult(
        dog_name=str(latest["dog_name"]),
        latest_age_months=float(latest["age_months"]),
        latest_weight_kg=float(latest["weight_kg"]),
        latest_height_cm=float(latest["height_cm"]),
        latest_growth_velocity=latest_velocity,
        reference_velocity_mean=reference_velocity_mean,
        reference_velocity_std=reference_velocity_std,
        velocity_z_score=float(velocity_z_score),
        expected_weight_at_age=expected_weight,
        weight_deviation_percent=float(weight_deviation_percent),
        nearest_profile_distance=nearest_distance,
        practical_signal=practical_signal,
        interpretation_points=interpretation_points,
    )


def create_figures(features: pd.DataFrame, assessment: AssessmentResult) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    ordered = features.sort_values("age_months")

    plt.figure(figsize=(8, 5))
    plt.plot(ordered["age_months"], ordered["weight_kg"], marker="o", label="Measured weight")
    plt.plot(ordered["age_months"], ordered["rolling_weight_mean_3"], marker="s", label="Rolling mean")
    plt.xlabel("Age in months")
    plt.ylabel("Weight in kg")
    plt.title("Practical Growth Assessment: Weight Trend")
    plt.legend()
    plt.tight_layout()
    plt.savefig(WEIGHT_FIGURE_PATH, dpi=160)
    plt.close()

    velocity = ordered.dropna(subset=["growth_velocity_kg_per_month"])
    plt.figure(figsize=(8, 5))
    plt.plot(velocity["age_months"], velocity["growth_velocity_kg_per_month"], marker="o", label="Growth velocity")
    plt.axhline(assessment.reference_velocity_mean, linestyle="--", label="Reference mean velocity")
    plt.axhline(
        assessment.reference_velocity_mean + assessment.reference_velocity_std,
        linestyle=":",
        label="Reference mean + 1 std",
    )
    plt.axhline(
        assessment.reference_velocity_mean - assessment.reference_velocity_std,
        linestyle=":",
        label="Reference mean - 1 std",
    )
    plt.xlabel("Age in months")
    plt.ylabel("kg per month")
    plt.title("Practical Growth Assessment: Velocity Signal")
    plt.legend()
    plt.tight_layout()
    plt.savefig(VELOCITY_FIGURE_PATH, dpi=160)
    plt.close()


def write_report(assessment: AssessmentResult, features: pd.DataFrame, input_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    interpretation = "\n".join(f"- {point}" for point in assessment.interpretation_points)
    latest_features = features.sort_values("age_months").iloc[-1]

    report = f"""# Practical Cane Corso Growth Assessment Report

This report is generated by `src/run_growth_assessment.py` from the example owner-style input file:

```text
{input_path.relative_to(PROJECT_ROOT)}
```

## Learning Purpose

This is a practical workflow layer for the course project. It shows how the mathematical features from the Feature Engineering and Time Series lecture can be used in a small applied pipeline:

```text
input measurements -> engineered features -> reference comparison -> readable report
```

It is intentionally educational. It is not a veterinary diagnosis, treatment recommendation, pedigree proof, or Cane Corso certification.

## Latest Measurement Summary

| Field | Value |
|---|---:|
| Dog name | {assessment.dog_name} |
| Latest age | {assessment.latest_age_months:.1f} months |
| Latest weight | {assessment.latest_weight_kg:.1f} kg |
| Latest height | {assessment.latest_height_cm:.1f} cm |
| Weight-to-height ratio | {float(latest_features['weight_to_height_ratio']):.3f} |
| Growth velocity | {assessment.latest_growth_velocity:.2f} kg/month |
| Rolling weight mean | {float(latest_features['rolling_weight_mean_3']):.2f} kg |

## Mathematical Signals

### Growth Velocity

```text
growth_velocity(t) = (weight(t) - weight(t-1)) / (age(t) - age(t-1))
```

Latest value:

```text
{assessment.latest_growth_velocity:.2f} kg/month
```

### Z-Score Against Reference Velocity

```text
z = (latest_velocity - reference_mean_velocity) / reference_standard_deviation
```

Values:

```text
reference_mean_velocity = {assessment.reference_velocity_mean:.2f}
reference_standard_deviation = {assessment.reference_velocity_std:.2f}
z_score = {assessment.velocity_z_score:.2f}
```

### Age-Based Weight Deviation

```text
weight_deviation_percent = (actual_weight - expected_weight_at_age) / expected_weight_at_age * 100
```

Values:

```text
expected_weight_at_age = {assessment.expected_weight_at_age:.2f} kg
weight_deviation_percent = {assessment.weight_deviation_percent:.2f}%
```

### Normalized Similarity Distance

The latest record is also compared with reference growth records using a normalized Euclidean distance over selected engineered features:

```text
distance = sqrt(sum((x_latest_scaled - x_reference_scaled)^2))
```

Nearest profile distance:

```text
{assessment.nearest_profile_distance:.2f}
```

## Practical Educational Signal

```text
{assessment.practical_signal}
```

Interpretation points:

{interpretation}

## Output Figures

```text
reports/figures/practical_growth_assessment_weight_trend.png
reports/figures/practical_growth_assessment_velocity_signal.png
```

## Responsible Use Boundary

This workflow can help a learner or owner organize measurements and understand growth trends. It should be used only as a learning and monitoring aid. Any real health concern, unusual growth, pain, lameness, feeding problem, or development concern should be discussed with a qualified veterinarian.
"""
    output_path.write_text(report, encoding="utf-8")


def run_assessment(
    input_path: Path = INPUT_PATH,
    reference_path: Path = REFERENCE_PATH,
    output_features_path: Path = OUTPUT_FEATURES_PATH,
    report_path: Path = REPORT_PATH,
) -> Dict[str, Path | AssessmentResult]:
    measurements = load_measurements(input_path)
    reference = pd.read_csv(reference_path)
    features = engineer_time_series_features(measurements)
    assessment = assess_latest_record(features, reference)

    output_features_path.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(output_features_path, index=False)
    create_figures(features, assessment)
    write_report(assessment, features, input_path, report_path)

    return {
        "features_path": output_features_path,
        "report_path": report_path,
        "weight_figure_path": WEIGHT_FIGURE_PATH,
        "velocity_figure_path": VELOCITY_FIGURE_PATH,
        "assessment": assessment,
    }


def main() -> None:
    result = run_assessment()
    assessment = result["assessment"]
    print("Created practical growth assessment workflow outputs")
    print(f"Input:   {INPUT_PATH}")
    print(f"Features:{result['features_path']}")
    print(f"Report:  {result['report_path']}")
    print(f"Signal:  {assessment.practical_signal}")
    print(f"Latest velocity z-score: {assessment.velocity_z_score:.2f}")


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path

import pandas as pd


def find_project_root() -> Path:
    """Return the project root whether the script is run from root or src/notebooks."""
    current = Path.cwd()
    if (current / "data").exists():
        return current
    if (current.parent / "data").exists():
        return current.parent
    return Path(__file__).resolve().parents[1]


def add_growth_time_series_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create learning-oriented time-series features from ordered dog growth records.

    The prototype dataset contains repeated measurements for the same dog over age.
    The features here are deterministic mathematical transformations, not medical
    decisions and not veterinary diagnosis.
    """
    required = {"dog_id", "age_months", "weight_kg", "height_cm"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    features = df.copy()
    features = features.sort_values(["dog_id", "age_months"]).reset_index(drop=True)

    grouped = features.groupby("dog_id", sort=False)

    features["previous_age_months"] = grouped["age_months"].shift(1)
    features["previous_weight_kg"] = grouped["weight_kg"].shift(1)
    features["previous_height_cm"] = grouped["height_cm"].shift(1)

    features["delta_age_months"] = features["age_months"] - features["previous_age_months"]
    features["weight_gain_kg"] = features["weight_kg"] - features["previous_weight_kg"]
    features["height_gain_cm"] = features["height_cm"] - features["previous_height_cm"]

    features["growth_velocity_kg_per_month"] = (
        features["weight_gain_kg"] / features["delta_age_months"]
    )
    features["height_velocity_cm_per_month"] = (
        features["height_gain_cm"] / features["delta_age_months"]
    )

    features["weight_to_height_ratio"] = features["weight_kg"] / features["height_cm"]
    features["lag_weight_kg"] = features["previous_weight_kg"]
    features["lag_height_cm"] = features["previous_height_cm"]

    features["rolling_weight_mean_3"] = grouped["weight_kg"].transform(
        lambda values: values.rolling(window=3, min_periods=1).mean()
    )
    features["rolling_height_mean_3"] = grouped["height_cm"].transform(
        lambda values: values.rolling(window=3, min_periods=1).mean()
    )
    features["rolling_growth_velocity_3"] = features.groupby("dog_id", sort=False)[
        "growth_velocity_kg_per_month"
    ].transform(lambda values: values.rolling(window=3, min_periods=1).mean())

    features["weight_change_percent"] = (
        features["weight_gain_kg"] / features["previous_weight_kg"]
    ) * 100

    def growth_phase(age_months: float) -> str:
        if age_months <= 4:
            return "early_puppy"
        if age_months <= 8:
            return "juvenile"
        if age_months <= 12:
            return "adolescent"
        return "young_adult"

    features["growth_phase"] = features["age_months"].apply(growth_phase)

    mean_velocity = features["growth_velocity_kg_per_month"].mean(skipna=True)
    std_velocity = features["growth_velocity_kg_per_month"].std(skipna=True)
    if pd.notna(std_velocity) and std_velocity != 0:
        features["growth_velocity_z_score"] = (
            features["growth_velocity_kg_per_month"] - mean_velocity
        ) / std_velocity
    else:
        features["growth_velocity_z_score"] = 0.0

    def velocity_signal(z_score: float) -> str:
        if pd.isna(z_score):
            return "first_record_no_previous_measurement"
        if z_score >= 1.0:
            return "faster_than_average_gain"
        if z_score <= -1.0:
            return "slower_than_average_gain"
        return "within_average_gain_band"

    features["growth_velocity_signal"] = features["growth_velocity_z_score"].apply(velocity_signal)
    return features


def main() -> None:
    project_root = find_project_root()
    input_path = project_root / "data" / "prototype" / "cane_corso_growth_sample.csv"
    output_path = project_root / "data" / "processed" / "cane_corso_time_series_features.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    features = add_growth_time_series_features(df)
    features.to_csv(output_path, index=False)

    print("Created time-series feature dataset")
    print(f"Input:  {input_path}")
    print(f"Output: {output_path}")
    print(f"Rows:   {len(features)}")
    print(f"Columns: {len(features.columns)}")


if __name__ == "__main__":
    main()

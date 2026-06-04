"""Align the feature engineering and time-series exercise with the project dataset.

The script adapts the exercise workflow to the Cane Corso growth prototype data:
problem framing, time audit, lag and rolling features, chronological testing,
ablation, residual analysis, and a multi-horizon forecasting plan.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "prototype" / "cane_corso_growth_sample.csv"
REPORT_DIR = ROOT / "reports" / "course_exercises"
REQ_PATH = ROOT / "data" / "course_exercises" / "feature_engineering_time_series_exercise_requirements.csv"


def make_encoder() -> OneHotEncoder:
    """Create an OneHotEncoder compatible with multiple scikit-learn versions."""
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


@dataclass(frozen=True)
class SplitData:
    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame


def load_growth_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing input dataset: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    required = {"dog_id", "dog_name", "sex", "age_months", "weight_kg", "height_cm", "activity_level"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df = df.sort_values(["dog_id", "age_months"]).reset_index(drop=True)
    base_date = pd.Timestamp("2024-01-01")
    df["measurement_date"] = base_date + pd.to_timedelta((df["age_months"] * 30).astype(int), unit="D")
    return df


def build_time_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    grouped = out.groupby("dog_id", group_keys=False)
    out["weight_lag_1"] = grouped["weight_kg"].shift(1)
    out["weight_lag_2"] = grouped["weight_kg"].shift(2)
    out["height_lag_1"] = grouped["height_cm"].shift(1)
    out["age_lag_1"] = grouped["age_months"].shift(1)
    out["weight_change_kg"] = out["weight_kg"] - out["weight_lag_1"]
    out["height_change_cm"] = out["height_cm"] - out["height_lag_1"]
    age_delta = out["age_months"] - out["age_lag_1"]
    out["weight_velocity_kg_per_month"] = out["weight_change_kg"] / age_delta.replace(0, np.nan)
    out["height_velocity_cm_per_month"] = out["height_change_cm"] / age_delta.replace(0, np.nan)
    out["rolling_weight_mean_2"] = grouped["weight_kg"].transform(lambda s: s.shift(1).rolling(2, min_periods=1).mean())
    out["rolling_weight_mean_3"] = grouped["weight_kg"].transform(lambda s: s.shift(1).rolling(3, min_periods=1).mean())
    out["rolling_height_mean_2"] = grouped["height_cm"].transform(lambda s: s.shift(1).rolling(2, min_periods=1).mean())
    out["age_sin"] = np.sin(2 * np.pi * out["age_months"] / 12)
    out["age_cos"] = np.cos(2 * np.pi * out["age_months"] / 12)
    out["age_stage"] = pd.cut(
        out["age_months"],
        bins=[0, 4, 8, 13],
        labels=["early_growth", "middle_growth", "late_growth"],
        include_lowest=True,
    ).astype(str)
    return out


def time_audit(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for dog_id, part in df.groupby("dog_id"):
        ages = part["age_months"].tolist()
        gaps = np.diff(ages).tolist()
        rows.append(
            {
                "dog_id": dog_id,
                "dog_name": part["dog_name"].iloc[0],
                "rows": len(part),
                "min_age_months": min(ages),
                "max_age_months": max(ages),
                "age_gaps_months": ";".join(str(int(g)) for g in gaps),
                "has_duplicate_age": bool(part.duplicated(["dog_id", "age_months"]).any()),
                "time_order_is_monotonic": bool(part["age_months"].is_monotonic_increasing),
            }
        )
    return pd.DataFrame(rows)


def chronological_split(df: pd.DataFrame) -> SplitData:
    parts = []
    for _, part in df.groupby("dog_id"):
        part = part.sort_values("age_months").reset_index(drop=True)
        n = len(part)
        part["split"] = "train"
        if n >= 4:
            part.loc[n - 2, "split"] = "validation"
            part.loc[n - 1, "split"] = "test"
        elif n >= 2:
            part.loc[n - 1, "split"] = "test"
        parts.append(part)
    split_df = pd.concat(parts, ignore_index=True)
    return SplitData(
        train=split_df[split_df["split"] == "train"].copy(),
        validation=split_df[split_df["split"] == "validation"].copy(),
        test=split_df[split_df["split"] == "test"].copy(),
    )


def evaluate(y_true: Iterable[float], y_pred: Iterable[float]) -> dict[str, float]:
    y_true = np.asarray(list(y_true), dtype=float)
    y_pred = np.asarray(list(y_pred), dtype=float)
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = float(mean_absolute_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred)) if len(y_true) > 1 else float("nan")
    return {"mae": mae, "rmse": rmse, "r2": r2}


def build_model(numeric_features: list[str], categorical_features: list[str], estimator: str) -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric_features),
            ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", make_encoder())]), categorical_features),
        ],
        remainder="drop",
    )
    if estimator == "linear_regression":
        model = LinearRegression()
    elif estimator == "ridge":
        model = Ridge(alpha=1.0)
    elif estimator == "random_forest":
        model = RandomForestRegressor(n_estimators=120, random_state=42, min_samples_leaf=1)
    else:
        raise ValueError(f"Unknown estimator: {estimator}")
    return Pipeline([("preprocess", preprocessor), ("model", model)])


def run_experiments(feature_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    modelling = feature_df.dropna(subset=["weight_lag_1"]).copy()
    split = chronological_split(modelling)

    experiments = [
        {
            "experiment": "baseline_lag_age",
            "estimator": "linear_regression",
            "numeric": ["age_months", "weight_lag_1"],
            "categorical": [],
            "feature_group": "lag plus age",
        },
        {
            "experiment": "lag_height_rolling",
            "estimator": "ridge",
            "numeric": ["age_months", "weight_lag_1", "height_lag_1", "rolling_weight_mean_2", "rolling_weight_mean_3"],
            "categorical": [],
            "feature_group": "lag, height and rolling statistics",
        },
        {
            "experiment": "time_velocity_category",
            "estimator": "ridge",
            "numeric": [
                "age_months",
                "weight_lag_1",
                "height_lag_1",
                "rolling_weight_mean_2",
                "weight_velocity_kg_per_month",
                "age_sin",
                "age_cos",
            ],
            "categorical": ["sex", "activity_level", "age_stage"],
            "feature_group": "time, velocity and categorical descriptors",
        },
        {
            "experiment": "nonlinear_reference",
            "estimator": "random_forest",
            "numeric": [
                "age_months",
                "weight_lag_1",
                "weight_lag_2",
                "height_lag_1",
                "rolling_weight_mean_2",
                "rolling_weight_mean_3",
                "weight_velocity_kg_per_month",
                "age_sin",
                "age_cos",
            ],
            "categorical": ["sex", "activity_level", "age_stage"],
            "feature_group": "nonlinear baseline with engineered time features",
        },
    ]

    rows = []
    residual_rows = []
    best_model = None
    best_rmse = float("inf")
    best_config = None

    for config in experiments:
        features = config["numeric"] + config["categorical"]
        pipeline = build_model(config["numeric"], config["categorical"], config["estimator"])
        pipeline.fit(split.train[features], split.train["weight_kg"])
        for split_name, part in [("validation", split.validation), ("test", split.test)]:
            pred = pipeline.predict(part[features])
            metrics = evaluate(part["weight_kg"], pred)
            rows.append(
                {
                    "experiment": config["experiment"],
                    "split": split_name,
                    "estimator": config["estimator"],
                    "feature_group": config["feature_group"],
                    "n_features": len(features),
                    "n_rows": len(part),
                    **metrics,
                }
            )
            if split_name == "test":
                for (_, sample), p in zip(part.iterrows(), pred):
                    residual_rows.append(
                        {
                            "experiment": config["experiment"],
                            "dog_id": sample["dog_id"],
                            "dog_name": sample["dog_name"],
                            "age_months": sample["age_months"],
                            "actual_weight_kg": sample["weight_kg"],
                            "predicted_weight_kg": round(float(p), 3),
                            "residual_kg": round(float(sample["weight_kg"] - p), 3),
                        }
                    )
            if split_name == "validation" and metrics["rmse"] < best_rmse:
                best_rmse = metrics["rmse"]
                best_model = pipeline
                best_config = config

    if best_model is None or best_config is None:
        raise RuntimeError("No best model was selected.")

    feature_columns = best_config["numeric"] + best_config["categorical"]
    combined_train = pd.concat([split.train, split.validation], ignore_index=True)
    best_model.fit(combined_train[feature_columns], combined_train["weight_kg"])
    test_predictions = best_model.predict(split.test[feature_columns])
    final_metrics = evaluate(split.test["weight_kg"], test_predictions)
    final_row = {
        "experiment": "selected_final_model",
        "split": "test",
        "estimator": best_config["estimator"],
        "feature_group": best_config["feature_group"],
        "n_features": len(feature_columns),
        "n_rows": len(split.test),
        **final_metrics,
    }
    metrics_df = pd.DataFrame(rows + [final_row])

    residual_df = pd.DataFrame(residual_rows)
    ablation_df = metrics_df[metrics_df["split"] == "test"].copy()
    return metrics_df, residual_df, ablation_df


def build_multi_horizon_plan() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "approach": "direct one-step model",
                "project_use": "Predict the next recorded growth measurement from current and previous measurements.",
                "leakage_risk": "Low if future rows are never used for feature construction.",
                "current_status": "Implemented as the baseline comparable forecasting workflow.",
            },
            {
                "approach": "direct multi-horizon model",
                "project_use": "Train separate targets for later future ages when more longitudinal data exists.",
                "leakage_risk": "Medium; each horizon must be created after chronological splitting rules are defined.",
                "current_status": "Documented as a next experiment for a larger real dataset.",
            },
            {
                "approach": "recursive forecasting",
                "project_use": "Use predicted weight as an input for a later predicted point.",
                "leakage_risk": "Medium to high; prediction error can compound across horizons.",
                "current_status": "Documented as an educational comparison, not used for final claims.",
            },
        ]
    )


def write_summary(metrics: pd.DataFrame, time_audit_df: pd.DataFrame, ablation: pd.DataFrame) -> None:
    best = metrics[metrics["split"] == "validation"].sort_values("rmse").head(1)
    selected = metrics[metrics["experiment"] == "selected_final_model"].iloc[0]
    lines = [
        "# Feature Engineering and Time Series Exercise Alignment Summary",
        "",
        "The workflow adapts the course exercise to longitudinal Cane Corso growth data.",
        "The target is `weight_kg`, and the time axis is represented by age-based measurement order.",
        "",
        "## Time audit",
        f"Dogs inspected: {len(time_audit_df)}",
        f"Duplicate age measurements detected: {bool(time_audit_df['has_duplicate_age'].any())}",
        "",
        "## Best validation experiment",
    ]
    if not best.empty:
        row = best.iloc[0]
        lines.extend(
            [
                f"Experiment: `{row['experiment']}`",
                f"Estimator: `{row['estimator']}`",
                f"Feature group: {row['feature_group']}",
                f"Validation MAE: {row['mae']:.3f}",
                f"Validation RMSE: {row['rmse']:.3f}",
            ]
        )
    lines.extend(
        [
            "",
            "## Selected final test result",
            f"Estimator: `{selected['estimator']}`",
            f"Feature group: {selected['feature_group']}",
            f"Test MAE: {selected['mae']:.3f}",
            f"Test RMSE: {selected['rmse']:.3f}",
            f"Test R²: {selected['r2']:.3f}",
            "",
            "## Interpretation boundary",
            "The dataset is small and educational. The result demonstrates a leakage-aware feature-engineering and time-series modelling workflow, not a production biological growth forecast.",
        ]
    )
    (REPORT_DIR / "feature_engineering_time_series_exercise_alignment_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_growth_data()
    feature_df = build_time_features(df)
    audit_df = time_audit(df)
    metrics_df, residual_df, ablation_df = run_experiments(feature_df)
    horizon_df = build_multi_horizon_plan()

    audit_df.to_csv(REPORT_DIR / "feature_engineering_time_audit.csv", index=False)
    metrics_df.to_csv(REPORT_DIR / "feature_engineering_time_series_metrics.csv", index=False)
    residual_df.to_csv(REPORT_DIR / "feature_engineering_time_series_residuals.csv", index=False)
    ablation_df.to_csv(REPORT_DIR / "feature_engineering_time_series_ablation.csv", index=False)
    horizon_df.to_csv(REPORT_DIR / "feature_engineering_multi_horizon_plan.csv", index=False)
    write_summary(metrics_df, audit_df, ablation_df)

    print("Feature engineering and time-series exercise alignment completed")
    print(f"Input rows: {len(df)}")
    print(f"Generated feature columns: {len(build_time_features(df).columns)}")
    print(f"Metrics report: {REPORT_DIR / 'feature_engineering_time_series_metrics.csv'}")
    print(f"Summary: {REPORT_DIR / 'feature_engineering_time_series_exercise_alignment_summary.md'}")
    print("Boundary: educational time-series workflow only; no veterinary diagnosis or production forecast.")


if __name__ == "__main__":
    main()

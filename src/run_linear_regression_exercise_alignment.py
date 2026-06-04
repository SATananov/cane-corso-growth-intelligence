"""Run a compact linear-regression exercise alignment workflow.

The workflow adapts the course exercise process to the Cane Corso Growth
Intelligence project domain. It compares a simple baseline, an enriched
preprocessing setup, and a tuned Ridge model.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "prototype" / "cane_corso_growth_sample.csv"
REPORT_DIR = ROOT / "reports" / "course_exercises"
METRICS_PATH = REPORT_DIR / "linear_regression_exercise_alignment_metrics.csv"
SUMMARY_PATH = REPORT_DIR / "linear_regression_exercise_alignment_summary.md"
REQUIREMENTS_PATH = ROOT / "data" / "course_exercises" / "linear_regression_testing_exercise_requirements.csv"

RANDOM_STATE = 42


def rmse(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
    """Return root mean squared error without requiring sklearn version-specific flags."""
    return mean_squared_error(y_true, y_pred) ** 0.5


def evaluate_model(name: str, model, X_test, y_test) -> dict[str, float | str]:
    """Evaluate a fitted regression model with the common exercise metrics."""
    predictions = model.predict(X_test)
    return {
        "model": name,
        "mae": round(mean_absolute_error(y_test, predictions), 4),
        "rmse": round(rmse(y_test, predictions), 4),
        "r2": round(r2_score(y_test, predictions), 4),
    }


def load_exercise_requirements() -> list[dict[str, str]]:
    with REQUIREMENTS_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    required_columns = {"age_months", "weight_kg", "height_cm", "sex", "activity_level"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    # Baseline: use only age. This matches the simple regression idea from the exercise.
    X_age = df[["age_months"]]
    y = df["weight_kg"]
    X_age_train, X_age_test, y_train, y_test = train_test_split(
        X_age,
        y,
        test_size=0.25,
        random_state=RANDOM_STATE,
    )

    baseline = LinearRegression()
    baseline.fit(X_age_train, y_train)

    results: list[dict[str, float | str]] = [
        evaluate_model("age_only_linear_regression", baseline, X_age_test, y_test)
    ]

    # Changed preprocessing: use more features and encode categorical variables.
    feature_columns = ["age_months", "height_cm", "sex", "activity_level"]
    X_full = df[feature_columns]
    X_train, X_test, y_train_full, y_test_full = train_test_split(
        X_full,
        y,
        test_size=0.25,
        random_state=RANDOM_STATE,
    )

    numeric_features = ["age_months", "height_cm"]
    categorical_features = ["sex", "activity_level"]

    preprocessing = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), numeric_features),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

    enriched_linear = Pipeline(
        steps=[
            ("preprocessing", preprocessing),
            ("model", LinearRegression()),
        ]
    )
    enriched_linear.fit(X_train, y_train_full)
    results.append(evaluate_model("enriched_linear_regression", enriched_linear, X_test, y_test_full))

    # Hyperparameter tuning: a small Ridge alpha grid.
    ridge_pipeline = Pipeline(
        steps=[
            ("preprocessing", preprocessing),
            ("model", Ridge()),
        ]
    )
    search = GridSearchCV(
        ridge_pipeline,
        param_grid={"model__alpha": [0.01, 0.1, 1.0, 10.0]},
        scoring="neg_root_mean_squared_error",
        cv=3,
    )
    search.fit(X_train, y_train_full)
    tuned_ridge = search.best_estimator_
    ridge_result = evaluate_model("tuned_ridge_regression", tuned_ridge, X_test, y_test_full)
    ridge_result["best_alpha"] = search.best_params_["model__alpha"]
    ridge_result["cv_rmse"] = round(abs(search.best_score_), 4)
    results.append(ridge_result)

    metrics_df = pd.DataFrame(results)
    metrics_df.to_csv(METRICS_PATH, index=False)

    requirement_rows = load_exercise_requirements()
    status_counts = pd.Series([row["coverage_status"] for row in requirement_rows]).value_counts().to_dict()

    best_by_rmse = metrics_df.sort_values("rmse", ascending=True).iloc[0]

    summary = f"""# Linear Regression Testing Exercise Alignment Summary

This report validates that the project follows the main workflow from the course exercise on linear regression, regularization, and testing.

## Dataset

- Source file: `{DATA_PATH.relative_to(ROOT)}`
- Rows: {len(df)}
- Target: `weight_kg`
- Main project interpretation: educational growth-weight prediction, not veterinary advice.

## Exercise coverage

- Exercise requirements checked: {len(requirement_rows)}
- Coverage status counts: {status_counts}

## Model comparison

{metrics_df.to_markdown(index=False)}

## Best model by RMSE

- Model: `{best_by_rmse['model']}`
- MAE: {best_by_rmse['mae']}
- RMSE: {best_by_rmse['rmse']}
- R2: {best_by_rmse['r2']}

## Interpretation

The exercise process is represented in the project through a baseline model, changed preprocessing, model comparison, and a small hyperparameter search. The dataset is intentionally small, so the result is useful for learning and workflow demonstration, not for biological or veterinary conclusions.
"""
    SUMMARY_PATH.write_text(summary, encoding="utf-8")

    print("Linear regression exercise alignment completed")
    print(f"Rows: {len(df)}")
    print(f"Exercise requirements checked: {len(requirement_rows)}")
    print(f"Metrics: {METRICS_PATH}")
    print(f"Summary: {SUMMARY_PATH}")
    print("Boundary: educational regression workflow only; not veterinary advice.")


if __name__ == "__main__":
    main()

"""Classification exercise alignment for the Cane Corso Growth Intelligence project.

The script demonstrates a reproducible binary classification workflow using the
project's growth data. It is intentionally educational: the derived target is a
proxy label for a faster-growth interval, not a veterinary diagnosis.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    confusion_matrix,
)
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
    cross_val_score,
    learning_curve,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


RANDOM_STATE = 42


@dataclass
class Protocol:
    target_name: str = "fast_growth_interval"
    main_metric: str = "f1"
    secondary_metrics: tuple[str, ...] = ("accuracy", "precision", "recall")
    test_size: float = 0.25
    random_state: int = RANDOM_STATE


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def make_one_hot_encoder() -> OneHotEncoder:
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def load_growth_data(root: Path) -> pd.DataFrame:
    candidates = [
        root / "data" / "prototype" / "cane_corso_growth_sample.csv",
        root / "data" / "processed" / "cane_corso_time_series_features.csv",
    ]
    for path in candidates:
        if path.exists():
            return pd.read_csv(path)

    raise FileNotFoundError(
        "Could not find project growth data. Expected one of: "
        + ", ".join(str(path) for path in candidates)
    )


def build_interval_dataset(raw: pd.DataFrame) -> pd.DataFrame:
    required = {"dog_id", "dog_name", "sex", "age_months", "weight_kg", "height_cm"}
    missing = sorted(required - set(raw.columns))
    if missing:
        raise ValueError(f"Missing required growth columns: {missing}")

    df = raw.copy()
    if "activity_level" not in df.columns:
        df["activity_level"] = "unknown"

    df = df.sort_values(["dog_id", "age_months"]).reset_index(drop=True)
    grouped = df.groupby("dog_id", sort=False)

    df["previous_weight_kg"] = grouped["weight_kg"].shift(1)
    df["previous_height_cm"] = grouped["height_cm"].shift(1)
    df["previous_age_months"] = grouped["age_months"].shift(1)
    df["weight_gain_kg"] = df["weight_kg"] - df["previous_weight_kg"]
    df["height_gain_cm"] = df["height_cm"] - df["previous_height_cm"]
    df["age_gap_months"] = df["age_months"] - df["previous_age_months"]
    df["weight_gain_per_month"] = df["weight_gain_kg"] / df["age_gap_months"].replace(0, np.nan)
    df["previous_weight_height_ratio"] = df["previous_weight_kg"] / df["previous_height_cm"].replace(0, np.nan)
    df["age_squared"] = df["age_months"] ** 2

    interval = df.dropna(
        subset=[
            "previous_weight_kg",
            "previous_height_cm",
            "weight_gain_per_month",
            "previous_weight_height_ratio",
        ]
    ).copy()

    threshold = float(interval["weight_gain_per_month"].median())
    interval["fast_growth_interval"] = (
        interval["weight_gain_per_month"] >= threshold
    ).astype(int)

    # Do not use the current interval gain as an input feature because it defines
    # the proxy target. Inputs are based on previous measurements and metadata.
    interval["sex"] = interval["sex"].astype(str)
    interval["activity_level"] = interval["activity_level"].astype(str)

    return interval.reset_index(drop=True)


def make_preprocessor(numeric_features: list[str], categorical_features: list[str]) -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("one_hot", make_one_hot_encoder()),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_features),
            ("categorical", categorical_pipeline, categorical_features),
        ],
        remainder="drop",
    )


def make_pipeline(estimator, numeric_features: list[str], categorical_features: list[str]) -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocess", make_preprocessor(numeric_features, categorical_features)),
            ("model", estimator),
        ]
    )


def safe_cv(y: pd.Series) -> StratifiedKFold:
    min_class_count = int(y.value_counts().min())
    n_splits = max(2, min(5, min_class_count))
    return StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)


def metric_row(name: str, model, X_train, X_test, y_train, y_test, cv) -> dict[str, float | str]:
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="f1")
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)

    return {
        "model": name,
        "cv_f1_mean": round(float(np.mean(cv_scores)), 4),
        "cv_f1_std": round(float(np.std(cv_scores)), 4),
        "test_accuracy": round(float(accuracy_score(y_test, prediction)), 4),
        "test_f1": round(float(f1_score(y_test, prediction, zero_division=0)), 4),
        "test_precision": round(float(precision_score(y_test, prediction, zero_division=0)), 4),
        "test_recall": round(float(recall_score(y_test, prediction, zero_division=0)), 4),
    }


def write_csv(path: Path, rows: Iterable[dict]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    root = project_root()
    reports = root / "reports" / "course_exercises"
    reports.mkdir(parents=True, exist_ok=True)

    protocol = Protocol()
    raw = load_growth_data(root)
    data = build_interval_dataset(raw)

    numeric_features = [
        "age_months",
        "previous_weight_kg",
        "previous_height_cm",
        "previous_weight_height_ratio",
        "age_gap_months",
        "age_squared",
    ]
    categorical_features = ["sex", "activity_level"]
    feature_columns = numeric_features + categorical_features

    X = data[feature_columns]
    y = data[protocol.target_name]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=protocol.test_size,
        random_state=protocol.random_state,
        stratify=y,
    )
    cv = safe_cv(y_train)

    models = {
        "dummy_most_frequent": DummyClassifier(strategy="most_frequent"),
        "dummy_stratified": DummyClassifier(strategy="stratified", random_state=RANDOM_STATE),
        "logistic_regression": make_pipeline(
            LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
            numeric_features,
            categorical_features,
        ),
        "random_forest": make_pipeline(
            RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE, max_depth=3),
            numeric_features,
            categorical_features,
        ),
    }

    metric_rows = [
        metric_row(name, model, X_train, X_test, y_train, y_test, cv)
        for name, model in models.items()
    ]

    logistic_grid = GridSearchCV(
        make_pipeline(
            LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
            numeric_features,
            categorical_features,
        ),
        param_grid={"model__C": [0.1, 1.0, 10.0]},
        cv=cv,
        scoring=protocol.main_metric,
    )
    metric_rows.append(
        metric_row("logistic_regression_tuned", logistic_grid, X_train, X_test, y_train, y_test, cv)
    )

    forest_grid = GridSearchCV(
        make_pipeline(
            RandomForestClassifier(random_state=RANDOM_STATE),
            numeric_features,
            categorical_features,
        ),
        param_grid={"model__n_estimators": [50, 100], "model__max_depth": [2, 3, None]},
        cv=cv,
        scoring=protocol.main_metric,
    )
    metric_rows.append(
        metric_row("random_forest_tuned", forest_grid, X_train, X_test, y_train, y_test, cv)
    )

    metrics_path = reports / "classification_exercise_alignment_metrics.csv"
    write_csv(metrics_path, metric_rows)

    best_name = max(metric_rows, key=lambda row: float(row["test_f1"]))["model"]
    best_model = {
        "dummy_most_frequent": models["dummy_most_frequent"],
        "dummy_stratified": models["dummy_stratified"],
        "logistic_regression": models["logistic_regression"],
        "random_forest": models["random_forest"],
        "logistic_regression_tuned": logistic_grid,
        "random_forest_tuned": forest_grid,
    }[best_name]
    best_model.fit(X_train, y_train)
    test_prediction = best_model.predict(X_test)

    if hasattr(best_model, "predict_proba"):
        probability = best_model.predict_proba(X_test)[:, 1]
    else:
        probability = np.zeros(len(X_test))

    errors = X_test.copy()
    errors["actual"] = y_test.to_numpy()
    errors["predicted"] = test_prediction
    errors["probability_fast_growth"] = np.round(probability, 4)
    errors["error_type"] = np.where(
        (errors["actual"] == 0) & (errors["predicted"] == 1),
        "false_positive",
        np.where(
            (errors["actual"] == 1) & (errors["predicted"] == 0),
            "false_negative",
            "correct",
        ),
    )
    errors.to_csv(reports / "classification_exercise_error_analysis.csv", index=False)

    try:
        importance = permutation_importance(
            best_model,
            X_test,
            y_test,
            n_repeats=10,
            random_state=RANDOM_STATE,
            scoring=protocol.main_metric,
        )
        importance_rows = [
            {
                "feature": feature,
                "importance_mean": round(float(mean), 6),
                "importance_std": round(float(std), 6),
            }
            for feature, mean, std in zip(
                feature_columns,
                importance.importances_mean,
                importance.importances_std,
            )
        ]
    except Exception as exc:  # pragma: no cover - defensive report path
        importance_rows = [{"feature": "not_available", "importance_mean": 0.0, "importance_std": 0.0, "note": str(exc)}]
    write_csv(reports / "classification_exercise_feature_importance.csv", importance_rows)

    ablation_groups = {
        "previous_body_size_only": ["previous_weight_kg", "previous_height_cm"],
        "previous_body_size_plus_age": ["age_months", "age_squared", "previous_weight_kg", "previous_height_cm"],
        "full_feature_set": feature_columns,
    }
    ablation_rows = []
    for group_name, columns in ablation_groups.items():
        group_numeric = [column for column in columns if column in numeric_features]
        group_categorical = [column for column in columns if column in categorical_features]
        group_model = make_pipeline(
            LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
            group_numeric,
            group_categorical,
        )
        row = metric_row(
            group_name,
            group_model,
            X_train[columns],
            X_test[columns],
            y_train,
            y_test,
            cv,
        )
        ablation_rows.append(row)
    write_csv(reports / "classification_exercise_ablation_study.csv", ablation_rows)

    learning_rows = []
    try:
        lc_model = models["logistic_regression"]
        train_sizes, train_scores, validation_scores = learning_curve(
            lc_model,
            X_train,
            y_train,
            cv=cv,
            scoring=protocol.main_metric,
            train_sizes=np.linspace(0.4, 1.0, 4),
        )
        for size, train_score, validation_score in zip(train_sizes, train_scores, validation_scores):
            learning_rows.append(
                {
                    "train_size": int(size),
                    "train_f1_mean": round(float(np.mean(train_score)), 4),
                    "validation_f1_mean": round(float(np.mean(validation_score)), 4),
                }
            )
    except Exception as exc:
        learning_rows.append(
            {
                "train_size": 0,
                "train_f1_mean": 0.0,
                "validation_f1_mean": 0.0,
                "note": f"Learning curve skipped for small sample: {exc}",
            }
        )
    write_csv(reports / "classification_exercise_learning_curve.csv", learning_rows)

    cm = confusion_matrix(y_test, test_prediction, labels=[0, 1])
    cm_rows = [
        {"actual": "not_fast_growth", "predicted_not_fast_growth": int(cm[0, 0]), "predicted_fast_growth": int(cm[0, 1])},
        {"actual": "fast_growth", "predicted_not_fast_growth": int(cm[1, 0]), "predicted_fast_growth": int(cm[1, 1])},
    ]
    write_csv(reports / "classification_exercise_confusion_matrix.csv", cm_rows)

    summary = f"""# Classification Exercise Alignment Summary

## Classification question

The project uses a binary educational target: whether a growth interval belongs to a faster-growth period. The target is derived from interval-level weight gain per month and is used only to demonstrate a classification workflow.

## Experimental protocol

- Fixed random seed: `{RANDOM_STATE}`
- Main metric: `{protocol.main_metric}`
- Secondary metrics: `{", ".join(protocol.secondary_metrics)}`
- Holdout test size: `{protocol.test_size}`
- Cross-validation: stratified folds based on available class counts
- Baselines: most-frequent dummy classifier and stratified dummy classifier

## Dataset summary

- Source rows: `{len(raw)}`
- Interval rows used for classification: `{len(data)}`
- Training rows: `{len(X_train)}`
- Test rows: `{len(X_test)}`
- Positive class count: `{int(y.sum())}`
- Negative class count: `{int((1 - y).sum())}`

## Best model in this run

The best test F1 score in this run was produced by `{best_name}`.

The result is useful as a course-aligned classification demonstration. It should not be interpreted as a veterinary judgment or as proof that a dog is growing correctly.

## Output files

- `reports/course_exercises/classification_exercise_alignment_metrics.csv`
- `reports/course_exercises/classification_exercise_confusion_matrix.csv`
- `reports/course_exercises/classification_exercise_error_analysis.csv`
- `reports/course_exercises/classification_exercise_feature_importance.csv`
- `reports/course_exercises/classification_exercise_ablation_study.csv`
- `reports/course_exercises/classification_exercise_learning_curve.csv`
"""
    (reports / "classification_exercise_alignment_summary.md").write_text(summary, encoding="utf-8")

    print("Classification exercise alignment completed")
    print(f"Rows used: {len(data)}")
    print(f"Metrics: {metrics_path}")
    print(f"Summary: {reports / 'classification_exercise_alignment_summary.md'}")
    print("Boundary: educational proxy classification only; no veterinary claim.")


if __name__ == "__main__":
    main()

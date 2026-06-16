"""Step 21: Machine Learning Tools exercise alignment.

The exercise asks for a more production-like ML workflow: project structure,
configuration, reusable scripts, experiment tracking, model comparison, model
persistence, smoke tests and complete artifacts.

This module applies those ideas to the Cane Corso Growth Intelligence project.
It intentionally uses the committed public processed dog-growth sample rather
than any local-only image dataset, so it can run from a clean GitHub clone.
"""

from __future__ import annotations

import json
import logging
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RANDOM_STATE = 42
LOGGER = logging.getLogger("ccgi.machine_learning_tools")


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    config_path: Path
    report_dir: Path
    model_dir: Path
    best_model_path: Path
    model_metadata_path: Path


class GrowthRecordTextBuilder(BaseEstimator, TransformerMixin):
    """Convert structured growth rows into short text records.

    The original exercise is based on job-post text. This project is a dog-growth
    monitoring project, so the text representation is project-aligned: every row
    is converted into a short clinical-style phrase containing age, weight,
    body-condition source and visit context tokens. This lets us compare sparse
    TF-IDF text features against dense TruncatedSVD text features while still
    using the project's own data story.
    """

    def __init__(self, text_columns: Iterable[str] | None = None):
        self.text_columns = list(text_columns or [])

    def fit(self, X: pd.DataFrame, y: Any = None) -> "GrowthRecordTextBuilder":
        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        frame = ensure_frame(X)
        return frame.apply(self._row_to_text, axis=1).to_numpy(dtype=str)

    @staticmethod
    def _age_bucket(age_months: Any) -> str:
        try:
            age = float(age_months)
        except (TypeError, ValueError):
            return "age_unknown"
        if age < 6:
            return "age_early_puppy"
        if age < 12:
            return "age_juvenile"
        if age < 24:
            return "age_young_adult"
        return "age_adult"

    @staticmethod
    def _weight_ratio_bucket(weight: Any, adult_weight: Any) -> str:
        try:
            ratio = float(weight) / max(float(adult_weight), 1e-9)
        except (TypeError, ValueError):
            return "weight_ratio_unknown"
        if ratio < 0.45:
            return "weight_ratio_low"
        if ratio < 0.85:
            return "weight_ratio_developing"
        if ratio < 1.15:
            return "weight_ratio_expected"
        return "weight_ratio_high"

    def _row_to_text(self, row: pd.Series) -> str:
        tokens: list[str] = []
        for column in self.text_columns:
            if column not in row.index:
                continue
            value = row[column]
            if pd.isna(value):
                token = f"{column}_missing"
            else:
                token = f"{column}_{str(value).strip().lower().replace(' ', '_')}"
            tokens.append(token)

        tokens.append(self._age_bucket(row.get("visit_age_months")))
        tokens.append(self._weight_ratio_bucket(row.get("weight_kg"), row.get("average_adult_breed_weight_kg")))
        tokens.append("growth_monitoring_record")
        return " ".join(tokens)


def ensure_frame(X: Any) -> pd.DataFrame:
    if isinstance(X, pd.DataFrame):
        return X.copy()
    return pd.DataFrame(X)


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def configure_logging(report_dir: Path) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    log_path = report_dir / "machine_learning_tools_pipeline.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_path, encoding="utf-8")],
        force=True,
    )


def resolve_config_path(config_path: Path) -> Path:
    if config_path.is_absolute():
        return config_path
    candidate = project_root() / config_path
    if candidate.exists():
        return candidate
    return config_path.resolve()


def load_config(config_path: Path) -> dict[str, Any]:
    resolved = resolve_config_path(config_path)
    with resolved.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    return config


def build_paths(config_path: Path, config: dict[str, Any]) -> ProjectPaths:
    root = project_root()
    outputs = config["outputs"]
    report_dir = root / outputs["report_dir"]
    model_dir = root / outputs["model_dir"]
    return ProjectPaths(
        root=root,
        config_path=resolve_config_path(config_path),
        report_dir=report_dir,
        model_dir=model_dir,
        best_model_path=root / outputs["best_model_path"],
        model_metadata_path=root / outputs["model_metadata_path"],
    )


def make_one_hot_encoder() -> OneHotEncoder:
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def load_dataset(config: dict[str, Any], root: Path) -> pd.DataFrame:
    data_config = config["data"]
    path = root / data_config["input_path"]
    if not path.exists():
        raise FileNotFoundError(f"Input dataset not found: {path}")

    frame = pd.read_csv(path)
    max_rows = data_config.get("max_rows")
    if max_rows and len(frame) > int(max_rows):
        # Use a deterministic shuffle sample instead of head(). The committed
        # classification sample is ordered by class, so head() could accidentally
        # select only one target class and break stratified training.
        frame = frame.sample(n=int(max_rows), random_state=int(config.get("random_state", RANDOM_STATE))).reset_index(drop=True)

    target_column = data_config["target_column"]
    if target_column not in frame.columns:
        raise ValueError(f"Target column '{target_column}' is missing from {path}")

    return frame


def selected_columns(config: dict[str, Any]) -> list[str]:
    features = config["features"]
    columns = list(dict.fromkeys(features["numeric_columns"] + features["categorical_columns"] + features["text_columns"]))
    return columns


def split_data(config: dict[str, Any], frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    target_column = config["data"]["target_column"]
    columns = [column for column in selected_columns(config) if column in frame.columns]
    X = frame[columns].copy()
    y = frame[target_column].astype(int).copy()
    return train_test_split(
        X,
        y,
        test_size=float(config["data"].get("test_size", 0.25)),
        random_state=int(config.get("random_state", RANDOM_STATE)),
        stratify=y,
    )


def make_metadata_preprocessor(config: dict[str, Any]) -> ColumnTransformer:
    features = config["features"]
    numeric_columns = features["numeric_columns"]
    categorical_columns = features["categorical_columns"]

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
            ("numeric", numeric_pipeline, numeric_columns),
            ("categorical", categorical_pipeline, categorical_columns),
        ],
        remainder="drop",
    )


def build_experiments(config: dict[str, Any]) -> dict[str, Pipeline]:
    random_state = int(config.get("random_state", RANDOM_STATE))
    vectorizer_config = config["vectorizer"]
    ngram_range = tuple(vectorizer_config.get("ngram_range", [1, 2]))
    min_df = int(vectorizer_config.get("min_df", 2))
    max_features = int(vectorizer_config.get("max_features", 700))
    text_columns = config["features"]["text_columns"]
    svd_components = int(config["dimensionality_reduction"].get("n_components", 12))

    logistic_config = config["models"]["logistic_regression"]
    forest_config = config["models"]["random_forest"]

    text_builder = GrowthRecordTextBuilder(text_columns=text_columns)
    metadata_preprocessor = make_metadata_preprocessor(config)

    logistic = LogisticRegression(
        max_iter=int(logistic_config.get("max_iter", 1000)),
        C=float(logistic_config.get("C", 1.0)),
        class_weight="balanced",
        random_state=random_state,
    )

    return {
        "text_tfidf_sparse_logistic": Pipeline(
            steps=[
                ("record_text", text_builder),
                ("tfidf", TfidfVectorizer(ngram_range=ngram_range, min_df=min_df, max_features=max_features)),
                ("model", logistic),
            ]
        ),
        "text_tfidf_svd_dense_logistic": Pipeline(
            steps=[
                ("record_text", text_builder),
                ("tfidf", TfidfVectorizer(ngram_range=ngram_range, min_df=min_df, max_features=max_features)),
                ("svd", TruncatedSVD(n_components=svd_components, random_state=random_state)),
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=random_state)),
            ]
        ),
        "metadata_logistic_regression": Pipeline(
            steps=[
                ("preprocess", metadata_preprocessor),
                ("model", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=random_state)),
            ]
        ),
        "metadata_random_forest": Pipeline(
            steps=[
                ("preprocess", metadata_preprocessor),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=int(forest_config.get("n_estimators", 120)),
                        max_depth=forest_config.get("max_depth", 6),
                        class_weight="balanced",
                        random_state=random_state,
                    ),
                ),
            ]
        ),
    }


def probability_for_positive(model: Pipeline, X: pd.DataFrame) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X)
        if probabilities.shape[1] == 2:
            return probabilities[:, 1]
    if hasattr(model, "decision_function"):
        scores = model.decision_function(X)
        return 1 / (1 + np.exp(-scores))
    prediction = model.predict(X)
    return np.asarray(prediction, dtype=float)


def evaluate_model(name: str, model: Pipeline, X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series) -> tuple[dict[str, Any], Pipeline, pd.DataFrame]:
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    probability = probability_for_positive(model, X_test)
    metrics = {
        "experiment": name,
        "accuracy": round(float(accuracy_score(y_test, prediction)), 6),
        "precision": round(float(precision_score(y_test, prediction, zero_division=0)), 6),
        "recall": round(float(recall_score(y_test, prediction, zero_division=0)), 6),
        "f1": round(float(f1_score(y_test, prediction, zero_division=0)), 6),
        "roc_auc": round(float(roc_auc_score(y_test, probability)), 6),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
    }
    predictions = X_test.copy()
    predictions["actual"] = y_test.to_numpy()
    predictions["predicted"] = prediction
    predictions["probability_needs_attention"] = np.round(probability, 6)
    predictions["experiment"] = name
    return metrics, model, predictions


def log_with_mlflow_if_available(config: dict[str, Any], paths: ProjectPaths, metrics: dict[str, Any], model: Pipeline, artifact_paths: list[Path]) -> dict[str, Any]:
    tracking_config = config.get("tracking", {})
    if not tracking_config.get("use_mlflow_if_available", True):
        return {"enabled": False, "reason": "disabled_in_config"}

    try:
        import mlflow  # type: ignore
        import mlflow.sklearn  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on optional local installation
        return {"enabled": False, "reason": f"mlflow_not_available: {exc}"}

    tracking_uri = paths.root / tracking_config.get("mlflow_tracking_uri", "mlruns")
    mlflow.set_tracking_uri(tracking_uri.as_uri())
    mlflow.set_experiment(config.get("experiment_name", "step21_machine_learning_tools"))
    with mlflow.start_run(run_name=str(metrics["experiment"])):
        mlflow.log_params({
            "dataset": config["data"]["input_path"],
            "target": config["data"]["target_column"],
            "test_size": config["data"].get("test_size"),
            "max_rows": config["data"].get("max_rows"),
        })
        metric_payload = {
            key: value
            for key, value in metrics.items()
            if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))
        }
        mlflow.log_metrics(metric_payload)
        for artifact in artifact_paths:
            if artifact.exists():
                mlflow.log_artifact(str(artifact))
        mlflow.sklearn.log_model(model, artifact_path="model")
    return {"enabled": True, "tracking_uri": tracking_uri.as_posix()}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_model_comparison_plot(results: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ordered = results.sort_values("f1", ascending=True)
    ax.barh(ordered["experiment"], ordered["f1"])
    ax.set_xlabel("F1 score")
    ax.set_title("Step 21 model / representation comparison")
    ax.set_xlim(0, 1.0)
    for index, value in enumerate(ordered["f1"]):
        ax.text(float(value) + 0.01, index, f"{float(value):.3f}", va="center")
    fig.tight_layout()
    fig.savefig(path, format="svg")
    plt.close(fig)


def write_markdown_reports(config: dict[str, Any], paths: ProjectPaths, results: pd.DataFrame, best_row: pd.Series, tracking_status: dict[str, Any], inspected_examples: pd.DataFrame) -> None:
    report_dir = paths.report_dir
    best_experiment = str(best_row["experiment"])
    comparison_table = results.sort_values("f1", ascending=False).to_markdown(index=False)

    summary = f"""# Step 21 Machine Learning Tools Report

This report applies the **Machine Learning Tools** exercise ideas to the Cane Corso Growth Intelligence project.

## What this step covers

- reusable script entry point: `python app.py --config configs/machine_learning_tools_config.json`
- JSON configuration for data, feature columns, vectorizer settings, dimensionality reduction and models
- comparison of sparse TF-IDF text representation vs dense TF-IDF + TruncatedSVD representation
- comparison of fixed metadata pipelines with Logistic Regression and Random Forest classifiers
- MLflow-compatible experiment tracking, with automatic MLflow logging when `mlflow` is installed
- DVC stage definition in `dvc.yaml`
- saved best pipeline with `joblib`
- smoke test for saved-model loading and prediction
- model card and inspected examples

## Best experiment

```text
{best_experiment}
```

## Results

{comparison_table}

## MLflow tracking status

```json
{json.dumps(tracking_status, indent=2)}
```

## Responsible-use note

The target is an educational binary growth-monitoring signal from a processed public dog-growth sample. It is not a veterinary diagnosis. Outputs are intended for course learning, reproducibility, model comparison and responsible monitoring.
"""
    (report_dir / "step21_machine_learning_tools_report.md").write_text(summary, encoding="utf-8")

    model_card = f"""# Model Card — Cane Corso Growth Status Pipeline

## Model overview

This model is the best-performing pipeline selected during Step 21 Machine Learning Tools alignment.

```text
Best pipeline: {best_experiment}
Saved model: {paths.best_model_path.relative_to(paths.root).as_posix()}
```

## Intended use

The model is intended for educational growth-monitoring experiments. It predicts a binary proxy signal:

- `0` = normal growth pattern in the processed sample
- `1` = needs-attention growth signal in the processed sample

It can support learning, comparison of ML pipelines, reproducibility practice and responsible exploration of growth records.

## Not intended use

The model must not be used as veterinary diagnosis, medical advice, breed certification, pedigree proof, or a replacement for professional evaluation.

## Data

The pipeline uses the committed processed dataset:

```text
{config['data']['input_path']}
```

Real image datasets remain optional and local-only. This Step 21 pipeline does not require them.

## Approach

The Step 21 run compares:

- sparse TF-IDF text representation built from structured growth records;
- dense TF-IDF + TruncatedSVD representation;
- metadata Logistic Regression pipeline;
- metadata Random Forest pipeline.

The best model is selected by F1 score, with ROC-AUC kept as a secondary metric.

## Metrics

{comparison_table}

## Tradeoffs

Text-style representations are useful for demonstrating the exercise idea of comparing sparse and dense text pipelines. Metadata pipelines are usually more natural for this project because the core data is structured: age, weight, body-condition labels and visit context.

## Limitations

- The label is a course-aligned proxy signal, not a medical truth.
- The dataset is processed and limited to the available public sample.
- Performance may change when the data distribution changes.
- The model should be monitored and re-evaluated before any real-world use.

## Inspected examples

The file `reports/machine_learning_tools/inspected_examples.csv` contains correct, incorrect and uncertain examples, where available.

## Usability

Run the workflow with:

```bash
python app.py --config configs/machine_learning_tools_config.json
```

Run the smoke test with:

```bash
python tests/smoke_test_machine_learning_tools.py
```
"""
    (report_dir / "model_card_growth_status.md").write_text(model_card, encoding="utf-8")

    dvc_note = f"""# Step 21 Data Governance and DVC Note

The exercise asks to track data versions and pipelines with DVC. This project includes a lightweight `dvc.yaml` stage for the Machine Learning Tools workflow.

The stage is intentionally small and clean-clone friendly:

```bash
dvc repro machine_learning_tools
```

Expected command behind the stage:

```bash
python app.py --config configs/machine_learning_tools_config.json
```

The committed processed dataset is used as input. Large raw datasets and real image datasets remain excluded from GitHub and should be handled through local storage or a proper DVC remote in a real production workflow.

Current best pipeline: `{best_experiment}`
"""
    (report_dir / "dvc_data_governance_note.md").write_text(dvc_note, encoding="utf-8")

    inspected_note = inspected_examples.head(10).to_markdown(index=False)
    (report_dir / "inspected_examples_summary.md").write_text(
        "# Inspected prediction examples\n\n" + inspected_note + "\n",
        encoding="utf-8",
    )


def build_inspected_examples(predictions: pd.DataFrame) -> pd.DataFrame:
    pred = predictions.copy()
    pred["is_correct"] = pred["actual"] == pred["predicted"]
    pred["uncertainty"] = (pred["probability_needs_attention"] - 0.5).abs()

    correct = pred[pred["is_correct"]].head(5).assign(example_type="correct")
    incorrect = pred[~pred["is_correct"]].head(5).assign(example_type="incorrect")
    uncertain = pred.sort_values("uncertainty").head(5).assign(example_type="uncertain_or_suspicious")
    examples = pd.concat([correct, incorrect, uncertain], ignore_index=True)
    return examples


def run_machine_learning_tools_pipeline(config_path: Path | str = Path("configs/machine_learning_tools_config.json")) -> dict[str, Any]:
    config_path = Path(config_path)
    config = load_config(config_path)
    paths = build_paths(config_path, config)
    configure_logging(paths.report_dir)
    LOGGER.info("Starting Step 21 Machine Learning Tools pipeline")

    paths.report_dir.mkdir(parents=True, exist_ok=True)
    paths.model_dir.mkdir(parents=True, exist_ok=True)

    frame = load_dataset(config, paths.root)
    X_train, X_test, y_train, y_test = split_data(config, frame)
    experiments = build_experiments(config)

    metric_rows: list[dict[str, Any]] = []
    prediction_frames: list[pd.DataFrame] = []
    fitted_models: dict[str, Pipeline] = {}

    for name, model in experiments.items():
        LOGGER.info("Training experiment: %s", name)
        metrics, fitted_model, predictions = evaluate_model(name, model, X_train, X_test, y_train, y_test)
        metric_rows.append(metrics)
        prediction_frames.append(predictions)
        fitted_models[name] = fitted_model

    results = pd.DataFrame(metric_rows).sort_values(["f1", "roc_auc", "accuracy"], ascending=False)
    results_path = paths.report_dir / "experiment_results.csv"
    results.to_csv(results_path, index=False)
    write_json(paths.report_dir / "experiment_results.json", metric_rows)

    best_name = str(results.iloc[0]["experiment"])
    best_model = fitted_models[best_name]
    joblib.dump(best_model, paths.best_model_path)

    all_predictions = pd.concat(prediction_frames, ignore_index=True)
    all_predictions.to_csv(paths.report_dir / "sample_predictions.csv", index=False)
    best_predictions = all_predictions[all_predictions["experiment"] == best_name].copy()
    inspected_examples = build_inspected_examples(best_predictions)
    inspected_examples.to_csv(paths.report_dir / "inspected_examples.csv", index=False)

    plot_path = paths.report_dir / "model_comparison_f1.svg"
    write_model_comparison_plot(results, plot_path)

    metadata = {
        "project": config.get("project_name"),
        "step": "Step 21 - Machine Learning Tools",
        "best_experiment": best_name,
        "target_column": config["data"]["target_column"],
        "input_path": config["data"]["input_path"],
        "feature_columns": selected_columns(config),
        "positive_class_meaning": "needs_attention_growth_signal",
        "model_path": paths.best_model_path.relative_to(paths.root).as_posix(),
        "report_dir": paths.report_dir.relative_to(paths.root).as_posix(),
    }
    write_json(paths.model_metadata_path, metadata)

    tracking_artifacts = [results_path, plot_path, paths.report_dir / "inspected_examples.csv"]
    tracking_status = log_with_mlflow_if_available(
        config=config,
        paths=paths,
        metrics=results.iloc[0].to_dict(),
        model=best_model,
        artifact_paths=tracking_artifacts,
    )
    write_json(paths.report_dir / "mlflow_tracking_manifest.json", tracking_status)

    write_markdown_reports(
        config=config,
        paths=paths,
        results=results,
        best_row=results.iloc[0],
        tracking_status=tracking_status,
        inspected_examples=inspected_examples,
    )

    LOGGER.info("Step 21 pipeline finished. Best experiment: %s", best_name)
    return {
        "best_experiment": best_name,
        "results_path": results_path.as_posix(),
        "model_path": paths.best_model_path.as_posix(),
        "tracking_status": tracking_status,
    }


if __name__ == "__main__":
    run_machine_learning_tools_pipeline()

"""Validate Step 21 Machine Learning Tools outputs."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import joblib
import pandas as pd

REPORT_DIR = ROOT / "reports" / "machine_learning_tools"
MODEL_PATH = ROOT / "models" / "machine_learning_tools" / "best_growth_status_pipeline.joblib"
METADATA_PATH = ROOT / "models" / "machine_learning_tools" / "best_growth_status_pipeline_metadata.json"
CONFIG_PATH = ROOT / "configs" / "machine_learning_tools_config.json"
REQUIRED_REPORTS = [
    REPORT_DIR / "experiment_results.csv",
    REPORT_DIR / "experiment_results.json",
    REPORT_DIR / "step21_machine_learning_tools_report.md",
    REPORT_DIR / "model_card_growth_status.md",
    REPORT_DIR / "sample_predictions.csv",
    REPORT_DIR / "inspected_examples.csv",
    REPORT_DIR / "model_comparison_f1.svg",
    REPORT_DIR / "mlflow_tracking_manifest.json",
    REPORT_DIR / "dvc_data_governance_note.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"Machine Learning Tools validation FAIL: {message}")


def main() -> None:
    if not CONFIG_PATH.exists():
        fail(f"missing config: {CONFIG_PATH}")
    if not MODEL_PATH.exists():
        fail(f"missing saved model: {MODEL_PATH}")
    if not METADATA_PATH.exists():
        fail(f"missing model metadata: {METADATA_PATH}")
    for report in REQUIRED_REPORTS:
        if not report.exists():
            fail(f"missing report artifact: {report}")
        if report.stat().st_size == 0:
            fail(f"empty report artifact: {report}")

    results = pd.read_csv(REPORT_DIR / "experiment_results.csv")
    expected = {"experiment", "accuracy", "precision", "recall", "f1", "roc_auc"}
    missing = expected - set(results.columns)
    if missing:
        fail(f"experiment_results.csv missing columns: {sorted(missing)}")
    if len(results) < 2:
        fail("expected at least two experiments for comparison")

    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    best_experiment = metadata.get("best_experiment")
    if best_experiment not in set(results["experiment"]):
        fail("metadata best_experiment is not present in experiment results")

    sample_path = ROOT / "data" / "processed" / "dog_growth_classification_sample.csv"
    sample = pd.read_csv(sample_path).head(5)
    feature_columns = [column for column in metadata["feature_columns"] if column in sample.columns]
    model = joblib.load(MODEL_PATH)
    prediction = model.predict(sample[feature_columns])
    if len(prediction) != len(sample):
        fail("saved model prediction length mismatch")

    print("Machine Learning Tools validation PASS")
    print(f"Best experiment: {best_experiment}")
    print(f"Experiments compared: {len(results)}")


if __name__ == "__main__":
    main()

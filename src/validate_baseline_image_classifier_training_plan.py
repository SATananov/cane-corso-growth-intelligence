"""Validate Step 20 baseline image classifier training-plan artifacts.

This validation is intentionally lightweight. It checks documentation, CSV plans,
and interpretation boundaries. It does not download images, train a model, or
create model weights.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TRAINING_PLAN_DOC = ROOT / "docs" / "baseline_image_classifier_training_plan.md"
SAFETY_DOC = ROOT / "docs" / "visual_similarity_training_safety_boundaries.md"
TRAINING_PLAN_CSV = ROOT / "data" / "baseline_image_classifier_training_plan.csv"
METRICS_PLAN_CSV = ROOT / "data" / "baseline_image_classifier_metrics_plan.csv"
REPORT_PATH = ROOT / "reports" / "baseline_image_classifier_training_plan_validation.md"

REQUIRED_TRAINING_KEYS = {
    "model_goal",
    "recommended_input_size",
    "recommended_first_model",
    "artifact_policy",
    "interpretation_boundary",
}

REQUIRED_METRICS = {
    "accuracy",
    "macro_f1",
    "per_class_precision",
    "per_class_recall",
    "confusion_matrix",
    "example_predictions",
}

REQUIRED_BOUNDARY_PHRASES = [
    "visual similarity",
    "not breed proof",
    "No pedigree",
    "No images are downloaded",
]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required CSV: {path}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def require_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8")


def validate_training_plan_csv(rows: list[dict[str, str]]) -> None:
    found = {row.get("plan_item", "").strip() for row in rows}
    missing = REQUIRED_TRAINING_KEYS - found
    if missing:
        raise AssertionError(f"Training plan CSV is missing keys: {sorted(missing)}")

    boundary_rows = [
        row for row in rows
        if row.get("plan_item", "").strip() == "interpretation_boundary"
    ]
    if not boundary_rows:
        raise AssertionError("Missing interpretation_boundary row")
    boundary_value = boundary_rows[0].get("value", "").strip().lower()
    if "visual" not in boundary_value or "breed" not in boundary_value:
        raise AssertionError("interpretation_boundary must mention visual/breed boundary")


def validate_metrics_csv(rows: list[dict[str, str]]) -> None:
    found = {row.get("metric", "").strip() for row in rows}
    missing = REQUIRED_METRICS - found
    if missing:
        raise AssertionError(f"Metrics CSV is missing metrics: {sorted(missing)}")

    required_rows = [row for row in rows if row.get("required", "").strip().lower() == "yes"]
    if len(required_rows) < 5:
        raise AssertionError("At least five required metrics are expected for the baseline plan")


def validate_docs(training_text: str, safety_text: str, patch_text: str | None = None) -> None:
    combined = "\n".join(text for text in [training_text, safety_text, patch_text or ""] if text)
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase.lower() not in combined.lower():
            raise AssertionError(f"Missing required boundary phrase: {phrase}")

    if "pedigree" not in safety_text.lower() or "genetic" not in safety_text.lower():
        raise AssertionError("Safety document must include pedigree/genetic boundary")


def write_report(training_rows: list[dict[str, str]], metric_rows: list[dict[str, str]]) -> None:
    required_metrics = [row["metric"] for row in metric_rows if row.get("required", "").lower() == "yes"]
    report = f"""# Baseline Image Classifier Training Plan Validation

Status: PASS

## Checked artifacts

- `docs/baseline_image_classifier_training_plan.md`
- `docs/visual_similarity_training_safety_boundaries.md`
- `data/baseline_image_classifier_training_plan.csv`
- `data/baseline_image_classifier_metrics_plan.csv`

## Summary

Training-plan rows: {len(training_rows)}
Metric-plan rows: {len(metric_rows)}
Required metrics: {', '.join(required_metrics)}

## Boundary

Step 20 validates the future image-classifier training plan only. It does not download images, train a model, create model weights, or claim breed proof.
"""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")


def main() -> None:
    training_text = require_file(TRAINING_PLAN_DOC)
    safety_text = require_file(SAFETY_DOC)
    patch_path = ROOT / "PATCH_REPORT_STEP20_BASELINE_IMAGE_CLASSIFIER_TRAINING_PLAN.md"
    patch_text = patch_path.read_text(encoding="utf-8") if patch_path.exists() else ""

    training_rows = read_csv_rows(TRAINING_PLAN_CSV)
    metric_rows = read_csv_rows(METRICS_PLAN_CSV)

    validate_training_plan_csv(training_rows)
    validate_metrics_csv(metric_rows)
    validate_docs(training_text, safety_text, patch_text)
    write_report(training_rows, metric_rows)

    print("Step 20 baseline image classifier training-plan validation PASS")
    print(f"Training plan rows: {len(training_rows)}")
    print(f"Metrics plan rows:  {len(metric_rows)}")
    print(f"Report: {REPORT_PATH}")
    print("Boundary: no image download, no model training, no breed-proof claim.")


if __name__ == "__main__":
    main()

"""Validate lightweight image classifier report artifacts."""

from __future__ import annotations

import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "reports"

REQUIRED_FILES = [
    REPORTS_DIR / "lightweight_image_classifier_training_report.md",
    REPORTS_DIR / "lightweight_image_classifier_metrics.csv",
    REPORTS_DIR / "lightweight_image_classifier_confusion_matrix.csv",
    REPORTS_DIR / "lightweight_image_classifier_prediction_examples.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not path.exists()]
    if missing:
        raise SystemExit(
            "Missing lightweight image classifier report artifact(s):\n"
            + "\n".join(f"- {path}" for path in missing)
            + "\nRun: python src/train_lightweight_image_classifier.py"
        )

    metrics = read_csv(REPORTS_DIR / "lightweight_image_classifier_metrics.csv")
    if not metrics:
        raise SystemExit("Metrics CSV is empty")

    required_splits = {"train", "validation", "test"}
    seen_splits = {row.get("split", "") for row in metrics}
    missing_splits = required_splits - seen_splits
    if missing_splits:
        raise SystemExit(f"Metrics CSV missing split(s): {sorted(missing_splits)}")

    for row in metrics:
        split = row["split"]
        samples = int(row["samples"])
        accuracy = float(row["accuracy"])
        macro_f1 = float(row["macro_f1"])
        weighted_f1 = float(row["weighted_f1"])
        if samples < 0:
            raise SystemExit(f"Negative sample count in split {split}")
        for metric_name, metric_value in [
            ("accuracy", accuracy),
            ("macro_f1", macro_f1),
            ("weighted_f1", weighted_f1),
        ]:
            if not (0.0 <= metric_value <= 1.0):
                raise SystemExit(f"{metric_name} out of range for split {split}: {metric_value}")

    report_text = (REPORTS_DIR / "lightweight_image_classifier_training_report.md").read_text(encoding="utf-8")
    required_phrases = [
        "visual similarity",
        "not breed proof",
        "No image files",
        "no model weights",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase.lower() not in report_text.lower()]
    if missing_phrases:
        raise SystemExit(f"Training report missing boundary phrase(s): {missing_phrases}")

    examples = read_csv(REPORTS_DIR / "lightweight_image_classifier_prediction_examples.csv")

    print("Lightweight image classifier output validation PASS")
    print(f"Metrics rows: {len(metrics)}")
    print(f"Prediction example rows: {len(examples)}")
    print("Boundary: visual similarity only; no image files or model weights are required in the repository.")


if __name__ == "__main__":
    main()

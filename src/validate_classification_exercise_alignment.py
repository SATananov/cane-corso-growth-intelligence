"""Validate classification exercise alignment artifacts."""

from __future__ import annotations

import csv
from pathlib import Path


REQUIRED_FILES = [
    "docs/course_exercises/classification_pipeline_reproducibility_alignment.md",
    "data/course_exercises/classification_pipeline_reproducibility_requirements.csv",
    "reports/course_exercises/classification_exercise_alignment_metrics.csv",
    "reports/course_exercises/classification_exercise_alignment_summary.md",
    "reports/course_exercises/classification_exercise_confusion_matrix.csv",
    "reports/course_exercises/classification_exercise_error_analysis.csv",
    "reports/course_exercises/classification_exercise_feature_importance.csv",
    "reports/course_exercises/classification_exercise_ablation_study.csv",
    "reports/course_exercises/classification_exercise_learning_curve.csv",
]


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    root = project_root()
    missing = [path for path in REQUIRED_FILES if not (root / path).exists()]
    if missing:
        raise SystemExit("Missing required classification alignment files: " + ", ".join(missing))

    requirements = read_csv(root / "data/course_exercises/classification_pipeline_reproducibility_requirements.csv")
    metrics = read_csv(root / "reports/course_exercises/classification_exercise_alignment_metrics.csv")
    errors = read_csv(root / "reports/course_exercises/classification_exercise_error_analysis.csv")
    ablation = read_csv(root / "reports/course_exercises/classification_exercise_ablation_study.csv")

    required_requirement_ids = {
        "dummy_models",
        "pipeline",
        "logistic_regression",
        "learning_curve",
        "feature_engineering",
        "different_model",
        "feature_importance",
        "error_analysis",
        "ablation",
    }
    actual_ids = {row["requirement_id"] for row in requirements}
    missing_ids = sorted(required_requirement_ids - actual_ids)
    if missing_ids:
        raise SystemExit("Missing exercise requirement rows: " + ", ".join(missing_ids))

    model_names = {row["model"] for row in metrics}
    required_models = {"dummy_most_frequent", "dummy_stratified", "logistic_regression", "random_forest"}
    missing_models = sorted(required_models - model_names)
    if missing_models:
        raise SystemExit("Missing model metric rows: " + ", ".join(missing_models))

    if len(errors) == 0:
        raise SystemExit("Error analysis file is empty.")

    if len(ablation) < 3:
        raise SystemExit("Ablation study should contain at least three feature-group rows.")

    print("Classification exercise alignment validation PASS")
    print(f"Requirement rows: {len(requirements)}")
    print(f"Metric rows: {len(metrics)}")
    print(f"Error-analysis rows: {len(errors)}")
    print(f"Ablation rows: {len(ablation)}")
    print("Boundary: educational proxy classification only; no veterinary claim.")


if __name__ == "__main__":
    main()

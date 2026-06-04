"""Validate the linear-regression exercise alignment artifacts."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS_PATH = ROOT / "data" / "course_exercises" / "linear_regression_testing_exercise_requirements.csv"
METRICS_PATH = ROOT / "reports" / "course_exercises" / "linear_regression_exercise_alignment_metrics.csv"
SUMMARY_PATH = ROOT / "reports" / "course_exercises" / "linear_regression_exercise_alignment_summary.md"
DOC_PATH = ROOT / "docs" / "course_exercises" / "linear_regression_testing_exercise_alignment.md"
NOTEBOOK_PATH = ROOT / "notebooks" / "16_linear_regression_testing_exercise_project_alignment.ipynb"

REQUIRED_PROBLEMS = set(range(1, 11))
REQUIRED_MODELS = {
    "age_only_linear_regression",
    "enriched_linear_regression",
    "tuned_ridge_regression",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def main() -> None:
    missing_files = [
        str(path.relative_to(ROOT))
        for path in [REQUIREMENTS_PATH, METRICS_PATH, SUMMARY_PATH, DOC_PATH, NOTEBOOK_PATH]
        if not path.exists()
    ]
    if missing_files:
        raise FileNotFoundError(f"Missing alignment artifacts: {missing_files}")

    requirements = read_csv(REQUIREMENTS_PATH)
    problems = {int(row["problem_number"]) for row in requirements}
    if problems != REQUIRED_PROBLEMS:
        raise ValueError(f"Expected problems 1-10, got {sorted(problems)}")

    uncovered = [row for row in requirements if row["coverage_status"] not in {"covered", "partially_covered"}]
    if uncovered:
        raise ValueError(f"Unexpected uncovered requirements: {uncovered}")

    metrics = read_csv(METRICS_PATH)
    models = {row["model"] for row in metrics}
    missing_models = REQUIRED_MODELS - models
    if missing_models:
        raise ValueError(f"Missing required model comparisons: {sorted(missing_models)}")

    metric_columns = {"mae", "rmse", "r2"}
    for row in metrics:
        for column in metric_columns:
            try:
                float(row[column])
            except Exception as exc:  # noqa: BLE001 - validation should explain the problematic value.
                raise ValueError(f"Invalid metric value in {row['model']} column {column}: {row[column]}") from exc

    summary_text = SUMMARY_PATH.read_text(encoding="utf-8")
    required_phrases = [
        "educational growth-weight prediction",
        "not veterinary advice",
        "hyperparameter search",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in summary_text]
    if missing_phrases:
        raise ValueError(f"Missing required summary phrases: {missing_phrases}")

    print("Linear regression exercise alignment validation PASS")
    print(f"Exercise requirements: {len(requirements)}")
    print(f"Model comparisons: {len(metrics)}")
    print("Boundary: project-specific adaptation of the course exercise; not veterinary advice.")


if __name__ == "__main__":
    main()

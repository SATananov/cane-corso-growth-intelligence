"""Validate the project alignment for the feature engineering and time-series exercise."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "course_exercises"
REQUIRED_FILES = [
    ROOT / "data" / "course_exercises" / "feature_engineering_time_series_exercise_requirements.csv",
    ROOT / "docs" / "course_exercises" / "feature_engineering_time_series_exercise_alignment.md",
    REPORT_DIR / "feature_engineering_time_audit.csv",
    REPORT_DIR / "feature_engineering_time_series_metrics.csv",
    REPORT_DIR / "feature_engineering_time_series_residuals.csv",
    REPORT_DIR / "feature_engineering_time_series_ablation.csv",
    REPORT_DIR / "feature_engineering_multi_horizon_plan.csv",
    REPORT_DIR / "feature_engineering_time_series_exercise_alignment_summary.md",
]


def main() -> None:
    missing = [str(path) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing expected alignment artifacts:\n" + "\n".join(missing))

    requirements = pd.read_csv(REQUIRED_FILES[0])
    metrics = pd.read_csv(REPORT_DIR / "feature_engineering_time_series_metrics.csv")
    residuals = pd.read_csv(REPORT_DIR / "feature_engineering_time_series_residuals.csv")
    ablation = pd.read_csv(REPORT_DIR / "feature_engineering_time_series_ablation.csv")
    time_audit = pd.read_csv(REPORT_DIR / "feature_engineering_time_audit.csv")
    horizon_plan = pd.read_csv(REPORT_DIR / "feature_engineering_multi_horizon_plan.csv")

    required_areas = {
        "Problem formulation",
        "Time column audit",
        "Baseline forecasting",
        "Iterative improvement",
        "Categories and text features",
        "Pipeline",
        "Model testing",
        "Feature ablation",
        "Multi-horizon forecasting",
    }
    found_areas = set(requirements["exercise_area"])
    missing_areas = required_areas.difference(found_areas)
    if missing_areas:
        raise AssertionError(f"Missing exercise requirement areas: {sorted(missing_areas)}")

    if metrics.empty or not {"experiment", "split", "mae", "rmse", "r2"}.issubset(metrics.columns):
        raise AssertionError("Metrics report is empty or missing required metric columns.")
    if "selected_final_model" not in set(metrics["experiment"]):
        raise AssertionError("Metrics report must include the selected final model.")
    if residuals.empty or "residual_kg" not in residuals.columns:
        raise AssertionError("Residual analysis report is missing residual_kg values.")
    if ablation["experiment"].nunique() < 3:
        raise AssertionError("Ablation report should compare at least three experiments.")
    if time_audit.empty or not bool(time_audit["time_order_is_monotonic"].all()):
        raise AssertionError("Time audit must confirm monotonic age order per dog.")
    if horizon_plan["approach"].nunique() < 3:
        raise AssertionError("Multi-horizon plan must describe direct and recursive ideas.")

    print("Feature engineering and time-series exercise alignment validation PASS")
    print(f"Requirement rows: {len(requirements)}")
    print(f"Experiment rows: {len(metrics)}")
    print(f"Residual rows: {len(residuals)}")
    print("Boundary: validates exercise alignment and reports only; no production forecast claim.")


if __name__ == "__main__":
    main()

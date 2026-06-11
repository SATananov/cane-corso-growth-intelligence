"""Validate Step 20 dimensionality reduction reports and notebooks."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

REPORT_DIR = Path("reports/course_exercises")

EXPECTED_REPORTS = [
    REPORT_DIR / "dimensionality_reduction_feature_audit.csv",
    REPORT_DIR / "dimensionality_reduction_filter_report.csv",
    REPORT_DIR / "dimensionality_reduction_random_forest_importance.csv",
    REPORT_DIR / "dimensionality_reduction_pca_explained_variance.csv",
    REPORT_DIR / "dimensionality_reduction_pca_components.csv",
    REPORT_DIR / "dimensionality_reduction_embedding_preview.csv",
    REPORT_DIR / "dimensionality_reduction_representation_metrics.csv",
    REPORT_DIR / "dimensionality_reduction_kernel_pca_metrics.csv",
    REPORT_DIR / "dimensionality_reduction_text_svd_components.csv",
    REPORT_DIR / "dimensionality_reduction_text_representation_metrics.csv",
    REPORT_DIR / "dimensionality_reduction_tsne_visualization_plan.csv",
    REPORT_DIR / "dimensionality_reduction_exercise_alignment_summary.md",

    REPORT_DIR / "dimensionality_reduction_problem5_component_terms.csv",
    REPORT_DIR / "dimensionality_reduction_problem5_component_examples.csv",
    REPORT_DIR / "dimensionality_reduction_problem5_visualization_coordinates.csv",
    REPORT_DIR / "dimensionality_reduction_problem5_visualization_interpretation.md",
]

EXPECTED_NOTEBOOKS = [
    Path("notebooks/06_dimensionality_reduction_future_course_topic.ipynb"),
    Path("notebooks/06_1_dimensionality_reduction_exercise_project_alignment.ipynb"),
]

EXPECTED_REPRESENTATIONS = {
    "raw_scaled_features",
    "pca_2_components",
    "LinDA_2_components_supervised",
    "isomap_2_components_visualization",
    "tSNE_2_components_visualization_only",
}


def assert_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing expected file: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"Expected file is empty: {path}")


def validate_notebooks() -> None:
    for notebook in EXPECTED_NOTEBOOKS:
        assert_file(notebook)
        with notebook.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("nbformat") != 4:
            raise ValueError(f"Notebook is not nbformat 4: {notebook}")
        if not data.get("cells"):
            raise ValueError(f"Notebook has no cells: {notebook}")
        if any(cell.get("outputs") for cell in data.get("cells", []) if cell.get("cell_type") == "code"):
            raise ValueError(f"Notebook should be saved without outputs: {notebook}")


def validate_reports() -> None:
    for path in EXPECTED_REPORTS:
        assert_file(path)

    metrics = pd.read_csv(REPORT_DIR / "dimensionality_reduction_representation_metrics.csv")
    found = set(metrics["representation"].astype(str))
    missing = EXPECTED_REPRESENTATIONS - found
    if missing:
        raise ValueError(f"Missing representation metrics: {sorted(missing)}")

    pca = pd.read_csv(REPORT_DIR / "dimensionality_reduction_pca_explained_variance.csv")
    if pca["cumulative_explained_variance"].max() < 0.99:
        raise ValueError("PCA cumulative explained variance should reach almost all variance across all components.")

    svd = pd.read_csv(REPORT_DIR / "dimensionality_reduction_text_svd_components.csv")
    if len(svd) < 2:
        raise ValueError("Expected at least two SVD components for text representation.")


    problem5_terms = pd.read_csv(REPORT_DIR / "dimensionality_reduction_problem5_component_terms.csv")
    required_term_columns = {
        "component",
        "top_positive_terms",
        "top_negative_terms_or_low_loading_terms",
        "interpreted_semantic_axis",
    }
    if not required_term_columns.issubset(problem5_terms.columns):
        raise ValueError("Problem 5 component term report is missing required interpretation columns.")
    if len(problem5_terms) < 2:
        raise ValueError("Problem 5 should inspect at least two SVD components.")

    problem5_examples = pd.read_csv(REPORT_DIR / "dimensionality_reduction_problem5_component_examples.csv")
    if problem5_examples["component"].nunique() < 2:
        raise ValueError("Problem 5 examples should cover at least two components.")
    if {"high_positive_value", "low_or_opposite_value"} - set(problem5_examples["side"].astype(str)):
        raise ValueError("Problem 5 examples must include both high-positive and contrasting records.")

    viz = pd.read_csv(REPORT_DIR / "dimensionality_reduction_problem5_visualization_coordinates.csv")
    if viz["visualization"].nunique() < 2:
        raise ValueError("Problem 5 must provide at least two visualization coordinate sets.")


def main() -> None:
    validate_notebooks()
    validate_reports()
    print("Step 20 validation passed: dimensionality reduction reports, Problem 5 analysis, and notebooks are valid.")


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    ROOT / "data" / "course_exercises" / "clustering_segmentation_exercise_requirements.csv",
    ROOT / "docs" / "course_exercises" / "clustering_segmentation_exercise_alignment.md",
    ROOT / "reports" / "course_exercises" / "clustering_exercise_alignment_metrics.csv",
    ROOT / "reports" / "course_exercises" / "clustering_exercise_segment_profiles.csv",
    ROOT / "reports" / "course_exercises" / "clustering_exercise_stability.csv",
    ROOT / "reports" / "course_exercises" / "clustering_exercise_cluster_feature_comparison.csv",
    ROOT / "reports" / "course_exercises" / "clustering_exercise_visualization_plan.csv",
    ROOT / "reports" / "course_exercises" / "clustering_exercise_alignment_summary.md",
]


def main() -> None:
    missing = [str(path) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing clustering exercise alignment outputs:\n" + "\n".join(missing))

    requirements = pd.read_csv(ROOT / "data" / "course_exercises" / "clustering_segmentation_exercise_requirements.csv")
    metrics = pd.read_csv(ROOT / "reports" / "course_exercises" / "clustering_exercise_alignment_metrics.csv")
    profiles = pd.read_csv(ROOT / "reports" / "course_exercises" / "clustering_exercise_segment_profiles.csv")
    stability = pd.read_csv(ROOT / "reports" / "course_exercises" / "clustering_exercise_stability.csv")
    comparison = pd.read_csv(ROOT / "reports" / "course_exercises" / "clustering_exercise_cluster_feature_comparison.csv")
    visualizations = pd.read_csv(ROOT / "reports" / "course_exercises" / "clustering_exercise_visualization_plan.csv")

    if len(requirements) < 10:
        raise ValueError("The exercise requirement mapping is too small.")
    if "silhouette" not in metrics.columns or metrics["silhouette"].isna().all():
        raise ValueError("Clustering metrics must include silhouette values.")
    if profiles["growth_segment"].nunique() < 2:
        raise ValueError("At least two growth segments are expected.")
    if len(stability) < 3:
        raise ValueError("Stability report must include several random seeds.")
    if comparison["feature_set"].nunique() < 3:
        raise ValueError("The cluster-feature comparison must include original, cluster-only and combined features.")
    if len(visualizations) < 4:
        raise ValueError("The visualization plan must contain at least four meaningful plots.")

    summary = (ROOT / "reports" / "course_exercises" / "clustering_exercise_alignment_summary.md").read_text(encoding="utf-8")
    required_phrases = [
        "educational modelling unit",
        "Recommended segmentation",
        "Cluster features in supervised prediction",
        "not as a medical diagnosis",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in summary]
    if missing_phrases:
        raise ValueError("Summary is missing required interpretation phrases: " + ", ".join(missing_phrases))

    print("Clustering exercise alignment validation PASS")
    print(f"Requirement rows: {len(requirements)}")
    print(f"Metric rows: {len(metrics)}")
    print(f"Segment profiles: {len(profiles)}")
    print(f"Feature-set comparisons: {len(comparison)}")
    print("Boundary: clustering is used for educational growth-state segmentation only.")


if __name__ == "__main__":
    main()

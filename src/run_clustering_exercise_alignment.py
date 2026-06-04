from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

from collections import Counter
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import adjusted_rand_score, accuracy_score, f1_score, silhouette_score
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "prototype" / "cane_corso_growth_sample.csv"
REPORT_DIR = ROOT / "reports" / "course_exercises"

METRICS_PATH = REPORT_DIR / "clustering_exercise_alignment_metrics.csv"
PROFILE_PATH = REPORT_DIR / "clustering_exercise_segment_profiles.csv"
STABILITY_PATH = REPORT_DIR / "clustering_exercise_stability.csv"
FEATURE_COMPARISON_PATH = REPORT_DIR / "clustering_exercise_cluster_feature_comparison.csv"
VISUALIZATION_PLAN_PATH = REPORT_DIR / "clustering_exercise_visualization_plan.csv"
SUMMARY_PATH = REPORT_DIR / "clustering_exercise_alignment_summary.md"


def make_encoder() -> OneHotEncoder:
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def to_dense(matrix):
    return matrix.toarray() if hasattr(matrix, "toarray") else np.asarray(matrix)


def mode_or_unknown(values: Iterable[object]) -> str:
    cleaned = [str(v) for v in values if pd.notna(v)]
    return Counter(cleaned).most_common(1)[0][0] if cleaned else "unknown"


def load_growth_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing expected dataset: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    required = {"dog_id", "dog_name", "sex", "age_months", "weight_kg", "height_cm", "activity_level"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["dog_id"] = df["dog_id"].astype(str)
    df["age_months"] = pd.to_numeric(df["age_months"], errors="coerce")
    df["weight_kg"] = pd.to_numeric(df["weight_kg"], errors="coerce")
    df["height_cm"] = pd.to_numeric(df["height_cm"], errors="coerce")

    df = df.dropna(subset=["dog_id", "age_months", "weight_kg", "height_cm"])
    df = df[(df["age_months"] > 0) & (df["weight_kg"] > 0) & (df["height_cm"] > 0)]
    df = df.drop_duplicates(subset=["dog_id", "age_months"], keep="first")
    df = df.sort_values(["dog_id", "age_months"]).reset_index(drop=True)

    df["previous_age_months"] = df.groupby("dog_id")["age_months"].shift(1)
    df["previous_weight_kg"] = df.groupby("dog_id")["weight_kg"].shift(1)
    df["previous_height_cm"] = df.groupby("dog_id")["height_cm"].shift(1)

    month_delta = (df["age_months"] - df["previous_age_months"]).replace(0, np.nan)
    df["weight_velocity_kg_per_month"] = (df["weight_kg"] - df["previous_weight_kg"]) / month_delta
    df["height_velocity_cm_per_month"] = (df["height_cm"] - df["previous_height_cm"]) / month_delta

    df["weight_velocity_kg_per_month"] = df["weight_velocity_kg_per_month"].fillna(
        df["weight_velocity_kg_per_month"].median()
    )
    df["height_velocity_cm_per_month"] = df["height_velocity_cm_per_month"].fillna(
        df["height_velocity_cm_per_month"].median()
    )

    first_age = df.groupby("dog_id")["age_months"].transform("min")
    final_weight = df.groupby("dog_id")["weight_kg"].transform("last")
    df["months_since_first"] = df["age_months"] - first_age
    df["final_observed_weight_kg"] = final_weight
    df["weight_gap_to_final_kg"] = df["final_observed_weight_kg"] - df["weight_kg"]
    df["weight_to_height_ratio"] = df["weight_kg"] / df["height_cm"]

    velocity_cutoff = df["weight_velocity_kg_per_month"].quantile(0.75)
    df["rapid_growth_indicator"] = (df["weight_velocity_kg_per_month"] >= velocity_cutoff).astype(int)

    return df


def build_preprocessor(numeric_features: list[str], categorical_features: list[str]) -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", RobustScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", make_encoder()),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_features),
            ("categorical", categorical_pipeline, categorical_features),
        ]
    )


def evaluate_kmeans(X: np.ndarray) -> tuple[pd.DataFrame, int, KMeans]:
    rows = []
    max_k = min(5, len(X) - 1)
    best_k = 2
    best_score = -1.0
    best_model = None

    for k in range(2, max_k + 1):
        model = KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = model.fit_predict(X)
        score = silhouette_score(X, labels)
        rows.append(
            {
                "algorithm": "kmeans",
                "cluster_count": k,
                "inertia": round(float(model.inertia_), 6),
                "silhouette": round(float(score), 6),
                "selected_for_project": False,
            }
        )
        if score > best_score:
            best_score = score
            best_k = k
            best_model = model

    for row in rows:
        if row["cluster_count"] == best_k:
            row["selected_for_project"] = True

    if best_model is None:
        raise RuntimeError("Could not fit KMeans.")

    return pd.DataFrame(rows), best_k, best_model


def evaluate_agglomerative(X: np.ndarray, k: int) -> pd.DataFrame:
    model = AgglomerativeClustering(n_clusters=k)
    labels = model.fit_predict(X)
    return pd.DataFrame(
        [
            {
                "algorithm": "agglomerative",
                "cluster_count": k,
                "inertia": np.nan,
                "silhouette": round(float(silhouette_score(X, labels)), 6),
                "selected_for_project": False,
            }
        ]
    )


def build_segment_profiles(df: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
    prof = df.copy()
    prof["growth_segment"] = labels

    grouped = prof.groupby("growth_segment")
    rows = []
    median_weights = grouped["weight_kg"].median().sort_values()
    ordered_segments = list(median_weights.index)
    name_map = {}
    if len(ordered_segments) >= 1:
        name_map[ordered_segments[0]] = "lighter_early_growth_profile"
    if len(ordered_segments) >= 2:
        name_map[ordered_segments[-1]] = "heavier_later_growth_profile"
    for segment in ordered_segments[1:-1]:
        name_map[segment] = "middle_growth_profile"

    for segment, data in grouped:
        segment_name = name_map.get(segment, "growth_profile")
        rows.append(
            {
                "growth_segment": int(segment),
                "segment_name": segment_name,
                "row_count": int(len(data)),
                "dog_count": int(data["dog_id"].nunique()),
                "median_age_months": round(float(data["age_months"].median()), 3),
                "median_weight_kg": round(float(data["weight_kg"].median()), 3),
                "median_height_cm": round(float(data["height_cm"].median()), 3),
                "median_weight_velocity_kg_per_month": round(float(data["weight_velocity_kg_per_month"].median()), 3),
                "most_common_sex": mode_or_unknown(data["sex"]),
                "most_common_activity": mode_or_unknown(data["activity_level"]),
                "suggested_action": "inspect trend consistency and compare with age-aware growth context",
                "risk_note": "small educational dataset; segment should not be interpreted as medical diagnosis",
            }
        )
    return pd.DataFrame(rows).sort_values("growth_segment")


def stability_report(X: np.ndarray, k: int) -> pd.DataFrame:
    seeds = [1, 7, 21, 42, 99]
    reference = KMeans(n_clusters=k, random_state=42, n_init=20).fit_predict(X)
    rows = []
    for seed in seeds:
        labels = KMeans(n_clusters=k, random_state=seed, n_init=20).fit_predict(X)
        rows.append(
            {
                "random_seed": seed,
                "adjusted_rand_index_vs_seed_42": round(float(adjusted_rand_score(reference, labels)), 6),
                "cluster_count": k,
            }
        )
    return pd.DataFrame(rows)


def supervised_cluster_feature_comparison(df: pd.DataFrame, X: np.ndarray, model: KMeans) -> pd.DataFrame:
    final_weight_by_dog = df.groupby("dog_id")["weight_kg"].transform("last")
    target = (final_weight_by_dog >= final_weight_by_dog.median()).astype(int).to_numpy()

    original = X
    distances = model.transform(X)
    combined = np.hstack([original, distances])

    feature_sets = {
        "original_growth_features": original,
        "cluster_distance_features": distances,
        "original_plus_cluster_distances": combined,
    }

    rows = []
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
    for name, features in feature_sets.items():
        clf = LogisticRegression(max_iter=1000)
        result = cross_validate(
            clf,
            features,
            target,
            cv=cv,
            scoring=["accuracy", "f1_macro"],
            error_score="raise",
        )
        rows.append(
            {
                "feature_set": name,
                "mean_accuracy": round(float(np.mean(result["test_accuracy"])), 6),
                "mean_f1_macro": round(float(np.mean(result["test_f1_macro"])), 6),
                "interpretation_limit": "educational comparison on a small prototype dataset",
            }
        )
    return pd.DataFrame(rows)


def write_visualization_plan() -> pd.DataFrame:
    rows = [
        {
            "visualization": "age_vs_weight_by_segment",
            "purpose": "show whether clusters separate early, middle, and later growth states",
        },
        {
            "visualization": "height_vs_weight_by_segment",
            "purpose": "inspect body-size profile differences between clusters",
        },
        {
            "visualization": "cluster_size_bar_chart",
            "purpose": "detect tiny or dominant clusters that may be preprocessing artifacts",
        },
        {
            "visualization": "pca_2d_cluster_projection",
            "purpose": "project the prepared feature space to two dimensions for debugging and communication",
        },
        {
            "visualization": "cluster_distance_feature_importance",
            "purpose": "explain whether cluster-derived features add predictive information",
        },
    ]
    return pd.DataFrame(rows)


def write_summary(df: pd.DataFrame, metrics: pd.DataFrame, profiles: pd.DataFrame, stability: pd.DataFrame, comparison: pd.DataFrame) -> None:
    chosen = metrics[metrics["selected_for_project"] == True].iloc[0]
    best_feature_set = comparison.sort_values(["mean_f1_macro", "mean_accuracy"], ascending=False).iloc[0]

    content = f"""# Clustering Exercise Alignment Summary

## Dataset and sample choice

The project uses Cane Corso prototype growth measurements. A single row is a dog-age growth-state observation. This is an educational modelling unit, not a final production-level independent sample. A larger version should use many dog-level longitudinal profiles.

Rows used: {len(df)}
Dogs represented: {df["dog_id"].nunique()}

## Recommended segmentation

The selected KMeans configuration uses **{int(chosen["cluster_count"])} clusters**.

Selected silhouette score: {chosen["silhouette"]}

## Segment profile table

The segment profile table is saved at:

`reports/course_exercises/clustering_exercise_segment_profiles.csv`

The profiles describe growth-state groups by age, weight, height, velocity, sex, and activity level.

## Contesting algorithm

Agglomerative clustering is included as a second clustering approach. It is reported beside KMeans to show whether the segment structure is stable across algorithms.

## Stability check

Average adjusted Rand index against the seed-42 reference:

{round(float(stability["adjusted_rand_index_vs_seed_42"].mean()), 6)}

## Cluster features in supervised prediction

The best educational feature set in the small comparison is:

`{best_feature_set["feature_set"]}`

Mean macro F1: {best_feature_set["mean_f1_macro"]}

This comparison is not a production estimate. It only shows how cluster-derived features can be tested as additional model inputs.

## Final recommendation

Use clustering as an interpretability layer for growth-state monitoring, not as a medical diagnosis and not as proof of breed identity. The current segmentation is useful for explaining growth patterns, generating hypotheses, and preparing stronger future experiments with larger data.
"""
    SUMMARY_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_growth_data()

    numeric_features = [
        "age_months",
        "weight_kg",
        "height_cm",
        "weight_velocity_kg_per_month",
        "height_velocity_cm_per_month",
        "weight_to_height_ratio",
        "weight_gap_to_final_kg",
        "months_since_first",
        "rapid_growth_indicator",
    ]
    categorical_features = ["sex", "activity_level"]

    preprocessor = build_preprocessor(numeric_features, categorical_features)
    X = to_dense(preprocessor.fit_transform(df[numeric_features + categorical_features]))

    kmeans_metrics, selected_k, kmeans_model = evaluate_kmeans(X)
    agglomerative_metrics = evaluate_agglomerative(X, selected_k)
    metrics = pd.concat([kmeans_metrics, agglomerative_metrics], ignore_index=True)

    labels = kmeans_model.predict(X)
    profiles = build_segment_profiles(df, labels)
    stability = stability_report(X, selected_k)
    comparison = supervised_cluster_feature_comparison(df, X, kmeans_model)
    visualization_plan = write_visualization_plan()

    metrics.to_csv(METRICS_PATH, index=False)
    profiles.to_csv(PROFILE_PATH, index=False)
    stability.to_csv(STABILITY_PATH, index=False)
    comparison.to_csv(FEATURE_COMPARISON_PATH, index=False)
    visualization_plan.to_csv(VISUALIZATION_PLAN_PATH, index=False)
    write_summary(df, metrics, profiles, stability, comparison)

    print("Clustering exercise project alignment completed")
    print(f"Rows used: {len(df)}")
    print(f"Dogs represented: {df['dog_id'].nunique()}")
    print(f"Selected KMeans clusters: {selected_k}")
    print(f"Metrics: {METRICS_PATH}")
    print(f"Segment profiles: {PROFILE_PATH}")
    print(f"Summary: {SUMMARY_PATH}")
    print("Boundary: educational segmentation only; no veterinary diagnosis or breed-proof claim.")


if __name__ == "__main__":
    main()

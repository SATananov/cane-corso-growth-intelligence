"""
Step 20: Dimensionality Reduction and Manifold Learning

Lightweight course-aligned module. No external downloads, no large datasets.
"""

from __future__ import annotations

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris, make_moons
from sklearn.decomposition import PCA, KernelPCA, TruncatedSVD
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.manifold import Isomap
from sklearn.metrics import balanced_accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42
REPORT_DIR = Path("reports/course_exercises")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def report_path(name: str) -> Path:
    return REPORT_DIR / f"dimensionality_reduction_{name}"


def load_iris_frame() -> tuple[pd.DataFrame, pd.Series]:
    iris = load_iris(as_frame=True)
    X = iris.data.rename(
        columns={
            "sepal length (cm)": "sepal_length_cm",
            "sepal width (cm)": "sepal_width_cm",
            "petal length (cm)": "petal_length_cm",
            "petal width (cm)": "petal_width_cm",
        }
    )
    y = pd.Series(iris.target, name="species").map(dict(enumerate(iris.target_names)))
    return X, y


def write_feature_reports(X: pd.DataFrame, y: pd.Series) -> None:
    audit = X.describe().T.reset_index().rename(columns={"index": "feature"})
    audit["variance"] = X.var().values
    audit["target_classes"] = y.nunique()
    audit.to_csv(report_path("feature_audit.csv"), index=False)

    rows = []
    for feature in X.columns:
        variance = float(X[feature].var())
        if variance < 0.05:
            rows.append({"filter": "low_variance", "feature_a": feature, "feature_b": "", "value": round(variance, 6), "action": "review"})

    corr = X.corr().abs()
    for i, a in enumerate(corr.columns):
        for b in corr.columns[i + 1:]:
            value = float(corr.loc[a, b])
            if value >= 0.85:
                rows.append({"filter": "high_correlation", "feature_a": a, "feature_b": b, "value": round(value, 6), "action": "review_one_of_the_pair"})

    if not rows:
        rows = [{"filter": "status", "feature_a": "all_features", "feature_b": "", "value": 0.0, "action": "no_removal_required_for_demo_thresholds"}]
    pd.DataFrame(rows).to_csv(report_path("filter_report.csv"), index=False)

    rf = RandomForestClassifier(n_estimators=80, random_state=RANDOM_STATE, class_weight="balanced")
    rf.fit(X, y)
    pd.DataFrame({"feature": X.columns, "importance": rf.feature_importances_}).sort_values(
        "importance", ascending=False
    ).to_csv(report_path("random_forest_importance.csv"), index=False)


def write_pca_and_embeddings(X: pd.DataFrame, y: pd.Series) -> None:
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(random_state=RANDOM_STATE)
    X_pca = pca.fit_transform(X_scaled)
    pd.DataFrame({
        "component": [f"PC{i + 1}" for i in range(len(pca.explained_variance_ratio_))],
        "explained_variance_ratio": pca.explained_variance_ratio_,
        "cumulative_explained_variance": np.cumsum(pca.explained_variance_ratio_),
    }).to_csv(report_path("pca_explained_variance.csv"), index=False)

    pd.DataFrame(
        pca.components_,
        columns=X.columns,
        index=[f"PC{i + 1}" for i in range(len(pca.components_))],
    ).reset_index(names="component").to_csv(report_path("pca_components.csv"), index=False)

    embedding = pd.DataFrame({"species": y.values, "PCA_1": X_pca[:, 0], "PCA_2": X_pca[:, 1]})

    try:
        linda = LinearDiscriminantAnalysis(n_components=2).fit_transform(X_scaled, y)
        embedding["LinDA_1"] = linda[:, 0]
        embedding["LinDA_2"] = linda[:, 1]
    except Exception as exc:
        warnings.warn(f"LinDA skipped: {exc}")

    try:
        iso = Isomap(n_neighbors=5, n_components=2).fit_transform(X_scaled)
        embedding["Isomap_1"] = iso[:, 0]
        embedding["Isomap_2"] = iso[:, 1]
    except Exception as exc:
        warnings.warn(f"Isomap skipped: {exc}")

    # t-SNE is documented as visualization-only in this project.
    # To keep the course patch fast and reproducible on all machines,
    # the script does not run a potentially slow t-SNE optimization by default.
    pd.DataFrame([
        {
            "method": "t-SNE",
            "recommended_use": "2D/3D visualization of local clusters",
            "production_note": "not_scored_as_a_stable_transform_for_new_incoming_data",
            "course_link": "covered_in_dimensionality_reduction_lecture_and_notes",
        }
    ]).to_csv(report_path("tsne_visualization_plan.csv"), index=False)

    embedding.head(30).to_csv(report_path("embedding_preview.csv"), index=False)


def score_train_test(name: str, pipeline: Pipeline, X: pd.DataFrame, y: pd.Series) -> dict[str, object]:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, stratify=y, random_state=RANDOM_STATE)
    pipeline.fit(X_train, y_train)
    pred = pipeline.predict(X_test)
    return {
        "representation": name,
        "balanced_accuracy": round(float(balanced_accuracy_score(y_test, pred)), 6),
        "macro_f1": round(float(f1_score(y_test, pred, average="macro")), 6),
        "notes": "train_test_logistic_regression_lightweight_demo",
    }


def write_representation_metrics(X: pd.DataFrame, y: pd.Series) -> None:
    rows = []
    configs = [
        ("raw_scaled_features", Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE))])),
        ("pca_2_components", Pipeline([("scale", StandardScaler()), ("pca", PCA(n_components=2, random_state=RANDOM_STATE)), ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE))])),
        ("LinDA_2_components_supervised", Pipeline([("scale", StandardScaler()), ("linda", LinearDiscriminantAnalysis(n_components=2)), ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE))])),
    ]
    for name, pipe in configs:
        try:
            rows.append(score_train_test(name, pipe, X, y))
        except Exception as exc:
            rows.append({"representation": name, "balanced_accuracy": np.nan, "macro_f1": np.nan, "notes": f"skipped: {exc}"})

    rows.append({"representation": "isomap_2_components_visualization", "balanced_accuracy": np.nan, "macro_f1": np.nan, "notes": "generated_for_embedding_preview_not_scored_as_production_pipeline"})
    rows.append({"representation": "tSNE_2_components_visualization_only", "balanced_accuracy": np.nan, "macro_f1": np.nan, "notes": "visualization_only_no_stable_transform_for_new_data"})
    pd.DataFrame(rows).to_csv(report_path("representation_metrics.csv"), index=False)


def write_kernel_pca_metrics() -> None:
    X, y = make_moons(n_samples=160, noise=0.08, random_state=RANDOM_STATE)
    X = pd.DataFrame(X, columns=["x1", "x2"])
    y = pd.Series(y, name="class")
    configs = [
        ("linear_pca_on_moons", Pipeline([("scale", StandardScaler()), ("pca", PCA(n_components=2, random_state=RANDOM_STATE)), ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE))])),
        ("rbf_kernel_pca_on_moons", Pipeline([("scale", StandardScaler()), ("kpca", KernelPCA(n_components=2, kernel="rbf", gamma=5, random_state=RANDOM_STATE)), ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE))])),
    ]
    rows = []
    for name, pipe in configs:
        rows.append(score_train_test(name, pipe, X, y))
    pd.DataFrame(rows).to_csv(report_path("kernel_pca_metrics.csv"), index=False)


def text_note_sample() -> pd.DataFrame:
    rows = [
        ("healthy", "steady monthly weight gain strong appetite normal activity balanced growth"),
        ("healthy", "height and weight progress consistent with age no warning signs"),
        ("healthy", "good muscle tone stable chest development regular feeding routine"),
        ("healthy", "growth curve remains within expected range energetic and active"),
        ("monitor", "weight increased faster than height review diet and activity"),
        ("monitor", "temporary slowdown in growth check feeding schedule next month"),
        ("monitor", "chest measurement changed quickly compare with previous records"),
        ("monitor", "mild asymmetry in growth notes requires follow up observation"),
        ("risk", "rapid weight gain with low activity possible overweight risk"),
        ("risk", "growth stagnation and reduced appetite veterinary consultation recommended"),
        ("risk", "large deviation from expected curve repeated warning measurements"),
        ("risk", "low weight progression and fatigue signal potential health concern"),
    ]
    return pd.DataFrame(rows, columns=["status", "note"])


def write_text_reports() -> None:
    data = text_note_sample()
    X_train, X_test, y_train, y_test = train_test_split(
        data["note"], data["status"], test_size=0.34, random_state=RANDOM_STATE, stratify=data["status"]
    )
    configs = [
        ("tfidf_sparse_text", Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)), ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE))])),
        ("tfidf_truncated_svd_latent_text", Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)), ("svd", TruncatedSVD(n_components=4, random_state=RANDOM_STATE)), ("scale", StandardScaler()), ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE))])),
    ]
    rows = []
    for name, pipe in configs:
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        rows.append({
            "representation": name,
            "balanced_accuracy": round(float(balanced_accuracy_score(y_test, pred)), 6),
            "macro_f1": round(float(f1_score(y_test, pred, average="macro")), 6),
            "notes": "tiny_project_style_text_sample_for_exercise_alignment",
        })
    pd.DataFrame(rows).to_csv(report_path("text_representation_metrics.csv"), index=False)

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    X_text = vectorizer.fit_transform(data["note"])
    svd = TruncatedSVD(n_components=4, random_state=RANDOM_STATE)
    svd.fit(X_text)
    terms = np.array(vectorizer.get_feature_names_out())
    component_rows = []
    for idx, comp in enumerate(svd.components_):
        positive_idx = np.argsort(comp)[-6:][::-1]
        negative_idx = np.argsort(comp)[:6]
        component_rows.append({
            "component": f"SVD{idx + 1}",
            "top_positive_terms": ", ".join(terms[positive_idx]),
            "top_negative_terms": ", ".join(terms[negative_idx]),
            "explained_variance_ratio": svd.explained_variance_ratio_[idx],
            "cumulative_explained_variance": np.cumsum(svd.explained_variance_ratio_)[idx],
        })
    pd.DataFrame(component_rows).to_csv(report_path("text_svd_components.csv"), index=False)


def write_summary() -> None:
    summary = """# Dimensionality Reduction Exercise Alignment Summary

Generated by `src/run_dimensionality_reduction_and_manifold_learning.py`.

## Lecture topics covered

- PCA with scaling and explained variance
- Kernel PCA for non-linear data
- LinDA / Linear Discriminant Analysis as supervised dimensionality reduction
- Isomap / isometric mapping for manifold visualization
- t-SNE as visualization-only embedding
- Feature selection through low variance, high correlation, and Random Forest importance
- Text latent representation through TF-IDF + TruncatedSVD

## Project decision

The original exercise uses an external Kaggle dataset. This project keeps the repository lightweight and reproducible by using built-in and synthetic data while preserving the required methodology: compare representations, evaluate beyond accuracy, and interpret reduced components.

## Generated report family

All generated files use the prefix `reports/course_exercises/dimensionality_reduction_`.
"""
    report_path("exercise_alignment_summary.md").write_text(summary, encoding="utf-8")


def main() -> None:
    X, y = load_iris_frame()
    write_feature_reports(X, y)
    write_pca_and_embeddings(X, y)
    write_representation_metrics(X, y)
    write_kernel_pca_metrics()
    write_text_reports()
    write_summary()
    print(f"Dimensionality reduction reports generated in {REPORT_DIR.as_posix()}")


if __name__ == "__main__":
    main()

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


def interpret_svd_axis(component_name: str) -> str:
    """Small, human-readable interpretation for the synthetic growth-note sample.

    The sign of SVD components can flip between implementations, so these labels are
    used as cautious interpretations rather than hard scientific conclusions.
    """
    mapping = {
        "SVD1": "general growth-note intensity: repeated growth, weight, activity and measurement vocabulary",
        "SVD2": "healthy expected development versus risk or monitoring language",
        "SVD3": "measurement-change and follow-up language versus stable routine language",
        "SVD4": "health-concern signals such as appetite, fatigue or deviation versus normal development notes",
    }
    return mapping.get(component_name, "latent semantic direction requiring manual inspection")


def write_problem5_component_analysis() -> None:
    """Generate the explicit Problem 5 component-analysis evidence.

    The original exercise asks for component inspection, example postings with high
    component values, at least two visualizations, and a written interpretation of
    whether visible patterns are meaningful or potentially misleading.  This project
    uses lightweight Cane Corso growth notes instead of the external fake-job dataset,
    but keeps the same methodology.
    """
    data = text_note_sample().reset_index(names="record_id")

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    X_text = vectorizer.fit_transform(data["note"])
    svd = TruncatedSVD(n_components=4, random_state=RANDOM_STATE)
    X_svd = svd.fit_transform(X_text)
    terms = np.array(vectorizer.get_feature_names_out())

    component_rows = []
    example_rows = []
    for idx, comp in enumerate(svd.components_):
        component = f"SVD{idx + 1}"
        positive_idx = np.argsort(comp)[-8:][::-1]
        negative_idx = np.argsort(comp)[:8]
        scores = X_svd[:, idx]

        component_rows.append(
            {
                "component": component,
                "top_positive_terms": ", ".join(terms[positive_idx]),
                "top_negative_terms_or_low_loading_terms": ", ".join(terms[negative_idx]),
                "explained_variance_ratio": round(float(svd.explained_variance_ratio_[idx]), 6),
                "cumulative_explained_variance": round(float(np.cumsum(svd.explained_variance_ratio_)[idx]), 6),
                "interpreted_semantic_axis": interpret_svd_axis(component),
                "interpretation_caution": "SVD component signs can flip; interpret term groups and high-scoring records together.",
            }
        )

        high_positive = np.argsort(scores)[-3:][::-1]
        high_negative = np.argsort(scores)[:3]
        for rank, row_idx in enumerate(high_positive, start=1):
            example_rows.append(
                {
                    "component": component,
                    "side": "high_positive_value",
                    "rank": rank,
                    "record_id": int(data.loc[row_idx, "record_id"]),
                    "status": data.loc[row_idx, "status"],
                    "component_value": round(float(scores[row_idx]), 6),
                    "note": data.loc[row_idx, "note"],
                    "why_it_matters": "Example growth note with strong loading on this latent component.",
                }
            )
        for rank, row_idx in enumerate(high_negative, start=1):
            example_rows.append(
                {
                    "component": component,
                    "side": "low_or_opposite_value",
                    "rank": rank,
                    "record_id": int(data.loc[row_idx, "record_id"]),
                    "status": data.loc[row_idx, "status"],
                    "component_value": round(float(scores[row_idx]), 6),
                    "note": data.loc[row_idx, "note"],
                    "why_it_matters": "Contrasting example used to understand whether the component has a meaningful axis.",
                }
            )

    pd.DataFrame(component_rows).to_csv(report_path("problem5_component_terms.csv"), index=False)
    pd.DataFrame(example_rows).to_csv(report_path("problem5_component_examples.csv"), index=False)

    # Coordinates for at least two notebook visualizations without storing images.
    coords = pd.DataFrame(
        {
            "visualization": "SVD_2D_text_notes",
            "record_id": data["record_id"],
            "label": data["status"],
            "x": X_svd[:, 0],
            "y": X_svd[:, 1],
            "source_text": data["note"],
            "interpretation_use": "Inspect whether healthy, monitor and risk notes separate in latent semantic space.",
        }
    )

    X_num, y_num = load_iris_frame()
    X_scaled = StandardScaler().fit_transform(X_num)
    pca_coords = PCA(n_components=2, random_state=RANDOM_STATE).fit_transform(X_scaled)
    pca_view = pd.DataFrame(
        {
            "visualization": "PCA_2D_numeric_reference",
            "record_id": np.arange(len(y_num)),
            "label": y_num.values,
            "x": pca_coords[:, 0],
            "y": pca_coords[:, 1],
            "source_text": "built-in numeric reference dataset used for projection methodology",
            "interpretation_use": "Reference visualization for how PCA separates numeric classes after scaling.",
        }
    )

    try:
        iso_coords = Isomap(n_neighbors=5, n_components=2).fit_transform(X_scaled)
        iso_view = pd.DataFrame(
            {
                "visualization": "Isomap_2D_numeric_reference",
                "record_id": np.arange(len(y_num)),
                "label": y_num.values,
                "x": iso_coords[:, 0],
                "y": iso_coords[:, 1],
                "source_text": "built-in numeric reference dataset used for manifold methodology",
                "interpretation_use": "Reference visualization for local neighborhood geometry; useful but not production preprocessing.",
            }
        )
        coords = pd.concat([coords, pca_view, iso_view], ignore_index=True)
    except Exception as exc:
        warnings.warn(f"Problem 5 Isomap coordinates skipped: {exc}")
        coords = pd.concat([coords, pca_view], ignore_index=True)

    coords.to_csv(report_path("problem5_visualization_coordinates.csv"), index=False)

    interpretation = """# Problem 5 — Component Analysis and Visualization Interpretation

This report directly addresses the most important part of the dimensionality-reduction exercise: inspect components, inspect examples with high component values, create visualizations, and explain what the visual geometry does and does not mean.

## Dataset adaptation

The original exercise uses fake-job postings. This project uses a small built-in set of Cane Corso growth-monitoring notes so the repository stays lightweight and reproducible. The methodology is the same:

- convert text to TF-IDF features;
- reduce sparse text features with TruncatedSVD;
- inspect top positive and low/opposite-loading terms;
- inspect example records with high component values;
- create 2D visualization coordinates;
- interpret whether visible grouping is meaningful or potentially misleading.

## Visualizations generated

The script generates coordinates for at least two visualizations:

1. `SVD_2D_text_notes` — first two SVD components from TF-IDF growth notes.
2. `PCA_2D_numeric_reference` — first two PCA components on a scaled built-in numeric reference dataset.
3. `Isomap_2D_numeric_reference` — manifold-learning reference coordinates when available.

The notebook contains plotting cells for these views. The project does not commit PNG images, keeping the repository clean while preserving reproducible visualization code.

## What the visualizations reveal

For the tiny text-note sample, risk and monitor notes can show partial separation because words such as `risk`, `warning`, `deviation`, `appetite`, `fatigue`, `review`, and `follow up` carry different TF-IDF/SVD signals from words such as `steady`, `normal`, `balanced`, and `expected`.

This should be interpreted as a methodology demonstration, not a scientific biological conclusion. The sample is intentionally small and manually written.

## Adapted exercise questions

### Do abnormal or risk growth cases form a cluster?

They may form a partial cluster in the SVD text-note space, but this is evidence of vocabulary separation, not proof of a biological growth cluster.

### Are there several kinds of risk cases?

The notes suggest at least two possible risk styles: rapid/overweight-risk language and stagnation/low-appetite/health-concern language. This is useful for project thinking, but it needs real data before becoming a model claim.

### Are the strongest patterns unrelated to the target?

Possibly. A component can capture writing style, repeated measurement words, age-related phrasing, or follow-up vocabulary instead of true risk. This is why component examples are exported next to terms.

### Does geometry reflect metadata or real patterns?

In this project-safe version, the text SVD geometry mostly reflects language patterns in growth notes. Numeric PCA and Isomap examples demonstrate projection methodology, not final Cane Corso biological evidence.

### Which visualization is most useful and which may be misleading?

The most useful view is the SVD component table combined with high-value example records, because it connects components to actual text. The most potentially misleading views are t-SNE or manifold plots if read as proof of real clusters. They are useful for exploration, not final evidence.

## Final project decision

Problem 5 is now represented explicitly through:

- `dimensionality_reduction_problem5_component_terms.csv`
- `dimensionality_reduction_problem5_component_examples.csv`
- `dimensionality_reduction_problem5_visualization_coordinates.csv`
- `dimensionality_reduction_problem5_visualization_interpretation.md`
- the notebook section **Problem 5 — Analyze and visualize components**
"""
    report_path("problem5_visualization_interpretation.md").write_text(interpretation, encoding="utf-8")


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
- Explicit Problem 5 component analysis: terms, example records, visual coordinates, and interpretation

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
    write_problem5_component_analysis()
    write_summary()
    print(f"Dimensionality reduction reports generated in {REPORT_DIR.as_posix()}")


if __name__ == "__main__":
    main()

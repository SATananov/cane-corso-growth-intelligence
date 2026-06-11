# Dimensionality Reduction Exercise Alignment

## Course exercise idea

The exercise asks students to compare different data representations using a real/fake job-posting classification dataset. The important learning objective is not the specific dataset itself, but the comparison between:

- structured metadata
- text features
- latent reduced representations
- supervised and unsupervised projections
- different metrics beyond accuracy
- interpretability of components and embeddings

## Project adaptation

The `cane-corso-growth-intelligence` project adapts this idea without downloading external Kaggle data or adding large files.

The module uses:

- the lightweight Iris dataset for numeric dimensionality reduction examples
- a synthetic non-linear sample for Kernel PCA
- a small project-style text-note sample for TF-IDF + TruncatedSVD
- Logistic Regression and Random Forest where useful
- balanced accuracy and macro F1 instead of accuracy alone

## Covered exercise requirements

| Exercise requirement | Project implementation |
|---|---|
| Inspect data and target distribution | Iris target distribution and feature audit |
| Feature selection / feature importance | Low variance, correlation audit, Random Forest importances |
| Baseline model | Logistic Regression on raw scaled features |
| Text features | Small project-style notes with TF-IDF |
| Latent space | TruncatedSVD for sparse text features, PCA for numeric features |
| Explained variance / components | PCA and SVD component reports |
| Visual representations | PCA, LinDA, Isomap, t-SNE embeddings |
| Compare representations | Metrics table with balanced accuracy and macro F1 |
| Compare classifiers | Logistic Regression baseline and Random Forest importances |
| Discuss trade-offs | Notes document and summary report |

## Why no external dataset is included

The original exercise points to a Kaggle dataset. Including that dataset would make the repository heavier and less portable. For the course project, the safer choice is to demonstrate the same methodology with small reproducible data.

This keeps the repository clean while preserving the educational value of the exercise.


## Strengthened Problem 5 coverage

Problem 5 from the exercise is treated as a priority because it tests whether dimensionality reduction is interpreted correctly, not just executed.

The project now includes explicit evidence for:

- high-positive and low/opposite-loading SVD terms;
- example growth-note records with high component values;
- cautious semantic-axis interpretation for each component;
- at least two visualization coordinate sets;
- direct answers to the exercise questions about clustering, misleading geometry, and whether patterns reflect the target or other factors.

See:

- `docs/course_exercises/dimensionality_reduction_problem5_component_analysis.md`
- `reports/course_exercises/dimensionality_reduction_problem5_component_terms.csv`
- `reports/course_exercises/dimensionality_reduction_problem5_component_examples.csv`
- `reports/course_exercises/dimensionality_reduction_problem5_visualization_coordinates.csv`
- `reports/course_exercises/dimensionality_reduction_problem5_visualization_interpretation.md`

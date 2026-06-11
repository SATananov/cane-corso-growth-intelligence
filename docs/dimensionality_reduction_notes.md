# Dimensionality Reduction and Manifold Learning Notes

This note documents how the course topic **Dimensionality Reduction** is represented inside the `cane-corso-growth-intelligence` project.

## Why dimensionality reduction matters for this project

The Cane Corso growth intelligence project can produce many candidate features: age, weight, height, chest measurements, growth velocity, rolling means, growth deltas, color/category metadata, lineage indicators, and free-text notes. Not all of those features should be used directly in every model.

Dimensionality reduction helps with three practical goals:

1. **Simplification** — reduce a large feature space to fewer informative representations.
2. **Visualization** — project complex data into 2D/3D views for inspection.
3. **Model comparison** — test whether compressed representations preserve enough signal for prediction.

## Feature selection vs. feature extraction

Feature selection keeps original columns. Examples used in this module:

- low-variance filtering
- high-correlation filtering
- Random Forest feature importance

Feature extraction creates new features that are combinations or transformations of the original features. Examples used in this module:

- PCA
- Kernel PCA
- LinDA / Linear Discriminant Analysis
- Isomap
- t-SNE for visualization
- TruncatedSVD for sparse text features

## PCA

Principal Component Analysis is a linear feature extraction method. It transforms the original feature space into orthogonal principal components sorted by explained variance. PCA is useful when many numeric features are correlated.

Important practical rule: **scale numeric features before PCA**. Otherwise, columns with large numeric ranges can dominate the principal components.

Project use:

- compress structured numeric growth features
- inspect explained variance
- compare a classifier on raw scaled features vs. PCA features

## Kernel PCA

Kernel PCA extends PCA to non-linear transformations through the kernel trick. The module includes a small synthetic non-linear example to show why a non-linear projection may be useful when the geometry cannot be captured well by standard linear PCA.

Project use:

- conceptual preparation for non-linear growth patterns
- demonstrates non-linear embedding without adding large data

## LinDA / Linear Discriminant Analysis

Linear Discriminant Analysis is a supervised dimensionality reduction method. Unlike PCA, it uses labels and tries to find directions that separate classes.

Project use:

- compare supervised transformation for growth-status classification
- demonstrate the difference between unsupervised variance-preserving methods and label-aware projections

## Manifold learning: Isomap and t-SNE

Manifold learning assumes that high-dimensional data may actually lie on a lower-dimensional surface.

- **Isomap** preserves approximate distances through a nearest-neighbor graph.
- **t-SNE** is mainly used for visualization and local cluster inspection.

Project use:

- 2D visual inspection of growth-status groups
- compare visual geometry between PCA, Isomap, and t-SNE
- avoid treating t-SNE as a production preprocessing step because it does not provide the same kind of stable transform for new data as PCA-style methods

## Text representation exercise alignment

The course exercise asks for comparison between metadata, text representations, and latent spaces. Since the original dataset is external and heavy, this project uses a small built-in text-note sample to demonstrate the same method safely:

- TF-IDF converts text into sparse features.
- TruncatedSVD compresses sparse text features into latent semantic components.
- Logistic Regression compares classification performance across representations.

This keeps the project GitHub-friendly while still covering the core course idea.


## Problem 5: component analysis and visualization

The exercise requirement to analyze and visualize components is represented explicitly in this project. The generated Problem 5 reports inspect TruncatedSVD components from the text-note representation, list top positive and low/opposite-loading terms, export example records with high component values, and provide visualization coordinates for notebook plots.

The key interpretation rule is conservative: a 2D projection can suggest structure, but it should not be treated as proof. For this project, SVD and projection views are used as exploratory tools for growth-note patterns until larger real Cane Corso growth datasets are available.

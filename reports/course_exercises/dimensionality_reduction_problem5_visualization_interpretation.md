# Problem 5 — Component Analysis and Visualization Interpretation

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

# Patch Report — Step 09: Unsupervised Learning and Clustering

## Purpose

This patch aligns the project with the third lecture topic:

```text
Unsupervised Learning, Clustering
```

It extends the project beyond supervised prediction and classification by adding exploratory growth-pattern grouping.

## Added Files

```text
notebooks/04_unsupervised_learning_clustering.ipynb
docs/clustering_learning_notes.md
PATCH_REPORT_STEP09_UNSUPERVISED_CLUSTERING.md
```

The notebook may generate the following figures when executed:

```text
reports/figures/kmeans_elbow_check.png
reports/figures/kmeans_silhouette_score.png
reports/figures/kmeans_growth_pattern_groups_pca.png
reports/figures/hierarchical_growth_groups_pca.png
reports/figures/dbscan_k_distance_check.png
reports/figures/dbscan_density_groups_pca.png
```

## Updated Files

```text
README.md
HOW_TO_RUN.md
COURSE_TOPIC_MAPPING.md
docs/math_foundation.md
```

## Lecture Coverage

The patch covers:

- Unsupervised Learning problem statement, intuition and challenges;
- K-Means Clustering motivation, example and `k-means++` initialization;
- Hierarchical Clustering motivation and example;
- K-Means vs Hierarchical Clustering comparison;
- DBSCAN density-based clustering and noise/no-outlier interpretation.

## Responsible Interpretation

The new clustering notebook keeps the same safety boundary as the rest of the project.

Clusters are interpreted as exploratory mathematical groups only.

They are not:

- veterinary diagnosis;
- official health assessment;
- breed proof;
- Cane Corso certification.

## Clean Submission Notes

No raw dataset archive is included.
No virtual environment is included.
No Git folder is included.
No cache files are included.

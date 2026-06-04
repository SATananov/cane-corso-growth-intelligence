# Clustering Exercise Alignment Summary

## Dataset and sample choice

The project uses Cane Corso prototype growth measurements. A single row is a dog-age growth-state observation. This is an educational modelling unit, not a final production-level independent sample. A larger version should use many dog-level longitudinal profiles.

Rows used: 32
Dogs represented: 4

## Recommended segmentation

The selected KMeans configuration uses **3 clusters**.

Selected silhouette score: 0.519267

## Segment profile table

The segment profile table is saved at:

`reports/course_exercises/clustering_exercise_segment_profiles.csv`

The profiles describe growth-state groups by age, weight, height, velocity, sex, and activity level.

## Contesting algorithm

Agglomerative clustering is included as a second clustering approach. It is reported beside KMeans to show whether the segment structure is stable across algorithms.

## Stability check

Average adjusted Rand index against the seed-42 reference:

1.0

## Cluster features in supervised prediction

The best educational feature set in the small comparison is:

`original_growth_features`

Mean macro F1: 0.859163

This comparison is not a production estimate. It only shows how cluster-derived features can be tested as additional model inputs.

## Final recommendation

Use clustering as an interpretability layer for growth-state monitoring, not as a medical diagnosis and not as proof of breed identity. The current segmentation is useful for explaining growth patterns, generating hypotheses, and preparing stronger future experiments with larger data.

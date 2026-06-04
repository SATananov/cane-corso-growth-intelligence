# Clustering and Segmentation Exercise Alignment

This document connects the clustering exercise to the Cane Corso Growth Intelligence project.

The original exercise is based on customer segmentation from transactional retail data. The project uses a different domain, so the direct business objects are changed:

| Exercise idea | Project translation |
|---|---|
| Customer behaviour | Cane Corso growth-state behaviour |
| Customer segments | Growth-state segments |
| Transaction cleaning | Measurement and identifier cleaning |
| Customer value profile | Growth profile and monitoring profile |
| Future buyer / high-value customer | Later growth behaviour proxy |
| Cluster features in prediction | Cluster-distance features added to a supervised baseline |

## Research question

Can growth-state observations be grouped into interpretable segments, and can those segments help explain or improve later growth-state prediction?

This is a domain adaptation of the original exercise. It does not claim to diagnose health or certify a dog. It only explores whether unsupervised learning can help describe patterns in the available educational growth data.

## Sample definition

The exercise warns that a single transaction is usually not the correct independent sample. In this project, the equivalent warning is that a single measurement is not a complete dog profile.

Because the current dataset is intentionally small, the educational clustering run uses a **dog-age growth-state observation** as the modelling row. This is useful for demonstrating the clustering workflow, but it is not a final production sampling strategy. A larger version of the project should aggregate multiple measurements into stable dog-level longitudinal profiles.

## Cleaning and feature policy

The project checks:

- missing dog identifiers;
- missing or impossible age, weight, or height values;
- non-positive measurements;
- repeated dog-age observations;
- unusually fast growth changes;
- categorical descriptors such as sex and activity level.

The created features include growth velocity, height velocity, weight-to-height ratio, distance to final observed weight, and chronological growth-age features.

## Time-aware evaluation

A chronological split is used for the descriptive clustering analysis. Early observations are treated as training context and later observations are treated as future-like context. This keeps the exercise aligned with the warning about time leakage.

Because the sample is small, supervised comparisons are reported as educational diagnostics rather than production-grade model estimates.

## Clustering workflow

The project runs:

- KMeans with several candidate values of `k`;
- inertia and silhouette comparison;
- agglomerative clustering as a contesting algorithm;
- segment profile creation;
- stability checks across multiple random seeds;
- a supervised comparison between original features, cluster-derived features, and combined features.

## Interpretation boundary

The segments are educational growth-state profiles. They are not veterinary diagnoses and are not evidence of breed identity, pedigree, or official status.

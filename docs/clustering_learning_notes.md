# Unsupervised Learning and Clustering Notes

This document explains how the third course topic is connected to the Cane Corso Growth Intelligence project.

## Problem Statement

Regression and classification use a known target:

```text
Regression: predict weight_kg
Classification: predict growth_status
```

Unsupervised learning does not use a target label. The goal is to discover structure inside the feature space:

```text
Clustering: group similar growth records without using y
```

For this project, clustering is useful as an exploratory layer. It can suggest similar growth-pattern groups and identify records that do not fit well into common groups.


## Mathematical Application Bridge

The project becomes stronger when the course topic is connected to a real product idea.

Real-world question:

```text
Can similar growth situations be grouped without manually assigning labels first?
```

Mathematical translation:

```text
x_i = [age_months, weight_kg, average_adult_breed_weight_kg,
       weight_to_adult_ratio, age_weight_ratio, adult_weight_group]
```

```text
X = matrix of all growth records
```

```text
y = not used
```

The clustering task becomes:

```text
find structure in X using distance, centroids, hierarchy or density
```

Practical product interpretation:

```text
This record resembles a specific growth-profile group in the dataset.
```

Safe limitation:

```text
A cluster is not a medical diagnosis. It is a mathematical similarity group.
```

## Intuition

Each dog growth record is represented as a point in a multi-dimensional space:

```text
x = [age, weight, adult_breed_weight, ratios, derived features]
```

Records that are close to each other may represent similar growth situations.

## Challenges

Clustering must be interpreted carefully because:

- there is no true label to check directly;
- results depend on selected features;
- scaling affects distance-based algorithms;
- outliers can change cluster structure;
- a mathematical cluster is not automatically a medical category.

## K-Means

K-Means creates `k` groups by assigning records to the nearest centroid.

Objective:

```text
c(i) = argmin_j ||x_i - mu_j||^2
```

```text
J = sum_i ||x_i - mu_c(i)||^2
```

The first formula assigns each point to the nearest centroid. The second formula shows the quantity that K-Means tries to reduce.

The notebook uses `k-means++` initialization because it chooses stronger starting centroids than random initialization.

K-Means is useful when the project needs a simple and fast grouping method, but it requires choosing `k`.

## Hierarchical Clustering

Hierarchical clustering builds groups step by step.

Agglomerative clustering starts with many small groups and merges similar groups until a final number of clusters is reached.

This is useful for explaining nested similarity structure, but it can be slower for large datasets.

## DBSCAN

DBSCAN groups dense areas and marks sparse points as noise.

Important parameters:

```text
eps = neighborhood radius
min_samples = minimum records needed to form a dense region
```

DBSCAN is useful for detecting records that do not naturally fit dense growth-pattern groups. In this project, those records should be treated as exploratory signals only, not veterinary conclusions.

## K-Means vs Hierarchical Clustering

| Method | Strength | Weakness |
|---|---|---|
| K-Means | fast, simple, useful baseline | must choose k, assumes compact groups |
| Hierarchical | explains nested similarity | slower, also needs a cut point |
| DBSCAN | can detect noise/outliers | sensitive to eps/min_samples |

## Responsible Use

The clustering notebook is educational and exploratory.

Correct interpretation:

```text
This record belongs to a mathematical group with similar records.
```

Incorrect interpretation:

```text
This cluster proves a health problem or official breed status.
```

The safest product use is to show clusters as additional context for owner-friendly monitoring, together with clear explanation and human review.


## From Algorithm Output to Application

A useful final project should not stop at algorithm output.

For this project, the interpretation layer is:

| Algorithm output | Mathematical meaning | Application meaning |
|---|---|---|
| K-Means cluster | nearest-centroid similarity group | simple growth-profile group |
| Hierarchical cluster | nested similarity structure | explanation of related records |
| DBSCAN noise | outside dense neighborhoods | candidate for careful review |
| Silhouette score | separation and cohesion indicator | quality check, not biological proof |

The strongest final-project sentence is:

```text
Clustering helps organize growth data into mathematically similar profiles so an owner-facing system can support monitoring and review without claiming diagnosis.
```

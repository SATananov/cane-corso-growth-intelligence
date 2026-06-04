# Visual Similarity Training Safety Boundaries

This document belongs to an optional exploratory extension outside the current core course sequence. The core course-aligned project remains the tabular growth-intelligence workflow using regression, classification, clustering, feature engineering and time-series features.

This document defines the safety and interpretation boundaries for the future baseline image classifier.

## Core principle

The image model should be described as a **visual similarity classifier**, not as a definitive breed detector.

A photograph can show visual features, but it cannot prove:

No pedigree, genetic origin, registry status, health status, or official breed identity can be proven from this educational visual model alone.


- pedigree,
- genetic origin,
- official breed identity,
- registry status,
- health status,
- correct breeding history.

## Safe prediction language

Use language like:

```text
The image has the strongest visual similarity to class X among the classes included in this educational model.
```

Avoid language like:

```text
This dog is definitely class X.
```

## Probability interpretation

Model probabilities should be explained carefully.

A result like:

```text
Cane Corso-like class: 0.65
Other molossoid-like class: 0.25
Unknown: 0.10
```

means that the model assigned the highest score to the first class **within its limited training set**. It does not mean the dog is officially that breed.

## Dataset limitations

The first baseline depends on Stanford Dogs availability and public labels. Some target molossoid breeds may be missing. If a class is missing, the project should not invent it or claim it was trained.

## Ethical and legal notes

The project should use:

- public datasets with documented sources,
- local-only copies of images,
- manifest files and reports in the repository,
- no random scraping from Google, Facebook, Instagram, or private pages without permission.

## the repository boundary

Do not commit:

- raw image datasets,
- extracted image folders,
- image archives,
- large trained model files,
- private user images.

Commit only:

- code,
- documentation,
- notebooks,
- small CSV manifests,
- evaluation reports.

## Final statement

The visual model is an educational experiment and a future support tool. It is not an official breed authority.

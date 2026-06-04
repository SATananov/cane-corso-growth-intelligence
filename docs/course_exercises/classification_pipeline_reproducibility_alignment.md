# Classification Exercise Alignment

This document explains how the project aligns with the classification exercise focused on complex models, data pipelines, reproducibility, model comparison, feature engineering, feature importance, and error analysis.

The exercise uses the Spaceship Titanic dataset as its teaching context. In this project, the same classification workflow is applied to the Cane Corso growth-intelligence domain. The goal is not to copy the original dataset, but to demonstrate the same machine learning reasoning on the project data.

## Project classification question

Can a small, reproducible pipeline classify whether a new growth interval belongs to a faster-growth period using previous measurements and simple engineered features?

This is an educational binary classification task. It does not diagnose health, does not replace veterinary judgment, and does not claim that a dog is developing correctly or incorrectly.

## How the exercise ideas are mapped

| Exercise concept | Project implementation |
|---|---|
| Data inspection | The script loads the prototype Cane Corso growth table and derives interval-level observations. |
| Experimental protocol | The script defines a fixed random seed, stratified holdout split, cross-validation strategy, main metric, and secondary metrics. |
| Dummy models | Two dummy classifiers are evaluated: most-frequent and stratified random guessing. |
| Basic pipeline | Numeric features are imputed and scaled; categorical features are imputed and one-hot encoded using a `ColumnTransformer`. |
| Logistic regression | A logistic regression pipeline is used as the first interpretable baseline classifier. |
| Learning curve | A learning-curve summary is produced when the sample size is sufficient. |
| Feature engineering | Previous weight, previous height, previous morphology ratio, and age-related features are used. |
| Alternative classifier | A random forest classifier is evaluated with the same split and comparable metrics. |
| Hyperparameter tuning | Logistic regression and random forest use small, reproducible parameter grids. |
| Feature importance | Permutation importance is used on the selected model to avoid relying only on model-specific importances. |
| Error analysis | False positives, false negatives, and confident errors are summarized. |
| Ablation study | Feature groups are compared to show how engineered information changes performance. |

## Interpretation boundaries

The target is a learning proxy derived from a small educational dataset. It is useful for demonstrating classification methodology, not for making real veterinary conclusions.

The correct interpretation is:

> The classifier demonstrates a reproducible binary classification workflow on growth-interval data.

The incorrect interpretation would be:

> The classifier proves whether a Cane Corso grows normally or abnormally.

The project deliberately avoids that claim.

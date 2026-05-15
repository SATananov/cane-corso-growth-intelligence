# Project Brief

## Working Title

Cane Corso Growth Intelligence

## Project Idea

Cane Corso Growth Intelligence is a machine learning course project focused on dog growth analysis.

The project uses the Cane Corso domain as a practical and personally meaningful context, while the technical implementation follows the course topics step by step.

The project is not a veterinary product and does not provide diagnosis. It is an educational machine learning project.

## Main Problem

Large-breed dogs grow quickly during the first months of life. Owners often want to understand growth patterns, weight development, and whether a record may need additional review.

Machine learning can be used to explore these questions in different ways:

- regression predicts numerical values
- classification predicts known categories
- clustering can later discover unknown groups

## Completed Stage 1: Regression

Course topic:

```text
Linear Regression, Regularization and Testing
```

Notebook:

```text
notebooks/01_linear_regression_growth_prediction.ipynb
```

This stage started with a prototype Cane Corso dataset and applied:

- problem statement and motivation
- simple linear regression
- polynomial regression
- multi-dimensional linear regression
- Ridge and Lasso regularization
- RANSAC robust regression
- MAE, MSE, RMSE, and R2 model testing
- final regression model comparison

The first regression task was:

```text
Can age and growth-related features be used to predict dog weight?
```

## Completed Stage 2: Real Data Foundation

The project now includes real processed public dog growth data.

Raw data is kept local only and is not committed to GitHub.

Processed samples committed to the project:

```text
data/processed/dog_growth_public_sample.csv
data/processed/dog_growth_classification_sample.csv
```

Scripts:

```text
src/create_public_sample.py
src/create_classification_sample.py
```

The real data foundation makes the project stronger because later notebooks can work with realistic public data instead of only a prototype dataset.

## Completed Stage 3: Classification

Course topic:

```text
Classification
```

Notebook:

```text
notebooks/03_classification_growth_status.ipynb
```

This stage uses the balanced classification-focused processed sample.

Classification target:

```text
growth_status
```

Target classes:

- `normal_growth`
- `needs_attention`

Binary target:

- `0` = `normal_growth`
- `1` = `needs_attention`

Models and evaluation covered:

- Logistic Regression
- Confusion Matrix
- Accuracy, Precision, Recall, F1-score
- ROC Curve and AUC
- Decision Tree Classifier
- Random Forest
- AdaBoost
- Support Vector Machine
- final classification model comparison

## Next Planned Stage

Next course topic:

```text
Unsupervised Learning, Clustering
```

Planned notebook:

```text
notebooks/04_unsupervised_clustering_growth_patterns.ipynb
```

Planned goal:

```text
Discover growth-pattern groups in real dog growth data using unsupervised clustering methods.
```

This stage will likely include:

- unsupervised learning problem statement
- clustering feature preparation
- K-Means clustering
- comparison of different K values
- Hierarchical Clustering
- DBSCAN
- final clustering comparison

## Current Data Layers

Prototype dataset:

```text
data/prototype/cane_corso_growth_sample.csv
```

General processed real public sample:

```text
data/processed/dog_growth_public_sample.csv
```

Classification-focused processed sample:

```text
data/processed/dog_growth_classification_sample.csv
```

Raw data folder:

```text
data/raw/
```

Only `data/raw/source_notes.md` is committed. Large raw external files remain local and are ignored by Git.


## Mathematical Foundation

The project includes a dedicated mathematical foundation document:

```text
docs/math_foundation.md
```

This document explains the formulas and model ideas used in the completed notebooks, including:

- regression equations
- Ordinary Least Squares
- MAE, MSE, RMSE, and R2 Score
- Ridge and Lasso regularization
- Logistic Regression and sigmoid probability
- confusion matrix metrics
- ROC/AUC
- Decision Tree impurity measures
- Random Forest, AdaBoost, and SVM intuition

This helps show that the project is not only code execution, but also an understanding of the mathematical ideas behind each machine learning method.

## Limitations

The project is educational.

The machine learning models should not be used for veterinary diagnosis or health decisions.

Dog growth depends on many factors, including sex, genetics, nutrition, activity, health, environment, and breed-specific differences.

The project focuses on applying course concepts correctly and documenting each stage clearly.

## Geometric Interpretation

The project also includes a geometric explanation of the machine learning methods in:

```text
docs/geometric_interpretation.md
```

This document explains the models as coordinate-space objects:

- data records as points
- regression as a line or curve
- residuals as distances from the model prediction
- classification as a decision boundary
- SVM as margin-based separation
- clustering as groups of nearby points

The related visual figures are stored in:

```text
reports/figures/
```

This supports the mathematical understanding of the project without changing the notebook experiments.

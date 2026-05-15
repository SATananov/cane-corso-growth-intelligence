# Course Topic Mapping

This document maps each completed course topic to the corresponding project files and notebook sections.

The goal is to show that the project follows the course material step by step and applies it to a practical dog growth analysis context.

## Project Stages

```text
01 Regression
02 Real Data Preparation
03 Classification
04 Unsupervised Learning / Clustering - planned
```


## Mathematical Foundation Document

The project includes a separate mathematical explanation file:

```text
docs/math_foundation.md
```

This file connects the code implementation to the formulas behind regression, classification, evaluation metrics, regularization, decision trees, ensemble methods, SVM, and planned clustering.

---

# Course Topic Mapping: Linear Regression, Regularization and Testing

Notebook:

```text
notebooks/01_linear_regression_growth_prediction.ipynb
```

Mathematical explanation:

```text
docs/math_foundation.md
```

## Topic Coverage

### 1. Regression - Problem Statement and Motivation

Covered in:

- `PROJECT_BRIEF.md`
- notebook introduction
- problem statement section

The project defines a regression problem: predicting dog weight from growth-related features.

### 2. Ordinary Least Squares / Simple Linear Regression

Covered in:

- `First Linear Regression Model` section

The first model uses:

- input: `age_months`
- target: `weight_kg`

### 3. Simulated / Prototype Example

Covered in:

- `data/prototype/cane_corso_growth_sample.csv`
- `DATA_SOURCES.md`

The prototype dataset is clearly marked as educational sample data.

### 4. Implementation on Data

Covered in:

- data loading section
- initial data exploration
- regression model training
- prediction results

### 5. Polynomial Regression

Covered in:

- `Polynomial Regression` section

This experiment tests a non-linear extension of linear regression.

### 6. Multi-Dimensional Linear Regression

Covered in:

- `Multi-Dimensional Linear Regression` section

This model uses multiple features such as age, height, sex, and activity level.

### 7. Regularization

Covered in:

- `Regularization: Ridge and Lasso Regression` section

The notebook compares:

- Ridge Regression
- Lasso Regression

### 8. RANSAC - Robust Regression Model

Covered in:

- `RANSAC Robust Regression` section

The notebook adds an artificial outlier and compares normal linear regression with RANSAC regression.

### 9. Model Testing

Covered in:

- evaluation metrics sections
- final model comparison table

The notebook uses:

- MAE
- MSE
- RMSE
- R2 Score

### 10. Final Regression Comparison

Covered in:

- `Final Model Comparison` section

The tested regression models are compared in one table.

Status:

```text
Linear Regression, Regularization and Testing ✅
```

---

# Real Data Foundation

Files:

```text
docs/real_data_source_notes.md
docs/real_data_download_instructions.md
docs/data_preparation_plan.md
notebooks/02_real_data_preparation.ipynb
src/create_public_sample.py
src/create_classification_sample.py
```

Processed samples:

```text
data/processed/dog_growth_public_sample.csv
data/processed/dog_growth_classification_sample.csv
```

The raw dataset is kept local only in `data/raw/` and is not committed to GitHub.

Status:

```text
Real Data Foundation ✅
```

---

# Course Topic Mapping: Classification

Notebook:

```text
notebooks/03_classification_growth_status.ipynb
```

Mathematical explanation:

```text
docs/math_foundation.md
```

The notebook follows the Classification lecture step by step and applies it to the balanced processed dog growth classification sample.

Classification sample:

```text
data/processed/dog_growth_classification_sample.csv
```

## Topic Coverage

### 1. Classification - Problem Statement and Motivation

Covered in:

- notebook introduction
- problem statement section

The project changes from predicting a numerical value to predicting a class.

Regression task:

- predict `weight_kg`

Classification task:

- predict `growth_status`

### 2. Binary Classification

Covered in:

- `Create Classification Target` section

Target column:

```text
growth_status
```

Binary numeric target:

- `0` = `normal_growth`
- `1` = `needs_attention`

The balanced classification sample contains:

- 5,000 `normal_growth` records
- 5,000 `needs_attention` records

### 3. Logistic Regression

Covered in:

- `Logistic Regression Classifier` section

The model predicts whether a record belongs to `normal_growth` or `needs_attention`.

### 4. Classification Evaluation

Covered in:

- `Classification Evaluation` section

The notebook uses:

- Confusion Matrix
- Accuracy
- Precision
- Recall
- F1-score
- Classification Report

### 5. ROC Curve and AUC

Covered in:

- `ROC Curve and AUC` section

The notebook uses:

- ROC curve
- AUC score

### 6. Decision Tree Classifier

Covered in:

- `Decision Tree Classifier` section

The section also includes feature importance.

### 7. Ensemble Models

Covered in:

- `Ensemble Models: Random Forest and AdaBoost` section

Models tested:

- Random Forest Classifier
- AdaBoost Classifier

### 8. Support Vector Machine

Covered in:

- `Support Vector Machine Classifier` section

The notebook trains an SVM classifier with an RBF kernel and evaluates it with classification metrics and ROC/AUC.

### 9. Final Classification Model Comparison

Covered in:

- `Final Classification Model Comparison` section

Models compared:

- Logistic Regression
- Decision Tree
- Random Forest
- AdaBoost
- Support Vector Machine

Metrics compared:

- Accuracy
- Precision
- Recall
- F1-score
- AUC

Status:

```text
Classification ✅
```

---

# Planned Course Topic Mapping: Unsupervised Learning, Clustering

Planned notebook:

```text
notebooks/04_unsupervised_clustering_growth_patterns.ipynb
```

Mathematical planning:

```text
docs/math_foundation.md
```

Planned topic coverage:

- Unsupervised Learning problem statement, intuition, and challenges
- K-Means clustering
- K-Means++ motivation
- comparison of different K values
- Hierarchical Clustering
- comparison between K-Means and Hierarchical Clustering
- DBSCAN
- final clustering comparison

Status:

```text
Unsupervised Learning, Clustering ⏳
```

---

# Geometric Interpretation Support

Supporting document:

```text
docs/geometric_interpretation.md
```

Supporting figures:

```text
reports/figures/regression_coordinate_system.png
reports/figures/polynomial_curve_coordinate_system.png
reports/figures/classification_feature_space_boundary.png
reports/figures/clustering_feature_space_concept.png
```

This section supports the course topics by showing how the mathematical methods can be understood geometrically:

- Regression learns a line or curve in a coordinate system.
- Prediction error is the distance between the actual point and the model prediction.
- Classification learns a decision boundary in feature space.
- SVM uses margin-based geometry.
- Clustering groups nearby points in feature space.

This supports the mathematical understanding requirement without changing the notebooks or model outputs.

# Course Topic Mapping

This document maps the current project work to the course topic:

**Linear Regression, Regularization and Testing**

The goal is to show that the notebook follows the course material step by step and applies it to a practical example: Cane Corso growth analysis.

## Topic Coverage

### 1. Regression - Problem Statement and Motivation

Covered in:

- `PROJECT_BRIEF.md`
- notebook introduction
- problem statement section

The project defines a simple regression problem: predicting dog weight from growth-related features.

### 2. Ordinary Least Squares / Simple Linear Regression

Covered in:

- `First Linear Regression Model` section in the notebook

The first model uses:

- input: `age_months`
- target: `weight_kg`

This is the baseline regression model.

### 3. Simulated / Prototype Example

Covered in:

- `data/prototype/cane_corso_growth_sample.csv`
- `DATA_SOURCES.md`

The dataset is clearly marked as prototype data and is used only for learning and first experiments.

### 4. Implementation on Data

Covered in:

- data loading section
- initial data exploration
- regression model training
- prediction results

The notebook loads the dataset, explores it, trains models, and evaluates the results.

### 5. Polynomial Regression

Covered in:

- `Polynomial Regression` section in the notebook

This experiment tests a non-linear extension of linear regression.

### 6. Multi-Dimensional Linear Regression

Covered in:

- `Multi-Dimensional Linear Regression` section in the notebook

This model uses multiple features:

- `age_months`
- `height_cm`
- `sex`
- `activity_level`

### 7. Regularization

Covered in:

- `Regularization: Ridge and Lasso Regression` section in the notebook

The notebook compares:

- Ridge Regression
- Lasso Regression

### 8. RANSAC - Robust Regression Model

Covered in:

- `RANSAC Robust Regression` section in the notebook

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

### 10. Final Comparison

Covered in:

- `Final Model Comparison` section in the notebook

The tested models are compared in one table.

## Current Status

The first course topic is covered as a first project stage.

The project is not finished yet. Future course topics will be added step by step in separate notebook sections and commits.

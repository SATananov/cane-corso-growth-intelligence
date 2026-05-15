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

---

# Course Topic Mapping: Classification

This section maps the second course topic to the project work.

Course topic:

**Classification**

The goal is to show that the notebook `notebooks/03_classification_growth_status.ipynb` follows the classification lecture step by step and applies it to the real processed dog growth dataset.

## Topic Coverage

### 1. Classification - Problem Statement and Motivation

Covered in:

- `notebooks/03_classification_growth_status.ipynb`
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

The target column is:

- `growth_status`

The binary numeric target is:

- `0` = `normal_growth`
- `1` = `needs_attention`

This is created from body condition score information.

### 3. Logistic Regression

Covered in:

- `Logistic Regression Classifier` section

The model uses the processed real dog growth sample and predicts whether a record belongs to `normal_growth` or `needs_attention`.

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

This evaluates the binary classifier at different probability thresholds.

### 6. Decision Tree Classifier

Covered in:

- `Decision Tree Classifier` section

The notebook trains a Decision Tree model and compares it with Logistic Regression.

The section also includes feature importance.

### 7. Ensemble Models

Covered in:

- `Ensemble Models: Random Forest and AdaBoost` section

The notebook tests:

- Random Forest Classifier
- AdaBoost Classifier

These models are used to compare ensemble methods with simpler classifiers.

### 8. Support Vector Machine

Covered in:

- `Support Vector Machine Classifier` section

The notebook trains an SVM classifier with an RBF kernel and evaluates it with classification metrics and ROC/AUC.

### 9. Final Classification Model Comparison

Covered in:

- `Final Classification Model Comparison` section

The tested models are compared using:

- Accuracy
- Precision
- Recall
- F1-score
- AUC

Models compared:

- Logistic Regression
- Decision Tree
- Random Forest
- AdaBoost
- Support Vector Machine

## Current Status

The Classification topic is covered as the second main project stage.

The project now includes:

- one regression notebook
- one real data preparation notebook
- one classification notebook
- a prototype dataset
- a processed real public dog growth sample

Future course topics will be added in the same way: topic by topic, notebook by notebook, and commit by commit.

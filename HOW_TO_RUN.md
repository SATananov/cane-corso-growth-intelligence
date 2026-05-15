# How to Run the Project

This file explains how to run the project locally.

## 1. Clone the repository

```bash
git clone https://github.com/SATananov/cane-corso-growth-intelligence.git
cd cane-corso-growth-intelligence
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

## 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Open the notebooks

The project currently contains three main notebooks.

### Regression Topic

```text
notebooks/01_linear_regression_growth_prediction.ipynb
```

This notebook covers:

- Linear Regression
- Polynomial Regression
- Multi-Dimensional Linear Regression
- Ridge and Lasso Regularization
- RANSAC Robust Regression
- Regression model comparison

### Real Data Preparation

```text
notebooks/02_real_data_preparation.ipynb
```

This notebook prepares the project for working with the real public dog growth dataset.

The full raw dataset is not committed to GitHub.

### Classification Topic

```text
notebooks/03_classification_growth_status.ipynb
```

This notebook covers:

- Classification problem statement
- Logistic Regression
- Confusion Matrix
- Accuracy, Precision, Recall, F1-score
- ROC Curve and AUC
- Decision Tree Classifier
- Random Forest
- AdaBoost
- Support Vector Machine
- Final classification model comparison


## 6. Read the mathematical foundation

The project includes a mathematical explanation of the main formulas used in the notebooks:

```text
docs/math_foundation.md
```

This document covers:

- regression equations and error metrics
- Ridge and Lasso regularization
- Logistic Regression and the sigmoid function
- confusion matrix metrics
- ROC/AUC
- Decision Tree impurity measures
- Random Forest, AdaBoost, and SVM intuition
- planned clustering mathematics

## 7. Project data

The project contains prototype data and processed real public data samples.

### Prototype dataset

```text
data/prototype/cane_corso_growth_sample.csv
```

This dataset is used for the first regression experiments.

### General processed real sample

```text
data/processed/dog_growth_public_sample.csv
```

This is a smaller processed sample created from the real public dog growth dataset.

It contains:

- 10,000 rows
- 12 columns
- source label: `real_public_processed_sample`

### Classification-focused processed sample

```text
data/processed/dog_growth_classification_sample.csv
```

This sample is balanced for the Classification topic and contains:

- 10,000 rows
- 15 columns
- 5,000 `normal_growth` records
- 5,000 `needs_attention` records
- source label: `real_public_classification_sample`

## 8. Source scripts

The project includes scripts used to create processed samples from the local raw dataset.

```text
src/create_public_sample.py
src/create_classification_sample.py
```

The raw dataset ZIP must be downloaded manually and kept locally in:

```text
data/raw/
```

The raw dataset is intentionally ignored by Git and is not committed to GitHub.

## 9. Current project stage

The project currently covers two completed course topics:

1. Linear Regression, Regularization and Testing
2. Classification

It also includes a Real Data Foundation stage with processed samples from a real public dog growth dataset.

The next planned course topic is:

```text
Unsupervised Learning, Clustering
```

Future topics will be added step by step in new notebooks, with separate commits and updated course mapping.

## 10. Read the geometric interpretation

The project includes a geometric explanation of the models:

```text
docs/geometric_interpretation.md
```

This document connects the project to coordinate systems and feature space. It explains:

- data records as points
- regression as a line or curve
- residuals as vertical errors
- classification as a decision boundary
- clustering as groups of nearby points

The related figures are stored in:

```text
reports/figures/
```

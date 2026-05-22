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

The project currently contains six notebooks.

### Project Concept and Mathematical Framing

```text
notebooks/00_project_concept_and_mathematical_framing.ipynb
```

This notebook explains the project idea, mathematical formulation, feature-vector view, responsible-use boundaries, and how the work connects to the course topics.

### Regression Topic

```text
notebooks/01_linear_regression_growth_prediction.ipynb
```

This notebook covers:

- Ordinary Least Squares simulated example
- Linear Regression
- Real-data regression on the processed public dog growth sample
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
- Precision-Recall Curve
- Threshold comparison
- Decision Tree Classifier
- Random Forest
- AdaBoost
- Support Vector Machine
- Basic hyperparameter tuning
- Drift and monitoring considerations
- Final classification model comparison

### Unsupervised Learning and Clustering Topic

```text
notebooks/04_unsupervised_learning_clustering.ipynb
```

This notebook covers:

- Unsupervised Learning problem statement and challenges
- k-Nearest Neighbors as a distance-based lazy-learning method
- Minkowski / Euclidean distance intuition
- synthetic blobs, moons and circles examples
- feature scaling for distance-based methods
- K-Means Clustering
- `k-means++` initialization
- elbow method, silhouette score and silhouette samples
- Hierarchical Clustering and dendrogram visualization
- K-Means vs Hierarchical Clustering comparison
- DBSCAN density clustering and noise detection
- clustering vs classification comparison using Adjusted Rand Index
- Step 09.1/09.2 notes: mathematical application bridge and exact lesson alignment


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
- kNN distance logic, K-Means, Hierarchical Clustering and DBSCAN mathematics

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

The original public dataset is distributed as a compressed archive. In this project, it is referred to as the **raw dataset archive** and should be kept locally in:

```text
data/raw/Final_Data_PLOS.zip
```

The raw dataset archive is intentionally ignored by Git and is not committed to GitHub. The current notebooks use the smaller processed CSV files already stored in `data/processed/`.

More detail is documented in:

```text
docs/raw_dataset_archive_policy.md
```

## 9. Current project stage

The project currently covers three completed course topics:

1. Linear Regression, Regularization and Testing
2. Classification
3. Unsupervised Learning and Clustering

It also includes a Real Data Foundation stage with processed samples from a real public dog growth dataset.

The next planned course topic is:

```text
Feature Engineering and Time Series
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

## Classification Exercise Notebook

The project also includes a classification workflow exercise notebook:

```text
notebooks/03_1_classification_pipeline_exercise.ipynb
```

This notebook can be opened in VSCode or Jupyter after installing the dependencies. It uses:

```text
data/processed/dog_growth_classification_sample.csv
```

The notebook covers dummy baselines, pipelines, cross-validation, learning curves, engineered features, model comparison, permutation importance, error analysis, and ablation study.

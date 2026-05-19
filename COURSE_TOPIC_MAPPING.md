# Course Topic Mapping

This document maps the course lectures to the project files, notebooks and planned stages.

The project is built lecture by lecture. The goal is not to create separate unrelated exercises, but to connect every topic into one coherent idea:

```text
Cane Corso Growth Intelligence = mathematical growth profiling + predictive monitoring + interpretable ML signals
```

---

## Notebook Mathematical Formulation Standard

For every course topic notebook, the project uses the same mathematical structure:

| Required part | Purpose |
|---|---|
| `Input vector X` | Defines the data representation used by the model |
| `Target y` | Defines what is predicted or explains that no target exists for unsupervised learning |
| `Model function f(x)` | Defines the mathematical mapping learned by the method |
| `Loss function` | Defines what error/objective the method tries to reduce |
| `Metrics` | Defines how the result is evaluated |
| `Interpretation` | Translates model output into the growth-monitoring story |
| `Limitations` | States assumptions, boundaries, and responsible use |

This standard should appear in every new notebook from Step 04 onward.

---

## Overall Coverage Status

| Course topic | Status | Project role |
|---|---:|---|
| Linear Regression, Regularization and Testing | Completed | expected growth prediction and residual analysis |
| Classification | Completed / extended | `normal_growth` vs `needs_attention` probability signal |
| Unsupervised Learning, Clustering | Planned next | unknown growth-pattern groups |
| Feature Engineering and Time Series | Partially started / planned | growth ratios, velocity, trajectory over time |
| Dimensionality Reduction | Planned | 2D visualization of high-dimensional growth profiles |
| MLflow | Planned | experiment tracking and model comparison |

---

## Concept and Mathematical Framing

Files:

```text
PROJECT_BRIEF.md
README.md
docs/product_idea_and_mathematical_framing.md
docs/model_learning_explanation.md
notebooks/00_project_concept_and_mathematical_framing.ipynb
```

Purpose:

- explain the project as a useful product idea, not only a homework task;
- define the mathematical feature-vector view;
- explain how the model learns from data;
- clarify the public data source and limitations;
- connect the project to an owner-friendly monitoring flow.

Status:

```text
Project idea and mathematical framing ✅
```

---

# Topic 1: Linear Regression, Regularization and Testing

Notebook:

```text
notebooks/01_linear_regression_growth_prediction.ipynb
```

Mathematical explanation:

```text
docs/math_foundation.md
docs/geometric_interpretation.md
```

## Topic Coverage

### 1. Regression Problem Statement and Motivation

Covered in:

- `PROJECT_BRIEF.md`
- notebook introduction
- problem statement section

The project defines a regression problem:

```text
predict dog weight from growth-related features
```

Stronger mathematical interpretation:

```text
learn an expected growth function y = f(x)
```

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

This model uses multiple features such as age, height, sex and activity level.

### 7. Regularization

Covered in:

- `Regularization: Ridge and Lasso Regression` section

The notebook compares:

- Ridge Regression
- Lasso Regression

### 8. RANSAC Robust Regression

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

### 10. Mathematical Improvement Direction

The project should emphasize residual analysis:

```text
residual = real_weight - predicted_weight
```

This connects model performance to error distribution, bias, outliers and expected growth deviation.

Status:

```text
Linear Regression, Regularization and Testing ✅
```

---

# Real Data Foundation

Files:

```text
DATA_SOURCES.md
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

The raw dataset is kept local only in `data/raw/` and should not be committed to GitHub or included in the final clean ZIP.

Status:

```text
Real Data Foundation ✅
```

---

# Topic 2: Classification

Notebook:

```text
notebooks/03_classification_growth_status.ipynb
```

Mathematical explanation:

```text
docs/math_foundation.md
docs/model_learning_explanation.md
```

The notebook follows the Classification lecture and applies it to the balanced processed dog growth classification sample.

Classification sample:

```text
data/processed/dog_growth_classification_sample.csv
```

## Topic Coverage

### 1. Classification Problem Statement and Motivation

Covered in:

- notebook introduction
- problem statement section
- project brief

The project changes from predicting a numerical value to predicting a class.

Regression task:

```text
predict weight_kg
```

Classification task:

```text
predict growth_status
```

### 2. Binary Classification

Covered in:

- `Create Classification Target` section

Target labels:

```text
normal_growth
needs_attention
```

Binary numeric labels:

```text
0 = normal_growth
1 = needs_attention
```

### 3. Logistic Regression

Covered in:

- Logistic Regression model section

Mathematical interpretation:

```text
p = 1 / (1 + e^(-z))
z = beta_0 + beta_1*x_1 + ... + beta_n*x_n
```

The model outputs a probability:

```text
P(needs_attention | x)
```

### 4. Train/Test Split

Covered in:

- data split section

The project evaluates models on unseen test data.

### 5. Confusion Matrix and Metrics

Covered in:

- confusion matrix section
- classification report section

Metrics:

- accuracy
- precision
- recall
- F1-score

### 6. ROC Curve and AUC

Covered in:

- ROC/AUC section

This evaluates probability separation across thresholds.

### 7. Decision Tree

Covered in:

- Decision Tree section

Adds interpretable rule-based classification.

### 8. Ensemble Models

Covered in:

- Random Forest
- AdaBoost

### 9. Support Vector Machine

Covered in:

- SVM section

The notebook trains an SVM classifier and evaluates it with classification metrics and ROC/AUC.

### 10. Final Model Comparison

Covered in:

- final classification model comparison section

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

# Classification Pipeline Exercise Extension

Notebook:

```text
notebooks/03_1_classification_pipeline_exercise.ipynb
```

This extension strengthens the classification stage by adding workflow quality.

## Exercise Coverage

### 1. Dummy Baselines

Covered by:

- `DummyClassifier(strategy="most_frequent")`
- `DummyClassifier(strategy="stratified")`

### 2. Data Pipeline

Covered by:

- `ColumnTransformer`
- numeric imputation
- scaling
- categorical imputation
- one-hot encoding
- Logistic Regression inside a pipeline

### 3. Cross-Validation

Covered by stratified cross-validation.

### 4. Learning Curve

Covered by the learning curve section.

The notebook evaluates how F1-score changes with different training set sizes.

### 5. Feature Engineering

Covered by engineered growth features such as:

- `weight_to_adult_breed_weight_ratio`
- `age_weight_ratio`
- `growth_pressure_index`
- `puppy_stage`
- `adult_breed_weight_group`

### 6. Model Comparison

Models tested include:

- Logistic Regression
- Random Forest
- Gradient Boosting

### 7. Feature Importances

Covered by permutation importance.

### 8. Error Analysis

The notebook checks:

- false positives
- false negatives
- error rate by puppy stage
- confidently wrong predictions

### 9. Ablation Study

The notebook compares feature groups under the same evaluation protocol.

Status:

```text
Classification Pipeline Extension ✅
```

---

# Topic 3: Unsupervised Learning, Clustering

Planned notebook:

```text
notebooks/04_unsupervised_clustering_growth_patterns.ipynb
```

Planned mathematical role:

```text
discover growth-pattern groups without using target labels
```

Planned coverage:

- unsupervised learning problem statement
- feature scaling
- K-Means
- K-Means++ motivation
- Elbow Method
- Silhouette Score
- Hierarchical Clustering
- DBSCAN
- cluster interpretation

Planned product interpretation:

```text
This dog record resembles a steady-growth / fast-growth / slow-growth / irregular-growth group.
```

Status:

```text
Unsupervised Learning, Clustering ⏳
```

---

# Topic 4: Feature Engineering and Time Series

Current status:

```text
Feature Engineering: partially covered
Time Series: planned
```

Already covered in the classification exercise:

- ratio features
- growth-pressure features
- puppy-stage grouping
- categorical encoding

Planned additions:

- growth velocity
- moving average
- rolling deviation
- ordered dog trajectory
- trend over time

Mathematical interpretation:

```text
growth_velocity = delta_weight / delta_time
relative_deviation = (actual_weight - expected_weight) / expected_weight
```

Status:

```text
Feature Engineering ⚠️ / Time Series ⏳
```

---

# Topic 5: Dimensionality Reduction

Planned notebook or section:

```text
notebooks/05_dimensionality_reduction_growth_profiles.ipynb
```

Planned methods:

- PCA
- optional t-SNE / UMAP discussion if appropriate

Mathematical role:

```text
project high-dimensional growth records into 2D for visualization
```

Product role:

```text
show a visual map of growth profiles and how records separate by status or cluster
```

Status:

```text
Dimensionality Reduction ⏳
```

---

# Topic 6: MLflow

Planned notebook or experiment folder:

```text
notebooks/06_mlflow_experiment_tracking.ipynb
```

Planned coverage:

- experiment tracking
- logged parameters
- logged metrics
- model comparison
- reproducibility notes

Product role:

```text
track which model version gives the best growth-monitoring signal
```

Status:

```text
MLflow ⏳
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

This section supports the course topics by showing how mathematical methods can be understood geometrically:

- data records as points;
- regression as a line or curve;
- residuals as distances from prediction;
- classification as a decision boundary;
- SVM as margin-based separation;
- clustering as groups of nearby points.

---

## Final Course Strategy

The final project should tell one coherent story:

```text
Cane Corso growth is represented mathematically.
Regression estimates expected development.
Classification gives probability-based growth signals.
Clustering discovers hidden growth profiles.
Feature engineering and time series turn raw records into trajectory features.
Dimensionality reduction visualizes the structure.
MLflow tracks the experiments professionally.
```

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
| Unsupervised Learning, Clustering | Completed | unknown growth-pattern groups and exploratory outlier/noise detection |
| Feature Engineering and Time Series | Completed | growth ratios, velocity, lag features and trajectory over time |
| Dimensionality Reduction | Planned next | 2D visualization of high-dimensional growth profiles |
| MLflow | Planned | experiment tracking and model comparison |
| Computer Vision Visual Similarity | Planned / documented | future image-based visual similarity, not breed proof |
| Image Dataset Feasibility | Completed as Step 12 plan | public dataset candidates and target molossoid class planning before training |
| Image Dataset Acquisition and Local Preparation | Completed as Step 13 plan | local-only image dataset folder structure, inventory template and validation before training |

---

## Concept and Mathematical Framing

Files:

```text
PROJECT_BRIEF.md
README.md
docs/product_idea_and_mathematical_framing.md
docs/model_learning_explanation.md
docs/growth_monitoring_motivation.md
notebooks/00_project_concept_and_mathematical_framing.ipynb
```

Purpose:

- explain the project as a useful product idea, not only a homework task;
- explain why large-breed growth monitoring is a meaningful motivation;
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

### 11. Course Coverage Alignment Additions

Step 08 strengthens this notebook with:

- a dedicated Ordinary Least Squares simulated example;
- a real-data regression section using `data/processed/dog_growth_public_sample.csv`;
- a simple real-data model and a multi-feature real-data model.

This makes the notebook map more directly to the lecture requirements for OLS, simulated examples, real-data implementation, model testing, extensions, regularization and robust regression.

Status:

```text
Linear Regression, Regularization and Testing ✅ strengthened in Step 08
```

---

## Data Source Selection Rationale

Covered in:

```text
DATA_SOURCES.md
docs/real_data_source_notes.md
docs/dataset_selection_rationale.md
```

The project documents why the University of Liverpool DataCat / PLOS ONE dog growth dataset was selected instead of a generic dog-related Kaggle dataset.

Reason:

```text
The selected public source is directly connected to age, bodyweight and growth monitoring, while many general dog datasets are designed for different tasks such as images, breed descriptions or synthetic wellness examples.
```

Status:

```text
Dataset selection rationale ✅
```

---

# Real Data Foundation

Files:

```text
DATA_SOURCES.md
docs/real_data_source_notes.md
docs/real_data_download_instructions.md
docs/raw_dataset_archive_policy.md
docs/dataset_selection_rationale.md
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

The original public dataset is kept local only as a raw dataset archive in `data/raw/` and should not be committed to GitHub or included in the final clean project submission. The notebooks use processed CSV samples from `data/processed/`.

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

### 2. Binary / Multiclass / Multilabel Classification

Covered in:

- `Create Classification Target` section
- `Classification Types and Use Cases` section

The current notebook uses binary classification and explains how the same project could later grow into multiclass or multilabel classification.

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

### 6. ROC Curve, Precision-Recall Curve and Thresholds

Covered in:

- ROC/AUC section
- Precision-Recall Curve section
- Threshold comparison table

This evaluates probability separation and explains how different decision thresholds change precision, recall and F1-score.

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

### 10. Basic Tuning

Covered in:

- `Basic Hyperparameter Tuning` section

The notebook uses `GridSearchCV` to tune Logistic Regression regularization strength.

### 11. Drift and Monitoring

Covered in:

- `Drift and Monitoring Considerations` section

The notebook explains why future owner records may differ from the training data and adds a basic distribution monitoring check.

### 12. Final Model Comparison

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
Classification ✅ strengthened in Step 08
```

---

# Topic 3: Unsupervised Learning and Clustering

Notebook:

```text
notebooks/04_unsupervised_learning_clustering.ipynb
```

Supporting explanation:

```text
docs/clustering_learning_notes.md
docs/math_foundation.md
docs/geometric_interpretation.md
```

The notebook follows the Unsupervised Learning and Clustering lecture and applies it to the processed real public dog growth sample.

Data used:

```text
data/processed/dog_growth_public_sample.csv
```

## Topic Coverage

### 1. Unsupervised Learning Problem Statement, Intuition and Challenges

Covered in:

- notebook introduction;
- mathematical formulation section;
- `docs/clustering_learning_notes.md`.

Project interpretation:

```text
discover similar growth-pattern groups without using a target label
```

### 2. K-Means Clustering Motivation, Example and k-means++

Covered in:

- K-Means section;
- `KMeans(init="k-means++")` implementation;
- elbow check;
- silhouette score check;
- PCA visualization of K-Means groups.

K-Means objective:

```text
minimize within-cluster squared distance
```

### 3. Hierarchical Clustering Motivation and Example

Covered in:

- Hierarchical Clustering section;
- `AgglomerativeClustering(linkage="ward")` implementation;
- cluster summary;
- PCA visualization of hierarchical groups.

### 4. Comparison Between K-Means and Hierarchical Clustering

Covered in:

- comparison table using Silhouette and Davies-Bouldin scores;
- pros and cons table in the notebook;
- responsible interpretation notes.

### 5. DBSCAN

Covered in:

- DBSCAN section;
- k-distance check;
- `DBSCAN(eps=..., min_samples=...)` implementation;
- noise-rate output;
- PCA visualization with `-1 = noise`.

Project interpretation:

```text
DBSCAN noise points are exploratory records that do not fit dense mathematical groups.
```

They are not diagnoses.

Status:

```text
Unsupervised Learning and Clustering ✅ completed in Step 09
```

### Step 09.1 Mathematical Application Polish

Step 09.1 strengthens the clustering topic for a math-focused final project.

Added emphasis:

- real-world application question;
- feature-vector definition `x_i`;
- K-Means assignment and objective formulas;
- Hierarchical Clustering and Ward linkage interpretation;
- DBSCAN density/noise interpretation;
- safe product wording for growth-profile hints.

Status:

```text
Clustering mathematical application bridge ✅ strengthened in Step 09.1
```

### Step 09.2 Exact Lesson Alignment

Step 09.2 aligns the notebook more closely with the exact lecture PDF structure.

Added coverage:

- k-Nearest Neighbors as a distance-based lazy learner;
- Minkowski / Euclidean distance explanation;
- educational kNN classification example;
- synthetic blobs, moons and circles examples;
- K-Means random initialization vs K-Means++ comparison context;
- silhouette samples graphical check;
- hierarchical dendrogram visualization;
- clustering vs classification comparison using Adjusted Rand Index.

Status:

```text
Unsupervised Learning and Clustering ✅ aligned with exact lecture structure in Step 09.2
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

# Topic 3 Follow-up: Clustering Application Polish

Completed notebook:

```text
notebooks/04_unsupervised_learning_clustering.ipynb
```

Mathematical role:

```text
discover growth-pattern groups without using target labels
```

Strengthened coverage:

- unsupervised learning problem statement
- feature scaling
- K-Means
- K-Means++ motivation
- Elbow Method
- Silhouette Score
- Hierarchical Clustering
- DBSCAN
- cluster interpretation

Product interpretation:

```text
This dog record resembles a steady-growth / fast-growth / slow-growth / irregular-growth group.
```

Status:

```text
Unsupervised Learning, Clustering ✅ strengthened in Step 09.1
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
Feature Engineering and Time Series ✅ + Practical Workflow ✅
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

# Applied Step 12: Public Image Dataset Feasibility

Files:

```text
docs/image_dataset_feasibility.md
data/image_dataset_feasibility_matrix.csv
data/molossoid_visual_target_classes.csv
src/validate_image_dataset_feasibility.py
notebooks/07_image_dataset_feasibility.ipynb
```

Course/project connection:

```text
Future Computer Vision -> responsible dataset feasibility before model training
```

Functional role:

```text
public dataset candidates + target visual classes + data rules -> safe image-model preparation
```

Responsible boundary:

```text
No image scraping, no committed image archives, no breed-proof claim from images.
```

Status:

```text
Public Image Dataset Feasibility ✅
```

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
A future Computer Vision extension can add image-based visual similarity probabilities, clearly separated from breed proof or certification. Step 12 adds the required public image dataset feasibility layer before any visual model is trained.
```

---

# Applied Step 10.1: Practical Growth Assessment Workflow

Files:

```text
notebooks/05_1_practical_growth_assessment_workflow.ipynb
src/run_growth_assessment.py
data/input/example_new_cane_corso_measurements.csv
reports/example_growth_assessment_report.md
```

Course connection:

```text
Feature Engineering and Time Series -> applied assessment workflow
```

Mathematical interpretation:

```text
weight_gain(t) = weight(t) - weight(t-1)
growth_velocity(t) = weight_gain(t) / delta_age(t)
z = (latest_velocity - reference_mean_velocity) / reference_standard_deviation
distance = sqrt(sum((x_latest_scaled - x_reference_scaled)^2))
```

Functional role:

```text
new measurement records -> engineered features -> practical educational report
```

Status:

```text
Practical Growth Assessment Workflow ✅
```

---

# Applied Step 11: Computer Vision Visual Similarity Plan

Files:

```text
docs/computer_vision_visual_similarity_plan.md
docs/image_dataset_research_plan.md
data/image_dataset_manifest_example.csv
data/images/README.md
src/validate_image_manifest.py
notebooks/06_computer_vision_visual_similarity_concept.ipynb
```

Course/project connection:

```text
Future Computer Vision / Image Classification extension
```

Mathematical interpretation:

```text
h = phi(X_image)
z = W h + b
p_i = exp(z_i) / sum(exp(z_j))
```

Functional role:

```text
dog image -> visual feature extractor -> breed-similarity probability distribution -> responsible interpretation
```

Responsible boundary:

```text
Visual similarity is not breed proof, pedigree proof, genetic testing, registry authority or veterinary diagnosis.
```

Status:

```text
Computer Vision Visual Similarity Plan ✅
```


---

## Image Dataset Acquisition and Local Preparation

Covered in:

```text
docs/image_dataset_acquisition_and_local_preparation.md
data/image_dataset_local_inventory_template.csv
notebooks/08_image_dataset_acquisition_local_preparation.ipynb
src/prepare_image_dataset_structure.py
src/validate_local_image_dataset.py
```

Step 13 prepares the project for future Computer Vision work by adding a local-only image dataset structure and validation workflow. It keeps downloaded public datasets and consent-based images out of GitHub while preserving reproducible instructions and metadata templates.

Status:

```text
Image Dataset Acquisition and Local Preparation ✅ planned / structure-only
```

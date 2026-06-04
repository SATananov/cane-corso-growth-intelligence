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

The project currently contains eleven notebooks.

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


### Feature Engineering and Time Series Topic

```text
notebooks/05_feature_engineering_time_series_growth.ipynb
```

This notebook covers:

- feature engineering problem statement;
- ordered growth records as a simple time series;
- lag features from previous measurements;
- weight gain and height gain;
- growth velocity per month;
- weight-to-height ratio;
- rolling average smoothing;
- z-score growth velocity signal;
- engineered feature correlation check;
- responsible interpretation for Cane Corso growth monitoring.

It also creates:

```text
data/processed/cane_corso_time_series_features.csv
```



### Computer Vision Visual Similarity Concept

```text
notebooks/08_computer_vision_visual_similarity_concept.ipynb
```

This notebook does not train a real image model yet. It explains the future Computer Vision extension, softmax probability interpretation, dataset feasibility, and the responsible boundary: visual similarity is not breed proof.


### Public Image Dataset Feasibility

```text
notebooks/09_image_dataset_feasibility.ipynb
```

This notebook reviews public image dataset candidates before any Computer Vision model is trained. It reads the feasibility matrix and target-class plan from CSV files and validates that the project remains a visual-similarity plan, not breed proof.

### Image Dataset Acquisition and Local Preparation

```text
notebooks/10_image_dataset_acquisition_local_preparation.ipynb
```

This notebook documents the local-only data acquisition workflow for the future Computer Vision module. It does not train an image model. It explains where local images would be stored, how class folders are prepared, and why downloaded images should remain outside Git history.

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

The selected real public source is the University of Liverpool DataCat / PLOS ONE dog growth dataset. Kaggle was considered as a useful dataset-search idea, but the selected source is more directly connected to age/bodyweight growth monitoring.

Read the data-source explanation here:

```text
docs/dataset_selection_rationale.md
```

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
src/create_time_series_features.py
src/run_growth_assessment.py
src/validate_image_manifest.py
src/validate_image_dataset_feasibility.py
src/prepare_image_dataset_structure.py
src/validate_local_image_dataset.py
```

The Step 12 dataset-feasibility validation script can be run with:

```powershell
python src/validate_image_dataset_feasibility.py
src/prepare_image_dataset_structure.py
src/validate_local_image_dataset.py
```

It validates the public dataset feasibility matrix, the target molossoid class plan, and confirms that no downloaded image files are committed under `data/images/`.

The image manifest validation script can be run with:

```powershell
python src/validate_image_manifest.py
```

It validates the structure of the example image manifest only. It does not download images or train an image model.


The Step 13 local image dataset preparation script can be run with:

```powershell
python src/prepare_image_dataset_structure.py
```

It creates the ignored local folder structure under:

```text
data/images/local_dataset/
```

Validate the local structure with:

```powershell
python src/validate_local_image_dataset.py
```

This validation allows zero images at Step 13. It checks folder structure and metadata templates only.

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

The project currently covers four completed course topics plus one future Computer Vision extension plan:

1. Linear Regression, Regularization and Testing
2. Classification
3. Unsupervised Learning and Clustering
4. Feature Engineering and Time Series
5. Computer Vision Visual Similarity Plan (concept and feasibility, not trained yet)
6. Public Image Dataset Feasibility (dataset candidates and target class planning, not trained yet)
7. Image Dataset Acquisition and Local Preparation (local-only structure and validation, not trained yet)

It also includes a Real Data Foundation stage with processed samples from a real public dog growth dataset and a dataset-selection rationale explaining why this source was chosen instead of a generic Kaggle dataset.

The next planned core course topic is:

```text
Dimensionality Reduction
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

## 11. Run the practical growth assessment workflow

Step 10.1 adds an applied workflow that turns example owner-style measurements into a readable educational report.

Input:

```text
data/input/example_new_cane_corso_measurements.csv
```

Run from the project root:

```powershell
& ".\.venv\Scripts\python.exe" ".\src\run_growth_assessment.py"
```

Expected outputs:

```text
data/processed/example_growth_assessment_features.csv
reports/example_growth_assessment_report.md
reports/figures/practical_growth_assessment_weight_trend.png
reports/figures/practical_growth_assessment_velocity_signal.png
```

Optional notebook walkthrough:

```text
notebooks/05_1_practical_growth_assessment_workflow.ipynb
```

This step demonstrates practical applicability while keeping the project educational and mathematically transparent.


### Local Stanford Dogs Inspection / Baseline Class Selection

```text
notebooks/13_local_stanford_dogs_inspection_baseline_class_selection.ipynb
```

This notebook documents the local inspection and first-baseline class selection workflow for Stanford Dogs.

Useful commands:

```bash
python src/select_stanford_dogs_baseline_classes.py
python src/validate_stanford_baseline_class_selection.py
```

Before the dataset is downloaded locally, zero confirmed classes is acceptable. The purpose is to keep class selection evidence-based before any image model is trained.


## Step 17 — Stanford Dogs Local Download / Real Class Inspection

Safe checks without downloading large files:

```bash
python src/download_stanford_dogs_local_dataset.py
python src/inspect_stanford_dogs_real_classes.py
python src/validate_stanford_dogs_real_inspection.py
python src/select_stanford_dogs_baseline_classes.py
python src/validate_stanford_baseline_class_selection.py
```

Optional real local download when ready:

```bash
python src/download_stanford_dogs_local_dataset.py --download-small
python src/download_stanford_dogs_local_dataset.py --download-images
python src/download_stanford_dogs_local_dataset.py --extract-images
python src/inspect_stanford_dogs_real_classes.py
python src/select_stanford_dogs_baseline_classes.py
```

Do not commit downloaded images, archives or extracted dataset folders.


### Future Course Topic Notebooks

These notebooks are intentionally reserved and should be completed after the course topics are covered:

```text
notebooks/06_dimensionality_reduction_future_course_topic.ipynb
notebooks/07_mlflow_future_course_topic.ipynb
```


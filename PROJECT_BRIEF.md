# Project Brief

## Project Title

**Cane Corso Growth Intelligence**

## Project Subtitle

**A Mathematical Growth Profiling System for Predictive Monitoring and Early Growth Pattern Detection**

---

## Main Idea

Cane Corso Growth Intelligence is a machine learning project that explores how simple dog growth records can be transformed into useful mathematical and visual insights.

The project starts from a practical everyday question:

```text
How can an owner understand whether a growing Cane Corso is developing close to an expected pattern?
```

Instead of treating the project as only a weight-prediction exercise, the stronger idea is to build a **mathematical growth profile**. Each measurement becomes a data point. Each dog can be interpreted as a growth trajectory over time. Machine learning models are then used to estimate expected growth, classify growth signals, discover similar growth groups, and explain model behavior through metrics and visualizations.

This makes the project both interesting and useful:

- interesting, because it connects real-world growth monitoring with mathematical modeling;
- useful, because the same idea can later become an owner-friendly growth monitor;
- academically relevant, because it applies multiple machine-learning topics from the course in one coherent domain.


## Scope in Relation to the Course

The main project is the tabular Cane Corso growth-intelligence workflow. It is aligned with the completed course-topic sequence represented in the project: regression, classification, unsupervised learning / clustering, feature engineering, time-series features, dimensionality reduction, Machine Learning Tools, data processing, model evaluation, and careful interpretation of results.

Dimensionality Reduction and Machine Learning Tools are completed course-aligned additions. They were implemented after the related lectures and exercises were covered, so the project continues to follow the real course path.

The image-based work is included only as an **exploratory extension**. It investigates whether a small public dog-image dataset can support a simple visual-similarity comparison between available large-dog classes. This part should not be presented as a core course requirement, a breed detector, a pedigree tool, or a Cane Corso certification system.

The final results and figures summary is prepared as part of the completed course-aligned project, including Dimensionality Reduction and Machine Learning Tools.

---

## Real-World Motivation

Large-breed puppies grow quickly. Owners often track weight, age and body measurements, but raw numbers are difficult to interpret without context.

This matters because rapid growth and excessive weight gain in large and giant breeds can increase mechanical stress on the developing bones and joints. The project therefore does not treat weight as an isolated number. It treats weight, age and repeated measurements as part of a growth trajectory that should be monitored carefully over time.

The project keeps this motivation responsible: it does not diagnose joint disease, organ disease or any medical condition. It produces an educational monitoring signal that can support better observation and, when appropriate, professional consultation.

A single record such as:

```text
age = 5 months, weight = 28 kg
```

does not answer the important questions:

```text
Is this close to expected development?
Is the dog growing faster or slower than similar dogs?
Is the trend stable over time?
Does the record need closer attention?
How confident is the model?
```

The project uses machine learning to convert these questions into measurable tasks.

A dedicated background note for this motivation is available in:

```text
docs/growth_monitoring_motivation.md
```

---

## Product-Oriented Use Case

A possible real user flow is:

```text
1. The owner enters age, weight, sex, height and optional growth information.
2. The system creates a mathematical feature vector.
3. Regression estimates expected weight or growth trend.
4. Classification gives a probability-based growth signal.
5. Clustering compares the record with similar growth patterns.
6. Visualizations explain the result using charts, residuals and metrics.
7. The owner sees a clear, non-medical monitoring signal.
```

The project should not be presented as a veterinary diagnostic system. The correct product framing is:

```text
owner-friendly growth monitoring system
```

not:

```text
medical diagnosis tool
```

---

## Mathematical Problem Formulation

Each growth record is represented as a vector:

```text
x = [age_months, weight_kg, height_cm, sex_encoded, body_ratio, growth_velocity, deviation_from_expected]
```

Depending on the lecture topic, the same data can be used for different tasks.

### Regression

Regression learns a function:

```text
y_weight = f(x)
```

The goal is to estimate a numerical target such as expected bodyweight.

### Classification

Classification learns a probability:

```text
P(needs_attention | x)
```

The model output is a probability-based signal, not a medical conclusion.

### Clustering

Clustering searches for hidden groups:

```text
cluster_id = g(x)
```

The goal is to discover unknown growth-pattern profiles without using predefined labels.

### Time Series

A dog can be represented as an ordered trajectory:

```text
trajectory = [(age_1, weight_1), (age_2, weight_2), ..., (age_n, weight_n)]
```

This allows later analysis of trend, velocity, moving averages and deviations over time.

---

## How the Model Learns

The project must clearly explain that a machine-learning model learns from historical records.

The process is:

```text
known examples -> prediction -> error -> parameter update -> evaluation on unseen data
```

For regression, the model compares predicted weight with real weight:

```text
residual_i = y_i - y_hat_i
```

Training means finding model parameters that reduce the total error, for example:

```text
minimize sum((y_i - y_hat_i)^2)
```

For classification, the model estimates a probability:

```text
p = P(needs_attention | x)
```

Then a threshold converts the probability into a class:

```text
if p >= threshold -> needs_attention
else -> normal_growth
```

This allows threshold discussion, precision/recall trade-off, ROC/AUC analysis and responsible interpretation.

A dedicated explanation is added in:

```text
docs/model_learning_explanation.md
```

---

## Data Foundation

The project uses two clearly separated data layers.

### 1. Prototype Cane Corso Dataset

```text
data/prototype/cane_corso_growth_sample.csv
```

This is a small educational sample used at the beginning of the project.

### 2. Real Public Dog Growth Dataset

The stronger data foundation comes from a public research dataset:

```text
Growth standard charts for monitoring bodyweight in dogs of different sizes - SUPPORTING DATA
```

Source:

```text
University of Liverpool DataCat
```

Related publication:

```text
Growth standard charts for monitoring bodyweight in dogs of different sizes, PLOS ONE, 2017
```

Important clarification:

```text
The project does not claim to have private Cane Corso veterinary records.
The Cane Corso domain is the practical product context.
The real public dog growth dataset provides the broader data foundation.
```

Processed samples:

```text
data/processed/dog_growth_public_sample.csv
data/processed/dog_growth_classification_sample.csv
```

The original public source distributes its full data as a compressed raw dataset archive. That archive is kept local and is not part of the committed project. The notebooks use the processed CSV samples above.

---

## Completed Stage 1: Regression

Course topic:

```text
Linear Regression, Regularization and Testing
```

Notebook:

```text
notebooks/01_linear_regression_growth_prediction.ipynb
```

Covered methods:

- simple linear regression
- polynomial regression
- multi-dimensional linear regression
- Ridge regression
- Lasso regression
- RANSAC robust regression
- MAE, MSE, RMSE, R2
- regression model comparison

The mathematical interpretation is:

```text
learn an expected growth function and analyze residual errors
```

---

## Completed Stage 2: Real Data Foundation

Notebook:

```text
notebooks/02_real_data_preparation.ipynb
```

Scripts:

```text
src/create_public_sample.py
src/create_classification_sample.py
```

This stage moves the project from a small prototype sample toward processed real public dog growth data.

---

## Completed Stage 3: Classification

Course topic:

```text
Classification
```

Notebook:

```text
notebooks/03_classification_growth_status.ipynb
```

Classification target:

```text
growth_status
```

Classes:

```text
normal_growth
needs_attention
```

Covered methods and evaluation:

- Logistic Regression
- Decision Tree
- Random Forest
- AdaBoost
- Support Vector Machine
- confusion matrix
- accuracy, precision, recall, F1-score
- ROC curve and AUC
- model comparison

The mathematical interpretation is:

```text
learn a decision boundary and estimate P(needs_attention | x)
```

---

## Classification Pipeline Extension

Notebook:

```text
notebooks/03_1_classification_pipeline_exercise.ipynb
```

This extension improves the project because it shows professional workflow:

- dummy baselines
- preprocessing pipeline
- train/test split
- stratified cross-validation
- learning curve
- feature engineering
- model comparison
- permutation importance
- error analysis
- ablation study

This helps show that the project is not only model fitting, but also method validation.

---

## Completed Stage 4: Unsupervised Learning and Clustering

Course topic:

```text
Unsupervised Learning, Clustering
```

Notebook:

```text
notebooks/04_unsupervised_learning_clustering.ipynb
```

Completed goal:

```text
Discover natural growth-pattern groups in the processed public dog growth data.
```

Covered methods:

- K-Means
- K-Means++
- Elbow Method
- Silhouette Score
- Hierarchical Clustering
- DBSCAN
- cluster interpretation

---

## What Should Impress the Examiner

The project should emphasize these strengths:

1. clear real-world problem formulation;
2. correct mathematical translation into vectors, functions, probabilities and metrics;
3. model learning explanation, not only library usage;
4. residual analysis and error interpretation;
5. probability and threshold discussion for classification;
6. feature engineering based on growth logic;
7. completed clustering and dimensionality reduction as mathematical structure discovery;
8. responsible interpretation and clear limitations;
9. reproducible notebooks and documented data sources;
10. a responsible Computer Vision extension plan that does not confuse visual similarity with breed proof.

---


## Optional Exploratory Visual Similarity Extension

The project includes an optional exploratory visual-similarity extension called a **visual similarity classifier**.

This future module would analyze a dog image and return probabilities over trained visual classes, for example:

```text
Cane Corso: 65%
Dogo Argentino: 15%
Presa Canario: 12%
Great Dane: 8%
```

The correct interpretation is visual similarity among trained classes, not official breed identification.

This combines naturally with the existing project:

```text
growth records -> growth monitoring signal
image -> visual similarity signal
combined report -> educational interpretation with limitations
```

The project does not currently have a private image dataset, so this stage documents public dataset research and a manifest-based data plan instead of training a fake model.

Supporting files:

```text
docs/computer_vision_visual_similarity_plan.md
docs/image_dataset_research_plan.md
notebooks/08_computer_vision_visual_similarity_concept.ipynb
```

---

## Visual Dataset Feasibility for the Exploratory Extension

The project now includes a optional visual-similarity direction for molossoid visual similarity, but image model training is intentionally postponed until the dataset question is handled responsibly.

this stage adds a feasibility matrix for public dog image datasets and a target-class plan for Cane Corso and related molossoid breeds. It also states that large image folders should remain local and that the project should not scrape social media or random web images without permission.

Supporting files:

```text
docs/image_dataset_feasibility.md
data/image_dataset_feasibility_matrix.csv
data/molossoid_visual_target_classes.csv
notebooks/09_image_dataset_feasibility.ipynb
src/validate_image_dataset_feasibility.py
```


## Image Dataset Acquisition and Local Preparation

this stage adds the practical local-data workflow needed before future visual-similarity training.

Supporting files:

```text
docs/image_dataset_acquisition_and_local_preparation.md
data/image_dataset_local_inventory_template.csv
notebooks/10_image_dataset_acquisition_local_preparation.ipynb
src/prepare_image_dataset_structure.py
src/validate_local_image_dataset.py
```

This stage prepares ignored local folders under:

```text
data/images/local_dataset/
```

It does not download image datasets, commit photos, train a visual model, or claim breed proof. It only prepares the project for responsible future image experiments.

---

## Limitations and Safety Boundary

The project is educational and analytical.

It should not be used as:

- veterinary diagnosis;
- health decision system;
- official breed verification;
- pedigree or certification authority.

Correct interpretation:

```text
The output is a machine-learning growth-monitoring signal that can support observation and learning.
```

Incorrect interpretation:

```text
The output proves a medical condition or replaces expert judgment.
```


## Notebook Mathematical Formulation Rule

Every notebook in the project should include a clear mathematical formulation section before the main modelling work. The required structure is:

```text
Input vector X
Target y
Model function f(x)
Loss function
Metrics
Interpretation
Limitations
```

This turns each lecture from a code exercise into a mathematically explained modelling stage. It also makes the project easier to defend, because every method is connected to a precise input, objective, evaluation metric, and responsible interpretation.

---



## Dataset Selection Rationale

The selected real public data source is documented in `docs/dataset_selection_rationale.md`. Kaggle was considered as a general dataset-search option, but the University of Liverpool DataCat / PLOS ONE dog growth dataset was selected because it is more directly connected to age/bodyweight growth monitoring.


## First Public Image Dataset Candidate

The project now has a documented first public image dataset candidate for the future visual-similarity module.

The candidate is Stanford Dogs / ImageNet Dogs, used only as a public baseline candidate. this stage does not train a visual-similarity model. It prepares the responsible data-acquisition plan and local inspection flow.

This supports the long-term direction:

```text
growth intelligence from tabular measurements + visual similarity from images
```

The visual result must remain educational and probabilistic. It should never be presented as breed proof, pedigree proof, registry proof or veterinary diagnosis.


## Evidence-Based Visual Class Selection

The project now includes a local class-selection workflow for the first public image dataset candidate.

This protects the Computer Vision extension from overstating what the dataset can support. A future image classifier can only return probabilities for classes included in its training labels.

Therefore, Cane Corso-specific visual recognition remains future work unless a verified public dataset or consent-based USG dataset provides confirmed Cane Corso images.


## Exploratory Computer Vision Data Inspection Extension

The project includes a local inspection workflow for Stanford Dogs / ImageNet Dogs. This supports a possible future visual-similarity classifier by verifying real local class folders before any image model training.

This extension strengthens the project methodology because it separates desired classes from available labels and keeps the visual module honest and evidence-based. It is included as preparation for possible later integration into the planned USG Cane Corso platform ecosystem, not as the main exam deliverable, breed proof, certification logic, registry logic, or veterinary logic.


## Completed Course-Aligned Notebooks

Dimensionality Reduction and Machine Learning Tools are completed course-aligned topics. Their notebooks are now implemented and documented in the project repository. Some legacy notebook filenames are preserved to keep the progressive course-development history traceable.

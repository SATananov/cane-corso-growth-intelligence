# Patch Report - Step 08: Course Coverage Alignment

## Purpose

This patch strengthens the project against the visible course requirements for:

1. Linear Regression, Regularization and Testing
2. Classification

The project already had strong coverage. This patch makes the mapping clearer and adds the missing or partially covered lecture points.

## Changed Files

```text
COURSE_TOPIC_MAPPING.md
HOW_TO_RUN.md
README.md
notebooks/01_linear_regression_growth_prediction.ipynb
notebooks/03_classification_growth_status.ipynb
PATCH_REPORT_STEP08_COURSE_COVERAGE_ALIGNMENT.md
```

## Regression Additions

Added to `notebooks/01_linear_regression_growth_prediction.ipynb`:

- dedicated Ordinary Least Squares simulated example;
- OLS fitted-line visualization;
- real-data regression section using `data/processed/dog_growth_public_sample.csv`;
- simple real-data linear regression;
- multi-feature real-data linear regression;
- real-data model comparison and interpretation.

This strengthens coverage for:

- Regression problem statement and motivation;
- Ordinary Least Squares method;
- simulated example;
- implementation on real data;
- model testing.

The notebook already covered:

- Polynomial Regression;
- Multi-Dimensional Linear Regression;
- Ridge and Lasso Regularization;
- RANSAC Robust Regression;
- regression metrics and model comparison.

## Classification Additions

Added to `notebooks/03_classification_growth_status.ipynb`:

- Binary / Multiclass / Multilabel classification explanation;
- Precision-Recall Curve;
- threshold comparison table;
- basic hyperparameter tuning with `GridSearchCV`;
- drift and monitoring considerations;
- simple distribution-monitoring check.

This strengthens coverage for:

- classification types and use cases;
- Logistic Regression threshold behavior;
- Precision / Recall / F1 interpretation;
- ROC/PR evaluation;
- tuning;
- interpretability and responsible drift monitoring.

The notebook already covered:

- Logistic Regression;
- train/test split;
- encoding and scaling;
- class imbalance awareness;
- Decision Tree;
- Random Forest and AdaBoost;
- Support Vector Machine;
- confusion matrix;
- accuracy, precision, recall, F1-score and AUC.

## Documentation Additions

Updated:

- `COURSE_TOPIC_MAPPING.md` with stronger topic-by-topic mapping;
- `HOW_TO_RUN.md` with the correct notebook count and the new coverage sections;
- `README.md` with recommended review order and Step 08 status.

## Safety and Scope

This patch does not change the processed datasets.

It does not claim veterinary diagnosis, medical advice, breed certification or pedigree proof.

The project remains an educational machine learning project for responsible growth-monitoring analysis.

## Suggested Local Verification

After applying the patch, run the notebooks in this order:

```text
notebooks/00_project_concept_and_mathematical_framing.ipynb
notebooks/01_linear_regression_growth_prediction.ipynb
notebooks/02_real_data_preparation.ipynb
notebooks/03_classification_growth_status.ipynb
notebooks/03_1_classification_pipeline_exercise.ipynb
```

Recommended local checks:

```powershell
python -m pip install -r requirements.txt
jupyter notebook
```

Then use `Restart Kernel and Run All` for the changed notebooks.

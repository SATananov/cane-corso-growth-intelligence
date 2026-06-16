# Step 21 Machine Learning Tools Report

This report applies the **Machine Learning Tools** exercise ideas to the Cane Corso Growth Intelligence project.

## What this step covers

- reusable script entry point: `python app.py --config configs/machine_learning_tools_config.json`
- JSON configuration for data, feature columns, vectorizer settings, dimensionality reduction and models
- comparison of sparse TF-IDF text representation vs dense TF-IDF + TruncatedSVD representation
- comparison of fixed metadata pipelines with Logistic Regression and Random Forest classifiers
- MLflow-compatible experiment tracking, with automatic MLflow logging when `mlflow` is installed
- DVC stage definition in `dvc.yaml`
- saved best pipeline with `joblib`
- smoke test for saved-model loading and prediction
- model card and inspected examples

## Best experiment

```text
text_tfidf_sparse_logistic
```

## Results

| experiment                    |   accuracy |   precision |   recall |       f1 |   roc_auc |   train_rows |   test_rows |
|:------------------------------|-----------:|------------:|---------:|---------:|----------:|-------------:|------------:|
| text_tfidf_sparse_logistic    |     1      |    1        | 1        | 1        |  1        |         3750 |        1250 |
| metadata_logistic_regression  |     1      |    1        | 1        | 1        |  1        |         3750 |        1250 |
| metadata_random_forest        |     1      |    1        | 1        | 1        |  1        |         3750 |        1250 |
| text_tfidf_svd_dense_logistic |     0.9984 |    0.998358 | 0.998358 | 0.998358 |  0.999959 |         3750 |        1250 |

## MLflow tracking status

```json
{
  "enabled": false,
  "reason": "mlflow_not_available: No module named 'mlflow'"
}
```

## Responsible-use note

The target is an educational binary growth-monitoring signal from a processed public dog-growth sample. It is not a veterinary diagnosis. Outputs are intended for course learning, reproducibility, model comparison and responsible monitoring.

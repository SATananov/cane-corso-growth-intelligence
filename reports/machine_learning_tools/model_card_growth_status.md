# Model Card — Cane Corso Growth Status Pipeline

## Model overview

This model is the best-performing pipeline selected during Step 21 Machine Learning Tools alignment.

```text
Best pipeline: text_tfidf_sparse_logistic
Saved model: models/machine_learning_tools/best_growth_status_pipeline.joblib
```

## Intended use

The model is intended for educational growth-monitoring experiments. It predicts a binary proxy signal:

- `0` = normal growth pattern in the processed sample
- `1` = needs-attention growth signal in the processed sample

It can support learning, comparison of ML pipelines, reproducibility practice and responsible exploration of growth records.

## Not intended use

The model must not be used as veterinary diagnosis, medical advice, breed certification, pedigree proof, or a replacement for professional evaluation.

## Data

The pipeline uses the committed processed dataset:

```text
data/processed/dog_growth_classification_sample.csv
```

Real image datasets remain optional and local-only. This Step 21 pipeline does not require them.

## Approach

The Step 21 run compares:

- sparse TF-IDF text representation built from structured growth records;
- dense TF-IDF + TruncatedSVD representation;
- metadata Logistic Regression pipeline;
- metadata Random Forest pipeline.

The best model is selected by F1 score, with ROC-AUC kept as a secondary metric.

## Metrics

| experiment                    |   accuracy |   precision |   recall |       f1 |   roc_auc |   train_rows |   test_rows |
|:------------------------------|-----------:|------------:|---------:|---------:|----------:|-------------:|------------:|
| text_tfidf_sparse_logistic    |     1      |    1        | 1        | 1        |  1        |         3750 |        1250 |
| metadata_logistic_regression  |     1      |    1        | 1        | 1        |  1        |         3750 |        1250 |
| metadata_random_forest        |     1      |    1        | 1        | 1        |  1        |         3750 |        1250 |
| text_tfidf_svd_dense_logistic |     0.9984 |    0.998358 | 0.998358 | 0.998358 |  0.999959 |         3750 |        1250 |

## Tradeoffs

Text-style representations are useful for demonstrating the exercise idea of comparing sparse and dense text pipelines. Metadata pipelines are usually more natural for this project because the core data is structured: age, weight, body-condition labels and visit context.

## Limitations

- The label is a course-aligned proxy signal, not a medical truth.
- The dataset is processed and limited to the available public sample.
- Performance may change when the data distribution changes.
- The model should be monitored and re-evaluated before any real-world use.

## Inspected examples

The file `reports/machine_learning_tools/inspected_examples.csv` contains correct, incorrect and uncertain examples, where available.

## Usability

Run the workflow with:

```bash
python app.py --config configs/machine_learning_tools_config.json
```

Run the smoke test with:

```bash
python tests/smoke_test_machine_learning_tools.py
```

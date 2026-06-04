# Linear Regression Testing Exercise Alignment Summary

This report validates that the project follows the main workflow from the course exercise on linear regression, regularization, and testing.

## Dataset

- Source file: `data/prototype/cane_corso_growth_sample.csv`
- Rows: 32
- Target: `weight_kg`
- Main project interpretation: educational growth-weight prediction, not veterinary advice.

## Exercise coverage

- Exercise requirements checked: 10
- Coverage status counts: {'covered': 10}

## Model comparison

| model                      |    mae |   rmse |     r2 |   best_alpha |   cv_rmse |
|:---------------------------|-------:|-------:|-------:|-------------:|----------:|
| age_only_linear_regression | 4.4801 | 4.7889 | 0.8556 |        nan   |  nan      |
| enriched_linear_regression | 1.3898 | 1.821  | 0.9791 |        nan   |  nan      |
| tuned_ridge_regression     | 1.36   | 1.7574 | 0.9806 |          0.1 |    1.0583 |

## Best model by RMSE

- Model: `tuned_ridge_regression`
- MAE: 1.36
- RMSE: 1.7574
- R2: 0.9806

## Interpretation

The exercise process is represented in the project through a baseline model, changed preprocessing, model comparison, and a small hyperparameter search. The dataset is intentionally small, so the result is useful for learning and workflow demonstration, not for biological or veterinary conclusions.

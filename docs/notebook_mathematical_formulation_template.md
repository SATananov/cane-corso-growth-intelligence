# Notebook Mathematical Formulation Template

Use this section in every new notebook before the modelling code starts.

```markdown
## Mathematical Formulation

### Input vector `X`

Describe the feature matrix used by the notebook.

```text
X = [feature_1, feature_2, feature_3, ...]
```

Explain what every important feature means in the real growth-monitoring context.

### Target `y`

Describe the value the model is trying to predict or explain.

```text
y = target_column
```

For unsupervised learning, state clearly that there is no known target:

```text
No known y is used. The model searches for structure in X.
```

### Model function `f(x)`

Write the model as a mathematical mapping.

```text
Regression:      f(x) ≈ expected_weight
Classification:  f(x) = P(needs_attention | x)
Clustering:      f(x) = cluster_id
Time series:     f(x_t, history) = next_value_or_trend
```

### Loss function

State the objective or error function.

```text
Regression:      MSE = mean((y_real - y_pred)^2)
Classification:  LogLoss / Cross-Entropy
Clustering:      within-cluster distance, inertia, density separation
Dimensionality:  reconstruction error / explained variance
```

### Metrics

List the metrics used to evaluate the result.

```text
Regression:      MAE, MSE, RMSE, R²
Classification:  Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC
Clustering:      Inertia, Silhouette Score, cluster stability
Time Series:     MAE/RMSE over time, trend error, visual trajectory fit
Dimensionality:  explained variance ratio, visual separation
```

### Interpretation

Explain what the output means for the project and for an owner-friendly growth-monitoring assistant.

### Limitations

Explain what the method cannot prove, what assumptions it makes, and why the result must not be interpreted as veterinary diagnosis.
```

## Project rule

Every future notebook should include this structure:

```text
problem -> mathematical formulation -> data -> model -> metrics -> interpretation -> limitations
```

This makes the project stronger mathematically and keeps every lecture connected to the same growth-intelligence story.

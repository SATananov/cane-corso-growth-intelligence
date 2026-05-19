# How the Model Learns

This document explains the learning process behind the project models.

The purpose is to make the project clear not only as code, but also as mathematical reasoning.

---

## 1. Learning From Examples

A machine-learning model learns from known examples.

In this project, each example is a dog growth record.

A record contains input information:

```text
x = growth-related features
```

and, depending on the task, a known target:

```text
y = real weight
```

or:

```text
y = growth_status
```

The model uses historical records to learn a relationship between input features and the target.

---

## 2. General Training Flow

The training process can be summarized as:

```text
known examples -> prediction -> error -> parameter update -> evaluation on unseen data
```

The practical workflow is:

```text
1. collect records
2. clean data
3. create features
4. split into training and test sets
5. train model on training data
6. predict on unseen test data
7. calculate errors and metrics
8. compare models
9. interpret results and limitations
```

The key idea is that the model should be evaluated on data it did not use during training.

This is why train/test split and cross-validation are important.

---

## 3. Feature Matrix and Target Vector

Machine-learning libraries usually represent the data as:

```text
X = feature matrix
y = target vector
```

For example:

```text
X = [
  [age_months, weight_kg, height_cm, sex_encoded, body_ratio],
  [age_months, weight_kg, height_cm, sex_encoded, body_ratio],
  ...
]
```

For regression:

```text
y = [real_weight_1, real_weight_2, ..., real_weight_n]
```

For classification:

```text
y = [normal_growth, needs_attention, ...]
```

The model does not learn from the dog directly. It learns from this mathematical representation.

---

## 4. How Regression Learns

Regression predicts a number.

A simple linear regression model has the form:

```text
y_hat = beta_0 + beta_1*x_1 + beta_2*x_2 + ... + beta_n*x_n
```

Where:

- `y_hat` is the predicted value;
- `x_1 ... x_n` are input features;
- `beta_0 ... beta_n` are learned parameters.

The model begins with unknown parameters. During training, it chooses parameters that make predictions close to real values.

The error for one record is:

```text
error_i = y_i - y_hat_i
```

The common training objective is to minimize squared error:

```text
minimize sum((y_i - y_hat_i)^2)
```

In practical language:

```text
The model predicts weight, compares it with the real weight, and adjusts its parameters so the total error becomes smaller.
```

---

## 5. Residual Analysis

A residual is the difference between the real value and the predicted value:

```text
residual = real_weight - predicted_weight
```

Residuals are important because they show where the model is wrong.

Good questions for the project:

- Are residuals centered around zero?
- Are residuals larger for young dogs or older dogs?
- Does the model systematically overpredict or underpredict?
- Are there extreme outliers?
- Is the error acceptable for the intended educational use?

This makes regression analysis stronger than simply reporting one score.

---

## 6. How Classification Learns

Classification predicts a category.

In this project, the binary classes are:

```text
normal_growth
needs_attention
```

Logistic Regression first creates a linear score:

```text
z = beta_0 + beta_1*x_1 + beta_2*x_2 + ... + beta_n*x_n
```

Then it uses the sigmoid function:

```text
p = 1 / (1 + e^(-z))
```

The result is a probability between 0 and 1.

For the project:

```text
p = P(needs_attention | x)
```

This probability becomes a class through a threshold:

```text
if p >= 0.5:
    prediction = needs_attention
else:
    prediction = normal_growth
```

---

## 7. Thresholds and Trade-Offs

The threshold does not have to be 0.5.

For example:

```text
threshold = 0.4
```

may catch more `needs_attention` records, but may also create more false positives.

```text
threshold = 0.7
```

may reduce false positives, but may miss more records that should be reviewed.

This creates a trade-off between:

- precision;
- recall;
- false positives;
- false negatives.

For growth monitoring, recall can be important because missing a possible `needs_attention` case may be worse than asking the owner to observe more carefully.

---

## 8. Why Evaluation Metrics Matter

Different metrics answer different questions.

| Metric | Question |
|---|---|
| Accuracy | How many predictions were correct overall? |
| Precision | When the model predicts `needs_attention`, how often is it correct? |
| Recall | Of all actual `needs_attention` records, how many did the model find? |
| F1-score | What is the balance between precision and recall? |
| ROC/AUC | How well does the model separate the two classes across thresholds? |

This is why the project compares several models and metrics instead of relying on one number.

---

## 9. How Tree and Ensemble Models Learn

Decision Trees learn by splitting the feature space.

A simple split can look like:

```text
if weight_kg <= threshold:
    go left
else:
    go right
```

The tree chooses splits that reduce impurity.

Random Forest trains many trees on different bootstrap samples and combines their predictions.

AdaBoost trains weak learners sequentially and gives more importance to records that previous learners misclassified.

These models are useful because they can learn non-linear patterns and interactions between features.

---

## 10. How SVM Learns

Support Vector Machine searches for a boundary between classes.

For a linear SVM, the boundary can be written as:

```text
w^T x + b = 0
```

The model tries to maximize the margin between classes.

With an RBF kernel, SVM can model non-linear boundaries by comparing distances between points.

This is why feature scaling is important: distance-based models are sensitive to the scale of features.

---

## 11. Why Feature Engineering Helps Learning

Raw data is not always the best representation.

Feature engineering creates more meaningful mathematical inputs.

Examples:

```text
body_ratio = weight_kg / height_cm
```

```text
growth_velocity = delta_weight / delta_time
```

```text
deviation_from_expected = actual_weight - predicted_expected_weight
```

```text
relative_deviation = deviation_from_expected / predicted_expected_weight
```

These features help the model learn growth behavior more directly.

---

## 12. How the Model Would Be Used for a New Owner Record

After training, the model can be used on a new record:

```text
new_record = [age_months, weight_kg, height_cm, sex_encoded, body_ratio]
```

The system can produce:

```text
predicted_expected_weight
probability_needs_attention
growth_signal
similar_growth_group
explanation
```

A responsible output should look like:

```text
The record is close to the expected range.
Continue monitoring and compare with future measurements.
```

or:

```text
The record is outside the expected pattern in this dataset.
This is not a diagnosis, but it may be worth observing more carefully.
```

---

## 13. What the Model Does Not Learn

The model does not learn:

- veterinary diagnosis;
- official health conclusions;
- breed purity;
- pedigree truth;
- cause of a medical condition.

It only learns patterns from the available data.

This limitation is important because the project must be useful without making unsafe claims.

---

## 14. One-Sentence Summary

```text
The model learns by converting growth records into mathematical features, comparing predictions with known outcomes, minimizing error during training, and evaluating performance on unseen data.
```

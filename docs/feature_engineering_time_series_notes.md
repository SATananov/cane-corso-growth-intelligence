# Feature Engineering and Time Series Notes

This document supports the notebook:

```text
notebooks/05_feature_engineering_time_series_growth.ipynb
```

## Purpose

The goal of this stage is to show that machine learning is not only model training. Before a model is trained, raw measurements often need to be transformed into features that better describe the problem.

For Cane Corso Growth Intelligence, a single row such as:

```text
age_months, weight_kg, height_cm
```

is useful, but it does not fully describe the growth story. Growth is a process over time. Therefore this stage creates mathematical features that describe change, speed, proportion, smoothing and relative deviation.

## Learning-Oriented Mathematical Framing

A growth record for dog `i` at time step `t` can be represented as:

```text
r(i,t) = [age_months(i,t), weight_kg(i,t), height_cm(i,t)]
```

The ordered sequence of records is:

```text
r(i,1), r(i,2), ..., r(i,T)
```

Feature engineering applies a transformation:

```text
phi(r(i,t), r(i,t-1)) = engineered feature vector
```

This means the project is not inventing random columns. It is creating new variables from mathematical relationships in the existing data.

## Main Features

### Weight Gain

```text
weight_gain(t) = weight(t) - weight(t-1)
```

This measures absolute change between two consecutive records.

### Height Gain

```text
height_gain(t) = height(t) - height(t-1)
```

This measures height change between two consecutive records.

### Growth Velocity

```text
growth_velocity(t) = weight_gain(t) / delta_age(t)
```

This converts weight change into a rate of change per month.

### Weight-to-Height Ratio

```text
weight_to_height_ratio(t) = weight_kg(t) / height_cm(t)
```

This is a simple proportional feature. It is not a medical score.

### Rolling Mean

```text
rolling_mean_k(t) = average(x(t), x(t-1), ..., x(t-k+1))
```

This smooths short-term changes and helps reveal the underlying trajectory.

### Z-Score

```text
z = (value - mean) / standard_deviation
```

This compares a value with the sample distribution. In the notebook it is used to create a simple learning signal for growth velocity.

## Why This Matters for the Course

This stage connects directly to the Feature Engineering and Time Series lecture:

- new variables are created from raw variables;
- records are ordered by dog and age;
- lag features use previous measurements;
- velocity features describe rate of change;
- rolling features smooth a short time window;
- the final engineered dataset can be reused by later models.

## Why This Matters for the Project

The practical project idea is not only to ask:

```text
How heavy is the dog now?
```

A stronger question is:

```text
How is the dog changing over time?
```

This stage prepares the project for trajectory-based monitoring while keeping responsible boundaries.

## Responsible Use Boundary

The features are educational ML signals only. They do not provide:

- veterinary diagnosis;
- medical advice;
- health certification;
- pedigree proof;
- breed certification.

A high or low feature value means only that a record differs mathematically from the small sample pattern used in this notebook. It should be interpreted carefully and with proper domain context.

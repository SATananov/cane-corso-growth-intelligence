# Linear Regression Testing Exercise Alignment

This document maps the course exercise **Linear Regression, Regularization and Testing** to the Cane Corso Growth Intelligence project.

The original exercise uses the Big Mart sales dataset. This project uses the same machine-learning process, but applies it to the project domain: growth monitoring for large-breed dogs. The target variable is bodyweight in kilograms, and the input features are growth-related measurements such as age, height, sex, and activity level.

## Why this exercise matters for the project

The exercise is useful because it teaches a complete regression workflow:

1. define the research question before modeling;
2. inspect the dataset;
3. convert features into numeric form;
4. split data reproducibly;
5. train a baseline linear model;
6. evaluate with several metrics;
7. compare against another regression approach;
8. tune hyperparameters;
9. iterate based on evidence;
10. change preprocessing and compare again.

This is exactly the type of process needed for a careful educational growth-intelligence project.

## Project adaptation

In this project, the exercise is adapted as follows:

| Exercise idea | Project adaptation |
|---|---|
| Predict sales | Predict bodyweight from growth records |
| Item and outlet identifiers | Dog growth features such as age, height, sex, activity level |
| Business interpretation | Owner-facing growth monitoring interpretation |
| Data science interpretation | Regression metrics and reproducible model comparison |
| Sales prediction model | Growth-weight regression model |

## What is already covered

The current project already includes:

- a clearly formulated domain and data science problem;
- exploratory data checks;
- numeric feature preparation;
- reproducible train/test splitting;
- a LinearRegression baseline;
- MAE, RMSE, and R2 evaluation;
- visual prediction/residual checks in the notebook workflow;
- polynomial regression;
- Ridge and Lasso regularization;
- robust regression discussion;
- real public dog-growth data context;
- a practical growth assessment workflow.

## Additional alignment added for the exercise

The file `src/run_linear_regression_exercise_alignment.py` adds a compact, reproducible alignment workflow for this exercise. It compares:

1. an age-only linear regression baseline;
2. an enriched feature preprocessing model using age, height, sex, and activity level;
3. a tuned Ridge regression model using a small `alpha` grid.

The goal is not to claim a production-ready biological model. The goal is to show that the project follows the regression exercise process in a domain-specific and reproducible way.

## Important limitation

The prototype Cane Corso dataset is small. Strong metrics on this sample do not prove that the model generalizes to all Cane Corso dogs. The result should be interpreted as an educational machine-learning workflow, not as veterinary advice.

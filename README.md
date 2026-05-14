# Cane Corso Growth Intelligence

This is a machine learning course project focused on growth analysis for Cane Corso and large-breed dogs.

The first goal is to start with a simple prototype dataset and apply the machine learning methods learned during the course step by step.

At the beginning, the project will focus on linear regression and basic model testing. Later, more methods may be added as they are covered in the course.

## Current Stage

The project currently contains a small prototype dataset with sample Cane Corso growth measurements.

This dataset is not real veterinary data. It is used only for initial experiments and learning purposes.

## Planned First Experiment

The first experiment will check whether age in months can be used to predict dog weight using linear regression.
## Course Topic Flow

The first stage of the project follows the course topic: **Linear Regression, Regularization and Testing**.

```mermaid
flowchart TD
    A["Course Topic: Linear Regression, Regularization and Testing"] --> B["Problem Statement and Motivation"]
    B --> C["Prototype Cane Corso Growth Dataset"]
    C --> D["Initial Data Exploration"]

    D --> E["Simple Linear Regression"]
    E --> F["Model Testing: MAE, RMSE, R2 Score"]

    E --> G["Polynomial Regression"]
    E --> H["Multi-Dimensional Linear Regression"]
    H --> I["Regularization: Ridge and Lasso"]

    E --> J["RANSAC Robust Regression"]

    F --> K["Final Model Comparison"]
    G --> K
    H --> K
    I --> K
    J --> K

    K --> L["Result Interpretation and Limitations"]
# Data Sources

## Prototype Dataset

The file data/prototype/cane_corso_growth_sample.csv contains a small prototype dataset created for the first machine learning experiments in this project.

The dataset includes sample Cane Corso growth measurements such as:

- dog id
- dog name
- sex
- age in months
- weight in kilograms
- height in centimeters
- activity level
- source type

This dataset is not real veterinary data. It is used only for learning, testing, and early regression experiments.

## Purpose

The purpose of this first dataset is to practice simple linear regression by checking whether age in months can be used to predict dog weight.

Later in the project, real public data sources may be added and documented separately.

---

## Real Public Dataset Source

The project will also use a real public dog growth dataset as a future data foundation.

Dataset title:

Growth standard charts for monitoring bodyweight in dogs of different sizes - SUPPORTING DATA

Source:

University of Liverpool DataCat: The Research Data Catalogue

Dataset DOI:

https://doi.org/10.17638/datacat.liverpool.ac.uk/377

Related publication:

Growth standard charts for monitoring bodyweight in dogs of different sizes

## Why this source is relevant

This source is relevant because it is connected to dog growth, age, and bodyweight data.

The current prototype dataset is useful for learning the course methods step by step, but a real public dataset will make the project stronger and more realistic.

## Data Usage Plan

The full raw dataset will not be committed directly to GitHub as a normal project file because it is large.

The project will use this source in a careful way:

1. document the public data source
2. keep source and download notes
3. create a smaller processed sample for experiments
4. clearly separate prototype data from real public data

## Current Data Layers

Current prototype dataset:

data/prototype/cane_corso_growth_sample.csv

Planned real data folder:

data/raw/

Planned processed data folder:

data/processed/

---


---

## Processed Real Public Sample

A processed sample has been created from the real public dog growth dataset.

Processed file:

data/processed/dog_growth_public_sample.csv

Sample size:

- 10,000 rows
- 12 columns

The sample was created using:

src/create_public_sample.py

## Processing Summary

The script reads the large raw CSV from the local ZIP archive in chunks.

It keeps only useful project columns related to:

- breed identifier
- dog identifier
- gender
- age at visit
- bodyweight
- body condition information
- preventive care visit flag
- healthy pet diagnosis flag
- average adult breed weight

The processed sample also adds:

- visit_age_months
- source_type

## Important Note

The processed sample is committed to GitHub because it is small and usable for notebook experiments.

The original raw dataset ZIP remains local only and is not committed to GitHub.

# Data Preparation Plan

This document describes how the project will move from prototype data to real public data.

## Current Situation

The project currently uses a small prototype dataset:

data/prototype/cane_corso_growth_sample.csv

This dataset is useful for learning and applying the first course topic step by step.

It is not real veterinary data.

## Real Data Foundation

The project will use a real public dog growth dataset as the next data foundation.

The real dataset will not be committed directly to GitHub in its full raw form.

Instead, the project will document the source and create a smaller processed sample for experiments.

## Preparation Steps

### 1. Download the raw dataset locally

The raw dataset should be downloaded manually and placed in:

data/raw/

The original large file should stay local and should not be committed to GitHub.

### 2. Inspect the raw data

The first step after downloading will be to inspect:

- available files
- column names
- number of rows
- missing values
- age-related columns
- weight-related columns
- possible category columns

### 3. Select useful columns

For this project, the most useful columns will likely be related to:

- dog age
- body weight
- sex
- breed or breed size group
- measurement date or time-related information, if available

### 4. Clean the data

The cleaning process may include:

- removing rows with missing age or weight values
- converting units if needed
- checking unrealistic values
- filtering young dogs if needed
- renaming columns for clarity

### 5. Create a processed sample

A smaller processed sample will be saved in:

data/processed/dog_growth_public_sample.csv

This file should be small enough to commit to GitHub.

### 6. Use the processed sample in notebooks

The processed sample will be used in future notebook sections.

The prototype dataset will remain in the project as the first learning dataset.

## Important Rule

The project must always clearly distinguish between:

- prototype educational data
- raw public data
- processed public data sample

## Why this step matters

Using real public data will make the project stronger and more realistic.

However, it must be done carefully, with clear documentation, source attribution, and responsible data handling.

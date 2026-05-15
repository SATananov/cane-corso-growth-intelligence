# Real Data Download Instructions

This document explains how the real public dog growth dataset should be handled in this project.

## Dataset

Dataset title:

Growth standard charts for monitoring bodyweight in dogs of different sizes - SUPPORTING DATA

Source:

University of Liverpool DataCat: The Research Data Catalogue

Dataset DOI:

https://doi.org/10.17638/datacat.liverpool.ac.uk/377

Related paper:

Growth standard charts for monitoring bodyweight in dogs of different sizes

PLOS ONE DOI:

https://doi.org/10.1371/journal.pone.0182064

## Available files on the source page

The source page provides:

- Final_Data_PLOS.zip
- Salt_PuppyGrowthCharts_Readme.txt

## Important repository rule

The full raw ZIP file should not be committed directly to GitHub.

Reason:

- it is a large external dataset
- it should be treated as raw source data
- the repository should stay lightweight and easy to clone
- the project should document the source instead of hiding the origin of the data

## Recommended local workflow

1. Open the dataset source page.
2. Download the original dataset file manually.
3. Place it locally in:

data/raw/

4. Do not commit the original ZIP file to GitHub.
5. Create a smaller processed sample for notebook experiments.
6. Save the processed sample in:

data/processed/

## Planned project files

Raw data location:

data/raw/Final_Data_PLOS.zip

Processed sample location:

data/processed/dog_growth_public_sample.csv

## Project usage

The current regression notebook uses a prototype dataset.

The real public dataset will be introduced in a later notebook section or separate data preparation notebook.

The project must always clearly distinguish between:

- prototype educational data
- real public data
- processed data derived from the public source

## Ethical note

The dataset source states that the study data are anonymised. The project will not attempt to identify clients, owners, animals, or clinics.

The data will be used only for educational machine learning experiments.

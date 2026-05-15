# Real Data Source Notes

This document describes the planned real public dataset for the next project stage.

## Selected Dataset

Dataset title:

Growth standard charts for monitoring bodyweight in dogs of different sizes - SUPPORTING DATA

Source:

University of Liverpool DataCat: The Research Data Catalogue

Dataset DOI:

https://doi.org/10.17638/datacat.liverpool.ac.uk/377

Related publication:

Growth standard charts for monitoring bodyweight in dogs of different sizes
PLOS ONE, 2017
https://doi.org/10.1371/journal.pone.0182064

## Why this dataset is useful

This dataset is relevant because the project is about dog growth analysis.

The dataset is connected to a study that developed evidence-based growth standards for dogs using bodyweight and age data from young dogs.

This makes it a stronger real-world source than a fully synthetic dataset.

## Available files

The DataCat page lists:

- Final_Data_PLOS.zip
- Salt_PuppyGrowthCharts_Readme.txt

## License

The DataCat page lists the available files under Creative Commons Attribution 4.0.

## Important project decision

The full raw ZIP file is large, so it should not be committed directly to GitHub as a normal repository file.

Instead, this project will:

1. document the real data source
2. keep download/source instructions
3. create a smaller processed sample for notebook experiments
4. clearly distinguish real public data from prototype data

## Current status

The real dataset has not yet been added as a project data file.

The current repository still uses:

data/prototype/cane_corso_growth_sample.csv

The next step will be to update DATA_SOURCES.md and prepare a real data workflow.

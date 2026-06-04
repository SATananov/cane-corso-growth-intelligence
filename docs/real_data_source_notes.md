# Real Data Source Notes

This document describes the real public dataset used as the data foundation for the project.

---

## Selected Dataset

Dataset title:

```text
Growth standard charts for monitoring bodyweight in dogs of different sizes - SUPPORTING DATA
```

Source:

```text
University of Liverpool DataCat: The Research Data Catalogue
```

Dataset DOI:

```text
https://doi.org/10.17638/datacat.liverpool.ac.uk/377
```

Related publication:

```text
Growth standard charts for monitoring bodyweight in dogs of different sizes
PLOS ONE, 2017
https://doi.org/10.1371/journal.pone.0182064
```

---

## Why This Dataset Is Useful

The project is about dog growth analysis. The selected public dataset is useful because it contains dog age and bodyweight information and is connected to published research on growth standards.

This makes the project stronger than a purely synthetic dataset.

The project uses the Cane Corso domain as a practical product case, but the public dataset is a broader dog growth dataset, not a private Cane Corso-only dataset.

---

## Why This Source Was Selected Instead of Kaggle

Kaggle is a useful dataset-discovery platform, and it can be a good starting point for many student machine-learning projects. For this project, however, the goal is not simply to find any dog-related dataset.

The project needs data that matches the mathematical problem:

```text
age/bodyweight records -> growth features -> model training -> monitoring signal
```

Many general dog datasets are better suited for other tasks, such as image classification, breed description lookup, adoption analysis or synthetic wellness examples. The selected University of Liverpool DataCat / PLOS ONE source is more directly aligned with dog bodyweight growth monitoring.

A full explanation is available in:

```text
docs/dataset_selection_rationale.md
```

---

## Available Raw Files

The DataCat source lists files such as:

- `Final_Data_PLOS.zip`
- `Salt_PuppyGrowthCharts_Readme.txt`

The raw files are external source files and should remain local in:

```text
data/raw/
```

They should not be included in the final clean repository submission ZIP.

---

## License Note

The DataCat page lists the available files under Creative Commons Attribution 4.0.

The project should keep the source title, DOI and related publication in the documentation.

---

## Current Project Usage

The project uses processed samples generated from the raw public dataset:

```text
data/processed/dog_growth_public_sample.csv
data/processed/dog_growth_classification_sample.csv
```

These processed samples are smaller, project-specific files that can be used in notebooks and committed to the repository.

Scripts:

```text
src/create_public_sample.py
src/create_classification_sample.py
```

---

## Important Honesty Rule

The project should say:

```text
This project uses a real public dog growth dataset and applies it to the Cane Corso Growth Intelligence idea.
```

The project should not say:

```text
This project uses private real Cane Corso veterinary records.
```

This distinction keeps the project academically honest and professionally responsible.

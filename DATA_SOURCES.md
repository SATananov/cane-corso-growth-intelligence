# Data Sources

This file documents the datasets used in the project and explains how prototype, raw, and processed data are separated.

## 1. Prototype Dataset

File:

```text
data/prototype/cane_corso_growth_sample.csv
```

This is a small educational dataset created for the first machine learning experiments.

It includes sample Cane Corso growth measurements such as:

- dog id
- dog name
- sex
- age in months
- weight in kilograms
- height in centimeters
- activity level
- source type

This dataset is not real veterinary data. It is used only for learning, testing, and early regression experiments.

## 2. Real Public Dataset Source

The project uses a real public dog growth dataset as the foundation for later experiments.

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
```

The source dataset is relevant because it contains dog age and bodyweight information and is connected to public research on dog growth standards.

## 3. Raw Data Rule

The full raw dataset is not committed directly to GitHub.

Reasons:

- it is a large external dataset
- the repository should stay lightweight
- the raw data source should remain clearly documented
- only project-specific processed samples should be committed

Raw data is expected locally in:

```text
data/raw/
```

The repository keeps only:

```text
data/raw/source_notes.md
```

The original raw ZIP and original raw metadata files are ignored by Git.

## 4. General Processed Real Public Sample

File:

```text
data/processed/dog_growth_public_sample.csv
```

Sample size:

- 10,000 rows
- 12 columns

Created by:

```text
src/create_public_sample.py
```

This script reads the large raw CSV from the local ZIP archive in chunks and creates a smaller processed sample.

The processed sample keeps project-useful columns related to:

- breed identifier
- dog identifier
- gender
- age at visit
- bodyweight
- body condition information
- preventive care visit flag
- healthy pet diagnosis flag
- average adult breed weight

It also adds:

- `visit_age_months`
- `source_type`

Source label:

```text
real_public_processed_sample
```

This sample is committed to GitHub because it is small and usable for notebook experiments.

## 5. Classification-Focused Processed Sample

File:

```text
data/processed/dog_growth_classification_sample.csv
```

Sample size:

- 10,000 rows
- 15 columns

Created by:

```text
src/create_classification_sample.py
```

This sample was created specifically for the Classification topic.

It keeps rows with usable body condition score information and creates the classification target:

```text
growth_status
```

Target classes:

- `normal_growth`
- `needs_attention`

Binary target:

- `0` = `normal_growth`
- `1` = `needs_attention`

Class balance:

- 5,000 `normal_growth` records
- 5,000 `needs_attention` records

Source label:

```text
real_public_classification_sample
```

This balanced sample is used in:

```text
notebooks/03_classification_growth_status.ipynb
```

## 6. Data Ethics and Limitations

The project does not attempt to identify clients, owners, animals, or clinics.

The data is used only for educational machine learning experiments.

The project does not provide veterinary diagnosis. Model outputs should be interpreted as learning exercises, not medical conclusions.

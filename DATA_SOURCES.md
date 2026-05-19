# Data Sources

This file documents the datasets used in the project and explains how prototype, raw, and processed data are separated.

The project is intentionally transparent about its data foundation. It does not claim to use private Cane Corso veterinary records. It uses a small educational prototype dataset and a real public dog growth dataset.

---

## 1. Prototype Dataset

File:

```text
data/prototype/cane_corso_growth_sample.csv
```

This is a small educational dataset created for the first machine-learning experiments.

It includes sample Cane Corso-style growth measurements such as:

- dog id
- dog name
- sex
- age in months
- weight in kilograms
- height in centimeters
- activity level
- source type

This dataset is not real veterinary data. It is used only for learning, testing, and early regression experiments.

---

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
PLOS ONE, 2017
```

The source dataset is relevant because it contains dog age and bodyweight information and is connected to public research on dog growth standards. This fits the project motivation because growth monitoring depends on repeated age and bodyweight records, especially when the goal is to compare measured development with expected patterns.

Important project interpretation:

```text
The public dataset provides a real dog-growth data foundation.
The Cane Corso domain provides the practical product context.
The project does not claim that the public dataset is a private Cane Corso-only dataset.
```

---

## 3. Raw Dataset Archive Rule

The full original dataset should not be committed directly to GitHub.

The public source distributes the original data as a compressed archive. In this project, that file is called the **raw dataset archive**:

```text
data/raw/Final_Data_PLOS.zip
```

This term means only the original public dataset distribution file. It does not refer to project patch files, clean checkpoint archives, submission archives, or any temporary development ZIP files.

Reasons for keeping the raw dataset archive local only:

- it is an external public dataset;
- the repository should stay lightweight;
- the source should remain clearly attributed;
- only project-specific processed samples should be committed;
- the final clean project submission should not contain large raw downloaded archives.

The repository should keep only lightweight source notes in `data/raw/`, such as:

```text
data/raw/source_notes.md
```

The raw dataset archive and any original source metadata files should remain local and ignored by Git.

A dedicated explanation is available in:

```text
docs/raw_dataset_archive_policy.md
```

---

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

This script reads the large raw CSV from the local raw dataset archive in chunks and creates a smaller processed sample.

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

---

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
notebooks/03_1_classification_pipeline_exercise.ipynb
```

---

## 6. Why This Data Choice Is Useful

The project is stronger than a fully synthetic exercise because it has:

- a personally meaningful Cane Corso product case;
- a real public dog-growth data foundation;
- documented source attribution;
- processed samples small enough for reproducible notebooks;
- a clear distinction between prototype data, raw external data and processed public samples.

This allows the project to stay honest while still being useful and interesting.

---

## 7. Data Ethics and Limitations

The project does not attempt to identify clients, owners, animals, or clinics.

The data is used only for educational machine-learning experiments.

The project does not provide veterinary diagnosis. Model outputs should be interpreted as growth-monitoring signals for analysis and learning, not as medical conclusions.

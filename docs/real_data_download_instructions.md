# Real Data Download Instructions

This document explains how the real public dog growth dataset should be handled in this project.

## Dataset

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

Related paper:

```text
Growth standard charts for monitoring bodyweight in dogs of different sizes
```

PLOS ONE DOI:

```text
https://doi.org/10.1371/journal.pone.0182064
```

---

## What the Dataset Archive Means

The source distributes the original dataset as a compressed archive file, commonly named:

```text
Final_Data_PLOS.zip
```

In this project, that file is called the **raw dataset archive**.

This is a data-source term. It means the original public data file is compressed before processing. It does not refer to project patch archives, clean checkpoint archives, or any development ZIP files used outside the analytical workflow.

---

## Repository Rule

The raw dataset archive should not be committed directly to GitHub.

Reasons:

- the data belongs to an external public source;
- the source should be documented and credited clearly;
- the repository should remain lightweight;
- the notebooks should rely on smaller processed samples;
- the final project submission should not include large raw downloaded archives.

The expected local path is:

```text
data/raw/Final_Data_PLOS.zip
```

The repository should include only lightweight notes in `data/raw/`, such as:

```text
data/raw/source_notes.md
```

---

## How to Regenerate Processed Samples

If the raw dataset archive is available locally, the processed samples can be regenerated with:

```bash
python src/create_public_sample.py
python src/create_classification_sample.py
```

The scripts read the local raw dataset archive, select relevant columns, clean usable records, and create smaller CSV files in:

```text
data/processed/
```

The current processed samples used by the notebooks are:

```text
data/processed/dog_growth_public_sample.csv
data/processed/dog_growth_classification_sample.csv
```

---

## Practical Workflow

```text
1. Download the original public dataset from the documented source.
2. Keep the compressed raw dataset archive locally in data/raw/.
3. Run the processing scripts if the processed samples need to be regenerated.
4. Commit only the small processed CSV samples and documentation.
5. Do not commit the original raw dataset archive.
```

This keeps the project transparent, reproducible, and suitable for GitHub review.

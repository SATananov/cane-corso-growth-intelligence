# Raw Dataset Archive Policy

This document explains what the project means by **raw dataset archive** and how it is different from the files used for development, repository submission, or saved state packaging.

## What “raw dataset archive” means

The original public dataset used by the project is distributed by its source as a compressed archive file:

```text
Final_Data_PLOS.zip
```

In this project, that file is called the **raw dataset archive**.

This is a normal data-engineering term. It means that the public dataset was provided as a compressed file that contains the original raw data. It does **not** mean that the project depends on random downloaded files, temporary update archives, or local working ZIP files.

## Why the raw archive is not committed

The raw dataset archive is intentionally kept outside repository because:

- it is an external public dataset;
- the original source must remain clearly attributed;
- the repository should stay lightweight and easy to review;
- the notebooks should use stable processed CSV files;
- the final project should not contain large raw downloaded archives.

The expected local path is:

```text
data/raw/Final_Data_PLOS.zip
```

The file can exist locally when the processed samples need to be regenerated, but it should not be committed to repository.

## What is committed instead

The project commits smaller processed CSV files created from the raw public dataset:

```text
data/processed/dog_growth_public_sample.csv
data/processed/dog_growth_classification_sample.csv
```

These processed samples are the files used by the current notebooks.

## How the scripts use the archive

The scripts in `src/` can read the local raw dataset archive, extract the relevant CSV data in chunks, clean useful columns, and save smaller processed samples.

The important workflow is:

```text
public dataset archive -> local processing script -> processed CSV sample -> notebook experiments
```

This separates the original data source from the project-ready data used for modelling.

## Important distinction

The term **raw dataset archive** refers only to the original public dataset distribution file.

It is different from:

- a project local backup archive;
- a clean submission archive;
- a development temporary update archive;
- any temporary local ZIP file used outside the project.

Only the processed CSV samples are part of the current analytical workflow.

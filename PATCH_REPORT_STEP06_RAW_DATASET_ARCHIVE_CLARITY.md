# Patch Report — Step 06 Raw Dataset Archive Clarity

## Purpose

This patch clarifies the data-source terminology across the project.

The project previously used the word `ZIP` in a few places when referring to the original public dataset file. This could sound like the project depends on random downloaded ZIP files or development patch archives. The wording is now standardized around the professional term:

```text
raw dataset archive
```

## Important meaning

In this project, **raw dataset archive** means only:

```text
data/raw/Final_Data_PLOS.zip
```

That is the original public dataset distribution file from the documented source.

It does not mean:

- a project patch archive;
- a clean checkpoint archive;
- a submission archive;
- a temporary local ZIP file;
- a random downloaded file.

## Files changed

- `README.md`
- `PROJECT_BRIEF.md`
- `COURSE_TOPIC_MAPPING.md`
- `DATA_SOURCES.md`
- `HOW_TO_RUN.md`
- `data/raw/source_notes.md`
- `docs/raw_dataset_archive_policy.md`
- `docs/real_data_download_instructions.md`
- `docs/real_data_source_notes.md`
- `docs/data_preparation_plan.md`
- `notebooks/02_real_data_preparation.ipynb`
- `src/create_public_sample.py`
- `src/create_classification_sample.py`

## What did not change

- No dataset values were changed.
- No model logic was changed.
- No notebook modelling results were changed.
- No current processed CSV files were changed.

## Result

The project now explains the data flow more professionally:

```text
public dataset archive -> local processing script -> processed CSV sample -> notebook experiments
```

This supports the final project story as a clear, reproducible machine-learning workflow.

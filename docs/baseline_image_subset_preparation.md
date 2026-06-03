# Step 19 — Baseline Image Subset Preparation

This step prepares a small, local, reproducible image subset for the first Stanford Dogs baseline image-classification experiment.

The project has already confirmed that Stanford Dogs can be downloaded locally and inspected without committing image files to GitHub. Step 19 builds on that by creating a controlled subset from the selected baseline classes.

## Purpose

The goal is not to train a model yet. The goal is to prepare the data correctly before training.

Step 19 creates:

- a local `train / validation / test` folder structure for the first image baseline;
- a manifest CSV describing every selected image;
- a summary report with counts by class and split;
- validation logic to confirm the subset is usable for a later baseline model.

## Why this matters

Image classification quality depends heavily on data preparation. A model trained on unclear, unbalanced or undocumented image folders may learn accidental patterns instead of useful visual features.

For this project, the data preparation layer is especially important because the future visual module is a **visual similarity classifier**, not a breed-proof system.

The classifier must never be presented as proof of:

- official breed identity;
- pedigree;
- registry status;
- genetic origin;
- veterinary condition;
- USG recognition or certification.

## Local-only output

The actual images are copied into a local ignored folder:

```text
data/images/local_dataset/splits/stanford_dogs_first_baseline/
  train/
  validation/
  test/
```

These image files must remain local and must not be committed to GitHub.

The GitHub repository should contain only:

- code;
- documentation;
- reports;
- CSV manifests;
- notebooks;
- patch reports.

## Commands

After Stanford Dogs has been downloaded and extracted locally, run:

```powershell
python src/prepare_stanford_dogs_baseline_subset.py
python src/validate_stanford_dogs_baseline_subset.py
```

The preparation script reads the selected classes from:

```text
reports/stanford_dogs_baseline_class_selection.csv
```

It uses only rows selected for the first baseline.

## Expected outputs

```text
reports/stanford_dogs_baseline_subset_manifest.csv
reports/stanford_dogs_baseline_subset_summary.md
```

The image subset itself is local-only:

```text
data/images/local_dataset/splits/stanford_dogs_first_baseline/
```

## Clean repository boundary

After running Step 19, `git status` should show only report/manifest changes and source/docs/notebook files from this patch. It should not show `.jpg`, `.jpeg`, `.png`, `images.tar`, `raw`, `downloads` or large dataset folders as untracked files.

If image files appear in `git status`, do not run `git add .` before checking `.gitignore`.

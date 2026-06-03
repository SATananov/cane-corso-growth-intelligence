# Patch Report — Step 13 Image Dataset Acquisition and Local Preparation

## Purpose

Step 13 prepares the project for a future Computer Vision image-classification baseline without committing actual image datasets to GitHub.

The step adds local acquisition instructions, a safe ignored folder structure, an inventory template, and validation scripts.

## Added Files

```text
docs/image_dataset_acquisition_and_local_preparation.md
data/images/local_dataset/.gitignore
data/images/local_dataset/README.md
data/image_dataset_local_inventory_template.csv
src/prepare_image_dataset_structure.py
src/validate_local_image_dataset.py
notebooks/08_image_dataset_acquisition_local_preparation.ipynb
PATCH_REPORT_STEP13_IMAGE_DATASET_ACQUISITION_LOCAL_PREPARATION.md
```

## Updated Files

```text
.gitignore
README.md
HOW_TO_RUN.md
DATA_SOURCES.md
PROJECT_BRIEF.md
COURSE_TOPIC_MAPPING.md
data/images/README.md
```

## Scope

This patch adds:

- local image dataset acquisition instructions;
- local folder preparation script;
- local folder validation script;
- target-class-aware image folder structure;
- local dataset inventory template;
- notebook documentation for Step 13;
- Git ignore rules for local image datasets and common image formats.

This patch does **not** add:

- downloaded public image datasets;
- private owner photos;
- scraped web images;
- trained Computer Vision model;
- breed-proof or pedigree-proof claims.

## Recommended Local Checks

```powershell
python src/prepare_image_dataset_structure.py
python src/validate_local_image_dataset.py
python src/validate_image_dataset_feasibility.py
python src/validate_image_manifest.py
python src/create_time_series_features.py
python src/run_growth_assessment.py
```

## Responsible Boundary

The future Computer Vision module must remain a visual-similarity classifier. It should not claim to prove official breed, pedigree, registry status, genetic origin, or veterinary conclusions from an image.

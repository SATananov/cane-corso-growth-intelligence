# Patch Report — Step 12: Public Image Dataset Feasibility

## Purpose

Step 12 adds a safe data-feasibility layer before any Computer Vision training is attempted.

The project idea is to eventually combine:

```text
growth measurements -> growth monitoring signal
image input -> visual similarity probabilities
combined report -> educational interpretation
```

However, the project does not currently have a private image dataset. Therefore Step 12 focuses on dataset research and validation.

## Files Added

```text
docs/image_dataset_feasibility.md
data/image_dataset_feasibility_matrix.csv
data/molossoid_visual_target_classes.csv
src/validate_image_dataset_feasibility.py
notebooks/07_image_dataset_feasibility.ipynb
PATCH_REPORT_STEP12_IMAGE_DATASET_FEASIBILITY.md
```

## Files Updated

```text
README.md
HOW_TO_RUN.md
DATA_SOURCES.md
COURSE_TOPIC_MAPPING.md
PROJECT_BRIEF.md
docs/image_dataset_research_plan.md
```

## Boundaries

Step 12 does not:

- download public image datasets;
- commit image files to GitHub;
- scrape Google, Instagram, Facebook or breeder websites;
- train a Computer Vision model;
- claim breed proof, pedigree proof or registry authority from an image.

## Validation

Run from the project root:

```powershell
python src/validate_image_dataset_feasibility.py
python src/validate_image_manifest.py
python src/create_time_series_features.py
python src/run_growth_assessment.py
```

Expected new validation result:

```text
Step 12 image dataset feasibility validation PASS
```

## Commit Message

```text
Step 12 add image dataset feasibility research
```

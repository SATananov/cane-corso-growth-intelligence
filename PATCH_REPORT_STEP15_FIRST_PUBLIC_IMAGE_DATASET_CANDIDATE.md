# Patch Report — Step 15: First Public Image Dataset Candidate / Download Guide

## Summary

Step 15 adds the first public image dataset candidate and a local download/inspection guide for the future Computer Vision visual-similarity module.

## Added files

```text
docs/first_public_image_dataset_candidate_download_guide.md
data/first_public_image_dataset_candidate.csv
data/stanford_dogs_local_download_checklist.csv
src/validate_first_public_image_dataset_candidate.py
src/inspect_stanford_dogs_local_dataset.py
notebooks/10_first_public_image_dataset_candidate_download_guide.ipynb
```

## Updated files

```text
README.md
HOW_TO_RUN.md
DATA_SOURCES.md
PROJECT_BRIEF.md
COURSE_TOPIC_MAPPING.md
```

## Scope

This patch does not download images and does not train an image model.

It only documents the first public dataset candidate, local folder policy, inspection script, and responsible interpretation boundaries.

## Responsible-use boundary

The planned model is a visual similarity classifier only. It is not breed proof, pedigree proof, registry proof, certificate proof or veterinary diagnosis.

## Suggested checks

```bash
python src/validate_first_public_image_dataset_candidate.py
python src/inspect_stanford_dogs_local_dataset.py
python src/audit_public_image_dataset_classes.py
python src/validate_local_image_dataset.py
python src/validate_image_dataset_feasibility.py
python src/validate_image_manifest.py
python src/create_time_series_features.py
python src/run_growth_assessment.py
```

# Patch Report — Step 19: Baseline Image Subset Preparation

## Purpose

Step 19 prepares the first local image subset for a future Stanford Dogs baseline visual-similarity classifier.

This step does not train an image model. It prepares a reproducible `train / validation / test` subset from the selected Stanford Dogs classes and writes a manifest/report for evidence.

## Added files

- `docs/baseline_image_subset_preparation.md`
- `docs/baseline_image_subset_policy.md`
- `data/stanford_dogs_baseline_subset_plan.csv`
- `src/prepare_stanford_dogs_baseline_subset.py`
- `src/validate_stanford_dogs_baseline_subset.py`
- `notebooks/13_baseline_image_subset_preparation.ipynb`
- `reports/stanford_dogs_baseline_subset_manifest.csv`
- `reports/stanford_dogs_baseline_subset_summary.md`

## Local-only boundary

The subset images are copied into:

```text
data/images/local_dataset/splits/stanford_dogs_first_baseline/
```

This folder is local-only and should not be committed to GitHub.

## Validation commands

```powershell
python src/prepare_stanford_dogs_baseline_subset.py
python src/validate_stanford_dogs_baseline_subset.py
python src/inspect_stanford_dogs_real_classes.py
python src/select_stanford_dogs_baseline_classes.py
python src/validate_stanford_dogs_real_inspection.py
python src/create_time_series_features.py
python src/run_growth_assessment.py
```

## Responsible interpretation

This step supports an educational visual-similarity baseline only. It does not prove breed, pedigree, registry status, genetic origin, USG recognition, certification or veterinary condition.

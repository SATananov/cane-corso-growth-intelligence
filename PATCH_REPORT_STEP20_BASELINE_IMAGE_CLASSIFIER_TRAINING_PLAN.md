# PATCH REPORT — Step 20: Baseline Image Classifier Training Plan

## Purpose

This patch adds a safe and documented training plan for the first baseline visual similarity classifier.

The goal is to prepare the project for a future lightweight Computer Vision prototype without training a model yet and without committing image data or model weights.

## Added files

- `docs/baseline_image_classifier_training_plan.md`
- `docs/visual_similarity_training_safety_boundaries.md`
- `data/baseline_image_classifier_training_plan.csv`
- `data/baseline_image_classifier_metrics_plan.csv`
- `src/validate_baseline_image_classifier_training_plan.py`
- `notebooks/14_baseline_image_classifier_training_plan.ipynb`
- `reports/baseline_image_classifier_training_plan_validation.md`

## Validation command

```powershell
python src/validate_baseline_image_classifier_training_plan.py
```

Optional continuity checks:

```powershell
python src/prepare_stanford_dogs_baseline_subset.py
python src/validate_stanford_dogs_baseline_subset.py
python src/inspect_stanford_dogs_real_classes.py
python src/select_stanford_dogs_baseline_classes.py
python src/validate_stanford_dogs_real_inspection.py
python src/create_time_series_features.py
python src/run_growth_assessment.py
```

## Boundaries

- No model is trained in this step.
- No images are downloaded in this step.
- No image files should be committed to GitHub.
- No large model weights should be committed to GitHub.
- The future model must be described as visual similarity only, not breed proof.

## Expected commit message

```text
Step 20 add baseline image classifier training plan
```

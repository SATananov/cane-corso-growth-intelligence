# Patch Report — Step 21 Lightweight Baseline Image Classifier Prototype

## Purpose

Step 21 adds the first lightweight image-classification prototype for the visual-similarity extension of the Cane Corso Growth Intelligence project.

## Scope

This patch adds:

- documentation for the lightweight classifier prototype;
- safety boundaries for visual-similarity interpretation;
- a configuration CSV for the baseline classifier;
- a training script using simple image features and scikit-learn logistic regression;
- a validation script for generated report artifacts;
- a notebook stub for the Step 21 workflow;
- placeholder reports that are updated when the script is run locally.

## Files added

```text
docs/lightweight_baseline_image_classifier_prototype.md
docs/lightweight_image_classifier_safety_boundaries.md
data/lightweight_image_classifier_config.csv
src/train_lightweight_image_classifier.py
src/validate_lightweight_image_classifier_outputs.py
notebooks/15_lightweight_baseline_image_classifier_prototype.ipynb
reports/lightweight_image_classifier_training_report.md
reports/lightweight_image_classifier_metrics.csv
reports/lightweight_image_classifier_confusion_matrix.csv
reports/lightweight_image_classifier_prediction_examples.csv
PATCH_REPORT_STEP21_LIGHTWEIGHT_BASELINE_IMAGE_CLASSIFIER.md
```

## Boundaries

- No image files are added to GitHub.
- No model weights are saved or committed.
- The classifier is visual-similarity only.
- The classifier does not prove breed, pedigree, genetics, registry status, or veterinary status.

## Recommended validation

```powershell
python src/train_lightweight_image_classifier.py
python src/validate_lightweight_image_classifier_outputs.py
python src/validate_baseline_image_classifier_training_plan.py
python src/validate_stanford_dogs_baseline_subset.py
python src/run_growth_assessment.py
```

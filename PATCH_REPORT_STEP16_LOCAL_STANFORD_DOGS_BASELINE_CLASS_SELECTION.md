# Patch Report — Step 16: Local Stanford Dogs Inspection / Baseline Class Selection

## Summary

Step 16 adds an evidence-based class-selection layer for the future Computer Vision visual-similarity module.

The project still does not train an image model. It now documents and validates how local Stanford Dogs labels should be inspected before selecting first-baseline classes.

## Added files

```text
docs/local_stanford_dogs_inspection_baseline_class_selection.md
docs/baseline_visual_class_selection_policy.md
data/stanford_dogs_baseline_class_candidates.csv
data/stanford_dogs_baseline_class_selection_template.csv
src/select_stanford_dogs_baseline_classes.py
src/validate_stanford_baseline_class_selection.py
notebooks/11_local_stanford_dogs_inspection_baseline_class_selection.ipynb
```

## Generated reports

```text
reports/stanford_dogs_baseline_class_selection.md
reports/stanford_dogs_baseline_class_selection.csv
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

No image model is trained in this step. No image dataset is downloaded or committed.

## Responsible-use boundary

Class selection must be based on confirmed local labels. If a desired class such as Cane Corso, Dogo Argentino or Presa Canario is missing from the selected public dataset, the project must not claim it can recognize that class.

The visual module remains a visual-similarity research plan only. It is not breed proof, pedigree proof, registry proof, certificate proof or veterinary diagnosis.

## Suggested checks

```bash
python src/select_stanford_dogs_baseline_classes.py
python src/validate_stanford_baseline_class_selection.py
python src/validate_first_public_image_dataset_candidate.py
python src/inspect_stanford_dogs_local_dataset.py
python src/audit_public_image_dataset_classes.py
python src/prepare_image_dataset_structure.py
python src/validate_local_image_dataset.py
python src/validate_image_dataset_feasibility.py
python src/validate_image_manifest.py
python src/create_time_series_features.py
python src/run_growth_assessment.py
```

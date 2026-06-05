# Patch Report — Step 17: Stanford Dogs Local Download / Real Class Inspection

## Summary

Step 17 adds a safe local download and real class inspection workflow for Stanford Dogs / ImageNet Dogs.

It does not download large archives by default and does not train an image model.

## Added

- `docs/stanford_dogs_local_download_real_class_inspection.md`
- `docs/stanford_dogs_real_class_inspection_protocol.md`
- `data/stanford_dogs_download_artifacts.csv`
- `data/stanford_dogs_real_inspection_rules.csv`
- `src/download_stanford_dogs_local_dataset.py`
- `src/inspect_stanford_dogs_real_classes.py`
- `src/validate_stanford_dogs_real_inspection.py`
- `notebooks/12_stanford_dogs_local_download_real_class_inspection.ipynb`
- `reports/stanford_dogs_download_readiness.md`
- `reports/stanford_dogs_real_class_inspection.md`

## Updated

- `README.md`
- `HOW_TO_RUN.md`
- `DATA_SOURCES.md`
- `PROJECT_BRIEF.md`
- `COURSE_TOPIC_MAPPING.md`

## Validation Commands

```bash
python src/download_stanford_dogs_local_dataset.py
python src/inspect_stanford_dogs_real_classes.py
python src/validate_stanford_dogs_real_inspection.py
python src/select_stanford_dogs_baseline_classes.py
python src/validate_stanford_baseline_class_selection.py
python src/validate_first_public_image_dataset_candidate.py
python src/audit_public_image_dataset_classes.py
python src/prepare_image_dataset_structure.py
python src/validate_local_image_dataset.py
python src/validate_image_dataset_feasibility.py
python src/validate_image_manifest.py
python src/create_time_series_features.py
python src/run_growth_assessment.py
```

## Boundary

This step supports local public dataset inspection only. It does not claim breed proof, pedigree proof, registry proof, certificate proof, veterinary diagnosis or image-model accuracy.

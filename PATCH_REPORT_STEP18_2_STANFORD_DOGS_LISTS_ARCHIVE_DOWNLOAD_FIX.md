# Patch Report — Step 18.2: Stanford Dogs Lists Archive Download Fix

## Summary

This patch fixes the Step 18 local Stanford Dogs metadata download workflow after a real local test showed that the direct `file_list.mat` URL can return `404 Not Found`.

## What changed

- Replaced direct `file_list.mat`, `train_list.mat`, and `test_list.mat` artifact rows with the official `lists.tar` split metadata archive.
- Kept `README.txt` as a small default download.
- Kept `images.tar` and `annotation.tar` as explicit-only large/optional artifacts.
- Added `--extract-lists` support.
- Made `--download-small` extract `lists.tar` locally when it is available.
- Updated Step 17/18 documentation with the real observed reason for the correction.

## Boundary

This patch does not download images by default, does not train a computer vision model, does not prove breed identity, and does not change the growth-model workflow.

## Recommended validation

```powershell
python src/download_stanford_dogs_local_dataset.py --download-small --force
python src/inspect_stanford_dogs_real_classes.py
python src/select_stanford_dogs_baseline_classes.py
python src/validate_stanford_dogs_real_inspection.py
python src/run_growth_assessment.py
```

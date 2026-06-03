# Patch Report — Step 18.1 Stanford Dogs SSL-safe Download URLs

## Purpose

This patch addresses a local download failure where Python/Windows reports an SSL certificate hostname mismatch for `https://vision.stanford.edu` while trying to download Stanford Dogs small metadata artifacts.

## Changes

- Updated `data/stanford_dogs_download_artifacts.csv` so the Stanford Dogs README uses the historically documented official `http://vision.stanford.edu/...` endpoint.
- Updated `src/download_stanford_dogs_local_dataset.py` with a safe official-host fallback from HTTPS to HTTP for Stanford Dogs artifacts.
- Added a User-Agent header and streamed file download handling.
- Added final URL reporting to `reports/stanford_dogs_download_readiness.md`.
- Documented that the project does **not** disable SSL verification.

## Boundary

This patch does not download images by default, does not train an image model, does not commit image files, and does not prove breed identity. It only makes the local Stanford Dogs download helper more robust for official public dataset artifacts.

## Validation commands

```powershell
python src/download_stanford_dogs_local_dataset.py --download-small --force
python src/inspect_stanford_dogs_real_classes.py
python src/select_stanford_dogs_baseline_classes.py
python src/validate_stanford_dogs_real_inspection.py
python src/create_time_series_features.py
python src/run_growth_assessment.py
```

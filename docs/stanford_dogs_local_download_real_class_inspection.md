# Step 17 — Stanford Dogs Local Download / Real Class Inspection

## Purpose

Step 17 moves the Computer Vision branch from planning to a **real local dataset inspection workflow**.

The project still does **not** train an image model in this step. Instead, it prepares a safe workflow for downloading Stanford Dogs locally, extracting it locally, inspecting real class folders and deciding which classes can be used later for a baseline classifier.

## Why This Step Matters

Before training any image classifier, the project must answer a simple question:

```text
Which breed labels are actually available in the local dataset?
```

The desired molossoid classes are not the same thing as available public dataset classes. Therefore, the project must not claim that Cane Corso, Dogo Argentino, Presa Canario or any other breed is available until the local dataset labels prove it.

## Dataset Candidate

The first public image dataset candidate remains Stanford Dogs / ImageNet Dogs.

It is useful as a first educational baseline because it is a known dog-breed image classification dataset. However, Step 17 treats every target class as evidence-based: a class can only be used if it is detected locally after download/extraction.

## Local Only Boundary

Downloaded image archives and extracted images are **local only**.

They must stay under:

```text
data/images/local_dataset/downloads/stanford_dogs/
data/images/local_dataset/raw/stanford_dogs/
```

These folders are ignored by Git. They should not be committed to GitHub.

## Not Downloaded by Default

The download script is intentionally safe:

```text
Large image archives are not downloaded by default.
```

Running the script without flags prepares folders and writes a readiness report only.

Small metadata can be downloaded explicitly:

```bash
python src/download_stanford_dogs_local_dataset.py --download-small
```

The large image archive requires an explicit flag:

```bash
python src/download_stanford_dogs_local_dataset.py --download-images
```

After the archive exists locally, extract it explicitly:

```bash
python src/download_stanford_dogs_local_dataset.py --extract-images
```

Then inspect real classes:

```bash
python src/inspect_stanford_dogs_real_classes.py
python src/select_stanford_dogs_baseline_classes.py
python src/validate_stanford_baseline_class_selection.py
```

## Expected Step 17 Checks

Use this safe sequence first:

```bash
python src/download_stanford_dogs_local_dataset.py
python src/inspect_stanford_dogs_real_classes.py
python src/validate_stanford_dogs_real_inspection.py
python src/select_stanford_dogs_baseline_classes.py
python src/validate_stanford_baseline_class_selection.py
```

This sequence should pass even before the large dataset is downloaded.

## Real Dataset Download Sequence

Only when disk space and internet connection are ready:

```bash
python src/download_stanford_dogs_local_dataset.py --download-small
python src/download_stanford_dogs_local_dataset.py --download-images
python src/download_stanford_dogs_local_dataset.py --extract-images
python src/inspect_stanford_dogs_real_classes.py
python src/select_stanford_dogs_baseline_classes.py
python src/validate_stanford_baseline_class_selection.py
```

If the local inspection still finds zero classes, do not train. First verify that the archive extracted into the expected folder structure.

## Interpretation Rules

A detected class means only:

```text
This public dataset contains a local image folder with this label.
```

It does **not** mean:

```text
The label is perfect.
The dog is genetically proven.
The dog has a pedigree.
The image proves breed identity.
The model can issue registry or certificate decisions.
```

## Responsible Boundary

This module is for **visual similarity** only.

It is not breed proof, not pedigree proof, not registry proof, not certificate proof and not veterinary diagnosis.

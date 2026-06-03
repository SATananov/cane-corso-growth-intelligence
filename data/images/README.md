# Image Dataset Folder

This folder is reserved for the future Computer Vision visual similarity module.

The current repository does not commit real image datasets. Full image datasets can be large and may have license or permission restrictions.

Current tracked files:

```text
data/image_dataset_manifest_example.csv
```

Future local structure may look like:

```text
data/images/local_only/
  cane_corso/
  dogo_argentino/
  presa_canario/
  great_dane/
  neapolitan_mastiff/
  bullmastiff/
  boxer/
  mastiff/
  other_unknown/
```

The folder name `local_only` is intentional: downloaded datasets or owner-provided images should remain local unless the project has clear permission and a proper storage strategy.

Responsible rule:

```text
No random Google, Instagram, Facebook, or breeder-site scraping without permission.
```


## Step 12 note

Step 12 intentionally keeps this folder free from downloaded image files. The project now stores image dataset feasibility metadata in `data/image_dataset_feasibility_matrix.csv` and target-class planning in `data/molossoid_visual_target_classes.csv`. Actual image archives should remain local until usage terms, class availability and storage strategy are confirmed.


## Step 13 Local Dataset Preparation

The project now reserves this ignored local folder for future image experiments:

```text
data/images/local_dataset/
```

Use it only on the local machine for downloaded public datasets or future consent-based owner images. Do not commit actual image files to GitHub.

Prepare the structure:

```powershell
python src/prepare_image_dataset_structure.py
```

Validate the structure:

```powershell
python src/validate_local_image_dataset.py
```

The committed repository should contain documentation, scripts and lightweight metadata templates only.

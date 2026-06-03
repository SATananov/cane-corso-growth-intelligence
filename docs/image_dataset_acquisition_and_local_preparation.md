# Step 13 — Image Dataset Acquisition Instructions and Local Preparation

This document explains how the future Computer Vision module should acquire and prepare image data **without committing downloaded images to GitHub**.

The project is still an educational machine-learning project. Step 13 does not train an image classifier yet. It prepares the responsible local data workflow needed before a baseline visual-similarity model can be created.

---

## Goal

The planned Computer Vision extension should eventually support a visual-similarity task such as:

```text
input dog image -> visual feature extractor -> class probabilities -> responsible interpretation
```

Example output format for a future model:

```text
Cane Corso: 65%
Dogo Argentino: 15%
Presa Canario: 12%
Great Dane: 8%
```

Correct interpretation:

```text
The image has strongest visual similarity to this trained class among the classes available to the model.
```

Incorrect interpretation:

```text
The image proves the official breed, pedigree, registry status or genetic origin of the dog.
```

---

## Why Local Preparation Is Needed

Public dog image datasets can be large and may have separate download conditions. Owner-provided photos may include privacy and permission requirements. For that reason, the repository should contain only:

```text
code
notebooks
documentation
small metadata templates
small example manifests
```

The repository should not contain:

```text
downloaded image datasets
private owner images
scraped social media images
large raw archives
unverified image folders
```

---

## Allowed Data Sources

Only these source categories are acceptable for the future image module:

1. Public image datasets with documented usage terms.
2. The user's own photos, if the user has the right to use them.
3. Owner-provided photos with clear permission.
4. Future USG consent-based image submissions, if the platform later implements a consent workflow.

The project should not use random Google, Instagram, Facebook, breeder-site or social-media images without permission.

---

## Candidate Public Datasets

Step 12 documents candidate sources in:

```text
data/image_dataset_feasibility_matrix.csv
```

Before using any candidate dataset, the project must verify:

```text
class availability
license / terms of use
whether educational use is allowed
whether redistribution is allowed
image quality
label reliability
class balance
```

The target molossoid class plan is documented in:

```text
data/molossoid_visual_target_classes.csv
```

The final class list must depend on real dataset availability. The project should not assume that every desired molossoid breed exists in every dataset.

---

## Local Folder Structure

The local image dataset should be created under an ignored folder:

```text
data/images/local_dataset/
```

Recommended local structure:

```text
data/images/local_dataset/
├── downloads/
│   └── original downloaded archives or extracted datasets
├── raw/
│   ├── cane_corso/
│   ├── dogo_argentino/
│   ├── presa_canario/
│   ├── great_dane/
│   └── ...
├── processed/
│   ├── cane_corso/
│   ├── dogo_argentino/
│   ├── presa_canario/
│   ├── great_dane/
│   └── ...
├── splits/
│   ├── train/
│   ├── validation/
│   └── test/
└── manifests/
    └── local_image_manifest.csv
```

The local folder is ignored by Git. It can exist on the developer machine, but images should not be committed.

---

## Preparation Commands

Create the local folder structure:

```powershell
python src/prepare_image_dataset_structure.py
```

Validate the local structure and metadata templates:

```powershell
python src/validate_local_image_dataset.py
```

This validation is structural. It does not prove image quality and does not train a model.

---

## Local Inventory Template

The project includes an inventory template:

```text
data/image_dataset_local_inventory_template.csv
```

Use it to document any locally downloaded dataset:

```text
dataset_name
source_url_or_reference
local_storage_path
class_list_checked
terms_checked
allowed_for_education
download_date
notes
```

The inventory file is a lightweight planning template. It is not a substitute for checking the official dataset terms.

---

## Responsible Train / Validation / Test Split

When real image files are available, the future model should separate data into:

```text
train
validation
test
```

The same individual dog should not appear across train and test if the project later uses owner-provided photos. Otherwise, the model may memorize the individual dog instead of learning class-level visual features.

Recommended baseline split:

```text
70% train
15% validation
15% test
```

The split must be documented in a manifest before training.

---

## Minimum Baseline Rule

For an early educational baseline, the project should avoid too many visual classes. A smaller and cleaner class set is better than many noisy classes.

Recommended first baseline:

```text
Cane Corso
Dogo Argentino
Presa Canario
Great Dane
Boxer or Bullmastiff
Other / Unknown, if properly designed
```

If the public dataset does not contain enough reliable examples for a class, that class should remain planned rather than forced.

---

## Step 13 Boundary

Step 13 adds:

```text
local acquisition instructions
local folder structure
local validation scripts
local inventory template
responsible image-data rules
```

Step 13 does not add:

```text
actual downloaded image datasets
private owner images
scraped web images
a trained Computer Vision model
breed-proof claims
```

Future training should happen only after the dataset source, class labels, local structure and usage terms are verified.

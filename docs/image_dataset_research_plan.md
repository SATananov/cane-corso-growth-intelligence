# Image Dataset Research Plan

## Goal

This document explains where the future visual similarity module can get training data.

The user does not currently have a private image dataset. Therefore the project should start with public datasets for research and baseline experiments, then later add a consent-based USG image dataset only when permitted images are available.

---

## Public Dataset Candidates

### 1. Stanford Dogs Dataset

Use case:

```text
baseline dog breed image classification and transfer learning
```

Known public description:

- 120 dog breeds;
- 20,580 images;
- built using ImageNet images and annotations;
- class labels and bounding boxes are provided.

Project use:

```text
candidate baseline dataset, subject to class coverage and usage terms
```

Source references:

```text
https://vision.stanford.edu/aditya86/StanfordDogs/
https://www.tensorflow.org/datasets/catalog/stanford_dogs
```

---

### 2. Kaggle Dog Breed Identification

Use case:

```text
competition-style dog breed classifier baseline
```

Known public description:

- 120 dog breeds;
- training and test JPEG image sets;
- commonly used in ML tutorials and competitions.

Project use:

```text
possible course-friendly Kaggle dataset if the class list and terms fit the project
```

Source reference:

```text
https://www.kaggle.com/competitions/dog-breed-identification
```

---

### 3. Tsinghua Dogs Dataset

Use case:

```text
larger fine-grained dog breed dataset, useful if target classes exist
```

Known public description:

- 130 dog breeds;
- 70,428 real-world images according to the publication;
- bounding boxes for whole dog body and head;
- at least 200 images per breed.

Project use:

```text
strong candidate for a future fine-grained visual similarity model, subject to access, terms and class coverage
```

Source references:

```text
https://cg.cs.tsinghua.edu.cn/ThuDogs/
https://link.springer.com/article/10.1007/s41095-020-0184-6
```

---

### 4. Oxford-IIIT Pet Dataset

Use case:

```text
well-documented image-classification learning dataset
```

Known public description:

- 37 pet categories;
- roughly 200 images per class;
- breed labels;
- head ROI;
- pixel-level trimap segmentation.

Project use:

```text
useful for learning segmentation/head ROI ideas, but may not contain the target molossoid classes
```

Source reference:

```text
https://www.robots.ox.ac.uk/~vgg/data/pets/
```

---

## Breed Coverage Check

Before training, the project must check whether the desired classes actually exist in the selected dataset.

Target candidate classes:

```text
cane_corso
dogo_argentino
presa_canario
great_dane
neapolitan_mastiff
bullmastiff
boxer
mastiff
other_unknown
```

If a class is missing, the project should either:

1. remove the class from the first baseline;
2. map to an available related class only if clearly documented;
3. postpone that class until a consent-based image dataset exists.

---

## Image Data Storage Rule

Do not commit large downloaded image datasets directly to GitHub.

The repository should contain:

```text
docs/computer_vision_visual_similarity_plan.md
docs/image_dataset_research_plan.md
data/image_dataset_manifest_example.csv
data/images/README.md
src/validate_image_manifest.py
```

Actual image files should remain local, or later be managed with a suitable data tool such as Git LFS or DVC if the project reaches that stage.

---

## Manifest-Based Approach

A future local dataset should be represented through a manifest CSV instead of hard-coding image paths in notebooks.

Example manifest:

```text
data/image_dataset_manifest_example.csv
```

This makes the project more maintainable and easier to validate.

---

## Responsible Dataset Rule

Allowed image sources:

- public datasets with documented source and terms;
- user's own images;
- owner-provided images with permission;
- future USG user-submitted images with clear consent.

Not allowed for a responsible project:

- random scraping from Google Images;
- Instagram/Facebook images without permission;
- breeder website images without permission;
- unclear copyright images.

---

## Current Status

Step 11 does not train an image model yet.

It creates the research, data-governance and mathematical plan needed before a future Computer Vision notebook is added.

Step 12 adds a more concrete feasibility layer:

```text
docs/image_dataset_feasibility.md
data/image_dataset_feasibility_matrix.csv
data/molossoid_visual_target_classes.csv
src/validate_image_dataset_feasibility.py
notebooks/07_image_dataset_feasibility.ipynb
```

The Step 12 decision is to verify public dataset metadata and terms before any image model training.

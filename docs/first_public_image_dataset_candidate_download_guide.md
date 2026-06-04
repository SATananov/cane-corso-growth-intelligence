# First public image dataset candidate stage — First Public Image Dataset Candidate / Download Guide

## Purpose

This stage chooses the first public image dataset candidate for the future Computer Vision part of the project.

The project is still **not training an image model** in First public image dataset candidate stage. The purpose is to document how the first public dataset candidate should be obtained and prepared locally without committing image archives or extracted image folders to repository.

## Selected First Candidate

The first candidate is:

```text
Stanford Dogs / ImageNet Dogs
```

Why this is selected first:

- it is a known public dog-breed image dataset used for fine-grained dog breed categorization;
- it has a clear class-label structure;
- it is suitable for a first educational baseline before any custom USG consent-based dataset exists;
- it lets the project practice the full image-classification workflow responsibly.

Important boundary:

```text
The dataset is selected as a first public baseline candidate, not as proof that all target molossoid classes are present.
```

Cane Corso, Dogo Argentino and Presa Canario must **not** be assumed to be available until the downloaded class labels are inspected locally.

## Responsible Use Boundary

The future visual model must be described as:

```text
visual similarity classifier
```

not as:

```text
breed proof
pedigree proof
registry proof
certificate proof
veterinary assessment
```

An image model can only estimate similarity to classes it has seen during training. A photo cannot prove origin, genetics, pedigree or official breed status.

## Local Folder Policy

Images and downloaded archives should stay local:

```text
data/images/local_dataset/downloads/stanford_dogs/
data/images/local_dataset/raw/stanford_dogs/
data/images/local_dataset/processed/stanford_dogs/
data/images/local_dataset/splits/stanford_dogs/
```

These folders are local working areas and should not be committed to repository. Local image archives and extracted folders must not be committed to repository.

repository should contain:

```text
code
documentation
small CSV manifests/checklists
notebooks explaining the process
```

repository should not contain:

```text
large image archives
raw extracted image folders
processed image arrays
training output saved artifacts
```

## Local Download Workflow

1. Read the dataset documentation.
2. Run the local folder preparation script:

```bash
python src/prepare_image_dataset_structure.py
```

3. Download or prepare the dataset only on the local machine.
4. Place the archive/extracted files under the local dataset folders.
5. Inspect labels/classes locally:

```bash
python src/inspect_stanford_dogs_local_dataset.py
```

6. Use the inspection result to decide the first baseline classes.
7. Do not train the model until the class list has been confirmed.

## What First public image dataset candidate stage Validates

First public image dataset candidate stage validates only the planning artifacts:

```bash
python src/validate_first_public_image_dataset_candidate.py
```

It checks that the selected candidate, checklist and responsible-use boundaries are documented.

## What First public image dataset candidate stage Does Not Validate

First public image dataset candidate stage does not validate:

- actual image download success;
- image quality;
- label correctness;
- class balance;
- copyright/license compatibility beyond documented caution;
- model accuracy;
- breed proof.

Those belong to later stages.

## Next Stage After This

The next logical stage is:

```text
Local Stanford Dogs class-selection stage — Local Stanford Dogs Inspection / Baseline Class Selection
```

That stage should inspect the local labels and decide which classes can be used for the first safe baseline.

# Local Stanford Dogs class-selection stage — Local Stanford Dogs Inspection / Baseline Class Selection

## Purpose

Local Stanford Dogs class-selection stage connects the public image dataset plan to a concrete local class-selection workflow.

The project still does **not** train an image model in this stage. Instead, it defines how to inspect the locally downloaded Stanford Dogs / ImageNet Dogs dataset and select only classes that are actually present.

The key rule is:

```text
Do not assume a breed class exists. Verify it from local labels/folders first.
```

## Why This Stage Is Needed

The long-term visual idea is a molossoid visual-similarity assistant, but a public dataset may not contain every desired class.

Target classes such as Cane Corso, Dogo Argentino and Presa Canario should not be claimed unless they are confirmed from a valid data source.

This stage protects the project from a common machine-learning mistake:

```text
desired class list != available training labels
```

## First Baseline Strategy

If the locally downloaded Stanford Dogs labels contain suitable classes, the first baseline should start with a small, honest subset, for example:

```text
Boxer
Bullmastiff
Great Dane
Mastiff / Tibetan Mastiff if confirmed and useful
```

This is **not** the final Cane Corso visual model. It is only a first educational Computer Vision baseline using confirmed public classes.

If Cane Corso, Dogo Argentino or Presa Canario are missing, the project should say so clearly:

```text
These classes are not confirmed in the selected public baseline dataset. Cane Corso-specific visual training is reserved for a future public dataset with verified labels or a future consent-based USG image dataset.
```

## Local Folder Expected by the Script

The inspection script checks:

```text
data/images/local_dataset/raw/stanford_dogs/
data/images/local_dataset/downloads/stanford_dogs/
```

The image folders should remain local and ignored by Git.

## Commands

Prepare the local folder structure:

```bash
python src/prepare_image_dataset_structure.py
```

Inspect current local Stanford Dogs state:

```bash
python src/inspect_stanford_dogs_local_dataset.py
```

Select baseline classes from confirmed local folders:

```bash
python src/select_stanford_dogs_baseline_classes.py
```

## Output

The class selection script writes:

```text
reports/stanford_dogs_baseline_class_selection.md
reports/stanford_dogs_baseline_class_selection.csv
```

Before the dataset is downloaded locally, the report may show zero available classes. That is acceptable at this stage.

## Responsible Boundary

A future image model should return visual-similarity probabilities only.

In short, it is visual similarity only and not breed proof.

It should not be described as:

```text
breed proof
pedigree proof
registry proof
certificate proof
veterinary diagnosis
```

## Next Stage After This

After local class availability is confirmed, the next logical stage is:

```text
Stanford Dogs local inspection stage — Baseline Image Classifier Prototype
```

That future stage may train a small educational classifier using only verified available classes.

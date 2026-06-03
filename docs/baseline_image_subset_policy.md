# Baseline Image Subset Policy

This policy defines how the first local image subset should be prepared for the Cane Corso Growth Intelligence visual-similarity extension.

## Dataset source

The first public image dataset candidate is Stanford Dogs / ImageNet Dogs.

The dataset is used as a learning baseline for image-classification workflow design. It is not a Cane Corso-specific dataset.

## Class selection

The first baseline can use only classes that are:

1. present in the local Stanford Dogs extraction;
2. confirmed by the class-selection report;
3. selected for the first baseline;
4. documented in the manifest and summary report.

If Cane Corso, Dogo Argentino or Presa Canario are not present in the public dataset, the project must not claim that the first public baseline can recognize them.

They remain future target classes for a consent-based USG dataset or another legally usable public source.

## Split policy

The first baseline subset uses a deterministic split:

- train: 70%;
- validation: 15%;
- test: 15%;
- random seed: 42.

The default maximum is intentionally small so the subset is easy to inspect and suitable for a first course prototype.

## Image storage policy

Actual images are local-only.

Do not commit:

- `.jpg`;
- `.jpeg`;
- `.png`;
- `.webp`;
- `images.tar`;
- extracted raw dataset folders;
- local train/validation/test image folders.

Commit only code, docs, notebooks, reports and CSV manifests.

## Interpretation policy

The future model may output probabilities such as:

```text
Boxer: 41%
Bullmastiff: 33%
Great Dane: 26%
```

These values must be interpreted only as similarity scores among the classes the model was trained on.

They are not proof of breed, pedigree, registry status, genetic origin or veterinary condition.

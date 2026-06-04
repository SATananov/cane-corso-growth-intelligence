# this stage — Baseline Image Classifier Training Plan

This document belongs to an optional exploratory extension outside the current core course sequence. The core course-aligned project remains the tabular growth-intelligence workflow using regression, classification, clustering, feature engineering and time-series features.

This document defines the first safe training plan for the visual similarity extension of the Cane Corso Growth Intelligence project.

The goal of this stage is **not** to claim official breed detection. The goal is to prepare a small, transparent, reproducible baseline image-classification experiment that can report visual similarity among the locally available Stanford Dogs classes selected in the previous stages.

## Current project context

The project already contains two learning directions:

1. **Tabular Growth Intelligence** — age, weight, height, engineered features, regression, classification, clustering, and growth monitoring signals.
2. **Visual Similarity Intelligence** — public dog-image dataset research, Stanford Dogs local inspection, candidate class selection, and a local baseline subset preparation workflow.

this stage connects the second direction to a future lightweight image-classification prototype.

## Training objective

The planned model should learn to classify images among the first baseline subset classes prepared from Stanford Dogs.

The intended output is a probability distribution such as:

```text
class_a: 0.62
class_b: 0.25
class_c: 0.13
```

This probability distribution must be interpreted as **visual similarity within the trained classes**, not as proof of breed identity.

## Boundary statement

The model must never be presented as:

- a pedigree detector,
- a breed certificate,
- a genetic test,
- a kennel/registry authority,
- a veterinary diagnostic tool.

The correct wording is:

> The model estimates visual similarity among the classes it was trained on. It does not prove breed, pedigree, genetic origin, health status, or official registry identity.

## Proposed model family

For the first prototype, the most reasonable approach is transfer learning using a pretrained convolutional neural network or a lightweight vision backbone.

Candidate approaches:

| Approach | Why it is suitable |
|---|---|
| MobileNetV2 / MobileNetV3 | Lightweight, fast, suitable for a course prototype |
| EfficientNet-B0 | Strong baseline, still reasonably lightweight |
| ResNet18 / ResNet50 | Classic image-classification baseline |
| Feature extractor + logistic regression | Good fallback if full deep-learning training is too heavy |

The recommended first implementation is:

```text
pretrained image backbone -> frozen feature extractor -> small classification head
```

This keeps training faster, easier to explain, and safer for a learning project.

## Input pipeline

The planned image pipeline should:

1. read the local subset manifest,
2. load images from the local split folders,
3. resize images to a fixed input size,
4. normalize pixel values using the pretrained model convention,
5. train only on the `train` split,
6. tune/observe on the `validation` split,
7. evaluate once on the `test` split.

Suggested image size for the first prototype:

```text
224 x 224
```

## Metrics

The first prototype should report:

- accuracy,
- macro F1-score,
- per-class precision,
- per-class recall,
- confusion matrix,
- a small example prediction table.

Because the dataset is small and the classes may be visually similar, macro-level metrics matter more than raw accuracy alone.

## Expected limitations

The first visual baseline will be limited by:

- small subset size,
- public dataset label quality,
- class availability in Stanford Dogs,
- image angle, lighting, crop, and pose variation,
- similarity between molossoid and large dog breeds,
- the fact that some target breeds may not exist in Stanford Dogs.

The project must explain these limitations clearly.

## Output artifacts for a future training stage

A future training stage may generate local artifacts such as:

```text
models/baseline_visual_classifier/
reports/baseline_visual_classifier_metrics.md
reports/baseline_visual_classifier_confusion_matrix.csv
reports/baseline_visual_classifier_predictions.csv
```

Large trained model weights should not be committed to the repository unless they are intentionally small and documented. The preferred rule is:

```text
the repository: code, documentation, notebooks, metrics, small CSV reports
Local only: image datasets, large model weights, raw archives
```

## Relationship to the growth module

The visual module should remain separate from the growth module at first. Later, a combined report can merge:

- growth monitoring signal,
- visual similarity signal,
- limitations and interpretation.

The combined report should still avoid any official breed, pedigree, or veterinary claim.

## this stage conclusion

this stage defines the training plan and validation boundaries. The next stage can implement a lightweight baseline training prototype, provided that the local image subset remains available and the repository remains free of large image/model artifacts.

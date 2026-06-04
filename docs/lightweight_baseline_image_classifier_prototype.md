# Step 21 — Lightweight Baseline Image Classifier Prototype

This step introduces the first real image-classification prototype for the visual-similarity extension of the Cane Corso Growth Intelligence project.

The goal is deliberately modest: train a small, explainable baseline classifier on the local Stanford Dogs subset prepared in Step 19. The prototype is not a final breed-recognition model and does not attempt to prove breed, pedigree, registry status, or genetic origin.

## Why a lightweight baseline first

A lightweight baseline is useful before deep learning because it establishes the complete machine-learning workflow:

1. load local image files from a prepared subset;
2. extract simple numerical features from each image;
3. train a supervised classifier;
4. evaluate it on validation and test splits;
5. produce metrics and prediction-probability examples;
6. document limitations before any transfer-learning model is attempted.

This is a good course-project step because it connects image data handling, feature extraction, classification, metrics, and responsible interpretation.

## Local-only image data

The image files are expected to be local-only under:

```text
data/images/local_dataset/splits/stanford_dogs_first_baseline/
  train/
  validation/
  test/
```

These images must not be committed to GitHub. The repository should only contain code, documentation, notebooks, CSV plans, and reports.

## Initial baseline classes

The first prototype uses the baseline classes selected from the local Stanford Dogs inspection. In the current local setup, the expected first baseline classes are:

```text
boxer
bullmastiff
great_dane
```

These classes are not used as a claim about Cane Corso identity. They are an educational first baseline because they are available in the public dataset and allow the image-classification workflow to be tested end-to-end.

## Feature extraction

The baseline script extracts simple numerical features from each image:

- RGB histogram features;
- per-channel mean values;
- per-channel standard deviation values;
- image aspect-ratio feature.

These are intentionally simple and interpretable. They are not expected to match a convolutional neural network, but they are suitable for a first baseline and for explaining the mathematics of feature vectors and classification.

## Model

The prototype trains a scikit-learn logistic regression classifier with standardized features. This is intentionally lightweight and easy to explain:

```text
image -> feature vector -> standardized feature vector -> classifier -> probabilities
```

The output probabilities should be interpreted as visual similarity scores among the trained classes only.

## Reports generated

Running the training script creates or updates:

```text
reports/lightweight_image_classifier_training_report.md
reports/lightweight_image_classifier_metrics.csv
reports/lightweight_image_classifier_confusion_matrix.csv
reports/lightweight_image_classifier_prediction_examples.csv
```

The reports are safe to commit because they do not contain image files or model weights.

## Boundary statement

This prototype is an educational visual-similarity model. It does not prove breed, pedigree, registry status, genetic origin, health status, or USG platform recognition. It should be presented as an exploratory ML baseline only.

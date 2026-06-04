# Lightweight image classifier prototype stage — Lightweight Baseline Image Classifier Training Report

This report records a local-only lightweight image-classification prototype.
The output is visual similarity among trained classes only; it is not breed proof, pedigree proof, registry proof, genetic proof, or veterinary advice.

## Dataset

Subset root: `C:\Users\stana\Desktop\cane-corso-growth-intelligence\data\images\local_dataset\splits\stanford_dogs_first_baseline`

## Labels

- boxer
- bullmastiff
- great_dane

## Counts by split

### train
- boxer: 56
- bullmastiff: 56
- great_dane: 56

### validation
- boxer: 12
- bullmastiff: 12
- great_dane: 12

### test
- boxer: 12
- bullmastiff: 12
- great_dane: 12

## Metrics

- train: samples=168, accuracy=0.6667, macro_f1=0.6664, weighted_f1=0.6664
- validation: samples=36, accuracy=0.4444, macro_f1=0.4410, weighted_f1=0.4410
- test: samples=36, accuracy=0.4444, macro_f1=0.4524, weighted_f1=0.4524

## Boundary

The model is a course-project baseline. It uses simple histogram/statistical image features and logistic regression.
No image files and no model weights should be committed to repository.

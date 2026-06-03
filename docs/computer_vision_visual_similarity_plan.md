# Computer Vision Visual Similarity Extension Plan

## Purpose

This document describes a future Computer Vision extension for the Cane Corso Growth Intelligence project.

The current project already works with tabular growth data: age, bodyweight, height, engineered features, classification signals, clustering, and time-series monitoring. The planned extension adds an image-based learning direction:

```text
uploaded dog image -> visual feature extractor -> breed-similarity probabilities -> responsible interpretation
```

The goal is not to prove breed identity. The goal is to create an educational **visual similarity classifier** for Cane Corso and visually related molossoid-type breeds.

Correct wording:

```text
The image is visually closest to Cane Corso among the trained classes.
```

Incorrect wording:

```text
The model proves that the dog is a Cane Corso.
```

---

## Why This Fits the Existing Project

The existing project focuses on growth intelligence:

```text
age / weight / height records -> mathematical growth profile -> monitoring signal
```

The visual extension adds a second signal:

```text
image -> visual similarity profile -> probability distribution over trained classes
```

A future combined report could show both signals side by side:

```text
Growth signal:
- current growth trajectory
- growth velocity
- z-score monitoring signal

Visual similarity signal:
- Cane Corso: 65%
- Dogo Argentino: 15%
- Presa Canario: 12%
- Great Dane: 8%

Responsible interpretation:
The result is educational and visual only. It is not pedigree proof, breed certification, genetic testing, or veterinary diagnosis.
```

---

## Data Reality

At the moment, the project does not have a private Cane Corso image dataset.

This is not a problem for the planning stage. The correct first step is to document the data strategy and evaluate public datasets before training any model.

The future data plan has two layers:

1. **Public image datasets for baseline experiments**
   - useful for learning image classification;
   - suitable for transfer-learning prototypes;
   - must be checked for breed coverage and terms of use.

2. **Future consent-based USG image dataset**
   - user-submitted or owner-provided images;
   - only with clear permission;
   - better for Cane Corso-specific visual similarity in the long term.

The project should not scrape random images from Google, Instagram, Facebook, or breeder websites without permission.

---

## Candidate Public Datasets

| Dataset | Why it is relevant | Important limitation |
|---|---|---|
| Stanford Dogs Dataset | Public fine-grained dog breed image dataset with 120 breeds and bounding-box annotations | Must verify whether the target molossoid classes are present |
| Kaggle Dog Breed Identification | Popular ML competition dataset for dog breed classification with 120 dog breeds | Kaggle account/API and competition rules may apply |
| Tsinghua Dogs Dataset | Larger fine-grained dog dataset with 130 breeds and head/body annotations | Must check download access, terms, and class names |
| Oxford-IIIT Pet Dataset | Well-documented pet image dataset with breed labels, head ROI, and segmentation | Limited breed coverage; may not contain the target molossoid classes |

Dataset research sources are summarized in:

```text
docs/image_dataset_research_plan.md
```

---

## Target Classes for the Future Module

The ideal future class set would focus on Cane Corso and visually related molossoid-type breeds:

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

The exact class list must depend on available, legally usable data. If a public dataset does not include a breed, the project should not pretend that it can train a reliable classifier for that breed.

---

## Mathematical Formulation

Let an input image be represented as:

```text
X_image
```

A pretrained convolutional or vision model transforms the image into a feature vector:

```text
h = phi(X_image)
```

A classification head maps the feature vector into logits:

```text
z = W h + b
```

The softmax function converts logits into class probabilities:

```text
p_i = exp(z_i) / sum(exp(z_j))
```

The output is a probability distribution over the trained visual classes:

```text
P(class_i | X_image)
```

Example output:

```text
Cane Corso: 0.65
Dogo Argentino: 0.15
Presa Canario: 0.12
Great Dane: 0.08
```

Interpretation:

```text
The strongest visual similarity among the trained classes is Cane Corso.
```

---

## Training Strategy

The recommended training strategy is **transfer learning**, not training a model from zero.

Possible future models:

- MobileNetV2 / MobileNetV3
- ResNet50
- EfficientNet
- Vision Transformer, if the course reaches that level

Suggested flow:

```text
public image dataset -> split train/validation/test -> pretrained model -> fine-tune classifier head -> evaluate -> explain limitations
```

Recommended metrics:

- accuracy;
- precision, recall, F1-score per class;
- confusion matrix;
- top-3 accuracy;
- calibration / confidence analysis, if taught later.

---

## Risk and Limitation Notes

Fine-grained dog breed image classification is difficult because breeds can be visually similar and images vary by:

- age stage;
- pose;
- lighting;
- camera angle;
- cropping;
- background;
- head-only vs full-body images;
- ears/tail cropping;
- body condition;
- mixed-breed appearance;
- label noise in public datasets.

Therefore the model output must always be presented as visual similarity, not as identity proof.

---

## Responsible Product Boundary

This future module must not be used as:

- breed certificate;
- pedigree proof;
- genetic test;
- official registry judgement;
- veterinary diagnosis;
- replacement for expert human review.

Correct final product wording:

```text
This model gives an educational visual similarity signal based on the classes it was trained on.
```

Incorrect final product wording:

```text
This model proves the breed of the dog from a photo.
```

---

## Future Implementation Steps

Recommended next steps:

1. verify which public datasets contain the desired molossoid breeds;
2. document terms of use and citations;
3. keep downloaded image datasets out of GitHub;
4. create a local image folder structure;
5. create an image manifest CSV;
6. train a small transfer-learning baseline;
7. add confusion matrix and top-k predictions;
8. combine the visual signal with the existing growth signal.

For now, Step 11 is intentionally a **feasibility and design step**, not a trained image model.

# Visual Similarity Class Audit Method

This document explains how the project audits image classes before training a model.

## Audit rules

A class can be used in the first baseline only if:

1. The dataset provides an explicit class label.
2. The class label is legally usable for the project context.
3. The class has enough images for train / validation / test splits.
4. The class is visually meaningful for the molossoid comparison task.
5. The documentation clearly states the limitations.

## Match levels

The audit uses the following match levels:

- `exact_target_class` — the public label directly matches the target class.
- `related_molossoid_class` — the label is not the exact target but is visually relevant for molossoid comparison.
- `negative_or_other_class` — useful as contrast / other class.
- `future_consent_required` — the target class is not available publicly and requires future consent-based data.
- `needs_local_verification` — the source is promising but the actual downloaded labels must be inspected.

## Baseline recommendation

The first image model should be a **small educational baseline**, not a production breed identification system.

Recommended baseline direction:

- Use only confirmed available classes.
- Start with 3–5 visually distinct classes.
- Keep `other_unknown` as a caution class or holdout category.
- Report probabilities as visual similarity scores.
- Do not use the output as a certificate, pedigree proof, or veterinary conclusion.

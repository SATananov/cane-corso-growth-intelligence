# Step 14 — Public Image Dataset Class Availability Audit

## Purpose

This step checks whether public dog image datasets can support the future **Molossoid Visual Similarity** module.

The goal is **not** to train an image model yet. The goal is to document which target visual classes may be available from public datasets and which classes must remain future work until a consent-based USG image dataset is collected.

## Why this step is needed

A visual classifier can only learn the classes that are actually represented in the image dataset. For a Cane Corso / molossoid comparison task, public datasets may contain common dog breeds such as Boxer, Great Dane, Bullmastiff, Mastiff, or Rottweiler, but they may not contain Cane Corso, Dogo Argentino, or Presa Canario as clean labeled classes.

Therefore, before training a model, the project performs a class availability audit.

## Target visual classes

The long-term target classes are:

- Cane Corso
- Dogo Argentino
- Presa Canario
- Great Dane
- Neapolitan Mastiff
- Bullmastiff
- Boxer
- Other / Unknown

The final baseline class list must depend on what is legally and practically available in public datasets.

## Dataset candidates

The public dataset candidates considered in this step are:

- Stanford Dogs Dataset
- Kaggle Dog Breed Identification
- Tsinghua Dogs Dataset
- Oxford-IIIT Pet Dataset

These datasets are used as **candidate public sources**. The project still treats the final class list as provisional until the actual downloaded class labels are inspected locally.

## Important safety boundary

This module must be described as **visual similarity**, not breed proof.

The output of a future model should be interpreted as:

> The image has the strongest visual similarity to a class among the trained classes.

It must not be interpreted as:

> This dog is officially proven to be this breed.

A photo cannot prove pedigree, genetic origin, registry status, health status, or official breed identity.

## Expected workflow

1. Prepare local image dataset folders using Step 13.
2. Inspect available class labels in the selected public dataset.
3. Map available class labels to the target molossoid visual classes.
4. Mark which classes are suitable for a baseline model.
5. Keep unavailable Cane Corso-specific classes as future work for a consent-based USG dataset.
6. Only after this audit, create a small baseline image classifier.

## Current conclusion

The project is ready for a **future baseline image classifier**, but the baseline must use only classes that are actually available and legally usable.

Cane Corso-specific image classification should remain a future extension unless a clean public Cane Corso class or consent-based USG dataset becomes available.

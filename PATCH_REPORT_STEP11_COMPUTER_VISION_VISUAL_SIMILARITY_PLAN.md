# Patch Report - Step 11 Computer Vision Visual Similarity Plan

## Purpose

Step 11 adds a safe Computer Vision extension plan to the Cane Corso Growth Intelligence project.

The goal is to discuss and document a future image-based visual similarity classifier without pretending that the current project already has a real Cane Corso image dataset or a trained image model.

---

## Added Files

```text
docs/computer_vision_visual_similarity_plan.md
docs/image_dataset_research_plan.md
data/images/README.md
data/image_dataset_manifest_example.csv
src/validate_image_manifest.py
notebooks/06_computer_vision_visual_similarity_concept.ipynb
```

---

## Updated Files

```text
README.md
HOW_TO_RUN.md
DATA_SOURCES.md
COURSE_TOPIC_MAPPING.md
PROJECT_BRIEF.md
```

---

## What This Step Adds

- explains how Computer Vision can be combined with the existing growth-intelligence project;
- frames the future model as visual similarity, not breed proof;
- documents public dataset candidates for baseline experiments;
- explains that the user does not currently have a private image dataset;
- adds a manifest-based image data strategy;
- adds a small manifest validation script;
- adds a concept notebook with softmax probability demonstration;
- keeps real image datasets out of GitHub.

---

## Responsible Boundary

The future image model must not be presented as:

- official breed identification;
- pedigree proof;
- genetic testing;
- registry authority;
- veterinary diagnosis.

Correct interpretation:

```text
The model returns an educational visual similarity signal among the trained classes.
```

---

## Validation

Recommended local checks:

```powershell
python src/validate_image_manifest.py
python src/create_time_series_features.py
python src/run_growth_assessment.py
```

Expected status:

```text
Image manifest validation: PASS
Created time-series feature dataset
Created practical growth assessment workflow outputs
```

---

## Status

```text
Step 11 Computer Vision Visual Similarity Plan: READY FOR LOCAL VALIDATION
```

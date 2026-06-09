# Step 20 Patch Notes — Dimensionality Reduction and Manifold Learning

This patch turns the previous future-topic placeholder into a complete lightweight course-aligned module for Dimensionality Reduction.

## What this adds

- PCA with scaling and explained variance analysis
- Kernel PCA for non-linear projections
- Linear Discriminant Analysis (LinDA) as supervised dimensionality reduction
- Isomap / isometric mapping for manifold learning
- t-SNE for visualization-only embedding
- Low-variance and high-correlation feature audit
- Random Forest feature importance as feature selection support
- TF-IDF + TruncatedSVD alignment with the course exercise on text representation
- Lightweight validation script and generated CSV/Markdown reports

## Files added or updated

- `notebooks/06_dimensionality_reduction_future_course_topic.ipynb` — upgraded from placeholder to real topic notebook
- `notebooks/06_1_dimensionality_reduction_exercise_project_alignment.ipynb`
- `src/run_dimensionality_reduction_and_manifold_learning.py`
- `src/validate_dimensionality_reduction_and_manifold_learning.py`
- `docs/dimensionality_reduction_notes.md`
- `docs/course_exercises/dimensionality_reduction_exercise_alignment.md`
- `data/course_exercises/dimensionality_reduction_exercise_requirements.csv`
- `reports/course_exercises/dimensionality_reduction_*`

## Safety rules followed

- No external downloads
- No Kaggle data included
- No images, model weights, datasets, `.env`, cache, or binary artifacts
- Uses only small built-in / synthetic examples from scikit-learn
- Suitable for GitHub and final course submission

# Machine Learning Tools Exercise Alignment

This document records how Step 21 applies the Machine Learning Tools exercise to the Cane Corso Growth Intelligence project.

## Scope

The original exercise is framed around a real/fake job posts dataset. This project keeps its own domain and applies the same best-practice ideas to the processed public dog-growth sample. The goal is not to change the project story, but to improve reproducibility, configurability, tracking, model comparison, persistence and documentation.

## Implemented artifacts

| Exercise area | Project artifact |
|---|---|
| Project structure | `src/`, `configs/`, `models/`, `reports/`, `tests/`, `docs/`, `notebooks/` |
| One-line run | `python app.py --config configs/machine_learning_tools_config.json` |
| Configurable settings | `configs/machine_learning_tools_config.json` |
| Text representation comparison | `text_tfidf_sparse_logistic` vs `text_tfidf_svd_dense_logistic` |
| Dimensionality reduction comparison | TruncatedSVD dense representation compared against sparse TF-IDF |
| Model comparison | Logistic Regression and Random Forest metadata pipelines |
| Experiment tracking | MLflow logging when available; fallback manifest in `reports/machine_learning_tools/mlflow_tracking_manifest.json` |
| Data governance / pipeline tracking | `dvc.yaml` stage and DVC note |
| Model persistence | `models/machine_learning_tools/best_growth_status_pipeline.joblib` |
| Smoke test | `python tests/smoke_test_machine_learning_tools.py` |
| Model card | `reports/machine_learning_tools/model_card_growth_status.md` |

## Commands

```bash
python app.py --config configs/machine_learning_tools_config.json
python src/validate_machine_learning_tools_outputs.py
python tests/smoke_test_machine_learning_tools.py
```

## Responsible-use boundary

The model predicts an educational binary growth-status proxy signal from a processed public dog-growth sample. It is not veterinary advice, diagnosis, pedigree proof, certification, or a replacement for professional evaluation.

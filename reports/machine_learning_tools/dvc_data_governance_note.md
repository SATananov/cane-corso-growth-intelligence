# Step 21 Data Governance and DVC Note

The exercise asks to track data versions and pipelines with DVC. This project includes a lightweight `dvc.yaml` stage for the Machine Learning Tools workflow.

The stage is intentionally small and clean-clone friendly:

```bash
dvc repro machine_learning_tools
```

Expected command behind the stage:

```bash
python app.py --config configs/machine_learning_tools_config.json
```

The committed processed dataset is used as input. Large raw datasets and real image datasets remain excluded from GitHub and should be handled through local storage or a proper DVC remote in a real production workflow.

Current best pipeline: `text_tfidf_sparse_logistic`

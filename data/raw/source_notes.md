# Raw Data Folder Notes

This folder is reserved for manually downloaded raw public datasets.

The original public dog growth dataset is distributed as a compressed archive. In this project, that file is referred to as the **raw dataset archive**:

```text
data/raw/Final_Data_PLOS.zip
```

The raw dataset archive is used only as the original source input for the processing scripts. It should stay local and should not be committed to GitHub.

The notebooks currently use processed CSV samples from:

```text
data/processed/
```

See these documents for the full source and workflow explanation:

```text
docs/real_data_download_instructions.md
docs/raw_dataset_archive_policy.md
docs/real_data_source_notes.md
```

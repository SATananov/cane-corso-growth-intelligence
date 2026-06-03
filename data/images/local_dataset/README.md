# Local Image Dataset Folder

This folder is reserved for local Computer Vision image datasets.

It is intentionally ignored by Git. Do not commit downloaded public datasets, private owner images, or consent-based image submissions to the repository.

Use the preparation script from the project root:

```powershell
python src/prepare_image_dataset_structure.py
```

Then validate the local structure:

```powershell
python src/validate_local_image_dataset.py
```

This folder is for local experimentation only. The committed project should contain code, documentation and lightweight metadata templates, not large image files.

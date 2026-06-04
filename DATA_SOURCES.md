# Data Sources

This file documents the datasets used in the project and explains how prototype, raw, and processed data are separated.

The project is intentionally transparent about its data foundation. It does not claim to use private Cane Corso veterinary records. It uses a small educational prototype dataset and a real public dog growth dataset.

---

## 1. Prototype Dataset

File:

```text
data/prototype/cane_corso_growth_sample.csv
```

This is a small educational dataset created for the first machine-learning experiments.

It includes sample Cane Corso-style growth measurements such as:

- dog id
- dog name
- sex
- age in months
- weight in kilograms
- height in centimeters
- activity level
- source type

This dataset is not real veterinary data. It is used only for learning, testing, and early regression experiments.

---

## 2. Real Public Dataset Source

The project uses a real public dog growth dataset as the foundation for later experiments.

Dataset title:

```text
Growth standard charts for monitoring bodyweight in dogs of different sizes - SUPPORTING DATA
```

Source:

```text
University of Liverpool DataCat: The Research Data Catalogue
```

Dataset DOI:

```text
https://doi.org/10.17638/datacat.liverpool.ac.uk/377
```

Related publication:

```text
Growth standard charts for monitoring bodyweight in dogs of different sizes
PLOS ONE, 2017
```

The source dataset is relevant because it contains dog age and bodyweight information and is connected to public research on dog growth standards. This fits the project motivation because growth monitoring depends on repeated age and bodyweight records, especially when the goal is to compare measured development with expected patterns.

Important project interpretation:

```text
The public dataset provides a real dog-growth data foundation.
The Cane Corso domain provides the practical product context.
The project does not claim that the public dataset is a private Cane Corso-only dataset.
```

---

## 3. Why This Dataset Instead of Kaggle?

Kaggle is a useful place to search for datasets, and it was considered as a possible source during the project planning. However, the project does not only need general dog data. It needs data that supports a mathematical growth-monitoring problem.

A random dog-related dataset may focus on images, breed descriptions, adoption records, synthetic wellness examples or general metadata. Those datasets may be useful for other tasks, but they do not necessarily support age/bodyweight growth modelling.

The University of Liverpool DataCat / PLOS ONE dataset was selected because it is directly connected to dog bodyweight growth standards and contains the type of information needed for growth-related machine-learning experiments.

Dedicated explanation:

```text
docs/dataset_selection_rationale.md
```

Main project boundary:

```text
Real public dog-growth dataset = data foundation.
Cane Corso Growth Intelligence = domain and product context.
```

---


## 4. Future Image Data Source Plan

The project now documents a future Computer Vision extension, but it does not currently include a private Cane Corso image dataset and it does not train an image model yet.

Planned visual task:

```text
dog image -> visual similarity probabilities over trained classes
```

Candidate public datasets for future baseline experiments include:

- Stanford Dogs Dataset;
- Kaggle Dog Breed Identification;
- Tsinghua Dogs Dataset;
- Oxford-IIIT Pet Dataset.

The exact class list must be verified before training. The project should not assume that every desired molossoid breed exists in every public dataset.

Target candidate classes for future research:

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

Responsible image data rule:

```text
Use public datasets with documented terms, user's own images, or owner-provided images with permission.
Do not scrape random Google, Instagram, Facebook, or breeder-site images without permission.
```

Supporting files:

```text
docs/computer_vision_visual_similarity_plan.md
docs/image_dataset_research_plan.md
data/image_dataset_manifest_example.csv
data/images/README.md
src/validate_image_manifest.py
```

---



## 5. Local Image Dataset Acquisition and Preparation

The local-only preparation workflow defines how future image datasets should be organized.

Local image root:

```text
data/images/local_dataset/
```

This folder is ignored by Git and should be used only on the developer machine for downloaded public datasets or future consent-based images.

Supporting files:

```text
docs/image_dataset_acquisition_and_local_preparation.md
data/image_dataset_local_inventory_template.csv
src/prepare_image_dataset_structure.py
src/validate_local_image_dataset.py
notebooks/10_image_dataset_acquisition_local_preparation.ipynb
```

Important rule:

```text
Do not commit downloaded image datasets, private owner images, or scraped web images to GitHub.
```

The current project still contains no committed image dataset and no trained image model. The preparation workflow defines the acquisition process and local structure only.

---

## 6. Raw Dataset Archive Rule

The full original dataset should not be committed directly to GitHub.

The public source distributes the original data as a compressed archive. In this project, that file is called the **raw dataset archive**:

```text
data/raw/Final_Data_PLOS.zip
```

This term means only the original public dataset distribution file. It is not part of the repository contents and is kept local when large image data is used.

Reasons for keeping the raw dataset archive local only:

- it is an external public dataset;
- the repository should stay lightweight;
- the source should remain clearly attributed;
- only project-specific processed samples should be committed;
- the final clean project submission should not contain large raw downloaded archives.

The repository should keep only lightweight source notes in `data/raw/`, such as:

```text
data/raw/source_notes.md
```

The raw dataset archive and any original source metadata files should remain local and ignored by Git.

A dedicated explanation is available in:

```text
docs/raw_dataset_archive_policy.md
```

---

## 7. General Processed Real Public Sample

File:

```text
data/processed/dog_growth_public_sample.csv
```

Sample size:

- 10,000 rows
- 12 columns

Created by:

```text
src/create_public_sample.py
```

This script reads the large raw CSV from the local raw dataset archive in chunks and creates a smaller processed sample.

The processed sample keeps project-useful columns related to:

- breed identifier
- dog identifier
- gender
- age at visit
- bodyweight
- body condition information
- preventive care visit flag
- healthy pet diagnosis flag
- average adult breed weight

It also adds:

- `visit_age_months`
- `source_type`

Source label:

```text
real_public_processed_sample
```

This sample is committed to GitHub because it is small and usable for notebook experiments.

---

## 8. Classification-Focused Processed Sample

File:

```text
data/processed/dog_growth_classification_sample.csv
```

Sample size:

- 10,000 rows
- 15 columns

Created by:

```text
src/create_classification_sample.py
```

This sample was created specifically for the Classification topic.

It keeps rows with usable body condition score information and creates the classification target:

```text
growth_status
```

Target classes:

- `normal_growth`
- `needs_attention`

Binary target:

- `0` = `normal_growth`
- `1` = `needs_attention`

Class balance:

- 5,000 `normal_growth` records
- 5,000 `needs_attention` records

Source label:

```text
real_public_classification_sample
```

This balanced sample is used in:

```text
notebooks/03_classification_growth_status.ipynb
notebooks/03_1_classification_pipeline_exercise.ipynb
```

---

## 8. Time-Series Feature Sample

File:

```text
data/processed/cane_corso_time_series_features.csv
```

Created by:

```text
src/create_time_series_features.py
```

This sample supports the Feature Engineering and Time Series stage. It contains engineered measurements such as lag features, weight gain, height gain, growth velocity, weight-to-height ratio, rolling average weight and z-score based monitoring signals.

This file is used in:

```text
notebooks/05_feature_engineering_time_series_growth.ipynb
```

---

## 8. Why This Data Choice Is Useful

The project is stronger than a fully synthetic exercise because it has:

- a personally meaningful Cane Corso product case;
- a real public dog-growth data foundation;
- documented source attribution;
- processed samples small enough for reproducible notebooks;
- a clear distinction between prototype data, raw external data and processed public samples.

This allows the project to stay honest while still being useful and interesting.

---

## 9. Data Ethics and Limitations

The project does not attempt to identify clients, owners, animals, or clinics.

The data is used only for educational machine-learning experiments.

The project does not provide veterinary diagnosis. Model outputs should be interpreted as growth-monitoring signals for analysis and learning, not as medical conclusions.


## Stanford Dogs Baseline Class Selection

The class-selection workflow documents how the local Stanford Dogs candidate classes are selected.

The project now documents likely baseline candidates such as Boxer, Bullmastiff and Great Dane, but still requires local label inspection before any class is used for training.

Supporting files:

```text
docs/local_stanford_dogs_inspection_baseline_class_selection.md
docs/baseline_visual_class_selection_policy.md
data/stanford_dogs_baseline_class_candidates.csv
data/stanford_dogs_baseline_class_selection_template.csv
src/select_stanford_dogs_baseline_classes.py
src/validate_stanford_baseline_class_selection.py
```

Important rule:

```text
Desired target classes must not be treated as available training classes until verified from local labels or a documented data source.
```


## Stanford Dogs Local Download Boundary

Stanford Dogs / ImageNet Dogs remains the first public image dataset candidate for the Computer Vision branch.

The local-only download and inspection workflow documents the real Stanford Dogs files inspected on the developer machine. It does not include image files in the repository and does not assume that any desired molossoid class is available until local class folders are inspected.

Large image archives must be downloaded only with explicit user action and kept under ignored local dataset folders.

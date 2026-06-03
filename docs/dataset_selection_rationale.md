# Dataset Selection Rationale: Why Liverpool DataCat Instead of Kaggle?

This document explains why the project uses the University of Liverpool DataCat / PLOS ONE public dog growth dataset as the main real-data foundation instead of selecting a general dog dataset from Kaggle.

---

## Short Answer

Kaggle is a useful place to search for public datasets, and it was considered as a possible source. However, for this project the most important requirement is not simply "dog data". The project needs data related to **dog growth over time**, especially age and bodyweight records.

The selected University of Liverpool DataCat dataset is more directly aligned with the project because it is connected to published research on dog bodyweight growth standards.

---

## Project Data Need

The project is about mathematical growth monitoring. This means the data should support questions such as:

```text
How does bodyweight change with age?
Can a measured record be compared with an expected growth pattern?
Can repeated measurements be transformed into growth velocity, lag features and monitoring signals?
```

For these questions, a suitable dataset should contain at least:

- dog age or visit age;
- bodyweight;
- enough records to support modelling and sampling;
- clear source attribution;
- a connection to growth monitoring or bodyweight standards.

---

## Why Not Use a Random Kaggle Dataset?

Kaggle can contain many dog-related datasets, but a dataset being about dogs does not automatically make it suitable for this project.

Many public dog datasets are focused on different tasks, for example:

- image classification;
- breed descriptions;
- breed-size tables;
- adoption records;
- synthetic pet wellness examples;
- general pet metadata.

Those datasets can be useful for other machine-learning tasks, but they are not necessarily the best foundation for modelling growth curves, bodyweight development, age-based changes, residuals, growth velocity or time-series features.

The project therefore uses Kaggle as a useful search idea, but not as the selected main source.

---

## Why the Liverpool DataCat / PLOS ONE Source Fits Better

Selected source:

```text
Growth standard charts for monitoring bodyweight in dogs of different sizes - SUPPORTING DATA
University of Liverpool DataCat
https://doi.org/10.17638/datacat.liverpool.ac.uk/377
```

Related publication:

```text
Growth standard charts for monitoring bodyweight in dogs of different sizes
PLOS ONE, 2017
https://doi.org/10.1371/journal.pone.0182064
```

This source fits the project because it is directly connected to:

- dog bodyweight;
- age-related growth monitoring;
- growth standards;
- public research data;
- clear academic attribution.

This makes it a stronger foundation than a general dog dataset that may not contain the growth information required by the project.

---

## Honest Project Boundary

The project should describe the data foundation like this:

```text
This project uses a real public dog growth dataset and applies the workflow to the Cane Corso Growth Intelligence idea.
```

The project should not describe the data foundation like this:

```text
This project is trained on private real Cane Corso veterinary records.
```

The Cane Corso part is the domain and product context. The public dataset is the real dog-growth data foundation used for learning, experiments and demonstration.

---

## Future Data Direction

A stronger future version of the project can add a Cane Corso-specific longitudinal dataset collected responsibly over time.

A useful future data table would include:

```text
dog_id
measurement_date
age_weeks
sex
weight_kg
height_cm
activity_level
food_type
notes
vet_confirmed_status_optional
```

This would allow the project to move from a general public dog-growth foundation toward a more breed-focused growth-monitoring model.

---

## Final Reasoning

The dataset choice is intentional:

```text
Kaggle was considered as a general dataset search option.
The selected Liverpool DataCat / PLOS ONE source was chosen because it is more directly connected to the mathematical problem of dog growth monitoring.
```

This keeps the project academically honest, mathematically aligned and easier to defend during review.

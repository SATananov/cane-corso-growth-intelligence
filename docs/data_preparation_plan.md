# Data Preparation Plan

This document describes how the project separates prototype data, raw external data and processed public samples.

---

## 1. Data Layers

The project uses three data layers.

### Prototype Data

```text
data/prototype/cane_corso_growth_sample.csv
```

A small educational dataset used for the first regression experiments.

### Raw Public Data

```text
data/raw/
```

The local folder where external source files can be placed manually.

Raw files should not be committed to repository or included in the final clean project submission.

### Processed Public Data

```text
data/processed/dog_growth_public_sample.csv
data/processed/dog_growth_classification_sample.csv
```

Smaller samples created from the real public dog growth dataset for notebook experiments.

---

## 2. Preparation Workflow

### Stage 1: Keep the raw dataset archive locally

The original public dataset is distributed as a compressed archive. In this project, that file is called the **raw dataset archive**.

Expected local path:

```text
data/raw/Final_Data_PLOS.zip
```

This is a normal dataset-distribution format, not a project update or clean local backup archive.

The original large file should stay local.

### Stage 2: Inspect the raw data

Check:

- available files;
- column names;
- number of rows;
- missing values;
- age-related columns;
- weight-related columns;
- body condition columns;
- category columns.

### Stage 3: Select useful columns

Useful columns are related to:

- dog age;
- body weight;
- sex;
- breed or breed-size identifier;
- body condition information;
- adult breed weight information;
- health-related flags if available.

### Stage 4: Clean the data

Cleaning may include:

- removing rows with missing age or weight;
- converting age to months;
- checking unrealistic values;
- renaming columns for clarity;
- keeping a consistent source label.

### Stage 5: Create processed samples

The project creates:

```text
data/processed/dog_growth_public_sample.csv
```

for general experiments and:

```text
data/processed/dog_growth_classification_sample.csv
```

for classification experiments.

### Stage 6: Use the processed samples in notebooks

The processed samples are small enough for reproducible notebooks and repository.

---

## 3. Classification Target Preparation

The classification stage creates:

```text
growth_status
```

with classes:

```text
normal_growth
needs_attention
```

The labels are educational machine-learning labels based on available body-condition information. They are not veterinary diagnosis labels.

---

## 4. Future Feature Engineering

Future notebooks can create features such as:

```text
body_ratio = weight_kg / height_cm
```

```text
growth_velocity = delta_weight / delta_time
```

```text
deviation_from_expected = actual_weight - predicted_expected_weight
```

```text
relative_deviation = deviation_from_expected / predicted_expected_weight
```

These features will make the project more mathematical and useful because they represent growth as a process, not only as a static row.

---

## 5. Important Rule

The project must always clearly distinguish between:

- prototype educational data;
- raw external public data;
- processed public data samples;
- product interpretation for the Cane Corso domain.

This distinction protects the academic integrity of the project.

---

## 6. Why This Stage Matters

Using real public data makes the project stronger and more realistic.

However, the project must be honest about the data source and must avoid unsafe claims.

Correct statement:

```text
The project uses public dog growth data as a foundation for a Cane Corso-oriented growth intelligence concept.
```

Incorrect statement:

```text
The project uses private Cane Corso veterinary records.
```

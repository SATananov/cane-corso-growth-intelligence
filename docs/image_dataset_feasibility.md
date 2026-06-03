# Step 12: Public Image Dataset Feasibility

## Purpose

This document evaluates whether public dog image datasets can support a future **Molossoid Visual Similarity Classifier** inside the Cane Corso Growth Intelligence project.

The project does not currently have a private Cane Corso image dataset. Therefore, the responsible first step is not model training. The responsible first step is to check public dataset candidates, class coverage, access rules, repository storage policy and limitations.

The future visual model must be framed as:

```text
image -> visual features -> similarity probabilities -> educational interpretation
```

It must not be framed as:

```text
image -> official breed proof
```

---

## Public Dataset Candidates

The feasibility matrix is stored in:

```text
data/image_dataset_feasibility_matrix.csv
```

The current candidates are:

| Dataset | Why it matters | Current project decision |
|---|---|---|
| Stanford Dogs | common fine-grained dog-breed benchmark with 120 breeds and 20,580 images | strong baseline candidate, but class coverage must be verified locally |
| Tsinghua Dogs | larger fine-grained dataset with 130 dog breeds and 70,428 images | strong candidate if access, terms and target classes fit |
| Oxford-IIIT Pet | well documented 37-category pet dataset with breed labels and annotations | useful for learning image classification, but likely too limited for molossoid class coverage |
| Kaggle Dog Breed Identification | course-friendly dog-breed competition dataset with 120 breed classes | useful Kaggle baseline candidate, subject to Kaggle terms and exact class list |

Source references are kept as URLs inside the feasibility matrix and in `docs/image_dataset_research_plan.md`.

---

## Target Molossoid / Related Classes

The target class plan is stored in:

```text
data/molossoid_visual_target_classes.csv
```

The future project would ideally compare classes such as:

```text
cane_corso
dogo_argentino
presa_canario
great_dane
neapolitan_mastiff
bullmastiff
boxer
dogue_de_bordeaux
other_unknown
```

However, Step 12 does **not** claim that all these classes are available in every public dataset.

The class list for each candidate dataset must be checked from the dataset metadata before training.

---

## Feasibility Rules

### Rule 1: No random image scraping

The project should not use random images from Google Images, Instagram, Facebook, breeder websites or social media posts without permission.

### Rule 2: GitHub stores metadata, not image archives

The repository should contain:

```text
code
docs
notebooks
small CSV manifests
validation scripts
```

It should not contain large downloaded image folders.

Actual image datasets should remain local or later be managed through a suitable data versioning strategy such as Git LFS or DVC if needed.

### Rule 3: Dataset terms must be checked

Before using any public image dataset, the project should check:

- access method;
- license or usage terms;
- whether redistribution is allowed;
- whether course/demo use is allowed;
- whether images can be committed to GitHub.

### Rule 4: Missing target classes are not a failure

If public datasets do not contain all desired molossoid classes, the baseline model should use only the classes that are available and clearly document the limitation.

For example:

```text
baseline public dataset classes -> educational classifier
future USG consent-based images -> Cane Corso-focused extension
```

---

## Step 12 Decision

Step 12 adds feasibility documentation and validation, but it intentionally does not train a visual model yet.

The correct next step after Step 12 is:

```text
Step 13: Download / metadata verification instructions for the selected public image dataset
```

Only after the class list and terms are verified should the project move to a baseline Computer Vision model.

---

## Responsible Interpretation Boundary

Future output should look like this:

```text
Visual similarity probabilities:
Cane Corso: 0.65
Dogo Argentino: 0.20
Great Dane: 0.10
Other / Unknown: 0.05
```

Interpretation:

```text
The uploaded image has the strongest visual similarity to the Cane Corso class among the trained classes.
```

It must not say:

```text
This dog is officially a Cane Corso.
```

The future module cannot prove breed, pedigree, genetics, registry status or health condition from an image.

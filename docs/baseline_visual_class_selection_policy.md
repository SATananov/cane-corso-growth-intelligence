# Baseline Visual Class Selection Policy

## Principle

The project should select visual classes from evidence, not from wishful thinking.

A class can be used in an image classifier only if it satisfies all of the following:

1. the class label exists in the selected dataset;
2. the local folder or metadata can be inspected;
3. there are enough images for a small baseline experiment;
4. the label meaning is documented;
5. the result is described as visual similarity only and not breed proof.

## Allowed First-Baseline Class Types

For the first public Stanford Dogs baseline, useful classes may include:

```text
confirmed molossoid-like classes
confirmed large-breed contrast classes
confirmed control classes that help explain visual separation
```

Examples that may be usable if confirmed locally:

```text
Boxer
Bullmastiff
Great Dane
Mastiff / Tibetan Mastiff
```

## Missing Target Classes

If a desired class such as Cane Corso, Dogo Argentino or Presa Canario is missing from the selected public dataset, the project should not invent it.

Correct wording:

```text
This class is not confirmed in the selected public baseline dataset.
```

Incorrect wording:

```text
The model can recognize Cane Corso even without Cane Corso training images.
```

## Minimum Baseline Recommendation

A small educational baseline should use at least two confirmed classes. A more useful baseline should use three to five confirmed classes.

The goal is not production accuracy. The goal is to demonstrate:

```text
image tensor -> class labels -> probability vector -> responsible interpretation
```

## GitHub Policy

Do not commit:

```text
raw image folders
large image archives
processed image arrays
trained model checkpoints
```

Commit only:

```text
documentation
scripts
notebooks
small CSV manifests
small generated reports
```

# Stanford Dogs Real Class Inspection Protocol

## Inspection Goal

The goal is to inspect local folders after Stanford Dogs is downloaded and extracted.

The project checks:

- whether a local Stanford Dogs raw folder exists
- how many image-containing class folders are present
- which folder names match the Step 16 baseline candidate aliases
- which classes are safe to consider for the first baseline

## Evidence-Based Class Rule

A class is not used because it is desired. It is used only if it is locally confirmed.

For example:

```text
Cane Corso desired != Cane Corso available
```

If Cane Corso is not present in Stanford Dogs, the project keeps Cane Corso-specific visual classification as a future dataset task.

## First Baseline Rule

The first image baseline should use only locally confirmed and reviewed classes.

A possible first baseline may include broad dog-breed contrast classes such as Boxer, Bullmastiff or Great Dane only if their class folders are actually detected locally.

## No Images in GitHub

Only scripts, manifests, reports and notebooks belong in GitHub.

Downloaded images and archives stay local.

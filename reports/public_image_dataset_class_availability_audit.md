# Public Image Dataset Class Availability Audit

This report validates the class-availability planning data for the future visual similarity module.

## Candidate rows by dataset

- Future USG Consent Dataset: 3
- Kaggle Dog Breed Identification: 2
- Oxford-IIIT Pet: 3
- Stanford Dogs: 4
- Tsinghua Dogs: 3

## Candidate rows by target class

- boxer: 3
- bullmastiff: 1
- cane_corso: 2
- dogo_argentino: 2
- great_dane: 2
- other_unknown: 3
- presa_canario: 2

## First baseline usability flags

- future: 3
- no_until_confirmed: 3
- optional: 2
- yes: 1
- yes_if_confirmed: 6

## Target audit rules

- cane_corso: future_consent_required_unless_public_exact_class_confirmed — Main USG visual context; do not fake availability if public dataset lacks a clean class.
- dogo_argentino: future_consent_required_unless_public_exact_class_confirmed — Important molossoid comparison class.
- presa_canario: future_consent_required_unless_public_exact_class_confirmed — Important molossoid comparison class.
- great_dane: use_if_public_class_confirmed — Large dog comparison class; visually distinct and useful for baseline.
- bullmastiff: use_if_public_class_confirmed — Related mastiff-type comparison class.
- boxer: use_if_public_class_confirmed — Common public dataset class and useful contrast.
- other_unknown: use_with_caution — Avoid forcing every image into a target breed; supports uncertainty handling.

## Optional local class directory inspection

No local class directory was provided. This is expected before downloading a public image dataset.

## Interpretation

This audit supports planning only. It does not download images, train a model, prove dataset quality, or prove breed identity from a photo.

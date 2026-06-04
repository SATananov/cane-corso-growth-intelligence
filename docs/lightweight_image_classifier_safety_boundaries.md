# Lightweight Image Classifier Safety Boundaries

The Step 21 classifier must stay within strict educational boundaries.

## Allowed interpretation

The classifier may say:

```text
This image is most visually similar to class X among the trained classes.
```

It may also report probabilities such as:

```text
boxer: 72%
bullmastiff: 18%
great_dane: 10%
```

These probabilities are model outputs for the trained classes only.

## Not allowed interpretation

The classifier must not claim:

- the dog is officially a certain breed;
- the dog has a certain pedigree;
- the dog has a genetic origin proven by image;
- the dog is eligible for any certificate or registry;
- the result is a veterinary or expert judgment.

## Dataset limitations

The first baseline uses public Stanford Dogs classes that are available locally. This means the first model may not include Cane Corso, Dogo Argentino, or Presa Canario if those classes are not present in the selected public dataset.

That limitation is acceptable because this step is about proving the image-classification workflow, not creating a final Cane Corso recognition system.

## Future direction

A future stronger version may use transfer learning and a consent-based USG image dataset. Until that data exists, Cane Corso-specific visual similarity must remain a future goal.

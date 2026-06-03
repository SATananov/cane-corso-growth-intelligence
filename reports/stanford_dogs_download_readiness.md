# Stanford Dogs Local Download Readiness

Download root: `C:\Users\stana\Desktop\cane-corso-growth-intelligence\data\images\local_dataset\downloads\stanford_dogs`
Raw root: `C:\Users\stana\Desktop\cane-corso-growth-intelligence\data\images\local_dataset\raw\stanford_dogs`

## Actions

| Artifact | Status | Exists after | Reason | Final URL | Local path |
|---|---|---:|---|---|---|
| stanford_dogs_readme | downloaded | True | download_small_requested | `http://vision.stanford.edu/aditya86/ImageNetDogs/README.txt` | `data\images\local_dataset\downloads\stanford_dogs\README.txt` |
| stanford_dogs_lists | downloaded | True | download_small_requested | `http://vision.stanford.edu/aditya86/ImageNetDogs/lists.tar` | `data\images\local_dataset\downloads\stanford_dogs\lists.tar` |
| stanford_dogs_images | planned_only | False | not_requested | `http://vision.stanford.edu/aditya86/ImageNetDogs/images.tar` | `data\images\local_dataset\downloads\stanford_dogs\images.tar` |
| stanford_dogs_annotations | planned_only | False | not_requested | `http://vision.stanford.edu/aditya86/ImageNetDogs/annotation.tar` | `data\images\local_dataset\downloads\stanford_dogs\annotation.tar` |

## Extraction

- Images extraction status: `not_requested`
- Annotations extraction status: `not_requested`
- Lists extraction status: `extracted`

## Download safety note

This script does not disable SSL verification. If the Stanford HTTPS endpoint fails on a local Python/Windows environment because of a certificate hostname mismatch, the script uses the official historically documented `http://vision.stanford.edu/...` Stanford Dogs endpoint instead.

Step 18.2 note: individual `file_list.mat`, `train_list.mat`, and `test_list.mat` links are not downloaded directly, because the official Stanford Dogs distribution provides these split files through `lists.tar`.

## Responsible boundary

This script prepares local public dataset artifacts only. It does not commit images, train a model, prove breed identity, prove pedigree, or create a registry/certificate decision.

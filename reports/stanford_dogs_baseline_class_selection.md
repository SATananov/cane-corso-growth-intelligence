# Stanford Dogs Baseline Class Selection

Raw root: `C:\Users\stana\Desktop\cane-corso-growth-intelligence\data\images\local_dataset\raw\stanford_dogs`
Downloads root: `C:\Users\stana\Desktop\cane-corso-growth-intelligence\data\images\local_dataset\downloads\stanford_dogs`
Local image-containing folders detected: 121
Candidate rows evaluated: 8
Confirmed candidate classes: 4
Selected first-baseline classes: 3

## Candidate decisions

| Candidate | Available locally | Image count | Include | Notes |
|---|---:|---:|---|---|
| Boxer | True | 151 | yes | confirmed from local folders |
| Bullmastiff | True | 156 | yes | confirmed from local folders |
| Great Dane | True | 156 | yes | confirmed from local folders |
| Mastiff | False | 0 | pending_or_no | not confirmed locally yet; do not train this class before data is available |
| Tibetan Mastiff | True | 152 | optional | confirmed from local folders |
| Cane Corso | False | 0 | pending_or_no | not confirmed locally yet; do not train this class before data is available |
| Dogo Argentino | False | 0 | pending_or_no | not confirmed locally yet; do not train this class before data is available |
| Presa Canario | False | 0 | pending_or_no | not confirmed locally yet; do not train this class before data is available |

## Interpretation

Before Stanford Dogs is downloaded/extracted locally, zero confirmed classes is acceptable.
The purpose of this class-selection stage is to make baseline class selection evidence-based, not to train a model.

A future baseline image classifier should use only classes confirmed as available locally.
If Cane Corso, Dogo Argentino or Presa Canario are not confirmed, the project must not claim that the model can recognize them.

## Responsible boundary

This report supports visual-similarity research only. It is not breed proof, pedigree proof, registry proof, certificate proof or veterinary diagnosis.

# Candidate Datasets for Brain MRI Reliability Study

## Purpose

This document records candidate datasets before acquisition. The goal is to choose datasets based on source quality, licensing, class structure, leakage risk, and suitability for cross-dataset reliability testing.

## Selection Rule

At least two datasets are required before model training:

1. One development/source dataset for training, validation, and internal testing.
2. One independent external target dataset for cross-dataset evaluation.

## Candidate Dataset Table

| ID | Dataset Name | Source Link | Classes | Approx. Size | License / Terms | Patient IDs Available? | Original Split? | Candidate Role | Leakage Risk | Decision |
|---|---|---|---|---:|---|---|---|---|---|---|
| D1 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Development source | TBD | Pending |
| D2 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | External target | TBD | Pending |
| D3 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Optional target | TBD | Pending |

## Minimum Dataset Pair Requirement

The first accepted pair must satisfy:

- Both datasets contain brain MRI tumour classification labels.
- Classes can be mapped consistently.
- Sources are independent enough to support dataset-shift testing.
- Dataset links and licenses are recorded.
- Data can be downloaded reproducibly.
- Obvious duplicates are checked before training.

## Notes

No dataset will be used for training until it has a completed documentation file and appears in the image manifest.

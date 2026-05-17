# Literature Integration Plan

## Purpose

This file defines the literature areas needed to convert the current manuscript draft from an internal research report into a properly supported academic thesis or journal-style paper.

The current manuscript has strong experimental structure, but it still needs formal references to support its motivation, methods, and interpretation.

## Current Manuscript Weakness

The manuscript currently makes strong claims about:

- Brain MRI tumour classification.
- Dataset leakage and overlap.
- Calibration and temperature scaling.
- Dataset shift.
- External validation.
- Reliability beyond accuracy.

However, these claims still need formal support from published literature.

## Literature Area 1: Brain MRI Tumour Classification Benchmarks

### Why needed

The Introduction needs to show that many brain MRI tumour classification studies report high internal accuracy on public datasets.

### Use in manuscript

Use these references to support statements such as:

- Deep learning is widely used for brain MRI tumour classification.
- CNNs, transformers, and hybrid models are commonly evaluated on public brain MRI datasets.
- Reported internal accuracies are often high.

### Target reference types

- Recent review articles.
- High-citation benchmark papers.
- Studies using CNNs, EfficientNet, ResNet, ViT, or hybrid models for brain tumour classification.

### Manuscript sections

- Introduction
- Discussion

## Literature Area 2: Dataset Leakage, Duplicate Images, and Public Dataset Overlap

### Why needed

This is central to the project. The D2 rejection is one of the strongest methodological findings.

### Use in manuscript

Use these references to support statements such as:

- Dataset leakage can inflate performance.
- Duplicate or near-duplicate images can contaminate train/test splits.
- Public datasets may not be independent even when presented separately.
- Medical imaging ML requires careful data partitioning.

### Target reference types

- Medical imaging leakage papers.
- General ML data leakage papers.
- Papers discussing duplicate patient/image leakage.
- Papers on dataset overlap or benchmark contamination.

### Manuscript sections

- Introduction
- Methods
- Results
- Discussion

## Literature Area 3: Calibration and Temperature Scaling

### Why needed

Temperature scaling is a major method in this project.

### Use in manuscript

Use these references to support statements such as:

- Neural networks can be overconfident.
- Calibration measures whether confidence matches empirical correctness.
- Expected calibration error, Brier score, and negative log-likelihood are common calibration metrics.
- Temperature scaling is a post-hoc calibration method fitted on validation logits.

### Target reference types

- Foundational calibration papers.
- Temperature scaling papers.
- Medical AI calibration papers.

### Manuscript sections

- Introduction
- Methods
- Results
- Discussion

## Literature Area 4: Dataset Shift and External Validation in Medical Imaging

### Why needed

The main finding depends on the difference between internal performance and D3B domain-shift behaviour.

### Use in manuscript

Use these references to support statements such as:

- Medical imaging models can fail under scanner, site, protocol, or population shift.
- Internal validation is insufficient for clinical reliability.
- External validation is necessary but must be carefully audited.
- Domain-shift testing is a key part of reliability evaluation.

### Target reference types

- Medical imaging generalisation papers.
- External validation studies.
- Dataset shift reviews.
- AI robustness and reliability papers.

### Manuscript sections

- Introduction
- Discussion
- Limitations

## Literature Area 5: Uncertainty-Aware Medical Image Classification

### Why needed

The current project focuses on calibration and confidence, but future work should connect to uncertainty-aware methods.

### Use in manuscript

Use these references to support future work statements such as:

- Calibration is not the same as full uncertainty estimation.
- Ensembles, Monte Carlo dropout, Bayesian neural networks, and evidential learning may improve uncertainty estimation.
- Uncertainty-aware methods should be evaluated under dataset shift.

### Target reference types

- MC dropout papers.
- Deep ensemble papers.
- Medical image uncertainty papers.
- Evidential deep learning papers.

### Manuscript sections

- Discussion
- Future work

## Literature Area 6: Reporting Standards and Clinical AI Evaluation

### Why needed

The manuscript makes claims about reliability and cautious interpretation. Reporting standards can strengthen this.

### Use in manuscript

Use these references to support statements such as:

- Clinical AI studies should report validation design transparently.
- External validation and dataset provenance matter.
- Claims of clinical reliability should be conservative.

### Target reference types

- CLAIM checklist.
- TRIPOD-AI / PROBAST-AI related work.
- CONSORT-AI / SPIRIT-AI if relevant.
- Medical AI reporting guidelines.

### Manuscript sections

- Methods
- Discussion
- Limitations

## Priority Order

The highest-priority literature areas are:

1. Calibration and temperature scaling.
2. Dataset leakage and overlap.
3. Dataset shift and external validation.
4. Brain MRI tumour classification benchmarks.
5. Reporting standards.
6. Uncertainty-aware methods.

## Immediate Next Task

Create a reference search table with columns:

- Area
- Search query
- Database
- Inclusion criteria
- Exclusion criteria
- Candidate paper title
- DOI / URL
- Why it is useful
- Manuscript section
- Status

## Warning

Do not insert weak or random citations only to increase reference count.

Every reference must support a specific manuscript claim.

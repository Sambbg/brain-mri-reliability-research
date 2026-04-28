# Dataset Acquisition Plan

## Purpose

This document records the initial dataset acquisition strategy for the Brain MRI Reliability Research project.

The goal is not to download as many datasets as possible. The goal is to build a controlled, reproducible dataset strategy that supports reliability-focused evaluation, including calibration, uncertainty estimation, robustness, and source-to-target generalisation.

A weak dataset strategy can invalidate the entire study through data leakage, duplicate images, unclear licensing, poor split design, or uncontrolled mixing of sources.

## Initial Dataset Acquisition Matrix

| Dataset | Role | Use now? | Why |
|---|---|---:|---|
| Kaggle / BT-MRI 4-class dataset | Development source | Yes | Good first benchmark, but leakage risk must be checked |
| BRISC2025 | External target | Yes | Better for source-to-target testing |
| Figshare / Br35H-style dataset | Secondary source | Maybe | Useful, but duplicate/leakage risk is high |
| BraTS | Optional extension | Later | 3D/segmentation complexity may slow you down |
| Local clinical data | High-value external validation | Only if realistic | Strong novelty, but ethics/logistics may delay you |

## Immediate Decision

The project will begin with two datasets only:

1. One source/development dataset.
2. One external target dataset.

This prevents uncontrolled dataset accumulation and makes the first experimental phase easier to audit.

## Initial Dataset Roles

### 1. Source / Development Dataset

The source dataset will be used for:

- initial data loading pipeline;
- preprocessing design;
- baseline model training;
- internal train/validation/test split;
- early calibration analysis;
- debugging the training and evaluation code.

This dataset must not be treated as enough evidence for clinical reliability.

### 2. External Target Dataset

The external target dataset will be used for:

- source-to-target generalisation testing;
- external validation;
- reliability stress-testing;
- calibration transfer analysis;
- uncertainty behaviour under distribution shift.

The external target dataset must remain separate from model development decisions.

## Dataset Rules

Before any dataset is used, the following must be recorded:

- dataset name;
- source URL;
- access date;
- license or usage terms;
- original citation, if available;
- number of images;
- class labels;
- file format;
- image dimensions;
- whether images are 2D slices or 3D volumes;
- whether patient identifiers are available;
- whether patient-level splitting is possible;
- known duplication risks;
- known overlap with other public datasets;
- preprocessing performed;
- final train/validation/test split method.

## Leakage Risk Policy

The project must explicitly check for:

- duplicate files;
- near-duplicate images;
- identical images with different filenames;
- train/test contamination;
- patient-level leakage, if patient identifiers exist;
- dataset overlap between public sources.

If patient-level identifiers are unavailable, this limitation must be stated clearly in the methodology.

## Dataset Storage Policy

Raw datasets must be stored in:

```text
data/raw/

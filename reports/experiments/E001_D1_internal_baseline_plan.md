# E001 — D1 Internal Leakage-Aware Baseline Plan

## Experiment ID
E001

## Purpose
Establish the first internal baseline for D1 using the leakage-aware split.

This experiment is not intended to prove clinical generalisation. It is intended to verify the training pipeline, evaluate basic in-domain performance, and provide a reproducible baseline before external dataset testing.

## Dataset
D1 — Nickparvar Kaggle Brain Tumor MRI Dataset

## Split
Use:

`data/splits/D1_leakage_aware_split.csv`

Do not use the original Kaggle Training/Testing split for this experiment.

## Split Justification
The original Kaggle split showed substantial pHash-based cross-split near-duplicate risk. A leakage-aware split was created by grouping pHash-near-duplicate images before assigning train, validation, and test partitions.

## Model
Initial baseline model:

- ResNet18

Reason:
ResNet18 is lightweight, fast, and suitable for validating the data pipeline before moving to larger models such as ResNet50, EfficientNet, ViT, or Swin Transformer.

## Input Handling
D1 images are grayscale (`mode=L`). For compatibility with ImageNet-pretrained CNNs, grayscale images will be converted to 3-channel format by repeating the single channel.

## Image Size
224 × 224

## Classes
- glioma
- meningioma
- notumor
- pituitary

## Training Configuration
- Epochs: 20
- Batch size: 32
- Optimizer: AdamW
- Learning rate: 0.0001
- Weight decay: 0.0001
- Loss: Cross-entropy
- Seed: 42

## Metrics
Minimum metrics:

- accuracy
- balanced accuracy
- macro-F1
- per-class precision
- per-class recall
- AUROC, if feasible
- confusion matrix

Calibration metrics will be added in a later experiment:

- ECE
- Brier score
- NLL
- reliability diagram

## Outputs
Expected outputs:

- trained model checkpoint
- CSV of epoch-level metrics
- test-set predictions CSV
- confusion matrix figure
- experiment log
- Git commit hash recorded in report

## Reproducibility Requirements
Before training:

1. Git status must be clean.
2. The config file must be committed.
3. The split CSV must already be committed.
4. The training script must save config, seed, and Git commit hash.
5. No manual editing of results after training.

## Interpretation Rule
If this model performs extremely well, the result must not be overclaimed. D1 remains a public 2D benchmark without patient identifiers. Strong D1 performance is useful for pipeline validation, but external validation is still required for the thesis.

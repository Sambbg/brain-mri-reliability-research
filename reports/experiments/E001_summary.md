# E001 Summary ? D1 ResNet18 Leakage-Aware Internal Baseline

## Purpose

E001 tested whether a standard CNN baseline could be trained reproducibly on the D1 leakage-aware split and whether post-hoc temperature scaling could improve calibration on the internal test set.

## Dataset

D1 ? Nickparvar Kaggle Brain Tumor MRI Dataset

## Split

Leakage-aware split generated after exact duplicate removal and perceptual-hash near-duplicate grouping.

| Split | Count |
|---|---:|
| Train | 4,909 |
| Validation | 1,053 |
| Test | 1,051 |

## Model

ResNet18 with ImageNet pretraining.

## Classification Results

| Metric | Value |
|---|---:|
| Best validation macro-F1 | 0.9704 |
| Test accuracy | 0.9667 |
| Test balanced accuracy | 0.9662 |
| Test macro-F1 | 0.9666 |

## Raw Softmax Calibration

| Metric | Value |
|---|---:|
| Mean confidence | 0.9836 |
| Confidence-accuracy gap | 0.0169 |
| ECE, 15 bins | 0.0208 |
| Brier score | 0.0557 |
| NLL | 0.1176 |

## Temperature Scaling

Temperature scaling was fitted using validation logits only.

| Item | Value |
|---|---:|
| Learned temperature | 1.232835 |

## Temperature-Scaled Calibration

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| Accuracy | 0.9667 | 0.9667 |
| Macro-F1 | 0.9666 | 0.9666 |
| Mean confidence | 0.9836 | 0.9773 |
| Confidence-accuracy gap | 0.0169 | 0.0106 |
| ECE, 15 bins | 0.0208 | 0.0145 |
| Brier score | 0.0557 | 0.0536 |
| NLL | 0.1176 | 0.1063 |

## Interpretation

E001 confirms that the reproducible training pipeline is functional. A standard ResNet18 baseline achieved strong internal performance on the D1 leakage-aware split.

The raw softmax model was mildly overconfident. Temperature scaling reduced ECE, Brier score, NLL, and the confidence-accuracy gap without changing classification accuracy or macro-F1.

This is a useful internal calibration result, but it is not evidence of clinical reliability or cross-dataset robustness. D1 remains a public 2D benchmark without patient identifiers. The next major methodological step is external dataset acquisition and train-source/test-target evaluation.

## Next Actions

1. Repeat E001 across additional seeds to estimate variance.
2. Acquire and process an independent external dataset.
3. Apply the same manifest, duplicate, and near-duplicate audit to the external dataset.
4. Run train-D1/test-external evaluation.
5. Compare raw and temperature-scaled calibration under dataset shift.

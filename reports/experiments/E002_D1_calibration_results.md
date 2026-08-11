# E002 - Calibration Evaluation Results

## Experiment

E002 - D1 EfficientNet-B0 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E002_D1_efficientnet_b0_baseline/seed45/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998692 |
| Raw probability row-sum maximum | 1.0000001301 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9657 |
| Mean confidence | 0.9745 |
| Confidence - accuracy gap | 0.0087 |
| Expected Calibration Error, 15 bins | 0.0133 |
| Brier score | 0.0549 |
| Negative Log-Likelihood | 0.1156 |

## Reliability Bin Table

| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |
|---:|---|---:|---:|---:|---:|
| 1 | 0.00-0.07 | 0 | NA | NA | NA |
| 2 | 0.07-0.13 | 0 | NA | NA | NA |
| 3 | 0.13-0.20 | 0 | NA | NA | NA |
| 4 | 0.20-0.27 | 0 | NA | NA | NA |
| 5 | 0.27-0.33 | 0 | NA | NA | NA |
| 6 | 0.33-0.40 | 0 | NA | NA | NA |
| 7 | 0.40-0.47 | 1 | 1.0000 | 0.4470 | 0.5530 |
| 8 | 0.47-0.53 | 8 | 0.7500 | 0.5169 | 0.2331 |
| 9 | 0.53-0.60 | 6 | 0.5000 | 0.5705 | 0.0705 |
| 10 | 0.60-0.67 | 15 | 0.6000 | 0.6302 | 0.0302 |
| 11 | 0.67-0.73 | 9 | 0.5556 | 0.7030 | 0.1475 |
| 12 | 0.73-0.80 | 14 | 0.6429 | 0.7696 | 0.1267 |
| 13 | 0.80-0.87 | 13 | 0.7692 | 0.8351 | 0.0659 |
| 14 | 0.87-0.93 | 32 | 0.8750 | 0.9092 | 0.0342 |
| 15 | 0.93-1.00 | 953 | 0.9906 | 0.9965 | 0.0059 |

## Interpretation

This calibration evaluation measures whether the EfficientNet-B0 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. These results are internal to D1 and should not be interpreted as external reliability evidence.

The model is overconfident on this internal test set: mean confidence is 0.9745, while accuracy is 0.9657. The confidence-accuracy gap is 0.0087.

The next step is to apply post-hoc temperature scaling using the validation set only, then evaluate the calibrated model on the held-out D1 test set.

# E002 - Calibration Evaluation Results

## Experiment

E002 - D1 EfficientNet-B0 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E002_D1_efficientnet_b0_baseline/seed42/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998767 |
| Raw probability row-sum maximum | 1.0000001363 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9743 |
| Mean confidence | 0.9834 |
| Confidence - accuracy gap | 0.0091 |
| Expected Calibration Error, 15 bins | 0.0150 |
| Brier score | 0.0409 |
| Negative Log-Likelihood | 0.1026 |

## Reliability Bin Table

| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |
|---:|---|---:|---:|---:|---:|
| 1 | 0.00-0.07 | 0 | NA | NA | NA |
| 2 | 0.07-0.13 | 0 | NA | NA | NA |
| 3 | 0.13-0.20 | 0 | NA | NA | NA |
| 4 | 0.20-0.27 | 0 | NA | NA | NA |
| 5 | 0.27-0.33 | 0 | NA | NA | NA |
| 6 | 0.33-0.40 | 1 | 0.0000 | 0.3731 | 0.3731 |
| 7 | 0.40-0.47 | 3 | 0.6667 | 0.4279 | 0.2388 |
| 8 | 0.47-0.53 | 3 | 0.6667 | 0.5184 | 0.1482 |
| 9 | 0.53-0.60 | 7 | 0.4286 | 0.5709 | 0.1423 |
| 10 | 0.60-0.67 | 7 | 0.7143 | 0.6357 | 0.0786 |
| 11 | 0.67-0.73 | 7 | 0.5714 | 0.7024 | 0.1310 |
| 12 | 0.73-0.80 | 6 | 1.0000 | 0.7682 | 0.2318 |
| 13 | 0.80-0.87 | 14 | 0.7143 | 0.8286 | 0.1144 |
| 14 | 0.87-0.93 | 11 | 0.7273 | 0.9028 | 0.1755 |
| 15 | 0.93-1.00 | 992 | 0.9919 | 0.9989 | 0.0069 |

## Interpretation

This calibration evaluation measures whether the EfficientNet-B0 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. These results are internal to D1 and should not be interpreted as external reliability evidence.

The model is overconfident on this internal test set: mean confidence is 0.9834, while accuracy is 0.9743. The confidence-accuracy gap is 0.0091.

The next step is to apply post-hoc temperature scaling using the validation set only, then evaluate the calibrated model on the held-out D1 test set.

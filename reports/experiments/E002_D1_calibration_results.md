# E002 - Calibration Evaluation Results

## Experiment

E002 - D1 EfficientNet-B0 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E002_D1_efficientnet_b0_baseline/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998725 |
| Raw probability row-sum maximum | 1.0000001262 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9676 |
| Mean confidence | 0.9812 |
| Confidence - accuracy gap | 0.0135 |
| Expected Calibration Error, 15 bins | 0.0196 |
| Brier score | 0.0533 |
| Negative Log-Likelihood | 0.1090 |

## Reliability Bin Table

| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |
|---:|---|---:|---:|---:|---:|
| 1 | 0.00-0.07 | 0 | NA | NA | NA |
| 2 | 0.07-0.13 | 0 | NA | NA | NA |
| 3 | 0.13-0.20 | 0 | NA | NA | NA |
| 4 | 0.20-0.27 | 0 | NA | NA | NA |
| 5 | 0.27-0.33 | 0 | NA | NA | NA |
| 6 | 0.33-0.40 | 0 | NA | NA | NA |
| 7 | 0.40-0.47 | 4 | 0.7500 | 0.4273 | 0.3227 |
| 8 | 0.47-0.53 | 5 | 0.2000 | 0.5173 | 0.3173 |
| 9 | 0.53-0.60 | 3 | 0.6667 | 0.5672 | 0.0994 |
| 10 | 0.60-0.67 | 4 | 1.0000 | 0.6433 | 0.3567 |
| 11 | 0.67-0.73 | 6 | 0.5000 | 0.6950 | 0.1950 |
| 12 | 0.73-0.80 | 9 | 0.4444 | 0.7750 | 0.3305 |
| 13 | 0.80-0.87 | 13 | 0.8462 | 0.8332 | 0.0129 |
| 14 | 0.87-0.93 | 39 | 0.8205 | 0.9057 | 0.0852 |
| 15 | 0.93-1.00 | 968 | 0.9886 | 0.9972 | 0.0086 |

## Interpretation

This calibration evaluation measures whether the EfficientNet-B0 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. These results are internal to D1 and should not be interpreted as external reliability evidence.

The model is overconfident on this internal test set: mean confidence is 0.9812, while accuracy is 0.9676. The confidence-accuracy gap is 0.0135.

The next step is to apply post-hoc temperature scaling using the validation set only, then evaluate the calibrated model on the held-out D1 test set.

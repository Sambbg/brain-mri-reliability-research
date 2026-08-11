# E002 - Calibration Evaluation Results

## Experiment

E002 - D1 EfficientNet-B0 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E002_D1_efficientnet_b0_baseline/seed44/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998693 |
| Raw probability row-sum maximum | 1.0000001154 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9629 |
| Mean confidence | 0.9854 |
| Confidence - accuracy gap | 0.0225 |
| Expected Calibration Error, 15 bins | 0.0273 |
| Brier score | 0.0616 |
| Negative Log-Likelihood | 0.1404 |

## Reliability Bin Table

| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |
|---:|---|---:|---:|---:|---:|
| 1 | 0.00-0.07 | 0 | NA | NA | NA |
| 2 | 0.07-0.13 | 0 | NA | NA | NA |
| 3 | 0.13-0.20 | 0 | NA | NA | NA |
| 4 | 0.20-0.27 | 0 | NA | NA | NA |
| 5 | 0.27-0.33 | 0 | NA | NA | NA |
| 6 | 0.33-0.40 | 1 | 1.0000 | 0.3874 | 0.6126 |
| 7 | 0.40-0.47 | 1 | 0.0000 | 0.4282 | 0.4282 |
| 8 | 0.47-0.53 | 4 | 0.2500 | 0.5054 | 0.2554 |
| 9 | 0.53-0.60 | 5 | 0.6000 | 0.5726 | 0.0274 |
| 10 | 0.60-0.67 | 5 | 0.8000 | 0.6231 | 0.1769 |
| 11 | 0.67-0.73 | 3 | 1.0000 | 0.6987 | 0.3013 |
| 12 | 0.73-0.80 | 8 | 0.2500 | 0.7660 | 0.5160 |
| 13 | 0.80-0.87 | 10 | 0.7000 | 0.8442 | 0.1442 |
| 14 | 0.87-0.93 | 14 | 0.6429 | 0.8997 | 0.2569 |
| 15 | 0.93-1.00 | 1000 | 0.9820 | 0.9976 | 0.0156 |

## Interpretation

This calibration evaluation measures whether the EfficientNet-B0 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. These results are internal to D1 and should not be interpreted as external reliability evidence.

The model is overconfident on this internal test set: mean confidence is 0.9854, while accuracy is 0.9629. The confidence-accuracy gap is 0.0225.

The next step is to apply post-hoc temperature scaling using the validation set only, then evaluate the calibrated model on the held-out D1 test set.

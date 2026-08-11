# E003 - Calibration Evaluation Results

## Experiment

E003 - D1 ViT-B/16 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E003_D1_vit_b16_baseline/seed42/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998664 |
| Raw probability row-sum maximum | 1.0000001348 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9534 |
| Mean confidence | 0.9775 |
| Confidence - accuracy gap | 0.0241 |
| Expected Calibration Error, 15 bins | 0.0291 |
| Brier score | 0.0753 |
| Negative Log-Likelihood | 0.1654 |

## Reliability Bin Table

| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |
|---:|---|---:|---:|---:|---:|
| 1 | 0.00-0.07 | 0 | NA | NA | NA |
| 2 | 0.07-0.13 | 0 | NA | NA | NA |
| 3 | 0.13-0.20 | 0 | NA | NA | NA |
| 4 | 0.20-0.27 | 0 | NA | NA | NA |
| 5 | 0.27-0.33 | 0 | NA | NA | NA |
| 6 | 0.33-0.40 | 0 | NA | NA | NA |
| 7 | 0.40-0.47 | 2 | 0.0000 | 0.4407 | 0.4407 |
| 8 | 0.47-0.53 | 3 | 1.0000 | 0.5188 | 0.4812 |
| 9 | 0.53-0.60 | 12 | 0.6667 | 0.5668 | 0.0999 |
| 10 | 0.60-0.67 | 9 | 0.5556 | 0.6344 | 0.0788 |
| 11 | 0.67-0.73 | 10 | 0.4000 | 0.7084 | 0.3084 |
| 12 | 0.73-0.80 | 10 | 0.5000 | 0.7672 | 0.2672 |
| 13 | 0.80-0.87 | 15 | 0.4667 | 0.8442 | 0.3775 |
| 14 | 0.87-0.93 | 16 | 0.6875 | 0.9063 | 0.2188 |
| 15 | 0.93-1.00 | 974 | 0.9846 | 0.9963 | 0.0117 |

## Interpretation

This calibration evaluation measures whether the ViT-B/16 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. These results are internal to D1 and should not be interpreted as external reliability evidence.

The model is overconfident on this internal test set: mean confidence is 0.9775, while accuracy is 0.9534. The confidence-accuracy gap is 0.0241.

The next step is to apply post-hoc temperature scaling using the validation set only, then evaluate the calibrated model on the held-out D1 test set.

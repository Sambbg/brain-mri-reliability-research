# E003 - Calibration Evaluation Results

## Experiment

E003 - D1 ViT-B/16 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E003_D1_vit_b16_baseline/seed43/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998638 |
| Raw probability row-sum maximum | 1.0000001202 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9562 |
| Mean confidence | 0.9779 |
| Confidence - accuracy gap | 0.0217 |
| Expected Calibration Error, 15 bins | 0.0259 |
| Brier score | 0.0700 |
| Negative Log-Likelihood | 0.1442 |

## Reliability Bin Table

| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |
|---:|---|---:|---:|---:|---:|
| 1 | 0.00-0.07 | 0 | NA | NA | NA |
| 2 | 0.07-0.13 | 0 | NA | NA | NA |
| 3 | 0.13-0.20 | 0 | NA | NA | NA |
| 4 | 0.20-0.27 | 0 | NA | NA | NA |
| 5 | 0.27-0.33 | 0 | NA | NA | NA |
| 6 | 0.33-0.40 | 0 | NA | NA | NA |
| 7 | 0.40-0.47 | 1 | 0.0000 | 0.4638 | 0.4638 |
| 8 | 0.47-0.53 | 9 | 0.1111 | 0.5069 | 0.3958 |
| 9 | 0.53-0.60 | 6 | 0.6667 | 0.5541 | 0.1126 |
| 10 | 0.60-0.67 | 4 | 1.0000 | 0.6251 | 0.3749 |
| 11 | 0.67-0.73 | 13 | 0.6923 | 0.6982 | 0.0059 |
| 12 | 0.73-0.80 | 9 | 0.7778 | 0.7715 | 0.0063 |
| 13 | 0.80-0.87 | 14 | 0.5714 | 0.8400 | 0.2685 |
| 14 | 0.87-0.93 | 28 | 0.5714 | 0.9077 | 0.3363 |
| 15 | 0.93-1.00 | 967 | 0.9886 | 0.9966 | 0.0080 |

## Interpretation

This calibration evaluation measures whether the ViT-B/16 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. These results are internal to D1 and should not be interpreted as external reliability evidence.

The model is overconfident on this internal test set: mean confidence is 0.9779, while accuracy is 0.9562. The confidence-accuracy gap is 0.0217.

The next step is to apply post-hoc temperature scaling using the validation set only, then evaluate the calibrated model on the held-out D1 test set.

# E003 - Calibration Evaluation Results

## Experiment

E003 - D1 ViT-B/16 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E003_D1_vit_b16_baseline/seed46/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998600 |
| Raw probability row-sum maximum | 1.0000001418 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9524 |
| Mean confidence | 0.9779 |
| Confidence - accuracy gap | 0.0255 |
| Expected Calibration Error, 15 bins | 0.0300 |
| Brier score | 0.0793 |
| Negative Log-Likelihood | 0.1758 |

## Reliability Bin Table

| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |
|---:|---|---:|---:|---:|---:|
| 1 | 0.00-0.07 | 0 | NA | NA | NA |
| 2 | 0.07-0.13 | 0 | NA | NA | NA |
| 3 | 0.13-0.20 | 0 | NA | NA | NA |
| 4 | 0.20-0.27 | 0 | NA | NA | NA |
| 5 | 0.27-0.33 | 0 | NA | NA | NA |
| 6 | 0.33-0.40 | 0 | NA | NA | NA |
| 7 | 0.40-0.47 | 2 | 0.5000 | 0.4339 | 0.0661 |
| 8 | 0.47-0.53 | 6 | 0.6667 | 0.5111 | 0.1555 |
| 9 | 0.53-0.60 | 8 | 0.5000 | 0.5773 | 0.0773 |
| 10 | 0.60-0.67 | 9 | 0.7778 | 0.6338 | 0.1439 |
| 11 | 0.67-0.73 | 8 | 0.5000 | 0.7078 | 0.2078 |
| 12 | 0.73-0.80 | 9 | 0.6667 | 0.7608 | 0.0942 |
| 13 | 0.80-0.87 | 12 | 0.4167 | 0.8310 | 0.4144 |
| 14 | 0.87-0.93 | 25 | 0.6400 | 0.9025 | 0.2625 |
| 15 | 0.93-1.00 | 972 | 0.9815 | 0.9964 | 0.0149 |

## Interpretation

This calibration evaluation measures whether the ViT-B/16 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. These results are internal to D1 and should not be interpreted as external reliability evidence.

The model is overconfident on this internal test set: mean confidence is 0.9779, while accuracy is 0.9524. The confidence-accuracy gap is 0.0255.

The next step is to apply post-hoc temperature scaling using the validation set only, then evaluate the calibrated model on the held-out D1 test set.

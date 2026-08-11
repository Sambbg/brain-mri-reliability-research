# E001 - Calibration Evaluation Results

## Experiment

E001 - D1 ResNet18 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E001_D1_resnet18_baseline/seed45/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998825 |
| Raw probability row-sum maximum | 1.0000001217 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9724 |
| Mean confidence | 0.9880 |
| Confidence - accuracy gap | 0.0156 |
| Expected Calibration Error, 15 bins | 0.0173 |
| Brier score | 0.0474 |
| Negative Log-Likelihood | 0.1355 |

## Reliability Bin Table

| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |
|---:|---|---:|---:|---:|---:|
| 1 | 0.00-0.07 | 0 | NA | NA | NA |
| 2 | 0.07-0.13 | 0 | NA | NA | NA |
| 3 | 0.13-0.20 | 0 | NA | NA | NA |
| 4 | 0.20-0.27 | 0 | NA | NA | NA |
| 5 | 0.27-0.33 | 0 | NA | NA | NA |
| 6 | 0.33-0.40 | 1 | 1.0000 | 0.3926 | 0.6074 |
| 7 | 0.40-0.47 | 0 | NA | NA | NA |
| 8 | 0.47-0.53 | 4 | 0.5000 | 0.4998 | 0.0002 |
| 9 | 0.53-0.60 | 3 | 0.6667 | 0.5649 | 0.1018 |
| 10 | 0.60-0.67 | 2 | 0.5000 | 0.6620 | 0.1620 |
| 11 | 0.67-0.73 | 5 | 0.4000 | 0.7108 | 0.3108 |
| 12 | 0.73-0.80 | 7 | 0.7143 | 0.7637 | 0.0494 |
| 13 | 0.80-0.87 | 14 | 0.6429 | 0.8379 | 0.1950 |
| 14 | 0.87-0.93 | 11 | 0.8182 | 0.9032 | 0.0850 |
| 15 | 0.93-1.00 | 1004 | 0.9871 | 0.9984 | 0.0113 |

## Interpretation

This calibration evaluation measures whether the ResNet18 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. The model is evaluated using raw softmax probabilities without post-hoc temperature scaling. These results are still internal to D1 and should not be interpreted as external reliability evidence.

The model is slightly overconfident on this internal test set: mean confidence is 0.9880, while accuracy is 0.9724. The confidence-accuracy gap is 0.0156.

The next step is to apply post-hoc calibration, especially temperature scaling, using the validation set only, then evaluate the calibrated model on the held-out test set.

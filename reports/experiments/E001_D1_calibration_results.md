# E001 - Calibration Evaluation Results

## Experiment

E001 - D1 ResNet18 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E001_D1_resnet18_baseline/seed46/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998677 |
| Raw probability row-sum maximum | 1.0000001340 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9648 |
| Mean confidence | 0.9693 |
| Confidence - accuracy gap | 0.0045 |
| Expected Calibration Error, 15 bins | 0.0162 |
| Brier score | 0.0535 |
| Negative Log-Likelihood | 0.1066 |

## Reliability Bin Table

| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |
|---:|---|---:|---:|---:|---:|
| 1 | 0.00-0.07 | 0 | NA | NA | NA |
| 2 | 0.07-0.13 | 0 | NA | NA | NA |
| 3 | 0.13-0.20 | 0 | NA | NA | NA |
| 4 | 0.20-0.27 | 0 | NA | NA | NA |
| 5 | 0.27-0.33 | 0 | NA | NA | NA |
| 6 | 0.33-0.40 | 4 | 0.5000 | 0.3743 | 0.1257 |
| 7 | 0.40-0.47 | 1 | 0.0000 | 0.4540 | 0.4540 |
| 8 | 0.47-0.53 | 3 | 0.6667 | 0.5143 | 0.1523 |
| 9 | 0.53-0.60 | 10 | 0.8000 | 0.5597 | 0.2403 |
| 10 | 0.60-0.67 | 11 | 0.5455 | 0.6317 | 0.0863 |
| 11 | 0.67-0.73 | 16 | 0.5625 | 0.6961 | 0.1336 |
| 12 | 0.73-0.80 | 19 | 0.7368 | 0.7664 | 0.0296 |
| 13 | 0.80-0.87 | 18 | 0.6111 | 0.8385 | 0.2274 |
| 14 | 0.87-0.93 | 30 | 1.0000 | 0.9067 | 0.0933 |
| 15 | 0.93-1.00 | 939 | 0.9925 | 0.9954 | 0.0029 |

## Interpretation

This calibration evaluation measures whether the ResNet18 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. The model is evaluated using raw softmax probabilities without post-hoc temperature scaling. These results are still internal to D1 and should not be interpreted as external reliability evidence.

The model is slightly overconfident on this internal test set: mean confidence is 0.9693, while accuracy is 0.9648. The confidence-accuracy gap is 0.0045.

The next step is to apply post-hoc calibration, especially temperature scaling, using the validation set only, then evaluate the calibrated model on the held-out test set.

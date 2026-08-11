# E001 - Calibration Evaluation Results

## Experiment

E001 - D1 ResNet18 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E001_D1_resnet18_baseline/seed42/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998728 |
| Raw probability row-sum maximum | 1.0000001410 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9543 |
| Mean confidence | 0.9710 |
| Confidence - accuracy gap | 0.0167 |
| Expected Calibration Error, 15 bins | 0.0181 |
| Brier score | 0.0656 |
| Negative Log-Likelihood | 0.1383 |

## Reliability Bin Table

| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |
|---:|---|---:|---:|---:|---:|
| 1 | 0.00-0.07 | 0 | NA | NA | NA |
| 2 | 0.07-0.13 | 0 | NA | NA | NA |
| 3 | 0.13-0.20 | 0 | NA | NA | NA |
| 4 | 0.20-0.27 | 0 | NA | NA | NA |
| 5 | 0.27-0.33 | 0 | NA | NA | NA |
| 6 | 0.33-0.40 | 1 | 1.0000 | 0.3555 | 0.6445 |
| 7 | 0.40-0.47 | 2 | 0.5000 | 0.4542 | 0.0458 |
| 8 | 0.47-0.53 | 10 | 0.4000 | 0.5095 | 0.1095 |
| 9 | 0.53-0.60 | 10 | 0.5000 | 0.5648 | 0.0648 |
| 10 | 0.60-0.67 | 17 | 0.2941 | 0.6363 | 0.3421 |
| 11 | 0.67-0.73 | 10 | 0.6000 | 0.6952 | 0.0952 |
| 12 | 0.73-0.80 | 8 | 0.6250 | 0.7721 | 0.1471 |
| 13 | 0.80-0.87 | 14 | 0.5714 | 0.8458 | 0.2744 |
| 14 | 0.87-0.93 | 35 | 0.8857 | 0.9106 | 0.0249 |
| 15 | 0.93-1.00 | 944 | 0.9926 | 0.9967 | 0.0041 |

## Interpretation

This calibration evaluation measures whether the ResNet18 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. The model is evaluated using raw softmax probabilities without post-hoc temperature scaling. These results are still internal to D1 and should not be interpreted as external reliability evidence.

The model is slightly overconfident on this internal test set: mean confidence is 0.9710, while accuracy is 0.9543. The confidence-accuracy gap is 0.0167.

The next step is to apply post-hoc calibration, especially temperature scaling, using the validation set only, then evaluate the calibrated model on the held-out test set.

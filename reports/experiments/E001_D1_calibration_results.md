# E001 - Calibration Evaluation Results

## Experiment

E001 - D1 ResNet18 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E001_D1_resnet18_baseline/seed43/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998738 |
| Raw probability row-sum maximum | 1.0000001470 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9676 |
| Mean confidence | 0.9823 |
| Confidence - accuracy gap | 0.0146 |
| Expected Calibration Error, 15 bins | 0.0169 |
| Brier score | 0.0517 |
| Negative Log-Likelihood | 0.1073 |

## Reliability Bin Table

| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |
|---:|---|---:|---:|---:|---:|
| 1 | 0.00-0.07 | 0 | NA | NA | NA |
| 2 | 0.07-0.13 | 0 | NA | NA | NA |
| 3 | 0.13-0.20 | 0 | NA | NA | NA |
| 4 | 0.20-0.27 | 0 | NA | NA | NA |
| 5 | 0.27-0.33 | 0 | NA | NA | NA |
| 6 | 0.33-0.40 | 0 | NA | NA | NA |
| 7 | 0.40-0.47 | 1 | 1.0000 | 0.4306 | 0.5694 |
| 8 | 0.47-0.53 | 3 | 0.6667 | 0.5181 | 0.1486 |
| 9 | 0.53-0.60 | 4 | 0.5000 | 0.5796 | 0.0796 |
| 10 | 0.60-0.67 | 7 | 0.4286 | 0.6263 | 0.1977 |
| 11 | 0.67-0.73 | 5 | 0.4000 | 0.7041 | 0.3041 |
| 12 | 0.73-0.80 | 16 | 0.3750 | 0.7633 | 0.3883 |
| 13 | 0.80-0.87 | 13 | 0.8462 | 0.8337 | 0.0125 |
| 14 | 0.87-0.93 | 20 | 0.8500 | 0.9116 | 0.0616 |
| 15 | 0.93-1.00 | 982 | 0.9908 | 0.9968 | 0.0060 |

## Interpretation

This calibration evaluation measures whether the ResNet18 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. The model is evaluated using raw softmax probabilities without post-hoc temperature scaling. These results are still internal to D1 and should not be interpreted as external reliability evidence.

The model is slightly overconfident on this internal test set: mean confidence is 0.9823, while accuracy is 0.9676. The confidence-accuracy gap is 0.0146.

The next step is to apply post-hoc calibration, especially temperature scaling, using the validation set only, then evaluate the calibrated model on the held-out test set.

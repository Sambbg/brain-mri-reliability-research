# E001 - Calibration Evaluation Results

## Experiment

E001 - D1 ResNet18 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E001_D1_resnet18_baseline/seed44/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998756 |
| Raw probability row-sum maximum | 1.0000001244 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9715 |
| Mean confidence | 0.9740 |
| Confidence - accuracy gap | 0.0026 |
| Expected Calibration Error, 15 bins | 0.0105 |
| Brier score | 0.0464 |
| Negative Log-Likelihood | 0.1053 |

## Reliability Bin Table

| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |
|---:|---|---:|---:|---:|---:|
| 1 | 0.00-0.07 | 0 | NA | NA | NA |
| 2 | 0.07-0.13 | 0 | NA | NA | NA |
| 3 | 0.13-0.20 | 0 | NA | NA | NA |
| 4 | 0.20-0.27 | 0 | NA | NA | NA |
| 5 | 0.27-0.33 | 0 | NA | NA | NA |
| 6 | 0.33-0.40 | 1 | 0.0000 | 0.3653 | 0.3653 |
| 7 | 0.40-0.47 | 2 | 1.0000 | 0.4267 | 0.5733 |
| 8 | 0.47-0.53 | 6 | 0.5000 | 0.5121 | 0.0121 |
| 9 | 0.53-0.60 | 5 | 0.8000 | 0.5783 | 0.2217 |
| 10 | 0.60-0.67 | 11 | 0.5455 | 0.6301 | 0.0847 |
| 11 | 0.67-0.73 | 19 | 0.6842 | 0.7041 | 0.0199 |
| 12 | 0.73-0.80 | 9 | 0.7778 | 0.7689 | 0.0089 |
| 13 | 0.80-0.87 | 17 | 0.9412 | 0.8328 | 0.1083 |
| 14 | 0.87-0.93 | 26 | 0.8462 | 0.9064 | 0.0603 |
| 15 | 0.93-1.00 | 955 | 0.9927 | 0.9964 | 0.0037 |

## Interpretation

This calibration evaluation measures whether the ResNet18 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. The model is evaluated using raw softmax probabilities without post-hoc temperature scaling. These results are still internal to D1 and should not be interpreted as external reliability evidence.

The model is slightly overconfident on this internal test set: mean confidence is 0.9740, while accuracy is 0.9715. The confidence-accuracy gap is 0.0026.

The next step is to apply post-hoc calibration, especially temperature scaling, using the validation set only, then evaluate the calibrated model on the held-out test set.

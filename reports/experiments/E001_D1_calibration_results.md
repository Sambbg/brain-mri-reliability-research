# E001 - Calibration Evaluation Results

## Experiment

E001 - D1 ResNet18 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E001_D1_resnet18_baseline/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998706 |
| Raw probability row-sum maximum | 1.0000001394 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9667 |
| Mean confidence | 0.9836 |
| Confidence - accuracy gap | 0.0169 |
| Expected Calibration Error, 15 bins | 0.0193 |
| Brier score | 0.0557 |
| Negative Log-Likelihood | 0.1176 |

## Reliability Bin Table

| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |
|---:|---|---:|---:|---:|---:|
| 1 | 0.00-0.07 | 0 | NA | NA | NA |
| 2 | 0.07-0.13 | 0 | NA | NA | NA |
| 3 | 0.13-0.20 | 0 | NA | NA | NA |
| 4 | 0.20-0.27 | 0 | NA | NA | NA |
| 5 | 0.27-0.33 | 0 | NA | NA | NA |
| 6 | 0.33-0.40 | 0 | NA | NA | NA |
| 7 | 0.40-0.47 | 0 | NA | NA | NA |
| 8 | 0.47-0.53 | 4 | 0.5000 | 0.5108 | 0.0108 |
| 9 | 0.53-0.60 | 9 | 0.5556 | 0.5757 | 0.0202 |
| 10 | 0.60-0.67 | 3 | 1.0000 | 0.6090 | 0.3910 |
| 11 | 0.67-0.73 | 7 | 0.4286 | 0.7072 | 0.2786 |
| 12 | 0.73-0.80 | 9 | 0.7778 | 0.7681 | 0.0097 |
| 13 | 0.80-0.87 | 11 | 0.6364 | 0.8443 | 0.2079 |
| 14 | 0.87-0.93 | 19 | 0.6842 | 0.8983 | 0.2141 |
| 15 | 0.93-1.00 | 989 | 0.9869 | 0.9974 | 0.0106 |

## Interpretation

This calibration evaluation measures whether the ResNet18 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. The model is evaluated using raw softmax probabilities without post-hoc temperature scaling. These results are still internal to D1 and should not be interpreted as external reliability evidence.

The model is slightly overconfident on this internal test set: mean confidence is 0.9836, while accuracy is 0.9667. The confidence-accuracy gap is 0.0169.

The next step is to apply post-hoc calibration, especially temperature scaling, using the validation set only, then evaluate the calibrated model on the held-out test set.

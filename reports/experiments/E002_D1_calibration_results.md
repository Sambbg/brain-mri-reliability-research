# E002 - Calibration Evaluation Results

## Experiment

E002 - D1 EfficientNet-B0 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E002_D1_efficientnet_b0_baseline/seed46/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998766 |
| Raw probability row-sum maximum | 1.0000001247 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9676 |
| Mean confidence | 0.9867 |
| Confidence - accuracy gap | 0.0190 |
| Expected Calibration Error, 15 bins | 0.0206 |
| Brier score | 0.0496 |
| Negative Log-Likelihood | 0.1102 |

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
| 8 | 0.47-0.53 | 5 | 0.4000 | 0.4946 | 0.0946 |
| 9 | 0.53-0.60 | 4 | 0.2500 | 0.5715 | 0.3215 |
| 10 | 0.60-0.67 | 5 | 0.8000 | 0.6374 | 0.1626 |
| 11 | 0.67-0.73 | 8 | 0.3750 | 0.7051 | 0.3301 |
| 12 | 0.73-0.80 | 6 | 0.5000 | 0.7629 | 0.2629 |
| 13 | 0.80-0.87 | 4 | 0.5000 | 0.8567 | 0.3567 |
| 14 | 0.87-0.93 | 19 | 0.7368 | 0.8952 | 0.1584 |
| 15 | 0.93-1.00 | 1000 | 0.9880 | 0.9984 | 0.0104 |

## Interpretation

This calibration evaluation measures whether the EfficientNet-B0 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. These results are internal to D1 and should not be interpreted as external reliability evidence.

The model is overconfident on this internal test set: mean confidence is 0.9867, while accuracy is 0.9676. The confidence-accuracy gap is 0.0190.

The next step is to apply post-hoc temperature scaling using the validation set only, then evaluate the calibrated model on the held-out D1 test set.

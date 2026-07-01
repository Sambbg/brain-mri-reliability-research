# E003 - Calibration Evaluation Results

## Experiment

E003 - D1 ViT-B/16 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E003_D1_vit_b16_baseline/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998715 |
| Raw probability row-sum maximum | 1.0000001338 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9581 |
| Mean confidence | 0.9740 |
| Confidence - accuracy gap | 0.0159 |
| Expected Calibration Error, 15 bins | 0.0198 |
| Brier score | 0.0689 |
| Negative Log-Likelihood | 0.1571 |

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
| 8 | 0.47-0.53 | 9 | 0.6667 | 0.5157 | 0.1510 |
| 9 | 0.53-0.60 | 11 | 0.5455 | 0.5702 | 0.0247 |
| 10 | 0.60-0.67 | 11 | 0.5455 | 0.6368 | 0.0914 |
| 11 | 0.67-0.73 | 9 | 0.7778 | 0.7016 | 0.0762 |
| 12 | 0.73-0.80 | 9 | 0.5556 | 0.7731 | 0.2176 |
| 13 | 0.80-0.87 | 15 | 0.6000 | 0.8339 | 0.2339 |
| 14 | 0.87-0.93 | 28 | 0.7857 | 0.9034 | 0.1177 |
| 15 | 0.93-1.00 | 959 | 0.9864 | 0.9955 | 0.0091 |

## Interpretation

This calibration evaluation measures whether the ViT-B/16 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. These results are internal to D1 and should not be interpreted as external reliability evidence.

The model is overconfident on this internal test set: mean confidence is 0.9740, while accuracy is 0.9581. The confidence-accuracy gap is 0.0159.

The next step is to apply post-hoc temperature scaling using the validation set only, then evaluate the calibrated model on the held-out D1 test set.

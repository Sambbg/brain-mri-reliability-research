# E003 - Calibration Evaluation Results

## Experiment

E003 - D1 ViT-B/16 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E003_D1_vit_b16_baseline/seed44/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998617 |
| Raw probability row-sum maximum | 1.0000001395 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9591 |
| Mean confidence | 0.9766 |
| Confidence - accuracy gap | 0.0175 |
| Expected Calibration Error, 15 bins | 0.0228 |
| Brier score | 0.0639 |
| Negative Log-Likelihood | 0.1496 |

## Reliability Bin Table

| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |
|---:|---|---:|---:|---:|---:|
| 1 | 0.00-0.07 | 0 | NA | NA | NA |
| 2 | 0.07-0.13 | 0 | NA | NA | NA |
| 3 | 0.13-0.20 | 0 | NA | NA | NA |
| 4 | 0.20-0.27 | 0 | NA | NA | NA |
| 5 | 0.27-0.33 | 0 | NA | NA | NA |
| 6 | 0.33-0.40 | 1 | 0.0000 | 0.3689 | 0.3689 |
| 7 | 0.40-0.47 | 7 | 0.0000 | 0.4414 | 0.4414 |
| 8 | 0.47-0.53 | 5 | 0.2000 | 0.5054 | 0.3054 |
| 9 | 0.53-0.60 | 4 | 0.5000 | 0.5771 | 0.0771 |
| 10 | 0.60-0.67 | 6 | 0.8333 | 0.6425 | 0.1908 |
| 11 | 0.67-0.73 | 11 | 0.6364 | 0.6947 | 0.0583 |
| 12 | 0.73-0.80 | 11 | 0.6364 | 0.7651 | 0.1288 |
| 13 | 0.80-0.87 | 10 | 1.0000 | 0.8343 | 0.1657 |
| 14 | 0.87-0.93 | 27 | 0.8519 | 0.9028 | 0.0510 |
| 15 | 0.93-1.00 | 969 | 0.9835 | 0.9963 | 0.0129 |

## Interpretation

This calibration evaluation measures whether the ViT-B/16 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. These results are internal to D1 and should not be interpreted as external reliability evidence.

The model is overconfident on this internal test set: mean confidence is 0.9766, while accuracy is 0.9591. The confidence-accuracy gap is 0.0175.

The next step is to apply post-hoc temperature scaling using the validation set only, then evaluate the calibrated model on the held-out D1 test set.

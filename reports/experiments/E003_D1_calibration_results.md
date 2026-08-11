# E003 - Calibration Evaluation Results

## Experiment

E003 - D1 ViT-B/16 internal leakage-aware baseline

## Input

- Prediction file: `experiments/E003_D1_vit_b16_baseline/seed45/test_predictions.csv`
- Samples evaluated: 1051
- Number of reliability bins: 15

## Probability Normalization Check

Softmax probabilities were re-normalized after CSV loading to avoid minor floating-point row-sum warnings during NLL calculation.

| Quantity | Value |
|---|---:|
| Raw probability row-sum minimum | 0.9999998648 |
| Raw probability row-sum maximum | 1.0000001346 |
| Normalized probability row-sum minimum | 1.0000000000 |
| Normalized probability row-sum maximum | 1.0000000000 |

## Calibration Metrics

| Metric | Value |
|---|---:|
| Accuracy | 0.9562 |
| Mean confidence | 0.9781 |
| Confidence - accuracy gap | 0.0219 |
| Expected Calibration Error, 15 bins | 0.0219 |
| Brier score | 0.0650 |
| Negative Log-Likelihood | 0.1347 |

## Reliability Bin Table

| Bin | Confidence range | Count | Accuracy | Mean confidence | Gap |
|---:|---|---:|---:|---:|---:|
| 1 | 0.00-0.07 | 0 | NA | NA | NA |
| 2 | 0.07-0.13 | 0 | NA | NA | NA |
| 3 | 0.13-0.20 | 0 | NA | NA | NA |
| 4 | 0.20-0.27 | 0 | NA | NA | NA |
| 5 | 0.27-0.33 | 0 | NA | NA | NA |
| 6 | 0.33-0.40 | 0 | NA | NA | NA |
| 7 | 0.40-0.47 | 3 | 0.0000 | 0.4503 | 0.4503 |
| 8 | 0.47-0.53 | 6 | 0.5000 | 0.5128 | 0.0128 |
| 9 | 0.53-0.60 | 9 | 0.5556 | 0.5709 | 0.0153 |
| 10 | 0.60-0.67 | 4 | 0.5000 | 0.6281 | 0.1281 |
| 11 | 0.67-0.73 | 7 | 0.5714 | 0.6970 | 0.1256 |
| 12 | 0.73-0.80 | 14 | 0.4286 | 0.7610 | 0.3325 |
| 13 | 0.80-0.87 | 15 | 0.8000 | 0.8374 | 0.0374 |
| 14 | 0.87-0.93 | 26 | 0.7692 | 0.9024 | 0.1332 |
| 15 | 0.93-1.00 | 967 | 0.9855 | 0.9973 | 0.0117 |

## Interpretation

This calibration evaluation measures whether the ViT-B/16 model's predicted confidence matches empirical correctness on the leakage-aware D1 test split. These results are internal to D1 and should not be interpreted as external reliability evidence.

The model is overconfident on this internal test set: mean confidence is 0.9781, while accuracy is 0.9562. The confidence-accuracy gap is 0.0219.

The next step is to apply post-hoc temperature scaling using the validation set only, then evaluate the calibrated model on the held-out D1 test set.

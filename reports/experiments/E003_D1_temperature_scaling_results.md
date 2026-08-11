# E003 - Temperature Scaling Calibration Results

## Experiment

E003 - ViT-B/16 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.257989`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9534 | 0.9534 |
| balanced_accuracy | 0.9531 | 0.9531 |
| macro_f1 | 0.9537 | 0.9537 |
| mean_confidence | 0.9775 | 0.9681 |
| confidence_accuracy_gap | 0.0241 | 0.0148 |
| ece_15_bins | 0.0291 | 0.0271 |
| brier_score | 0.0753 | 0.0719 |
| negative_log_likelihood | 0.1654 | 0.1479 |

## Interpretation

Temperature scaling reduced ECE from 0.0291 to 0.0271. NLL also improved from 0.1654 to 0.1479. The confidence-accuracy gap changed from 0.0241 to 0.0148.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.

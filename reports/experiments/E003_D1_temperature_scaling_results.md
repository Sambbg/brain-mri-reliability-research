# E003 - Temperature Scaling Calibration Results

## Experiment

E003 - ViT-B/16 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.229500`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9591 | 0.9591 |
| balanced_accuracy | 0.9589 | 0.9589 |
| macro_f1 | 0.9588 | 0.9588 |
| mean_confidence | 0.9766 | 0.9678 |
| confidence_accuracy_gap | 0.0175 | 0.0088 |
| ece_15_bins | 0.0228 | 0.0169 |
| brier_score | 0.0639 | 0.0630 |
| negative_log_likelihood | 0.1496 | 0.1372 |

## Interpretation

Temperature scaling reduced ECE from 0.0228 to 0.0169. NLL also improved from 0.1496 to 0.1372. The confidence-accuracy gap changed from 0.0175 to 0.0088.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.

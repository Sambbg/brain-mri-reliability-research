# E002 - Temperature Scaling Calibration Results

## Experiment

E002 - EfficientNet-B0 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.176001`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9629 | 0.9629 |
| balanced_accuracy | 0.9626 | 0.9626 |
| macro_f1 | 0.9632 | 0.9632 |
| mean_confidence | 0.9854 | 0.9816 |
| confidence_accuracy_gap | 0.0225 | 0.0188 |
| ece_15_bins | 0.0273 | 0.0238 |
| brier_score | 0.0616 | 0.0599 |
| negative_log_likelihood | 0.1404 | 0.1264 |

## Interpretation

Temperature scaling reduced ECE from 0.0273 to 0.0238. NLL also improved from 0.1404 to 0.1264. The confidence-accuracy gap changed from 0.0225 to 0.0188.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.

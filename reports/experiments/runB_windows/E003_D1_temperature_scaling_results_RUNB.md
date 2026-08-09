# E003 - Temperature Scaling Calibration Results

## Experiment

E003 - ViT-B/16 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.377024`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9648 | 0.9648 |
| balanced_accuracy | 0.9644 | 0.9644 |
| macro_f1 | 0.9648 | 0.9648 |
| mean_confidence | 0.9879 | 0.9790 |
| confidence_accuracy_gap | 0.0231 | 0.0142 |
| ece_15_bins | 0.0273 | 0.0191 |
| brier_score | 0.0621 | 0.0587 |
| negative_log_likelihood | 0.1556 | 0.1270 |

## Interpretation

Temperature scaling reduced ECE from 0.0273 to 0.0191. NLL also improved from 0.1556 to 0.1270. The confidence-accuracy gap changed from 0.0231 to 0.0142.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.

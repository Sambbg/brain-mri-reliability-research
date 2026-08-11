# E003 - Temperature Scaling Calibration Results

## Experiment

E003 - ViT-B/16 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.218531`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9562 | 0.9562 |
| balanced_accuracy | 0.9558 | 0.9558 |
| macro_f1 | 0.9565 | 0.9565 |
| mean_confidence | 0.9779 | 0.9700 |
| confidence_accuracy_gap | 0.0217 | 0.0138 |
| ece_15_bins | 0.0259 | 0.0224 |
| brier_score | 0.0700 | 0.0676 |
| negative_log_likelihood | 0.1442 | 0.1322 |

## Interpretation

Temperature scaling reduced ECE from 0.0259 to 0.0224. NLL also improved from 0.1442 to 0.1322. The confidence-accuracy gap changed from 0.0217 to 0.0138.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.

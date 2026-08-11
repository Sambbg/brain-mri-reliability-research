# E003 - Temperature Scaling Calibration Results

## Experiment

E003 - ViT-B/16 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.233862`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9562 | 0.9562 |
| balanced_accuracy | 0.9559 | 0.9559 |
| macro_f1 | 0.9564 | 0.9564 |
| mean_confidence | 0.9781 | 0.9703 |
| confidence_accuracy_gap | 0.0219 | 0.0140 |
| ece_15_bins | 0.0219 | 0.0153 |
| brier_score | 0.0650 | 0.0628 |
| negative_log_likelihood | 0.1347 | 0.1234 |

## Interpretation

Temperature scaling reduced ECE from 0.0219 to 0.0153. NLL also improved from 0.1347 to 0.1234. The confidence-accuracy gap changed from 0.0219 to 0.0140.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.

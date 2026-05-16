# E003 - Temperature Scaling Calibration Results

## Experiment

E003 - ViT-B/16 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.236274`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9581 | 0.9581 |
| balanced_accuracy | 0.9578 | 0.9578 |
| macro_f1 | 0.9582 | 0.9582 |
| mean_confidence | 0.9740 | 0.9636 |
| confidence_accuracy_gap | 0.0159 | 0.0055 |
| ece_15_bins | 0.0198 | 0.0109 |
| brier_score | 0.0689 | 0.0674 |
| negative_log_likelihood | 0.1571 | 0.1451 |

## Interpretation

Temperature scaling reduced ECE from 0.0198 to 0.0109. NLL also improved from 0.1571 to 0.1451. The confidence-accuracy gap changed from 0.0159 to 0.0055.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.

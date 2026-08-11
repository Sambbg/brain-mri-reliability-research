# E003 - Temperature Scaling Calibration Results

## Experiment

E003 - ViT-B/16 temperature scaling on D1 leakage-aware split

## Method

Temperature scaling was fitted using validation-set logits only. The learned temperature was then applied to the held-out test set. The model weights were not retrained.

## Temperature

- Learned temperature: `1.230566`

## Test Metrics Before and After Temperature Scaling

| Metric | Raw softmax | Temperature-scaled |
|---|---:|---:|
| accuracy | 0.9524 | 0.9524 |
| balanced_accuracy | 0.9521 | 0.9521 |
| macro_f1 | 0.9529 | 0.9529 |
| mean_confidence | 0.9779 | 0.9696 |
| confidence_accuracy_gap | 0.0255 | 0.0172 |
| ece_15_bins | 0.0300 | 0.0225 |
| brier_score | 0.0793 | 0.0763 |
| negative_log_likelihood | 0.1758 | 0.1574 |

## Interpretation

Temperature scaling reduced ECE from 0.0300 to 0.0225. NLL also improved from 0.1758 to 0.1574. The confidence-accuracy gap changed from 0.0255 to 0.0172.

These results are still internal to D1 and should not be interpreted as external reliability evidence. The next major test is whether calibration behaviour changes under cross-dataset evaluation.

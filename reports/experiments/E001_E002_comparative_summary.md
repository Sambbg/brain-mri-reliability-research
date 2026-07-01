# E001 vs E002 Comparative Summary

## Purpose

This summary compares the first two baseline models:

- E001: ResNet18 trained on D1 leakage-aware split
- E002: EfficientNet-B0 trained on D1 leakage-aware split

The purpose is to determine whether the observed D3B domain-shift behaviour is specific to ResNet18 or also appears in a stronger CNN baseline.

## Internal D1 Test Performance

| Metric | E001 ResNet18 | E002 EfficientNet-B0 |
|---|---:|---:|
| Test accuracy | 0.9667 | 0.9676 |
| Test balanced accuracy | 0.9662 | 0.9677 |
| Test macro-F1 | 0.9666 | 0.9680 |
| Best validation macro-F1 | 0.9704 | 0.9736 |
| Best epoch | 8 | 6 |

## Internal D1 Calibration Before Temperature Scaling

| Metric | E001 ResNet18 | E002 EfficientNet-B0 |
|---|---:|---:|
| Accuracy | 0.9667 | 0.9676 |
| Mean confidence | 0.9836 | 0.9812 |
| Confidence-accuracy gap | 0.0169 | 0.0135 |
| ECE, 15 bins | 0.0193 | 0.0196 |
| Brier score | 0.0557 | 0.0533 |
| Negative log-likelihood | 0.1176 | 0.1090 |

## Internal D1 Calibration After Temperature Scaling

| Metric | E001 ResNet18 | E002 EfficientNet-B0 |
|---|---:|---:|
| Learned temperature | 1.2328 | 1.1596 |
| Accuracy | 0.9667 | 0.9676 |
| Macro-F1 | 0.9666 | 0.9680 |
| Mean confidence | 0.9773 | 0.9759 |
| Confidence-accuracy gap | 0.0106 | 0.0082 |
| ECE, 15 bins | 0.0145 | 0.0152 |
| Brier score | 0.0536 | 0.0523 |
| Negative log-likelihood | 0.1063 | 0.1034 |

## D3B Raw Domain-Shift Behaviour

D3B is a glioma-focused domain-shift dataset. These results must not be interpreted as four-class external accuracy.

| Metric | E001 ResNet18 | E002 EfficientNet-B0 |
|---|---:|---:|
| D3B slices | 265 | 265 |
| D3B patients | 53 | 53 |
| Slice-level glioma prediction rate | 0.2943 | 0.4415 |
| Patient-majority glioma rate | 0.2642 | 0.4717 |
| Series-majority glioma rate | 0.2642 | 0.4717 |
| Mean glioma probability | 0.2936 | 0.3879 |
| Median glioma probability | 0.1478 | 0.3442 |
| Mean max confidence | 0.7209 | 0.6837 |
| Mean entropy | 0.7157 | 0.7970 |

## D3B Temperature-Scaled Behaviour

| Metric | E001 ResNet18 | E002 EfficientNet-B0 |
|---|---:|---:|
| Slice-level glioma prediction rate | 0.2943 | 0.4415 |
| Mean glioma probability | 0.2927 | 0.3776 |
| Median glioma probability | 0.1796 | 0.3457 |
| Mean max confidence | 0.6678 | 0.6451 |
| Median max confidence | 0.6548 | 0.6262 |
| Mean entropy | 0.8363 | 0.8838 |
| Patient-majority glioma rate | 0.2642 | 0.4717 |
| Series-majority glioma rate | 0.2642 | 0.4717 |

## Interpretation

E002 EfficientNet-B0 achieved slightly better internal D1 performance than E001 ResNet18, but the improvement was small. Both models achieved high internal accuracy and macro-F1 on the leakage-aware D1 test split.

Both models were slightly overconfident internally before temperature scaling. Temperature scaling improved calibration metrics for both models without changing accuracy or macro-F1.

Under D3B domain shift, EfficientNet-B0 performed better than ResNet18 in terms of glioma prediction rate. However, EfficientNet-B0 still predicted glioma for only 44.15% of D3B slices and only 47.17% of patients by majority vote. This means the stronger CNN baseline reduced but did not eliminate domain-shift instability.

Temperature scaling softened confidence for both models under D3B shift, but it did not change class predictions or majority-vote behaviour. Therefore, the observed D3B failure is not merely a calibration problem. It reflects feature/domain-shift sensitivity.

## Conservative Claim

Across two CNN baselines, high internal D1 performance did not guarantee stable behaviour on a visually distinct glioma-focused D3B dataset. EfficientNet-B0 improved D3B glioma recognition compared with ResNet18, but both models showed substantial domain-shift instability. Post-hoc temperature scaling improved confidence softness but did not correct prediction distribution under D3B shift.

## Do Not Claim

These results do not prove:

1. Clinical diagnostic reliability.
2. Full four-class external accuracy on D3B.
3. Patient-level tumour classification accuracy on D3B.
4. That EfficientNet-B0 is definitively superior to ResNet18.
5. That temperature scaling solves external reliability.

## Next Required Step

The next experiment should test whether a transformer-based architecture, such as ViT-B/16 or Swin-T, behaves differently under the same evaluation pipeline.

Recommended next experiment:

E003 — ViT-B/16 trained on D1 leakage-aware split, followed by D1 calibration, D3B domain-shift evaluation, and D3B temperature-scaled confidence analysis.

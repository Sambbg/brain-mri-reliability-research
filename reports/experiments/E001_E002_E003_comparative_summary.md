# E001 vs E002 vs E003 Comparative Summary

## Purpose

This document compares three baseline models evaluated under the same reliability-focused pipeline:

- E001: ResNet18
- E002: EfficientNet-B0
- E003: ViT-B/16

All models were trained on the D1 leakage-aware split and evaluated using internal D1 performance, internal calibration, post-hoc temperature scaling, and D3B glioma-focused domain-shift behaviour.

## Internal D1 Test Performance

| Metric | E001 ResNet18 | E002 EfficientNet-B0 | E003 ViT-B/16 |
|---|---:|---:|---:|
| Test accuracy | 0.9667 | 0.9676 | 0.9581 |
| Test balanced accuracy | 0.9662 | 0.9677 | 0.9578 |
| Test macro-F1 | 0.9666 | 0.9680 | 0.9582 |
| Best validation macro-F1 | 0.9704 | 0.9736 | 0.9667 |
| Best epoch | 8 | 6 | 5 |

## Internal D1 Calibration Before Temperature Scaling

| Metric | E001 ResNet18 | E002 EfficientNet-B0 | E003 ViT-B/16 |
|---|---:|---:|---:|
| Accuracy | 0.9667 | 0.9676 | 0.9581 |
| Mean confidence | 0.9836 | 0.9812 | 0.9740 |
| Confidence-accuracy gap | 0.0169 | 0.0135 | 0.0159 |
| ECE, 15 bins | 0.0193 | 0.0196 | 0.0198 |
| Brier score | 0.0557 | 0.0533 | 0.0689 |
| Negative log-likelihood | 0.1176 | 0.1090 | 0.1571 |

## Internal D1 Calibration After Temperature Scaling

| Metric | E001 ResNet18 | E002 EfficientNet-B0 | E003 ViT-B/16 |
|---|---:|---:|---:|
| Learned temperature | 1.2328 | 1.1596 | 1.2363 |
| Accuracy | 0.9667 | 0.9676 | 0.9581 |
| Macro-F1 | 0.9666 | 0.9680 | 0.9582 |
| Mean confidence | 0.9773 | 0.9759 | 0.9636 |
| Confidence-accuracy gap | 0.0106 | 0.0082 | 0.0055 |
| ECE, 15 bins | 0.0145 | 0.0152 | 0.0109 |
| Brier score | 0.0536 | 0.0523 | 0.0674 |
| Negative log-likelihood | 0.1063 | 0.1034 | 0.1451 |

## D3B Raw Domain-Shift Behaviour

D3B is a glioma-focused domain-shift dataset. These results must not be interpreted as four-class external accuracy.

| Metric | E001 ResNet18 | E002 EfficientNet-B0 | E003 ViT-B/16 |
|---|---:|---:|---:|
| D3B slices | 265 | 265 | 265 |
| D3B patients | 53 | 53 | 53 |
| Slice-level glioma prediction rate | 0.2943 | 0.4415 | 0.4038 |
| Patient-majority glioma rate | 0.2642 | 0.4717 | 0.3774 |
| Series-majority glioma rate | 0.2642 | 0.4717 | 0.3774 |
| Mean glioma probability | 0.2936 | 0.3879 | 0.3553 |
| Median glioma probability | 0.1478 | 0.3442 | 0.3185 |
| Mean max confidence | 0.7209 | 0.6837 | 0.7203 |
| Mean entropy | 0.7157 | 0.7970 | 0.6748 |

## D3B Temperature-Scaled Behaviour

| Metric | E001 ResNet18 | E002 EfficientNet-B0 | E003 ViT-B/16 |
|---|---:|---:|---:|
| Slice-level glioma prediction rate | 0.2943 | 0.4415 | 0.4038 |
| Mean glioma probability | 0.2927 | 0.3776 | 0.3488 |
| Median glioma probability | 0.1796 | 0.3457 | 0.3349 |
| Mean max confidence | 0.6678 | 0.6451 | 0.6710 |
| Median max confidence | 0.6548 | 0.6262 | 0.6610 |
| Mean entropy | 0.8363 | 0.8838 | 0.7913 |
| Patient-majority glioma rate | 0.2642 | 0.4717 | 0.3774 |
| Series-majority glioma rate | 0.2642 | 0.4717 | 0.3774 |

## Key Findings

EfficientNet-B0 achieved the strongest internal D1 performance, followed closely by ResNet18. ViT-B/16 performed worse internally than both CNN baselines.

All three models showed strong internal D1 test performance, but this did not translate into stable D3B domain-shift behaviour.

Under D3B shift, EfficientNet-B0 had the highest glioma prediction rate, followed by ViT-B/16, then ResNet18. However, none of the three models predicted glioma for a majority of D3B slices.

Temperature scaling improved internal calibration metrics for all three models. It also softened confidence on D3B, reducing maximum softmax confidence and increasing entropy. However, it did not change class predictions or patient-majority behaviour under D3B shift.

## Conservative Interpretation

Across three architectures, high internal D1 performance did not guarantee stable behaviour on a visually distinct glioma-focused D3B dataset. The failure pattern is not restricted to one model family. EfficientNet-B0 performed best under D3B shift, but still failed to recognise glioma as the majority prediction across D3B slices.

Temperature scaling improved confidence calibration but did not correct domain-shift prediction instability. This supports the central argument that calibration alone is insufficient evidence of clinical or cross-dataset reliability.

## Do Not Claim

These results do not prove:

1. Clinical diagnostic reliability.
2. Full four-class external accuracy on D3B.
3. Patient-level tumour classification accuracy on D3B.
4. That ViT-B/16 is generally inferior to CNNs.
5. That EfficientNet-B0 is clinically reliable.
6. That temperature scaling solves external reliability.
7. That D3B is a complete external validation dataset.

## Strongest Defensible Claim

A leakage-aware, calibration-aware, cross-dataset evaluation pipeline showed that three high-performing D1-trained models failed to maintain stable glioma-domain prediction behaviour on visually distinct D3B images. Post-hoc temperature scaling improved confidence softness but did not correct prediction distribution under dataset shift.

## Next Required Step

The next step should be to produce an integrated results narrative for the thesis/paper draft, linking:

1. D1 leakage-aware internal performance.
2. D2 rejection due to D1-D2 overlap.
3. D3B selection and conversion.
4. Cross-model D3B domain-shift behaviour.
5. Why calibration alone is insufficient.

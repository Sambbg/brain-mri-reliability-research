# Shifted-domain prediction behaviour

Mean ± SD across seeds 42-46. Run set `2026-08-sweep-a`.

Neither probe reproduces the four-class D1 label structure, so these are prediction and confidence behaviour under shift, not diagnostic accuracy.

## D3B ? cross-species (canine)

53 patients, 265 slices.

| Architecture | Slice glioma rate | Patient-majority | Mean confidence | Mean entropy | Median glioma prob |
|---|---|---|---|---|---|
| ResNet18 | 0.4023 ± 0.1227 | 0.4075 ± 0.1507 | 0.7138 ± 0.0347 | 0.7052 ± 0.0823 | 0.2976 ± 0.2076 |
| EfficientNet-B0 | 0.3683 ± 0.1396 | 0.3887 ± 0.1648 | 0.7306 ± 0.0308 | 0.6850 ± 0.0768 | 0.2360 ± 0.1962 |
| ViT-B/16 | 0.2491 ± 0.0656 | 0.2377 ± 0.0762 | 0.7821 ± 0.0314 | 0.5483 ± 0.0756 | 0.1311 ± 0.0508 |

Predicted-class distribution across the four D1 classes:

| Architecture | Glioma | Meningioma | No tumour | Pituitary |
|---|---|---|---|---|
| ResNet18 | 0.402 ± 0.123 | 0.170 ± 0.035 | 0.261 ± 0.138 | 0.167 ± 0.114 |
| EfficientNet-B0 | 0.368 ± 0.140 | 0.155 ± 0.059 | 0.205 ± 0.035 | 0.272 ± 0.148 |
| ViT-B/16 | 0.249 ± 0.066 | 0.291 ± 0.151 | 0.430 ± 0.107 | 0.029 ± 0.033 |

Temperature scaling on this probe. Predictions are unchanged by construction ? scaling is monotonic in the logits ? so only confidence moves:

| Architecture | Glioma rate raw ? scaled | Confidence raw ? scaled | Entropy raw ? scaled |
|---|---|---|---|
| ResNet18 | 0.4023 ± 0.1227 ? 0.4023 ± 0.1227 | 0.7138 ± 0.0347 ? 0.6670 ± 0.0330 | 0.7052 ± 0.0823 ? 0.8114 ± 0.0713 |
| EfficientNet-B0 | 0.3683 ± 0.1396 ? 0.3683 ± 0.1396 | 0.7306 ± 0.0308 ? 0.6834 ± 0.0214 | 0.6850 ± 0.0768 ? 0.7967 ± 0.0455 |
| ViT-B/16 | 0.2491 ± 0.0656 ? 0.2491 ± 0.0656 | 0.7821 ± 0.0314 ? 0.7368 ± 0.0364 | 0.5483 ± 0.0756 ? 0.6600 ± 0.0859 |

## D3C ? same-species (human)

610 patients, 3050 slices.

| Architecture | Slice glioma rate | Patient-majority | Mean confidence | Mean entropy | Median glioma prob |
|---|---|---|---|---|---|
| ResNet18 | 0.6744 ± 0.0727 | 0.6882 ± 0.0760 | 0.7837 ± 0.0523 | 0.5418 ± 0.1262 | 0.6979 ± 0.1212 |
| EfficientNet-B0 | 0.5138 ± 0.0646 | 0.5207 ± 0.0761 | 0.8115 ± 0.0484 | 0.4859 ± 0.1243 | 0.4843 ± 0.1473 |
| ViT-B/16 | 0.2635 ± 0.1139 | 0.2607 ± 0.1225 | 0.8596 ± 0.0387 | 0.3528 ± 0.0947 | 0.1017 ± 0.1556 |

Predicted-class distribution across the four D1 classes:

| Architecture | Glioma | Meningioma | No tumour | Pituitary |
|---|---|---|---|---|
| ResNet18 | 0.674 ± 0.073 | 0.007 ± 0.004 | 0.271 ± 0.066 | 0.048 ± 0.046 |
| EfficientNet-B0 | 0.514 ± 0.065 | 0.013 ± 0.005 | 0.416 ± 0.099 | 0.057 ± 0.034 |
| ViT-B/16 | 0.263 ± 0.114 | 0.077 ± 0.051 | 0.628 ± 0.169 | 0.032 ± 0.042 |

Temperature scaling on this probe. Predictions are unchanged by construction ? scaling is monotonic in the logits ? so only confidence moves:

| Architecture | Glioma rate raw ? scaled | Confidence raw ? scaled | Entropy raw ? scaled |
|---|---|---|---|
| ResNet18 | 0.6744 ± 0.0727 ? 0.6744 ± 0.0727 | 0.7837 ± 0.0523 ? 0.7422 ± 0.0490 | 0.5418 ± 0.1262 ? 0.6461 ± 0.1120 |
| EfficientNet-B0 | 0.5138 ± 0.0646 ? 0.5138 ± 0.0646 | 0.8115 ± 0.0484 ? 0.7740 ± 0.0376 | 0.4859 ± 0.1243 ? 0.5845 ± 0.0960 |
| ViT-B/16 | 0.2635 ± 0.1139 ? 0.2635 ± 0.1139 | 0.8596 ± 0.0387 ? 0.8272 ± 0.0472 | 0.3528 ± 0.0947 ? 0.4396 ± 0.1141 |


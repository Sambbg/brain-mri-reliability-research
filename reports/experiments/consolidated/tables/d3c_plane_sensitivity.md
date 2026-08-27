# D3C imaging-plane sensitivity analysis

Generated: 2026-08-27T13:41:51

Eleven of the 610 D3C patients carry series acquired more than 10 degrees from axial. Imaging plane is a plausible alternative explanation for the shifted-domain prediction behaviour reported in Section 4.6, so every D3C behavioural metric is recomputed with those patients removed.

Full cohort: 610 patients / 3050 slices. Sensitivity cohort: 599 patients / 2995 slices (11 patients, 55 slices removed).

Oblique flags sourced from: manifest column `oblique_gt_10deg`. This filters saved per-slice predictions; no model was retrained or re-run.

## Glioma prediction rate, full versus sensitivity cohort

| Architecture | Full cohort | Oblique dropped | Difference |
|---|---|---|---|
| ResNet18 | 0.6744 ± 0.0727 | 0.6796 ± 0.0740 | +0.0052 |
| EfficientNet-B0 | 0.5138 ± 0.0646 | 0.5163 ± 0.0648 | +0.0026 |
| ViT-B/16 | 0.2635 ± 0.1139 | 0.2631 ± 0.1147 | -0.0004 |

## Patient-majority glioma rate

| Architecture | Full cohort | Oblique dropped | Difference |
|---|---|---|---|
| ResNet18 | 0.6928 ± 0.0725 | 0.6988 ± 0.0725 | +0.0060 |
| EfficientNet-B0 | 0.5203 ± 0.0741 | 0.5232 ± 0.0749 | +0.0029 |
| ViT-B/16 | 0.2639 ± 0.1223 | 0.2634 ± 0.1239 | -0.0005 |

## Confidence and entropy

| Architecture | Confidence full ? dropped | Entropy full ? dropped |
|---|---|---|
| ResNet18 | 0.7837 ? 0.7838 | 0.5418 ? 0.5414 |
| EfficientNet-B0 | 0.8115 ? 0.8112 | 0.4859 ? 0.4864 |
| ViT-B/16 | 0.8596 ? 0.8597 | 0.3528 ? 0.3525 |

## Architecture ordering

- Full cohort: ResNet18 > EfficientNet-B0 > ViT-B/16
- Oblique dropped: ResNet18 > EfficientNet-B0 > ViT-B/16
- Ordering preserved: **yes**

## Interpretation

Removing the 11 oblique patients changes the mean glioma prediction rate by at most 0.0052 and leaves the architecture ordering unchanged. The between-architecture separation reported in Section 4.6 is therefore not an artefact of imaging plane, and the full cohort is retained for the primary analysis.

Because the sensitivity cohort is a strict subset of the full cohort and the eleven removed patients are a small fraction of the total, this analysis bounds the plane effect rather than eliminating it. Obliquity below the 10-degree threshold is not controlled.


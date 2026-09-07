# Baseline glioma-propensity control

The D3C result reports that the three architectures assign human glioblastoma
slices to the glioma class at very different rates. That is interpreted as
behaviour under shift. This check tests the competing explanation: that the
architectures simply differ in how readily they assign anything to glioma.

The decisive measure is the **off-target glioma rate** on the internal test
set: of the D1 test images that are not glioma, what share does each model
assign to glioma anyway? That isolates glioma-ward bias from glioma
competence.

## Results, mean +/- SD across five seeds

| Measure | ResNet18 | EfficientNet-B0 | ViT-B/16 | Ordering |
|---|---|---|---|---|
| Internal glioma prediction rate (all test images) | 0.2539 ± 0.0019 | 0.2521 ± 0.0083 | 0.2565 ± 0.0092 | ViT-B/16 > ResNet18 > EfficientNet-B0 |
| Internal off-target glioma rate (non-glioma images only) | 0.0105 ± 0.0046 | 0.0107 ± 0.0079 | 0.0174 ± 0.0087 | ViT-B/16 > EfficientNet-B0 > ResNet18 |
| Internal mean predicted glioma probability | 0.2582 ± 0.0042 | 0.2531 ± 0.0066 | 0.2555 ± 0.0080 | ResNet18 > ViT-B/16 > EfficientNet-B0 |
| Internal glioma recall | 0.9613 ± 0.0090 | 0.9539 ± 0.0119 | 0.9517 ± 0.0112 | ResNet18 > EfficientNet-B0 > ViT-B/16 |
| D3C glioma assignment rate | 0.6744 ± 0.0727 | 0.5138 ± 0.0646 | 0.2635 ± 0.1139 | ResNet18 > EfficientNet-B0 > ViT-B/16 |
| D3B glioma assignment rate | 0.4023 ± 0.1227 | 0.3683 ± 0.1396 | 0.2491 ± 0.0656 | ResNet18 > EfficientNet-B0 > ViT-B/16 |

## Separation

| Measure | Between-arch spread | Mean seed SD | SNR |
|---|---|---|---|
| Internal off-target glioma rate | 0.0069 | 0.0071 | 0.98 |
| D3C glioma assignment rate | 0.4109 | 0.0837 | 4.91 |

## Verdict

**The D3C ordering does not match the internal off-target ordering.**

- D3C: ResNet18 > EfficientNet-B0 > ViT-B/16
- Internal off-target: ViT-B/16 > EfficientNet-B0 > ResNet18

Baseline glioma propensity does not explain the D3C separation. The
architectures that assign more D3C slices to glioma are not the ones most
disposed to assign non-glioma internal images to glioma, so the separation
is a property of behaviour under shift rather than of a class prior.

This strengthens the manuscript's central result and should be reported.

Ordering by internal glioma rate over all test images: ViT-B/16 > ResNet18 > EfficientNet-B0
(matches D3C ordering: no)

## Reporting

Whichever way this resolves, it belongs in the manuscript. A reviewer who
thinks of the propensity explanation will ask for exactly this table, and it
costs two sentences in Section 3.4 plus one row in a supplementary table.


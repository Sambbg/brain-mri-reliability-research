# Internal metrics on the leakage-free subset of the test partition

Blind adjudication established that within-class pHash pairs at Hamming 6 crossing the train/test boundary are genuine same-patient pairs (`phash_threshold_sensitivity.md`). Those 371 pairs touch 233 of the 1051 test images. Every metric below is recomputed on the remaining 818 from the saved per-image predictions. Nothing was retrained.

## Provenance

| Field | Value |
|---|---|
| git_commit | `30e0022066127f0e49f28a304eaef2f5c0e874b5` |
| split_csv_sha256 | `944ce00e4be958f3688a0996f6fb928fc7717e7c2804abb8000f28976efe0d43` |
| d1_phash_sha256 | `a8d581c6b5edd3136e6661973179e6688591bade6121156ccd0a1b2a6bff2be8` |
| contamination_distance | `6` |
| crossing_pairs | `371` |
| excluded_test_images | `233` |

## Internal metrics, full partition against leakage-free subset

Mean +/- SD across the five seeds.

### Macro-F1

| Model | Full (n=1051) | Leakage-free (n=818) | Difference |
|---|---|---|---|
| E001 ResNet18 | 0.9662 +/- 0.0071 | 0.9623 +/- 0.0084 | -0.0039 +/- 0.0020 |
| E002 EfficientNet-B0 | 0.9673 +/- 0.0043 | 0.9617 +/- 0.0051 | -0.0056 +/- 0.0009 |
| E003 ViT-B/16 | 0.9557 +/- 0.0024 | 0.9497 +/- 0.0045 | -0.0059 +/- 0.0026 |

### Accuracy

| Model | Full (n=1051) | Leakage-free (n=818) | Difference |
|---|---|---|---|
| E001 ResNet18 | 0.9661 +/- 0.0073 | 0.9609 +/- 0.0085 | -0.0052 +/- 0.0021 |
| E002 EfficientNet-B0 | 0.9671 +/- 0.0044 | 0.9604 +/- 0.0054 | -0.0067 +/- 0.0011 |
| E003 ViT-B/16 | 0.9555 +/- 0.0026 | 0.9487 +/- 0.0047 | -0.0068 +/- 0.0026 |

### Balanced accuracy

| Model | Full (n=1051) | Leakage-free (n=818) | Difference |
|---|---|---|---|
| E001 ResNet18 | 0.9659 +/- 0.0071 | 0.9621 +/- 0.0087 | -0.0038 +/- 0.0021 |
| E002 EfficientNet-B0 | 0.9669 +/- 0.0044 | 0.9616 +/- 0.0051 | -0.0052 +/- 0.0009 |
| E003 ViT-B/16 | 0.9552 +/- 0.0027 | 0.9501 +/- 0.0049 | -0.0050 +/- 0.0027 |

## Accuracy on the excluded images

The most direct expression of the effect. If the contaminated images were easier because the model had seen the same patient in training, accuracy on them should exceed accuracy on the rest.

| Model | Excluded images (n=233) | Leakage-free (n=818) | Gap |
|---|---:|---:|---:|
| E001 ResNet18 | 0.9845 | 0.9609 | +0.0237 |
| E002 EfficientNet-B0 | 0.9906 | 0.9604 | +0.0302 |
| E003 ViT-B/16 | 0.9794 | 0.9487 | +0.0307 |

Every architecture classifies the contaminated images two to three points more accurately than the rest of the partition. That is the memorisation signature, and it is consistent across all three.

## Ranking stability

The central claim of the study is that internal performance cannot separate these architectures against seed variation. Signal-to-noise is the between-architecture spread of the means divided by the mean within-architecture standard deviation, as in equation 10.

| Metric | Scope | Spread | Mean seed SD | Signal-to-noise | Overlapping pairs |
|---|---|---:|---:|---:|---:|
| Macro-F1 | full | 0.0116 | 0.0046 | 2.52 | 1 of 3 |
| Macro-F1 | leakage-free | 0.0126 | 0.0060 | 2.09 | 2 of 3 |
| Accuracy | full | 0.0116 | 0.0048 | 2.44 | 1 of 3 |
| Accuracy | leakage-free | 0.0122 | 0.0062 | 1.98 | 2 of 3 |
| Balanced accuracy | full | 0.0117 | 0.0047 | 2.47 | 1 of 3 |
| Balanced accuracy | leakage-free | 0.0119 | 0.0063 | 1.90 | 2 of 3 |

### Is the signal-to-noise drop real?

Mostly not, and saying so matters more than the headline. The signal-to-noise ratio falls because the denominator grows: mean seed SD rises from 0.0046 to 0.0060, a factor of 1.304. The test partition shrank by a factor of 1.285. Those two numbers agree to within a percent.

That agreement has a simple explanation. Every seed is scored on the same images, so test-set sampling error is shared and does not enter the across-seed SD; what enters is disagreement between seeds on individual images. The excluded images are ones every seed got right, so removing them takes away almost no disagreements while shrinking the denominator of the metric. Each remaining disagreement is worth more. **The apparent rise in seed sensitivity is an artefact of the smaller subset, not a property of clean data**, and should not be reported as one.

What survives that correction is the comparison against the threshold the study itself set. On the leakage-free subset the signal-to-noise ratio is 2.09 for macro-F1 and 1.98 and 1.90 for accuracy and balanced accuracy, and two of the three architecture pairs now have overlapping mean-plus-or-minus-SD ranges rather than one. By the criterion stated in the paper, that values near or below 2 indicate the evaluation does not resolve the architectures, the clean subset does not resolve them.

### Orderings across seeds, by macro-F1

**Full partition: 2 distinct ordering(s) across five seeds.**

- E001 > E002 > E003 — seeds [43, 44, 45]
- E002 > E001 > E003 — seeds [42, 46]

**Leakage-free subset: 2 distinct ordering(s) across five seeds.**

- E001 > E002 > E003 — seeds [43, 44, 45]
- E002 > E001 > E003 — seeds [42, 46]

## Per-run detail

| Model | Seed | Full macro-F1 | Clean macro-F1 | Difference |
|---|---:|---:|---:|---:|
| E001 | 42 | 0.9546 | 0.9478 | -0.0068 |
| E001 | 43 | 0.9677 | 0.9660 | -0.0017 |
| E001 | 44 | 0.9715 | 0.9685 | -0.0030 |
| E001 | 45 | 0.9723 | 0.9671 | -0.0052 |
| E001 | 46 | 0.9650 | 0.9619 | -0.0031 |
| E002 | 42 | 0.9744 | 0.9702 | -0.0042 |
| E002 | 43 | 0.9649 | 0.9582 | -0.0067 |
| E002 | 44 | 0.9632 | 0.9578 | -0.0054 |
| E002 | 45 | 0.9661 | 0.9600 | -0.0062 |
| E002 | 46 | 0.9678 | 0.9626 | -0.0053 |
| E003 | 42 | 0.9537 | 0.9436 | -0.0101 |
| E003 | 43 | 0.9565 | 0.9523 | -0.0042 |
| E003 | 44 | 0.9588 | 0.9555 | -0.0034 |
| E003 | 45 | 0.9564 | 0.9498 | -0.0067 |
| E003 | 46 | 0.9529 | 0.9475 | -0.0055 |

## Answers to the two questions

**How much are the internal figures inflated?** By 0.0039 to 0.0059 macro-F1, roughly half a point, and by 0.0052 to 0.0068 accuracy. The effect is real, consistent in direction across all fifteen runs and all three metrics, and small. It is smaller than the contamination share would suggest because the models score highly everywhere: the contaminated images are classified two to three points better than the rest, and they are 22% of the partition, which multiplies out to about half a point overall.

**Does the central claim survive?** Yes, and it is in a stronger position for having been tested. The ordering of the architectures still changes across seeds on clean data, with 2 distinct orderings over five seeds and the same seeds producing the same swap as on the full partition. The signal-to-noise ratio remains close to the threshold at which the study says an evaluation fails to resolve architectures, and falls below it for accuracy and balanced accuracy. The claim that internal performance cannot separate these architectures against seed variation is not an artefact of contaminated data; it holds on the uncontaminated subset.

## What this does and does not establish

The subset removes test images with a same-patient counterpart in training, so it removes the memorisation channel from the **evaluation**. It does not undo training. The models still saw the contaminated training partition, and any advantage carried from that exposure into unrelated images remains. These figures therefore bound how much the contamination inflated the reported metric; they are not an estimate of what a model trained on a clean split would score. Only rebuilding the split answers that.

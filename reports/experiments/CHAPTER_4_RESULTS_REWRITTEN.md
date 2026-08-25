# Chapter 4 ? Results

*Rewritten against run set `2026-08-sweep-a` (seeds 42?46 × 3 architectures,
15 runs). All values are means ± standard deviations across seeds unless stated
otherwise. Every figure and table referenced here is generated programmatically
from `reports/experiments/consolidated/`.*

---

## 4.1 Dataset audit and usage decisions

The dataset audit determined the final evaluation design. Four dataset roles were
defined: D1 as the internal development dataset, D2 as a rejected external-validation
candidate, and two independent glioma-focused shifted-domain probes ? D3B, a
cross-species canine collection, and D3C, a same-species human glioblastoma collection.

D1 was retained for training, validation and internal testing. Exact-duplicate auditing
by SHA-256 removed 187 images across 153 duplicate groups from the 7,200 distributed,
leaving 7,013 unique images. Perceptual hashing at a Hamming threshold of 4 then detected
5,125 near-duplicate pairs, of which 1,926 crossed the distributed train/test boundary.
Because visually near-identical images appeared on both sides of that boundary, the
distributed split was not used. A leakage-aware split was constructed instead by forming
connected components over near-duplicate pairs and assigning whole groups ? never
individual images ? to the training, validation and test partitions in 70/15/15
proportions, yielding 4,909 / 1,053 / 1,051 images and no near-duplicate pair crossing
any partition boundary. The split file is fixed for the study and is identified by
SHA-256 `944ce00e?`; every run reported below was trained on that identical split.

D2 was rejected. Of its 5,950 images, 4,740 were byte-identical to images in D1 under
SHA-256 ? approximately four-fifths of the dataset ? with a further 7,290 perceptual
near-duplicate pairs, 5,037 of them at Hamming distance zero. D2 is substantially a
repackaging of the same underlying images as D1. Had it been used as external validation,
the resulting figure would have been measured largely on images seen during training. It
was excluded from every performance and generalisation claim. This rejection is reported
as a methodological result: independence between separately named public benchmarks must
be demonstrated, not assumed.

Both shifted-domain probes passed the same audit. D3B returned no exact and no perceptual
near-duplicates against D1 across 1,858,445 comparisons. D3C returned no exact overlaps
and seven within-class near-duplicate pairs across 19,951,985 comparisons, with no
cross-class pairs; the flagged pairs were concentrated in two patients, reviewed, and
retained as coincidental anatomical similarity between central glioma slices.

A separate audit addressed a preprocessing concern recorded earlier in the project. D3C
is distributed as `Processed_CaPTk`, which had been assumed to imply skull stripping and
therefore a systematic difference from the unstripped D1 images. Measured across 40
randomly sampled D3C series against 40 matched D1 glioma images, this assumption proved
false: no D3C image had a masked background, the air region was 26.2% exactly zero at the
median where a mask would give 1.0, image corners were 54.0% non-zero, and 25.6% of
outer-ring pixels exceeded the brain-core median, which is the T1 scalp-fat signature.
The same measurements taken from the source DICOM matched the converted PNGs, ruling out
the conversion as a cause. D3C retains extracranial anatomy throughout and is, on these
measures, *less* masked than D1 (air exactly-zero 0.262 versus 0.373). The
skull-stripping confound was therefore withdrawn. Weaker preprocessing differences ?
CaPTk co-registration, resampling and intensity normalisation ? remain and are carried
into the limitations.

| Dataset | Cohort | Role | Decision |
|---|---|---|---|
| D1 | 7,013 images, four classes | Internal training, validation, testing | Retained |
| D2 | 5,950 images | Candidate external validation | Rejected: 4,740 byte-identical to D1 |
| D3B | 53 patients / 265 slices | Cross-species shifted-domain probe | Retained, glioma-focused only |
| D3C | 610 patients / 3,050 slices | Same-species shifted-domain probe | Retained, glioma-focused only |

**Table 4.1.** Final dataset roles after auditing. Neither probe reproduces the four-class
D1 label structure, so neither supports a four-class external accuracy figure.

---

## 4.2 Run set and provenance

All results below derive from a single run set, `2026-08-sweep-a`: three architectures
trained at five random seeds (42?46), giving 15 runs. Each run records its git commit,
seed, data-split SHA-256 and checkpoint SHA-256. Before any summary is produced, an
automated check verifies that all runs share one run identifier, an identical split hash,
matching seed sets across architectures, and identical probe cohorts; the summary is
refused otherwise.

This procedure replaces an earlier reporting practice in which results were assembled
from more than one set of trained checkpoints. Two earlier run sets ? Run A (Ubuntu) and
Run B (Windows) ? are preserved as the historical record and are superseded in full.
No value from either appears in this chapter.

Reporting five seeds rather than one is not a cosmetic change. As Sections 4.3 and 4.7
show, the between-architecture differences in internal performance are of the same order
as the variation induced by the random seed alone, so a single-run comparison of these
architectures is not interpretable.

---

## 4.3 Internal performance on D1

All three architectures reached high internal performance on the held-out leakage-aware
test partition, with test macro-F1 means between 0.9557 and 0.9673 (Table 4.2).

| Architecture | Test accuracy | Balanced accuracy | Test macro-F1 |
|---|---|---|---|
| ResNet18 | 0.9660 ± 0.0072 | 0.9658 ± 0.0072 | 0.9662 ± 0.0071 |
| EfficientNet-B0 | 0.9672 ± 0.0043 | 0.9674 ± 0.0043 | 0.9673 ± 0.0043 |
| ViT-B/16 | 0.9557 ± 0.0024 | 0.9554 ± 0.0025 | 0.9557 ± 0.0024 |

**Table 4.2.** Internal classification performance on the D1 test partition
(n = 1,051), mean ± SD across seeds 42?46.

The important feature of Table 4.2 is not the ordering but its fragility. The spread
between architecture means in test macro-F1 is 0.0116, against a mean within-architecture
standard deviation across seeds of 0.0046 ? a ratio of 2.52. The two convolutional models
differ by 0.0011, roughly a quarter of one standard deviation, and their per-seed ranges
overlap almost entirely (ResNet18 0.9546?0.9723; EfficientNet-B0 0.9632?0.9744).
Across the five seeds the architecture ordering by internal macro-F1 takes two distinct
forms, with EfficientNet-B0 ranking first at two seeds and ResNet18 at three.

Only the ViT-B/16 versus EfficientNet-B0 contrast is separated cleanly, with
non-overlapping ranges. The two convolutional models are not distinguishable on this
metric at this sample of seeds. A single-run internal comparison of these three
architectures ? the design used almost universally in the brain MRI classification
literature ? would report a difference that is within seed noise.

Per-class performance is consistent across architectures (Table 4.3). Pituitary tumour is
the best-recognised class for all three (F1 0.9770?0.9905). The principal internal
confusion is between no-tumour and meningioma: meningioma precision is the lowest
per-class value for every architecture (0.9217?0.9289) while meningioma recall is among
the highest (0.9603?0.9768), indicating that images from other classes ? chiefly
no-tumour ? are drawn into the meningioma class. No architecture confuses glioma with
pituitary in either direction at any seed.

| Architecture | Glioma | Meningioma | No tumour | Pituitary |
|---|---|---|---|---|
| ResNet18 | 0.9653 ± 0.0106 | 0.9487 ± 0.0112 | 0.9608 ± 0.0047 | 0.9901 ± 0.0044 |
| EfficientNet-B0 | 0.9611 ± 0.0081 | 0.9513 ± 0.0102 | 0.9663 ± 0.0046 | 0.9905 ± 0.0023 |
| ViT-B/16 | 0.9507 ± 0.0071 | 0.9404 ± 0.0106 | 0.9546 ± 0.0040 | 0.9770 ± 0.0037 |

**Table 4.3.** Per-class F1 on the D1 test partition, mean ± SD across seeds.

These metrics are interpreted narrowly. They establish that high internal performance is
achievable across three architecture families on a leakage-controlled split. They do not
by themselves demonstrate calibration quality, external generalisation, or clinical
reliability, and ? as the spread above shows ? they do not reliably rank the
architectures that produced them.

---

## 4.4 Internal calibration and temperature scaling

All three architectures were mildly overconfident before scaling, with expected
calibration error between 0.0158 and 0.0259 and every learned temperature above one
(Table 4.4). Temperature scaling improved every calibration metric for every
architecture: expected calibration error, negative log-likelihood, Brier score and the
confidence?accuracy gap all fell. Because scaling is monotonic in the logits, accuracy,
balanced accuracy, macro-F1 and the confusion matrix are unchanged.

| Architecture | T | ECE raw ? scaled | NLL raw ? scaled | Brier raw ? scaled | Conf?acc gap raw ? scaled |
|---|---|---|---|---|---|
| ResNet18 | 1.2257 ± 0.0663 | 0.0158 ± 0.0030 ? 0.0113 ± 0.0016 | 0.1186 ± 0.0167 ? 0.1101 ± 0.0115 | 0.0529 ± 0.0077 ? 0.0519 ± 0.0071 | 0.0108 ± 0.0067 ? 0.0034 ± 0.0062 |
| EfficientNet-B0 | 1.2263 ± 0.1023 | 0.0194 ± 0.0055 ? 0.0155 ± 0.0051 | 0.1190 ± 0.0147 ? 0.1069 ± 0.0141 | 0.0518 ± 0.0076 ? 0.0504 ± 0.0073 | 0.0160 ± 0.0066 ? 0.0113 ± 0.0062 |
| ViT-B/16 | 1.2341 ± 0.0145 | 0.0259 ± 0.0036 ? 0.0208 ± 0.0048 | 0.1539 ± 0.0165 ? 0.1396 ± 0.0133 | 0.0707 ± 0.0066 ? 0.0683 ± 0.0058 | 0.0221 ± 0.0030 ? 0.0137 ± 0.0031 |

**Table 4.4.** Internal calibration on the D1 test partition before and after post-hoc
temperature scaling, mean ± SD across seeds. Lower is better throughout.

Two observations follow, both of which are visible only when seeds are aggregated.

First, **the learned temperature is a property of the checkpoint, not of the
architecture.** The three architecture means are nearly identical (1.226, 1.226, 1.234),
while the variation across seeds within a single architecture is larger than the variation
between architectures: ResNet18 alone spans 1.1519 to 1.3113, and EfficientNet-B0 spans
1.0700 to 1.3076. Any interpretation attaching a characteristic temperature to an
architecture, on the basis of a single training run, describes that run rather than that
architecture.

Second, **ViT-B/16 is consistently the worst-calibrated of the three**, both before and
after scaling, on all four metrics. It retains the highest expected calibration error
(0.0208 ± 0.0048 after scaling against ResNet18's 0.0113 ± 0.0016), the highest negative
log-likelihood and the highest Brier score. This is consistent across all five seeds and
mirrors its slightly lower internal macro-F1.

The scope of this result is in-distribution. It establishes that D1-trained models are
well calibrated on D1 and that temperature scaling refines rather than rescues that
calibration. Whether internal calibration transfers to visually distinct data is a
separate question, examined in Sections 4.5 and 4.6.

---

## 4.5 D3B ? cross-species (canine) shifted-domain evaluation

D3B is the cross-species probe: 265 central slices from 53 canine patients, carrying a
single collection-level glioma label. It represents the most severe covariate shift in
the study, since the D1-trained models had never encountered canine neuroanatomy.

No architecture assigned a majority of canine glioma slices to the glioma class
(Table 4.5). Slice-level glioma prediction rates were 0.4023 ± 0.1227 for ResNet18,
0.3683 ± 0.1396 for EfficientNet-B0, and 0.2491 ± 0.0656 for ViT-B/16, with
patient-majority rates closely tracking the slice-level figures.

| Architecture | Slice glioma rate | Patient-majority | Mean confidence | Mean entropy |
|---|---|---|---|---|
| ResNet18 | 0.4023 ± 0.1227 | 0.4075 ± 0.1507 | 0.7138 ± 0.0347 | 0.7052 ± 0.0823 |
| EfficientNet-B0 | 0.3683 ± 0.1396 | 0.3887 ± 0.1648 | 0.7306 ± 0.0308 | 0.6850 ± 0.0768 |
| ViT-B/16 | 0.2491 ± 0.0656 | 0.2377 ± 0.0762 | 0.7821 ± 0.0314 | 0.5483 ± 0.0756 |

**Table 4.5.** D3B shifted-domain behaviour, mean ± SD across seeds.

**D3B does not resolve differences between the architectures.** The spread between
architecture means is 0.1532, against a mean within-architecture seed standard deviation
of 0.1093 ? a ratio of 1.40. All three pairwise ranges overlap, and the ordering takes
four distinct forms across five seeds. The probe supports the finding that every
architecture substantially under-recognises glioma under extreme covariate shift; it does
not support any claim about which architecture does so least. The most likely explanation
is cohort size: at 53 patients, a single patient is close to 2% of the cohort.

The predicted-class distribution shows that the non-glioma predictions are not uniform.
ResNet18 spreads its remaining predictions across no-tumour (0.261 ± 0.138), meningioma
(0.170 ± 0.035) and pituitary (0.167 ± 0.114); ViT-B/16 assigns a plurality to no-tumour
(0.430 ± 0.107) and almost nothing to pituitary (0.029 ± 0.033). The architectures do not
merely under-predict glioma ? they redistribute canine glioma images differently.

Confidence remained moderate under this shift (mean maximum confidence 0.71?0.78) with
correspondingly elevated entropy. The models did not collapse toward uniform uncertainty;
they continued to produce structured, moderately confident predictions, a substantial
share of which were not glioma.

Temperature scaling, applied using the temperature fitted on the D1 validation logits,
softened confidence on D3B without altering any prediction. Mean maximum confidence fell
for all three architectures (for example, ResNet18 from 0.7138 ± 0.0347 to
0.6670 ± 0.0330) and entropy rose correspondingly, while slice-level, patient-majority
and series-majority glioma rates were identical before and after scaling.

---

## 4.6 D3C ? same-species (human) shifted-domain evaluation

D3C is the same-species probe: 3,050 central slices from 610 human adult-glioblastoma
patients drawn from UPENN-GBM. Its purpose is to remove biological species as an
alternative explanation for shifted-domain instability, and it supplies a cohort more
than ten times larger than D3B.

The three architectures separated widely and consistently (Table 4.6). Slice-level glioma
prediction rates were 0.6744 ± 0.0727 for ResNet18, 0.5138 ± 0.0646 for EfficientNet-B0,
and 0.2635 ± 0.1139 for ViT-B/16. Three architectures that are not reliably
distinguishable on internal macro-F1 therefore range from recognising roughly two-thirds
of human glioma slices to about one quarter.

| Architecture | Slice glioma rate | Patient-majority | Mean confidence | Mean entropy | Median glioma prob. |
|---|---|---|---|---|---|
| ResNet18 | 0.6744 ± 0.0727 | 0.6882 ± 0.0760 | 0.7837 ± 0.0523 | 0.5418 ± 0.1262 | 0.6979 ± 0.1212 |
| EfficientNet-B0 | 0.5138 ± 0.0646 | 0.5207 ± 0.0761 | 0.8115 ± 0.0484 | 0.4859 ± 0.1243 | 0.4843 ± 0.1473 |
| ViT-B/16 | 0.2635 ± 0.1139 | 0.2607 ± 0.1225 | 0.8596 ± 0.0387 | 0.3528 ± 0.0947 | 0.1017 ± 0.1556 |

**Table 4.6.** D3C shifted-domain behaviour, mean ± SD across seeds.

Unlike D3B, this separation is stable. The between-architecture spread is 0.4109 against
a mean within-architecture seed standard deviation of 0.0837 ? a ratio of 4.91. Only one
of the three pairwise comparisons shows overlapping ranges, and ResNet18 ranks first at
every one of the five seeds.

**Misassigned human glioma slices go predominantly to the no-tumour class.** ResNet18
assigns 0.271 ± 0.066 of slices to no-tumour, EfficientNet-B0 0.416 ± 0.099, and ViT-B/16
0.628 ± 0.169. Meningioma and pituitary receive very little (0.007?0.077 and 0.032?0.057
respectively). Because all three architectures were evaluated on an identical set of
slices, the large between-architecture difference in no-tumour assignment cannot be
attributed to the slice-selection strategy; it reflects different learned behaviour under
shift. Human glioblastoma images being assigned to a no-tumour class is a more consequential
failure mode than the mixed non-glioma predictions observed on the canine probe.

**Confidence is inversely related to glioma recognition.** ViT-B/16, the architecture
least able to recognise human glioma (0.2635 ± 0.1139), is the most confident of the
three (mean maximum confidence 0.8596 ± 0.0387), has the lowest predictive entropy
(0.3528 ± 0.0947), and assigns a median glioma probability of only 0.1017 ± 0.1556.
ResNet18, which recognises glioma most often, is the least confident (0.7837 ± 0.0523)
with the highest entropy. This inversion holds at every seed.

This is the clearest reliability signal in the study. A model that is confidently wrong on
same-species out-of-distribution data is more hazardous than one that is uncertainly
wrong, because high confidence is precisely the cue a downstream reader would treat as
reassurance. It also demonstrates why prediction distribution and confidence must be
reported jointly: had only aggregate confidence been reported, the fact that the least
reliable architecture on D3C was also the most confident would have been invisible.

Temperature scaling reproduced the D3B pattern. Mean maximum confidence fell for all three
architectures and entropy rose, while glioma prediction rates were identical before and
after scaling. Softening ViT-B/16's confidence did not change the fact that it assigned
most human glioma slices to the no-tumour class.

A caveat applies to the no-tumour result. Slices were selected by anatomical position
rather than by verified tumour presence, so a fraction of no-tumour predictions may
correspond to slices with limited visible tumour. This does not affect the
between-architecture comparison, since all architectures were evaluated on identical
slices, but it does place a bound on the absolute interpretation of the no-tumour share.

---

## 4.7 Ranking stability across evaluations

Placing the three evaluations side by side makes the central result explicit
(Table 4.7).

| Evaluation | Between-arch. spread | Mean seed SD | Signal-to-noise | Distinct orderings (5 seeds) | Overlapping pairs |
|---|---|---|---|---|---|
| Internal macro-F1 | 0.0116 | 0.0046 | 2.52 | 2 | 2 of 3 |
| D3B glioma rate | 0.1532 | 0.1093 | 1.40 | 4 | 3 of 3 |
| D3C glioma rate | 0.4109 | 0.0837 | 4.91 | 2 | 1 of 3 |

**Table 4.7.** Architecture separation against seed-induced variation for each evaluation.

Three points follow.

First, **internal macro-F1 carries little architecture-ranking signal on this benchmark.**
At a signal-to-noise ratio of 2.52 with two of three pairwise ranges overlapping and two
distinct orderings across five seeds, the internal metric does not reliably distinguish
these architectures. The difference between the two best-performing models is 0.0011.

Second, **the same-species shifted-domain probe separates them consistently**, at nearly
twice the signal-to-noise ratio and with a single ordering dominant at four of five seeds
and the same architecture ranked first at all five.

Third, **the cross-species probe separates them least of all.** At 53 patients, D3B is
underpowered for ranking, and its four distinct orderings across five seeds should be read
as such rather than as evidence of genuine instability in relative architecture
performance.

It is worth stating plainly what this replaces. An earlier analysis of this project, drawn
from two different sets of trained checkpoints, reported that the architecture ordering
reversed between the canine and human probes. Under a single verified run set the ordering
is ResNet18 > EfficientNet-B0 > ViT-B/16 on the means of both probes. There is no
reversal, and the earlier finding is withdrawn.

---

## 4.8 Correlation between internal performance and shifted-domain behaviour

The relationship between internal macro-F1 and D3C glioma prediction rate depends on the
level at which it is measured (Table 4.8).

| Probe | Pooled across 15 runs | Between architecture means | Within architecture, centred |
|---|---|---|---|
| D3B | +0.756 | +0.956 | +0.664 |
| D3C | +0.474 | +0.886 | **?0.514** |

**Table 4.8.** Correlation between internal test macro-F1 and shifted-domain glioma
prediction rate at three levels of aggregation.

On D3C the association is strongly positive between architectures (+0.886) and negative
within them (?0.514). This sign reversal under within-group centring is a Simpson's
paradox: across architectures, better internal performance accompanies better
shifted-domain recognition, but within a single architecture the seeds that perform best
internally tend to perform *worse* on the human probe. Selecting a checkpoint by internal
validation score therefore does not merely fail to select for shifted-domain reliability
on this benchmark; within an architecture it selects mildly against it.

The effect is specific to D3C. On D3B both the between- and within-architecture
correlations are positive, with no sign change.

This result should be read with its limits in view. The between-architecture correlation
is computed over three points, and the within-architecture correlation over 15 runs
grouped into three architectures of five. It is an observation on this benchmark with
these architectures, not a general law, and it would be strengthened materially by
additional architectures.

---

## 4.9 Seed sensitivity: the seed-42 runs

One seed warrants separate reporting. At seed 42, ResNet18 and ViT-B/16 produced their
highest D3C glioma prediction rates by a wide margin ? 0.8013 and 0.4630 respectively,
against ranges of 0.6220?0.6613 and 0.1856?0.2502 at the other four seeds. Expressed in
standard deviations of each architecture's remaining seeds, these are z = +8.7 and
z = +9.3. EfficientNet-B0 shows no such effect: its seed-42 rate of 0.4577 falls inside
its own range across the other seeds.

The cause was investigated and not established. No quantity recorded about training on D1
distinguishes the seed-42 runs or predicts the D3C rate: per-class recall, predicted-class
shares, learned temperature, best epoch and total epochs trained are all non-significant
predictors across the 15 runs. The one concrete training-trajectory difference found is
that ViT-B/16 trained markedly longer at this seed (17 epochs, best epoch 12, against
10?12 epochs and best epoch 5?7 elsewhere), and this applies to one architecture only.
ResNet18 and ViT-B/16 track each other closely across seeds (r = +0.993 over all five
seeds; r = +0.842 with seed 42 removed), so seed 42 is better described as the extreme end
of a seed axis those two architectures share than as a discrete anomaly.

**This is reported as unexplained seed sensitivity rather than attributed to a mechanism
the data does not support.** Seed 42 was not excluded: excluding it would require a reason
established before its result was known, and there is none. It is itself evidence for the
argument of this study ? a single-seed shifted-domain result can land far from the others
for reasons invisible in every internal metric.

---

## 4.10 Summary of results

1. **Internal performance is high and does not reliably rank the architectures.** Test
   macro-F1 means span 0.9557?0.9673, but the between-architecture spread (0.0116) is only
   2.52 times the mean seed-induced standard deviation (0.0046), the two best models differ
   by 0.0011, and the ordering changes between seeds.

2. **All three architectures are mildly overconfident internally, and temperature scaling
   improves every calibration metric** without altering any prediction. The learned
   temperature varies more across seeds within an architecture than it does between
   architectures, and ViT-B/16 is consistently the worst calibrated.

3. **D2 was unsuitable as external validation**, with 4,740 of its 5,950 images
   byte-identical to D1. Rejecting it prevented a misleading generalisation claim.

4. **Both probes show substantial under-recognition of glioma under shift**, but only the
   same-species human probe separates the architectures reliably (signal-to-noise 4.91
   against 1.40 for the canine probe, which is underpowered for ranking at 53 patients).

5. **On D3C, misassigned human glioma slices go predominantly to no-tumour** ? from
   0.271 ± 0.066 for ResNet18 to 0.628 ± 0.169 for ViT-B/16 ? with meningioma and pituitary
   receiving very little.

6. **Confidence is inversely related to glioma recognition on D3C.** The architecture least
   able to recognise human glioma is the most confident and the least uncertain, at every
   seed.

7. **Temperature scaling softened confidence on both probes but changed no prediction**,
   confirming across two independent shifted domains that calibration and shift robustness
   are distinct problems.

8. **The association between internal performance and shifted-domain behaviour reverses
   sign under within-architecture centring on D3C** (+0.886 between, ?0.514 within), so
   internal validation score is not a proxy for shifted-domain reliability and, within an
   architecture, points mildly the wrong way.

# Chapter 5 ? Conclusion, Limitations, and Future Work

*Rewritten against run set `2026-08-sweep-a` (seeds 42?46 × 3 architectures,
15 runs).*

---

## 5.1 Conclusion

This study set out to test whether internally high-performing brain MRI tumour
classification models remain reliable when assessed under leakage-aware splitting,
overlap auditing, calibration analysis, and glioma-focused shifted-domain testing. The
framework was applied to three established architectures ? ResNet18, EfficientNet-B0,
and ViT-B/16 ? each trained at five random seeds on an identical leakage-aware split of
a widely used public four-class benchmark.

The central finding is negative, and it concerns the evaluation protocol rather than any
particular model. **On this benchmark, internal test macro-F1 does not carry a
reproducible architecture-ranking signal.** The spread between architecture means is
0.0116, against a mean within-architecture standard deviation across seeds of 0.0046.
The two best-performing architectures differ by 0.0011 ? roughly a quarter of one
standard deviation ? and their per-seed ranges overlap almost entirely. The ordering
changes between seeds. A single training run reported as internal macro-F1, which is the
design used almost universally in this literature, therefore measures seed variation as
much as it measures architecture.

The same three architectures are separated consistently by a same-species shifted-domain
probe. On the human glioblastoma collection, glioma prediction rates were 0.6744 ± 0.0727,
0.5138 ± 0.0646 and 0.2635 ± 0.1139 for ResNet18, EfficientNet-B0 and ViT-B/16
respectively ? a signal-to-noise ratio of 4.91 against 2.52 for internal macro-F1, with
one architecture ranked first at all five seeds. Models that internal evaluation cannot
distinguish behave very differently on out-of-distribution data of the same species, and
that difference is stable enough to be measured.

Two further results sharpen this. First, **misassigned human glioma slices go
predominantly to the no-tumour class**, from 0.271 ± 0.066 for ResNet18 to 0.628 ± 0.169
for ViT-B/16, with meningioma and pituitary receiving very little. Because all
architectures were evaluated on identical slices, this reflects learned behaviour rather
than slice selection. Second, **confidence is inversely related to glioma recognition on
the human probe**: ViT-B/16, least able to recognise human glioma, is the most confident
(mean maximum confidence 0.8596 ± 0.0387), the least uncertain (entropy 0.3528 ± 0.0947),
and assigns a median glioma probability of 0.1017 ± 0.1556. This inversion holds at every
seed. A model that is confidently wrong on same-species out-of-distribution data is more
hazardous than one that is uncertainly wrong, because confidence is the cue a downstream
reader treats as reassurance.

The relationship between internal performance and shifted-domain behaviour also depends
on the level at which it is measured. Across the fifteen runs, the correlation between
internal macro-F1 and human-probe glioma rate is +0.886 between architecture means but
?0.514 within architectures after centring. This sign reversal ? a Simpson's paradox ? means
that selecting a checkpoint by internal validation score does not merely fail to select
for shifted-domain reliability; within an architecture it selects mildly against it. The
effect is specific to the human probe; the canine probe shows no sign change.

Post-hoc temperature scaling improved every internal calibration metric for every
architecture without altering any prediction, and softened confidence on both probes while
leaving glioma prediction rates identical. This confirms, across two independent shifted
domains, that calibration and shift robustness are distinct problems: temperature scaling
adjusts the confidence attached to a prediction but cannot correct the prediction itself.

The rejection of D2 remains a methodological result in its own right. Of its 5,950 images,
4,740 were byte-identical to images in the internal dataset under SHA-256 hashing, with a
further 7,290 perceptual near-duplicate pairs. Two separately named public benchmarks
shared the majority of their images. Independence must be demonstrated empirically rather
than inferred from a dataset's name or packaging.

Taken together, these findings support a conservative conclusion. High internal accuracy
on this benchmark is not evidence of reliability, and ? more pointedly ? it is not even
evidence of relative merit between architectures, because at this level of performance the
internal metric cannot resolve them against seed noise. Defensible evaluation requires
leakage-aware splitting, overlap auditing, calibration assessment, repeated training runs
with dispersion reported, and carefully qualified shifted-domain testing, considered
jointly.

---

## 5.2 Correction to an earlier analysis

An earlier analysis of this project, presented in a previous draft, reported that the
architecture ordering reversed between the canine and human probes: ResNet18 weakest on
the canine collection but strongest on the human one, ViT-B/16 the reverse. That finding
is withdrawn.

The reversal was an artefact of comparing results from two different sets of trained
checkpoints. The earlier draft drew its internal, calibration and canine-probe numbers
from one run set and its human-probe numbers from another, trained separately. The two
were additionally evaluated on different human cohorts, of 569 and 610 patients. Under a
single verified run set the ordering is ResNet18 > EfficientNet-B0 > ViT-B/16 on the means
of both probes, and ResNet18 ranks first on the human probe at all five seeds.

Three further claims in that draft were single-seed artefacts and are also withdrawn: the
canine-probe predicted-class distributions, the apparent per-architecture differences in
learned temperature, and the finding that ViT-B/16 showed the largest calibration
improvement. Across seeds the three architectures' mean temperatures are nearly identical
(1.226, 1.226, 1.234) while a single architecture varies more than that between seeds, and
ViT-B/16 is consistently the worst-calibrated model rather than the most improved.

The defect was structural. Experiment artefacts were not version-controlled, so no
mechanism bound a reported value to the checkpoint that produced it, and regenerating one
stage overwrote its outputs while leaving downstream tables unmarked. This has been
corrected: artefacts are now version-controlled, each run records its git commit, seed,
data-split hash and checkpoint hash, and summary generation refuses to proceed unless all
runs share a single run identifier, an identical split hash, matching seed sets, and
identical evaluation cohorts. Both earlier run sets are preserved as the historical record.

This correction is reported here rather than absorbed silently, because the earlier claim
appeared in submitted work and because the episode illustrates the study's own argument:
results assembled without provenance discipline can support a conclusion that the
underlying data does not.

---

## 5.3 Strengths

**Leakage-aware internal preparation.** The benchmark was not used as distributed.
Exact-duplicate auditing removed 187 images, and perceptual hashing detected 5,125
near-duplicate pairs, of which 1,926 crossed the distributed train/test boundary. Whole
near-duplicate groups were assigned to single partitions, and the resulting split was
verified free of cross-partition near-duplicates.

**Empirical auditing of dataset independence.** The rejection of D2 prevented an inflated
external-validation claim and is reportable in its own right. Both retained probes passed
the same audit.

**Repeated training runs with dispersion.** Five seeds per architecture is what makes the
central claim possible. With one run per architecture the internal differences reported
here would have appeared to be architecture effects; they are not. This also makes the
study's own conclusions falsifiable in a way single-run studies are not.

**A measured rather than assumed preprocessing control.** The skull-stripping confound
recorded earlier against the human probe was tested and withdrawn: across 40 sampled
series measured against 40 matched internal images, the human probe retains extracranial
anatomy throughout and is on these measures less masked than the internal dataset. The
same measurements taken from source DICOM matched the converted images, ruling out the
conversion as a cause.

**Two probes differing along one deliberate axis.** The cross-species probe establishes
behaviour under extreme covariate shift; the same-species probe removes species as an
alternative explanation and supplies a cohort more than ten times larger. Reporting both,
including the finding that the smaller probe cannot resolve architectures, is more
informative than reporting either alone.

**Multi-metric calibration analysis.** Expected calibration error, negative
log-likelihood, Brier score and the confidence?accuracy gap were reported jointly, before
and after temperature scaling, on the internal test set and both probes. The consistency
of improvement across all four metrics is what makes the internal calibration result
robust to any single metric's binning sensitivity.

**Reproducibility as a design requirement.** All tables and figures are generated
programmatically from saved artefacts. Each run is bound to a git commit, a seed, a
data-split hash and a checkpoint hash, and summary generation is gated on provenance
consistency.

**Explicit refusal to over-claim.** Shifted-domain results are reported as prediction and
confidence behaviour, not diagnostic accuracy. The seed-42 runs are reported as
unexplained rather than attributed to a mechanism the data does not support, and are not
excluded.

---

## 5.4 Limitations

**Three architectures.** ResNet18, EfficientNet-B0 and ViT-B/16 span three distinct
inductive biases, but three points is a thin basis for the correlation decomposition in
particular, where the between-architecture term is computed over three means. The
Simpson's paradox result should be read as an observation on this benchmark rather than an
established general effect.

**Five seeds.** Five is sufficient to show that the between-architecture differences in
internal macro-F1 are of the same order as seed variation, but it is a small sample for
estimating that variation precisely. Comparable studies in medical imaging have used
substantially more.

**Glioma prediction rate is a behavioural proxy, not accuracy.** Neither probe reproduces
the four-class label structure, so conventional accuracy is undefined on both. A lower
glioma prediction rate indicates that fewer glioma-domain slices were assigned to the
glioma class; it does not directly establish that a model is less capable of recognising
glioma, as opposed to differently disposed toward the no-tumour decision region.

**Central slices, not lesion-verified slices.** Slices were selected by anatomical
position rather than confirmed tumour presence, so not every slice is guaranteed to
contain conspicuous tumour. This places a bound on the absolute interpretation of the
no-tumour share, though not on the between-architecture comparison, since all
architectures saw identical slices.

**Two-dimensional slices, not volumes.** Central-slice conversion made the DICOM sources
compatible with the 2D pipeline but does not capture the three-dimensional structure of
the volumes.

**The canine probe is underpowered for ranking.** At 53 patients its signal-to-noise
ratio is 1.40 with all pairwise ranges overlapping. Its four distinct orderings across
five seeds should be read as insufficient resolution rather than as genuine instability.

**Image-level rather than patient-level leakage control.** The internal dataset is
distributed without patient identifiers, so leakage was controlled at the level of images
and near-duplicate groups. This is cleaner than the distributed split but is not equivalent
to a patient-disjoint split, and internal performance is accordingly not evidence of
patient-level generalisation.

**Residual preprocessing differences.** Although skull stripping was ruled out, the human
probe is co-registered, resampled and intensity-normalised by CaPTk while the internal
dataset is not. This is a genuine domain difference that is not separately controlled.

**Per-seed rather than pooled statistical modelling.** The mixed-effects analysis is
fitted separately at each seed, which treats seed as a fixed stratum and is why the
reported odds ratios span a wide range. A model pooling all fifteen runs with seed as a
random effect would give a single architecture contrast with a proper variance component.

**One post-hoc calibration method.** Temperature scaling was the only method tested;
others may behave differently, particularly under shift.

**No uncertainty-aware methods.** Monte Carlo dropout, deep ensembles, Bayesian networks
and evidential learning were not implemented, so the study is limited to calibration and
confidence-distribution analysis.

**An unexplained seed effect.** The seed-42 behaviour on the human probe affects two of
three architectures and is not predicted by any recorded internal quantity. It is
reported rather than resolved.

---

## 5.5 Future work

**Pool the statistical model across seeds.** Fitting a single mixed-effects model over all
fifteen runs, with crossed random effects for patient and seed, would give one
architecture contrast with an explicit variance component for seed. This is the most
direct improvement available and requires no additional training.

**Add architectures.** ConvNeXt-T and Swin-T are the natural additions: they extend the
inductive-bias coverage, strengthen the correlation decomposition where three points is
currently the binding constraint, and would allow the ranking-stability result to be
tested against a wider set of models.

**Increase the seed count.** Ten seeds would tighten the variance estimates that the
central claim depends on, at modest computational cost for the two convolutional models.

**Select slices by tumour burden.** The human collection is distributed with
expert-reviewed tumour segmentations. Selecting the slice of maximum tumour
cross-sectional area per patient, or reporting glioma prediction rate as a function of
tumour area, would remove the principal caveat attached to the no-tumour finding and
convert the study's most striking result into its most defensible one.

**Test whether a source-class confound contributes.** The internal dataset draws its three
tumour classes from one upstream lineage and its no-tumour class from another. If part of
what the models learned is upstream source rather than pathology, that would help explain
why misassigned probe slices concentrate in the no-tumour class. This is testable without
retraining, by classifying source within the internal dataset, comparing low-level image
statistics across classes, and inspecting attribution maps on misassigned probe slices.

**Obtain an independent four-class external dataset.** A genuinely independent collection
reproducing the four internal classes, and passing the same overlap audit, would permit
conventional external accuracy and calibration to be reported alongside the existing
shifted-domain analysis.

**Evaluate uncertainty-aware methods under the same protocol.** A deep ensemble is
comparatively inexpensive here, since fifteen trained models already exist. These methods
should be tested on both probes to determine whether they flag unreliable shifted-domain
predictions more effectively than temperature scaling alone.

**Extend the contamination audit across the benchmark family.** The audit pipeline is
already built and requires no GPU. Applying it pairwise across the most widely used public
brain MRI classification datasets would produce a contamination matrix of direct practical
use to anyone selecting an external validation set in this field.

# Chapter 2 additions ? new §2.6 and rewritten §2.8

*The existing §2.6 (Uncertainty-Aware Medical Image Classification) becomes §2.7, and the
existing §2.7 (Reporting Standards) becomes §2.8. The Research Gap becomes §2.9.*

---

## 2.6 Training Variance, Underspecification, and the Reproducibility of Model Rankings

The reliability dimensions considered so far ? leakage, contamination, calibration, and
dataset shift ? all concern whether a reported performance figure is measuring what it
appears to measure. A further question precedes them: whether the figure is stable enough
to support the comparison it is used for. Almost all brain MRI tumour classification
studies train each architecture once and report the resulting metric as a property of that
architecture. Whether that is defensible depends on how much of the reported difference is
attributable to the architecture and how much to the random elements of training.

### 2.6.1 Seeds as a source of variance

Deep network training is stochastic in several respects: weight initialisation, the
ordering of training examples, data augmentation sampling, and non-deterministic GPU
operations. A random seed fixes all of these, and changing it produces a different trained
model from identical data and identical hyperparameters. The magnitude of the resulting
variation determines whether a difference between two reported figures can be attributed
to the methods that produced them.

Outside medicine, the canonical demonstration trained CIFAR-10 classifiers across a very
large number of seeds and found a spread in accuracy wide enough that a seed could be
selected to support a favourable comparison, concluding that reporting a single run
conceals a meaningful component of the reported result (Picard, 2021). Within medical
imaging, a taxonomy of variance sources distinguishes those arising from data, from
implementation, and from training stochasticity, and argues that reproducibility claims
must specify which are controlled (Renard et al., 2020).

The most directly relevant evidence comes from studies that repeat training many times on
medical data. Training nnU-Net at fifty seeds across three three-dimensional segmentation
tasks, including brain tumour, Åkesson et al. (2024) found that the best-performing seed
of an algorithm statistically significantly outperformed between none and roughly
three-quarters of the remaining seeds *of the same algorithm* under hold-out validation.
Their conclusion is unambiguous: a statistically significant difference in performance is a
weak and unreliable indicator of a true difference between two learning algorithms. A
parallel study of diagnostic tasks found retraining variance to be significant relative to
variance arising from the data itself, and reported that a substantial minority of
comparisons between identical methods produced spuriously significant p-values (Bosma et
al., 2023). Earlier work on chest radiograph classification at fifty seeds found
substantial variability in individual predictions that was not fully reflected in
variability of the aggregate test AUC (Zech et al., 2019) ? that is, the reported metric
was more stable than the model behaviour underlying it, which is precisely the condition
under which a single-run comparison appears trustworthy while remaining uninformative.

### 2.6.2 Underspecification

These observations are formalised in the concept of underspecification: a training
pipeline is underspecified when many distinct predictors achieve equivalent held-out
performance while encoding different inductive biases, so that the held-out metric does not
determine which predictor is obtained. Under this account, seed variation is not noise
around a single true model but a selection among genuinely different solutions that the
in-distribution objective cannot distinguish. The consequence is that differences invisible
in-distribution can become large under distribution shift, and recent work in medical
imaging adopts underspecification explicitly as the reason models with similar validation
performance exhibit divergent real-world failure modes (Stammel et al., 2026).

The evidentiary consequence has begun to be quantified. Work presented in 2025 extends
established models of false-claim probability by introducing a term for seed-induced
variance, and shows by simulation that this variance raises the threshold of evidence
required before an outperformance claim is justified. The implication for a literature in
which near-saturated single-run accuracies are routinely compared across architectures is
that many reported orderings may not be reproducible.

### 2.6.3 Ranking stability under shift

If in-distribution metrics cannot reliably order models, the question becomes whether any
evaluation can. Two lines of evidence bear on this.

The first holds that in-distribution and out-of-distribution performance are strongly and
positively correlated across a wide range of models and shifts, such that in-distribution
accuracy is a usable proxy for out-of-distribution accuracy (Miller et al., 2021). The
second qualifies it: inverse correlations between in-distribution and out-of-distribution
performance do occur on real-world data, arise even in a minimal linear setting, and have
been systematically under-reported because model selection procedures are themselves biased
toward in-distribution performance (Teney et al., 2022). Their conclusion ? that studies
using in-distribution performance for model selection will necessarily miss the
best-performing models under shift ? bears directly on the standard practice of selecting a
checkpoint by validation score.

Empirical benchmarking has begun to report ranking instability directly. A recent
evaluation of ten segmentation models on a small dataset found that rankings changed
substantially between in-distribution and out-of-distribution settings, that bootstrap
confidence intervals among top models overlapped substantially, and that differences were
driven more by statistical noise than by algorithmic superiority (Konrad et al., 2025).
Studies of architectural robustness under temporal shift report a related mechanism:
architectures whose inductive biases favour localised, highly discriminative features
achieve the highest in-distribution accuracy, yet those features are the ones most likely
to change across domains, so the same architectures degrade fastest (Holzinger et al.,
2026).

### 2.6.4 Position of the present study

Two features of this literature define the space this study occupies. First, the
repeated-seed evidence in medical imaging is concentrated in segmentation (Åkesson et al.,
2024; Renard et al., 2020; Konrad et al., 2025), with classification represented by
diagnostic tasks on non-MRI modalities (Bosma et al., 2023; Zech et al., 2019). No
repeated-seed analysis has been reported on the four-class brain MRI tumour benchmark that
carries the largest published literature in this area. Second, existing work on ranking
stability under shift reports that rankings *change* between settings; it does not ask
whether a shifted-domain evaluation might resolve architectures that the in-distribution
metric cannot. That is a different question, and it is the one this study asks.

---

## 2.9 Research Gap

*(Replaces the existing §2.8 in full.)*

The literature reviewed above establishes five points that together define the gap
addressed by this study.

First, deep learning achieves very high internal accuracy on public brain MRI tumour
benchmarks, and those results are reported almost exclusively as single-dataset,
single-run metrics with little attention to leakage, calibration, or external behaviour
(Section 2.2).

Second, data leakage and benchmark contamination are demonstrably capable of inflating
apparent performance by tens of percentage points, and this benchmark family is
specifically affected: near-duplicate images cross the distributed partition boundary, and
high classification accuracy has been shown to be achievable on it using no information
about the tumour at all (Section 2.3).

Third, modern networks are systematically overconfident, and although temperature scaling
improves calibration it cannot by construction correct class predictions, with its benefits
degrading under shift (Section 2.4).

Fourth, internal performance routinely fails to survive a change of imaging source, with
the great majority of externally validated radiological models showing performance drops
(Section 2.5).

Fifth ? and this is the point that reframes the others ? the internal metric used to
compare architectures is itself unstable across training runs. Repeated-seed studies in
medical imaging find that the same algorithm at different seeds can produce differences
large enough to be declared statistically significant, so that a single-run comparison
between two architectures may report a difference that would not survive repetition
(Section 2.6).

The decisive observation is not that any one of these dimensions is unstudied. Each has its
own substantial literature. It is that they are almost never assessed together, on the same
models and datasets, within a single reproducible evaluation ? and that the fifth is
routinely omitted even from studies that address the others. A study may audit leakage and
report calibration while still comparing architectures on the basis of one training run
each, in which case its architecture-level conclusions rest on a foundation that the
reproducibility literature has shown to be unreliable.

This study addresses that gap by integrating the five dimensions into one reliability-first
framework applied to a common set of established architectures. It pairs leakage-aware
preparation of a four-class internal dataset with exact and perceptual overlap auditing of
candidate external datasets; joins internal classification metrics with a multi-metric
calibration analysis and post-hoc temperature scaling; adds a carefully qualified
glioma-focused shifted-domain evaluation of prediction and confidence behaviour; and ? the
element that distinguishes it from prior work on this benchmark ? repeats every
configuration across five random seeds, so that every reported difference can be read
against the variation induced by training stochasticity alone.

Doing so permits a question that single-run studies cannot pose: not merely whether
internal accuracy predicts behaviour under shift, but whether internal accuracy is
reproducible enough to rank the architectures it is used to rank, and whether a
shifted-domain evaluation is more discriminative than the internal metric rather than
merely different from it. The contribution is therefore not a new architecture or a higher
accuracy figure, but the integration and the repetition: by combining within one
reproducible pipeline the checks that the literature reports only in isolation, and by
reporting every result with the dispersion that makes it interpretable, the framework
provides a more conservative and defensible assessment of brain MRI tumour classifier
reliability than internal accuracy alone. The methodology implementing this framework is
described in Chapter 3.

---

## Notes

**Placement.** §2.6 sits after dataset shift (§2.5) and before uncertainty (§2.7) because
it depends on the shift material ? §2.6.3 cannot be read without §2.5 ? and because
uncertainty estimation reads naturally as the last of the modelling topics before reporting
standards.

**Citations used.** Picard (2021), Renard et al. (2020), Åkesson et al. (2024), Bosma et
al. (2023), Zech et al. (2019), Miller et al. (2021), Teney et al. (2022), plus Konrad et
al. (2025), Holzinger et al. (2026), Stammel et al. (2026) and arXiv:2511.02453. The first
seven are in `CANONICAL_REFERENCES_45.md` §6 and verified. **The last four are not yet in
the canonical list and must be added and verified before submission** ? Konrad, Holzinger
and Stammel are recent and were located via Consensus; arXiv:2511.02453 needs its full
citation resolved.

**Table 2.2 update.** With §2.6 present, the reliability-dimensions table in §2.2.2 should
gain a sixth column: *repeated runs reported*. On present evidence the answer is "no" for
every study in it, which makes the argument visible at a glance and costs one column.

**§2.8 numbering.** The existing Reporting Standards section becomes §2.8 and needs no
change of content, though it could note that reporting checklists do not currently require
repeated runs ? a small point that connects it to §2.6.

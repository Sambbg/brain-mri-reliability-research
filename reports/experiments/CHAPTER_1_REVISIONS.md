# Chapter 1 ? revised sections

*Replacement text for §1.1, §1.2, §1.4, §1.5, §1.6 and §1.7. Section 1.3 (Research Aim)
is revised in one sentence.*

---

## 1.1 Project Background

*(Replace the final paragraph of the existing §1.1. The first two paragraphs stand.)*

Deep learning models often report high internal performance on public benchmark datasets.
Metrics such as accuracy, balanced accuracy, precision, recall, and macro-F1 are
frequently used to demonstrate model performance and, in comparative studies, to rank one
architecture against another. However, high internal performance alone does not
necessarily prove that a model is reliable, and a difference in internal performance
between two architectures does not necessarily establish that one is better than the
other. A model may perform well on an internal test set but behave unpredictably when
applied to images from a different dataset, imaging source, or acquisition environment.
Equally, a model trained twice on identical data with different random initialisations may
produce internal metrics that differ by as much as the reported gap between two distinct
architectures, in which case the comparison between them is not interpretable.

Reliability in medical imaging AI therefore requires evaluation beyond a single internal
classification metric. Important reliability dimensions include leakage-aware dataset
splitting, duplicate and near-duplicate image checking, public dataset overlap auditing,
calibration analysis, shifted-domain evaluation, and the reproducibility of reported
results across repeated training runs. These additional checks matter because internal
performance can be affected by data contamination, repeated images, dataset overlap, model
overconfidence, or the stochastic elements of training itself.

This project evaluates whether high-performing classifiers remain reliable when assessed
using leakage-aware preparation, calibration analysis, dataset overlap auditing,
glioma-focused shifted-domain testing, and repeated training across multiple random seeds.

---

## 1.2 Problem Statement

*(Insert as a new third paragraph, after the paragraph on inflated internal metrics and
before the paragraph on model confidence.)*

A further problem concerns the stability of the reported metric itself. Deep network
training is stochastic: weight initialisation, the ordering of training examples, and
augmentation sampling all vary with the random seed, so training the same architecture
twice on identical data yields two different models. Where studies report a single
training run per architecture, as is standard in this literature, any difference between
the reported figures conflates a difference between architectures with a difference
between random draws. Published repeated-run studies in medical imaging have found that
the same algorithm at different seeds can produce differences large enough to be declared
statistically significant, which implies that architecture rankings drawn from single runs
may not be reproducible (Åkesson et al., 2024; Bosma et al., 2023).

---

## 1.3 Research Aim

*(One-sentence revision to the existing text.)*

The aim of this research is to evaluate whether high-performing brain MRI tumour
classification models remain reliable, and whether their reported internal performance is
reproducible enough to support the architecture comparisons it is used for, when assessed
using leakage-aware dataset preparation, calibration analysis, dataset overlap auditing,
glioma-focused shifted-domain testing, and repeated training across multiple random seeds.

---

## 1.4 Research Questions

1. How do ResNet18, EfficientNet-B0, and ViT-B/16 perform internally on a leakage-aware
   four-class brain MRI tumour classification dataset, how reproducible is that
   performance across repeated training runs, and how well calibrated are their confidence
   estimates?

2. To what extent do candidate external brain MRI datasets overlap with the internal
   dataset, and can they be considered independent enough to support reliable external
   evaluation?

3. How do internally high-performing brain MRI tumour classification models behave under
   glioma-focused shifted-domain conditions, across repeated training runs, in terms of
   prediction distribution, glioma prediction rate, confidence, and entropy?

4. Does internal classification performance predict shifted-domain behaviour, and is
   either evaluation able to distinguish the architectures reliably against the variation
   induced by training stochasticity alone?

---

## 1.5 Research Objectives

1. To evaluate the internal classification performance, its reproducibility across
   repeated training runs, and the confidence calibration of ResNet18, EfficientNet-B0,
   and ViT-B/16 on a leakage-aware four-class brain MRI tumour dataset.

2. To assess the independence of candidate external brain MRI datasets by identifying
   exact and perceptual overlap with the internal dataset.

3. To evaluate the shifted-domain behaviour of internally high-performing brain MRI
   tumour classification models under glioma-focused conditions, across repeated training
   runs, using prediction distribution, prediction rate, confidence, and entropy analysis.

4. To compare the ability of internal and shifted-domain evaluation to distinguish the
   three architectures against seed-induced variation, and to characterise the
   relationship between internal performance and shifted-domain behaviour.

---

## 1.6 Scope of Study

*(Replace the second and third paragraphs. The first, fourth and fifth paragraphs stand.)*

The study includes four-class internal brain MRI tumour classification using a
leakage-aware dataset split consisting of glioma, meningioma, pituitary tumour, and
no-tumour classes. Three established deep learning architectures are evaluated: ResNet18,
EfficientNet-B0, and ViT-B/16. Each architecture is trained five times, once at each of
five random seeds, on an identical data split and under an identical training procedure,
giving fifteen training runs in total. All reported quantities are means with standard
deviations across those runs rather than single-run point estimates. The internal
evaluation is limited to classification performance metrics and calibration-related
metrics; no cross-validation or hyperparameter search is performed.

The study also includes dataset independence assessment through exact and perceptual
overlap auditing of candidate external datasets against the internal dataset.
Shifted-domain evaluation is limited to two independent glioma-focused datasets, selected
to differ along a single deliberate axis, biological species: a cross-species canine
glioma collection and a same-species human glioblastoma collection. Both are
glioma-focused and neither reproduces the four-class label structure of the internal
dataset, so they are used to analyse model prediction behaviour and confidence
characteristics under domain shift rather than to estimate four-class external diagnostic
accuracy. The same-species probe is included specifically to test whether shifted-domain
behaviour observed on the cross-species source persists when biological species is held
constant, and it supplies a substantially larger cohort against which the stability of that
behaviour across seeds can be assessed.

---

## 1.7 Significance of Study

The significance of this study lies in its reliability-first evaluation framework. The
published literature on brain MRI tumour classification reports internal test accuracies
approaching saturation, and commonly compares architectures on that basis. This project
evaluates whether such internal performance remains meaningful when leakage, dataset
overlap, calibration, shifted-domain behaviour, and reproducibility across training runs
are also considered.

The first contribution is the use of repeated training runs. Each architecture is trained
at five random seeds rather than once, which permits a question that single-run studies
cannot pose: whether the internal metric used to rank these architectures is stable enough
to rank them. Where the difference between architecture means is of the same order as the
variation induced by the random seed, an internal comparison based on one run per
architecture is not interpretable, and reporting dispersion is what makes this visible.

The second contribution is the treatment of D2. D2 was initially considered as a candidate
external validation dataset, but exact and perceptual overlap auditing showed substantial
overlap with D1. Rejecting D2 as clean external validation is a useful methodological
result because it demonstrates that public datasets should not automatically be assumed
independent, and it prevents an inflated or misleading external-validation claim.

The third contribution is the use of two glioma-focused shifted-domain probes rather than
one. D3B, a cross-species canine glioma collection, provides evidence about how D1-trained
models behave when applied to a visually distinct glioma-domain source. D3C, a
same-species human adult-glioblastoma collection, complements it by removing biological
species as an alternative explanation for any instability observed: instability on a canine
collection alone could be dismissed as a species artefact, whereas the same behaviour on
human data acquired under different scanner and cohort conditions cannot. The human probe
also supplies a substantially larger cohort ? 610 patients and 3,050 slices, against 53
patients and 265 slices for the canine probe ? which proves consequential, since the
smaller probe is shown to lack the resolution to distinguish the architectures at all while
the larger one distinguishes them consistently. Because neither probe reproduces the
four-class structure of the internal dataset, both are treated as shifted-domain stress
tests of prediction and confidence behaviour rather than as conventional external
validation, avoiding any overstated generalisation claim.

The fourth contribution is the calibration analysis. Accuracy and macro-F1 describe
whether the predicted class is correct, but they do not show whether the model's confidence
is reliable. By including expected calibration error, negative log-likelihood, Brier score,
confidence?accuracy gap, and temperature scaling ? reported across seeds rather than from a
single run ? this study evaluates confidence quality in addition to classification
performance, and is able to distinguish properties of an architecture from properties of a
particular trained checkpoint.

---

## Notes

**New RQ4 and Objective 4.** The existing three research questions cover internal
performance, overlap, and shifted-domain behaviour, but none asks the comparative question
the revised study actually answers: whether either evaluation can distinguish the
architectures against seed noise. Without it, the central result of Chapter 4 answers no
stated research question.

**§1.7 restructured into four numbered contributions.** Repeated runs are placed first
because they are what distinguishes this study from prior work on this benchmark. The
probe paragraph is reworded so it no longer implies the two probes gave divergent
orderings, and it now states the finding that the small probe lacks resolution ? which
turns a null result into a reported contribution.

**Cohort figures corrected** in §1.7: 610 patients and 3,050 slices.

**Two citations added** to §1.2: Åkesson et al. (2024) and Bosma et al. (2023), both in
`CANONICAL_REFERENCES_45.md` §6 and both verified.

**Numbering.** If RQ4 and Objective 4 are adopted, check that Chapter 5 answers all four,
and that any table mapping objectives to chapters is updated.

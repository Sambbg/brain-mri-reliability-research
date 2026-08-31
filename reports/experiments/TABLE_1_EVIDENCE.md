# Table 1 — Evidence Record

Supporting evidence for every cell in Table 1 of the manuscript. Each entry was
determined from the full text of the cited paper, not from its abstract. Where a
cell reads "No", the sections searched are named.

This file exists because Table 1 makes claims about other researchers' methodology.
Those claims should be checkable.

**Criteria applied**

- *Calibration* — any confidence-quality metric: expected calibration error, Brier
  score, negative log-likelihood used as a calibration measure, reliability diagram,
  or temperature scaling. Training loss reported as an overfitting diagnostic does
  not count. ROC/AUC does not count, being discrimination rather than calibration.
- *Leakage or overlap audit* — hashing, near-duplicate detection, patient-level
  grouping, or an explicit statement about cross-partition contamination.
- *External or shifted-domain validation* — evaluation on data not used in training.
  Where the target set shares an upstream source with the training set, this is
  recorded but flagged.
- *Repeated training runs* — multiple random initialisations, or variance reported
  across training runs. **k-fold cross-validation does not qualify**: it resamples
  data, not initialisation. Bootstrap over test predictions does not qualify either,
  for the same reason.

---

## Shah et al. (2022), *IEEE Access* 10:65426

**Task and result.** Section V-B reports the fine-tuned EfficientNet-B0 achieving
98.87%. Two qualifications carried into the table: the task is **binary**
tumour/non-tumour rather than multi-class, and the figure is **validation** accuracy
on the 20% split, with only 60 further images held out for testing. AUC 0.988,
Figure 10.

**Split.** Section IV-A: 3,762 images, 3,060 subset, 1,500 per class, 80% (2,400)
training and 20% (600) validation, plus 60 test images. Custom. Source described as
a BraTS-derived subset via TCIA.

**Calibration — No.** Section IV-E defines precision, sensitivity, specificity,
accuracy and F1 (equations 8–12), plus confusion matrix and ROC/AUC. Cross-entropy
appears in Section III-D as the training objective, not as an evaluation metric. No
ECE, Brier, reliability diagram or temperature scaling in Sections III, IV or V.

**Leakage audit — No.** BraTS-derived data is volumetric per patient, so slice-level
splitting is a live risk, but no patient-level grouping is described in Sections IV-A
or IV-B. The only related statement concerns manual removal of images that might
mislead training — a quality filter, not a duplicate or overlap audit.

**External validation — No.** Section V-B compares six architectures on the same
split (Table 3); Table 4 compares accuracies reported in prior literature. The paper
states these are not directly comparable due to differing data preparation. No second
cohort is scored.

**Repeated runs — No.** Section III-D specifies 50 epochs per model, single run each.
Table 1 lists hyperparameters with no seed field. Sections IV-D, V-A and V-B searched.

---

## Zulfiqar et al. (2023), *Biomedical Signal Processing and Control* 84:104777

**Result.** Table 5: EfficientNetB2, test accuracy 98.86%, precision 98.65, recall
98.77, F1 98.71 averaged over three classes.

**Split.** Section 3.1: "the total dataset samples are split into the train and test
set into a ratio of 80:20". Custom; Figshare ships no canonical split. Augmentation
is correctly restricted to the training set (Section 3.2, Table 2).

**Calibration — No.** Section 4.4 enumerates the complete metric set: accuracy
(4.4.1), precision (4.4.2), sensitivity (4.4.3), specificity (4.4.4), F1 (4.4.5),
confusion matrix (4.4.6). Figure 10 shows accuracy and loss curves as fit
diagnostics. Sections 3, 4 and 5 searched.

**Leakage audit — No.** Section 4.1 states each file contains "class label, patient
ID, image data", so patient identity was available and unused. Section 3.1 shuffles
slices before splitting; for a 3,064-slice, 233-patient cohort this places slices from
one patient on both sides. No hashing, no near-duplicate check, no statement.

**External validation — Yes, flagged.** Section 5.4 reports cross-dataset validation
on a Kaggle collection, EfficientNetB2 reaching 91.35% (Table 9). Not independent:
Reyes and Sánchez (Section 3.1.2 of that paper) document more than 2,260 coinciding
images between that collection and Figshare. Zulfiqar et al. make no independence
claim or check, and merge the target set's train and test folders for scoring.

**Repeated runs — No.** Section 4.3 (Table 3) lists fixed epochs, batch size and
optimiser with no seed field. Sections 5, 5.1 and 5.2 searched. One training run per
variant; no seed sweep, no standard deviation, no confidence interval, no k-fold.

---

## Reyes and Sánchez (2024), *Heliyon* 10:e25468

**Result.** Table 5 (Figshare, transfer learning with fine-tuning): ResNet101 and
EfficientNetB3 both at 98.7%. Table 6 (Kaggle): EfficientNetB3 at 97.5%. Per-class
precision in Table 7; no macro-F1 reported.

**Split.** Section 3.1.1: 80% train, 10% validation, 10% test, random (Tables 1–2).
Custom for both datasets.

**Calibration — No.** Section 3.3.4 defines cross-entropy loss (equation 1), accuracy
(2), precision (3) and recall (4). Figures 6–8 plot training and validation accuracy
and loss as fit diagnostics. Sections 3.3, 4 and 5 searched.

**Overlap audit — Partly.** Section 3.1.2 states the Kaggle collection draws on other
sources, "where we found more than 2260 images of coincidence between the two
datasets", repeated in Section 5. This is the only explicit duplicate finding among
the five papers. Two limits: the detection method is not described, and there is no
patient-level splitting within Figshare — Section 3.1.1 says images "were randomly
organized in three sets" and patient identity is never used.

**External validation — No.** Each dataset is trained and tested within itself
(Tables 3–6); no model trained on one is scored on the other. Section 5.1
acknowledges that models trained on Figshare may not hold up on other MR sources.

**Repeated runs — Yes, partial.** Section 3.3.3: "The experiments were executed five
times with different random seeds and the results are reported in Sect. 4 for the
highest accuracy." Five initialisations per configuration, so this is genuine repeated
training, but only the maximum is reported, with no mean, standard deviation or
interval. Max-of-five reporting biases the headline figure upward relative to a single
run, so this is recorded as a qualified "Yes" rather than a clean one.

---

## Disci et al. (2025), *Cancers* 17:121

**Result, with a correction.** Table 2 gives Xception testing accuracy **0.9527**,
macro-F1 0.9491, weighted F1 0.9529. The paper's headline figure of 98.73% is **not a
test metric**: Table 2 gives it support = 7,023, which is train plus test.
Reconstruction confirms this is a sample-weighted average of training and testing
accuracy:

    (0.9952 × 5,712 + 0.9527 × 1,311) / 7,023 = 0.9873

dominated by the training set. The table reports 95.27%; the 98.73% figure is not
comparable with any other row.

**Split.** Section 2.1: 7,023 images "divided into 5,712 training images and 1,311
testing images" — the distributed split as published. The only paper among the five
that does not re-partition.

**Calibration — No.** Section 2.5 lists accuracy, precision, recall, F1, loss, and
macro and weighted averages. Test cross-entropy is tabulated (Xception 0.1214), which
is technically a proper scoring rule, but is interpreted only as an overfitting signal
and never as calibration. Sections 2.5, 3 and 4 searched.

**Leakage audit — No.** Sections 2.1–2.3 cover class counts, grayscale, threshold and
crop preprocessing, and brightness–contrast augmentation. No hashing, near-duplicate
detection or patient-level statement. Two observations relevant to this study's
argument: the source collection is itself a merger of three upstream datasets, and
Section 2.3 states the preprocessing and augmentation pipeline was applied to both the
training and testing sets.

**External validation — No, explicitly.** Section 4: "the lack of external validation
and cross-validation limits generalizability". A stated self-acknowledgement rather
than an inferred omission.

**Repeated runs — No.** Section 2.5: 5 epochs, batch size 20, single run per
architecture, no seed specified. The Section 4 statement above also rules out
cross-validation.

---

## Elhadidy et al. (2025), *Computers in Biology and Medicine* 188:109872

**Result.** Table 5, Section 3.2: EfficientNet "Accuracy of Testing 98.72%", Swin
98.08%, CNN 95.16%. Note that Section 3.3 gives a conflicting figure of 99.69% for
EfficientNet in a separate comparison, and Table 6 shows Swin Transformer with
pituitary precision, recall and F1 all 0.00 alongside a claimed 98.08% accuracy.
These internal inconsistencies are not resolved in the paper. The table reports the
Table 5 value.

**Split.** Section 3.2: "The dataset was split into training and testing sets using an
80-20 split." Custom. Section 2.3 states the 7,023 samples were "augmented to a total
of 9,749 samples", and Table 7 lists the proposed models as trained on 9,749 images,
which places augmentation before the split. Augmented copies of one source image may
therefore fall on both sides. The paper does not address this.

**Calibration — No.** Metrics are defined in Section 3.2, equations 2–4: accuracy,
sensitivity, specificity. Confusion matrices and an AUC-ROC curve appear in Figure 15,
which is discrimination rather than calibration. Table 5 reports a scalar loss (0.0303)
never analysed as a confidence-quality measure. Sections 2.4, 3.1, 3.2 and 3.3
searched.

**Leakage audit — No.** Section 2.1 gives class counts and MRI views; Sections 2.2–2.3
cover normalisation, resizing and augmentation. No hashing, near-duplicate detection or
patient-level grouping. The source collection is a merger of three upstream datasets —
the paper itself lists that provenance for another study in Table 7 — but performs no
overlap check.

**External validation — No.** Section 3.3 is titled "Results validation" but presents a
literature comparison table of published accuracies from other papers rather than
evaluation on held-out external data. No second cohort is scored.

**Repeated runs — No.** Section 3.1 reports 5-fold cross-validation ("randomly
partitioned into five equal folds"), which is data resampling rather than repeated
initialisation. A claim of "reduction in standard deviation of classification accuracy
across different training runs" appears in that subsection with no seeds named, no
standard deviation values and no intervals. Recorded as cross-validation only.

---

## Study omitted

**Vimala et al. (2023), *Scientific Reports* 13:23029** meets the inclusion criteria
and was omitted.

Its abstract and conclusion report test accuracy 99.06%, precision 98.73%, recall
99.13% and F1 98.79%, while its own Results section states EfficientNetB2 achieved F1
98.71% and test accuracy 98.86% — figures numerically identical to Zulfiqar et al.
(2023) on the same dataset and pipeline, with near-identical figure captions. Table 4's
class-wise row is inconsistent with both sets of figures.

The relationship between the two reports is unresolved. Listing both as independent
evidence points would misrepresent the number of independent observations supporting the
table's pattern, so the study is excluded and the exclusion noted in the caption without
speculating on its cause.

---

## Two patterns worth stating in the text

**The repeated-runs column is effectively empty.** Of five studies, exactly one ran
repeated initialisations, and it reports only the maximum of five — which inflates the
headline figure rather than characterising variance. None reports a mean with standard
deviation or an interval across training runs.

**"External validation" in this literature largely means Figshare evaluated against a
Kaggle collection partly built from Figshare.** Zulfiqar et al. claim cross-dataset
validation on that collection. Reyes and Sánchez independently document more than 2,260
coinciding images between it and Figshare. The study claiming external validation does
not check independence; the study that checks independence declines to run the
cross-dataset test.

That contrast is a documented instance of the problem this study addresses, rather than
an asserted one, and it belongs in Section 3.1 alongside the rejection of the candidate
external dataset.

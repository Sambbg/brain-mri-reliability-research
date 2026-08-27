# Post-Submission Tasks

Deferred from the thesis deadline. Ordered by return on effort for a journal version.

---

## 1. Audit the Nickparvar?BRISC2025 overlap against a specific published evaluation

**Highest-value item. Do this first.**

Kakon, S. C., Jamwal, H. D. S., & Singh, S. (2026). Improving Cross-Domain Generalization
in Brain MRIs via Feature Space Stability Regularization. *Mathematics, 14*(6), 1082.
https://doi.org/10.3390/math14061082

Their Data Availability statement names `masoudnickparvar/brain-tumor-mri-dataset` as the
training source and `briscdataset/brisc2025` as the external validation set ? D1 and D2 in
this project. They state that no BRISC-2025 samples were used in training, fine-tuning or
hyperparameter selection, which is true as written: they trained on Nickparvar. But our
audit found 4,740 of 5,950 BRISC2025 images byte-identical to D1 under SHA-256, with a
further 7,290 perceptual near-duplicate pairs.

They report a domain gap of 0.94% for DenseNet-121 on the external set.

**What must be established before this can be claimed:**

- They used **1,000 BRISC images** (250 per class), not the full set. Our audit covered
  5,950. Identify their subset and audit *those* images specifically.
- The number that matters: what fraction of their external test set appears in the
  Nickparvar training partition ? not in Nickparvar overall.
- Domain gaps across their architectures range 0.94% to 10.23%. Total contamination would
  drive all gaps to near zero, so this is partial. Quantify rather than assert.

**Secondary observations, already established from their text:**

- Their in-domain test set is the distributed Nickparvar test directory (1,311 images).
  Our audit found 1,926 near-duplicate pairs crossing that distributed boundary, so their
  internal accuracy is inflated independently of the BRISC question.
- Single seed throughout: "all the models used the same random seed (seed = 42)". Their
  bootstrap resamples test predictions, not training runs, so it captures sampling
  variability and not seed variability. Our five-seed result speaks directly to this.
- They describe BRISC-2025 as "acquired using standardized 3T imaging protocols." If BRISC
  is collated from pre-existing public datasets, that characterisation is incorrect, and it
  is the assumption that makes the external-validation design appear sound.

**Framing.** Factual, no adjectives. This is careful work ? ablations across three
perturbation components, ? sensitivity sweeps, calibration metrics, bootstrap CIs, a
mechanistic feature-stability analysis. That competent researchers fell into this is the
argument for auditing, not evidence of carelessness. Report the measurement and let the
reader draw the inference.

**Also check:** whether other published work uses the same Nickparvar ? BRISC pairing.
Three or four instances makes it a pattern rather than an anecdote.

---

## 2. Read the BRISC Scientific Data descriptor

BRISC Dataset and Collaborators (2026). BRISC 2025: Annotated Dataset for Brain Tumor
Image Segmentation and Classification. *Scientific Data, 13*, 361.

Now published ? the arXiv preprint citation (arXiv:2506.14318) is superseded and must be
updated wherever it appears.

If the descriptor documents derivation from Nickparvar, the overlap was disclosed by
BRISC's own authors, and the finding becomes "the information was public and went unused"
rather than "undocumented contamination." That is a different and more defensible claim.
Establish which before writing anything.

---

## 3. Pool the mixed-effects model across seeds

Currently fitted separately at each seed, which treats seed as a fixed stratum and is why
the reported odds ratios span 0.077 to 0.843. A model pooling all 15 runs with crossed
random effects for patient and seed gives one architecture contrast with a proper variance
component for seed.

No retraining required. Most direct statistical improvement available, and it directly
instantiates the underspecification argument the paper makes.

---

## 4. Add ConvNeXt-T and Swin-T

Three architectures is the binding constraint on the correlation decomposition ? the
between-architecture term is computed over three means. Two more would materially
strengthen the Simpson's paradox result, extend inductive-bias coverage, and Swin would
allow direct engagement with MTA-Swin.

---

## 5. Select D3C slices by tumour burden

UPENN-GBM ships expert-reviewed tumour segmentations. Selecting the slice of maximum
tumour cross-sectional area per patient, or reporting glioma prediction rate as a function
of tumour area, removes the principal caveat on the no-tumour finding and converts the
study's most striking result into its most defensible one.

---

## 6. Test the source-class confound hypothesis

D1 draws its three tumour classes from Figshare/SARTAJ and its no-tumour class from Br35H.
If part of what the models learned is upstream source rather than pathology, that would
explain why misassigned probe slices concentrate in no-tumour.

Testable without retraining:
- Train a binary source classifier on D1 (Figshare-derived vs Br35H-derived). Near-perfect
  accuracy means the shortcut is available.
- Compare intensity histograms, background fraction, field of view and image dimensions
  across the four D1 classes.
- Grad-CAM or attention rollout on misassigned D3C slices: lesion, or skull margin?

---

## 7. Label-shuffle control

Train one model on D1 with labels randomly permuted. Chance is 25% for four classes.
Anything materially above that indicates residual leakage.

This is the single most convincing pipeline-correctness check available and costs one
training run. Yagis et al. (2021) did exactly this: their randomly-labelled dataset reached
roughly 96% under slice-level splitting and the expected 50% under subject-level splitting.

---

## 8. Extend the contamination audit across the benchmark family

The audit pipeline is built and needs no GPU. Running it pairwise across the most widely
used public brain MRI classification datasets ? Figshare CE-MRI, SARTAJ, Br35H, Nickparvar,
BRISC2025 and the common Kaggle repackagings ? produces a contamination matrix of direct
practical use to anyone selecting an external validation set in this field.

Candidate for a standalone short data note, with item 1 as its concrete hook.

---

## 9. Verify remaining references

`CANONICAL_REFERENCES_45.md` tracks status. 14 verified, 17 canonical and spot-checkable,
14 outstanding.

Priority is the eight where a specific figure is quoted in text. Note the correction
already found: Yagis et al. report 30% (OASIS), 29% (ADNI), 48% (PPMI) and 55% (Versilia,
a fourth dataset) ? the proposal attributes the 29?55% range to three datasets.

Recommended: build the list in Zotero by DOI. Anything that fails to resolve is wrong or
fabricated, and the export becomes the single source of truth for every document.

---

## 10. Retire the placeholder citation system

`reference_list_placeholders.md`, `references_search_table.md` and
`citation_integrity_audit.py` serve the superseded manuscript draft. The audit checks
placeholders against placeholders and cannot detect a fabricated reference. Replace with a
check that resolves DOIs from the canonical APA list.

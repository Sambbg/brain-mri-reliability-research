# Citation Insertion Plan

## Purpose

This file maps verified references to exact manuscript locations and claims.

The goal is to prevent citation padding and ensure that every reference supports a specific statement.

## Citation Strategy

Citations will be inserted into the manuscript only where they support:

1. A background claim.
2. A methodological choice.
3. A known risk or limitation.
4. A result interpretation.
5. A future-work direction.

Do not insert citations only to increase the reference count.

---

# Section 1: Introduction

## Claim: Deep learning is widely used for MRI brain tumour analysis

### Manuscript location

Introduction, early background paragraph.

### Supporting references

- REF-BMRI-001
- REF-BMRI-002
- REF-BMRI-003

### Intended citation purpose

Support the general background that deep learning has become common in MRI brain tumour analysis, including classification, detection, and segmentation.

---

## Claim: Many studies emphasise internal performance on public datasets

### Manuscript location

Introduction, research gap paragraph.

### Supporting references

- REF-BMRI-001
- REF-BMRI-002
- REF-BMRI-003
- REF-BMRI-004

### Intended citation purpose

Support the motivation for evaluating reliability beyond internal accuracy.

### Warning

Do not overclaim that all prior studies are weak. Phrase this carefully as a common limitation in the literature.

---

## Claim: Leakage and duplicate data can inflate apparent model performance

### Manuscript location

Introduction, reliability problem paragraph.

### Supporting references

- REF-LEAK-001
- REF-LEAK-002
- REF-LEAK-003

### Intended citation purpose

Support the argument that leakage-aware splitting and overlap auditing are necessary.

---

## Claim: Calibration matters because high accuracy does not guarantee reliable confidence

### Manuscript location

Introduction, calibration paragraph.

### Supporting references

- REF-CAL-001
- REF-CAL-002

### Intended citation purpose

Support why calibration metrics are included alongside accuracy and macro-F1.

---

## Claim: External validation and dataset shift are central to medical imaging reliability

### Manuscript location

Introduction, final gap paragraph.

### Supporting references

- REF-SHIFT-001
- REF-SHIFT-002
- REF-SHIFT-003

### Intended citation purpose

Support the use of D3B as a domain-shift test rather than relying only on D1 internal testing.

---

# Section 2: Methods

## Claim: Dataset usage decisions were based on leakage-aware evidence

### Manuscript location

Methods, dataset section.

### Supporting references

- REF-LEAK-001
- REF-LEAK-003
- REF-LEAK-004

### Intended citation purpose

Support exact/pHash auditing and conservative rejection of D2.

---

## Claim: Temperature scaling is a post-hoc calibration method

### Manuscript location

Methods, calibration section.

### Supporting references

- REF-CAL-001

### Intended citation purpose

Support the use of validation logits to learn a single scalar temperature.

---

## Claim: ECE, NLL, and Brier score are suitable calibration/probabilistic metrics

### Manuscript location

Methods, evaluation metrics section.

### Supporting references

- REF-CAL-001
- REF-CAL-002
- REF-CAL-003

### Intended citation purpose

Support the selected calibration and probabilistic evaluation metrics.

---

## Claim: Reporting should be transparent and reproducible

### Manuscript location

Methods, reproducibility subsection or final methods paragraph.

### Supporting references

- REF-REPORT-001
- REF-REPORT-002

### Intended citation purpose

Support transparent reporting of dataset sources, model design, evaluation, and limitations.

---

# Section 3: Results

## Claim: D2 was rejected due to overlap

### Manuscript location

Results, dataset audit subsection.

### Supporting references

- REF-LEAK-001
- REF-LEAK-002
- REF-LEAK-003

### Intended citation purpose

References are not used to prove the result; they support why the result matters.

### Warning

The actual D2 overlap numbers must come from this project’s own artifacts, not from the literature.

---

## Claim: D3B performance shows internal accuracy does not guarantee shifted-domain reliability

### Manuscript location

Results, D3B section.

### Supporting references

- REF-SHIFT-001
- REF-SHIFT-002

### Intended citation purpose

References support interpretation, not the numerical result.

---

# Section 4: Discussion

## Claim: High internal performance should not be treated as clinical reliability

### Manuscript location

Discussion, main interpretation paragraph.

### Supporting references

- REF-SHIFT-001
- REF-SHIFT-002
- REF-REPORT-001
- REF-REPORT-002

### Intended citation purpose

Support cautious interpretation of internal performance and domain-shift findings.

---

## Claim: Calibration improves confidence quality but does not fix shifted-domain class behaviour

### Manuscript location

Discussion, calibration interpretation paragraph.

### Supporting references

- REF-CAL-001
- REF-SHIFT-001
- REF-SHIFT-002

### Intended citation purpose

Support the distinction between confidence calibration and external/domain-shift robustness.

---

## Claim: Future work should include uncertainty-aware methods

### Manuscript location

Discussion, future work paragraph.

### Supporting references

- REF-UNC-001
- REF-UNC-002
- REF-UNC-003
- REF-UNC-004
- REF-UNC-005

### Intended citation purpose

Support future work on MC dropout, deep ensembles, and medical imaging uncertainty estimation.

---

## Claim: Clinical translation would require prospective/clinical evaluation

### Manuscript location

Discussion, final limitations/future clinical translation paragraph.

### Supporting references

- REF-REPORT-001
- REF-REPORT-002
- REF-REPORT-003

### Intended citation purpose

Support the statement that this work is retrospective experimental evidence, not clinical deployment evidence.

---

# Citation Insertion Rules

Before inserting a reference into the manuscript:

1. Confirm the reference exists in `references_search_table.md`.
2. Confirm the manuscript claim is listed in this plan.
3. Insert the citation only once or twice where it is most useful.
4. Avoid dense citation clusters.
5. Do not cite arXiv/preprints when a stronger peer-reviewed review or guideline is available.
6. Do not cite uncertainty papers as if uncertainty experiments were already performed.
7. Do not cite clinical-trial reporting guidelines as if this study were a clinical trial.

---

# Immediate Next Step

Insert citation placeholders into `manuscript_draft_v1.md` using reference IDs first, not final formatted references.

Example placeholder format:

`[REF-CAL-001]`

Final citation style will be applied later after the target journal or thesis format is chosen.

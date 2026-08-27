# Chapter 3 ? edit sheet for the remaining sections

§3.6 is already rewritten in `SECTION_3_6_REWRITTEN.md`. This covers the other eight
sections. Each item gives the current text and its replacement.

All numbers reflect the re-run audit of August 2026 and run set `2026-08-sweep-a`.

---

## §3.1 Study Design Rationale

### 3.1-a ? Add repeated runs to the design description

**Current**, second paragraph: *"Three established architectures spanning distinct model
families ? were trained on the identical D1 leakage-aware split, using the same
preprocessing, the same optimisation protocol, and the same model-selection criterion?"*

**Insert after that sentence:**

> Each architecture was trained five times, once at each of five random seeds, so that
> fifteen runs in total contribute to every reported comparison. Repetition is part of the
> controlled design rather than an additional robustness check: holding the data, split and
> training procedure fixed isolates the effect of the learned representation only if the
> variation introduced by training stochasticity is also measured, since otherwise a
> difference attributed to architecture may reflect a difference between random draws.

### 3.1-b ? Correct the cohort figures

**Current:** *"569 patients and 2,845 slices, against 53 patients and 265 slices for the
canine probe"*

**Replace with:** *"610 patients and 3,050 slices, against 53 patients and 265 slices for
the canine probe"*

### 3.1-c ? Revise the near-parity sentence

**Current:** *"Where the three models achieved comparable internal performance (Chapter 4),
this near-parity functioned as a controlled baseline ? a set of models close to
interchangeable in-distribution ? against which their behaviour under dataset shift became
interpretable."*

**Replace with:**

> Where the three models achieved comparable internal performance (Chapter 4), the design
> permits a stronger statement than near-parity alone: because each architecture was
> trained at five seeds, the difference between architecture means can be read against the
> variation within each architecture, and the internal metric can be assessed for whether
> it distinguishes them at all. Divergence that emerges only under shift can then be read
> as a difference in representational robustness rather than as a difference in internal
> skill, in evaluation inputs, or in random initialisation.

---

## §3.2 Dataset and Roles

### 3.2-a ? Table 3.1, D3C row

**Current:** `569 patients / 569 series / 2,845 central slices`
**Replace with:** `610 patients / 610 series / 3,050 central slices`

### 3.2-b ? §3.2.4, D3C description

**Current:** *"the retained cohort of 569 patients and 569 series was converted to 2,845
central 2D slices"*

**Replace with:**

> 614 series were selected and converted to 3,070 central 2D slices, of which four series
> were subsequently excluded as non-axial (Section 3.3.2), giving an analysis cohort of 610
> patients, 610 series and 3,050 central slices.

### 3.2-c ? §3.2.4, add the preprocessing note

**Append to the end of §3.2.4:**

> D3C is distributed in a CaPTk-processed form. An earlier stage of this project recorded a
> concern that this implied skull stripping, and therefore a systematic preprocessing
> difference from the unstripped D1 images. That concern was tested directly and withdrawn
> (Section 3.3.2). Weaker preprocessing differences ? co-registration, resampling and
> intensity normalisation ? remain and are carried into the limitations.

---

## §3.3 Data Preparation and Preprocessing

### 3.3-a ? §3.3.2, record the non-axial exclusion

**Current:** *"For D3C (human, UPENN-GBM), 575 series were selected, of which 569 were
successfully retrieved and converted, giving 569 series from 569 patients (Table 3.3)."*

**Replace with:**

> For D3C (human, UPENN-GBM), series were selected and converted for 614 patients, giving
> 3,070 central slices. Each converted series was then checked for imaging plane using the
> DICOM ImageOrientationPatient direction cosines. Four series were more than 45 degrees
> from axial and were excluded as non-axial, leaving an analysis cohort of 610 patients, 610
> series and 3,050 central slices. A further eleven series lie between 10 and 45 degrees
> from axial; these were retained, flagged in the analysis manifest, and used for the plane
> sensitivity analysis reported in Section 4.6. The excluded slices are retained separately
> so that the exclusion can be audited or reversed.

### 3.3-b ? Table 3.3, D3C row

**Replace with:** `D3C | Human | 614 | 614 | 610 (after exclusion) | 3,050`

Add a footnote: *614 series were converted to 3,070 slices; four non-axial series (20
slices) were excluded, giving the 610-patient / 3,050-slice analysis cohort.*

### 3.3-c ? §3.3.2, add the skull-stripping audit

**Insert as a new paragraph after the slice-extraction description:**

> Because D3C is distributed in a CaPTk-processed form, the possibility that it had been
> skull-stripped ? and therefore differed systematically from the unstripped D1 images ?
> was tested rather than assumed. Forty D3C series were sampled at random and measured
> against forty matched D1 glioma images on four quantities: the proportion of the outer
> air region exactly zero, the proportion of non-zero image corners, the proportion of
> outer-ring pixels exceeding the brain-core median, and the presence of a masked
> background. No D3C image had a masked background. The air region was 26.2 per cent
> exactly zero at the median, where a background mask would give a value near 1.0; image
> corners were 54.0 per cent non-zero; and 25.6 per cent of outer-ring pixels exceeded the
> brain-core median, which is the expected signature of scalp fat on T1. The same
> measurements taken directly from the source DICOM matched the converted PNGs, ruling out
> the conversion step as a cause. On these measures D3C retains extracranial anatomy
> throughout and is in fact less masked than D1, whose air region is 37.3 per cent exactly
> zero at the median. The skull-stripping concern was therefore withdrawn, and no
> corresponding control is applied.

---

## §3.4 Dataset Independence and Contamination Auditing

### 3.4-a ? Table 3.4, D1 vs D3C row

**Current:** `D1 vs D3C | 19,951,985 | 0 | 7 | 0 | Retained`
**Replace with:** `D1 vs D3C | 21,529,910 | 0 | 7 | 0 | Retained`

Add a footnote: *The D1?D3C audit compares all 3,070 converted D3C slices against the
7,013 D1 images. The 3,050-slice analysis cohort is a subset, so the audit covers a
superset of the evaluated data.*

### 3.4-b ? §3.4.3, update the D3C paragraph

**Current:** *"For D3C, all 19,951,985 comparisons against D1 likewise returned no exact
duplicates; perceptual hashing flagged only seven near-duplicate pairs?"*

**Replace with:**

> For D3C, all 21,529,910 comparisons against D1 likewise returned no exact duplicates;
> perceptual hashing flagged only seven near-duplicate pairs, all of which fell within the
> glioma class rather than across classes and which were concentrated in two UPENN-GBM
> patients. Seven flagged pairs out of more than twenty-one million comparisons is a
> negligible rate and is consistent with coincidental anatomical similarity between central
> glioma slices rather than shared image provenance; the flagged pairs were reviewed and
> retained on this basis. The audit was performed over all 3,070 converted D3C slices,
> which is a superset of the 3,050-slice analysis cohort, so no evaluated slice is
> unaudited. A separate check confirmed that no perceptual hash value in D3C is shared
> between patients: all within-D3C hash collisions occur between adjacent central slices of
> the same series, as expected by construction.

---

## §3.5 Model Architectures

No changes required. Verify that the parameter counts in Table 3.5 match the values used
in Chapter 4.

---

## §3.7 Evaluation Protocol and Metrics

### 3.7-a ? §3.7.1, replace the wrong formula

**Critical.** The macro-F1 subsection currently displays the expected calibration error
formula, while the surrounding prose describes a formula that is not shown.

**Delete** the displayed ECE equation from §3.7.1 and **replace with:**

> macro-F1 = (1/C) ?_{c=1}^{C} F1_c

Verify that the ECE formula remains correctly placed in §3.7.2, where it belongs.

### 3.7-b ? §3.7 preamble, note aggregation across seeds

**Insert after the first paragraph:**

> Every metric defined below was computed independently for each of the fifteen runs. All
> values reported in Chapter 4 are means with standard deviations across the five seeds of
> an architecture, and no metric is reported from a single run. Where a metric depends on a
> fitted parameter ? the temperature of Section 3.7.3 ? that parameter is fitted separately
> within each run.

### 3.7-c ? §3.7.4, add the plane sensitivity metric

**Append to §3.7.4:**

> Because imaging plane is a plausible alternative explanation for shifted-domain
> prediction behaviour, all D3C behavioural metrics were additionally recomputed on a
> sensitivity cohort with the eleven oblique series excluded (Section 3.3.2), and the
> difference is reported alongside the full-cohort values.

---

## §3.8 Calibration and Temperature Scaling Method

### 3.8-a ? Correct the omission of D3C

**Current:** *"After fitting, the learned scalar temperature was applied to the D1 test
logits and the D3B shifted-domain logits."*

**Replace with:** *"After fitting, the learned scalar temperature was applied to the D1
test logits and to both the D3B and D3C shifted-domain logits."*

**Current:** *"This allowed the study to evaluate whether temperature scaling improved
internal calibration on D1 and whether it softened confidence under D3B shift."*

**Replace with:** *"This allowed the study to evaluate whether temperature scaling improved
internal calibration on D1 and whether it softened confidence under both D3B and D3C
shift."*

### 3.8-b ? Note that temperature is fitted per run

**Append to the paragraph describing the fitting procedure:**

> A temperature was fitted independently within each of the fifteen runs, on that run's own
> validation logits. This is necessary because the temperature is a property of a trained
> checkpoint rather than of an architecture: across seeds, the fitted temperature varies
> more within a single architecture than it does between architectures (Section 4.4).

---

## §3.9 Reproducibility, Data Availability, and Ethics

### 3.9-a ? §3.9.1, add artefact-level provenance

**Append after the paragraph on git commit recording:**

> Provenance was additionally recorded at the level of individual artefacts. Every run
> wrote a record containing its run-set identifier, architecture, seed, git commit, the
> SHA-256 hash of the data-split file, and the SHA-256 hash of the resulting checkpoint,
> binding each reported value to the exact code, partition and weights that produced it.
> Experiment artefacts are version-controlled alongside the code.
>
> Summary generation enforces these records. Before producing any aggregate, the
> consolidation step verifies that all contributing runs share a single run-set identifier,
> an identical split hash, matching seed sets across architectures, and identical
> evaluation cohorts, and refuses to produce a summary otherwise. This guard exists because
> an earlier stage of the project assembled reported values from more than one set of
> trained checkpoints; the episode and its correction are described in Section 5.2.

### 3.9-b ? §3.9.2, correct the D3C description

**Current:** *"D3C from the human UPENN-GBM collection"*

**Replace with:** *"D3C from the human UPENN-GBM collection, of which 614 series were
retrieved and 610 retained after the non-axial exclusion described in Section 3.3.2"*

---

## Application order

1. **§3.7-a** ? the wrong formula. A methods chapter displaying the wrong equation is the
   most damaging single item here.
2. **§3.8-a** ? the D3C omission. Currently states the study did something it did not.
3. **§3.3-a, §3.4-a, §3.4-b, §3.2-a, §3.2-b, §3.1-b** ? the cohort and audit numbers.
4. **§3.1-a, §3.7-b, §3.8-b, §3.9-a** ? repeated-run content.
5. **§3.3-c, §3.2-c, §3.7-c** ? the two audits.

Items 1 and 2 are factual errors. Items 3 to 5 bring the chapter into line with what was
done.

---

## Cross-check after applying

- Search the document for `569`, `2,845`, `2845`, `19,951,985` ? none should remain.
- Search for `trained once`, `single-run`, `single fixed seed` ? none should remain in
  Chapter 3.
- Confirm §3.7.1 and §3.7.2 display different formulas.
- Confirm every forward reference in Chapter 3 points at a section that still exists after
  the Chapter 2 renumbering.

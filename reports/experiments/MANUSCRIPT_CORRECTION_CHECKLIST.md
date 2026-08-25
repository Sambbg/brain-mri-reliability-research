# Manuscript Correction Checklist ? Chapters 1?3, front matter, figures

Every item below is a specific edit to the thesis document. Ordered by severity.
Tick as completed.

Source of truth for all numbers: `reports/experiments/consolidated/`.

---

## A. Factual errors ? must fix

### A1. Abstract
**Status:** rewritten in `ABSTRACT_REWRITTEN.md`. Replace wholesale.

The existing abstract contains four factual errors: macro-F1 stated as 0.9666?0.9680 for
all three architectures (ViT-B/16 is 0.9557); D3C described as 2,845 slices from 569
patients (it is 3,050 from 610); six single-seed glioma rates presented as results; and
the ordering reversal, which does not exist.

- [ ] Replace abstract with Version A

---

### A2. D3C cohort size ? appears in at least five places
The cohort was 569 patients / 2,845 slices under Run B. Under the sweep it is
**610 patients / 3,050 slices**. Every occurrence must change.

- [ ] §1.7 Significance ? "569 patients and 2,845 slices, against 53 patients and 265
      slices" ? "610 patients and 3,050 slices, against 53 patients and 265 slices"
- [ ] §3.1 Study Design Rationale ? same phrase, same correction
- [ ] §3.2.4 D3C description ? "retained cohort of 569 patients and 569 series was
      converted to 2,845 central 2D slices" ? 610 patients / 610 series / 3,050 slices
- [ ] Table 3.1, D3C row ? "569 patients / 569 series / 2,845 central slices" ? 610 / 610 / 3,050
- [ ] Table 3.3 (series selection) ? D3C row: series retained, patients, central slices
- [ ] Table 2.1, D3C row ? "569 patients / 569 series / 2,845 central slices"
- [ ] §3.4.1 / Table 3.4 ? the D1?D3C comparison count (19,951,985) was computed against
      the 569-patient cohort. **Recompute or state which cohort it refers to.**

> Note: check whether the overlap audit was re-run against the 610-patient cohort. If not,
> either re-run it or state explicitly that the audit was performed on the earlier cohort
> and that the additional patients were not audited. Do not leave this ambiguous.

---

### A3. §3.7.1 ? wrong formula printed
The macro-F1 section displays the **expected calibration error** formula:

```
ECE = ? (|B_m|/n) · |acc(B_m) ? conf(B_m)|
```

The surrounding text reads "the unweighted mean of the per-class F1 scores ... where C is
the number of classes and F1_c is the F1 score of class c" ? which describes a formula
that is not shown.

- [ ] Replace with: `macro-F1 = (1/C) ?_{c=1}^{C} F1_c`
- [ ] Verify the ECE formula in §3.7.2 is still present and correct (it is, and is
      duplicated here in error)

---

### A4. §3.8 ? omits D3C
Reads: "the learned scalar temperature was applied to the D1 test logits and the D3B
shifted-domain logits." Stale text predating D3C.

- [ ] "...applied to the D1 test logits and to the D3B and D3C shifted-domain logits"
- [ ] Same paragraph: "whether temperature scaling improved internal calibration on D1 and
      whether it softened confidence under D3B shift" ? "...under D3B and D3C shift"

---

### A5. Table 2.1 footnotes ? unresolved editorial notes in submitted text
Three footnotes contain instructions to yourself:

- Footnote c: "Exact public name to be confirmed against the project audit folder."
- Footnote d: "Source collection to be confirmed against the audit folder; the draft label
  'ICDC-Glioma' is incorrect and must be replaced throughout."
- Footnote e: "53 patients / 53 series, five central slices each" ? attached to the **D3C**
  row but describing **D3B**.

- [ ] Resolve footnote c: confirm the collection name against
      `reports/datasets/D3B_icdc_glioma_probe_result.md` and state it plainly
- [ ] Resolve footnote d: either confirm ICDC-Glioma is correct, or replace throughout.
      **This is cited in the references as Amin et al. (2020), DOI 10.7937/TCIA.SVQT-Q016 ?
      verify that DOI resolves to the collection you actually downloaded**
- [ ] Move footnote e to the D3B row, or correct it to 610 patients / 3,050 slices

---

### A6. Chapter 4 note-to-self left in text
Table 4.5c carries: "Consistency check: T should equal the value fitted on the D1
validation logits... The stored D3C artifact lists 1.2725 / 1.1598 / 1.3770; reconcile
before submission."

Table 4.6 carries: "The stored table_8 artifact lists internal macro-F1 as 0.9753 /
0.9680 / 0.9648... reconcile which metric the artifact used."

Both are resolved ? the discrepancy was Run A versus Run B ? and both tables are replaced
by the Chapter 4 rewrite.

- [ ] Confirm no "reconcile before submission" text survives anywhere in the document
- [ ] Search the document for "to be added", "to be confirmed", "TBD", "regenerated"

---

## B. Numbering and structure

### B1. Duplicate table number
Two different tables are both numbered **2.2**: the reliability-dimensions comparison in
§2.2.2, and the leakage-magnitude table in §2.3.1.

- [ ] Renumber the second to Table 2.3
- [ ] Update the two in-text references: §2.2.2 refers to "Table 2.2" for leakage
      magnitudes; §2.8 refers to "Table 2.1" where it means the reliability-dimensions table

### B2. Inconsistent figure numbering
Chapter 3 uses bare numbering (Figure 1?5); Chapter 4 uses chaptered (Figure 4.1, 4.8).

- [ ] Convert Chapter 3 to chaptered: Figure 3.1?3.5
- [ ] Update all in-text references

### B3. Chapter 2 numbered list is malformed
§2.1 introduces "five reliability dimensions" then lists items (i)?(vi), where item (i) is
the introductory sentence rather than a dimension.

- [ ] Remove the stray (i), leaving five items

### B4. Table 4.2b / 4.4b / 4.5b lettering
Sub-lettered tables are inconsistent with the rest of the numbering scheme.

- [ ] Renumber sequentially, or state the convention in the list of tables

---

## C. Language and presentation

### C1. First person inconsistent in Acknowledgements
Switches between "we were in contact", "our sincere appreciation", and "my main thesis
supervisor" within a single page.

- [ ] Use first person singular throughout

### C2. Markdown leaked into the document
§5.1 contains `**the ordering of the models reversed between the two probes**` with
literal asterisks. That passage is removed by the Chapter 5 rewrite, but check for others.

- [ ] Search for `**` and `##` in the body text

### C3. Equations rendering as corrupt characters
The PDF shows garbled output for several equations, e.g.
`??? = $ |?!| ? · |???(?!) ? ????(?!)|`. This is a font-embedding or symbol-encoding
failure.

- [ ] Rebuild every equation using the equation editor rather than pasted symbols
- [ ] Affects §3.7.1, §3.7.2 (ECE, NLL, Brier), §3.7.4 (predictive entropy)
- [ ] Export to PDF and check each equation visually

### C4. Missing spaces after line breaks
Several instances of words running together across line breaks: "highconfidence",
"macroF1", "notumour", "gliomafocused", "samespecies", "crossvalidation", "negativelog
likelihood".

- [ ] Search for these specific strings and repair

### C5. Abstract closing sentence has stray formatting
"...before	making	reliability	claims." ? tab characters instead of spaces.

- [ ] Fixed by the abstract replacement, but verify

---

## D. Content updates flowing from the sweep

### D1. §1.4 / §1.5 ? research questions and objectives
RQ1 asks how the three architectures "perform internally ... and how well calibrated are
their confidence estimates." The sweep adds a dimension this doesn't capture:
reproducibility of that performance.

- [ ] Consider revising RQ1 to: "How do ResNet18, EfficientNet-B0 and ViT-B/16 perform
      internally on a leakage-aware four-class brain MRI dataset, how reproducible is that
      performance across training seeds, and how well calibrated are their confidence
      estimates?"
- [ ] Mirror in Objective 1
- [ ] RQ3 and Objective 3 should mention that shifted-domain behaviour is assessed across
      repeated runs, not a single run

### D2. §3.6 ? training procedure now describes a sweep
Currently: "Each model was trained once, under the single fixed seed, without repeated
runs... All reported quantities are therefore single-run point estimates rather than
averages over multiple training runs, and no training-time variance or confidence
intervals are available."

This is now false and describes the study's principal weakness as though it still applies.

- [ ] Replace with a description of the five-seed sweep: seeds 42?46, three architectures,
      fifteen runs, identical split, per-run provenance recording
- [ ] State that all reported quantities are means with standard deviations across seeds
- [ ] Remove the sentence disclaiming variance estimates

### D3. §3.6 ? global seed statement
"a single global random seed of 42 was set" ? the seed is now a run parameter.

- [ ] "The random seed was set per run as an explicit parameter (seeds 42?46), applied to
      the Python, NumPy and PyTorch CPU and CUDA generators, to seeded DataLoader worker
      initialisation, and to a seeded generator"

### D4. §3.9.1 ? reproducibility section needs the provenance guard
Describes git commit recording and clean-tree gating, but not the artefact-level
provenance now in place.

- [ ] Add: every artefact records run identifier, seed, split hash and checkpoint hash;
      summary generation refuses to proceed unless all runs share a run identifier, split
      hash, seed set and evaluation cohort
- [ ] Add: experiment artefacts are version-controlled

### D5. §3.2 / Table 3.1 ? skull-stripping status
Nothing in Chapter 3 records that the skull-stripping confound was tested and withdrawn.
The Chapter 4 rewrite covers it, but the methods chapter should note the audit exists.

- [ ] Add a sentence to §3.3.2 or §3.2.4 pointing to the audit and its finding

### D6. §1.7 Significance ? remove the reversal framing
"Instability on a canine collection alone could be dismissed as a species artefact;
observing the same instability on human data ... cannot be explained in that way."

This survives, but the section should not imply that the two probes gave *divergent*
orderings.

- [ ] Verify §1.7 makes no reversal claim
- [ ] Consider adding that the human probe additionally resolves architectures the canine
      probe cannot

---

## E. Citations ? separate task

Not included above because it needs its own pass. The citation integrity audit in the repo
checks only that placeholders match placeholders; it does not verify that any reference
exists. `references_search_table.md` lists every entry as "TBD / To search".

- [ ] Resolve every DOI in the reference list
- [ ] Check author lists, years, journal names and volume/page numbers against the resolved
      record
- [ ] Flag any reference that cannot be resolved

Two to check first, because the identifiers are unusual in form:
- Aresta et al. (2026), medRxiv, DOI `10.64898/2026.01.13.26344038`
- Musa et al. (2026), *Big Data and Cognitive Computing* 10(3), 76

And one that matters for the dataset naming question in A5:
- Amin et al. (2020), ICDC-Glioma, DOI `10.7937/TCIA.SVQT-Q016`

---

## Suggested order

1. A1?A6 (factual errors) ? half a day
2. D1?D6 (content updates) ? half a day
3. B1?B4, C1?C5 (numbering and presentation) ? two hours
4. E (citations) ? half a day, done separately

Items A and D change what the document claims. Items B and C change how it reads. If time
runs short, A and D are the ones that matter.

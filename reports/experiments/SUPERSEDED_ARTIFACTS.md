# Superseded Artifacts

Nothing listed here should be cited, quoted, or regenerated into a manuscript. All of it
is retained as the historical record and as evidence of what was corrected.

**Authoritative results live in `reports/experiments/consolidated/`.**

Last updated: August 2026, after run set `2026-08-sweep-a`.

---

## Run sets

| Run set | Branch / archive | Contains | Status |
|---|---|---|---|
| Run A (Ubuntu) | `runA-ubuntu-preserved`, `research_ARCHIVE_RUN_A_20260809.tar.gz` | Internal performance, calibration, D3B. **No D3C.** | Superseded |
| Run B (Windows) | `windows-runB-archive`, `reports/experiments/runB_windows/` | D3C only, on the earlier 569-patient cohort | Superseded |
| `2026-08-sweep-a` | `main` | All evaluations, 5 seeds × 3 architectures, 610-patient D3C | **Authoritative** |

The proposal PDF's Chapter 4 draws internal, calibration and D3B numbers from Run A and
D3C numbers from Run B. Those are different checkpoints evaluated on different cohorts.
The ordering-reversal claim that followed from that comparison is withdrawn.

---

## Tables

| File | Problem |
|---|---|
| `tables/table_2_internal_performance.*` | Seed 46 only, reported as the result |
| `tables/table_4_d3b_domain_shift.*` | Seed 46 only |
| `tables/table_5_d3b_temperature_scaled.*` | Seed 46 only |
| `tables/table_6_d3c_domain_shift.csv` | Run B, 569-patient cohort |
| `tables/table_7_d3c_temperature_scaled.csv` | Run B |
| `tables/table_8_cross_dataset_comparison.csv` | Mixes Run A and Run B macro-F1 |
| `tables/temperature_scaling_schema_debug.md` | Diagnostic scratch file |

Replaced by `consolidated/tables/`, all seed-aggregated with dispersion.

---

## Figures

`reports/experiments/figures/figure_2` through `figure_9` were generated from Run A or
Run B. Replaced by `consolidated/figures/`.

`figure_1_reliability_pipeline` remains valid ? it is a schematic, not a result.

---

## Manuscript drafts

| File | Problem |
|---|---|
| `manuscript_draft_v1.md` and all `_before_*` variants | Run A, D3B-only. Mentions D3C zero times. Uses `REF-XXX-NNN` placeholders. |
| `paper_ready_results_section.md` | Run A single-seed numbers |
| `paper_ready_discussion_section.md` | Built on the withdrawn reversal |
| `paper_ready_abstract_conclusion.md` | Run A numbers |
| `paper_ready_introduction_section.md` | Predates the seed sweep |
| `paper_ready_methods_section.md` | Describes single-run training |
| `integrated_results_narrative.md` | Run A |

Replaced by `CHAPTER_4_RESULTS_REWRITTEN.md`, `CHAPTER_5_CONCLUSION_REWRITTEN.md`,
`ABSTRACT_REWRITTEN.md`.

---

## Reference tracking

| File | Problem |
|---|---|
| `reference_list_placeholders.md` | 23 entries, placeholder IDs, serves the superseded draft. Overlaps the proposal's list by 8 entries. |
| `supervisor_review_package/05_reference_list_placeholders.md` | Byte-identical copy of the above |
| `references_search_table.md` | Every entry `TBD / To search` |
| `citation_integrity_audit.md` | Checks placeholders against placeholders. Does not verify that any reference exists. Its PASS is not evidence of citation integrity. |

Replaced by `CANONICAL_REFERENCES_45.md`.

---

## Supervisor review package

`reports/supervisor_review_package/` was assembled from Run A and is superseded in full,
except `SUPERVISOR_UPDATE_2026-08.md`, which documents the correction.

---

## Withdrawn claims

Recorded so they cannot re-enter the manuscript.

| Claim | Where | Status |
|---|---|---|
| Architecture ordering reverses between D3B and D3C | Proposal §4.6, §5.1 | **Withdrawn.** Ordering is E001 > E002 > E003 on the means of both probes; E001 first on D3C at 5/5 seeds. |
| D3B prediction shares (ResNet18 13.2% no-tumour) | Proposal Table 4.4b | **Withdrawn.** One seed of Run A. Across seeds, 26.1% ± 13.8%. |
| Per-architecture temperature differences | Proposal Table 4.3 | **Withdrawn.** Architecture means are 1.226 / 1.226 / 1.234; ResNet18 alone spans 1.1519?1.3113 across seeds. |
| ViT-B/16 showed the largest ECE reduction | Proposal §4.3 | **Withdrawn.** ViT is consistently the worst calibrated, before and after scaling, at every seed. |
| D3C cohort of 569 patients / 2,845 slices | Throughout the proposal | **Superseded.** 610 patients / 3,050 slices. |
| Skull stripping confounds D3C | Earlier project notes | **Withdrawn on measurement.** See `reports/datasets/D3C_skull_stripping_audit.md`. D3C retains extracranial anatomy and is less masked than D1. |

---

## Why this happened

Experiment artefacts were excluded from version control, so nothing bound a reported
value to the checkpoint that produced it. Regenerating one stage overwrote its outputs in
place while leaving downstream tables untouched and unmarked.

Now prevented: artefacts are version-controlled; every run records run identifier, seed,
split hash and checkpoint hash; and `scripts/consolidate_sweep_results.py` refuses to
summarise unless all runs share a run identifier, split hash, seed set and evaluation
cohort.

---

## Superseded audit figures

| Figure | Where it appears | Replacement |
|---|---|---|
| D1?D3C: 19,951,985 comparisons | Proposal Table 3.4, §3.4.3, §4.1 | **21,529,910** over 3,070 slices |
| D3C cohort 569 patients / 2,845 slices | Throughout the proposal | **610 patients / 3,050 slices** analysed; 614 / 3,070 audited |
| "approximately twenty million comparisons" | Proposal §5.1 | more than twenty-one million |

The original D1?D3C audit was run against the earlier 569-patient cohort, so roughly 205
slices from 41 patients were never compared against D1. The re-run covers all 3,070
converted slices, a superset of the 3,050 evaluated.

## Claims closed by measurement since the sweep

| Claim | Status |
|---|---|
| D3C is skull-stripped and therefore differs systematically from D1 | **Withdrawn.** D3C retains extracranial anatomy and is less masked than D1. |
| Imaging plane may explain the D3C shifted-domain separation | **Ruled out.** Dropping 11 oblique patients shifts the mean glioma rate by ?0.0052 and preserves the ordering. |

# Session Notes — 2026-08-09 to 2026-08-12

Working session covering two themes: enforcing the `CLAUDE.md` hard rules in the
training and table-generation layer, repairing the D3C cohort pipeline, and running the
seed sweep. All work is committed on `main`. Run set `2026-08-sweep-a` (seeds 42-46 x 3
architectures) supersedes every earlier D1 and D3C number, including Run A, Run B, and
the 0.69/0.46/0.22 glioma prediction rates.

## Commits

| Commit | What it addressed |
|---|---|
| `d6ae740` | Rules 1–3 in the three trainers. Deterministic training (`deterministic=True`, `benchmark=False`, `use_deterministic_algorithms(True)`, seeded `worker_init_fn` and `Generator`, `CUBLAS_WORKSPACE_CONFIG` set before CUDA init). `validate_config()` asserts config against executed code; E002/E003 configs stripped of the unimplemented `scheduler` blocks and duplicated keys. Provenance (`run_id`, git commit, seed, `split_csv_sha256`, `checkpoint_sha256`) on every training artefact plus a `provenance.json` sidecar; `RUN_ID` required from the environment. `verify_split()` enforces rule 5 at runtime. Adds `CLAUDE.md`. |
| `0a896d7` | Removed the duplicate series-selection logic from `download_d3c_selected_series.py` and drove download, inspection and conversion from the selection manifest. All three now abort on orphan series, missing series, or a DICOM whose header UID is outside the selected set. |
| `dfe80b9` | Made `select_d3c_upenn_gbm_series.py` itself deterministic: `kind="mergesort"`, total-order sort keys ending in `SeriesInstanceUID`, `drop_duplicates` in place of `groupby().first()`, fixed column order, manifest sha256 recorded in the report. |
| `4b7b502` | Committed the corrected, hash-pinned selection manifest and report. |
| `3d13c38` | `.gitignore`: replaced `experiments/*/` with `experiments/**/*.pt`, so 48 artefact files (2.6 MB) are version-controlled and the three checkpoints (1.2 GB) stay out. |
| `d3ad69a` | Rule 4 in `generate_summary_tables.py`: `assert_single_run_set()` aborts unless the three `provenance.json` files share a `run_id` and a `split_csv_sha256`; `git_commit` deliberately not asserted. Adds `table_1_run_set_provenance`. Refreshed the `CLAUDE.md` rule status. |
| `7098e1f` | Header-based cohort composition in the D3C inspection: acquisition plane from the slice normal, contrast from `ContrastBolusAgent`, new columns in the series summary CSV. |
| `94b4fc8` | Pre/post contrast from `ContrastBolusStartTime` versus `AcquisitionTime`, with field coverage reported before any verdict. |
| `f5f844f` | D3C cohort completed: 614/614 series from the hash-pinned manifest, 0 failures. |
| `311d47f` | A blank `SeriesInstanceUID` is an error, not a bin. 614 LICENSE sidecars had collapsed into a phantom 615th series; files are now partitioned by the DICM magic number and counted in the report. |
| `f557f43` | D3C cohort exclusion at the analysis-manifest level: 4 non-axial series dropped, 11 oblique flagged, selection record and hash untouched. |
| `3c3f677`, `1cc9aa7` | Skull-stripping audit and the resulting retraction. |
| `17b3af3`, `776d9ec` | `src/stats/`: Wilson, patient-clustered bootstrap, McNemar with Holm, random-intercept logistic regression. 77 tests, cross-validated against statsmodels 0.14.6. |
| `5ee1e28` | D3C inspection, pHash manifest and both overlap audits regenerated against the 614-series cohort. |
| `98ecc2e`, `4ec3a01` | Seed sweep wiring: `--seed`, seed-scoped outputs, 21 downstream scripts re-pathed, rule 4 extended to require identical `seed`, resumable driver. |
| `7049875` | D3C evaluation pointed at the analysis cohort; evaluation sweep driver. |
| `237736a` | `src/stats/` wired to the real data: correlation, bootstrap CIs, McNemar/Holm, mixed model. |
| `05f17a3` | Seed-42 investigation: partly characterised, not explained. |

Plus 30 mechanical per-run commits from the two sweep drivers (15 training, 15
evaluation), each committing one run's artefacts so the next passes `ensure_clean_git()`.

## Retraction: D3C is not skull-stripped

**Claim withdrawn.** D3C was recorded in `CLAUDE.md`, in this file, and in statements
made during the session as "100% Processed_CaPTk (skull-stripped, atlas-registered)",
with skull stripping treated as a cohort-wide confound requiring a control on the D1
test split.

**How it went wrong.** The `Processed_CaPTk` string was read as evidence of skull
stripping. It is not: CaPTk preprocessing covers reorientation, co-registration and
resampling, and stripping is a separate step that was not applied to the DICOM series in
this collection. Confirming that all 614 series carry the string confirmed only that —
it was then reported as confirming the confound "at 100%", which the evidence never
supported.

**Evidence** (`reports/datasets/D3C_skull_stripping_audit.md`, commit `3c3f677`;
40 sampled D3C series, central slice each, against 40 matched D1 glioma images):

| Metric | D3C | D1 |
|---|---|---|
| Images with a masked background | **0 / 40** | 0 / 40 |
| Air region exactly zero (1.0 = masked) | 0.262 [0.122–0.685] | 0.373 [0.049–0.839] |
| Corner non-zero fraction | 0.540 | 0.280 |
| Outer ring brighter than brain core | 0.256 | 0.198 |

Skull stripping sets everything outside the brain to exactly zero; no D3C image shows
that. A quarter of outer-ring pixels are brighter than the brain core, the T1 scalp-fat
signature. Measurements on the source DICOM are identical to those on the converted
PNGs, so the conversion is not responsible. D3C is *less* masked than D1, so there is no
stripping differential between the cohorts.

**Corrected severity.** From "known confound requiring a dedicated control experiment"
to "not a confound; no control required". The planned skull-stripping control on the D1
test split is removed from the outstanding work.

**What survives.** D3C is co-registered, resampled and intensity-normalised by CaPTk
while D1 is not. Those are genuine preprocessing differences and a real domain shift
component, and they stay as a stated limitation — but they are not skull removal and do
not justify the stronger claim.

## Two defects worth remembering

**`groupby("PatientID").first()`** returns the first *non-null value of each column
independently*, not the first row. A null in the winning series was backfilled from a
different series, so an output row could describe no real series. Reproduced directly.
Replaced with `drop_duplicates(subset="PatientID", keep="first")`.

**Duplicate selection logic.** `download_d3c_selected_series.py` re-implemented the
selection rule with a different term vocabulary and disagreed with the authoritative
step. The single-source-of-truth manifest plus abort-on-orphan guards is the structural
fix; the duplicated classifier is deleted.

## Known traps

Three facts that are easy to misread and are not obvious from the artefacts alone.

**Commit `afbd3f2` is mislabelled.** Its subject line reads "E002 frozen run set, seed
42", but it contains **no E002 files at all** — only three modified E001 files from a
second E001 run. E002 was never trained under `RUN_ID=2026-08-frozen-a`; its directory was
empty until the sweep. Anyone reading `git log --oneline` will believe a run set existed
that never did. The commit is left as-is because rewriting history would be worse; this
note is the correction. `2026-08-sweep-a` is the only complete run set.

**`checkpoint_sha256` is not reproducible, and that is not a determinism failure.** E001
was trained twice from the same seed at different commits and reproduced all six test
metrics to full float precision (`test_macro_f1` 0.9546127394877477, `best_epoch` 6), but
the two checkpoints have different SHA-256 digests. This is `torch.save` serialisation,
not training nondeterminism. Since rule 3 records `checkpoint_sha256` and rule 1 claims
determinism, a future session comparing two runs by checkpoint hash would reasonably but
wrongly conclude that determinism had broken. **Compare metrics, not checkpoint bytes.**

**The independence audit's comparison count overstates its power.** The near-overlap
report cites 21,529,910 pairwise comparisons between D1 and D3C, which sounds
exhaustive. But the D3C manifest holds 3,070 unique SHA-256 values and only **2,563
unique pHash values** — the five central slices of a series are frequently pHash-identical
to each other. The comparisons are therefore not 21.5M independent visual comparisons,
and the "0 exact, 7 near" result is correspondingly weaker than the raw count implies.
Related: all four D1 images in the 7 near pairs are in the **Training** split, so if those
pairs are genuine near-duplicates rather than hash collisions, two of 614 D3C patients
were seen in near-identical form during training.

## D3C cohort state

- **Selected: 614 patients / 614 series** — 568 `preferred_t1_postcontrast`,
  46 `secondary_t1`.
- **Manifest sha256: `fc6deef35438027d6b76fdc323b5a4d96538312dd2da8f4a93afb40f3488761c`**
  (`reports/datasets/d3c_upenn_gbm_series_selection/selected_series_one_per_patient.csv`),
  confirmed byte-identical across two independent live TCIA queries.
- Prior downloads produced **575** (Ubuntu) and **569** (Windows) from the duplicate
  selector: 39 patients dropped entirely, 37 of them `preferred_t1_postcontrast`, and a
  different series chosen for 28 of the patients both selectors kept.
- **28 orphan directories deleted** (5,070 files), each re-verified at deletion time as
  a direct child of `RAW_DIR` and absent from the manifest. 547 correct series retained.
- **Complete: 614 / 614 series present**, 0 download failures, 113,133 DICOM files plus
  614 LICENSE sidecars. Inspection and conversion both run: 614 series / 614 patients
  inspected, 3,070 PNGs written.
- **Analysis cohort: 610 patients / 3,050 slices** after excluding the 4 non-axial
  series, with 11 oblique series flagged rather than dropped
  (`reports/datasets/D3C_cohort_exclusion_report.md`). The selection manifest is
  unchanged and keeps its hash.
- **Independence audit redone** against the 614-series cohort: 21,529,910 comparisons,
  0 exact overlaps, 7 near pairs (pHash <= 4), 0 cross-class. The 7 involve only 2 D3C
  patients and 4 D1 images, all glioma-glioma, and **all four D1 images are in the
  Training split**.

## Header findings (confirmed on the full 614-series cohort)

Provisional first-slice figures were 3 non-axial and 7 oblique; the full run over all
113,133 DICOM files gives **4 non-axial** (2 coronal, 2 sagittal) and **11 oblique >10°**,
worst 26.1°, with **0 series showing inconsistent orientation across slices**.

- **Plane:** 550 axial (99.46%), 2 coronal, 1 sagittal. Every series has
  `ImageOrientationPatient`.
- **3 non-axial series flagged.** D1 is axial, so these are a plane confound. All three
  are honestly described (`COR T1 MPR`, `COR T1 POST FS`, `T1 SAG MPRAGE`) — the
  description-based classifier accepted them despite the plane.
- **7 axial series more than 10° off plane**, worst 26.1°. All labelled `AX`/`axial`, so
  free text could never have caught these.
- **Contrast timing is unrecoverable.** `ContrastBolusStartTime` is populated in
  **0 of 555** series; `AcquisitionTime` in all 555. A direct tag audit over 120 series
  shows the timing half of the Contrast/Bolus module stripped — `StartTime`, `StopTime`,
  `FlowRate` absent entirely, `TotalDose` present but zero-length in 112 of 112 — while
  `Agent` survives in 117 and `Volume` in 116. `StudyTime` blanked in 119 of 120,
  consistent with de-identification. **Pre versus post contrast cannot be verified from
  headers for D3C and remains inferred from `SeriesDescription`; this is a limitation,
  not a verified property.** The 42 `secondary_t1` series cannot be resolved.
- All 614 selected series are `Processed_CaPTk`. **This does not mean skull-stripped.**
  An earlier note in this file, and a statement made during the session, took the
  `Processed_CaPTk` string as confirmation of a skull-stripping confound "at 100%". That
  was wrong: all that had been confirmed was that every series carries the string. A
  quantitative audit (`reports/datasets/D3C_skull_stripping_audit.md`, commit `3c3f677`)
  shows D3C retains extracranial anatomy cohort-wide — 0 of 40 sampled images have a
  masked background, and D3C is less masked than D1 on every measure. See the retraction
  below.

**No selection change has been made** on the basis of these findings, per instruction.

## Seed sweep results — run set `2026-08-sweep-a`

15 training runs (seeds 42–46 × 3 architectures) in 2:41:04, then 90 evaluation steps in
9:24. D3C figures are on the **analysis cohort**: 610 patients / 3,050 slices, after the
documented non-axial exclusion. All 15 runs carry a consistent `provenance.json`
(`run_id`, `seed`, `seed_source=cli`, frozen split hash) and 15 distinct git commits, one
per run.

The refactor that added `--seed` was verified behaviour-neutral: E001 at seed 42
reproduced the pre-refactor run on all six metrics to full float precision
(`test_macro_f1` 0.9546127394877477, `best_epoch` 6).

### Internal test macro-F1

| Model | seed42 | seed43 | seed44 | seed45 | seed46 | mean ± SD |
|---|---|---|---|---|---|---|
| E001 ResNet18 | 0.9546 | 0.9677 | 0.9715 | 0.9723 | 0.9650 | 0.9662 ± 0.0071 |
| E002 EfficientNet-B0 | 0.9744 | 0.9649 | 0.9632 | 0.9661 | 0.9678 | 0.9673 ± 0.0043 |
| E003 ViT-B/16 | 0.9537 | 0.9565 | 0.9588 | 0.9564 | 0.9529 | 0.9557 ± 0.0024 |

**Seed variation is as large as architecture variation.** E001 and E002 differ by 0.0011
on the mean against SDs of 0.0071 and 0.0043, and their rank swaps between seeds (E002
ahead at seed 42, E001 ahead at seed 44). Single-seed internal rankings are not stable.

### D3C glioma prediction rate (610 patients / 3,050 slices)

| Model | seed42 | seed43 | seed44 | seed45 | seed46 | mean ± SD |
|---|---|---|---|---|---|---|
| E001 ResNet18 | 0.8013 | 0.6331 | 0.6541 | 0.6613 | 0.6220 | 0.6744 ± 0.0727 |
| E002 EfficientNet-B0 | 0.4577 | 0.6118 | 0.5256 | 0.4525 | 0.5213 | 0.5138 ± 0.0646 |
| E003 ViT-B/16 | 0.4630 | 0.2102 | 0.2085 | 0.2502 | 0.1856 | 0.2635 ± 0.1139 |

E001 > E002 > E003 holds at four of five seeds; the exception is seed 42, where E002 and
E003 effectively tie. Separation relative to seed noise, as a gap-to-SD ratio: E001 vs
E002 is **0.19 internally but 2.34 on D3C**; E001 vs E003, 2.22 against 4.40.

### D3B glioma prediction rate (53 patients / 265 slices)

| Model | seed42 | seed43 | seed44 | seed45 | seed46 | mean ± SD |
|---|---|---|---|---|---|---|
| E001 ResNet18 | 0.3094 | 0.4604 | 0.3245 | 0.5925 | 0.3245 | 0.4023 ± 0.1227 |
| E002 EfficientNet-B0 | 0.5962 | 0.2226 | 0.3811 | 0.3132 | 0.3283 | 0.3683 ± 0.1396 |
| E003 ViT-B/16 | 0.2377 | 0.2453 | 0.3283 | 0.2830 | 0.1509 | 0.2491 ± 0.0656 |

**D3B supports no ranking claim.** There is no stable ordering: E001 and E002 alternate
at the top across seeds, and E003 leads E001 at seed 44. At 53 patients the seed noise
swamps any architecture effect. D3B should be reported as a cross-species probe with
intervals, and must not be used to rank the models.

### Internal performance against shifted-domain behaviour: Simpson's paradox

| Grouping | n | Pearson r | 95% CI | p |
|---|---|---|---|---|
| Pooled (all 15 runs) | 15 | **+0.474** | [−0.049, 0.789] | 0.074 |
| E001 within | 5 | −0.799 | [−0.987, 0.196] | 0.105 |
| E002 within | 5 | −0.542 | [−0.966, 0.638] | 0.345 |
| E003 within | 5 | −0.376 | [−0.951, 0.755] | 0.532 |
| **Architecture-centred** | 15 | **−0.514** | [−0.812, −0.001] | **0.050** |

The pooled and within-architecture correlations have **opposite signs**. Architecture is
a confounder: E003 sits low on both axes and drags the pooled estimate positive. Holding
architecture fixed, a run that scores better internally predicts glioma *less* often
under shift. **Never quote the pooled figure on its own.** The centred estimate sits
exactly on p = 0.050 and the within-architecture correlations are n=5 each, so this is
suggestive, not established.

### E001 vs E002 — the central comparison

Random-intercept logistic regression, `glioma_predicted ~ model + (1|patient)`, E001 as
reference, fitted per seed:

| Seed | OR (E002 vs E001) | 95% CI | p | McNemar Holm p |
|---|---|---|---|---|
| 42 | 0.0765 | [0.0650, 0.0899] | 6.1e-212 | 4.4e-177 |
| 43 | 0.8434 | [0.7318, 0.9721] | 1.9e-02 | 3.1e-02 |
| 44 | 0.3842 | [0.3337, 0.4424] | 2.4e-40 | 5.1e-34 |
| 45 | 0.1912 | [0.1639, 0.2230] | 1.7e-98 | 9.0e-100 |
| 46 | 0.4590 | [0.3981, 0.5293] | 9.0e-27 | 3.0e-27 |

**Direction consistent and significant at all five seeds**: E002 has lower odds of
predicting glioma than E001 for the same patient. Two models internal macro-F1 cannot
separate are clearly separated under shift. But the **magnitude is not stable** — OR
spans 0.077 to 0.843, an elevenfold range — so "E001 predicts glioma more often than
E002 under shift" is supported; "by a factor of X" is not. Seed 43 is the weak case and
the only seed where the two bootstrap CIs overlap.

Supporting inference: patient-clustered bootstrap (2,000 resamples of patients) gives a
median CI width of 0.0626 against roughly 0.0334 for a naive slice-level interval, with
ICC 0.489–0.690. Slice-level intervals would have been nearly twice too narrow, and at
seed 43 would have falsely separated E001 from E002. McNemar with Holm: 14 of 15
comparisons significant, the exception being E002 vs E003 at seed 42.

### Seed 42 investigation: unexplained

**Verdict: partly characterised, not explained.** Recorded in
`reports/experiments/D3C_seed42_investigation.md`.

- The premise that all three architectures are anomalous is **wrong**. Against each
  model's own other four seeds, the seed-42 D3C rate is z=+8.7 (E001) and z=+9.3 (E003)
  but **z=−1.1 for E002**, which is entirely ordinary. The non-significant McNemar is
  E002 vs E003 and arises because E003 rose to meet a normal E002.
- E003 alone shows a training-trajectory difference: 17 epochs, best epoch 12, against
  10–12 epochs and best epoch 5–7 elsewhere.
- E001 and E003 track each other across seeds at r=+0.993, and the association survives
  dropping seed 42 (r=+0.842), so it is not an artefact of the outlier. E002 does not
  track either. Seed 42 is the extreme end of a shared seed axis, not a discrete event.
- **Nothing measured on D1 predicts the D3C rate** once architecture means are removed:
  per-class recall, predicted-class shares, temperature, best epoch and epochs trained
  are all non-significant.

Report as **unexplained seed sensitivity**. Excluding seed 42 would need a reason
established before its result was seen, and there is none. Report all five seeds with
intervals.

## Outstanding

**Analysis and reporting**

- **Segmentation-gated D3C** — not started. No design for this is recorded in the repo;
  it needs specifying before it can be scoped.
- **Figure regeneration with error bars.** `generate_summary_figures.py` and
  `generate_d3c_summary.py` still draw single-seed figures. Every headline figure now
  needs to show the seed spread, since the whole point of the sweep is that single-seed
  values are unstable. The bootstrap intervals in
  `reports/experiments/tables/d3c_bootstrap_intervals.csv` are the input.
- **Seed-scope the tables.** `generate_summary_tables.py` writes to
  `reports/experiments/tables/` regardless of `SEED`, so each run overwrites the last and
  only the most recent seed survives on disk. Tables need a seed segment in their path
  before the five seeds can coexist. The five per-seed table sets generated so far are
  deliberately uncommitted for this reason.

**Rule gaps (from the `CLAUDE.md` status list)**

- **Rule 4 — the two summary scripts.** `generate_summary_figures.py` and
  `generate_d3c_summary.py` aggregate across the three models with no
  `assert_single_run_set()` call. They can silently mix seeds or run sets, which is
  exactly the defect `generate_summary_tables.py` now guards against. This is the most
  significant remaining gap.
- **Rule 3:** the calibration, D3B/D3C evaluation and temperature-scaling scripts still
  write unstamped artefacts — no `run_id`, seed or checkpoint hash. Their outputs are
  traceable only by the directory they sit in.
- **Rule 2:** `configs/E001_*.yaml` still declares `dataset.image_column`,
  `label_column`, `split_column`, `training.loss`, the whole `evaluation:` block and
  five `outputs.save_*` flags that no code reads.

**Statistical follow-ups**

- The architecture-centred correlation sits exactly on p = 0.050 with n=15 and three
  architecture means removed. It is suggestive, not established, and should not be
  reported as a finding without more seeds.
- The mixed model is fitted per seed. Pooling seeds needs a second random effect for
  seed, which `src/stats/mixed_effects.py` does not implement.
- Wilson intervals in `src/stats/wilson.py` are built and tested but still unused by any
  analysis.

**Repository hygiene**

- `all_series.csv` and `classified_series.csv` under
  `reports/datasets/d3c_upenn_gbm_series_selection/` are stale orphans from the Windows
  import, written by no current script, with the deleted classifier's vocabulary — 35
  `preferred_t1_postcontrast` against the real 605. Delete, or have the selection script
  write `classified_series.csv` so the analysis is reproducible against the pinned cohort.
- Three D3C scripts carry a UTF-8 BOM from the Windows branch
  (`convert_d3c_selected_slices.py`, `probe_d3c_upenn_gbm_tcia.py`,
  `select_d3c_upenn_gbm_series.py`). Harmless to Python; inconsistent with the repo.
- `~/research_ARCHIVE_RUN_A/` has never been verified to exist or to match the Run A
  numbers it is supposed to preserve.

**Untouched** (carried over from `CLAUDE.md` known context)

- D3C is co-registered, resampled and intensity-normalised by CaPTk while D1 is not.
  That preprocessing difference stands as a limitation; it is not skull stripping.
- Pre versus post contrast cannot be verified from D3C headers and remains inferred from
  `SeriesDescription`.

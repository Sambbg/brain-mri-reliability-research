# Session Notes — 2026-08-09

Working session covering two themes: enforcing the `CLAUDE.md` hard rules in the
training and table-generation layer, and repairing the D3C cohort pipeline. All work
is committed on `main`. No models were retrained and no results were regenerated.

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
- **67 missing series being re-downloaded.** In progress at session end (~562/614).
  Inspection and conversion have not yet been run against the completed cohort.

## Header findings (provisional)

Measured on 553–555 series, first slice each, so the cross-slice orientation check is
not included. To be confirmed by the full inspection run.

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

## Outstanding

**Blocking the frozen run set**

- Re-download must complete, then `inspect_d3c_dicom_download.py` and
  `convert_d3c_selected_slices.py` need running against the 614-series cohort.
- Retraining under a single `RUN_ID` has not started. Until it does,
  `generate_summary_tables.py` aborts by design (no `provenance.json` exists) and every
  existing D1 and D3C number is superseded — including the 0.69/0.46/0.22 glioma
  prediction rates and the independence audit, which was run against the 575-series
  cohort.
- Decision needed on the 3 non-axial and 7 oblique series.

**Rule gaps (from the `CLAUDE.md` status list)**

- **Rule 2:** `configs/E001_*.yaml` still declares `dataset.image_column`,
  `label_column`, `split_column`, `training.loss`, the whole `evaluation:` block and
  five `outputs.save_*` flags that no code reads.
- **Rule 3:** the calibration, D3B/D3C evaluation and temperature-scaling scripts still
  write unstamped artefacts.
- **Rule 4:** `generate_summary_figures.py` and `generate_d3c_summary.py` aggregate
  across the three models without asserting a shared run set.
- **Rule 6 interaction:** with `experiments/` tracked, the first trainer's outputs dirty
  the tree and `ensure_clean_git()` blocks the second. Commit each model's artefacts
  before training the next. This is why `run_id`, not the git commit, identifies a run
  set.

**Repository hygiene**

- 18 Run A artefacts became visible to git with the `.gitignore` fix and are
  **deliberately uncommitted** — they predate rule 3, carry no provenance, and will be
  superseded by the frozen run set. Decide whether to snapshot Run A or wait.
- `reports/datasets/D3C_acquisition_log.md` and `d3c_selected_series_download/*` still
  describe the defective 575-series download; left uncommitted until the re-download
  regenerates them.
- `all_series.csv` and `classified_series.csv` under
  `reports/datasets/d3c_upenn_gbm_series_selection/` are stale orphans from the Windows
  import. No current script writes them and their category vocabulary is the deleted
  classifier's — 35 `preferred_t1_postcontrast` against the real 605. Delete them, or
  have the selection script write `classified_series.csv` so the analysis is
  reproducible against the pinned cohort.
- Three D3C scripts carry a UTF-8 BOM from the Windows branch
  (`convert_d3c_selected_slices.py`, `probe_d3c_upenn_gbm_tcia.py`,
  `select_d3c_upenn_gbm_series.py`). Harmless to Python; inconsistent with the repo.
**Untouched this session** (carried over from `CLAUDE.md` known context)

- `src/stats/` remains unbuilt: Wilson intervals, patient-clustered bootstrap, McNemar
  with Holm, mixed-effects logistic regression.
- Seed sweep wired up: seeds 42–46 × 3 architectures via `scripts/run_seed_sweep.py`,
  under `RUN_ID=2026-08-sweep-a`. Trainers take `--seed` and write to
  `experiments/<exp>/seed<N>/`; downstream scripts resolve that directory from `SEED`.
- ~~The D3C skull-stripping confound still needs a skull-stripping control on the D1
  test split.~~ **Withdrawn.** D3C is not skull-stripped, so no such control is
  required. See the retraction below.

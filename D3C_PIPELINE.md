# D3C Pipeline — UPENN-GBM Human Glioma Domain-Shift Evaluation

D3C is the primary same-species (human) glioma-focused domain-shift dataset, alongside
the canine cross-species probe (D3B). Source: UPENN-GBM (TCIA), 630 patients in the
collection, SpeciesDescription = "Homo sapiens". Role: shifted-domain evaluation of the
D1-trained models; not a full four-class external validation set (glioma-focused only).

All commands run from the repository root inside the project virtual environment.

## Two conventions that apply throughout

**`RUN_ID`** identifies a frozen run set and is required by the training scripts. Every
model compared in one table must share it. Current run set: `2026-08-sweep-a`.

**`SEED`** selects which seed's artefacts a downstream script reads. Training writes to
`experiments/<experiment>/seed<N>/`; calibration, evaluation and table generation resolve
that directory from the `SEED` environment variable, defaulting to 42.

    SEED=44 python src/evaluation/generate_summary_tables.py

**Commit between steps.** The training and temperature-scaling scripts call
`ensure_clean_git()` and abort on a dirty tree, and experiment artefacts are tracked. The
two sweep drivers handle this themselves; if running a step by hand, commit first.

## Prerequisite — D1 manifests (needed by the overlap audit)

    python src/data/create_d1_manifest.py
    python src/data/create_d1_deduplicated_manifest.py
    python src/data/create_d1_perceptual_hash_manifest.py

## Stage 1 — Cohort acquisition and preparation

1.  `python src/data/probe_d3c_upenn_gbm_tcia.py`
        Queries TCIA. Confirms 630 patients, Homo sapiens, MR modality, and the
        SeriesDescription vocabulary. No image download.

2.  `python src/data/select_d3c_upenn_gbm_series.py`
        **The single source of truth for the cohort.** Selects one T1 series per patient
        (post-contrast preferred). Deterministic: total-order sort keys ending in
        SeriesInstanceUID, `kind="mergesort"`, `drop_duplicates` rather than
        `groupby().first()`, fixed column order. Records the manifest sha256 in its
        report — quote that hash when reporting D3C results.
        Current: 614 patients, sha256 `fc6deef3...761c`.

3.  `python src/data/download_d3c_selected_series.py`
        Downloads exactly the SeriesInstanceUIDs in the manifest. Performs no selection
        of its own. Audits every selected series against disk and aborts if any is
        missing, writing `download_failures.csv` with reasons.

4.  `python src/data/inspect_d3c_dicom_download.py`
        Validates DICOM readability, measures acquisition plane from
        ImageOrientationPatient and contrast status from the headers, and writes the
        Cohort Composition section. Aborts on any series not in the manifest, any
        selected series missing, and any DICOM with a blank SeriesInstanceUID. Non-DICOM
        sidecars (TCIA ships one LICENSE per series directory) are identified by the
        absence of the DICM magic number, set aside, and counted in the report.

5.  `python src/data/convert_d3c_selected_slices.py`
        Writes 5 central-slice PNGs per series and the slice manifest. Manifest-driven
        with the same orphan and gap guards.

6.  `python src/data/create_d3c_perceptual_hash_manifest.py`
        Adds exact (SHA-256) and perceptual (pHash) hashes.

7.  `python src/data/build_d3c_analysis_manifest.py`
        **Applies the documented cohort exclusion.** Drops the 4 non-axial series (a
        plane confound against axial D1) and flags the 11 axial series more than 10
        degrees off plane with an `oblique_gt_10deg` column, so a plane sensitivity
        analysis filters one column rather than running a second exclusion. The selection
        manifest is not modified and keeps its hash; the exclusion is a separate,
        auditable step. Asserts the selection hash before running and aborts if the
        derived exclusion differs from the documented one.
        Output: 610 patients / 3050 slices — **this is what the evaluations read.**

## Stage 2 — Independence audit against D1

8.  `python src/data/check_d1_d3c_exact_overlap.py`     # expect 0 exact pairs
9.  `python src/data/check_d1_d3c_near_overlap.py`      # pHash Hamming <= 4

## Stage 3 — Training the seed sweep

    RUN_ID=2026-08-sweep-a python scripts/run_seed_sweep.py

Runs seeds 42-46 x 3 architectures, committing after each run so the next passes
`ensure_clean_git()`. Refuses to start on a dirty tree, stops on the first failure, and
skips (seed, architecture) pairs already recorded under this RUN_ID, so it is resumable.
`--dry-run` and `--seeds N ...` are available. About 2h40m for 15 runs.

Individual runs, if needed:

    RUN_ID=2026-08-sweep-a python src/training/train_e001_resnet18.py --seed 43

## Stage 4 — Calibration, temperature scaling and shifted-domain evaluation

    python scripts/run_eval_sweep.py

Runs the six per-model steps across all 15 checkpoints. Ordering is not arbitrary: the
temperature-scaling scripts call `ensure_clean_git()`, so each group runs temperature
scaling first while the tree is clean, then the five steps that do not care, then commits
once. Resumable; skips steps whose output exists. About 9 minutes.

## Stage 5 — Tables, statistics and investigation

    SEED=42 python src/evaluation/generate_summary_tables.py     # repeat per seed
    python src/evaluation/analyse_seed_sweep_statistics.py
    python src/evaluation/investigate_seed42_anomaly.py

`generate_summary_tables.py` asserts the three models share a `run_id`, a `seed` and a
`split_csv_sha256` before writing anything, and aborts otherwise.

`analyse_seed_sweep_statistics.py` is the consumer of `src/stats/`: internal-vs-shift
correlation, patient-clustered bootstrap CIs, McNemar with Holm, and the random-intercept
logistic model.

`investigate_seed42_anomaly.py` tests whether anything distinguishes the seed-42 runs.

Not yet seed-aware: `generate_summary_figures.py` and `generate_d3c_summary.py` neither
assert a shared run set nor show error bars. See SESSION_NOTES.md Outstanding.

## Key outputs

- `reports/datasets/d3c_upenn_gbm_series_selection/selected_series_one_per_patient.csv`
  (the cohort record, hash-pinned)
- `data/processed/D3C_analysis_manifest.csv`      (what the evaluations read)
- `data/processed/D3C_excluded_slices.csv`        (the exclusion, auditable/reversible)
- `reports/datasets/D3C_cohort_exclusion_report.md`
- `reports/datasets/D3C_dicom_inspection_report.md`  (plane, contrast, integrity)
- `reports/datasets/D1_D3C_near_overlap_report.md`
- `experiments/E00X_*/seed<N>/d3c_domain_shift_metrics.json`
- `reports/experiments/D3C_seed_sweep_statistics.md`
- `reports/experiments/D3C_seed42_investigation.md`

## Result summary — run set `2026-08-sweep-a`

Slice-level D3C glioma prediction rate, mean ± SD across seeds 42-46, on the 610-patient
analysis cohort:

| Model | D3C rate | Internal macro-F1 |
|---|---|---|
| E001 ResNet18 | 0.6744 ± 0.0727 | 0.9662 ± 0.0071 |
| E002 EfficientNet-B0 | 0.5138 ± 0.0646 | 0.9673 ± 0.0043 |
| E003 ViT-B/16 | 0.2635 ± 0.1139 | 0.9557 ± 0.0024 |

E001 vs E002 are indistinguishable internally (0.0011 apart, ranks swap between seeds)
but separated under shift at every seed (OR 0.077-0.843, all p < 0.05). Independence
audit: 21,529,910 comparisons, 0 exact, 7 near pairs, 0 cross-class.

> **Superseded.** Earlier versions of this file reported 69.4% / 46.3% / 21.8% from a
> single non-deterministic run against a defective 569-patient cohort. Those numbers, and
> all Run A and Run B figures, are superseded by `2026-08-sweep-a`.

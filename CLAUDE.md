# Brain MRI Reliability Research

MSc project, UTM. Evaluates whether internal accuracy predicts shifted-domain
reliability in brain MRI tumour classification.

## Hard rules

1. Training MUST be deterministic: cudnn.deterministic=True, cudnn.benchmark=False,
   torch.use_deterministic_algorithms(True), seeded DataLoader worker_init_fn and
   torch.Generator. Never set benchmark=True.
2. Configs MUST match executed code. If a config key is not implemented, delete
   the key. Do not leave `scheduler: cosine` declared but unimplemented.
3. Every output artefact MUST record run_id, git commit, seed, split_csv_sha256,
   and checkpoint_sha256.
4. Table generation MUST assert all three models share a run_id, a seed AND an
   identical split_csv_sha256, and abort otherwise. seed is required because a sweep
   runs every architecture at several seeds under one run_id, so run_id alone no longer
   identifies a comparable set. git_commit MUST NOT be asserted: experiment
   artefacts are version-controlled, so each model's outputs are committed before the
   next model trains and the three legitimately carry different commits.
5. NEVER regenerate data/splits/D1_leakage_aware_split.csv. Its sha256 is
   944ce00e4be958f3688a0996f6fb928fc7717e7c2804abb8000f28976efe0d43.
6. ensure_clean_git() blocks training on a dirty tree. Commit before every run.
7. Do not modify anything under reports/experiments/runB_windows/ or the
   runA-ubuntu-preserved branch. Both are provenance evidence.

## Known context

- Run A (Ubuntu, May 2026) produced tables 2-5: temperatures 1.2328/1.1596/1.2363,
  macro-F1 0.9666/0.9680/0.9582. Run B (Windows) produced tables 7-8: temperatures
  1.2725/1.1598/1.3770, macro-F1 0.9753/-/0.9648. Same split, different checkpoints.
  **Both are superseded by run set `2026-08-sweep-a`** (seeds 42-46 x 3 architectures).
  Do not reconcile current artefacts against these numbers; they are the historical
  record of the defect that the sweep fixed. See Q1_REVIEW_AUDIT.md finding D-1.
- Run A checkpoints archived at ~/research_ARCHIVE_RUN_A/.
- D3C is 100% Processed_CaPTk. **It is NOT skull-stripped** — this corrects an earlier
  entry here that called it skull-stripped and required a skull-stripping control on the
  D1 test split. Measured on 40 sampled series against 40 matched D1 glioma images
  (`reports/datasets/D3C_skull_stripping_audit.md`): 0 of 40 D3C images have a masked
  background, air is only 26% exactly-zero at the median where a mask would give 1.0,
  corners are 54% non-zero, and 26% of outer-ring pixels are brighter than the brain
  core, which is the T1 scalp-fat signature. D3C is if anything *less* masked than D1
  (air exactly-zero 0.262 vs 0.373), so there is no stripping differential and no
  confound in that direction. `Processed_CaPTk` denotes reorientation, co-registration
  and resampling, not stripping. **No skull-stripping control is needed.**
- The weaker preprocessing differences remain a stated limitation: D3C is
  co-registered, resampled and intensity-normalised by CaPTk, while D1 is not. That is a
  genuine domain difference and belongs in the limitations, but it is not skull removal.
- `src/stats/` is built and wired: Wilson intervals, patient-clustered bootstrap,
  McNemar with Holm, random-intercept logistic regression. 77 tests, cross-validated
  against statsmodels 0.14.6. Consumed by
  `src/evaluation/analyse_seed_sweep_statistics.py`. Wilson intervals are implemented
  and tested but not yet used by any analysis.
- Seed sweep: seeds 42-46 x 3 architectures under `RUN_ID=2026-08-sweep-a`, driven by
  `scripts/run_seed_sweep.py`; calibration, temperature scaling and the D3B/D3C
  evaluations across all 15 checkpoints by `scripts/run_eval_sweep.py`. Both commit
  between runs so `ensure_clean_git()` passes, and skip completed work, so both are
  resumable. Analysis on top: `src/evaluation/analyse_seed_sweep_statistics.py` (the
  consumer of `src/stats/`) and `src/evaluation/investigate_seed42_anomaly.py`.
  `D3C_PIPELINE.md` holds the full run order.

## Environment

Ubuntu 22.04, RTX 3060 12GB, venv at ./venv, PyTorch 2.11.0+cu130.
Run everything from repo root with venv activated.

## Rule implementation status

Where each rule is enforced, and what is still outstanding. Keep this current — a
stale status list is exactly the kind of misleading artefact these rules exist to
prevent.

- **Rule 1 — enforced** in the three trainers: `set_seed()` sets
  `deterministic=True` / `benchmark=False` / `use_deterministic_algorithms(True)`,
  `seed_worker` and a seeded `Generator` are passed to every DataLoader, and
  `CUBLAS_WORKSPACE_CONFIG` is set at import time because it must precede CUDA init.
  Verified on torch 2.11.0+cu130: all three architectures give bitwise-identical
  gradients across repeated passes, and E001 trained twice at seed 42 reproduced all six
  test metrics to full float precision. **Caveat:** `checkpoint_sha256` still differs
  between such runs — that is `torch.save` serialisation, not nondeterminism. Compare
  metrics, not checkpoint bytes. See SESSION_NOTES.md "Known traps".
- **Rule 2 — enforced** in the trainers by `validate_config()`, which asserts
  `dataset_id`, `classes`, `architecture`, `optimizer` and
  `early_stopping.monitor`/`mode` against what the code implements. *Outstanding:*
  `configs/E001_*.yaml` still declares `dataset.image_column`, `label_column`,
  `split_column`, `training.loss`, the whole `evaluation:` block and five
  `outputs.save_*` flags that no code reads.
- **Rule 3 — enforced** in the trainers: a `provenance` block on `metadata.json`,
  `final_results.json` and `best_model.pt`, an authoritative `provenance.json`
  sidecar, and a `run_id` column on every CSV. `RUN_ID` is required from the
  environment. *Outstanding:* the calibration, D3B/D3C evaluation and temperature
  scaling scripts still write unstamped artefacts.
- **Rule 4 — enforced** in `src/evaluation/generate_summary_tables.py`:
  `assert_single_run_set()` runs before any table is written and aborts unless the
  three `provenance.json` files share a `run_id`, a `seed` and a `split_csv_sha256`.
  Set `SEED` to generate tables for a seed other than 42.
  `table_1_run_set_provenance` records the run set, including the per-model commits.
  *Outstanding:* `generate_summary_figures.py` and `generate_d3c_summary.py`
  aggregate across the three models without asserting.
- **Rule 5 — enforced at runtime** by `verify_split()` in each trainer, which aborts
  unless the split hashes to the value recorded in rule 5.
- **Rule 6 — note the interaction with version-controlled artefacts.** Because
  `experiments/` is now tracked (only `experiments/**/*.pt` is ignored), the first
  trainer's outputs dirty the tree and `ensure_clean_git()` will block the second.
  Commit each model's artefacts before training the next. This is why `run_id` and
  not the git commit identifies a run set.

The D3C cohort is likewise pinned: `select_d3c_upenn_gbm_series.py` is deterministic
and records the manifest sha256 in its report. The download, inspection and
conversion steps read that manifest and abort on any series it does not list.

## Repository conventions

- **Datasets:** `D1` (nickparvar Kaggle, primary internal, 4-class), `D2` (BRISC2025),
  `D3A` (UCSF-PDGM, probe only), `D3B` (ICDC-Glioma, canine cross-species OOD probe),
  `D3C` (UPENN-GBM, human glioma, primary domain-shift set).
- **Experiments:** `E001` ResNet18, `E002` EfficientNet-B0, `E003` ViT-B/16, all
  trained on the D1 leakage-aware split. Config `configs/E00X_D1_<arch>_baseline.yaml`,
  outputs `experiments/E00X_D1_<arch>_baseline/seed<N>/`, reports
  `reports/experiments/E00X_*.md`.
  File names encode the pair being acted on (`check_d1_d3c_near_overlap.py`,
  `evaluate_e002_d3c_temperature_scaled.py`).
- Scripts are standalone entry points run from the repo root; inputs and outputs are
  module-level constants at the top of the file. The three trainers are the one
  exception: they accept `--seed N`, which overrides `training.seed` and selects the
  seed-scoped output directory. Downstream scripts read `SEED` from the environment
  (default 42) to locate that directory. `src/` is not an
  importable package. Per-model variants are duplicated rather than parameterised,
  so a behavioural change usually means editing all three files identically.
- Every analysis script emits both a machine-readable artefact (JSON/CSV under
  `experiments/`) and a Markdown report under `reports/`, written by the script's
  own `write_report()`. To change a report, change the generator and re-run — never
  hand-edit a report or hand-write a metric into prose.
- Class order is `["glioma", "meningioma", "notumor", "pituitary"]` -> indices 0-3
  everywhere. Glioma is index 0; `glioma_probability` in the shift evaluations
  depends on that.
- Preprocessing: resize 224x224, grayscale->RGB, ImageNet mean/std, no augmentation
  in eval transforms.
- Gitignored: `venv/`, `data/raw/`, `data/processed/`, `models/`, `*.pt`, `results/`,
  and `experiments/*/`. Tracked: `src/`, `configs/`, `reports/`. A result that exists
  only under `experiments/` is not preserved; data and experiment artefacts must be
  regenerated locally after a fresh clone or branch switch. `.gitattributes` forces
  LF because the work has moved between Windows and Ubuntu.

## Interpretation rules

These are research claims, not style preferences.

- D3B and D3C are glioma-focused and lack D1's full four-class label set. Never
  report them as four-class external accuracy. They measure prediction distribution,
  confidence, and entropy under shift.
- D3B is canine: a cross-species OOD probe, secondary to the human D3C result.
- Independence audits (exact SHA-256 + perceptual hash) support visual distinctness
  only; they do not prove patient-level independence. Existing reports are worded
  carefully; preserve that.

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
4. Table generation MUST assert all three models share a run_id, and abort otherwise.
5. NEVER regenerate data/splits/D1_leakage_aware_split.csv. Its sha256 is
   944ce00e4be958f3688a0996f6fb928fc7717e7c2804abb8000f28976efe0d43.
6. ensure_clean_git() blocks training on a dirty tree. Commit before every run.
7. Do not modify anything under reports/experiments/runB_windows/ or the
   runA-ubuntu-preserved branch. Both are provenance evidence.

## Known context

- Run A (Ubuntu, May 2026) produced tables 2-5: temperatures 1.2328/1.1596/1.2363,
  macro-F1 0.9666/0.9680/0.9582. Run B (Windows) produced tables 7-8: temperatures
  1.2725/1.1598/1.3770, macro-F1 0.9753/-/0.9648. Same split, different checkpoints.
  All results must be regenerated from a single frozen run set.
- Run A checkpoints archived at ~/research_ARCHIVE_RUN_A/.
- D3C is 100% Processed_CaPTk (skull-stripped, atlas-registered). Known confound
  requiring a skull-stripping control on the D1 test split.
- No statistical inference exists in the repo yet. src/stats/ is to be built:
  Wilson intervals, patient-clustered bootstrap, McNemar with Holm, mixed-effects
  logistic regression.
- Single seed (42) only. 5 seeds x 3 architectures required.

## Environment

Ubuntu 22.04, RTX 3060 12GB, venv at ./venv, PyTorch 2.11.0+cu130.
Run everything from repo root with venv activated.

## Current violations of the hard rules

The rules above describe the required state. As of this writing the repo does not
meet rules 1-4; treat these as the outstanding remediation list, not as precedent
to copy.

- Rule 1: all three trainers set `cudnn.deterministic = False` and
  `cudnn.benchmark = True` (`src/training/train_e00*.py:105-106`). No
  `use_deterministic_algorithms`, no `worker_init_fn`, no seeded `Generator`.
- Rule 2: `scheduler: cosine` is declared in `configs/E002_*.yaml` (twice: under
  `training:` and as a top-level `scheduler:` block) and `configs/E003_*.yaml`,
  but no training script constructs a scheduler.
- Rule 3: `metadata.json` records git commit, device, torch/CUDA versions only.
  No run_id, split_csv_sha256, or checkpoint_sha256 anywhere in the repo.
- Rule 4: `src/evaluation/generate_summary_tables.py` has no run_id assertion.
- Rule 5 verified holding: the split file on disk matches the recorded sha256.

## Repository conventions

- **Datasets:** `D1` (nickparvar Kaggle, primary internal, 4-class), `D2` (BRISC2025),
  `D3A` (UCSF-PDGM, probe only), `D3B` (ICDC-Glioma, canine cross-species OOD probe),
  `D3C` (UPENN-GBM, human glioma, primary domain-shift set).
- **Experiments:** `E001` ResNet18, `E002` EfficientNet-B0, `E003` ViT-B/16, all
  trained on the D1 leakage-aware split. Config `configs/E00X_D1_<arch>_baseline.yaml`,
  outputs `experiments/E00X_D1_<arch>_baseline/`, reports `reports/experiments/E00X_*.md`.
  File names encode the pair being acted on (`check_d1_d3c_near_overlap.py`,
  `evaluate_e002_d3c_temperature_scaled.py`).
- Scripts are standalone, argument-free entry points run from the repo root; inputs
  and outputs are module-level constants at the top of the file. `src/` is not an
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

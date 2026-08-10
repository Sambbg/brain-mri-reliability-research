# Q1 Pre-Submission Audit — Reliability Evaluation of Brain MRI Tumour Classification Models Under Calibration and Dataset Shift

**Reviewer role:** senior biomedical engineering researcher / Q1 peer reviewer
**Materials reviewed:** `brain-mri-reliability-research-main` repository (231 files) — source code, configs, split file, dataset audit reports, all experiment reports, all result tables, manuscript drafts
**Date of audit:** 9 August 2026 
**Revised:** 10 August 2026 — finding D-2 (skull-stripping confound) retracted after measurement disproved it. Retractions are marked in place rather than deleted. See D-2.

A note on scope before anything else. This audit is based on what is *in the repository*. The `experiments/` directory is gitignored, so no checkpoints, no `final_results.json`, no `calibration_metrics.json`, and no prediction CSVs were available. Every numeric claim below was reconstructed from the committed markdown reports and CSV tables. That limitation is itself one of the findings.

---

# 1. EXECUTIVE VERDICT

The research question is legitimate, the dataset-hygiene work is genuinely above average for an MSc project, and one of your side findings is more publishable than your headline finding. But the manuscript as currently evidenced **cannot be submitted to a Q1 journal**, and not because of polish. Three defects are individually sufficient for desk rejection or a reject-with-resubmission from any competent reviewer:

1. **Your results tables come from at least two different training runs of the same configurations, and your headline comparison mixes them.** The D3B numbers and the D3C numbers were produced by different model weights. The rank-reversal finding — the intellectual centrepiece of the paper — is therefore currently a comparison between two different sets of models, not a comparison between two probes.

2. ~~**Every D3C image is a `Processed_CaPTk` derivative** — skull-stripped and atlas-registered...~~ **RETRACTED — see D-2.** This finding was wrong. D3C images retain skull, scalp and orbital anatomy; `Processed_CaPTk` denotes reorientation, co-registration and resampling, not brain extraction. Verified by measurement on 40 D3C series against 40 matched D1 images. No skull-stripping confound exists, and no control experiment is required. The 69.4% `notumor` failure mode remains unexplained and is now an open scientific question rather than a suspected artefact.

3. **You have one seed per architecture, non-deterministic training, and zero statistical testing.** Worse — and this is the part that should genuinely alarm you — your own repository contains evidence that re-running the *same* config with the *same* seed changed ResNet18's internal macro-F1 by 0.0087, which is nearly the entire spread across your three architectures (0.0098). Run-to-run noise is on the same order as the between-model effect you are interpreting.

None of these is fatal to the *project*. All three are fixable, and I estimate 4–7 weeks of work, most of it compute rather than thinking. But writing the manuscript before fixing them would be writing a manuscript you will have to retract or substantially rewrite.

I would also say this plainly: **your most defensible novel contribution is not the one you have written up.** It is buried in `reports/datasets/`. More on that in Section 3.

---

# 2. WHAT MY RESEARCH ACTUALLY CONTRIBUTES

Stripped of framing:

**What you actually did.** You took the most widely used public four-class brain MRI benchmark (Nickparvar Kaggle, 7,200 images), audited it for exact and perceptual duplicates, found substantial cross-split near-duplicate contamination in the vendor-supplied Training/Testing partition, and rebuilt a leakage-aware split by grouping near-duplicates before partitioning. You then trained three ImageNet-pretrained architectures (ResNet18, EfficientNet-B0, ViT-B/16) on that split, measured internal accuracy and post-hoc calibration (temperature scaling fitted correctly on validation only), and evaluated all three on two glioma-only shifted-domain probes: a canine collection (ICDC-Glioma, 53 patients) and a human glioblastoma collection (UPENN-GBM, 569 patients). You report that internal macro-F1 is nearly identical across the three models while the fraction of shifted-domain glioma cases recognised as glioma diverges sharply and reverses rank between the two probes.

**What that contributes, honestly:**

- **An empirical demonstration** (not a method) that architectures matched on internal benchmark performance are not matched on out-of-distribution behaviour. This is a replication of the underspecification result in a new application domain.
- **A dataset-integrity audit** of two widely circulated public brain MRI benchmarks, with concrete overlap counts.
- **A documented, scriptable evaluation protocol** with acquisition logs, hash audits, and per-stage reports.

**What it does not contribute:**

- No new method, no new architecture, no new calibration technique, no new uncertainty estimator, no new dataset released.
- No clinical insight. You cannot say anything about clinical performance from a glioma-only probe with collection-level labels.
- No causal explanation for *why* the models diverge. You observe divergence; you do not attribute it.

---

# 3. NOVELTY AUDIT

Against the categories you asked for:

| Category | Present? | Assessment |
|---|---|---|
| A. Novel scientific question | **No** | "Does internal accuracy predict OOD reliability?" was answered no by Zech et al. (2018), AlBadawy et al. (2018), Pooch et al. (2020), and definitively by D'Amour et al. (2020) on underspecification. Your rank-reversal observation *is* the underspecification result. |
| B. Novel methodology | **No** | pHash deduplication, union-find grouping, temperature scaling, macro-F1 — all standard. |
| C. Novel architecture | **No** | Three off-the-shelf torchvision models with default heads. |
| D. Novel dataset contribution | **Partial — and this is your strongest card** | See below. |
| E. Novel experimental framework | **Weak** | The framework is a sensible assembly of existing components. "We combined leakage auditing + calibration + shift probes" is an engineering integration, not a framework contribution. |
| F. Novel reliability/uncertainty analysis | **No** | ECE, NLL, Brier, entropy, max-softmax. All standard. No uncertainty method beyond temperature scaling, and temperature scaling cannot change argmax (see §7). |
| G. Novel clinical insight | **No** | Glioma-only probes with collection-level labels support no clinical claim. |
| H. Engineering implementation | **Yes** | This is the honest primary category for the work as currently framed. |

**Would a Q1 reviewer call this incremental?** Yes, and easily, on the current framing. Reviewer 3 (ML) will write: *"The central claim — that internal accuracy does not predict OOD performance — is well established. The authors evaluate three standard architectures with standard metrics and report a rank reversal across two probes without seed replication or significance testing. I do not see a contribution beyond a domain-specific replication."* That review would be correct.

## The contribution you are under-selling

In `reports/datasets/D1_D2_exact_overlap_report.md` you record:

- D1 (Nickparvar, 7,013 deduplicated images) vs D2 (BRISC2025, 5,950 images)
- **4,740 exact SHA256 overlap pairs**
- 7,290 pHash near-overlap pairs, of which **5,037 at Hamming distance 0**
- 68 cross-class near-overlap pairs

And within D1 itself:

- 187 exact duplicate rows removed from 7,200
- **1,926 cross-split near-duplicate pairs** in the vendor Training/Testing partition
- 46 cross-class near-duplicate pairs (i.e. visually near-identical images carrying *different* labels)

That is a concrete, byte-level, independently verifiable finding about two benchmarks used in a large number of published papers, including papers that use one as "external validation" for the other. It is falsifiable, it is checkable in an afternoon by any reviewer, and — unlike your rank-reversal result — it is not a replication of anything.

**Recommendation:** the two-paper split you have already been considering is correct, and I would go further: the dataset-contamination audit is the stronger paper and should probably go first. It is short, self-contained, needs no retraining, and is not blocked by any of the three critical defects in §1. The reliability paper needs another month of compute regardless.

For the reliability paper, the strongest *defensible* novelty claim is narrow and should be stated narrowly:

> *Under a leakage-controlled split of a widely used public brain MRI benchmark, three architectures matched to within [CI] on internal macro-F1 differ by up to [X] percentage points in shifted-domain glioma recognition, and their ordering is not preserved across two independent shifted probes.*

That is publishable in a good Q2 or a mid-Q1 applied journal (Diagnostics, Computers in Biology and Medicine, Scientific Reports) **if and only if** the confidence intervals and seed replication exist to fill in those brackets. Without them the sentence has no content.

---

# 4. METHODOLOGY AUDIT

## 4.1 Reconstructed pipeline

```
Kaggle D1 (7,200 JPEG)                    TCIA ICDC-Glioma (57 pt)      TCIA UPENN-GBM (614 pt)
        │                                          │                             │
   SHA256 dedup (−187)                    series selection (53)         series selection (614)
        │                                          │                             │
   pHash manifest (7,013)                  DICOM → PNG, 1–99 pct         DICOM → PNG, 1–99 pct
        │                                   5 central slices/series       5 central slices/series
   union-find grouping (d≤4)                        │                             │
   → 4,755 groups                            265 images / 53 pt          2,845 images / 569 pt
        │                                          │                        (45 patients lost)
   greedy stratified assignment                    │                             │
   → train 4,909 / val 1,053 / test 1,051          │                             │
        │                                          │                             │
   train 3 models, seed 42, 20 ep, ES(5)           │                             │
        │                                          │                             │
   ├─ internal test metrics ────────────────────── │ ─────────────────────────── │
   ├─ temperature fit on val ───────────────────── │ ─────────────────────────── │
   └─ apply T to shifted probes ─────────────── D3B eval ──────────────────── D3C eval
                                                    │                             │
                                          glioma prediction rate         glioma prediction rate
```

## 4.2 Stage-by-stage findings

**Raw data → dedup.** Sound. SHA256 audit is correct and the report is honest about what it found. **PASS.**

**Dedup → leakage grouping.** This is where the first serious methodological weakness sits.

You group images by pHash Hamming distance ≤ 4 using union-find, then split by group. The intent — avoid near-duplicate leakage — is right. The execution has two problems:

- **pHash grouping is not patient grouping, and the numbers prove it.** You produced 4,755 groups from 7,013 images, of which **3,731 are singletons**. In any real brain MRI collection, a single patient contributes on the order of 10–40 usable slices. If your grouping were capturing patients, you would see a group-size distribution centred well above 1. It does not. Your split therefore controls near-duplicate leakage but **almost certainly does not control patient-level leakage**. Adjacent slices from the same patient, 6–10mm apart, are visually distinct enough to exceed Hamming distance 4 and will be scattered across train/val/test.
- **Union-find over a non-metric similarity chains.** pHash Hamming distance is not transitive: A~B and B~C does not give A~C. Union-find merges them anyway. Your largest group is 24 images. Some of those groups are chained artefacts rather than genuine duplicate sets, which *over*-groups and slightly reduces effective sample diversity. This is the lesser of the two problems but a reviewer who reads the code will mention it.

**Consequence for claims.** Your internal macro-F1 of ~0.96–0.97 is very likely still inflated by patient-level leakage. You cannot fix this — D1 has no patient identifiers, full stop. What you *must* do is state it as a hard limitation and stop describing the split as "leakage-aware" without qualification. The accurate term is **"near-duplicate-aware"**. That single word change removes a claim you cannot defend. `src/data/create_d1_leakage_aware_split.py` already says this in its caveats section; the manuscript does not.

**Severity: HIGH.** Not fixable. Must be reframed and disclosed.

**Mixed-label groups.** 25 groups spanning 123 images contain more than one class label. `assign_groups_to_splits()` resolves this with `majority_label()` and assigns the whole group to one split, but **the individual images keep their original conflicting labels**. So you have ~123 images in your training data that are near-identical to images with different labels. That is label noise you have detected and then silently retained. At minimum, quantify it, run a sensitivity analysis excluding those 123 images, and report both. **Severity: MEDIUM.**

**Training.** Several problems.

- **`torch.backends.cudnn.deterministic = False` and `benchmark = True`** in all three training scripts. Combined with a single seed, this means your runs are not reproducible even by you. The comment in the code says "Improves reproducibility" — it does the opposite of what the flags below it do. This is not pedantry; §5 shows it materially changed your results.
- **Training protocol is not matched across architectures.** E001/E002 use lr=1e-4, batch=32; E003 uses lr=5e-5, batch=16. No learning-rate search was performed for any model. You are comparing three architectures under three different, untuned settings, and then interpreting the differences between them as properties of the architectures. A reviewer will ask whether ViT-B/16's distinctive behaviour (highest mean confidence 0.9115, lowest entropy 0.2261, lowest glioma recognition 0.2179 on D3C) reflects the architecture or reflects the fact that it was trained differently and stopped at epoch 5.
- **`scheduler: cosine` is declared in the E002 and E003 configs and is never implemented.** I grepped all three training scripts for `lr_scheduler`, `scheduler`, `StepLR`, `Cosine` — zero matches. The scripts copy the config to `config_used.yaml` as a provenance artefact, so your archived provenance record describes a training procedure that did not occur. If you release code, a reviewer will find this in minutes. **Severity: HIGH** (it is a correctness-of-record problem, not just a bug).
- **Early stopping and checkpoint selection on val macro-F1.** Correct, no test contamination. **PASS.**
- **`RandomHorizontalFlip(p=0.5)` on brain MRI.** Defensible but worth a sentence. It destroys laterality, which is clinically meaningful. Low severity; just justify it.

**Calibration.** `fit_temperature()` uses validation logits only, LBFGS, applied to test. This is textbook-correct and I have no criticism of the implementation. **PASS.** The ECE implementation (15 equal-width bins, standard formula) is also correct.

**Shifted-domain evaluation.** See §5 — this is where the two critical dataset defects live.

---

# 5. DATA & LEAKAGE AUDIT

## D-1 — CRITICAL — Results derive from multiple, non-identical training runs

This is the defect that blocks everything else, so I will lay out the evidence completely.

For E001 (ResNet18), the repository contains two mutually incompatible sets of numbers for **the same model on the same test split**:

| Source file | Test accuracy | Conf–acc gap | Temperature | Raw ECE → scaled |
|---|---|---|---|---|
| `E001_D1_calibration_results.md` | 0.9667 | 0.0169 | — | — |
| `table_2_internal_performance.csv` | 0.9667 | — | — | — |
| `table_3_internal_calibration.csv` | — | 0.0169 | **1.2328** | 0.0208 → 0.0145 |
| `E001_D1_temperature_scaling_results.md` | **0.9753** | **0.0085** | **1.2725** | 0.0149 → 0.0119 |
| `table_8_cross_dataset_comparison.csv` | **0.9753** (macro-F1) | — | — | — |
| `table_7_d3c_temperature_scaled.csv` | — | — | **1.2725** | — |

Temperature scaling does not retrain the network. Loading the same checkpoint and evaluating the same test CSV must give the same accuracy. It gave 0.9667 in one run and 0.9753 in another. **The checkpoint changed between those two runs.**

The same pattern holds for E003 (ViT-B/16): calibration report accuracy 0.9581 (matching table 2's 0.9582 macro-F1) versus temperature-scaling report accuracy 0.9648 and T=1.3770 (matching table 8's 0.9648 and table 7's 1.3770). And for E002, more subtly: table 3 records T=1.1596 with raw ECE 0.0186 and scaled 0.0152, while its own report records T=1.159784 with raw ECE 0.0189 and scaled 0.0141. All three models were re-trained.

**Now the part that actually matters for your paper.** Look at which temperatures appear in which shifted-domain table:

| | E001 | E002 | E003 |
|---|---|---|---|
| `table_5_d3b_temperature_scaled.csv` (canine) | 1.2328 | 1.1596 | 1.2363 |
| `table_7_d3c_temperature_scaled.csv` (human) | 1.2725 | 1.1598 | 1.3770 |

The D3B evaluations were run against **checkpoint set A**. The D3C evaluations were run against **checkpoint set B**. Your headline finding — that model ranking reverses between the canine probe and the human probe — is currently a comparison of *different models* on *different probes*. The rank reversal may be entirely or partly a checkpoint artefact.

I want to be precise about what I am and am not saying. I am not saying the finding is false. I am saying that **as the evidence currently stands in this repository, the finding is not supported**, and any reviewer who reconciles your tables will reach the same conclusion. Your own `manuscript_consistency_audit.md` did not catch this because it checked the manuscript against the stale tables rather than checking the tables against the artefacts.

**Fix:** freeze one commit, retrain all three architectures from scratch, and regenerate every table, figure, and report from that single run set in one pass. Delete every result artefact that predates the freeze. Nothing else in this audit can be trusted until this is done.

**Severity: CRITICAL. All experiments must be rerun.**

## D-2 — ~~CRITICAL~~ **RETRACTED** — D3C is *not* skull-stripped

> **Retraction, 10 August 2026.** This finding was wrong and is preserved rather than deleted because the retraction is part of the record. The reviewer (me) inferred brain extraction from the `Processed_CaPTk` string in `SeriesDescription` without ever inspecting an image. Visual inspection of UPENN-GBM-00331 showed intact skull, scalp and orbits; a quantitative audit over 40 D3C series against 40 matched D1 glioma images then confirmed it cohort-wide.
>
> | Metric | D3C PNG | D3C source DICOM | D1 glioma |
> |---|---|---|---|
> | Air region exactly zero (1.0 = masked) | 0.262 | 0.262 | 0.373 |
> | Corner non-zero fraction | 0.540 | 0.540 | 0.280 |
> | Outer ring brighter than brain core | 0.256 | 0.256 | 0.198 |
> | Images with masked background | 0 / 40 | 0 / 40 | 0 / 40 |
>
> Skull stripping is a masking operation and sets everything outside the brain to exactly zero. Not one D3C image has a masked background, and D3C is *less* background-suppressed than D1. Source DICOM measurements are identical to the converted PNGs, so conversion neither creates nor destroys the signal. Evidence: `src/data/audit_d3c_skull_stripping.py`, `reports/datasets/D3C_skull_stripping_audit.md`, commit `3c3f677`.
>
> **Corrected severity: not a confound. No control experiment required.** The weaker preprocessing differences — co-registration, resampling, and intensity normalisation applied to D3C but not D1 — remain, and are covered under D-7. This retraction makes the D3C result *stronger*, since the most parsimonious rival explanation for the divergence is now excluded by measurement rather than argument.

### Original finding, as written (incorrect)

From `d3c_upenn_gbm_series_selection/selected_series_one_per_patient.csv`: 614 of 614 selected series have `Processed_CaPTk` in `SeriesDescription`. The original finding asserted that CaPTk-processed structural images in UPENN-GBM are brain-extracted, and that a drop in glioma recognition therefore reflected sensitivity to a preprocessing operation rather than genuine domain shift. It proposed a skull-stripping control on the D1 test split as the highest-value experiment in this audit, plus a matched-preprocessing arm for D3B.

The premise was never verified against pixel data. It was false.

**What survives from the original finding.** The observation that all 614 series are CaPTk-processed is correct, as is the observation that of 3,680 indexed UPENN-GBM MR series, 1,073 are non-CaPTk and none of those are T1. What does not survive is the inference from "CaPTk-processed" to "skull-stripped".

## D-3 — HIGH — The primary outcome metric rests on an unverified label assumption

Your headline metric is "glioma prediction rate": the fraction of shifted-domain slices assigned to the glioma class. This treats *every* selected slice as a slice on which "glioma" is the correct answer.

You select 5 central slices per series by index position (`select_central_indices()`), not by tumour presence. In a GBM case the tumour is usually but not always visible on central axial slices — and in UPENN-GBM specifically, tumours are frequently peripheral, temporal, or superior. For a slice with no visible tumour, `notumor` is arguably the *correct* prediction, and you are scoring it as a failure.

This directly inflates the phenomenon you are reporting, and it does so unevenly across models, because models differ in how aggressively they predict `notumor`.

**This is fixable and the fix is available to you.** UPENN-GBM ships tumour segmentation labels (automated plus a manually corrected subset). Intersect your selected slices with the segmentation masks, compute tumour area per slice, and either (a) restrict the analysis to slices with tumour area above a threshold, or (b) report glioma prediction rate stratified by tumour area. Option (b) is more interesting scientifically — "recognition rate scales with lesion conspicuity" is a real finding, and it converts a weakness into a result.

For D3B (ICDC-Glioma) no segmentations are available, which is a further reason to demote D3B to a secondary probe.

**Severity: HIGH. New analysis required.**

## D-4 — HIGH — No patient-level independence in D1, and the split does not establish it

Covered in §4.2. D1 has no patient identifiers. 3,731 of 4,755 groups are singletons. Patient-level leakage between train and test is likely and unquantifiable. Internal performance figures should be presented as *benchmark* performance, never as generalisation evidence, and the word "leakage-aware" should be replaced with "near-duplicate-aware" throughout.

**Severity: HIGH. Not fixable. Must be disclosed.**

## D-5 — MEDIUM — D1 source-class confound is undocumented

The Nickparvar dataset is an aggregation of three sources (figshare/Cheng, SARTAJ, Br35H). Nothing in `reports/datasets/D1_nickparvar_kaggle.md` records per-image source provenance. If, as is widely reported, the `notumor` class derives from a different source collection than the tumour classes, then the `notumor` decision boundary may encode acquisition characteristics rather than pathology — and your D3C result, where models dump 69% of slices into `notumor`, becomes much harder to interpret.

**Action:** reconstruct source provenance from filename prefixes and image characteristics, document it in Table 1, and check whether `notumor` images are separable from tumour images by low-level statistics alone (a simple logistic regression on intensity histograms will tell you in an hour). If they are, you must say so.

**Severity: MEDIUM–HIGH depending on what you find. Investigate before writing.**

## D-6 — MEDIUM — Undocumented cohort attrition in D3C

`selected_series_one_per_patient.csv` contains 614 patients. Your conversion report and all downstream tables report 569. **45 patients (7.3%) disappeared with no documented reason.** Reviewers ask about attrition. Produce a flow diagram (CONSORT-style) with exclusion counts and reasons at every stage for all three datasets.

**Severity: MEDIUM.**

## D-7 — MEDIUM — Preprocessing pipelines are not comparable across datasets

D1 arrives as pre-processed JPEGs produced by an unknown pipeline. D3B and D3C are converted from DICOM by your own script using 1st–99th percentile intensity windowing. So the intensity normalisation applied to training data and to shift-probe data is systematically different, and you have no way to characterise D1's. Add this to the limitations, and note that with D-2 retracted this is now the *only* preprocessing confound between D1 and D3C, not a secondary one. Its severity is unchanged (MEDIUM) but its relative importance rises.

**Severity: MEDIUM.**

## D-8 — LOW — Unresolved D1–D3C near-overlap pairs

7 pHash pairs at distance ≤4 between D1 and D3C, all glioma-glioma, all involving `AX T1 MPRAGE ISOTROPIC: Processed_CaPTk` series from patients UPENN-GBM-00331 and 00281. Your own report says manual review is required. It has not been done. Do it — it is 7 image pairs — and state the outcome. Almost certainly hash collisions, but "almost certainly" is not a result.

**Severity: LOW. Must be closed before submission.**

## D-9 — Leakage forms checked and cleared

For completeness, these I looked for and did **not** find:

- Test-set exposure during model selection — **clear** (checkpoint and early stopping both keyed to validation macro-F1)
- Temperature fitted on test — **clear** (`fit_temperature` receives validation logits only; verified in all three calibration scripts)
- Normalisation statistics computed over full dataset — **clear** (fixed ImageNet statistics)
- Augmentation applied to eval transforms — **clear** (separate `eval_transform`)
- Threshold tuning on test — **clear** (argmax only, no thresholds)
- Label leakage from filenames into the model — **clear** (paths not used as features)

---

# 6. CODE AUDIT

| # | File | Function / section | Problem | Why it matters | Severity | Fix | Rerun? |
|---|---|---|---|---|---|---|---|
| 1 | all 3 `src/training/train_e00*.py` | `set_seed()` | `cudnn.deterministic = False`, `benchmark = True`, comment claims it "improves reproducibility" | Same seed does not reproduce; §5 D-1 shows this changed results materially | **CRITICAL** | Set `deterministic=True`, `benchmark=False`, add `torch.use_deterministic_algorithms(True)`, seed DataLoader workers via `worker_init_fn` and a `torch.Generator` | **YES** |
| 2 | all 3 training scripts | optimizer construction | `scheduler: cosine` in E002/E003 configs is never implemented; no `lr_scheduler` anywhere | `config_used.yaml` is archived as provenance and misdescribes training | **HIGH** | Either implement `CosineAnnealingLR` or delete the key from configs; the archived config must match executed code | **YES** if implemented |
| 3 | `src/evaluation/generate_summary_tables.py` | `main()` | Generates tables 1–5 only; tables 6–8 are produced elsewhere at a different time, from a different checkpoint state | Root cause of D-1; guarantees table drift | **CRITICAL** | One script, one entry point, regenerates *all* tables and figures in a single invocation, and writes the git hash + checkpoint SHA256 into every output | **YES** |
| 4 | `generate_summary_tables.py` | `get_metric_from_groups()` | Tries ~10 key aliases across 3 nesting patterns with silent fallthrough to `None` | Silent schema drift; a renamed key yields a blank cell or a wrong-but-plausible value rather than an error. The existence of `temperature_scaling_schema_debug.md` shows you already hit this | **HIGH** | Replace with a strict schema: one canonical key set, `KeyError` on miss. Delete the fallback chain | No |
| 5 | all training scripts | `main()` | No checkpoint hash, no dataset hash, no run ID recorded in output artefacts | Impossible to detect that a table was built from a stale checkpoint — exactly what happened | **HIGH** | Write `{run_id, git_hash, checkpoint_sha256, split_csv_sha256, timestamp}` into every JSON, and have table generation assert all three models share a run set | No |
| 6 | `src/data/create_d1_leakage_aware_split.py` | union-find over pHash | Non-transitive similarity merged transitively; O(n²) at 7,013 rows | Over-grouping; groups up to size 24 | **MEDIUM** | Report group-size distribution and a sensitivity analysis at thresholds d≤2, 4, 6 | **YES** (splits change) |
| 7 | `create_d1_leakage_aware_split.py` | `assign_groups_to_splits()` | Mixed-label groups (25 groups, 123 images) assigned by majority; member labels left conflicting | Retained label noise in training data | **MEDIUM** | Quantify, run leave-them-out sensitivity, report both | **YES** for sensitivity arm |
| 8 | `src/evaluation/evaluate_e00*_on_d3c.py` | `load_checkpoint()` | Falls through `model_state_dict` → `state_dict` → `model` → bare dict without validating which succeeded | Silently loading a wrong-shaped or partially-matching state dict is possible | **MEDIUM** | Require the canonical key; `strict=True`; log the loaded key and a parameter checksum | No |
| 9 | `evaluate_*_on_d3c.py` / `_on_d3b.py` | module constants | Checkpoint paths, batch size, image size hard-coded at module level, duplicated across 12 near-identical scripts | 12 copies drift independently; already the case between D3B and D3C variants | **MEDIUM** | Collapse to one parameterised evaluator taking `--experiment` and `--dataset` | No |
| 10 | `src/data/convert_d3c_selected_slices.py` | `select_central_indices()` | Slices chosen by index position, no tumour-presence check | Root cause of D-3 | **HIGH** | Intersect with UPENN-GBM segmentations; stratify by lesion area | **YES** (new analysis) |
| 11 | `.gitignore` | `experiments/*/`, `models/*` | No results artefacts, metrics JSONs, or checkpoints are version-controlled | Nothing in the paper is independently verifiable; forced this audit to work from markdown | **HIGH** | Commit all JSON/CSV metrics and prediction files (small); publish checkpoints to Zenodo with a DOI | No |
| 12 | entire `src/` | — | Zero unit tests, zero assertions on split disjointness, class-index mapping, or row counts | A silent index-mapping error would be invisible | **MEDIUM** | Add tests: split disjointness, `CLASS_TO_INDEX` consistency across train/calibration/eval scripts, manifest row counts, no path in >1 split | No |
| 13 | `src/training/train_e001_resnet18.py` | `run_epoch()` | Called with `optimizer=None` for test but signature does not enforce mutual exclusivity with `train_mode` | Harmless today, fragile | **LOW** | Split into `train_epoch` / `eval_epoch` | No |
| 14 | all scripts | — | Windows/POSIX path mixing in reports (`data\processed\...` vs `data/processed/...`) | Cosmetic, but signals the pipeline ran on two machines — relevant given D-1 | **COSMETIC** | Use `Path` consistently, normalise in reports | No |

**One structural observation.** `ensure_clean_git()` in the training scripts is genuinely good practice and rare at MSc level. It is undermined by the fact that the artefacts it protects are gitignored. Keep the check; fix the ignore rules.

---

# 7. EXPERIMENTAL DESIGN AUDIT

## What is currently missing

**Seed replication.** One run per architecture. No variance. This is not a nice-to-have; the effect sizes you are interpreting are of the same order as the run-to-run noise your own repository accidentally documents. Minimum: 5 seeds per architecture, reporting mean ± SD for internal macro-F1, ECE, and every shifted-domain rate.

~~**A skull-stripping control.**~~ **Withdrawn — see the D-2 retraction.** D3C is not skull-stripped, so no such control is needed. What replaces it as the highest-value experiment is the segmentation-gated D3C analysis (D-3), which is now also the most likely route to explaining the `notumor` failure mode.

**A "no-shift" negative control.** You have no arm that establishes what the glioma prediction rate looks like on data that is *not* shifted. The glioma-class recall on the D1 test split (0.9665 for ResNet18) is the natural anchor, and it belongs in the same figure as the D3B and D3C rates so the reader can see the magnitude of the drop. Currently Figure 9 / table 8 compares internal *macro-F1* against shifted *glioma rate* — two different quantities on the same axis, which is not a legitimate comparison and a reviewer will say so.

**Per-class results for E002 and E003.** The repository contains `E001_D1_resnet18_baseline_results.md` with a full confusion matrix and per-class precision/recall. There is no equivalent for E002 or E003. You cannot publish a three-architecture comparison with per-class results for one architecture.

**Any explanation of the divergence.** You observe that ViT recognises 21.8% of D3C glioma cases and ResNet18 recognises 69.4%. You do not investigate why. A reviewer will accept "we observe" for a short paper, but the paper is much stronger with even a modest attribution analysis — e.g. Grad-CAM/attention-rollout on matched D1 and D3C slices showing whether the low-recognition model attends to extracranial structure. With D-2 retracted this becomes *more* important, not less: the failure mode no longer has a candidate artefactual explanation, so attribution analysis is the main available route to explaining it. This is the one place I would endorse adding an interpretability method.

## What a skeptical reviewer will request, ranked

| Rank | Experiment | Purpose | Reviewer concern addressed | Difficulty | Scientific value | Must run? |
|---|---|---|---|---|---|---|
| 1 | Single-commit full retrain, all 3 models, all tables regenerated in one pass | Restore provenance integrity | D-1: results from mixed runs | Low (compute only) | Critical — everything depends on it | **YES** |
| 2 | 5 seeds × 3 architectures; mean ± SD on all metrics | Variance estimation | No evidence rank differences exceed noise | Medium (15 runs) | Critical | **YES** |
| 3 | ~~Skull-strip D1 test split~~ **WITHDRAWN** (D-2 retracted; D3C is not skull-stripped) | — | — | — | **NO** |
| 4 | Segmentation-gated D3C analysis (tumour-bearing slices only; stratify by lesion area) | Validate the primary outcome metric | D-3: label assumption | Medium | High | **YES** |
| 5 | Bootstrap CIs (patient-clustered) on every reported rate; McNemar on paired model predictions | Statistical support | No inference anywhere | Low | Critical | **YES** |
| 6 | ~~Matched preprocessing for D3B~~ **WITHDRAWN** (premise was D-2) | — | — | — | **NO** |
| 7 | Per-class confusion matrices, E002 and E003 | Basic completeness | Incomplete reporting | Trivial | Medium | **YES** |
| 8 | Attention/Grad-CAM comparison on matched D1 vs D3C slices | Mechanism for divergence | "You describe but do not explain" | Medium | High | Recommended |
| 9 | Split-threshold sensitivity (pHash d ≤ 2, 4, 6) | Robustness of the split itself | Arbitrary threshold | Low | Medium | Recommended |
| 10 | Source-provenance analysis of D1 `notumor` class | Rule out acquisition-based shortcut | D-5 | Low | Medium–High | Recommended |
| 11 | Simple baseline (logistic regression on ImageNet features, or small CNN from scratch) | Anchor the deep models | "No simple baseline" | Low | Medium | Recommended |
| 12 | Deep ensemble or MC-dropout on the shift probes | Test whether uncertainty methods detect the shift | "Only temperature scaling" | Medium | Medium | Optional |

I deliberately do **not** recommend: larger architectures, additional datasets beyond those listed, additional calibration methods, or additional metrics. None of those addresses a weakness identified here.

## Baselines

You have three deep models and nothing else. Missing:

- **A trivial baseline.** Majority class, or ImageNet-features + logistic regression. Its value is not that it competes — it is that it establishes how much of the 0.96 macro-F1 is attributable to the deep model versus to a benchmark that is easy. On a contaminated benchmark, a linear probe on frozen features often reaches 0.93+, and reporting that is a genuinely interesting piece of evidence for your own argument.
- **Published benchmark comparison.** Numerous papers report 0.97–0.99 on this exact Kaggle dataset using the vendor split. You should report your leakage-aware number alongside a vendor-split number **from your own models** to quantify how much of the published literature's performance is attributable to the contaminated split. That single comparison would materially strengthen the paper and costs one extra training run per model.

---

# 8. STATISTICAL AUDIT

I grepped the entire repository for `bootstrap`, `mcnemar`, `confidence interval`, `wilson`, `p-value`, `scipy.stats`, and `permutation`. **Zero matches in `src/`.** The only hit anywhere was the phrase "confidence intervals" used in `paper_ready_methods_section.md` to mean confidence *bins* in a reliability diagram — which is a different concept and, if it reaches a reviewer, will read as a misunderstanding of the term.

There is no inferential statistics in this project at all. Every reported difference is a point estimate from n=1.

### Claims currently lacking any statistical support

| Claim | Current evidence | Required |
|---|---|---|
| The three models have "near-identical" internal performance | 0.9582 / 0.9666 / 0.9680, single run each | 5+ seeds; equivalence testing or overlapping CIs. Note the spread (0.0098) is smaller than your own observed run-to-run shift for E001 (0.0087) |
| Internal ranking (EfficientNet > ResNet > ViT) | Point estimates | McNemar on paired test-set predictions, Holm-corrected across the 3 pairwise comparisons |
| Temperature scaling improves internal calibration | ECE drops in all 3 | Bootstrap CI on ΔECE; ECE is a biased, binning-sensitive estimator, so also report ECE at 10/15/20 bins and adaptive-binning ECE |
| D3C glioma rates differ across models (0.694 / 0.463 / 0.218) | Point estimates | **Patient-clustered** bootstrap CIs (5 slices per patient are not independent — this is the single most common statistical error in this literature and you will be caught by it). Then McNemar or a mixed-effects logistic model with patient random intercept |
| Rank order reverses between D3B and D3C | Point estimates from *different checkpoints* | After D-1 is fixed: seed replication, then a formal interaction test (model × probe) |
| ViT is "most confident" / "least reliable" | Mean confidence 0.9115 | CI on the mean; and note that mean confidence is dominated by the 69% of slices it assigns to `notumor` — report confidence conditioned on predicted class |

### Specific recommendations

1. **Patient-clustered bootstrap** for every D3B/D3C rate. Resample *patients*, not slices. With 569 D3C patients your CIs will be reasonably tight; with 53 D3B patients they will be wide, and that width is itself informative — it may show the D3B ordering is not distinguishable at all, which would substantially weaken the rank-reversal claim and is exactly the kind of thing you need to know before writing.
2. **Wilson score intervals** for all proportions in tables 2, 4, 6, 8. Cheap, standard, expected.
3. **McNemar's test** for paired model comparisons on the same images. Assumptions: paired binary outcomes, adequate discordant counts (use exact binomial if discordant pairs < 25). Holm correction across the pairwise family.
4. **Mixed-effects logistic regression** for D3C: `glioma_predicted ~ model + (1|patient)`, which handles the slice-within-patient clustering properly and gives you the model contrast with a valid standard error in one step. This is the analysis a statistics-literate reviewer will actually want.
5. **Report effect sizes**, not just significance. With 2,845 slices almost everything will be "significant"; the difference between 0.694 and 0.463 is meaningful, the difference between 0.9666 and 0.9680 is not.

---

# 9. Q1 REVIEWER SIMULATION

## Reviewer 1 — Methodology and Statistics

**Recommendation: REJECT (resubmission encouraged after major work)**

The manuscript addresses a worthwhile question with a sensible high-level design, and the dataset auditing is more careful than is typical. However, I cannot recommend publication in its current form for three reasons.

First, the results are not internally consistent. Table 3 reports a temperature of 1.2328 for ResNet18 with raw ECE 0.0208; the supplementary calibration report for the same model reports T = 1.2725 and raw ECE 0.0149. Test accuracy for this model appears as both 0.9667 and 0.9753. Since temperature scaling does not modify network weights, these values cannot both describe the same checkpoint. Critically, the canine-probe table uses the first set of temperatures and the human-probe table uses the second. The central claim of the paper is a rank reversal between these two probes, and it is therefore not established that the reversal reflects the probes rather than the checkpoints.

Second, there is no statistical inference of any kind. Every comparison is between point estimates from single training runs. The authors describe internal performance as "near-identical" across architectures (range 0.0098 in macro-F1) while their own reporting inconsistencies imply run-to-run variation of comparable magnitude. Additionally, the shifted-domain rates aggregate five slices per patient and are treated as independent observations; clustered inference is required.

Third, the split is described as leakage-aware but controls only perceptual near-duplicates. 3,731 of 4,755 groups are singletons, which is inconsistent with grouping having captured patient identity. As the source dataset lacks patient identifiers, patient-level independence cannot be established and should not be implied.

Required before resubmission: single-provenance regeneration of all results; ≥5 seeds per architecture with dispersion reported; patient-clustered confidence intervals and paired significance testing; terminology corrected throughout.

## Reviewer 2 — Biomedical and Clinical Significance

**Recommendation: MAJOR REVISION**

The clinical motivation is sound and, unusually, the authors are appropriately restrained in their clinical claims — the limitations and non-deployment statements are well drafted. My concerns are about whether the experiments measure what the authors believe they measure.

*[This paragraph originally raised skull-stripping as the principal concern. That premise was retracted — see D-2 — and the concern is withdrawn.]* My principal remaining concern about the human cohort is that the reported failure mode is unexplained: 69% of slices assigned to `notumor` at high confidence, with no attribution analysis offered. Preprocessing differences do remain — the D3C images are co-registered and resampled, and intensity-normalised by the authors' own pipeline while D1's preprocessing is unknown — but these are weaker than the acquisition and population shift the authors intend to study, and the authors should quantify rather than assume that.

Second, the primary outcome is the proportion of slices assigned to the glioma class, computed over five geometrically central slices per series with no verification of tumour presence. Glioblastoma is frequently not centred; `notumor` may be the correct label for a proportion of these slices. UPENN-GBM provides tumour segmentations and these should be used to gate or stratify the analysis.

Third, the canine cohort (53 patients) is not described as canine in the manuscript draft I reviewed. Cross-species evaluation is defensible as an out-of-distribution probe but must be stated in the abstract, not only in supplementary material.

Fourth, the four-class problem does not correspond to a clinical decision. Clinicians do not choose among glioma/meningioma/pituitary/no-tumour from a single axial slice. The authors should state explicitly what clinical question, if any, this task approximates.

## Reviewer 3 — Machine Learning

**Recommendation: MAJOR REVISION, leaning reject on novelty**

The finding that models matched on in-distribution metrics diverge out-of-distribution is the underspecification result of D'Amour et al. (2020), and the medical-imaging instantiation has been reported by Zech et al. (2018) and others. The authors do not cite this literature — the reference list consists entirely of placeholders — and do not position their contribution against it. As presented, this is a domain-specific replication.

The experimental setup has correctable weaknesses. The three architectures are trained under different hyperparameters (ViT at lr 5e-5, batch 16; the CNNs at 1e-4, batch 32) with no tuning for any of them, so architecture and training configuration are confounded. The configs specify a cosine schedule that is absent from the released training code. There is no non-deep baseline, so the reader cannot judge how much of the 0.96 macro-F1 requires a deep model at all — on a benchmark with the contamination levels the authors themselves document, a linear probe on frozen ImageNet features may be competitive, and that would be worth knowing.

On calibration: Tables 5 and 7 report that temperature scaling leaves the glioma prediction rate unchanged. Temperature scaling is a monotone transform and cannot alter the argmax; this is an identity, not a result, and presenting it as an empirical finding across two tables is not appropriate. The genuinely empirical content — the change in entropy and mean confidence — should be reported directly and the identity stated in one sentence in the methods.

That said, the dataset overlap audit is a real contribution. The authors document 4,740 exact SHA256 matches between the Nickparvar benchmark and BRISC2025. Given how frequently these datasets are used as independent train/test pairs, this is of direct interest to the community and is, in my view, more novel than the paper's stated contribution. I would encourage the authors to consider whether this should be foregrounded.

---

# 10. REQUIRED EXPERIMENTS

Ordered by scientific value. Items 1–7 are blocking.

| # | Experiment | Purpose | Difficulty | Blocking? |
|---|---|---|---|---|
| 1 | **Provenance freeze.** Tag a commit, retrain all 3 models from scratch, regenerate every table/figure/report in one scripted pass, write checkpoint SHA256 into every artefact, delete all prior results | Fixes D-1 | Low | **YES** |
| 2 | **5 seeds × 3 architectures** (15 runs), full metric suite per run, report mean ± SD | Variance; makes every comparison interpretable | Medium | **YES** |
| 3 | ~~Skull-stripping control~~ **WITHDRAWN** — D-2 retracted, D3C is not skull-stripped | — | **NO** |
| 4 | **Segmentation-gated D3C analysis** — intersect selected slices with UPENN-GBM masks; restrict and stratify by lesion area | Validates primary metric (D-3) | Medium | **YES** |
| 5 | **Patient-clustered bootstrap + McNemar + mixed-effects model** across all rates | Statistical support | Low | **YES** |
| 6 | **Per-class confusion matrices for E002 and E003** | Completeness | Trivial | **YES** |
| 7 | **Vendor-split vs leakage-aware-split comparison** using your own models | Quantifies benchmark contamination effect; directly supports the paper's thesis | Low | **YES** |
| 8 | ~~Skull-strip D3B~~ **WITHDRAWN** — premise was D-2 | — | **NO** |
| 9 | **Simple baseline** (frozen ImageNet features + logistic regression) | Anchors the deep models | Low | Strongly recommended |
| 10 | **D1 source-provenance analysis**, especially `notumor` | Rules out acquisition shortcut (D-5) | Low | Strongly recommended |
| 11 | **pHash threshold sensitivity** (d ≤ 2, 4, 6) | Split robustness | Low | Recommended |
| 12 | **Attention/Grad-CAM on matched D1 vs D3C slices** | Mechanism for divergence | Medium | Recommended |
| 13 | **Manual review of the 7 D1–D3C near-overlap pairs** | Closes an open item you raised yourself | Trivial | **YES** (trivial) |

---

# 11. REQUIRED CODE CHANGES

**Before any experiment is rerun:**

1. Determinism: `deterministic=True`, `benchmark=False`, `torch.use_deterministic_algorithms(True)`, seeded `worker_init_fn` and `torch.Generator` for all DataLoaders.
2. Remove `scheduler: cosine` from E002/E003 configs, or implement it. Configs and code must agree.
3. Add run-provenance stamping: `{run_id, git_hash, checkpoint_sha256, split_csv_sha256, timestamp, seed}` written into every metrics JSON.
4. Un-ignore `experiments/**/*.json`, `experiments/**/*.csv`. Keep checkpoints out of git; publish them to Zenodo.
5. Add a `--seed` CLI argument so 5 seeds do not require editing configs.

**Before any table is regenerated:**

6. Single `regenerate_all_outputs.py` producing tables 1–8 and figures 1–9 in one invocation.
7. That script must assert all three models share a `run_id` and abort loudly otherwise. This assertion alone would have prevented D-1.
8. Replace `get_metric_from_groups()` alias-chasing with a strict canonical schema that raises on missing keys.
9. Delete `temperature_scaling_schema_debug.md` and the debug function once the schema is fixed — it is a symptom, not a tool.

**Before submission:**

10. Collapse the 12 duplicated `evaluate_*_on_d3*.py` scripts into one parameterised evaluator.
11. Add the statistics module: Wilson intervals, patient-clustered bootstrap, McNemar with Holm correction, mixed-effects logistic model.
12. Add tests: split disjointness by filepath; `CLASS_TO_INDEX` identical across training/calibration/evaluation modules; manifest row counts; no filepath in more than one split.
13. `strict=True` on all `load_state_dict` calls; log a parameter checksum after loading.
14. Normalise path separators in all report output.

---

# 12. CLAIMS I MUST REMOVE OR MODIFY

| Claim as currently written | Verdict | Required change |
|---|---|---|
| "leakage-aware split" (throughout) | **Overstated** | → "near-duplicate-aware split". Add explicit statement that patient-level independence is not established and cannot be, as D1 lacks patient identifiers |
| "models achieve near-identical internal macro-F1 (~0.96–0.98)" | **Unsupported** | Requires seed replication + CIs. Also the range quoted in the README (0.96–0.98) does not match table 2 (0.9582–0.9680) |
| "confirming that internal accuracy does not predict shifted-domain reliability" (README) | **Overstated** | "confirming" from n=1 per arm, with a preprocessing confound present, is not defensible. → "consistent with"; and only after the confound is controlled |
| Rank reversal between D3B and D3C | **Not currently supported** | Blocked by D-1. Re-establish under one checkpoint set with seed replication, then state with CIs |
| "temperature scaling did not correct shifted-domain class behaviour" | **Trivially true, presented as empirical** | State once in Methods as a property of monotone scaling. Report only the entropy/confidence changes as findings. Delete the "scaled glioma prediction rate" columns from tables 5 and 7 — they are identical to the raw columns by construction and invite a reviewer to conclude you do not know why |
| "the most confident model showed the lowest human glioma recognition rate" | **No longer confounded by D-2; still needs variance** | The skull-stripping objection is withdrawn. Remaining requirement: seed replication and CIs. Also: mean confidence is dominated by `notumor` predictions; condition on predicted class |
| "external dataset probes" / "external validation" | **Imprecise** | These are single-class OOD probes with collection-level labels. Use "shifted-domain probe" consistently and never "external validation" |
| "D3B is retained as an external glioma-focused domain-shift dataset" (README) — no mention of species | **Non-disclosure** | The word "canine" appears zero times in `manuscript_draft_v1.md`. It must appear in the abstract |
| "glioma prediction rate" as a reliability measure | **Requires qualification** | Until segmentation-gated, describe as "proportion of selected central slices assigned to the glioma class", and state the tumour-presence assumption explicitly |
| "reproducible ... pipeline" | **Not currently true** | Non-deterministic training, gitignored artefacts, config/code mismatch. Fix the code, then the claim becomes true |
| "This study provides a reproducible MSc-level framework" | **Weak framing** | Never signal degree level in a journal manuscript. Delete |
| All `[REF-*-00N]` placeholders | **Blocking** | ~66 real citations needed. Must include the underspecification and OOD-generalisation literature that Reviewer 3 will expect |

One more, on tone. Your drafts are unusually good at self-limitation — the "Disallowed Experimental Use" section in `D3B_usage_decision.md` is the kind of discipline most PhD students never develop. Keep that. The problem is not that you overclaim rhetorically; it is that specific numerical claims have lost their evidentiary footing.

---

# 13. PUBLICATION READINESS SCORE

**Honest assessment: based on the evidence currently available, I would not consider this research ready for manuscript preparation.**

The blocker is not writing quality or framing. It is that the numbers in your tables cannot currently be attributed to a single set of models, and that no comparison in the manuscript carries a confidence interval. (The `Processed_CaPTk` confound asserted in the first version of this audit has been retracted — see D-2.)

| Dimension | Score | Reasoning |
|---|---|---|
| **Novelty** | **35%** | Headline finding is a replication of underspecification/OOD literature. The dataset-contamination audit (4,740 exact overlaps between two public benchmarks) is genuinely novel but is not the paper's stated contribution. Score rises to ~60% if that is foregrounded or split into its own paper |
| **Methodology** | **45%** | Correct temperature scaling, correct checkpoint selection, no test contamination, honest dataset decisions. Undermined by unmatched training protocols across architectures, config/code mismatch, non-deterministic training, and a split that does not do what it is named for |
| **Data quality** | **35%** | Auditing effort is strong and unusual. But: no patient IDs in D1; D3C is 100% derivative preprocessing; primary metric rests on an unverified tumour-presence assumption; 45 patients unaccounted for; source-class confound uninvestigated |
| **Experimental validation** | **30%** | Three architectures, two probes, calibration analysis — reasonable scope. No seed replication, no controls, no baselines, per-class results for only one of three models, no mechanism analysis |
| **Statistical validity** | **10%** | No inference of any kind. No CIs, no significance tests, no clustering correction, n=1 per arm. The 10% is for correctly choosing macro-F1 and balanced accuracy over raw accuracy |
| **Reproducibility** | **25%** | Excellent intent — `ensure_clean_git()`, git hashes, config archiving, acquisition logs, pinned `requirements.txt`. Defeated in practice by non-deterministic flags, gitignored artefacts, configs describing untrained schedules, and demonstrated table drift |
| **Scientific significance** | **40%** | The question matters and the medical-imaging community needs this kind of work. The specific evidence offered does not yet establish the specific claim |

**Overall publication readiness: 31%**

For calibration on what that number means: 31% is "the project is real, the data exist, the question is good, and the remaining work is well-defined and mostly mechanical." It is not "start over." A project at 31% with a clear 4–6 week plan is in a substantially better position than a project at 60% whose remaining 40% is conceptual.

---

# 14. PRIORITISED ACTION PLAN

## P0 — MUST FIX BEFORE ANY PAPER WRITING

| Item | Problem | Why it matters | Action | Files | New experiment? |
|---|---|---|---|---|---|
| **P0-1** | Results from ≥2 different runs; D3B and D3C use different checkpoints | Headline claim currently compares different models, not different probes | Tag commit, retrain all 3, regenerate everything in one pass, stamp checkpoint hashes, delete prior artefacts | all training + evaluation scripts, `generate_summary_tables.py` | **YES** |
| **P0-2** | Non-deterministic training | Same seed does not reproduce; already caused P0-1 | Determinism flags, seeded workers, `--seed` CLI | 3 training scripts | **YES** |
| ~~**P0-3**~~ | ~~D3C 100% CaPTk skull-stripped~~ **WITHDRAWN — D-2 retracted** | D3C retains skull and scalp; verified by measurement | No action required | — | **NO** |
| **P0-4** | No variance estimates | Effect sizes are of the same order as run-to-run noise | 5 seeds × 3 architectures, mean ± SD everywhere | training scripts, table generation | **YES** |
| **P0-5** | Zero statistical inference | Every claim is a bare point estimate | Wilson CIs, patient-clustered bootstrap, McNemar + Holm, mixed-effects logistic | new `src/stats/` | No (analysis) |
| **P0-6** | Config declares unimplemented scheduler | Archived provenance misdescribes training | Remove or implement | E002/E003 configs, training scripts | **YES** if implemented |

## P1 — MUST COMPLETE BEFORE SUBMISSION

| Item | Problem | Action | New experiment? |
|---|---|---|---|
| **P1-1** | Primary metric assumes tumour on every central slice | Segmentation-gated + lesion-area-stratified D3C analysis | **YES** |
| **P1-2** | E002/E003 have no per-class results | Generate confusion matrices and per-class precision/recall | No |
| **P1-3** | Split terminology overstates what was controlled | "near-duplicate-aware" throughout + explicit patient-independence limitation | No |
| **P1-4** | Canine species undisclosed in manuscript | State in abstract, title consideration, and Table 1 | No |
| **P1-5** | Artefacts gitignored | Commit metrics JSON/CSV; checkpoints to Zenodo with DOI | No |
| **P1-6** | 66 placeholder references | Real citation set, including underspecification and medical-imaging OOD literature | No |
| **P1-7** | 45 D3C patients unaccounted for | CONSORT-style flow diagram, all three datasets | No |
| **P1-8** | 7 D1–D3C near-overlap pairs unreviewed | Manual review, report outcome | No |
| **P1-9** | Table 8 compares macro-F1 against glioma rate on one axis | Replace with a like-for-like comparison: glioma-class recall internal vs D3B vs D3C | No |
| **P1-10** | Manuscript draft predates D3C and contradicts current tables | Full rewrite after P0 completes — do not patch | No |

## P2 — STRONGLY RECOMMENDED

- ~~**P2-1** Skull-strip D3B~~ **WITHDRAWN** — premise was D-2
- **P2-2** Simple baseline (frozen features + logistic regression)
- **P2-3** Vendor-split vs leakage-aware-split comparison using your own models — this directly quantifies the contamination effect and strengthens the thesis
- **P2-4** D1 source-provenance analysis, especially the `notumor` class
- **P2-5** pHash threshold sensitivity (d ≤ 2, 4, 6)
- **P2-6** Mixed-label group sensitivity analysis (the 123 images)
- **P2-7** Split the dataset-contamination audit into its own short paper
- **P2-8** Unit tests for split disjointness and class-index consistency

## P3 — OPTIONAL

- **P3-1** Grad-CAM / attention-rollout on matched D1 vs D3C slices
- **P3-2** Deep ensemble or MC-dropout as an uncertainty comparator
- **P3-3** Consolidate the 12 duplicated evaluation scripts
- **P3-4** Adaptive-binning ECE alongside fixed-bin ECE

---

# 15. FOUR-WEEK RESEARCH IMPROVEMENT PLAN

This assumes roughly full-time availability and a single RTX 3060. Training three models for 20 epochs on 4,909 images is a matter of hours, so seed replication is bounded by patience rather than hardware.

## Week 1 — Restore provenance and determinism

- Days 1–2: implement P0-2 (determinism), P0-6 (config/code agreement), run-provenance stamping, `--seed` CLI, un-ignore artefacts. Write `regenerate_all_outputs.py` with the run-ID assertion.
- Days 3–4: verify determinism empirically — run E001 twice with seed 42 and confirm bit-identical test predictions. **Do not proceed until this passes.** This is the check whose absence created your current problem.
- Days 5–7: launch the 15-run matrix (5 seeds × 3 architectures). While it runs, write the statistics module (Wilson, clustered bootstrap, McNemar, mixed-effects).

**Exit criterion:** two runs of the same config produce identical outputs, and 15 checkpoints exist with recorded hashes.

## Week 2 — Validate the primary outcome metric

*Revised 10 August 2026. This week originally centred on a skull-stripping control. That finding (D-2) was retracted, so the week is reallocated to the segmentation-gated analysis, which is now the highest-value remaining experiment and the most likely route to explaining the `notumor` failure mode.*

- Days 1–3: obtain UPENN-GBM tumour segmentations; intersect with the 3,050 slices of the analysis cohort; compute per-slice lesion area.
- Day 4: re-run D3C analysis gated on tumour presence, and stratified by lesion area. "Recognition rate scales with lesion conspicuity" is a real finding if it holds, and converts a metric weakness into a result.
- Days 5–6: quantify the *remaining* preprocessing differences (D-7) rather than assuming them — compare intensity distributions, resolution and registration between D1 and D3C, and report the magnitude.
- Day 7: attribution analysis (Grad-CAM / attention rollout) on matched D1 and D3C slices, now the main available route to explaining why ViT sends two-thirds of D3C to `notumor` at high confidence.

**Exit criterion:** the primary metric is computed on verified tumour-bearing slices, and you have at least a candidate explanation for the failure mode rather than only a description of it.

## Week 3 — Complete the evidence base and analyse

- Days 1–2: all statistical analyses across the 15 runs — CIs on everything, McNemar for internal comparisons, mixed-effects model for D3C, formal model × probe interaction test.
- Day 3: per-class confusion matrices for all models; vendor-split comparison runs (P2-3).
- Day 4: simple baseline (P2-2); D1 source-provenance analysis (P2-4).
- Days 5–6: regenerate all tables and figures from the frozen run set. Manual review of the 7 overlap pairs. CONSORT flow diagrams.
- Day 7: **honest reassessment.** Look at the CIs. If the rank reversal does not survive seed replication, the paper's thesis changes — and you need to know that on day 21, not day 90. A negative result here is not a failure; "architectures differ less than preprocessing does" is a publishable and arguably more useful finding.

**Exit criterion:** every number you intend to print exists with an interval attached and a single run-set provenance.

## Week 4 — Write

- Days 1–2: reference set (P1-6). Position explicitly against the underspecification and medical-imaging OOD literature — do not let a reviewer be the one to raise it.
- Days 3–5: full manuscript rewrite from the new results. Do not patch `manuscript_draft_v1.md`; it predates D3C, contradicts the current tables, and omits the canine disclosure.
- Day 6: claim audit — walk §12 of this document line by line against the new draft.
- Day 7: reproducibility package — Zenodo checkpoints, committed artefacts, environment lock, README with exact run order.

**Realistic caveat:** four weeks is achievable if nothing surprises you. Segmentation intersection is the place that historically expands. Budget six weeks and treat four as the optimistic case.

---

# 16. FINAL Q1 DECISION

## **NOT READY — ADDITIONAL EXPERIMENTS REQUIRED**

Not "major methodological changes" — the methodology is largely sound and the research question is worth asking. Not "fundamentally weak" — the contribution is real, though it is not entirely the contribution you think it is.

The decision rests on three specific, well-defined gaps:

1. **Provenance.** Your tables mix at least two training runs, and your headline comparison straddles the boundary. This is not a scientific error; it is a workflow failure. But it means that at this moment, nobody — including you — knows whether the rank-reversal finding is real. That question is answerable in about a week.

2. ~~**Confounding.**~~ **RESOLVED.** This audit originally asserted that D3C was skull-stripped and made that one of three blocking defects. It was wrong, and measurement retracted it. The rival explanation is excluded, which strengthens rather than weakens the D3C result. What replaces it as the open question is *why* the models fail as they do — the `notumor` failure mode now has no artefactual explanation on offer.

3. **Inference.** One seed, no intervals, no tests, and clustered observations treated as independent. No Q1 journal in this field will accept that in 2026, and no reviewer will need more than one paragraph to say so.

What I want to acknowledge, because it is genuinely uncommon: the dataset-auditing discipline in this project is better than what I see in most submitted manuscripts. The `ensure_clean_git()` guard, the "Disallowed Experimental Use" sections, the decision to reject D2 rather than use a convenient external set, the honest caveats already written into `create_d1_leakage_aware_split.py` — that is real methodological maturity, and it is the reason this project is four to six weeks from submittable rather than abandoned. The irony worth sitting with is that the same rigour applied to *datasets* was not applied to *result provenance*, and that is what has blocked you.

One strategic note to close on. You are sitting on 4,740 byte-identical file matches between two public benchmarks that the literature treats as independent. That finding needs no retraining, no controls, no seeds, and no confound resolution. It is complete today. Consider writing that paper while the 15-run matrix trains.

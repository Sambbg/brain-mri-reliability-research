# D3C Pipeline — UPENN-GBM Human Glioma Domain-Shift Evaluation

D3C is the primary same-species (human) glioma-focused domain-shift dataset,
added alongside the canine cross-species probe (D3B). Source: UPENN-GBM (TCIA),
630 patients, SpeciesDescription = "Homo sapiens". Role: shifted-domain
evaluation of the D1-trained models; not a full four-class external validation
set (glioma-focused only).

All commands run from the repository root inside the project virtual environment.
After any step that writes tracked files, commit before the next run:
    git add -A ; git commit -m "d3c step"

## Prerequisite — D1 manifests (needed by the overlap audit)
    python src/data/create_d1_manifest.py
    python src/data/create_d1_deduplicated_manifest.py
    python src/data/create_d1_perceptual_hash_manifest.py

## Acquisition and preparation
1.  python src/data/probe_d3c_upenn_gbm_tcia.py
        Queries TCIA. Confirms 630 patients, Homo sapiens, MR modality,
        and the SeriesDescription vocabulary. No image download.
2.  python src/data/select_d3c_upenn_gbm_series.py
        Classifies series and selects one T1 series per patient
        (post-contrast T1 preferred, otherwise pre/plain T1).
3.  python src/data/download_d3c_selected_series.py
        Downloads the selected series to data/raw/D3C_upenn_gbm.
4.  python src/data/inspect_d3c_dicom_download.py
        Validates DICOM readability and records series-level metadata.
5.  python src/data/convert_d3c_selected_slices.py
        Writes 5 central-slice PNGs per series and the slice manifest.
6.  python src/data/create_d3c_perceptual_hash_manifest.py
        Adds exact (SHA-256) and perceptual (pHash) hashes to the manifest.

## Independence audit vs D1 (contamination check)
7.  python src/data/check_d1_d3c_exact_overlap.py     # expect 0 exact pairs
8.  python src/data/check_d1_d3c_near_overlap.py       # expect ~0 near pairs

## Evaluation of the three D1-trained models on D3C
9.  python src/evaluation/evaluate_e001_on_d3c.py
10. python src/evaluation/evaluate_e002_on_d3c.py
11. python src/evaluation/evaluate_e003_on_d3c.py
12. python src/evaluation/evaluate_e001_d3c_temperature_scaled.py
13. python src/evaluation/evaluate_e002_d3c_temperature_scaled.py
14. python src/evaluation/evaluate_e003_d3c_temperature_scaled.py

## Key outputs
- data/processed/D3C_selected_slices_manifest_phash.csv    (model input manifest)
- reports/datasets/D3C_acquisition_log.md                  (species/provenance record)
- reports/datasets/D1_D3C_exact_overlap_report.md          (0 exact pairs)
- reports/datasets/D1_D3C_near_overlap_report.md           (independence result)
- experiments/E00X_*/d3c_domain_shift_metrics.json         (per-model D3C metrics)
- reports/experiments/E00X_D3C_domain_shift_results.md
- reports/experiments/E00X_D3C_temperature_scaled_results.md

## Result summary (slice-level glioma prediction rate)
- ResNet18: 69.4%   EfficientNet-B0: 46.3%   ViT-B/16: 21.8%
- Temperature scaling changes confidence but not the predicted classes.
- Independence audit: 0 exact and 7 within-class (glioma-glioma) near pairs
  out of ~20M comparisons; 0 cross-class near pairs.


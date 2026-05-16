# Results Evidence Index

## Purpose

This file maps the major claims of the research project to the exact reports and artifacts that support them.

It is intended to make the project auditable, reproducible, and easier to convert into a thesis or journal-style paper.

## Claim 1: D1 was prepared using a leakage-aware split

Supporting files:

- `data/splits/D1_leakage_aware_split.csv`
- `reports/datasets/D1_exact_duplicate_report.md`
- `data/processed/D1_manifest.csv`
- `data/processed/D1_manifest_deduplicated.csv`

Evidence summary:

D1 was checked for duplicate images using exact hashing. Duplicate-aware splitting was then used to reduce leakage risk between train, validation, and test sets.

## Claim 2: D2 was rejected as a clean external validation dataset

Supporting files:

- `reports/datasets/D1_D2_exact_overlap_report.md`
- `reports/datasets/D1_D2_near_overlap_report.md`

Evidence summary:

D2 showed substantial exact and perceptual overlap with D1. Therefore, D2 was not suitable as a clean independent external validation dataset.

## Claim 3: D3B was selected as a glioma-focused domain-shift dataset

Supporting files:

- `reports/datasets/D3B_usage_decision.md`
- `reports/datasets/D3B_sequence_selection_protocol.md`
- `reports/datasets/D3B_series_selection_report.md`
- `reports/datasets/D3B_acquisition_log.md`
- `reports/datasets/D3B_dicom_inspection_report.md`
- `reports/datasets/D3B_slice_conversion_report.md`

Evidence summary:

D3B was selected from ICDC-Glioma, with one candidate anatomical series selected per patient where possible. DICOM series were downloaded, inspected, and converted into central 2D slices using a reproducible rule.

## Claim 4: D3B is visually distinct from D1 under available hash checks

Supporting files:

- `reports/datasets/D1_D3B_exact_overlap_report.md`
- `reports/datasets/D1_D3B_near_overlap_report.md`
- `reports/datasets/D3B_perceptual_hash_report.md`

Evidence summary:

No exact SHA256 overlap and no pHash near-overlap were detected between D1 and D3B converted slices at the chosen threshold. This supports treating D3B as visually distinct from D1 for domain-shift analysis.

## Claim 5: E001 ResNet18 achieved strong internal D1 performance but unstable D3B behaviour

Supporting files:

- `experiments/E001_D1_resnet18_baseline/final_results.json`
- `reports/experiments/E001_D3B_domain_shift_results.md`
- `reports/experiments/E001_D3B_temperature_scaled_results.md`
- `reports/experiments/E001_integrated_summary.md`

Evidence summary:

E001 achieved high internal D1 test performance, but predicted glioma for only a minority of D3B slices and patients. Temperature scaling softened confidence but did not change prediction distribution.

## Claim 6: E002 EfficientNet-B0 achieved the best internal and D3B behaviour among tested models, but remained unstable

Supporting files:

- `experiments/E002_D1_efficientnet_b0_baseline/final_results.json`
- `reports/experiments/E002_D1_calibration_results.md`
- `reports/experiments/E002_D1_temperature_scaling_results.md`
- `reports/experiments/E002_D3B_domain_shift_results.md`
- `reports/experiments/E002_D3B_temperature_scaled_results.md`

Evidence summary:

E002 achieved the strongest internal D1 performance and the highest D3B glioma prediction rate among the tested models. However, it still failed to predict glioma for a majority of D3B slices.

## Claim 7: E003 ViT-B/16 did not outperform CNN baselines

Supporting files:

- `experiments/E003_D1_vit_b16_baseline/final_results.json`
- `reports/experiments/E003_D1_calibration_results.md`
- `reports/experiments/E003_D1_temperature_scaling_results.md`
- `reports/experiments/E003_D3B_domain_shift_results.md`
- `reports/experiments/E003_D3B_temperature_scaled_results.md`

Evidence summary:

E003 performed worse than E001 and E002 internally. Under D3B shift, it performed better than ResNet18 but worse than EfficientNet-B0 in glioma prediction rate.

## Claim 8: Temperature scaling improved internal calibration but did not fix D3B prediction instability

Supporting files:

- `reports/experiments/E001_D3B_temperature_scaled_results.md`
- `reports/experiments/E002_D3B_temperature_scaled_results.md`
- `reports/experiments/E003_D3B_temperature_scaled_results.md`
- `reports/experiments/E001_E002_E003_comparative_summary.md`

Evidence summary:

Temperature scaling reduced confidence and increased entropy under D3B shift, but class prediction counts and patient-majority predictions remained unchanged. Therefore, the D3B issue is not merely a calibration problem.

## Claim 9: High internal D1 accuracy is insufficient evidence of cross-dataset reliability

Supporting files:

- `reports/experiments/E001_E002_E003_comparative_summary.md`
- `reports/experiments/integrated_results_narrative.md`

Evidence summary:

Across ResNet18, EfficientNet-B0, and ViT-B/16, high internal D1 performance did not guarantee stable glioma-domain behaviour on D3B. This supports the central research argument that accuracy alone is insufficient for reliability claims.

## Key Thesis-Ready Statement

A leakage-aware, calibration-aware, cross-dataset evaluation pipeline showed that three high-performing D1-trained brain MRI tumour classifiers did not maintain stable glioma-domain prediction behaviour on visually distinct D3B images. Post-hoc temperature scaling improved confidence softness but did not correct prediction distribution under dataset shift.

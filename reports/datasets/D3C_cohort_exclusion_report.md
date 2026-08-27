# D3C Cohort Exclusion Report

Generated: 2026-08-10T02:11:33

## What This Step Does, and Does Not, Change

The selection manifest is the record of what was selected and is **not** modified by this step. It keeps its hash so the selected cohort stays independently verifiable, and the exclusion is applied downstream as a separate, auditable transformation.

- Selection manifest: `reports/datasets/d3c_upenn_gbm_series_selection/selected_series_one_per_patient.csv`
- Selection manifest sha256, unchanged: `fc6deef35438027d6b76fdc323b5a4d96538312dd2da8f4a93afb40f3488761c`
- Slice manifest in: `data/processed/D3C_selected_slices_manifest_phash.csv`
- Series geometry in: `reports/datasets/D3C_dicom_series_summary.csv`
- Analysis manifest out: `data/processed/D3C_analysis_manifest.csv`
- Analysis manifest sha256: `61178f9849f9753d05957b3376eea6993d934ed2da8e9fb29a8870e88f1219f5`
- Excluded slices out: `data/processed/D3C_excluded_slices.csv`

## Rule 1, Exclusion: Non-Axial Series

D1 is axial throughout. A coronal or sagittal D3C series is therefore a plane confound: any difference in prediction behaviour could reflect acquisition geometry rather than domain shift, and the two cannot be separated after the fact. These series are removed from the analysis cohort.

The plane is measured from the DICOM slice normal, the cross product of the two direction cosines in ImageOrientationPatient. It is not parsed from SeriesDescription.

Series excluded: 4

| PatientID | Plane | Obliquity (deg) | SeriesDescription |
|---|---|---:|---|
| UPENN-GBM-00017 | sagittal | 0.3 | T1 SAG MPRAGE : Processed_CaPTk |
| UPENN-GBM-00095 | coronal | 4.026 | COR T1 MPR: Processed_CaPTk |
| UPENN-GBM-00493 | coronal | 0.0 | COR T1 POST FS: Processed_CaPTk |
| UPENN-GBM-00537 | sagittal | 0.0 | T1 MPRAGE SAG ISO post gad: Processed_CaPTk |

## Rule 2, Flag Only: Oblique Axial Series

Axial series lying more than 10 degrees off the true axial plane are **kept** in the analysis cohort, because they are axial acquisitions, but are marked with the boolean column `oblique_gt_10deg`. A sensitivity analysis can therefore drop them by filtering that column, with no second exclusion step and no second manifest.

Series flagged: 11

| PatientID | Obliquity (deg) | SeriesDescription |
|---|---:|---|
| UPENN-GBM-00536 | 26.1 | AX T1  POST : Processed_CaPTk |
| UPENN-GBM-00570 | 15.705 | Ax T1 Post: Processed_CaPTk |
| UPENN-GBM-00544 | 15.099 | AXIAL T1 FLOW COMP POST : Processed_CaPTk |
| UPENN-GBM-00532 | 14.005 | AXIAL T1 FLOW COMP POST : Processed_CaPTk |
| UPENN-GBM-00515 | 13.441 | AX T1 POST: Processed_CaPTk |
| UPENN-GBM-00452 | 12.982 | POST AX T1  FS FSE: Processed_CaPTk |
| UPENN-GBM-00283 | 11.485 | AX T1 PRE : Processed_CaPTk |
| UPENN-GBM-00506 | 11.4 | AX T1 POST: Processed_CaPTk |
| UPENN-GBM-00010 | 11.3 | t1 axial stealth-post : Processed_CaPTk |
| UPENN-GBM-00331 | 10.6 | AX T1 MPRAGE ISOTROPIC: Processed_CaPTk |
| UPENN-GBM-00484 | 10.4 | Ax T1 Post: Processed_CaPTk |

## Resulting Counts

| Cohort | Patients | Series | Slices |
|---|---:|---:|---:|
| Selected (record, unchanged) | 614 | 614 | 3070 |
| Excluded, non-axial | 4 | 4 | 20 |
| **Analysis cohort** | **610** | **610** | **3050** |
| of which flagged oblique | 11 | 11 | 55 |
| Sensitivity cohort, oblique dropped | 599 | 599 | 2995 |

## How to Use This

- Primary analysis: use `data/processed/D3C_analysis_manifest.csv` in full.
- Plane sensitivity analysis: use the same manifest filtered to `oblique_gt_10deg == False`.
- Report both, and state the exclusion in the methods. The excluded slices remain available in `data/processed/D3C_excluded_slices.csv` so the exclusion can be audited or reversed without regenerating anything.

## Limitation

Excluding non-axial series removes a plane confound; it does not make D3C a four-class external validation set, and it does not address the skull-stripping confound, which applies to the whole cohort.

## Note (August 2026)

The reference above to a skull-stripping confound is superseded. See
`reports/datasets/D3C_skull_stripping_audit.md`: measured across 40 sampled D3C series
against 40 matched D1 images, D3C retains extracranial anatomy throughout and is less
masked than D1 on every measure. The confound was withdrawn on measurement.

The plane sensitivity analysis recommended above is implemented in
`scripts/d3c_plane_sensitivity.py`, with results in
`reports/experiments/consolidated/tables/d3c_plane_sensitivity.md`.

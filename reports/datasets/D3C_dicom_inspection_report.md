# D3C DICOM Inspection Report

## Input

- Selection manifest: `reports/datasets/d3c_upenn_gbm_series_selection/selected_series_one_per_patient.csv`
- Selected series: 614
- Raw directory: `data/raw/D3C_upenn_gbm`
- DICOM files inspected: 113133
- Non-DICOM sidecar files set aside: 614 (LICENSE)
- DICOM files with a missing or blank SeriesInstanceUID: 0
- Files successfully read as DICOM: 113133
- Read errors: 0
- Files with readable pixel arrays: 113133
- Unique series: 614
- Unique patients: 614
- Series not listed in the selection manifest: 0
- Selected series with no readable DICOM: 0

## Cohort Integrity

614 non-DICOM sidecar files (LICENSE) were identified by the absence of the DICM magic number and set aside before inspection. They are excluded from the series accounting but counted here, not dropped in silence.

The 614 series inspected match the 614 series in the selection manifest exactly. No orphan series were included.

## Cohort Composition

Acquisition plane and contrast status are read from DICOM headers, not parsed from SeriesDescription. Plane comes from the slice normal, the cross product of the two direction cosines in ImageOrientationPatient. Contrast comes from ContrastBolusAgent (0018,0010).

### Acquisition Plane, Series Level

| Plane | Series | Share |
|---|---:|---:|
| axial | 610 | 0.9935 |
| coronal | 2 | 0.0033 |
| sagittal | 2 | 0.0033 |

D1 is axial. Any non-axial series is a plane confound: a difference in predictions could reflect acquisition geometry rather than domain shift.

### Non-Axial Series, Flagged: 4

| PatientID | Plane | Obliquity (deg) | SeriesDescription |
|---|---|---:|---|
| UPENN-GBM-00095 | coronal | 4.026 | COR T1 MPR: Processed_CaPTk |
| UPENN-GBM-00493 | coronal | 0.0 | COR T1 POST FS: Processed_CaPTk |
| UPENN-GBM-00537 | sagittal | 0.0 | T1 MPRAGE SAG ISO post gad: Processed_CaPTk |
| UPENN-GBM-00017 | sagittal | 0.3 | T1 SAG MPRAGE : Processed_CaPTk |

### Oblique Axial Series, more than 10 degrees off plane: 11

| PatientID | Obliquity (deg) | SeriesDescription |
|---|---:|---|
| UPENN-GBM-00452 | 12.982 | POST AX T1  FS FSE: Processed_CaPTk |
| UPENN-GBM-00010 | 11.3 | t1 axial stealth-post : Processed_CaPTk |
| UPENN-GBM-00532 | 14.005 | AXIAL T1 FLOW COMP POST : Processed_CaPTk |
| UPENN-GBM-00283 | 11.485 | AX T1 PRE : Processed_CaPTk |
| UPENN-GBM-00544 | 15.099 | AXIAL T1 FLOW COMP POST : Processed_CaPTk |
| UPENN-GBM-00331 | 10.6 | AX T1 MPRAGE ISOTROPIC: Processed_CaPTk |
| UPENN-GBM-00484 | 10.4 | Ax T1 Post: Processed_CaPTk |
| UPENN-GBM-00536 | 26.1 | AX T1  POST : Processed_CaPTk |
| UPENN-GBM-00506 | 11.4 | AX T1 POST: Processed_CaPTk |
| UPENN-GBM-00515 | 13.441 | AX T1 POST: Processed_CaPTk |
| UPENN-GBM-00570 | 15.705 | Ax T1 Post: Processed_CaPTk |

### Series with Inconsistent Orientation Across Slices: 0

None. Every series holds a single consistent orientation.

### Contrast Status from ContrastBolusAgent

| ContrastBolusAgent | Series |
|---|---:|
| present | 601 |
| absent or empty | 13 |

| Agent value | Series |
|---|---:|
| OMNISCAN | 77 |
| 12ML MULTIHANCE | 76 |
| 13ML MULTIHANCE | 52 |
| 11ML MULTIHANCE | 24 |
| 15ML MULTIHANCE | 20 |
| 10ML MULTIHANCE | 20 |
| 9ML MULTIHANCE | 17 |
| 18ML MULTIHANCE | 15 |
| 8ML MULTIHANCE | 13 |
| 14ML MULTIHANCE | 13 |
| 16ML MULTIHANCE | 12 |
| 12ML OMNISCAN | 10 |
| 22ML MULTIHANCE | 10 |
| 20ML MULTIHANCE | 9 |
| 26ML MULTIHANCE | 9 |
| OMNISCAN 3.0 + 12.0 | 9 |
| 24ML MULTIHANCE | 9 |
| 11 ML MULTIHANCE | 8 |
| OMNI 15 ML | 6 |
| 7ML MULTIHANCE | 6 |

### Pre versus Post Contrast from Acquisition Timing

ContrastBolusAgent only records that contrast was administered during the study; scanners routinely copy it to every series in that study, including pre-contrast acquisitions, so it cannot discriminate pre from post at series level. Comparing ContrastBolusStartTime (0018,1042) with the earliest AcquisitionTime (0008,0032) in the series can: a series that began after the bolus started is post-contrast.

#### Field Coverage

| Field | Series populated | Share |
|---|---:|---:|
| ContrastBolusStartTime | 0 | 0.0000 |
| AcquisitionTime | 613 | 0.9984 |
| Both, so timing is decidable | 0 | 0.0000 |

**Timing cannot be evaluated for any series.** Neither field pair is populated anywhere in the 614 selected series, so pre versus post contrast cannot be established from headers at all. It remains inferred from SeriesDescription and must be reported as an assumption, not as a verified property of the cohort.


### Header Contrast versus Description-Based Category

The selection step infers contrast from SeriesDescription. This cross-tab checks that inference against the header.

| selection_category | Series | ContrastBolusAgent present |
|---|---:|---:|
| preferred_t1_postcontrast | 568 | 565 |
| secondary_t1 | 46 | 36 |

If ContrastBolusAgent is absent across the cohort, contrast status cannot be verified from headers at all and remains inferred from free text. Record that as a limitation rather than treating the description as confirmation.

## Modality Counts

| Modality | Count |
|---|---:|
| MR | 113133 |

## Image Dimension Counts

| Rows x Columns | Count |
|---|---:|
| 256 x 192 | 92859 |
| 512 x 384 | 9616 |
| 256 x 256 | 3716 |
| 512 x 512 | 3689 |
| 256 x 208 | 832 |
| 256 x 232 | 720 |
| 250 x 187 | 576 |
| 256 x 224 | 448 |
| 256 x 200 | 192 |
| 512 x 448 | 164 |
| 512 x 416 | 137 |
| 320 x 320 | 57 |
| 320 x 260 | 57 |
| 512 x 432 | 38 |
| 320 x 250 | 32 |

## Top Series Descriptions

| SeriesDescription | Count |
|---|---:|
| t1 axial stealth-post : Processed_CaPTk | 64731 |
| t1 axial stealth-post_TERA: Processed_CaPTk | 12672 |
| t1 axial stealth-post_T : Processed_CaPTk | 12288 |
| AX T1 3D POST STEALTH : Processed_CaPTk | 7504 |
| AX T1 MPRAGE ISOTROPIC: Processed_CaPTk | 4592 |
| AX T1 POST STEALTH: Processed_CaPTk | 1728 |
| AX T1 SE C+ : Processed_CaPTk | 1156 |
| AX T1 3D POST STEALTH_TERA: Processed_CaPTk | 1152 |
| t1_mprage_tra_p2_iso_1.0 POST : Processed_CaPTk | 928 |
| T1 MPRAGE AXIAL IPAT: Processed_CaPTk | 768 |
| AXIAL T1 MPRAGE BRAIN : Processed_CaPTk | 576 |
| AX T1 3D MPRAGE : Processed_CaPTk | 416 |
| AXIAL T1 3D MPRAGE BRAIN POST : Processed_CaPTk | 416 |
| AX T1 POST STEALTH_TERA : Processed_CaPTk | 384 |
| T1 MPRAGE AX: Processed_CaPTk | 384 |
| AX TI 3D MPRAGE : Processed_CaPTk | 384 |
| AX 3D T1 POST STEALTH : Processed_CaPTk | 384 |
| AX T1 POST: Processed_CaPTk | 281 |
| AX T1  POST : Processed_CaPTk | 256 |
| AX T1 POST STEALTH_T: Processed_CaPTk | 192 |
| AX T1 3D  MPRAGE  POST: Processed_CaPTk | 192 |
| SurgNavSys_AX T1 3D POST STEALTH - T1Post.R : Processed_CaPTk | 192 |
| AX T1 MPRAGE STEALTH POST : Processed_CaPTk | 192 |
| AXIAL T1 BRAIN 3D : Processed_CaPTk | 192 |
| AX T1 MPRAGE ISOTROPIC NEW POST : Processed_CaPTk | 192 |
| T1 MPRAGE POST: Processed_CaPTk | 176 |
| T1 MPRAGE SAG ISO post gad: Processed_CaPTk | 176 |
| T1 SAG MPRAGE : Processed_CaPTk | 160 |
| AXIAL T1 FLOW COMP POST : Processed_CaPTk | 102 |
| COR T1 MPR: Processed_CaPTk | 68 |

## Series Summary

- Series summary CSV: `reports/datasets/D3C_dicom_series_summary.csv`

| PatientID | SeriesDescription | File count | Pixel readable | Dimensions |
|---|---|---:|---:|---|
| UPENN-GBM-00349 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00342 | AX T1 POST STEALTH: Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00452 | POST AX T1  FS FSE: Processed_CaPTk | 35 | 35 | 512x512: 35 |
| UPENN-GBM-00554 | AX T1 POST STEALTH_TERA : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00177 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00346 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00266 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00600 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00167 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00137 | AX T1 3D POST STEALTH : Processed_CaPTk | 192 | 192 | 512x384: 192 |
| UPENN-GBM-00255 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00439 | AX T1 POST STEALTH_T: Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00352 | t1 axial stealth-post_T : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00134 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00629 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00268 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00528 | AX T1 3D POST STEALTH_TERA: Processed_CaPTk | 192 | 192 | 512x384: 192 |
| UPENN-GBM-00508 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00580 | AXIAL T1 FLOW COMP POST : Processed_CaPTk | 27 | 27 | 512x448: 27 |
| UPENN-GBM-00575 | T1 MPRAGE AX: Processed_CaPTk | 192 | 192 | 512x384: 192 |
| UPENN-GBM-00069 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x256: 192 |
| UPENN-GBM-00173 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00567 | t1 axial stealth-post_TERA: Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00084 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00429 | t1 axial stealth-post_T : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00572 | t1 axial stealth-post_TERA: Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00117 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00007 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00507 | AX T1 SE C+ : Processed_CaPTk | 248 | 248 | 512x512: 248 |
| UPENN-GBM-00505 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00419 | t1 axial stealth-post_T : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00373 | t1 axial stealth-post_T : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00468 | t1 axial stealth-post_TERA: Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00578 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00182 | T1 MPRAGE AXIAL IPAT: Processed_CaPTk | 192 | 192 | 512x384: 192 |
| UPENN-GBM-00443 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00082 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00494 | AX T1 POST: Processed_CaPTk | 36 | 36 | 512x416: 36 |
| UPENN-GBM-00148 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00287 | AX T1 3D POST STEALTH : Processed_CaPTk | 192 | 192 | 512x384: 192 |
| UPENN-GBM-00042 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00116 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00608 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00295 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00500 | t1_mprage_tra_p2_iso_1.0 POST : Processed_CaPTk | 176 | 176 | 256x232: 176 |
| UPENN-GBM-00055 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00112 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00543 | t1 axial stealth-post_TERA: Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00132 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00453 | t1 axial stealth-post_TERA: Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00451 | t1 axial stealth-post_TERA: Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00032 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00584 | T1 MPRAGE AX: Processed_CaPTk | 192 | 192 | 512x384: 192 |
| UPENN-GBM-00611 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00612 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00290 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00577 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00588 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |
| UPENN-GBM-00307 | AX T1 3D POST STEALTH : Processed_CaPTk | 192 | 192 | 512x384: 192 |
| UPENN-GBM-00091 | t1 axial stealth-post : Processed_CaPTk | 192 | 192 | 256x192: 192 |

## Interpretation

This inspection verifies that the selected D3C DICOM series were downloaded and can be read with pydicom. Series are enumerated from the selection manifest, not by globbing the raw directory, so only the selected cohort is inspected. No image conversion or slice selection is performed in this step. The next step is to create a reproducible D3C slice-conversion script using a fixed central-slice rule.

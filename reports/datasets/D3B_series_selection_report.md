# D3B Series Selection Report - ICDC-Glioma

## Input

- Collection: `ICDC-Glioma`
- Total series returned: 650
- Unique patients: 57

## Selection Rule

Series were classified using SeriesDescription, ProtocolName, and BodyPartExamined.

Priority order:

1. Preferred T1 post-contrast / contrast-enhanced anatomical series.
2. Secondary non-contrast T1 anatomical series.
3. Exclude localizers, DWI/ADC, T2/FLAIR/PD-only, spine/non-brain, derived, and other unsupported series.

A stricter rule was applied so that broad post-contrast terms such as `post` or `+C` do not override clear T2/FLAIR/PD evidence unless explicit T1/RAGE/MPRAGE/SPGR evidence is also present.

At most one eligible series was selected per patient.

## Classification Counts

| Category | Count |
|---|---:|
| excluded_derived | 16 |
| excluded_dwi_adc | 43 |
| excluded_localizer | 52 |
| excluded_other | 67 |
| excluded_spine_nonbrain | 30 |
| excluded_t2_flair | 206 |
| preferred_t1_postcontrast | 82 |
| secondary_t1 | 154 |

## Selected Series Summary

- Patients with selected eligible series: 53
- Selected series count: 53

## Selected Category Counts

| Category | Count |
|---|---:|
| preferred_t1_postcontrast | 28 |
| secondary_t1 | 25 |

## Example Selected Series

| PatientID | SeriesDescription | ProtocolName | ImageCount | Category |
|---|---|---|---:|---|
| GLIOMA01-i_03A6 | BRAIN/T1_TRANS | None | 19 | secondary_t1 |
| GLIOMA01-i_05CA | T1 FS TRANS +C | T1 FS TRANS +C | 32 | preferred_t1_postcontrast |
| GLIOMA01-i_0FF0 | O-Ax T1 SE S | Brain, Dual Coil/ | 20 | secondary_t1 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | MP RAGE FS +C | 256 | preferred_t1_postcontrast |
| GLIOMA01-i_1166 | FSPGR 3D | BRAIN CARDIAC COIL/8 | 164 | secondary_t1 |
| GLIOMA01-i_157E | O-Ax T1-POST GAD | 2864128/6 | 26 | preferred_t1_postcontrast |
| GLIOMA01-i_1793 | BRAIN/T1_TRANS | None | 21 | secondary_t1 |
| GLIOMA01-i_22C7 | O-Ax T1 SE S | None | 18 | secondary_t1 |
| GLIOMA01-i_2C4F | RAGE FS TRANS +C | MP RAGE FS +C | 62 | preferred_t1_postcontrast |
| GLIOMA01-i_2EC9 | AX FSE T1 | BRAIN CARDIAC COIL/4 | 29 | secondary_t1 |
| GLIOMA01-i_3F8C | O-Ax T1 SE S | Brain, Head Coil/ | 20 | secondary_t1 |
| GLIOMA01-i_4990 | None | TE 20 T1  TRANS +C | 20 | preferred_t1_postcontrast |
| GLIOMA01-i_49E6 | MP RAGE TRANS FS + C | MP RAGE FS +C | 47 | preferred_t1_postcontrast |
| GLIOMA01-i_4AAB | BRAIN/T1_SAG | None | 19 | secondary_t1 |
| GLIOMA01-i_502F | T1/SAG/SE +C | T1/SAG/SE +C | 21 | preferred_t1_postcontrast |
| GLIOMA01-i_51A5 | MP RAGE FS +C | MP RAGE FS +C | 256 | preferred_t1_postcontrast |
| GLIOMA01-i_56B5 | MP RAGE FS +C | MP RAGE FS +C | 256 | preferred_t1_postcontrast |
| GLIOMA01-i_5CE5 | Ax 3DT1 SPGR S | CED Post/ | 74 | preferred_t1_postcontrast |
| GLIOMA01-i_5E9A | BRAIN/T1_TRANS | None | 25 | secondary_t1 |
| GLIOMA01-i_607E | AX FSE T1 | BRAIN ARRAY COIL/4 | 26 | secondary_t1 |
| GLIOMA01-i_6254 | RAGE FS TRANS+C | MP RAGE FS +C | 31 | preferred_t1_postcontrast |
| GLIOMA01-i_63FE | MP RAGE FS +C | MP RAGE FS +C | 256 | preferred_t1_postcontrast |
| GLIOMA01-i_6454 | RAGE FS +C TRANS | MP RAGE FS +C | 42 | preferred_t1_postcontrast |
| GLIOMA01-i_6561 | FSPGR 3D | BRAIN KNEE COIL/8 | 136 | secondary_t1 |
| GLIOMA01-i_6638 | MP RAGE TRANS + C | MP RAGE FS +C | 42 | preferred_t1_postcontrast |

## Interpretation

This report does not download images. It only identifies candidate MRI series for a future controlled DICOM acquisition. ICDC-Glioma remains a glioma-focused domain-shift candidate, not a direct four-class external validation dataset.

The selected series list should be manually reviewed before DICOM download, especially because MRI series descriptions are heterogeneous and may contain institution-specific naming conventions.

# D3B Slice Conversion Report

## Input

- Raw DICOM directory: `data/raw/D3B_icdc_glioma`
- Total files scanned: 2988
- Valid MR DICOM image files: 2935
- Skipped non-image / invalid files: 53
- Unique valid series: 53

## Conversion Rule

- Selected central slices per series: 5
- Slice order used InstanceNumber where available, then ImagePositionPatient, then SliceLocation, then filepath.
- Pixel arrays were converted to 8-bit grayscale PNG using 1st-99th percentile intensity scaling.
- LICENSE files and non-pixel objects were ignored.

## Output

- Output image directory: `data/processed/D3B_icdc_glioma_selected_slices`
- Manifest: `data/processed/D3B_selected_slices_manifest.csv`
- Output images created: 265
- Patients represented: 53
- Series represented: 53

## Label Strategy

- Assigned label: `glioma`
- Label source: collection-level ICDC-Glioma identity
- Important limitation: this is not slice-level tumour annotation.

## Image Dimension Counts

| Height x Width | Count |
|---|---:|
| 256 x 256 | 150 |
| 512 x 512 | 100 |
| 256 x 232 | 5 |
| 384 x 384 | 5 |
| 320 x 320 | 5 |

## Top Series Descriptions Among Selected Images

| SeriesDescription | Count |
|---|---:|
| BRAIN/T1_TRANS | 35 |
| FSPGR 3D | 20 |
| AX FSE T1 | 20 |
| T1/T/SE  +C | 20 |
| O-Ax T1 SE S | 20 |
| MP RAGE FS +C | 15 |
| T1 FS TRANS +C | 10 |
| Ax 3DT1 SPGR S | 10 |
|  | 10 |
| BRAIN/T1_SAG | 10 |
| t1_cor_tse post gad | 5 |
| Ax T1 +C | 5 |
| MP RAGE FS +C SUB | 5 |
| RAGE FS +C TRANS | 5 |
| RAGE FS TRANS +C | 5 |
| MP RAGE TRANS +C | 5 |
| Ax_T1_fl2d post | 5 |
| O-Sag T1 SE S | 5 |
| RAGE FS TRANS+C | 5 |
| RAGE TRANS +C | 5 |
| MP RAGE TRANS FS + C | 5 |
| BRAIN/T1_DORSAL+C | 5 |
| MP RAGE TRANS + C | 5 |
| T1+C Axial | 5 |
| O-Ax T1-POST GAD | 5 |
| T1/SAG/SE +C | 5 |
| O-Ax T1-POST | 5 |
| MP RAGE FS TRANS+C | 5 |
| T1 FLAIR FS TRANS +C | 5 |

## Series-Level Summary

| PatientID | SeriesDescription | Total valid slices | Selected slices |
|---|---|---:|---:|
| GLIOMA01-i_6561 | FSPGR 3D | 136 | 5 |
| GLIOMA01-i_C3C0 | t1_cor_tse post gad | 14 | 5 |
| GLIOMA01-i_BF76 | Ax T1 +C | 30 | 5 |
| GLIOMA01-i_1165 | MP RAGE FS +C SUB | 256 | 5 |
| GLIOMA01-i_8743 | AX FSE T1 | 28 | 5 |
| GLIOMA01-i_FECA | T1/T/SE  +C | 16 | 5 |
| GLIOMA01-i_05CA | T1 FS TRANS +C | 32 | 5 |
| GLIOMA01-i_D026 | FSPGR 3D | 164 | 5 |
| GLIOMA01-i_0FF0 | O-Ax T1 SE S | 20 | 5 |
| GLIOMA01-i_6454 | RAGE FS +C TRANS | 42 | 5 |
| GLIOMA01-i_A71E | T1/T/SE  +C | 20 | 5 |
| GLIOMA01-i_E952 | BRAIN/T1_TRANS | 19 | 5 |
| GLIOMA01-i_2C4F | RAGE FS TRANS +C | 62 | 5 |
| GLIOMA01-i_51A5 | MP RAGE FS +C | 256 | 5 |
| GLIOMA01-i_B02B | O-Ax T1 SE S | 19 | 5 |
| GLIOMA01-i_8228 | MP RAGE TRANS +C | 49 | 5 |
| GLIOMA01-i_C04D | Ax_T1_fl2d post | 30 | 5 |
| GLIOMA01-i_22C7 | O-Ax T1 SE S | 18 | 5 |
| GLIOMA01-i_92AC | O-Sag T1 SE S | 20 | 5 |
| GLIOMA01-i_6254 | RAGE FS TRANS+C | 31 | 5 |
| GLIOMA01-i_D7EC | T1/T/SE  +C | 22 | 5 |
| GLIOMA01-i_1793 | BRAIN/T1_TRANS | 21 | 5 |
| GLIOMA01-i_B3CE | RAGE TRANS +C | 40 | 5 |
| GLIOMA01-i_49E6 | MP RAGE TRANS FS + C | 47 | 5 |
| GLIOMA01-i_8BDE | T1/T/SE  +C | 16 | 5 |
| GLIOMA01-i_FC65 | BRAIN/T1_DORSAL+C | 19 | 5 |
| GLIOMA01-i_D756 | Ax 3DT1 SPGR S | 90 | 5 |
| GLIOMA01-i_2EC9 | AX FSE T1 | 29 | 5 |
| GLIOMA01-i_B70F | BRAIN/T1_TRANS | 23 | 5 |
| GLIOMA01-i_6638 | MP RAGE TRANS + C | 42 | 5 |
| GLIOMA01-i_5E9A | BRAIN/T1_TRANS | 25 | 5 |
| GLIOMA01-i_BD58 | T1+C Axial | 15 | 5 |
| GLIOMA01-i_E271 | AX FSE T1 | 25 | 5 |
| GLIOMA01-i_99AF |  | 22 | 5 |
| GLIOMA01-i_6D5C | BRAIN/T1_SAG | 19 | 5 |
| GLIOMA01-i_157E | O-Ax T1-POST GAD | 26 | 5 |
| GLIOMA01-i_4990 |  | 20 | 5 |
| GLIOMA01-i_56B5 | MP RAGE FS +C | 256 | 5 |
| GLIOMA01-i_03A6 | BRAIN/T1_TRANS | 19 | 5 |
| GLIOMA01-i_502F | T1/SAG/SE +C | 21 | 5 |
| GLIOMA01-i_3F8C | O-Ax T1 SE S | 20 | 5 |
| GLIOMA01-i_607E | AX FSE T1 | 26 | 5 |
| GLIOMA01-i_B023 | FSPGR 3D | 132 | 5 |
| GLIOMA01-i_63FE | MP RAGE FS +C | 256 | 5 |
| GLIOMA01-i_6B06 | O-Ax T1-POST | 26 | 5 |
| GLIOMA01-i_95FC | T1 FS TRANS +C | 45 | 5 |
| GLIOMA01-i_D732 | BRAIN/T1_TRANS | 24 | 5 |
| GLIOMA01-i_5CE5 | Ax 3DT1 SPGR S | 74 | 5 |
| GLIOMA01-i_4AAB | BRAIN/T1_SAG | 19 | 5 |
| GLIOMA01-i_1166 | FSPGR 3D | 164 | 5 |
| GLIOMA01-i_C561 | MP RAGE FS TRANS+C | 40 | 5 |
| GLIOMA01-i_750B | BRAIN/T1_TRANS | 19 | 5 |
| GLIOMA01-i_F5BE | T1 FLAIR FS TRANS +C | 31 | 5 |

## Interpretation

This conversion creates a reproducible 2D slice-level dataset from D3B using a fixed central-slice rule. It should be used for glioma-focused domain-shift confidence analysis, not full four-class external validation. Because selected slices are central rather than tumour-confirmed, results must be interpreted cautiously.

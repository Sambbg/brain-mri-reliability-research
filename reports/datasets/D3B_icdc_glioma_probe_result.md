# D3B Access Probe Result ? ICDC-Glioma

## Date
2026-05-12

## Dataset Candidate
D3B ? ICDC-Glioma

## Probe Method
A TCIA/NBIA metadata probe was performed using `tcia-utils`.

The probe queried:

- patients
- studies
- series

for collection:

`ICDC-Glioma`

## Result

The collection was accessible through the local `tcia-utils` / NBIA API route.

## Metadata Returned

| Item | Count |
|---|---:|
| Patients | 57 |
| Studies | 58 |
| Series | 650 |

## Modality

All returned series were MRI:

| Modality | Count |
|---|---:|
| MR | 650 |

## Observed Series Characteristics

The returned metadata showed multiple MRI sequence types, including T1, T1 post-contrast, T2, FLAIR, DWI, localizer/scout, and other acquisition types.

Examples of returned series descriptions included:

- T1+C Axial
- T1 Axial
- T2 Axial
- T2 Axial FLAIR
- MP RAGE FS +C
- T1 FLAIR TRANS
- DWI TRANS
- localizer
- BRAIN/T1_TRANS
- BRAIN/T1_TRANS+C
- BRAIN/FLAIR_TRANS

## Interpretation

ICDC-Glioma is technically accessible through the current TCIA/NBIA tooling and is therefore more feasible than UCSF-PDGM using the tested access route.

However, ICDC-Glioma is glioma-focused and does not directly match the D1 four-class task:

- glioma
- meningioma
- pituitary
- notumor

Therefore, it should not be treated as a direct four-class external validation dataset.

## Potential Use

ICDC-Glioma may be useful for:

1. Glioma-focused external domain-shift analysis.
2. Testing whether the D1-trained model assigns high glioma confidence to clinically sourced glioma MRI series.
3. Out-of-distribution or domain-shift confidence analysis.
4. Future glioma-only sub-study.

## Limitation

The dataset is DICOM/series-based rather than simple class-labelled JPEG folders. Additional preprocessing will be required, including:

1. Choosing usable MRI sequences.
2. Downloading selected series.
3. Converting DICOM slices to image format or loading DICOM directly.
4. Selecting slices fairly and reproducibly.
5. Creating a manifest.
6. Checking overlap against D1 if converted images are comparable.
7. Defining an appropriate experiment that does not falsely claim four-class external validation.

## Preliminary Decision

ICDC-Glioma is technically feasible and should remain under investigation as a D3 candidate.

It is not a direct replacement for a clean four-class external dataset.

## Next Step

Create a sequence-selection protocol before downloading any DICOM images. The protocol should define which series types are eligible, which should be excluded, and how slices will be selected.

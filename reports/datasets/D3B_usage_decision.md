# D3B Usage Decision ? ICDC-Glioma

## Decision Date
2026-05-12

## Dataset Candidate
D3B ? ICDC-Glioma

## Decision
Proceed with ICDC-Glioma as a glioma-focused external domain-shift candidate.

Do not treat ICDC-Glioma as a direct four-class external validation dataset.

## Reason

ICDC-Glioma is accessible through the current TCIA/NBIA tooling and returned usable metadata:

| Item | Count |
|---|---:|
| Patients | 57 |
| Studies | 58 |
| Series | 650 |
| Modality | MR |

A sequence-selection script identified 53 eligible patient-level series:

| Selected category | Count |
|---|---:|
| preferred_t1_postcontrast | 28 |
| secondary_t1 | 25 |
| Total selected series | 53 |

## Strengths

1. TCIA-accessible metadata.
2. Patient-level organisation.
3. MR imaging series rather than repackaged Kaggle JPEG folders.
4. Stronger provenance than D1/D2-style public image folders.
5. Suitable for external domain-shift confidence analysis.

## Limitations

1. Glioma-focused only.
2. No meningioma, pituitary, or notumor classes.
3. Not suitable for ordinary four-class accuracy reporting.
4. DICOM preprocessing is required.
5. Slice-level tumour visibility is not guaranteed.
6. Collection-level glioma labels are not equivalent to slice-level tumour annotation.

## Allowed Experimental Use

ICDC-Glioma may be used to evaluate:

1. Prediction distribution of the D1-trained four-class model on clinically sourced glioma MRI.
2. Proportion of selected slices predicted as glioma.
3. Mean glioma probability.
4. Maximum softmax confidence.
5. Entropy.
6. Raw vs temperature-scaled confidence behaviour under domain shift.

## Disallowed Experimental Use

ICDC-Glioma must not be used to claim:

1. Full four-class external validation.
2. Clinical diagnostic reliability.
3. Patient-level tumour classification accuracy without suitable labels.
4. Generalisation to meningioma, pituitary, or notumor cases.

## Next Required Step

Download only the selected 53 series, not the full 650 series.

After download:

1. Create D3B acquisition log.
2. Convert selected DICOM series into reproducible 2D images.
3. Select fixed central slices per series.
4. Create D3B image manifest.
5. Run D1-vs-D3B overlap audit where technically comparable.
6. Evaluate the D1-trained E001 model on D3B as glioma-focused domain-shift analysis.

# D3 Candidate Search Protocol

## Purpose

The purpose of D3 is to identify a stronger external dataset candidate for cross-dataset evaluation after D2/BRISC2025 was found to have massive overlap with D1.

D3 must not be selected merely because it is easy to download. It must be selected using evidence-based criteria that support publication-grade reliability evaluation.

## Background

D1 was used as the initial source dataset.

D2/BRISC2025 was initially selected as a candidate external dataset because it matched D1's four-class structure. However, D1-D2 overlap auditing showed that D2 is not independent from D1.

D1-D2 exact SHA256 overlap result:

| Item | Count |
|---|---:|
| D1 rows compared | 7,013 |
| D2 rows compared | 5,950 |
| Shared SHA256 hashes | 4,740 |
| Exact overlap pairs | 4,740 |
| Cross-class exact overlap pairs | 0 |

This means approximately 79.7% of deduplicated D2 classification images are byte-identical to D1 images.

Therefore, D3 must be selected more carefully.

## D3 Selection Goal

D3 should function as a stronger external target dataset for evaluating:

1. Cross-dataset classification performance.
2. Calibration under dataset shift.
3. Confidence degradation when moving away from the D1 source distribution.
4. Whether post-hoc calibration fitted on D1 validation data remains useful under external testing.

## Preferred Dataset Properties

A strong D3 candidate should ideally have:

1. Clear original source.
2. Patient-level or case-level metadata.
3. Minimal evidence of reuse from D1/Kaggle/Figshare image pools.
4. Public access or documented application route.
5. Brain MRI images suitable for tumour classification.
6. Class labels that can be mapped responsibly.
7. Sufficient sample size for evaluation.
8. Licensing terms that allow academic use.
9. Dataset documentation or associated paper.
10. Different provenance from D1.

## Acceptable Dataset Types

The following dataset types are acceptable candidates:

### Type A ? Patient-level clinical/open repository dataset

Examples:
- TCIA brain MRI collections
- Institutionally released research datasets
- datasets with patient/case metadata

This is the strongest option, but requires more preprocessing.

### Type B ? BraTS-derived classification subset

BraTS has stronger provenance than many Kaggle classification datasets, but it may not map directly to the D1 four-class task. It may support tumour-vs-non-tumour or tumour-grade tasks rather than D1-style glioma/meningioma/pituitary/notumor classification.

### Type C ? Three-class external tumour dataset

A three-class dataset may be usable if restricted to tumour classes only:

- glioma
- meningioma
- pituitary

This would require a separate experimental framing because the notumor class would be excluded.

### Type D ? Public Kaggle/Figshare dataset

This is lowest preference. It may still be used, but only after strict D1 overlap checking.

## Exclusion Criteria

A dataset should be rejected as D3 if:

1. It is a repackaged version of D1.
2. It has massive exact SHA256 overlap with D1.
3. It has substantial pHash near-overlap with D1.
4. It has unclear labels.
5. It has no usable documentation.
6. It cannot legally be used.
7. It is too small for meaningful evaluation.
8. It uses classes that cannot be responsibly mapped to the project task.
9. It lacks enough information to support reproducibility.

## Minimum Audit Requirements Before Use

Any D3 candidate must go through:

1. Acquisition log.
2. Manifest generation.
3. Exact duplicate audit within D3.
4. pHash near-duplicate audit within D3.
5. Exact SHA256 overlap audit against D1.
6. pHash near-overlap audit against D1.
7. Label mapping documentation.
8. Usage decision document.

## Candidate Evaluation Table

Each candidate must be evaluated using the following fields:

| Field | Notes |
|---|---|
| Candidate ID | D3A, D3B, D3C, etc. |
| Dataset name | Full dataset name |
| Source URL | Dataset or paper URL |
| Access method | Direct, Kaggle, TCIA, request, etc. |
| Classes | Original labels |
| Possible mapping | Mapping to project labels |
| Sample size | Number of images/cases |
| Patient-level metadata | Yes/No/Unknown |
| Modality | MRI type if known |
| License | Academic/commercial restrictions |
| Likely D1 overlap risk | Low/Medium/High |
| Strength | Why useful |
| Weakness | Why risky |
| Preliminary decision | Accept, reject, investigate |

## Immediate Search Priorities

Priority 1:
Find a dataset with stronger provenance than Kaggle repackages, preferably TCIA or institutionally documented.

Priority 2:
If no four-class external dataset is clean, consider a three-class tumour-only external evaluation excluding notumor.

Priority 3:
Use D2 only as an overlap-audit case, not as independent validation.

## Decision Rule

D3 is accepted only if its overlap audit shows substantially lower overlap with D1 than D2.

D2 exact overlap baseline:

- 4,740 exact overlapping images
- approximately 79.7% of D2

A D3 candidate with similar overlap must be rejected as an independent external dataset.

## Next Step

Search for D3 candidates and document at least three options before downloading the next dataset.

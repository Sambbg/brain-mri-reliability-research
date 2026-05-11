# D3 Candidate Dataset Table

## Purpose

This table tracks possible D3 external dataset candidates after D2/BRISC2025 was rejected as a clean independent external validation dataset due to massive overlap with D1.

## Candidate Table

| Candidate ID | Dataset Name | Source | Access Method | Classes | Possible Mapping | Sample Size | Patient Metadata | Modality | License | Likely D1 Overlap Risk | Strength | Weakness | Preliminary Decision |
|---|---|---|---|---|---|---:|---|---|---|---|---|---|---|
| D3A | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Investigate |
| D3B | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Investigate |
| D3C | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Investigate |

## Notes

Do not download a D3 candidate until its source, label structure, licensing, and expected overlap risk have been documented.

Any accepted candidate must undergo:

1. Manifest generation.
2. Internal exact duplicate audit.
3. Internal pHash near-duplicate audit.
4. D1-vs-D3 exact SHA256 overlap audit.
5. D1-vs-D3 pHash near-overlap audit.
6. Usage decision documentation.



# D3 Candidate Dataset Table

## Purpose

This table tracks possible D3 external dataset candidates after D2/BRISC2025 was rejected as a clean independent external validation dataset due to massive overlap with D1.

## Background

D2/BRISC2025 was rejected as the main external validation dataset because 4,740 out of 5,950 deduplicated D2 images were exact SHA256 matches with D1. This means approximately 79.7% of D2 overlapped with D1 at byte level.

Therefore, D3 candidate selection must prioritise provenance over convenience.

## Candidate Table

| Candidate ID | Dataset Name | Source | Access Method | Classes | Possible Mapping | Sample Size | Patient Metadata | Modality | License / Terms | Likely D1 Overlap Risk | Strength | Weakness | Preliminary Decision |
|---|---|---|---|---|---|---:|---|---|---|---|---|---|---|
| D3A | UCSF-PDGM | The Cancer Imaging Archive | TCIA download | Diffuse glioma cases | Not direct four-class mapping; possible glioma-focused/domain-shift evaluation | 501 subjects | Yes, subject-level dataset | Standardized 3T preoperative MRI | TCIA terms; verify before use | Low-Medium | Strong provenance, histopathologically proven diffuse gliomas, patient-level dataset | Does not include meningioma/pituitary/notumor four-class structure | Strong candidate; investigate first |
| D3B | BraTS 2024 / BraTS-type glioma dataset | Synapse / BraTS / challenge data | Synapse registration/download | Glioma-focused segmentation labels | Not direct four-class mapping; possible tumour-domain or glioma-only evaluation | Varies by BraTS task | Case-level data usually available | Multi-site multiparametric MRI | Challenge data terms; verify before use | Low-Medium | Stronger clinical provenance than Kaggle, multi-site, established benchmark | Segmentation-focused; not a direct D1 class match; access friction | Investigate if UCSF-PDGM is unsuitable |
| D3C | Figshare Cheng Brain Tumor Dataset | Figshare | Direct/Figshare download | Meningioma, glioma, pituitary | Three-class tumour-only evaluation; excludes notumor | 3,064 images from 233 patients | Yes, reported patient count | T1-weighted contrast-enhanced MRI | Figshare terms; verify exact licence | High | Classic dataset, patient count reported, easy to audit | Very likely overlap risk with D1/Kaggle-derived datasets; no notumor class | Use only as overlap-audit or tumour-only fallback |

## Current Ranking

1. D3A ? UCSF-PDGM  
2. D3B ? BraTS 2024 / BraTS-type dataset  
3. D3C ? Figshare Cheng dataset  

## Decision

Investigate D3A first because it has stronger provenance and lower expected D1 overlap risk than another Kaggle-style classification dataset.

## Next Step

Create D3A documentation for UCSF-PDGM and verify access/download method before acquiring data.

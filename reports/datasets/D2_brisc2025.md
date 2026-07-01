# Dataset Documentation ? D2 BRISC2025

## Dataset Name
BRISC2025 / BRISC Annotated Dataset for Brain Tumor Segmentation and Classification

## Dataset Role
External target candidate for cross-dataset reliability evaluation

## Source
- Kaggle dataset: `briscdataset/brisc2025`
- Kaggle URL: https://www.kaggle.com/datasets/briscdataset/brisc2025
- Figshare page: BRISC Annotated Dataset for Brain Tumor Segmentation and Classification
- Nature Scientific Data paper: BRISC: Annotated Dataset for Brain Tumor Segmentation and Classification
- Download date: TBD
- DOI: TBD after source verification

## Dataset Description
BRISC2025 is a brain MRI dataset for segmentation and classification. Current source descriptions report that it contains 6,000 contrast-enhanced T1-weighted MRI scans with four categories:

1. Glioma
2. Meningioma
3. Pituitary tumour
4. Non-tumorous / no tumour

The dataset reportedly includes expert annotation by radiologists and physicians and provides segmentation masks in addition to classification labels.

## Intended Use in This Project
D2 is intended as the first external target candidate for evaluating whether the D1-trained ResNet18 baseline remains accurate and calibrated under dataset shift.

## Why D2 Is Useful
D2 is attractive because:

1. It has the same broad four-class structure as D1.
2. It includes non-tumorous cases.
3. It is larger than many older public datasets.
4. It has stronger annotation claims than ordinary Kaggle-only collections.
5. It may support both classification and future segmentation-aware reliability analysis.

## Major Caution
D2 must not be blindly treated as fully independent from D1.

BRISC2025 was reportedly collated from multiple public datasets, and some descriptions state that it was created partly to improve/curate existing public brain MRI collections. Therefore, D2 may overlap with D1 or related public datasets.

Before D2 is used for external validation, the following checks are required:

1. Generate a D2 manifest.
2. Run exact duplicate checks within D2.
3. Run pHash near-duplicate checks within D2.
4. Run D1-vs-D2 exact hash overlap checks.
5. Run D1-vs-D2 pHash near-duplicate overlap checks.
6. Decide whether D2 can be used as external test data, or only as a curated secondary development dataset.

## Expected Classes

| Raw class name | Mapped project label | Notes |
|---|---|---|
| glioma | glioma | Confirm folder spelling after download |
| meningioma | meningioma | Confirm folder spelling after download |
| pituitary | pituitary | Confirm folder spelling after download |
| non-tumorous / no tumor / notumor | notumor | Must standardise label name |

## Expected Size

| Item | Expected value |
|---|---:|
| Total images | 6,000 |
| Classes | 4 |
| MRI type | Contrast-enhanced T1-weighted MRI |
| Masks available | Yes, reportedly |

Exact counts must be verified locally after download.

## Metadata Availability
- Patient IDs available: TBD
- Scanner/site information available: TBD
- Radiologist/physician annotation: Reported by source summaries, must verify in source paper
- Original split available: TBD
- Masks available: Reported, must verify after download

## Leakage Risk
Current leakage risk: **Medium-High**

Reasons:

1. Public dataset.
2. Collated from other public sources.
3. Possible overlap with D1 or related Kaggle/Figshare datasets.
4. Patient identifiers not yet confirmed.
5. External-test validity depends on D1-vs-D2 overlap checks.

## Preliminary Decision
Use cautiously as external target candidate.

## Final Decision
Pending after acquisition, manifest generation, duplicate checks, and D1-vs-D2 overlap audit.

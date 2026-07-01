# Dataset Selection Protocol

## Project Title
Beyond Accuracy: Calibration and Cross-Dataset Reliability in Brain MRI Tumour Classification

## Purpose
This document defines the dataset selection rules for the study before model training begins. The aim is to avoid dataset leakage, weak reproducibility, and uncontrolled post-hoc dataset choices.

## Research Question
How well do contemporary brain MRI tumour classifiers preserve calibration and predictive reliability when evaluated across independent datasets, and which calibration strategies reduce overconfidence under dataset shift?

## Dataset Inclusion Criteria
A dataset may be included if it satisfies most of the following:

1. It contains brain MRI images relevant to tumour classification.
2. It has clearly defined class labels.
3. It has a public source, DOI, Kaggle page, official challenge page, or published paper.
4. Its license or terms allow academic research use.
5. The number of images or cases is documented.
6. The dataset source can be cited.
7. The download date and version can be recorded.
8. The dataset can be stored locally without manual relabelling ambiguity.

## Dataset Exclusion Criteria
A dataset should be excluded or treated cautiously if:

1. The source is unclear.
2. The same images appear to be copied from another dataset.
3. Class labels are poorly documented.
4. There is no reliable citation or source page.
5. The license is unclear or restrictive.
6. Images are already pre-split in a way that may cause leakage.
7. Patient-level identifiers are unavailable and duplicate detection is impossible.

## Candidate Datasets

| Dataset | Source URL / DOI | Classes | Approx. Size | License | Patient IDs Available? | Role in Study | Status |
|---|---|---:|---:|---|---|---|---|
| Dataset 1 | TBD | TBD | TBD | TBD | TBD | Development source | Pending |
| Dataset 2 | TBD | TBD | TBD | TBD | TBD | External target | Pending |
| Dataset 3 | TBD | TBD | TBD | TBD | TBD | Optional external target | Pending |

## Planned Dataset Roles

### Development Source Dataset
This dataset will be used for initial training, validation, and in-domain testing.

### External Target Dataset
This dataset will not be used during model training. It will be used to measure cross-dataset generalisation and calibration under dataset shift.

### Optional Secondary Dataset
This dataset may be used later if it adds meaningful heterogeneity and does not introduce uncontrolled leakage.

## Leakage Risk Rules

Each dataset will be assessed for leakage risk before training.

### High Leakage Risk
- Single public 2D slice dataset.
- No patient-level identifiers.
- No clear source separation.
- Possible duplicate images.
- Heavy augmentation in previous papers without clear split control.

### Medium Leakage Risk
- Public dataset with reasonable documentation.
- Multiple sources or official split, but limited patient-level metadata.

### Low Leakage Risk
- Patient-level or centre-level split available.
- External validation possible.
- Source, labels, and metadata are clearly documented.

## Required Metadata Per Image

The final image manifest should contain:

- image_id
- filepath
- dataset_name
- class_label
- original_split_if_any
- patient_id_if_available
- image_width
- image_height
- file_extension
- sha256_hash
- perceptual_hash
- duplicate_group_id
- usable
- exclusion_reason

## Minimum Acceptance Standard Before Training

No model training will begin until:

1. At least one source dataset and one external target dataset are selected.
2. Dataset source links are recorded.
3. Dataset licenses are recorded.
4. A manifest file exists.
5. Duplicate detection has been run.
6. Train/validation/test splits are saved as CSV files.
7. The split-generation script is committed to Git.

## Notes
This protocol is written before model training to reduce post-hoc decision-making and improve reproducibility.

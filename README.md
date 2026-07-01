# Evaluating Calibration, Uncertainty, and Cross-Dataset Reliability in Brain MRI Tumour Classification

## Academic Project Information

**Degree Level:** Master's Research  
**University:** Universiti Teknologi Malaysia (UTM), Malaysia  
**Faculty / Department:** Department of Biomedical Engineering & Health Science  
**Supervisor:** Dr. Tan Tian Swee  

## Research Title

**Evaluating Calibration, Uncertainty, and Cross-Dataset Reliability in Brain MRI Tumour Classification**

## Abstract

Deep learning models for brain MRI tumour classification commonly report high classification accuracy on public datasets, but high accuracy alone does not establish clinical reliability. In medical imaging, a model should not only make correct predictions under familiar conditions, but should also provide well-calibrated confidence estimates and behave appropriately when exposed to data from different sources.

This research investigates the reliability of deep learning-based brain MRI tumour classification models beyond standard accuracy metrics. The study focuses on calibration, uncertainty estimation, leakage-aware dataset preparation, and cross-dataset generalisation. The primary dataset is used for internal model development and evaluation, while external dataset probes are used to assess whether model confidence remains reliable under dataset shift.

A major objective of this project is to produce a reproducible and academically defensible evaluation pipeline. This includes dataset acquisition logs, duplicate and near-duplicate audits, leakage-aware splitting, environment documentation, experiment configuration files, and structured reporting of results. The research is designed to examine whether brain MRI tumour classifiers remain trustworthy when evaluated using reliability-focused metrics rather than accuracy alone.

## Research Question

How reliable are deep learning-based brain MRI tumour classification models when evaluated beyond standard accuracy, using calibration, uncertainty, and cross-dataset validation metrics?

## Research Aim

To evaluate the reliability of brain MRI tumour classification models by analysing not only classification performance, but also calibration quality, uncertainty behaviour, leakage resistance, and robustness under dataset shift.

## Research Objectives

1. To construct a reproducible brain MRI tumour classification research pipeline.
2. To document dataset acquisition, preprocessing, deduplication, and leakage-control procedures.
3. To train and evaluate baseline deep learning models on a leakage-aware internal dataset split.
4. To assess model calibration using reliability-focused metrics such as expected calibration error and confidence-based evaluation.
5. To investigate model behaviour under cross-dataset shift using external dataset probes.
6. To determine whether high classification accuracy is sufficient evidence of model reliability in brain MRI tumour classification.

## Project Rationale

Many brain MRI tumour classification studies focus heavily on accuracy, precision, recall, and F1-score. While these metrics are useful, they do not fully answer whether a model is reliable enough for medical decision-support contexts. A model may achieve high accuracy while still being overconfident, poorly calibrated, or fragile when tested on data from a different source.

This project therefore treats reliability as a broader concept involving:

- Classification performance
- Calibration quality
- Uncertainty behaviour
- Dataset leakage control
- Cross-dataset robustness
- Reproducibility of the full research pipeline

## Current Dataset Status

### D1: Primary Internal Dataset

D1 is used as the main dataset for model development, internal validation, and internal testing. The dataset has undergone duplicate analysis, perceptual-hash analysis, and leakage-aware splitting.

D1 supports:

- Four-class brain MRI tumour classification
- Internal training, validation, and testing
- Calibration analysis
- Baseline reliability evaluation

### D3B: External Domain-Shift Probe Dataset

D3B is retained as an external glioma-focused domain-shift dataset. It is not treated as a full four-class external validation dataset because its class coverage does not match D1.

D3B supports:

- External glioma-focused confidence analysis
- Dataset-shift reliability testing
- Evaluation of model confidence behaviour under visually distinct external data

D3B does not support:

- Full four-class external validation
- Claims of complete patient-level independence
- Broad external clinical generalisation across all tumour classes

## Leakage and Overlap Control

The project includes explicit image-level leakage checks, including:

- SHA256 exact duplicate detection
- Perceptual hash near-duplicate detection
- Cross-dataset overlap audits
- Leakage-aware train, validation, and test splitting

The D1-D3B near-overlap audit compared 7,013 D1 images against 265 selected D3B slices, producing 1,858,445 pairwise comparisons. No near-overlap pairs were detected at the selected perceptual hash threshold. This supports treating D3B as visually distinct from D1 for domain-shift confidence analysis, although it does not prove patient-level independence.

## Repository Structure

```text
research/
├── configs/                 # Experiment configuration files
├── data/                    # Local data storage, excluded from GitHub and supervisor mirror where appropriate
│   ├── raw/                 # Raw datasets
│   ├── processed/           # Processed manifests and derived files
│   └── splits/              # Leakage-aware split files
├── logs/                    # Research logs and progress documentation
├── models/                  # Model weights and checkpoints, excluded from supervisor mirror
├── reports/                 # Dataset, experiment, environment, and reproducibility reports
│   ├── datasets/
│   ├── environment/
│   └── experiments/
├── scripts/                 # Utility scripts
├── src/                     # Source code
│   ├── calibration/
│   ├── data/
│   ├── evaluation/
│   ├── models/
│   ├── training/
│   └── utils/
└── README.md

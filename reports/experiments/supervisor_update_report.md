# Supervisor Update Report

## Project Title

Reliability Evaluation of Brain MRI Tumour Classification Models Under Calibration and Dataset Shift

## Degree Level

Master's research project

## Purpose of This Update

This report summarises the current progress of the project, the completed experimental work, the main findings so far, and the remaining work required before thesis or journal submission.

---

## Research Aim

The project investigates whether high-performing brain MRI tumour classification models remain reliable when evaluated beyond standard internal accuracy.

The study focuses on:

- Leakage-aware dataset preparation.
- Duplicate and public-dataset overlap auditing.
- Internal classification performance.
- Calibration and temperature scaling.
- Shifted-domain evaluation using a glioma-focused external source.
- Conservative interpretation of reliability claims.

The central research question is:

> Are high-performing brain MRI tumour classification models still reliable when assessed using calibration, confidence behaviour, and shifted-domain evaluation rather than internal accuracy alone?

---

## Completed Work

### 1. Repository and reproducibility setup

The project repository now includes:

- Reproducible experiment scripts.
- Saved configuration files.
- Generated result tables.
- Generated manuscript figures.
- Manuscript draft.
- Dataset usage documentation.
- Citation tracking files.
- Manuscript readiness audits.
- AI-use and citation-integrity protocol.

This structure was created to support traceability and reproducibility.

---

### 2. Dataset preparation and auditing

Three dataset roles were defined:

| Dataset | Role | Decision |
|---|---|---|
| D1 | Primary four-class internal dataset | Used for training, validation, and testing |
| D2 | Candidate external dataset | Rejected due to substantial overlap with D1 |
| D3B | ICDC-Glioma / TCIA-derived glioma-focused dataset | Used cautiously for shifted-domain analysis |

The rejection of D2 is an important methodological outcome. It shows that public datasets should not automatically be treated as independent external validation sources without overlap auditing.

---

### 3. Model training

Three architectures were trained and evaluated:

| Experiment | Model |
|---|---|
| E001 | ResNet18 |
| E002 | EfficientNet-B0 |
| E003 | ViT-B/16 |

All models were trained and evaluated using the same internal D1 split structure.

---

### 4. Internal D1 performance

All three models achieved strong internal test performance.

| Model | Accuracy | Balanced Accuracy | Macro-F1 |
|---|---:|---:|---:|
| ResNet18 | 0.9667 | 0.9662 | 0.9666 |
| EfficientNet-B0 | 0.9676 | 0.9677 | 0.9680 |
| ViT-B/16 | 0.9581 | 0.9578 | 0.9582 |

EfficientNet-B0 achieved the strongest internal result, but the differences between ResNet18 and EfficientNet-B0 were small.

---

### 5. Calibration and temperature scaling

Post-hoc temperature scaling improved internal calibration for all three models.

| Model | Raw ECE | Scaled ECE |
|---|---:|---:|
| ResNet18 | 0.0208 | 0.0145 |
| EfficientNet-B0 | 0.0186 | 0.0152 |
| ViT-B/16 | 0.0198 | 0.0109 |

This shows that model confidence could be softened and improved on the internal test set.

---

### 6. D3B shifted-domain evaluation

D3B was used as a glioma-focused shifted-domain dataset, not as full four-class external validation.

| Model | D3B Glioma Slice Prediction Rate | D3B Patient-Majority Glioma Rate |
|---|---:|---:|
| ResNet18 | 0.2943 | 0.2642 |
| EfficientNet-B0 | 0.4415 | 0.4717 |
| ViT-B/16 | 0.4038 | 0.3774 |

Although D3B was glioma-focused, none of the models consistently predicted glioma across the dataset.

This is the main reliability finding of the project.

---

### 7. Temperature-scaled D3B confidence behaviour

Temperature scaling reduced confidence and increased entropy on D3B, but it did not change predicted class labels.

This means calibration softened model confidence but did not fix shifted-domain class behaviour.

---

## Main Findings So Far

The project currently supports the following findings:

1. High internal D1 performance was achieved across all three architectures.
2. EfficientNet-B0 had the strongest internal macro-F1.
3. D2 was not suitable as clean external validation because of substantial overlap with D1.
4. D3B showed unstable glioma-focused shifted-domain behaviour.
5. Temperature scaling improved internal calibration.
6. Temperature scaling softened D3B confidence but did not change class predictions.
7. Internal accuracy alone is insufficient evidence of model reliability.

---

## Current Manuscript Status

The manuscript draft now includes:

- Introduction.
- Methods.
- Results.
- Discussion.
- Conclusion.
- Declarations.
- Figure and table callouts.
- Citation placeholders.
- Data/code/ethics/AI-use statements.

The manuscript also has:

- Table 1: Dataset summary and usage decision.
- Table 2: Internal model performance.
- Table 3: Internal calibration.
- Table 4: D3B shifted-domain behaviour.
- Table 5: D3B temperature-scaled behaviour.
- Figure 1: Reliability-first evaluation pipeline.
- Figure 2: Internal macro-F1 comparison.
- Figure 3: ECE before and after temperature scaling.
- Figure 4: D3B glioma prediction rates.
- Figure 5: D3B prediction distribution.
- Figure 6: D3B confidence softening.

---

## Current Readiness Level

| Output type | Readiness |
|---|---|
| MSc supervisor progress update | Ready |
| MSc thesis results chapter draft | Strong first draft |
| Journal submission | Not ready yet |
| Q1 journal submission | Not ready yet |

The project is now strong enough to present to a supervisor for methodological feedback.

It is not yet ready for journal submission because the literature needs full manual verification, reference placeholders need final formatting, and the manuscript requires journal-specific formatting and polishing.

---

## Main Limitations

1. D3B is glioma-focused and cannot support full four-class external accuracy estimation.
2. The D3B analysis uses selected central 2D slices, not full volumetric modelling.
3. Only three architectures were tested.
4. Temperature scaling was the only post-hoc calibration method tested.
5. Full uncertainty-aware methods such as ensembles or Monte Carlo dropout have not yet been implemented.
6. The current manuscript contains citation placeholders, not final formatted references.

---

## Supervisor Feedback Requested

Feedback is requested on the following points:

1. Is the research question appropriately scoped for a Master's project?
2. Is the D2 rejection due to dataset overlap methodologically acceptable and worth emphasising?
3. Is the use of D3B as a glioma-focused shifted-domain dataset acceptable, provided it is not claimed as full external validation?
4. Are the current models sufficient for the MSc thesis, or should additional architectures or uncertainty methods be added?
5. Should the thesis prioritise reliability evaluation over model development?
6. Is the current manuscript structure suitable for a thesis chapter or paper-style dissertation?
7. What target journal or thesis formatting style should be used next?

---

## Immediate Next Steps

1. Manually verify all cited references.
2. Convert citation placeholders into final reference format.
3. Export the manuscript to DOCX or PDF for supervisor review.
4. Ask supervisor for methodological feedback.
5. Decide whether additional uncertainty-aware experiments are required.
6. Choose whether the final output should be thesis-first or journal-paper-first.

---

## Summary Judgment

The project has moved beyond a simple classification experiment. It now has a defensible reliability-evaluation structure with dataset auditing, calibration analysis, shifted-domain testing, and conservative interpretation.

The strongest contribution is not that one model achieved the highest accuracy. The stronger contribution is that the project demonstrates why internal accuracy is insufficient and why leakage auditing, calibration, and shifted-domain evaluation are necessary for brain MRI tumour classification research.

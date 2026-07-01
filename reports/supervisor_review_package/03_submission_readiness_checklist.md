# Submission Readiness Checklist

## Purpose

This checklist separates the current manuscript status into two levels:

1. MSc supervisor / progress-report readiness.
2. Journal submission readiness.

The project is currently strong as an MSc research manuscript draft, but it is not yet ready for direct journal submission.

---

## Current Status Summary

The project now includes:

- Reproducible experiment scripts.
- Three trained model pipelines: ResNet18, EfficientNet-B0, and ViT-B/16.
- D1 internal evaluation.
- D2 overlap audit and rejection.
- D3B shifted-domain evaluation.
- Calibration and temperature scaling analysis.
- Generated tables.
- Generated figures.
- Manuscript draft.
- Figure and table captions.
- Citation placeholders.
- Reference tracking files.
- Citation integrity audit.
- AI use and citation integrity protocol.

Current status:

- MSc supervisor update: Ready.
- MSc thesis results chapter draft: Strong first draft.
- Journal submission: Not ready yet.
- Q1 journal submission: Not ready yet.

---

## MSc Supervisor-Ready Checklist

| Item | Status | Notes |
|---|---|---|
| Clear research question | Complete | Focuses on reliability beyond internal accuracy |
| Reproducible environment | Complete | Environment and setup documentation exist |
| Dataset usage decisions | Complete | D1 used, D2 rejected, D3B used cautiously |
| Leakage / overlap auditing | Complete | D2 overlap and D1-D3B audit documented |
| Internal model training | Complete | E001, E002, E003 complete |
| Internal performance results | Complete | Table 2 and Figure 2 |
| Calibration results | Complete | Table 3 and Figure 3 |
| D3B shifted-domain results | Complete | Table 4 and Figures 4–5 |
| D3B temperature-scaled results | Complete | Table 5 and Figure 6 |
| Pipeline figure | Complete | Figure 1 |
| Manuscript draft | Complete | Draft includes Introduction, Methods, Results, Discussion, Conclusion |
| Citation placeholders | In progress | Placeholders inserted, but final citation style not applied |
| Literature integration | In progress | Reference backbone exists |
| Supervisor explanation quality | Strong | Suitable for showing progress and methodological maturity |

Judgment:

The project is ready to show to a supervisor as a serious MSc-level research update.

---

## Journal Submission-Ready Checklist

| Item | Status | Required action |
|---|---|---|
| Final literature review | Not complete | Read and verify every cited paper fully |
| Final reference formatting | Not complete | Convert REF placeholders into target journal style |
| Target journal selected | Not complete | Choose journal before final formatting |
| Journal author guidelines checked | Not complete | Check word limits, figure limits, structure, AI policy |
| AI disclosure decision | Not complete | Follow target journal policy |
| Data availability statement | Not complete | Define what can be shared and what is restricted |
| Code availability statement | Not complete | Link GitHub repository once cleaned |
| Ethics / dataset use statement | Not complete | Clarify public dataset use and TCIA/D3B terms |
| Figure visual inspection | Not complete | Open every figure and verify readability |
| Table formatting | Not complete | Convert markdown tables to journal format |
| Abstract polish | Not complete | Needs journal-style abstract |
| Methods detail check | In progress | Needs final reproducibility pass |
| Statistical reporting check | Not complete | Ensure all metrics and sample counts are consistent |
| Limitations polish | In progress | Already conservative, but needs final journal style |
| External validation language check | In progress | Must avoid overclaiming D3B |
| Clinical claim check | In progress | Must avoid deployment or diagnostic-readiness claims |
| Supplementary material plan | Not complete | Decide what goes into supplement |
| Supervisor review | Not complete | Supervisor should review before journal targeting |
| Independent code/result check | Not complete | Ideally rerun key scripts or verify artifacts |

Judgment:

The manuscript is not journal-submission-ready yet. It needs literature verification, journal formatting, final reference conversion, and a stricter reporting pass.

---

## Critical Do-Not-Claim List

The manuscript must not claim:

1. That D3B is full four-class external validation.
2. That the models are clinically reliable.
3. That the models are ready for deployment.
4. That EfficientNet-B0 is universally superior.
5. That ViT-B/16 is generally worse than CNNs.
6. That temperature scaling solves dataset shift.
7. That calibration is equivalent to full uncertainty estimation.
8. That D2 was useless; the correct claim is that D2 was unsuitable as clean external validation because of overlap.
9. That the study proves all brain MRI classifiers are unreliable.
10. That the study is a clinical validation study.

---

## Defensible Core Claims

The manuscript can defensibly claim:

1. High internal performance was achieved on D1.
2. D2 was rejected as clean external validation due to substantial overlap with D1.
3. D3B showed unstable glioma-focused shifted-domain behaviour.
4. Temperature scaling improved internal calibration.
5. Temperature scaling softened D3B confidence but did not change class predictions.
6. Internal accuracy alone is insufficient evidence of reliability.
7. Leakage-aware auditing, calibration, and shifted-domain testing provide a more conservative evaluation framework.
8. The current study is a reproducible MSc-level reliability evaluation of brain MRI tumour classification models.

---

## Immediate Next Steps

1. Convert citation placeholders into a final reference format after selecting a target style.
2. Add a final reference list to the manuscript.
3. Create data availability, code availability, and AI-use disclosure statements.
4. Export the manuscript to DOCX or PDF for supervisor review.
5. Ask the supervisor for methodological feedback before aiming at a journal.

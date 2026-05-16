# Figures and Tables Plan

## Purpose

This document defines the figures and tables needed for the thesis/manuscript based on the current experimental evidence.

The goal is to make the results clear, defensible, and publication-ready.

## Proposed Tables

### Table 1. Dataset Summary and Usage Decision

Purpose:

Summarise D1, D2, and D3B, including their role in the study and whether each was used for performance evaluation.

Columns:

- Dataset ID
- Source / description
- Format
- Classes / label structure
- Samples used
- Role in study
- Usage decision
- Reason

Expected rows:

- D1: primary four-class internal dataset
- D2: rejected external candidate due to D1-D2 overlap
- D3B: glioma-focused domain-shift dataset

Supporting files:

- `reports/datasets/D1_exact_duplicate_report.md`
- `reports/datasets/D1_D2_exact_overlap_report.md`
- `reports/datasets/D1_D2_near_overlap_report.md`
- `reports/datasets/D3B_usage_decision.md`
- `reports/datasets/D3B_slice_conversion_report.md`

---

### Table 2. Internal D1 Test Performance Across Models

Purpose:

Compare internal D1 classification performance.

Columns:

- Model
- Accuracy
- Balanced accuracy
- Macro-F1
- Best validation macro-F1
- Best epoch

Rows:

- E001 ResNet18
- E002 EfficientNet-B0
- E003 ViT-B/16

Supporting files:

- `experiments/E001_D1_resnet18_baseline/final_results.json`
- `experiments/E002_D1_efficientnet_b0_baseline/final_results.json`
- `experiments/E003_D1_vit_b16_baseline/final_results.json`

---

### Table 3. Internal Calibration Before and After Temperature Scaling

Purpose:

Show whether temperature scaling improved internal D1 calibration.

Columns:

- Model
- Temperature
- Raw ECE
- Scaled ECE
- Raw NLL
- Scaled NLL
- Raw confidence-accuracy gap
- Scaled confidence-accuracy gap

Supporting files:

- `experiments/E001_D1_resnet18_baseline/temperature_scaling_metrics.json`
- `experiments/E002_D1_efficientnet_b0_baseline/temperature_scaling_metrics.json`
- `experiments/E003_D1_vit_b16_baseline/temperature_scaling_metrics.json`

---

### Table 4. D3B Domain-Shift Behaviour Across Models

Purpose:

Show that high internal performance did not translate into stable D3B glioma-domain behaviour.

Columns:

- Model
- Slice-level glioma prediction rate
- Patient-majority glioma rate
- Series-majority glioma rate
- Mean glioma probability
- Mean max confidence
- Mean entropy

Supporting files:

- `experiments/E001_D1_resnet18_baseline/d3b_domain_shift_metrics.json`
- `experiments/E002_D1_efficientnet_b0_baseline/d3b_domain_shift_metrics.json`
- `experiments/E003_D1_vit_b16_baseline/d3b_domain_shift_metrics.json`

---

### Table 5. D3B Raw vs Temperature-Scaled Behaviour

Purpose:

Show that temperature scaling softened confidence but did not change prediction distribution.

Columns:

- Model
- Raw glioma prediction rate
- Scaled glioma prediction rate
- Raw mean max confidence
- Scaled mean max confidence
- Raw mean entropy
- Scaled mean entropy
- Raw patient-majority glioma rate
- Scaled patient-majority glioma rate

Supporting files:

- `experiments/E001_D1_resnet18_baseline/d3b_temperature_scaled_metrics.json`
- `experiments/E002_D1_efficientnet_b0_baseline/d3b_temperature_scaled_metrics.json`
- `experiments/E003_D1_vit_b16_baseline/d3b_temperature_scaled_metrics.json`

---

## Proposed Figures

### Figure 1. Reliability-First Evaluation Pipeline

Purpose:

Show the complete workflow from D1 preparation to D3B domain-shift evaluation.

Suggested structure:

1. D1 manifest creation
2. Duplicate audit
3. Leakage-aware split
4. Model training
5. Internal testing
6. Calibration analysis
7. Temperature scaling
8. Candidate external dataset audit
9. D2 rejection
10. D3B construction
11. D3B domain-shift evaluation
12. Cross-model comparison

Type:

- Flowchart / pipeline diagram

Importance:

Very high. This should be the main methodological figure.

---

### Figure 2. Internal D1 Macro-F1 Across Models

Purpose:

Compare internal test macro-F1 for ResNet18, EfficientNet-B0, and ViT-B/16.

Type:

- Bar chart

Expected message:

EfficientNet-B0 is slightly best internally, ViT-B/16 is lowest, but all are high.

---

### Figure 3. Internal Calibration Improvement After Temperature Scaling

Purpose:

Show ECE before and after temperature scaling for each model.

Type:

- Grouped bar chart

Expected message:

Temperature scaling improves internal calibration for all models.

---

### Figure 4. D3B Glioma Prediction Rate Across Models

Purpose:

Show the central domain-shift result.

Type:

- Bar chart

Expected message:

No model predicts glioma for a majority of D3B slices.

This should be one of the strongest results figures.

---

### Figure 5. D3B Prediction Distribution Across Models

Purpose:

Show all predicted class proportions on D3B.

Type:

- Stacked bar chart

Expected message:

Models distribute D3B glioma-domain images across non-glioma classes, especially notumor/meningioma/pituitary depending on architecture.

---

### Figure 6. D3B Confidence Softening After Temperature Scaling

Purpose:

Show that temperature scaling reduces confidence but does not change predictions.

Type:

- Grouped bar chart or paired point plot

Metrics:

- Raw mean max confidence
- Scaled mean max confidence
- Raw entropy
- Scaled entropy

Expected message:

Confidence softens, entropy increases, but class distribution remains unstable.

---

### Figure 7. Dataset Overlap Audit Summary

Purpose:

Show D2 rejection and D3B acceptance.

Type:

- Small table-like figure or bar chart

Suggested values:

- D1-D2 exact overlap pairs: 4740
- D1-D2 pHash near-overlap pairs: 7290
- D1-D3B exact overlap pairs: 0
- D1-D3B pHash near-overlap pairs: 0

Expected message:

External dataset independence cannot be assumed.

---

## Priority Order

If time is limited, create these first:

1. Figure 1: Reliability-first evaluation pipeline
2. Table 2: Internal D1 model performance
3. Table 4: D3B domain-shift behaviour
4. Figure 4: D3B glioma prediction rate
5. Figure 7: Dataset overlap audit summary

## Recommended Manuscript Use

Minimum manuscript package:

- 4 tables
- 4 figures

Suggested final combination:

Tables:

1. Dataset summary and usage decision
2. Internal D1 test performance
3. Internal calibration before/after temperature scaling
4. D3B domain-shift behaviour

Figures:

1. Reliability-first evaluation pipeline
2. Internal macro-F1 comparison
3. D3B glioma prediction rate
4. D3B raw vs temperature-scaled confidence behaviour

## Warning

Do not overload the manuscript with too many figures. The strongest story is:

1. Internal performance looks strong.
2. D2 was rejected because external independence failed.
3. D3B was visually distinct.
4. All models failed stable D3B glioma-domain behaviour.
5. Temperature scaling softened confidence but did not fix prediction distribution.

# Final Manuscript Readiness Audit

## Purpose

This audit checks whether the current project has the minimum manuscript-ready components required for a structured thesis or journal-style draft.

## Current Manuscript Files

- `reports/experiments/manuscript_draft_v1.md`
- `reports/experiments/paper_ready_introduction_section.md`
- `reports/experiments/paper_ready_methods_section.md`
- `reports/experiments/paper_ready_results_section.md`
- `reports/experiments/paper_ready_discussion_section.md`
- `reports/experiments/paper_ready_abstract_conclusion.md`

Status: Present.

## Tables

- Table 1: `reports/experiments/tables/table_1_dataset_summary.md`
- Table 2: `reports/experiments/tables/table_2_internal_performance.md`
- Table 3: `reports/experiments/tables/table_3_internal_calibration.md`
- Table 4: `reports/experiments/tables/table_4_d3b_domain_shift.md`
- Table 5: `reports/experiments/tables/table_5_d3b_temperature_scaled.md`

Status: Present.

## Figures

- Figure 1: `reports/experiments/figures/figure_1_reliability_pipeline.png`
- Figure 2: `reports/experiments/figures/figure_2_internal_macro_f1.png`
- Figure 3: `reports/experiments/figures/figure_3_internal_ece_before_after.png`
- Figure 4: `reports/experiments/figures/figure_4_d3b_glioma_prediction_rate.png`
- Figure 5: `reports/experiments/figures/figure_5_d3b_prediction_distribution.png`
- Figure 6: `reports/experiments/figures/figure_6_d3b_confidence_softening.png`

Status: Present.

## Captions

- `reports/experiments/figure_captions.md`
- `reports/experiments/table_captions.md`

Status: Present.

## Evidence Indexes and Audits

- `reports/experiments/results_evidence_index.md`
- `reports/experiments/manuscript_assets_index.md`
- `reports/experiments/manuscript_consistency_audit.md`
- `reports/experiments/E001_E002_E003_comparative_summary.md`
- `reports/experiments/integrated_results_narrative.md`

Status: Present.

## Reproducibility Scripts

- `src/evaluation/generate_summary_tables.py`
- `src/evaluation/generate_summary_figures.py`
- `src/evaluation/generate_pipeline_figure.py`

Status: Present.

## Experimental Coverage

The manuscript currently covers:

1. D1 leakage-aware internal performance.
2. D2 rejection due to overlap.
3. D3B selection, conversion, and overlap auditing.
4. Three model architectures: ResNet18, EfficientNet-B0, and ViT-B/16.
5. Internal calibration and temperature scaling.
6. D3B domain-shift prediction behaviour.
7. D3B temperature-scaled confidence behaviour.
8. Cross-model comparison.

Status: Strong for current MSc-stage manuscript draft.

## Main Remaining Weaknesses

1. The manuscript still needs formal literature citations.
2. The introduction and discussion need to be connected to existing published studies.
3. The Methods section needs final polishing for journal style.
4. The figures should be visually inspected before final submission.
5. The manuscript should eventually be exported to DOCX/PDF for supervisor review.
6. External validation remains limited because D3B is glioma-focused, not full four-class.
7. The study does not yet include uncertainty-aware methods such as ensembles or MC dropout.

## Current Readiness Judgment

The project is now manuscript-structured. It is no longer only a code/results repository.

Current readiness level:

- MSc progress report: Strong.
- MSc thesis results chapter draft: Strong first draft.
- Journal submission: Not ready yet.
- Q1 journal submission: Not ready yet without deeper literature integration, stricter polishing, and possibly additional uncertainty-aware experiments.

## Next Recommended Step

The next step is to create a literature integration plan that maps the manuscript claims to real references.

Priority literature areas:

1. Brain MRI tumour classification benchmarks.
2. Dataset leakage and duplicate image risks.
3. Calibration and temperature scaling.
4. Dataset shift and external validation in medical imaging.
5. Uncertainty-aware medical image classification.

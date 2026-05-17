# Manuscript Consistency Audit

## Purpose

This audit checks whether the current manuscript draft is consistent with the generated result tables and figures.

## Manuscript File Checked

- `reports/experiments/manuscript_draft_v1.md`

## Generated Evidence Used

- `reports/experiments/tables/table_2_internal_performance.md`
- `reports/experiments/tables/table_3_internal_calibration.md`
- `reports/experiments/tables/table_4_d3b_domain_shift.md`
- `reports/experiments/tables/table_5_d3b_temperature_scaled.md`
- `reports/experiments/figures/`

## Verified Internal D1 Performance Values

The manuscript uses the following values:

- ResNet18 test macro-F1: 0.9666
- EfficientNet-B0 test macro-F1: 0.9680
- ViT-B/16 test macro-F1: 0.9582

These match Table 2.

## Verified Internal Calibration Values

The manuscript uses the following ECE changes:

- ResNet18: 0.0208 to 0.0145
- EfficientNet-B0: 0.0186 to 0.0152
- ViT-B/16: 0.0198 to 0.0109

These match Table 3.

## Verified D3B Domain-Shift Values

The manuscript uses the following D3B glioma prediction values:

- ResNet18 slice-level glioma rate: 29.43%
- ResNet18 patient-majority glioma rate: 26.42%
- EfficientNet-B0 slice-level glioma rate: 44.15%
- EfficientNet-B0 patient-majority glioma rate: 47.17%
- ViT-B/16 slice-level glioma rate: 40.38%
- ViT-B/16 patient-majority glioma rate: 37.74%

These match Table 4.

## Verified D3B Temperature-Scaled Interpretation

The manuscript states that temperature scaling softened confidence under D3B shift but did not change prediction distributions or patient-majority predictions.

This matches Table 5 and the D3B temperature-scaled reports.

## Verified Figure and Table Callouts

The manuscript now includes callouts to:

- Table 2 and Figure 2 for internal D1 model performance.
- Table 3 and Figure 3 for internal calibration.
- Table 4 and Figure 4 for D3B glioma prediction rate.
- Figure 5 for D3B prediction distribution.
- Table 5 and Figure 6 for D3B temperature-scaled confidence behaviour.

## Remaining Weaknesses

The manuscript currently does not include a dedicated Table 1 dataset summary.

The manuscript does not yet include Figure 1, the reliability-first evaluation pipeline diagram.

The manuscript still needs formal references/citations from the literature.

The manuscript should later be revised into journal formatting with formal subsections, numbered tables, numbered figures, and citation placeholders.

## Current Status

The current manuscript draft is internally consistent with the generated experimental evidence.

The next recommended step is to create Table 1: Dataset Summary and Usage Decision.


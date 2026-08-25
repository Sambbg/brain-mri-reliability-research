# Consolidated tables and figures

Generated: 2026-08-25T19:16:36

All values are aggregated across seeds 42-46 of run set `2026-08-sweep-a`. Nothing here reports a single seed.

Supersedes everything in `reports/experiments/tables/` and `reports/experiments/figures/`, which report either a single seed or the Run A / Run B checkpoints.

## Tables

| File | Contents |
|---|---|
| `per_class_internal_performance` | Precision, recall, F1 per class per architecture |
| `internal_confusion_matrices` | Mean confusion matrices with row proportions |
| `internal_calibration` | ECE, NLL, Brier, confidence gap before and after temperature scaling |
| `probe_prediction_behaviour` | D3B and D3C prediction shares, confidence, entropy, and temperature-scaled behaviour |
| `reliability_bins_pooled` | Count-weighted reliability bins for the diagrams |

## Figures

| File | Contents |
|---|---|
| `fig_internal_vs_shifted_domain` | Internal near-parity beside shifted-domain divergence |
| `fig_seed_spread` | Per-seed points with signal-to-noise per evaluation |
| `fig_reliability_diagrams` | Calibration curves, raw and scaled |
| `fig_probe_prediction_distribution` | Where probe predictions land across the four D1 classes |
| `fig_confusion_matrices` | Internal confusion matrices |


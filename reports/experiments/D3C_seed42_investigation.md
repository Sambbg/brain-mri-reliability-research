# Seed 42 on D3C: Investigation

Generated: 2026-08-12T00:09:42

Seed 42 gave E001 and E003 their highest D3C glioma prediction rates and produced the only McNemar comparison that survived Holm correction as non-significant. This asks whether any recorded property of those runs distinguishes them.

## First correction: it is not all three architectures

Seed 42's D3C rate, in z units against the same model's other four seeds:

| Model | Seed 42 rate | Other seeds | z | Outside range |
|---|---:|---|---:|---|
| E001 | 0.8013 | 0.6220-0.6613 | +8.7 | yes |
| E002 | 0.4577 | 0.4525-0.6118 | -1.1 | no |
| E003 | 0.4630 | 0.1856-0.2502 | +9.3 | yes |

E001 and E003 are extreme. **E002 is not**: its seed-42 D3C rate sits inside its own range across the other seeds. The non-significant McNemar at seed 42 is E002 vs E003, and it arises because E003 rose to meet a perfectly ordinary E002, not because both were disturbed.

## What does stand out

| Metric | E001 | E002 | E003 |
|---|---:|---:|---:|
| d3c_glioma_rate | 0.801 (z+8.7) | 0.458 (z-1.1) | 0.463 (z+9.3) |
| d3b_glioma_rate | 0.309 (z-0.9) | 0.596 (z+4.3) | 0.238 (z-0.2) |
| test_macro_f1 | 0.955 (z-4.3) | 0.974 (z+4.6) | 0.954 (z-1.0) |
| best_epoch | 6.000 (z-0.1) | 11.000 (z+0.4) | 12.000 (z+6.5) |
| epochs_trained | 11.000 (z-0.1) | 16.000 (z+0.4) | 17.000 (z+6.5) |
| temperature | 1.270 (z+0.8) | 1.274 (z+0.5) | 1.258 (z+4.5) |
| d3c_pred_notumor | 0.185 (z-2.0) | 0.524 (z+1.5) | 0.335 (z-7.6) |
| d3c_mean_confidence | 0.856 (z+2.4) | 0.863 (z+1.4) | 0.804 (z-2.6) |
| d1_recall_glioma | 0.952 (z-1.5) | 0.967 (z+1.4) | 0.937 (z-2.2) |
| d1_recall_notumor | 0.944 (z-0.3) | 0.960 (z+2.8) | 0.928 (z-0.2) |

Using |z| > 3 as the bar, the standouts are listed above. Two are worth naming:

- **The notumor share is outside its own range for all three models at seed 42** — but in opposite directions. E001 and E003 call less of D3C notumor than at any other seed, and E002 calls more. The D3C glioma rate is very largely the mirror of the notumor share, so this is a restatement of the anomaly rather than a cause of it.
- **E003 trained markedly longer at seed 42**, 17 epochs with best epoch 12, against 10-12 epochs and best epoch 5-7 elsewhere. This is the single concrete training-trajectory difference found, and it applies to one architecture only.

## A real shared pattern, which is not specific to seed 42

Models at the same seed share one thing: the seeded DataLoader generator gives identical batch ordering and an identical augmentation stream. If that drove the effect, the architectures would move together across seeds.

| Pair | r (all 5 seeds) | p | r (seed 42 dropped) | p |
|---|---:|---:|---:|---:|
| E001 vs E002 | -0.585 | 0.300 | -0.588 | 0.412 |
| E001 vs E003 | +0.993 | 0.001 | +0.842 | 0.158 |
| E002 vs E003 | -0.572 | 0.314 | -0.542 | 0.458 |

E001 and E003 track each other almost perfectly across seeds, and the association survives dropping seed 42, so it is not an artefact of the outlier. E002 does not track either of them. Seed 42 is therefore better described as the extreme end of a seed axis that E001 and E003 share than as a discrete anomaly. Why E002 sits off that axis is not established, and with five seeds the correlation is suggestive rather than demonstrated.

## What does not explain it

Correlation with the D3C glioma rate across all 15 runs, with architecture means removed:

| Predictor | r | p |
|---|---:|---:|
| test_macro_f1 | -0.514 | 0.050 |
| best_epoch | +0.511 | 0.052 |
| epochs_trained | +0.511 | 0.052 |
| temperature | +0.416 | 0.123 |
| d1_recall_notumor | -0.362 | 0.185 |
| d1_recall_glioma | -0.283 | 0.306 |
| d1_pred_share_notumor | -0.212 | 0.448 |
| d1_pred_share_glioma | +0.003 | 0.992 |

No measure taken on D1 predicts shifted-domain behaviour. Per-class recall, the predicted-class shares, the learned temperature, the best epoch and the number of epochs trained are all non-significant. Internal macro-F1 is the only predictor near the threshold, and its association is negative — the Part 1 result, and a description of the phenomenon rather than a mechanism for it.

## Verdict

**Partly characterised, not explained.** Three things are established: the anomaly is confined to E001 and E003, E002's seed-42 D3C rate being ordinary; E003 trained substantially longer at this seed; and E001 and E003 move together across seeds in a way that does not depend on seed 42.

No cause was found. Nothing recorded about training on D1 — trajectory, stopping point, calibration temperature, or per-class confusion structure — distinguishes the seed-42 runs or predicts the D3C rate. **This should be reported as unexplained seed sensitivity rather than attributed to a mechanism the data does not support.** It is itself evidence for the project's argument: a single-seed shifted-domain result can land far from the others for reasons not visible in any internal metric.

The defensible response is to report all five seeds with intervals rather than to explain or exclude this one. Excluding seed 42 would need a reason established before seeing its result, and there is none.

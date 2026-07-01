# D1 Usage Decision — Nickparvar Kaggle Brain Tumor MRI Dataset

## Decision Date
2026-04-29

## Dataset
D1 — Nickparvar Kaggle Brain Tumor MRI Dataset

## Decision
Use D1 as a development/source dataset only.

Do not treat the original Kaggle Testing folder as a clean independent test set for publication-grade claims.

## Reason

D1 is useful because it contains 7,200 four-class brain MRI images covering:

- glioma
- meningioma
- pituitary
- no tumour

However, quality-control checks identified important risks.

## Exact Duplicate Audit

The exact SHA256 duplicate audit found:

| Item | Count |
|---|---:|
| Original rows | 7,200 |
| Unique SHA256 hashes | 7,013 |
| Duplicate hash groups | 153 |
| Images involved in duplicate groups | 340 |
| Rows removed by exact deduplication | 187 |
| Cross-split exact duplicate groups | 0 |
| Cross-class exact duplicate groups | 0 |

This means exact train/test duplicate leakage was not found, but repeated images exist within the dataset.

## Near-Duplicate Audit

The pHash near-duplicate audit on the exact-deduplicated manifest found:

| Item | Count |
|---|---:|
| Rows compared | 7,013 |
| Near-duplicate pairs found | 5,125 |
| Cross-split near-duplicate pairs | 1,926 |
| Cross-class near-duplicate pairs | 46 |

This creates a serious risk that the original Training/Testing folders are not independent enough for reliable evaluation.

## Consequence for Experiments

The original D1 split will not be used as the main evidence of model generalisation.

Instead:

1. D1 may be used for initial model development.
2. The exact-deduplicated manifest should be used.
3. A new leakage-aware split should be created.
4. External evaluation must use a genuinely independent dataset.
5. Any results from the original Kaggle split must be labelled as exploratory only.

## Publication-Framing Implication

This finding supports the thesis motivation: public brain MRI classification benchmarks may contain hidden duplication and near-duplication risks that inflate apparent performance and reduce trustworthiness of reported accuracy.

## Next Required Step
Create a leakage-aware D1 split based on near-duplicate grouping, or move to acquiring an external dataset before model training.

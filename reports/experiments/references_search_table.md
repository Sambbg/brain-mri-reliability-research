# References Search Table

## Purpose

This table tracks the literature needed to support the manuscript claims.

Every reference added to the final manuscript must support a specific claim. Do not add references only to increase the reference count.

## Search Table

| ID | Area | Search query | Database / source | Inclusion criteria | Exclusion criteria | Candidate paper title | DOI / URL | Why it is useful | Manuscript section | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| R001 | Calibration and temperature scaling | neural network calibration temperature scaling expected calibration error | Google Scholar / PubMed / IEEE | Foundational or highly cited calibration paper | Blog posts, non-peer-reviewed summaries | TBD | TBD | Supports calibration and temperature scaling method | Introduction / Methods / Discussion | To search |
| R002 | Dataset leakage and overlap | medical imaging dataset leakage duplicate images train test split | Google Scholar / PubMed | Discusses leakage, duplicate images, or data contamination in medical imaging ML | Non-medical examples only unless foundational | TBD | TBD | Supports D1 duplicate audit and D2 rejection rationale | Introduction / Methods / Discussion | To search |
| R003 | Dataset shift and external validation | medical imaging AI dataset shift external validation generalisation | Google Scholar / PubMed | Discusses external validation, domain shift, scanner/site shift, or robustness | Papers only reporting internal validation | TBD | TBD | Supports D3B domain-shift evaluation rationale | Introduction / Discussion | To search |
| R004 | Brain MRI tumour classification benchmarks | brain MRI tumor classification deep learning public dataset ResNet EfficientNet Vision Transformer | Google Scholar / IEEE / PubMed | Recent brain MRI tumour classification papers using CNNs or transformers | Papers without MRI or tumour classification relevance | TBD | TBD | Supports background that high internal accuracy is common | Introduction | To search |
| R005 | Uncertainty-aware medical imaging | uncertainty estimation medical image classification deep ensembles Monte Carlo dropout calibration | Google Scholar / PubMed | Uncertainty methods evaluated in medical imaging or foundational uncertainty method | Weak opinion articles | TBD | TBD | Supports future work and distinction between calibration and uncertainty | Discussion / Future work | To search |
| R006 | Reporting standards clinical AI | CLAIM checklist medical imaging artificial intelligence reporting guidelines external validation | PubMed / Google Scholar | Reporting guideline or checklist relevant to medical AI | Non-healthcare AI reporting only | TBD | TBD | Supports cautious reliability claims and reporting standards | Methods / Discussion / Limitations | To search |

## Priority Search Order

1. Calibration and temperature scaling.
2. Dataset leakage and overlap.
3. Dataset shift and external validation.
4. Brain MRI tumour classification benchmarks.
5. Reporting standards.
6. Uncertainty-aware methods.

## Notes

Each selected paper should later be added to a formal reference list in the required citation style.

For each selected paper, record:

- Full title.
- Authors.
- Year.
- Journal or conference.
- DOI or stable URL.
- Exact manuscript claim it supports.
- Whether it is foundational, review, benchmark, or method paper.

## Quality Rules

Prefer:

- Peer-reviewed journal articles.
- Highly cited foundational papers.
- Recent review papers.
- Medical imaging-specific reliability papers.
- Official reporting standards.

Avoid:

- Random low-quality papers.
- Papers with unclear datasets.
- Papers that only report high accuracy without reliability relevance.
- Citations that do not directly support a manuscript claim.

## Verified Calibration References

| ID | Area | Search query | Database / source | Inclusion criteria | Exclusion criteria | Candidate paper title | DOI / URL | Why it is useful | Manuscript section | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| REF-CAL-001 | Calibration and temperature scaling | neural network calibration temperature scaling expected calibration error | ICML / arXiv | Foundational calibration paper for modern neural networks | Non-peer-reviewed summaries only | On Calibration of Modern Neural Networks | https://arxiv.org/abs/1706.04599 | Supports neural network miscalibration, expected calibration error, and post-hoc temperature scaling | Introduction / Methods / Discussion | Verified |
| REF-CAL-002 | Calibration error metrics | expected calibration error maximum calibration error Bayesian binning calibrated probabilities | AAAI / PMC | Defines and uses calibration error metrics including ECE and MCE | Papers not focused on probability calibration | Obtaining Well Calibrated Probabilities Using Bayesian Binning | https://pmc.ncbi.nlm.nih.gov/articles/PMC4410090/ | Supports calibration-error measurement and probability calibration concepts | Methods | Verified |
| REF-CAL-003 | Brier score | Brier score verification forecasts probability 1950 | Monthly Weather Review | Original source for probability forecast verification and Brier score | Secondary references only | Verification of Forecasts Expressed in Terms of Probability | https://journals.ametsoc.org/view/journals/mwre/78/1/1520-0493_1950_078_0001_vofeit_2_0_co_2.xml | Supports use of Brier score as a probabilistic prediction metric | Methods | Verified |

## Calibration Manuscript Claim Mapping

| Claim ID | Manuscript claim | Supporting reference |
|---|---|---|
| CLAIM-CAL-001 | Modern neural networks can achieve high accuracy while being poorly calibrated. | REF-CAL-001 |
| CLAIM-CAL-002 | Temperature scaling is a simple post-hoc calibration method fitted using validation logits. | REF-CAL-001 |
| CLAIM-CAL-003 | Expected calibration error is a standard summary measure of calibration mismatch. | REF-CAL-001; REF-CAL-002 |
| CLAIM-CAL-004 | Brier score can be used to evaluate probabilistic prediction quality. | REF-CAL-003 |

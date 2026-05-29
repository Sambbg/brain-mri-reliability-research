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

## Verified Dataset Leakage and Overlap References

| ID | Area | Search query | Database / source | Inclusion criteria | Exclusion criteria | Candidate paper title | DOI / URL | Why it is useful | Manuscript section | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| REF-LEAK-001 | Dataset leakage and radiology data handling | radiology machine learning data handling patient level split leakage | Radiology: Artificial Intelligence / PMC | Radiology-specific paper discussing data handling, splitting, and bias | Non-medical or non-radiology leakage examples only | Mitigating Bias in Radiology Machine Learning: 1. Data Handling | https://pmc.ncbi.nlm.nih.gov/articles/PMC9533091/ | Supports leakage prevention, patient-level splitting, and careful medical imaging data handling | Introduction / Methods / Discussion | Verified |
| REF-LEAK-002 | Data leakage and inflated medical imaging performance | inflation test accuracy data leakage deep learning OCT images | Scientific Data / Nature | Medical imaging study directly quantifying performance inflation from improper splitting | Non-peer-reviewed summaries | Inflation of test accuracy due to data leakage in deep learning-based classification of OCT images | https://www.nature.com/articles/s41597-022-01618-6 | Supports the claim that improper splitting can substantially inflate medical imaging model performance | Introduction / Discussion | Verified |
| REF-LEAK-003 | Brain MRI leakage | brain MRI classification data leakage 2D CNN | Frontiers / PMC | Brain MRI-specific study on data leakage in 2D CNN classification | Papers unrelated to MRI | Effect of data leakage in brain MRI classification using 2D convolutional neural networks | https://pmc.ncbi.nlm.nih.gov/articles/PMC8604922/ | Directly supports the relevance of leakage-aware evaluation in brain MRI classification | Introduction / Methods / Discussion | Verified |
| REF-LEAK-004 | Leakage-aware splitting | information leakage data splitting machine learning DataSAIL | PMC | General method paper focused on splitting to avoid information leakage | Opinion pieces or blogs | Data splitting to avoid information leakage with DataSAIL | https://pmc.ncbi.nlm.nih.gov/articles/PMC11978981/ | Supports the broader principle that splitting strategy is essential to prevent information leakage and memorisation | Methods / Discussion | Verified |

## Dataset Leakage Manuscript Claim Mapping

| Claim ID | Manuscript claim | Supporting reference |
|---|---|---|
| CLAIM-LEAK-001 | Medical imaging ML performance can be inflated when related images or patients leak across train/test splits. | REF-LEAK-001; REF-LEAK-002; REF-LEAK-003 |
| CLAIM-LEAK-002 | Patient-level or group-level splitting is important for reducing leakage in radiology ML. | REF-LEAK-001; REF-LEAK-003 |
| CLAIM-LEAK-003 | Public datasets require overlap auditing before being treated as independent validation sets. | REF-LEAK-001; REF-LEAK-004 |
| CLAIM-LEAK-004 | D2 should not be used as clean external validation after substantial exact and perceptual overlap with D1 was detected. | REF-LEAK-001; REF-LEAK-002; REF-LEAK-003 |

## Verified Dataset Shift and External Validation References

| ID | Area | Search query | Database / source | Inclusion criteria | Exclusion criteria | Candidate paper title | DOI / URL | Why it is useful | Manuscript section | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| REF-SHIFT-001 | External validation in radiology deep learning | external validation deep learning radiologic diagnosis systematic review | Radiology: Artificial Intelligence / PMC | Systematic review of external validation in radiologic DL diagnosis | Single-centre internal validation studies only | External Validation of Deep Learning Algorithms for Radiologic Diagnosis: A Systematic Review | https://doi.org/10.1148/ryai.210064 | Supports the claim that radiology DL models often show reduced performance under external validation | Introduction / Discussion / Limitations | Verified |
| REF-SHIFT-002 | Medical imaging AI generalisability | assessing generalizability artificial intelligence medical imaging external validation | PMC / PubMed | Review focused on AI generalisability in medical imaging | Non-imaging AI papers | Assessing the generalizability of artificial intelligence in medical imaging | https://pmc.ncbi.nlm.nih.gov/articles/PMC12689012/ | Supports need for validation across institutions, populations, and imaging conditions | Introduction / Discussion | Verified |
| REF-SHIFT-003 | Domain generalization in medical imaging | domain generalization medical image analysis review dataset shift | arXiv | Review focused on domain generalization in medical image analysis | Non-medical domain generalization only | Domain Generalization for Medical Image Analysis: A Review | https://arxiv.org/abs/2310.08598 | Supports the broader problem of medical image domain shift and generalisation | Introduction / Discussion / Future work | Verified |
| REF-SHIFT-004 | Shift-data curation in medical imaging | MedShift automated identification shift data medical image dataset curation | PMC | Medical imaging paper focused on identifying shifted datasets for validation/generalisation | Non-medical shift detection only | MedShift: Automated Identification of Shift Data for Medical Image Dataset Curation | https://pmc.ncbi.nlm.nih.gov/articles/PMC10513895/ | Supports the need to identify and curate shifted datasets for robust validation | Methods / Discussion | Verified |

## Dataset Shift Manuscript Claim Mapping

| Claim ID | Manuscript claim | Supporting reference |
|---|---|---|
| CLAIM-SHIFT-001 | Strong internal performance does not guarantee external or shifted-domain reliability in medical imaging. | REF-SHIFT-001; REF-SHIFT-002 |
| CLAIM-SHIFT-002 | External validation should ideally test models across different institutions, patient populations, scanners, or imaging conditions. | REF-SHIFT-001; REF-SHIFT-002 |
| CLAIM-SHIFT-003 | D3B should be interpreted as glioma-focused domain-shift analysis rather than full four-class external validation. | REF-SHIFT-001; REF-SHIFT-002; REF-SHIFT-003 |
| CLAIM-SHIFT-004 | Curating shifted medical image datasets is important for evaluating model generalisation. | REF-SHIFT-003; REF-SHIFT-004 |

## Verified Brain MRI Tumour Classification References

| ID | Area | Search query | Database / source | Inclusion criteria | Exclusion criteria | Candidate paper title | DOI / URL | Why it is useful | Manuscript section | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| REF-BMRI-001 | Brain MRI tumour deep learning review | brain tumor MRI deep learning review classification segmentation | npj Precision Oncology / PMC / Nature | Recent review covering deep learning for brain tumour MRI analysis | Narrow single-model studies only | A review of deep learning for brain tumor analysis in MRI | https://www.nature.com/articles/s41698-024-00789-2 | Supports the background claim that deep learning is widely applied to MRI brain tumour analysis, including classification | Introduction / Discussion | Verified |
| REF-BMRI-002 | Brain tumour detection/classification/segmentation review | brain tumor detection classification segmentation deep learning MRI review public datasets metrics | Informatics in Medicine Unlocked / ScienceDirect | Review covering datasets, preprocessing, performance metrics, detection, classification, and segmentation | Papers unrelated to MRI | Brain tumor detection, classification and segmentation by deep learning based on MRI images | https://www.sciencedirect.com/science/article/pii/S2590005625001985 | Supports background on common datasets, model types, metrics, and clinical-relevance limitations in MRI brain tumour DL | Introduction / Discussion | Verified |
| REF-BMRI-003 | Recent systematic review | deep learning brain tumor detection classification MRI systematic review 2020 2024 | Journal of Imaging Informatics in Medicine / Springer | Recent systematic review focused on MRI brain tumour detection/classification | Non-systematic opinion papers | Deep Learning Approaches for Brain Tumor Detection and Classification Using MRI Images (2020 to 2024): A Systematic Review | https://doi.org/10.1007/s10278-024-01283-8 | Supports the claim that recent literature contains many MRI brain tumour DL classification studies | Introduction | Verified |
| REF-BMRI-004 | Four-class MRI tumour classification benchmark example | four class brain tumor MRI classification glioma meningioma pituitary no tumor ResNet EfficientNet | arXiv | Study using four-class MRI tumour classification with common pretrained architectures | Studies without comparable class structure | Deep Learning in Medical Image Classification from MRI-based Brain Tumor Images | https://arxiv.org/abs/2408.00636 | Supports background that four-class public MRI tumour classification benchmarks are commonly used with CNN backbones | Introduction / Methods context | Verified |

## Brain MRI Tumour Classification Manuscript Claim Mapping

| Claim ID | Manuscript claim | Supporting reference |
|---|---|---|
| CLAIM-BMRI-001 | Deep learning is widely used for MRI brain tumour analysis, including classification. | REF-BMRI-001; REF-BMRI-002 |
| CLAIM-BMRI-002 | Recent MRI brain tumour classification studies commonly evaluate CNN, transformer, or hybrid architectures on public datasets. | REF-BMRI-001; REF-BMRI-002; REF-BMRI-003 |
| CLAIM-BMRI-003 | Four-class brain MRI tumour classification benchmarks commonly include glioma, meningioma, pituitary tumour, and no-tumour classes. | REF-BMRI-004 |
| CLAIM-BMRI-004 | Many studies emphasise internal performance metrics, which motivates additional reliability evaluation using leakage audits, calibration, and domain-shift testing. | REF-BMRI-001; REF-BMRI-002; REF-BMRI-003 |

## Verified Reporting Standards References

| ID | Area | Search query | Database / source | Inclusion criteria | Exclusion criteria | Candidate paper title | DOI / URL | Why it is useful | Manuscript section | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| REF-REPORT-001 | Medical imaging AI reporting standards | CLAIM 2024 checklist artificial intelligence medical imaging reporting guideline | Radiology: Artificial Intelligence / PMC / EQUATOR | Reporting guideline specifically for AI in medical imaging | Non-imaging AI reporting only | Checklist for Artificial Intelligence in Medical Imaging (CLAIM): 2024 Update | https://pmc.ncbi.nlm.nih.gov/articles/PMC11304031/ | Supports transparent and reproducible reporting of medical imaging AI studies | Methods / Discussion / Limitations | Verified |
| REF-REPORT-002 | Prediction model reporting standards | TRIPOD AI statement reporting clinical prediction models machine learning 2024 | BMJ / EQUATOR | Reporting guideline for prediction model studies using regression or machine learning | Clinical trial-only guidance | TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods | https://www.bmj.com/content/385/bmj-2023-078378 | Supports transparent reporting of prediction model development and evaluation | Methods / Discussion / Limitations | Verified |
| REF-REPORT-003 | AI clinical trial reporting standards | CONSORT AI SPIRIT AI reporting guidelines artificial intelligence clinical trials | Nature Medicine / Trials | Reporting guidelines for clinical trials or protocols involving AI interventions | Not to be used as direct evidence for this non-clinical experimental study | Guidelines for clinical trial protocols for interventions involving artificial intelligence: the SPIRIT-AI extension; Reporting guidelines for clinical trials of artificial intelligence interventions: CONSORT-AI | https://www.nature.com/articles/s41591-020-1037-7 | Supports future-work claim that clinical deployment requires prospective and transparently reported clinical evaluation | Discussion / Future work | Verified |

## Reporting Standards Manuscript Claim Mapping

| Claim ID | Manuscript claim | Supporting reference |
|---|---|---|
| CLAIM-REPORT-001 | Medical imaging AI studies should report data sources, evaluation design, model development, and validation transparently. | REF-REPORT-001 |
| CLAIM-REPORT-002 | Prediction model studies using machine learning should report model development and evaluation clearly. | REF-REPORT-002 |
| CLAIM-REPORT-003 | This study should be interpreted as retrospective experimental evaluation, not clinical deployment evidence. | REF-REPORT-001; REF-REPORT-002 |
| CLAIM-REPORT-004 | Future clinical translation would require prospective clinical evaluation and appropriate clinical-trial reporting standards. | REF-REPORT-003 |

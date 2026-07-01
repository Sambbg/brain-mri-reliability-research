# Manuscript Statements

## Purpose

This file stores draft manuscript statements that can later be inserted into the final thesis, supervisor report, or journal manuscript.

These statements are draft versions and should be revised according to the final target journal or university format.

---

## Data Availability Statement

This study used publicly available brain MRI datasets and a TCIA/ICDC-derived glioma-focused dataset. The primary internal dataset was used for four-class brain MRI tumour classification, while the ICDC-Glioma / TCIA-derived dataset was used for glioma-focused shifted-domain analysis after DICOM inspection and slice conversion.

The processed dataset manifests, dataset usage decisions, overlap-audit outputs, and derived experiment summaries are stored in the project repository. Raw imaging data are not redistributed in this repository. Users should obtain original imaging data directly from the relevant public dataset providers and comply with their usage terms.

---

## Code Availability Statement

The code used for dataset preparation, overlap auditing, model training, calibration analysis, shifted-domain evaluation, and manuscript figure/table generation is stored in the project repository.

The repository includes scripts for:

- Dataset preparation and audit workflows.
- Training ResNet18, EfficientNet-B0, and ViT-B/16 models.
- Internal performance evaluation.
- Temperature scaling and calibration analysis.
- D3B shifted-domain analysis.
- Generation of manuscript tables and figures.
- Citation and manuscript-readiness audits.

Before public release or journal submission, the repository should be cleaned to ensure that no restricted data, large model files, private paths, or unnecessary temporary files are included.

---

## Ethics and Dataset Use Statement

This study used retrospective publicly available imaging data and did not involve direct patient recruitment, intervention, or prospective clinical testing by the author. No clinical decisions were made using the models developed in this project.

The ICDC-Glioma / TCIA-derived dataset was used only for research evaluation and shifted-domain analysis. Raw data redistribution is not performed in this repository. All dataset use should comply with the original dataset licences, access terms, and citation requirements.

This study should be interpreted as a retrospective experimental evaluation of model reliability, not as clinical validation or deployment evidence.

---

## AI-Assisted Writing and Research Support Statement

The author used ChatGPT as an AI-assisted tool for project organisation, code drafting support, debugging guidance, manuscript outlining, language refinement, table and figure planning, and citation-tracking workflow design.

All experimental design decisions, code execution, data processing, model training, result verification, interpretation, and final manuscript content remain the responsibility of the author. The AI tool was not treated as an author and was not used as a scientific source. All cited literature must be independently verified by the author before thesis submission or journal submission.

This statement should be revised according to the disclosure requirements of the target journal, university, or supervisor.

---

## Clinical Use Disclaimer

The models evaluated in this study are not intended for clinical deployment. The study does not establish diagnostic safety, clinical efficacy, prospective validity, or readiness for use in patient care.

Further validation using site-diverse datasets, prospective evaluation, clinical workflow assessment, and appropriate regulatory and ethical review would be required before any clinical-use claim could be considered.

---

## Conflict of Interest Statement

The author declares no known conflict of interest related to this study.

This statement should be updated if any funding source, institutional relationship, commercial interest, or software/hardware dependency creates a potential conflict.

---

## Funding Statement

No dedicated external funding is currently declared for this study.

This statement should be updated if institutional, grant, commercial, or scholarship funding is later used or acknowledged.

---

## Author Responsibility Statement

The author is responsible for the integrity of the work, including the accuracy of reported results, verification of cited literature, correctness of code execution, and final interpretation of findings.

Generated outputs, tables, figures, and manuscript text should be checked against saved experiment artifacts before submission.

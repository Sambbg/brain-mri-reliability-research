# AI Use and Citation Integrity Protocol

## Purpose

This protocol defines how AI assistance and literature integration will be handled in this research project.

The goal is to ensure that the manuscript remains academically defensible, transparent, and reproducible.

## AI Use Position

AI tools may be used for:

- Project organisation.
- Code drafting support.
- Debugging assistance.
- Manuscript outlining.
- Language refinement.
- Table and figure planning.
- Literature search planning.

AI tools must not be treated as:

- A scientific source.
- An author.
- A replacement for reading papers.
- A substitute for methodological judgment.
- A justification for claims not supported by evidence.

## Author Responsibility

The author remains responsible for:

- Experimental design decisions.
- Running all code.
- Verifying all outputs.
- Checking all tables and figures.
- Reading and validating all cited references.
- Ensuring that every claim is supported.
- Ensuring that limitations are honestly stated.
- Final manuscript approval.

## Citation Integrity Rules

Every cited paper must support a specific manuscript claim.

Do not cite a paper unless:

1. The title, authors, year, venue, and DOI/URL have been verified.
2. The paper has been read at least at abstract, methods, and conclusion level.
3. The specific claim supported by the paper is recorded.
4. The paper is relevant to the manuscript section where it is cited.

Do not use citations as decoration.

Do not use papers only because they appear to support the desired conclusion.

Do not cite papers that have not been checked.

## Literature Integration Rules

Literature integration should be used to:

- Position the research gap.
- Support methodological choices.
- Compare findings with prior work.
- Explain why leakage, calibration, and dataset shift matter.
- Clarify limitations and future work.

Literature integration should not be used to:

- Rewrite the research history dishonestly.
- Pretend the study was fully literature-led if it was developed iteratively.
- Hide weak evidence.
- Overstate clinical reliability.
- Claim external validation where only domain-shift analysis was performed.

## Disclosure Principle

If the target journal requires AI disclosure, the manuscript should include a declaration describing how AI was used.

Suggested disclosure wording:

> The author used ChatGPT as an AI-assisted tool for project organisation, code drafting support, manuscript outlining, and language editing. All experimental design decisions, code execution, data analysis, result verification, interpretation, and final manuscript content were reviewed and approved by the author. The AI tool was not listed as an author and was not used as a source of scientific evidence. All cited literature was independently verified by the author.

## Current Project Safeguards

This project already includes:

- Git version control.
- Reproducible scripts.
- Saved configuration files.
- Saved experiment outputs.
- Dataset overlap audits.
- Generated tables from JSON artifacts.
- Generated figures from saved tables.
- Conservative interpretation notes.
- Manuscript consistency audit.
- Final manuscript readiness audit.

These safeguards reduce the risk of unverifiable or AI-generated claims.

## Remaining Requirements Before Journal Submission

Before any journal submission:

1. Verify all references manually.
2. Read every cited paper.
3. Add citation placeholders to the manuscript only where justified.
4. Confirm journal AI disclosure policy.
5. Confirm journal data/code availability policy.
6. Recheck all manuscript claims against saved experimental artifacts.
7. Revise the manuscript for journal style.
8. Avoid claiming clinical validation.
9. Avoid claiming full external four-class validation on D3B.
10. Clearly state that D3B is glioma-focused domain-shift analysis.

## Status

This protocol should be followed for all future literature integration and manuscript revision.

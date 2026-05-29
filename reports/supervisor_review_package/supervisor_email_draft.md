# Supervisor Email Draft

Subject: MSc Research Progress Update – Brain MRI Reliability Evaluation

Dear Dr [Supervisor Name],

I hope you are well.

I am writing to share my current MSc research progress for your review. I have prepared a supervisor review package containing the current manuscript draft, progress summary, figures, tables, reproducibility audits, and draft manuscript statements.

The current project title is:

**Reliability Evaluation of Brain MRI Tumour Classification Models Under Calibration and Dataset Shift**

The study evaluates whether high-performing brain MRI tumour classification models remain reliable when assessed beyond internal accuracy. The current work focuses on leakage-aware dataset preparation, overlap auditing, calibration, temperature scaling, and shifted-domain evaluation.

The main progress so far includes:

1. Training and evaluation of three architectures:
   - ResNet18
   - EfficientNet-B0
   - ViT-B/16

2. Internal D1 evaluation showing high performance across all three models.

3. Calibration analysis showing that temperature scaling improved internal calibration.

4. Dataset overlap auditing showing that D2 was unsuitable as clean external validation because of substantial overlap with D1.

5. D3B shifted-domain evaluation showing that high internal performance did not guarantee stable glioma-focused prediction behaviour.

6. A manuscript draft with tables, figures, citation placeholders, and draft declarations.

The main point I would like your feedback on is whether the current research framing is acceptable for a Master's project: specifically, whether the emphasis should remain on reliability evaluation rather than developing a novel model architecture.

I would also appreciate your feedback on:

- Whether the D2 rejection due to dataset overlap is methodologically acceptable and worth emphasising.
- Whether D3B is acceptable as a glioma-focused shifted-domain analysis, provided I do not claim it as full four-class external validation.
- Whether the current experiments are sufficient for the MSc thesis, or whether additional uncertainty-aware experiments are necessary.
- Whether the manuscript should be structured as a thesis chapter first or developed toward a journal-style paper.

I have attached the supervisor review package for your comments.

Kind regards,  
Samuel Gonzalves

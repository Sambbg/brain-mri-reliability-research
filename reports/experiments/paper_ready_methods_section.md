# Paper-Ready Methods Section Draft

## Methods

### Study design

This study used a reliability-focused experimental design to evaluate brain MRI tumour classification models beyond internal accuracy. The evaluation pipeline included leakage-aware dataset preparation, duplicate and overlap auditing, internal model evaluation, calibration analysis, post-hoc temperature scaling, and glioma-focused domain-shift testing.

Three model architectures were evaluated:

- E001: ResNet18
- E002: EfficientNet-B0
- E003: ViT-B/16

All models were trained on the same D1 leakage-aware split and evaluated using the same internal and cross-dataset protocol.

### Dataset D1: internal training and testing dataset

D1 was used as the primary four-class brain MRI tumour classification dataset. The four classes were:

- glioma
- meningioma
- notumor
- pituitary

A manifest was created to record image paths, labels, and split information. Exact duplicate analysis was performed using SHA256 hashing. A leakage-aware split was then used to reduce the risk of duplicate or near-identical samples appearing across training, validation, and test subsets.

The final D1 split contained separate training, validation, and test partitions. All model comparisons used this same split to ensure fairness across architectures.

### Dataset D2: rejected external validation candidate

D2 was initially considered as an external validation candidate. However, exact SHA256 overlap and perceptual-hash near-overlap audits showed substantial overlap between D1 and D2.

Because of this overlap, D2 was rejected as a clean independent external validation dataset. D2 was not used for model performance claims.

### Dataset D3B: glioma-focused domain-shift dataset

D3B was derived from the ICDC-Glioma collection. It was used as a visually distinct glioma-focused domain-shift dataset.

D3B was not treated as a full four-class external validation dataset because it does not share the same four-class label structure as D1. Instead, it was used to test whether D1-trained models recognised visually distinct glioma-domain images as glioma.

Selected DICOM series were downloaded, inspected, and converted into 2D PNG images using a reproducible central-slice rule. Five central slices were selected per valid series. The final converted D3B dataset contained 265 slices from 53 patients and 53 series.

### D3B overlap auditing

After conversion, D3B was compared against D1 using exact SHA256 hashing and perceptual hashing. No exact SHA256 overlap and no pHash near-overlap were detected at the selected threshold. This supported treating D3B as visually distinct from D1 for glioma-focused domain-shift analysis.

### Model training

Each model was trained on the D1 training split using the same leakage-aware data partition. Validation performance was monitored during training, and the best model checkpoint was selected based on validation macro-F1.

The three architectures were:

- ResNet18
- EfficientNet-B0
- ViT-B/16

All models used four output classes corresponding to the D1 class labels.

### Internal evaluation

Each trained model was evaluated on the D1 test split. The following metrics were calculated:

- accuracy
- balanced accuracy
- macro-F1
- class-level precision
- class-level recall
- class-level F1-score
- confusion matrix

These metrics measured internal classification performance only.

### Calibration evaluation

Internal calibration was evaluated on the D1 test split using:

- mean maximum softmax confidence
- confidence-accuracy gap
- expected calibration error using 15 bins
- Brier score
- negative log-likelihood

Reliability bin tables were generated to show the relationship between confidence and empirical accuracy across confidence intervals.

### Temperature scaling

Post-hoc temperature scaling was applied to each model. The temperature parameter was fitted using validation-set logits only. The learned temperature was then applied to held-out D1 test logits.

Temperature scaling was evaluated by comparing raw softmax metrics against temperature-scaled metrics. The model weights were not retrained during temperature scaling.

### D3B domain-shift evaluation

Each D1-trained model was evaluated on the D3B central-slice dataset. Because D3B is glioma-focused and does not support full four-class external accuracy evaluation, the analysis focused on prediction behaviour and confidence rather than conventional accuracy.

The following D3B metrics were calculated:

- slice-level glioma prediction rate
- patient-majority glioma prediction rate
- series-majority glioma prediction rate
- mean glioma probability
- median glioma probability
- mean maximum softmax confidence
- median maximum softmax confidence
- entropy
- prediction distribution across the four D1 classes

### D3B temperature-scaled evaluation

The temperature learned from D1 validation logits was applied to D3B predictions. Raw and temperature-scaled D3B confidence metrics were compared.

This analysis tested whether calibration softened confidence under dataset shift and whether it changed prediction distributions. Since temperature scaling does not alter logits ordering, class predictions were expected to remain unchanged unless numerical ties occurred.

### Reproducibility and version control

All scripts, configuration files, reports, and tabular outputs were version-controlled using Git. Raw medical image data and large model checkpoints were kept outside normal Git tracking where appropriate.

Each experiment produced a structured folder containing configuration files, metadata, metrics history, test predictions, confusion matrices, calibration metrics, and domain-shift outputs.

### Statistical interpretation

This study did not attempt to prove clinical diagnostic validity. The goal was to evaluate reliability-related behaviour under controlled experimental conditions.

D3B results were interpreted conservatively as glioma-focused domain-shift behaviour, not as four-class external accuracy or clinical diagnostic accuracy.

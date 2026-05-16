# Paper-Ready Discussion Section Draft

## Discussion

### Principal finding

This study shows that high internal classification performance is not sufficient evidence of reliability in brain MRI tumour classification. Across ResNet18, EfficientNet-B0, and ViT-B/16, all models achieved strong internal performance on the leakage-aware D1 test split, yet none maintained stable glioma-domain prediction behaviour on visually distinct D3B images.

This finding directly challenges the common assumption that high test accuracy on public brain MRI datasets is enough to support reliability claims. Even when duplicate leakage was controlled and internal calibration was improved using temperature scaling, the models remained unstable under cross-dataset shift.

### Internal performance can hide external fragility

The internal D1 results were strong across all three architectures. EfficientNet-B0 achieved the highest internal macro-F1, followed closely by ResNet18, while ViT-B/16 remained slightly lower but still high.

If this study had stopped at internal accuracy and macro-F1, the models would appear highly reliable. However, the D3B evaluation showed a different picture. ResNet18 predicted glioma for only 29.43% of D3B slices, EfficientNet-B0 for 44.15%, and ViT-B/16 for 40.38%.

This means that internal performance substantially overestimated model reliability under domain shift.

### Dataset overlap auditing is essential

One of the most important methodological findings was the rejection of D2 as an external validation dataset. D2 initially appeared useful as an external candidate, but exact and perceptual overlap auditing revealed substantial D1-D2 overlap.

This matters because many medical imaging studies treat public datasets as independent simply because they have different names or sources. This study shows that such an assumption is unsafe. Without overlap auditing, an apparently external evaluation may actually contain reused or visually duplicated samples, leading to inflated generalisation claims.

Therefore, dataset independence should be treated as an empirical question, not an assumption.

### Calibration improved confidence but did not solve domain shift

Temperature scaling improved internal calibration for all three models. It reduced ECE, reduced confidence-accuracy gaps, and improved negative log-likelihood. This confirms that post-hoc calibration is useful for improving confidence quality on the internal distribution.

However, temperature scaling did not correct the D3B prediction distribution. The class predictions and patient-majority behaviour remained unchanged after scaling. This is expected because temperature scaling modifies probability sharpness but does not change the learned feature representation.

This distinction is important. Calibration can make confidence values less extreme, but it cannot force a model to learn domain-invariant tumour features after training. Therefore, calibration should not be presented as a solution to dataset shift.

### Architecture alone did not solve reliability

EfficientNet-B0 performed best overall, both internally and on D3B. However, even EfficientNet-B0 failed to predict glioma for a majority of D3B slices. ViT-B/16 did not outperform the CNN baselines and showed substantial D3B instability, including frequent notumor predictions on glioma-domain images.

This weakens any simplistic claim that transformer-based models are inherently more reliable than CNNs. Architecture may improve performance, but reliability depends on data quality, dataset independence, calibration, and robustness under shift.

The results suggest that model architecture alone is not enough to solve reliability problems in brain MRI tumour classification.

### Implications for brain MRI tumour classification research

The findings support a reliability-first evaluation framework. Future studies should report more than accuracy, precision, recall, and F1-score. At minimum, reliability-focused evaluation should include:

1. Duplicate and overlap auditing.
2. Leakage-aware splitting.
3. Internal calibration metrics.
4. Post-hoc calibration analysis.
5. External or domain-shift evaluation.
6. Conservative interpretation of external results.

This is especially important in medical imaging, where overconfident or unstable predictions may be harmful if misinterpreted as clinically meaningful.

### Why the D3B result should be interpreted carefully

D3B is not a full four-class external validation dataset. It is a glioma-focused domain-shift dataset. Therefore, the D3B results should not be described as four-class external accuracy.

The correct interpretation is narrower: D3B tests whether D1-trained models recognise visually distinct glioma-domain images as glioma and how their confidence behaves under dataset shift.

This makes the D3B result valuable, but it must be framed conservatively. It demonstrates instability in glioma-domain prediction behaviour, not clinical diagnostic accuracy.

### Methodological strength of the study

The main strength of this study is that it does not rely on a single metric or a single model. The evaluation pipeline combines:

- Leakage-aware D1 splitting.
- Duplicate and overlap auditing.
- Three model architectures.
- Internal calibration analysis.
- Temperature scaling.
- D3B domain-shift evaluation.
- Conservative interpretation of external evidence.

This makes the results more defensible than a standard accuracy-only benchmark comparison.

### Limitations

This study has several limitations.

First, D3B is glioma-focused and does not provide the same four-class label structure as D1. Therefore, it cannot support full four-class external accuracy claims.

Second, D3B labels are collection-level glioma labels rather than slice-level tumour annotations. The central-slice conversion strategy is reproducible, but it does not guarantee that every selected slice contains visible tumour tissue.

Third, only three architectures were evaluated. Additional architectures, including DenseNet, Swin Transformer, ConvNeXt, and uncertainty-aware models, may produce different results.

Fourth, this study evaluates prediction behaviour and confidence under dataset shift. It does not establish clinical diagnostic validity.

Fifth, the models were trained using 2D image representations. Full 3D volumetric modelling may better capture anatomical context.

### Future work

Future work should extend this evaluation in several directions.

First, additional independent datasets should be identified and audited for overlap before use.

Second, uncertainty-aware methods such as Monte Carlo dropout, deep ensembles, or evidential learning should be evaluated under the same D3B domain-shift protocol.

Third, 3D or multi-slice models should be compared against 2D central-slice approaches.

Fourth, external datasets with compatible four-class labels should be sought to allow full external accuracy and calibration evaluation.

Finally, reliability claims should be connected to clinically meaningful error analysis, including failure modes by tumour type, acquisition protocol, scanner vendor, and MRI sequence.

### Overall conclusion

The study demonstrates that strong internal performance and improved internal calibration do not guarantee cross-dataset reliability. Across three architectures, D1-trained models behaved unstably on visually distinct D3B glioma-domain images. Temperature scaling softened confidence but did not correct prediction distribution under shift.

The strongest conclusion is that brain MRI tumour classification models should not be evaluated by internal accuracy alone. Reliable evaluation requires dataset auditing, calibration analysis, and domain-shift testing before making claims about clinical or external reliability.

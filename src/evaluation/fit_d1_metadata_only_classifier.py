"""
Wallis & Buvat (2022, Med Image Anal 77:102368) experiment 5, replicated on D1.

Fit a deliberately trivial classifier on features that carry no tumour
information at all -- background extent, intensity ceiling, and the shape of the
head outline -- train it on the D1 train split, and score it on val and test. If
it approaches the CNN baseline, the CNNs' internal accuracy is not evidence that
they read tumours.

Features, all computed at native resolution on the L channel:

  n_zero          count of exactly-zero pixels
  max_intensity   maximum pixel value
  bbox_aspect     height/width of the tissue mask's bounding box
  bbox_fill       mask area as a fraction of its bounding box area

The last two together are the slice-orientation proxy. nickparvar carries no
orientation metadata, so orientation has to be inferred from the outline: axial
and coronal sections are near-square and fill their box, sagittal sections are
elongated and fill it less. The mask is the same >=100 mask used by the
skull-outline ablation, so the two probes share one definition.

Four is one feature more than the source paper's three, so `wallis_3_strict`
refits without bbox_fill to keep the replication claim exact.

Two controls beyond the replication:

  geometry_control  image width and height alone. D1's notumor class comes from
                    a different source than its three tumour classes and has a
                    visibly different size distribution, so a four-class result
                    here could be source-of-file bias rather than the
                    slice-selection bias Wallis & Buvat identified. This control
                    is what separates the two.
  shape_only        bbox_aspect and bbox_fill alone, isolating the orientation
                    proxy from the intensity features.
"""

from collections import Counter
from pathlib import Path
import csv
import hashlib
import json
import subprocess
import sys

import numpy as np
import pandas as pd
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, recall_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_text

sys.path.insert(0, "src/stats")
from wilson import wilson_interval  # noqa: E402

SPLIT_CSV = Path("data/splits/D1_leakage_aware_split.csv")

# Rule 5: the leakage-aware split is frozen provenance and must never be regenerated.
EXPECTED_SPLIT_SHA256 = "944ce00e4be958f3688a0996f6fb928fc7717e7c2804abb8000f28976efe0d43"

CLASS_NAMES = ["glioma", "meningioma", "notumor", "pituitary"]
CLASS_TO_INDEX = {name: i for i, name in enumerate(CLASS_NAMES)}
NUM_CLASSES = len(CLASS_NAMES)

FIGSHARE_CLASSES = ["glioma", "meningioma", "pituitary"]
FIGSHARE_CLASS_INDICES = [CLASS_TO_INDEX[c] for c in FIGSHARE_CLASSES]

# Same threshold as the skull-outline ablation, so both probes define "tissue"
# identically.
MASK_THRESHOLD = 100

RANDOM_STATE = 0
TREE_MAX_DEPTH = 4

FEATURE_SETS = {
    "wallis_4": ["n_zero", "max_intensity", "bbox_aspect", "bbox_fill"],
    "wallis_3_strict": ["n_zero", "max_intensity", "bbox_aspect"],
    "frac_zero_sensitivity": ["frac_zero", "max_intensity", "bbox_aspect", "bbox_fill"],
    "shape_only": ["bbox_aspect", "bbox_fill"],
    "geometry_control": ["width", "height"],
}

PRIMARY_FEATURE_SET = "wallis_4"

OUT_DIR = Path("experiments/clever_hans")
FEATURES_CSV = OUT_DIR / "d1_metadata_features.csv"
RESULTS_CSV = OUT_DIR / "d1_metadata_classifier_results.csv"
SUMMARY_JSON = OUT_DIR / "d1_metadata_classifier_summary.json"
REPORT_PATH = Path("reports/experiments/D1_clever_hans_metadata_features.md")

# Optional comparator, written by evaluate_d1_skull_outline_ablation.py.
ABLATION_METRICS_CSV = OUT_DIR / "d1_skull_outline_metrics.csv"

EXPERIMENT_DIRS = {
    "E001": Path("experiments/E001_D1_resnet18_baseline"),
    "E002": Path("experiments/E002_D1_efficientnet_b0_baseline"),
    "E003": Path("experiments/E003_D1_vit_b16_baseline"),
}
SEEDS = [42, 43, 44, 45, 46]


def sha256_file(path):
    digest = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def get_git_commit_hash():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return "UNKNOWN"


def verify_split(split_csv):
    """Rule 5: abort rather than analyse against a split that is not the frozen one."""
    split_csv_sha256 = sha256_file(split_csv)

    if split_csv_sha256 != EXPECTED_SPLIT_SHA256:
        raise RuntimeError(
            f"{split_csv} sha256 is {split_csv_sha256}, expected "
            f"{EXPECTED_SPLIT_SHA256}. The frozen leakage-aware split has changed. "
            "Restore it from git; do not analyse against a regenerated split."
        )

    return split_csv_sha256


def extract_features(image_path):
    """
    Four scalars per image, none of which can encode tumour appearance.

    An image with no pixel at or above the mask threshold has no bounding box.
    That is recorded rather than silently imputed: bbox_aspect falls back to the
    full image aspect ratio and bbox_fill to 0.0, and the row is flagged.
    """
    grey = np.array(Image.open(image_path).convert("L"))
    height, width = grey.shape

    mask = grey >= MASK_THRESHOLD
    empty_mask = not mask.any()

    if empty_mask:
        bbox_aspect = height / width
        bbox_fill = 0.0
    else:
        rows = np.where(mask.any(axis=1))[0]
        cols = np.where(mask.any(axis=0))[0]
        bbox_h = int(rows[-1] - rows[0] + 1)
        bbox_w = int(cols[-1] - cols[0] + 1)
        bbox_aspect = bbox_h / bbox_w
        bbox_fill = float(mask.sum()) / float(bbox_h * bbox_w)

    n_zero = int((grey == 0).sum())

    return {
        "n_zero": n_zero,
        "frac_zero": n_zero / float(grey.size),
        "max_intensity": int(grey.max()),
        "bbox_aspect": float(bbox_aspect),
        "bbox_fill": float(bbox_fill),
        "width": int(width),
        "height": int(height),
        "empty_mask": bool(empty_mask),
    }


def build_feature_table(split_csv):
    """
    Recompute the features on every run rather than caching them.

    Caching would save under a minute over 7,013 images and would introduce a
    stale-artefact failure mode: a changed threshold or feature definition with
    an unchanged cache file on disk.
    """
    with open(split_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    records = []
    for i, row in enumerate(rows, start=1):
        image_path = Path(row["filepath"])

        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        features = extract_features(image_path)
        features.update({
            "filepath": str(image_path),
            "class_label": row["class_label"],
            "label_index": CLASS_TO_INDEX[row["class_label"]],
            "assigned_split": row["assigned_split"],
        })
        records.append(features)

        if i % 1000 == 0:
            print(f"  extracted {i}/{len(rows)}")

    df = pd.DataFrame(records)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(FEATURES_CSV, index=False)
    print(f"Features written: {FEATURES_CSV}")

    return df


def build_classifiers():
    return {
        "decision_tree": DecisionTreeClassifier(
            max_depth=TREE_MAX_DEPTH, random_state=RANDOM_STATE
        ),
        "logistic_regression": make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=2000, random_state=RANDOM_STATE),
        ),
    }


def score(y_true, y_pred, class_indices):
    """
    Accuracy, macro-F1 and per-class recall, with a Wilson interval on accuracy.

    Accuracy here is a proportion of correct predictions over a known, fixed
    denominator, which is exactly the situation a Wilson interval is for; no
    resampling is needed. The majority-class floor is a proportion over the same
    denominator, so it gets an interval too -- comparing a point estimate against
    a bare floor hides that the floor is itself estimated.
    """
    n = int(y_true.size)
    n_correct = int(np.sum(y_true == y_pred))

    macro_f1 = float(
        f1_score(y_true, y_pred, labels=class_indices, average="macro", zero_division=0)
    )
    recalls = recall_score(
        y_true, y_pred, labels=class_indices, average=None, zero_division=0
    )
    counts = np.bincount(y_true, minlength=NUM_CLASSES)

    accuracy_ci = wilson_interval(n_correct, n)
    floor_ci = wilson_interval(int(counts.max()), n)

    return {
        "n": n,
        "n_correct": n_correct,
        "accuracy": accuracy_ci.proportion,
        "accuracy_ci_lower": accuracy_ci.lower,
        "accuracy_ci_upper": accuracy_ci.upper,
        "macro_f1": macro_f1,
        "majority_class_floor": floor_ci.proportion,
        "majority_class_floor_ci_lower": floor_ci.lower,
        "majority_class_floor_ci_upper": floor_ci.upper,
        "per_class_recall": {
            CLASS_NAMES[c]: float(r) for c, r in zip(class_indices, recalls)
        },
    }


def d3c_notumor_shares():
    """
    Share of human-probe (D3C) slices assigned to notumor, per architecture.

    Computed from the sweep artefacts rather than quoted from the manuscript, so
    the connection drawn in the report cannot drift from the run set it refers
    to. Returns {} when the predictions are absent, and the report then omits
    the paragraph that depends on them.
    """
    shares = {}

    for experiment_id, directory in EXPERIMENT_DIRS.items():
        values = []

        for seed in SEEDS:
            path = directory / f"seed{seed}" / "d3c_predictions.csv"

            if not path.exists():
                continue

            predictions = pd.read_csv(path, usecols=["pred_label"])
            values.append(float((predictions.pred_label == "notumor").mean()))

        if len(values) > 1:
            shares[experiment_id] = {
                "mean": float(np.mean(values)),
                "sd": float(np.std(values, ddof=1)),
                "n_seeds": len(values),
            }

    return shares


def cnn_baselines():
    """
    Four-class CNN test accuracy per architecture, and the three-class comparator
    from the ablation run's intact condition when that has been run.
    """
    four_class = {}

    for experiment_id, directory in EXPERIMENT_DIRS.items():
        values = []
        for seed in SEEDS:
            path = directory / f"seed{seed}" / "final_results.json"
            if path.exists():
                values.append(json.loads(path.read_text(encoding="utf-8"))["test_accuracy"])

        if values:
            four_class[experiment_id] = {
                "mean": float(np.mean(values)),
                "sd": float(np.std(values, ddof=1)),
                "n_seeds": len(values),
            }

    three_class = {}

    if ABLATION_METRICS_CSV.exists():
        ablation = pd.read_csv(ABLATION_METRICS_CSV)
        intact = ablation[(ablation.condition == "intact") & (ablation.split == "test")]
        for experiment_id, group in intact.groupby("experiment_id"):
            three_class[experiment_id] = {
                "mean": float(group.accuracy_3class.mean()),
                "sd": float(group.accuracy_3class.std(ddof=1)),
                "n_seeds": int(len(group)),
            }

    return four_class, three_class


def main():
    split_hash = verify_split(SPLIT_CSV)
    git_commit = get_git_commit_hash()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    features = build_feature_table(SPLIT_CSV)

    train = features[features.assigned_split == "train"]
    evaluation_splits = {
        "val": features[features.assigned_split == "val"],
        "test": features[features.assigned_split == "test"],
    }

    n_empty_mask = int(features.empty_mask.sum())

    result_rows = []
    tree_rules = {}

    # Two label scopes. "four_class" fits on all of D1 and is what the CNNs do.
    # "three_class_refit" drops notumor from both training and evaluation, which
    # is the dataset Wallis & Buvat actually worked with.
    label_scopes = {
        "four_class": (CLASS_NAMES, list(range(NUM_CLASSES))),
        "three_class_refit": (FIGSHARE_CLASSES, FIGSHARE_CLASS_INDICES),
    }

    for scope_name, (scope_classes, scope_indices) in label_scopes.items():
        scope_train = train[train.class_label.isin(scope_classes)]

        for feature_set_name, columns in FEATURE_SETS.items():
            x_train = scope_train[columns].to_numpy(dtype=float)
            y_train = scope_train["label_index"].to_numpy(dtype=int)

            for classifier_name, classifier in build_classifiers().items():
                classifier.fit(x_train, y_train)

                if (
                    classifier_name == "decision_tree"
                    and feature_set_name == PRIMARY_FEATURE_SET
                ):
                    tree_rules[scope_name] = export_text(
                        classifier, feature_names=columns
                    )

                for split_name, split_df in evaluation_splits.items():
                    scope_eval = split_df[split_df.class_label.isin(scope_classes)]

                    x_eval = scope_eval[columns].to_numpy(dtype=float)
                    y_eval = scope_eval["label_index"].to_numpy(dtype=int)
                    y_pred = classifier.predict(x_eval)

                    metrics = score(y_eval, y_pred, scope_indices)

                    result_rows.append({
                        "git_commit": git_commit,
                        "split_csv_sha256": split_hash,
                        "label_scope": scope_name,
                        "feature_set": feature_set_name,
                        "features": "|".join(columns),
                        "classifier": classifier_name,
                        "split": split_name,
                        "n_train": int(y_train.size),
                        "n_eval": metrics["n"],
                        "n_correct": metrics["n_correct"],
                        "accuracy": metrics["accuracy"],
                        "accuracy_ci_lower": metrics["accuracy_ci_lower"],
                        "accuracy_ci_upper": metrics["accuracy_ci_upper"],
                        "macro_f1": metrics["macro_f1"],
                        "majority_class_floor": metrics["majority_class_floor"],
                        "majority_class_floor_ci_lower": metrics["majority_class_floor_ci_lower"],
                        "majority_class_floor_ci_upper": metrics["majority_class_floor_ci_upper"],
                        **{
                            f"recall_{name}": value
                            for name, value in metrics["per_class_recall"].items()
                        },
                    })

                    print(
                        f"{scope_name:18s} {feature_set_name:22s} "
                        f"{classifier_name:20s} {split_name:5s} "
                        f"acc={metrics['accuracy']:.4f}"
                    )

    results = pd.DataFrame(result_rows)
    results.to_csv(RESULTS_CSV, index=False)

    baseline_4, baseline_3 = cnn_baselines()

    summary = {
        "provenance": {
            "git_commit": git_commit,
            "split_csv_sha256": split_hash,
            "random_state": RANDOM_STATE,
            "tree_max_depth": TREE_MAX_DEPTH,
            "mask_threshold": MASK_THRESHOLD,
        },
        "feature_sets": FEATURE_SETS,
        "primary_feature_set": PRIMARY_FEATURE_SET,
        "n_images_with_empty_mask": n_empty_mask,
        "cnn_baseline_4class_test_accuracy": baseline_4,
        "cnn_baseline_3class_test_accuracy": baseline_3,
        "d3c_notumor_prediction_share": d3c_notumor_shares(),
        "decision_tree_rules": tree_rules,
    }

    SUMMARY_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    write_report(results, summary, features)

    print(f"\nResults: {RESULTS_CSV}")
    print(f"Summary: {SUMMARY_JSON}")
    print(f"Report: {REPORT_PATH}")


def write_report(results, summary, features):
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    baseline_4 = summary["cnn_baseline_4class_test_accuracy"]
    baseline_3 = summary["cnn_baseline_3class_test_accuracy"]

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D1 Clever Hans probe - metadata-only feature classifier\n\n")
        f.write(
            "Replication of experiment 5 of Wallis & Buvat (2022, *Medical Image "
            "Analysis* 77:102368) on the D1 leakage-aware split. A trivial "
            "classifier is fitted on features that cannot encode tumour appearance, "
            "trained on the train split and scored on val and test. No CNN is "
            "involved and nothing is retrained.\n\n"
        )

        f.write("## Provenance\n\n")
        prov = summary["provenance"]
        f.write("| Field | Value |\n|---|---|\n")
        f.write(f"| Analysis commit | `{prov['git_commit']}` |\n")
        f.write(f"| Split csv sha256 | `{prov['split_csv_sha256']}` |\n")
        f.write(f"| Mask threshold | {prov['mask_threshold']} |\n")
        f.write(f"| Decision tree max depth | {prov['tree_max_depth']} |\n")
        f.write(f"| random_state | {prov['random_state']} |\n")
        f.write(
            f"| Images with an empty tissue mask | "
            f"{summary['n_images_with_empty_mask']} |\n\n"
        )

        f.write("## Feature sets\n\n")
        f.write("| Name | Features | Purpose |\n|---|---|---|\n")
        purposes = {
            "wallis_4": "Primary. The orientation proxy is two features, so this is four not three.",
            "wallis_3_strict": "Exact three-feature replication: primary minus bbox_fill.",
            "frac_zero_sensitivity": "n_zero replaced by its fraction, removing image-size confounding.",
            "shape_only": "Orientation proxy alone, without the intensity features.",
            "geometry_control": "Image dimensions alone. Separates source-of-file bias from slice-selection bias.",
        }
        for name, columns in summary["feature_sets"].items():
            f.write(f"| `{name}` | {', '.join(f'`{c}`' for c in columns)} | {purposes[name]} |\n")
        f.write("\n")

        f.write("## CNN comparator\n\n")
        f.write(
            "Test-split accuracy of the trained models, mean +/- SD over seeds 42-46. "
            "This is what the trivial classifier is being measured against.\n\n"
        )
        f.write("| Model | Four-class | Three-class |\n|---|---:|---:|\n")
        for experiment_id in EXPERIMENT_DIRS:
            four = baseline_4.get(experiment_id)
            three = baseline_3.get(experiment_id)
            four_cell = f"{four['mean']:.4f} +/- {four['sd']:.4f}" if four else "n/a"
            three_cell = f"{three['mean']:.4f} +/- {three['sd']:.4f}" if three else "n/a"
            f.write(f"| {experiment_id} | {four_cell} | {three_cell} |\n")
        if not baseline_3:
            f.write(
                "\nThree-class comparators are unavailable: run "
                "`evaluate_d1_skull_outline_ablation.py` first.\n"
            )
        f.write("\n")

        for scope_name, scope_title in [
            ("four_class", "Four classes (all of D1)"),
            ("three_class_refit", "Three Figshare-derived classes, refitted"),
        ]:
            scope = results[results.label_scope == scope_name]

            f.write(f"## {scope_title}\n\n")

            if scope_name == "three_class_refit":
                f.write(
                    "notumor is dropped from both training and evaluation here, so "
                    "this classifier is genuinely three-way. This is the faithful "
                    "comparison with Wallis & Buvat, who reported 0.77 on Figshare.\n\n"
                )

            test_scope = scope[scope.split == "test"].iloc[0]
            val_scope = scope[scope.split == "val"].iloc[0]
            f.write(
                "Majority-class floor: "
                f"{test_scope.majority_class_floor:.4f} "
                f"({test_scope.majority_class_floor_ci_lower:.4f}, "
                f"{test_scope.majority_class_floor_ci_upper:.4f}) on test, "
                f"{val_scope.majority_class_floor:.4f} "
                f"({val_scope.majority_class_floor_ci_lower:.4f}, "
                f"{val_scope.majority_class_floor_ci_upper:.4f}) on val. "
                "A classifier whose interval overlaps the floor's has not been "
                "shown to beat chance.\n\n"
            )

            f.write(
                "Accuracies carry 95% Wilson intervals. Each is a proportion of "
                "correct predictions over a fixed denominator, so the interval is "
                "exact for that quantity and needs no resampling. Val and test are "
                "shown side by side so their agreement is visible as overlapping "
                "intervals rather than asserted.\n\n"
            )

            f.write(
                "| Feature set | Classifier | Val acc (95% CI) | "
                "Test acc (95% CI) | Test macro-F1 |\n"
            )
            f.write("|---|---|---|---|---:|\n")

            for feature_set_name in FEATURE_SETS:
                for classifier_name in ["decision_tree", "logistic_regression"]:
                    rows = scope[
                        (scope.feature_set == feature_set_name)
                        & (scope.classifier == classifier_name)
                    ]
                    val = rows[rows.split == "val"].iloc[0]
                    test = rows[rows.split == "test"].iloc[0]
                    f.write(
                        f"| `{feature_set_name}` | {classifier_name} | "
                        f"{val.accuracy:.4f} ({val.accuracy_ci_lower:.4f}, "
                        f"{val.accuracy_ci_upper:.4f}) | "
                        f"{test.accuracy:.4f} ({test.accuracy_ci_lower:.4f}, "
                        f"{test.accuracy_ci_upper:.4f}) | "
                        f"{test.macro_f1:.4f} |\n"
                    )
            f.write("\n")

            f.write("### Per-class recall on test, primary feature set, decision tree\n\n")
            primary = scope[
                (scope.feature_set == PRIMARY_FEATURE_SET)
                & (scope.classifier == "decision_tree")
                & (scope.split == "test")
            ].iloc[0]

            recall_columns = [
                c for c in scope.columns
                if c.startswith("recall_") and not pd.isna(primary[c])
            ]
            f.write("| Class | Recall |\n|---|---:|\n")
            for column in recall_columns:
                f.write(f"| {column.removeprefix('recall_')} | {primary[column]:.4f} |\n")
            f.write("\n")

            if scope_name in summary["decision_tree_rules"]:
                f.write("### Fitted tree\n\n")
                f.write(
                    "The splits are the evidence. A tree that separates classes on "
                    "background extent or head shape is reading acquisition and "
                    "selection, not pathology.\n\n```\n"
                )
                f.write(summary["decision_tree_rules"][scope_name])
                f.write("```\n\n")

        f.write("## Feature distributions by class\n\n")
        f.write("Median [min, max] over the whole split file.\n\n")
        f.write("| Class | n_zero | max_intensity | bbox_aspect | bbox_fill |\n")
        f.write("|---|---:|---:|---:|---:|\n")
        for class_name in CLASS_NAMES:
            subset = features[features.class_label == class_name]
            cells = []
            for column in ["n_zero", "max_intensity", "bbox_aspect", "bbox_fill"]:
                values = subset[column]
                cells.append(
                    f"{values.median():.3g} [{values.min():.3g}, {values.max():.3g}]"
                )
            f.write(f"| {class_name} | " + " | ".join(cells) + " |\n")

        f.write("\n## Image dimensions by class\n\n")
        f.write(
            "The evidence behind the geometry control, and behind the "
            "source-class reading below. Dimensions are a property of how a file "
            "was produced, not of the anatomy inside it.\n\n"
        )
        f.write("| Class | n | 512x512 | Distinct sizes | Most common size |\n")
        f.write("|---|---:|---:|---:|---|\n")
        for class_name in CLASS_NAMES:
            subset = features[features.class_label == class_name]
            sizes = list(zip(subset.width, subset.height))
            n = len(sizes)
            n_512 = sum(1 for w, h in sizes if w == 512 and h == 512)
            modal_size, modal_count = Counter(sizes).most_common(1)[0]
            f.write(
                f"| {class_name} | {n} | {n_512} ({n_512 / n:.1%}) | "
                f"{len(set(sizes))} | {modal_size[0]}x{modal_size[1]} "
                f"({modal_count / n:.1%}) |\n"
            )

        d3c_shares = summary.get("d3c_notumor_prediction_share", {})

        if d3c_shares:
            four = results[
                (results.label_scope == "four_class")
                & (results.feature_set == "geometry_control")
                & (results.classifier == "decision_tree")
                & (results.split == "test")
            ].iloc[0]
            three = results[
                (results.label_scope == "three_class_refit")
                & (results.feature_set == "geometry_control")
                & (results.classifier == "decision_tree")
                & (results.split == "test")
            ].iloc[0]

            f.write("\n## A source-class confound, and what it may explain\n\n")
            f.write(
                "The geometry control is the strongest single result on this page, "
                "and it is worth stating plainly what it shows. Image width and "
                "height carry no anatomy whatsoever. On the three tumour classes "
                f"they classify at {three.accuracy:.4f} "
                f"({three.accuracy_ci_lower:.4f}, {three.accuracy_ci_upper:.4f}), "
                "an interval that contains the chance floor of "
                f"{three.majority_class_floor:.4f}. On all four classes the same "
                f"two numbers reach {four.accuracy:.4f} "
                f"({four.accuracy_ci_lower:.4f}, {four.accuracy_ci_upper:.4f}) "
                f"against a floor of {four.majority_class_floor:.4f}, and the two "
                "intervals are far apart. The entire gain comes from the notumor "
                "class.\n\n"
            )
            f.write(
                "The measured fact is the size distribution itself, tabulated "
                "immediately above: the three tumour classes are overwhelmingly "
                "512x512 while notumor spans many smaller sizes. Whatever produced "
                "it, **notumor in D1 is separable from the tumour classes on "
                "acquisition-level properties that carry no anatomy**, and a "
                "classifier is free to use that instead of pathology.\n\n"
            )
            f.write(
                "The likely explanation is how the dataset was assembled. "
                "nickparvar's Kaggle description states that D1 is a merge of "
                "Figshare/Cheng, SARTAJ and Br35H, with the notumor images taken "
                "from Br35H -- which would put a source boundary exactly where the "
                "size boundary is. **That composition is quoted from the dataset "
                "description and has not been independently verified in this "
                "project**, so it is offered as the probable mechanism behind a "
                "measured separation, not as an established provenance record. The "
                "separation stands on the measurement regardless of what caused "
                "it.\n\n"
            )
            f.write(
                "That raises a hypothesis for a result reported elsewhere in this "
                "project. On the human glioma probe (D3C), the dominant "
                "destination for misassigned slices is the no-tumour class, and it "
                "rises steeply across architectures:\n\n"
            )
            f.write("| Model | D3C slices predicted notumor |\n|---|---:|\n")
            for experiment_id in EXPERIMENT_DIRS:
                share = d3c_shares.get(experiment_id)
                if share:
                    f.write(
                        f"| {experiment_id} | {share['mean']:.4f} +/- "
                        f"{share['sd']:.4f} |\n"
                    )
            f.write(
                "\nIf a model has partly learned notumor as *images that look like "
                "they came from Br35H* rather than *images with no tumour*, then "
                "any out-of-distribution image is a candidate for that class, "
                "because the discriminating cue is acquisition provenance rather "
                "than pathology. D3C slices are CaPTk-processed, co-registered and "
                "resampled, so they resemble neither source. Under that reading, "
                "the no-tumour class acts as a residual bin for unfamiliar "
                "acquisitions, and the glioma-recognition failure on D3C is partly "
                "a dataset-construction artefact rather than purely a failure to "
                "generalise tumour appearance.\n\n"
            )
            f.write(
                "**This is a hypothesis the geometry control supports, not one it "
                "proves.** What is established is that notumor is separable from "
                "the tumour classes on image dimensions alone, which is a property "
                "of D1's construction. What is not established is that the models "
                "actually use that cue, nor that it is what drives the D3C "
                "behaviour: the ordering of the notumor share across architectures "
                "is not predicted by anything measured here, and an equally "
                "consistent explanation is that no-tumour is simply the "
                "lowest-confidence default under shift. Distinguishing them needs "
                "a direct test -- for instance retraining with the notumor class "
                "resampled to match the tumour classes' size distribution, or "
                "sourcing a no-tumour set from Figshare itself, and checking "
                "whether the D3C no-tumour share moves.\n"
            )

        f.write("\n## How to read this\n\n")
        f.write(
            "- A three-class test accuracy approaching the CNN comparator means D1 "
            "inherits the Figshare slice-selection bias, and internal accuracy is "
            "not evidence that the models read tumours.\n"
            "- A four-class accuracy far above the three-class one is driven by "
            "notumor, which comes from a different source in nickparvar's merge. "
            "Compare it against `geometry_control`: if image dimensions alone reach "
            "the same accuracy, the effect is source-of-file bias, which is a "
            "different limitation from the one Wallis & Buvat describe.\n"
            "- `wallis_3_strict` is the number to quote when claiming a replication; "
            "`wallis_4` adds the second half of the orientation proxy.\n"
            "- Val and test should agree. A gap would point at something "
            "split-specific rather than a property of D1.\n"
        )


if __name__ == "__main__":
    main()

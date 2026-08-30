"""
Wallis & Buvat (2022, Med Image Anal 77:102368) experiment 4, replicated on D1.

Binarise every D1 image to a skull/tissue outline -- pixels below 100 go to 0,
the rest to 255 -- which erases all internal tissue structure, and evaluate the
15 frozen checkpoints on it without retraining. If accuracy survives the
ablation, the models are reading something other than tumour appearance.

Two deviations from the source paper, both deliberate:

  * The paper works on Figshare/Cheng, which is glioma/meningioma/pituitary with
    no notumor class. D1 (nickparvar) merges Figshare with a second source for
    notumor. Every metric is therefore reported twice: over all four classes,
    and over the three Figshare-derived tumour classes alone, which is the
    faithful comparison. See the report's interpretation section.
  * Both the val and test splits are evaluated. A dataset-level property should
    appear in both; a discrepancy would point at something split-specific.

The intact condition is run alongside the binarised one and asserted against the
`test_accuracy` recorded in each run's final_results.json. That identity control
is what makes the ablation number meaningful -- without it, a low binarised
accuracy could just as easily mean the harness is loading the wrong thing.

Single script over all 15 checkpoints rather than the per-model duplication used
by the older evaluate_e00X_* scripts: the whole point is a comparison held
identical across architectures, and run_eval_sweep.py already set this precedent.
"""

from pathlib import Path
import csv
import hashlib
import json
import os
import subprocess

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import yaml
from PIL import Image
from sklearn.metrics import f1_score, recall_score
from torch.utils.data import DataLoader, Dataset
from torchvision import models, transforms

SPLIT_CSV = Path("data/splits/D1_leakage_aware_split.csv")

# Rule 5: the leakage-aware split is frozen provenance and must never be regenerated.
EXPECTED_SPLIT_SHA256 = "944ce00e4be958f3688a0996f6fb928fc7717e7c2804abb8000f28976efe0d43"

CLASS_NAMES = ["glioma", "meningioma", "notumor", "pituitary"]
CLASS_TO_INDEX = {name: i for i, name in enumerate(CLASS_NAMES)}
NUM_CLASSES = len(CLASS_NAMES)

# The three Figshare/Cheng-derived classes. notumor comes from a different source
# in nickparvar's merge and is excluded from the faithful replication.
FIGSHARE_CLASS_INDICES = [0, 1, 3]

SEEDS = [42, 43, 44, 45, 46]
SPLITS = ["val", "test"]

# "pixels below 100 -> 0, above -> 1", scaled to 8-bit so the existing eval
# transform (ToTensor + ImageNet normalisation) is reused unchanged.
BINARISE_THRESHOLD = 100

CONDITIONS = ["intact", "skull_outline"]

OUT_DIR = Path("experiments/clever_hans")
PREDICTIONS_CSV = OUT_DIR / "d1_skull_outline_predictions.csv"
METRICS_CSV = OUT_DIR / "d1_skull_outline_metrics.csv"
METRICS_JSON = OUT_DIR / "d1_skull_outline_summary.json"
REPORT_PATH = Path("reports/experiments/D1_clever_hans_skull_outline.md")


def build_resnet18():
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)
    return model


def build_efficientnet_b0():
    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, NUM_CLASSES)
    return model


def build_vit_b16():
    model = models.vit_b_16(weights=None)
    model.heads.head = nn.Linear(model.heads.head.in_features, NUM_CLASSES)
    return model


ARCHITECTURES = [
    {
        "experiment_id": "E001",
        "display_name": "ResNet18",
        "config": Path("configs/E001_D1_resnet18_baseline.yaml"),
        "experiment_dir": Path("experiments/E001_D1_resnet18_baseline"),
        "builder": build_resnet18,
    },
    {
        "experiment_id": "E002",
        "display_name": "EfficientNet-B0",
        "config": Path("configs/E002_D1_efficientnet_b0_baseline.yaml"),
        "experiment_dir": Path("experiments/E002_D1_efficientnet_b0_baseline"),
        "builder": build_efficientnet_b0,
    },
    {
        "experiment_id": "E003",
        "display_name": "ViT-B/16",
        "config": Path("configs/E003_D1_vit_b16_baseline.yaml"),
        "experiment_dir": Path("experiments/E003_D1_vit_b16_baseline"),
        "builder": build_vit_b16,
    },
]


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


def git_tree_is_dirty():
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        )
        return bool(result.stdout.strip())
    except Exception:
        return True


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


def load_split_rows(split_csv):
    with open(split_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    by_split = {"train": [], "val": [], "test": []}

    for row in rows:
        split = row["assigned_split"]
        if split in by_split:
            by_split[split].append(row)

    for split, split_rows in by_split.items():
        if not split_rows:
            raise RuntimeError(f"Split '{split}' is empty in {split_csv}.")

    return by_split


def assert_single_run_set(architectures, seeds):
    """
    Rule 4, adapted. The three models must share a run_id and a split_csv_sha256.

    seed is deliberately NOT asserted equal here: this analysis sweeps all five
    seeds by design, so a single seed cannot identify the comparable set. Every
    output row carries its own seed instead. git_commit is not asserted, for the
    reason given in CLAUDE.md rule 4.
    """
    run_ids = set()
    split_hashes = set()
    provenance = {}

    for arch in architectures:
        for seed in seeds:
            path = arch["experiment_dir"] / f"seed{seed}" / "provenance.json"

            if not path.exists():
                raise FileNotFoundError(f"Provenance not found: {path}")

            with path.open(encoding="utf-8") as f:
                record = json.load(f)

            run_ids.add(record.get("run_id"))
            split_hashes.add(record.get("split_csv_sha256"))
            provenance[(arch["experiment_id"], seed)] = record

    if len(run_ids) != 1:
        raise RuntimeError(
            f"Checkpoints span multiple run_ids: {sorted(map(str, run_ids))}. "
            "Refusing to aggregate across run sets."
        )

    if len(split_hashes) != 1:
        raise RuntimeError(
            f"Checkpoints span multiple split_csv_sha256 values: "
            f"{sorted(map(str, split_hashes))}. Refusing to aggregate."
        )

    split_hash = split_hashes.pop()

    if split_hash != EXPECTED_SPLIT_SHA256:
        raise RuntimeError(
            f"Checkpoints were trained against split {split_hash}, but the frozen "
            f"split hashes to {EXPECTED_SPLIT_SHA256}."
        )

    return run_ids.pop(), split_hash, provenance


class D1AblationDataset(Dataset):
    """
    D1 images, optionally binarised to a tissue outline before the eval transform.

    Binarisation happens at native resolution, so the subsequent bilinear resize
    to 224 reintroduces intermediate values only along mask edges. Those edges
    carry no tissue information; binarising after the resize instead would give a
    strictly two-valued tensor but a mask defined on interpolated pixels.
    """

    def __init__(self, rows, transform, binarise):
        self.rows = rows
        self.transform = transform
        self.binarise = binarise

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, idx):
        row = self.rows[idx]

        image_path = Path(row["filepath"])
        label_name = row["class_label"]

        if label_name not in CLASS_TO_INDEX:
            raise ValueError(f"Unknown class label: {label_name}")

        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        if self.binarise:
            grey = np.array(Image.open(image_path).convert("L"))
            mask = (grey >= BINARISE_THRESHOLD).astype(np.uint8) * 255
            image = Image.fromarray(mask, mode="L").convert("RGB")
        else:
            image = Image.open(image_path).convert("RGB")

        if self.transform is not None:
            image = self.transform(image)

        return image, CLASS_TO_INDEX[label_name], str(image_path)


def build_eval_transform(image_size):
    """Identical to build_transforms()[1] in all three trainers."""
    return transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])


def load_checkpoint(model, checkpoint_path, device):
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

    checkpoint = torch.load(checkpoint_path, map_location=device)

    if not isinstance(checkpoint, dict):
        raise TypeError(f"Unexpected checkpoint type: {type(checkpoint)}")

    for key in ["model_state_dict", "state_dict", "model"]:
        if key in checkpoint:
            model.load_state_dict(checkpoint[key])
            return model

    model.load_state_dict(checkpoint)
    return model


@torch.no_grad()
def run_inference(model, loader, device):
    model.eval()

    all_true = []
    all_pred = []
    all_paths = []

    for images, labels, paths in loader:
        images = images.to(device, non_blocking=True)
        logits = model(images)
        preds = torch.argmax(logits, dim=1)

        all_true.append(labels.numpy())
        all_pred.append(preds.cpu().numpy())
        all_paths.extend(paths)

    return (
        np.concatenate(all_true),
        np.concatenate(all_pred),
        all_paths,
    )


def compute_metrics(y_true, y_pred, class_indices):
    """
    Metrics restricted to images whose true label is in class_indices.

    The model still emits all four classes, so on the three-class subset a
    notumor prediction counts as an error. That is the correct treatment: these
    are four-way models being scored on a subset, not three-way models.
    """
    mask = np.isin(y_true, class_indices)
    subset_true = y_true[mask]
    subset_pred = y_pred[mask]

    if subset_true.size == 0:
        raise ValueError(f"No samples for class indices {class_indices}.")

    accuracy = float(np.mean(subset_true == subset_pred))
    macro_f1 = float(
        f1_score(subset_true, subset_pred, labels=class_indices, average="macro", zero_division=0)
    )
    recalls = recall_score(
        subset_true, subset_pred, labels=class_indices, average=None, zero_division=0
    )

    counts = np.bincount(subset_true, minlength=NUM_CLASSES)
    majority_floor = float(counts.max() / subset_true.size)

    return {
        "n": int(subset_true.size),
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "majority_class_floor": majority_floor,
        "per_class_recall": {
            CLASS_NAMES[c]: float(r) for c, r in zip(class_indices, recalls)
        },
    }


def main():
    split_hash = verify_split(SPLIT_CSV)
    by_split = load_split_rows(SPLIT_CSV)

    run_id, checkpoint_split_hash, provenance_records = assert_single_run_set(
        ARCHITECTURES, SEEDS
    )

    git_commit = get_git_commit_hash()
    tree_dirty = git_tree_is_dirty()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    metric_rows = []
    prediction_frames = []
    identity_checks = []

    for arch in ARCHITECTURES:
        config = yaml.safe_load(arch["config"].read_text(encoding="utf-8"))
        image_size = config["data_loading"]["image_size"]
        batch_size = config["data_loading"]["batch_size"]
        num_workers = config["data_loading"]["num_workers"]

        transform = build_eval_transform(image_size)

        for seed in SEEDS:
            seed_dir = arch["experiment_dir"] / f"seed{seed}"
            checkpoint_path = seed_dir / "best_model.pt"

            model = arch["builder"]()
            model = load_checkpoint(model, checkpoint_path, device).to(device)

            checkpoint_hash = sha256_file(checkpoint_path)

            for split in SPLITS:
                for condition in CONDITIONS:
                    dataset = D1AblationDataset(
                        rows=by_split[split],
                        transform=transform,
                        binarise=(condition == "skull_outline"),
                    )
                    loader = DataLoader(
                        dataset,
                        batch_size=batch_size,
                        shuffle=False,
                        num_workers=num_workers,
                        pin_memory=True,
                    )

                    y_true, y_pred, paths = run_inference(model, loader, device)

                    four_class = compute_metrics(y_true, y_pred, list(range(NUM_CLASSES)))
                    three_class = compute_metrics(y_true, y_pred, FIGSHARE_CLASS_INDICES)

                    # Collapse diagnostic. A model genuinely reading a signal from
                    # the outline spreads its predictions; a model pushed
                    # off-distribution dumps everything into one class. Without
                    # this, a mid-range accuracy under ablation is ambiguous
                    # between the two, and they mean opposite things.
                    shares = np.bincount(y_pred, minlength=NUM_CLASSES) / y_pred.size

                    metric_rows.append({
                        "run_id": run_id,
                        "git_commit": git_commit,
                        "experiment_id": arch["experiment_id"],
                        "architecture": arch["display_name"],
                        "seed": seed,
                        "split": split,
                        "condition": condition,
                        "split_csv_sha256": split_hash,
                        "checkpoint_sha256": checkpoint_hash,
                        "n_4class": four_class["n"],
                        "accuracy_4class": four_class["accuracy"],
                        "macro_f1_4class": four_class["macro_f1"],
                        "majority_floor_4class": four_class["majority_class_floor"],
                        "n_3class": three_class["n"],
                        "accuracy_3class": three_class["accuracy"],
                        "macro_f1_3class": three_class["macro_f1"],
                        "majority_floor_3class": three_class["majority_class_floor"],
                        **{
                            f"recall_{name}": value
                            for name, value in four_class["per_class_recall"].items()
                        },
                        **{
                            f"pred_share_{name}": float(share)
                            for name, share in zip(CLASS_NAMES, shares)
                        },
                        "max_pred_share": float(shares.max()),
                        "modal_pred_class": CLASS_NAMES[int(shares.argmax())],
                    })

                    prediction_frames.append(pd.DataFrame({
                        "run_id": run_id,
                        "experiment_id": arch["experiment_id"],
                        "seed": seed,
                        "split": split,
                        "condition": condition,
                        "filepath": paths,
                        "true_index": y_true,
                        "true_label": [CLASS_NAMES[i] for i in y_true],
                        "pred_index": y_pred,
                        "pred_label": [CLASS_NAMES[i] for i in y_pred],
                    }))

                    if split == "test" and condition == "intact":
                        recorded = json.loads(
                            (seed_dir / "final_results.json").read_text(encoding="utf-8")
                        )["test_accuracy"]
                        delta = abs(four_class["accuracy"] - recorded)

                        identity_checks.append({
                            "experiment_id": arch["experiment_id"],
                            "seed": seed,
                            "recorded_test_accuracy": float(recorded),
                            "reproduced_test_accuracy": four_class["accuracy"],
                            "absolute_delta": float(delta),
                            "passed": bool(delta < 1e-6),
                        })

                    print(
                        f"{arch['experiment_id']} seed{seed} {split:5s} {condition:13s} "
                        f"acc4={four_class['accuracy']:.4f} acc3={three_class['accuracy']:.4f}"
                    )

            del model
            if device.type == "cuda":
                torch.cuda.empty_cache()

    failed = [c for c in identity_checks if not c["passed"]]

    metrics_df = pd.DataFrame(metric_rows)
    metrics_df.to_csv(METRICS_CSV, index=False)
    pd.concat(prediction_frames, ignore_index=True).to_csv(PREDICTIONS_CSV, index=False)

    summary = {
        "provenance": {
            "run_id": run_id,
            "git_commit": git_commit,
            "git_tree_dirty": tree_dirty,
            "seeds": SEEDS,
            "split_csv_sha256": split_hash,
            "checkpoint_split_csv_sha256": checkpoint_split_hash,
            "checkpoint_sha256": {
                f"{exp_id}_seed{seed}": record.get("checkpoint_sha256")
                for (exp_id, seed), record in provenance_records.items()
            },
        },
        "method": {
            "binarise_threshold": BINARISE_THRESHOLD,
            "binarise_stage": "native resolution, before resize",
            "splits": SPLITS,
            "conditions": CONDITIONS,
            "three_class_subset": [CLASS_NAMES[i] for i in FIGSHARE_CLASS_INDICES],
        },
        "identity_control": {
            "checks": identity_checks,
            "all_passed": len(failed) == 0,
        },
    }

    METRICS_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    write_report(metrics_df, summary)

    if failed:
        raise RuntimeError(
            "Identity control FAILED for "
            + ", ".join(f"{c['experiment_id']} seed{c['seed']}" for c in failed)
            + ". The intact condition did not reproduce the recorded test accuracy, so "
            "the ablation numbers describe a harness that does not match training. "
            f"Artefacts were still written to {OUT_DIR} for inspection."
        )

    print(f"\nMetrics: {METRICS_CSV}")
    print(f"Predictions: {PREDICTIONS_CSV}")
    print(f"Summary: {METRICS_JSON}")
    print(f"Report: {REPORT_PATH}")


def _agg(df, experiment_id, split, condition, column):
    sub = df[
        (df.experiment_id == experiment_id)
        & (df.split == split)
        & (df.condition == condition)
    ][column]
    return sub.mean(), sub.std(ddof=1)


def write_report(df, summary):
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    prov = summary["provenance"]
    identity = summary["identity_control"]

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D1 Clever Hans probe - skull-outline ablation\n\n")
        f.write(
            "Replication of experiment 4 of Wallis & Buvat (2022, *Medical Image "
            "Analysis* 77:102368) on the D1 leakage-aware split. Every image is "
            f"binarised at native resolution -- pixels below {BINARISE_THRESHOLD} to 0, "
            "the rest to 255 -- which erases all internal tissue structure while "
            "preserving the head and skull outline. The 15 frozen checkpoints are "
            "evaluated on the result without retraining.\n\n"
        )

        f.write("## Provenance\n\n")
        f.write("| Field | Value |\n|---|---|\n")
        f.write(f"| Checkpoint run set | `{prov['run_id']}` |\n")
        f.write(f"| Analysis commit | `{prov['git_commit']}` |\n")
        f.write(f"| Tree dirty at analysis time | {prov['git_tree_dirty']} |\n")
        f.write(f"| Seeds | {', '.join(str(s) for s in prov['seeds'])} |\n")
        f.write(f"| Split csv sha256 | `{prov['split_csv_sha256']}` |\n")
        f.write(f"| Binarisation threshold | {BINARISE_THRESHOLD} |\n")
        f.write(
            "| Binarisation stage | native resolution, before the 224x224 resize |\n\n"
        )

        f.write("## Identity control\n\n")
        f.write(
            "The intact condition is run through the same harness and compared "
            "against the `test_accuracy` recorded in each run's "
            "`final_results.json`. If these do not match, nothing else on this page "
            "can be trusted.\n\n"
        )
        f.write("| Model | Seed | Recorded | Reproduced | Delta | Pass |\n")
        f.write("|---|---:|---:|---:|---:|:--:|\n")
        for check in identity["checks"]:
            f.write(
                f"| {check['experiment_id']} | {check['seed']} | "
                f"{check['recorded_test_accuracy']:.6f} | "
                f"{check['reproduced_test_accuracy']:.6f} | "
                f"{check['absolute_delta']:.2e} | "
                f"{'yes' if check['passed'] else '**NO**'} |\n"
            )
        f.write(
            f"\n**All identity checks passed: "
            f"{'yes' if identity['all_passed'] else 'NO'}**\n\n"
        )

        for split in SPLITS:
            sub = df[df.split == split]
            floor4 = sub.majority_floor_4class.iloc[0]
            floor3 = sub.majority_floor_3class.iloc[0]

            f.write(f"## {split.capitalize()} split\n\n")
            f.write(
                f"n = {int(sub.n_4class.iloc[0])} four-class, "
                f"{int(sub.n_3class.iloc[0])} three-class. "
                f"Majority-class floor {floor4:.4f} and {floor3:.4f}.\n\n"
            )

            f.write("### Four classes (all of D1)\n\n")
            f.write(
                "| Model | Intact acc | Outline acc | Retained | Intact F1 | Outline F1 |\n"
            )
            f.write("|---|---:|---:|---:|---:|---:|\n")
            for arch in ARCHITECTURES:
                eid = arch["experiment_id"]
                im, isd = _agg(df, eid, split, "intact", "accuracy_4class")
                om, osd = _agg(df, eid, split, "skull_outline", "accuracy_4class")
                ifm, ifsd = _agg(df, eid, split, "intact", "macro_f1_4class")
                ofm, ofsd = _agg(df, eid, split, "skull_outline", "macro_f1_4class")
                f.write(
                    f"| {eid} {arch['display_name']} | {im:.4f} +/- {isd:.4f} | "
                    f"{om:.4f} +/- {osd:.4f} | {om / im:.3f} | "
                    f"{ifm:.4f} +/- {ifsd:.4f} | {ofm:.4f} +/- {ofsd:.4f} |\n"
                )

            f.write("\n### Three Figshare-derived classes (glioma, meningioma, pituitary)\n\n")
            f.write(
                "This is the faithful comparison with Wallis & Buvat, whose dataset "
                "had no notumor class. The models remain four-way, so a notumor "
                "prediction on these images counts as an error.\n\n"
            )
            f.write(
                "| Model | Intact acc | Outline acc | Retained | Intact F1 | Outline F1 |\n"
            )
            f.write("|---|---:|---:|---:|---:|---:|\n")
            for arch in ARCHITECTURES:
                eid = arch["experiment_id"]
                im, isd = _agg(df, eid, split, "intact", "accuracy_3class")
                om, osd = _agg(df, eid, split, "skull_outline", "accuracy_3class")
                ifm, ifsd = _agg(df, eid, split, "intact", "macro_f1_3class")
                ofm, ofsd = _agg(df, eid, split, "skull_outline", "macro_f1_3class")
                f.write(
                    f"| {eid} {arch['display_name']} | {im:.4f} +/- {isd:.4f} | "
                    f"{om:.4f} +/- {osd:.4f} | {om / im:.3f} | "
                    f"{ifm:.4f} +/- {ifsd:.4f} | {ofm:.4f} +/- {ofsd:.4f} |\n"
                )
            f.write("\n")

        f.write("## Per-class recall under the ablation (test split)\n\n")
        f.write(
            "Which classes survive binarisation matters. Retained accuracy "
            "concentrated in one class is a different finding from retained "
            "accuracy spread across all four.\n\n"
        )
        f.write("| Model | Condition | " + " | ".join(CLASS_NAMES) + " |\n")
        f.write("|---|---|" + "---:|" * NUM_CLASSES + "\n")
        for arch in ARCHITECTURES:
            eid = arch["experiment_id"]
            for condition in CONDITIONS:
                cells = []
                for name in CLASS_NAMES:
                    mean, sd = _agg(df, eid, "test", condition, f"recall_{name}")
                    cells.append(f"{mean:.4f} +/- {sd:.4f}")
                f.write(f"| {eid} | {condition} | " + " | ".join(cells) + " |\n")

        f.write("\n## Collapse diagnostic (test split)\n\n")
        f.write(
            "Accuracy alone cannot distinguish two opposite situations: a model "
            "reading a real signal from the outline, and a model pushed "
            "off-distribution that dumps every image into one class. The predicted-"
            "class distribution separates them. Under the intact condition the four "
            "classes are near-equally represented in the test split, so a balanced "
            "prediction distribution is the expectation for a model that is still "
            "discriminating.\n\n"
        )
        f.write(
            "| Model | Condition | "
            + " | ".join(CLASS_NAMES)
            + " | Max share | Modal class |\n"
        )
        f.write("|---|---|" + "---:|" * (NUM_CLASSES + 1) + "---|\n")
        for arch in ARCHITECTURES:
            eid = arch["experiment_id"]
            for condition in CONDITIONS:
                cells = []
                for name in CLASS_NAMES:
                    mean, _ = _agg(df, eid, "test", condition, f"pred_share_{name}")
                    cells.append(f"{mean:.3f}")
                max_share, _ = _agg(df, eid, "test", condition, "max_pred_share")
                modal = df[
                    (df.experiment_id == eid)
                    & (df.split == "test")
                    & (df.condition == condition)
                ].modal_pred_class.mode().iloc[0]
                f.write(
                    f"| {eid} | {condition} | "
                    + " | ".join(cells)
                    + f" | {max_share:.3f} | {modal} |\n"
                )

        collapsed = df[
            (df.split == "test")
            & (df.condition == "skull_outline")
            & (df.max_pred_share > 0.5)
        ]
        f.write(
            f"\n**{len(collapsed)} of "
            f"{len(df[(df.split == 'test') & (df.condition == 'skull_outline')])} "
            "checkpoints put more than half of all test images into a single class "
            "under the ablation.**\n\n"
        )

        f.write("## Per-checkpoint detail\n\n")
        f.write(
            "| Model | Seed | Split | Condition | Acc (4c) | Acc (3c) | F1 (4c) | F1 (3c) |\n"
        )
        f.write("|---|---:|---|---|---:|---:|---:|---:|\n")
        for _, row in df.sort_values(
            ["experiment_id", "seed", "split", "condition"]
        ).iterrows():
            f.write(
                f"| {row.experiment_id} | {row.seed} | {row.split} | {row.condition} | "
                f"{row.accuracy_4class:.4f} | {row.accuracy_3class:.4f} | "
                f"{row.macro_f1_4class:.4f} | {row.macro_f1_3class:.4f} |\n"
            )

        f.write("\n## How to read this\n\n")
        f.write(
            "- Outline accuracy near intact accuracy would mean internal performance "
            "is substantially attributable to something other than tumour "
            "appearance.\n"
            "- Outline accuracy at or below the majority-class floor, **combined with "
            "a collapsed prediction distribution**, means something weaker and "
            "different: the binarised images are simply outside the distribution "
            "these models were trained on. That is a statement about the ablation, "
            "not about D1.\n"
            "- Accuracy *below* the majority floor is the clearest sign of collapse. "
            "A model retaining any usable signal cannot do worse than always naming "
            "the largest class; a model dumping everything into a small class can.\n"
            "- A high four-class number alongside a floor-level three-class number is "
            "**not** slice-selection bias. It indicates the notumor class is "
            "separable on image-level properties, which follows from its coming from a "
            "different source in the merge. See the metadata-feature probe "
            "(`D1_clever_hans_metadata_features.md`) and its geometry control.\n"
            "- The val and test splits should agree. A gap between them would point at "
            "something split-specific rather than a property of D1.\n\n"
        )

        f.write("## Scope limit of this experiment\n\n")
        f.write(
            "These 15 checkpoints were trained on intact images and are evaluated "
            "here on binarised ones without retraining, as specified. That makes this "
            "a weaker test than it may appear, and the direction of the weakness "
            "matters: **a null result here is not evidence that D1 is free of the "
            "bias Wallis & Buvat describe.** Distribution shift alone can destroy "
            "accuracy regardless of what the models were reading, and the collapse "
            "diagnostic above shows whether that is what happened.\n\n"
            "Establishing what a skull outline alone supports on D1 requires training "
            "a classifier on binarised images, which this experiment does not do. The "
            "metadata-feature probe (`D1_clever_hans_metadata_features.md`) does fit "
            "its classifier from scratch on non-tumour features, and is therefore the "
            "load-bearing evidence of the two.\n\n"
            "The full text of Wallis & Buvat (2022) is paywalled and it was not "
            "verified whether their experiment 4 trained on the binarised images or "
            "evaluated pre-trained models on them. If they trained, this experiment "
            "is not a replication of theirs and the two results are not comparable.\n"
        )


if __name__ == "__main__":
    main()

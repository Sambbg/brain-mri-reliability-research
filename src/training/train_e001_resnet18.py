from pathlib import Path
import csv
import hashlib
import json
import os
import random
import shutil
import subprocess
from datetime import datetime
from collections import Counter

# Rule 1: torch.use_deterministic_algorithms(True) requires a deterministic cuBLAS
# workspace on CUDA >= 10.2. It must be set before torch initialises CUDA, so it is
# set at import time rather than inside set_seed(). setdefault leaves an
# operator-supplied value alone.
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

import numpy as np
import pandas as pd
import yaml
from PIL import Image

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report,
)


CONFIG_PATH = Path("configs/E001_D1_resnet18_baseline.yaml")

CLASS_TO_INDEX = {
    "glioma": 0,
    "meningioma": 1,
    "notumor": 2,
    "pituitary": 3,
}

INDEX_TO_CLASS = {v: k for k, v in CLASS_TO_INDEX.items()}

CLASS_NAMES = [INDEX_TO_CLASS[i] for i in range(len(INDEX_TO_CLASS))]

# Rule 2: what this script actually implements. validate_config() asserts the config
# declares the same, so a config key can never describe behaviour that does not run.
DATASET_ID = "D1_nickparvar_kaggle"
ARCHITECTURE = "resnet18"
OPTIMIZER_NAME = "adamw"
MONITOR_METRIC = "val_macro_f1"
MONITOR_MODE = "max"

# Rule 5: the leakage-aware split is frozen provenance and must never be regenerated.
EXPECTED_SPLIT_SHA256 = (
    "944ce00e4be958f3688a0996f6fb928fc7717e7c2804abb8000f28976efe0d43"
)


class BrainMRIDataset(Dataset):
    def __init__(self, rows, transform=None):
        self.rows = rows
        self.transform = transform

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

        image = Image.open(image_path).convert("RGB")
        label = CLASS_TO_INDEX[label_name]

        if self.transform is not None:
            image = self.transform(image)

        return image, label, str(image_path)


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


def ensure_clean_git():
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    )
    if result.stdout.strip():
        raise RuntimeError(
            "Git working tree is not clean. Commit or stash changes before training.\n"
            + result.stdout
        )


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    # Rule 1: training must be deterministic. Never set benchmark=True — cudnn
    # autotuning selects different kernels between runs and destroys bit-level
    # reproducibility, which is the whole point of a frozen run set.
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    torch.use_deterministic_algorithms(True)


def seed_worker(worker_id):
    """Rule 1: give every DataLoader worker a deterministic, distinct RNG stream.

    Train-time augmentation (RandomHorizontalFlip, RandomRotation) runs inside worker
    processes, so without this the augmentation stream varies between runs.
    """
    worker_seed = torch.initial_seed() % 2**32
    np.random.seed(worker_seed)
    random.seed(worker_seed)


def make_generator(seed):
    """Rule 1: explicit, seeded generator so shuffling and worker base seeds are fixed."""
    generator = torch.Generator()
    generator.manual_seed(seed)
    return generator


def load_config(path):
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def sha256_file(path):
    digest = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def get_run_id():
    """Rule 3/4: one declared identifier ties E001, E002 and E003 into a frozen run set."""
    run_id = os.environ.get("RUN_ID", "").strip()

    if not run_id:
        raise RuntimeError(
            "RUN_ID is not set. Declare the frozen run set explicitly, for example:\n"
            "  RUN_ID=2026-08-frozen-a python src/training/train_e001_resnet18.py\n"
            "All three models reported in one table must share a single RUN_ID."
        )

    return run_id


def validate_config(config):
    """Rule 2: every config key must correspond to behaviour this script executes.

    Keys that describe the run but were previously never read are checked here rather
    than deleted, so the config remains a faithful declaration of what ran. Keys that
    were pure duplicates or unimplemented (scheduler, num_epochs, experiment_dir) are
    removed from the config files instead.
    """
    checks = [
        ("dataset.dataset_id", config["dataset"]["dataset_id"], DATASET_ID),
        ("dataset.classes", config["dataset"]["classes"], CLASS_NAMES),
        ("model.architecture", config["model"]["architecture"], ARCHITECTURE),
        (
            "training.optimizer",
            str(config["training"]["optimizer"]).lower(),
            OPTIMIZER_NAME,
        ),
        (
            "training.early_stopping.monitor",
            config["training"]["early_stopping"]["monitor"],
            MONITOR_METRIC,
        ),
        (
            "training.early_stopping.mode",
            config["training"]["early_stopping"]["mode"],
            MONITOR_MODE,
        ),
    ]

    for key, declared, implemented in checks:
        if declared != implemented:
            raise ValueError(
                f"Config/code mismatch for {key}: the config declares {declared!r} "
                f"but this script implements {implemented!r}. Fix one or the other; "
                "a declared key must never be unimplemented."
            )


def verify_split(split_csv):
    """Rule 5: abort rather than train against a split that is not the frozen one."""
    split_csv_sha256 = sha256_file(split_csv)

    if split_csv_sha256 != EXPECTED_SPLIT_SHA256:
        raise RuntimeError(
            f"{split_csv} sha256 is {split_csv_sha256}, expected "
            f"{EXPECTED_SPLIT_SHA256}. The frozen leakage-aware split has changed. "
            "Restore it from git; do not retrain against a regenerated split."
        )

    return split_csv_sha256


def load_split_rows(split_csv):
    with open(split_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    by_split = {
        "train": [],
        "val": [],
        "test": [],
    }

    for row in rows:
        split = row["assigned_split"]
        if split not in by_split:
            raise ValueError(f"Unexpected split: {split}")
        by_split[split].append(row)

    return by_split


def build_transforms(image_size):
    train_transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=10),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])

    eval_transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])

    return train_transform, eval_transform


def build_model(num_classes, pretrained=True):
    weights = models.ResNet18_Weights.IMAGENET1K_V1 if pretrained else None
    model = models.resnet18(weights=weights)

    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)

    return model


def run_epoch(model, loader, criterion, optimizer, device, train_mode):
    if train_mode:
        model.train()
    else:
        model.eval()

    total_loss = 0.0
    all_labels = []
    all_preds = []
    all_probs = []
    all_paths = []

    for images, labels, paths in loader:
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)

        if train_mode:
            optimizer.zero_grad(set_to_none=True)

        with torch.set_grad_enabled(train_mode):
            logits = model(images)
            loss = criterion(logits, labels)

            if train_mode:
                loss.backward()
                optimizer.step()

        probs = torch.softmax(logits.detach(), dim=1)
        preds = torch.argmax(probs, dim=1)

        batch_size = labels.size(0)
        total_loss += loss.item() * batch_size

        all_labels.extend(labels.detach().cpu().numpy().tolist())
        all_preds.extend(preds.detach().cpu().numpy().tolist())
        all_probs.extend(probs.detach().cpu().numpy().tolist())
        all_paths.extend(paths)

    avg_loss = total_loss / len(loader.dataset)

    metrics = compute_metrics(all_labels, all_preds)

    return avg_loss, metrics, all_labels, all_preds, all_probs, all_paths


def compute_metrics(labels, preds):
    return {
        "accuracy": accuracy_score(labels, preds),
        "balanced_accuracy": balanced_accuracy_score(labels, preds),
        "macro_f1": f1_score(labels, preds, average="macro"),
    }


def save_predictions(output_path, labels, preds, probs, paths, run_id):
    rows = []

    for label, pred, prob, path in zip(labels, preds, probs, paths):
        row = {
            "run_id": run_id,
            "filepath": path,
            "true_index": label,
            "true_label": INDEX_TO_CLASS[label],
            "pred_index": pred,
            "pred_label": INDEX_TO_CLASS[pred],
        }

        for idx, class_name in INDEX_TO_CLASS.items():
            row[f"prob_{class_name}"] = prob[idx]

        rows.append(row)

    pd.DataFrame(rows).to_csv(output_path, index=False)


def save_confusion_matrix(output_path, labels, preds, run_id):
    cm = confusion_matrix(labels, preds, labels=list(INDEX_TO_CLASS.keys()))
    df = pd.DataFrame(
        cm,
        index=[f"true_{INDEX_TO_CLASS[i]}" for i in INDEX_TO_CLASS],
        columns=[f"pred_{INDEX_TO_CLASS[i]}" for i in INDEX_TO_CLASS],
    )
    df.insert(0, "run_id", run_id)
    df.to_csv(output_path)


def main():
    ensure_clean_git()
    run_id = get_run_id()

    config = load_config(CONFIG_PATH)
    validate_config(config)

    seed = int(config["training"]["seed"])
    set_seed(seed)

    output_dir = Path(config["outputs"]["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    git_hash = get_git_commit_hash()

    split_csv = config["dataset"]["split_csv"]
    split_csv_sha256 = verify_split(split_csv)

    # Rule 3: the provenance block stamped onto every artefact this script writes.
    # checkpoint_sha256 stays None until the best checkpoint is final; a checkpoint
    # cannot contain its own digest, so the copy saved inside best_model.pt keeps it
    # None by construction and provenance.json carries the authoritative value.
    provenance = {
        "run_id": run_id,
        "git_commit": git_hash,
        "seed": seed,
        "split_csv": str(split_csv),
        "split_csv_sha256": split_csv_sha256,
        "checkpoint_sha256": None,
    }

    # Save config copy and metadata before training.
    shutil.copy2(CONFIG_PATH, output_dir / "config_used.yaml")

    metadata = {
        "experiment_id": config["experiment"]["id"],
        "experiment_name": config["experiment"]["name"],
        "started_at": datetime.now().isoformat(),
        "git_commit_hash": git_hash,
        "config_path": str(CONFIG_PATH),
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "torch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_version": torch.version.cuda,
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "provenance": provenance,
    }

    # Written once here so a crashed run still leaves a record, and rewritten after
    # training with finished_at and the checkpoint digest.
    with (output_dir / "metadata.json").open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    rows_by_split = load_split_rows(split_csv)

    print("Rows by split:")
    for split, rows in rows_by_split.items():
        print(split, len(rows), Counter(row["class_label"] for row in rows))

    image_size = int(config["data_loading"]["image_size"])
    batch_size = int(config["data_loading"]["batch_size"])
    num_workers = int(config["data_loading"]["num_workers"])

    train_transform, eval_transform = build_transforms(image_size)

    train_dataset = BrainMRIDataset(rows_by_split["train"], transform=train_transform)
    val_dataset = BrainMRIDataset(rows_by_split["val"], transform=eval_transform)
    test_dataset = BrainMRIDataset(rows_by_split["test"], transform=eval_transform)

    pin_memory = bool(config["data_loading"]["pin_memory"]) and torch.cuda.is_available()

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory,
        worker_init_fn=seed_worker,
        generator=make_generator(seed),
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
        worker_init_fn=seed_worker,
        generator=make_generator(seed + 1),
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
        worker_init_fn=seed_worker,
        generator=make_generator(seed + 2),
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = build_model(
        num_classes=int(config["model"]["num_classes"]),
        pretrained=bool(config["model"]["pretrained"]),
    ).to(device)

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=float(config["training"]["learning_rate"]),
        weight_decay=float(config["training"]["weight_decay"]),
    )

    epochs = int(config["training"]["epochs"])

    early_stopping_enabled = bool(config["training"]["early_stopping"]["enabled"])
    patience = int(config["training"]["early_stopping"]["patience"])

    best_val_macro_f1 = -1.0
    best_epoch = -1
    epochs_without_improvement = 0

    history = []

    for epoch in range(1, epochs + 1):
        train_loss, train_metrics, *_ = run_epoch(
            model, train_loader, criterion, optimizer, device, train_mode=True
        )

        val_loss, val_metrics, *_ = run_epoch(
            model, val_loader, criterion, optimizer, device, train_mode=False
        )

        record = {
            "run_id": run_id,
            "epoch": epoch,
            "train_loss": train_loss,
            "val_loss": val_loss,
            "train_accuracy": train_metrics["accuracy"],
            "train_balanced_accuracy": train_metrics["balanced_accuracy"],
            "train_macro_f1": train_metrics["macro_f1"],
            "val_accuracy": val_metrics["accuracy"],
            "val_balanced_accuracy": val_metrics["balanced_accuracy"],
            "val_macro_f1": val_metrics["macro_f1"],
        }

        history.append(record)

        print(
            f"Epoch {epoch:03d}/{epochs} | "
            f"train_loss={train_loss:.4f} | "
            f"train_macro_f1={train_metrics['macro_f1']:.4f} | "
            f"val_loss={val_loss:.4f} | "
            f"val_macro_f1={val_metrics['macro_f1']:.4f}"
        )

        current_val_macro_f1 = val_metrics["macro_f1"]

        if current_val_macro_f1 > best_val_macro_f1:
            best_val_macro_f1 = current_val_macro_f1
            best_epoch = epoch
            epochs_without_improvement = 0

            torch.save(
                {
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "best_val_macro_f1": best_val_macro_f1,
                    "config": config,
                    "git_commit_hash": git_hash,
                    "provenance": provenance,
                },
                output_dir / "best_model.pt",
            )
        else:
            epochs_without_improvement += 1

        pd.DataFrame(history).to_csv(output_dir / "metrics_history.csv", index=False)

        if early_stopping_enabled and epochs_without_improvement >= patience:
            print(
                f"Early stopping triggered at epoch {epoch}. "
                f"Best epoch: {best_epoch}, best val macro-F1: {best_val_macro_f1:.4f}"
            )
            break

    # Load best checkpoint for final test evaluation.
    checkpoint = torch.load(output_dir / "best_model.pt", map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])

    # Rule 3: the checkpoint is final from here on, so its digest can be recorded.
    provenance["checkpoint_sha256"] = sha256_file(output_dir / "best_model.pt")

    test_loss, test_metrics, test_labels, test_preds, test_probs, test_paths = run_epoch(
        model, test_loader, criterion, optimizer=None, device=device, train_mode=False
    )

    save_predictions(
        output_dir / "test_predictions.csv",
        test_labels,
        test_preds,
        test_probs,
        test_paths,
        run_id,
    )

    save_confusion_matrix(
        output_dir / "test_confusion_matrix.csv",
        test_labels,
        test_preds,
        run_id,
    )

    report = classification_report(
        test_labels,
        test_preds,
        target_names=[INDEX_TO_CLASS[i] for i in range(len(INDEX_TO_CLASS))],
        output_dict=True,
        zero_division=0,
    )

    final_results = {
        "provenance": provenance,
        "best_epoch": best_epoch,
        "best_val_macro_f1": best_val_macro_f1,
        "test_loss": test_loss,
        "test_accuracy": test_metrics["accuracy"],
        "test_balanced_accuracy": test_metrics["balanced_accuracy"],
        "test_macro_f1": test_metrics["macro_f1"],
        "classification_report": report,
    }

    with (output_dir / "final_results.json").open("w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=2)

    # Rule 3: authoritative sidecar record, complete including the checkpoint digest.
    with (output_dir / "provenance.json").open("w", encoding="utf-8") as f:
        json.dump(provenance, f, indent=2)

    # metrics_history.csv was rewritten every epoch; the final write already carries
    # run_id on every row, so no rewrite is needed here.
    metadata["finished_at"] = datetime.now().isoformat()

    with (output_dir / "metadata.json").open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("\nFinal test results:")
    print(json.dumps(final_results, indent=2))

    print(f"\nOutputs saved to: {output_dir}")
    print(f"Run ID: {run_id}")
    print(f"Checkpoint sha256: {provenance['checkpoint_sha256']}")


if __name__ == "__main__":
    main()

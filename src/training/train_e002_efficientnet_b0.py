from pathlib import Path
import csv
import json
import random
import shutil
import subprocess
from datetime import datetime
from collections import Counter

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


CONFIG_PATH = Path("configs/E002_D1_efficientnet_b0_baseline.yaml")

CLASS_TO_INDEX = {
    "glioma": 0,
    "meningioma": 1,
    "notumor": 2,
    "pituitary": 3,
}

INDEX_TO_CLASS = {v: k for k, v in CLASS_TO_INDEX.items()}


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

    # Improves reproducibility, although exact determinism can reduce speed.
    torch.backends.cudnn.deterministic = False
    torch.backends.cudnn.benchmark = True


def load_config(path):
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


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
    if pretrained:
        weights = models.EfficientNet_B0_Weights.DEFAULT
    else:
        weights = None

    model = models.efficientnet_b0(weights=weights)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)

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


def save_predictions(output_path, labels, preds, probs, paths):
    rows = []

    for label, pred, prob, path in zip(labels, preds, probs, paths):
        row = {
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


def save_confusion_matrix(output_path, labels, preds):
    cm = confusion_matrix(labels, preds, labels=list(INDEX_TO_CLASS.keys()))
    df = pd.DataFrame(
        cm,
        index=[f"true_{INDEX_TO_CLASS[i]}" for i in INDEX_TO_CLASS],
        columns=[f"pred_{INDEX_TO_CLASS[i]}" for i in INDEX_TO_CLASS],
    )
    df.to_csv(output_path)


def main():
    ensure_clean_git()

    config = load_config(CONFIG_PATH)

    seed = int(config["training"]["seed"])
    set_seed(seed)

    output_dir = Path(config["outputs"]["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    git_hash = get_git_commit_hash()

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
    }

    with (output_dir / "metadata.json").open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    split_csv = config["dataset"]["split_csv"]
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
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
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

    test_loss, test_metrics, test_labels, test_preds, test_probs, test_paths = run_epoch(
        model, test_loader, criterion, optimizer=None, device=device, train_mode=False
    )

    save_predictions(
        output_dir / "test_predictions.csv",
        test_labels,
        test_preds,
        test_probs,
        test_paths,
    )

    save_confusion_matrix(
        output_dir / "test_confusion_matrix.csv",
        test_labels,
        test_preds,
    )

    report = classification_report(
        test_labels,
        test_preds,
        target_names=[INDEX_TO_CLASS[i] for i in range(len(INDEX_TO_CLASS))],
        output_dict=True,
        zero_division=0,
    )

    final_results = {
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

    print("\nFinal test results:")
    print(json.dumps(final_results, indent=2))

    print(f"\nOutputs saved to: {output_dir}")


if __name__ == "__main__":
    main()

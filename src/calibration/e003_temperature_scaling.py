from pathlib import Path
import csv
import json
import subprocess
from collections import Counter

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image
from sklearn.metrics import accuracy_score, f1_score, balanced_accuracy_score, log_loss


CONFIG_PATH = Path("configs/E003_D1_vit_b_16_baseline.yaml")
SPLIT_CSV = Path("data/splits/D1_leakage_aware_split.csv")
CHECKPOINT_PATH = Path("experiments/E003_D1_vit_b_16_baseline/best_model.pt")

OUT_DIR = Path("experiments/E003_D1_vit_b_16_baseline")
REPORT_PATH = Path("reports/experiments/E003_D1_temperature_scaling_results.md")

IMAGE_SIZE = 224
BATCH_SIZE = 32
NUM_WORKERS = 4

CLASS_NAMES = ["glioma", "meningioma", "notumor", "pituitary"]

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
            raise ValueError(f"Unknown label: {label_name}")

        if not image_path.exists():
            raise FileNotFoundError(f"Missing image: {image_path}")

        image = Image.open(image_path).convert("RGB")
        label = CLASS_TO_INDEX[label_name]

        if self.transform is not None:
            image = self.transform(image)

        return image, label, str(image_path)


class ModelWithTemperature(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.temperature = nn.Parameter(torch.ones(1) * 1.0)

    def forward(self, x):
        logits = self.model(x)
        return self.temperature_scale(logits)

    def temperature_scale(self, logits):
        temperature = self.temperature.unsqueeze(1).expand(logits.size(0), logits.size(1))
        return logits / temperature


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
            "Git working tree is not clean. Commit/stash changes before calibration.\n"
            + result.stdout
        )


def load_split_rows(split_name):
    with SPLIT_CSV.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    split_rows = [row for row in rows if row["assigned_split"] == split_name]

    if not split_rows:
        raise RuntimeError(f"No rows found for split: {split_name}")

    return split_rows


def build_eval_transform():
    return transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])


def build_model():
    model = models.vit_b_16(weights=None)
    in_features = model.heads.head.in_features
    model.heads.head = nn.Linear(in_features, len(CLASS_NAMES))
    return model


def load_checkpoint_model(device):
    if not CHECKPOINT_PATH.exists():
        raise FileNotFoundError(f"Checkpoint not found: {CHECKPOINT_PATH}")

    model = build_model()
    checkpoint = torch.load(CHECKPOINT_PATH, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()

    return model


def make_loader(split_name):
    rows = load_split_rows(split_name)
    dataset = BrainMRIDataset(rows, transform=build_eval_transform())

    loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=torch.cuda.is_available(),
    )

    return loader


@torch.no_grad()
def collect_logits(model, loader, device):
    all_logits = []
    all_labels = []
    all_paths = []

    model.eval()

    for images, labels, paths in loader:
        images = images.to(device, non_blocking=True)
        logits = model(images)

        all_logits.append(logits.cpu())
        all_labels.append(labels.cpu())
        all_paths.extend(paths)

    logits = torch.cat(all_logits, dim=0)
    labels = torch.cat(all_labels, dim=0)

    return logits, labels, all_paths


def fit_temperature(logits, labels, device):
    temperature_model = nn.Parameter(torch.ones(1, device=device) * 1.0)
    nll_criterion = nn.CrossEntropyLoss()

    logits = logits.to(device)
    labels = labels.to(device)

    optimizer = torch.optim.LBFGS([temperature_model], lr=0.01, max_iter=100)

    def closure():
        optimizer.zero_grad()
        scaled_logits = logits / temperature_model.clamp(min=1e-6)
        loss = nll_criterion(scaled_logits, labels)
        loss.backward()
        return loss

    optimizer.step(closure)

    learned_temperature = float(temperature_model.detach().cpu().item())

    if learned_temperature <= 0:
        raise RuntimeError(f"Invalid learned temperature: {learned_temperature}")

    return learned_temperature


def softmax_np(logits):
    logits = np.asarray(logits, dtype=float)
    logits = logits - np.max(logits, axis=1, keepdims=True)
    exp_logits = np.exp(logits)
    return exp_logits / np.sum(exp_logits, axis=1, keepdims=True)


def expected_calibration_error(y_true, probs, n_bins=15):
    y_true = np.asarray(y_true)
    probs = np.asarray(probs)

    confidences = np.max(probs, axis=1)
    predictions = np.argmax(probs, axis=1)

    bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    rows = []

    for i in range(n_bins):
        lower = bin_boundaries[i]
        upper = bin_boundaries[i + 1]

        if i == 0:
            in_bin = (confidences >= lower) & (confidences <= upper)
        else:
            in_bin = (confidences > lower) & (confidences <= upper)

        count = int(np.sum(in_bin))

        if count == 0:
            rows.append({
                "bin": i + 1,
                "lower": lower,
                "upper": upper,
                "count": 0,
                "accuracy": np.nan,
                "confidence": np.nan,
                "gap": np.nan,
            })
            continue

        bin_acc = np.mean(y_true[in_bin] == predictions[in_bin])
        bin_conf = np.mean(confidences[in_bin])
        gap = abs(bin_acc - bin_conf)

        ece += (count / len(y_true)) * gap

        rows.append({
            "bin": i + 1,
            "lower": lower,
            "upper": upper,
            "count": count,
            "accuracy": bin_acc,
            "confidence": bin_conf,
            "gap": gap,
        })

    return float(ece), pd.DataFrame(rows)


def multiclass_brier_score(y_true, probs, num_classes):
    y_onehot = np.eye(num_classes)[y_true]
    return float(np.mean(np.sum((probs - y_onehot) ** 2, axis=1)))


def compute_metrics(y_true, probs, n_bins=15):
    y_pred = np.argmax(probs, axis=1)
    confidences = np.max(probs, axis=1)

    ece, bins = expected_calibration_error(y_true, probs, n_bins=n_bins)

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro")),
        "mean_confidence": float(np.mean(confidences)),
        "confidence_accuracy_gap": float(np.mean(confidences) - accuracy_score(y_true, y_pred)),
        "ece_15_bins": float(ece),
        "brier_score": multiclass_brier_score(y_true, probs, num_classes=len(CLASS_NAMES)),
        "negative_log_likelihood": float(log_loss(y_true, probs, labels=list(range(len(CLASS_NAMES))))),
    }, bins


def save_predictions(path, y_true, raw_probs, calibrated_probs, paths):
    rows = []

    raw_pred = np.argmax(raw_probs, axis=1)
    cal_pred = np.argmax(calibrated_probs, axis=1)

    for i in range(len(y_true)):
        row = {
            "filepath": paths[i],
            "true_index": int(y_true[i]),
            "true_label": INDEX_TO_CLASS[int(y_true[i])],
            "raw_pred_index": int(raw_pred[i]),
            "raw_pred_label": INDEX_TO_CLASS[int(raw_pred[i])],
            "calibrated_pred_index": int(cal_pred[i]),
            "calibrated_pred_label": INDEX_TO_CLASS[int(cal_pred[i])],
        }

        for idx, class_name in INDEX_TO_CLASS.items():
            row[f"raw_prob_{class_name}"] = float(raw_probs[i, idx])
            row[f"calibrated_prob_{class_name}"] = float(calibrated_probs[i, idx])

        rows.append(row)

    pd.DataFrame(rows).to_csv(path, index=False)


def main():
    ensure_clean_git()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    git_hash = get_git_commit_hash()

    print(f"Device: {device}")
    print(f"Git commit: {git_hash}")

    model = load_checkpoint_model(device)

    val_loader = make_loader("val")
    test_loader = make_loader("test")

    print("Collecting validation logits...")
    val_logits, val_labels, _ = collect_logits(model, val_loader, device)

    print("Collecting test logits...")
    test_logits, test_labels, test_paths = collect_logits(model, test_loader, device)

    print("Fitting temperature on validation logits only...")
    temperature = fit_temperature(val_logits, val_labels, device)

    print(f"Learned temperature: {temperature:.6f}")

    val_logits_np = val_logits.numpy()
    test_logits_np = test_logits.numpy()

    y_val = val_labels.numpy()
    y_test = test_labels.numpy()

    raw_test_probs = softmax_np(test_logits_np)
    calibrated_test_probs = softmax_np(test_logits_np / temperature)

    raw_metrics, raw_bins = compute_metrics(y_test, raw_test_probs, n_bins=15)
    calibrated_metrics, calibrated_bins = compute_metrics(y_test, calibrated_test_probs, n_bins=15)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_bins.to_csv(OUT_DIR / "test_raw_reliability_bins_from_logits.csv", index=False)
    calibrated_bins.to_csv(OUT_DIR / "test_temperature_scaled_reliability_bins.csv", index=False)

    save_predictions(
        OUT_DIR / "test_temperature_scaled_predictions.csv",
        y_test,
        raw_test_probs,
        calibrated_test_probs,
        test_paths,
    )

    result = {
        "experiment": "E003_temperature_scaling",
        "base_experiment": "E003_D1_vit_b_16_baseline",
        "git_commit_hash": git_hash,
        "temperature_fitted_on": "validation_split_only",
        "learned_temperature": temperature,
        "validation_samples": int(len(y_val)),
        "test_samples": int(len(y_test)),
        "raw_test_metrics": raw_metrics,
        "temperature_scaled_test_metrics": calibrated_metrics,
    }

    with (OUT_DIR / "temperature_scaling_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# E003 - Temperature Scaling Calibration Results\n\n")

        f.write("## Experiment\n\n")
        f.write("E003 - ViT-B/16 temperature scaling on D1 leakage-aware split\n\n")

        f.write("## Method\n\n")
        f.write(
            "Temperature scaling was fitted using validation-set logits only. "
            "The learned temperature was then applied to the held-out test set. "
            "The model weights were not retrained.\n\n"
        )

        f.write("## Temperature\n\n")
        f.write(f"- Learned temperature: `{temperature:.6f}`\n\n")

        f.write("## Test Metrics Before and After Temperature Scaling\n\n")
        f.write("| Metric | Raw softmax | Temperature-scaled |\n")
        f.write("|---|---:|---:|\n")

        metric_order = [
            "accuracy",
            "balanced_accuracy",
            "macro_f1",
            "mean_confidence",
            "confidence_accuracy_gap",
            "ece_15_bins",
            "brier_score",
            "negative_log_likelihood",
        ]

        for metric in metric_order:
            f.write(
                f"| {metric} | "
                f"{raw_metrics[metric]:.4f} | "
                f"{calibrated_metrics[metric]:.4f} |\n"
            )

        f.write("\n## Interpretation\n\n")

        raw_ece = raw_metrics["ece_15_bins"]
        cal_ece = calibrated_metrics["ece_15_bins"]
        raw_nll = raw_metrics["negative_log_likelihood"]
        cal_nll = calibrated_metrics["negative_log_likelihood"]
        raw_gap = raw_metrics["confidence_accuracy_gap"]
        cal_gap = calibrated_metrics["confidence_accuracy_gap"]

        if cal_ece < raw_ece:
            f.write(
                f"Temperature scaling reduced ECE from {raw_ece:.4f} to {cal_ece:.4f}. "
            )
        else:
            f.write(
                f"Temperature scaling did not reduce ECE; ECE changed from {raw_ece:.4f} to {cal_ece:.4f}. "
            )

        if cal_nll < raw_nll:
            f.write(
                f"NLL also improved from {raw_nll:.4f} to {cal_nll:.4f}. "
            )
        else:
            f.write(
                f"NLL did not improve; it changed from {raw_nll:.4f} to {cal_nll:.4f}. "
            )

        f.write(
            f"The confidence-accuracy gap changed from {raw_gap:.4f} to {cal_gap:.4f}.\n\n"
        )

        f.write(
            "These results are still internal to D1 and should not be interpreted as "
            "external reliability evidence. The next major test is whether calibration "
            "behaviour changes under cross-dataset evaluation.\n"
        )

    print("\nRaw test metrics:")
    print(json.dumps(raw_metrics, indent=2))

    print("\nTemperature-scaled test metrics:")
    print(json.dumps(calibrated_metrics, indent=2))

    print(f"\nReport saved to: {REPORT_PATH}")
    print(f"Metrics saved to: {OUT_DIR / 'temperature_scaling_metrics.json'}")


if __name__ == "__main__":
    main()

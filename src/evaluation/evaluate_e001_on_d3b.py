from pathlib import Path
import json
import math
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
from PIL import Image

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
import os

# Seed-scoped experiment directory. Training writes to <exp_dir>/seed<N>/, so a
# sweep does not overwrite itself. Set SEED to read a seed other than 42.
SEED_SUBDIR = "seed" + os.environ.get("SEED", "42")


EXPERIMENT_DIR = Path(f"experiments/E001_D1_resnet18_baseline/{SEED_SUBDIR}")
CHECKPOINT_PATH = EXPERIMENT_DIR / "best_model.pt"

D3B_MANIFEST = Path("data/processed/D3B_selected_slices_manifest_phash.csv")

PREDICTIONS_CSV = EXPERIMENT_DIR / "d3b_predictions.csv"
METRICS_JSON = EXPERIMENT_DIR / "d3b_domain_shift_metrics.json"
REPORT_PATH = Path("reports/experiments/E001_D3B_domain_shift_results.md")

CLASS_NAMES = ["glioma", "meningioma", "notumor", "pituitary"]
NUM_CLASSES = len(CLASS_NAMES)

BATCH_SIZE = 32
NUM_WORKERS = 4
IMAGE_SIZE = 224


class D3BSliceDataset(Dataset):
    def __init__(self, manifest_path: Path, transform=None):
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")

        self.df = pd.read_csv(manifest_path)
        self.transform = transform

        if "output_image_path" not in self.df.columns:
            raise ValueError("Manifest missing required column: output_image_path")

        self.df = self.df.reset_index(drop=True)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        image_path = Path(row["output_image_path"])

        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        image = Image.open(image_path).convert("RGB")

        if self.transform is not None:
            image = self.transform(image)

        metadata = row.to_dict()

        return image, metadata


def build_transform():
    return transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])


def build_model():
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)
    return model


def load_checkpoint(model, checkpoint_path: Path, device):
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

    checkpoint = torch.load(checkpoint_path, map_location=device)

    if isinstance(checkpoint, dict):
        possible_keys = [
            "model_state_dict",
            "state_dict",
            "model",
        ]

        loaded = False
        for key in possible_keys:
            if key in checkpoint:
                model.load_state_dict(checkpoint[key])
                loaded = True
                break

        if not loaded:
            # Assume checkpoint itself may be a state_dict-like dictionary.
            model.load_state_dict(checkpoint)
    else:
        raise TypeError(f"Unexpected checkpoint type: {type(checkpoint)}")

    return model


def collate_fn(batch):
    images = torch.stack([item[0] for item in batch])
    metadata = [item[1] for item in batch]
    return images, metadata


def entropy_from_probs(probs):
    probs = np.asarray(probs, dtype=np.float64)
    probs = np.clip(probs, 1e-12, 1.0)
    return float(-np.sum(probs * np.log(probs)))


def run_inference(model, loader, device):
    model.eval()
    prediction_rows = []

    with torch.no_grad():
        for batch_idx, (images, metadata_batch) in enumerate(loader):
            images = images.to(device)

            logits = model(images)
            probs = torch.softmax(logits, dim=1).cpu().numpy()
            logits_np = logits.cpu().numpy()

            for i, metadata in enumerate(metadata_batch):
                sample_probs = probs[i]
                sample_logits = logits_np[i]

                pred_index = int(np.argmax(sample_probs))
                pred_label = CLASS_NAMES[pred_index]
                max_confidence = float(np.max(sample_probs))
                glioma_probability = float(sample_probs[0])
                entropy = entropy_from_probs(sample_probs)

                row = {
                    "dataset_id": metadata.get("dataset_id", ""),
                    "patient_id": metadata.get("patient_id", ""),
                    "study_instance_uid": metadata.get("study_instance_uid", ""),
                    "series_instance_uid": metadata.get("series_instance_uid", ""),
                    "series_description": metadata.get("series_description", ""),
                    "protocol_name": metadata.get("protocol_name", ""),
                    "body_part_examined": metadata.get("body_part_examined", ""),
                    "label": metadata.get("label", ""),
                    "label_source": metadata.get("label_source", ""),
                    "output_image_path": metadata.get("output_image_path", ""),
                    "source_dicom_path": metadata.get("source_dicom_path", ""),
                    "selected_rank": metadata.get("selected_rank", ""),
                    "slice_index_in_sorted_series": metadata.get("slice_index_in_sorted_series", ""),
                    "total_valid_slices_in_series": metadata.get("total_valid_slices_in_series", ""),
                    "pred_index": pred_index,
                    "pred_label": pred_label,
                    "max_confidence": max_confidence,
                    "glioma_probability": glioma_probability,
                    "entropy": entropy,
                }

                for class_idx, class_name in enumerate(CLASS_NAMES):
                    row[f"logit_{class_name}"] = float(sample_logits[class_idx])
                    row[f"prob_{class_name}"] = float(sample_probs[class_idx])

                prediction_rows.append(row)

    return pd.DataFrame(prediction_rows)


def summarise_predictions(pred_df):
    n = len(pred_df)

    prediction_counts = pred_df["pred_label"].value_counts().to_dict()
    prediction_proportions = {
        label: prediction_counts.get(label, 0) / n for label in CLASS_NAMES
    }

    glioma_prediction_rate = prediction_proportions["glioma"]

    metrics = {
        "n_slices": int(n),
        "n_patients": int(pred_df["patient_id"].nunique()),
        "n_series": int(pred_df["series_instance_uid"].nunique()),
        "glioma_prediction_rate": float(glioma_prediction_rate),
        "mean_glioma_probability": float(pred_df["glioma_probability"].mean()),
        "median_glioma_probability": float(pred_df["glioma_probability"].median()),
        "mean_max_confidence": float(pred_df["max_confidence"].mean()),
        "median_max_confidence": float(pred_df["max_confidence"].median()),
        "mean_entropy": float(pred_df["entropy"].mean()),
        "median_entropy": float(pred_df["entropy"].median()),
        "prediction_counts": {
            label: int(prediction_counts.get(label, 0)) for label in CLASS_NAMES
        },
        "prediction_proportions": {
            label: float(prediction_proportions[label]) for label in CLASS_NAMES
        },
    }

    # Patient-level majority prediction summary
    patient_majority = {}
    for patient_id, group in pred_df.groupby("patient_id"):
        counts = group["pred_label"].value_counts()
        majority_label = counts.index[0]
        patient_majority[patient_id] = majority_label

    patient_majority_counts = Counter(patient_majority.values())
    metrics["patient_majority_prediction_counts"] = {
        label: int(patient_majority_counts.get(label, 0)) for label in CLASS_NAMES
    }
    metrics["patient_majority_glioma_rate"] = float(
        patient_majority_counts.get("glioma", 0) / max(len(patient_majority), 1)
    )

    # Series-level majority prediction summary
    series_majority = {}
    for series_uid, group in pred_df.groupby("series_instance_uid"):
        counts = group["pred_label"].value_counts()
        majority_label = counts.index[0]
        series_majority[series_uid] = majority_label

    series_majority_counts = Counter(series_majority.values())
    metrics["series_majority_prediction_counts"] = {
        label: int(series_majority_counts.get(label, 0)) for label in CLASS_NAMES
    }
    metrics["series_majority_glioma_rate"] = float(
        series_majority_counts.get("glioma", 0) / max(len(series_majority), 1)
    )

    return metrics


def write_report(metrics, pred_df):
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    pred_counts = metrics["prediction_counts"]
    pred_props = metrics["prediction_proportions"]

    patient_counts = metrics["patient_majority_prediction_counts"]
    series_counts = metrics["series_majority_prediction_counts"]

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# E001 on D3B Domain-Shift Evaluation\n\n")

        f.write("## Experiment\n\n")
        f.write("E001 ResNet18 trained on D1 leakage-aware split, evaluated on D3B ICDC-Glioma central slices.\n\n")

        f.write("## Inputs\n\n")
        f.write(f"- Checkpoint: `{CHECKPOINT_PATH}`\n")
        f.write(f"- D3B manifest: `{D3B_MANIFEST}`\n")
        f.write(f"- D3B slices evaluated: {metrics['n_slices']}\n")
        f.write(f"- Patients represented: {metrics['n_patients']}\n")
        f.write(f"- Series represented: {metrics['n_series']}\n\n")

        f.write("## Critical Interpretation Rule\n\n")
        f.write(
            "D3B is glioma-focused and does not contain the full D1 four-class label set. "
            "Therefore, this evaluation must not be interpreted as four-class external accuracy. "
            "It is a glioma-focused domain-shift confidence and prediction-distribution analysis.\n\n"
        )

        f.write("## Slice-Level Prediction Distribution\n\n")
        f.write("| Predicted class | Count | Proportion |\n")
        f.write("|---|---:|---:|\n")
        for label in CLASS_NAMES:
            f.write(f"| {label} | {pred_counts[label]} | {pred_props[label]:.4f} |\n")

        f.write("\n## Core D3B Metrics\n\n")
        f.write("| Metric | Value |\n")
        f.write("|---|---:|\n")
        f.write(f"| Glioma prediction rate, slice-level | {metrics['glioma_prediction_rate']:.4f} |\n")
        f.write(f"| Mean glioma probability | {metrics['mean_glioma_probability']:.4f} |\n")
        f.write(f"| Median glioma probability | {metrics['median_glioma_probability']:.4f} |\n")
        f.write(f"| Mean maximum softmax confidence | {metrics['mean_max_confidence']:.4f} |\n")
        f.write(f"| Median maximum softmax confidence | {metrics['median_max_confidence']:.4f} |\n")
        f.write(f"| Mean entropy | {metrics['mean_entropy']:.4f} |\n")
        f.write(f"| Median entropy | {metrics['median_entropy']:.4f} |\n")

        f.write("\n## Patient-Level Majority Prediction\n\n")
        f.write("| Majority predicted class | Patient count |\n")
        f.write("|---|---:|\n")
        for label in CLASS_NAMES:
            f.write(f"| {label} | {patient_counts[label]} |\n")
        f.write(f"\nPatient-level majority glioma rate: `{metrics['patient_majority_glioma_rate']:.4f}`\n")

        f.write("\n## Series-Level Majority Prediction\n\n")
        f.write("| Majority predicted class | Series count |\n")
        f.write("|---|---:|\n")
        for label in CLASS_NAMES:
            f.write(f"| {label} | {series_counts[label]} |\n")
        f.write(f"\nSeries-level majority glioma rate: `{metrics['series_majority_glioma_rate']:.4f}`\n")

        f.write("\n## Example Predictions\n\n")
        f.write("| PatientID | SeriesDescription | Selected rank | Predicted class | Glioma probability | Max confidence | Entropy |\n")
        f.write("|---|---|---:|---|---:|---:|---:|\n")

        for _, row in pred_df.head(30).iterrows():
            f.write(
                f"| {row['patient_id']} | "
                f"{str(row['series_description']).replace('|', '/')} | "
                f"{row['selected_rank']} | "
                f"{row['pred_label']} | "
                f"{row['glioma_probability']:.4f} | "
                f"{row['max_confidence']:.4f} | "
                f"{row['entropy']:.4f} |\n"
            )

        f.write("\n## Interpretation\n\n")
        f.write(
            "This report evaluates whether the D1-trained E001 model recognises D3B glioma-domain images "
            "as glioma and how confident it is under domain shift. Because D3B labels are collection-level "
            "glioma labels rather than slice-level tumour annotations, the results should be interpreted "
            "as domain-shift behaviour, not clinical diagnostic accuracy.\n\n"
        )

        f.write(
            "The next step is to apply the E001 temperature scaling parameter to these D3B logits/probabilities "
            "and compare raw versus calibrated confidence under domain shift.\n"
        )


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    dataset = D3BSliceDataset(D3B_MANIFEST, transform=build_transform())
    loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        collate_fn=collate_fn,
    )

    model = build_model()
    model = load_checkpoint(model, CHECKPOINT_PATH, device)
    model = model.to(device)

    pred_df = run_inference(model, loader, device)

    PREDICTIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    pred_df.to_csv(PREDICTIONS_CSV, index=False)

    metrics = summarise_predictions(pred_df)

    with METRICS_JSON.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    write_report(metrics, pred_df)

    print("D3B evaluation complete.")
    print(json.dumps(metrics, indent=2))
    print(f"Predictions saved to: {PREDICTIONS_CSV}")
    print(f"Metrics saved to: {METRICS_JSON}")
    print(f"Report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()

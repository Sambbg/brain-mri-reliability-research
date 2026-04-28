from pathlib import Path
import csv
from collections import Counter

import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from torchvision import transforms


SPLIT_CSV = Path("data/splits/D1_leakage_aware_split.csv")
IMAGE_SIZE = 224
BATCH_SIZE = 32

CLASS_TO_INDEX = {
    "glioma": 0,
    "meningioma": 1,
    "notumor": 2,
    "pituitary": 3,
}


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

        return image, label


def load_split_rows(split_name):
    with SPLIT_CSV.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    split_rows = [row for row in rows if row["assigned_split"] == split_name]

    if not split_rows:
        raise RuntimeError(f"No rows found for split: {split_name}")

    return split_rows


def main():
    if not SPLIT_CSV.exists():
        raise FileNotFoundError(f"Split CSV not found: {SPLIT_CSV}")

    transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])

    for split_name in ["train", "val", "test"]:
        rows = load_split_rows(split_name)
        dataset = BrainMRIDataset(rows, transform=transform)

        loader = DataLoader(
            dataset,
            batch_size=BATCH_SIZE,
            shuffle=(split_name == "train"),
            num_workers=4,
            pin_memory=torch.cuda.is_available(),
        )

        images, labels = next(iter(loader))

        print(f"\nSplit: {split_name}")
        print(f"Rows: {len(dataset)}")
        print(f"Batch image tensor shape: {images.shape}")
        print(f"Batch label tensor shape: {labels.shape}")
        print(f"Batch labels: {Counter(labels.tolist())}")

        assert images.shape[0] <= BATCH_SIZE
        assert images.shape[1] == 3
        assert images.shape[2] == IMAGE_SIZE
        assert images.shape[3] == IMAGE_SIZE
        assert labels.ndim == 1

    print("\nD1 DataLoader verification passed.")


if __name__ == "__main__":
    main()

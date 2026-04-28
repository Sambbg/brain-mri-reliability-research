from pathlib import Path
import hashlib
import csv
from PIL import Image

DATASET_ID = "D1_nickparvar_kaggle"
RAW_ROOT = Path("data/raw/D1_nickparvar_kaggle")
OUT_PATH = Path("data/processed/D1_manifest.csv")

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def inspect_image(path: Path):
    with Image.open(path) as img:
        return img.width, img.height, img.mode


def main():
    if not RAW_ROOT.exists():
        raise FileNotFoundError(f"Raw dataset folder not found: {RAW_ROOT}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for split_dir in ["Training", "Testing"]:
        split_path = RAW_ROOT / split_dir
        if not split_path.exists():
            raise FileNotFoundError(f"Expected split folder missing: {split_path}")

        for class_dir in sorted([p for p in split_path.iterdir() if p.is_dir()]):
            class_label = class_dir.name

            for image_path in sorted(class_dir.rglob("*")):
                if not image_path.is_file():
                    continue

                extension = image_path.suffix.lower()

                if extension not in VALID_EXTENSIONS:
                    continue

                try:
                    width, height, mode = inspect_image(image_path)
                    file_hash = sha256_file(image_path)

                    rows.append({
                        "dataset_id": DATASET_ID,
                        "split": split_dir,
                        "class_label": class_label,
                        "filepath": str(image_path),
                        "filename": image_path.name,
                        "extension": extension,
                        "file_size_bytes": image_path.stat().st_size,
                        "width": width,
                        "height": height,
                        "mode": mode,
                        "sha256": file_hash,
                    })

                except Exception as exc:
                    rows.append({
                        "dataset_id": DATASET_ID,
                        "split": split_dir,
                        "class_label": class_label,
                        "filepath": str(image_path),
                        "filename": image_path.name,
                        "extension": extension,
                        "file_size_bytes": image_path.stat().st_size,
                        "width": "ERROR",
                        "height": "ERROR",
                        "mode": "ERROR",
                        "sha256": "ERROR",
                        "error": repr(exc),
                    })

    if not rows:
        raise RuntimeError("No image rows were collected. Check dataset path and file extensions.")

    fieldnames = [
        "dataset_id",
        "split",
        "class_label",
        "filepath",
        "filename",
        "extension",
        "file_size_bytes",
        "width",
        "height",
        "mode",
        "sha256",
    ]

    with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Manifest written to: {OUT_PATH}")
    print(f"Rows: {len(rows)}")

    split_counts = {}
    class_counts = {}

    for row in rows:
        split_counts[row["split"]] = split_counts.get(row["split"], 0) + 1
        key = (row["split"], row["class_label"])
        class_counts[key] = class_counts.get(key, 0) + 1

    print("\nSplit counts:")
    for split, count in sorted(split_counts.items()):
        print(f"  {split}: {count}")

    print("\nClass counts:")
    for (split, class_label), count in sorted(class_counts.items()):
        print(f"  {split} / {class_label}: {count}")


if __name__ == "__main__":
    main()

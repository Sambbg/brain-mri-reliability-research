from pathlib import Path
import csv
from PIL import Image
import imagehash

IN_PATH = Path("data/processed/D1_manifest_deduplicated.csv")
OUT_PATH = Path("data/processed/D1_manifest_deduplicated_phash.csv")
REPORT_PATH = Path("reports/datasets/D1_perceptual_hash_report.md")


def load_manifest(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")

    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute_hashes(image_path: Path):
    with Image.open(image_path) as img:
        img = img.convert("L")
        phash = imagehash.phash(img)
        ahash = imagehash.average_hash(img)
        dhash = imagehash.dhash(img)

    return str(phash), str(ahash), str(dhash)


def main():
    rows = load_manifest(IN_PATH)
    output_rows = []

    errors = []

    for i, row in enumerate(rows, start=1):
        image_path = Path(row["filepath"])

        try:
            phash, ahash, dhash = compute_hashes(image_path)
            new_row = dict(row)
            new_row["phash"] = phash
            new_row["ahash"] = ahash
            new_row["dhash"] = dhash
            output_rows.append(new_row)

        except Exception as exc:
            new_row = dict(row)
            new_row["phash"] = "ERROR"
            new_row["ahash"] = "ERROR"
            new_row["dhash"] = "ERROR"
            output_rows.append(new_row)
            errors.append((str(image_path), repr(exc)))

        if i % 1000 == 0:
            print(f"Processed {i}/{len(rows)} images")

    fieldnames = list(output_rows[0].keys())

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    unique_phashes = len({row["phash"] for row in output_rows if row["phash"] != "ERROR"})
    unique_ahashes = len({row["ahash"] for row in output_rows if row["ahash"] != "ERROR"})
    unique_dhashes = len({row["dhash"] for row in output_rows if row["dhash"] != "ERROR"})

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D1 Perceptual Hash Report\n\n")

        f.write("## Input and Output\n\n")
        f.write(f"- Input manifest: `{IN_PATH}`\n")
        f.write(f"- Output manifest: `{OUT_PATH}`\n")
        f.write(f"- Total rows processed: {len(rows)}\n\n")

        f.write("## Hash Methods\n\n")
        f.write("- `phash`: perceptual hash, useful for visually similar image detection.\n")
        f.write("- `ahash`: average hash, simple global appearance hash.\n")
        f.write("- `dhash`: difference hash, edge/gradient-oriented hash.\n\n")

        f.write("## Summary\n\n")
        f.write(f"- Unique pHash values: {unique_phashes}\n")
        f.write(f"- Unique aHash values: {unique_ahashes}\n")
        f.write(f"- Unique dHash values: {unique_dhashes}\n")
        f.write(f"- Errors: {len(errors)}\n\n")

        f.write("## Interpretation\n\n")
        f.write(
            "This report adds perceptual hash values to the exact-deduplicated manifest. "
            "The next step is to compare Hamming distances between pHash values to identify near-duplicate image pairs. "
            "Near-duplicates may indicate repeated slices, resized images, cropped copies, or other leakage risks that exact SHA256 cannot detect.\n"
        )

        if errors:
            f.write("\n## Errors\n\n")
            for path, err in errors:
                f.write(f"- `{path}`: {err}\n")

    print(f"Output written to: {OUT_PATH}")
    print(f"Report written to: {REPORT_PATH}")
    print(f"Rows processed: {len(rows)}")
    print(f"Errors: {len(errors)}")
    print(f"Unique pHash values: {unique_phashes}")


if __name__ == "__main__":
    main()

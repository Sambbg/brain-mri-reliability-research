from pathlib import Path
import csv
import hashlib

import pandas as pd
from PIL import Image

INPUT_MANIFEST = Path("data/processed/D3B_selected_slices_manifest.csv")
OUTPUT_MANIFEST = Path("data/processed/D3B_selected_slices_manifest_phash.csv")
REPORT_PATH = Path("reports/datasets/D3B_perceptual_hash_report.md")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def average_hash(image: Image.Image, hash_size: int = 8) -> str:
    img = image.convert("L").resize((hash_size, hash_size), Image.Resampling.LANCZOS)
    pixels = list(img.getdata())
    avg = sum(pixels) / len(pixels)
    bits = "".join("1" if p > avg else "0" for p in pixels)
    return f"{int(bits, 2):0{hash_size * hash_size // 4}x}"


def difference_hash(image: Image.Image, hash_size: int = 8) -> str:
    img = image.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = list(img.getdata())

    bits = []
    for row in range(hash_size):
        row_start = row * (hash_size + 1)
        for col in range(hash_size):
            left = pixels[row_start + col]
            right = pixels[row_start + col + 1]
            bits.append("1" if left > right else "0")

    bit_string = "".join(bits)
    return f"{int(bit_string, 2):0{hash_size * hash_size // 4}x}"


def perceptual_hash(image: Image.Image, hash_size: int = 8, highfreq_factor: int = 4) -> str:
    """
    Simple pHash implementation using DCT-like transform via scipy if available.
    Falls back to average hash if scipy is unavailable.

    For reproducibility, the report records that this is a lightweight pHash.
    """
    try:
        import numpy as np
        from scipy.fftpack import dct

        img_size = hash_size * highfreq_factor
        img = image.convert("L").resize((img_size, img_size), Image.Resampling.LANCZOS)
        pixels = np.asarray(img, dtype=np.float32)

        dct_rows = dct(pixels, axis=0, norm="ortho")
        dct_full = dct(dct_rows, axis=1, norm="ortho")

        dct_low = dct_full[:hash_size, :hash_size]
        dct_values = dct_low.flatten()

        # Exclude DC coefficient.
        median = np.median(dct_values[1:])
        bits = "".join("1" if value > median else "0" for value in dct_values)

        return f"{int(bits, 2):0{hash_size * hash_size // 4}x}"

    except Exception:
        return average_hash(image, hash_size=hash_size)


def main():
    if not INPUT_MANIFEST.exists():
        raise FileNotFoundError(f"Input manifest not found: {INPUT_MANIFEST}")

    df = pd.read_csv(INPUT_MANIFEST)

    required_cols = ["output_image_path"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column in manifest: {col}")

    rows = []
    errors = []

    for idx, row in df.iterrows():
        if (idx + 1) % 50 == 0:
            print(f"Processed {idx + 1}/{len(df)} images")

        image_path = Path(row["output_image_path"])

        try:
            if not image_path.exists():
                raise FileNotFoundError(f"Image not found: {image_path}")

            with Image.open(image_path) as img:
                phash = perceptual_hash(img)
                ahash = average_hash(img)
                dhash = difference_hash(img)

            row_dict = row.to_dict()
            row_dict["sha256_recomputed"] = sha256_file(image_path)
            row_dict["phash"] = phash
            row_dict["ahash"] = ahash
            row_dict["dhash"] = dhash
            row_dict["hash_error"] = ""

            rows.append(row_dict)

        except Exception as exc:
            row_dict = row.to_dict()
            row_dict["sha256_recomputed"] = ""
            row_dict["phash"] = ""
            row_dict["ahash"] = ""
            row_dict["dhash"] = ""
            row_dict["hash_error"] = repr(exc)
            rows.append(row_dict)
            errors.append((str(image_path), repr(exc)))

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUTPUT_MANIFEST, index=False)

    unique_phash = out_df["phash"].replace("", pd.NA).dropna().nunique()
    unique_ahash = out_df["ahash"].replace("", pd.NA).dropna().nunique()
    unique_dhash = out_df["dhash"].replace("", pd.NA).dropna().nunique()

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D3B Perceptual Hash Report\n\n")

        f.write("## Input and Output\n\n")
        f.write(f"- Input manifest: `{INPUT_MANIFEST}`\n")
        f.write(f"- Output manifest: `{OUTPUT_MANIFEST}`\n")
        f.write(f"- Total rows processed: {len(out_df)}\n")
        f.write(f"- Errors: {len(errors)}\n\n")

        f.write("## Hash Methods\n\n")
        f.write("- `phash`: lightweight perceptual hash based on low-frequency DCT coefficients.\n")
        f.write("- `ahash`: average hash.\n")
        f.write("- `dhash`: difference hash.\n")
        f.write("- `sha256_recomputed`: exact file hash of the converted PNG image.\n\n")

        f.write("## Summary\n\n")
        f.write(f"- Unique pHash values: {unique_phash}\n")
        f.write(f"- Unique aHash values: {unique_ahash}\n")
        f.write(f"- Unique dHash values: {unique_dhash}\n")
        f.write(f"- Hashing errors: {len(errors)}\n\n")

        f.write("## Interpretation\n\n")
        f.write(
            "This report adds exact and perceptual hashes to the D3B converted central-slice manifest. "
            "The next step is to compare D3B against D1 using exact SHA256 overlap and pHash near-overlap checks. "
            "This is required before using D3B for domain-shift evaluation.\n"
        )

        if errors:
            f.write("\n## Errors\n\n")
            for path, err in errors[:100]:
                f.write(f"- `{path}`: {err}\n")

    print(f"Output written to: {OUTPUT_MANIFEST}")
    print(f"Report written to: {REPORT_PATH}")
    print(f"Rows processed: {len(out_df)}")
    print(f"Errors: {len(errors)}")
    print(f"Unique pHash values: {unique_phash}")


if __name__ == "__main__":
    main()

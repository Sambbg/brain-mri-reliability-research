from pathlib import Path
from collections import defaultdict, Counter
import csv
import hashlib

import numpy as np
import pandas as pd
from PIL import Image
import pydicom

RAW_DIR = Path("data/raw/D3B_icdc_glioma")
OUT_DIR = Path("data/processed/D3B_icdc_glioma_selected_slices")
MANIFEST_PATH = Path("data/processed/D3B_selected_slices_manifest.csv")
REPORT_PATH = Path("reports/datasets/D3B_slice_conversion_report.md")

DATASET_ID = "D3B_icdc_glioma"
LABEL = "glioma"
LABEL_SOURCE = "collection_level_icdc_glioma"
SLICES_PER_SERIES = 5


def safe_get(ds, name, default=""):
    value = getattr(ds, name, default)
    if value is None:
        return default
    return str(value)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_valid_dicom(path: Path):
    if path.name.upper() == "LICENSE":
        return None

    try:
        ds = pydicom.dcmread(path, stop_before_pixels=False, force=True)

        if safe_get(ds, "Modality", "") != "MR":
            return None

        if "PixelData" not in ds:
            return None

        arr = ds.pixel_array

        if arr is None:
            return None

        if arr.ndim != 2:
            return None

        return ds

    except Exception:
        return None


def get_sort_key(item):
    path, ds = item

    instance_number = safe_get(ds, "InstanceNumber", "")
    image_position = safe_get(ds, "ImagePositionPatient", "")
    slice_location = safe_get(ds, "SliceLocation", "")

    try:
        return (0, float(instance_number))
    except Exception:
        pass

    if image_position:
        try:
            # DICOM ImagePositionPatient usually has x/y/z. Sort by z if possible.
            parts = [float(x.strip()) for x in str(image_position).replace("[", "").replace("]", "").split(",")]
            if len(parts) >= 3:
                return (1, parts[2])
        except Exception:
            pass

    try:
        return (2, float(slice_location))
    except Exception:
        pass

    return (9, str(path))


def select_central_indices(n: int, k: int):
    if n <= 0:
        return []

    if n <= k:
        return list(range(n))

    center = n // 2
    half = k // 2

    start = center - half
    end = start + k

    if start < 0:
        start = 0
        end = k

    if end > n:
        end = n
        start = n - k

    return list(range(start, end))


def normalize_to_uint8(arr: np.ndarray) -> np.ndarray:
    arr = arr.astype(np.float32)

    # Robust percentile scaling avoids a few extreme pixels dominating.
    low = np.percentile(arr, 1)
    high = np.percentile(arr, 99)

    if high <= low:
        low = float(np.min(arr))
        high = float(np.max(arr))

    if high <= low:
        return np.zeros(arr.shape, dtype=np.uint8)

    arr = np.clip(arr, low, high)
    arr = (arr - low) / (high - low)
    arr = (arr * 255.0).round().astype(np.uint8)

    return arr


def save_png_from_dicom(ds, out_path: Path):
    arr = ds.pixel_array

    # Apply rescale slope/intercept if present.
    slope = float(getattr(ds, "RescaleSlope", 1.0) or 1.0)
    intercept = float(getattr(ds, "RescaleIntercept", 0.0) or 0.0)
    arr = arr.astype(np.float32) * slope + intercept

    arr_uint8 = normalize_to_uint8(arr)

    image = Image.fromarray(arr_uint8, mode="L")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path)


def collect_series():
    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Raw directory not found: {RAW_DIR}")

    series = defaultdict(list)
    total_files = 0
    valid_dicom_files = 0
    skipped_files = 0

    for path in RAW_DIR.rglob("*"):
        if not path.is_file():
            continue

        total_files += 1
        ds = read_valid_dicom(path)

        if ds is None:
            skipped_files += 1
            continue

        valid_dicom_files += 1
        series_uid = safe_get(ds, "SeriesInstanceUID", "UNKNOWN")
        series[series_uid].append((path, ds))

    return series, total_files, valid_dicom_files, skipped_files


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    series, total_files, valid_dicom_files, skipped_files = collect_series()

    manifest_rows = []
    series_summary_rows = []

    for series_uid, items in sorted(series.items()):
        sorted_items = sorted(items, key=get_sort_key)
        n = len(sorted_items)
        selected_indices = select_central_indices(n, SLICES_PER_SERIES)

        if not selected_indices:
            continue

        first_ds = sorted_items[0][1]

        patient_id = safe_get(first_ds, "PatientID", "")
        study_uid = safe_get(first_ds, "StudyInstanceUID", "")
        modality = safe_get(first_ds, "Modality", "")
        series_description = safe_get(first_ds, "SeriesDescription", "")
        protocol_name = safe_get(first_ds, "ProtocolName", "")
        body_part = safe_get(first_ds, "BodyPartExamined", "")

        series_summary_rows.append({
            "series_instance_uid": series_uid,
            "patient_id": patient_id,
            "study_instance_uid": study_uid,
            "series_description": series_description,
            "protocol_name": protocol_name,
            "total_valid_slices": n,
            "selected_slices": len(selected_indices),
        })

        safe_patient = patient_id if patient_id else "unknown_patient"
        safe_series_short = series_uid[-12:] if len(series_uid) > 12 else series_uid

        for rank, idx in enumerate(selected_indices, start=1):
            source_path, ds = sorted_items[idx]

            instance_number = safe_get(ds, "InstanceNumber", "")
            rows = safe_get(ds, "Rows", "")
            columns = safe_get(ds, "Columns", "")
            image_position = safe_get(ds, "ImagePositionPatient", "")
            slice_location = safe_get(ds, "SliceLocation", "")

            out_filename = (
                f"{safe_patient}__{safe_series_short}"
                f"__central{rank:02d}_idx{idx:04d}.png"
            )
            out_path = OUT_DIR / safe_patient / out_filename

            save_png_from_dicom(ds, out_path)

            file_size = out_path.stat().st_size
            sha = sha256_file(out_path)

            manifest_rows.append({
                "dataset_id": DATASET_ID,
                "patient_id": patient_id,
                "study_instance_uid": study_uid,
                "series_instance_uid": series_uid,
                "series_description": series_description,
                "protocol_name": protocol_name,
                "body_part_examined": body_part,
                "modality": modality,
                "label": LABEL,
                "label_source": LABEL_SOURCE,
                "source_dicom_path": str(source_path),
                "output_image_path": str(out_path),
                "slice_index_in_sorted_series": idx,
                "selected_rank": rank,
                "total_valid_slices_in_series": n,
                "instance_number": instance_number,
                "image_position_patient": image_position,
                "slice_location": slice_location,
                "image_width": columns,
                "image_height": rows,
                "file_size_bytes": file_size,
                "sha256": sha,
            })

    fieldnames = [
        "dataset_id",
        "patient_id",
        "study_instance_uid",
        "series_instance_uid",
        "series_description",
        "protocol_name",
        "body_part_examined",
        "modality",
        "label",
        "label_source",
        "source_dicom_path",
        "output_image_path",
        "slice_index_in_sorted_series",
        "selected_rank",
        "total_valid_slices_in_series",
        "instance_number",
        "image_position_patient",
        "slice_location",
        "image_width",
        "image_height",
        "file_size_bytes",
        "sha256",
    ]

    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(manifest_rows)

    selected_patients = sorted(set(row["patient_id"] for row in manifest_rows))
    selected_series = sorted(set(row["series_instance_uid"] for row in manifest_rows))
    description_counts = Counter(row["series_description"] for row in manifest_rows)
    dimension_counts = Counter((row["image_height"], row["image_width"]) for row in manifest_rows)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D3B Slice Conversion Report\n\n")

        f.write("## Input\n\n")
        f.write(f"- Raw DICOM directory: `{RAW_DIR}`\n")
        f.write(f"- Total files scanned: {total_files}\n")
        f.write(f"- Valid MR DICOM image files: {valid_dicom_files}\n")
        f.write(f"- Skipped non-image / invalid files: {skipped_files}\n")
        f.write(f"- Unique valid series: {len(series)}\n\n")

        f.write("## Conversion Rule\n\n")
        f.write(f"- Selected central slices per series: {SLICES_PER_SERIES}\n")
        f.write("- Slice order used InstanceNumber where available, then ImagePositionPatient, then SliceLocation, then filepath.\n")
        f.write("- Pixel arrays were converted to 8-bit grayscale PNG using 1st-99th percentile intensity scaling.\n")
        f.write("- LICENSE files and non-pixel objects were ignored.\n\n")

        f.write("## Output\n\n")
        f.write(f"- Output image directory: `{OUT_DIR}`\n")
        f.write(f"- Manifest: `{MANIFEST_PATH}`\n")
        f.write(f"- Output images created: {len(manifest_rows)}\n")
        f.write(f"- Patients represented: {len(selected_patients)}\n")
        f.write(f"- Series represented: {len(selected_series)}\n\n")

        f.write("## Label Strategy\n\n")
        f.write("- Assigned label: `glioma`\n")
        f.write("- Label source: collection-level ICDC-Glioma identity\n")
        f.write("- Important limitation: this is not slice-level tumour annotation.\n\n")

        f.write("## Image Dimension Counts\n\n")
        f.write("| Height x Width | Count |\n")
        f.write("|---|---:|\n")
        for (height, width), count in dimension_counts.most_common():
            f.write(f"| {height} x {width} | {count} |\n")

        f.write("\n## Top Series Descriptions Among Selected Images\n\n")
        f.write("| SeriesDescription | Count |\n")
        f.write("|---|---:|\n")
        for desc, count in description_counts.most_common(30):
            f.write(f"| {str(desc).replace('|', '/')} | {count} |\n")

        f.write("\n## Series-Level Summary\n\n")
        f.write("| PatientID | SeriesDescription | Total valid slices | Selected slices |\n")
        f.write("|---|---|---:|---:|\n")
        for row in series_summary_rows[:80]:
            f.write(
                f"| {row['patient_id']} | "
                f"{str(row['series_description']).replace('|', '/')} | "
                f"{row['total_valid_slices']} | "
                f"{row['selected_slices']} |\n"
            )

        f.write("\n## Interpretation\n\n")
        f.write(
            "This conversion creates a reproducible 2D slice-level dataset from D3B using a fixed central-slice rule. "
            "It should be used for glioma-focused domain-shift confidence analysis, not full four-class external validation. "
            "Because selected slices are central rather than tumour-confirmed, results must be interpreted cautiously.\n"
        )

    print(f"Total files scanned: {total_files}")
    print(f"Valid MR DICOM image files: {valid_dicom_files}")
    print(f"Skipped files: {skipped_files}")
    print(f"Unique valid series: {len(series)}")
    print(f"Output images created: {len(manifest_rows)}")
    print(f"Patients represented: {len(selected_patients)}")
    print(f"Series represented: {len(selected_series)}")
    print(f"Manifest written to: {MANIFEST_PATH}")
    print(f"Report written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()

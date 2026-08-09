from pathlib import Path
from collections import defaultdict
import csv
import hashlib
import sys

import numpy as np
from PIL import Image
import pydicom

try:
    from tqdm import tqdm
except ImportError:
    print("tqdm not installed. Run:  pip install tqdm")
    sys.exit(1)

RAW_DIR = Path("data/raw/D3C_upenn_gbm")
OUT_DIR = Path("data/processed/D3C_upenn_gbm_selected_slices")
MANIFEST_PATH = Path("data/processed/D3C_selected_slices_manifest.csv")
REPORT_PATH = Path("reports/datasets/D3C_slice_conversion_report.md")

DATASET_ID = "D3C_upenn_gbm"
LABEL = "glioma"
LABEL_SOURCE = "collection_level_upenn_gbm"
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


def read_header_only(path: Path):
    if path.name.upper() == "LICENSE":
        return None
    try:
        ds = pydicom.dcmread(path, stop_before_pixels=True, force=True)
        if safe_get(ds, "Modality", "") != "MR":
            return None
        return ds
    except Exception:
        return None


def get_sort_key_from_header(path, ds):
    instance_number = safe_get(ds, "InstanceNumber", "")
    image_position = safe_get(ds, "ImagePositionPatient", "")
    slice_location = safe_get(ds, "SliceLocation", "")
    try:
        return (0, float(instance_number))
    except Exception:
        pass
    if image_position:
        try:
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


def select_central_indices(n, k):
    if n <= 0:
        return []
    if n <= k:
        return list(range(n))
    center = n // 2
    half = k // 2
    start = center - half
    end = start + k
    if start < 0:
        start, end = 0, k
    if end > n:
        end, start = n, n - k
    return list(range(start, end))


def normalize_to_uint8(arr):
    arr = arr.astype(np.float32)
    low = np.percentile(arr, 1)
    high = np.percentile(arr, 99)
    if high <= low:
        low = float(np.min(arr))
        high = float(np.max(arr))
    if high <= low:
        return np.zeros(arr.shape, dtype=np.uint8)
    arr = np.clip(arr, low, high)
    arr = (arr - low) / (high - low)
    return (arr * 255.0).round().astype(np.uint8)


def save_png_from_dicom_path(path, out_path):
    ds = pydicom.dcmread(path, stop_before_pixels=False, force=True)
    arr = ds.pixel_array
    if arr.ndim != 2:
        return None
    slope = float(getattr(ds, "RescaleSlope", 1.0) or 1.0)
    intercept = float(getattr(ds, "RescaleIntercept", 0.0) or 0.0)
    arr = arr.astype(np.float32) * slope + intercept
    arr_uint8 = normalize_to_uint8(arr)
    image = Image.fromarray(arr_uint8, mode="L")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path)
    return ds


def collect_series_headers():
    if not RAW_DIR.exists():
        raise FileNotFoundError("Raw directory not found: " + str(RAW_DIR))
    files = [p for p in RAW_DIR.rglob("*") if p.is_file()]
    series = defaultdict(list)
    valid = 0
    for path in tqdm(files, desc="Scanning DICOM headers", unit="file", ncols=80):
        ds = read_header_only(path)
        if ds is None:
            continue
        valid += 1
        series[safe_get(ds, "SeriesInstanceUID", "UNKNOWN")].append((path, ds))
    return series, len(files), valid


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    series, total_files, valid_files = collect_series_headers()

    manifest_rows = []
    total_series = len(series)

    for series_uid, items in tqdm(sorted(series.items()), desc="Writing central slices", unit="series", ncols=80):
        sorted_items = sorted(items, key=lambda it: get_sort_key_from_header(it[0], it[1]))
        n = len(sorted_items)
        selected = select_central_indices(n, SLICES_PER_SERIES)
        if not selected:
            continue

        first_ds = sorted_items[0][1]
        patient_id = safe_get(first_ds, "PatientID", "")
        study_uid = safe_get(first_ds, "StudyInstanceUID", "")
        series_description = safe_get(first_ds, "SeriesDescription", "")
        protocol_name = safe_get(first_ds, "ProtocolName", "")
        body_part = safe_get(first_ds, "BodyPartExamined", "")

        safe_patient = patient_id if patient_id else "unknown_patient"
        safe_series_short = series_uid[-12:] if len(series_uid) > 12 else series_uid

        for rank, idx in enumerate(selected, start=1):
            source_path, hdr = sorted_items[idx]
            out_filename = safe_patient + "__" + safe_series_short + "__central" + str(rank).zfill(2) + "_idx" + str(idx).zfill(4) + ".png"
            out_path = OUT_DIR / safe_patient / out_filename
            try:
                full_ds = save_png_from_dicom_path(source_path, out_path)
            except Exception:
                full_ds = None
            if full_ds is None:
                continue

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
                "modality": "MR",
                "label": LABEL,
                "label_source": LABEL_SOURCE,
                "source_dicom_path": str(source_path),
                "output_image_path": str(out_path),
                "slice_index_in_sorted_series": idx,
                "selected_rank": rank,
                "total_valid_slices_in_series": n,
                "instance_number": safe_get(hdr, "InstanceNumber", ""),
                "image_position_patient": safe_get(hdr, "ImagePositionPatient", ""),
                "slice_location": safe_get(hdr, "SliceLocation", ""),
                "image_width": safe_get(full_ds, "Columns", ""),
                "image_height": safe_get(full_ds, "Rows", ""),
                "file_size_bytes": file_size,
                "sha256": sha,
            })

    fieldnames = ["dataset_id", "patient_id", "study_instance_uid", "series_instance_uid",
                  "series_description", "protocol_name", "body_part_examined", "modality",
                  "label", "label_source", "source_dicom_path", "output_image_path",
                  "slice_index_in_sorted_series", "selected_rank", "total_valid_slices_in_series",
                  "instance_number", "image_position_patient", "slice_location",
                  "image_width", "image_height", "file_size_bytes", "sha256"]

    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(manifest_rows)

    patients = sorted(set(r["patient_id"] for r in manifest_rows))
    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D3C Slice Conversion Report - UPENN-GBM (human)" + chr(10))
        f.write("- Valid MR files: " + str(valid_files) + chr(10))
        f.write("- Series: " + str(total_series) + chr(10))
        f.write("- Images written: " + str(len(manifest_rows)) + chr(10))
        f.write("- Patients: " + str(len(patients)) + chr(10))

    print("")
    print("DONE. images=" + str(len(manifest_rows)) + " patients=" + str(len(patients)) + " series=" + str(total_series))
    print("Manifest: " + str(MANIFEST_PATH))


if __name__ == "__main__":
    main()

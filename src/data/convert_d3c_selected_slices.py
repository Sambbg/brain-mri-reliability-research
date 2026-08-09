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

# The authoritative selection, produced by src/data/select_d3c_upenn_gbm_series.py.
# Conversion is driven by that manifest rather than by globbing RAW_DIR: a glob silently
# converts any series left behind by an earlier, different selection, which is how a
# defective D3C cohort was produced before.
SELECTION_CSV = Path(
    "reports/datasets/d3c_upenn_gbm_series_selection/selected_series_one_per_patient.csv"
)

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


def load_selected_series_uids():
    """Read the SeriesInstanceUIDs the selection step chose, one per patient."""
    if not SELECTION_CSV.exists():
        raise FileNotFoundError(
            "Selection manifest not found: " + str(SELECTION_CSV) + chr(10)
            + "Run src/data/select_d3c_upenn_gbm_series.py before this step."
        )

    with SELECTION_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if "SeriesInstanceUID" not in (reader.fieldnames or []):
            raise ValueError(str(SELECTION_CSV) + " has no SeriesInstanceUID column.")

        uids = [(row.get("SeriesInstanceUID") or "").strip() for row in reader]

    uids = [uid for uid in uids if uid]

    if not uids:
        raise RuntimeError(str(SELECTION_CSV) + " lists no SeriesInstanceUIDs.")

    unique_uids = set(uids)
    if len(unique_uids) != len(uids):
        raise ValueError(str(SELECTION_CSV) + " contains duplicate SeriesInstanceUID rows.")

    return unique_uids


def collect_selected_series_files(selected_uids):
    """Enumerate files for the selected series only, aborting on orphans or gaps."""
    if not RAW_DIR.exists():
        raise FileNotFoundError("Raw directory not found: " + str(RAW_DIR))

    on_disk_uids = {p.name for p in RAW_DIR.iterdir() if p.is_dir()}

    orphan_uids = sorted(on_disk_uids - selected_uids)
    if orphan_uids:
        raise RuntimeError(
            str(len(orphan_uids)) + " series directories under " + str(RAW_DIR)
            + " are not listed in " + str(SELECTION_CSV) + ". These are orphans from a "
            "different selection and must not be converted into D3C. Clear the raw "
            "directory and re-run src/data/download_d3c_selected_series.py." + chr(10)
            + "First orphans:" + chr(10) + "  " + (chr(10) + "  ").join(orphan_uids[:10])
        )

    missing_uids = sorted(selected_uids - on_disk_uids)
    if missing_uids:
        raise RuntimeError(
            str(len(missing_uids)) + " selected series are missing from " + str(RAW_DIR)
            + ". The downloaded cohort does not match the selected cohort. Re-run "
            "src/data/download_d3c_selected_series.py." + chr(10)
            + "First missing:" + chr(10) + "  " + (chr(10) + "  ").join(missing_uids[:10])
        )

    files = []
    for series_uid in sorted(selected_uids):
        files.extend([p for p in (RAW_DIR / series_uid).rglob("*") if p.is_file()])

    return files


def collect_series_headers(selected_uids):
    files = collect_selected_series_files(selected_uids)
    series = defaultdict(list)
    valid = 0
    for path in tqdm(files, desc="Scanning DICOM headers", unit="file", ncols=80):
        ds = read_header_only(path)
        if ds is None:
            continue
        valid += 1
        series[safe_get(ds, "SeriesInstanceUID", "UNKNOWN")].append((path, ds))

    # Header-level cohort check, before any PNG is written. The directory check above
    # compares directory names; this compares the SeriesInstanceUID recorded in each
    # DICOM, so a directory holding files from another series is caught too.
    unexpected_series = sorted(set(series) - selected_uids)
    if unexpected_series:
        raise RuntimeError(
            str(len(unexpected_series)) + " scanned series are not in "
            + str(SELECTION_CSV) + ". Orphan series must not be converted into D3C."
            + chr(10) + "First:" + chr(10) + "  "
            + (chr(10) + "  ").join(unexpected_series[:10])
        )

    unreadable_series = sorted(selected_uids - set(series))
    if unreadable_series:
        raise RuntimeError(
            str(len(unreadable_series)) + " selected series produced no readable MR "
            "DICOM header. The cohort is incomplete." + chr(10) + "First:" + chr(10)
            + "  " + (chr(10) + "  ").join(unreadable_series[:10])
        )

    return series, len(files), valid


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    selected_uids = load_selected_series_uids()

    print("Selection manifest: " + str(SELECTION_CSV))
    print("Selected series: " + str(len(selected_uids)))

    series, total_files, valid_files = collect_series_headers(selected_uids)

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
        f.write("- Selection manifest: `" + str(SELECTION_CSV) + "`" + chr(10))
        f.write("- Selected series: " + str(len(selected_uids)) + chr(10))
        f.write("- Valid MR files: " + str(valid_files) + chr(10))
        f.write("- Series: " + str(total_series) + chr(10))
        f.write("- Images written: " + str(len(manifest_rows)) + chr(10))
        f.write("- Patients: " + str(len(patients)) + chr(10))
        f.write(
            "- Series converted match the selection manifest exactly; no orphan series "
            "were included." + chr(10)
        )

    print("")
    print("DONE. images=" + str(len(manifest_rows)) + " patients=" + str(len(patients)) + " series=" + str(total_series))
    print("Manifest: " + str(MANIFEST_PATH))


if __name__ == "__main__":
    main()

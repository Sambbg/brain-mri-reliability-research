from pathlib import Path
from collections import Counter, defaultdict
import csv

import pydicom

RAW_DIR = Path("data/raw/D3C_upenn_gbm")
REPORT_PATH = Path("reports/datasets/D3C_dicom_inspection_report.md")
SERIES_SUMMARY_CSV = Path("reports/datasets/D3C_dicom_series_summary.csv")

# The authoritative selection, produced by src/data/select_d3c_upenn_gbm_series.py.
# This step is driven by that manifest rather than by globbing RAW_DIR: a glob silently
# sweeps in any series left behind by an earlier, different selection, which is how a
# defective D3C cohort was produced before.
SELECTION_CSV = Path(
    "reports/datasets/d3c_upenn_gbm_series_selection/selected_series_one_per_patient.csv"
)

DICOM_EXTENSIONS = {".dcm", ""}


def safe_get(ds, name, default=""):
    value = getattr(ds, name, default)
    if value is None:
        return default
    return str(value)


def read_dicom_header(path: Path):
    return pydicom.dcmread(path, stop_before_pixels=False, force=True)


def load_selected_series_uids():
    """Read the SeriesInstanceUIDs the selection step chose, one per patient."""
    if not SELECTION_CSV.exists():
        raise FileNotFoundError(
            f"Selection manifest not found: {SELECTION_CSV}\n"
            "Run src/data/select_d3c_upenn_gbm_series.py before this step."
        )

    with SELECTION_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if "SeriesInstanceUID" not in (reader.fieldnames or []):
            raise ValueError(f"{SELECTION_CSV} has no SeriesInstanceUID column.")

        uids = [(row.get("SeriesInstanceUID") or "").strip() for row in reader]

    uids = [uid for uid in uids if uid]

    if not uids:
        raise RuntimeError(f"{SELECTION_CSV} lists no SeriesInstanceUIDs.")

    unique_uids = set(uids)
    if len(unique_uids) != len(uids):
        raise ValueError(f"{SELECTION_CSV} contains duplicate SeriesInstanceUID rows.")

    return unique_uids


def collect_selected_series_files(selected_uids):
    """Enumerate files for the selected series only, aborting on orphans or gaps."""
    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Raw D3C directory not found: {RAW_DIR}")

    on_disk_uids = {p.name for p in RAW_DIR.iterdir() if p.is_dir()}

    orphan_uids = sorted(on_disk_uids - selected_uids)
    if orphan_uids:
        raise RuntimeError(
            f"{len(orphan_uids)} series directories under {RAW_DIR} are not listed in "
            f"{SELECTION_CSV}. These are orphans from a different selection and must not "
            "be inspected as part of D3C. Clear the raw directory and re-run "
            "src/data/download_d3c_selected_series.py.\nFirst orphans:\n  "
            + "\n  ".join(orphan_uids[:10])
        )

    missing_uids = sorted(selected_uids - on_disk_uids)
    if missing_uids:
        raise RuntimeError(
            f"{len(missing_uids)} selected series are missing from {RAW_DIR}. The "
            "downloaded cohort does not match the selected cohort. Re-run "
            "src/data/download_d3c_selected_series.py.\nFirst missing:\n  "
            + "\n  ".join(missing_uids[:10])
        )

    files = []
    empty_series = []

    for series_uid in sorted(selected_uids):
        series_files = [p for p in (RAW_DIR / series_uid).rglob("*") if p.is_file()]

        if not series_files:
            empty_series.append(series_uid)
            continue

        files.extend(series_files)

    if empty_series:
        raise RuntimeError(
            f"{len(empty_series)} selected series directories contain no files.\n  "
            + "\n  ".join(empty_series[:10])
        )

    return files


def main():
    selected_uids = load_selected_series_uids()
    files = collect_selected_series_files(selected_uids)

    print(f"Selection manifest: {SELECTION_CSV}")
    print(f"Selected series: {len(selected_uids)}")
    print(f"Files to inspect: {len(files)}")

    if not files:
        raise RuntimeError(f"No files found under {RAW_DIR}")

    rows = []
    read_errors = []

    series_file_counts = Counter()
    series_pixel_readable_counts = Counter()
    series_descriptions = {}
    series_modalities = {}
    series_patient_ids = {}
    series_study_uids = {}
    series_dimensions = defaultdict(Counter)
    series_instance_numbers = defaultdict(list)
    series_image_positions = defaultdict(list)

    for idx, path in enumerate(files, start=1):
        if idx % 500 == 0:
            print(f"Inspecting {idx}/{len(files)} files")

        try:
            ds = read_dicom_header(path)

            series_uid = safe_get(ds, "SeriesInstanceUID", "UNKNOWN")
            study_uid = safe_get(ds, "StudyInstanceUID", "")
            patient_id = safe_get(ds, "PatientID", "")
            modality = safe_get(ds, "Modality", "")
            series_description = safe_get(ds, "SeriesDescription", "")
            protocol_name = safe_get(ds, "ProtocolName", "")
            body_part = safe_get(ds, "BodyPartExamined", "")
            instance_number = safe_get(ds, "InstanceNumber", "")
            rows_value = safe_get(ds, "Rows", "")
            cols_value = safe_get(ds, "Columns", "")

            pixel_readable = False
            pixel_error = ""

            try:
                _ = ds.pixel_array
                pixel_readable = True
            except Exception as exc:
                pixel_error = repr(exc)

            series_file_counts[series_uid] += 1

            if pixel_readable:
                series_pixel_readable_counts[series_uid] += 1

            series_descriptions[series_uid] = series_description
            series_modalities[series_uid] = modality
            series_patient_ids[series_uid] = patient_id
            series_study_uids[series_uid] = study_uid
            series_dimensions[series_uid][(rows_value, cols_value)] += 1

            if instance_number:
                series_instance_numbers[series_uid].append(instance_number)

            image_position = safe_get(ds, "ImagePositionPatient", "")
            if image_position:
                series_image_positions[series_uid].append(image_position)

            rows.append({
                "filepath": str(path),
                "patient_id": patient_id,
                "study_instance_uid": study_uid,
                "series_instance_uid": series_uid,
                "modality": modality,
                "series_description": series_description,
                "protocol_name": protocol_name,
                "body_part_examined": body_part,
                "instance_number": instance_number,
                "rows": rows_value,
                "columns": cols_value,
                "pixel_readable": pixel_readable,
                "pixel_error": pixel_error,
            })

        except Exception as exc:
            read_errors.append((str(path), repr(exc)))

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    series_rows = []

    for series_uid, file_count in sorted(series_file_counts.items()):
        dims = series_dimensions[series_uid]
        dim_summary = "; ".join(
            [f"{r}x{c}: {n}" for (r, c), n in dims.most_common()]
        )

        series_rows.append({
            "series_instance_uid": series_uid,
            "patient_id": series_patient_ids.get(series_uid, ""),
            "study_instance_uid": series_study_uids.get(series_uid, ""),
            "modality": series_modalities.get(series_uid, ""),
            "series_description": series_descriptions.get(series_uid, ""),
            "file_count": file_count,
            "pixel_readable_count": series_pixel_readable_counts.get(series_uid, 0),
            "dimension_summary": dim_summary,
            "has_instance_numbers": len(series_instance_numbers[series_uid]) > 0,
            "has_image_position_patient": len(series_image_positions[series_uid]) > 0,
        })

    with SERIES_SUMMARY_CSV.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "series_instance_uid",
            "patient_id",
            "study_instance_uid",
            "modality",
            "series_description",
            "file_count",
            "pixel_readable_count",
            "dimension_summary",
            "has_instance_numbers",
            "has_image_position_patient",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(series_rows)

    modality_counts = Counter(row["modality"] for row in rows)
    description_counts = Counter(row["series_description"] for row in rows)
    dimension_counts = Counter((row["rows"], row["columns"]) for row in rows)
    pixel_readable_total = sum(1 for row in rows if row["pixel_readable"])

    # Header-level cohort check. The directory-level check above compares directory
    # names; this compares the SeriesInstanceUID actually recorded in each DICOM, so a
    # directory holding files from some other series is caught too. Reports are written
    # first so the evidence survives the abort.
    inspected_series = set(series_file_counts)
    unexpected_series = sorted(inspected_series - selected_uids)
    unreadable_series = sorted(selected_uids - inspected_series)

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D3C DICOM Inspection Report\n\n")

        f.write("## Input\n\n")
        f.write(f"- Selection manifest: `{SELECTION_CSV}`\n")
        f.write(f"- Selected series: {len(selected_uids)}\n")
        f.write(f"- Raw directory: `{RAW_DIR}`\n")
        f.write(f"- Total files found: {len(files)}\n")
        f.write(f"- Files successfully read as DICOM: {len(rows)}\n")
        f.write(f"- Read errors: {len(read_errors)}\n")
        f.write(f"- Files with readable pixel arrays: {pixel_readable_total}\n")
        f.write(f"- Unique series: {len(series_file_counts)}\n")
        f.write(f"- Unique patients: {len(set(row['patient_id'] for row in rows))}\n")
        f.write(
            "- Series not listed in the selection manifest: "
            f"{len(unexpected_series)}\n"
        )
        f.write(
            f"- Selected series with no readable DICOM: {len(unreadable_series)}\n\n"
        )

        f.write("## Cohort Integrity\n\n")
        if not unexpected_series and not unreadable_series:
            f.write(
                f"The {len(inspected_series)} series inspected match the "
                f"{len(selected_uids)} series in the selection manifest exactly. No "
                "orphan series were included.\n"
            )
        else:
            f.write(
                "This inspection does not match the selection manifest and the cohort "
                "must not be used until it does.\n\n"
            )
            for uid in unexpected_series[:20]:
                f.write(f"- Not in manifest: `{uid}`\n")
            for uid in unreadable_series[:20]:
                f.write(f"- Selected but unreadable: `{uid}`\n")

        f.write("\n## Modality Counts\n\n")
        f.write("| Modality | Count |\n")
        f.write("|---|---:|\n")
        for modality, count in sorted(modality_counts.items()):
            f.write(f"| {modality} | {count} |\n")

        f.write("\n## Image Dimension Counts\n\n")
        f.write("| Rows x Columns | Count |\n")
        f.write("|---|---:|\n")
        for (r, c), count in dimension_counts.most_common():
            f.write(f"| {r} x {c} | {count} |\n")

        f.write("\n## Top Series Descriptions\n\n")
        f.write("| SeriesDescription | Count |\n")
        f.write("|---|---:|\n")
        for description, count in description_counts.most_common(30):
            safe_description = str(description).replace("|", "/")
            f.write(f"| {safe_description} | {count} |\n")

        f.write("\n## Series Summary\n\n")
        f.write(f"- Series summary CSV: `{SERIES_SUMMARY_CSV}`\n\n")
        f.write("| PatientID | SeriesDescription | File count | Pixel readable | Dimensions |\n")
        f.write("|---|---|---:|---:|---|\n")

        for row in series_rows[:60]:
            f.write(
                f"| {row['patient_id']} | "
                f"{str(row['series_description']).replace('|', '/')} | "
                f"{row['file_count']} | "
                f"{row['pixel_readable_count']} | "
                f"{row['dimension_summary']} |\n"
            )

        f.write("\n## Interpretation\n\n")
        f.write(
            "This inspection verifies that the selected D3C DICOM series were downloaded "
            "and can be read with pydicom. Series are enumerated from the selection "
            "manifest, not by globbing the raw directory, so only the selected cohort is "
            "inspected. No image conversion or slice selection is performed in this step. "
            "The next step is to create a reproducible D3C slice-conversion script using a "
            "fixed central-slice rule.\n"
        )

        if read_errors:
            f.write("\n## Read Errors\n\n")
            for path, err in read_errors[:100]:
                f.write(f"- `{path}`: {err}\n")

    print(f"Total files found: {len(files)}")
    print(f"Files read as DICOM: {len(rows)}")
    print(f"Read errors: {len(read_errors)}")
    print(f"Files with readable pixel arrays: {pixel_readable_total}")
    print(f"Unique series: {len(series_file_counts)}")
    print(f"Unique patients: {len(set(row['patient_id'] for row in rows))}")
    print(f"Report written to: {REPORT_PATH}")
    print(f"Series summary CSV written to: {SERIES_SUMMARY_CSV}")

    if unexpected_series:
        raise RuntimeError(
            f"{len(unexpected_series)} inspected series are not in {SELECTION_CSV}. "
            "Orphan series must not be included in D3C.\nFirst:\n  "
            + "\n  ".join(unexpected_series[:10])
        )

    if unreadable_series:
        raise RuntimeError(
            f"{len(unreadable_series)} selected series produced no readable DICOM. "
            "The inspected cohort is incomplete.\nFirst:\n  "
            + "\n  ".join(unreadable_series[:10])
        )

    print(
        f"Cohort integrity OK: {len(inspected_series)} series inspected, "
        f"matching the {len(selected_uids)} selected."
    )


if __name__ == "__main__":
    main()

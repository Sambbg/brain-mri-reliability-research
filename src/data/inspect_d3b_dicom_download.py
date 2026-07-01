from pathlib import Path
from collections import Counter, defaultdict
import csv

import pydicom

RAW_DIR = Path("data/raw/D3B_icdc_glioma")
REPORT_PATH = Path("reports/datasets/D3B_dicom_inspection_report.md")
SERIES_SUMMARY_CSV = Path("reports/datasets/D3B_dicom_series_summary.csv")

DICOM_EXTENSIONS = {".dcm", ""}


def safe_get(ds, name, default=""):
    value = getattr(ds, name, default)
    if value is None:
        return default
    return str(value)


def read_dicom_header(path: Path):
    return pydicom.dcmread(path, stop_before_pixels=False, force=True)


def find_candidate_files():
    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Raw D3B directory not found: {RAW_DIR}")

    files = [p for p in RAW_DIR.rglob("*") if p.is_file()]
    return files


def main():
    files = find_candidate_files()

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

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D3B DICOM Inspection Report\n\n")

        f.write("## Input\n\n")
        f.write(f"- Raw directory: `{RAW_DIR}`\n")
        f.write(f"- Total files found: {len(files)}\n")
        f.write(f"- Files successfully read as DICOM: {len(rows)}\n")
        f.write(f"- Read errors: {len(read_errors)}\n")
        f.write(f"- Files with readable pixel arrays: {pixel_readable_total}\n")
        f.write(f"- Unique series: {len(series_file_counts)}\n")
        f.write(f"- Unique patients: {len(set(row['patient_id'] for row in rows))}\n\n")

        f.write("## Modality Counts\n\n")
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
            "This inspection verifies that the selected D3B DICOM series were downloaded "
            "and can be read with pydicom. No image conversion or slice selection is performed "
            "in this step. The next step is to create a reproducible D3B slice-conversion script "
            "using a fixed central-slice rule.\n"
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


if __name__ == "__main__":
    main()

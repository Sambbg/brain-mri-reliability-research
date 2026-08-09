from pathlib import Path
from collections import Counter, defaultdict
import csv

import numpy as np
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

# TCIA ships a plain-text licence file inside every downloaded series directory. It is
# not DICOM, so pydicom's force=True parses it into an essentially empty dataset with no
# SeriesInstanceUID. Such files are set aside by name and counted in the report; they are
# never allowed to collapse into a catch-all series bin, which previously made 614
# licence files appear as one phantom 615th series with a blank PatientID.
KNOWN_SIDECAR_FILENAMES = {"LICENSE"}


def is_dicom_file(path: Path) -> bool:
    """True if the file carries the DICM magic number at offset 128.

    Checked from the file itself rather than trusting the filename, so a genuine DICOM
    with an unexpected name is still inspected and a non-DICOM file cannot be read as
    one.
    """
    try:
        with path.open("rb") as handle:
            header = handle.read(132)
    except OSError:
        return False

    return len(header) >= 132 and header[128:132] == b"DICM"


def safe_get(ds, name, default=""):
    value = getattr(ds, name, default)
    if value is None:
        return default
    return str(value)


def read_dicom_header(path: Path):
    return pydicom.dcmread(path, stop_before_pixels=False, force=True)


def get_image_orientation(ds):
    """ImageOrientationPatient as six floats, or None if absent or malformed."""
    value = getattr(ds, "ImageOrientationPatient", None)

    if value is None:
        return None

    try:
        values = [float(v) for v in value]
    except (TypeError, ValueError):
        return None

    if len(values) != 6:
        return None

    return values


def parse_dicom_time(value):
    """DICOM TM value (HHMMSS.FFFFFF) to seconds since midnight, or None.

    Returns None rather than guessing on anything malformed, so unparsable times are
    counted as missing coverage instead of silently becoming a timing verdict.
    """
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    try:
        hours = int(text[0:2])
        minutes = int(text[2:4]) if len(text) >= 4 else 0
        seconds = float(text[4:]) if len(text) > 4 else 0.0
    except ValueError:
        return None

    if not (0 <= hours <= 23 and 0 <= minutes <= 59 and 0.0 <= seconds < 61.0):
        return None

    return hours * 3600 + minutes * 60 + seconds


SECONDS_PER_DAY = 24 * 3600


def classify_contrast_timing(bolus_start_seconds, acquisition_seconds):
    """Pre or post contrast from the clock, not from the series description.

    A series that began after the contrast bolus started is post-contrast. Both tags are
    times of day with no date, so a study running across midnight would otherwise show a
    ~24h error; deltas beyond half a day are wrapped.
    """
    if bolus_start_seconds is None or acquisition_seconds is None:
        return "unknown", None

    delta = acquisition_seconds - bolus_start_seconds

    if delta < -SECONDS_PER_DAY / 2:
        delta += SECONDS_PER_DAY
    elif delta > SECONDS_PER_DAY / 2:
        delta -= SECONDS_PER_DAY

    return ("post_contrast" if delta >= 0 else "pre_contrast"), delta


PLANE_BY_AXIS = {0: "sagittal", 1: "coronal", 2: "axial"}

# An axial series more than this far off the true axial plane is reported separately.
OBLIQUITY_FLAG_DEGREES = 10.0


def derive_plane(iop):
    """Acquisition plane from the slice normal, not from SeriesDescription.

    ImageOrientationPatient holds two direction cosines, for the image row and column
    axes. Their cross product is the slice normal. DICOM patient axes are x = left/right,
    y = anterior/posterior, z = foot/head, so a normal dominated by z is an axial
    acquisition, by x sagittal, by y coronal.

    This is measured geometry. SeriesDescription is free text and has already proven
    unreliable for this cohort, so plane and contrast status are both read from headers.
    """
    row = np.array(iop[:3], dtype=float)
    col = np.array(iop[3:], dtype=float)

    normal = np.cross(row, col)
    norm = float(np.linalg.norm(normal))

    if norm == 0.0:
        return None, None, None

    normal = normal / norm
    axis = int(np.argmax(np.abs(normal)))
    dominance = float(abs(normal[axis]))
    obliquity_degrees = float(np.degrees(np.arccos(min(1.0, dominance))))

    return PLANE_BY_AXIS[axis], dominance, obliquity_degrees


def load_selection_manifest():
    """Return {SeriesInstanceUID: manifest row} from the authoritative selection."""
    if not SELECTION_CSV.exists():
        raise FileNotFoundError(
            f"Selection manifest not found: {SELECTION_CSV}\n"
            "Run src/data/select_d3c_upenn_gbm_series.py before this step."
        )

    with SELECTION_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if "SeriesInstanceUID" not in (reader.fieldnames or []):
            raise ValueError(f"{SELECTION_CSV} has no SeriesInstanceUID column.")

        rows = list(reader)

    manifest = {}
    for row in rows:
        uid = (row.get("SeriesInstanceUID") or "").strip()
        if not uid:
            continue
        if uid in manifest:
            raise ValueError(f"{SELECTION_CSV} contains duplicate SeriesInstanceUID rows.")
        manifest[uid] = row

    if not manifest:
        raise RuntimeError(f"{SELECTION_CSV} lists no SeriesInstanceUIDs.")

    return manifest


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

    dicom_files = []
    sidecar_files = []
    unexpected_files = []
    empty_series = []

    for series_uid in sorted(selected_uids):
        series_files = [p for p in (RAW_DIR / series_uid).rglob("*") if p.is_file()]

        if not series_files:
            empty_series.append(series_uid)
            continue

        for path in series_files:
            if is_dicom_file(path):
                dicom_files.append(path)
            elif path.name.upper() in KNOWN_SIDECAR_FILENAMES:
                sidecar_files.append(path)
            else:
                unexpected_files.append(path)

    if empty_series:
        raise RuntimeError(
            f"{len(empty_series)} selected series directories contain no files.\n  "
            + "\n  ".join(empty_series[:10])
        )

    if unexpected_files:
        raise RuntimeError(
            f"{len(unexpected_files)} files under {RAW_DIR} are neither DICOM nor a "
            f"recognised sidecar {sorted(KNOWN_SIDECAR_FILENAMES)}. They are not being "
            "skipped silently; identify them before inspecting the cohort.\nFirst:\n  "
            + "\n  ".join(str(p) for p in unexpected_files[:10])
        )

    return dicom_files, sidecar_files


def main():
    manifest = load_selection_manifest()
    selected_uids = set(manifest)
    files, sidecar_files = collect_selected_series_files(selected_uids)

    print(f"Selection manifest: {SELECTION_CSV}")
    print(f"Selected series: {len(selected_uids)}")
    print(f"DICOM files to inspect: {len(files)}")
    print(f"Non-DICOM sidecar files set aside: {len(sidecar_files)}")

    if not files:
        raise RuntimeError(f"No files found under {RAW_DIR}")

    rows = []
    read_errors = []
    # DICOM files whose SeriesInstanceUID is missing or blank. These abort the run: a
    # file that claims to be DICOM but cannot say which series it belongs to must not be
    # counted, binned, or dropped without comment.
    missing_uid_files = []

    series_file_counts = Counter()
    series_pixel_readable_counts = Counter()
    series_descriptions = {}
    series_modalities = {}
    series_patient_ids = {}
    series_study_uids = {}
    series_dimensions = defaultdict(Counter)
    series_instance_numbers = defaultdict(list)
    series_image_positions = defaultdict(list)

    # Cohort composition, read from headers rather than from SeriesDescription.
    series_orientations = defaultdict(set)
    series_first_orientation = {}
    series_contrast_agents = defaultdict(set)
    series_bolus_start_seconds = {}
    series_acquisition_seconds = defaultdict(list)

    for idx, path in enumerate(files, start=1):
        if idx % 500 == 0:
            print(f"Inspecting {idx}/{len(files)} files")

        try:
            ds = read_dicom_header(path)

            series_uid = safe_get(ds, "SeriesInstanceUID", "").strip()

            if not series_uid:
                # No default bucket: an unattributable DICOM is an error, recorded here
                # and raised after the report is written.
                missing_uid_files.append(str(path))
                continue

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

            orientation = get_image_orientation(ds)
            if orientation is not None:
                series_orientations[series_uid].add(
                    tuple(round(v, 4) for v in orientation)
                )
                # "First slice" is the first file in sorted enumeration order, which is
                # deterministic; orientation is constant within a well-formed series and
                # any series where it is not is flagged below.
                series_first_orientation.setdefault(series_uid, orientation)

            series_contrast_agents[series_uid].add(
                safe_get(ds, "ContrastBolusAgent", "").strip()
            )

            bolus_start = parse_dicom_time(getattr(ds, "ContrastBolusStartTime", None))
            if bolus_start is not None:
                series_bolus_start_seconds.setdefault(series_uid, bolus_start)

            acquisition_time = parse_dicom_time(getattr(ds, "AcquisitionTime", None))
            if acquisition_time is not None:
                series_acquisition_seconds[series_uid].append(acquisition_time)

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

        orientation = series_first_orientation.get(series_uid)
        if orientation is None:
            plane, dominance, obliquity = "unknown", None, None
        else:
            plane, dominance, obliquity = derive_plane(orientation)
            if plane is None:
                plane = "degenerate"

        agents = {a for a in series_contrast_agents.get(series_uid, set()) if a}
        manifest_row = manifest.get(series_uid, {})

        bolus_start = series_bolus_start_seconds.get(series_uid)
        acquisition_times = series_acquisition_seconds.get(series_uid, [])
        # The start of the series is what decides pre versus post, so use the earliest
        # acquisition time in it rather than an arbitrary slice.
        acquisition_start = min(acquisition_times) if acquisition_times else None
        timing_class, timing_delta = classify_contrast_timing(bolus_start, acquisition_start)

        series_rows.append({
            "series_instance_uid": series_uid,
            "patient_id": series_patient_ids.get(series_uid, ""),
            "study_instance_uid": series_study_uids.get(series_uid, ""),
            "modality": series_modalities.get(series_uid, ""),
            "series_description": series_descriptions.get(series_uid, ""),
            "selection_category": manifest_row.get("selection_category", ""),
            "file_count": file_count,
            "pixel_readable_count": series_pixel_readable_counts.get(series_uid, 0),
            "dimension_summary": dim_summary,
            "has_instance_numbers": len(series_instance_numbers[series_uid]) > 0,
            "has_image_position_patient": len(series_image_positions[series_uid]) > 0,
            "acquisition_plane": plane,
            "plane_dominance": "" if dominance is None else round(dominance, 6),
            "obliquity_degrees": "" if obliquity is None else round(obliquity, 3),
            "orientation_consistent": len(series_orientations.get(series_uid, set())) <= 1,
            "contrast_bolus_agent": "; ".join(sorted(agents)),
            "has_contrast_bolus_agent": bool(agents),
            "contrast_bolus_start_seconds": "" if bolus_start is None else round(bolus_start, 3),
            "acquisition_start_seconds": "" if acquisition_start is None else round(acquisition_start, 3),
            "contrast_timing_delta_seconds": "" if timing_delta is None else round(timing_delta, 3),
            "contrast_timing_class": timing_class,
        })

    with SERIES_SUMMARY_CSV.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "series_instance_uid",
            "patient_id",
            "study_instance_uid",
            "modality",
            "series_description",
            "selection_category",
            "file_count",
            "pixel_readable_count",
            "dimension_summary",
            "has_instance_numbers",
            "has_image_position_patient",
            "acquisition_plane",
            "plane_dominance",
            "obliquity_degrees",
            "orientation_consistent",
            "contrast_bolus_agent",
            "has_contrast_bolus_agent",
            "contrast_bolus_start_seconds",
            "acquisition_start_seconds",
            "contrast_timing_delta_seconds",
            "contrast_timing_class",
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
        f.write(f"- DICOM files inspected: {len(files)}\n")
        f.write(
            f"- Non-DICOM sidecar files set aside: {len(sidecar_files)} "
            f"({', '.join(sorted(KNOWN_SIDECAR_FILENAMES))})\n"
        )
        f.write(
            f"- DICOM files with a missing or blank SeriesInstanceUID: "
            f"{len(missing_uid_files)}\n"
        )
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

        f.write(
            f"{len(sidecar_files)} non-DICOM sidecar files "
            f"({', '.join(sorted(KNOWN_SIDECAR_FILENAMES))}) were identified by the "
            "absence of the DICM magic number and set aside before inspection. They are "
            "excluded from the series accounting but counted here, not dropped in "
            "silence.\n\n"
        )

        if missing_uid_files:
            f.write(
                f"**{len(missing_uid_files)} DICOM files have a missing or blank "
                "SeriesInstanceUID.** They cannot be attributed to a series and are not "
                "assigned to one; this inspection is aborted rather than reported.\n\n"
            )
            for path in missing_uid_files[:20]:
                f.write(f"- `{path}`\n")
            f.write("\n")

        if not unexpected_series and not unreadable_series and not missing_uid_files:
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

        f.write("\n## Cohort Composition\n\n")
        f.write(
            "Acquisition plane and contrast status are read from DICOM headers, not "
            "parsed from SeriesDescription. Plane comes from the slice normal, the cross "
            "product of the two direction cosines in ImageOrientationPatient. Contrast "
            "comes from ContrastBolusAgent (0018,0010).\n\n"
        )

        plane_counts = Counter(row["acquisition_plane"] for row in series_rows)
        non_axial = [r for r in series_rows if r["acquisition_plane"] != "axial"]
        oblique_axial = [
            r for r in series_rows
            if r["acquisition_plane"] == "axial"
            and r["obliquity_degrees"] != ""
            and r["obliquity_degrees"] > OBLIQUITY_FLAG_DEGREES
        ]
        inconsistent = [r for r in series_rows if not r["orientation_consistent"]]

        f.write("### Acquisition Plane, Series Level\n\n")
        f.write("| Plane | Series | Share |\n")
        f.write("|---|---:|---:|\n")
        for plane, count in sorted(plane_counts.items(), key=lambda kv: (-kv[1], kv[0])):
            share = count / len(series_rows) if series_rows else 0.0
            f.write(f"| {plane} | {count} | {share:.4f} |\n")

        f.write(
            "\nD1 is axial. Any non-axial series is a plane confound: a difference in "
            "predictions could reflect acquisition geometry rather than domain shift.\n\n"
        )

        if non_axial:
            f.write(f"### Non-Axial Series, Flagged: {len(non_axial)}\n\n")
            f.write("| PatientID | Plane | Obliquity (deg) | SeriesDescription |\n")
            f.write("|---|---|---:|---|\n")
            for row in non_axial[:40]:
                f.write(
                    f"| {row['patient_id']} | {row['acquisition_plane']} | "
                    f"{row['obliquity_degrees']} | "
                    f"{str(row['series_description']).replace('|', '/')} |\n"
                )
            if len(non_axial) > 40:
                f.write(
                    f"\n{len(non_axial) - 40} further non-axial series are listed in "
                    f"`{SERIES_SUMMARY_CSV}`.\n"
                )
        else:
            f.write("### Non-Axial Series, Flagged: 0\n\n")
            f.write("Every selected series is axial. No plane confound.\n")

        f.write(
            f"\n### Oblique Axial Series, more than {OBLIQUITY_FLAG_DEGREES:.0f} degrees "
            f"off plane: {len(oblique_axial)}\n\n"
        )
        if oblique_axial:
            f.write("| PatientID | Obliquity (deg) | SeriesDescription |\n")
            f.write("|---|---:|---|\n")
            for row in oblique_axial[:20]:
                f.write(
                    f"| {row['patient_id']} | {row['obliquity_degrees']} | "
                    f"{str(row['series_description']).replace('|', '/')} |\n"
                )
        else:
            f.write("None. Every axial series lies close to the true axial plane.\n")

        f.write(
            f"\n### Series with Inconsistent Orientation Across Slices: "
            f"{len(inconsistent)}\n\n"
        )
        if inconsistent:
            f.write(
                "These series contain slices at more than one orientation, which usually "
                "means a multi-plane or localizer series slipped through selection.\n\n"
            )
            for row in inconsistent[:20]:
                f.write(
                    f"- `{row['series_instance_uid']}` "
                    f"({row['patient_id']}, {row['acquisition_plane']})\n"
                )
        else:
            f.write("None. Every series holds a single consistent orientation.\n")

        with_contrast = [r for r in series_rows if r["has_contrast_bolus_agent"]]
        agent_counts = Counter(
            r["contrast_bolus_agent"] for r in series_rows if r["has_contrast_bolus_agent"]
        )

        f.write("\n### Contrast Status from ContrastBolusAgent\n\n")
        f.write("| ContrastBolusAgent | Series |\n")
        f.write("|---|---:|\n")
        f.write(f"| present | {len(with_contrast)} |\n")
        f.write(f"| absent or empty | {len(series_rows) - len(with_contrast)} |\n")

        if agent_counts:
            f.write("\n| Agent value | Series |\n")
            f.write("|---|---:|\n")
            for agent, count in agent_counts.most_common(20):
                f.write(f"| {str(agent).replace('|', '/')} | {count} |\n")

        f.write("\n### Pre versus Post Contrast from Acquisition Timing\n\n")
        f.write(
            "ContrastBolusAgent only records that contrast was administered during the "
            "study; scanners routinely copy it to every series in that study, including "
            "pre-contrast acquisitions, so it cannot discriminate pre from post at series "
            "level. Comparing ContrastBolusStartTime (0018,1042) with the earliest "
            "AcquisitionTime (0008,0032) in the series can: a series that began after the "
            "bolus started is post-contrast.\n\n"
        )

        total_series = len(series_rows)
        have_bolus = [r for r in series_rows if r["contrast_bolus_start_seconds"] != ""]
        have_acq = [r for r in series_rows if r["acquisition_start_seconds"] != ""]
        have_both = [r for r in series_rows if r["contrast_timing_class"] != "unknown"]
        coverage = len(have_both) / total_series if total_series else 0.0

        f.write("#### Field Coverage\n\n")
        f.write("| Field | Series populated | Share |\n")
        f.write("|---|---:|---:|\n")
        f.write(
            f"| ContrastBolusStartTime | {len(have_bolus)} | "
            f"{len(have_bolus) / total_series if total_series else 0:.4f} |\n"
        )
        f.write(
            f"| AcquisitionTime | {len(have_acq)} | "
            f"{len(have_acq) / total_series if total_series else 0:.4f} |\n"
        )
        f.write(f"| Both, so timing is decidable | {len(have_both)} | {coverage:.4f} |\n\n")

        if not have_both:
            f.write(
                f"**Timing cannot be evaluated for any series.** Neither field pair is "
                f"populated anywhere in the {total_series} selected series, so pre versus "
                "post contrast cannot be established from headers at all. It remains "
                "inferred from SeriesDescription and must be reported as an assumption, "
                "not as a verified property of the cohort.\n\n"
            )
        elif coverage < 0.95:
            f.write(
                f"**Coverage is incomplete: timing is decidable for only "
                f"{len(have_both)} of {total_series} series ({coverage:.1%}).** The "
                f"breakdown below therefore describes that subset alone and says nothing "
                f"about the remaining {total_series - len(have_both)} series, whose "
                "contrast status stays inferred from SeriesDescription. Do not read these "
                "counts as a cohort-wide result or rescale them to the full cohort.\n\n"
            )
        else:
            f.write(
                f"Coverage is {coverage:.1%}, so the breakdown below is representative of "
                "the cohort.\n\n"
            )

        if have_both:
            timing_counts = Counter(r["contrast_timing_class"] for r in have_both)
            f.write("#### Timing Verdict, Decidable Series Only\n\n")
            f.write("| Verdict | Series | Share of decidable |\n")
            f.write("|---|---:|---:|\n")
            for verdict, count in sorted(timing_counts.items()):
                f.write(f"| {verdict} | {count} | {count / len(have_both):.4f} |\n")

            deltas = sorted(r["contrast_timing_delta_seconds"] for r in have_both)
            median_delta = deltas[len(deltas) // 2]
            f.write(
                f"\nDelta is acquisition start minus bolus start, in seconds. "
                f"Median {median_delta:.1f}s, minimum {deltas[0]:.1f}s, "
                f"maximum {deltas[-1]:.1f}s.\n\n"
            )

            f.write("#### Timing Verdict against Description-Based Category\n\n")
            f.write(
                "Denominators are decidable series only, not all series in the category.\n\n"
            )
            f.write("| selection_category | Decidable | post_contrast | pre_contrast |\n")
            f.write("|---|---:|---:|---:|\n")
            decidable_categories = Counter(r["selection_category"] for r in have_both)
            for category, count in sorted(decidable_categories.items()):
                post = sum(
                    1 for r in have_both
                    if r["selection_category"] == category
                    and r["contrast_timing_class"] == "post_contrast"
                )
                pre = sum(
                    1 for r in have_both
                    if r["selection_category"] == category
                    and r["contrast_timing_class"] == "pre_contrast"
                )
                f.write(f"| {category or '(unknown)'} | {count} | {post} | {pre} |\n")

            disagreements = [
                r for r in have_both
                if (r["selection_category"] == "preferred_t1_postcontrast"
                    and r["contrast_timing_class"] == "pre_contrast")
            ]
            f.write(
                f"\nSeries described as post-contrast but acquired before the bolus: "
                f"{len(disagreements)}\n"
            )
            if disagreements:
                f.write("\n| PatientID | Delta (s) | SeriesDescription |\n")
                f.write("|---|---:|---|\n")
                for row in disagreements[:20]:
                    f.write(
                        f"| {row['patient_id']} | {row['contrast_timing_delta_seconds']} | "
                        f"{str(row['series_description']).replace('|', '/')} |\n"
                    )

        f.write("\n### Header Contrast versus Description-Based Category\n\n")
        f.write(
            "The selection step infers contrast from SeriesDescription. This cross-tab "
            "checks that inference against the header.\n\n"
        )
        f.write("| selection_category | Series | ContrastBolusAgent present |\n")
        f.write("|---|---:|---:|\n")
        category_counts = Counter(row["selection_category"] for row in series_rows)
        for category, count in sorted(category_counts.items()):
            present = sum(
                1 for r in series_rows
                if r["selection_category"] == category and r["has_contrast_bolus_agent"]
            )
            f.write(f"| {category or '(unknown)'} | {count} | {present} |\n")

        f.write(
            "\nIf ContrastBolusAgent is absent across the cohort, contrast status cannot "
            "be verified from headers at all and remains inferred from free text. Record "
            "that as a limitation rather than treating the description as confirmation.\n"
        )

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

    print(f"DICOM files inspected: {len(files)}")
    print(f"Non-DICOM sidecar files set aside: {len(sidecar_files)}")
    print(f"DICOM files with missing/blank SeriesInstanceUID: {len(missing_uid_files)}")
    print(f"Files read as DICOM: {len(rows)}")
    print(f"Read errors: {len(read_errors)}")
    print(f"Files with readable pixel arrays: {pixel_readable_total}")
    print(f"Unique series: {len(series_file_counts)}")
    print(f"Unique patients: {len(set(row['patient_id'] for row in rows))}")
    print(f"Report written to: {REPORT_PATH}")
    print(f"Series summary CSV written to: {SERIES_SUMMARY_CSV}")

    if missing_uid_files:
        raise RuntimeError(
            f"{len(missing_uid_files)} DICOM files have a missing or blank "
            "SeriesInstanceUID and cannot be attributed to a series. They have not been "
            "binned under a placeholder or skipped silently; resolve them before "
            "inspecting the cohort.\nFirst:\n  "
            + "\n  ".join(missing_uid_files[:10])
        )

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

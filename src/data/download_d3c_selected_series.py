from pathlib import Path
from datetime import datetime
import pandas as pd
from tcia_utils import nbia

COLLECTION = "UPENN-GBM"

RAW_OUT_DIR = Path("data/raw/D3C_upenn_gbm")
REPORT_DIR = Path("reports/datasets/d3c_selected_series_download")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# The authoritative selection, produced by src/data/select_d3c_upenn_gbm_series.py.
# This script must never re-derive it. A second, independent implementation of the
# selection rule used to live here and silently disagreed: it dropped 39 patients
# (37 of them preferred_t1_postcontrast) and picked a different series for 28 more,
# with the outcome varying between runs because it depended on TCIA row order.
SELECTION_CSV = Path(
    "reports/datasets/d3c_upenn_gbm_series_selection/selected_series_one_per_patient.csv"
)

SELECTED_SERIES_CSV = REPORT_DIR / "selected_series_one_per_patient.csv"
DOWNLOAD_METADATA_CSV = REPORT_DIR / "download_metadata.csv"
DOWNLOAD_FAILURES_CSV = REPORT_DIR / "download_failures.csv"
ACQUISITION_LOG = Path("reports/datasets/D3C_acquisition_log.md")

MAX_WORKERS = 4

REQUIRED_COLUMNS = ["PatientID", "SeriesInstanceUID", "selection_category"]

FAILURE_COLUMNS = [
    "PatientID",
    "SeriesInstanceUID",
    "selection_category",
    "expected_path",
    "failure_reason",
]


def load_selected_series():
    """Read the one-series-per-patient manifest written by the selection step."""
    if not SELECTION_CSV.exists():
        raise FileNotFoundError(
            f"Selection manifest not found: {SELECTION_CSV}\n"
            "Run src/data/select_d3c_upenn_gbm_series.py before downloading."
        )

    selected = pd.read_csv(SELECTION_CSV)

    if selected.empty:
        raise RuntimeError(f"{SELECTION_CSV} contains no rows.")

    missing_columns = [c for c in REQUIRED_COLUMNS if c not in selected.columns]
    if missing_columns:
        raise ValueError(
            f"{SELECTION_CSV} is missing required columns: {missing_columns}"
        )

    selected["SeriesInstanceUID"] = (
        selected["SeriesInstanceUID"].astype(str).str.strip()
    )

    blank = selected["SeriesInstanceUID"].isin(["", "nan", "None"])
    if blank.any():
        raise ValueError(
            f"{SELECTION_CSV} has {int(blank.sum())} rows with no SeriesInstanceUID."
        )

    duplicate_series = int(selected["SeriesInstanceUID"].duplicated().sum())
    if duplicate_series:
        raise ValueError(
            f"{SELECTION_CSV} has {duplicate_series} duplicate SeriesInstanceUID rows."
        )

    duplicate_patients = int(selected["PatientID"].duplicated().sum())
    if duplicate_patients:
        raise ValueError(
            f"{SELECTION_CSV} has {duplicate_patients} patients with more than one "
            "series. The selection step must yield exactly one series per patient."
        )

    return selected


def audit_downloads(selected, download_metadata):
    """Return one row per selected series that is not present on disk, with a reason."""
    metadata_uids = set()
    if (
        download_metadata is not None
        and "SeriesInstanceUID" in download_metadata.columns
    ):
        metadata_uids = set(
            download_metadata["SeriesInstanceUID"].astype(str).str.strip()
        )

    failures = []

    for row in selected.itertuples(index=False):
        series_uid = str(row.SeriesInstanceUID)
        target_dir = RAW_OUT_DIR / series_uid

        if not target_dir.exists():
            failure_reason = "directory_not_created"
        elif not any(p.is_file() for p in target_dir.iterdir()):
            failure_reason = "directory_empty"
        elif metadata_uids and series_uid not in metadata_uids:
            failure_reason = "absent_from_download_metadata"
        else:
            continue

        failures.append({
            "PatientID": row.PatientID,
            "SeriesInstanceUID": series_uid,
            "selection_category": row.selection_category,
            "expected_path": str(target_dir),
            "failure_reason": failure_reason,
        })

    return pd.DataFrame(failures, columns=FAILURE_COLUMNS)


def write_acquisition_log(selected, download_metadata, failures, downloaded_count):
    ACQUISITION_LOG.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now().isoformat(timespec="seconds")

    selected_category_counts = selected["selection_category"].value_counts().sort_index()

    with ACQUISITION_LOG.open("w", encoding="utf-8") as f:
        f.write("# D3C Acquisition Log - UPENN-GBM Selected Series\n\n")

        f.write("## Acquisition Date\n")
        f.write(f"{now}\n\n")

        f.write("## Dataset\n")
        f.write("UPENN-GBM\n\n")

        f.write("## Dataset Role\n")
        f.write(
            "Glioma-focused external domain-shift candidate. This dataset is not a direct "
            "four-class external validation dataset for D1.\n\n"
        )

        f.write("## Collection\n")
        f.write(f"`{COLLECTION}`\n\n")

        f.write("## Local Raw Path\n")
        f.write(f"`{RAW_OUT_DIR}`\n\n")

        f.write("## Download Method\n")
        f.write("Downloaded selected SeriesInstanceUIDs using `tcia_utils.nbia.downloadSeries`.\n\n")

        f.write("```python\n")
        f.write("nbia.downloadSeries(series_uids, input_type='list', path='data/raw/D3C_upenn_gbm')\n")
        f.write("```\n\n")

        f.write("## Selection Rule\n")
        f.write(
            "This script performs no selection of its own. It downloads exactly the "
            f"SeriesInstanceUIDs listed in `{SELECTION_CSV}`, which is produced by "
            "`src/data/select_d3c_upenn_gbm_series.py` according to "
            "`reports/datasets/D3C_sequence_selection_protocol.md`.\n\n"
        )

        f.write("Priority applied by the selection step:\n\n")
        f.write("1. Preferred T1 post-contrast / contrast-enhanced anatomical series.\n")
        f.write("2. Secondary non-contrast T1 anatomical series.\n\n")

        f.write("## Selected Series Summary\n\n")
        f.write(f"- Selection manifest: `{SELECTION_CSV}`\n")
        f.write(f"- Selected patients: {selected['PatientID'].nunique()}\n")
        f.write(f"- Selected series: {len(selected)}\n")
        f.write(f"- Series present on disk after download: {downloaded_count}\n")
        f.write(f"- Failed series: {len(failures)}\n\n")

        f.write("## Selected Category Counts\n\n")
        f.write("| Category | Count |\n")
        f.write("|---|---:|\n")
        for category, count in selected_category_counts.items():
            f.write(f"| {category} | {count} |\n")

        f.write("\n## Download Metadata\n\n")
        if download_metadata is not None and not download_metadata.empty:
            f.write(f"- Download metadata rows: {len(download_metadata)}\n")
            f.write(f"- Download metadata file: `{DOWNLOAD_METADATA_CSV}`\n")
        else:
            f.write("- Download metadata was not returned or was empty.\n")

        f.write("\n## Download Failures\n\n")
        if failures.empty:
            f.write(
                f"None. All {len(selected)} selected series are present on disk, so the "
                "downloaded cohort matches the selected cohort exactly.\n"
            )
        else:
            f.write(f"- Failed series: {len(failures)}\n")
            f.write(f"- Failure detail: `{DOWNLOAD_FAILURES_CSV}`\n\n")
            f.write("| Failure reason | Count |\n")
            f.write("|---|---:|\n")
            for reason, count in failures["failure_reason"].value_counts().sort_index().items():
                f.write(f"| {reason} | {count} |\n")
            f.write(
                "\nThis cohort is incomplete and must not be used for evaluation until "
                "the failures are resolved and the download is re-run.\n"
            )

        f.write("\n## Important Limitation\n\n")
        f.write(
            "D3C contains glioma cases only. It must not be used to claim full four-class "
            "external validation. It will be used only for glioma-focused domain-shift "
            "confidence analysis.\n"
        )


def main():
    RAW_OUT_DIR.mkdir(parents=True, exist_ok=True)

    selected = load_selected_series()

    # Record exactly what this run attempted, copied from the authoritative manifest.
    selected.to_csv(SELECTED_SERIES_CSV, index=False)

    series_uids = selected["SeriesInstanceUID"].tolist()

    print(f"Selection manifest: {SELECTION_CSV}")
    print(f"Selected patients: {selected['PatientID'].nunique()}")
    print(f"Selected series: {len(series_uids)}")
    print(f"Download output directory: {RAW_OUT_DIR}")

    print("\nSelected category counts:")
    print(selected["selection_category"].value_counts().sort_index().to_string())

    print("\nStarting selected-series download...")
    print("This may take time depending on series size and network speed.")

    download_metadata = nbia.downloadSeries(
        series_uids,
        input_type="list",
        path=str(RAW_OUT_DIR),
        format="df",
        csv_filename=str(DOWNLOAD_METADATA_CSV),
        as_zip=False,
        max_workers=MAX_WORKERS,
    )

    if isinstance(download_metadata, pd.DataFrame):
        download_metadata.to_csv(DOWNLOAD_METADATA_CSV, index=False)
        print(f"Download metadata rows: {len(download_metadata)}")
    else:
        print(f"Download metadata type: {type(download_metadata)}")
        download_metadata = None

    failures = audit_downloads(selected, download_metadata)
    failures.to_csv(DOWNLOAD_FAILURES_CSV, index=False)

    downloaded_count = len(selected) - len(failures)

    write_acquisition_log(selected, download_metadata, failures, downloaded_count)

    print(f"\nSelected series: {len(selected)}")
    print(f"Series present on disk: {downloaded_count}")
    print(f"Failed series: {len(failures)}")
    print(f"Raw output directory: {RAW_OUT_DIR}")
    print(f"Selected series CSV: {SELECTED_SERIES_CSV}")
    print(f"Acquisition log: {ACQUISITION_LOG}")

    if not failures.empty:
        print(f"\nFailure detail written to: {DOWNLOAD_FAILURES_CSV}")
        print(failures["failure_reason"].value_counts().sort_index().to_string())
        print("\nFirst failed series:")
        print(failures.head(10).to_string(index=False))

        raise RuntimeError(
            f"Downloaded {downloaded_count} of {len(selected)} selected series. "
            f"{len(failures)} failed; see {DOWNLOAD_FAILURES_CSV}. The downloaded "
            "cohort must match the selected cohort exactly before D3C is used."
        )

    print("\nDownload complete. Downloaded cohort matches selected cohort exactly.")


if __name__ == "__main__":
    main()

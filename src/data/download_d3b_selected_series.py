from pathlib import Path
from datetime import datetime
import re
import pandas as pd
from tcia_utils import nbia

COLLECTION = "ICDC-Glioma"

RAW_OUT_DIR = Path("data/raw/D3B_icdc_glioma")
REPORT_DIR = Path("reports/datasets/d3b_selected_series_download")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

SELECTED_SERIES_CSV = REPORT_DIR / "selected_series_one_per_patient.csv"
DOWNLOAD_METADATA_CSV = REPORT_DIR / "download_metadata.csv"
ACQUISITION_LOG = Path("reports/datasets/D3B_acquisition_log.md")

MAX_WORKERS = 4


PREFERRED_T1_POSTCONTRAST_TERMS = [
    "t1+c",
    "t1 +c",
    "t1 + c",
    "t1 post",
    "t1 post gad",
    "t1 ce",
    "t1 gd",
    "t1 fs trans +c",
    "t1/sag/se +c",
    "t1/d/se +c",
    "t1/t/se +c",
    "mprage +c",
    "mprage post",
    "mp rage +c",
    "mp rage fs +c",
    "mp rage trans fs + c",
    "mp rage trans +c",
    "mp rage sag +c",
    "rage trans +c",
    "rage trans + c",
    "rage sag +c",
    "rage sag + c",
    "rage fs trans +c",
    "ax_t1_fl2d post",
    "sag_t1_fl2d post",
    "ax t1 fl2d post",
    "sag t1 fl2d post",
    "brain/t1_trans+c",
    "brain/t1_sag+c",
    "brain/t1_dors+c",
    "t1 trans +c",
    "t1 sag +c",
    "t1 axial +c",
    "t1 ax +c",
    "t1 cor +c",
    "t1 dorsal +c",
    "spgr +c",
    "3dt1 spgr",
    "3d t1 spgr",
]

SECONDARY_T1_TERMS = [
    "t1 axial",
    "t1 ax",
    "t1 sag",
    "t1 sagittal",
    "t1 cor",
    "t1 coronal",
    "t1 flair",
    "t1 se",
    "t1 trans",
    "t1 dorsal",
    "t1/t/se",
    "t1/d/se",
    "t1/sag/se",
    "ax fse t1",
    "sag fse t1",
    "o ax t1 se",
    "o sag t1 se",
    "brain/t1_trans",
    "brain/t1_sag",
    "brain/t1_dors",
    "rage trans",
    "rage sag",
    "rage dorsal",
    "mp rage",
    "mprage",
    "spgr",
    "3dt1",
    "3d t1",
]

LOCALIZER_TERMS = [
    "localizer",
    "locator",
    "scout",
    "3 plane",
    "3-plane",
    "3 pl",
    "3-pl",
    "screen save",
]

DWI_ADC_TERMS = [
    "dwi",
    "adc",
    "trace",
    "diffusion",
    "dti",
]

T2_FLAIR_PD_TERMS = [
    "t2",
    "flair",
    "t2star",
    "t2 star",
    "gre t2",
    "gre_t2",
    "pd t2",
    "pd",
    "frfse",
    "fse t2",
]

SPINE_NONBRAIN_TERMS = [
    "spine",
    "cervical",
    "lumbar",
    "thoracic",
]

DERIVED_TERMS = [
    "created from",
    "secondary capture",
    "reformat",
    "reformatted",
    "subtraction",
]

EXPLICIT_T1_EVIDENCE_TERMS = [
    "t1",
    "rage",
    "mprage",
    "mp rage",
    "spgr",
    "3dt1",
    "3d t1",
    "fl2d",
]


def normalize_text(value):
    if pd.isna(value):
        return ""

    text = str(value).lower()
    text = text.replace("_", " ")
    text = text.replace("-", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def contains_any(text, terms):
    return any(term in text for term in terms)


def classify_series(row):
    description = normalize_text(row.get("SeriesDescription", ""))
    protocol = normalize_text(row.get("ProtocolName", ""))
    body_part = normalize_text(row.get("BodyPartExamined", ""))

    combined = " ".join([description, protocol, body_part]).strip()

    has_t1_evidence = contains_any(combined, EXPLICIT_T1_EVIDENCE_TERMS)
    has_postcontrast_evidence = contains_any(combined, PREFERRED_T1_POSTCONTRAST_TERMS)
    has_secondary_t1_evidence = contains_any(combined, SECONDARY_T1_TERMS)
    has_t2_flair_pd_evidence = contains_any(combined, T2_FLAIR_PD_TERMS)

    if contains_any(combined, SPINE_NONBRAIN_TERMS):
        return "excluded_spine_nonbrain"

    if contains_any(combined, LOCALIZER_TERMS):
        return "excluded_localizer"

    if contains_any(combined, DWI_ADC_TERMS):
        return "excluded_dwi_adc"

    if has_t2_flair_pd_evidence and not has_t1_evidence:
        return "excluded_t2_flair"

    if has_postcontrast_evidence and has_t1_evidence:
        return "preferred_t1_postcontrast"

    if has_secondary_t1_evidence:
        return "secondary_t1"

    if has_t2_flair_pd_evidence:
        return "excluded_t2_flair"

    if contains_any(combined, DERIVED_TERMS):
        return "excluded_derived"

    return "excluded_other"


def category_priority(category):
    priorities = {
        "preferred_t1_postcontrast": 1,
        "secondary_t1": 2,
    }
    return priorities.get(category, 99)


def fetch_series_metadata():
    print(f"Fetching series metadata for collection: {COLLECTION}")
    series = nbia.getSeries(collection=COLLECTION)

    if series is None:
        raise RuntimeError("nbia.getSeries returned None.")

    df = pd.DataFrame(series)

    if df.empty:
        raise RuntimeError("No series metadata returned.")

    return df


def select_one_series_per_patient(df):
    df = df.copy()
    df["selection_category"] = df.apply(classify_series, axis=1)

    eligible = df[df["selection_category"].isin([
        "preferred_t1_postcontrast",
        "secondary_t1",
    ])].copy()

    if eligible.empty:
        raise RuntimeError("No eligible series found.")

    eligible["selection_priority"] = eligible["selection_category"].apply(category_priority)

    if "ImageCount" in eligible.columns:
        eligible["ImageCount_numeric"] = pd.to_numeric(
            eligible["ImageCount"],
            errors="coerce"
        ).fillna(0)
    else:
        eligible["ImageCount_numeric"] = 0

    eligible = eligible.sort_values(
        [
            "PatientID",
            "selection_priority",
            "ImageCount_numeric",
            "SeriesDescription",
            "SeriesInstanceUID",
        ],
        ascending=[True, True, False, True, True],
    )

    selected = eligible.groupby("PatientID", as_index=False).first()

    return selected


def write_acquisition_log(selected, download_metadata):
    ACQUISITION_LOG.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now().isoformat(timespec="seconds")

    selected_category_counts = selected["selection_category"].value_counts().sort_index()

    with ACQUISITION_LOG.open("w", encoding="utf-8") as f:
        f.write("# D3B Acquisition Log ? ICDC-Glioma Selected Series\n\n")

        f.write("## Acquisition Date\n")
        f.write(f"{now}\n\n")

        f.write("## Dataset\n")
        f.write("ICDC-Glioma\n\n")

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
        f.write("nbia.downloadSeries(series_uids, input_type='list', path='data/raw/D3B_icdc_glioma')\n")
        f.write("```\n\n")

        f.write("## Selection Rule\n")
        f.write(
            "At most one eligible T1-like series was selected per patient according to "
            "`reports/datasets/D3B_sequence_selection_protocol.md`.\n\n"
        )

        f.write("Priority:\n\n")
        f.write("1. Preferred T1 post-contrast / contrast-enhanced anatomical series.\n")
        f.write("2. Secondary non-contrast T1 anatomical series.\n\n")

        f.write("## Selected Series Summary\n\n")
        f.write(f"- Selected patients: {selected['PatientID'].nunique()}\n")
        f.write(f"- Selected series: {len(selected)}\n\n")

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

        f.write("\n## Important Limitation\n\n")
        f.write(
            "D3B contains glioma cases only. It must not be used to claim full four-class "
            "external validation. It will be used only for glioma-focused domain-shift "
            "confidence analysis.\n"
        )


def main():
    RAW_OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = fetch_series_metadata()
    selected = select_one_series_per_patient(df)

    selected.to_csv(SELECTED_SERIES_CSV, index=False)

    series_uids = selected["SeriesInstanceUID"].dropna().astype(str).tolist()

    print(f"Selected patients: {selected['PatientID'].nunique()}")
    print(f"Selected series: {len(series_uids)}")
    print(f"Selected series CSV: {SELECTED_SERIES_CSV}")
    print(f"Download output directory: {RAW_OUT_DIR}")

    if not series_uids:
        raise RuntimeError("No SeriesInstanceUIDs selected.")

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

    write_acquisition_log(selected, download_metadata if isinstance(download_metadata, pd.DataFrame) else None)

    print("\nDownload complete.")
    print(f"Raw output directory: {RAW_OUT_DIR}")
    print(f"Selected series CSV: {SELECTED_SERIES_CSV}")
    print(f"Acquisition log: {ACQUISITION_LOG}")


if __name__ == "__main__":
    main()

from pathlib import Path
import re

import pandas as pd
from tcia_utils import nbia

COLLECTION = "ICDC-Glioma"

OUT_DIR = Path("reports/datasets/d3b_icdc_glioma_series_selection")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SERIES_CSV = OUT_DIR / "all_series.csv"
CLASSIFIED_CSV = OUT_DIR / "classified_series.csv"
SELECTED_CSV = OUT_DIR / "selected_series_one_per_patient.csv"
REPORT_PATH = Path("reports/datasets/D3B_series_selection_report.md")


PREFERRED_T1_POSTCONTRAST_TERMS = [
    "t1+c",
    "t1 +c",
    "t1 + c",
    "t1 post",
    "t1 post gad",
    "t1-post gad",
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


def safe_call(name, func, **kwargs):
    print(f"Calling {name} with parameters: {kwargs}")

    try:
        result = func(**kwargs)
    except Exception as exc:
        raise RuntimeError(f"{name} failed: {repr(exc)}") from exc

    if result is None:
        raise RuntimeError(f"{name} returned None.")

    if not isinstance(result, list):
        raise RuntimeError(f"{name} returned unexpected type: {type(result)}")

    print(f"{name} returned {len(result)} rows.")
    return result


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

    # Strong safeguard:
    # A series that clearly says T2/FLAIR/PD should not be accepted just because
    # the protocol text contains loose words such as "post" or "+C".
    # It can only pass if there is explicit T1/RAGE/MPRAGE/SPGR evidence.
    if has_t2_flair_pd_evidence and not has_t1_evidence:
        return "excluded_t2_flair"

    # Preferred category requires both post-contrast evidence and explicit T1-like evidence.
    # This prevents cases such as:
    # SeriesDescription = "O-Ax T2 frFSE S", ProtocolName = "CED Post/3"
    # from being falsely classified as T1 post-contrast.
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
        "excluded_localizer": 9,
        "excluded_dwi_adc": 9,
        "excluded_t2_flair": 9,
        "excluded_spine_nonbrain": 9,
        "excluded_derived": 9,
        "excluded_other": 9,
    }
    return priorities.get(category, 99)


def select_one_series_per_patient(df):
    eligible = df[df["selection_category"].isin([
        "preferred_t1_postcontrast",
        "secondary_t1",
    ])].copy()

    if eligible.empty:
        return eligible

    eligible["selection_priority"] = eligible["selection_category"].apply(category_priority)

    if "ImageCount" in eligible.columns:
        eligible["ImageCount_numeric"] = pd.to_numeric(
            eligible["ImageCount"],
            errors="coerce"
        ).fillna(0)
    else:
        eligible["ImageCount_numeric"] = 0

    sort_cols = [
        "PatientID",
        "selection_priority",
        "ImageCount_numeric",
        "SeriesDescription",
        "SeriesInstanceUID",
    ]

    ascending = [
        True,
        True,
        False,
        True,
        True,
    ]

    eligible = eligible.sort_values(sort_cols, ascending=ascending)

    selected = eligible.groupby("PatientID", as_index=False).first()

    return selected


def write_report(df, selected):
    total_series = len(df)
    total_patients = df["PatientID"].nunique() if "PatientID" in df.columns else 0
    selected_patients = (
        selected["PatientID"].nunique()
        if not selected.empty and "PatientID" in selected.columns
        else 0
    )

    category_counts = df["selection_category"].value_counts().sort_index()

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D3B Series Selection Report - ICDC-Glioma\n\n")

        f.write("## Input\n\n")
        f.write(f"- Collection: `{COLLECTION}`\n")
        f.write(f"- Total series returned: {total_series}\n")
        f.write(f"- Unique patients: {total_patients}\n\n")

        f.write("## Selection Rule\n\n")
        f.write(
            "Series were classified using SeriesDescription, ProtocolName, "
            "and BodyPartExamined.\n\n"
        )
        f.write("Priority order:\n\n")
        f.write("1. Preferred T1 post-contrast / contrast-enhanced anatomical series.\n")
        f.write("2. Secondary non-contrast T1 anatomical series.\n")
        f.write(
            "3. Exclude localizers, DWI/ADC, T2/FLAIR/PD-only, spine/non-brain, "
            "derived, and other unsupported series.\n\n"
        )
        f.write(
            "A stricter rule was applied so that broad post-contrast terms such as "
            "`post` or `+C` do not override clear T2/FLAIR/PD evidence unless explicit "
            "T1/RAGE/MPRAGE/SPGR evidence is also present.\n\n"
        )
        f.write("At most one eligible series was selected per patient.\n\n")

        f.write("## Classification Counts\n\n")
        f.write("| Category | Count |\n")
        f.write("|---|---:|\n")
        for category, count in category_counts.items():
            f.write(f"| {category} | {count} |\n")

        f.write("\n## Selected Series Summary\n\n")
        f.write(f"- Patients with selected eligible series: {selected_patients}\n")
        f.write(f"- Selected series count: {len(selected)}\n\n")

        if not selected.empty:
            selected_counts = selected["selection_category"].value_counts().sort_index()

            f.write("## Selected Category Counts\n\n")
            f.write("| Category | Count |\n")
            f.write("|---|---:|\n")
            for category, count in selected_counts.items():
                f.write(f"| {category} | {count} |\n")

            f.write("\n## Example Selected Series\n\n")
            f.write("| PatientID | SeriesDescription | ProtocolName | ImageCount | Category |\n")
            f.write("|---|---|---|---:|---|\n")

            for _, row in selected.head(25).iterrows():
                f.write(
                    f"| {row.get('PatientID', '')} | "
                    f"{str(row.get('SeriesDescription', '')).replace('|', '/')} | "
                    f"{str(row.get('ProtocolName', '')).replace('|', '/')} | "
                    f"{row.get('ImageCount', '')} | "
                    f"{row.get('selection_category', '')} |\n"
                )

        f.write("\n## Interpretation\n\n")
        f.write(
            "This report does not download images. It only identifies candidate MRI series "
            "for a future controlled DICOM acquisition. ICDC-Glioma remains a glioma-focused "
            "domain-shift candidate, not a direct four-class external validation dataset.\n\n"
        )

        f.write(
            "The selected series list should be manually reviewed before DICOM download, "
            "especially because MRI series descriptions are heterogeneous and may contain "
            "institution-specific naming conventions.\n"
        )


def main():
    print(f"Fetching series metadata for collection: {COLLECTION}")

    series = safe_call("getSeries", nbia.getSeries, collection=COLLECTION)
    df = pd.DataFrame(series)

    if df.empty:
        raise RuntimeError("No series metadata returned.")

    df.to_csv(SERIES_CSV, index=False)

    df["selection_category"] = df.apply(classify_series, axis=1)

    selected = select_one_series_per_patient(df)

    df.to_csv(CLASSIFIED_CSV, index=False)
    selected.to_csv(SELECTED_CSV, index=False)

    write_report(df, selected)

    print(f"All series saved to: {SERIES_CSV}")
    print(f"Classified series saved to: {CLASSIFIED_CSV}")
    print(f"Selected series saved to: {SELECTED_CSV}")
    print(f"Report written to: {REPORT_PATH}")

    print("\nSelection category counts:")
    print(df["selection_category"].value_counts().sort_index().to_string())

    print("\nSelected series count:", len(selected))
    if not selected.empty:
        print("Selected patients:", selected["PatientID"].nunique())
        print("\nSelected category counts:")
        print(selected["selection_category"].value_counts().sort_index().to_string())


if __name__ == "__main__":
    main()

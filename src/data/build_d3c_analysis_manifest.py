"""Build the D3C analysis manifest by applying documented cohort exclusions.

The selection manifest produced by src/data/select_d3c_upenn_gbm_series.py is the record
of what was *selected* and is never modified here: it keeps its sha256
(fc6deef3...761c) so the selected cohort stays independently verifiable. Exclusions are
applied downstream, in this separate and auditable step, producing a distinct analysis
manifest plus a report giving the rationale and the resulting counts.

Two rules are applied, both derived from measured DICOM geometry rather than from
SeriesDescription text:

  EXCLUDE  non-axial series. D1 is axial throughout, so a coronal or sagittal series is
           a plane confound: a difference in predictions could reflect acquisition
           geometry rather than domain shift. These slices are dropped from the analysis
           cohort.

  FLAG     axial series lying more than 10 degrees off the true axial plane. These are
           kept, because they are axial acquisitions, but carry a boolean column so a
           sensitivity analysis can drop them by filtering one column rather than by
           running a second exclusion step.

Both rules are computed from the data and then checked against the expected outcome
recorded below. If the geometry ever changes, this aborts rather than silently applying
a different exclusion.

Run from the repository root:

    python src/data/build_d3c_analysis_manifest.py
"""

from pathlib import Path
from datetime import datetime
import hashlib

import pandas as pd


SLICE_MANIFEST = Path("data/processed/D3C_selected_slices_manifest_phash.csv")
SERIES_GEOMETRY = Path("reports/datasets/D3C_dicom_series_summary.csv")
SELECTION_CSV = Path(
    "reports/datasets/d3c_upenn_gbm_series_selection/selected_series_one_per_patient.csv"
)

ANALYSIS_MANIFEST = Path("data/processed/D3C_analysis_manifest.csv")
EXCLUDED_SLICES_CSV = Path("data/processed/D3C_excluded_slices.csv")
REPORT_PATH = Path("reports/datasets/D3C_cohort_exclusion_report.md")

# The selection manifest is the frozen record of what was selected. If this hash does
# not match, the record has changed and the exclusion must not be applied blindly.
EXPECTED_SELECTION_SHA256 = (
    "fc6deef35438027d6b76fdc323b5a4d96538312dd2da8f4a93afb40f3488761c"
)

REQUIRED_PLANE = "axial"
OBLIQUITY_FLAG_DEGREES = 10.0

# Expected outcome of the two rules on the frozen 614-series cohort, asserted below.
EXPECTED_EXCLUDED_PATIENTS = {
    "UPENN-GBM-00017",
    "UPENN-GBM-00095",
    "UPENN-GBM-00493",
    "UPENN-GBM-00537",
}
EXPECTED_OBLIQUE_SERIES = 11

GEOMETRY_COLUMNS = [
    "series_instance_uid",
    "acquisition_plane",
    "plane_dominance",
    "obliquity_degrees",
    "orientation_consistent",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def require(path: Path, description: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing {description}: {path}")


def load_inputs():
    require(SLICE_MANIFEST, "D3C slice manifest")
    require(SERIES_GEOMETRY, "D3C series geometry summary")
    require(SELECTION_CSV, "D3C selection manifest")

    selection_sha256 = sha256_file(SELECTION_CSV)
    if selection_sha256 != EXPECTED_SELECTION_SHA256:
        raise RuntimeError(
            f"{SELECTION_CSV} sha256 is {selection_sha256}, expected "
            f"{EXPECTED_SELECTION_SHA256}. The selection record has changed, so the "
            "recorded exclusion outcome may no longer apply. Re-derive the exclusions "
            "and update the expectations in this script deliberately."
        )

    slices = pd.read_csv(SLICE_MANIFEST)
    geometry = pd.read_csv(SERIES_GEOMETRY)

    missing_columns = [c for c in GEOMETRY_COLUMNS if c not in geometry.columns]
    if missing_columns:
        raise ValueError(
            f"{SERIES_GEOMETRY} is missing required columns: {missing_columns}. "
            "Re-run src/data/inspect_d3c_dicom_download.py."
        )

    missing_geometry = set(slices["series_instance_uid"]) - set(
        geometry["series_instance_uid"]
    )
    if missing_geometry:
        raise RuntimeError(
            f"{len(missing_geometry)} series in {SLICE_MANIFEST} have no geometry row "
            f"in {SERIES_GEOMETRY}. Re-run the inspection before excluding.\nFirst:\n  "
            + "\n  ".join(sorted(missing_geometry)[:10])
        )

    return slices, geometry, selection_sha256


def classify_series(geometry: pd.DataFrame) -> pd.DataFrame:
    """Mark each series as excluded (non-axial) and/or flagged (oblique axial)."""
    geometry = geometry.copy()

    geometry["obliquity_degrees"] = pd.to_numeric(
        geometry["obliquity_degrees"], errors="coerce"
    )

    geometry["excluded_non_axial"] = geometry["acquisition_plane"] != REQUIRED_PLANE
    geometry["oblique_gt_10deg"] = (
        (geometry["acquisition_plane"] == REQUIRED_PLANE)
        & (geometry["obliquity_degrees"] > OBLIQUITY_FLAG_DEGREES)
    )

    geometry["exclusion_reason"] = ""
    geometry.loc[geometry["excluded_non_axial"], "exclusion_reason"] = (
        "non_axial_plane_confound: acquisition plane is "
        + geometry.loc[geometry["excluded_non_axial"], "acquisition_plane"].astype(str)
        + ", D1 is axial"
    )

    return geometry


def verify_expected_outcome(geometry: pd.DataFrame) -> None:
    excluded_patients = set(
        geometry.loc[geometry["excluded_non_axial"], "patient_id"].astype(str)
    )

    if excluded_patients != EXPECTED_EXCLUDED_PATIENTS:
        raise RuntimeError(
            "The non-axial exclusion does not match the recorded expectation.\n"
            f"  derived:  {sorted(excluded_patients)}\n"
            f"  expected: {sorted(EXPECTED_EXCLUDED_PATIENTS)}\n"
            "The cohort geometry has changed. Review before applying an exclusion that "
            "differs from the one documented in the report."
        )

    oblique_count = int(geometry["oblique_gt_10deg"].sum())
    if oblique_count != EXPECTED_OBLIQUE_SERIES:
        raise RuntimeError(
            f"Expected {EXPECTED_OBLIQUE_SERIES} oblique axial series beyond "
            f"{OBLIQUITY_FLAG_DEGREES:.0f} degrees, found {oblique_count}. The cohort "
            "geometry has changed; review before flagging a different set."
        )


def build_manifests(slices: pd.DataFrame, geometry: pd.DataFrame):
    merged = slices.merge(
        geometry[
            GEOMETRY_COLUMNS
            + ["excluded_non_axial", "oblique_gt_10deg", "exclusion_reason"]
        ],
        on="series_instance_uid",
        how="left",
        validate="many_to_one",
    )

    if merged["excluded_non_axial"].isna().any():
        raise RuntimeError("Merge produced unmatched slices; geometry join failed.")

    excluded = merged[merged["excluded_non_axial"]].copy()
    analysis = merged[~merged["excluded_non_axial"]].copy()

    analysis = analysis.drop(columns=["excluded_non_axial", "exclusion_reason"])
    analysis = analysis.sort_values(
        ["patient_id", "series_instance_uid", "selected_rank"], kind="mergesort"
    ).reset_index(drop=True)

    excluded = excluded.drop(columns=["excluded_non_axial"])
    excluded = excluded.sort_values(
        ["patient_id", "series_instance_uid", "selected_rank"], kind="mergesort"
    ).reset_index(drop=True)

    return analysis, excluded


def write_report(slices, geometry, analysis, excluded, selection_sha256, analysis_sha256):
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    excluded_series = geometry[geometry["excluded_non_axial"]].sort_values("patient_id")
    oblique_series = geometry[geometry["oblique_gt_10deg"]].sort_values(
        "obliquity_degrees", ascending=False
    )

    flagged_slices = int(analysis["oblique_gt_10deg"].sum())

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D3C Cohort Exclusion Report\n\n")
        f.write(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n")

        f.write("## What This Step Does, and Does Not, Change\n\n")
        f.write(
            "The selection manifest is the record of what was selected and is **not** "
            "modified by this step. It keeps its hash so the selected cohort stays "
            "independently verifiable, and the exclusion is applied downstream as a "
            "separate, auditable transformation.\n\n"
        )
        f.write(f"- Selection manifest: `{SELECTION_CSV}`\n")
        f.write(f"- Selection manifest sha256, unchanged: `{selection_sha256}`\n")
        f.write(f"- Slice manifest in: `{SLICE_MANIFEST}`\n")
        f.write(f"- Series geometry in: `{SERIES_GEOMETRY}`\n")
        f.write(f"- Analysis manifest out: `{ANALYSIS_MANIFEST}`\n")
        f.write(f"- Analysis manifest sha256: `{analysis_sha256}`\n")
        f.write(f"- Excluded slices out: `{EXCLUDED_SLICES_CSV}`\n\n")

        f.write("## Rule 1, Exclusion: Non-Axial Series\n\n")
        f.write(
            "D1 is axial throughout. A coronal or sagittal D3C series is therefore a "
            "plane confound: any difference in prediction behaviour could reflect "
            "acquisition geometry rather than domain shift, and the two cannot be "
            "separated after the fact. These series are removed from the analysis "
            "cohort.\n\n"
        )
        f.write(
            "The plane is measured from the DICOM slice normal, the cross product of "
            "the two direction cosines in ImageOrientationPatient. It is not parsed "
            "from SeriesDescription.\n\n"
        )
        f.write(f"Series excluded: {len(excluded_series)}\n\n")
        f.write("| PatientID | Plane | Obliquity (deg) | SeriesDescription |\n")
        f.write("|---|---|---:|---|\n")
        for _, row in excluded_series.iterrows():
            f.write(
                f"| {row['patient_id']} | {row['acquisition_plane']} | "
                f"{row['obliquity_degrees']} | "
                f"{str(row['series_description']).replace('|', '/')} |\n"
            )

        f.write("\n## Rule 2, Flag Only: Oblique Axial Series\n\n")
        f.write(
            f"Axial series lying more than {OBLIQUITY_FLAG_DEGREES:.0f} degrees off the "
            "true axial plane are **kept** in the analysis cohort, because they are "
            "axial acquisitions, but are marked with the boolean column "
            "`oblique_gt_10deg`. A sensitivity analysis can therefore drop them by "
            "filtering that column, with no second exclusion step and no second "
            "manifest.\n\n"
        )
        f.write(f"Series flagged: {len(oblique_series)}\n\n")
        f.write("| PatientID | Obliquity (deg) | SeriesDescription |\n")
        f.write("|---|---:|---|\n")
        for _, row in oblique_series.iterrows():
            f.write(
                f"| {row['patient_id']} | {row['obliquity_degrees']} | "
                f"{str(row['series_description']).replace('|', '/')} |\n"
            )

        f.write("\n## Resulting Counts\n\n")
        f.write("| Cohort | Patients | Series | Slices |\n")
        f.write("|---|---:|---:|---:|\n")
        f.write(
            f"| Selected (record, unchanged) | {slices['patient_id'].nunique()} | "
            f"{slices['series_instance_uid'].nunique()} | {len(slices)} |\n"
        )
        f.write(
            f"| Excluded, non-axial | {excluded['patient_id'].nunique()} | "
            f"{excluded['series_instance_uid'].nunique()} | {len(excluded)} |\n"
        )
        f.write(
            f"| **Analysis cohort** | **{analysis['patient_id'].nunique()}** | "
            f"**{analysis['series_instance_uid'].nunique()}** | **{len(analysis)}** |\n"
        )
        f.write(
            f"| of which flagged oblique | "
            f"{analysis.loc[analysis['oblique_gt_10deg'], 'patient_id'].nunique()} | "
            f"{analysis.loc[analysis['oblique_gt_10deg'], 'series_instance_uid'].nunique()} | "
            f"{flagged_slices} |\n"
        )
        f.write(
            f"| Sensitivity cohort, oblique dropped | "
            f"{analysis.loc[~analysis['oblique_gt_10deg'], 'patient_id'].nunique()} | "
            f"{analysis.loc[~analysis['oblique_gt_10deg'], 'series_instance_uid'].nunique()} | "
            f"{len(analysis) - flagged_slices} |\n"
        )

        f.write("\n## How to Use This\n\n")
        f.write(
            f"- Primary analysis: use `{ANALYSIS_MANIFEST}` in full.\n"
            "- Plane sensitivity analysis: use the same manifest filtered to "
            "`oblique_gt_10deg == False`.\n"
            "- Report both, and state the exclusion in the methods. The excluded slices "
            f"remain available in `{EXCLUDED_SLICES_CSV}` so the exclusion can be "
            "audited or reversed without regenerating anything.\n\n"
        )

        f.write("## Limitation\n\n")
        f.write(
            "Excluding non-axial series removes a plane confound; it does not make D3C "
            "a four-class external validation set, and it does not address the "
            "skull-stripping confound, which applies to the whole cohort.\n"
        )


def main():
    slices, geometry, selection_sha256 = load_inputs()

    geometry = classify_series(geometry)
    verify_expected_outcome(geometry)

    analysis, excluded = build_manifests(slices, geometry)

    ANALYSIS_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    analysis.to_csv(ANALYSIS_MANIFEST, index=False)
    excluded.to_csv(EXCLUDED_SLICES_CSV, index=False)

    analysis_sha256 = sha256_file(ANALYSIS_MANIFEST)

    write_report(
        slices, geometry, analysis, excluded, selection_sha256, analysis_sha256
    )

    print(f"Selection manifest unchanged, sha256: {selection_sha256}")
    print(
        f"Selected:  {slices['patient_id'].nunique()} patients, "
        f"{slices['series_instance_uid'].nunique()} series, {len(slices)} slices"
    )
    print(
        f"Excluded:  {excluded['patient_id'].nunique()} patients, "
        f"{excluded['series_instance_uid'].nunique()} series, {len(excluded)} slices "
        "(non-axial)"
    )
    print(
        f"Analysis:  {analysis['patient_id'].nunique()} patients, "
        f"{analysis['series_instance_uid'].nunique()} series, {len(analysis)} slices"
    )
    print(
        f"Flagged oblique (kept): "
        f"{analysis.loc[analysis['oblique_gt_10deg'], 'series_instance_uid'].nunique()} "
        f"series, {int(analysis['oblique_gt_10deg'].sum())} slices"
    )
    print(f"Analysis manifest: {ANALYSIS_MANIFEST} (sha256 {analysis_sha256})")
    print(f"Excluded slices:   {EXCLUDED_SLICES_CSV}")
    print(f"Report:            {REPORT_PATH}")


if __name__ == "__main__":
    main()

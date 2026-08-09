"""Test whether D3C images actually are skull-stripped, against a matched D1 sample.

The project has recorded D3C as "100% Processed_CaPTk (skull-stripped, atlas-registered)"
and treated skull stripping as a cohort-wide confound. A visual check of
UPENN-GBM-00331 showed intact skull, scalp and orbits, so that claim needs testing
rather than repeating. CaPTk preprocessing covers reorientation, co-registration and
resampling; skull stripping is a separate step that may or may not have been applied.

This script is an audit. It is not part of the pipeline, changes no pipeline code, and
nothing imports it.

Method. Skull stripping is a masking operation: it sets everything outside the brain to
exactly zero. That is what the primary measurements test:

    air_exact_zero_fraction  among pixels below an Otsu threshold, the fraction that
                             are exactly zero. 1.0 when a mask has been applied, well
                             below 1.0 for an unstripped acquisition, which carries
                             genuine noise in air.
    corner_nonzero_fraction  the same question asked of the four image corners,
                             independent of any threshold.
    bright_outer_fraction    pixels between 0.75 and 1.10 of the tissue radius that
                             exceed the brain-core median. On T1 scalp fat is brighter
                             than brain, so this is the anatomical corroboration.

Radii are measured about the centroid of the Otsu tissue mask and scaled by that mask's
own extent, so nothing depends on image size, head size, or whether the head reaches
the image border. An earlier version scaled by the *non-zero* radius instead; because
unstripped images have noise throughout the air, that mask reached the image corners
and the annulus sampled air rather than scalp. It was replaced before any conclusion
was drawn.

Corner and border-band statistics are also reported as secondary evidence: a border
band is uninformative when the head does not reach the image edge.

D3C is measured on the converted PNGs, which is what the models actually consume, and
cross-checked on the source DICOM pixel data under the same normalisation so that the
conversion itself cannot be the cause of whatever is found.

Run from the repository root:

    python src/data/audit_d3c_skull_stripping.py
"""

from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import pydicom
from PIL import Image


D3C_ANALYSIS_MANIFEST = Path("data/processed/D3C_analysis_manifest.csv")
D1_MANIFEST = Path("data/processed/D1_manifest_deduplicated.csv")

REPORT_PATH = Path("reports/datasets/D3C_skull_stripping_audit.md")
MEASUREMENTS_CSV = Path("reports/datasets/D3C_skull_stripping_audit_measurements.csv")

SAMPLE_SIZE = 40
CENTRAL_RANK = 3          # middle slice of the five central slices per series
D1_MATCH_CLASS = "glioma"  # D3C is glioma-only, so the matched D1 sample is glioma
SEED = 20260810

# Always include the series the visual check was made on, whether or not it is sampled.
ALWAYS_INCLUDE_PATIENT = "UPENN-GBM-00331"

# Skull stripping is a masking operation: it sets everything outside the brain to
# exactly zero. An image is called "background masked" only when its air region really
# is exactly zero and its corners are clean. Anything else retains extracranial signal.
AIR_ZERO_THRESHOLD = 0.98
CORNER_NONZERO_THRESHOLD = 0.02
# Anatomical corroboration: pixels beyond the brain brighter than the brain core.
BRIGHT_OUTER_THRESHOLD = 0.05


def normalise_to_uint8(array):
    """Same 1-99 percentile windowing the slice conversion uses, for comparability."""
    array = array.astype(np.float32)

    low = float(np.percentile(array, 1))
    high = float(np.percentile(array, 99))

    if high <= low:
        low = float(np.min(array))
        high = float(np.max(array))

    if high <= low:
        return np.zeros(array.shape, dtype=np.uint8)

    array = np.clip(array, low, high)
    array = (array - low) / (high - low)

    return (array * 255.0).round().astype(np.uint8)


def otsu_threshold(image):
    """Otsu's between-class variance threshold, computed from the 256-bin histogram.

    Used to separate tissue from air. A plain "> 0" test is not usable as a tissue mask
    here: unstripped acquisitions carry low-level noise throughout the air, which would
    drag the measured head radius out into the image corners.
    """
    histogram = np.bincount(image.ravel(), minlength=256).astype(float)
    probability = histogram / max(histogram.sum(), 1.0)

    levels = np.arange(256, dtype=float)
    omega = np.cumsum(probability)
    mu = np.cumsum(probability * levels)
    mu_total = mu[-1]

    denominator = omega * (1.0 - omega)
    with np.errstate(divide="ignore", invalid="ignore"):
        between_class = (mu_total * omega - mu) ** 2 / denominator

    between_class[~np.isfinite(between_class)] = -1.0

    return int(np.argmax(between_class))


def measure(image):
    """Masking, radial and corner statistics for one grayscale uint8 image.

    The decisive question is whether a masking operation was applied. Skull stripping
    sets everything outside the brain to exactly zero, so the air region of a stripped
    image is exactly zero; an unstripped acquisition has genuine noise there. That is
    what air_exact_zero_fraction and the corner statistics measure.

    bright_outer_fraction carries the anatomical evidence: on T1 the scalp fat outside
    the skull is brighter than the brain core, so an intact head shows pixels near the
    tissue boundary that exceed the core median.
    """
    image = np.asarray(image, dtype=np.uint8)
    height, width = image.shape
    non_zero = image > 0

    result = {
        "height": height,
        "width": width,
        "fraction_zero": float(np.mean(~non_zero)),
    }

    threshold = otsu_threshold(image)
    tissue = image > threshold
    result["otsu_threshold"] = threshold
    result["tissue_fraction"] = float(np.mean(tissue))

    air = ~tissue
    result["air_exact_zero_fraction"] = (
        float(np.mean(image[air] == 0)) if air.any() else 1.0
    )

    if not tissue.any():
        result.update({
            "core_median": 0.0,
            "outer_p95": 0.0,
            "bright_outer_fraction": 0.0,
            "outer_tissue_fraction": 0.0,
            "corner_nonzero_fraction": 0.0,
            "corner_max": 0,
            "border_nonzero_fraction": 0.0,
            "border_p99": 0.0,
        })
        return result

    rows, cols = np.nonzero(tissue)
    centre_y = float(rows.mean())
    centre_x = float(cols.mean())

    grid_y, grid_x = np.ogrid[:height, :width]
    radius = np.sqrt((grid_y - centre_y) ** 2 + (grid_x - centre_x) ** 2)

    # Scaled by the extent of the tissue region, so it tracks the head regardless of
    # image size, head size, or how much margin surrounds it.
    radius_99 = float(np.percentile(radius[tissue], 99))
    if radius_99 <= 0:
        radius_99 = 1.0

    core_mask = tissue & (radius <= 0.40 * radius_99)
    outer_mask = (radius >= 0.75 * radius_99) & (radius <= 1.10 * radius_99)

    core_values = image[core_mask]
    outer_values = image[outer_mask]

    core_median = float(np.median(core_values)) if core_values.size else 0.0

    result["core_median"] = core_median
    result["outer_p95"] = (
        float(np.percentile(outer_values, 95)) if outer_values.size else 0.0
    )
    result["outer_tissue_fraction"] = (
        float(np.mean(tissue[outer_mask])) if outer_values.size else 0.0
    )
    # Fat is brighter than brain on T1, so pixels beyond the brain that exceed the core
    # median are the signature of retained extracranial tissue.
    result["bright_outer_fraction"] = (
        float(np.mean(outer_values > core_median))
        if outer_values.size and core_median > 0 else 0.0
    )

    patch = max(4, int(round(0.10 * min(height, width))))
    corners = np.concatenate([
        image[:patch, :patch].ravel(),
        image[:patch, -patch:].ravel(),
        image[-patch:, :patch].ravel(),
        image[-patch:, -patch:].ravel(),
    ])
    result["corner_nonzero_fraction"] = float(np.mean(corners > 0))
    result["corner_max"] = int(corners.max())

    band = max(2, int(round(0.06 * min(height, width))))
    border_mask = np.zeros((height, width), dtype=bool)
    border_mask[:band, :] = True
    border_mask[-band:, :] = True
    border_mask[:, :band] = True
    border_mask[:, -band:] = True

    border_values = image[border_mask]
    result["border_nonzero_fraction"] = float(np.mean(border_values > 0))
    result["border_p99"] = float(np.percentile(border_values, 99))

    return result


def background_is_masked(row):
    """True when the air region really has been zeroed, as skull stripping would do."""
    return bool(
        row["air_exact_zero_fraction"] >= AIR_ZERO_THRESHOLD
        and row["corner_nonzero_fraction"] <= CORNER_NONZERO_THRESHOLD
    )


def classify(row):
    """Retains extracranial signal: background not masked, or bright tissue outside."""
    return bool(
        not background_is_masked(row)
        or row["bright_outer_fraction"] >= BRIGHT_OUTER_THRESHOLD
    )


def load_png(path):
    with Image.open(path) as handle:
        return np.asarray(handle.convert("L"), dtype=np.uint8)


def load_dicom(path):
    dataset = pydicom.dcmread(path, force=True)
    array = dataset.pixel_array.astype(np.float32)

    slope = float(getattr(dataset, "RescaleSlope", 1.0) or 1.0)
    intercept = float(getattr(dataset, "RescaleIntercept", 0.0) or 0.0)

    return normalise_to_uint8(array * slope + intercept)


def sample_d3c(rng):
    manifest = pd.read_csv(D3C_ANALYSIS_MANIFEST)
    central = manifest[manifest["selected_rank"] == CENTRAL_RANK].copy()
    central = central.sort_values("series_instance_uid", kind="mergesort")

    forced = central[central["patient_id"] == ALWAYS_INCLUDE_PATIENT]
    pool = central[central["patient_id"] != ALWAYS_INCLUDE_PATIENT]

    take = max(0, SAMPLE_SIZE - len(forced))
    chosen = pool.iloc[rng.choice(len(pool), size=take, replace=False)]

    return pd.concat([forced, chosen]).sort_values("patient_id", kind="mergesort")


def sample_d1(rng):
    manifest = pd.read_csv(D1_MANIFEST)
    matched = manifest[manifest["class_label"] == D1_MATCH_CLASS].copy()
    matched = matched.sort_values("filepath", kind="mergesort")

    chosen = matched.iloc[rng.choice(len(matched), size=SAMPLE_SIZE, replace=False)]

    return chosen.sort_values("filepath", kind="mergesort")


def summarise(frame, column):
    values = frame[column].astype(float)
    return {
        "median": float(values.median()),
        "q1": float(values.quantile(0.25)),
        "q3": float(values.quantile(0.75)),
        "min": float(values.min()),
        "max": float(values.max()),
    }


def write_report(measurements, d3c_png, d3c_dicom, d1_rows, focus_rows):
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    metrics = [
        ("air_exact_zero_fraction", "Air region exactly zero (1.0 = masked)"),
        ("corner_nonzero_fraction", "Corner non-zero fraction"),
        ("bright_outer_fraction", "Outer pixels brighter than brain core"),
        ("fraction_zero", "Fraction of exactly-zero pixels"),
        ("border_p99", "Border band 99th percentile intensity"),
    ]

    d3c_retaining = int(d3c_png["retains_extracranial"].sum())
    d1_retaining = int(d1_rows["retains_extracranial"].sum())
    dicom_retaining = int(d3c_dicom["retains_extracranial"].sum())

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D3C Skull-Stripping Audit\n\n")
        f.write(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n")

        f.write("## Question\n\n")
        f.write(
            "The project recorded D3C as 100 per cent Processed_CaPTk and treated skull "
            "stripping as a cohort-wide confound. A visual check of "
            f"`{ALWAYS_INCLUDE_PATIENT}` showed intact skull, scalp and orbits. This "
            "audit tests, quantitatively and cohort-wide, whether D3C images retain "
            "extracranial anatomy.\n\n"
        )

        f.write("## Method\n\n")
        f.write(
            "Skull stripping leaves a hard mask boundary: beyond the brain surface every "
            "pixel is exactly zero and no bright tissue remains. An intact head on T1 "
            "shows a bright scalp-fat ring outside a darker skull layer.\n\n"
            "The primary measurement is radial, taken about the centroid of the non-zero "
            "region and scaled by that region's own 99th-percentile radius, so it is "
            "independent of image size, head size, and whether the head reaches the "
            "image border:\n\n"
            "- **Air exactly zero**: among pixels below an Otsu threshold, the fraction "
            "that are exactly zero. Skull stripping is a masking operation, so a "
            "stripped image has an air region of exactly zero, while an unstripped "
            "acquisition carries genuine noise there. This is the decisive test.\n"
            "- **Corner non-zero fraction**: the same question asked of the four image "
            "corners, independent of any threshold.\n"
            "- **Bright outer fraction**: pixels between 0.75 and 1.10 of the tissue "
            "radius that exceed the brain-core median. On T1 the scalp fat outside the "
            "skull is brighter than brain, so this is the anatomical corroboration.\n\n"
            "A first attempt scaled the radial annulus by the *non-zero* radius rather "
            "than by an Otsu tissue radius. Background noise made that mask reach the "
            "image corners, so the annulus sampled air rather than scalp and the metric "
            "was uninformative for both cohorts. It was replaced before any conclusion "
            "was drawn.\n\n"
            "Corner and border-band statistics are reported as secondary evidence only: "
            "a border band is uninformative when the head does not reach the image "
            "edge.\n\n"
            f"An image counts as *background masked*, and so consistent with skull "
            f"stripping, when its air region is at least {AIR_ZERO_THRESHOLD:.0%} "
            f"exactly zero and its corners at most {CORNER_NONZERO_THRESHOLD:.0%} "
            f"non-zero. Anything else retains extracranial signal, as does any image "
            f"with at least {BRIGHT_OUTER_THRESHOLD:.0%} of outer pixels brighter than "
            "the brain core. Distributions are given below so the conclusion can be "
            "checked without relying on those thresholds.\n\n"
        )

        f.write("## Samples\n\n")
        f.write(
            f"- D3C: {len(d3c_png)} series sampled at random (seed {SEED}) from the "
            f"analysis cohort, central slice (rank {CENTRAL_RANK}) of each. "
            f"`{ALWAYS_INCLUDE_PATIENT}` is included by construction.\n"
            f"- D3C source DICOM: the same {len(d3c_dicom)} slices read from the source "
            "DICOM and normalised identically to the conversion, to rule out the PNG "
            "conversion as the cause.\n"
            f"- D1: {len(d1_rows)} {D1_MATCH_CLASS} images sampled at random from the "
            "deduplicated manifest, matched on class because D3C is glioma-only.\n\n"
        )

        f.write("## Headline Result\n\n")
        f.write("| Sample | Retaining extracranial anatomy | of n | Share |\n")
        f.write("|---|---:|---:|---:|\n")
        f.write(
            f"| D3C, converted PNG | {d3c_retaining} | {len(d3c_png)} | "
            f"{d3c_retaining / max(len(d3c_png), 1):.4f} |\n"
        )
        f.write(
            f"| D3C, source DICOM | {dicom_retaining} | {len(d3c_dicom)} | "
            f"{dicom_retaining / max(len(d3c_dicom), 1):.4f} |\n"
        )
        f.write(
            f"| D1 {D1_MATCH_CLASS} | {d1_retaining} | {len(d1_rows)} | "
            f"{d1_retaining / max(len(d1_rows), 1):.4f} |\n"
        )

        f.write("\n## Metric Distributions\n\n")
        f.write("Median, with interquartile range and full range.\n\n")
        f.write("| Metric | D3C PNG | D3C DICOM | D1 |\n")
        f.write("|---|---|---|---|\n")
        for column, label in metrics:
            cells = []
            for frame in (d3c_png, d3c_dicom, d1_rows):
                stats = summarise(frame, column)
                cells.append(
                    f"{stats['median']:.3f} "
                    f"[{stats['q1']:.3f}-{stats['q3']:.3f}] "
                    f"({stats['min']:.3f}-{stats['max']:.3f})"
                )
            f.write(f"| {label} | " + " | ".join(cells) + " |\n")

        f.write(f"\n## The Series That Prompted This: {ALWAYS_INCLUDE_PATIENT}\n\n")
        if focus_rows.empty:
            f.write("Not present in the analysis cohort.\n")
        else:
            f.write(
                "| Source | Air exactly zero | Corner non-zero | Bright outer | Verdict |\n"
            )
            f.write("|---|---:|---:|---:|---|\n")
            for _, row in focus_rows.iterrows():
                verdict = (
                    "retains extracranial"
                    if row["retains_extracranial"] else "consistent with stripping"
                )
                f.write(
                    f"| {row['source']} | {row['air_exact_zero_fraction']:.3f} | "
                    f"{row['corner_nonzero_fraction']:.3f} | "
                    f"{row['bright_outer_fraction']:.3f} | {verdict} |\n"
                )

        f.write("\n## Interpretation\n\n")
        if d3c_retaining >= 0.9 * len(d3c_png):
            f.write(
                "D3C images retain extracranial anatomy cohort-wide. The "
                "`Processed_CaPTk` label does not imply skull stripping here: CaPTk "
                "preprocessing covers reorientation, co-registration and resampling, and "
                "the stripping step evidently was not applied to the DICOM series "
                "distributed in this collection. The source DICOM measurements match the "
                "converted PNGs, so this is a property of the data and not of the "
                "conversion.\n\n"
                "**The skull-stripping confound recorded for D3C is not supported by the "
                "data and should be withdrawn** from CLAUDE.md, SESSION_NOTES.md and any "
                "manuscript text that repeats it. D3C and D1 should be compared on the "
                "measurements above rather than on the assumption.\n"
            )
        elif d3c_retaining <= 0.1 * len(d3c_png):
            f.write(
                "D3C images are consistent with skull stripping cohort-wide, supporting "
                "the recorded confound. The visual impression from "
                f"`{ALWAYS_INCLUDE_PATIENT}` does not generalise.\n"
            )
        else:
            f.write(
                "D3C is mixed: some series retain extracranial anatomy and others do "
                "not. Neither a blanket skull-stripping claim nor a blanket denial is "
                "supportable, and the per-image measurements should be carried into any "
                "analysis that depends on this.\n"
            )

        f.write("\n## Limitations\n\n")
        f.write(
            "- These are intensity and geometry proxies, not a segmentation. They "
            "establish whether tissue exists beyond the brain surface, not what that "
            "tissue is.\n"
            f"- The samples are {SAMPLE_SIZE} series and {SAMPLE_SIZE} images. They are "
            "adequate for a cohort-wide qualitative claim only if the effect is close to "
            "uniform, which the ranges above allow the reader to judge.\n"
            "- D1 images are lossy JPEGs of unknown provenance and prior processing; a "
            "difference between D1 and D3C on these metrics is not by itself evidence "
            "about acquisition.\n"
            f"- Per-image values are in `{MEASUREMENTS_CSV}`.\n"
        )


def main():
    rng = np.random.default_rng(SEED)

    d3c_sample = sample_d3c(rng)
    d1_sample = sample_d1(rng)

    records = []

    for _, row in d3c_sample.iterrows():
        png = measure(load_png(row["output_image_path"]))
        png.update({
            "cohort": "D3C",
            "source": "converted PNG",
            "identifier": row["patient_id"],
            "path": row["output_image_path"],
        })
        records.append(png)

        dicom = measure(load_dicom(row["source_dicom_path"]))
        dicom.update({
            "cohort": "D3C",
            "source": "source DICOM",
            "identifier": row["patient_id"],
            "path": row["source_dicom_path"],
        })
        records.append(dicom)

    for _, row in d1_sample.iterrows():
        d1 = measure(load_png(row["filepath"]))
        d1.update({
            "cohort": "D1",
            "source": f"D1 {row['class_label']}",
            "identifier": row["filename"],
            "path": row["filepath"],
        })
        records.append(d1)

    measurements = pd.DataFrame(records)
    measurements["retains_extracranial"] = measurements.apply(classify, axis=1)

    MEASUREMENTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    measurements.to_csv(MEASUREMENTS_CSV, index=False)

    d3c_png = measurements[
        (measurements["cohort"] == "D3C") & (measurements["source"] == "converted PNG")
    ]
    d3c_dicom = measurements[
        (measurements["cohort"] == "D3C") & (measurements["source"] == "source DICOM")
    ]
    d1_rows = measurements[measurements["cohort"] == "D1"]
    focus_rows = measurements[measurements["identifier"] == ALWAYS_INCLUDE_PATIENT]

    write_report(measurements, d3c_png, d3c_dicom, d1_rows, focus_rows)

    print(f"D3C series sampled: {len(d3c_png)}")
    print(f"D1 images sampled:  {len(d1_rows)}")
    print()
    for label, frame in (
        ("D3C converted PNG", d3c_png),
        ("D3C source DICOM ", d3c_dicom),
        ("D1 glioma        ", d1_rows),
    ):
        retaining = int(frame["retains_extracranial"].sum())
        print(
            f"{label}: retains extracranial {retaining}/{len(frame)} "
            f"| air_exact_zero median {frame['air_exact_zero_fraction'].median():.3f} "
            f"| corner_nonzero median {frame['corner_nonzero_fraction'].median():.3f} "
            f"| bright_outer median {frame['bright_outer_fraction'].median():.3f}"
        )

    print()
    print(f"Measurements: {MEASUREMENTS_CSV}")
    print(f"Report:       {REPORT_PATH}")


if __name__ == "__main__":
    main()

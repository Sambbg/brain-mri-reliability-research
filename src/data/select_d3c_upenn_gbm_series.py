from pathlib import Path
import hashlib
import json, socket, time, threading, datetime
import re
import pandas as pd
from tcia_utils import nbia

TCIA_TIMEOUT_SECONDS = 30
TCIA_MAX_RETRIES = 20
TCIA_RETRY_SLEEP = 20
socket.setdefaulttimeout(TCIA_TIMEOUT_SECONDS)

COLLECTION = "UPENN-GBM"
OUT_DIR = Path("reports/datasets/d3c_upenn_gbm_series_selection")
OUT_DIR.mkdir(parents=True, exist_ok=True)
SELECTED_CSV = OUT_DIR / "selected_series_one_per_patient.csv"
REPORT_PATH = Path("reports/datasets/D3C_series_selection_report.md")

POSTCONTRAST_TERMS = ["post", "+c", " gd", "gad", "stealth post"]
T1_TERMS = ["t1", "mprage", "mp rage", "spgr", "3dt1", "3d t1", "rage", "fl2d"]
T2_FLAIR_PD_TERMS = ["t2", "flair", " pd", "frfse"]
DWI_TERMS = ["dwi", "adc", "dti", "mddw", "diffusion", "trace"]
PERF_TERMS = ["perf", "perfusion", "bolus", "dsc", "dce"]
LOCALIZER_TERMS = ["localizer", "locator", "scout", "3 plane", "3-plane", "screen save"]

ELIGIBLE_CATEGORIES = ["preferred_t1_postcontrast", "secondary_t1"]

# Fixed leading column order for the output manifest. The TCIA response is a list of
# dicts whose key order is not guaranteed, so without this the CSV column order -- and
# therefore its sha256 -- could differ between runs that selected identical series.
LEADING_COLUMNS = [
    "PatientID",
    "SeriesInstanceUID",
    "StudyInstanceUID",
    "selection_category",
    "selection_priority",
    "ImageCount_numeric",
]


def ts():
    return datetime.datetime.now().strftime("%H:%M:%S")


def heartbeat(stop_event, label):
    secs = 0
    while not stop_event.wait(5):
        secs += 5
        print("    [" + ts() + "] still waiting on " + label + " (" + str(secs) + "s)...", flush=True)


def safe_call(name, func, **kwargs):
    print("[" + ts() + "] === " + name + " ===", flush=True)
    result = None
    last_exc = None
    for attempt in range(1, TCIA_MAX_RETRIES + 1):
        print("[" + ts() + "] " + name + " attempt " + str(attempt) + "/" + str(TCIA_MAX_RETRIES), flush=True)
        stop_event = threading.Event()
        hb = threading.Thread(target=heartbeat, args=(stop_event, name), daemon=True)
        hb.start()
        try:
            result = func(**kwargs)
        except Exception as exc:
            last_exc = exc
            result = None
        finally:
            stop_event.set()
            hb.join()
        if result is not None:
            print("[" + ts() + "] " + name + " OK", flush=True)
            break
        print("[" + ts() + "] " + name + " attempt " + str(attempt) + " failed: " + repr(last_exc), flush=True)
        if attempt < TCIA_MAX_RETRIES:
            time.sleep(TCIA_RETRY_SLEEP)
    if result is None:
        raise RuntimeError(name + " gave up. Last error: " + repr(last_exc))
    return result


def normalize_text(value):
    if pd.isna(value):
        return ""
    text = str(value).lower().replace("_", " ").replace("-", " ")
    return re.sub(r"\s+", " ", text).strip()


def contains_any(text, terms):
    return any(term in text for term in terms)


def classify_series(row):
    desc = normalize_text(row.get("SeriesDescription", ""))
    proto = normalize_text(row.get("ProtocolName", ""))
    combined = (desc + " " + proto).strip()
    has_t1 = contains_any(combined, T1_TERMS)
    if contains_any(combined, LOCALIZER_TERMS):
        return "excluded_localizer"
    if contains_any(combined, DWI_TERMS):
        return "excluded_dwi_adc"
    if contains_any(combined, PERF_TERMS):
        return "excluded_perfusion"
    if contains_any(combined, T2_FLAIR_PD_TERMS) and not has_t1:
        return "excluded_t2_flair"
    if has_t1:
        if contains_any(combined, POSTCONTRAST_TERMS):
            return "preferred_t1_postcontrast"
        return "secondary_t1"
    return "excluded_other"


def category_priority(category):
    return {"preferred_t1_postcontrast": 1, "secondary_t1": 2}.get(category, 99)


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def order_columns(df):
    leading = [c for c in LEADING_COLUMNS if c in df.columns]
    remaining = sorted(c for c in df.columns if c not in leading)
    return df[leading + remaining]


def select_one_series_per_patient(df):
    """Choose exactly one series per patient under an explicit total order.

    This manifest is the single source of truth for the D3C cohort, so the result must
    not depend on the order TCIA happened to return rows in:

      - The sort keys end in SeriesInstanceUID, which is unique per series and asserted
        to be so below, making the ordering a total order rather than a partial one.
      - kind="mergesort" is a stable sort, so equal keys can never permute.
      - The winning row per patient is taken with drop_duplicates(keep="first"), which
        returns whole rows. groupby().first() must not be used: it takes the first
        non-null value of each column independently, so a null in the winning row is
        silently backfilled from a different series and the output row can correspond
        to no real series at all.
    """
    eligible = df[df["selection_category"].isin(ELIGIBLE_CATEGORIES)].copy()
    if eligible.empty:
        return eligible

    duplicate_uids = int(eligible["SeriesInstanceUID"].duplicated().sum())
    if duplicate_uids:
        raise ValueError(
            str(duplicate_uids) + " eligible rows share a SeriesInstanceUID, so the "
            "sort keys do not form a total order and the selection could depend on API "
            "row order. Resolve the duplicates before selecting."
        )

    eligible["selection_priority"] = eligible["selection_category"].apply(category_priority)

    if "ImageCount" in eligible.columns:
        eligible["ImageCount_numeric"] = pd.to_numeric(eligible["ImageCount"], errors="coerce").fillna(0)
    else:
        eligible["ImageCount_numeric"] = 0

    eligible = eligible.sort_values(
        ["PatientID", "selection_priority", "ImageCount_numeric", "SeriesInstanceUID"],
        ascending=[True, True, False, True],
        kind="mergesort",
    )

    selected = eligible.drop_duplicates(subset="PatientID", keep="first")

    # PatientID is unique after the deduplication, so this is itself a total order.
    selected = selected.sort_values("PatientID", kind="mergesort").reset_index(drop=True)

    return order_columns(selected)


def write_report(df, selected, manifest_sha256):
    all_category_counts = df["selection_category"].value_counts().sort_index()
    selected_category_counts = selected["selection_category"].value_counts().sort_index()

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D3C Series Selection - UPENN-GBM (human)\n\n")
        f.write("Selected one T1 series per patient (post-contrast preferred).\n\n")

        f.write("## Output Manifest\n\n")
        f.write("- Manifest: `" + str(SELECTED_CSV) + "`\n")
        f.write("- sha256: `" + manifest_sha256 + "`\n")
        f.write("- Selected series: " + str(len(selected)) + "\n")
        f.write("- Patients covered: " + str(selected["PatientID"].nunique()) + "\n")
        f.write("- Series returned by TCIA: " + str(len(df)) + "\n\n")

        f.write(
            "This manifest is the single source of truth for the D3C cohort. The "
            "download, inspection and conversion steps read it and refuse to process any "
            "series it does not list. Quote the sha256 above when reporting D3C results, "
            "so the cohort behind a number is verifiable.\n\n"
        )

        f.write("## Determinism\n\n")
        f.write("The selection does not depend on the order TCIA returns series in:\n\n")
        f.write(
            "- Sort keys `PatientID`, `selection_priority`, `ImageCount_numeric` "
            "(descending), `SeriesInstanceUID` form a total order, because "
            "SeriesInstanceUID is unique per series and is asserted to be so.\n"
        )
        f.write("- `kind=\"mergesort\"` is a stable sort, so equal keys never permute.\n")
        f.write(
            "- One row per patient is taken with `drop_duplicates(keep=\"first\")`, which "
            "returns whole rows. `groupby().first()` is not used: it takes the first "
            "non-null value of each column independently and can compose an output row "
            "from several different series.\n"
        )
        f.write(
            "- Manifest columns are written in a fixed order, so the sha256 depends only "
            "on the selected content and not on the key order of the API response.\n\n"
        )

        f.write("## Selection Category Counts, All Series\n\n")
        f.write("| Category | Count |\n")
        f.write("|---|---:|\n")
        for category, count in all_category_counts.items():
            f.write("| " + str(category) + " | " + str(count) + " |\n")

        f.write("\n## Selected Category Counts\n\n")
        f.write("| Category | Count |\n")
        f.write("|---|---:|\n")
        for category, count in selected_category_counts.items():
            f.write("| " + str(category) + " | " + str(count) + " |\n")

        f.write("\n## Limitation\n\n")
        f.write(
            "D3C contains glioma cases only. It must not be used to claim full four-class "
            "external validation.\n"
        )


def main():
    series = safe_call("getSeries", nbia.getSeries, collection=COLLECTION)
    df = pd.DataFrame(series)
    if df.empty:
        raise RuntimeError("No series returned.")
    df["selection_category"] = df.apply(classify_series, axis=1)
    selected = select_one_series_per_patient(df)
    if selected.empty:
        raise RuntimeError("No eligible series found.")
    selected.to_csv(SELECTED_CSV, index=False)
    manifest_sha256 = sha256_file(SELECTED_CSV)
    write_report(df, selected, manifest_sha256)
    print("", flush=True)
    print("Selection category counts:", flush=True)
    print(df["selection_category"].value_counts().sort_index().to_string(), flush=True)
    print("", flush=True)
    print("Selected series (one per patient): " + str(len(selected)), flush=True)
    if not selected.empty:
        print("Patients covered: " + str(selected["PatientID"].nunique()), flush=True)
        print("Selected breakdown:", flush=True)
        print(selected["selection_category"].value_counts().to_string(), flush=True)
    print("Selected CSV: " + str(SELECTED_CSV), flush=True)
    print("Manifest sha256: " + manifest_sha256, flush=True)
    print("Report: " + str(REPORT_PATH), flush=True)


if __name__ == "__main__":
    main()

from pathlib import Path
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


def select_one_series_per_patient(df):
    eligible = df[df["selection_category"].isin(["preferred_t1_postcontrast", "secondary_t1"])].copy()
    if eligible.empty:
        return eligible
    eligible["selection_priority"] = eligible["selection_category"].apply(category_priority)
    if "ImageCount" in eligible.columns:
        eligible["ImageCount_numeric"] = pd.to_numeric(eligible["ImageCount"], errors="coerce").fillna(0)
    else:
        eligible["ImageCount_numeric"] = 0
    eligible = eligible.sort_values(["PatientID", "selection_priority", "ImageCount_numeric", "SeriesInstanceUID"], ascending=[True, True, False, True])
    return eligible.groupby("PatientID", as_index=False).first()


def main():
    series = safe_call("getSeries", nbia.getSeries, collection=COLLECTION)
    df = pd.DataFrame(series)
    if df.empty:
        raise RuntimeError("No series returned.")
    df["selection_category"] = df.apply(classify_series, axis=1)
    selected = select_one_series_per_patient(df)
    selected.to_csv(SELECTED_CSV, index=False)
    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("# D3C Series Selection - UPENN-GBM (human)\n\n")
        f.write("Selected one T1 series per patient (post-contrast preferred).\n")
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


if __name__ == "__main__":
    main()

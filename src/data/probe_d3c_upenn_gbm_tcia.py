from pathlib import Path
import json, socket, time, threading, datetime
import pandas as pd
from tcia_utils import nbia

TCIA_TIMEOUT_SECONDS = 30
TCIA_MAX_RETRIES = 20
TCIA_RETRY_SLEEP = 20
socket.setdefaulttimeout(TCIA_TIMEOUT_SECONDS)

COLLECTION = "UPENN-GBM"
OUT_DIR = Path("reports/datasets/d3c_upenn_gbm_probe")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def ts():
    return datetime.datetime.now().strftime("%H:%M:%S")


def save_json(obj, path):
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def heartbeat(stop_event, label):
    secs = 0
    while not stop_event.wait(5):
        secs += 5
        print("    [" + ts() + "] still waiting on " + label + " (" + str(secs) + "s, timeout at " + str(TCIA_TIMEOUT_SECONDS) + "s)...", flush=True)


def safe_call(name, func, **kwargs):
    print("[" + ts() + "] === " + name + " === (timeout " + str(TCIA_TIMEOUT_SECONDS) + "s, up to " + str(TCIA_MAX_RETRIES) + " tries)", flush=True)
    result = None
    last_exc = None
    for attempt in range(1, TCIA_MAX_RETRIES + 1):
        print("[" + ts() + "] " + name + " attempt " + str(attempt) + "/" + str(TCIA_MAX_RETRIES) + " starting...", flush=True)
        stop_event = threading.Event()
        hb = threading.Thread(target=heartbeat, args=(stop_event, name), daemon=True)
        hb.start()
        t0 = time.time()
        try:
            result = func(**kwargs)
        except Exception as exc:
            last_exc = exc
            result = None
        finally:
            stop_event.set()
            hb.join()
        dt = round(time.time() - t0, 1)
        if result is not None:
            print("[" + ts() + "] " + name + " OK in " + str(dt) + "s", flush=True)
            break
        print("[" + ts() + "] " + name + " attempt " + str(attempt) + " failed after " + str(dt) + "s: " + repr(last_exc), flush=True)
        if attempt < TCIA_MAX_RETRIES:
            for remaining in range(TCIA_RETRY_SLEEP, 0, -5):
                print("    [" + ts() + "] retrying in " + str(remaining) + "s...", flush=True)
                time.sleep(min(5, remaining))
    if result is None:
        print("[" + ts() + "] " + name + " GAVE UP after " + str(TCIA_MAX_RETRIES) + " tries. Last error: " + repr(last_exc), flush=True)
        return None
    if isinstance(result, list):
        print("[" + ts() + "] " + name + " returned " + str(len(result)) + " rows.", flush=True)
    return result


def to_dataframe(result):
    if result is None:
        return pd.DataFrame()
    if isinstance(result, list):
        return pd.DataFrame(result)
    try:
        return pd.DataFrame(result)
    except Exception:
        return pd.DataFrame()


def save_table(name, result):
    df = to_dataframe(result)
    if df.empty:
        print("No rows to save for " + name, flush=True)
        return df
    df.to_csv(OUT_DIR / (name + ".csv"), index=False)
    save_json(result, OUT_DIR / (name + ".json"))
    print(name + " rows: " + str(len(df)), flush=True)
    return df


def main():
    print("[" + ts() + "] Probing collection: " + COLLECTION, flush=True)
    patients_df = save_table("patients", safe_call("getPatient", nbia.getPatient, collection=COLLECTION))
    studies_df = save_table("studies", safe_call("getStudy", nbia.getStudy, collection=COLLECTION))
    series_df = save_table("series", safe_call("getSeries", nbia.getSeries, collection=COLLECTION))
    print("", flush=True)
    print("Summary: patients=" + str(len(patients_df)) + " studies=" + str(len(studies_df)) + " series=" + str(len(series_df)), flush=True)
    if not series_df.empty:
        if "Modality" in series_df.columns:
            print("Modality counts:", flush=True)
            print(series_df["Modality"].value_counts().to_string(), flush=True)
        if "SeriesDescription" in series_df.columns:
            print("Top SeriesDescription counts:", flush=True)
            print(series_df["SeriesDescription"].value_counts().head(50).to_string(), flush=True)
    print("Probe outputs saved to: " + str(OUT_DIR), flush=True)


if __name__ == "__main__":
    main()

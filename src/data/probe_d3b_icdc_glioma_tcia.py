from pathlib import Path
import json
import pandas as pd

from tcia_utils import nbia

COLLECTION = "ICDC-Glioma"
OUT_DIR = Path("reports/datasets/d3b_icdc_glioma_probe")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def save_json(obj, path: Path):
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def safe_call(name, func, **kwargs):
    print(f"\nCalling {name} with parameters: {kwargs}")

    try:
        result = func(**kwargs)
    except Exception as exc:
        print(f"{name} failed: {repr(exc)}")
        return None

    if result is None:
        print(f"{name} returned None.")
        return None

    if isinstance(result, list):
        print(f"{name} returned list with {len(result)} rows.")
        return result

    if isinstance(result, dict):
        print(f"{name} returned dict with keys: {list(result.keys())}")
        return result

    print(f"{name} returned object of type: {type(result)}")
    return result


def to_dataframe(result):
    if result is None:
        return pd.DataFrame()

    if isinstance(result, pd.DataFrame):
        return result

    if isinstance(result, list):
        return pd.DataFrame(result)

    if isinstance(result, dict):
        for _, value in result.items():
            if isinstance(value, list):
                return pd.DataFrame(value)
        return pd.DataFrame([result])

    try:
        return pd.DataFrame(result)
    except Exception:
        return pd.DataFrame()


def save_table(name, result):
    df = to_dataframe(result)

    if df.empty:
        print(f"No rows to save for {name}.")
        return df

    csv_path = OUT_DIR / f"{name}.csv"
    json_path = OUT_DIR / f"{name}.json"

    df.to_csv(csv_path, index=False)
    save_json(result, json_path)

    print(f"{name} rows: {len(df)}")
    print(f"{name} columns: {list(df.columns)}")
    print(f"Saved: {csv_path}")

    return df


def main():
    print(f"Probing TCIA/NBIA collection: {COLLECTION}")

    patients = safe_call("getPatient", nbia.getPatient, collection=COLLECTION)
    patients_df = save_table("patients", patients)

    studies = safe_call("getStudy", nbia.getStudy, collection=COLLECTION)
    studies_df = save_table("studies", studies)

    series = safe_call("getSeries", nbia.getSeries, collection=COLLECTION)
    series_df = save_table("series", series)

    print("\nSummary")
    print(f"Patients: {len(patients_df)}")
    print(f"Studies: {len(studies_df)}")
    print(f"Series: {len(series_df)}")

    if not series_df.empty:
        useful_cols = [
            col for col in [
                "PatientID",
                "StudyInstanceUID",
                "SeriesInstanceUID",
                "Modality",
                "SeriesDescription",
                "BodyPartExamined",
                "Manufacturer",
                "ManufacturerModelName",
            ]
            if col in series_df.columns
        ]

        if useful_cols:
            print("\nSeries preview:")
            print(series_df[useful_cols].head(30).to_string(index=False))

        if "Modality" in series_df.columns:
            print("\nModality counts:")
            print(series_df["Modality"].value_counts().to_string())

        if "SeriesDescription" in series_df.columns:
            print("\nTop SeriesDescription counts:")
            print(series_df["SeriesDescription"].value_counts().head(50).to_string())

    print(f"\nProbe outputs saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()

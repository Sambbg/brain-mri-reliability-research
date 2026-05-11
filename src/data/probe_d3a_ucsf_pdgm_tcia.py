from pathlib import Path
import json
import pandas as pd

from tcia_utils import nbia

OUT_DIR = Path("reports/datasets/d3a_tcia_probe")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SEARCH_TERMS = ["UCSF", "PDGM", "GLIOMA", "BRAIN"]

CANDIDATE_COLLECTION_NAMES = [
    "UCSF-PDGM",
    "UCSF PDGM",
    "UCSF-PDGM-v3",
    "UCSF-PDGM-V3",
    "UCSF-PDGM-v4",
    "UCSF-PDGM-V4",
]


def save_json(obj, path: Path):
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def safe_call(name, func, **kwargs):
    """
    Calls a tcia_utils function safely.

    Different tcia_utils versions sometimes return:
    - list
    - dict
    - None
    - pandas-like structures

    This wrapper prevents the script from crashing when TCIA returns no result.
    """
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
    """
    Converts common tcia_utils return types into a DataFrame.
    """
    if result is None:
        return pd.DataFrame()

    if isinstance(result, pd.DataFrame):
        return result

    if isinstance(result, list):
        return pd.DataFrame(result)

    if isinstance(result, dict):
        # Some API responses wrap rows inside a dict.
        for _, value in result.items():
            if isinstance(value, list):
                return pd.DataFrame(value)

        return pd.DataFrame([result])

    try:
        return pd.DataFrame(result)
    except Exception:
        return pd.DataFrame()


def sanitize_filename(text: str) -> str:
    return (
        text.replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
        .replace("*", "_")
        .replace("?", "_")
        .replace('"', "_")
        .replace("<", "_")
        .replace(">", "_")
        .replace("|", "_")
    )


def get_collections():
    """
    Uses nbia.getCollections because this installed tcia_utils version does not
    expose getCollectionValues.
    """
    collections = safe_call("getCollections", nbia.getCollections)
    collections_df = to_dataframe(collections)

    if collections_df.empty:
        print("\nNo collection table returned. Cannot search collection names from API.")
        return collections, collections_df

    collections_csv = OUT_DIR / "collections.csv"
    collections_json = OUT_DIR / "collections.json"

    collections_df.to_csv(collections_csv, index=False)
    save_json(collections, collections_json)

    print(f"\nCollections saved to: {collections_csv}")
    print("Collection columns:", list(collections_df.columns))

    print("\nSearching collection table for candidate names...")

    text_df = collections_df.astype(str)

    mask = pd.Series(False, index=collections_df.index)

    for term in SEARCH_TERMS:
        term_mask = text_df.apply(
            lambda col: col.str.contains(term, case=False, na=False)
        ).any(axis=1)
        mask = mask | term_mask

    matches = collections_df[mask]

    if matches.empty:
        print("No matching collections found for search terms:", SEARCH_TERMS)
    else:
        matches_path = OUT_DIR / "collection_matches.csv"
        matches.to_csv(matches_path, index=False)

        print(f"Matching collections saved to: {matches_path}")
        print("\nMatching collections preview:")
        print(matches.head(50).to_string(index=False))

    return collections, collections_df


def probe_collection(collection_name: str):
    print("\n" + "=" * 80)
    print(f"Testing collection candidate: {collection_name}")

    safe_name = sanitize_filename(collection_name)

    patients = safe_call("getPatient", nbia.getPatient, collection=collection_name)
    patients_df = to_dataframe(patients)

    if patients_df.empty:
        print(f"No patient rows returned for: {collection_name}")
    else:
        out_csv = OUT_DIR / f"patients_{safe_name}.csv"
        out_json = OUT_DIR / f"patients_{safe_name}.json"

        patients_df.to_csv(out_csv, index=False)
        save_json(patients, out_json)

        print(f"Patients saved to: {out_csv}")
        print(f"Patient rows: {len(patients_df)}")
        print("Patient columns:", list(patients_df.columns))
        print(patients_df.head(10).to_string(index=False))

    series = safe_call("getSeries", nbia.getSeries, collection=collection_name)
    series_df = to_dataframe(series)

    if series_df.empty:
        print(f"No series rows returned for: {collection_name}")
    else:
        out_csv = OUT_DIR / f"series_{safe_name}.csv"
        out_json = OUT_DIR / f"series_{safe_name}.json"

        series_df.to_csv(out_csv, index=False)
        save_json(series, out_json)

        print(f"Series saved to: {out_csv}")
        print(f"Series rows: {len(series_df)}")
        print("Series columns:", list(series_df.columns))

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
            print(series_df[useful_cols].head(20).to_string(index=False))

        if "Modality" in series_df.columns:
            print("\nModality counts:")
            print(series_df["Modality"].value_counts().to_string())

        if "SeriesDescription" in series_df.columns:
            print("\nTop SeriesDescription counts:")
            print(series_df["SeriesDescription"].value_counts().head(30).to_string())


def main():
    print("D3A TCIA/NBIA probe")
    print("Goal: identify the correct collection name/API behaviour before downloading data.")

    get_collections()

    for collection_name in CANDIDATE_COLLECTION_NAMES:
        probe_collection(collection_name)

    print(f"\nProbe outputs saved to: {OUT_DIR}")
    print("\nNext step:")
    print("Inspect collection_matches.csv and any patients/series CSV files that were created.")


if __name__ == "__main__":
    main()

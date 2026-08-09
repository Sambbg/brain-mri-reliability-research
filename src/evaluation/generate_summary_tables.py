from pathlib import Path
import json
import pandas as pd


OUT_DIR = Path("reports/experiments/tables")
OUT_DIR.mkdir(parents=True, exist_ok=True)


MODELS = {
    "E001 ResNet18": {
        "exp_dir": Path("experiments/E001_D1_resnet18_baseline"),
    },
    "E002 EfficientNet-B0": {
        "exp_dir": Path("experiments/E002_D1_efficientnet_b0_baseline"),
    },
    "E003 ViT-B/16": {
        "exp_dir": Path("experiments/E003_D1_vit_b16_baseline"),
    },
}


PROVENANCE_FILENAME = "provenance.json"


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_run_set_provenance() -> dict:
    """Rule 4: read each model's provenance sidecar before any table is generated."""
    provenance = {}

    for model_name, info in MODELS.items():
        path = info["exp_dir"] / PROVENANCE_FILENAME

        if not path.exists():
            raise FileNotFoundError(
                f"Missing {path}.\n"
                "Tables may only be generated from a frozen run set produced by the "
                "current training scripts, which write provenance.json. Retrain with "
                "RUN_ID set, for example:\n"
                "  RUN_ID=2026-08-frozen-a python src/training/train_e001_resnet18.py"
            )

        provenance[model_name] = load_json(path)

    return provenance


def assert_single_run_set(provenance: dict):
    """Rule 4: abort unless all three models come from one frozen run set.

    run_id is the run-set identity and must be identical.

    split_csv_sha256 must also be identical: three models compared in one table have to
    have been trained and tested on the same leakage-aware split, and that can never
    legitimately differ.

    git_commit is deliberately NOT asserted. Experiment artefacts are version-controlled,
    so each model's outputs are committed before the next model trains, which means the
    three models in a single run set legitimately carry different commits.
    """

    def collect(field):
        return {name: prov.get(field) for name, prov in provenance.items()}

    def describe(values):
        return "\n".join(f"  {name}: {value!r}" for name, value in values.items())

    run_ids = collect("run_id")
    if None in run_ids.values() or len(set(run_ids.values())) != 1:
        raise RuntimeError(
            "Models do not share a single run_id, so they are not one frozen run set "
            "and must not appear in the same table:\n" + describe(run_ids)
        )

    split_hashes = collect("split_csv_sha256")
    if None in split_hashes.values() or len(set(split_hashes.values())) != 1:
        raise RuntimeError(
            "Models were not trained against an identical split_csv_sha256. Models "
            "compared in one table must share the same split; this must never differ:\n"
            + describe(split_hashes)
        )

    run_id = next(iter(run_ids.values()))
    split_csv_sha256 = next(iter(split_hashes.values()))

    return run_id, split_csv_sha256


def make_table_1_run_set(provenance: dict) -> None:
    """Record the run set the tables were generated from, including per-model commits."""
    rows = []

    for model_name, prov in provenance.items():
        rows.append({
            "Model": model_name,
            "Run ID": prov.get("run_id"),
            "Seed": prov.get("seed"),
            "Git commit": prov.get("git_commit"),
            "Split sha256": prov.get("split_csv_sha256"),
            "Checkpoint sha256": prov.get("checkpoint_sha256"),
        })

    df = pd.DataFrame(rows)
    save_table(df, "table_1_run_set_provenance")


def round_value(value, digits=4):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return round(float(value), digits)
    return value


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    columns = [str(col) for col in df.columns]

    def cell(value):
        if pd.isna(value):
            return ""
        return str(value)

    lines = []
    lines.append("| " + " | ".join(columns) + " |")
    lines.append("| " + " | ".join(["---"] * len(columns)) + " |")

    for _, row in df.iterrows():
        lines.append("| " + " | ".join(cell(row[col]) for col in df.columns) + " |")

    return "\n".join(lines) + "\n"


def save_table(df: pd.DataFrame, stem: str) -> None:
    csv_path = OUT_DIR / f"{stem}.csv"
    md_path = OUT_DIR / f"{stem}.md"

    df.to_csv(csv_path, index=False)

    with md_path.open("w", encoding="utf-8") as f:
        f.write(dataframe_to_markdown(df))

    print(f"Saved: {csv_path}")
    print(f"Saved: {md_path}")


def get_first_existing(d: dict, keys: list[str]):
    for key in keys:
        if key in d:
            return d[key]
    return None


def get_temperature(metrics: dict):
    return get_first_existing(
        metrics,
        [
            "temperature",
            "learned_temperature",
            "optimal_temperature",
            "temperature_value",
        ],
    )


def get_metric_from_groups(metrics: dict, group_names: list[str], metric_keys: list[str]):
    """
    Robustly read metric values from common JSON schemas.

    Supported forms include:
    - metrics["raw"]["ece_15_bins"]
    - metrics["raw_test_metrics"]["ece_15_bins"]
    - metrics["temperature_scaled"]["ece_15_bins"]
    - metrics["scaled_test_metrics"]["ece_15_bins"]
    - metrics["raw_ece_15_bins"]
    - metrics["scaled_ece_15_bins"]
    - metrics["ece_15_bins"]
    """

    # Nested form
    for group in group_names:
        group_obj = metrics.get(group)
        if isinstance(group_obj, dict):
            for metric_key in metric_keys:
                if metric_key in group_obj:
                    return group_obj[metric_key]

    # Flat prefixed form
    for group in group_names:
        for metric_key in metric_keys:
            candidates = [
                f"{group}_{metric_key}",
                f"{group}_test_{metric_key}",
                f"{group.replace('_metrics', '')}_{metric_key}",
            ]
            for candidate in candidates:
                if candidate in metrics:
                    return metrics[candidate]

    # Direct top-level fallback
    for metric_key in metric_keys:
        if metric_key in metrics:
            return metrics[metric_key]

    return None


def debug_temperature_schema():
    """
    Write a tiny schema report so we know exactly what the temperature JSON files contain.
    This protects against silent blank table values.
    """
    lines = ["# Temperature Scaling JSON Schema Debug\n"]

    for model_name, info in MODELS.items():
        path = info["exp_dir"] / "temperature_scaling_metrics.json"
        metrics = load_json(path)

        lines.append(f"## {model_name}\n")
        lines.append(f"- File: `{path}`")
        lines.append(f"- Top-level keys: `{list(metrics.keys())}`")

        for key, value in metrics.items():
            if isinstance(value, dict):
                lines.append(f"- Nested `{key}` keys: `{list(value.keys())}`")

        lines.append("")

    debug_path = OUT_DIR / "temperature_scaling_schema_debug.md"
    debug_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved: {debug_path}")


def make_table_2_internal_performance():
    rows = []

    for model_name, info in MODELS.items():
        exp_dir = info["exp_dir"]
        final_results = load_json(exp_dir / "final_results.json")

        rows.append({
            "Model": model_name,
            "Test accuracy": round_value(final_results.get("test_accuracy")),
            "Test balanced accuracy": round_value(final_results.get("test_balanced_accuracy")),
            "Test macro-F1": round_value(final_results.get("test_macro_f1")),
            "Best validation macro-F1": round_value(final_results.get("best_val_macro_f1")),
            "Best epoch": final_results.get("best_epoch"),
        })

    df = pd.DataFrame(rows)
    save_table(df, "table_2_internal_performance")


def make_table_3_internal_calibration():
    rows = []

    raw_groups = ["raw", "raw_metrics", "raw_test", "raw_test_metrics", "before", "before_temperature_scaling"]
    scaled_groups = [
        "temperature_scaled",
        "temperature_scaled_metrics",
        "temperature_scaled_test",
        "temperature_scaled_test_metrics",
        "scaled",
        "scaled_metrics",
        "scaled_test",
        "scaled_test_metrics",
        "after",
        "after_temperature_scaling",
    ]

    metric_aliases = {
        "ece": ["ece_15_bins", "ece", "expected_calibration_error"],
        "nll": ["negative_log_likelihood", "nll"],
        "gap": ["confidence_accuracy_gap", "confidence_gap"],
        "brier": ["brier_score", "brier"],
    }

    for model_name, info in MODELS.items():
        exp_dir = info["exp_dir"]

        raw_cal = load_json(exp_dir / "calibration_metrics.json")
        temp = load_json(exp_dir / "temperature_scaling_metrics.json")

        raw_ece = get_metric_from_groups(temp, raw_groups, metric_aliases["ece"])
        raw_nll = get_metric_from_groups(temp, raw_groups, metric_aliases["nll"])
        raw_gap = get_metric_from_groups(temp, raw_groups, metric_aliases["gap"])
        raw_brier = get_metric_from_groups(temp, raw_groups, metric_aliases["brier"])

        scaled_ece = get_metric_from_groups(temp, scaled_groups, metric_aliases["ece"])
        scaled_nll = get_metric_from_groups(temp, scaled_groups, metric_aliases["nll"])
        scaled_gap = get_metric_from_groups(temp, scaled_groups, metric_aliases["gap"])
        scaled_brier = get_metric_from_groups(temp, scaled_groups, metric_aliases["brier"])

        rows.append({
            "Model": model_name,
            "Temperature": round_value(get_temperature(temp)),
            "Raw ECE": round_value(raw_ece if raw_ece is not None else raw_cal.get("ece_15_bins")),
            "Scaled ECE": round_value(scaled_ece),
            "Raw NLL": round_value(raw_nll if raw_nll is not None else raw_cal.get("negative_log_likelihood")),
            "Scaled NLL": round_value(scaled_nll),
            "Raw confidence-accuracy gap": round_value(raw_gap if raw_gap is not None else raw_cal.get("confidence_accuracy_gap")),
            "Scaled confidence-accuracy gap": round_value(scaled_gap),
            "Raw Brier score": round_value(raw_brier if raw_brier is not None else raw_cal.get("brier_score")),
            "Scaled Brier score": round_value(scaled_brier),
        })

    df = pd.DataFrame(rows)

    # Fail loudly if scaled metrics are still missing.
    required_scaled_cols = [
        "Scaled ECE",
        "Scaled NLL",
        "Scaled confidence-accuracy gap",
        "Scaled Brier score",
    ]
    missing = []
    for col in required_scaled_cols:
        if df[col].isna().any():
            missing.append(col)

    if missing:
        raise RuntimeError(
            "Table 3 still has missing scaled values in columns: "
            + ", ".join(missing)
            + ". Check reports/experiments/tables/temperature_scaling_schema_debug.md"
        )

    save_table(df, "table_3_internal_calibration")


def make_table_4_d3b_domain_shift():
    rows = []

    for model_name, info in MODELS.items():
        exp_dir = info["exp_dir"]
        metrics = load_json(exp_dir / "d3b_domain_shift_metrics.json")

        rows.append({
            "Model": model_name,
            "D3B slices": metrics.get("n_slices"),
            "D3B patients": metrics.get("n_patients"),
            "D3B series": metrics.get("n_series"),
            "Slice-level glioma prediction rate": round_value(metrics.get("glioma_prediction_rate")),
            "Patient-majority glioma rate": round_value(metrics.get("patient_majority_glioma_rate")),
            "Series-majority glioma rate": round_value(metrics.get("series_majority_glioma_rate")),
            "Mean glioma probability": round_value(metrics.get("mean_glioma_probability")),
            "Median glioma probability": round_value(metrics.get("median_glioma_probability")),
            "Mean max confidence": round_value(metrics.get("mean_max_confidence")),
            "Mean entropy": round_value(metrics.get("mean_entropy")),
        })

    df = pd.DataFrame(rows)
    save_table(df, "table_4_d3b_domain_shift")


def make_table_5_d3b_temperature_scaled():
    rows = []

    for model_name, info in MODELS.items():
        exp_dir = info["exp_dir"]
        metrics = load_json(exp_dir / "d3b_temperature_scaled_metrics.json")

        raw = metrics.get("raw", {})
        scaled = metrics.get("temperature_scaled", {})

        rows.append({
            "Model": model_name,
            "Temperature": round_value(metrics.get("temperature")),
            "Raw glioma prediction rate": round_value(raw.get("glioma_prediction_rate")),
            "Scaled glioma prediction rate": round_value(scaled.get("glioma_prediction_rate")),
            "Raw mean glioma probability": round_value(raw.get("mean_glioma_probability")),
            "Scaled mean glioma probability": round_value(scaled.get("mean_glioma_probability")),
            "Raw mean max confidence": round_value(raw.get("mean_max_confidence")),
            "Scaled mean max confidence": round_value(scaled.get("mean_max_confidence")),
            "Raw mean entropy": round_value(raw.get("mean_entropy")),
            "Scaled mean entropy": round_value(scaled.get("mean_entropy")),
            "Raw patient-majority glioma rate": round_value(raw.get("patient_majority_glioma_rate")),
            "Scaled patient-majority glioma rate": round_value(scaled.get("patient_majority_glioma_rate")),
            "Raw series-majority glioma rate": round_value(raw.get("series_majority_glioma_rate")),
            "Scaled series-majority glioma rate": round_value(scaled.get("series_majority_glioma_rate")),
        })

    df = pd.DataFrame(rows)
    save_table(df, "table_5_d3b_temperature_scaled")


def main():
    # Rule 4: verify the run set before generating anything, so a mixed-run set can
    # never reach a table.
    provenance = load_run_set_provenance()
    run_id, split_csv_sha256 = assert_single_run_set(provenance)

    print(f"Frozen run set: {run_id}")
    print(f"Split sha256:   {split_csv_sha256}")
    print(f"Models:         {len(provenance)}")

    make_table_1_run_set(provenance)
    debug_temperature_schema()
    make_table_2_internal_performance()
    make_table_3_internal_calibration()
    make_table_4_d3b_domain_shift()
    make_table_5_d3b_temperature_scaled()

    print(f"\nAll summary tables generated successfully from run set {run_id}.")
    print(f"Output directory: {OUT_DIR}")


if __name__ == "__main__":
    main()

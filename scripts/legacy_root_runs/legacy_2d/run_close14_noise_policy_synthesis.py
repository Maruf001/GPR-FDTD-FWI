#!/usr/bin/env python3
"""Synthesize existing close14 noise/acquisition policy evidence."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_coordinate_resolution_policy_synthesis import policy_label_for_counts, row_clean  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_AGGREGATE_GLOBS = (
    "outputs/experiments/*coordinate_confidence_close14*seed_replicates/data/coordinate_confidence_aggregate.csv",
    "outputs/experiments/*coordinate_confidence_close14_seed34_noise15p361328125_sources4_5_7_aggregate/data/coordinate_confidence_aggregate.csv",
)
DEFAULT_BOUNDARY_JSON = (
    "outputs/experiments/418_coordinate_confidence_close14_txrx50_noise_boundary_summary/"
    "data/noise_boundary_summary.json"
)


def safe_float(value, default=math.nan) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return float(default)
    return out if math.isfinite(out) else float(default)


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_output_id(path: Path) -> int | None:
    for part in path.parts:
        match = re.match(r"^(\d+)_", part)
        if match:
            return int(match.group(1))
    return None


def parse_noise_percent(text: str) -> float | None:
    match = re.search(r"noise(\d+(?:p\d+)?)", text)
    if not match:
        return None
    return float(match.group(1).replace("p", "."))


def parse_seed(text: str) -> int | None:
    match = re.search(r"seed(\d+)", text)
    if not match:
        return None
    return int(match.group(1))


def infer_noise_percent(rows: list[dict], path: Path) -> float:
    values = {
        parse_noise_percent(str(row.get("case_label", "")))
        for row in rows
        if parse_noise_percent(str(row.get("case_label", ""))) is not None
    }
    if len(values) == 1:
        return float(next(iter(values)))
    from_path = parse_noise_percent(str(path))
    if from_path is not None:
        return float(from_path)
    return 10.0


def summarize_aggregate_csv(path: Path) -> dict:
    rows = read_csv_rows(path)
    if not rows:
        raise ValueError(f"empty aggregate CSV: {path}")
    clean_count = sum(1 for row in rows if row_clean(row))
    truth_count = sum(1 for row in rows if str(row.get("is_truth_geometry", "")).lower() == "true")
    x_ambiguity_count = sum(1 for row in rows if safe_float(row.get("ambiguity_x_width_mm"), 0.0) > 0.0)
    radius_margins = [safe_float(row.get("radius_margin_abs")) for row in rows]
    radius_margins = [value for value in radius_margins if math.isfinite(value)]
    seeds = {
        parse_seed(str(row.get("case_label", "")))
        for row in rows
        if parse_seed(str(row.get("case_label", ""))) is not None
    }
    sources = sorted({safe_float(row.get("sources")) for row in rows if math.isfinite(safe_float(row.get("sources")))})
    txrx_values = sorted({
        safe_float(row.get("tx_rx_offset_mm"))
        for row in rows
        if math.isfinite(safe_float(row.get("tx_rx_offset_mm")))
    })
    run_names = sorted({str(row.get("run_name", "")) for row in rows if row.get("run_name")})
    noise_percent = infer_noise_percent(rows, path)
    label = policy_label_for_counts(row_count=len(rows), clean_count=clean_count, truth_count=truth_count)
    if len(sources) == 1:
        sources_label = str(int(sources[0]))
    else:
        sources_label = ",".join(str(int(value)) for value in sources)
    if len(txrx_values) == 1:
        txrx_label = f"{txrx_values[0]:g}"
    else:
        txrx_label = ",".join(f"{value:g}" for value in txrx_values)
    return {
        "output_id": parse_output_id(path),
        "aggregate_csv": str(path),
        "run_name": path.parents[1].name,
        "noise_rms_percent": noise_percent,
        "sources": sources_label,
        "tx_rx_offset_mm": txrx_label,
        "seed_count": len(seeds),
        "unique_seed_values": ",".join(str(seed) for seed in sorted(seeds)),
        "run_count": len(run_names),
        "row_count": len(rows),
        "truth_geometry_count": truth_count,
        "clean_row_count": clean_count,
        "x_ambiguity_row_count": x_ambiguity_count,
        "radius_margin_abs_min": min(radius_margins) if radius_margins else math.nan,
        "radius_margin_abs_mean": float(np.mean(radius_margins)) if radius_margins else math.nan,
        "radius_margin_abs_max": max(radius_margins) if radius_margins else math.nan,
        "policy_label": label,
        "is_seed_replicated": len(seeds) >= 3,
    }


def load_boundary_summary(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    summary = data.get("summary", {})
    return {
        "path": str(path),
        "row_count": summary.get("row_count"),
        "clean_row_count": summary.get("clean_row_count"),
        "point_correct_not_clean_row_count": summary.get("point_correct_not_clean_row_count"),
        "single_seed_clean_noise_rms_percent_max": summary.get("single_seed_clean_noise_rms_percent_max"),
        "final_ambiguous_upper_noise_rms_percent": summary.get("final_ambiguous_upper_noise_rms_percent"),
        "final_ambiguous_upper_experiment_id": summary.get("final_ambiguous_upper_experiment_id"),
        "final_ambiguous_upper_nominal_margin_to_cutoff": summary.get("final_ambiguous_upper_nominal_margin_to_cutoff"),
        "final_bracket_width_percent_rms": summary.get("final_bracket_width_percent_rms"),
        "stop_due_to_numerical_edge": summary.get("stop_due_to_numerical_edge"),
    }


def derive_summary(rows: list[dict], boundary: dict) -> dict:
    clean_replicated = [
        row
        for row in rows
        if row["is_seed_replicated"] and row["policy_label"] == "clean_replicated"
    ]
    by_txrx: dict[str, list[dict]] = {}
    for row in rows:
        by_txrx.setdefault(str(row["tx_rx_offset_mm"]), []).append(row)
    txrx_rows = []
    for txrx, txrx_group in sorted(by_txrx.items(), key=lambda item: safe_float(item[0].split(",")[0])):
        clean = [row for row in txrx_group if row["policy_label"] == "clean_replicated"]
        replicated_clean = [row for row in clean if row["is_seed_replicated"]]
        txrx_rows.append({
            "tx_rx_offset_mm": txrx,
            "aggregate_count": len(txrx_group),
            "seed_replicated_count": sum(1 for row in txrx_group if row["is_seed_replicated"]),
            "max_replicated_clean_noise_rms_percent": (
                max(row["noise_rms_percent"] for row in replicated_clean)
                if replicated_clean
                else math.nan
            ),
            "max_any_clean_noise_rms_percent": max(row["noise_rms_percent"] for row in clean) if clean else math.nan,
            "minimum_replicated_clean_margin": (
                min(row["radius_margin_abs_min"] for row in replicated_clean)
                if replicated_clean
                else math.nan
            ),
        })
    txrx45 = [row for row in txrx_rows if row["tx_rx_offset_mm"] == "45"]
    txrx50 = [row for row in txrx_rows if row["tx_rx_offset_mm"] == "50"]
    txrx45_limit = txrx45[0]["max_replicated_clean_noise_rms_percent"] if txrx45 else math.nan
    txrx50_limit = txrx50[0]["max_replicated_clean_noise_rms_percent"] if txrx50 else math.nan
    upper = safe_float(boundary.get("final_ambiguous_upper_noise_rms_percent"))
    bracket_width = safe_float(boundary.get("final_bracket_width_percent_rms"))
    decision = (
        "Existing close14 evidence gives a seed-replicated clean bound of "
        f"{txrx50_limit:.12g}% RMS at Tx/Rx50 and a single-seed ambiguity edge at "
        f"{upper:.12g}% RMS. Tx/Rx45 is seed-replicated clean through "
        f"{txrx45_limit:.12g}% RMS in the archived branch."
    )
    return {
        "aggregate_row_count": len(rows),
        "clean_replicated_aggregate_count": len(clean_replicated),
        "tx_rx_policy_rows": txrx_rows,
        "txrx45_replicated_clean_noise_rms_percent": txrx45_limit,
        "txrx50_replicated_clean_noise_rms_percent": txrx50_limit,
        "txrx50_single_seed_ambiguous_upper_noise_rms_percent": upper,
        "txrx50_noise_boundary_bracket_width_percent_rms": bracket_width,
        "boundary": boundary,
        "decision": decision,
    }


def figure_stats(path: Path) -> dict:
    with Image.open(path) as image:
        arr = np.asarray(image.convert("RGB"))
        gray = np.asarray(image.convert("L"))
    sample = arr.reshape(-1, 3)[:: max(1, arr.reshape(-1, 3).shape[0] // 10000)]
    return {
        "path": str(path),
        "width": int(arr.shape[1]),
        "height": int(arr.shape[0]),
        "sampled_unique_colors": int(np.unique(sample, axis=0).shape[0]),
        "nonwhite_fraction": float(np.mean(np.any(arr < 250, axis=2))),
        "dynamic_range": int(gray.max()) - int(gray.min()),
    }


def plot_synthesis(rows: list[dict], boundary: dict, summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.8), constrained_layout=True)
    colors = {"45": "#4c78a8", "50": "#f58518", "45,50": "#54a24b"}
    markers = {"clean_replicated": "o", "truth_selected_interval": "s", "mixed_or_failed": "x"}

    for row in rows:
        txrx = str(row["tx_rx_offset_mm"])
        axes[0].scatter(
            row["noise_rms_percent"],
            row["radius_margin_abs_min"],
            color=colors.get(txrx, "#666666"),
            marker=markers.get(row["policy_label"], "o"),
            s=65 if row["is_seed_replicated"] else 42,
            alpha=0.9,
        )
        axes[1].scatter(
            row["noise_rms_percent"],
            row["x_ambiguity_row_count"],
            color=colors.get(txrx, "#666666"),
            marker=markers.get(row["policy_label"], "o"),
            s=65 if row["is_seed_replicated"] else 42,
            alpha=0.9,
        )
    axes[0].set_xlabel("noise RMS (%)")
    axes[0].set_ylabel("minimum radius margin")
    axes[0].set_title("Close14 aggregate margin")
    axes[0].grid(color="#dddddd", linewidth=0.6)

    axes[1].set_xlabel("noise RMS (%)")
    axes[1].set_ylabel("x-ambiguity rows")
    axes[1].set_title("Aggregate ambiguity")
    axes[1].grid(color="#dddddd", linewidth=0.6)

    clean_limit = safe_float(summary.get("txrx50_replicated_clean_noise_rms_percent"))
    upper = safe_float(boundary.get("final_ambiguous_upper_noise_rms_percent"))
    width = safe_float(boundary.get("final_bracket_width_percent_rms"))
    axes[2].bar(["clean max", "ambig. upper"], [clean_limit, upper], color=["#54a24b", "#e45756"])
    axes[2].set_ylabel("noise RMS (%)")
    axes[2].set_title(f"Tx/Rx50 scalar edge, width={width:.3g}%")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Close14 noise and acquisition policy synthesis", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def expand_default_aggregate_paths() -> list[Path]:
    paths: list[Path] = []
    for pattern in DEFAULT_AGGREGATE_GLOBS:
        paths.extend(Path(PROJECT_ROOT).glob(pattern))
    return sorted(set(paths), key=lambda path: str(path))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("aggregate_csv", nargs="*", help="close14 coordinate_confidence_aggregate.csv paths")
    parser.add_argument("--boundary-json", default=DEFAULT_BOUNDARY_JSON)
    parser.add_argument("--run-name", default="close14_noise_policy_synthesis")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    aggregate_paths = [Path(path) for path in args.aggregate_csv] if args.aggregate_csv else expand_default_aggregate_paths()
    if not aggregate_paths:
        raise ValueError("no close14 aggregate CSVs found")
    rows = [summarize_aggregate_csv(path) for path in aggregate_paths]
    rows.sort(key=lambda row: (safe_float(str(row["tx_rx_offset_mm"]).split(",")[0]), row["noise_rms_percent"], str(row["sources"])))
    boundary = load_boundary_summary(Path(args.boundary_json))
    summary = derive_summary(rows, boundary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root="outputs/experiments"))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "close14_noise_policy_rows.csv"
    txrx_csv = data_dir / "close14_noise_policy_by_txrx.csv"
    summary_json = data_dir / "close14_noise_policy_summary.json"
    figure_path = Path(plot_synthesis(rows, boundary, summary, figures_dir / "close14_noise_policy_synthesis.png"))
    validation_csv = data_dir / "figure_validation.csv"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(txrx_csv, [json_safe(row) for row in summary["tx_rx_policy_rows"]])
    validation_rows = [figure_stats(figure_path)]
    write_csv(validation_csv, [json_safe(row) for row in validation_rows])
    summary_payload = {
        **summary,
        "input_aggregate_csvs": [str(path) for path in aggregate_paths],
        "paths": {
            "rows_csv": str(rows_csv),
            "txrx_csv": str(txrx_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(summary_payload), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "close14_noise_policy_synthesis",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "txrx_csv": str(txrx_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary_payload), indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Separate physical non-overlap spacing policy from overlap stress tests."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import defaultdict
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
from run_coordinate_resolution_policy_synthesis import (  # noqa: E402
    POLICY_COLORS,
    DEFAULT_AGGREGATE_CSVS,
    load_policy_groups,
    safe_float,
    write_csv_rows,
)
from run_gssi_field_preprocess_feature_qc import json_safe  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_EXTRA_AGGREGATE_CSVS = [
    "outputs/experiments/360_coordinate_confidence_close14_sources4_txrx50_noise15p361328125_seed_replicates/data/coordinate_confidence_aggregate.csv",
]


def physical_regime(edge_clearance_mm: float) -> str:
    if edge_clearance_mm < -1.0e-9:
        return "overlap_stress_test"
    if abs(edge_clearance_mm) <= 1.0e-9:
        return "tangent_nonoverlap_limit"
    return "separated_nonoverlap"


def add_physical_columns(group_rows: list[dict], target_radius_pair_sum_mm: float) -> list[dict]:
    rows = []
    for row in group_rows:
        out = dict(row)
        edge_clearance = safe_float(row["close_spacing_mm"]) - float(target_radius_pair_sum_mm)
        out["target_radius_pair_sum_mm"] = float(target_radius_pair_sum_mm)
        out["edge_clearance_mm"] = edge_clearance
        out["physical_regime"] = physical_regime(edge_clearance)
        out["is_physical_nonoverlap"] = edge_clearance >= -1.0e-9
        rows.append(out)
    return rows


def summarize_physical_policy(rows: list[dict]) -> dict:
    by_txrx: dict[float, list[dict]] = defaultdict(list)
    for row in rows:
        by_txrx[safe_float(row["tx_rx_offset_mm"])].append(row)

    txrx_rows = []
    for txrx, group in sorted(by_txrx.items()):
        clean_nonoverlap = [
            row for row in group
            if row["policy_label"] == "clean_replicated" and bool(row["is_physical_nonoverlap"])
        ]
        clean_overlap = [
            row for row in group
            if row["policy_label"] == "clean_replicated" and not bool(row["is_physical_nonoverlap"])
        ]
        txrx_rows.append({
            "tx_rx_offset_mm": txrx,
            "closest_clean_physical_spacing_mm": min(
                (safe_float(row["close_spacing_mm"]) for row in clean_nonoverlap),
                default=math.nan,
            ),
            "clean_physical_spacings_mm": ", ".join(
                str(int(safe_float(row["close_spacing_mm"])))
                for row in sorted(clean_nonoverlap, key=lambda item: safe_float(item["close_spacing_mm"]))
            ),
            "clean_overlap_stress_spacings_mm": ", ".join(
                str(int(safe_float(row["close_spacing_mm"])))
                for row in sorted(clean_overlap, key=lambda item: safe_float(item["close_spacing_mm"]))
            ),
            "tested_group_count": len(group),
        })

    clean_nonoverlap_count = sum(
        1 for row in rows
        if row["policy_label"] == "clean_replicated" and bool(row["is_physical_nonoverlap"])
    )
    clean_overlap_count = sum(
        1 for row in rows
        if row["policy_label"] == "clean_replicated" and not bool(row["is_physical_nonoverlap"])
    )
    decision = (
        "For physical rebar-spacing claims with the current target1/target2 "
        "6 mm and 8 mm radius pair, close14 is the tangent non-overlap limit. "
        "The archive supports clean non-overlap/tangent recovery at close14 for "
        "the tested Tx/Rx45 and Tx/Rx50 branches; close10 and close12 should be "
        "reported only as overlapping-cylinder algorithmic stress tests."
    )
    return {
        "group_count": len(rows),
        "clean_nonoverlap_group_count": clean_nonoverlap_count,
        "clean_overlap_stress_group_count": clean_overlap_count,
        "tx_rx_policy_rows": txrx_rows,
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


def plot_physical_policy(rows: list[dict], save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.0), constrained_layout=True)
    marker_by_regime = {
        "separated_nonoverlap": "o",
        "tangent_nonoverlap_limit": "s",
        "overlap_stress_test": "X",
    }
    for row in rows:
        axes[0].scatter(
            [safe_float(row["close_spacing_mm"])],
            [safe_float(row["tx_rx_offset_mm"])],
            s=120,
            marker=marker_by_regime[row["physical_regime"]],
            color=POLICY_COLORS.get(row["policy_label"], "#777777"),
            edgecolors="#222222",
            linewidths=0.8,
        )
    axes[0].axvline(14.0, color="#222222", linestyle="--", linewidth=1.0, label="6+8 mm tangent")
    axes[0].set_xlabel("center spacing [mm]")
    axes[0].set_ylabel("Tx/Rx offset [mm]")
    axes[0].set_title("Physical spacing vs stress-test spacing")
    axes[0].grid(True, alpha=0.25)
    axes[0].legend(frameon=False, fontsize=8)

    clean = [row for row in rows if row["policy_label"] == "clean_replicated"]
    axes[1].bar(
        [f"{int(safe_float(row['close_spacing_mm']))}@{int(safe_float(row['tx_rx_offset_mm']))}" for row in clean],
        [safe_float(row["edge_clearance_mm"]) for row in clean],
        color=["#1b7837" if bool(row["is_physical_nonoverlap"]) else "#d99a19" for row in clean],
    )
    axes[1].axhline(0.0, color="#222222", linewidth=1.0)
    axes[1].set_ylabel("edge clearance [mm]")
    axes[1].set_title("Clean rows: non-overlap vs overlap")
    axes[1].tick_params(axis="x", rotation=45, labelsize=8)
    axes[1].grid(axis="y", alpha=0.25)

    fig.suptitle("Coordinate policy physical-spacing guardrail", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def default_paths() -> list[Path]:
    return [Path(path) for path in DEFAULT_AGGREGATE_CSVS + DEFAULT_EXTRA_AGGREGATE_CSVS]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("aggregate_csv", nargs="*", help="coordinate confidence aggregate CSV paths")
    parser.add_argument("--target-radius-pair-sum-mm", type=float, default=14.0)
    parser.add_argument("--run-name", default="coordinate_physical_spacing_policy_synthesis")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    input_paths = [Path(path) for path in args.aggregate_csv] if args.aggregate_csv else default_paths()
    for path in input_paths:
        if not path.exists():
            raise FileNotFoundError(path)

    group_rows = add_physical_columns(load_policy_groups(input_paths), args.target_radius_pair_sum_mm)
    summary = summarize_physical_policy(group_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    group_csv = data_dir / "coordinate_physical_spacing_policy_groups.csv"
    txrx_csv = data_dir / "coordinate_physical_spacing_policy_by_txrx.csv"
    summary_json = data_dir / "coordinate_physical_spacing_policy_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_physical_policy(group_rows, figures_dir / "coordinate_physical_spacing_policy.png"))

    write_csv_rows(group_csv, group_rows)
    write_csv_rows(txrx_csv, summary["tx_rx_policy_rows"])
    validation_rows = [figure_stats(figure_path)]
    write_csv_rows(validation_csv, validation_rows)
    summary["input_aggregate_csvs"] = [str(path) for path in input_paths]
    summary["paths"] = {
        "group_csv": str(group_csv),
        "txrx_csv": str(txrx_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "coordinate_physical_spacing_policy_synthesis",
        {
            "input_aggregate_csvs": [str(path) for path in input_paths],
            "summary_json": str(summary_json),
            "group_csv": str(group_csv),
            "txrx_csv": str(txrx_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

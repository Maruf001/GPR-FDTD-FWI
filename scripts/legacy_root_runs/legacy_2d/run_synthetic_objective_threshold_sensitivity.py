#!/usr/bin/env python3
"""Test objective near-tie sensitivity to ambiguity-threshold scaling."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_archive_location_clean_metric_audit import safe_float  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_COMPETITOR_ROWS = (
    "outputs/experiments/1287_competing_geometry_near_tie_audit/data/"
    "competing_geometry_near_tie_rows.csv"
)
DEFAULT_THRESHOLD_SCALES = "0.1,0.25,0.5,0.75,1.0,1.25,1.5,2.0"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_scales(text: str) -> list[float]:
    scales = [float(part.strip()) for part in text.split(",") if part.strip()]
    if not scales:
        raise ValueError("at least one threshold scale is required")
    return sorted(scales)


def is_target2_close14_known_x(row: dict) -> bool:
    text = " ".join(str(row.get(key, "")) for key in ("aggregate_run", "source_csv", "run_name")).lower()
    return (
        int(safe_float(row.get("target_index"), -1)) == 2
        and "close14" in text
        and str(row.get("geometry_delta_class", "")) == "x"
        and math.isfinite(safe_float(row.get("sources")))
        and math.isfinite(safe_float(row.get("tx_rx_offset_mm")))
    )


def ratio_row(row: dict) -> dict:
    best = safe_float(row.get("best_misfit"))
    threshold = safe_float(row.get("ambiguity_misfit_threshold"))
    gap = safe_float(row.get("competitor_objective_gap_abs"))
    width = threshold - best
    ratio = gap / width if math.isfinite(width) and width > 0.0 else math.nan
    return {
        **row,
        "threshold_width": width,
        "competitor_gap_to_threshold_width_ratio": ratio,
    }


def threshold_sensitivity_rows(rows: list[dict], scales: list[float]) -> list[dict]:
    filtered = [ratio_row(row) for row in rows if is_target2_close14_known_x(row)]
    grouped: dict[tuple[int, float], list[dict]] = defaultdict(list)
    for row in filtered:
        grouped[(int(round(safe_float(row.get("sources")))), safe_float(row.get("tx_rx_offset_mm")))].append(row)

    out: list[dict] = []
    for (sources, txrx), group_rows in sorted(grouped.items()):
        ratios = [
            safe_float(row.get("competitor_gap_to_threshold_width_ratio"))
            for row in group_rows
            if math.isfinite(safe_float(row.get("competitor_gap_to_threshold_width_ratio")))
        ]
        for scale in scales:
            near_count = sum(1 for ratio in ratios if ratio <= scale)
            out.append({
                "target_index": 2,
                "family_label": "target2_close14",
                "geometry_delta_class": "x",
                "sources": sources,
                "tx_rx_offset_mm": txrx,
                "threshold_scale": scale,
                "row_count": len(group_rows),
                "near_tie_count_at_scale": near_count,
                "near_tie_fraction_at_scale": near_count / len(group_rows) if group_rows else math.nan,
                "min_gap_to_threshold_ratio": min(ratios) if ratios else math.nan,
                "median_gap_to_threshold_ratio": float(np.median(ratios)) if ratios else math.nan,
                "max_gap_to_threshold_ratio": max(ratios) if ratios else math.nan,
                "interpretation": (
                    "persistent_under_tight_threshold"
                    if scale <= 0.75 and near_count > 0
                    else "default_threshold_near_tie"
                    if abs(scale - 1.0) < 1e-12 and near_count > 0
                    else "separated_at_this_scale"
                    if near_count == 0
                    else "loose_threshold_sensitive"
                ),
            })
    return out


def summarize_threshold_sensitivity(rows: list[dict]) -> dict:
    scale_rows = {(row["sources"], row["tx_rx_offset_mm"], row["threshold_scale"]): row for row in rows}

    def total_at(scale: float) -> int:
        return sum(int(row["near_tie_count_at_scale"]) for row in rows if abs(row["threshold_scale"] - scale) < 1e-12)

    default_near = total_at(1.0)
    tight_075 = total_at(0.75)
    tight_05 = total_at(0.5)
    loose_125 = total_at(1.25)
    source5_45_default = int(scale_rows.get((5, 45.0, 1.0), {}).get("near_tie_count_at_scale", 0))
    source5_45_tight05 = int(scale_rows.get((5, 45.0, 0.5), {}).get("near_tie_count_at_scale", 0))
    source4_45_default = int(scale_rows.get((4, 45.0, 1.0), {}).get("near_tie_count_at_scale", 0))
    source7_45_default = int(scale_rows.get((7, 45.0, 1.0), {}).get("near_tie_count_at_scale", 0))
    source4_50_default = int(scale_rows.get((4, 50.0, 1.0), {}).get("near_tie_count_at_scale", 0))
    source4_50_loose125 = int(scale_rows.get((4, 50.0, 1.25), {}).get("near_tie_count_at_scale", 0))
    row_count = sum(int(row["row_count"]) for row in rows if abs(row["threshold_scale"] - 1.0) < 1e-12)
    return {
        "policy_label": "close14_target2_objective_threshold_sensitivity_source5_persistent_cpu_no_gpu",
        "family_label": "target2_close14",
        "geometry_delta_class": "x",
        "default_scale_row_count": row_count,
        "near_tie_count_at_scale_0p5": tight_05,
        "near_tie_count_at_scale_0p75": tight_075,
        "near_tie_count_at_scale_1p0": default_near,
        "near_tie_count_at_scale_1p25": loose_125,
        "source5_txrx45_near_tie_count_at_scale_0p5": source5_45_tight05,
        "source5_txrx45_near_tie_count_at_scale_1p0": source5_45_default,
        "source4_txrx45_default_threshold_edge_count": source4_45_default,
        "source7_txrx45_default_threshold_edge_count": source7_45_default,
        "source4_txrx50_default_near_tie_count": source4_50_default,
        "source4_txrx50_loose_1p25_near_tie_count": source4_50_loose125,
        "gpu_priority": "none_now",
        "decision": (
            "The source5/TxRx45 close14 target2 x near ties persist under a 0.5x "
            "threshold, while the source4 and source7 default near ties are edge "
            "cases. TxRx50 is clean at the default threshold but becomes sensitive "
            "under looser thresholds, so future GPU work should wait for a fixed "
            "objective threshold and remain narrow."
        ),
    }


def plot_threshold_sensitivity(rows: list[dict], summary: dict, save_path: Path) -> str:
    groups = sorted({(row["sources"], row["tx_rx_offset_mm"]) for row in rows})
    scales = sorted({row["threshold_scale"] for row in rows})

    fig, axes = plt.subplots(1, 2, figsize=(15.0, 5.2), constrained_layout=True)
    for sources, txrx in groups:
        group_rows = [row for row in rows if row["sources"] == sources and row["tx_rx_offset_mm"] == txrx]
        group_rows = sorted(group_rows, key=lambda row: row["threshold_scale"])
        axes[0].plot(
            [row["threshold_scale"] for row in group_rows],
            [row["near_tie_count_at_scale"] for row in group_rows],
            marker="o",
            linewidth=1.8,
            label=f"{sources} src, {txrx:g} mm",
        )
    axes[0].axvline(1.0, color="#6b6b6b", linestyle="--", linewidth=1.0)
    axes[0].set_xticks(scales)
    axes[0].set_xlabel("ambiguity-threshold scale")
    axes[0].set_ylabel("near-tie row count")
    axes[0].set_title("Close14 target2 x near ties by threshold scale")
    axes[0].grid(color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    labels = ["0.5x", "0.75x", "1.0x", "1.25x"]
    values = [
        summary["near_tie_count_at_scale_0p5"],
        summary["near_tie_count_at_scale_0p75"],
        summary["near_tie_count_at_scale_1p0"],
        summary["near_tie_count_at_scale_1p25"],
    ]
    axes[1].bar(np.arange(len(values)), values, color=["#2f9d55", "#4c78a8", "#c7302b", "#f58518"])
    axes[1].set_xticks(np.arange(len(values)), labels)
    axes[1].set_ylabel("near-tie row count")
    axes[1].set_title("Aggregate threshold sensitivity")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"Synthetic objective-threshold sensitivity: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--competitor-rows-csv", default=DEFAULT_COMPETITOR_ROWS)
    parser.add_argument("--threshold-scales", default=DEFAULT_THRESHOLD_SCALES)
    parser.add_argument("--run-name", default="synthetic_objective_threshold_sensitivity")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    scales = parse_scales(args.threshold_scales)
    rows = threshold_sensitivity_rows(read_csv_rows(Path(args.competitor_rows_csv)), scales)
    summary = summarize_threshold_sensitivity(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "synthetic_objective_threshold_sensitivity_rows.csv"
    summary_json = data_dir / "synthetic_objective_threshold_sensitivity_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_threshold_sensitivity(rows, summary, figures_dir / "synthetic_objective_threshold_sensitivity.png"))

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "competitor_rows_csv": args.competitor_rows_csv,
        "threshold_scales": ",".join(str(scale) for scale in scales),
        **summary,
        "paths": {
            "rows_csv": str(rows_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "synthetic_objective_threshold_sensitivity",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

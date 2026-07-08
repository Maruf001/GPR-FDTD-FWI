#!/usr/bin/env python3
"""Map objective-uniqueness caveats by acquisition metadata and target."""

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


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _is_finite(value: object) -> bool:
    return math.isfinite(safe_float(value))


def _label_number(value: object, suffix: str = "") -> str:
    numeric = safe_float(value)
    if not math.isfinite(numeric):
        return "unknown"
    if abs(numeric - round(numeric)) < 1e-9:
        return f"{int(round(numeric))}{suffix}"
    return f"{numeric:g}{suffix}"


def _near_tie_tier(row: dict) -> str:
    return str(row.get("near_tie_tier", "")).strip()


def _metadata_status(row: dict) -> str:
    has_sources = _is_finite(row.get("sources"))
    has_offset = _is_finite(row.get("tx_rx_offset_mm"))
    if has_sources and has_offset:
        return "known_sources_and_txrx"
    if has_sources:
        return "known_sources_missing_txrx"
    if has_offset:
        return "missing_sources_known_txrx"
    return "archive_missing_sources_and_txrx"


def _actionability(row: dict, near_tie_count: int) -> tuple[str, str, str]:
    if near_tie_count == 0:
        return (
            "no_current_gap",
            "none",
            "No acquisition probe is indicated for this cell.",
        )
    status = _metadata_status(row)
    target = int(safe_float(row.get("target_index"), -1))
    delta = str(row.get("geometry_delta_class", ""))
    if status != "known_sources_and_txrx":
        return (
            "archive_metadata_gap",
            "none_archive_claim_caveat",
            "Keep objective-uniqueness caveats; do not launch GPU work solely to repair archive metadata.",
        )
    if target == 2 and "x" in delta:
        return (
            "known_acquisition_x_resolution_gap",
            "low_conditional_after_objective_scope",
            "Use CPU objective/reporting design first; only consider a narrow target2 x-resolution probe if the manuscript needs it.",
        )
    return (
        "known_acquisition_objective_gap",
        "low_conditional_after_objective_scope",
        "Use CPU objective/reporting design first; any GPU follow-up should be narrow and hypothesis-driven.",
    )


def acquisition_gap_rows(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        key = (
            int(safe_float(row.get("target_index"), -1)),
            _label_number(row.get("sources")),
            _label_number(row.get("tx_rx_offset_mm"), "mm"),
            _metadata_status(row),
            str(row.get("geometry_delta_class", "") or "none"),
        )
        grouped[key].append(row)

    out: list[dict] = []
    for key, group_rows in grouped.items():
        target, sources_label, txrx_label, metadata_status, geometry_delta_class = key
        exact = len(group_rows)
        separated = sum(1 for row in group_rows if _near_tie_tier(row) == "competitor_separated")
        reported = sum(1 for row in group_rows if _near_tie_tier(row) == "reported_width_near_tie")
        hidden = sum(
            1 for row in group_rows if _near_tie_tier(row) == "zero_width_competing_geometry_near_tie"
        )
        near_tie_count = reported + hidden
        representative = group_rows[0]
        actionability, gpu_priority, action = _actionability(representative, near_tie_count)
        gaps = [
            safe_float(row.get("competitor_objective_gap_abs"))
            for row in group_rows
            if math.isfinite(safe_float(row.get("competitor_objective_gap_abs")))
        ]
        out.append({
            "target_index": target,
            "sources_label": sources_label,
            "tx_rx_offset_label": txrx_label,
            "metadata_status": metadata_status,
            "geometry_delta_class": geometry_delta_class,
            "exact_strong_row_count": exact,
            "competitor_separated_count": separated,
            "reported_width_near_tie_count": reported,
            "zero_width_competing_geometry_near_tie_count": hidden,
            "near_tie_row_count": near_tie_count,
            "objective_unique_fraction": separated / exact if exact else math.nan,
            "near_tie_fraction": near_tie_count / exact if exact else math.nan,
            "min_competitor_objective_gap_abs": min(gaps) if gaps else math.nan,
            "actionability_label": actionability,
            "gpu_priority": gpu_priority,
            "recommended_action": action,
        })
    return sorted(
        out,
        key=lambda row: (
            row["actionability_label"] != "known_acquisition_x_resolution_gap",
            -row["near_tie_row_count"],
            row["target_index"],
            row["sources_label"],
            row["tx_rx_offset_label"],
            row["geometry_delta_class"],
        ),
    )


def summarize_gap_map(rows: list[dict]) -> dict:
    exact = sum(int(row["exact_strong_row_count"]) for row in rows)
    near_ties = sum(int(row["near_tie_row_count"]) for row in rows)
    known_near_ties = sum(
        int(row["near_tie_row_count"])
        for row in rows
        if row["metadata_status"] == "known_sources_and_txrx"
    )
    archive_near_ties = near_ties - known_near_ties
    target1_known = sum(
        int(row["near_tie_row_count"])
        for row in rows
        if row["target_index"] == 1 and row["metadata_status"] == "known_sources_and_txrx"
    )
    target2_known = sum(
        int(row["near_tie_row_count"])
        for row in rows
        if row["target_index"] == 2 and row["metadata_status"] == "known_sources_and_txrx"
    )
    actionable_cells = [
        row for row in rows if row["actionability_label"] == "known_acquisition_x_resolution_gap"
    ]
    top_action = actionable_cells[0] if actionable_cells else {}
    return {
        "policy_label": "objective_uniqueness_gap_map_known_target2_x_gaps_cpu_no_gpu",
        "cell_count": len(rows),
        "exact_strong_row_count": exact,
        "near_tie_row_count": near_ties,
        "known_acquisition_near_tie_row_count": known_near_ties,
        "archive_metadata_near_tie_row_count": archive_near_ties,
        "target1_known_acquisition_near_tie_row_count": target1_known,
        "target2_known_acquisition_near_tie_row_count": target2_known,
        "known_actionable_cell_count": len(actionable_cells),
        "top_actionable_target_index": top_action.get("target_index", ""),
        "top_actionable_sources_label": top_action.get("sources_label", ""),
        "top_actionable_tx_rx_offset_label": top_action.get("tx_rx_offset_label", ""),
        "top_actionable_near_tie_row_count": top_action.get("near_tie_row_count", 0),
        "gpu_priority": "none_now",
        "decision": (
            "The objective-uniqueness caveats are mostly archive-metadata caveats. "
            "Known-acquisition near ties are target2 x-resolution gaps, so any "
            "future GPU work should be a narrow target2 probe after CPU objective "
            "scope is fixed, not a broad sweep."
        ),
    }


def plot_gap_map(rows: list[dict], summary: dict, save_path: Path) -> str:
    known_rows = [row for row in rows if row["near_tie_row_count"] > 0][:12]
    labels = [
        f"t{row['target_index']}\n{row['sources_label']}\n{row['tx_rx_offset_label']}\n{row['geometry_delta_class']}"
        for row in known_rows
    ]
    x = np.arange(len(known_rows))
    near = np.asarray([row["near_tie_row_count"] for row in known_rows], dtype=np.float64)
    exact = np.asarray([row["exact_strong_row_count"] for row in known_rows], dtype=np.float64)
    known = summary["known_acquisition_near_tie_row_count"]
    archive = summary["archive_metadata_near_tie_row_count"]

    fig, axes = plt.subplots(1, 2, figsize=(15.0, 5.2), constrained_layout=True)
    axes[0].bar([0, 1], [known, archive], color=["#2f9d55", "#6b6b6b"], width=0.55)
    axes[0].set_xticks([0, 1], ["known\nacquisition", "archive\nmetadata"])
    axes[0].set_ylabel("near-tie row count")
    axes[0].set_title("Near ties by metadata actionability")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x - 0.18, exact, width=0.36, color="#4c78a8", label="exact-strong rows")
    axes[1].bar(x + 0.18, near, width=0.36, color="#c7302b", label="near-tie rows")
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("row count")
    axes[1].set_title("Top objective-uniqueness gap cells")
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"Synthetic objective-uniqueness acquisition gap map: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--competitor-rows-csv", default=DEFAULT_COMPETITOR_ROWS)
    parser.add_argument("--run-name", default="synthetic_objective_uniqueness_acquisition_gap_map")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    rows = acquisition_gap_rows(read_csv_rows(Path(args.competitor_rows_csv)))
    summary = summarize_gap_map(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "synthetic_objective_uniqueness_acquisition_gap_rows.csv"
    summary_json = data_dir / "synthetic_objective_uniqueness_acquisition_gap_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(
        plot_gap_map(rows, summary, figures_dir / "synthetic_objective_uniqueness_acquisition_gap_map.png")
    )

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "competitor_rows_csv": args.competitor_rows_csv,
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
        "synthetic_objective_uniqueness_acquisition_gap_map",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

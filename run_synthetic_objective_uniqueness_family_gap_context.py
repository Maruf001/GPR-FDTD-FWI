#!/usr/bin/env python3
"""Summarize objective-uniqueness gaps by synthetic experiment family."""

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


def finite_label(value: object, suffix: str = "") -> str:
    numeric = safe_float(value)
    if not math.isfinite(numeric):
        return "unknown"
    if abs(numeric - round(numeric)) < 1e-9:
        return f"{int(round(numeric))}{suffix}"
    return f"{numeric:g}{suffix}"


def metadata_status(row: dict) -> str:
    has_sources = math.isfinite(safe_float(row.get("sources")))
    has_offset = math.isfinite(safe_float(row.get("tx_rx_offset_mm")))
    if has_sources and has_offset:
        return "known_sources_and_txrx"
    if has_sources:
        return "known_sources_missing_txrx"
    if has_offset:
        return "missing_sources_known_txrx"
    return "archive_missing_sources_and_txrx"


def family_label(row: dict) -> str:
    target = int(safe_float(row.get("target_index"), -1))
    text = " ".join(
        str(row.get(key, ""))
        for key in ("aggregate_run", "source_csv", "run_name", "case_label")
    ).lower()
    if "close14" in text:
        return "target2_close14"
    if "close50" in text:
        return "target2_close50"
    if "variable_depth_radius" in text:
        return "target2_variable_depth_radius"
    if "variable_radius_target2" in text:
        return "target2_variable_radius_legacy"
    if target == 1 and ("seed_offset2mm" in text or "coordinate_optimizer_noise" in text):
        return "target1_legacy_archive"
    return "other_archive_or_mixed"


def is_near_tie(row: dict) -> bool:
    return str(row.get("near_tie_tier", "")) != "competitor_separated"


def family_gap_rows(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        key = (
            int(safe_float(row.get("target_index"), -1)),
            family_label(row),
            metadata_status(row),
            str(row.get("geometry_delta_class", "") or "none"),
        )
        grouped[key].append(row)

    out: list[dict] = []
    for (target, family, metadata, delta), group_rows in grouped.items():
        exact = len(group_rows)
        near = [row for row in group_rows if is_near_tie(row)]
        reported = sum(1 for row in near if row.get("near_tie_tier") == "reported_width_near_tie")
        zero_width = sum(
            1 for row in near if row.get("near_tie_tier") == "zero_width_competing_geometry_near_tie"
        )
        source_labels = sorted({finite_label(row.get("sources")) for row in near})
        txrx_labels = sorted({finite_label(row.get("tx_rx_offset_mm"), "mm") for row in near})
        known_near = sum(1 for row in near if metadata_status(row) == "known_sources_and_txrx")
        gaps = [
            safe_float(row.get("competitor_objective_gap_abs"))
            for row in near
            if math.isfinite(safe_float(row.get("competitor_objective_gap_abs")))
        ]
        if not near:
            action = "family_clean_in_current_archive"
            gpu = "none"
            recommendation = "No near-tie action is indicated for this family slice."
        elif family == "target2_close14" and known_near and "x" in delta:
            action = "known_close14_target2_x_gap"
            gpu = "low_conditional_after_objective_scope"
            recommendation = (
                "If a GPU probe is needed, keep it narrow: target2 close14 x-resolution "
                "around the existing Tx/Rx=45 mm family after CPU objective scope is fixed."
            )
        elif family == "target2_variable_depth_radius" and known_near:
            action = "known_target2_depth_radius_gap"
            gpu = "low_conditional_after_objective_scope"
            recommendation = (
                "Treat as a separate target2 depth/radius ambiguity; do not mix it with close-spacing x-resolution claims."
            )
        else:
            action = "archive_or_metadata_claim_caveat"
            gpu = "none_archive_claim_caveat"
            recommendation = (
                "Keep as manuscript claim caveat; current metadata do not justify a new GPU run."
            )
        out.append({
            "target_index": target,
            "family_label": family,
            "metadata_status": metadata,
            "geometry_delta_class": delta,
            "exact_strong_row_count": exact,
            "near_tie_row_count": len(near),
            "reported_width_near_tie_count": reported,
            "zero_width_competing_geometry_near_tie_count": zero_width,
            "known_acquisition_near_tie_count": known_near,
            "near_tie_source_labels": ";".join(source_labels),
            "near_tie_tx_rx_offset_labels": ";".join(txrx_labels),
            "min_near_tie_objective_gap_abs": min(gaps) if gaps else math.nan,
            "actionability_label": action,
            "gpu_priority": gpu,
            "recommended_action": recommendation,
        })
    return sorted(
        out,
        key=lambda row: (
            row["actionability_label"] != "known_close14_target2_x_gap",
            row["actionability_label"] != "known_target2_depth_radius_gap",
            -row["near_tie_row_count"],
            row["target_index"],
            row["family_label"],
            row["metadata_status"],
            row["geometry_delta_class"],
        ),
    )


def summarize_family_gaps(rows: list[dict]) -> dict:
    near_total = sum(int(row["near_tie_row_count"]) for row in rows)
    known_close14_x = sum(
        int(row["known_acquisition_near_tie_count"])
        for row in rows
        if row["actionability_label"] == "known_close14_target2_x_gap"
    )
    known_depth_radius = sum(
        int(row["known_acquisition_near_tie_count"])
        for row in rows
        if row["actionability_label"] == "known_target2_depth_radius_gap"
    )
    target1_archive = sum(
        int(row["near_tie_row_count"])
        for row in rows
        if row["family_label"] == "target1_legacy_archive"
    )
    close50_known = sum(
        int(row["known_acquisition_near_tie_count"])
        for row in rows
        if row["family_label"] == "target2_close50"
    )
    return {
        "policy_label": "objective_uniqueness_family_context_close14_target2_cpu_no_gpu",
        "family_cell_count": len(rows),
        "near_tie_row_count": near_total,
        "known_close14_target2_x_near_tie_count": known_close14_x,
        "known_target2_depth_radius_near_tie_count": known_depth_radius,
        "target1_legacy_archive_near_tie_count": target1_archive,
        "target2_close50_known_near_tie_count": close50_known,
        "gpu_priority": "none_now",
        "decision": (
            "Known-acquisition target2 x-resolution caveats come from the close14 "
            "family, not close50. Keep target1 as an archive caveat and separate "
            "variable-depth/radius ambiguity from close-spacing x-resolution."
        ),
    }


def plot_family_label(row: dict) -> str:
    family = str(row["family_label"]).replace("target2_", "").replace("_", "\n")
    return f"t{row['target_index']}\n{family}\n{row['geometry_delta_class']}"


def plot_family_context(rows: list[dict], summary: dict, save_path: Path) -> str:
    visible = [row for row in rows if row["near_tie_row_count"] > 0]
    labels = [plot_family_label(row) for row in visible]
    x = np.arange(len(visible))
    near = np.asarray([row["near_tie_row_count"] for row in visible], dtype=np.float64)
    known = np.asarray([row["known_acquisition_near_tie_count"] for row in visible], dtype=np.float64)

    fig, axes = plt.subplots(1, 2, figsize=(15.0, 5.2), constrained_layout=True)
    axes[0].bar(
        np.arange(4),
        [
            summary["known_close14_target2_x_near_tie_count"],
            summary["known_target2_depth_radius_near_tie_count"],
            summary["target1_legacy_archive_near_tie_count"],
            summary["target2_close50_known_near_tie_count"],
        ],
        color=["#c7302b", "#f58518", "#6b6b6b", "#2f9d55"],
        width=0.58,
    )
    axes[0].set_xticks(
        np.arange(4),
        ["known\nclose14 x", "known\ndepth/radius", "target1\narchive", "known\nclose50"],
    )
    axes[0].set_ylabel("near-tie row count")
    axes[0].set_title("Family-level actionability")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x - 0.18, near, width=0.36, color="#c7302b", label="near-tie rows")
    axes[1].bar(x + 0.18, known, width=0.36, color="#2f9d55", label="known acquisition")
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("row count")
    axes[1].set_title("Near ties by family slice")
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"Synthetic objective-uniqueness family context: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--competitor-rows-csv", default=DEFAULT_COMPETITOR_ROWS)
    parser.add_argument("--run-name", default="synthetic_objective_uniqueness_family_gap_context")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    rows = family_gap_rows(read_csv_rows(Path(args.competitor_rows_csv)))
    summary = summarize_family_gaps(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "synthetic_objective_uniqueness_family_gap_rows.csv"
    summary_json = data_dir / "synthetic_objective_uniqueness_family_gap_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(
        plot_family_context(rows, summary, figures_dir / "synthetic_objective_uniqueness_family_gap_context.png")
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
        "synthetic_objective_uniqueness_family_gap_context",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

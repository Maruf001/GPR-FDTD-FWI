#!/usr/bin/env python3
"""Audit spatial transferability between short and long measured-field anchors."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_TIMING_ENVELOPE_RUN = "115_gssi51600s_field_cue_timing_envelope_post_cue_support_catalog"
DEFAULT_SPATIAL_MATCH_THRESHOLD_MM = 100.0


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def anchor_rows_by_family(rows: list[dict], family: str, *, content_only: bool = False) -> list[dict]:
    out = [row for row in rows if str(row.get("support_family", "")) == family]
    if content_only:
        out = [
            row for row in out
            if str(row.get("support_category", "")) == "short_content_backed_time_zero_anchor"
        ]
    return out


def nearest_anchor(source: dict, candidates: list[dict]) -> tuple[dict | None, float]:
    source_x = safe_float(source.get("anchor_x_mm"))
    if not math.isfinite(source_x) or not candidates:
        return None, math.nan
    best = min(candidates, key=lambda row: abs(safe_float(row.get("anchor_x_mm")) - source_x))
    return best, abs(safe_float(best.get("anchor_x_mm")) - source_x)


def build_spatial_transfer_rows(
    timing_rows: list[dict],
    *,
    spatial_match_threshold_mm: float = DEFAULT_SPATIAL_MATCH_THRESHOLD_MM,
) -> list[dict]:
    short_content = anchor_rows_by_family(timing_rows, "short_relative_timing", content_only=True)
    long_pattern = anchor_rows_by_family(timing_rows, "long_pattern_only")
    out = []
    for direction, sources, targets in (
        ("short_content_to_nearest_long_pattern", short_content, long_pattern),
        ("long_pattern_to_nearest_short_content", long_pattern, short_content),
    ):
        for source in sources:
            target, distance = nearest_anchor(source, targets)
            source_offset = safe_float(source.get("offset_ns"))
            target_offset = safe_float(target.get("offset_ns")) if target else math.nan
            delta_half_widths = safe_float(source.get("delta_to_short_content_half_widths"))
            target_delta_half_widths = safe_float(target.get("delta_to_short_content_half_widths")) if target else math.nan
            out.append(
                {
                    "transfer_direction": direction,
                    "source_anchor_id": source.get("support_anchor_id", ""),
                    "source_family": source.get("support_family", ""),
                    "source_category": source.get("support_category", ""),
                    "source_x_mm": safe_float(source.get("anchor_x_mm")),
                    "source_offset_ns": source_offset,
                    "source_delta_half_widths": delta_half_widths,
                    "nearest_anchor_id": target.get("support_anchor_id", "") if target else "",
                    "nearest_family": target.get("support_family", "") if target else "",
                    "nearest_category": target.get("support_category", "") if target else "",
                    "nearest_x_mm": safe_float(target.get("anchor_x_mm")) if target else math.nan,
                    "nearest_offset_ns": target_offset,
                    "nearest_delta_half_widths": target_delta_half_widths,
                    "spatial_distance_mm": distance,
                    "within_spatial_threshold": bool(math.isfinite(distance) and distance <= spatial_match_threshold_mm),
                    "timing_classes_match": (
                        str(source.get("timing_envelope_class", ""))
                        == str(target.get("timing_envelope_class", ""))
                        if target else False
                    ),
                    "source_transfer_scope": source.get("transfer_scope", ""),
                    "nearest_transfer_scope": target.get("transfer_scope", "") if target else "",
                }
            )
    return out


def summarize(
    transfer_rows: list[dict],
    timing_summary: dict,
    *,
    spatial_match_threshold_mm: float = DEFAULT_SPATIAL_MATCH_THRESHOLD_MM,
) -> dict:
    short_rows = [
        row for row in transfer_rows
        if row["transfer_direction"] == "short_content_to_nearest_long_pattern"
    ]
    long_rows = [
        row for row in transfer_rows
        if row["transfer_direction"] == "long_pattern_to_nearest_short_content"
    ]
    long_distances = [
        safe_float(row.get("spatial_distance_mm"))
        for row in long_rows
        if math.isfinite(safe_float(row.get("spatial_distance_mm")))
    ]
    short_distances = [
        safe_float(row.get("spatial_distance_mm"))
        for row in short_rows
        if math.isfinite(safe_float(row.get("spatial_distance_mm")))
    ]
    long_within = sum(bool(row.get("within_spatial_threshold")) for row in long_rows)
    short_within = sum(bool(row.get("within_spatial_threshold")) for row in short_rows)
    ready_for_transfer = (
        bool(short_rows)
        and bool(long_rows)
        and short_within == len(short_rows)
        and long_within == len(long_rows)
        and bool(timing_summary.get("ready_for_long_short_transfer", False))
    )
    return {
        "policy_label": "gssi51600s_field_spatial_transfer_audit_no_short_to_long_transfer",
        "spatial_match_threshold_mm": spatial_match_threshold_mm,
        "short_content_anchor_count": len(short_rows),
        "short_content_with_nearest_long_within_threshold_count": short_within,
        "long_pattern_anchor_count": len(long_rows),
        "long_pattern_with_nearest_short_content_within_threshold_count": long_within,
        "median_short_to_long_distance_mm": float(np.median(short_distances)) if short_distances else math.nan,
        "median_long_to_short_distance_mm": float(np.median(long_distances)) if long_distances else math.nan,
        "max_long_to_short_distance_mm": max(long_distances) if long_distances else math.nan,
        "ready_for_short_to_long_timing_transfer": ready_for_transfer,
        "ready_for_absolute_time_zero": False,
        "ready_for_cover_depth_recovery": False,
        "ready_for_radius_recovery": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "Use this as a spatial-transfer guardrail for the measured field data. "
            "The short content-backed anchors do not provide dense spatial support for the long "
            "pattern anchors, and the timing-envelope policy already rejects short-to-long transfer. "
            "Therefore the field data remain 2D QC/supplement evidence, not field FWI or 3D/HPC input."
        ),
    }


def plot_spatial_transfer(rows: list[dict], summary: dict, save_path: Path) -> str:
    long_rows = [
        row for row in rows
        if row["transfer_direction"] == "long_pattern_to_nearest_short_content"
    ]
    short_rows = [
        row for row in rows
        if row["transfer_direction"] == "short_content_to_nearest_long_pattern"
    ]
    fig, axes = plt.subplots(1, 2, figsize=(14.8, 5.2), constrained_layout=True)

    for ax, plot_rows, title in (
        (axes[0], short_rows, "Short content anchors to nearest long pattern"),
        (axes[1], long_rows, "Long pattern anchors to nearest short content"),
    ):
        labels = [str(row["source_anchor_id"]).replace("_", "\n") for row in plot_rows]
        values = [safe_float(row["spatial_distance_mm"], 0.0) for row in plot_rows]
        colors = ["#4c9f70" if row["within_spatial_threshold"] else "#d08a2e" for row in plot_rows]
        ax.bar(np.arange(len(plot_rows)), values, color=colors, edgecolor="#333333")
        ax.axhline(summary["spatial_match_threshold_mm"], color="#c7302b", linestyle="--", linewidth=1.2)
        ax.set_xticks(np.arange(len(plot_rows)), labels, fontsize=8)
        ax.set_ylabel("nearest-anchor distance (mm)")
        ax.set_title(title)
        ax.grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.96,
        f"long covered={summary['long_pattern_with_nearest_short_content_within_threshold_count']}/{summary['long_pattern_anchor_count']}\n"
        f"short covered={summary['short_content_with_nearest_long_within_threshold_count']}/{summary['short_content_anchor_count']}\n"
        "field FWI=false",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI 51600S spatial transfer audit: short timing does not cover long profile", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, summary_json: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_spatial_transfer_audit.png`",
                "",
                "This figure audits nearest-anchor spatial transferability between short",
                "content-backed timing anchors and long pattern-only anchors.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Spatial threshold: `{summary['spatial_match_threshold_mm']}` mm.",
                f"Short content anchors within threshold of a long anchor: `{summary['short_content_with_nearest_long_within_threshold_count']}` / `{summary['short_content_anchor_count']}`.",
                f"Long pattern anchors within threshold of a short content anchor: `{summary['long_pattern_with_nearest_short_content_within_threshold_count']}` / `{summary['long_pattern_anchor_count']}`.",
                f"Ready for short-to-long timing transfer: `{summary['ready_for_short_to_long_timing_transfer']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Transfer rows: `{rows_csv.name}`.",
                f"- Summary JSON: `{summary_json.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved field timing-envelope rows only. It does not run",
                "FDTD, FWI, GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--timing-envelope-run", default=DEFAULT_TIMING_ENVELOPE_RUN)
    parser.add_argument("--spatial-match-threshold-mm", type=float, default=DEFAULT_SPATIAL_MATCH_THRESHOLD_MM)
    parser.add_argument("--run-name", default="gssi51600s_field_spatial_transfer_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_root = field_dataset_output_root(args.field_root, args.dataset_id)
    source_dir = output_root / args.timing_envelope_run
    timing_rows = read_csv_rows(source_dir / "data/field_cue_timing_envelope_rows.csv")
    timing_summary = read_json(source_dir / "data/field_cue_timing_envelope_summary.json")
    transfer_rows = build_spatial_transfer_rows(
        timing_rows,
        spatial_match_threshold_mm=args.spatial_match_threshold_mm,
    )
    summary = summarize(
        transfer_rows,
        timing_summary,
        spatial_match_threshold_mm=args.spatial_match_threshold_mm,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(output_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_spatial_transfer_audit_rows.csv"
    summary_json = data_dir / "field_spatial_transfer_audit_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_spatial_transfer_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in transfer_rows])
    plot_spatial_transfer(transfer_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "source_timing_envelope_rows_csv": str(source_dir / "data/field_cue_timing_envelope_rows.csv"),
        "source_timing_envelope_summary_json": str(source_dir / "data/field_cue_timing_envelope_summary.json"),
        "rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, rows_csv, summary_json)
    write_run_manifest(
        str(outdir),
        "gssi51600s_field_spatial_transfer_audit",
        {
            "timing_envelope_run": args.timing_envelope_run,
            "spatial_match_threshold_mm": args.spatial_match_threshold_mm,
            "dataset_id": args.dataset_id,
            "readgssi_version": readgssi_version(),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

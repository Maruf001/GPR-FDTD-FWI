#!/usr/bin/env python3
"""Overlay field cue/support anchors with the short-pair timing uncertainty envelope."""

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


DEFAULT_TIME_ZERO_BUDGET_RUN = "075_gssi51600s_field_time_zero_uncertainty_budget"
DEFAULT_TIMING_DISCRIMINANT_RUN = "105_gssi51600s_field_timing_discriminant_scorecard"
DEFAULT_CUE_SUPPORT_RUN = "113_gssi51600s_field_cue_support_catalog"


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


def boolish(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def timing_discriminant_lookup(rows: list[dict]) -> dict[str, dict]:
    return {str(row.get("timing_discriminant", "")): row for row in rows}


def envelope_class(row: dict, delta_half_widths: float) -> str:
    family = str(row.get("support_family", ""))
    if family == "short_relative_timing":
        return (
            "short_anchor_inside_conservative_envelope"
            if delta_half_widths <= 1.0
            else "short_anchor_outside_conservative_envelope"
        )
    if family == "long_pattern_only":
        return (
            "long_pattern_rejects_short_transfer"
            if delta_half_widths > 1.0
            else "long_pattern_inside_short_transfer_envelope"
        )
    return "context_only"


def build_anchor_rows(
    support_rows: list[dict],
    timing_rows: list[dict],
    time_zero_summary: dict,
) -> list[dict]:
    short_offset = safe_float(time_zero_summary.get("relative_anchor_offset_ns"))
    half_width = safe_float(time_zero_summary.get("conservative_half_width_ns"))
    discriminants = timing_discriminant_lookup(timing_rows)
    early = discriminants.get("early_common_mode", {})
    long = discriminants.get("long_pattern_only", {})
    out = []
    for row in support_rows:
        offset = safe_float(row.get("offset_ns"))
        delta = offset - short_offset if math.isfinite(offset) and math.isfinite(short_offset) else math.nan
        delta_widths = abs(delta) / half_width if math.isfinite(delta) and half_width > 0.0 else math.nan
        support_family = str(row.get("support_family", ""))
        if support_family == "short_relative_timing":
            discriminant = "short_content_relative"
            transfer_scope = "short_relative_timing_qc"
        elif support_family == "long_pattern_only":
            discriminant = "long_pattern_only"
            transfer_scope = "long_pattern_only_no_short_transfer"
        else:
            discriminant = "context_only"
            transfer_scope = "context_only"
        out.append(
            {
                "support_anchor_id": row.get("support_anchor_id", ""),
                "profile_group": row.get("profile_group", ""),
                "support_family": support_family,
                "support_category": row.get("support_category", ""),
                "support_label": row.get("support_label", ""),
                "is_claim_supporting": boolish(row.get("is_claim_supporting")),
                "anchor_x_mm": safe_float(row.get("anchor_x_mm")),
                "offset_ns": offset,
                "short_content_offset_ns": short_offset,
                "short_content_half_width_ns": half_width,
                "delta_to_short_content_ns": delta,
                "delta_to_short_content_half_widths": delta_widths,
                "timing_envelope_class": envelope_class(row, delta_widths),
                "timing_discriminant": discriminant,
                "transfer_scope": transfer_scope,
                "allowed_use": row.get("allowed_use", ""),
                "blocked_use": row.get("blocked_use", ""),
            }
        )

    # Add aggregate timing discriminants as non-anchor reference rows for manuscript tables.
    for discriminant, row in (("early_common_mode", early), ("long_pattern_only", long)):
        if not row:
            continue
        offset = safe_float(row.get("representative_offset_ns"))
        delta = offset - short_offset if math.isfinite(offset) and math.isfinite(short_offset) else math.nan
        delta_widths = abs(delta) / half_width if math.isfinite(delta) and half_width > 0.0 else math.nan
        out.append(
            {
                "support_anchor_id": f"discriminant_{discriminant}",
                "profile_group": "aggregate_timing_discriminant",
                "support_family": "timing_discriminant_reference",
                "support_category": discriminant,
                "support_label": row.get("strength_label", ""),
                "is_claim_supporting": False,
                "anchor_x_mm": math.nan,
                "offset_ns": offset,
                "short_content_offset_ns": short_offset,
                "short_content_half_width_ns": half_width,
                "delta_to_short_content_ns": delta,
                "delta_to_short_content_half_widths": delta_widths,
                "timing_envelope_class": (
                    "reference_outside_short_envelope"
                    if delta_widths > 1.0
                    else "reference_inside_short_envelope"
                ),
                "timing_discriminant": discriminant,
                "transfer_scope": row.get("allowed_use", ""),
                "allowed_use": row.get("allowed_use", ""),
                "blocked_use": row.get("blocked_use", ""),
            }
        )
    return out


def summarize(anchor_rows: list[dict], time_zero_summary: dict, cue_summary: dict) -> dict:
    short_rows = [row for row in anchor_rows if row["support_family"] == "short_relative_timing"]
    short_content = [row for row in short_rows if row["support_category"] == "short_content_backed_time_zero_anchor"]
    long_rows = [row for row in anchor_rows if row["support_family"] == "long_pattern_only"]
    inside = lambda row: safe_float(row.get("delta_to_short_content_half_widths"), math.inf) <= 1.0
    outside = lambda row: safe_float(row.get("delta_to_short_content_half_widths"), 0.0) > 1.0
    return {
        "policy_label": "gssi51600s_field_cue_timing_envelope_short_relative_qc",
        "support_anchor_row_count": len([row for row in anchor_rows if not str(row["support_anchor_id"]).startswith("discriminant_")]),
        "timing_reference_row_count": len([row for row in anchor_rows if str(row["support_anchor_id"]).startswith("discriminant_")]),
        "short_anchor_count": len(short_rows),
        "short_anchor_inside_envelope_count": sum(inside(row) for row in short_rows),
        "short_content_anchor_count": len(short_content),
        "short_content_anchor_inside_envelope_count": sum(inside(row) for row in short_content),
        "long_pattern_anchor_count": len(long_rows),
        "long_pattern_reject_short_transfer_count": sum(outside(row) for row in long_rows),
        "short_content_offset_ns": safe_float(time_zero_summary.get("relative_anchor_offset_ns")),
        "short_content_half_width_ns": safe_float(time_zero_summary.get("conservative_half_width_ns")),
        "short_content_anchor_support_fraction": safe_float(cue_summary.get("short_content_anchor_support_fraction")),
        "ready_for_short_relative_timing_qc": len(short_content) > 0 and all(inside(row) for row in short_content),
        "ready_for_long_short_transfer": False,
        "ready_for_absolute_time_zero": False,
        "ready_for_cover_depth_recovery": False,
        "ready_for_radius_recovery": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "Use this as a field cue timing-envelope integration for short-pair relative "
            "timing QC. Short content-backed anchors remain inside the conservative envelope, "
            "while long pattern anchors reject transfer of the short-pair correction. This "
            "does not create absolute time-zero, cover-depth, radius, field FWI, 3D, or HPC readiness."
        ),
    }


def plot_envelope(anchor_rows: list[dict], summary: dict, save_path: Path) -> str:
    plot_rows = [
        row for row in anchor_rows
        if row["support_family"] in {"short_relative_timing", "long_pattern_only"}
    ]
    labels = [str(row["support_anchor_id"]).replace("_", "\n") for row in plot_rows]
    values = [safe_float(row["delta_to_short_content_half_widths"], 0.0) for row in plot_rows]
    colors = [
        "#4c9f70" if row["support_family"] == "short_relative_timing" else "#d08a2e"
        for row in plot_rows
    ]
    fig, axes = plt.subplots(1, 2, figsize=(15.2, 5.4), constrained_layout=True)
    x = np.arange(len(plot_rows))
    axes[0].bar(x, values, color=colors, edgecolor="#333333")
    axes[0].axhline(1.0, color="#c7302b", linestyle="--", linewidth=1.2, label="conservative half-width")
    axes[0].set_xticks(x, labels, fontsize=8)
    axes[0].set_ylabel("|delta to short content| / half-width")
    axes[0].set_title("Cue/support timing envelope")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    categories = ["short\ninside", "long\nreject", "absolute\nready", "field\nFWI"]
    counts = [
        summary["short_anchor_inside_envelope_count"],
        summary["long_pattern_reject_short_transfer_count"],
        1 if summary["ready_for_absolute_time_zero"] else 0,
        1 if summary["ready_for_field_fwi"] else 0,
    ]
    axes[1].bar(np.arange(len(categories)), counts, color=["#4c9f70", "#d08a2e", "#c7302b", "#c7302b"])
    axes[1].set_xticks(np.arange(len(categories)), categories)
    axes[1].set_ylabel("count or readiness flag")
    axes[1].set_title("Field timing scope boundary")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.96,
        f"short offset={summary['short_content_offset_ns']:.3f} ns\n"
        f"half-width={summary['short_content_half_width_ns']:.3f} ns\n"
        "field FWI=false",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI 51600S cue timing envelope: short relative QC, not absolute time-zero", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, summary_json: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_cue_timing_envelope.png`",
                "",
                "This figure overlays measured field cue/support anchors with the",
                "short-pair conservative relative time-zero uncertainty envelope.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Short anchors inside envelope: `{summary['short_anchor_inside_envelope_count']}` of `{summary['short_anchor_count']}`.",
                f"Short content-backed anchors inside envelope: `{summary['short_content_anchor_inside_envelope_count']}` of `{summary['short_content_anchor_count']}`.",
                f"Long pattern anchors rejecting short transfer: `{summary['long_pattern_reject_short_transfer_count']}` of `{summary['long_pattern_anchor_count']}`.",
                f"Ready for absolute time-zero: `{summary['ready_for_absolute_time_zero']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Timing-envelope rows: `{rows_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                "",
                "Scope boundary:",
                "",
                "This is measured-field relative timing QC. It does not create",
                "absolute time-zero, cover-depth, radius, field FWI, 3D, or HPC claims.",
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
    parser.add_argument("--time-zero-budget-run", default=DEFAULT_TIME_ZERO_BUDGET_RUN)
    parser.add_argument("--timing-discriminant-run", default=DEFAULT_TIMING_DISCRIMINANT_RUN)
    parser.add_argument("--cue-support-run", default=DEFAULT_CUE_SUPPORT_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_cue_timing_envelope")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    time_zero_summary = read_json(
        dataset_root / args.time_zero_budget_run / "data/field_time_zero_uncertainty_budget_summary.json"
    )
    timing_rows = read_csv_rows(
        dataset_root / args.timing_discriminant_run / "data/field_timing_discriminant_scorecard_rows.csv"
    )
    support_rows = read_csv_rows(
        dataset_root / args.cue_support_run / "data/field_support_anchor_catalog.csv"
    )
    cue_summary = read_json(dataset_root / args.cue_support_run / "data/field_cue_support_catalog_summary.json")
    envelope_rows = build_anchor_rows(support_rows, timing_rows, time_zero_summary)
    summary = summarize(envelope_rows, time_zero_summary, cue_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_cue_timing_envelope_rows.csv"
    summary_json = data_dir / "field_cue_timing_envelope_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_cue_timing_envelope.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in envelope_rows])
    plot_envelope(envelope_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "time_zero_summary_json": str(
            dataset_root / args.time_zero_budget_run / "data/field_time_zero_uncertainty_budget_summary.json"
        ),
        "timing_discriminant_csv": str(
            dataset_root / args.timing_discriminant_run / "data/field_timing_discriminant_scorecard_rows.csv"
        ),
        "support_anchor_csv": str(dataset_root / args.cue_support_run / "data/field_support_anchor_catalog.csv"),
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
        "gssi_field_cue_timing_envelope",
        {
            "dataset_id": args.dataset_id,
            "time_zero_budget_run": args.time_zero_budget_run,
            "timing_discriminant_run": args.timing_discriminant_run,
            "cue_support_run": args.cue_support_run,
            "rows_csv": str(rows_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Refresh the field time-zero evidence ladder with short-anchor leave-one evidence."""

from __future__ import annotations

import argparse
import csv
import json
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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_BASE_LADDER_RUN = "119_gssi51600s_field_time_zero_evidence_ladder"
DEFAULT_SHORT_ANCHOR_LEAVE_ONE_RUN = "120_gssi51600s_field_short_anchor_leave_one_audit"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "supported"}


def gate_row(
    *,
    gate_key: str,
    status: str,
    readiness_score: float,
    evidence: str,
    allowed_use: str,
    blocked_use: str,
) -> dict:
    return {
        "gate_key": gate_key,
        "status": status,
        "readiness_score": float(readiness_score),
        "evidence": evidence,
        "allowed_use": allowed_use,
        "blocked_use": blocked_use,
    }


def build_post_leave_one_rows(base_rows: list[dict], leave_one: dict) -> list[dict]:
    content_supported = boolish(leave_one.get("content_only_supported"))
    leave_one_claim = boolish(leave_one.get("ready_for_leave_one_content_anchor_claim"))
    status = "supported_content_only_not_leave_one_content" if content_supported and not leave_one_claim else "review"
    score = 0.88 if content_supported and not leave_one_claim else 0.45
    extra = gate_row(
        gate_key="short_anchor_content_only_redundancy",
        status=status,
        readiness_score=score,
        evidence=(
            f"content_only={content_supported}; "
            f"content_half_range={safe_float(leave_one.get('content_only_offset_half_range_ns')):.6f} ns; "
            f"all_short_half_range={safe_float(leave_one.get('all_short_offset_half_range_ns')):.6f} ns; "
            f"leave_one_supported={safe_float(leave_one.get('leave_one_supported_count')):.0f}/"
            f"{safe_float(leave_one.get('leave_one_case_count')):.0f}; "
            f"degraded={safe_float(leave_one.get('leave_one_degraded_single_content_count')):.0f}"
        ),
        allowed_use="short-profile relative time-zero QC using content-backed anchors",
        blocked_use="leave-one-content redundancy, absolute time-zero, cover-depth, radius, field FWI, 3D/HPC",
    )
    return [dict(row) for row in base_rows] + [extra]


def summarize_post_leave_one(rows: list[dict], base_summary: dict, leave_one: dict) -> dict:
    content_supported = boolish(leave_one.get("content_only_supported"))
    leave_one_claim = boolish(leave_one.get("ready_for_leave_one_content_anchor_claim"))
    short_ready = boolish(base_summary.get("ready_for_short_relative_timing_qc")) and content_supported
    return {
        "policy_label": "gssi51600s_field_time_zero_evidence_ladder_post_leave_one_short_qc_only",
        "source_ladder_policy_label": base_summary.get("policy_label", ""),
        "short_anchor_leave_one_policy_label": leave_one.get("policy_label", ""),
        "ladder_row_count": len(rows),
        "ready_for_short_relative_timing_qc": bool(short_ready),
        "ready_for_content_only_short_qc": bool(content_supported),
        "ready_for_leave_one_content_anchor_claim": bool(leave_one_claim),
        "ready_for_long_short_transfer": False,
        "ready_for_absolute_time_zero": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "short_relative_offset_ns": safe_float(base_summary.get("short_relative_offset_ns")),
        "short_conservative_half_width_ns": safe_float(base_summary.get("short_conservative_half_width_ns")),
        "content_only_offset_half_range_ns": safe_float(leave_one.get("content_only_offset_half_range_ns")),
        "all_short_offset_half_range_ns": safe_float(leave_one.get("all_short_offset_half_range_ns")),
        "leave_one_supported_count": safe_float(leave_one.get("leave_one_supported_count"), 0.0),
        "leave_one_degraded_single_content_count": safe_float(
            leave_one.get("leave_one_degraded_single_content_count"), 0.0
        ),
        "short_anchor_inside_supported_interval_count": safe_float(
            base_summary.get("short_anchor_inside_supported_interval_count"), 0.0
        ),
        "long_pattern_reject_short_transfer_count": safe_float(
            base_summary.get("long_pattern_reject_short_transfer_count"), 0.0
        ),
        "median_long_to_short_distance_mm": safe_float(base_summary.get("median_long_to_short_distance_mm"), 0.0),
        "gpu_priority": "none",
        "decision": (
            "Use this as the current measured-field time-zero ladder: short-profile relative timing QC "
            "is supported even after dropping the timing-only short anchor, but the evidence is not "
            "leave-one-content redundant and remains blocked for absolute time-zero, field FWI, 3D/HPC, "
            "and calibrated depth/radius recovery."
        ),
    }


def plot_ladder(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [str(row["gate_key"]).replace("_", "\n") for row in rows]
    scores = [safe_float(row["readiness_score"], 0.0) for row in rows]
    colors = ["#2f9d55" if score >= 0.75 else "#d99a19" if score >= 0.35 else "#c7302b" for score in scores]
    fig, axes = plt.subplots(1, 2, figsize=(14.8, 5.2), constrained_layout=True)
    x = np.arange(len(rows))
    axes[0].bar(x, scores, color=colors, edgecolor="#333333", linewidth=0.6)
    axes[0].set_xticks(x, labels, fontsize=7)
    axes[0].set_ylim(0.0, 1.05)
    axes[0].set_ylabel("readiness score")
    axes[0].set_title("Post leave-one field time-zero ladder")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    gate_labels = ["short\nrelative", "content\nonly", "leave-one\ncontent", "absolute\nt0", "field\nFWI", "3D\nHPC"]
    gate_values = [
        summary["ready_for_short_relative_timing_qc"],
        summary["ready_for_content_only_short_qc"],
        summary["ready_for_leave_one_content_anchor_claim"],
        summary["ready_for_absolute_time_zero"],
        summary["ready_for_field_fwi"],
        summary["ready_for_3d_hpc"],
    ]
    axes[1].bar(
        np.arange(len(gate_labels)),
        [1 if value else 0 for value in gate_values],
        color=["#2f9d55" if value else "#c7302b" for value in gate_values],
    )
    axes[1].set_xticks(np.arange(len(gate_labels)), gate_labels, fontsize=9)
    axes[1].set_ylim(0.0, 1.05)
    axes[1].set_title("Claim gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.95,
        f"content half-range={summary['content_only_offset_half_range_ns']:.6f} ns\n"
        f"all-short half-range={summary['all_short_offset_half_range_ns']:.6f} ns\n"
        f"leave-one supported={summary['leave_one_supported_count']:.0f}\n"
        f"degraded={summary['leave_one_degraded_single_content_count']:.0f}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local GSSI field time-zero ladder after leave-one audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_time_zero_ladder_post_leave_one.png`",
                "",
                "This CPU-only figure refreshes the local GSSI time-zero evidence ladder",
                "with the short-anchor leave-one/content-only audit.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Ready for short relative timing QC: `{summary['ready_for_short_relative_timing_qc']}`.",
                f"Ready for content-only short QC: `{summary['ready_for_content_only_short_qc']}`.",
                f"Ready for leave-one-content anchor claim: `{summary['ready_for_leave_one_content_anchor_claim']}`.",
                f"Ready for absolute time-zero: `{summary['ready_for_absolute_time_zero']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                f"Ready for 3D/HPC: `{summary['ready_for_3d_hpc']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Ladder rows: `{rows_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads existing field summaries only. It does not run FDTD, FWI,",
                "GPU kernels, 3D/HPC jobs, or neural-network training.",
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
    parser.add_argument("--base-ladder-run", default=DEFAULT_BASE_LADDER_RUN)
    parser.add_argument("--short-anchor-leave-one-run", default=DEFAULT_SHORT_ANCHOR_LEAVE_ONE_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_time_zero_ladder_post_leave_one")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    base_dir = dataset_root / args.base_ladder_run
    leave_one_dir = dataset_root / args.short_anchor_leave_one_run
    base_rows = read_csv_rows(base_dir / "data/field_time_zero_evidence_ladder_rows.csv")
    base_summary = read_json(base_dir / "data/field_time_zero_evidence_ladder_summary.json")
    leave_one_summary = read_json(leave_one_dir / "data/field_short_anchor_leave_one_summary.json")
    rows = build_post_leave_one_rows(base_rows, leave_one_summary)
    summary = summarize_post_leave_one(rows, base_summary, leave_one_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_time_zero_evidence_ladder_rows.csv"
    summary_json = data_dir / "field_time_zero_evidence_ladder_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_time_zero_ladder_post_leave_one.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    plot_ladder(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "source_ladder_summary_json": str(base_dir / "data/field_time_zero_evidence_ladder_summary.json"),
        "short_anchor_leave_one_summary_json": str(
            leave_one_dir / "data/field_short_anchor_leave_one_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, rows_csv)
    write_run_manifest(
        str(outdir),
        "gssi_field_time_zero_ladder_post_leave_one",
        {
            "base_ladder_run": args.base_ladder_run,
            "short_anchor_leave_one_run": args.short_anchor_leave_one_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

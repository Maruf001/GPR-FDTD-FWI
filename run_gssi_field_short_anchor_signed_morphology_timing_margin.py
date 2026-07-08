#!/usr/bin/env python3
"""Compare signed-morphology timing slack with field time-zero uncertainty."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_TIME_ZERO_LADDER_RUN = "121_gssi51600s_field_time_zero_ladder_post_leave_one"
DEFAULT_SIGNED_MORPHOLOGY_RUN = "126_gssi51600s_field_short_anchor_signed_morphology_audit"
DEFAULT_SIGNED_SENSITIVITY_RUN = "127_gssi51600s_field_short_anchor_signed_morphology_sensitivity"
DEFAULT_TIMING_CAP_NS = 0.05
DEFAULT_MODERATE_TIMING_CAP_NS = 0.02


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "supported"}


def _finite(values: list[float]) -> list[float]:
    return [value for value in values if math.isfinite(value)]


def build_timing_margin_rows(
    signed_rows: list[dict],
    ladder_summary: dict,
    *,
    timing_cap_ns: float = DEFAULT_TIMING_CAP_NS,
    moderate_timing_cap_ns: float = DEFAULT_MODERATE_TIMING_CAP_NS,
) -> list[dict]:
    content_half_range = safe_float(ladder_summary.get("content_only_offset_half_range_ns"))
    conservative_half_width = safe_float(ladder_summary.get("short_conservative_half_width_ns"))
    rows: list[dict] = []
    for row in signed_rows:
        residual = abs(safe_float(row.get("corrected_abs_timing_residual_ns")))
        default_slack = timing_cap_ns - residual
        moderate_slack = moderate_timing_cap_ns - residual
        rows.append(
            {
                "pair_index": int(safe_float(row.get("pair_index"), -1)),
                "reference_file": row.get("reference_file", ""),
                "comparison_file": row.get("comparison_file", ""),
                "corrected_abs_timing_residual_ns": residual,
                "default_timing_cap_ns": timing_cap_ns,
                "default_timing_slack_ns": default_slack,
                "moderate_timing_cap_ns": moderate_timing_cap_ns,
                "moderate_timing_slack_ns": moderate_slack,
                "content_only_offset_half_range_ns": content_half_range,
                "short_conservative_half_width_ns": conservative_half_width,
                "default_slack_covers_content_uncertainty": default_slack >= content_half_range,
                "default_slack_covers_conservative_uncertainty": default_slack >= conservative_half_width,
                "moderate_slack_covers_content_uncertainty": moderate_slack >= content_half_range,
                "signed_morphology_supported": boolish(row.get("signed_morphology_supported")),
                "allowed_use": "short-profile content-only timing margin for signed morphology QC",
                "blocked_use": "absolute time-zero, conservative timing claim, field FWI, 3D/HPC",
            }
        )
    return sorted(rows, key=lambda item: item["pair_index"])


def summarize_timing_margin(
    rows: list[dict],
    ladder_summary: dict,
    signed_summary: dict,
    sensitivity_summary: dict,
) -> dict:
    default_slacks = _finite([safe_float(row.get("default_timing_slack_ns")) for row in rows])
    moderate_slacks = _finite([safe_float(row.get("moderate_timing_slack_ns")) for row in rows])
    residuals = _finite([safe_float(row.get("corrected_abs_timing_residual_ns")) for row in rows])
    content_ready_count = sum(1 for row in rows if boolish(row.get("default_slack_covers_content_uncertainty")))
    conservative_ready_count = sum(1 for row in rows if boolish(row.get("default_slack_covers_conservative_uncertainty")))
    moderate_content_ready_count = sum(1 for row in rows if boolish(row.get("moderate_slack_covers_content_uncertainty")))
    signed_supported_count = sum(1 for row in rows if boolish(row.get("signed_morphology_supported")))
    all_pairs = len(rows)
    all_content_ready = all_pairs > 0 and content_ready_count == all_pairs
    all_conservative_ready = all_pairs > 0 and conservative_ready_count == all_pairs
    all_moderate_content_ready = all_pairs > 0 and moderate_content_ready_count == all_pairs
    return {
        "policy_label": "gssi51600s_field_short_anchor_signed_morphology_timing_margin_qc_only",
        "source_time_zero_ladder_policy_label": ladder_summary.get("policy_label", ""),
        "source_signed_morphology_policy_label": signed_summary.get("policy_label", ""),
        "source_signed_sensitivity_policy_label": sensitivity_summary.get("policy_label", ""),
        "content_pair_count": all_pairs,
        "signed_morphology_supported_pair_count": signed_supported_count,
        "default_timing_cap_ns": safe_float(rows[0].get("default_timing_cap_ns")) if rows else math.nan,
        "moderate_timing_cap_ns": safe_float(rows[0].get("moderate_timing_cap_ns")) if rows else math.nan,
        "max_corrected_abs_timing_residual_ns": max(residuals) if residuals else math.nan,
        "min_default_timing_slack_ns": min(default_slacks) if default_slacks else math.nan,
        "min_moderate_timing_slack_ns": min(moderate_slacks) if moderate_slacks else math.nan,
        "content_only_offset_half_range_ns": safe_float(ladder_summary.get("content_only_offset_half_range_ns")),
        "short_conservative_half_width_ns": safe_float(ladder_summary.get("short_conservative_half_width_ns")),
        "source_support_limit_timing_cap_ns": safe_float(sensitivity_summary.get("support_limit_timing_cap_ns")),
        "default_slack_content_covered_pair_count": content_ready_count,
        "default_slack_conservative_covered_pair_count": conservative_ready_count,
        "moderate_slack_content_covered_pair_count": moderate_content_ready_count,
        "ready_for_content_only_morphology_timing_qc": all_content_ready,
        "ready_for_conservative_timing_morphology_claim": all_conservative_ready,
        "ready_for_moderate_timing_morphology_margin": all_moderate_content_ready,
        "ready_for_absolute_time_zero": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "ready_for_heavy_field_work": False,
        "gpu_priority": "none",
        "decision": (
            "The signed short-anchor morphology has enough default timing-cap slack to cover the "
            "content-only short-profile time-zero half-range, but not the conservative all-short timing "
            "half-width. Treat this as content-only timing-margin support for field morphology QC, not "
            "absolute time-zero, conservative timing, field FWI, 3D/HPC, or heavy field-work evidence."
        ),
    }


def build_gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "content_only_morphology_timing_qc",
            "ready": summary["ready_for_content_only_morphology_timing_qc"],
            "allowed_use": "field supplement content-only timing-margin support for signed morphology QC",
            "blocked_use": "absolute time-zero or conservative timing claim",
            "evidence": (
                f"min default slack={summary['min_default_timing_slack_ns']:.6f} ns; "
                f"content half-range={summary['content_only_offset_half_range_ns']:.6f} ns"
            ),
        },
        {
            "gate_key": "conservative_timing_morphology_claim",
            "ready": summary["ready_for_conservative_timing_morphology_claim"],
            "allowed_use": "none",
            "blocked_use": "conservative all-short timing morphology claim",
            "evidence": (
                f"min default slack={summary['min_default_timing_slack_ns']:.6f} ns; "
                f"conservative half-width={summary['short_conservative_half_width_ns']:.6f} ns"
            ),
        },
        {
            "gate_key": "moderate_timing_morphology_margin",
            "ready": summary["ready_for_moderate_timing_morphology_margin"],
            "allowed_use": "none" if not summary["ready_for_moderate_timing_morphology_margin"] else "strict timing-margin context",
            "blocked_use": "strict or conservative timing-margin claim",
            "evidence": f"min moderate slack={summary['min_moderate_timing_slack_ns']:.6f} ns",
        },
        {
            "gate_key": "absolute_time_zero",
            "ready": summary["ready_for_absolute_time_zero"],
            "allowed_use": "none",
            "blocked_use": "absolute field time-zero",
            "evidence": "field ladder still supports relative short-profile timing QC only",
        },
        {
            "gate_key": "field_fwi",
            "ready": summary["ready_for_field_fwi"],
            "allowed_use": "none",
            "blocked_use": "field FWI, 3D/HPC, or heavy field work",
            "evidence": "timing-margin support is not an inversion launch contract",
        },
    ]


def plot_timing_margin(rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), constrained_layout=True)
    labels = [f"pair {row['pair_index']}" for row in rows]
    x = np.arange(len(rows), dtype=float)
    width = 0.35
    axes[0].bar(
        x - width / 2,
        [safe_float(row.get("default_timing_slack_ns")) for row in rows],
        width=width,
        color="#4c72b0",
        label="default cap slack",
    )
    axes[0].bar(
        x + width / 2,
        [safe_float(row.get("moderate_timing_slack_ns")) for row in rows],
        width=width,
        color="#dd8452",
        label="moderate cap slack",
    )
    axes[0].axhline(summary["content_only_offset_half_range_ns"], color="#55a868", linestyle="--", linewidth=0.9)
    axes[0].axhline(summary["short_conservative_half_width_ns"], color="#c44e52", linestyle="--", linewidth=0.9)
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel("timing slack (ns)")
    axes[0].set_title("Signed morphology timing slack")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    gate_labels = ["content\nonly", "conservative", "moderate", "absolute\nt0", "field\nFWI"]
    gate_values = [
        summary["ready_for_content_only_morphology_timing_qc"],
        summary["ready_for_conservative_timing_morphology_claim"],
        summary["ready_for_moderate_timing_morphology_margin"],
        summary["ready_for_absolute_time_zero"],
        summary["ready_for_field_fwi"],
    ]
    colors = ["#59a14f" if value else "#bab0ac" for value in gate_values]
    axes[1].bar(np.arange(len(gate_labels)), [1 if value else 0 for value in gate_values], color=colors)
    axes[1].set_xticks(np.arange(len(gate_labels)), gate_labels)
    axes[1].set_ylim(0, 1.15)
    axes[1].set_yticks([0, 1], ["blocked", "ready"])
    axes[1].set_title("Timing-margin gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.05,
        0.08,
        f"min default slack: {summary['min_default_timing_slack_ns']:.6f} ns\n"
        f"content half-range: {summary['content_only_offset_half_range_ns']:.6f} ns\n"
        f"conservative half-width: {summary['short_conservative_half_width_ns']:.6f} ns\n"
        f"ready for field FWI: {summary['ready_for_field_fwi']}",
        transform=axes[1].transAxes,
        va="bottom",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI 51600s signed morphology timing-margin audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_short_anchor_signed_morphology_timing_margin.png`",
                "",
                "This CPU-only figure compares signed short-anchor morphology timing slack against",
                "the measured-field time-zero uncertainty ladder.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Content pairs: `{summary['content_pair_count']}`.",
                f"Minimum default timing slack: `{summary['min_default_timing_slack_ns']}` ns.",
                f"Content-only half-range: `{summary['content_only_offset_half_range_ns']}` ns.",
                f"Conservative short half-width: `{summary['short_conservative_half_width_ns']}` ns.",
                f"Ready for content-only morphology timing QC: `{summary['ready_for_content_only_morphology_timing_qc']}`.",
                f"Ready for conservative timing morphology claim: `{summary['ready_for_conservative_timing_morphology_claim']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                "",
                "Outputs:",
                "",
                f"- Timing margin rows: `{rows_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved field QC tables only. It does not run FDTD, FWI, GPU kernels,",
                "3D/HPC jobs, or neural-network training.",
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
    parser.add_argument("--time-zero-ladder-run", default=DEFAULT_TIME_ZERO_LADDER_RUN)
    parser.add_argument("--signed-morphology-run", default=DEFAULT_SIGNED_MORPHOLOGY_RUN)
    parser.add_argument("--signed-sensitivity-run", default=DEFAULT_SIGNED_SENSITIVITY_RUN)
    parser.add_argument("--timing-cap-ns", type=float, default=DEFAULT_TIMING_CAP_NS)
    parser.add_argument("--moderate-timing-cap-ns", type=float, default=DEFAULT_MODERATE_TIMING_CAP_NS)
    parser.add_argument("--run-name", default="gssi51600s_field_short_anchor_signed_morphology_timing_margin")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    field_root = field_dataset_output_root(args.field_root, args.dataset_id)
    ladder_dir = field_root / args.time_zero_ladder_run
    signed_dir = field_root / args.signed_morphology_run
    sensitivity_dir = field_root / args.signed_sensitivity_run

    ladder_summary = read_json(ladder_dir / "data/field_time_zero_evidence_ladder_summary.json")
    signed_summary = read_json(signed_dir / "data/field_short_anchor_signed_morphology_summary.json")
    sensitivity_summary = read_json(
        sensitivity_dir / "data/field_short_anchor_signed_morphology_sensitivity_summary.json"
    )
    signed_rows = read_csv_rows(signed_dir / "data/field_short_anchor_signed_morphology_rows.csv")

    rows = build_timing_margin_rows(
        signed_rows,
        ladder_summary,
        timing_cap_ns=args.timing_cap_ns,
        moderate_timing_cap_ns=args.moderate_timing_cap_ns,
    )
    summary = summarize_timing_margin(rows, ladder_summary, signed_summary, sensitivity_summary)
    gates = build_gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=field_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_short_anchor_signed_morphology_timing_margin_rows.csv"
    gates_csv = data_dir / "field_short_anchor_signed_morphology_timing_margin_gates.csv"
    summary_json = data_dir / "field_short_anchor_signed_morphology_timing_margin_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_short_anchor_signed_morphology_timing_margin.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_timing_margin(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, rows_csv)
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "source_time_zero_ladder_summary_json": str(ladder_dir / "data/field_time_zero_evidence_ladder_summary.json"),
        "source_signed_morphology_summary_json": str(
            signed_dir / "data/field_short_anchor_signed_morphology_summary.json"
        ),
        "source_signed_morphology_rows_csv": str(signed_dir / "data/field_short_anchor_signed_morphology_rows.csv"),
        "source_signed_sensitivity_summary_json": str(
            sensitivity_dir / "data/field_short_anchor_signed_morphology_sensitivity_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi51600s_field_short_anchor_signed_morphology_timing_margin",
        {
            "dataset_id": args.dataset_id,
            "time_zero_ladder_run": args.time_zero_ladder_run,
            "signed_morphology_run": args.signed_morphology_run,
            "signed_sensitivity_run": args.signed_sensitivity_run,
            "summary_json": str(summary_json),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

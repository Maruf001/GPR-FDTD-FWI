#!/usr/bin/env python3
"""Synthesize field timing-anchor conflicts from existing GSSI QC outputs."""

from __future__ import annotations

import argparse
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
DEFAULT_TIME_ZERO_PERTURBATION_RUN = "078_gssi51600s_field_time_zero_perturbation_sensitivity"
DEFAULT_EARLY_TIME_ANCHOR_RUN = "090_gssi51600s_field_early_time_anchor_audit"
DEFAULT_LONG_SHIFT_SENSITIVITY_RUN = "055_gssi51600s_long_profile_shift_scan_sensitivity"
DEFAULT_ACQUISITION_READINESS_RUN = "081_gssi51600s_field_acquisition_readiness_audit"
DEFAULT_APPARENT_DEPTH_QC_RUN = "084_gssi51600s_field_apparent_depth_qc"
DEFAULT_HYPERBOLA_TIMEZERO_DEGENERACY_RUN = "086_gssi51600s_field_hyperbola_timezero_degeneracy_audit"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def load_summaries(dataset_root: Path, runs: dict[str, str]) -> dict[str, dict]:
    return {
        "time_zero_budget": read_json(
            dataset_root
            / runs["time_zero_budget"]
            / "data"
            / "field_time_zero_uncertainty_budget_summary.json"
        ),
        "time_zero_perturbation": read_json(
            dataset_root
            / runs["time_zero_perturbation"]
            / "data"
            / "field_time_zero_perturbation_sensitivity_summary.json"
        ),
        "early_time_anchor": read_json(
            dataset_root
            / runs["early_time_anchor"]
            / "data"
            / "field_early_time_anchor_audit_summary.json"
        ),
        "long_shift_sensitivity": read_json(
            dataset_root
            / runs["long_shift_sensitivity"]
            / "data"
            / "long_profile_shift_scan_sensitivity_summary.json"
        ),
        "acquisition_readiness": read_json(
            dataset_root
            / runs["acquisition_readiness"]
            / "data"
            / "field_acquisition_readiness_summary.json"
        ),
        "apparent_depth_qc": read_json(
            dataset_root
            / runs["apparent_depth_qc"]
            / "data"
            / "field_apparent_depth_qc_summary.json"
        ),
        "hyperbola_timezero_degeneracy": read_json(
            dataset_root
            / runs["hyperbola_timezero_degeneracy"]
            / "data"
            / "field_hyperbola_timezero_degeneracy_summary.json"
        ),
    }


def anchor_rows(summaries: dict[str, dict]) -> list[dict]:
    time_zero = summaries["time_zero_budget"]
    perturbation = summaries["time_zero_perturbation"]
    early = summaries["early_time_anchor"]
    long_shift = summaries["long_shift_sensitivity"]

    short_offset = safe_float(time_zero.get("relative_anchor_offset_ns"))
    half_width = safe_float(time_zero.get("conservative_half_width_ns"))
    early_offset = safe_float(early.get("short_pair_early_shift_ns"))
    long_offset = safe_float(long_shift.get("best_offset_median_ns"))
    bootstrap_lower = safe_float(time_zero.get("bootstrap_ci_lower_ns"))
    bootstrap_upper = safe_float(time_zero.get("bootstrap_ci_upper_ns"))
    conservative_lower = short_offset - half_width
    conservative_upper = short_offset + half_width

    def delta_to_short(offset: float) -> float:
        return abs(offset - short_offset) if math.isfinite(offset) and math.isfinite(short_offset) else math.nan

    def half_width_units(delta: float) -> float:
        return delta / half_width if math.isfinite(delta) and math.isfinite(half_width) and half_width > 0 else math.nan

    early_delta = delta_to_short(early_offset)
    long_delta = delta_to_short(long_offset)
    long_early_delta = abs(long_offset - early_offset)
    return [
        {
            "anchor_source": "short_content_backed_relative_time_zero",
            "pair_scope": "short_014_016",
            "offset_ns": short_offset,
            "uncertainty_half_width_ns": half_width,
            "delta_to_short_content_ns": 0.0,
            "delta_to_short_content_half_widths": 0.0,
            "delta_to_early_common_mode_ns": delta_to_short(early_offset),
            "support_status": "relative_time_zero_supported_not_absolute",
            "allowed_use": "short-pair measured relative timing and uncertainty budget",
            "not_allowed": "absolute time-zero, cover-depth, radius, field FWI, or 3D inversion",
        },
        {
            "anchor_source": "early_common_mode_direct_ringdown",
            "pair_scope": "short_014_016_and_long_015_013",
            "offset_ns": early_offset,
            "uncertainty_half_width_ns": half_width,
            "delta_to_short_content_ns": early_delta,
            "delta_to_short_content_half_widths": half_width_units(early_delta),
            "delta_to_early_common_mode_ns": 0.0,
            "support_status": "common_mode_negative_control_conflicts_with_content_timing",
            "allowed_use": "instrument/common-mode repeatability negative control",
            "not_allowed": "absolute time-zero calibration or replacement for content-backed timing",
        },
        {
            "anchor_source": "long_pattern_only_shift",
            "pair_scope": "long_015_013",
            "offset_ns": long_offset,
            "uncertainty_half_width_ns": half_width,
            "delta_to_short_content_ns": long_delta,
            "delta_to_short_content_half_widths": half_width_units(long_delta),
            "delta_to_early_common_mode_ns": long_early_delta,
            "support_status": "pattern_only_stable_rejects_short_transfer",
            "allowed_use": "long-profile pattern-only visual QC",
            "not_allowed": "phase anchor, absolute time-zero, field FWI, or 3D inversion",
        },
        {
            "anchor_source": "bootstrap_ci_lower",
            "pair_scope": "short_014_016",
            "offset_ns": bootstrap_lower,
            "uncertainty_half_width_ns": half_width,
            "delta_to_short_content_ns": delta_to_short(bootstrap_lower),
            "delta_to_short_content_half_widths": half_width_units(delta_to_short(bootstrap_lower)),
            "delta_to_early_common_mode_ns": abs(bootstrap_lower - early_offset),
            "support_status": "bootstrap_ci_supported",
            "allowed_use": "lower uncertainty bound for short-pair relative timing",
            "not_allowed": "absolute time-zero calibration",
        },
        {
            "anchor_source": "bootstrap_ci_upper",
            "pair_scope": "short_014_016",
            "offset_ns": bootstrap_upper,
            "uncertainty_half_width_ns": half_width,
            "delta_to_short_content_ns": delta_to_short(bootstrap_upper),
            "delta_to_short_content_half_widths": half_width_units(delta_to_short(bootstrap_upper)),
            "delta_to_early_common_mode_ns": abs(bootstrap_upper - early_offset),
            "support_status": "bootstrap_ci_supported",
            "allowed_use": "upper uncertainty bound for short-pair relative timing",
            "not_allowed": "absolute time-zero calibration",
        },
        {
            "anchor_source": "conservative_lower",
            "pair_scope": "short_014_016",
            "offset_ns": conservative_lower,
            "uncertainty_half_width_ns": half_width,
            "delta_to_short_content_ns": half_width,
            "delta_to_short_content_half_widths": 1.0,
            "delta_to_early_common_mode_ns": abs(conservative_lower - early_offset),
            "support_status": (
                "conservative_envelope_supported"
                if safe_float(perturbation.get("conservative_supported_count")) > 0
                else "conservative_envelope_review"
            ),
            "allowed_use": "lower conservative stress bound for short-pair relative timing",
            "not_allowed": "absolute time-zero calibration",
        },
        {
            "anchor_source": "conservative_upper",
            "pair_scope": "short_014_016",
            "offset_ns": conservative_upper,
            "uncertainty_half_width_ns": half_width,
            "delta_to_short_content_ns": half_width,
            "delta_to_short_content_half_widths": 1.0,
            "delta_to_early_common_mode_ns": abs(conservative_upper - early_offset),
            "support_status": (
                "conservative_envelope_supported"
                if safe_float(perturbation.get("conservative_supported_count")) > 0
                else "conservative_envelope_review"
            ),
            "allowed_use": "upper conservative stress bound for short-pair relative timing",
            "not_allowed": "absolute time-zero calibration",
        },
    ]


def guardrail_rows(summaries: dict[str, dict]) -> list[dict]:
    time_zero = summaries["time_zero_budget"]
    perturbation = summaries["time_zero_perturbation"]
    early = summaries["early_time_anchor"]
    long_shift = summaries["long_shift_sensitivity"]
    acquisition = summaries["acquisition_readiness"]
    apparent_depth = summaries["apparent_depth_qc"]
    hyperbola = summaries["hyperbola_timezero_degeneracy"]
    return [
        {
            "guardrail": "time_zero_budget",
            "metric": "conservative_half_width_ns",
            "value": safe_float(time_zero.get("conservative_half_width_ns")),
            "status": time_zero.get("policy_label", ""),
            "claim_boundary": "relative short-pair QC only",
        },
        {
            "guardrail": "perturbation_robustness",
            "metric": "bootstrap_ci_supported_count",
            "value": safe_float(perturbation.get("bootstrap_ci_supported_count")),
            "status": perturbation.get("policy_label", ""),
            "claim_boundary": "uncertainty stress test only",
        },
        {
            "guardrail": "early_time_negative_control",
            "metric": "short_pair_early_agrees_with_content_budget",
            "value": 1.0 if early.get("short_pair_early_agrees_with_content_budget", False) else 0.0,
            "status": early.get("policy_label", ""),
            "claim_boundary": "common-mode is not absolute time-zero",
        },
        {
            "guardrail": "long_pattern_shift",
            "metric": "reject_short_transfer_window_count",
            "value": safe_float(long_shift.get("reject_short_transfer_window_count")),
            "status": long_shift.get("policy_label", ""),
            "claim_boundary": "long pair remains pattern-only",
        },
        {
            "guardrail": "acquisition_readiness",
            "metric": "ready_for_field_fwi",
            "value": 1.0 if acquisition.get("ready_for_field_fwi", False) else 0.0,
            "status": acquisition.get("policy_label", ""),
            "claim_boundary": "field FWI and 3D remain blocked",
        },
        {
            "guardrail": "apparent_depth_qc",
            "metric": "ready_for_cover_depth_recovery",
            "value": 1.0 if apparent_depth.get("ready_for_cover_depth_recovery", False) else 0.0,
            "status": apparent_depth.get("policy_label", ""),
            "claim_boundary": "relative depth-scale QC only",
        },
        {
            "guardrail": "hyperbola_timezero_degeneracy",
            "metric": "field_fwi_ready",
            "value": 1.0 if hyperbola.get("field_fwi_ready", False) else 0.0,
            "status": hyperbola.get("policy_label", ""),
            "claim_boundary": "score degeneracy blocks calibrated inversion",
        },
    ]


def claim_boundary_rows() -> list[dict]:
    return [
        {
            "claim_area": "field_timing_anchor_conflict",
            "allowed_claim": (
                "Use the synthesis to show that short content-backed relative timing, "
                "early/common-mode timing, and long-profile pattern timing are distinct "
                "field QC anchors with different scopes."
            ),
            "not_allowed": (
                "Do not average or reconcile these anchors into one absolute time-zero, "
                "cover-depth, radius, field FWI, or 3D inversion claim."
            ),
        },
        {
            "claim_area": "field_short_relative_time_zero",
            "allowed_claim": "Use the short 014/016 content-backed offset as relative timing QC with uncertainty bounds.",
            "not_allowed": "Do not use it as absolute time-zero calibration or transfer it to the long pair.",
        },
        {
            "claim_area": "field_early_time_negative_control",
            "allowed_claim": "Use the early/direct component as common-mode negative-control evidence.",
            "not_allowed": "Do not use the early/direct component as content-backed timing or absolute time-zero.",
        },
        {
            "claim_area": "field_long_pattern_only",
            "allowed_claim": "Use the +0.06 ns long-pair offset as pattern-only visual QC.",
            "not_allowed": "Do not call the long-pair offset a phase anchor, transferable time-zero, or inversion result.",
        },
    ]


def summarize_conflict(rows: list[dict], guardrails: list[dict], summaries: dict[str, dict]) -> dict:
    by_source = {row["anchor_source"]: row for row in rows}
    time_zero = summaries["time_zero_budget"]
    perturbation = summaries["time_zero_perturbation"]
    early = summaries["early_time_anchor"]
    long_shift = summaries["long_shift_sensitivity"]
    acquisition = summaries["acquisition_readiness"]
    apparent_depth = summaries["apparent_depth_qc"]
    hyperbola = summaries["hyperbola_timezero_degeneracy"]

    early_delta_widths = safe_float(
        by_source["early_common_mode_direct_ringdown"].get("delta_to_short_content_half_widths")
    )
    long_delta_widths = safe_float(
        by_source["long_pattern_only_shift"].get("delta_to_short_content_half_widths")
    )
    perturbation_ready = (
        safe_float(perturbation.get("bootstrap_ci_supported_count"))
        == safe_float(perturbation.get("bootstrap_ci_row_count"))
        and safe_float(perturbation.get("conservative_supported_count"))
        == safe_float(perturbation.get("conservative_row_count"))
    )
    long_rejects_short = safe_float(long_shift.get("reject_short_transfer_window_count")) == safe_float(
        long_shift.get("window_count")
    )
    absolute_ready = any(
        bool(summary.get("absolute_time_zero_ready", False))
        for summary in (time_zero, early)
    )
    field_fwi_ready = any(
        bool(summary.get("field_fwi_ready", False) or summary.get("ready_for_field_fwi", False))
        for summary in (time_zero, perturbation, early, acquisition, apparent_depth, hyperbola)
    )
    return {
        "policy_label": "field_timing_anchor_conflict_short_relative_not_absolute",
        "anchor_row_count": len(rows),
        "guardrail_row_count": len(guardrails),
        "claim_boundary_count": len(claim_boundary_rows()),
        "short_content_offset_ns": safe_float(time_zero.get("relative_anchor_offset_ns")),
        "short_content_half_width_ns": safe_float(time_zero.get("conservative_half_width_ns")),
        "early_common_mode_shift_ns": safe_float(early.get("short_pair_early_shift_ns")),
        "long_pattern_offset_ns": safe_float(long_shift.get("best_offset_median_ns")),
        "early_vs_short_delta_ns": safe_float(
            by_source["early_common_mode_direct_ringdown"].get("delta_to_short_content_ns")
        ),
        "early_vs_short_delta_half_widths": early_delta_widths,
        "long_vs_short_delta_ns": safe_float(
            by_source["long_pattern_only_shift"].get("delta_to_short_content_ns")
        ),
        "long_vs_short_delta_half_widths": long_delta_widths,
        "long_vs_early_delta_ns": safe_float(
            by_source["long_pattern_only_shift"].get("delta_to_early_common_mode_ns")
        ),
        "early_agrees_with_content_budget": bool(early.get("short_pair_early_agrees_with_content_budget", False)),
        "long_pattern_rejects_short_transfer_all_windows": long_rejects_short,
        "perturbation_budget_supported": perturbation_ready,
        "field_2d_qc_ready": bool(acquisition.get("ready_for_2d_qc", False)),
        "absolute_time_zero_ready": absolute_ready,
        "cover_depth_ready": bool(apparent_depth.get("ready_for_cover_depth_recovery", False)),
        "radius_ready": bool(hyperbola.get("radius_claim_ready", False)),
        "field_fwi_ready": field_fwi_ready,
        "ready_for_manuscript_field_timing_boundary": (
            not absolute_ready
            and not field_fwi_ready
            and not bool(early.get("short_pair_early_agrees_with_content_budget", False))
            and long_rejects_short
            and perturbation_ready
        ),
        "gpu_priority": "none",
        "decision": (
            "Use this synthesis to keep field timing anchors separated: short 014/016 "
            "content-backed timing is relative QC with uncertainty bounds, early/direct "
            "timing is common-mode negative control, and long 015/013 timing is "
            "pattern-only visual QC. Do not convert these into absolute time-zero, "
            "cover-depth, radius, field FWI, or 3D claims."
        ),
    }


def plot_conflict(rows: list[dict], guardrails: list[dict], summary: dict, save_path: Path) -> str:
    anchor_rows_for_plot = [
        row for row in rows
        if row["anchor_source"] in {
            "early_common_mode_direct_ringdown",
            "long_pattern_only_shift",
            "short_content_backed_relative_time_zero",
        }
    ]
    labels = [row["anchor_source"].replace("_", "\n") for row in anchor_rows_for_plot]
    offsets = np.asarray([safe_float(row["offset_ns"], 0.0) for row in anchor_rows_for_plot], dtype=np.float64)
    half_width = safe_float(summary.get("short_content_half_width_ns"), 0.0)
    guard_labels = [row["guardrail"].replace("_", "\n") for row in guardrails]
    guard_values = np.asarray([safe_float(row["value"], 0.0) for row in guardrails], dtype=np.float64)

    fig, axes = plt.subplots(1, 2, figsize=(14.8, 5.2), constrained_layout=True)
    x = np.arange(len(labels))
    axes[0].bar(x, offsets, color=["#6b6b6b", "#4c78a8", "#2f9d55"], width=0.58)
    axes[0].axhline(0.0, color="#333333", linewidth=0.8)
    short_offset = safe_float(summary.get("short_content_offset_ns"), 0.0)
    axes[0].axhspan(
        short_offset - half_width,
        short_offset + half_width,
        color="#2f9d55",
        alpha=0.16,
        label="short-pair conservative band",
    )
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel("comparison-minus-reference offset [ns]")
    axes[0].set_title("Field timing anchors are not interchangeable")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    gx = np.arange(len(guard_labels))
    colors = ["#2f9d55" if value > 0 else "#c7302b" for value in guard_values]
    axes[1].bar(gx, guard_values, color=colors, width=0.58)
    axes[1].set_xticks(gx, guard_labels)
    axes[1].set_ylabel("guardrail metric value")
    axes[1].set_title("Claim blockers remain active")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.95,
        f"absolute_t0={summary['absolute_time_zero_ready']} | field_fwi={summary['field_fwi_ready']} | gpu={summary['gpu_priority']}",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        fontsize=9,
    )
    fig.suptitle(f"GSSI 51600S timing-anchor conflict synthesis: {summary['policy_label']}", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--time-zero-budget-run", default=DEFAULT_TIME_ZERO_BUDGET_RUN)
    parser.add_argument("--time-zero-perturbation-run", default=DEFAULT_TIME_ZERO_PERTURBATION_RUN)
    parser.add_argument("--early-time-anchor-run", default=DEFAULT_EARLY_TIME_ANCHOR_RUN)
    parser.add_argument("--long-shift-sensitivity-run", default=DEFAULT_LONG_SHIFT_SENSITIVITY_RUN)
    parser.add_argument("--acquisition-readiness-run", default=DEFAULT_ACQUISITION_READINESS_RUN)
    parser.add_argument("--apparent-depth-qc-run", default=DEFAULT_APPARENT_DEPTH_QC_RUN)
    parser.add_argument("--hyperbola-timezero-degeneracy-run", default=DEFAULT_HYPERBOLA_TIMEZERO_DEGENERACY_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_timing_anchor_conflict_synthesis")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    runs = {
        "time_zero_budget": args.time_zero_budget_run,
        "time_zero_perturbation": args.time_zero_perturbation_run,
        "early_time_anchor": args.early_time_anchor_run,
        "long_shift_sensitivity": args.long_shift_sensitivity_run,
        "acquisition_readiness": args.acquisition_readiness_run,
        "apparent_depth_qc": args.apparent_depth_qc_run,
        "hyperbola_timezero_degeneracy": args.hyperbola_timezero_degeneracy_run,
    }
    summaries = load_summaries(dataset_root, runs)
    anchors = anchor_rows(summaries)
    guardrails = guardrail_rows(summaries)
    claims = claim_boundary_rows()
    summary = summarize_conflict(anchors, guardrails, summaries)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    anchor_csv = data_dir / "field_timing_anchor_conflict_rows.csv"
    guardrail_csv = data_dir / "field_timing_anchor_guardrail_rows.csv"
    claims_csv = data_dir / "field_timing_anchor_claim_boundaries.csv"
    summary_json = data_dir / "field_timing_anchor_conflict_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_conflict(anchors, guardrails, summary, figures_dir / "field_timing_anchor_conflict.png"))

    write_csv(anchor_csv, [json_safe(row) for row in anchors])
    write_csv(guardrail_csv, [json_safe(row) for row in guardrails])
    write_csv(claims_csv, [json_safe(row) for row in claims])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "runs": runs,
        **summary,
        "paths": {
            "anchor_rows_csv": str(anchor_csv),
            "guardrail_rows_csv": str(guardrail_csv),
            "claim_boundaries_csv": str(claims_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
        "readgssi_version": readgssi_version(),
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_timing_anchor_conflict_synthesis",
        {
            "summary_json": str(summary_json),
            "anchor_rows_csv": str(anchor_csv),
            "guardrail_rows_csv": str(guardrail_csv),
            "claim_boundaries_csv": str(claims_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

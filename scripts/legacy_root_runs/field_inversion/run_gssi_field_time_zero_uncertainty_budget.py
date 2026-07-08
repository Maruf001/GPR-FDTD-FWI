#!/usr/bin/env python3
"""Synthesize a relative time-zero uncertainty budget for local GSSI field QC."""

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
from run_gssi_field_corrected_profile_stack import safe_float  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_TRANSFER_RUN = "024_gssi51600s_short_profile_time_zero_transfer_policy"
DEFAULT_APPLICATION_RUN = "025_gssi51600s_short_profile_time_zero_application_policy"
DEFAULT_PHASE_CONVENTION_RUN = "027_gssi51600s_short_profile_phase_convention_transfer_policy"
DEFAULT_BOOTSTRAP_RUN = "029_gssi51600s_short_profile_timing_bootstrap_policy"
DEFAULT_CONTENT_ANCHOR_RUN = "037_gssi51600s_content_time_zero_anchor_policy"
DEFAULT_TRACE_ALIGNMENT_RUN = "039_gssi51600s_content_anchor_trace_alignment"
DEFAULT_TRACE_SENSITIVITY_RUN = "041_gssi51600s_content_anchor_trace_alignment_sensitivity"
DEFAULT_STACK_RUN = "043_gssi51600s_corrected_profile_stack"
DEFAULT_STACK_SENSITIVITY_RUN = "045_gssi51600s_corrected_profile_stack_sensitivity"
DEFAULT_SPATIAL_SUPPORT_RUN = "047_gssi51600s_corrected_stack_spatial_support"
DEFAULT_SUPPORTED_INTERVAL_RUN = "049_gssi51600s_supported_interval_visual_qc"
DEFAULT_BANDLIMITED_RUN = "068_gssi51600s_field_bandlimited_repeatability_audit"
DEFAULT_EVENT_SUPPORT_RUN = "072_gssi51600s_field_event_support_tiers"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def nested_summary(payload: dict) -> dict:
    return payload.get("summary", payload)


def load_budget_inputs(dataset_root: Path, runs: dict[str, str]) -> dict[str, dict]:
    return {
        "transfer": read_json(
            dataset_root / runs["transfer"] / "data" / "short_profile_time_zero_transfer_summary.json"
        ),
        "application": read_json(
            dataset_root / runs["application"] / "data" / "short_profile_time_zero_application_summary.json"
        ),
        "phase_convention": read_json(
            dataset_root / runs["phase_convention"] / "data" / "short_profile_phase_convention_transfer_summary.json"
        ),
        "bootstrap": read_json(
            dataset_root / runs["bootstrap"] / "data" / "short_profile_timing_bootstrap_policy_summary.json"
        ),
        "content_anchor": read_json(
            dataset_root / runs["content_anchor"] / "data" / "short_profile_content_time_zero_anchor_summary.json"
        ),
        "trace_alignment": read_json(
            dataset_root / runs["trace_alignment"] / "data" / "content_anchor_trace_alignment_summary.json"
        ),
        "trace_sensitivity": read_json(
            dataset_root
            / runs["trace_sensitivity"]
            / "data"
            / "content_anchor_trace_alignment_sensitivity_summary.json"
        ),
        "stack": read_json(dataset_root / runs["stack"] / "data" / "corrected_profile_stack_summary.json"),
        "stack_sensitivity": read_json(
            dataset_root
            / runs["stack_sensitivity"]
            / "data"
            / "corrected_profile_stack_sensitivity_summary.json"
        ),
        "spatial_support": read_json(
            dataset_root / runs["spatial_support"] / "data" / "corrected_stack_spatial_support_summary.json"
        ),
        "supported_interval": read_json(
            dataset_root / runs["supported_interval"] / "data" / "supported_interval_visual_qc_summary.json"
        ),
        "bandlimited": read_json(
            dataset_root / runs["bandlimited"] / "data" / "field_bandlimited_repeatability_summary.json"
        ),
        "event_support": read_json(
            dataset_root / runs["event_support"] / "data" / "field_event_support_tiers_summary.json"
        ),
    }


def bounded_row(
    *,
    budget_key: str,
    evidence_scope: str,
    policy_label: str,
    central_ns: float,
    lower_ns: float,
    upper_ns: float,
    support_count: float,
    total_count: float,
    quality_metric_label: str,
    quality_metric_value: float,
    claim_allowed: str,
    claim_blocked: str,
) -> dict:
    lower = safe_float(lower_ns)
    upper = safe_float(upper_ns)
    central = safe_float(central_ns)
    half_width = max(abs(central - lower), abs(upper - central)) if all(
        math.isfinite(value) for value in (central, lower, upper)
    ) else math.nan
    support_fraction = support_count / total_count if total_count else math.nan
    return {
        "budget_key": budget_key,
        "evidence_scope": evidence_scope,
        "policy_label": policy_label,
        "central_offset_ns": central,
        "lower_bound_ns": lower,
        "upper_bound_ns": upper,
        "half_width_ns": half_width,
        "support_count": support_count,
        "total_count": total_count,
        "support_fraction": support_fraction,
        "quality_metric_label": quality_metric_label,
        "quality_metric_value": quality_metric_value,
        "claim_allowed": claim_allowed,
        "claim_blocked": claim_blocked,
    }


def support_row(
    *,
    budget_key: str,
    evidence_scope: str,
    policy_label: str,
    support_count: float,
    total_count: float,
    quality_metric_label: str,
    quality_metric_value: float,
    claim_allowed: str,
    claim_blocked: str,
) -> dict:
    support_fraction = support_count / total_count if total_count else math.nan
    return {
        "budget_key": budget_key,
        "evidence_scope": evidence_scope,
        "policy_label": policy_label,
        "central_offset_ns": math.nan,
        "lower_bound_ns": math.nan,
        "upper_bound_ns": math.nan,
        "half_width_ns": math.nan,
        "support_count": support_count,
        "total_count": total_count,
        "support_fraction": support_fraction,
        "quality_metric_label": quality_metric_label,
        "quality_metric_value": quality_metric_value,
        "claim_allowed": claim_allowed,
        "claim_blocked": claim_blocked,
    }


def budget_rows(summaries: dict[str, dict]) -> list[dict]:
    transfer = nested_summary(summaries["transfer"])
    application = nested_summary(summaries["application"])
    phase = nested_summary(summaries["phase_convention"])
    bootstrap = nested_summary(summaries["bootstrap"])
    anchor = summaries["content_anchor"]
    trace = summaries["trace_alignment"]
    trace_sensitivity = summaries["trace_sensitivity"]
    stack = nested_summary(summaries["stack"])
    stack_sensitivity = summaries["stack_sensitivity"]
    spatial = summaries["spatial_support"]
    interval = summaries["supported_interval"]
    bandlimited = summaries["bandlimited"]
    event_support = summaries["event_support"]
    applied_offset = safe_float(application.get("applied_transfer_offset_ns"))
    bootstrap_median = safe_float(bootstrap.get("observed_median_offset_ns"))
    rows = [
        bounded_row(
            budget_key="short_pair_transfer_offset_range",
            evidence_scope="event_pair_delta",
            policy_label=transfer.get("policy_label", ""),
            central_ns=safe_float(transfer.get("median_comparison_minus_reference_phase_time_ns")),
            lower_ns=safe_float(transfer.get("min_comparison_minus_reference_phase_time_ns")),
            upper_ns=safe_float(transfer.get("max_comparison_minus_reference_phase_time_ns")),
            support_count=safe_float(transfer.get("event_pair_count")),
            total_count=safe_float(transfer.get("event_pair_count")),
            quality_metric_label="best_normalized_correlation",
            quality_metric_value=safe_float(transfer.get("best_normalized_correlation")),
            claim_allowed="relative short-pair timing-transfer estimate",
            claim_blocked="absolute time-zero, radius, cover-depth, geometry, 3D, or FWI",
        ),
        bounded_row(
            budget_key="phase_convention_stable_median_spread",
            evidence_scope="phase_convention",
            policy_label=phase.get("policy_label", ""),
            central_ns=0.5
            * (
                safe_float(phase.get("stable_median_delta_min_ns"))
                + safe_float(phase.get("stable_median_delta_max_ns"))
            ),
            lower_ns=safe_float(phase.get("stable_median_delta_min_ns")),
            upper_ns=safe_float(phase.get("stable_median_delta_max_ns")),
            support_count=safe_float(phase.get("stable_phase_convention_count")),
            total_count=safe_float(phase.get("phase_convention_count")),
            quality_metric_label="stable_median_delta_spread_ns",
            quality_metric_value=safe_float(phase.get("stable_median_delta_spread_ns")),
            claim_allowed="relative offset is stable across accepted phase conventions",
            claim_blocked="phase-convention agreement as absolute calibration",
        ),
        bounded_row(
            budget_key="bootstrap_stable_offset_ci",
            evidence_scope="bootstrap_stable_offsets",
            policy_label=bootstrap.get("policy_label", ""),
            central_ns=bootstrap_median,
            lower_ns=safe_float(bootstrap.get("min_bootstrap_ci_lower_ns")),
            upper_ns=safe_float(bootstrap.get("max_bootstrap_ci_upper_ns")),
            support_count=safe_float(bootstrap.get("stable_offset_count")),
            total_count=safe_float(bootstrap.get("stable_offset_count")),
            quality_metric_label="max_bootstrap_ci_width_ns",
            quality_metric_value=safe_float(bootstrap.get("max_bootstrap_ci_width_ns")),
            claim_allowed="uncertainty-bounded relative timing QC",
            claim_blocked="absolute calibrated time-zero claim",
        ),
        bounded_row(
            budget_key="applied_transfer_residual_guardrail",
            evidence_scope="leave_one_out_residual",
            policy_label=application.get("policy_label", ""),
            central_ns=applied_offset,
            lower_ns=applied_offset - safe_float(application.get("leave_one_out_max_abs_residual_ns")),
            upper_ns=applied_offset + safe_float(application.get("leave_one_out_max_abs_residual_ns")),
            support_count=safe_float(application.get("event_pair_count")),
            total_count=safe_float(application.get("event_pair_count")),
            quality_metric_label="mean_abs_residual_reduction_factor",
            quality_metric_value=safe_float(application.get("mean_abs_residual_reduction_factor")),
            claim_allowed="applied relative correction reduces event residuals",
            claim_blocked="residual guardrail as field inversion validation",
        ),
        bounded_row(
            budget_key="content_anchor_residual_guardrail",
            evidence_scope="content_backed_anchors",
            policy_label=anchor.get("policy_label", ""),
            central_ns=bootstrap_median,
            lower_ns=bootstrap_median - safe_float(anchor.get("max_abs_content_timing_residual_ns")),
            upper_ns=bootstrap_median + safe_float(anchor.get("max_abs_content_timing_residual_ns")),
            support_count=safe_float(anchor.get("supported_content_anchor_pair_count")),
            total_count=safe_float(anchor.get("event_pair_count")),
            quality_metric_label="min_content_pair_absolute_correlation",
            quality_metric_value=safe_float(anchor.get("min_content_pair_absolute_correlation")),
            claim_allowed="content-backed short-pair relative time-zero visual QC",
            claim_blocked="timing-only cue or absolute time-zero calibration",
        ),
        bounded_row(
            budget_key="trace_alignment_residual_guardrail",
            evidence_scope="field_trace_alignment",
            policy_label=trace.get("policy_label", ""),
            central_ns=applied_offset,
            lower_ns=applied_offset - safe_float(trace.get("max_corrected_abs_timing_residual_ns")),
            upper_ns=applied_offset + safe_float(trace.get("max_corrected_abs_timing_residual_ns")),
            support_count=safe_float(trace.get("field_trace_alignment_improved_count")),
            total_count=safe_float(trace.get("supported_anchor_pair_count")),
            quality_metric_label="mean_corrected_abs_correlation",
            quality_metric_value=safe_float(trace.get("mean_corrected_abs_correlation")),
            claim_allowed="measured trace agreement improves after relative correction",
            claim_blocked="trace alignment as geometry/radius/FWI evidence",
        ),
        support_row(
            budget_key="trace_alignment_window_robustness",
            evidence_scope="window_sensitivity",
            policy_label=trace_sensitivity.get("policy_label", ""),
            support_count=safe_float(trace_sensitivity.get("improved_pair_window_count")),
            total_count=safe_float(trace_sensitivity.get("pair_window_row_count")),
            quality_metric_label="min_corrected_abs_correlation",
            quality_metric_value=safe_float(trace_sensitivity.get("min_corrected_abs_correlation")),
            claim_allowed="relative trace-alignment improvement survives tested windows",
            claim_blocked="window robustness as field FWI readiness",
        ),
        support_row(
            budget_key="corrected_profile_stack_robustness",
            evidence_scope="bscan_stack",
            policy_label=stack.get("policy_label", ""),
            support_count=safe_float(stack.get("improved_column_count")),
            total_count=safe_float(stack.get("finite_column_count")),
            quality_metric_label="corrected_matrix_abs_correlation",
            quality_metric_value=safe_float(stack.get("corrected_matrix_abs_correlation")),
            claim_allowed="B-scan-level agreement improves after relative correction",
            claim_blocked="corrected stack as absolute time-zero or field inversion",
        ),
        support_row(
            budget_key="corrected_stack_window_sensitivity",
            evidence_scope="bscan_window_sensitivity",
            policy_label=stack_sensitivity.get("policy_label", ""),
            support_count=safe_float(stack_sensitivity.get("robust_window_count")),
            total_count=safe_float(stack_sensitivity.get("window_count")),
            quality_metric_label="min_matrix_abs_correlation_improvement",
            quality_metric_value=safe_float(stack_sensitivity.get("min_matrix_abs_correlation_improvement")),
            claim_allowed="B-scan-level improvement survives tested shallow windows",
            claim_blocked="window robustness as full-profile interpretability",
        ),
        support_row(
            budget_key="spatial_support_mask",
            evidence_scope="corrected_stack_spatial_support",
            policy_label=spatial.get("policy_label", ""),
            support_count=safe_float(spatial.get("all_window_supported_column_count")),
            total_count=safe_float(spatial.get("finite_column_count")),
            quality_metric_label="largest_interval_length_m",
            quality_metric_value=safe_float(spatial.get("largest_majority_interval_length_m")),
            claim_allowed="interpret corrected-stack visuals only inside supported intervals",
            claim_blocked="unsupported columns as field interpretation",
        ),
        support_row(
            budget_key="supported_interval_visual_endpoint",
            evidence_scope="supported_interval_visual_qc",
            policy_label=interval.get("policy_label", ""),
            support_count=safe_float(interval.get("supported_interval_count")),
            total_count=safe_float(interval.get("selected_interval_count")),
            quality_metric_label="min_corrected_interval_abs_correlation",
            quality_metric_value=safe_float(interval.get("min_corrected_interval_abs_correlation")),
            claim_allowed="supported intervals are the preferred corrected-stack visual endpoint",
            claim_blocked="visual endpoint as absolute time-zero calibration",
        ),
        support_row(
            budget_key="bandlimited_short_repeatability",
            evidence_scope="frequency_band_support",
            policy_label=bandlimited.get("policy_label", ""),
            support_count=safe_float(bandlimited.get("short_supported_band_count")),
            total_count=float(max(1, len(bandlimited.get("bands", [])))),
            quality_metric_label="short_unfiltered_abs_correlation_gain",
            quality_metric_value=safe_float(bandlimited.get("short_unfiltered_abs_correlation_gain")),
            claim_allowed="relative correction is supported across most tested field bands",
            claim_blocked="band support as absolute time-zero or inversion evidence",
        ),
        support_row(
            budget_key="event_support_time_zero_boundary",
            evidence_scope="event_support_tiers",
            policy_label=event_support.get("policy_label", ""),
            support_count=safe_float(event_support.get("short_content_anchor_supported_count")),
            total_count=safe_float(event_support.get("short_event_pair_count")),
            quality_metric_label="short_content_anchor_support_fraction",
            quality_metric_value=safe_float(event_support.get("short_content_anchor_support_fraction")),
            claim_allowed="two of three short-pair events are content-backed timing anchors",
            claim_blocked="timing-only event as content-backed anchor or FWI evidence",
        ),
    ]
    return rows


def finite_half_widths(rows: list[dict]) -> list[float]:
    return [safe_float(row.get("half_width_ns")) for row in rows if math.isfinite(safe_float(row.get("half_width_ns")))]


def summarize_budget(rows: list[dict], summaries: dict[str, dict]) -> dict:
    application = nested_summary(summaries["application"])
    bootstrap = nested_summary(summaries["bootstrap"])
    anchor = summaries["content_anchor"]
    trace_sensitivity = summaries["trace_sensitivity"]
    spatial = summaries["spatial_support"]
    bandlimited = summaries["bandlimited"]
    widths = finite_half_widths(rows)
    conservative_half_width = max(widths) if widths else math.nan
    return {
        "policy_label": "field_time_zero_uncertainty_budget_short_pair_relative_qc_not_absolute",
        "budget_row_count": len(rows),
        "relative_anchor_offset_ns": safe_float(application.get("applied_transfer_offset_ns")),
        "bootstrap_observed_median_offset_ns": safe_float(bootstrap.get("observed_median_offset_ns")),
        "bootstrap_ci_lower_ns": safe_float(bootstrap.get("min_bootstrap_ci_lower_ns")),
        "bootstrap_ci_upper_ns": safe_float(bootstrap.get("max_bootstrap_ci_upper_ns")),
        "bootstrap_ci_width_ns": safe_float(bootstrap.get("max_bootstrap_ci_width_ns")),
        "conservative_half_width_ns": conservative_half_width,
        "leave_one_out_max_abs_residual_ns": safe_float(application.get("leave_one_out_max_abs_residual_ns")),
        "content_anchor_supported_pair_count": safe_float(anchor.get("supported_content_anchor_pair_count")),
        "content_anchor_event_pair_count": safe_float(anchor.get("event_pair_count")),
        "max_abs_content_anchor_residual_ns": safe_float(anchor.get("max_abs_content_timing_residual_ns")),
        "trace_window_supported_count": safe_float(trace_sensitivity.get("improved_pair_window_count")),
        "trace_window_row_count": safe_float(trace_sensitivity.get("pair_window_row_count")),
        "spatial_all_window_supported_fraction": (
            safe_float(spatial.get("all_window_supported_column_count"))
            / safe_float(spatial.get("finite_column_count"))
        ),
        "short_band_supported_count": safe_float(bandlimited.get("short_supported_band_count")),
        "short_band_supported_bands": bandlimited.get("short_supported_bands", ""),
        "absolute_time_zero_ready": False,
        "field_fwi_ready": False,
        "field_gpu_fwi_priority": "none",
        "ready_for_manuscript_time_zero_budget": True,
        "decision": (
            "Use this as a relative time-zero uncertainty budget for the "
            "short 014/016 field pair only. The supported estimate is bounded "
            "by phase-convention and bootstrap evidence and stress-tested by "
            "content anchors, trace alignment, stack windows, spatial support, "
            "and band-limited repeatability. It remains measured-field QC, not "
            "absolute time-zero calibration, field FWI, 3D inversion, radius, "
            "or cover-depth evidence."
        ),
    }


def plot_budget(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["budget_key"].replace("_", "\n") for row in rows]
    half_widths = np.asarray(
        [
            safe_float(row["half_width_ns"]) if math.isfinite(safe_float(row["half_width_ns"])) else 0.0
            for row in rows
        ],
        dtype=np.float64,
    )
    supports = np.asarray(
        [
            safe_float(row["support_fraction"]) if math.isfinite(safe_float(row["support_fraction"])) else 0.0
            for row in rows
        ],
        dtype=np.float64,
    )
    y = np.arange(len(rows))
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 8.0), constrained_layout=True)
    axes[0].barh(y, half_widths, color="#4c78a8")
    axes[0].set_yticks(y, labels)
    axes[0].invert_yaxis()
    axes[0].set_xlabel("half-width or residual guardrail [ns]")
    axes[0].set_title("Timing-offset uncertainty rows")
    axes[0].grid(axis="x", color="#dddddd", linewidth=0.6)
    axes[1].barh(y, supports, color="#2f9d55")
    axes[1].set_yticks(y, [""] * len(rows))
    axes[1].invert_yaxis()
    axes[1].set_xlim(0.0, 1.05)
    axes[1].set_xlabel("support fraction")
    axes[1].set_title("Robustness/support rows")
    axes[1].grid(axis="x", color="#dddddd", linewidth=0.6)
    axes[0].text(
        0.02,
        0.02,
        (
            f"offset={summary['relative_anchor_offset_ns']:.6f} ns | "
            f"bootstrap={summary['bootstrap_ci_lower_ns']:.6f}-{summary['bootstrap_ci_upper_ns']:.6f} ns"
        ),
        transform=axes[0].transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
    )
    axes[1].text(
        0.02,
        0.02,
        f"absolute_time_zero={summary['absolute_time_zero_ready']} | fwi={summary['field_fwi_ready']}",
        transform=axes[1].transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
    )
    fig.suptitle("GSSI 51600S short-pair relative time-zero uncertainty budget", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--transfer-run", default=DEFAULT_TRANSFER_RUN)
    parser.add_argument("--application-run", default=DEFAULT_APPLICATION_RUN)
    parser.add_argument("--phase-convention-run", default=DEFAULT_PHASE_CONVENTION_RUN)
    parser.add_argument("--bootstrap-run", default=DEFAULT_BOOTSTRAP_RUN)
    parser.add_argument("--content-anchor-run", default=DEFAULT_CONTENT_ANCHOR_RUN)
    parser.add_argument("--trace-alignment-run", default=DEFAULT_TRACE_ALIGNMENT_RUN)
    parser.add_argument("--trace-sensitivity-run", default=DEFAULT_TRACE_SENSITIVITY_RUN)
    parser.add_argument("--stack-run", default=DEFAULT_STACK_RUN)
    parser.add_argument("--stack-sensitivity-run", default=DEFAULT_STACK_SENSITIVITY_RUN)
    parser.add_argument("--spatial-support-run", default=DEFAULT_SPATIAL_SUPPORT_RUN)
    parser.add_argument("--supported-interval-run", default=DEFAULT_SUPPORTED_INTERVAL_RUN)
    parser.add_argument("--bandlimited-run", default=DEFAULT_BANDLIMITED_RUN)
    parser.add_argument("--event-support-run", default=DEFAULT_EVENT_SUPPORT_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_time_zero_uncertainty_budget")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    runs = {
        "transfer": args.transfer_run,
        "application": args.application_run,
        "phase_convention": args.phase_convention_run,
        "bootstrap": args.bootstrap_run,
        "content_anchor": args.content_anchor_run,
        "trace_alignment": args.trace_alignment_run,
        "trace_sensitivity": args.trace_sensitivity_run,
        "stack": args.stack_run,
        "stack_sensitivity": args.stack_sensitivity_run,
        "spatial_support": args.spatial_support_run,
        "supported_interval": args.supported_interval_run,
        "bandlimited": args.bandlimited_run,
        "event_support": args.event_support_run,
    }
    summaries = load_budget_inputs(dataset_root, runs)
    rows = budget_rows(summaries)
    summary = summarize_budget(rows, summaries)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_time_zero_uncertainty_budget_rows.csv"
    summary_json = data_dir / "field_time_zero_uncertainty_budget_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_budget(rows, summary, figures_dir / "field_time_zero_uncertainty_budget.png"))

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "runs": runs,
        **summary,
        "paths": {
            "rows_csv": str(rows_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
        "readgssi_version": readgssi_version(),
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_time_zero_uncertainty_budget",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

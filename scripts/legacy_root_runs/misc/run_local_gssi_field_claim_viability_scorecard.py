#!/usr/bin/env python3
"""Build a field manuscript claim-viability scorecard from existing GSSI evidence."""

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
from matplotlib.patches import Patch  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_EVENT_SUPPORT_RUN = "072_gssi51600s_field_event_support_tiers"
DEFAULT_ACQUISITION_RUN = "081_gssi51600s_field_acquisition_readiness_audit"
DEFAULT_APPARENT_DEPTH_RUN = "084_gssi51600s_field_apparent_depth_qc"
DEFAULT_APPARENT_DEPTH_SENSITIVITY_RUN = "085_gssi51600s_field_apparent_depth_sensitivity"
DEFAULT_DEGENERACY_RUN = "086_gssi51600s_field_hyperbola_timezero_degeneracy_audit"
DEFAULT_CUE_SPACING_RUN = "093_gssi51600s_field_cue_spacing_context_audit"
DEFAULT_FIELD_BUNDLE_RUN = "102_gssi51600s_field_publication_claim_bundle_post_timing_window_family"
DEFAULT_TIMING_SCORECARD_RUN = "105_gssi51600s_field_timing_discriminant_scorecard"
DEFAULT_DATASET_CARD_RUN = "011_local_gssi_field_dataset_card_post_timing_window_family"


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


def bool_value(value) -> bool:
    return str(value).strip().lower() == "true"


def clamp01(value: float) -> float:
    value = safe_float(value, 0.0)
    return min(1.0, max(0.0, value))


def event_row(rows: list[dict], tier_key: str) -> dict:
    for row in rows:
        if row.get("tier_key") == tier_key:
            return row
    return {}


def timing_row(rows: list[dict], key: str) -> dict:
    for row in rows:
        if row.get("timing_discriminant") == key:
            return row
    return {}


def claim_row(
    *,
    claim_key: str,
    evidence_family: str,
    status: str,
    support_score: float,
    primary_metric_label: str,
    primary_metric_value: float,
    allowed_claim: str,
    blocked_claim: str,
    source: str,
) -> dict:
    return {
        "claim_key": claim_key,
        "evidence_family": evidence_family,
        "status": status,
        "support_score": clamp01(support_score),
        "primary_metric_label": primary_metric_label,
        "primary_metric_value": safe_float(primary_metric_value, 0.0),
        "allowed_claim": allowed_claim,
        "blocked_claim": blocked_claim,
        "source": source,
    }


def build_claim_rows(
    *,
    event_rows: list[dict],
    timing_rows: list[dict],
    acquisition: dict,
    apparent_depth: dict,
    depth_sensitivity: dict,
    degeneracy: dict,
    cue_spacing: dict,
    dataset_card: dict,
    publication_bundle: dict,
) -> list[dict]:
    short_timing = timing_row(timing_rows, "short_content_relative")
    raw_timing = timing_row(timing_rows, "raw_no_correction")
    long_timing = timing_row(timing_rows, "long_pattern_only")
    early_timing = timing_row(timing_rows, "early_common_mode")
    stack_support = event_row(event_rows, "short_supported_stack_intervals")
    short_content = event_row(event_rows, "short_content_time_zero_anchors")
    long_pattern = event_row(event_rows, "long_stable_pattern_anchors")

    same_time_spacing = safe_float(cue_spacing.get("min_dataset_same_time_lateral_spacing_mm"))
    synthetic_spacing = safe_float(cue_spacing.get("synthetic_close_spacing_context_max_mm"))
    spacing_ratio = same_time_spacing / synthetic_spacing if synthetic_spacing > 0 else math.nan
    depth_budget_mm = safe_float(apparent_depth.get("time_zero_depth_equivalent_mm"))
    corrected_depth_residual_mm = safe_float(apparent_depth.get("max_corrected_depth_residual_mm"))
    depth_residual_fraction = (
        corrected_depth_residual_mm / depth_budget_mm if depth_budget_mm > 0 else math.nan
    )
    spatial_support = safe_float(acquisition.get("spatial_all_window_supported_fraction"))

    return [
        claim_row(
            claim_key="field_dataset_methods_2d_line_profiles",
            evidence_family="dataset_geometry",
            status="supported",
            support_score=1.0 if acquisition.get("ready_for_2d_qc") else 0.0,
            primary_metric_label="profile_count",
            primary_metric_value=safe_float(dataset_card.get("profile_count")),
            allowed_claim="Dense along-line local GSSI profiles can support 2D field QC and methods context.",
            blocked_claim="3D survey, field FWI benchmark, radius recovery, or cover-depth recovery.",
            source=DEFAULT_ACQUISITION_RUN,
        ),
        claim_row(
            claim_key="short_pair_relative_time_zero",
            evidence_family="timing",
            status="supported",
            support_score=safe_float(short_timing.get("support_fraction")),
            primary_metric_label="nominal_relative_offset_ns",
            primary_metric_value=safe_float(short_timing.get("representative_offset_ns")),
            allowed_claim="Short repeat pair supports a relative time-zero correction and corrected-stack QC.",
            blocked_claim="Absolute time-zero calibration, field FWI, 3D inversion, radius, or cover-depth recovery.",
            source=DEFAULT_TIMING_SCORECARD_RUN,
        ),
        claim_row(
            claim_key="early_common_mode_anchor",
            evidence_family="timing",
            status="scope_limited",
            support_score=safe_float(early_timing.get("support_fraction")),
            primary_metric_label="early_uniqueness_margin",
            primary_metric_value=safe_float(early_timing.get("strength_metric")),
            allowed_claim="Early/direct windows can be reported as common-mode timing controls.",
            blocked_claim="Absolute time-zero calibration.",
            source=DEFAULT_TIMING_SCORECARD_RUN,
        ),
        claim_row(
            claim_key="raw_no_correction_control",
            evidence_family="timing",
            status="rejected_control",
            support_score=1.0 - safe_float(raw_timing.get("support_fraction")),
            primary_metric_label="raw_supported_fraction",
            primary_metric_value=safe_float(raw_timing.get("support_fraction")),
            allowed_claim="Raw/no-correction rows are useful as a negative-control baseline.",
            blocked_claim="Uncorrected short-pair timing support.",
            source=DEFAULT_TIMING_SCORECARD_RUN,
        ),
        claim_row(
            claim_key="long_profile_pattern_only_alignment",
            evidence_family="timing",
            status="scope_limited",
            support_score=safe_float(long_timing.get("support_fraction")),
            primary_metric_label="pattern_offset_ns",
            primary_metric_value=safe_float(long_timing.get("representative_offset_ns")),
            allowed_claim="Long profiles support stable pattern-only visual QC.",
            blocked_claim="Phase time-zero, short-transfer timing, field FWI, or 3D inversion.",
            source=DEFAULT_TIMING_SCORECARD_RUN,
        ),
        claim_row(
            claim_key="corrected_stack_supported_intervals",
            evidence_family="event_support",
            status="scope_limited",
            support_score=min(
                safe_float(stack_support.get("support_fraction"), 0.0),
                spatial_support if math.isfinite(spatial_support) else 1.0,
            ),
            primary_metric_label="all_window_supported_fraction",
            primary_metric_value=spatial_support,
            allowed_claim="Corrected-stack visual QC can be used inside supported intervals.",
            blocked_claim="Full-profile interpretation or field inversion outside supported intervals.",
            source=DEFAULT_EVENT_SUPPORT_RUN,
        ),
        claim_row(
            claim_key="short_content_event_support",
            evidence_family="event_support",
            status="scope_limited",
            support_score=safe_float(short_content.get("support_fraction")),
            primary_metric_label="min_content_abs_corr",
            primary_metric_value=safe_float(short_content.get("quality_metric_value")),
            allowed_claim="Short-pair content-backed timing is usable as local field QC.",
            blocked_claim="Known-truth geometry, radius, or calibrated cover-depth evidence.",
            source=DEFAULT_EVENT_SUPPORT_RUN,
        ),
        claim_row(
            claim_key="field_cue_spacing_context",
            evidence_family="spacing",
            status="context_only",
            support_score=1.0 if cue_spacing.get("ready_for_field_context") else 0.0,
            primary_metric_label="field_to_synthetic_spacing_ratio",
            primary_metric_value=spacing_ratio,
            allowed_claim="Measured visible cue spacings can contextualize the synthetic close-spacing stress scale.",
            blocked_claim="Measured-field validation of synthetic close-spacing resolution thresholds.",
            source=DEFAULT_CUE_SPACING_RUN,
        ),
        claim_row(
            claim_key="apparent_depth_scale_qc",
            evidence_family="depth_scale",
            status="scope_limited",
            support_score=1.0 - clamp01(depth_residual_fraction),
            primary_metric_label="max_corrected_depth_residual_mm",
            primary_metric_value=corrected_depth_residual_mm,
            allowed_claim="Apparent-depth scale can be used as relative QC after short-pair correction.",
            blocked_claim="Calibrated cover-depth recovery.",
            source=DEFAULT_APPARENT_DEPTH_RUN,
        ),
        claim_row(
            claim_key="cover_depth_recovery",
            evidence_family="depth_scale",
            status="blocked",
            support_score=0.0 if not depth_sensitivity.get("cover_depth_claim_ready") else 1.0,
            primary_metric_label="max_apparent_depth_span_mm",
            primary_metric_value=safe_float(depth_sensitivity.get("max_apparent_depth_span_mm")),
            allowed_claim="None from the current field dataset beyond apparent-depth QC scale.",
            blocked_claim="Cover-depth recovery from this field dataset.",
            source=DEFAULT_APPARENT_DEPTH_SENSITIVITY_RUN,
        ),
        claim_row(
            claim_key="radius_or_parametric_field_inversion",
            evidence_family="inversion",
            status="blocked",
            support_score=0.0 if not degeneracy.get("radius_claim_ready") else 1.0,
            primary_metric_label="max_near_top_time_zero_span_ns",
            primary_metric_value=safe_float(degeneracy.get("max_near_top_time_zero_span_ns")),
            allowed_claim="None; keep radius and parametric field inversion claims on synthetic known-truth data.",
            blocked_claim="Radius recovery or calibrated parametric inversion from these field profiles.",
            source=DEFAULT_DEGENERACY_RUN,
        ),
        claim_row(
            claim_key="field_fwi_3d_hpc_submission",
            evidence_family="compute_readiness",
            status="blocked",
            support_score=0.0,
            primary_metric_label="field_hpc_priority",
            primary_metric_value=0.0,
            allowed_claim="No local or NERSC field-side heavy job is justified from this dataset alone.",
            blocked_claim="Field FWI, 3D inversion, or A100/HPC submission from these field profiles.",
            source=DEFAULT_ACQUISITION_RUN,
        ),
        claim_row(
            claim_key="field_publication_bundle_current",
            evidence_family="manuscript_handoff",
            status="supported",
            support_score=1.0
            if (
                publication_bundle.get("ready_for_manuscript")
                or publication_bundle.get("ready_for_manuscript_field_supplement")
            )
            else 0.0,
            primary_metric_label="publication_bundle_figure_count",
            primary_metric_value=safe_float(publication_bundle.get("figure_row_count")),
            allowed_claim="Use the current field publication bundle for paper-facing field figures and claim boundaries.",
            blocked_claim="Treating the standalone timing scorecard as already promoted into a refreshed bundle.",
            source=DEFAULT_FIELD_BUNDLE_RUN,
        ),
    ]


def summarize_claim_rows(
    rows: list[dict],
    *,
    acquisition: dict,
    timing_summary: dict,
    cue_spacing: dict,
    apparent_depth: dict,
    depth_sensitivity: dict,
    degeneracy: dict,
) -> dict:
    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
    ready = (
        acquisition.get("ready_for_2d_qc") is True
        and acquisition.get("ready_for_3d_hpc") is False
        and acquisition.get("ready_for_field_fwi") is False
        and timing_summary.get("absolute_time_zero_ready") is False
        and apparent_depth.get("ready_for_cover_depth_recovery") is False
        and depth_sensitivity.get("cover_depth_claim_ready") is False
        and degeneracy.get("radius_claim_ready") is False
    )
    return {
        "policy_label": (
            "local_gssi_field_claim_viability_scorecard_ready_no_field_fwi"
            if ready
            else "local_gssi_field_claim_viability_scorecard_review_required"
        ),
        "claim_row_count": len(rows),
        "supported_count": status_counts.get("supported", 0),
        "scope_limited_count": status_counts.get("scope_limited", 0),
        "context_only_count": status_counts.get("context_only", 0),
        "rejected_control_count": status_counts.get("rejected_control", 0),
        "blocked_count": status_counts.get("blocked", 0),
        "ready_for_2d_field_qc": bool(acquisition.get("ready_for_2d_qc", False)),
        "ready_for_absolute_time_zero": bool(timing_summary.get("absolute_time_zero_ready", False)),
        "ready_for_cover_depth_recovery": bool(depth_sensitivity.get("cover_depth_claim_ready", False)),
        "ready_for_radius_recovery": bool(degeneracy.get("radius_claim_ready", False)),
        "ready_for_field_fwi": bool(acquisition.get("ready_for_field_fwi", False)),
        "ready_for_3d_hpc": bool(acquisition.get("ready_for_3d_hpc", False)),
        "min_same_time_lateral_spacing_mm": safe_float(cue_spacing.get("min_dataset_same_time_lateral_spacing_mm")),
        "synthetic_close_spacing_context_max_mm": safe_float(cue_spacing.get("synthetic_close_spacing_context_max_mm")),
        "max_corrected_depth_residual_mm": safe_float(apparent_depth.get("max_corrected_depth_residual_mm")),
        "time_zero_depth_equivalent_mm": safe_float(apparent_depth.get("time_zero_depth_equivalent_mm")),
        "max_apparent_depth_sensitivity_span_mm": safe_float(
            depth_sensitivity.get("max_apparent_depth_span_mm")
        ),
        "max_near_top_time_zero_span_ns": safe_float(degeneracy.get("max_near_top_time_zero_span_ns")),
        "scorecard_promoted_to_publication_bundle": False,
        "gpu_priority": "none",
        "ready_for_manuscript_field_claim_viability": ready,
        "decision": (
            "Use this scorecard to separate field claims into supported 2D QC, "
            "scope-limited timing/spacing/depth context, negative controls, and blocked "
            "absolute-time-zero/FWI/3D/radius/cover-depth claims. No GPU or HPC field job follows."
        ),
    }


def status_color(status: str) -> str:
    return {
        "supported": "#2f9d55",
        "scope_limited": "#d98c20",
        "context_only": "#4c78a8",
        "rejected_control": "#6b6b6b",
        "blocked": "#c7302b",
    }.get(status, "#6b6b6b")


def plot_scorecard(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["claim_key"].replace("_", "\n") for row in rows]
    scores = [safe_float(row["support_score"], 0.0) for row in rows]
    colors = [status_color(row["status"]) for row in rows]

    gate_labels = ["2D QC", "abs t0", "cover\ndepth", "radius", "field\nFWI", "3D/HPC"]
    gate_values = [
        1.0 if summary["ready_for_2d_field_qc"] else 0.0,
        1.0 if summary["ready_for_absolute_time_zero"] else 0.0,
        1.0 if summary["ready_for_cover_depth_recovery"] else 0.0,
        1.0 if summary["ready_for_radius_recovery"] else 0.0,
        1.0 if summary["ready_for_field_fwi"] else 0.0,
        1.0 if summary["ready_for_3d_hpc"] else 0.0,
    ]
    metric_labels = ["cue spacing", "synthetic\nclose", "depth\nresidual", "t0 depth\nbudget"]
    metric_values = [
        summary["min_same_time_lateral_spacing_mm"],
        summary["synthetic_close_spacing_context_max_mm"],
        summary["max_corrected_depth_residual_mm"],
        summary["time_zero_depth_equivalent_mm"],
    ]

    fig = plt.figure(figsize=(16.0, 8.2), constrained_layout=True)
    grid = fig.add_gridspec(2, 2, height_ratios=[1.15, 1.0])
    ax_claims = fig.add_subplot(grid[0, :])
    ax_gates = fig.add_subplot(grid[1, 0])
    ax_metrics = fig.add_subplot(grid[1, 1])

    x = np.arange(len(rows))
    ax_claims.bar(x, scores, color=colors, width=0.68)
    ax_claims.set_xticks(x, labels, fontsize=7)
    ax_claims.set_ylim(0, 1.05)
    ax_claims.set_ylabel("support or rejection score")
    ax_claims.set_title("Field claim viability by evidence family")
    ax_claims.grid(axis="y", color="#dddddd", linewidth=0.6)
    legend_statuses = ["supported", "scope_limited", "context_only", "rejected_control", "blocked"]
    ax_claims.legend(
        handles=[
            Patch(color=status_color(status), label=status.replace("_", " "))
            for status in legend_statuses
        ],
        loc="upper right",
        ncol=5,
        frameon=False,
        fontsize=8,
    )

    gate_colors = ["#2f9d55" if value else "#c7302b" for value in gate_values]
    ax_gates.bar(np.arange(len(gate_values)), gate_values, color=gate_colors, width=0.62)
    ax_gates.set_xticks(np.arange(len(gate_values)), gate_labels)
    ax_gates.set_ylim(0, 1.15)
    ax_gates.set_yticks([0, 1], ["blocked", "ready"])
    ax_gates.set_title("Use gates")
    ax_gates.grid(axis="y", color="#dddddd", linewidth=0.6)

    ax_metrics.bar(np.arange(len(metric_values)), metric_values, color=["#4c78a8", "#6b6b6b", "#d98c20", "#6b6b6b"], width=0.62)
    ax_metrics.set_xticks(np.arange(len(metric_values)), metric_labels)
    ax_metrics.set_ylabel("mm")
    ax_metrics.set_title("Context metrics")
    ax_metrics.grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Local GSSI field claim viability: 2D QC only, no field FWI/3D/HPC", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(
    path: Path,
    summary: dict,
    rows_csv: Path,
    summary_json: Path,
    validation_csv: Path,
) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_gssi_field_claim_viability_scorecard.png`",
                "",
                "This CPU-only scorecard consolidates existing local GSSI field",
                "evidence into supported, scope-limited, context-only, rejected",
                "control, and blocked manuscript claim classes.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Claim rows: `{summary['claim_row_count']}`.",
                f"Supported rows: `{summary['supported_count']}`.",
                f"Scope-limited rows: `{summary['scope_limited_count']}`.",
                f"Blocked rows: `{summary['blocked_count']}`.",
                f"Ready for 2D field QC: `{summary['ready_for_2d_field_qc']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                f"Ready for 3D/HPC: `{summary['ready_for_3d_hpc']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Claim rows: `{rows_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                f"- Figure validation: `{validation_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "The scorecard supports manuscript wording discipline. It does",
                "not promote field data to absolute time-zero, cover-depth,",
                "radius, field FWI, 3D, HPC, or synthetic-resolution validation.",
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
    parser.add_argument("--event-support-run", default=DEFAULT_EVENT_SUPPORT_RUN)
    parser.add_argument("--acquisition-run", default=DEFAULT_ACQUISITION_RUN)
    parser.add_argument("--apparent-depth-run", default=DEFAULT_APPARENT_DEPTH_RUN)
    parser.add_argument("--apparent-depth-sensitivity-run", default=DEFAULT_APPARENT_DEPTH_SENSITIVITY_RUN)
    parser.add_argument("--degeneracy-run", default=DEFAULT_DEGENERACY_RUN)
    parser.add_argument("--cue-spacing-run", default=DEFAULT_CUE_SPACING_RUN)
    parser.add_argument("--field-bundle-run", default=DEFAULT_FIELD_BUNDLE_RUN)
    parser.add_argument("--timing-scorecard-run", default=DEFAULT_TIMING_SCORECARD_RUN)
    parser.add_argument("--dataset-card-run", default=DEFAULT_DATASET_CARD_RUN)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--run-name", default="local_gssi_field_claim_viability_scorecard")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    summary_root = Path(args.summary_root)

    event_rows = read_csv_rows(
        dataset_root / args.event_support_run / "data/field_event_support_tiers.csv"
    )
    timing_rows = read_csv_rows(
        dataset_root
        / args.timing_scorecard_run
        / "data/field_timing_discriminant_scorecard_rows.csv"
    )
    acquisition = read_json(
        dataset_root / args.acquisition_run / "data/field_acquisition_readiness_summary.json"
    )
    apparent_depth = read_json(
        dataset_root / args.apparent_depth_run / "data/field_apparent_depth_qc_summary.json"
    )
    depth_sensitivity = read_json(
        dataset_root
        / args.apparent_depth_sensitivity_run
        / "data/field_apparent_depth_sensitivity_summary.json"
    )
    degeneracy = read_json(
        dataset_root
        / args.degeneracy_run
        / "data/field_hyperbola_timezero_degeneracy_summary.json"
    )
    cue_spacing = read_json(
        dataset_root / args.cue_spacing_run / "data/field_cue_spacing_context_summary.json"
    )
    publication_bundle = read_json(
        dataset_root / args.field_bundle_run / "data/field_publication_claim_bundle_summary.json"
    )
    timing_summary = read_json(
        dataset_root
        / args.timing_scorecard_run
        / "data/field_timing_discriminant_scorecard_summary.json"
    )
    dataset_card = read_json(
        summary_root / args.dataset_card_run / "data/local_gssi_field_dataset_card_summary.json"
    )

    rows = build_claim_rows(
        event_rows=event_rows,
        timing_rows=timing_rows,
        acquisition=acquisition,
        apparent_depth=apparent_depth,
        depth_sensitivity=depth_sensitivity,
        degeneracy=degeneracy,
        cue_spacing=cue_spacing,
        dataset_card=dataset_card,
        publication_bundle=publication_bundle,
    )
    summary = summarize_claim_rows(
        rows,
        acquisition=acquisition,
        timing_summary=timing_summary,
        cue_spacing=cue_spacing,
        apparent_depth=apparent_depth,
        depth_sensitivity=depth_sensitivity,
        degeneracy=degeneracy,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_gssi_field_claim_viability_rows.csv"
    summary_json = data_dir / "local_gssi_field_claim_viability_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_gssi_field_claim_viability_scorecard.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    plot_scorecard(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, rows_csv, summary_json, validation_csv)
    write_run_manifest(
        str(outdir),
        "local_gssi_field_claim_viability_scorecard",
        {
            "dataset_id": args.dataset_id,
            "event_support_run": args.event_support_run,
            "acquisition_run": args.acquisition_run,
            "apparent_depth_run": args.apparent_depth_run,
            "apparent_depth_sensitivity_run": args.apparent_depth_sensitivity_run,
            "degeneracy_run": args.degeneracy_run,
            "cue_spacing_run": args.cue_spacing_run,
            "field_bundle_run": args.field_bundle_run,
            "timing_scorecard_run": args.timing_scorecard_run,
            "dataset_card_run": args.dataset_card_run,
            "readgssi_version": readgssi_version(),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

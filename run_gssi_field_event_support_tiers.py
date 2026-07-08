#!/usr/bin/env python3
"""Build measured-field event support tiers from existing GSSI QC outputs."""

from __future__ import annotations

import argparse
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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_corrected_profile_stack import safe_float  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_GEOMETRY_RUN = "015_gssi51600s_survey_geometry_audit"
DEFAULT_SHORT_ANCHOR_RUN = "037_gssi51600s_content_time_zero_anchor_policy"
DEFAULT_SHORT_INTERVAL_RUN = "049_gssi51600s_supported_interval_visual_qc"
DEFAULT_LONG_VISUAL_RUN = "057_gssi51600s_long_profile_pattern_visual_qc"
DEFAULT_LONG_HOLDOUT_RUN = "058_gssi51600s_long_profile_pattern_holdout_qc"
DEFAULT_BANDLIMITED_RUN = "068_gssi51600s_field_bandlimited_repeatability_audit"
DEFAULT_TIMING_DISCRIMINANT_RUN = "105_gssi51600s_field_timing_discriminant_scorecard"
DEFAULT_HPC_DIMENSIONALITY_RUN = "106_gssi51600s_field_hpc_dimensionality_decision_card"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_support_inputs(dataset_root: Path, runs: dict[str, str]) -> dict[str, dict]:
    return {
        "geometry": read_json(dataset_root / runs["geometry"] / "data" / "survey_geometry_audit_summary.json"),
        "short_anchor": read_json(
            dataset_root
            / runs["short_anchor"]
            / "data"
            / "short_profile_content_time_zero_anchor_summary.json"
        ),
        "short_interval": read_json(
            dataset_root
            / runs["short_interval"]
            / "data"
            / "supported_interval_visual_qc_summary.json"
        ),
        "long_visual": read_json(
            dataset_root
            / runs["long_visual"]
            / "data"
            / "long_profile_pattern_visual_qc_summary.json"
        ),
        "long_holdout": read_json(
            dataset_root
            / runs["long_holdout"]
            / "data"
            / "long_profile_pattern_holdout_qc_summary.json"
        ),
        "bandlimited": read_json(
            dataset_root
            / runs["bandlimited"]
            / "data"
            / "field_bandlimited_repeatability_summary.json"
        ),
        "timing_discriminant": read_json(
            dataset_root
            / runs["timing_discriminant"]
            / "data"
            / "field_timing_discriminant_scorecard_summary.json"
        ),
        "hpc_dimensionality": read_json(
            dataset_root
            / runs["hpc_dimensionality"]
            / "data"
            / "field_hpc_dimensionality_decision_summary.json"
        ),
    }


def fraction(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return float(numerator) / float(denominator)


def tier_rows(summaries: dict[str, dict]) -> list[dict]:
    geometry = summaries["geometry"]
    short_anchor = summaries["short_anchor"]
    short_interval = summaries["short_interval"]
    long_visual = summaries["long_visual"]
    long_holdout = summaries["long_holdout"]
    bandlimited = summaries["bandlimited"]
    timing_discriminant = summaries["timing_discriminant"]
    hpc_dimensionality = summaries["hpc_dimensionality"]
    band_count = max(1, len(bandlimited.get("bands", [])))

    rows = [
        {
            "tier_key": "survey_2d_boundary",
            "profile_group": "all_profiles",
            "support_scope": "survey_geometry",
            "support_tier": "2d_line_profile_boundary",
            "supported_count": safe_float(geometry.get("profile_count")),
            "total_count": safe_float(geometry.get("profile_count")),
            "support_fraction": 1.0,
            "quality_metric_label": "profile_count",
            "quality_metric_value": safe_float(geometry.get("profile_count")),
            "claim_allowed": "independent 2D line-profile QC evidence",
            "claim_blocked": "3D survey grid and measured-data FWI benchmark",
        },
        {
            "tier_key": "short_content_time_zero_anchors",
            "profile_group": "short_014_016",
            "support_scope": "relative_time_zero",
            "support_tier": "content_time_zero_visual_qc",
            "supported_count": safe_float(short_anchor.get("supported_content_anchor_pair_count")),
            "total_count": safe_float(short_anchor.get("event_pair_count")),
            "support_fraction": fraction(
                safe_float(short_anchor.get("supported_content_anchor_pair_count")),
                safe_float(short_anchor.get("event_pair_count")),
            ),
            "quality_metric_label": "min_content_abs_corr",
            "quality_metric_value": safe_float(short_anchor.get("min_content_pair_absolute_correlation")),
            "claim_allowed": "short-pair content-backed relative time-zero visual QC",
            "claim_blocked": "absolute time-zero, radius, cover depth, 3D, or field FWI",
        },
        {
            "tier_key": "short_timing_only_cue",
            "profile_group": "short_014_016",
            "support_scope": "relative_timing",
            "support_tier": "timing_only_limited_qc",
            "supported_count": safe_float(short_anchor.get("timing_only_event_pair_count")),
            "total_count": safe_float(short_anchor.get("event_pair_count")),
            "support_fraction": fraction(
                safe_float(short_anchor.get("timing_only_event_pair_count")),
                safe_float(short_anchor.get("event_pair_count")),
            ),
            "quality_metric_label": "max_all_abs_residual_ns",
            "quality_metric_value": safe_float(short_anchor.get("max_abs_all_timing_residual_ns")),
            "claim_allowed": "short-pair timing-only cue as limited relative-timing evidence",
            "claim_blocked": "content-backed event or geometry/radius evidence",
        },
        {
            "tier_key": "short_supported_stack_intervals",
            "profile_group": "short_014_016",
            "support_scope": "corrected_stack",
            "support_tier": "supported_visual_qc",
            "supported_count": safe_float(short_interval.get("supported_interval_count")),
            "total_count": safe_float(short_interval.get("selected_interval_count")),
            "support_fraction": fraction(
                safe_float(short_interval.get("supported_interval_count")),
                safe_float(short_interval.get("selected_interval_count")),
            ),
            "quality_metric_label": "min_corrected_interval_abs_corr",
            "quality_metric_value": safe_float(short_interval.get("min_corrected_interval_abs_correlation")),
            "claim_allowed": "supported corrected-stack interval visual QC",
            "claim_blocked": "interpretation outside all-window-supported intervals",
        },
        {
            "tier_key": "long_stable_pattern_anchors",
            "profile_group": "long_015_013",
            "support_scope": "pattern_alignment",
            "support_tier": "pattern_only_visual_qc",
            "supported_count": safe_float(long_holdout.get("stable_supported_anchor_count")),
            "total_count": safe_float(long_holdout.get("stable_anchor_count")),
            "support_fraction": fraction(
                safe_float(long_holdout.get("stable_supported_anchor_count")),
                safe_float(long_holdout.get("stable_anchor_count")),
            ),
            "quality_metric_label": "min_shifted_abs_corr",
            "quality_metric_value": safe_float(long_visual.get("min_pattern_shift_abs_correlation")),
            "claim_allowed": "long-pair stable-anchor pattern-only visual QC",
            "claim_blocked": "phase anchor or transferable time-zero correction",
        },
        {
            "tier_key": "long_repeat_limited_holdout",
            "profile_group": "long_015_013",
            "support_scope": "pattern_holdout",
            "support_tier": "pattern_only_holdout_qc",
            "supported_count": safe_float(long_holdout.get("repeat_limited_supported_anchor_count")),
            "total_count": safe_float(long_holdout.get("repeat_limited_anchor_count")),
            "support_fraction": fraction(
                safe_float(long_holdout.get("repeat_limited_supported_anchor_count")),
                safe_float(long_holdout.get("repeat_limited_anchor_count")),
            ),
            "quality_metric_label": "min_repeat_limited_abs_corr",
            "quality_metric_value": safe_float(long_holdout.get("min_repeat_limited_pattern_shift_abs_correlation")),
            "claim_allowed": "long-pair repeat-limited holdout stress QC",
            "claim_blocked": "claim-bearing phase-anchor or geometry evidence",
        },
        {
            "tier_key": "short_bandlimited_repeatability",
            "profile_group": "short_014_016",
            "support_scope": "frequency_band",
            "support_tier": "bandlimited_repeatability_qc",
            "supported_count": safe_float(bandlimited.get("short_supported_band_count")),
            "total_count": float(band_count),
            "support_fraction": fraction(safe_float(bandlimited.get("short_supported_band_count")), float(band_count)),
            "quality_metric_label": "unfiltered_gain",
            "quality_metric_value": safe_float(bandlimited.get("short_unfiltered_abs_correlation_gain")),
            "claim_allowed": "short-pair field QC band choices after relative correction",
            "claim_blocked": "absolute time-zero or inversion evidence",
        },
        {
            "tier_key": "long_bandlimited_pattern",
            "profile_group": "long_015_013",
            "support_scope": "frequency_band",
            "support_tier": "bandlimited_pattern_only_qc",
            "supported_count": safe_float(bandlimited.get("long_pattern_supported_band_count")),
            "total_count": float(band_count),
            "support_fraction": fraction(
                safe_float(bandlimited.get("long_pattern_supported_band_count")),
                float(band_count),
            ),
            "quality_metric_label": "unfiltered_pattern_gain",
            "quality_metric_value": safe_float(bandlimited.get("long_unfiltered_pattern_gain")),
            "claim_allowed": "long-pair pattern-only band support",
            "claim_blocked": "band-limited phase-anchor or absolute time-zero evidence",
        },
        {
            "tier_key": "timing_discriminant_scorecard",
            "profile_group": "all_profiles",
            "support_scope": "timing_family",
            "support_tier": "timing_scope_boundary_qc",
            "supported_count": safe_float(timing_discriminant.get("score_row_count")),
            "total_count": safe_float(timing_discriminant.get("score_row_count")),
            "support_fraction": 1.0 if safe_float(timing_discriminant.get("score_row_count")) else 0.0,
            "quality_metric_label": "short_min_nonraw_matrix_improvement",
            "quality_metric_value": safe_float(timing_discriminant.get("short_min_nonraw_matrix_improvement")),
            "claim_allowed": "timing-family scorecard separating early, short, raw, and long timing evidence",
            "claim_blocked": "absolute time-zero, field FWI, 3D, radius, or cover-depth claims",
        },
        {
            "tier_key": "hpc_dimensionality_boundary",
            "profile_group": "all_profiles",
            "support_scope": "hpc_dimensionality",
            "support_tier": "hpc_2d_boundary_no_hpc",
            "supported_count": 1.0 if hpc_dimensionality.get("ready_for_2d_qc", False) else 0.0,
            "total_count": 1.0,
            "support_fraction": 1.0 if hpc_dimensionality.get("ready_for_2d_qc", False) else 0.0,
            "quality_metric_label": "is_3d_survey",
            "quality_metric_value": 1.0 if hpc_dimensionality.get("is_3d_survey", False) else 0.0,
            "claim_allowed": "local CPU-side independent 2D line-profile QC",
            "claim_blocked": "3D HPC, measured-field FWI, radius recovery, and cover-depth recovery",
        },
        {
            "tier_key": "field_fwi_readiness_blocked",
            "profile_group": "all_profiles",
            "support_scope": "field_fwi_readiness",
            "support_tier": "blocked_not_ready",
            "supported_count": 0.0,
            "total_count": 1.0,
            "support_fraction": 0.0,
            "quality_metric_label": "gpu_priority",
            "quality_metric_value": 0.0,
            "claim_allowed": "none; keep GPU/FWI priority at none",
            "claim_blocked": "field FWI, 3D inversion, radius, and cover-depth claims",
        },
    ]
    return rows


def summarize_tiers(rows: list[dict], summaries: dict[str, dict]) -> dict:
    by_key = {row["tier_key"]: row for row in rows}
    blocked = [row for row in rows if "blocked" in row["support_tier"]]
    short_anchor = summaries["short_anchor"]
    long_holdout = summaries["long_holdout"]
    timing_discriminant = summaries["timing_discriminant"]
    hpc_dimensionality = summaries["hpc_dimensionality"]
    return {
        "policy_label": "field_event_support_tiers_timing_discriminant_hpc_2d_qc_ready_not_fwi",
        "tier_row_count": len(rows),
        "blocked_row_count": len(blocked),
        "short_content_anchor_supported_count": safe_float(
            short_anchor.get("supported_content_anchor_pair_count")
        ),
        "short_event_pair_count": safe_float(short_anchor.get("event_pair_count")),
        "short_content_anchor_support_fraction": safe_float(
            by_key["short_content_time_zero_anchors"]["support_fraction"]
        ),
        "short_timing_only_event_count": safe_float(short_anchor.get("timing_only_event_pair_count")),
        "long_stable_supported_anchor_count": safe_float(long_holdout.get("stable_supported_anchor_count")),
        "long_repeat_limited_supported_anchor_count": safe_float(
            long_holdout.get("repeat_limited_supported_anchor_count")
        ),
        "long_pattern_total_supported_anchor_count": safe_float(
            long_holdout.get("stable_supported_anchor_count")
        )
        + safe_float(long_holdout.get("repeat_limited_supported_anchor_count")),
        "bandlimited_short_supported_band_count": safe_float(
            summaries["bandlimited"].get("short_supported_band_count")
        ),
        "bandlimited_long_pattern_supported_band_count": safe_float(
            summaries["bandlimited"].get("long_pattern_supported_band_count")
        ),
        "timing_discriminant_included": True,
        "timing_discriminant_score_row_count": safe_float(timing_discriminant.get("score_row_count")),
        "timing_discriminant_short_nonraw_supported_count": safe_float(
            timing_discriminant.get("short_nonraw_supported_count")
        ),
        "timing_discriminant_long_reject_short_transfer_count": safe_float(
            timing_discriminant.get("long_reject_short_transfer_count")
        ),
        "timing_discriminant_absolute_time_zero_ready": bool(
            timing_discriminant.get("absolute_time_zero_ready", False)
        ),
        "hpc_dimensionality_included": True,
        "hpc_dimensionality_field_geometry_type": hpc_dimensionality.get("field_geometry_type", ""),
        "hpc_dimensionality_ready_for_2d_qc": bool(hpc_dimensionality.get("ready_for_2d_qc", False)),
        "hpc_dimensionality_ready_for_3d_hpc": bool(hpc_dimensionality.get("ready_for_3d_hpc", False)),
        "hpc_dimensionality_ready_for_field_fwi": bool(hpc_dimensionality.get("ready_for_field_fwi", False)),
        "hpc_dimensionality_field_hpc_priority": hpc_dimensionality.get("field_hpc_priority", ""),
        "survey_classification": summaries["geometry"].get("classification", ""),
        "field_fwi_ready": False,
        "field_gpu_fwi_priority": "none",
        "ready_for_manuscript_field_support_table": True,
        "decision": (
            "Use this event-support tier table as measured-field supplement "
            "evidence only. The short pair has content-backed relative "
            "time-zero visual-QC support for two of three event pairs, while "
            "the long pair has pattern-only support across stable and "
            "repeat-limited anchors. The timing-discriminant scorecard and "
            "HPC dimensionality decision keep timing families and 2D-only scope "
            "separate. Missing survey grid metadata and missing long-profile "
            "phase anchors still block 3D, radius, cover-depth, and measured-data "
            "FWI claims."
        ),
    }


def plot_tiers(rows: list[dict], summary: dict, save_path: Path) -> str:
    label_map = {
        "survey_2d_boundary": "survey\n2D boundary",
        "short_content_time_zero_anchors": "short\ncontent anchors",
        "short_timing_only_cue": "short\ntiming-only cue",
        "short_supported_stack_intervals": "short\nsupported intervals",
        "long_stable_pattern_anchors": "long\nstable pattern",
        "long_repeat_limited_holdout": "long\nholdout pattern",
        "short_bandlimited_repeatability": "short\nbandlimited",
        "long_bandlimited_pattern": "long\nbandlimited",
        "timing_discriminant_scorecard": "timing\ndiscriminants",
        "hpc_dimensionality_boundary": "HPC\n2D boundary",
        "field_fwi_readiness_blocked": "field FWI\nblocked",
    }
    labels = [label_map.get(row["tier_key"], row["tier_key"].replace("_", "\n")) for row in rows]
    values = np.asarray([safe_float(row["support_fraction"]) for row in rows], dtype=np.float64)
    color_map = {
        "2d_line_profile_boundary": "#6b6b6b",
        "content_time_zero_visual_qc": "#2f9d55",
        "timing_only_limited_qc": "#d99a19",
        "supported_visual_qc": "#4c78a8",
        "pattern_only_visual_qc": "#7f3c8d",
        "pattern_only_holdout_qc": "#9467bd",
        "bandlimited_repeatability_qc": "#1f77b4",
        "bandlimited_pattern_only_qc": "#17becf",
        "timing_scope_boundary_qc": "#e15759",
        "hpc_2d_boundary_no_hpc": "#8cd17d",
        "blocked_not_ready": "#b33a3a",
    }
    colors = [color_map.get(row["support_tier"], "#999999") for row in rows]
    y = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(13.5, 8.6), constrained_layout=True)
    ax.barh(y, values, color=colors)
    ax.set_yticks(y, labels)
    ax.tick_params(axis="y", labelsize=9)
    ax.invert_yaxis()
    ax.set_xlim(0.0, 1.05)
    ax.set_xlabel("supported / total")
    ax.set_title("Measured GSSI field event support tiers")
    ax.grid(axis="x", color="#dddddd", linewidth=0.6)
    for idx, row in enumerate(rows):
        ax.text(
            min(values[idx] + 0.025, 1.0),
            idx,
            f"{safe_float(row['supported_count']):.0f}/{safe_float(row['total_count']):.0f}",
            va="center",
            ha="left" if values[idx] < 0.92 else "right",
            fontsize=9,
        )
    ax.text(
        0.01,
        0.02,
        f"policy={summary['policy_label']} | gpu/fwi={summary['field_gpu_fwi_priority']} | survey={summary['survey_classification']}",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
    )
    fig.suptitle("Field support tiers are QC evidence, not field FWI or 3D inversion", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--geometry-run", default=DEFAULT_GEOMETRY_RUN)
    parser.add_argument("--short-anchor-run", default=DEFAULT_SHORT_ANCHOR_RUN)
    parser.add_argument("--short-interval-run", default=DEFAULT_SHORT_INTERVAL_RUN)
    parser.add_argument("--long-visual-run", default=DEFAULT_LONG_VISUAL_RUN)
    parser.add_argument("--long-holdout-run", default=DEFAULT_LONG_HOLDOUT_RUN)
    parser.add_argument("--bandlimited-run", default=DEFAULT_BANDLIMITED_RUN)
    parser.add_argument("--timing-discriminant-run", default=DEFAULT_TIMING_DISCRIMINANT_RUN)
    parser.add_argument("--hpc-dimensionality-run", default=DEFAULT_HPC_DIMENSIONALITY_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_event_support_tiers")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    runs = {
        "geometry": args.geometry_run,
        "short_anchor": args.short_anchor_run,
        "short_interval": args.short_interval_run,
        "long_visual": args.long_visual_run,
        "long_holdout": args.long_holdout_run,
        "bandlimited": args.bandlimited_run,
        "timing_discriminant": args.timing_discriminant_run,
        "hpc_dimensionality": args.hpc_dimensionality_run,
    }
    summaries = load_support_inputs(dataset_root, runs)
    rows = tier_rows(summaries)
    summary = summarize_tiers(rows, summaries)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_event_support_tiers.csv"
    summary_json = data_dir / "field_event_support_tiers_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_tiers(rows, summary, figures_dir / "field_event_support_tiers.png"))

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
        "gssi_field_event_support_tiers",
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

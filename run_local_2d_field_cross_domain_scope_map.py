#!/usr/bin/env python3
"""Map synthetic 2D and measured-field evidence into separated claim scopes."""

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
from run_local_2d_field_manuscript_evidence_audit import (  # noqa: E402
    DEFAULT_FIELD_BUNDLE_RUN,
    DEFAULT_FIELD_POLICY_RUN,
    DEFAULT_SYNTHETIC_BUNDLE_RUN,
    DEFAULT_SYNTHETIC_NEXT_MATRIX_RUN,
)
from run_local_2d_field_manuscript_table_pack import (  # noqa: E402
    DEFAULT_AUDIT_RUN,
    DEFAULT_FIELD_SOURCE_NOTES_RUN,
    DEFAULT_SYNTHETIC_SOURCE_NOTES_RUN,
)
from run_synthetic_2d_publication_figure_bundle import DEFAULT_EXPERIMENT_ROOT  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SYNTHETIC_RESOLUTION_RUN = "1307_synthetic_2d_resolution_claim_map_current"
DEFAULT_FIELD_CUE_SPACING_RUN = "094_gssi51600s_field_cue_spacing_sensitivity_audit"
DEFAULT_FIELD_TIMING_WINDOW_RUN = "101_gssi51600s_field_timing_window_family_classification"
DEFAULT_TABLE_PACK_RUN = "124_local_2d_field_manuscript_table_pack_post_controlled_prior_budget"


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


def no_gpu_value(value) -> bool:
    return str(value).strip().lower() in {"", "none", "none_now", "no_gpu_required"}


def row_by_key(rows: list[dict], key: str) -> dict:
    for row in rows:
        if row.get("map_key") == key:
            return row
    return {}


def fraction(numerator, denominator) -> float:
    den = safe_float(denominator, 0.0)
    if den <= 0:
        return math.nan
    return safe_float(numerator, 0.0) / den


def build_scope_rows(
    *,
    resolution_summary: dict,
    resolution_rows: list[dict],
    synthetic_bundle: dict,
    synthetic_next: dict,
    field_cue_spacing: dict,
    field_timing_window: dict,
    field_bundle: dict,
    field_policy: dict,
    table_pack: dict,
) -> list[dict]:
    physical = row_by_key(resolution_rows, "physical_nonoverlap_guardrail")
    close14 = row_by_key(
        resolution_rows,
        "target2_close14_source5_txrx45_objective_limit",
    )
    close50 = row_by_key(resolution_rows, "target2_close50_linear29p5_seed_frequency")
    current_queue = row_by_key(resolution_rows, "current_synthetic_gpu_queue")

    field_min_spacing = safe_float(
        field_cue_spacing.get("min_same_time_lateral_spacing_mm_across_thresholds")
    )
    synthetic_close_context = safe_float(field_cue_spacing.get("synthetic_close_spacing_context_max_mm"))
    physical_guardrail = safe_float(resolution_summary.get("physical_nonoverlap_guardrail_mm"))
    close14_near_tie_fraction = fraction(close14.get("support_count"), close14.get("total_count"))
    close50_clean_fraction = fraction(close50.get("support_count"), close50.get("total_count"))
    short_timing_fraction = fraction(
        field_timing_window.get("short_nonraw_supported_count"),
        field_timing_window.get("short_nonraw_row_count"),
    )
    long_reject_fraction = fraction(
        field_timing_window.get("long_reject_short_transfer_row_count"),
        field_timing_window.get("long_row_count"),
    )

    return [
        {
            "scope_key": "synthetic_known_truth_resolution_only",
            "paper_section": "synthetic_resolution",
            "synthetic_evidence": (
                f"physical_nonoverlap_guardrail_mm={physical_guardrail:.3f}; "
                f"claim={physical.get('claim_status', '')}"
            ),
            "field_evidence": (
                f"field_min_same_time_spacing_mm={field_min_spacing:.3f}; "
                f"field_resolution_ready={field_cue_spacing.get('ready_for_resolution_benchmark', False)}"
            ),
            "allowed_joint_claim": (
                "Synthetic known-truth runs support controlled 2D resolution and ambiguity claims; "
                "field cue spacings can be cited only as measured context."
            ),
            "blocked_joint_claim": (
                "Do not claim the measured GSSI field data validates the synthetic close-spacing "
                "resolution threshold."
            ),
            "decision": "synthetic_result_field_context_only",
            "primary_metric": physical_guardrail,
            "gpu_priority": "none",
        },
        {
            "scope_key": "field_spacing_outside_synthetic_stress_regime",
            "paper_section": "field_context",
            "synthetic_evidence": f"synthetic_close_context_max_mm={synthetic_close_context:.3f}",
            "field_evidence": f"min_same_time_lateral_spacing_mm={field_min_spacing:.3f}",
            "allowed_joint_claim": (
                "The measured visible same-time cue spacings are wider than the synthetic close-spacing "
                "stress scale."
            ),
            "blocked_joint_claim": "Do not use this field dataset as a known-truth 25-30 mm spacing benchmark.",
            "decision": "field_context_not_resolution_benchmark",
            "primary_metric": field_min_spacing / synthetic_close_context if synthetic_close_context else math.nan,
            "gpu_priority": "none",
        },
        {
            "scope_key": "target2_close14_objective_limit",
            "paper_section": "synthetic_objective_uniqueness",
            "synthetic_evidence": (
                f"near_tie_count_at_0p5={safe_float(close14.get('primary_metric_value')):.0f}; "
                f"near_tie_fraction={close14_near_tie_fraction:.3f}"
            ),
            "field_evidence": "not field-testable in this dataset",
            "allowed_joint_claim": "Truth is selected strongly in the controlled close14 branch.",
            "blocked_joint_claim": "Do not call close14 objective-unique because the +1 mm competitor persists.",
            "decision": "synthetic_near_tie_caveat",
            "primary_metric": close14_near_tie_fraction,
            "gpu_priority": "none",
        },
        {
            "scope_key": "target2_close50_linear29p5_seed_frequency",
            "paper_section": "synthetic_acquisition_caveat",
            "synthetic_evidence": (
                f"strict_clean_seed_fraction={close50_clean_fraction:.3f}; "
                f"ambiguous_seeds={resolution_summary.get('target2_close50_ambiguous_seed_values', '')}"
            ),
            "field_evidence": "not field-testable in this dataset",
            "allowed_joint_claim": "The linear 29.5 mm branch is exact/strong across three seeds.",
            "blocked_joint_claim": "Do not promote 29.5 mm to a clean replicated sub-30 mm threshold.",
            "decision": "synthetic_seed_frequency_caveat",
            "primary_metric": close50_clean_fraction,
            "gpu_priority": "none",
        },
        {
            "scope_key": "field_timing_window_family_boundary",
            "paper_section": "field_timing",
            "synthetic_evidence": "separate from known-truth synthetic resolution claims",
            "field_evidence": (
                f"early_near_zero={safe_float(field_timing_window.get('early_strict_near_zero_lag_row_count')):.0f}/"
                f"{safe_float(field_timing_window.get('early_strict_row_count')):.0f}; "
                f"short_supported={safe_float(field_timing_window.get('short_nonraw_supported_count')):.0f}/"
                f"{safe_float(field_timing_window.get('short_nonraw_row_count')):.0f}; "
                f"long_reject={safe_float(field_timing_window.get('long_reject_short_transfer_row_count')):.0f}/"
                f"{safe_float(field_timing_window.get('long_row_count')):.0f}"
            ),
            "allowed_joint_claim": (
                "Field timing windows support a scoped timing/repeatability supplement and keep "
                "short, early, and long timing families separate."
            ),
            "blocked_joint_claim": "Do not use timing-window support as absolute time-zero or field FWI input.",
            "decision": "field_timing_boundary_only",
            "primary_metric": min(short_timing_fraction, long_reject_fraction),
            "gpu_priority": "none",
        },
        {
            "scope_key": "detector_controlled_prior_refinement_scope",
            "paper_section": "synthetic_detector_refinement",
            "synthetic_evidence": (
                "controlled_prior_ready="
                f"{table_pack.get('detector_radius_material_prior_controlled_ready', False)}; "
                "detector_inferred_ready="
                f"{table_pack.get('detector_radius_material_prior_detector_inferred_ready', False)}; "
                "fixed_fine_points="
                f"{safe_float(table_pack.get('detector_controlled_prior_refinement_fixed_fine_points'), 0.0):.0f}; "
                "permutation_multiplier="
                f"{safe_float(table_pack.get('detector_controlled_prior_refinement_permutation_multiplier'), 0.0):.1f}"
            ),
            "field_evidence": (
                f"field_fwi_ready={table_pack.get('field_collection_handoff_ready_field_fwi', False)}; "
                f"field_3d_hpc_ready={table_pack.get('field_collection_handoff_ready_3d_hpc', False)}"
            ),
            "allowed_joint_claim": (
                "The detector seed work has a controlled synthetic radius/material prior budget for "
                "design sizing."
            ),
            "blocked_joint_claim": (
                "Do not treat the controlled prior as detector-inferred radius/material, field transfer, "
                "refinement launch, field FWI, 3D/HPC, or GPU authorization."
            ),
            "decision": "controlled_prior_budget_no_launch",
            "primary_metric": safe_float(
                table_pack.get("detector_controlled_prior_refinement_permutation_multiplier"), 0.0
            ),
            "gpu_priority": "none",
        },
        {
            "scope_key": "current_no_gpu_queue",
            "paper_section": "compute_policy",
            "synthetic_evidence": (
                f"immediate_gpu={safe_float(synthetic_next.get('immediate_gpu_priority_count'), 0.0):.0f}; "
                f"conditional_gpu={safe_float(synthetic_next.get('conditional_gpu_candidate_count'), 0.0):.0f}; "
                f"resolution_queue={current_queue.get('claim_status', '')}"
            ),
            "field_evidence": (
                f"field_bundle_gpu={field_bundle.get('gpu_priority', '')}; "
                f"field_policy_gpu={field_policy.get('publication_claim_bundle_gpu_priority', '')}"
            ),
            "allowed_joint_claim": "Current manuscript tables are ready without a local GPU run.",
            "blocked_joint_claim": "Do not launch broad GPU sweeps without a new objective or calibrated geometry question.",
            "decision": "no_current_gpu_action",
            "primary_metric": 0.0,
            "gpu_priority": "none",
        },
        {
            "scope_key": "current_manuscript_package",
            "paper_section": "manuscript_tables",
            "synthetic_evidence": (
                f"synthetic_figures={safe_float(synthetic_bundle.get('figure_count')):.0f}; "
                f"synthetic_claims={safe_float(synthetic_bundle.get('claim_boundary_count')):.0f}"
            ),
            "field_evidence": (
                f"field_figures={safe_float(field_bundle.get('figure_row_count')):.0f}; "
                f"field_claims={safe_float(field_bundle.get('claim_boundary_count')):.0f}; "
                f"table_ready={table_pack.get('ready_for_manuscript_table_use', False)}"
            ),
            "allowed_joint_claim": "Use the current CSV tables as manuscript planning evidence with separated scopes.",
            "blocked_joint_claim": "Do not merge synthetic known-truth and measured-field QC into one validation claim.",
            "decision": "ready_scope_separated_package",
            "primary_metric": 1.0 if table_pack.get("ready_for_manuscript_table_use", False) else 0.0,
            "gpu_priority": "none",
        },
    ]


def summarize_scope(
    rows: list[dict],
    *,
    field_cue_spacing: dict,
    field_timing_window: dict,
    synthetic_next: dict,
    field_bundle: dict,
    field_policy: dict,
    table_pack: dict,
) -> dict:
    field_min_spacing = safe_float(
        field_cue_spacing.get("min_same_time_lateral_spacing_mm_across_thresholds")
    )
    synthetic_close_context = safe_float(field_cue_spacing.get("synthetic_close_spacing_context_max_mm"))
    short_supported = safe_float(field_timing_window.get("short_nonraw_supported_count"), 0.0)
    short_rows = safe_float(field_timing_window.get("short_nonraw_row_count"), 0.0)
    long_reject = safe_float(field_timing_window.get("long_reject_short_transfer_row_count"), 0.0)
    long_rows = safe_float(field_timing_window.get("long_row_count"), 0.0)
    no_gpu = (
        no_gpu_value(synthetic_next.get("gpu_priority", ""))
        and no_gpu_value(field_bundle.get("gpu_priority", ""))
        and no_gpu_value(field_policy.get("publication_claim_bundle_gpu_priority", ""))
        and no_gpu_value(table_pack.get("gpu_priority", ""))
    )
    ready = (
        bool(table_pack.get("ready_for_manuscript_table_use", False))
        and bool(field_cue_spacing.get("ready_for_field_context", False))
        and not bool(field_cue_spacing.get("ready_for_resolution_benchmark", False))
        and not bool(field_timing_window.get("absolute_time_zero_ready", False))
        and not bool(field_timing_window.get("field_fwi_ready", False))
        and not bool(table_pack.get("detector_radius_material_prior_detector_inferred_ready", False))
        and not bool(table_pack.get("detector_controlled_prior_refinement_launch_ready", False))
        and not bool(table_pack.get("detector_controlled_prior_refinement_ready_for_fwi", False))
        and no_gpu
    )
    return {
        "policy_label": (
            "local_2d_field_cross_domain_scope_map_ready_no_gpu"
            if ready
            else "local_2d_field_cross_domain_scope_map_review_required"
        ),
        "scope_row_count": len(rows),
        "field_min_same_time_spacing_mm": field_min_spacing,
        "synthetic_close_spacing_context_max_mm": synthetic_close_context,
        "field_to_synthetic_spacing_ratio": (
            field_min_spacing / synthetic_close_context if synthetic_close_context else math.nan
        ),
        "field_ready_for_resolution_benchmark": bool(
            field_cue_spacing.get("ready_for_resolution_benchmark", False)
        ),
        "field_timing_short_nonraw_supported_count": short_supported,
        "field_timing_short_nonraw_row_count": short_rows,
        "field_timing_short_nonraw_supported_fraction": fraction(short_supported, short_rows),
        "field_timing_long_reject_short_transfer_count": long_reject,
        "field_timing_long_row_count": long_rows,
        "field_timing_long_reject_short_transfer_fraction": fraction(long_reject, long_rows),
        "synthetic_immediate_gpu_priority_count": safe_float(
            synthetic_next.get("immediate_gpu_priority_count"), 0.0
        ),
        "synthetic_conditional_gpu_candidate_count": safe_float(
            synthetic_next.get("conditional_gpu_candidate_count"), 0.0
        ),
        "field_absolute_time_zero_ready": bool(field_timing_window.get("absolute_time_zero_ready", False)),
        "field_fwi_ready": bool(field_timing_window.get("field_fwi_ready", False)),
        "detector_controlled_prior_ready": bool(
            table_pack.get("detector_radius_material_prior_controlled_ready", False)
        ),
        "detector_inferred_radius_material_ready": bool(
            table_pack.get("detector_radius_material_prior_detector_inferred_ready", False)
        ),
        "detector_controlled_prior_fixed_fine_points": safe_float(
            table_pack.get("detector_controlled_prior_refinement_fixed_fine_points"), 0.0
        ),
        "detector_controlled_prior_permutation_multiplier": safe_float(
            table_pack.get("detector_controlled_prior_refinement_permutation_multiplier"), 0.0
        ),
        "detector_controlled_prior_launch_ready": bool(
            table_pack.get("detector_controlled_prior_refinement_launch_ready", False)
        ),
        "detector_controlled_prior_fwi_ready": bool(
            table_pack.get("detector_controlled_prior_refinement_ready_for_fwi", False)
        ),
        "manuscript_table_ready": bool(table_pack.get("ready_for_manuscript_table_use", False)),
        "gpu_priority": "none" if no_gpu else "review",
        "ready_for_manuscript_scope_table": ready,
        "decision": (
            "Use this cross-domain scope map to keep synthetic known-truth resolution, "
            "measured-field timing/spacing QC, and no-GPU/no-FWI boundaries separated."
        ),
    }


def plot_scope_map(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [
        "field/synth\nspacing ratio",
        "field short\ntiming support",
        "field long\nreject short",
        "synthetic\nimmediate GPU",
        "synthetic\nconditional GPU",
        "table\nready",
    ]
    values = [
        safe_float(summary.get("field_to_synthetic_spacing_ratio"), 0.0),
        safe_float(summary.get("field_timing_short_nonraw_supported_fraction"), 0.0),
        safe_float(summary.get("field_timing_long_reject_short_transfer_fraction"), 0.0),
        safe_float(summary.get("synthetic_immediate_gpu_priority_count"), 0.0),
        safe_float(summary.get("synthetic_conditional_gpu_candidate_count"), 0.0),
        1.0 if summary.get("manuscript_table_ready", False) else 0.0,
    ]
    colors = ["#4c78a8", "#2f9d55", "#2f9d55", "#c7302b", "#c7302b", "#6b6b6b"]
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 4.6), constrained_layout=True)
    axes[0].bar(np.arange(len(values)), values, color=colors, width=0.62)
    axes[0].set_xticks(np.arange(len(values)), labels)
    axes[0].set_title("Scope gate metrics")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].set_ylim(0, max(2.1, max(values) + 0.25))
    for idx, value in enumerate(values):
        axes[0].text(idx, value + 0.04, f"{value:.2f}", ha="center", va="bottom", fontsize=8)

    row_labels = [row["scope_key"].replace("_", "\n") for row in rows]
    row_values = [safe_float(row.get("primary_metric"), 0.0) for row in rows]
    axes[1].barh(np.arange(len(rows)), row_values, color="#8c564b", height=0.58)
    axes[1].set_yticks(np.arange(len(rows)), row_labels, fontsize=8)
    axes[1].invert_yaxis()
    axes[1].set_title("Primary metric by scope row")
    axes[1].grid(axis="x", color="#dddddd", linewidth=0.6)
    fig.suptitle(f"Local 2D/field cross-domain scope: {summary['policy_label']}", fontweight="bold")
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
                "## `local_2d_field_cross_domain_scope_map.png`",
                "",
                "This is a CPU-only manuscript scope map. It combines current",
                "synthetic 2D known-truth policy summaries with measured-field",
                "spacing and timing QC summaries.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Scope rows: `{summary['scope_row_count']}`.",
                f"Field/synthetic spacing ratio: `{summary['field_to_synthetic_spacing_ratio']:.3f}`.",
                f"Field resolution benchmark ready: `{summary['field_ready_for_resolution_benchmark']}`.",
                f"Field FWI ready: `{summary['field_fwi_ready']}`.",
                f"Detector controlled-prior ready: `{summary['detector_controlled_prior_ready']}`.",
                f"Detector-inferred radius/material ready: `{summary['detector_inferred_radius_material_ready']}`.",
                f"Detector controlled-prior fixed fine points: `{summary['detector_controlled_prior_fixed_fine_points']:.0f}`.",
                f"Detector controlled-prior launch ready: `{summary['detector_controlled_prior_launch_ready']}`.",
                f"Detector controlled-prior FWI ready: `{summary['detector_controlled_prior_fwi_ready']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Inputs and outputs:",
                "",
                f"- Scope rows: `{rows_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                f"- Figure validation: `{validation_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "The figure does not merge synthetic known-truth resolution claims",
                "with measured-field QC. It explicitly blocks field resolution",
                "benchmark, absolute time-zero, 3D, cover-depth, radius, and field",
                "FWI claims from the current measured GSSI dataset.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default=DEFAULT_EXPERIMENT_ROOT)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--synthetic-resolution-run", default=DEFAULT_SYNTHETIC_RESOLUTION_RUN)
    parser.add_argument("--synthetic-bundle-run", default=DEFAULT_SYNTHETIC_BUNDLE_RUN)
    parser.add_argument("--synthetic-next-matrix-run", default=DEFAULT_SYNTHETIC_NEXT_MATRIX_RUN)
    parser.add_argument("--field-cue-spacing-run", default=DEFAULT_FIELD_CUE_SPACING_RUN)
    parser.add_argument("--field-timing-window-run", default=DEFAULT_FIELD_TIMING_WINDOW_RUN)
    parser.add_argument("--field-bundle-run", default=DEFAULT_FIELD_BUNDLE_RUN)
    parser.add_argument("--field-policy-run", default=DEFAULT_FIELD_POLICY_RUN)
    parser.add_argument("--table-pack-run", default=DEFAULT_TABLE_PACK_RUN)
    parser.add_argument("--audit-run", default=DEFAULT_AUDIT_RUN)
    parser.add_argument("--synthetic-source-notes-run", default=DEFAULT_SYNTHETIC_SOURCE_NOTES_RUN)
    parser.add_argument("--field-source-notes-run", default=DEFAULT_FIELD_SOURCE_NOTES_RUN)
    parser.add_argument("--run-name", default="local_2d_field_cross_domain_scope_map")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    experiment_root = Path(args.experiment_root)
    field_root = field_dataset_output_root(args.field_root, args.dataset_id)
    table_root = Path("outputs/summary_tables") / args.table_pack_run

    resolution_dir = experiment_root / args.synthetic_resolution_run
    synthetic_bundle_dir = experiment_root / args.synthetic_bundle_run
    synthetic_next_dir = experiment_root / args.synthetic_next_matrix_run
    field_cue_dir = field_root / args.field_cue_spacing_run
    field_timing_dir = field_root / args.field_timing_window_run
    field_bundle_dir = field_root / args.field_bundle_run
    field_policy_dir = field_root / args.field_policy_run

    resolution_summary = read_json(
        resolution_dir / "data/synthetic_2d_resolution_claim_map_summary.json"
    )
    resolution_rows = read_csv_rows(
        resolution_dir / "data/synthetic_2d_resolution_claim_map_rows.csv"
    )
    synthetic_bundle = read_json(
        synthetic_bundle_dir / "data/synthetic_2d_publication_figure_bundle_summary.json"
    )
    synthetic_next = read_json(
        synthetic_next_dir / "data/synthetic_2d_next_question_matrix_summary.json"
    )
    field_cue_spacing = read_json(
        field_cue_dir / "data/field_cue_spacing_threshold_sensitivity_summary.json"
    )
    field_timing_window = read_json(
        field_timing_dir / "data/field_timing_window_family_classification_summary.json"
    )
    field_bundle = read_json(field_bundle_dir / "data/field_publication_claim_bundle_summary.json")
    field_policy = read_json(field_policy_dir / "data/field_dataset_policy_summary.json")
    table_pack = read_json(table_root / "data/local_2d_field_manuscript_table_pack_summary.json")

    rows = build_scope_rows(
        resolution_summary=resolution_summary,
        resolution_rows=resolution_rows,
        synthetic_bundle=synthetic_bundle,
        synthetic_next=synthetic_next,
        field_cue_spacing=field_cue_spacing,
        field_timing_window=field_timing_window,
        field_bundle=field_bundle,
        field_policy=field_policy,
        table_pack=table_pack,
    )
    summary = summarize_scope(
        rows,
        field_cue_spacing=field_cue_spacing,
        field_timing_window=field_timing_window,
        synthetic_next=synthetic_next,
        field_bundle=field_bundle,
        field_policy=field_policy,
        table_pack=table_pack,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root="outputs/summary_tables"))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_field_cross_domain_scope_rows.csv"
    summary_json = data_dir / "local_2d_field_cross_domain_scope_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_field_cross_domain_scope_map.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    plot_scope_map(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "scope_rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, rows_csv, summary_json, validation_csv)
    write_run_manifest(
        str(outdir),
        "local_2d_field_cross_domain_scope_map",
        {
            "synthetic_resolution_run": args.synthetic_resolution_run,
            "synthetic_bundle_run": args.synthetic_bundle_run,
            "synthetic_next_matrix_run": args.synthetic_next_matrix_run,
            "field_cue_spacing_run": args.field_cue_spacing_run,
            "field_timing_window_run": args.field_timing_window_run,
            "field_bundle_run": args.field_bundle_run,
            "field_policy_run": args.field_policy_run,
            "table_pack_run": args.table_pack_run,
            "audit_run": args.audit_run,
            "synthetic_source_notes_run": args.synthetic_source_notes_run,
            "field_source_notes_run": args.field_source_notes_run,
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

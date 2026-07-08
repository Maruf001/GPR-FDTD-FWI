#!/usr/bin/env python3
"""Audit readiness of detector/hyperbola baselines for the local 2D manuscript."""

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


DEFAULT_SINGLE_DETECTOR_RUNS = (
    "112_single_rebar_detection_depth_radius_noise_benchmark,"
    "113_single_rebar_detection_source_mismatch_benchmark"
)
DEFAULT_TWO_STAGE_RUN = "134_two_stage_refinement_aggregate_118_132_interval_runtime"
DEFAULT_ASSIGNMENT_RUNS = (
    "452_detection_assignment_variable_depth_radius_451,"
    "463_detection_assignment_variable_depth_radius_462,"
    "473_detection_assignment_variable_depth_radius_472"
)
DEFAULT_FIELD_HYPERBOLA_RUN = "003_gssi51600s_hyperbola_calibration_qc"
DEFAULT_FIELD_DEGENERACY_RUN = "086_gssi51600s_field_hyperbola_timezero_degeneracy_audit"
DEFAULT_CONTRIBUTION_RUN = "014_local_2d_manuscript_contribution_matrix_post_field_viability"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_run_list(text: str) -> list[str]:
    return [part.strip() for part in str(text).split(",") if part.strip()]


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def fraction(numerator: float, denominator: float) -> float:
    denominator = safe_float(denominator, 0.0)
    if denominator <= 0:
        return math.nan
    return safe_float(numerator, 0.0) / denominator


def audit_row(
    *,
    baseline_key: str,
    domain: str,
    status: str,
    readiness_score: float,
    evidence_count: float,
    primary_metric_label: str,
    primary_metric_value: float,
    ready_use: str,
    blocked_use: str,
    next_action: str,
    gpu_priority: str = "none",
) -> dict:
    return {
        "baseline_key": baseline_key,
        "domain": domain,
        "status": status,
        "readiness_score": min(1.0, max(0.0, safe_float(readiness_score, 0.0))),
        "evidence_count": safe_float(evidence_count, 0.0),
        "primary_metric_label": primary_metric_label,
        "primary_metric_value": safe_float(primary_metric_value, 0.0),
        "ready_use": ready_use,
        "blocked_use": blocked_use,
        "next_action": next_action,
        "gpu_priority": gpu_priority,
    }


def summarize_single_detector(summaries: list[dict]) -> dict:
    scenario_count = 0.0
    detected_count = 0.0
    hit_count = 0.0
    max_x_error = 0.0
    max_z_error = 0.0
    for summary in summaries:
        aggregate = summary.get("aggregate", {})
        scenario_count += safe_float(aggregate.get("scenario_count"), 0.0)
        detected_count += safe_float(aggregate.get("detected_count"), 0.0)
        hit_count += safe_float(aggregate.get("hit_count"), 0.0)
        max_x_error = max(max_x_error, safe_float(aggregate.get("max_x_error_mm"), 0.0))
        max_z_error = max(max_z_error, safe_float(aggregate.get("max_z_error_mm"), 0.0))
    return {
        "scenario_count": scenario_count,
        "detected_count": detected_count,
        "hit_count": hit_count,
        "hit_rate": fraction(hit_count, scenario_count),
        "detected_fraction": fraction(detected_count, scenario_count),
        "max_x_error_mm": max_x_error,
        "max_z_error_mm": max_z_error,
    }


def summarize_two_stage(rows: list[dict]) -> dict:
    exact_rows = [
        row
        for row in rows
        if safe_float(row.get("x_error_mm"), 999.0) == 0.0
        and safe_float(row.get("z_error_mm"), 999.0) == 0.0
        and safe_float(row.get("radius_error_mm"), 999.0) == 0.0
    ]
    strong = [row for row in rows if row.get("confidence") == "strong"]
    weak = [row for row in rows if row.get("confidence") == "weak"]
    max_wall = max((safe_float(row.get("overall_wall_s"), 0.0) for row in rows), default=0.0)
    return {
        "row_count": len(rows),
        "exact_count": len(exact_rows),
        "exact_fraction": fraction(len(exact_rows), len(rows)),
        "strong_count": len(strong),
        "weak_count": len(weak),
        "weak_fraction": fraction(len(weak), len(rows)),
        "max_wall_s": max_wall,
    }


def summarize_assignments(summaries: list[dict]) -> dict:
    total_assigned = 0.0
    run_count = len(summaries)
    min_score = math.nan
    for summary in summaries:
        total_assigned += safe_float(summary.get("count"), 0.0)
        for row in summary.get("assigned_rows", []):
            score = safe_float(row.get("normalized_score"))
            if math.isfinite(score):
                min_score = score if not math.isfinite(min_score) else min(min_score, score)
    return {
        "run_count": run_count,
        "assigned_count": total_assigned,
        "assigned_per_run": fraction(total_assigned, run_count),
        "min_normalized_score": min_score,
    }


def build_audit_rows(
    *,
    single_detector: dict,
    two_stage: dict,
    assignments: dict,
    field_hyperbola: dict,
    field_degeneracy: dict,
    contribution_summary: dict,
) -> list[dict]:
    return [
        audit_row(
            baseline_key="single_rebar_hyperbola_detector_location",
            domain="synthetic_detector",
            status="ready_location_baseline",
            readiness_score=single_detector["hit_rate"],
            evidence_count=single_detector["scenario_count"],
            primary_metric_label="single_detector_hit_rate",
            primary_metric_value=single_detector["hit_rate"],
            ready_use="Single-rebar x/z detector baseline over depth, radius, noise, and source mismatch.",
            blocked_use="Radius recovery or close multi-rebar objective-ambiguity baseline.",
            next_action="Use as a location-seed baseline, not as the final comparator for radius/ambiguity claims.",
        ),
        audit_row(
            baseline_key="single_rebar_detector_seeded_refinement",
            domain="synthetic_pipeline",
            status="ready_pipeline_baseline",
            readiness_score=two_stage["exact_fraction"],
            evidence_count=two_stage["row_count"],
            primary_metric_label="two_stage_exact_fraction",
            primary_metric_value=two_stage["exact_fraction"],
            ready_use="Detector-to-refinement single-rebar pipeline baseline with exact x/z/r rows.",
            blocked_use="General multi-rebar close-spacing or objective-uniqueness proof.",
            next_action="Cite as workflow feasibility and use weak rows to motivate ambiguity intervals.",
        ),
        audit_row(
            baseline_key="multi_rebar_detector_assignment_variable_depth_radius",
            domain="synthetic_detector",
            status="partial_seed_baseline",
            readiness_score=min(1.0, assignments["assigned_per_run"] / 3.0),
            evidence_count=assignments["assigned_count"],
            primary_metric_label="assigned_candidates_per_run",
            primary_metric_value=assignments["assigned_per_run"],
            ready_use="Multi-rebar detector assignment can seed variable-depth/radius workflows.",
            blocked_use="Standalone baseline for final radius or objective near-tie reporting.",
            next_action="Use as seed-stage evidence; design a same-case detector-only comparator before claiming baseline superiority.",
        ),
        audit_row(
            baseline_key="field_hyperbola_template_overlay",
            domain="field_hyperbola",
            status="field_context_only",
            readiness_score=1.0,
            evidence_count=safe_float(field_hyperbola.get("apex_fit_count"), 0.0),
            primary_metric_label="field_apex_fit_count",
            primary_metric_value=safe_float(field_hyperbola.get("apex_fit_count"), 0.0),
            ready_use="Measured-field hyperbola-template overlays as visual/context QC.",
            blocked_use="Known-truth field calibration, cover depth, radius, FWI, or 3D claims.",
            next_action="Keep as field context; do not use to validate synthetic resolution thresholds.",
        ),
        audit_row(
            baseline_key="field_hyperbola_timezero_degeneracy",
            domain="field_hyperbola",
            status="blocked_calibrated_field_baseline",
            readiness_score=0.0,
            evidence_count=safe_float(field_degeneracy.get("surface_summary_row_count"), 0.0),
            primary_metric_label="near_top_time_zero_span_ns",
            primary_metric_value=safe_float(field_degeneracy.get("max_near_top_time_zero_span_ns"), 0.0),
            ready_use="Negative guardrail showing why field hyperbola overlays are not calibrated inversion.",
            blocked_use="Cover-depth, radius, absolute time-zero, or field FWI baseline.",
            next_action="Use as a limitation/guardrail row in manuscript wording.",
        ),
        audit_row(
            baseline_key="current_synthetic_claim_baseline_gap",
            domain="manuscript_gap",
            status="contract_needed",
            readiness_score=0.45,
            evidence_count=safe_float(contribution_summary.get("contribution_row_count"), 0.0),
            primary_metric_label="current_gpu_candidates",
            primary_metric_value=safe_float(contribution_summary.get("synthetic_immediate_gpu_priority_count"), 0.0)
            + safe_float(contribution_summary.get("synthetic_conditional_gpu_candidate_count"), 0.0),
            ready_use="Current evidence identifies the baseline-comparison need without requiring immediate GPU work.",
            blocked_use="Claiming superiority over hyperbola/database/ML baselines without a same-case comparison.",
            next_action="Design a CPU-first same-case detector/database baseline for the current close14/close50 claims before any GPU escalation.",
        ),
    ]


def summarize_audit(rows: list[dict], single_detector: dict, two_stage: dict, assignments: dict) -> dict:
    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
    ready_count = status_counts.get("ready_location_baseline", 0) + status_counts.get("ready_pipeline_baseline", 0)
    return {
        "policy_label": "local_2d_baseline_readiness_cpu_first_no_gpu",
        "baseline_row_count": len(rows),
        "ready_baseline_count": ready_count,
        "partial_baseline_count": status_counts.get("partial_seed_baseline", 0),
        "field_context_count": status_counts.get("field_context_only", 0),
        "blocked_or_contract_needed_count": (
            status_counts.get("blocked_calibrated_field_baseline", 0)
            + status_counts.get("contract_needed", 0)
        ),
        "single_detector_scenario_count": single_detector["scenario_count"],
        "single_detector_hit_rate": single_detector["hit_rate"],
        "two_stage_row_count": two_stage["row_count"],
        "two_stage_exact_fraction": two_stage["exact_fraction"],
        "two_stage_strong_count": two_stage["strong_count"],
        "two_stage_weak_count": two_stage["weak_count"],
        "assignment_run_count": assignments["run_count"],
        "assignment_candidate_count": assignments["assigned_count"],
        "immediate_gpu_priority_count": 0,
        "conditional_gpu_candidate_count": 0,
        "gpu_priority": "none",
        "ready_for_baseline_section_planning": True,
        "decision": (
            "Existing detector outputs support a location-seed and single-rebar "
            "detector-to-refinement baseline, while same-case close14/close50 detector/database "
            "comparisons still need a CPU-first contract. Do not launch broad GPU work."
        ),
    }


def status_color(status: str) -> str:
    return {
        "ready_location_baseline": "#2f9d55",
        "ready_pipeline_baseline": "#4c78a8",
        "partial_seed_baseline": "#d98c20",
        "field_context_only": "#6b6b6b",
        "blocked_calibrated_field_baseline": "#c7302b",
        "contract_needed": "#9467bd",
    }.get(status, "#6b6b6b")


def plot_audit(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["baseline_key"].replace("_", "\n") for row in rows]
    scores = [safe_float(row["readiness_score"], 0.0) for row in rows]
    colors = [status_color(row["status"]) for row in rows]
    statuses = list(dict.fromkeys(row["status"] for row in rows))

    fig, axes = plt.subplots(1, 2, figsize=(15.5, 5.4), constrained_layout=True)
    x = np.arange(len(rows))
    axes[0].bar(x, scores, color=colors, width=0.64)
    axes[0].set_xticks(x, labels, fontsize=8)
    axes[0].set_ylim(0, 1.05)
    axes[0].set_ylabel("readiness score")
    axes[0].set_title("Baseline readiness")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(
        handles=[Patch(color=status_color(status), label=status.replace("_", " ")) for status in statuses],
        loc="upper right",
        frameon=False,
        fontsize=8,
    )

    metric_labels = ["single\nscenarios", "single\nhit rate", "two-stage\nrows", "two-stage\nexact", "assigned\ncandidates", "GPU\nqueue"]
    metric_values = [
        summary["single_detector_scenario_count"],
        summary["single_detector_hit_rate"],
        summary["two_stage_row_count"],
        summary["two_stage_exact_fraction"],
        summary["assignment_candidate_count"],
        summary["immediate_gpu_priority_count"] + summary["conditional_gpu_candidate_count"],
    ]
    axes[1].bar(np.arange(len(metric_values)), metric_values, color=["#4c78a8", "#2f9d55", "#4c78a8", "#2f9d55", "#d98c20", "#c7302b"], width=0.62)
    axes[1].set_xticks(np.arange(len(metric_values)), metric_labels)
    axes[1].set_title("Key counts and gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Local 2D baseline readiness: CPU-first comparison planning", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, summary_json: Path, validation_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_baseline_readiness_audit.png`",
                "",
                "This CPU-only audit summarizes existing synthetic detector,",
                "detector-seeded refinement, multi-rebar assignment, and field",
                "hyperbola-template evidence for manuscript baseline planning.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Baseline rows: `{summary['baseline_row_count']}`.",
                f"Ready baseline rows: `{summary['ready_baseline_count']}`.",
                f"Single-detector scenarios: `{summary['single_detector_scenario_count']:.0f}`.",
                f"Single-detector hit rate: `{summary['single_detector_hit_rate']:.3f}`.",
                f"Two-stage exact fraction: `{summary['two_stage_exact_fraction']:.3f}`.",
                f"Immediate GPU candidates: `{summary['immediate_gpu_priority_count']}`.",
                f"Conditional GPU candidates: `{summary['conditional_gpu_candidate_count']}`.",
                "",
                "Outputs:",
                "",
                f"- Baseline rows: `{rows_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                f"- Figure validation: `{validation_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "The audit plans baseline comparisons; it does not run detector,",
                "FDTD, FWI, GPU, field FWI, 3D/HPC, or neural-network jobs.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default="outputs/experiments")
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--single-detector-runs", default=DEFAULT_SINGLE_DETECTOR_RUNS)
    parser.add_argument("--two-stage-run", default=DEFAULT_TWO_STAGE_RUN)
    parser.add_argument("--assignment-runs", default=DEFAULT_ASSIGNMENT_RUNS)
    parser.add_argument("--field-hyperbola-run", default=DEFAULT_FIELD_HYPERBOLA_RUN)
    parser.add_argument("--field-degeneracy-run", default=DEFAULT_FIELD_DEGENERACY_RUN)
    parser.add_argument("--contribution-run", default=DEFAULT_CONTRIBUTION_RUN)
    parser.add_argument("--run-name", default="local_2d_baseline_readiness_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    experiment_root = Path(args.experiment_root)
    summary_root = Path(args.summary_root)
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)

    detector_summaries = [
        read_json(experiment_root / run / "data/detection_benchmark_summary.json")
        for run in parse_run_list(args.single_detector_runs)
    ]
    two_stage_rows = read_csv_rows(
        experiment_root / args.two_stage_run / "data/two_stage_refinement_aggregate.csv"
    )
    assignment_summaries = [
        read_json(experiment_root / run / "data/detection_assignment_summary.json")
        for run in parse_run_list(args.assignment_runs)
    ]
    field_hyperbola = read_json(
        dataset_root / args.field_hyperbola_run / "data/field_hyperbola_calibration_summary.json"
    )
    field_degeneracy = read_json(
        dataset_root
        / args.field_degeneracy_run
        / "data/field_hyperbola_timezero_degeneracy_summary.json"
    )
    contribution_summary = read_json(
        summary_root / args.contribution_run / "data/local_2d_manuscript_contribution_summary.json"
    )

    single_detector = summarize_single_detector(detector_summaries)
    two_stage = summarize_two_stage(two_stage_rows)
    assignments = summarize_assignments(assignment_summaries)
    rows = build_audit_rows(
        single_detector=single_detector,
        two_stage=two_stage,
        assignments=assignments,
        field_hyperbola=field_hyperbola,
        field_degeneracy=field_degeneracy,
        contribution_summary=contribution_summary,
    )
    summary = summarize_audit(rows, single_detector, two_stage, assignments)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_baseline_readiness_rows.csv"
    summary_json = data_dir / "local_2d_baseline_readiness_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_baseline_readiness_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    plot_audit(rows, summary, figure_path)
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
        "local_2d_baseline_readiness_audit",
        {
            "single_detector_runs": parse_run_list(args.single_detector_runs),
            "two_stage_run": args.two_stage_run,
            "assignment_runs": parse_run_list(args.assignment_runs),
            "field_hyperbola_run": args.field_hyperbola_run,
            "field_degeneracy_run": args.field_degeneracy_run,
            "contribution_run": args.contribution_run,
            "readgssi_version": readgssi_version(),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

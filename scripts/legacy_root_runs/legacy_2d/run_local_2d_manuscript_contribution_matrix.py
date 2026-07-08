#!/usr/bin/env python3
"""Build a manuscript contribution matrix for the current local 2D/field evidence."""

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
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SYNTHETIC_BUNDLE_RUN = "1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation"
DEFAULT_SYNTHETIC_NEXT_RUN = "1356_synthetic_2d_next_question_matrix_post_matched_source3_policy"
DEFAULT_CROSS_DOMAIN_RUN = "010_local_2d_field_cross_domain_scope_map_post_timing_window_family"
DEFAULT_FIELD_VIABILITY_RUN = "013_local_gssi_field_claim_viability_scorecard_post_timing_discriminant"
DEFAULT_SYNTHETIC_CORPUS_RUN = "012_synthetic_2d_archive_corpus_card_post_field_timing_refresh"
DEFAULT_LITERATURE_MATRIX = "docs/papers/2026-06-07_literature_positioning_matrix.md"
DEFAULT_NEURAL_TRIAGE = "docs/update/summary/010_2026-06-18_neural_network_field_2d_triage.md"
DEFAULT_MATCHED_SOURCE3_POLICY = (
    "outputs/summary_tables/121_close_spacing_matched_source3_policy_synthesis/"
    "data/close_spacing_matched_source3_policy_summary.json"
)


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


def row_value(rows: list[dict], key: str, key_col: str, value_col: str, default: str = "") -> str:
    for row in rows:
        if row.get(key_col) == key:
            return str(row.get(value_col, default))
    return default


def claim_allowed(rows: list[dict], claim_area: str) -> str:
    return row_value(rows, claim_area, "claim_area", "allowed_claim")


def claim_blocked(rows: list[dict], claim_area: str) -> str:
    return row_value(rows, claim_area, "claim_area", "not_allowed")


def field_claim_status(rows: list[dict], claim_key: str) -> str:
    return row_value(rows, claim_key, "claim_key", "status")


def field_claim_score(rows: list[dict], claim_key: str) -> float:
    return safe_float(row_value(rows, claim_key, "claim_key", "support_score", "0.0"), 0.0)


def next_matrix_count(rows: list[dict], column: str, value: str) -> int:
    return sum(str(row.get(column, "")).strip().lower() == value for row in rows)


def contribution_row(
    *,
    contribution_key: str,
    manuscript_role: str,
    readiness: str,
    readiness_score: float,
    novelty_angle: str,
    current_evidence: str,
    prior_art_boundary: str,
    limitation: str,
    next_action: str,
    gpu_priority: str,
) -> dict:
    return {
        "contribution_key": contribution_key,
        "manuscript_role": manuscript_role,
        "readiness": readiness,
        "readiness_score": min(1.0, max(0.0, safe_float(readiness_score, 0.0))),
        "novelty_angle": novelty_angle,
        "current_evidence": current_evidence,
        "prior_art_boundary": prior_art_boundary,
        "limitation": limitation,
        "next_action": next_action,
        "gpu_priority": gpu_priority,
    }


def build_contribution_rows(
    *,
    synthetic_claims: list[dict],
    synthetic_next_rows: list[dict],
    cross_domain_rows: list[dict],
    field_viability_rows: list[dict],
    field_viability_summary: dict,
    synthetic_bundle_summary: dict,
    synthetic_corpus_summary: dict,
    matched_source3_summary: dict,
    literature_matrix_exists: bool,
    neural_triage_exists: bool,
) -> list[dict]:
    synthetic_figures = safe_float(synthetic_bundle_summary.get("figure_count"), 0.0)
    synthetic_claim_count = safe_float(synthetic_bundle_summary.get("claim_boundary_count"), 0.0)
    archive_runs = safe_float(synthetic_corpus_summary.get("archive_run_count"), 0.0)
    field_score_rows = safe_float(field_viability_summary.get("claim_row_count"), 0.0)
    field_ready = bool(field_viability_summary.get("ready_for_manuscript_field_claim_viability", False))
    gpu_immediate = next_matrix_count(synthetic_next_rows, "gpu_priority", "immediate")
    gpu_conditional = next_matrix_count(synthetic_next_rows, "gpu_readiness", "conditional")

    cross_field_boundary = row_value(
        cross_domain_rows,
        "field_timing_window_family_boundary",
        "scope_key",
        "allowed_joint_claim",
    )
    no_gpu_boundary = row_value(cross_domain_rows, "current_no_gpu_queue", "scope_key", "allowed_joint_claim")

    return [
        contribution_row(
            contribution_key="controlled_close_spacing_resolution_map",
            manuscript_role="core_result",
            readiness="ready",
            readiness_score=1.0,
            novelty_angle=(
                "Controlled acquisition-aware resolution/ambiguity mapping for nearby rebars, "
                "not a universal rebar-detection claim."
            ),
            current_evidence=claim_allowed(synthetic_claims, "resolution_limit"),
            prior_art_boundary=(
                "Close rebar detection/sizing and FWI exist; the publishable angle is the "
                "explicit ambiguity-margin and acquisition-dependence protocol."
            ),
            limitation=claim_blocked(synthetic_claims, "resolution_limit"),
            next_action="Use the current resolution-claim map and claim-boundary CSV in manuscript drafting.",
            gpu_priority="none",
        ),
        contribution_row(
            contribution_key="objective_near_tie_reporting_protocol",
            manuscript_role="core_method",
            readiness="ready",
            readiness_score=0.95,
            novelty_angle=(
                "Separate exact recovery, strict location-clean geometry, zero-width objective near ties, "
                "and geometry-ambiguous intervals."
            ),
            current_evidence=claim_allowed(synthetic_claims, "reporting_tiers"),
            prior_art_boundary=(
                "Prior work often reports best estimates or accuracy; this project can emphasize "
                "near-best competitor and ambiguity-interval reporting."
            ),
            limitation=claim_blocked(synthetic_claims, "reporting_tiers"),
            next_action="Make the tier definitions a methods subsection before reporting performance tables.",
            gpu_priority="none",
        ),
        contribution_row(
            contribution_key="target2_close14_objective_limit",
            manuscript_role="negative_result",
            readiness="ready",
            readiness_score=0.92,
            novelty_angle="Truth selection can be strong while objective uniqueness remains blocked by a +1 mm competitor.",
            current_evidence=claim_allowed(synthetic_claims, "target2_close14_objective_limit"),
            prior_art_boundary="Close-spacing difficulty is known; the useful result is quantified near-tie persistence.",
            limitation=claim_blocked(synthetic_claims, "target2_close14_objective_limit"),
            next_action="Report as a controlled failure-mode boundary, not as clean close14 resolution.",
            gpu_priority="none",
        ),
        contribution_row(
            contribution_key="target2_close50_seed_frequency_caveat",
            manuscript_role="acquisition_result",
            readiness="ready",
            readiness_score=0.88,
            novelty_angle="Three-seed frequency separates exact/strong recovery from clean replicated lateral resolution.",
            current_evidence=claim_allowed(synthetic_claims, "target2_close50_linear29p5_seed_frequency"),
            prior_art_boundary="Sub-threshold spacing claims need seed replication and ambiguity gating.",
            limitation=claim_blocked(synthetic_claims, "target2_close50_linear29p5_seed_frequency"),
            next_action="Keep 30 mm as paper-safe clean threshold; describe 29.5 mm as exact but not clean-replicated.",
            gpu_priority="none",
        ),
        contribution_row(
            contribution_key="matched_source3_acquisition_geometry_contrast",
            manuscript_role="acquisition_result",
            readiness="ready"
            if bool(matched_source3_summary.get("guarded_acquisition_geometry_contrast_ready", False))
            else "review",
            readiness_score=0.90
            if bool(matched_source3_summary.get("guarded_acquisition_geometry_contrast_ready", False))
            else 0.35,
            novelty_angle=(
                "Reciprocal matched source3 controls separate exact truth selection from a stable near-truth wrong branch."
            ),
            current_evidence=(
                f"close14 truth fraction={matched_source3_summary.get('close14_truth_geometry_fraction', 'missing')}; "
                f"close50 truth fraction={matched_source3_summary.get('close50_truth_geometry_fraction', 'missing')}; "
                f"close50 wrong branch={matched_source3_summary.get('close50_replicated_wrong_branch', 'missing')}; "
                f"spacing-only={matched_source3_summary.get('spacing_only_causal_generalization_ready', 'missing')}"
            ),
            prior_art_boundary=(
                "This is not a generic source-density rule; the contribution is the matched-control claim boundary."
            ),
            limitation=(
                "Still not spacing-only causal proof because absolute target2 position changes with the target1-target2 gap."
            ),
            next_action="Use summary table 121 as the manuscript source-density claim gate.",
            gpu_priority="none",
        ),
        contribution_row(
            contribution_key="target1_acquisition_confidence_surface",
            manuscript_role="acquisition_result",
            readiness="ready",
            readiness_score=0.82,
            novelty_angle="Stable exact geometry can coexist with nonmonotonic source-density confidence behavior.",
            current_evidence=claim_allowed(synthetic_claims, "target1_acquisition_confidence"),
            prior_art_boundary="Acquisition design is common; the angle is target-specific confidence policy.",
            limitation=claim_blocked(synthetic_claims, "target1_acquisition_confidence"),
            next_action="Use target1 as acquisition-policy evidence, not as a reason for broad source-count reruns.",
            gpu_priority="none",
        ),
        contribution_row(
            contribution_key="field_2d_qc_supplement",
            manuscript_role="field_supplement",
            readiness="ready" if field_ready else "review",
            readiness_score=1.0 if field_ready else 0.35,
            novelty_angle="Measured GSSI data support scoped 2D QC, timing discipline, and claim boundaries.",
            current_evidence=(
                f"field claim-viability rows={field_score_rows:.0f}; "
                f"2D QC status={field_claim_status(field_viability_rows, 'field_dataset_methods_2d_line_profiles')}; "
                f"short timing status={field_claim_status(field_viability_rows, 'short_pair_relative_time_zero')}"
            ),
            prior_art_boundary="Field data strengthen practical context but do not validate synthetic known-truth thresholds.",
            limitation="No absolute time-zero, target labels, crossline grid, field FWI, cover-depth, or radius validation.",
            next_action="Use field figures as a supplement/methods QC package with explicit blocked-claim language.",
            gpu_priority="none",
        ),
        contribution_row(
            contribution_key="field_synthetic_scope_separation",
            manuscript_role="guardrail",
            readiness="ready",
            readiness_score=1.0,
            novelty_angle="The paper can be honest about measured field QC versus synthetic known-truth resolution.",
            current_evidence=cross_field_boundary,
            prior_art_boundary="Applied competitors often include lab/field validation; this project should not overstate field proof.",
            limitation="Field cue spacing and timing QC do not relabel synthetic confidence thresholds.",
            next_action="Keep synthetic and field claim tables separate through drafting.",
            gpu_priority="none",
        ),
        contribution_row(
            contribution_key="neural_network_baseline_not_current_path",
            manuscript_role="future_work",
            readiness="deferred",
            readiness_score=0.25 if neural_triage_exists else 0.0,
            novelty_angle="Neural methods are relevant baselines/surrogates, not current local training targets.",
            current_evidence=(
                "local neural triage present" if neural_triage_exists else "local neural triage missing"
            ),
            prior_art_boundary="CNN/YOLO, learned forward solvers, and 3DInvNet-like inversion already exist.",
            limitation="Current local field data have four profiles and no labels/3D grid; training would be premature.",
            next_action="Use neural work as literature/baseline context unless a labeled synthetic benchmark is designed.",
            gpu_priority="none",
        ),
        contribution_row(
            contribution_key="literature_positioning_boundary",
            manuscript_role="framing",
            readiness="ready" if literature_matrix_exists else "review",
            readiness_score=0.9 if literature_matrix_exists else 0.2,
            novelty_angle="Do not claim first GPR FWI rebar sizing; claim controlled identifiability and ambiguity protocol.",
            current_evidence="local literature positioning matrix present" if literature_matrix_exists else "literature matrix missing",
            prior_art_boundary="FWI sizing, source-wavelet handling, MIMO sizing, and ML detection are established.",
            limitation="The strongest present evidence remains controlled synthetic plus scoped field QC.",
            next_action="Use the literature matrix to write the introduction and limitations without novelty overreach.",
            gpu_priority="none",
        ),
        contribution_row(
            contribution_key="current_no_gpu_queue",
            manuscript_role="compute_policy",
            readiness="ready",
            readiness_score=1.0,
            novelty_angle="Research priority is manuscript synthesis and narrow hypothesis design, not broad GPU use.",
            current_evidence=(
                f"{no_gpu_boundary}; synthetic figures={synthetic_figures:.0f}; "
                f"synthetic claims={synthetic_claim_count:.0f}; archive runs={archive_runs:.0f}; "
                f"immediate_gpu={gpu_immediate}; conditional_gpu={gpu_conditional}"
            ),
            prior_art_boundary="More compute is not a contribution unless tied to a new hypothesis or baseline comparison.",
            limitation="No current matrix row justifies broad local GPU, field FWI, or HPC work.",
            next_action="Draft, audit, or design a genuinely new narrow hypothesis before any GPU submission.",
            gpu_priority="none",
        ),
    ]


def summarize_contributions(rows: list[dict], *, field_summary: dict, synthetic_next_rows: list[dict]) -> dict:
    readiness_counts: dict[str, int] = {}
    for row in rows:
        readiness_counts[row["readiness"]] = readiness_counts.get(row["readiness"], 0) + 1
    immediate_gpu = next_matrix_count(synthetic_next_rows, "gpu_priority", "immediate")
    conditional_gpu = next_matrix_count(synthetic_next_rows, "gpu_readiness", "conditional")
    ready = (
        readiness_counts.get("ready", 0) >= 8
        and bool(field_summary.get("ready_for_manuscript_field_claim_viability", False))
        and immediate_gpu == 0
        and conditional_gpu == 0
    )
    return {
        "policy_label": (
            "local_2d_manuscript_contribution_matrix_ready_no_gpu"
            if ready
            else "local_2d_manuscript_contribution_matrix_review_required"
        ),
        "contribution_row_count": len(rows),
        "ready_count": readiness_counts.get("ready", 0),
        "deferred_count": readiness_counts.get("deferred", 0),
        "review_count": readiness_counts.get("review", 0),
        "core_result_count": sum(row["manuscript_role"] == "core_result" for row in rows),
        "core_method_count": sum(row["manuscript_role"] == "core_method" for row in rows),
        "field_supplement_count": sum(row["manuscript_role"] == "field_supplement" for row in rows),
        "guardrail_count": sum(row["manuscript_role"] == "guardrail" for row in rows),
        "future_work_count": sum(row["manuscript_role"] == "future_work" for row in rows),
        "synthetic_immediate_gpu_priority_count": immediate_gpu,
        "synthetic_conditional_gpu_candidate_count": conditional_gpu,
        "field_ready_for_2d_qc": bool(field_summary.get("ready_for_2d_field_qc", False)),
        "field_ready_for_fwi": bool(field_summary.get("ready_for_field_fwi", False)),
        "field_ready_for_3d_hpc": bool(field_summary.get("ready_for_3d_hpc", False)),
        "gpu_priority": "none",
        "ready_for_manuscript_positioning": ready,
        "recommended_framing": (
            "Controlled acquisition-aware identifiability and ambiguity-margin study for "
            "closely spaced multi-rebar 2D GPR inversion, with measured field data used only "
            "as scoped 2D QC and timing-boundary evidence."
        ),
    }


def role_color(role: str) -> str:
    return {
        "core_result": "#2f9d55",
        "core_method": "#4c78a8",
        "negative_result": "#d98c20",
        "acquisition_result": "#8c564b",
        "field_supplement": "#6b6b6b",
        "guardrail": "#c7302b",
        "future_work": "#9467bd",
        "framing": "#17a2a2",
        "compute_policy": "#333333",
    }.get(role, "#6b6b6b")


def plot_contribution_matrix(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["contribution_key"].replace("_", "\n") for row in rows]
    scores = [safe_float(row["readiness_score"], 0.0) for row in rows]
    colors = [role_color(row["manuscript_role"]) for row in rows]
    roles = list(dict.fromkeys(row["manuscript_role"] for row in rows))

    fig, axes = plt.subplots(2, 1, figsize=(16.0, 8.0), constrained_layout=True)
    x = np.arange(len(rows))
    axes[0].bar(x, scores, color=colors, width=0.68)
    axes[0].set_xticks(x, labels, fontsize=7)
    axes[0].set_ylim(0, 1.05)
    axes[0].set_ylabel("readiness score")
    axes[0].set_title("Contribution readiness")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(
        handles=[Patch(color=role_color(role), label=role.replace("_", " ")) for role in roles],
        loc="upper right",
        ncol=5,
        frameon=False,
        fontsize=8,
    )

    gate_labels = ["ready rows", "deferred", "review", "GPU now", "GPU cond.", "field FWI", "3D/HPC"]
    gate_values = [
        summary["ready_count"],
        summary["deferred_count"],
        summary["review_count"],
        summary["synthetic_immediate_gpu_priority_count"],
        summary["synthetic_conditional_gpu_candidate_count"],
        1 if summary["field_ready_for_fwi"] else 0,
        1 if summary["field_ready_for_3d_hpc"] else 0,
    ]
    axes[1].bar(np.arange(len(gate_values)), gate_values, color=["#2f9d55", "#9467bd", "#d98c20", "#c7302b", "#c7302b", "#c7302b", "#c7302b"], width=0.62)
    axes[1].set_xticks(np.arange(len(gate_values)), gate_labels)
    axes[1].set_title("Readiness and compute gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Local 2D manuscript contribution matrix: ready to draft, no GPU queue", fontweight="bold")
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
                "## `local_2d_manuscript_contribution_matrix.png`",
                "",
                "This CPU-only matrix maps the current synthetic 2D, field QC,",
                "literature-positioning, neural-network triage, and compute-policy",
                "evidence into manuscript contribution roles.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Contribution rows: `{summary['contribution_row_count']}`.",
                f"Ready rows: `{summary['ready_count']}`.",
                f"Deferred rows: `{summary['deferred_count']}`.",
                f"Synthetic immediate GPU candidates: `{summary['synthetic_immediate_gpu_priority_count']}`.",
                f"Synthetic conditional GPU candidates: `{summary['synthetic_conditional_gpu_candidate_count']}`.",
                f"Field ready for FWI: `{summary['field_ready_for_fwi']}`.",
                f"Field ready for 3D/HPC: `{summary['field_ready_for_3d_hpc']}`.",
                "",
                "Outputs:",
                "",
                f"- Contribution rows: `{rows_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                f"- Figure validation: `{validation_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "The matrix supports manuscript planning and claim discipline. It",
                "does not launch or justify broad GPU runs, field FWI, 3D/HPC,",
                "or neural-network training from the current local data.",
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
    parser.add_argument("--synthetic-bundle-run", default=DEFAULT_SYNTHETIC_BUNDLE_RUN)
    parser.add_argument("--synthetic-next-run", default=DEFAULT_SYNTHETIC_NEXT_RUN)
    parser.add_argument("--cross-domain-run", default=DEFAULT_CROSS_DOMAIN_RUN)
    parser.add_argument("--field-viability-run", default=DEFAULT_FIELD_VIABILITY_RUN)
    parser.add_argument("--synthetic-corpus-run", default=DEFAULT_SYNTHETIC_CORPUS_RUN)
    parser.add_argument("--literature-matrix", default=DEFAULT_LITERATURE_MATRIX)
    parser.add_argument("--neural-triage", default=DEFAULT_NEURAL_TRIAGE)
    parser.add_argument("--matched-source3-policy", default=DEFAULT_MATCHED_SOURCE3_POLICY)
    parser.add_argument("--run-name", default="local_2d_manuscript_contribution_matrix")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    experiment_root = Path(args.experiment_root)
    summary_root = Path(args.summary_root)

    synthetic_bundle_dir = experiment_root / args.synthetic_bundle_run
    synthetic_next_dir = experiment_root / args.synthetic_next_run
    cross_domain_dir = summary_root / args.cross_domain_run
    field_viability_dir = summary_root / args.field_viability_run
    synthetic_corpus_dir = summary_root / args.synthetic_corpus_run

    synthetic_claims = read_csv_rows(
        synthetic_bundle_dir / "data/synthetic_2d_publication_claim_boundaries.csv"
    )
    synthetic_bundle_summary = read_json(
        synthetic_bundle_dir / "data/synthetic_2d_publication_figure_bundle_summary.json"
    )
    synthetic_next_rows = read_csv_rows(
        synthetic_next_dir / "data/synthetic_2d_next_question_matrix_rows.csv"
    )
    cross_domain_rows = read_csv_rows(
        cross_domain_dir / "data/local_2d_field_cross_domain_scope_rows.csv"
    )
    field_viability_rows = read_csv_rows(
        field_viability_dir / "data/local_gssi_field_claim_viability_rows.csv"
    )
    field_viability_summary = read_json(
        field_viability_dir / "data/local_gssi_field_claim_viability_summary.json"
    )
    synthetic_corpus_summary = read_json(
        synthetic_corpus_dir / "data/synthetic_2d_archive_corpus_card_summary.json"
    )
    matched_source3_summary = read_json(Path(args.matched_source3_policy))

    rows = build_contribution_rows(
        synthetic_claims=synthetic_claims,
        synthetic_next_rows=synthetic_next_rows,
        cross_domain_rows=cross_domain_rows,
        field_viability_rows=field_viability_rows,
        field_viability_summary=field_viability_summary,
        synthetic_bundle_summary=synthetic_bundle_summary,
        synthetic_corpus_summary=synthetic_corpus_summary,
        matched_source3_summary=matched_source3_summary,
        literature_matrix_exists=Path(args.literature_matrix).exists(),
        neural_triage_exists=Path(args.neural_triage).exists(),
    )
    summary = summarize_contributions(
        rows,
        field_summary=field_viability_summary,
        synthetic_next_rows=synthetic_next_rows,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_manuscript_contribution_rows.csv"
    summary_json = data_dir / "local_2d_manuscript_contribution_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_manuscript_contribution_matrix.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    plot_contribution_matrix(rows, summary, figure_path)
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
        "local_2d_manuscript_contribution_matrix",
        {
            "synthetic_bundle_run": args.synthetic_bundle_run,
            "synthetic_next_run": args.synthetic_next_run,
            "cross_domain_run": args.cross_domain_run,
            "field_viability_run": args.field_viability_run,
            "synthetic_corpus_run": args.synthetic_corpus_run,
            "literature_matrix": args.literature_matrix,
            "neural_triage": args.neural_triage,
            "matched_source3_policy": args.matched_source3_policy,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

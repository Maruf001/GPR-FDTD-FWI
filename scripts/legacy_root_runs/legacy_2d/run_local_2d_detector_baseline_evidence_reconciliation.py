#!/usr/bin/env python3
"""Reconcile same-case detector baseline evidence for local 2D claims."""

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
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SIMPLE_RUN = "018_local_2d_detector_baseline_synthesis_post_cpu_runs"
DEFAULT_SENSITIVITY_RUN = "020_local_2d_detector_parameter_sensitivity_post_rank_depth_metrics"
DEFAULT_RANK_POLICY_RUN = "021_local_2d_detector_candidate_rank_policy_post_sensitivity"
DEFAULT_UPPER_BOUND_RUN = "039_local_2d_detector_upper_bound_policy_post_selector_audit"
DEFAULT_SOURCE_DENSITY_RUN = "103_close_spacing_source_density_archive_map"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def source_density_group(source_rows: list[dict], family: str, source_count: int) -> dict:
    for row in source_rows:
        if row.get("family") == family and safe_int(row.get("source_count"), -1) == source_count:
            return row
    return {}


def evidence_rows(
    simple_summary: dict,
    sensitivity_summary: dict,
    rank_summary: dict,
    upper_summary: dict,
    source_density_rows: list[dict],
) -> list[dict]:
    close14_source3 = source_density_group(source_density_rows, "close14", 3)
    return [
        {
            "evidence_key": "simple_top20_detector",
            "evidence_role": "weak_image_feature_baseline",
            "case_count": safe_int(simple_summary.get("case_count")),
            "all_truth_case_count": safe_int(simple_summary.get("all_truth_case_count")),
            "target0_hit_count": safe_int(simple_summary.get("target0_hit_count")),
            "target1_hit_count": safe_int(simple_summary.get("target1_hit_count")),
            "target2_hit_count": safe_int(simple_summary.get("target2_hit_count")),
            "rank_or_budget": "top20 detector candidates",
            "supports_claim": "naive detector under-resolves close-spacing cases",
            "blocks_claim": "detector is a competitive standalone recovery method",
        },
        {
            "evidence_key": "saved_bscan_parameter_sensitivity",
            "evidence_role": "truth_containing_candidate_generator",
            "case_count": safe_int(sensitivity_summary.get("case_count")),
            "all_truth_case_count": safe_int(sensitivity_summary.get("rescued_case_count")),
            "target0_hit_count": safe_int(sensitivity_summary.get("any_config_target0_case_count")),
            "target1_hit_count": safe_int(sensitivity_summary.get("case_count")),
            "target2_hit_count": safe_int(sensitivity_summary.get("any_config_target2_case_count")),
            "rank_or_budget": f"best config max rank {sensitivity_summary.get('best_config_max_assigned_rank')}",
            "supports_claim": "detector family contains all truths for every case under tuned CPU rescore",
            "blocks_claim": "top-pick or parameter-free detector baseline",
        },
        {
            "evidence_key": "candidate_rank_policy",
            "evidence_role": "rank_budget_gate",
            "case_count": safe_int(rank_summary.get("case_count")),
            "all_truth_case_count": safe_int(rank_summary.get("best_case_count_by_rank_cap", {}).get("top40")),
            "target0_hit_count": math.nan,
            "target1_hit_count": math.nan,
            "target2_hit_count": math.nan,
            "rank_or_budget": f"minimal all-case rank cap {rank_summary.get('minimal_rank_cap_for_full_case_recovery')}",
            "supports_claim": "all-case detector candidate recovery needs a deeper rank cap",
            "blocks_claim": "cheap top-5/top-10 detector-to-FWI handoff",
        },
        {
            "evidence_key": "rank_gated_upper_bound",
            "evidence_role": "upper_bound_not_deployable_selector",
            "case_count": safe_int(upper_summary.get("case_count")),
            "all_truth_case_count": safe_int(upper_summary.get("best_rank_gated_upper_bound_all_truth_case_count")),
            "target0_hit_count": math.nan,
            "target1_hit_count": math.nan,
            "target2_hit_count": math.nan,
            "rank_or_budget": (
                f"top{upper_summary.get('minimal_all_case_rank_gated_triples_per_case')} triples per case"
            ),
            "supports_claim": "truth-containing upper bound exists with rank-gated triples",
            "blocks_claim": "validated truth-free top-1 selector or detector-seeded FWI readiness",
        },
        {
            "evidence_key": "close14_source3_source_density_context",
            "evidence_role": "source_density_guardrail",
            "case_count": safe_int(close14_source3.get("row_count")),
            "all_truth_case_count": safe_int(close14_source3.get("truth_geometry_count")),
            "target0_hit_count": math.nan,
            "target1_hit_count": math.nan,
            "target2_hit_count": math.nan,
            "rank_or_budget": "source3 Tx/Rx45 seeds 13,21,34",
            "supports_claim": "close14 source3 is near-exact context, not replicated failure",
            "blocks_claim": "generic statement that three-source acquisition fails",
        },
    ]


def summarize_reconciliation(rows: list[dict], upper_summary: dict, source_density_summary: dict) -> dict:
    simple = next(row for row in rows if row["evidence_key"] == "simple_top20_detector")
    sensitivity = next(row for row in rows if row["evidence_key"] == "saved_bscan_parameter_sensitivity")
    rank_policy = next(row for row in rows if row["evidence_key"] == "candidate_rank_policy")
    upper = next(row for row in rows if row["evidence_key"] == "rank_gated_upper_bound")
    simple_all_truth_fraction = (
        safe_float(simple["all_truth_case_count"], 0.0) / safe_float(simple["case_count"], 1.0)
    )
    sensitivity_all_truth_fraction = (
        safe_float(sensitivity["all_truth_case_count"], 0.0) / safe_float(sensitivity["case_count"], 1.0)
    )
    ready_upper_bound = boolish(upper_summary.get("ready_for_rank_gated_upper_bound_claim"))
    detector_seeded_fwi = boolish(upper_summary.get("ready_for_detector_seeded_fwi"))
    return {
        "policy_label": "local_2d_detector_baseline_evidence_reconciliation",
        "evidence_row_count": len(rows),
        "simple_detector_all_truth_fraction": simple_all_truth_fraction,
        "sensitivity_rescued_fraction": sensitivity_all_truth_fraction,
        "minimal_rank_cap_for_full_case_recovery": safe_int(
            str(rank_policy["rank_or_budget"]).rsplit(" ", 1)[-1], 0
        ),
        "rank_gated_upper_bound_all_truth_case_count": safe_int(upper["all_truth_case_count"]),
        "ready_for_rank_gated_upper_bound_claim": ready_upper_bound,
        "ready_for_detector_seeded_fwi": detector_seeded_fwi,
        "ready_for_broad_gpu_queue": False,
        "ready_for_field_or_3d_work": False,
        "gpu_priority": "none",
        "source_density_context": source_density_summary.get("near_exact_nonclose50_source3_families", ""),
        "recommended_manuscript_use": (
            "Report the simple detector as a weak baseline, then report saved-B-scan sensitivity and "
            "rank-gated upper-bound results as evidence that image-domain candidate lists can contain "
            "the true geometry only at deeper rank budgets. Do not claim a validated detector selector "
            "or launch detector-seeded FWI from these rows."
        ),
        "decision": (
            "The detector evidence is publication-useful as a baseline ladder: simple top-20 detector "
            "under-resolves, tuned saved-B-scan rescoring recovers all truths as candidate-list evidence, "
            "and the all-case upper bound needs rank-gated candidate triples. Detector-seeded FWI, broad "
            "GPU work, field work, and 3D/HPC remain blocked by this synthesis."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "rank_gated_upper_bound_claim",
            "ready": summary["ready_for_rank_gated_upper_bound_claim"],
            "allowed_use": "publication baseline-context upper-bound statement",
            "blocked_use": "validated standalone detector",
            "evidence": f"upper_bound_cases={summary['rank_gated_upper_bound_all_truth_case_count']}",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI launch",
            "evidence": "truth-free selector still has zero deployable all-truth top-1 recovery",
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "broad detector or FWI GPU queue",
            "evidence": "CPU synthesis only; no new simulation requested",
        },
        {
            "gate_key": "field_or_3d_handoff",
            "ready": summary["ready_for_field_or_3d_work"],
            "allowed_use": "none",
            "blocked_use": "field FWI or 3D/HPC handoff",
            "evidence": "synthetic 2D detector baseline evidence; field controls remain separate",
        },
    ]


def plot_reconciliation(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["evidence_key"].replace("_", "\n") for row in rows[:4]]
    case_count = [safe_float(row["case_count"], 0.0) for row in rows[:4]]
    all_truth = [safe_float(row["all_truth_case_count"], 0.0) for row in rows[:4]]
    x = np.arange(len(labels))

    fig, axes = plt.subplots(1, 2, figsize=(14.2, 5.2), constrained_layout=True)
    axes[0].bar(x, case_count, color="#d9d9d9", label="cases")
    axes[0].bar(x, all_truth, color="#4e79a7", label="all-truth cases")
    axes[0].set_xticks(x, labels, fontsize=8)
    axes[0].set_ylabel("case count")
    axes[0].set_title("Detector evidence ladder")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    gates = gate_rows(summary)
    gate_labels = [row["gate_key"].replace("_", "\n") for row in gates]
    gate_values = [1.0 if boolish(row["ready"]) else 0.0 for row in gates]
    gate_colors = ["#59a14f" if value else "#e15759" for value in gate_values]
    axes[1].bar(np.arange(len(gates)), gate_values, color=gate_colors)
    axes[1].set_xticks(np.arange(len(gates)), gate_labels, fontsize=8)
    axes[1].set_ylim(0, 1.1)
    axes[1].set_yticks([0, 1], ["blocked", "ready"])
    axes[1].set_title("Launch gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Local 2D Detector Baseline Evidence Reconciliation", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--simple-run", default=DEFAULT_SIMPLE_RUN)
    parser.add_argument("--sensitivity-run", default=DEFAULT_SENSITIVITY_RUN)
    parser.add_argument("--rank-policy-run", default=DEFAULT_RANK_POLICY_RUN)
    parser.add_argument("--upper-bound-run", default=DEFAULT_UPPER_BOUND_RUN)
    parser.add_argument("--source-density-run", default=DEFAULT_SOURCE_DENSITY_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_baseline_evidence_reconciliation")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    simple_summary = read_json(
        summary_root / args.simple_run / "data/local_2d_detector_baseline_synthesis_summary.json"
    )
    sensitivity_summary = read_json(
        summary_root / args.sensitivity_run / "data/local_2d_detector_parameter_sensitivity_summary.json"
    )
    rank_summary = read_json(
        summary_root / args.rank_policy_run / "data/local_2d_detector_candidate_rank_policy_summary.json"
    )
    upper_summary = read_json(
        summary_root / args.upper_bound_run / "data/local_2d_detector_upper_bound_policy_summary.json"
    )
    source_density_summary = read_json(
        summary_root / args.source_density_run / "data/close_spacing_source_density_archive_map_summary.json"
    )
    source_density_rows = read_csv_rows(
        summary_root / args.source_density_run / "data/close_spacing_source_density_group_summary.csv"
    )
    rows = evidence_rows(
        simple_summary,
        sensitivity_summary,
        rank_summary,
        upper_summary,
        source_density_rows,
    )
    summary = summarize_reconciliation(rows, upper_summary, source_density_summary)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_detector_baseline_evidence_rows.csv"
    gates_csv = data_dir / "local_2d_detector_baseline_evidence_gates.csv"
    summary_json = data_dir / "local_2d_detector_baseline_evidence_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_baseline_evidence_reconciliation.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_reconciliation(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
        "source_runs": {
            "simple": args.simple_run,
            "sensitivity": args.sensitivity_run,
            "rank_policy": args.rank_policy_run,
            "upper_bound": args.upper_bound_run,
            "source_density": args.source_density_run,
        },
    }
    figure_notes.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_baseline_evidence_reconciliation.png`",
                "",
                "This figure reconciles existing CPU detector-baseline evidence. It does not",
                "rerun FDTD, FWI, GPU kernels, field FWI, neural networks, or 3D/HPC jobs.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Simple detector all-truth fraction: `{summary['simple_detector_all_truth_fraction']}`.",
                f"Sensitivity rescued fraction: `{summary['sensitivity_rescued_fraction']}`.",
                f"Detector-seeded FWI ready: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_baseline_evidence_reconciliation",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "gates_csv": str(gates_csv),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

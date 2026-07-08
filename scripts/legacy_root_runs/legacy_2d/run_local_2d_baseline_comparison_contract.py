#!/usr/bin/env python3
"""Write a CPU-first baseline-comparison contract for current close14/close50 claims."""

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
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_BASELINE_AUDIT_RUN = "015_local_2d_baseline_readiness_audit_post_contribution_matrix"
DEFAULT_CONTRIBUTION_RUN = "014_local_2d_manuscript_contribution_matrix_post_field_viability"
DEFAULT_SYNTHETIC_BUNDLE_RUN = "1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation"


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


def claim_text(rows: list[dict], claim_area: str, field: str) -> str:
    for row in rows:
        if row.get("claim_area") == claim_area:
            return str(row.get(field, ""))
    return ""


def contract_row(
    *,
    contract_key: str,
    priority: str,
    baseline_method: str,
    scenario_scope: str,
    seed_scope: str,
    current_evidence: str,
    required_outputs: str,
    decision_gate: str,
    launch_now: bool,
    gpu_allowed: bool,
    cpu_first: bool,
    blocked_scope: str,
) -> dict:
    return {
        "contract_key": contract_key,
        "priority": priority,
        "baseline_method": baseline_method,
        "scenario_scope": scenario_scope,
        "seed_scope": seed_scope,
        "current_evidence": current_evidence,
        "required_outputs": required_outputs,
        "decision_gate": decision_gate,
        "launch_now": bool(launch_now),
        "gpu_allowed": bool(gpu_allowed),
        "cpu_first": bool(cpu_first),
        "blocked_scope": blocked_scope,
    }


def build_contract_rows(
    *,
    baseline_summary: dict,
    contribution_summary: dict,
    synthetic_claims: list[dict],
) -> list[dict]:
    close14_evidence = claim_text(synthetic_claims, "target2_close14_objective_limit", "allowed_claim")
    close14_blocked = claim_text(synthetic_claims, "target2_close14_objective_limit", "not_allowed")
    close50_evidence = claim_text(synthetic_claims, "target2_close50_linear29p5_seed_frequency", "allowed_claim")
    close50_blocked = claim_text(synthetic_claims, "target2_close50_linear29p5_seed_frequency", "not_allowed")
    no_gpu_ready = (
        safe_float(baseline_summary.get("immediate_gpu_priority_count"), 0.0) == 0.0
        and safe_float(baseline_summary.get("conditional_gpu_candidate_count"), 0.0) == 0.0
        and safe_float(contribution_summary.get("synthetic_immediate_gpu_priority_count"), 0.0) == 0.0
        and safe_float(contribution_summary.get("synthetic_conditional_gpu_candidate_count"), 0.0) == 0.0
    )
    launch_now = False
    return [
        contract_row(
            contract_key="target2_close14_same_case_detector_baseline",
            priority="highest_cpu_first",
            baseline_method="hyperbola_detector_or_database_location_assignment",
            scenario_scope="target2 close14 source5 Tx/Rx=45 mm objective-limit branch",
            seed_scope="seeds 13, 21, 34; compare 6 objective rows",
            current_evidence=close14_evidence,
            required_outputs=(
                "detector candidates, truth-match rank, x/z errors, near-tie/merged-cue flag, "
                "and comparison against FWI +1 mm objective competitor"
            ),
            decision_gate=(
                "If detector/database cannot separate the +1 mm competitor, report close14 as a "
                "shared physics/image-resolution ambiguity; if detector separates it but FWI does not, "
                "report a waveform-objective uniqueness limitation."
            ),
            launch_now=launch_now,
            gpu_allowed=False,
            cpu_first=True,
            blocked_scope=close14_blocked,
        ),
        contract_row(
            contract_key="target2_close50_linear29p5_same_case_detector_seed_frequency",
            priority="high_cpu_first",
            baseline_method="hyperbola_detector_or_database_location_assignment",
            scenario_scope="target2 close50 linear receiver Tx/Rx=29.5 mm seed-frequency branch",
            seed_scope="seeds 13, 21, 34; compare strict-clean seeds against ambiguous seed13",
            current_evidence=close50_evidence,
            required_outputs=(
                "per-seed detector x/z ranks, ambiguity/merge flags, and whether detector-only "
                "behavior tracks the FWI strict-clean versus x-ambiguous split"
            ),
            decision_gate=(
                "If detector-only ambiguity follows seed13, use it as an image-level baseline caveat; "
                "if not, keep seed13 as an FWI objective/reporting caveat."
            ),
            launch_now=launch_now,
            gpu_allowed=False,
            cpu_first=True,
            blocked_scope=close50_blocked,
        ),
        contract_row(
            contract_key="target1_acquisition_surface_baseline_optional",
            priority="optional_after_close_branches",
            baseline_method="detector_seed_stability_audit",
            scenario_scope="target1 acquisition-confidence surface",
            seed_scope="existing canonical target1 archive rows only",
            current_evidence=contribution_summary.get("recommended_framing", ""),
            required_outputs="detector seed stability versus source-count confidence tiers",
            decision_gate="Only run if manuscript needs a detector baseline for acquisition sensitivity.",
            launch_now=False,
            gpu_allowed=False,
            cpu_first=True,
            blocked_scope="Do not reopen target1 source-count GPU runs under the current hypothesis.",
        ),
        contract_row(
            contract_key="field_hyperbola_not_a_validation_baseline",
            priority="guardrail",
            baseline_method="field_hyperbola_template_overlay_guardrail",
            scenario_scope="local GSSI field profiles",
            seed_scope="field profiles only; no known-truth target labels",
            current_evidence=baseline_summary.get("decision", ""),
            required_outputs="none beyond existing field hyperbola/time-zero degeneracy rows",
            decision_gate="Keep as field context and guardrail, not a synthetic resolution validator.",
            launch_now=False,
            gpu_allowed=False,
            cpu_first=False,
            blocked_scope="No field cover-depth, radius, FWI, 3D, or HPC baseline from this dataset.",
        ),
        contract_row(
            contract_key="neural_network_baseline_deferred",
            priority="future_work",
            baseline_method="CNN_or_learned_forward_baseline",
            scenario_scope="future labeled synthetic benchmark only",
            seed_scope="not applicable to current four-profile field dataset",
            current_evidence="Neural methods are relevant prior art, but current local data are not a training set.",
            required_outputs="labeled synthetic benchmark, train/validation split, baseline metrics",
            decision_gate="Defer until a labeled benchmark is deliberately designed.",
            launch_now=False,
            gpu_allowed=False,
            cpu_first=False,
            blocked_scope="Do not train neural networks from the current local field profiles.",
        ),
    ] if no_gpu_ready else []


def summarize_contract(rows: list[dict]) -> dict:
    cpu_first_count = sum(bool(row["cpu_first"]) for row in rows)
    launch_now_count = sum(bool(row["launch_now"]) for row in rows)
    gpu_allowed_count = sum(bool(row["gpu_allowed"]) for row in rows)
    return {
        "policy_label": "local_2d_baseline_comparison_contract_cpu_first_not_launched",
        "contract_row_count": len(rows),
        "cpu_first_contract_count": cpu_first_count,
        "launch_now_count": launch_now_count,
        "gpu_allowed_count": gpu_allowed_count,
        "highest_priority_contract": rows[0]["contract_key"] if rows else "",
        "immediate_gpu_priority_count": 0,
        "conditional_gpu_candidate_count": 0,
        "gpu_priority": "none",
        "ready_for_future_baseline_runner_design": bool(rows and launch_now_count == 0 and gpu_allowed_count == 0),
        "decision": (
            "Do not launch the baseline comparison yet. The next implementation step is a CPU-first "
            "same-case detector/database baseline runner for close14 and close50, with skip-existing "
            "outputs and no GPU requirement."
        ),
    }


def plot_contract(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["contract_key"].replace("_", "\n") for row in rows]
    priority_scores = {
        "highest_cpu_first": 1.0,
        "high_cpu_first": 0.82,
        "optional_after_close_branches": 0.45,
        "guardrail": 0.25,
        "future_work": 0.18,
    }
    scores = [priority_scores.get(row["priority"], 0.0) for row in rows]
    colors = ["#2f9d55" if row["cpu_first"] else "#6b6b6b" for row in rows]

    fig, axes = plt.subplots(1, 2, figsize=(15.5, 5.2), constrained_layout=True)
    x = np.arange(len(rows))
    axes[0].bar(x, scores, color=colors, width=0.64)
    axes[0].set_xticks(x, labels, fontsize=8)
    axes[0].set_ylim(0, 1.05)
    axes[0].set_ylabel("contract priority")
    axes[0].set_title("Baseline comparison contracts")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    gate_labels = ["contracts", "CPU-first", "launch now", "GPU allowed", "GPU queue"]
    gate_values = [
        summary["contract_row_count"],
        summary["cpu_first_contract_count"],
        summary["launch_now_count"],
        summary["gpu_allowed_count"],
        summary["immediate_gpu_priority_count"] + summary["conditional_gpu_candidate_count"],
    ]
    axes[1].bar(np.arange(len(gate_values)), gate_values, color=["#4c78a8", "#2f9d55", "#c7302b", "#c7302b", "#c7302b"], width=0.62)
    axes[1].set_xticks(np.arange(len(gate_values)), gate_labels)
    axes[1].set_title("Launch and compute gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Local 2D baseline comparison contract: CPU-first, not launched", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, summary_json: Path, validation_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_baseline_comparison_contract.png`",
                "",
                "This CPU-only contract turns the baseline-readiness audit into",
                "explicit future same-case detector/database comparison targets.",
                "No detector, FDTD, FWI, GPU, field FWI, 3D/HPC, or neural-network",
                "run is launched by this artifact.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Contract rows: `{summary['contract_row_count']}`.",
                f"CPU-first contracts: `{summary['cpu_first_contract_count']}`.",
                f"Launch-now contracts: `{summary['launch_now_count']}`.",
                f"GPU-allowed contracts: `{summary['gpu_allowed_count']}`.",
                f"Highest priority: `{summary['highest_priority_contract']}`.",
                "",
                "Outputs:",
                "",
                f"- Contract rows: `{rows_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                f"- Figure validation: `{validation_csv.name}`.",
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
    parser.add_argument("--baseline-audit-run", default=DEFAULT_BASELINE_AUDIT_RUN)
    parser.add_argument("--contribution-run", default=DEFAULT_CONTRIBUTION_RUN)
    parser.add_argument("--synthetic-bundle-run", default=DEFAULT_SYNTHETIC_BUNDLE_RUN)
    parser.add_argument("--run-name", default="local_2d_baseline_comparison_contract")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    experiment_root = Path(args.experiment_root)

    baseline_summary = read_json(
        summary_root / args.baseline_audit_run / "data/local_2d_baseline_readiness_summary.json"
    )
    contribution_summary = read_json(
        summary_root / args.contribution_run / "data/local_2d_manuscript_contribution_summary.json"
    )
    synthetic_claims = read_csv_rows(
        experiment_root / args.synthetic_bundle_run / "data/synthetic_2d_publication_claim_boundaries.csv"
    )

    rows = build_contract_rows(
        baseline_summary=baseline_summary,
        contribution_summary=contribution_summary,
        synthetic_claims=synthetic_claims,
    )
    summary = summarize_contract(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_baseline_comparison_contract_rows.csv"
    summary_json = data_dir / "local_2d_baseline_comparison_contract_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_baseline_comparison_contract.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    plot_contract(rows, summary, figure_path)
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
        "local_2d_baseline_comparison_contract",
        {
            "baseline_audit_run": args.baseline_audit_run,
            "contribution_run": args.contribution_run,
            "synthetic_bundle_run": args.synthetic_bundle_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Integrate detector handoff failures with the close50 sampling boundary."""

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
from run_local_2d_detector_blind_envelope_robustness_audit import parse_bool  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_RELIABILITY_RUN = "069_local_2d_detector_blind_envelope_reliability_gate"
DEFAULT_STABILITY_RUN = "063_local_2d_detector_blind_envelope_policy_stability"
DEFAULT_ROBUSTNESS_RUN = "061_local_2d_detector_blind_envelope_robustness_audit"
DEFAULT_CONTRACT_RUN = "077_local_2d_detector_refinement_launch_contract_audit"
DEFAULT_PHYSICS_LINK_RUN = "074_local_2d_detector_physics_ambiguity_link"
DEFAULT_SAMPLING_BOUNDARY_RUN = "1338_close50_sampling_boundary_synthesis"
DEFAULT_STABLE_SLOT_RANGE_THRESHOLD_MM = 5.0


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def lookup(rows: list[dict], key: str) -> dict[str, dict]:
    return {str(row.get(key, "")): row for row in rows}


def close50_linear29p5_boundary(boundary_rows: list[dict]) -> dict:
    for row in boundary_rows:
        if row.get("sampling_family") != "linear_receiver":
            continue
        if math.isclose(safe_float(row.get("tx_rx_offset_mm"), math.nan), 29.5):
            return row
    return {}


def branch_offset(branch_key: str) -> float:
    if branch_key == "target2_close50_linear29p5":
        return 29.5
    return math.nan


def build_integration_rows(
    reliability_rows: list[dict],
    stability_rows: list[dict],
    robustness_split_rows: list[dict],
    contract_rows: list[dict],
    physics_rows: list[dict],
    boundary_rows: list[dict],
    *,
    stable_slot_range_threshold_mm: float = DEFAULT_STABLE_SLOT_RANGE_THRESHOLD_MM,
) -> list[dict]:
    stability_by_case = lookup(stability_rows, "case_label")
    contract_by_case = lookup(contract_rows, "case_label")
    physics_by_case = lookup(physics_rows, "case_label")
    branch_failures = set()
    for row in robustness_split_rows:
        if row.get("split_field") != "branch_key":
            continue
        labels = str(row.get("heldout_failed_case_labels", "")).split(";")
        branch_failures.update(label for label in labels if label)

    linear_boundary = close50_linear29p5_boundary(boundary_rows)
    first_clean = 30.0
    if linear_boundary:
        # The synthesized boundary file records 30 mm as the nearest-sampled clean threshold.
        first_clean = 30.0
    outputs = []
    for row in reliability_rows:
        case_label = str(row.get("case_label", ""))
        branch_key = str(row.get("branch_key", ""))
        case_variant = str(row.get("case_variant", ""))
        offset = branch_offset(branch_key)
        below_clean = math.isfinite(offset) and offset < first_clean
        reliability_label = str(
            row.get("truth_free_reliability_label", row.get("detector_reliability_label", ""))
        )
        stable_assignment = parse_bool(row.get("truth_free_stable_assignment"))
        detector_review = parse_bool(row.get("detector_review")) or reliability_label.startswith("review")
        if "truth_free_stable_assignment" in row:
            detector_review = not stable_assignment
        stability = stability_by_case.get(case_label, {})
        contract = contract_by_case.get(case_label, {})
        physics = physics_by_case.get(case_label, {})
        transfer_failure = case_label in branch_failures
        sampling_status = str(linear_boundary.get("boundary_status", "")) if below_clean else "not_in_close50_boundary"
        paper_role = str(linear_boundary.get("paper_role", "")) if below_clean else "detector_reference"
        if detector_review and below_clean and case_variant == "nominal":
            integration_label = "review_localized_to_sub30_nominal_caveat"
        elif transfer_failure and below_clean:
            integration_label = "branch_transfer_failure_on_sub30_caveat"
        elif below_clean:
            integration_label = "stable_despite_sub30_caveat"
        else:
            integration_label = "stable_reference_branch"
        outputs.append(
            {
                "case_label": case_label,
                "branch_key": branch_key,
                "seed": safe_int(row.get("seed"), 0),
                "case_variant": case_variant,
                "detector_reliability_label": reliability_label,
                "detector_review": detector_review,
                "detector_success_fraction": safe_float(
                    row.get("success_fraction_truth_eval", row.get("detector_success_fraction")), 0.0
                ),
                "detector_max_slot_x_range_mm": safe_float(
                    row.get("max_slot_x_range_mm", row.get("detector_max_slot_x_range_mm")), 0.0
                ),
                "truth_free_stable_under_slot_gate": (
                    safe_float(row.get("max_slot_x_range_mm", row.get("detector_max_slot_x_range_mm")), math.inf)
                    <= stable_slot_range_threshold_mm
                ),
                "policy_stability_label": stability.get("stability_label", ""),
                "policy_success_fraction": safe_float(stability.get("success_fraction"), math.nan),
                "branch_transfer_failure": transfer_failure,
                "candidate_component_seed_ready": parse_bool(contract.get("candidate_component_seed_ready")),
                "sampling_family": "linear_receiver" if below_clean else "",
                "sampling_tx_rx_offset_mm": offset,
                "sampling_first_clean_threshold_mm": first_clean if below_clean else math.nan,
                "sampling_below_clean_threshold": below_clean,
                "sampling_boundary_status": sampling_status,
                "sampling_paper_role": paper_role,
                "synthetic_x_ambiguous_row": parse_bool(physics.get("synthetic_x_ambiguous_row")),
                "synthetic_strict_clean_row": parse_bool(physics.get("synthetic_strict_clean_row")),
                "review_near_boundary_nominal": parse_bool(physics.get("review_near_boundary_nominal")),
                "integration_label": integration_label,
                "paper_use": (
                    "detector review supports close50 sub-30 caveat"
                    if detector_review
                    else "stable detector seed-table evidence"
                ),
                "gpu_action": "none",
            }
        )
    return sorted(outputs, key=lambda row: (row["branch_key"], row["seed"], row["case_variant"]))


def build_category_rows(rows: list[dict]) -> list[dict]:
    categories = [
        ("close14 stable reference", lambda row: row["branch_key"] == "target2_close14" and not row["detector_review"]),
        (
            "close50 source-mismatch stable",
            lambda row: row["branch_key"] == "target2_close50_linear29p5"
            and row["case_variant"] == "source_mismatch"
            and not row["detector_review"],
        ),
        (
            "close50 nominal stable",
            lambda row: row["branch_key"] == "target2_close50_linear29p5"
            and row["case_variant"] == "nominal"
            and not row["detector_review"],
        ),
        (
            "close50 nominal review",
            lambda row: row["branch_key"] == "target2_close50_linear29p5"
            and row["case_variant"] == "nominal"
            and row["detector_review"],
        ),
    ]
    output = []
    for label, predicate in categories:
        selected = [row for row in rows if predicate(row)]
        output.append(
            {
                "category": label,
                "case_count": len(selected),
                "review_case_count": sum(row["detector_review"] for row in selected),
                "below_clean_case_count": sum(row["sampling_below_clean_threshold"] for row in selected),
                "branch_transfer_failure_count": sum(row["branch_transfer_failure"] for row in selected),
                "candidate_component_seed_ready_count": sum(row["candidate_component_seed_ready"] for row in selected),
                "max_slot_x_range_mm": max(
                    [safe_float(row["detector_max_slot_x_range_mm"], 0.0) for row in selected] or [0.0]
                ),
            }
        )
    return output


def summarize_integration(rows: list[dict], category_rows: list[dict], sampling_summary: dict) -> dict:
    review_rows = [row for row in rows if row["detector_review"]]
    below_clean_rows = [row for row in rows if row["sampling_below_clean_threshold"]]
    review_below = [row for row in review_rows if row["sampling_below_clean_threshold"]]
    review_nominal = [row for row in review_rows if row["case_variant"] == "nominal"]
    transfer_failures = [row for row in rows if row["branch_transfer_failure"]]
    close50_nominal = [
        row
        for row in rows
        if row["branch_key"] == "target2_close50_linear29p5" and row["case_variant"] == "nominal"
    ]
    close50_source = [
        row
        for row in rows
        if row["branch_key"] == "target2_close50_linear29p5" and row["case_variant"] == "source_mismatch"
    ]
    x_ambiguous_reviews = [row for row in review_rows if row["synthetic_x_ambiguous_row"]]
    branch_localized = len(review_rows) > 0 and len(review_below) == len(review_rows) and len(review_nominal) == len(review_rows)
    return {
        "policy_label": "local_2d_detector_sampling_boundary_integration_cpu_no_fwi",
        "case_count": len(rows),
        "category_count": len(category_rows),
        "detector_review_case_count": len(review_rows),
        "review_below_clean_case_count": len(review_below),
        "review_nominal_case_count": len(review_nominal),
        "below_clean_case_count": len(below_clean_rows),
        "stable_below_clean_case_count": sum(not row["detector_review"] for row in below_clean_rows),
        "branch_transfer_failure_case_count": len(transfer_failures),
        "branch_transfer_failure_below_clean_case_count": sum(
            row["sampling_below_clean_threshold"] for row in transfer_failures
        ),
        "close50_nominal_case_count": len(close50_nominal),
        "close50_nominal_review_case_count": sum(row["detector_review"] for row in close50_nominal),
        "close50_source_mismatch_case_count": len(close50_source),
        "close50_source_mismatch_review_case_count": sum(row["detector_review"] for row in close50_source),
        "review_x_ambiguous_case_count": len(x_ambiguous_reviews),
        "sampling_first_clean_threshold_mm": sampling_summary.get("nearest_first_clean_replicated_tx_rx_mm", 30.0),
        "sampling_linear29p5_boundary_status": "exact_strong_not_clean",
        "sampling_ready_for_sub30_clean_threshold_claim": bool(
            sampling_summary.get("ready_for_sub30_clean_threshold_claim", False)
        ),
        "branch_localized_detector_boundary_claim_ready": branch_localized,
        "per_seed_physics_equivalence_ready": len(x_ambiguous_reviews) == len(review_rows) if review_rows else False,
        "ready_for_detector_sampling_boundary_claim": branch_localized,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_gpu_probe": False,
        "gpu_priority": "none",
        "decision": (
            "Detector review and branch-transfer failures are localized to the close50 linear 29.5 mm "
            "near-boundary caveat, especially nominal cases below the 30 mm clean threshold. This supports a "
            "branch-local detector ambiguity-boundary claim, but not per-seed physics equivalence or "
            "detector-seeded FWI."
        ),
    }


def plot_integration(rows: list[dict], category_rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["case_label"].replace("|", "\n") for row in rows]
    x_ranges = [safe_float(row["detector_max_slot_x_range_mm"], 0.0) for row in rows]
    colors = ["#e15759" if row["detector_review"] else "#59a14f" for row in rows]

    fig, axes = plt.subplots(1, 2, figsize=(14.2, 5.0), constrained_layout=True)
    axes[0].bar(np.arange(len(rows)), x_ranges, color=colors)
    axes[0].axhline(DEFAULT_STABLE_SLOT_RANGE_THRESHOLD_MM, color="#333333", linestyle="--", linewidth=0.9)
    axes[0].set_xticks(np.arange(len(rows)), labels, rotation=45, ha="right", fontsize=7)
    axes[0].set_ylabel("detector x-slot range [mm]")
    axes[0].set_title("Truth-free detector drift gate")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    cat_labels = [row["category"].replace(" ", "\n") for row in category_rows]
    case_counts = [safe_int(row["case_count"], 0) for row in category_rows]
    review_counts = [safe_int(row["review_case_count"], 0) for row in category_rows]
    index = np.arange(len(category_rows))
    axes[1].bar(index, case_counts, color="#4e79a7", label="cases")
    axes[1].bar(index, review_counts, color="#e15759", label="review")
    axes[1].set_xticks(index, cat_labels, fontsize=8)
    axes[1].set_ylabel("case count")
    axes[1].set_title("Review localization by branch/condition")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].text(
        0.03,
        0.95,
        f"review below clean: {summary['review_below_clean_case_count']}/{summary['detector_review_case_count']}\n"
        f"close50 nominal reviews: {summary['close50_nominal_review_case_count']}/{summary['close50_nominal_case_count']}\n"
        f"close50 source-mismatch reviews: {summary['close50_source_mismatch_review_case_count']}/{summary['close50_source_mismatch_case_count']}\n"
        f"detector FWI: {summary['ready_for_detector_seeded_fwi']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector and close50 sampling-boundary integration", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def build_gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "branch_localized_detector_boundary_claim",
            "ready": summary["branch_localized_detector_boundary_claim_ready"],
            "evidence": (
                f"review below clean={summary['review_below_clean_case_count']}/"
                f"{summary['detector_review_case_count']}; review nominal="
                f"{summary['review_nominal_case_count']}/{summary['detector_review_case_count']}"
            ),
            "allowed_use": "detector ambiguity-boundary manuscript claim",
            "blocked_use": "global detector policy fix",
        },
        {
            "gate_key": "per_seed_physics_equivalence",
            "ready": summary["per_seed_physics_equivalence_ready"],
            "evidence": (
                f"x-ambiguous reviews={summary['review_x_ambiguous_case_count']}/"
                f"{summary['detector_review_case_count']}"
            ),
            "allowed_use": "none",
            "blocked_use": "claiming every detector review is explained by per-seed coordinate ambiguity",
        },
        {
            "gate_key": "sub30_clean_threshold",
            "ready": summary["sampling_ready_for_sub30_clean_threshold_claim"],
            "evidence": "close50 linear 29.5 mm is exact/strong but not clean; nearest 30 mm is clean replicated",
            "allowed_use": "sub-30 caveat text",
            "blocked_use": "sub-30 clean threshold claim",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "evidence": "review cases and launch-contract blockers remain",
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI or GPU probe",
        },
    ]


def write_figure_notes(path: Path, summary: dict, cases_csv: Path, categories_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_sampling_boundary_integration.png`",
                "",
                "This CPU-only figure integrates detector reliability/stability rows",
                "with the close50 sampling-boundary synthesis. It reads saved tables",
                "only and does not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC, or",
                "neural-network training.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Detector review cases: `{summary['detector_review_case_count']}`.",
                f"Review cases below clean threshold: `{summary['review_below_clean_case_count']}`.",
                f"Close50 nominal review cases: `{summary['close50_nominal_review_case_count']}`.",
                f"Per-seed physics equivalence ready: `{summary['per_seed_physics_equivalence_ready']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Case rows: `{cases_csv.name}`.",
                f"- Category rows: `{categories_csv.name}`.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--experiment-root", default="outputs/experiments")
    parser.add_argument("--reliability-run", default=DEFAULT_RELIABILITY_RUN)
    parser.add_argument("--stability-run", default=DEFAULT_STABILITY_RUN)
    parser.add_argument("--robustness-run", default=DEFAULT_ROBUSTNESS_RUN)
    parser.add_argument("--contract-run", default=DEFAULT_CONTRACT_RUN)
    parser.add_argument("--physics-link-run", default=DEFAULT_PHYSICS_LINK_RUN)
    parser.add_argument("--sampling-boundary-run", default=DEFAULT_SAMPLING_BOUNDARY_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_sampling_boundary_integration")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    experiment_root = Path(args.experiment_root)
    reliability_dir = summary_root / args.reliability_run
    stability_dir = summary_root / args.stability_run
    robustness_dir = summary_root / args.robustness_run
    contract_dir = summary_root / args.contract_run
    physics_dir = summary_root / args.physics_link_run
    sampling_dir = experiment_root / args.sampling_boundary_run

    reliability_rows = read_csv_rows(reliability_dir / "data/local_2d_detector_blind_envelope_reliability_gate_cases.csv")
    stability_rows = read_csv_rows(stability_dir / "data/local_2d_detector_blind_envelope_policy_stability_cases.csv")
    robustness_split_rows = read_csv_rows(
        robustness_dir / "data/local_2d_detector_blind_envelope_robustness_split_rows.csv"
    )
    contract_rows = read_csv_rows(contract_dir / "data/local_2d_detector_refinement_launch_contract_cases.csv")
    physics_rows = read_csv_rows(physics_dir / "data/local_2d_detector_physics_ambiguity_link_cases.csv")
    boundary_rows = read_csv_rows(sampling_dir / "data/close50_sampling_boundary_rows.csv")
    sampling_summary = read_json(sampling_dir / "data/close50_sampling_boundary_synthesis_summary.json")

    case_rows = build_integration_rows(
        reliability_rows,
        stability_rows,
        robustness_split_rows,
        contract_rows,
        physics_rows,
        boundary_rows,
    )
    category_rows = build_category_rows(case_rows)
    summary = summarize_integration(case_rows, category_rows, sampling_summary)
    gates = build_gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    cases_csv = data_dir / "local_2d_detector_sampling_boundary_integration_cases.csv"
    categories_csv = data_dir / "local_2d_detector_sampling_boundary_integration_categories.csv"
    gates_csv = data_dir / "local_2d_detector_sampling_boundary_integration_gates.csv"
    summary_json = data_dir / "local_2d_detector_sampling_boundary_integration_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_sampling_boundary_integration.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(cases_csv, [json_safe(row) for row in case_rows])
    write_csv(categories_csv, [json_safe(row) for row in category_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_integration(case_rows, category_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, cases_csv, categories_csv)

    summary["paths"] = {
        "case_rows_csv": str(cases_csv),
        "category_rows_csv": str(categories_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "source_reliability_cases_csv": str(
            reliability_dir / "data/local_2d_detector_blind_envelope_reliability_gate_cases.csv"
        ),
        "source_stability_cases_csv": str(
            stability_dir / "data/local_2d_detector_blind_envelope_policy_stability_cases.csv"
        ),
        "source_robustness_split_csv": str(
            robustness_dir / "data/local_2d_detector_blind_envelope_robustness_split_rows.csv"
        ),
        "source_contract_cases_csv": str(
            contract_dir / "data/local_2d_detector_refinement_launch_contract_cases.csv"
        ),
        "source_physics_cases_csv": str(
            physics_dir / "data/local_2d_detector_physics_ambiguity_link_cases.csv"
        ),
        "source_sampling_boundary_rows_csv": str(sampling_dir / "data/close50_sampling_boundary_rows.csv"),
        "source_sampling_boundary_summary_json": str(
            sampling_dir / "data/close50_sampling_boundary_synthesis_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_sampling_boundary_integration",
        {
            "reliability_run": args.reliability_run,
            "stability_run": args.stability_run,
            "robustness_run": args.robustness_run,
            "contract_run": args.contract_run,
            "physics_link_run": args.physics_link_run,
            "sampling_boundary_run": args.sampling_boundary_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

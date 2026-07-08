#!/usr/bin/env python3
"""Audit robustness of the blind component-envelope detector assignment."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
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
from run_local_2d_detector_blind_component_envelope_assembly import (  # noqa: E402
    DEFAULT_COMPONENT_GATE_RUN,
    EVALUATION_X_SLOTS,
    case_key,
    mode_for_span,
    precompute_case_features,
    read_csv_rows,
    safe_float,
    safe_int,
    sort_variants,
    summarize_variant,
    target_slot_evaluation,
)
from run_local_2d_detector_rank_budget_diagnostic import read_json  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_BLIND_ENVELOPE_RUN = "059_local_2d_detector_blind_component_envelope_assembly"
MARGIN_REVIEW_THRESHOLD = 0.10


def parse_bool(value) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def variant_spec(row: dict) -> dict:
    return {
        "variant_label": str(row["variant_label"]),
        "envelope_weight": safe_float(row.get("envelope_weight"), 0.0),
        "structural_weight": safe_float(row.get("structural_weight"), 0.0),
        "support_weight": safe_float(row.get("support_weight"), 0.0),
        "center_weight": safe_float(row.get("center_weight"), 0.0),
        "span_threshold_mm": safe_float(row.get("span_threshold_mm"), 0.0),
    }


def group_by_variant(selected_rows: list[dict]) -> tuple[dict[str, list[dict]], dict[str, dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    specs = {}
    for row in selected_rows:
        label = str(row["variant_label"])
        grouped[label].append(row)
        specs[label] = variant_spec(row)
    return grouped, specs


def selected_variant_for_training(
    grouped: dict[str, list[dict]],
    specs: dict[str, dict],
    *,
    holdout_field: str,
    holdout_value: str,
) -> dict:
    training_summaries = []
    for label, rows in grouped.items():
        training_rows = [row for row in rows if str(row.get(holdout_field, "")) != str(holdout_value)]
        training_summaries.append(summarize_variant(training_rows, specs[label]))
    return sort_variants(training_summaries)[0]


def heldout_split_rows(selected_rows: list[dict], split_field: str) -> list[dict]:
    grouped, specs = group_by_variant(selected_rows)
    split_rows = []
    for holdout_value in sorted({str(row.get(split_field, "")) for row in selected_rows}):
        selected_variant = selected_variant_for_training(
            grouped,
            specs,
            holdout_field=split_field,
            holdout_value=holdout_value,
        )
        label = str(selected_variant["variant_label"])
        heldout_rows = [row for row in grouped[label] if str(row.get(split_field, "")) == holdout_value]
        case_count = len(heldout_rows)
        all_slot_count = sum(parse_bool(row.get("all_target_slots_hit")) for row in heldout_rows)
        split_rows.append(
            {
                "split_field": split_field,
                "holdout_value": holdout_value,
                "selected_variant_label": label,
                "selected_envelope_weight": safe_float(selected_variant.get("envelope_weight"), 0.0),
                "selected_structural_weight": safe_float(selected_variant.get("structural_weight"), 0.0),
                "selected_support_weight": safe_float(selected_variant.get("support_weight"), 0.0),
                "selected_center_weight": safe_float(selected_variant.get("center_weight"), 0.0),
                "selected_span_threshold_mm": safe_float(selected_variant.get("span_threshold_mm"), 0.0),
                "training_case_count": safe_int(selected_variant.get("case_count"), 0),
                "training_all_target_slot_case_count": safe_int(selected_variant.get("all_target_slot_case_count"), 0),
                "heldout_case_count": case_count,
                "heldout_all_target_slot_case_count": all_slot_count,
                "heldout_failed_case_count": case_count - all_slot_count,
                "heldout_mean_target_slot_hit_count": float(
                    np.mean([safe_float(row.get("target_slot_hit_count"), 0.0) for row in heldout_rows])
                )
                if heldout_rows
                else 0.0,
                "heldout_failed_case_labels": ";".join(
                    str(row.get("case_label", ""))
                    for row in heldout_rows
                    if not parse_bool(row.get("all_target_slots_hit"))
                ),
            }
        )
    return split_rows


def summarize_split_rows(rows: list[dict], prefix: str) -> dict:
    case_count = sum(safe_int(row.get("heldout_case_count"), 0) for row in rows)
    all_case_count = sum(safe_int(row.get("heldout_all_target_slot_case_count"), 0) for row in rows)
    return {
        f"{prefix}_split_count": len(rows),
        f"{prefix}_case_count": case_count,
        f"{prefix}_all_target_slot_case_count": all_case_count,
        f"{prefix}_failed_case_count": case_count - all_case_count,
        f"{prefix}_mean_target_slot_hit_count": float(
            np.average(
                [safe_float(row.get("heldout_mean_target_slot_hit_count"), 0.0) for row in rows],
                weights=[safe_int(row.get("heldout_case_count"), 0) for row in rows],
            )
        )
        if case_count
        else 0.0,
    }


def component_rows_by_case(rows: list[dict]) -> dict[tuple[str, str, str, str], list[dict]]:
    grouped: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[case_key(row)].append(row)
    return grouped


def triple_score(case_feature: dict, triple: dict, variant: dict) -> tuple[float, str]:
    mode = mode_for_span(
        safe_float(case_feature.get("observed_support_span_mm"), 0.0),
        safe_float(variant.get("span_threshold_mm"), 0.0),
    )
    structural_key = "pair_structure_score" if mode == "close_pair" else "regular_structure_score"
    center_weight = 0.0 if mode == "close_pair" else safe_float(variant.get("center_weight"), 0.0)
    score = (
        safe_float(triple.get("base_sum"), 0.0)
        + safe_float(variant.get("envelope_weight"), 0.0) * safe_float(triple.get("edge_envelope_score"), 0.0)
        + safe_float(variant.get("structural_weight"), 0.0) * safe_float(triple.get(structural_key), 0.0)
        + safe_float(variant.get("support_weight"), 0.0) * safe_float(triple.get("support_score"), 0.0)
        + center_weight * safe_float(triple.get("regular_center_score"), 0.0)
    )
    return score, mode


def ranked_triples_for_case(case_feature: dict, variant: dict) -> list[dict]:
    expected_slots = EVALUATION_X_SLOTS.get(str(case_feature.get("branch_key", "")), ())
    ranked = []
    for triple in case_feature["candidate_triples"]:
        score, mode = triple_score(case_feature, triple, variant)
        evaluation = target_slot_evaluation(triple["selected_components"], expected_slots)
        ranked.append(
            {
                "selection_score": score,
                "selection_mode": mode,
                "selected_x_values_mm": ",".join(f"{x:g}" for x in triple["selected_x"]),
                "selected_z_values_mm": ",".join(f"{z:g}" for z in triple["selected_z"]),
                "selected_ranks": ",".join(f"{rank:g}" for rank in triple["selected_ranks"]),
                "target_slot_hit_count": safe_int(evaluation["target_slot_hit_count"], 0),
                "all_target_slots_hit": bool(evaluation["all_target_slots_hit"]),
                "max_target_slot_abs_error_mm": max(evaluation["target_slot_abs_errors_mm"] or [math.inf]),
            }
        )
    return sorted(
        ranked,
        key=lambda row: (
            safe_float(row["selection_score"], -math.inf),
            safe_int(row["target_slot_hit_count"], 0),
            str(row["selected_x_values_mm"]),
        ),
        reverse=True,
    )


def margin_rows(component_rows: list[dict], variant: dict) -> list[dict]:
    rows = []
    for key, case_rows in component_rows_by_case(component_rows).items():
        case_feature = precompute_case_features(key, case_rows)
        ranked = ranked_triples_for_case(case_feature, variant)
        top = ranked[0]
        first_all_index = next(
            (index for index, row in enumerate(ranked, start=1) if row["all_target_slots_hit"]),
            None,
        )
        best_wrong = next((row for row in ranked if not row["all_target_slots_hit"]), None)
        margin = (
            safe_float(top["selection_score"], 0.0) - safe_float(best_wrong["selection_score"], 0.0)
            if best_wrong is not None
            else math.inf
        )
        rows.append(
            {
                "case_label": case_feature["case_label"],
                "branch_key": case_feature["branch_key"],
                "seed": case_feature["seed"],
                "case_variant": case_feature["case_variant"],
                "selected_variant_label": variant["variant_label"],
                "top_all_target_slots_hit": bool(top["all_target_slots_hit"]),
                "top_target_slot_hit_count": safe_int(top["target_slot_hit_count"], 0),
                "first_all_target_slot_rank": safe_int(first_all_index, 0),
                "top_selection_score": safe_float(top["selection_score"], 0.0),
                "best_wrong_selection_score": safe_float(best_wrong["selection_score"], math.nan)
                if best_wrong is not None
                else math.inf,
                "truth_vs_wrong_score_margin": margin,
                "margin_below_review_threshold": margin < MARGIN_REVIEW_THRESHOLD,
                "top_selected_x_values_mm": top["selected_x_values_mm"],
                "best_wrong_selected_x_values_mm": best_wrong["selected_x_values_mm"] if best_wrong else "",
                "best_wrong_target_slot_hit_count": safe_int(best_wrong["target_slot_hit_count"], 0)
                if best_wrong
                else 0,
                "top_max_target_slot_abs_error_mm": safe_float(top["max_target_slot_abs_error_mm"], math.inf),
            }
        )
    return sorted(rows, key=lambda row: safe_float(row["truth_vs_wrong_score_margin"], math.inf))


def summarize_audit(
    variant_rows: list[dict],
    split_rows: list[dict],
    margins: list[dict],
    source_summary: dict,
) -> dict:
    seed_summary = summarize_split_rows([row for row in split_rows if row["split_field"] == "seed"], "leave_one_seed")
    branch_summary = summarize_split_rows(
        [row for row in split_rows if row["split_field"] == "branch_key"], "leave_one_branch"
    )
    condition_summary = summarize_split_rows(
        [row for row in split_rows if row["split_field"] == "case_variant"], "leave_one_condition"
    )
    case_count = safe_int(source_summary.get("case_count"), 0)
    full_success_variants = [
        row for row in variant_rows if safe_int(row.get("all_target_slot_case_count"), 0) == case_count
    ]
    near_success_variants = [
        row for row in variant_rows if safe_int(row.get("all_target_slot_case_count"), 0) >= max(case_count - 1, 0)
    ]
    finite_margins = [
        safe_float(row.get("truth_vs_wrong_score_margin"), math.nan)
        for row in margins
        if math.isfinite(safe_float(row.get("truth_vs_wrong_score_margin"), math.nan))
    ]
    min_margin = min(finite_margins) if finite_margins else math.inf
    branch_ready = branch_summary["leave_one_branch_all_target_slot_case_count"] == branch_summary["leave_one_branch_case_count"]
    seed_ready = seed_summary["leave_one_seed_all_target_slot_case_count"] == seed_summary["leave_one_seed_case_count"]
    condition_ready = (
        condition_summary["leave_one_condition_all_target_slot_case_count"]
        == condition_summary["leave_one_condition_case_count"]
    )
    return {
        "policy_label": "local_2d_detector_blind_envelope_robustness_audit_cpu_no_fwi",
        "source_policy_label": source_summary.get("policy_label", ""),
        "case_count": case_count,
        "variant_count": len(variant_rows),
        "full_success_variant_count": len(full_success_variants),
        "near_success_variant_count": len(near_success_variants),
        "source_best_all_target_slot_case_count": safe_int(source_summary.get("best_all_target_slot_case_count"), 0),
        "source_leave_one_case_all_target_slot_case_count": safe_int(
            source_summary.get("leave_one_case_all_target_slot_case_count"), 0
        ),
        **seed_summary,
        **branch_summary,
        **condition_summary,
        "best_variant_min_truth_vs_wrong_score_margin": min_margin,
        "best_variant_median_truth_vs_wrong_score_margin": float(np.median(finite_margins)) if finite_margins else math.inf,
        "best_variant_low_margin_case_count": sum(
            bool(row.get("margin_below_review_threshold", False)) for row in margins
        ),
        "best_variant_first_all_rank_max": max(
            [safe_int(row.get("first_all_target_slot_rank"), 0) for row in margins] or [0]
        ),
        "heldout_seed_robust": seed_ready,
        "heldout_branch_robust": branch_ready,
        "heldout_condition_robust": condition_ready,
        "robustness_boundary": (
            "seed_and_condition_robust_but_not_branch_independent"
            if seed_ready and condition_ready and not branch_ready
            else "all_tested_splits_robust"
            if seed_ready and condition_ready and branch_ready
            else "review_required"
        ),
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "The blind-envelope assignment is robust across held-out seeds and source-condition splits, and many "
            "variants recover all saved cases. It is not fully branch-independent under leave-one-branch training, "
            "and one selected case has a low truth-versus-wrong score margin. Keep this as CPU-side detector "
            "handoff evidence, not a detector-seeded FWI trigger."
        ),
    }


def plot_audit(split_rows: list[dict], margins: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.8, 4.8), constrained_layout=True)
    labels = ["source\nbest", "leave-one\ncase", "leave-one\nseed", "leave-one\nbranch", "leave-one\ncondition"]
    values = [
        summary["source_best_all_target_slot_case_count"],
        summary["source_leave_one_case_all_target_slot_case_count"],
        summary["leave_one_seed_all_target_slot_case_count"],
        summary["leave_one_branch_all_target_slot_case_count"],
        summary["leave_one_condition_all_target_slot_case_count"],
    ]
    axes[0].bar(np.arange(len(labels)), values, color=["#59a14f", "#4e79a7", "#4e79a7", "#f28e2b", "#4e79a7"])
    axes[0].set_xticks(np.arange(len(labels)), labels)
    axes[0].set_ylim(0, max(summary["case_count"], 1))
    axes[0].set_ylabel("all-slot cases")
    axes[0].set_title("Held-out split recovery")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    margin_values = [safe_float(row["truth_vs_wrong_score_margin"], 0.0) for row in margins]
    axes[1].bar(np.arange(len(margin_values)), margin_values, color="#76b7b2")
    axes[1].axhline(MARGIN_REVIEW_THRESHOLD, color="#e15759", linestyle="--", linewidth=1.0)
    axes[1].set_xticks(np.arange(len(margin_values)), [row["case_label"].replace("|", "\n") for row in margins], rotation=45, ha="right", fontsize=7)
    axes[1].set_ylabel("score margin")
    axes[1].set_title("Best variant margin vs wrong triple")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.96,
        f"full-success variants: {summary['full_success_variant_count']}\n"
        f"min margin: {summary['best_variant_min_truth_vs_wrong_score_margin']:.3f}\n"
        f"boundary: {summary['robustness_boundary']}",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D blind-envelope detector robustness audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, split_csv: Path, margin_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_blind_envelope_robustness_audit.png`",
                "",
                "This CPU-only figure audits held-out split robustness and",
                "truth-versus-wrong score margins for the blind component-envelope",
                "detector assignment policy.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Full-success variants: `{summary['full_success_variant_count']}`.",
                f"Leave-one-seed all-slot cases: `{summary['leave_one_seed_all_target_slot_case_count']}`.",
                f"Leave-one-branch all-slot cases: `{summary['leave_one_branch_all_target_slot_case_count']}`.",
                f"Leave-one-condition all-slot cases: `{summary['leave_one_condition_all_target_slot_case_count']}`.",
                f"Minimum truth-versus-wrong score margin: `{summary['best_variant_min_truth_vs_wrong_score_margin']}`.",
                f"Robustness boundary: `{summary['robustness_boundary']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Held-out split rows: `{split_csv.name}`.",
                f"- Margin rows: `{margin_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved detector component rows and saved blind-envelope",
                "policy rows only. It does not run FDTD, FWI, GPU kernels, field FWI,",
                "3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--blind-envelope-run", default=DEFAULT_BLIND_ENVELOPE_RUN)
    parser.add_argument("--component-gate-run", default=DEFAULT_COMPONENT_GATE_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_blind_envelope_robustness_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    source_dir = summary_root / args.blind_envelope_run
    component_dir = summary_root / args.component_gate_run

    source_summary = read_json(
        source_dir / "data/local_2d_detector_blind_component_envelope_assembly_summary.json"
    )
    variant_rows = read_csv_rows(
        source_dir / "data/local_2d_detector_blind_component_envelope_assembly_variants.csv"
    )
    selected_rows = read_csv_rows(
        source_dir / "data/local_2d_detector_blind_component_envelope_assembly_selected_cases.csv"
    )
    component_rows = read_csv_rows(
        component_dir / "data/local_2d_detector_component_waveform_gate_rows.csv"
    )

    split_rows = []
    for split_field in ("seed", "branch_key", "case_variant"):
        split_rows.extend(heldout_split_rows(selected_rows, split_field))
    best_variant = variant_spec(sort_variants(variant_rows)[0])
    margins = margin_rows(component_rows, best_variant)
    summary = summarize_audit(variant_rows, split_rows, margins, source_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    split_csv = data_dir / "local_2d_detector_blind_envelope_robustness_split_rows.csv"
    margin_csv = data_dir / "local_2d_detector_blind_envelope_robustness_margin_rows.csv"
    summary_json = data_dir / "local_2d_detector_blind_envelope_robustness_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_blind_envelope_robustness_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(split_csv, [json_safe(row) for row in split_rows])
    write_csv(margin_csv, [json_safe(row) for row in margins])
    plot_audit(split_rows, margins, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, split_csv, margin_csv)
    summary["paths"] = {
        "split_rows_csv": str(split_csv),
        "margin_rows_csv": str(margin_csv),
        "summary_json": str(summary_json),
        "source_blind_envelope_summary_json": str(
            source_dir / "data/local_2d_detector_blind_component_envelope_assembly_summary.json"
        ),
        "source_blind_envelope_variants_csv": str(
            source_dir / "data/local_2d_detector_blind_component_envelope_assembly_variants.csv"
        ),
        "source_blind_envelope_selected_cases_csv": str(
            source_dir / "data/local_2d_detector_blind_component_envelope_assembly_selected_cases.csv"
        ),
        "source_component_rows_csv": str(component_dir / "data/local_2d_detector_component_waveform_gate_rows.csv"),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_blind_envelope_robustness_audit",
        {
            "blind_envelope_run": args.blind_envelope_run,
            "component_gate_run": args.component_gate_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

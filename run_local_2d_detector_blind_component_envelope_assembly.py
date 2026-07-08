#!/usr/bin/env python3
"""Probe truth-free envelope assembly of saved local 2D detector components."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from itertools import combinations, permutations
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
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from run_local_2d_detector_slot_component_assembly_probe import (  # noqa: E402
    EXPECTED_X_SLOTS as EVALUATION_X_SLOTS,
    component_base_score,
    component_rows_for_case,
)
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_COMPONENT_GATE_RUN = "035_local_2d_detector_component_waveform_gate_post_rank_budget"
DEFAULT_DEPTH_SLOT_PRIOR_RUN = "055_local_2d_detector_depth_slot_prior_probe"
DEFAULT_SLOT_COMPONENT_RUN = "057_local_2d_detector_slot_component_assembly_probe"
ENVELOPE_WEIGHTS = (1.0, 2.0, 4.0, 6.0)
STRUCTURAL_WEIGHTS = (0.0, 0.4, 0.6, 0.8)
SUPPORT_WEIGHTS = (0.0, 0.08, 0.12)
CENTER_WEIGHTS = (0.0, 0.1)
SPAN_THRESHOLDS_MM = (90.0, 100.0, 105.0)
SUPPORT_BANDWIDTH_MM = 8.0
EDGE_SCALE_MM = 30.0
PAIR_SMALL_GAP_MM = 14.0
PAIR_BROAD_GAP_MM = 60.0
STRUCTURAL_SCALE_MM = 60.0
CENTER_SCALE_MM = 40.0
TARGET_TOLERANCE_MM = 10.0


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def case_key(row: dict) -> tuple[str, str, str, str]:
    return (
        str(row.get("branch_key", "")),
        str(row.get("seed", "")),
        str(row.get("case_variant", "")),
        str(row.get("run_name", "")),
    )


def case_label_from_key(key: tuple[str, str, str, str]) -> str:
    branch_key, seed, case_variant, _run_name = key
    return f"{branch_key}|seed{seed}|{case_variant}"


def component_score(component: dict) -> float:
    return component_base_score(component, score_weight=1.0, depth_weight=1.0, rank_weight=0.02)


def quantile(values: list[float], q: float) -> float:
    return float(np.quantile(np.asarray(values, dtype=float), q))


def mode_for_span(observed_span_mm: float, span_threshold_mm: float) -> str:
    return "close_pair" if float(observed_span_mm) < float(span_threshold_mm) else "regular"


def pair_structure_score(gaps: tuple[float, float]) -> float:
    small_gap = min(gaps)
    broad_gap = max(gaps)
    return -(
        abs(small_gap - PAIR_SMALL_GAP_MM) + abs(broad_gap - PAIR_BROAD_GAP_MM)
    ) / STRUCTURAL_SCALE_MM


def regular_structure_score(gaps: tuple[float, float]) -> float:
    return -abs(gaps[0] - gaps[1]) / STRUCTURAL_SCALE_MM


def target_slot_evaluation(selected: list[dict], expected_slots: tuple[float, ...], tolerance_mm: float = TARGET_TOLERANCE_MM) -> dict:
    if len(selected) < len(expected_slots):
        return {
            "target_slot_hit_count": 0,
            "all_target_slots_hit": False,
            "target_slot_hit_flags": [False for _slot in expected_slots],
            "target_slot_abs_errors_mm": [math.inf for _slot in expected_slots],
        }

    selected_x = [safe_float(component.get("x_mm"), math.inf) for component in selected]
    best_order = min(
        permutations(range(len(selected_x)), len(expected_slots)),
        key=lambda order: sum(abs(selected_x[index] - expected_slots[target_index]) for target_index, index in enumerate(order)),
    )
    errors = [
        abs(selected_x[index] - expected_slots[target_index])
        for target_index, index in enumerate(best_order)
    ]
    hits = [error <= tolerance_mm for error in errors]
    return {
        "target_slot_hit_count": sum(hits),
        "all_target_slots_hit": all(hits),
        "target_slot_hit_flags": hits,
        "target_slot_abs_errors_mm": errors,
    }


def precompute_case_features(key: tuple[str, str, str, str], case_rows: list[dict]) -> dict:
    components = component_rows_for_case(case_rows)
    x_values = [safe_float(component.get("x_mm"), 0.0) for component in components]
    q10 = quantile(x_values, 0.10)
    q90 = quantile(x_values, 0.90)
    observed_span = q90 - q10
    support_weights = [max(0.0, component_score(component) + 0.5) for component in components]

    candidate_triples = []
    for indices in combinations(range(len(components)), 3):
        selected = [components[index] for index in indices]
        selected_by_x = sorted(selected, key=lambda component: safe_float(component.get("x_mm"), 0.0))
        sorted_x = tuple(safe_float(component.get("x_mm"), 0.0) for component in selected_by_x)
        gaps = (sorted_x[1] - sorted_x[0], sorted_x[2] - sorted_x[1])
        if min(gaps) < 5.0:
            continue
        support_score = 0.0
        for component, support_weight in zip(components, support_weights):
            distance = min(abs(safe_float(component.get("x_mm"), 0.0) - selected_x) for selected_x in sorted_x)
            support_score += support_weight * math.exp(-((distance / SUPPORT_BANDWIDTH_MM) ** 2))
        midpoint = (sorted_x[0] + sorted_x[2]) / 2.0
        candidate_triples.append(
            {
                "selected_components": selected_by_x,
                "selected_x": sorted_x,
                "selected_z": tuple(safe_float(component.get("z_mm"), 0.0) for component in selected_by_x),
                "selected_ranks": tuple(safe_float(component.get("rank"), 999.0) for component in selected_by_x),
                "base_sum": sum(component_score(component) for component in selected_by_x),
                "edge_envelope_score": -(abs(sorted_x[0] - q10) + abs(sorted_x[2] - q90)) / EDGE_SCALE_MM,
                "support_score": support_score,
                "regular_structure_score": regular_structure_score(gaps),
                "pair_structure_score": pair_structure_score(gaps),
                "regular_center_score": -abs(sorted_x[1] - midpoint) / CENTER_SCALE_MM,
                "x_span_mm": sorted_x[2] - sorted_x[0],
                "gap_left_mm": gaps[0],
                "gap_right_mm": gaps[1],
            }
        )

    branch_key, seed, case_variant, run_name = key
    return {
        "case_key": key,
        "case_label": case_label_from_key(key),
        "branch_key": branch_key,
        "seed": safe_int(seed),
        "case_variant": case_variant,
        "run_name": run_name,
        "component_candidate_count": len(components),
        "support_q10_mm": q10,
        "support_q90_mm": q90,
        "observed_support_span_mm": observed_span,
        "candidate_triples": candidate_triples,
    }


def variant_label(envelope_weight: float, structural_weight: float, support_weight: float, center_weight: float, span_threshold_mm: float) -> str:
    return (
        f"env{envelope_weight:g}_struct{structural_weight:g}_support{support_weight:g}_"
        f"center{center_weight:g}_span{span_threshold_mm:g}"
    )


def variant_grid(
    *,
    envelope_weights: tuple[float, ...] = ENVELOPE_WEIGHTS,
    structural_weights: tuple[float, ...] = STRUCTURAL_WEIGHTS,
    support_weights: tuple[float, ...] = SUPPORT_WEIGHTS,
    center_weights: tuple[float, ...] = CENTER_WEIGHTS,
    span_thresholds_mm: tuple[float, ...] = SPAN_THRESHOLDS_MM,
) -> list[dict]:
    rows = []
    for envelope_weight in envelope_weights:
        for structural_weight in structural_weights:
            for support_weight in support_weights:
                for center_weight in center_weights:
                    for span_threshold_mm in span_thresholds_mm:
                        rows.append(
                            {
                                "variant_label": variant_label(
                                    envelope_weight,
                                    structural_weight,
                                    support_weight,
                                    center_weight,
                                    span_threshold_mm,
                                ),
                                "envelope_weight": float(envelope_weight),
                                "structural_weight": float(structural_weight),
                                "support_weight": float(support_weight),
                                "center_weight": float(center_weight),
                                "span_threshold_mm": float(span_threshold_mm),
                            }
                        )
    return rows


def select_components_for_variant(case_feature: dict, variant: dict) -> dict:
    mode = mode_for_span(
        safe_float(case_feature.get("observed_support_span_mm"), 0.0),
        safe_float(variant.get("span_threshold_mm"), 0.0),
    )
    structural_key = "pair_structure_score" if mode == "close_pair" else "regular_structure_score"
    center_weight = 0.0 if mode == "close_pair" else safe_float(variant.get("center_weight"), 0.0)
    best = None
    for triple in case_feature["candidate_triples"]:
        selection_score = (
            safe_float(triple.get("base_sum"), 0.0)
            + safe_float(variant.get("envelope_weight"), 0.0) * safe_float(triple.get("edge_envelope_score"), 0.0)
            + safe_float(variant.get("structural_weight"), 0.0) * safe_float(triple.get(structural_key), 0.0)
            + safe_float(variant.get("support_weight"), 0.0) * safe_float(triple.get("support_score"), 0.0)
            + center_weight * safe_float(triple.get("regular_center_score"), 0.0)
        )
        sort_key = (
            selection_score,
            safe_float(triple.get("edge_envelope_score"), 0.0),
            safe_float(triple.get("support_score"), 0.0),
            safe_float(triple.get("base_sum"), 0.0),
            -abs(safe_float(triple.get("gap_left_mm"), 0.0) - safe_float(triple.get("gap_right_mm"), 0.0)),
            tuple(-x for x in triple["selected_x"]),
        )
        if best is None or sort_key > best["sort_key"]:
            best = {
                **triple,
                "selection_score": selection_score,
                "selection_mode": mode,
                "active_structure_score": safe_float(triple.get(structural_key), 0.0),
                "sort_key": sort_key,
            }
    if best is None:
        raise ValueError(f"no selectable component triples for case {case_feature['case_label']}")
    return best


def selected_case_output(case_feature: dict, variant: dict) -> dict:
    selected = select_components_for_variant(case_feature, variant)
    expected_slots = EVALUATION_X_SLOTS.get(str(case_feature.get("branch_key", "")), ())
    slot_eval = target_slot_evaluation(selected["selected_components"], expected_slots)
    return {
        **variant,
        "case_label": case_feature["case_label"],
        "branch_key": case_feature["branch_key"],
        "seed": case_feature["seed"],
        "case_variant": case_feature["case_variant"],
        "run_name": case_feature["run_name"],
        "selection_mode": selected["selection_mode"],
        "component_candidate_count": case_feature["component_candidate_count"],
        "support_q10_mm": case_feature["support_q10_mm"],
        "support_q90_mm": case_feature["support_q90_mm"],
        "observed_support_span_mm": case_feature["observed_support_span_mm"],
        "selected_component_count": len(selected["selected_components"]),
        "selected_x_values_mm": ",".join(f"{x:g}" for x in selected["selected_x"]),
        "selected_z_values_mm": ",".join(f"{z:g}" for z in selected["selected_z"]),
        "selected_ranks": ",".join(f"{rank:g}" for rank in selected["selected_ranks"]),
        "selection_score": selected["selection_score"],
        "selected_base_sum": selected["base_sum"],
        "edge_envelope_score": selected["edge_envelope_score"],
        "support_score": selected["support_score"],
        "active_structure_score": selected["active_structure_score"],
        "regular_structure_score": selected["regular_structure_score"],
        "pair_structure_score": selected["pair_structure_score"],
        "regular_center_score": selected["regular_center_score"],
        "x_span_mm": selected["x_span_mm"],
        "gap_left_mm": selected["gap_left_mm"],
        "gap_right_mm": selected["gap_right_mm"],
        "target_slot_hit_count": slot_eval["target_slot_hit_count"],
        "all_target_slots_hit": slot_eval["all_target_slots_hit"],
        "target_slot_hit_flags": ",".join("1" if hit else "0" for hit in slot_eval["target_slot_hit_flags"]),
        "target_slot_abs_errors_mm": ",".join(f"{error:g}" for error in slot_eval["target_slot_abs_errors_mm"]),
        "max_target_slot_abs_error_mm": max(slot_eval["target_slot_abs_errors_mm"] or [math.inf]),
        "truth_free_selection_at_inference": True,
        "uses_branch_slots_for_selection": False,
    }


def summarize_variant(selected_rows: list[dict], variant: dict) -> dict:
    case_count = len(selected_rows)
    return {
        **variant,
        "case_count": case_count,
        "all_target_slot_case_count": sum(bool(row["all_target_slots_hit"]) for row in selected_rows),
        "failed_case_count": sum(not bool(row["all_target_slots_hit"]) for row in selected_rows),
        "mean_target_slot_hit_count": float(np.mean([safe_float(row["target_slot_hit_count"], 0.0) for row in selected_rows]))
        if selected_rows
        else 0.0,
        "mean_max_target_slot_abs_error_mm": float(
            np.mean([safe_float(row["max_target_slot_abs_error_mm"], 0.0) for row in selected_rows])
        )
        if selected_rows
        else 0.0,
        "close_pair_mode_case_count": sum(row.get("selection_mode") == "close_pair" for row in selected_rows),
        "regular_mode_case_count": sum(row.get("selection_mode") == "regular" for row in selected_rows),
        "min_component_candidate_count": min([safe_int(row["component_candidate_count"], 0) for row in selected_rows] or [0]),
        "truth_free_selection_at_inference": True,
        "uses_branch_slots_for_selection": False,
        "uses_truth_for_grid_scoring": True,
    }


def sort_variants(rows: list[dict]) -> list[dict]:
    return sorted(
        rows,
        key=lambda row: (
            -safe_int(row.get("all_target_slot_case_count"), 0),
            -safe_float(row.get("mean_target_slot_hit_count"), 0.0),
            safe_float(row.get("mean_max_target_slot_abs_error_mm"), math.inf),
            safe_float(row.get("failed_case_count"), math.inf),
            -safe_float(row.get("envelope_weight"), 0.0),
            -safe_float(row.get("support_weight"), 0.0),
            safe_float(row.get("structural_weight"), 0.0),
            safe_float(row.get("center_weight"), 0.0),
        ),
    )


def evaluate_envelope_assembly(rows: list[dict], variants: list[dict] | None = None) -> tuple[list[dict], list[dict], list[dict]]:
    grouped: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[case_key(row)].append(row)
    case_features = [precompute_case_features(key, case_rows) for key, case_rows in grouped.items()]
    variants = variants or variant_grid()

    selected_rows = []
    variant_rows = []
    for variant in variants:
        case_outputs = [selected_case_output(case_feature, variant) for case_feature in case_features]
        selected_rows.extend(case_outputs)
        variant_rows.append(summarize_variant(case_outputs, variant))
    return variant_rows, selected_rows, case_features


def leave_one_case_validation(selected_rows: list[dict]) -> tuple[list[dict], dict]:
    by_case: dict[str, list[dict]] = defaultdict(list)
    by_variant: dict[str, list[dict]] = defaultdict(list)
    variant_specs: dict[str, dict] = {}
    for row in selected_rows:
        by_case[str(row["case_label"])].append(row)
        by_variant[str(row["variant_label"])].append(row)
        variant_specs[str(row["variant_label"])] = {
            key: row[key]
            for key in ("variant_label", "envelope_weight", "structural_weight", "support_weight", "center_weight", "span_threshold_mm")
        }

    heldout_rows = []
    for heldout_case in sorted(by_case):
        train_summaries = []
        for variant_label_value, rows_for_variant in by_variant.items():
            training_rows = [row for row in rows_for_variant if row["case_label"] != heldout_case]
            train_summaries.append(summarize_variant(training_rows, variant_specs[variant_label_value]))
        selected_variant = sort_variants(train_summaries)[0]["variant_label"]
        selected_case_rows = [
            row
            for row in by_case[heldout_case]
            if row["variant_label"] == selected_variant
        ]
        if len(selected_case_rows) != 1:
            raise ValueError(f"expected one held-out row for {heldout_case} and {selected_variant}")
        heldout_rows.append(
            {
                **selected_case_rows[0],
                "heldout_case_label": heldout_case,
                "selected_by_training_variant_label": selected_variant,
            }
        )

    summary = {
        "leave_one_case_count": len(heldout_rows),
        "leave_one_case_all_target_slot_case_count": sum(bool(row["all_target_slots_hit"]) for row in heldout_rows),
        "leave_one_case_mean_target_slot_hit_count": float(
            np.mean([safe_float(row["target_slot_hit_count"], 0.0) for row in heldout_rows])
        )
        if heldout_rows
        else 0.0,
        "leave_one_case_failed_case_count": sum(not bool(row["all_target_slots_hit"]) for row in heldout_rows),
    }
    return heldout_rows, summary


def summarize_envelope_assembly(
    variant_rows: list[dict],
    selected_rows: list[dict],
    *,
    candidate_row_count: int,
    depth_slot_summary: dict,
    slot_component_summary: dict,
) -> dict:
    best = sort_variants(variant_rows)[0]
    leave_one_rows, leave_one_summary = leave_one_case_validation(selected_rows)
    ready_for_fwi = False
    return {
        "policy_label": "local_2d_detector_blind_component_envelope_assembly_cpu_no_fwi",
        "candidate_row_count": candidate_row_count,
        "variant_count": len(variant_rows),
        "case_count": safe_int(best.get("case_count"), 0),
        "current_triple_selector_all_truth_case_count": safe_int(depth_slot_summary.get("base_all_truth_case_count"), 0),
        "depth_slot_prior_best_all_truth_case_count": safe_int(depth_slot_summary.get("best_all_truth_case_count"), 0),
        "known_slot_component_upper_bound_case_count": safe_int(slot_component_summary.get("best_all_target_slot_case_count"), 0),
        "best_all_target_slot_case_count": safe_int(best.get("all_target_slot_case_count"), 0),
        "best_failed_case_count": safe_int(best.get("failed_case_count"), 0),
        "best_mean_target_slot_hit_count": safe_float(best.get("mean_target_slot_hit_count"), 0.0),
        "best_mean_max_target_slot_abs_error_mm": safe_float(best.get("mean_max_target_slot_abs_error_mm"), 0.0),
        "best_variant_label": best.get("variant_label", ""),
        "best_envelope_weight": safe_float(best.get("envelope_weight"), 0.0),
        "best_structural_weight": safe_float(best.get("structural_weight"), 0.0),
        "best_support_weight": safe_float(best.get("support_weight"), 0.0),
        "best_center_weight": safe_float(best.get("center_weight"), 0.0),
        "best_span_threshold_mm": safe_float(best.get("span_threshold_mm"), 0.0),
        "best_close_pair_mode_case_count": safe_int(best.get("close_pair_mode_case_count"), 0),
        "best_regular_mode_case_count": safe_int(best.get("regular_mode_case_count"), 0),
        "min_component_candidate_count": safe_int(best.get("min_component_candidate_count"), 0),
        **leave_one_summary,
        "truth_free_selection_at_inference": True,
        "uses_branch_slots_for_selection": False,
        "uses_truth_for_grid_scoring": True,
        "ready_for_detector_seeded_fwi": ready_for_fwi,
        "gpu_priority": "none",
        "decision": (
            "A blind envelope/support component assembly closes the saved-case target-slot assignment gap "
            "without using branch slot coordinates at inference. Because the grid is still selected on this "
            "small synthetic corpus and only validates component-slot coverage, keep this as CPU-side policy "
            "evidence rather than launching detector-seeded FWI."
        ),
        "_leave_one_case_rows": leave_one_rows,
    }


def plot_envelope_assembly(variant_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.8, 4.8), constrained_layout=True)

    labels = ["triple\nselector", "depth/slot\nprior", "known-slot\nupper bound", "blind\nenvelope", "leave-one\ncase"]
    values = [
        summary["current_triple_selector_all_truth_case_count"],
        summary["depth_slot_prior_best_all_truth_case_count"],
        summary["known_slot_component_upper_bound_case_count"],
        summary["best_all_target_slot_case_count"],
        summary["leave_one_case_all_target_slot_case_count"],
    ]
    colors = ["#e15759", "#f28e2b", "#76b7b2", "#59a14f", "#4e79a7"]
    axes[0].bar(np.arange(len(labels)), values, color=colors)
    axes[0].set_xticks(np.arange(len(labels)), labels)
    axes[0].set_ylim(0, max(summary["case_count"], 1))
    axes[0].set_ylabel("cases")
    axes[0].set_title("Target-slot recovery ladder")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    x = [safe_float(row["envelope_weight"], 0.0) for row in variant_rows]
    y = [safe_float(row["support_weight"], 0.0) for row in variant_rows]
    c = [safe_float(row["all_target_slot_case_count"], 0.0) for row in variant_rows]
    scatter = axes[1].scatter(x, y, c=c, cmap="viridis", vmin=0, vmax=max(summary["case_count"], 1), s=70, edgecolor="#333333", linewidth=0.3)
    axes[1].set_xlabel("envelope weight")
    axes[1].set_ylabel("support weight")
    axes[1].set_title("Blind policy grid")
    axes[1].grid(color="#dddddd", linewidth=0.6)
    fig.colorbar(scatter, ax=axes[1], fraction=0.046, pad=0.04, label="all-slot cases")
    axes[1].text(
        0.04,
        0.96,
        f"best: {summary['best_variant_label']}\n"
        f"truth-free inference: {summary['truth_free_selection_at_inference']}\n"
        f"FWI-ready: {summary['ready_for_detector_seeded_fwi']}",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector blind component-envelope assembly", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, variant_csv: Path, selected_csv: Path, loo_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_blind_component_envelope_assembly.png`",
                "",
                "This CPU-only figure evaluates a blind component-envelope assembly",
                "policy over saved local 2D detector component rows.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Best all-target-slot cases: `{summary['best_all_target_slot_case_count']}`.",
                f"Leave-one-case all-target-slot cases: `{summary['leave_one_case_all_target_slot_case_count']}`.",
                f"Known-slot upper bound cases: `{summary['known_slot_component_upper_bound_case_count']}`.",
                f"Uses branch slots for selection: `{summary['uses_branch_slots_for_selection']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Variant grid: `{variant_csv.name}`.",
                f"- Selected case rows: `{selected_csv.name}`.",
                f"- Leave-one-case rows: `{loo_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "The selector uses candidate component support envelopes and spacing",
                "structure, not the known branch slot coordinates. Truth is used only",
                "to score the policy grid and report target-slot recovery. This does",
                "not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC jobs, or",
                "neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--component-gate-run", default=DEFAULT_COMPONENT_GATE_RUN)
    parser.add_argument("--depth-slot-prior-run", default=DEFAULT_DEPTH_SLOT_PRIOR_RUN)
    parser.add_argument("--slot-component-run", default=DEFAULT_SLOT_COMPONENT_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_blind_component_envelope_assembly")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    component_dir = summary_root / args.component_gate_run
    depth_slot_dir = summary_root / args.depth_slot_prior_run
    slot_component_dir = summary_root / args.slot_component_run

    rows = read_csv_rows(component_dir / "data/local_2d_detector_component_waveform_gate_rows.csv")
    depth_slot_summary = read_json(depth_slot_dir / "data/local_2d_detector_depth_slot_prior_probe_summary.json")
    slot_component_summary = read_json(slot_component_dir / "data/local_2d_detector_slot_component_assembly_summary.json")

    variant_rows, selected_rows, _case_features = evaluate_envelope_assembly(rows)
    summary = summarize_envelope_assembly(
        variant_rows,
        selected_rows,
        candidate_row_count=len(rows),
        depth_slot_summary=depth_slot_summary,
        slot_component_summary=slot_component_summary,
    )
    leave_one_rows = summary.pop("_leave_one_case_rows")

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    variant_csv = data_dir / "local_2d_detector_blind_component_envelope_assembly_variants.csv"
    selected_csv = data_dir / "local_2d_detector_blind_component_envelope_assembly_selected_cases.csv"
    loo_csv = data_dir / "local_2d_detector_blind_component_envelope_assembly_leave_one_case.csv"
    summary_json = data_dir / "local_2d_detector_blind_component_envelope_assembly_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_blind_component_envelope_assembly.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(variant_csv, [json_safe(row) for row in sort_variants(variant_rows)])
    write_csv(selected_csv, [json_safe(row) for row in selected_rows])
    write_csv(loo_csv, [json_safe(row) for row in leave_one_rows])
    plot_envelope_assembly(variant_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, variant_csv, selected_csv, loo_csv)
    summary["paths"] = {
        "variant_grid_csv": str(variant_csv),
        "selected_cases_csv": str(selected_csv),
        "leave_one_case_csv": str(loo_csv),
        "summary_json": str(summary_json),
        "source_component_rows_csv": str(component_dir / "data/local_2d_detector_component_waveform_gate_rows.csv"),
        "comparison_depth_slot_prior_summary_json": str(
            depth_slot_dir / "data/local_2d_detector_depth_slot_prior_probe_summary.json"
        ),
        "comparison_slot_component_upper_bound_summary_json": str(
            slot_component_dir / "data/local_2d_detector_slot_component_assembly_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_blind_component_envelope_assembly",
        {
            "component_gate_run": args.component_gate_run,
            "depth_slot_prior_run": args.depth_slot_prior_run,
            "slot_component_run": args.slot_component_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

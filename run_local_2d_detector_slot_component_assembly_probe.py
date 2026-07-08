#!/usr/bin/env python3
"""Probe branch-slot assembly of saved local 2D detector components."""

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
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_COMPONENT_GATE_RUN = "035_local_2d_detector_component_waveform_gate_post_rank_budget"
DEFAULT_DEPTH_SLOT_PRIOR_RUN = "055_local_2d_detector_depth_slot_prior_probe"
EXPECTED_X_SLOTS = {
    "target2_close14": (190.0, 250.0, 264.0),
    "target2_close50_linear29p5": (190.0, 250.0, 300.0),
}
SLOT_WEIGHTS = (1.0, 2.0, 4.0, 8.0, 12.0)
DEPTH_WEIGHTS = (0.0, 1.0, 4.0, 8.0)
SCORE_WEIGHTS = (0.5, 1.0)
RANK_WEIGHTS = (0.0, 0.02, 0.05)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def numeric_list(value: str) -> list[float]:
    out = []
    for part in str(value or "").split(","):
        part = part.strip()
        if part:
            out.append(float(part))
    return out


def case_key(row: dict) -> tuple[str, str, str, str]:
    return (
        str(row.get("branch_key", "")),
        str(row.get("seed", "")),
        str(row.get("case_variant", "")),
        str(row.get("run_name", "")),
    )


def depth_prior_score(z_mm: float, *, center_mm: float = 90.0, deadband_mm: float = 10.0, scale_mm: float = 30.0) -> float:
    return -max(0.0, abs(float(z_mm) - center_mm) - deadband_mm) / scale_mm


def component_rows_for_case(case_rows: list[dict]) -> list[dict]:
    components: dict[tuple[float, float, float], dict] = {}
    for row in case_rows:
        xs = numeric_list(row.get("candidate_x_values_mm", ""))
        zs = numeric_list(row.get("candidate_z_values_mm", ""))
        ranks = numeric_list(row.get("candidate_ranks", ""))
        scores = numeric_list(row.get("component_score_values", ""))
        for index, x_mm in enumerate(xs):
            z_mm = zs[index] if index < len(zs) else math.nan
            rank = ranks[index] if index < len(ranks) else 999.0
            score = scores[index] if index < len(scores) else safe_float(row.get("score_component_min"), 0.0)
            key = (round(x_mm, 3), round(z_mm, 3), round(rank, 3))
            current = {
                "component_key": f"x{x_mm:g}_z{z_mm:g}_r{rank:g}",
                "x_mm": float(x_mm),
                "z_mm": float(z_mm),
                "rank": float(rank),
                "component_score": float(score),
                "source_combo_index": row.get("combo_index", ""),
            }
            existing = components.get(key)
            if existing is None or current["component_score"] > existing["component_score"]:
                components[key] = current
    return list(components.values())


def component_base_score(component: dict, *, score_weight: float, depth_weight: float, rank_weight: float) -> float:
    return (
        float(score_weight) * safe_float(component.get("component_score"), 0.0)
        + float(depth_weight) * depth_prior_score(safe_float(component.get("z_mm"), 0.0))
        - float(rank_weight) * safe_float(component.get("rank"), 999.0)
    )


def assemble_slot_components(
    components: list[dict],
    expected_slots: tuple[float, ...],
    *,
    slot_weight: float,
    depth_weight: float,
    score_weight: float,
    rank_weight: float,
) -> list[dict]:
    selected = []
    used: set[str] = set()
    for target_index, target_x in enumerate(expected_slots):
        best_component = None
        best_score = -math.inf
        for component in components:
            key = str(component["component_key"])
            if key in used:
                continue
            slot_penalty = float(slot_weight) * abs(safe_float(component["x_mm"]) - float(target_x)) / 30.0
            score = component_base_score(
                component,
                score_weight=score_weight,
                depth_weight=depth_weight,
                rank_weight=rank_weight,
            ) - slot_penalty
            if score > best_score:
                best_score = score
                best_component = component
        if best_component is None:
            continue
        used.add(str(best_component["component_key"]))
        selected.append(
            {
                **best_component,
                "target_slot_index": target_index,
                "target_x_mm": float(target_x),
                "slot_abs_error_mm": abs(safe_float(best_component["x_mm"]) - float(target_x)),
                "slot_assembly_score": best_score,
            }
        )
    return selected


def slot_hit_flags(selected: list[dict], *, tolerance_mm: float = 10.0) -> list[bool]:
    return [safe_float(component.get("slot_abs_error_mm"), math.inf) <= tolerance_mm for component in selected]


def variant_label(slot_weight: float, depth_weight: float, score_weight: float, rank_weight: float) -> str:
    return f"slot{slot_weight:g}_depth{depth_weight:g}_score{score_weight:g}_rank{rank_weight:g}"


def evaluate_slot_assembly(
    rows: list[dict],
    *,
    slot_weights: tuple[float, ...] = SLOT_WEIGHTS,
    depth_weights: tuple[float, ...] = DEPTH_WEIGHTS,
    score_weights: tuple[float, ...] = SCORE_WEIGHTS,
    rank_weights: tuple[float, ...] = RANK_WEIGHTS,
) -> tuple[list[dict], list[dict]]:
    grouped: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[case_key(row)].append(row)

    components_by_case = {key: component_rows_for_case(case_rows) for key, case_rows in grouped.items()}
    variant_rows = []
    selected_rows = []
    for slot_weight in slot_weights:
        for depth_weight in depth_weights:
            for score_weight in score_weights:
                for rank_weight in rank_weights:
                    label = variant_label(slot_weight, depth_weight, score_weight, rank_weight)
                    case_outputs = []
                    for key, components in components_by_case.items():
                        branch_key, seed, case_variant, run_name = key
                        expected_slots = EXPECTED_X_SLOTS.get(branch_key)
                        if expected_slots is None:
                            continue
                        selected = assemble_slot_components(
                            components,
                            expected_slots,
                            slot_weight=slot_weight,
                            depth_weight=depth_weight,
                            score_weight=score_weight,
                            rank_weight=rank_weight,
                        )
                        hits = slot_hit_flags(selected)
                        row = {
                            "variant_label": label,
                            "slot_weight": float(slot_weight),
                            "depth_weight": float(depth_weight),
                            "score_weight": float(score_weight),
                            "rank_weight": float(rank_weight),
                            "case_label": f"{branch_key}|seed{seed}|{case_variant}",
                            "branch_key": branch_key,
                            "seed": safe_int(seed),
                            "case_variant": case_variant,
                            "run_name": run_name,
                            "component_candidate_count": len(components),
                            "selected_component_count": len(selected),
                            "all_target_slots_hit": len(hits) == len(expected_slots) and all(hits),
                            "target_slot_hit_count": sum(hits),
                            "selected_x_values_mm": ",".join(f"{component['x_mm']:g}" for component in selected),
                            "selected_z_values_mm": ",".join(f"{component['z_mm']:g}" for component in selected),
                            "selected_ranks": ",".join(f"{component['rank']:g}" for component in selected),
                            "slot_abs_errors_mm": ",".join(f"{component['slot_abs_error_mm']:g}" for component in selected),
                        }
                        case_outputs.append(row)
                        selected_rows.append(row)
                    variant_rows.append(
                        {
                            "variant_label": label,
                            "slot_weight": float(slot_weight),
                            "depth_weight": float(depth_weight),
                            "score_weight": float(score_weight),
                            "rank_weight": float(rank_weight),
                            "case_count": len(case_outputs),
                            "all_target_slot_case_count": sum(bool(row["all_target_slots_hit"]) for row in case_outputs),
                            "failed_case_count": sum(not bool(row["all_target_slots_hit"]) for row in case_outputs),
                            "mean_target_slot_hit_count": float(
                                np.mean([safe_float(row["target_slot_hit_count"], 0.0) for row in case_outputs])
                            )
                            if case_outputs
                            else 0.0,
                            "min_component_candidate_count": min(
                                [safe_int(row["component_candidate_count"], 0) for row in case_outputs] or [0]
                            ),
                            "median_component_candidate_count": float(
                                np.median([safe_int(row["component_candidate_count"], 0) for row in case_outputs])
                            )
                            if case_outputs
                            else 0.0,
                        }
                    )
    return variant_rows, selected_rows


def sort_variants(rows: list[dict]) -> list[dict]:
    return sorted(
        rows,
        key=lambda row: (
            -safe_int(row["all_target_slot_case_count"]),
            -safe_float(row["mean_target_slot_hit_count"], 0.0),
            safe_float(row["slot_weight"], 0.0),
            safe_float(row["depth_weight"], 0.0),
            safe_float(row["rank_weight"], 0.0),
            safe_float(row["score_weight"], 0.0),
        ),
    )


def summarize_slot_assembly(
    variant_rows: list[dict],
    *,
    candidate_row_count: int,
    comparison_summary: dict | None = None,
) -> dict:
    comparison_summary = comparison_summary or {}
    best = sort_variants(variant_rows)[0]
    return {
        "policy_label": "local_2d_detector_slot_component_assembly_probe_cpu_no_fwi",
        "candidate_row_count": candidate_row_count,
        "variant_count": len(variant_rows),
        "case_count": safe_int(best.get("case_count"), 0),
        "current_triple_selector_all_truth_case_count": safe_int(
            comparison_summary.get("base_all_truth_case_count"), 0
        ),
        "depth_slot_prior_best_all_truth_case_count": safe_int(
            comparison_summary.get("best_all_truth_case_count"), 0
        ),
        "best_all_target_slot_case_count": safe_int(best.get("all_target_slot_case_count"), 0),
        "best_mean_target_slot_hit_count": safe_float(best.get("mean_target_slot_hit_count"), 0.0),
        "best_failed_case_count": safe_int(best.get("failed_case_count"), 0),
        "best_slot_weight": safe_float(best.get("slot_weight"), 0.0),
        "best_depth_weight": safe_float(best.get("depth_weight"), 0.0),
        "best_score_weight": safe_float(best.get("score_weight"), 0.0),
        "best_rank_weight": safe_float(best.get("rank_weight"), 0.0),
        "min_component_candidate_count": safe_int(best.get("min_component_candidate_count"), 0),
        "median_component_candidate_count": safe_float(best.get("median_component_candidate_count"), 0.0),
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "Branch-slot component assembly recovers every target slot in the saved cases, but it is an "
            "upper-bound/contract result because it uses known branch slot locations. Use it to show that "
            "component evidence is present and the remaining problem is deployable target assignment."
        ),
    }


def plot_slot_assembly(variant_rows: list[dict], summary: dict, save_path: Path) -> str:
    slot_values = sorted({safe_float(row["slot_weight"]) for row in variant_rows})
    depth_values = sorted({safe_float(row["depth_weight"]) for row in variant_rows})
    grid = np.full((len(depth_values), len(slot_values)), np.nan)
    filtered = [
        row
        for row in variant_rows
        if safe_float(row["score_weight"]) == summary["best_score_weight"]
        and safe_float(row["rank_weight"]) == summary["best_rank_weight"]
    ]
    for row in filtered:
        i = depth_values.index(safe_float(row["depth_weight"]))
        j = slot_values.index(safe_float(row["slot_weight"]))
        grid[i, j] = safe_float(row["all_target_slot_case_count"], 0.0)

    fig, axes = plt.subplots(1, 2, figsize=(13.8, 4.8), constrained_layout=True)
    image = axes[0].imshow(grid, origin="lower", cmap="viridis", vmin=0, vmax=max(summary["case_count"], 1))
    axes[0].set_xticks(np.arange(len(slot_values)), [f"{value:g}" for value in slot_values])
    axes[0].set_yticks(np.arange(len(depth_values)), [f"{value:g}" for value in depth_values])
    axes[0].set_xlabel("slot weight")
    axes[0].set_ylabel("depth weight")
    axes[0].set_title("Slot-assembly all-target cases")
    fig.colorbar(image, ax=axes[0], fraction=0.046, pad=0.04)

    labels = ["triple\nselector", "depth/slot\nprior", "slot\nassembly"]
    values = [
        summary["current_triple_selector_all_truth_case_count"],
        summary["depth_slot_prior_best_all_truth_case_count"],
        summary["best_all_target_slot_case_count"],
    ]
    axes[1].bar(np.arange(len(labels)), values, color=["#e15759", "#f28e2b", "#59a14f"])
    axes[1].set_xticks(np.arange(len(labels)), labels)
    axes[1].set_ylim(0, max(summary["case_count"], 1))
    axes[1].set_ylabel("cases")
    axes[1].set_title("Target-slot coverage ladder")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.04,
        0.95,
        f"best slot={summary['best_slot_weight']:.1f}\n"
        f"best depth={summary['best_depth_weight']:.1f}\n"
        f"upper-bound only",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector branch-slot component assembly probe", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, variant_csv: Path, selected_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_slot_component_assembly_probe.png`",
                "",
                "This CPU-only figure tests whether saved detector components can recover",
                "the known branch target slots when assembled slot-by-slot.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Current triple selector all-truth cases: `{summary['current_triple_selector_all_truth_case_count']}`.",
                f"Depth/slot prior best all-truth cases: `{summary['depth_slot_prior_best_all_truth_case_count']}`.",
                f"Slot assembly all-target cases: `{summary['best_all_target_slot_case_count']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Variant grid: `{variant_csv.name}`.",
                f"- Selected case rows: `{selected_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This is a branch-slot upper-bound/contract probe. It uses the known",
                "synthetic branch slot locations and is not a deployable detector selector.",
                "It does not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC jobs, or",
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
    parser.add_argument("--run-name", default="local_2d_detector_slot_component_assembly_probe")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dir = Path(args.summary_root) / args.component_gate_run
    comparison_dir = Path(args.summary_root) / args.depth_slot_prior_run
    rows = read_csv_rows(source_dir / "data/local_2d_detector_component_waveform_gate_rows.csv")
    comparison_summary = read_json(
        comparison_dir / "data/local_2d_detector_depth_slot_prior_probe_summary.json"
    )

    variant_rows, selected_rows = evaluate_slot_assembly(rows)
    summary = summarize_slot_assembly(
        variant_rows,
        candidate_row_count=len(rows),
        comparison_summary=comparison_summary,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    variant_csv = data_dir / "local_2d_detector_slot_component_assembly_variants.csv"
    selected_csv = data_dir / "local_2d_detector_slot_component_assembly_selected_cases.csv"
    summary_json = data_dir / "local_2d_detector_slot_component_assembly_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_slot_component_assembly_probe.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(variant_csv, [json_safe(row) for row in sort_variants(variant_rows)])
    write_csv(selected_csv, [json_safe(row) for row in selected_rows])
    plot_slot_assembly(variant_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, variant_csv, selected_csv)
    summary["paths"] = {
        "variant_grid_csv": str(variant_csv),
        "selected_cases_csv": str(selected_csv),
        "summary_json": str(summary_json),
        "source_component_rows_csv": str(source_dir / "data/local_2d_detector_component_waveform_gate_rows.csv"),
        "comparison_depth_slot_prior_summary_json": str(
            comparison_dir / "data/local_2d_detector_depth_slot_prior_probe_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_slot_component_assembly_probe",
        {
            "component_gate_run": args.component_gate_run,
            "depth_slot_prior_run": args.depth_slot_prior_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

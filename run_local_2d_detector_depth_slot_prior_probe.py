#!/usr/bin/env python3
"""Probe broad depth and slot priors for the local 2D detector selector."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter, defaultdict
from itertools import permutations
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
from run_local_2d_detector_geometry_family_selector import (  # noqa: E402
    enrich_row,
    failure_label,
    selector_grid,
    selector_score,
)
from run_local_2d_detector_rank_budget_diagnostic import safe_float, safe_int  # noqa: E402
from run_local_2d_detector_target_failure_taxonomy import missing_targets  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_COMPONENT_GATE_RUN = "035_local_2d_detector_component_waveform_gate_post_rank_budget"
DEFAULT_SELECTOR_LABEL = "cb0.5_hy0.2_min0_span0.5_sgap4_center0.2_rank0.1"
DEPTH_WEIGHTS = (0.0, 0.1, 0.2, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0)
SLOT_WEIGHTS = (0.0, 0.1, 0.2, 0.5, 1.0, 2.0, 4.0, 8.0)
EXPECTED_X_SLOTS = {
    "target2_close14": (190.0, 250.0, 264.0),
    "target2_close50_linear29p5": (190.0, 250.0, 300.0),
}


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def selector_from_label(selector_label: str) -> dict:
    matches = [selector for selector in selector_grid() if selector["selector_label"] == selector_label]
    if not matches:
        raise ValueError(f"unknown selector label: {selector_label}")
    return matches[0]


def numeric_list(value: str) -> list[float]:
    out = []
    for part in str(value or "").split(","):
        part = part.strip()
        if part:
            out.append(float(part))
    return out


def depth_prior_score(row: dict, *, center_mm: float = 90.0, deadband_mm: float = 10.0, scale_mm: float = 30.0) -> float:
    depths = numeric_list(row.get("candidate_z_values_mm", ""))
    if not depths:
        return -1.0
    penalties = [max(0.0, abs(depth - center_mm) - deadband_mm) / scale_mm for depth in depths]
    return -float(sum(penalties) / len(penalties))


def slot_prior_score(row: dict, *, scale_mm: float = 30.0) -> float:
    xs = numeric_list(row.get("candidate_x_values_mm", ""))
    expected = EXPECTED_X_SLOTS.get(str(row.get("branch_key", "")))
    if len(xs) != 3 or expected is None:
        return -1.0
    best_cost = min(sum(abs(candidate - target) for candidate, target in zip(ordering, expected)) for ordering in permutations(xs))
    return -float(best_cost / (len(expected) * scale_mm))


def combined_score(row: dict, selector: dict, *, depth_weight: float, slot_weight: float) -> float:
    return (
        selector_score(row, selector)
        + float(depth_weight) * depth_prior_score(row)
        + float(slot_weight) * slot_prior_score(row)
    )


def case_key(row: dict) -> tuple[str, str, str, str]:
    return (
        str(row.get("branch_key", "")),
        str(row.get("seed", "")),
        str(row.get("case_variant", "")),
        str(row.get("run_name", "")),
    )


def selected_row_for_case(rows: list[dict], selector: dict, *, depth_weight: float, slot_weight: float) -> dict:
    return max(
        rows,
        key=lambda row: (
            combined_score(row, selector, depth_weight=depth_weight, slot_weight=slot_weight),
            -safe_float(row.get("rank_sum_numeric"), 10_000.0),
            -safe_float(row.get("max_rank_numeric"), 10_000.0),
            str(row.get("candidate_x_values_mm", "")),
        ),
    )


def variant_label(depth_weight: float, slot_weight: float) -> str:
    return f"depth{depth_weight:g}_slot{slot_weight:g}"


def selected_case_output(row: dict, selector: dict, *, depth_weight: float, slot_weight: float) -> dict:
    label = failure_label(row)
    missing = missing_targets(label)
    return {
        "variant_label": variant_label(depth_weight, slot_weight),
        "depth_weight": float(depth_weight),
        "slot_weight": float(slot_weight),
        "case_label": row.get("case_label", ""),
        "branch_key": row.get("branch_key", ""),
        "seed": safe_int(row.get("seed")),
        "case_variant": row.get("case_variant", ""),
        "combo_index": row.get("combo_index", ""),
        "candidate_ranks": row.get("candidate_ranks", ""),
        "candidate_x_values_mm": row.get("candidate_x_values_mm", ""),
        "candidate_z_values_mm": row.get("candidate_z_values_mm", ""),
        "unique_all_truths": bool(row.get("unique_all_truths_bool")),
        "unique_truth_hit_count": safe_int(row.get("unique_truth_hit_count_numeric")),
        "failure_label": label,
        "missing_target0": "target0" in missing,
        "missing_target1": "target1" in missing,
        "missing_target2": "target2" in missing,
        "selector_score": selector_score(row, selector),
        "depth_prior_score": depth_prior_score(row),
        "slot_prior_score": slot_prior_score(row),
        "combined_score": combined_score(row, selector, depth_weight=depth_weight, slot_weight=slot_weight),
    }


def evaluate_prior_grid(
    rows: list[dict],
    selector: dict,
    *,
    depth_weights: tuple[float, ...] = DEPTH_WEIGHTS,
    slot_weights: tuple[float, ...] = SLOT_WEIGHTS,
) -> tuple[list[dict], list[dict]]:
    grouped: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[case_key(row)].append(row)

    variant_rows = []
    selected_rows = []
    for depth_weight in depth_weights:
        for slot_weight in slot_weights:
            selected = [
                selected_row_for_case(case_rows, selector, depth_weight=depth_weight, slot_weight=slot_weight)
                for case_rows in grouped.values()
            ]
            case_outputs = [
                selected_case_output(row, selector, depth_weight=depth_weight, slot_weight=slot_weight)
                for row in selected
            ]
            selected_rows.extend(case_outputs)
            failure_counts = Counter(row["failure_label"] for row in case_outputs if not row["unique_all_truths"])
            missing_counts = {
                target: sum(bool(row[f"missing_{target}"]) for row in case_outputs if not row["unique_all_truths"])
                for target in ("target0", "target1", "target2")
            }
            variant_rows.append(
                {
                    "variant_label": variant_label(depth_weight, slot_weight),
                    "depth_weight": float(depth_weight),
                    "slot_weight": float(slot_weight),
                    "case_count": len(case_outputs),
                    "all_truth_case_count": sum(bool(row["unique_all_truths"]) for row in case_outputs),
                    "failed_selector_case_count": sum(not bool(row["unique_all_truths"]) for row in case_outputs),
                    "mean_unique_truth_hit_count": float(
                        np.mean([safe_float(row["unique_truth_hit_count"], 0.0) for row in case_outputs])
                    ),
                    "missing_target0_case_count": missing_counts["target0"],
                    "missing_target1_case_count": missing_counts["target1"],
                    "missing_target2_case_count": missing_counts["target2"],
                    "multi_target_failure_case_count": sum(
                        sum(bool(row[f"missing_{target}"]) for target in ("target0", "target1", "target2")) > 1
                        for row in case_outputs
                        if not row["unique_all_truths"]
                    ),
                    "dominant_failure_label": failure_counts.most_common(1)[0][0] if failure_counts else "all_truth",
                }
            )
    return variant_rows, selected_rows


def sort_variants(rows: list[dict]) -> list[dict]:
    return sorted(
        rows,
        key=lambda row: (
            -safe_int(row["all_truth_case_count"]),
            -safe_float(row["mean_unique_truth_hit_count"], 0.0),
            safe_float(row["missing_target1_case_count"], 0.0),
            safe_float(row["depth_weight"], 0.0),
            safe_float(row["slot_weight"], 0.0),
        ),
    )


def summarize_prior_probe(variant_rows: list[dict], *, selector_label: str, candidate_row_count: int) -> dict:
    sorted_rows = sort_variants(variant_rows)
    best = sorted_rows[0]
    base_matches = [
        row for row in variant_rows if safe_float(row["depth_weight"], -1.0) == 0.0 and safe_float(row["slot_weight"], -1.0) == 0.0
    ]
    base = base_matches[0] if base_matches else {}
    case_count = safe_int(best.get("case_count"), 0)
    ready = safe_int(best.get("all_truth_case_count"), 0) == case_count
    return {
        "policy_label": "local_2d_detector_depth_slot_prior_probe_cpu_no_fwi",
        "selector_label": selector_label,
        "candidate_row_count": candidate_row_count,
        "variant_count": len(variant_rows),
        "case_count": case_count,
        "base_all_truth_case_count": safe_int(base.get("all_truth_case_count"), 0),
        "best_all_truth_case_count": safe_int(best.get("all_truth_case_count"), 0),
        "best_improvement_over_base_all_truth_cases": safe_int(best.get("all_truth_case_count"), 0)
        - safe_int(base.get("all_truth_case_count"), 0),
        "best_mean_unique_truth_hit_count": safe_float(best.get("mean_unique_truth_hit_count"), 0.0),
        "best_depth_weight": safe_float(best.get("depth_weight"), 0.0),
        "best_slot_weight": safe_float(best.get("slot_weight"), 0.0),
        "best_failed_selector_case_count": safe_int(best.get("failed_selector_case_count"), 0),
        "best_missing_target1_case_count": safe_int(best.get("missing_target1_case_count"), 0),
        "best_missing_target2_case_count": safe_int(best.get("missing_target2_case_count"), 0),
        "best_multi_target_failure_case_count": safe_int(best.get("multi_target_failure_case_count"), 0),
        "ready_for_detector_seeded_fwi": bool(ready),
        "gpu_priority": "none",
        "decision": (
            "A broad depth prior improves the saved selector modestly, but the best CPU-only variant still "
            "recovers all truth in fewer than half of cases. This is a feature-design clue, not a detector-seeded "
            "FWI trigger."
        ),
    }


def plot_prior_probe(variant_rows: list[dict], summary: dict, save_path: Path) -> str:
    depth_values = sorted({safe_float(row["depth_weight"]) for row in variant_rows})
    slot_values = sorted({safe_float(row["slot_weight"]) for row in variant_rows})
    grid = np.full((len(depth_values), len(slot_values)), np.nan)
    for row in variant_rows:
        i = depth_values.index(safe_float(row["depth_weight"]))
        j = slot_values.index(safe_float(row["slot_weight"]))
        grid[i, j] = safe_float(row["all_truth_case_count"], 0.0)

    fig, axes = plt.subplots(1, 2, figsize=(13.8, 4.8), constrained_layout=True)
    image = axes[0].imshow(grid, origin="lower", cmap="viridis", vmin=0, vmax=max(summary["case_count"], 1))
    axes[0].set_xticks(np.arange(len(slot_values)), [f"{value:g}" for value in slot_values])
    axes[0].set_yticks(np.arange(len(depth_values)), [f"{value:g}" for value in depth_values])
    axes[0].set_xlabel("slot prior weight")
    axes[0].set_ylabel("depth prior weight")
    axes[0].set_title("All-truth cases across prior grid")
    fig.colorbar(image, ax=axes[0], fraction=0.046, pad=0.04)

    labels = ["base", "best"]
    all_truth = [summary["base_all_truth_case_count"], summary["best_all_truth_case_count"]]
    failed = [
        summary["case_count"] - summary["base_all_truth_case_count"],
        summary["best_failed_selector_case_count"],
    ]
    x = np.arange(len(labels))
    axes[1].bar(x, all_truth, color="#59a14f", label="all-truth")
    axes[1].bar(x, failed, bottom=all_truth, color="#e15759", label="failed")
    axes[1].set_xticks(x, labels)
    axes[1].set_ylim(0, max(summary["case_count"], 1))
    axes[1].set_ylabel("cases")
    axes[1].set_title("Base selector vs best prior variant")
    axes[1].legend(loc="upper right", fontsize=8)
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.04,
        0.95,
        f"best depth={summary['best_depth_weight']:.1f}\n"
        f"best slot={summary['best_slot_weight']:.1f}\n"
        f"target1 misses={summary['best_missing_target1_case_count']}",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector depth/slot prior probe", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, variant_csv: Path, selected_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_depth_slot_prior_probe.png`",
                "",
                "This CPU-only figure probes broad depth and expected-x-slot priors on the",
                "saved detector component-gate rows.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Base all-truth cases: `{summary['base_all_truth_case_count']}`.",
                f"Best all-truth cases: `{summary['best_all_truth_case_count']}`.",
                f"Best depth weight: `{summary['best_depth_weight']}`.",
                f"Best slot weight: `{summary['best_slot_weight']}`.",
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
                "This probe reads existing saved detector rows only. It does not run FDTD, FWI,",
                "GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.",
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
    parser.add_argument("--selector-label", default=DEFAULT_SELECTOR_LABEL)
    parser.add_argument("--run-name", default="local_2d_detector_depth_slot_prior_probe")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dir = Path(args.summary_root) / args.component_gate_run
    raw_rows = read_csv_rows(source_dir / "data/local_2d_detector_component_waveform_gate_rows.csv")
    rows = [enrich_row(row) for row in raw_rows]
    selector = selector_from_label(args.selector_label)

    variant_rows, selected_rows = evaluate_prior_grid(rows, selector)
    summary = summarize_prior_probe(variant_rows, selector_label=args.selector_label, candidate_row_count=len(rows))

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    variant_csv = data_dir / "local_2d_detector_depth_slot_prior_probe_variants.csv"
    selected_csv = data_dir / "local_2d_detector_depth_slot_prior_probe_selected_cases.csv"
    summary_json = data_dir / "local_2d_detector_depth_slot_prior_probe_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_depth_slot_prior_probe.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(variant_csv, [json_safe(row) for row in sort_variants(variant_rows)])
    write_csv(selected_csv, [json_safe(row) for row in selected_rows])
    plot_prior_probe(variant_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, variant_csv, selected_csv)
    summary["paths"] = {
        "variant_grid_csv": str(variant_csv),
        "selected_cases_csv": str(selected_csv),
        "summary_json": str(summary_json),
        "source_component_rows_csv": str(source_dir / "data/local_2d_detector_component_waveform_gate_rows.csv"),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_depth_slot_prior_probe",
        {
            "component_gate_run": args.component_gate_run,
            "selector_label": args.selector_label,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

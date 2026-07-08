#!/usr/bin/env python3
"""Test simple counterfactual reweighting around the local 2D detector selector."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import Counter
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
    DEFAULT_COMPONENT_GATE_RUN,
    FEATURE_FIELDS,
    enrich_row,
    precompute_selected_indices,
    selected_rows_for_selector_index,
    selector_grid,
    summarize_selected,
)
from run_local_2d_detector_rank_budget_diagnostic import read_csv_rows, read_json, safe_float, safe_int  # noqa: E402
from run_local_2d_detector_selector_gap_decomposition import (  # noqa: E402
    build_gap_rows,
    summarize_features,
    summarize_gap_decomposition,
)
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_GEOMETRY_SELECTOR_RUN = "041_local_2d_detector_geometry_family_selector_post_upper_bound_policy"


def selector_from_label(selector_label: str) -> dict:
    matches = [selector for selector in selector_grid() if selector["selector_label"] == selector_label]
    if not matches:
        raise ValueError(f"unknown selector label: {selector_label}")
    return matches[0]


def _with_label(base: dict, *, family: str, label_suffix: str, updates: dict) -> dict:
    out = dict(base)
    out.update(updates)
    if "rank_sum_weight" in updates and "max_rank_weight" not in updates:
        out["max_rank_weight"] = 0.5 * safe_float(updates["rank_sum_weight"], 0.0)
    out["counterfactual_family"] = family
    out["counterfactual_label"] = f"{family}_{label_suffix}"
    out["selector_label"] = out["counterfactual_label"]
    return out


def counterfactual_selector_grid(base: dict) -> list[dict]:
    selectors = []
    selectors.append(_with_label(base, family="base", label_suffix="current", updates={}))
    ablations = {
        "drop_component_balanced": {"component_balanced_weight": 0.0},
        "drop_hybrid_component": {"hybrid_span_component_weight": 0.0},
        "drop_span_prior": {"span_prior_weight": 0.0},
        "drop_signed_gap_prior": {"signed_gap_prior_weight": 0.0},
        "drop_center_prior": {"center_prior_weight": 0.0},
        "drop_rank_penalty": {"rank_sum_weight": 0.0, "max_rank_weight": 0.0},
    }
    for label, updates in ablations.items():
        selectors.append(_with_label(base, family="ablation", label_suffix=label, updates=updates))
    for value in (0.0, 0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0):
        selectors.append(
            _with_label(
                base,
                family="signed_gap_sweep",
                label_suffix=f"w{value:g}",
                updates={"signed_gap_prior_weight": value},
            )
        )
    for value in (0.0, 0.025, 0.05, 0.1, 0.2, 0.4):
        selectors.append(
            _with_label(
                base,
                family="rank_sweep",
                label_suffix=f"w{value:g}",
                updates={"rank_sum_weight": value, "max_rank_weight": 0.5 * value},
            )
        )
    for value in (0.0, 0.25, 0.5, 0.75, 1.0, 2.0):
        selectors.append(
            _with_label(
                base,
                family="span_sweep",
                label_suffix=f"w{value:g}",
                updates={"span_prior_weight": value},
            )
        )
    for value in (0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0):
        selectors.append(
            _with_label(
                base,
                family="component_sweep",
                label_suffix=f"w{value:g}",
                updates={"component_balanced_weight": value},
            )
        )
    for value in (0.0, 0.1, 0.2, 0.4, 0.8):
        selectors.append(
            _with_label(
                base,
                family="hybrid_sweep",
                label_suffix=f"w{value:g}",
                updates={"hybrid_span_component_weight": value},
            )
        )
    for value in (0.0, 0.1, 0.2, 0.4):
        selectors.append(
            _with_label(
                base,
                family="center_sweep",
                label_suffix=f"w{value:g}",
                updates={"center_prior_weight": value},
            )
        )

    seen = set()
    unique = []
    for selector in selectors:
        label = selector["counterfactual_label"]
        if label not in seen:
            seen.add(label)
            unique.append(selector)
    return unique


def evaluate_counterfactuals(rows: list[dict], selectors: list[dict]) -> tuple[list[dict], list[dict]]:
    _, selected_indices = precompute_selected_indices(rows, selectors)
    variant_rows = []
    selected_case_rows = []
    for idx, selector in enumerate(selectors):
        selected_rows = selected_rows_for_selector_index(selectors, rows, selected_indices, idx)
        selected_case_rows.extend(selected_rows)
        selected_summary = summarize_selected(selector, selected_rows)
        gap_rows = build_gap_rows(rows, selector)
        feature_rows = summarize_features(gap_rows)
        gap_summary = summarize_gap_decomposition(gap_rows, feature_rows, selector)
        loss_counts = Counter(row["dominant_loss_feature"] for row in gap_rows if not bool(row["selected_all_truth"]))
        variant_rows.append(
            {
                "counterfactual_label": selector["counterfactual_label"],
                "counterfactual_family": selector["counterfactual_family"],
                "all_truth_case_count": safe_int(selected_summary["all_truth_case_count"]),
                "target0_hit_count": safe_int(selected_summary["target0_hit_count"]),
                "target1_hit_count": safe_int(selected_summary["target1_hit_count"]),
                "target2_hit_count": safe_int(selected_summary["target2_hit_count"]),
                "mean_unique_truth_hit_count": safe_float(selected_summary["mean_unique_truth_hit_count"]),
                "failed_selector_case_count": safe_int(gap_summary["failed_selector_case_count"]),
                "median_required_selector_gain_to_choose_truth": safe_float(
                    gap_summary["median_required_selector_gain_to_choose_truth"]
                ),
                "max_required_selector_gain_to_choose_truth": safe_float(
                    gap_summary["max_required_selector_gain_to_choose_truth"]
                ),
                "dominant_loss_feature": gap_summary["dominant_loss_feature"],
                "dominant_loss_feature_case_count": safe_int(
                    loss_counts.get(gap_summary["dominant_loss_feature"], 0)
                ),
                "component_balanced_weight": safe_float(selector.get("component_balanced_weight")),
                "hybrid_span_component_weight": safe_float(selector.get("hybrid_span_component_weight")),
                "component_min_weight": safe_float(selector.get("component_min_weight")),
                "span_prior_weight": safe_float(selector.get("span_prior_weight")),
                "signed_gap_prior_weight": safe_float(selector.get("signed_gap_prior_weight")),
                "center_prior_weight": safe_float(selector.get("center_prior_weight")),
                "rank_sum_weight": safe_float(selector.get("rank_sum_weight")),
                "max_rank_weight": safe_float(selector.get("max_rank_weight")),
            }
        )
    return variant_rows, selected_case_rows


def sort_variant_rows(rows: list[dict]) -> list[dict]:
    return sorted(
        rows,
        key=lambda row: (
            -safe_int(row["all_truth_case_count"]),
            -safe_float(row["mean_unique_truth_hit_count"], 0.0),
            safe_float(row["median_required_selector_gain_to_choose_truth"], math.inf),
            safe_float(row["max_required_selector_gain_to_choose_truth"], math.inf),
            str(row["counterfactual_label"]),
        ),
    )


def summarize_families(variant_rows: list[dict]) -> list[dict]:
    rows = []
    for family in sorted({row["counterfactual_family"] for row in variant_rows}):
        family_rows = [row for row in variant_rows if row["counterfactual_family"] == family]
        best = sort_variant_rows(family_rows)[0]
        rows.append(
            {
                "counterfactual_family": family,
                "variant_count": len(family_rows),
                "best_counterfactual_label": best["counterfactual_label"],
                "best_all_truth_case_count": safe_int(best["all_truth_case_count"]),
                "best_mean_unique_truth_hit_count": safe_float(best["mean_unique_truth_hit_count"]),
                "best_median_required_selector_gain": safe_float(
                    best["median_required_selector_gain_to_choose_truth"]
                ),
                "best_dominant_loss_feature": best["dominant_loss_feature"],
            }
        )
    return sorted(rows, key=lambda row: (-safe_int(row["best_all_truth_case_count"]), row["counterfactual_family"]))


def summarize_counterfactual_sensitivity(variant_rows: list[dict], family_rows: list[dict], base_label: str) -> dict:
    sorted_rows = sort_variant_rows(variant_rows)
    best = sorted_rows[0]
    base = [row for row in variant_rows if row["counterfactual_label"] == "base_current"][0]
    sgap_rows = [row for row in variant_rows if row["counterfactual_family"] == "signed_gap_sweep"]
    sgap_best = sort_variant_rows(sgap_rows)[0] if sgap_rows else {}
    improvement = safe_int(best["all_truth_case_count"]) - safe_int(base["all_truth_case_count"])
    ready = False
    return {
        "policy_label": "local_2d_detector_selector_counterfactual_sensitivity_cpu_no_fwi",
        "source_selector_label": base_label,
        "counterfactual_variant_count": len(variant_rows),
        "counterfactual_family_count": len(family_rows),
        "base_all_truth_case_count": safe_int(base["all_truth_case_count"]),
        "base_failed_selector_case_count": safe_int(base["failed_selector_case_count"]),
        "base_dominant_loss_feature": base["dominant_loss_feature"],
        "best_counterfactual_label": best["counterfactual_label"],
        "best_counterfactual_family": best["counterfactual_family"],
        "best_all_truth_case_count": safe_int(best["all_truth_case_count"]),
        "best_failed_selector_case_count": safe_int(best["failed_selector_case_count"]),
        "best_mean_unique_truth_hit_count": safe_float(best["mean_unique_truth_hit_count"]),
        "best_median_required_selector_gain": safe_float(best["median_required_selector_gain_to_choose_truth"]),
        "best_max_required_selector_gain": safe_float(best["max_required_selector_gain_to_choose_truth"]),
        "best_dominant_loss_feature": best["dominant_loss_feature"],
        "best_improvement_over_base_all_truth_cases": improvement,
        "signed_gap_best_label": sgap_best.get("counterfactual_label", ""),
        "signed_gap_best_all_truth_case_count": safe_int(sgap_best.get("all_truth_case_count"), 0),
        "signed_gap_zero_all_truth_case_count": safe_int(
            next(
                (
                    row["all_truth_case_count"]
                    for row in sgap_rows
                    if safe_float(row.get("signed_gap_prior_weight")) == 0.0
                ),
                0,
            )
        ),
        "ready_for_detector_seeded_fwi": ready,
        "gpu_priority": "none",
        "decision": (
            "Use this CPU-only counterfactual sensitivity as a guardrail around the detector selector. "
            "Simple one-dimensional reweighting around the geometry-family selector does not create a "
            "deployable top-1 detector initializer, so the detector role remains rank-gated/upper-bound "
            "unless a materially stronger waveform objective is introduced."
        ),
    }


def plot_counterfactual_sensitivity(
    summary: dict,
    variant_rows: list[dict],
    family_rows: list[dict],
    save_path: Path,
) -> str:
    families = family_rows
    family_labels = [row["counterfactual_family"].replace("_", "\n") for row in families]
    family_values = [safe_int(row["best_all_truth_case_count"]) for row in families]
    sgap_rows = sorted(
        [row for row in variant_rows if row["counterfactual_family"] == "signed_gap_sweep"],
        key=lambda row: safe_float(row["signed_gap_prior_weight"], 0.0),
    )
    fig, axes = plt.subplots(1, 2, figsize=(15.0, 5.2), constrained_layout=True)
    axes[0].bar(np.arange(len(families)), family_values, color="#4e79a7")
    axes[0].axhline(summary["base_all_truth_case_count"], color="#e15759", linestyle="--", linewidth=1.2)
    axes[0].set_xticks(np.arange(len(families)), family_labels, fontsize=8)
    axes[0].set_ylabel("best all-truth cases")
    axes[0].set_ylim(0, 12)
    axes[0].set_title("Best variant by counterfactual family")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    x = [safe_float(row["signed_gap_prior_weight"], 0.0) for row in sgap_rows]
    y_truth = [safe_int(row["all_truth_case_count"]) for row in sgap_rows]
    y_gain = [safe_float(row["median_required_selector_gain_to_choose_truth"], 0.0) for row in sgap_rows]
    axes[1].plot(x, y_truth, marker="o", color="#59a14f", label="all-truth cases")
    axes[1].set_xlabel("signed-gap prior weight")
    axes[1].set_ylabel("all-truth cases", color="#2f7d32")
    axes[1].set_ylim(0, 12)
    axes[1].tick_params(axis="y", labelcolor="#2f7d32")
    twin = axes[1].twinx()
    twin.plot(x, y_gain, marker="s", color="#e15759", label="median required gain")
    twin.set_ylabel("median required selector gain", color="#b0302f")
    twin.tick_params(axis="y", labelcolor="#b0302f")
    axes[1].set_title("Signed-gap weight sensitivity")
    axes[1].grid(axis="x", color="#eeeeee", linewidth=0.6)
    axes[1].text(
        0.02,
        0.95,
        f"base={summary['base_all_truth_case_count']}/12\n"
        f"best={summary['best_all_truth_case_count']}/12\n"
        f"improvement={summary['best_improvement_over_base_all_truth_cases']}\n"
        f"FWI={summary['ready_for_detector_seeded_fwi']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector selector counterfactual sensitivity", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, variant_csv: Path, family_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_selector_counterfactual_sensitivity.png`",
                "",
                "This CPU-only analysis tests simple one-dimensional reweighting around",
                "the current local 2D geometry-family detector selector.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Counterfactual variants: `{summary['counterfactual_variant_count']}`.",
                f"Base all-truth cases: `{summary['base_all_truth_case_count']}`.",
                f"Best counterfactual: `{summary['best_counterfactual_label']}`.",
                f"Best all-truth cases: `{summary['best_all_truth_case_count']}`.",
                f"Best improvement over base: `{summary['best_improvement_over_base_all_truth_cases']}`.",
                f"Best dominant loss feature: `{summary['best_dominant_loss_feature']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Variant rows: `{variant_csv.name}`.",
                f"- Family summary: `{family_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved detector rows only. It does not run FDTD, FWI,",
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
    parser.add_argument("--geometry-selector-run", default=DEFAULT_GEOMETRY_SELECTOR_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_selector_counterfactual_sensitivity")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    component_gate_dir = Path(args.summary_root) / args.component_gate_run
    geometry_selector_dir = Path(args.summary_root) / args.geometry_selector_run
    rows = [
        enrich_row(row)
        for row in read_csv_rows(component_gate_dir / "data/local_2d_detector_component_waveform_gate_rows.csv")
    ]
    selector_summary = read_json(
        geometry_selector_dir / "data/local_2d_detector_geometry_family_selector_summary.json"
    )
    source_selector_label = selector_summary["best_in_sample_selector_label"]
    base_selector = selector_from_label(source_selector_label)
    selectors = counterfactual_selector_grid(base_selector)
    variant_rows, selected_case_rows = evaluate_counterfactuals(rows, selectors)
    variant_rows = sort_variant_rows(variant_rows)
    family_rows = summarize_families(variant_rows)
    summary = summarize_counterfactual_sensitivity(variant_rows, family_rows, source_selector_label)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    variant_csv = data_dir / "local_2d_detector_selector_counterfactual_sensitivity_rows.csv"
    family_csv = data_dir / "local_2d_detector_selector_counterfactual_sensitivity_family_summary.csv"
    selected_csv = data_dir / "local_2d_detector_selector_counterfactual_selected_cases.csv"
    summary_json = data_dir / "local_2d_detector_selector_counterfactual_sensitivity_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_selector_counterfactual_sensitivity.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(variant_csv, [json_safe(row) for row in variant_rows])
    write_csv(family_csv, [json_safe(row) for row in family_rows])
    write_csv(selected_csv, [json_safe(row) for row in selected_case_rows])
    plot_counterfactual_sensitivity(summary, variant_rows, family_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "source_component_gate_rows_csv": str(component_gate_dir / "data/local_2d_detector_component_waveform_gate_rows.csv"),
        "source_geometry_selector_summary_json": str(
            geometry_selector_dir / "data/local_2d_detector_geometry_family_selector_summary.json"
        ),
        "variant_csv": str(variant_csv),
        "family_summary_csv": str(family_csv),
        "selected_cases_csv": str(selected_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, variant_csv, family_csv)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_selector_counterfactual_sensitivity",
        {
            "component_gate_run": args.component_gate_run,
            "geometry_selector_run": args.geometry_selector_run,
            "source_selector_label": source_selector_label,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

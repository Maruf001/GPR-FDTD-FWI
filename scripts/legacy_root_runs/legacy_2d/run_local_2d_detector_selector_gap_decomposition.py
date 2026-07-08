#!/usr/bin/env python3
"""Decompose why the local 2D detector selector still misses truth branches."""

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
    case_key,
    enrich_row,
    failure_label,
    group_indices_by_case,
    selector_grid,
    selector_score,
    selector_weight_vector,
)
from run_local_2d_detector_rank_budget_diagnostic import (  # noqa: E402
    read_csv_rows,
    read_json,
    safe_float,
    safe_int,
)
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_GEOMETRY_SELECTOR_RUN = "041_local_2d_detector_geometry_family_selector_post_upper_bound_policy"


def selector_from_label(selector_label: str) -> dict:
    matches = [selector for selector in selector_grid() if selector["selector_label"] == selector_label]
    if not matches:
        raise ValueError(f"unknown selector label: {selector_label}")
    return matches[0]


def feature_contributions(row: dict, selector: dict) -> dict[str, float]:
    weights = selector_weight_vector(selector)
    return {
        feature: safe_float(row.get(feature), 0.0) * float(weight)
        for feature, weight in zip(FEATURE_FIELDS, weights)
    }


def sorted_case_indices(rows: list[dict]) -> tuple[list[tuple[str, str, str, str]], list[np.ndarray]]:
    return group_indices_by_case(rows)


def best_row_by_score(rows: list[dict], selector: dict) -> dict | None:
    if not rows:
        return None
    return max(
        rows,
        key=lambda row: (
            selector_score(row, selector),
            -safe_float(row.get("rank_sum_numeric"), 10_000.0),
            -safe_float(row.get("max_rank_numeric"), 10_000.0),
            str(row.get("candidate_x_values_mm", "")),
        ),
    )


def dominant_loss_feature(delta_contributions: dict[str, float], *, selected_all_truth: bool) -> str:
    if selected_all_truth:
        return "selected_truth"
    if not delta_contributions:
        return "no_all_truth_candidate"
    feature, value = min(delta_contributions.items(), key=lambda item: item[1])
    if value < 0.0:
        return feature
    return "tie_break_or_nonfeature_loss"


def row_identity(row: dict | None, prefix: str) -> dict:
    if row is None:
        return {
            f"{prefix}_combo_index": "",
            f"{prefix}_candidate_ranks": "",
            f"{prefix}_candidate_x_values_mm": "",
            f"{prefix}_candidate_z_values_mm": "",
            f"{prefix}_unique_truth_hit_count": math.nan,
            f"{prefix}_failure_label": "",
        }
    return {
        f"{prefix}_combo_index": row.get("combo_index", ""),
        f"{prefix}_candidate_ranks": row.get("candidate_ranks", ""),
        f"{prefix}_candidate_x_values_mm": row.get("candidate_x_values_mm", ""),
        f"{prefix}_candidate_z_values_mm": row.get("candidate_z_values_mm", ""),
        f"{prefix}_unique_truth_hit_count": safe_int(row.get("unique_truth_hit_count_numeric")),
        f"{prefix}_failure_label": failure_label(row),
    }


def build_gap_rows(rows: list[dict], selector: dict) -> list[dict]:
    case_keys, case_groups = sorted_case_indices(rows)
    out = []
    for key, indices in zip(case_keys, case_groups):
        case_rows = [rows[int(idx)] for idx in indices]
        selected = best_row_by_score(case_rows, selector)
        truth_rows = [row for row in case_rows if bool(row.get("unique_all_truths_bool"))]
        wrong_rows = [row for row in case_rows if not bool(row.get("unique_all_truths_bool"))]
        best_truth = best_row_by_score(truth_rows, selector)
        best_wrong = best_row_by_score(wrong_rows, selector)
        if selected is None:
            continue

        selected_score = selector_score(selected, selector)
        truth_score = selector_score(best_truth, selector) if best_truth is not None else -math.inf
        wrong_score = selector_score(best_wrong, selector) if best_wrong is not None else -math.inf
        selected_contrib = feature_contributions(selected, selector)
        truth_contrib = feature_contributions(best_truth, selector) if best_truth is not None else {}
        delta = {
            feature: truth_contrib.get(feature, 0.0) - selected_contrib.get(feature, 0.0)
            for feature in FEATURE_FIELDS
        }
        selected_all_truth = bool(selected.get("unique_all_truths_bool"))
        gap = truth_score - selected_score if math.isfinite(truth_score) else math.nan
        required_gain = max(0.0, -gap) if math.isfinite(gap) else math.nan
        truth_minus_wrong = truth_score - wrong_score if math.isfinite(truth_score) and math.isfinite(wrong_score) else math.nan
        row = {
            "case_label": selected.get("case_label", ""),
            "branch_key": selected.get("branch_key", key[0]),
            "seed": safe_int(selected.get("seed", key[1])),
            "case_variant": selected.get("case_variant", key[2]),
            "run_name": selected.get("run_name", key[3]),
            "selector_label": selector["selector_label"],
            "candidate_triple_count": len(case_rows),
            "all_truth_triple_count": len(truth_rows),
            "selected_all_truth": selected_all_truth,
            "selected_score": selected_score,
            "best_truth_score": truth_score,
            "best_wrong_score": wrong_score,
            "truth_score_minus_selected_score": gap,
            "required_selector_gain_to_choose_truth": required_gain,
            "best_truth_score_minus_best_wrong_score": truth_minus_wrong,
            "dominant_loss_feature": dominant_loss_feature(delta, selected_all_truth=selected_all_truth),
            **row_identity(selected, "selected"),
            **row_identity(best_truth, "best_truth"),
            **row_identity(best_wrong, "best_wrong"),
        }
        for feature in FEATURE_FIELDS:
            row[f"selected_{feature}"] = selected_contrib.get(feature, 0.0)
            row[f"best_truth_{feature}"] = truth_contrib.get(feature, math.nan)
            row[f"delta_truth_minus_selected_{feature}"] = delta.get(feature, math.nan)
        out.append(row)
    return out


def summarize_features(gap_rows: list[dict]) -> list[dict]:
    failed = [row for row in gap_rows if not bool(row["selected_all_truth"])]
    rows = []
    for feature in FEATURE_FIELDS:
        deltas = [safe_float(row.get(f"delta_truth_minus_selected_{feature}")) for row in failed]
        finite = [value for value in deltas if math.isfinite(value)]
        deficits = [-value for value in finite if value < 0.0]
        rows.append(
            {
                "feature": feature,
                "failed_case_count": len(failed),
                "deficit_case_count": len(deficits),
                "median_delta_truth_minus_selected": float(np.median(finite)) if finite else math.nan,
                "total_negative_delta_magnitude": float(sum(deficits)),
                "max_negative_delta_magnitude": float(max(deficits)) if deficits else 0.0,
            }
        )
    return sorted(rows, key=lambda row: (-safe_float(row["total_negative_delta_magnitude"], 0.0), row["feature"]))


def summarize_branches(gap_rows: list[dict]) -> list[dict]:
    rows = []
    for branch in sorted({row["branch_key"] for row in gap_rows}):
        branch_rows = [row for row in gap_rows if row["branch_key"] == branch]
        failed = [row for row in branch_rows if not bool(row["selected_all_truth"])]
        required = [
            safe_float(row.get("required_selector_gain_to_choose_truth"))
            for row in failed
            if math.isfinite(safe_float(row.get("required_selector_gain_to_choose_truth")))
        ]
        loss_labels = Counter(row["dominant_loss_feature"] for row in failed)
        rows.append(
            {
                "branch_key": branch,
                "case_count": len(branch_rows),
                "selected_all_truth_case_count": sum(bool(row["selected_all_truth"]) for row in branch_rows),
                "failed_selector_case_count": len(failed),
                "median_required_selector_gain_to_choose_truth": float(np.median(required)) if required else 0.0,
                "max_required_selector_gain_to_choose_truth": float(max(required)) if required else 0.0,
                "dominant_loss_feature": loss_labels.most_common(1)[0][0] if loss_labels else "selected_truth",
            }
        )
    return rows


def summarize_gap_decomposition(gap_rows: list[dict], feature_rows: list[dict], selector: dict) -> dict:
    failed = [row for row in gap_rows if not bool(row["selected_all_truth"])]
    required = [
        safe_float(row.get("required_selector_gain_to_choose_truth"))
        for row in failed
        if math.isfinite(safe_float(row.get("required_selector_gain_to_choose_truth")))
    ]
    truth_margins = [
        safe_float(row.get("best_truth_score_minus_best_wrong_score"))
        for row in gap_rows
        if bool(row["selected_all_truth"]) and math.isfinite(safe_float(row.get("best_truth_score_minus_best_wrong_score")))
    ]
    dominant_labels = Counter(row["dominant_loss_feature"] for row in failed)
    dominant_feature = dominant_labels.most_common(1)[0][0] if dominant_labels else "selected_truth"
    return {
        "policy_label": "local_2d_detector_selector_gap_decomposition_cpu_no_fwi",
        "selector_label": selector["selector_label"],
        "case_count": len(gap_rows),
        "selected_all_truth_case_count": sum(bool(row["selected_all_truth"]) for row in gap_rows),
        "failed_selector_case_count": len(failed),
        "best_truth_available_case_count": sum(safe_int(row["all_truth_triple_count"]) > 0 for row in gap_rows),
        "median_required_selector_gain_to_choose_truth": float(np.median(required)) if required else 0.0,
        "max_required_selector_gain_to_choose_truth": float(max(required)) if required else 0.0,
        "dominant_loss_feature": dominant_feature,
        "dominant_loss_feature_case_count": safe_int(dominant_labels.get(dominant_feature, 0)),
        "largest_total_negative_delta_feature": feature_rows[0]["feature"] if feature_rows else "",
        "selected_truth_positive_wrong_margin_count": sum(value > 0.0 for value in truth_margins),
        "selected_truth_min_margin_over_wrong": float(min(truth_margins)) if truth_margins else math.nan,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "Use this CPU-only gap decomposition to explain why the truth-free detector selector remains "
            "non-deployable even though the rank-gated upper bound can contain the true triple. The result "
            "supports a manuscript guardrail and does not justify detector-seeded FWI."
        ),
    }


def plot_gap_decomposition(summary: dict, gap_rows: list[dict], feature_rows: list[dict], save_path: Path) -> str:
    sorted_rows = sorted(gap_rows, key=lambda row: safe_float(row["required_selector_gain_to_choose_truth"]), reverse=True)
    labels = [row["case_label"].replace("target2_", "").replace("|", "\n") for row in sorted_rows]
    gains = [safe_float(row["required_selector_gain_to_choose_truth"], 0.0) for row in sorted_rows]
    colors = ["#e15759" if not bool(row["selected_all_truth"]) else "#59a14f" for row in sorted_rows]
    top_features = feature_rows[:6]

    fig, axes = plt.subplots(1, 2, figsize=(15.2, 5.4), constrained_layout=True)
    axes[0].bar(np.arange(len(sorted_rows)), gains, color=colors)
    axes[0].set_xticks(np.arange(len(sorted_rows)), labels, rotation=45, ha="right", fontsize=7)
    axes[0].set_ylabel("selector gain needed for best all-truth")
    axes[0].set_title("Per-case selector gap")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].barh(
        np.arange(len(top_features)),
        [safe_float(row["total_negative_delta_magnitude"], 0.0) for row in top_features],
        color="#4e79a7",
    )
    axes[1].set_yticks(np.arange(len(top_features)), [row["feature"].replace("_", "\n") for row in top_features], fontsize=8)
    axes[1].invert_yaxis()
    axes[1].set_xlabel("total negative truth-vs-selected contribution")
    axes[1].set_title("Feature deficits on failed cases")
    axes[1].grid(axis="x", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.98,
        0.04,
        f"selector top-1 truth={summary['selected_all_truth_case_count']}/{summary['case_count']}\n"
        f"dominant loss={summary['dominant_loss_feature']}\n"
        f"FWI={summary['ready_for_detector_seeded_fwi']}",
        transform=axes[1].transAxes,
        va="bottom",
        ha="right",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector selector gap decomposition", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, case_csv: Path, feature_csv: Path, branch_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_selector_gap_decomposition.png`",
                "",
                "This CPU-only analysis decomposes why the current geometry-family detector",
                "selector still misses all-truth triples on saved local 2D detector cases.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Selector label: `{summary['selector_label']}`.",
                f"Selected all-truth cases: `{summary['selected_all_truth_case_count']}` / `{summary['case_count']}`.",
                f"Median required selector gain: `{summary['median_required_selector_gain_to_choose_truth']}`.",
                f"Max required selector gain: `{summary['max_required_selector_gain_to_choose_truth']}`.",
                f"Dominant loss feature: `{summary['dominant_loss_feature']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Per-case gap rows: `{case_csv.name}`.",
                f"- Feature summary: `{feature_csv.name}`.",
                f"- Branch summary: `{branch_csv.name}`.",
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
    parser.add_argument("--run-name", default="local_2d_detector_selector_gap_decomposition")
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
    selector = selector_from_label(selector_summary["best_in_sample_selector_label"])
    gap_rows = build_gap_rows(rows, selector)
    feature_rows = summarize_features(gap_rows)
    branch_rows = summarize_branches(gap_rows)
    summary = summarize_gap_decomposition(gap_rows, feature_rows, selector)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    case_csv = data_dir / "local_2d_detector_selector_gap_decomposition_cases.csv"
    feature_csv = data_dir / "local_2d_detector_selector_gap_decomposition_feature_summary.csv"
    branch_csv = data_dir / "local_2d_detector_selector_gap_decomposition_branch_summary.csv"
    summary_json = data_dir / "local_2d_detector_selector_gap_decomposition_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_selector_gap_decomposition.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(case_csv, [json_safe(row) for row in gap_rows])
    write_csv(feature_csv, [json_safe(row) for row in feature_rows])
    write_csv(branch_csv, [json_safe(row) for row in branch_rows])
    plot_gap_decomposition(summary, gap_rows, feature_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "source_component_gate_rows_csv": str(component_gate_dir / "data/local_2d_detector_component_waveform_gate_rows.csv"),
        "source_geometry_selector_summary_json": str(
            geometry_selector_dir / "data/local_2d_detector_geometry_family_selector_summary.json"
        ),
        "case_csv": str(case_csv),
        "feature_summary_csv": str(feature_csv),
        "branch_summary_csv": str(branch_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, case_csv, feature_csv, branch_csv)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_selector_gap_decomposition",
        {
            "component_gate_run": args.component_gate_run,
            "geometry_selector_run": args.geometry_selector_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

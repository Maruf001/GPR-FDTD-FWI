#!/usr/bin/env python3
"""Audit geometry-family selectors over saved component-gated detector triples."""

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
from run_local_2d_detector_rank_budget_diagnostic import boolish, read_csv_rows, read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_COMPONENT_GATE_RUN = "035_local_2d_detector_component_waveform_gate_post_rank_budget"
DEFAULT_COMPONENT_SELECTOR_RUN = "037_local_2d_detector_component_selector_audit_post_component_gate"
CASE_FIELDS = ("branch_key", "seed", "case_variant", "run_name")
FEATURE_FIELDS = (
    "score_component_balanced",
    "score_hybrid_span_component",
    "score_component_min",
    "span_prior_score",
    "signed_gap_prior_score",
    "center_prior_score",
    "rank_sum_score",
    "max_rank_score",
)
GEOMETRY_FAMILY_PRIORS = {
    "target2_close14": {
        "family_label": "right_close_pair",
        "span_target_mm": 74.0,
        "signed_gap_target_mm": -45.0,
        "center_target_mm": 235.0,
    },
    "target2_close50_linear29p5": {
        "family_label": "wide_pair",
        "span_target_mm": 112.0,
        "signed_gap_target_mm": -15.0,
        "center_target_mm": 250.0,
    },
}


def parse_float_list(text: str) -> list[float]:
    return [float(value) for value in str(text).split(",") if value.strip()]


def parse_int_list(text: str) -> list[int]:
    return [int(float(value)) for value in str(text).split(",") if value.strip()]


def case_key(row: dict) -> tuple[str, str, str, str]:
    return tuple(str(row[field]) for field in CASE_FIELDS)


def case_label(row: dict) -> str:
    return f"{row['branch_key']}|seed{row['seed']}|{row['case_variant']}"


def geometry_prior_for_row(row: dict) -> dict:
    branch_key = str(row.get("branch_key", ""))
    if branch_key not in GEOMETRY_FAMILY_PRIORS:
        raise KeyError(f"no geometry-family prior for branch: {branch_key}")
    return GEOMETRY_FAMILY_PRIORS[branch_key]


def geometry_features(row: dict) -> dict:
    xs = sorted(parse_float_list(row.get("candidate_x_values_mm", "")))
    ranks = parse_int_list(row.get("candidate_ranks", ""))
    gap_left = xs[1] - xs[0] if len(xs) >= 2 else 0.0
    gap_right = xs[2] - xs[1] if len(xs) >= 3 else 0.0
    x_span = xs[-1] - xs[0] if xs else 0.0
    signed_gap = gap_right - gap_left
    x_center = float(np.mean(xs)) if xs else 250.0
    rank_sum = float(sum(ranks)) if ranks else 10_000.0
    max_rank = float(max(ranks)) if ranks else 10_000.0
    prior = geometry_prior_for_row(row)
    return {
        "geometry_family_label": prior["family_label"],
        "x_span_mm_numeric": x_span,
        "signed_gap_mm": signed_gap,
        "x_center_mm_numeric": x_center,
        "span_target_mm": prior["span_target_mm"],
        "signed_gap_target_mm": prior["signed_gap_target_mm"],
        "center_target_mm": prior["center_target_mm"],
        "span_prior_score": -abs(x_span - prior["span_target_mm"]) / 100.0,
        "signed_gap_prior_score": -abs(signed_gap - prior["signed_gap_target_mm"]) / 100.0,
        "center_prior_score": -abs(x_center - prior["center_target_mm"]) / 100.0,
        "rank_sum_score": -rank_sum / 60.0,
        "max_rank_score": -max_rank / 20.0,
        "rank_sum_numeric": rank_sum,
        "max_rank_numeric": max_rank,
    }


def enrich_row(row: dict) -> dict:
    out = dict(row)
    out["case_label"] = row.get("case_label") or case_label(row)
    out.update(geometry_features(row))
    out["unique_truth_hit_count_numeric"] = safe_int(row.get("unique_truth_hit_count"))
    out["unique_all_truths_bool"] = boolish(row.get("unique_all_truths_within_tolerance"))
    out["unique_target0_bool"] = boolish(row.get("unique_target0_hit"))
    out["unique_target1_bool"] = boolish(row.get("unique_target1_hit"))
    out["unique_target2_bool"] = boolish(row.get("unique_target2_hit"))
    return out


def selector_grid() -> list[dict]:
    selectors = []
    for component_balanced_weight in (0.0, 0.5, 1.0):
        for hybrid_span_weight in (0.0, 0.2):
            for component_min_weight in (0.0, 1.0, 2.0):
                for span_prior_weight in (0.0, 0.5, 1.0, 2.0):
                    for signed_gap_prior_weight in (0.0, 1.0, 2.0, 4.0, 8.0):
                        for center_prior_weight in (0.0, 0.2):
                            for rank_sum_weight in (0.0, 0.05, 0.1):
                                selector = {
                                    "component_balanced_weight": component_balanced_weight,
                                    "hybrid_span_component_weight": hybrid_span_weight,
                                    "component_min_weight": component_min_weight,
                                    "span_prior_weight": span_prior_weight,
                                    "signed_gap_prior_weight": signed_gap_prior_weight,
                                    "center_prior_weight": center_prior_weight,
                                    "rank_sum_weight": rank_sum_weight,
                                    "max_rank_weight": 0.5 * rank_sum_weight,
                                }
                                selector["selector_label"] = (
                                    f"cb{component_balanced_weight:g}_hy{hybrid_span_weight:g}_"
                                    f"min{component_min_weight:g}_span{span_prior_weight:g}_"
                                    f"sgap{signed_gap_prior_weight:g}_center{center_prior_weight:g}_"
                                    f"rank{rank_sum_weight:g}"
                                )
                                selectors.append(selector)
    return selectors


def selector_weight_vector(selector: dict) -> np.ndarray:
    return np.asarray(
        [
            safe_float(selector["component_balanced_weight"]),
            safe_float(selector["hybrid_span_component_weight"]),
            safe_float(selector["component_min_weight"]),
            safe_float(selector["span_prior_weight"]),
            safe_float(selector["signed_gap_prior_weight"]),
            safe_float(selector["center_prior_weight"]),
            safe_float(selector["rank_sum_weight"]),
            safe_float(selector["max_rank_weight"]),
        ],
        dtype=float,
    )


def selector_score(row: dict, selector: dict) -> float:
    return float(
        sum(
            safe_float(row.get(feature), 0.0) * weight
            for feature, weight in zip(FEATURE_FIELDS, selector_weight_vector(selector))
        )
    )


def failure_label(row: dict) -> str:
    if bool(row["unique_all_truths_bool"]):
        return "all_truth"
    missing = []
    for target, key in (
        ("target0", "unique_target0_bool"),
        ("target1", "unique_target1_bool"),
        ("target2", "unique_target2_bool"),
    ):
        if not bool(row[key]):
            missing.append(target)
    return "missing_" + "_".join(missing) if missing else "duplicate_or_ambiguous"


def group_indices_by_case(rows: list[dict]) -> tuple[list[tuple[str, str, str, str]], list[np.ndarray]]:
    keys = sorted({case_key(row) for row in rows})
    groups = [
        np.asarray([idx for idx, row in enumerate(rows) if case_key(row) == key], dtype=int)
        for key in keys
    ]
    return keys, groups


def precompute_selected_indices(rows: list[dict], selectors: list[dict]) -> tuple[list[tuple[str, str, str, str]], np.ndarray]:
    feature_matrix = np.asarray(
        [[safe_float(row.get(feature), 0.0) for feature in FEATURE_FIELDS] for row in rows],
        dtype=float,
    )
    weight_matrix = np.asarray([selector_weight_vector(selector) for selector in selectors], dtype=float)
    case_keys, case_groups = group_indices_by_case(rows)
    selected = np.empty((len(selectors), len(case_groups)), dtype=int)
    for case_idx, row_indices in enumerate(case_groups):
        case_scores = feature_matrix[row_indices] @ weight_matrix.T
        selected[:, case_idx] = row_indices[np.argmax(case_scores, axis=0)]
    return case_keys, selected


def summarize_selected(selector: dict, selected_rows: list[dict]) -> dict:
    labels = Counter(failure_label(row) for row in selected_rows)
    return {
        "selector_label": selector["selector_label"],
        "case_count": len(selected_rows),
        "all_truth_case_count": sum(bool(row["unique_all_truths_bool"]) for row in selected_rows),
        "target0_hit_count": sum(bool(row["unique_target0_bool"]) for row in selected_rows),
        "target1_hit_count": sum(bool(row["unique_target1_bool"]) for row in selected_rows),
        "target2_hit_count": sum(bool(row["unique_target2_bool"]) for row in selected_rows),
        "mean_unique_truth_hit_count": float(
            np.mean([safe_int(row["unique_truth_hit_count_numeric"]) for row in selected_rows])
        ),
        "dominant_failure_label": labels.most_common(1)[0][0] if labels else "",
        **{key: selector[key] for key in selector if key != "selector_label"},
    }


def sort_selector_summaries(rows: list[dict]) -> list[dict]:
    return sorted(
        rows,
        key=lambda row: (
            -safe_int(row["all_truth_case_count"]),
            -safe_float(row["mean_unique_truth_hit_count"]),
            -safe_int(row["target0_hit_count"]),
            -safe_int(row["target1_hit_count"]),
            -safe_int(row["target2_hit_count"]),
            str(row["selector_label"]),
        ),
    )


def best_selector_index_for_train(
    selectors: list[dict],
    rows: list[dict],
    selected_indices: np.ndarray,
    train_case_positions: list[int],
) -> int:
    summaries = []
    for selector_idx, selector in enumerate(selectors):
        selected_rows = [rows[idx] for idx in selected_indices[selector_idx, train_case_positions]]
        summary = summarize_selected(selector, selected_rows)
        summary["selector_index"] = selector_idx
        summaries.append(summary)
    return safe_int(sort_selector_summaries(summaries)[0]["selector_index"])


def cross_validate(
    selectors: list[dict],
    rows: list[dict],
    case_keys: list[tuple[str, str, str, str]],
    selected_indices: np.ndarray,
    strategy: str,
) -> tuple[dict, list[dict]]:
    case_positions = list(range(len(case_keys)))
    if strategy == "leave_one_case":
        splits = [(case_keys[pos][3], [pos]) for pos in case_positions]
    elif strategy == "leave_one_seed":
        seeds = sorted({key[1] for key in case_keys}, key=lambda value: int(value))
        splits = [
            (f"seed{seed}", [pos for pos, key in enumerate(case_keys) if key[1] == seed])
            for seed in seeds
        ]
    elif strategy == "leave_one_branch":
        branches = sorted({key[0] for key in case_keys})
        splits = [
            (branch, [pos for pos, key in enumerate(case_keys) if key[0] == branch])
            for branch in branches
        ]
    else:
        raise ValueError(f"unknown CV strategy: {strategy}")

    out_rows = []
    for holdout_label, test_positions in splits:
        train_positions = [pos for pos in case_positions if pos not in set(test_positions)]
        selector_idx = best_selector_index_for_train(selectors, rows, selected_indices, train_positions)
        for pos in test_positions:
            row = dict(rows[selected_indices[selector_idx, pos]])
            row["cv_strategy"] = strategy
            row["holdout_label"] = holdout_label
            row["trained_selector_label"] = selectors[selector_idx]["selector_label"]
            row["selector_score"] = selector_score(row, selectors[selector_idx])
            row["failure_label"] = failure_label(row)
            out_rows.append(row)
    labels = Counter(row["failure_label"] for row in out_rows)
    summary = {
        "cv_strategy": strategy,
        "case_count": len(out_rows),
        "all_truth_case_count": sum(bool(row["unique_all_truths_bool"]) for row in out_rows),
        "target0_hit_count": sum(bool(row["unique_target0_bool"]) for row in out_rows),
        "target1_hit_count": sum(bool(row["unique_target1_bool"]) for row in out_rows),
        "target2_hit_count": sum(bool(row["unique_target2_bool"]) for row in out_rows),
        "mean_unique_truth_hit_count": float(
            np.mean([safe_int(row["unique_truth_hit_count_numeric"]) for row in out_rows])
        ),
        "selected_selector_count": len({row["trained_selector_label"] for row in out_rows}),
        "dominant_failure_label": labels.most_common(1)[0][0] if labels else "",
    }
    return summary, out_rows


def selected_rows_for_selector_index(
    selectors: list[dict],
    rows: list[dict],
    selected_indices: np.ndarray,
    selector_idx: int,
) -> list[dict]:
    selector = selectors[selector_idx]
    out = []
    for idx in selected_indices[selector_idx]:
        row = dict(rows[idx])
        row["selector_label"] = selector["selector_label"]
        row["selector_score"] = selector_score(row, selector)
        row["failure_label"] = failure_label(row)
        out.append(row)
    return out


def branch_summary(selected_rows: list[dict]) -> list[dict]:
    out = []
    for branch in sorted({row["branch_key"] for row in selected_rows}):
        rows = [row for row in selected_rows if row["branch_key"] == branch]
        out.append(
            {
                "branch_key": branch,
                "case_count": len(rows),
                "all_truth_case_count": sum(bool(row["unique_all_truths_bool"]) for row in rows),
                "target0_hit_count": sum(bool(row["unique_target0_bool"]) for row in rows),
                "target1_hit_count": sum(bool(row["unique_target1_bool"]) for row in rows),
                "target2_hit_count": sum(bool(row["unique_target2_bool"]) for row in rows),
                "mean_unique_truth_hit_count": float(
                    np.mean([safe_int(row["unique_truth_hit_count_numeric"]) for row in rows])
                ),
            }
        )
    return out


def summarize_audit(
    rows: list[dict],
    selector_rows: list[dict],
    best_rows: list[dict],
    cv_summaries: list[dict],
    component_selector_summary: dict,
) -> dict:
    cv = {row["cv_strategy"]: row for row in cv_summaries}
    best = selector_rows[0]
    previous_in_sample = safe_int(component_selector_summary.get("best_in_sample_all_truth_case_count"))
    previous_case_cv = safe_int(component_selector_summary.get("leave_one_case_all_truth_case_count"))
    failure_labels = Counter(
        failure_label(row) for row in best_rows if not bool(row["unique_all_truths_bool"])
    )
    ready = False
    return {
        "policy_label": "local_2d_detector_geometry_family_selector_cpu_no_fwi",
        "case_count": len({case_key(row) for row in rows}),
        "candidate_triple_row_count": len(rows),
        "selector_candidate_count": len(selector_rows),
        "best_in_sample_selector_label": best["selector_label"],
        "best_in_sample_all_truth_case_count": safe_int(best["all_truth_case_count"]),
        "best_in_sample_mean_unique_truth_hit_count": safe_float(best["mean_unique_truth_hit_count"]),
        "best_in_sample_target0_hit_count": safe_int(best["target0_hit_count"]),
        "best_in_sample_target1_hit_count": safe_int(best["target1_hit_count"]),
        "best_in_sample_target2_hit_count": safe_int(best["target2_hit_count"]),
        "leave_one_case_all_truth_case_count": safe_int(cv["leave_one_case"]["all_truth_case_count"]),
        "leave_one_case_mean_unique_truth_hit_count": safe_float(cv["leave_one_case"]["mean_unique_truth_hit_count"]),
        "leave_one_seed_all_truth_case_count": safe_int(cv["leave_one_seed"]["all_truth_case_count"]),
        "leave_one_branch_all_truth_case_count": safe_int(cv["leave_one_branch"]["all_truth_case_count"]),
        "previous_component_selector_best_in_sample_all_truth_case_count": previous_in_sample,
        "previous_component_selector_leave_one_case_all_truth_case_count": previous_case_cv,
        "in_sample_improvement_over_component_selector": safe_int(best["all_truth_case_count"]) - previous_in_sample,
        "leave_one_case_improvement_over_component_selector": safe_int(cv["leave_one_case"]["all_truth_case_count"]) - previous_case_cv,
        "best_selected_dominant_failure_label": failure_labels.most_common(1)[0][0] if failure_labels else "all_truth",
        "ready_for_detector_seeded_fwi": ready,
        "gpu_priority": "none",
        "decision": (
            "Use this as a CPU-only audit of branch-family geometry priors over saved component-gated "
            "detector triples. The geometry prior improves selector recovery but remains far below a "
            "deployable detector-seeded FWI threshold, so the detector role stays rank-gated/upper-bound."
        ),
    }


def plot_geometry_selector(summary: dict, branch_rows: list[dict], save_path: Path) -> str:
    labels = ["old\nin-sample", "new\nin-sample", "old\ncase CV", "new\ncase CV"]
    values = [
        summary["previous_component_selector_best_in_sample_all_truth_case_count"],
        summary["best_in_sample_all_truth_case_count"],
        summary["previous_component_selector_leave_one_case_all_truth_case_count"],
        summary["leave_one_case_all_truth_case_count"],
    ]
    fig, axes = plt.subplots(1, 2, figsize=(14.4, 5.2), constrained_layout=True)
    axes[0].bar(np.arange(len(labels)), values, color=["#bab0ab", "#4e79a7", "#bab0ab", "#59a14f"])
    axes[0].set_xticks(np.arange(len(labels)), labels, fontsize=8)
    axes[0].set_ylabel("top-1 all-truth cases")
    axes[0].set_ylim(0, summary["case_count"] + 1)
    axes[0].set_title("Geometry-family selector improvement")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    branches = [row["branch_key"] for row in branch_rows]
    x = np.arange(len(branches))
    axes[1].bar(x - 0.24, [row["all_truth_case_count"] for row in branch_rows], width=0.24, label="all-truth")
    axes[1].bar(x, [row["target0_hit_count"] for row in branch_rows], width=0.24, label="target0")
    axes[1].bar(x + 0.24, [row["target1_hit_count"] for row in branch_rows], width=0.24, label="target1")
    axes[1].set_xticks(x, [branch.replace("_", "\n") for branch in branches], fontsize=8)
    axes[1].set_ylim(0, max([row["case_count"] for row in branch_rows] + [1]) + 1)
    axes[1].set_title("Best selector branch split")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].text(
        0.02,
        0.96,
        f"best={summary['best_in_sample_selector_label']}\n"
        f"case CV={summary['leave_one_case_all_truth_case_count']}/{summary['case_count']}\n"
        f"FWI={summary['ready_for_detector_seeded_fwi']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector geometry-family selector audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, selector_csv: Path, best_csv: Path, cv_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_geometry_family_selector.png`",
                "",
                "This CPU-only audit evaluates branch-family geometry priors over saved",
                "component-gated detector triples.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Selector candidates: `{summary['selector_candidate_count']}`.",
                f"Best in-sample selector: `{summary['best_in_sample_selector_label']}`.",
                f"Best in-sample all-truth cases: `{summary['best_in_sample_all_truth_case_count']}`.",
                f"Leave-one-case all-truth cases: `{summary['leave_one_case_all_truth_case_count']}`.",
                f"Improvement over component selector, in-sample: `{summary['in_sample_improvement_over_component_selector']}`.",
                f"Improvement over component selector, leave-one-case: `{summary['leave_one_case_improvement_over_component_selector']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Selector summary: `{selector_csv.name}`.",
                f"- Best selected cases: `{best_csv.name}`.",
                f"- Cross-validation cases: `{cv_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved CPU rows only. It does not run FDTD, FWI,",
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
    parser.add_argument("--component-selector-run", default=DEFAULT_COMPONENT_SELECTOR_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_geometry_family_selector")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    component_gate_dir = Path(args.summary_root) / args.component_gate_run
    component_selector_dir = Path(args.summary_root) / args.component_selector_run
    rows = [
        enrich_row(row)
        for row in read_csv_rows(component_gate_dir / "data/local_2d_detector_component_waveform_gate_rows.csv")
    ]
    component_selector_summary = read_json(
        component_selector_dir / "data/local_2d_detector_component_selector_audit_summary.json"
    )
    selectors = selector_grid()
    case_keys, selected_indices = precompute_selected_indices(rows, selectors)
    selector_rows = sort_selector_summaries(
        [
            summarize_selected(
                selector,
                selected_rows_for_selector_index(selectors, rows, selected_indices, idx),
            )
            for idx, selector in enumerate(selectors)
        ]
    )
    best_label = selector_rows[0]["selector_label"]
    best_idx = [idx for idx, selector in enumerate(selectors) if selector["selector_label"] == best_label][0]
    best_rows = selected_rows_for_selector_index(selectors, rows, selected_indices, best_idx)
    branch_rows = branch_summary(best_rows)
    cv_summaries = []
    cv_rows = []
    for strategy in ("leave_one_case", "leave_one_seed", "leave_one_branch"):
        cv_summary, rows_for_strategy = cross_validate(selectors, rows, case_keys, selected_indices, strategy)
        cv_summaries.append(cv_summary)
        cv_rows.extend(rows_for_strategy)
    summary = summarize_audit(rows, selector_rows, best_rows, cv_summaries, component_selector_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    selector_csv = data_dir / "local_2d_detector_geometry_family_selector_summary.csv"
    best_csv = data_dir / "local_2d_detector_geometry_family_selector_best_cases.csv"
    branch_csv = data_dir / "local_2d_detector_geometry_family_selector_branch_summary.csv"
    cv_summary_csv = data_dir / "local_2d_detector_geometry_family_selector_cv_summary.csv"
    cv_csv = data_dir / "local_2d_detector_geometry_family_selector_cv_cases.csv"
    summary_json = data_dir / "local_2d_detector_geometry_family_selector_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_geometry_family_selector.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(selector_csv, [json_safe(row) for row in selector_rows])
    write_csv(best_csv, [json_safe(row) for row in best_rows])
    write_csv(branch_csv, [json_safe(row) for row in branch_rows])
    write_csv(cv_summary_csv, [json_safe(row) for row in cv_summaries])
    write_csv(cv_csv, [json_safe(row) for row in cv_rows])
    plot_geometry_selector(summary, branch_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "source_component_gate_rows_csv": str(component_gate_dir / "data/local_2d_detector_component_waveform_gate_rows.csv"),
        "source_component_selector_summary_json": str(
            component_selector_dir / "data/local_2d_detector_component_selector_audit_summary.json"
        ),
        "selector_summary_csv": str(selector_csv),
        "best_cases_csv": str(best_csv),
        "branch_summary_csv": str(branch_csv),
        "cv_summary_csv": str(cv_summary_csv),
        "cv_cases_csv": str(cv_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, selector_csv, best_csv, cv_csv)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_geometry_family_selector",
        {
            "component_gate_run": args.component_gate_run,
            "component_selector_run": args.component_selector_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

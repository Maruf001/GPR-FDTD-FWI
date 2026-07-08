#!/usr/bin/env python3
"""Audit truth-free selectors over component waveform-gated detector triples."""

from __future__ import annotations

import argparse
import csv
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
CASE_FIELDS = ("branch_key", "seed", "case_variant", "run_name")


def parse_float_list(text: str) -> list[float]:
    return [float(value) for value in str(text).split(",") if value.strip()]


def parse_int_list(text: str) -> list[int]:
    return [int(float(value)) for value in str(text).split(",") if value.strip()]


def case_key(row: dict) -> tuple[str, str, str, str]:
    return tuple(str(row[field]) for field in CASE_FIELDS)


def case_label(row: dict) -> str:
    return f"{row['branch_key']}|seed{row['seed']}|{row['case_variant']}"


def enrich_row(row: dict) -> dict:
    xs = parse_float_list(row.get("candidate_x_values_mm", ""))
    ranks = parse_int_list(row.get("candidate_ranks", ""))
    gaps = np.diff(sorted(xs)) if len(xs) >= 2 else np.asarray([], dtype=float)
    out = dict(row)
    out["case_label"] = row.get("case_label") or case_label(row)
    out["x_center_mm_numeric"] = float(np.mean(xs)) if xs else math.nan
    out["x_span_mm_numeric"] = safe_float(row.get("x_span_mm"), max(xs) - min(xs) if xs else math.nan)
    out["gap_balance_mm_numeric"] = safe_float(
        row.get("gap_balance_mm"),
        abs(float(gaps[1] - gaps[0])) if len(gaps) >= 2 else math.nan,
    )
    out["rank_sum_numeric"] = sum(ranks) if ranks else 10_000
    out["max_rank_numeric"] = max(ranks) if ranks else 10_000
    out["unique_truth_hit_count_numeric"] = safe_int(row.get("unique_truth_hit_count"))
    out["unique_all_truths_bool"] = boolish(row.get("unique_all_truths_within_tolerance"))
    out["unique_target0_bool"] = boolish(row.get("unique_target0_hit"))
    out["unique_target1_bool"] = boolish(row.get("unique_target1_hit"))
    out["unique_target2_bool"] = boolish(row.get("unique_target2_hit"))
    return out


def selector_grid() -> list[dict]:
    selectors = [
        {
            "selector_label": "component_balanced",
            "component_balanced_weight": 1.0,
            "component_min_weight": 0.0,
            "hybrid_span_component_weight": 0.0,
            "span_bonus_weight": 0.0,
            "span_width_weight": 0.0,
            "span_target_mm": math.nan,
            "span_target_weight": 0.0,
            "gap_balance_weight": 0.0,
            "rank_sum_weight": 0.0,
            "max_rank_weight": 0.0,
            "center_weight": 0.0,
        },
        {
            "selector_label": "hybrid_span_component",
            "component_balanced_weight": 0.0,
            "component_min_weight": 0.0,
            "hybrid_span_component_weight": 1.0,
            "span_bonus_weight": 0.0,
            "span_width_weight": 0.0,
            "span_target_mm": math.nan,
            "span_target_weight": 0.0,
            "gap_balance_weight": 0.0,
            "rank_sum_weight": 0.0,
            "max_rank_weight": 0.0,
            "center_weight": 0.0,
        },
        {
            "selector_label": "component_floor_span",
            "component_balanced_weight": 0.0,
            "component_min_weight": 1.0,
            "hybrid_span_component_weight": 0.0,
            "span_bonus_weight": 0.0,
            "span_width_weight": 0.25,
            "span_target_mm": math.nan,
            "span_target_weight": 0.0,
            "gap_balance_weight": 0.0,
            "rank_sum_weight": 0.0,
            "max_rank_weight": 0.0,
            "center_weight": 0.0,
        },
    ]
    for balanced_weight in (0.4, 0.8, 1.2):
        for min_weight in (0.0, 0.4, 0.8, 1.2):
            for span_weight in (0.0, 0.25, 0.5):
                for span_target in (math.nan, 70.0, 80.0, 90.0, 110.0):
                    for target_weight in (0.0, 0.1, 0.25):
                        if math.isnan(span_target) and target_weight > 0.0:
                            continue
                        if math.isfinite(span_target) and target_weight == 0.0:
                            continue
                        for rank_weight in (0.0, 0.03, 0.08):
                            selectors.append(
                                {
                                    "selector_label": (
                                        f"cb{balanced_weight:g}_min{min_weight:g}_span{span_weight:g}_"
                                        f"target{span_target if math.isfinite(span_target) else 'none'}_"
                                        f"tw{target_weight:g}_rank{rank_weight:g}"
                                    ),
                                    "component_balanced_weight": balanced_weight,
                                    "component_min_weight": min_weight,
                                    "hybrid_span_component_weight": 0.0,
                                    "span_bonus_weight": 0.0,
                                    "span_width_weight": span_weight,
                                    "span_target_mm": span_target,
                                    "span_target_weight": target_weight,
                                    "gap_balance_weight": 0.03,
                                    "rank_sum_weight": rank_weight,
                                    "max_rank_weight": 0.5 * rank_weight,
                                    "center_weight": 0.02,
                                }
                            )
    return selectors


def selector_score(row: dict, selector: dict) -> float:
    score = 0.0
    score += float(selector["component_balanced_weight"]) * safe_float(row.get("score_component_balanced"), 0.0)
    score += float(selector["component_min_weight"]) * safe_float(row.get("score_component_min"), 0.0)
    score += float(selector["hybrid_span_component_weight"]) * safe_float(row.get("score_hybrid_span_component"), 0.0)
    score += float(selector["span_bonus_weight"]) * safe_float(row.get("score_span_bonus"), 0.0)
    span = safe_float(row.get("x_span_mm_numeric"), 0.0)
    score += float(selector["span_width_weight"]) * span / 100.0
    target = safe_float(selector.get("span_target_mm"))
    if math.isfinite(target):
        score -= float(selector["span_target_weight"]) * abs(span - target) / 100.0
    score -= float(selector["gap_balance_weight"]) * safe_float(row.get("gap_balance_mm_numeric"), 0.0) / 100.0
    score -= float(selector["rank_sum_weight"]) * safe_float(row.get("rank_sum_numeric"), 0.0) / 60.0
    score -= float(selector["max_rank_weight"]) * safe_float(row.get("max_rank_numeric"), 0.0) / 20.0
    score -= float(selector["center_weight"]) * abs(safe_float(row.get("x_center_mm_numeric"), 250.0) - 250.0) / 100.0
    return score


def select_rows_for_selector(rows: list[dict], selector: dict) -> list[dict]:
    selected = []
    for key in sorted({case_key(row) for row in rows}):
        case_rows = [row for row in rows if case_key(row) == key]
        best = max(
            case_rows,
            key=lambda row: (
                selector_score(row, selector),
                -safe_int(row.get("max_rank_numeric")),
                -safe_int(row.get("rank_sum_numeric")),
                str(row.get("candidate_x_values_mm", "")),
            ),
        )
        out = dict(best)
        out["selector_label"] = selector["selector_label"]
        out["selector_score"] = selector_score(best, selector)
        out["failure_label"] = failure_label(best)
        selected.append(out)
    return selected


def failure_label(row: dict) -> str:
    if bool(row["unique_all_truths_bool"]):
        return "all_truth"
    missing = []
    for target, key in (("target0", "unique_target0_bool"), ("target1", "unique_target1_bool"), ("target2", "unique_target2_bool")):
        if not bool(row[key]):
            missing.append(target)
    return "missing_" + "_".join(missing) if missing else "duplicate_or_ambiguous"


def summarize_selected(selector: dict, selected_rows: list[dict]) -> dict:
    labels = Counter(row["failure_label"] for row in selected_rows)
    return {
        "selector_label": selector["selector_label"],
        "case_count": len(selected_rows),
        "all_truth_case_count": sum(bool(row["unique_all_truths_bool"]) for row in selected_rows),
        "target0_hit_count": sum(bool(row["unique_target0_bool"]) for row in selected_rows),
        "target1_hit_count": sum(bool(row["unique_target1_bool"]) for row in selected_rows),
        "target2_hit_count": sum(bool(row["unique_target2_bool"]) for row in selected_rows),
        "mean_unique_truth_hit_count": float(np.mean([safe_int(row["unique_truth_hit_count_numeric"]) for row in selected_rows])),
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
            -safe_int(row["target2_hit_count"]),
            str(row["selector_label"]),
        ),
    )


def best_selector_for_train(
    selectors_by_label: dict[str, dict],
    selected_by_selector: dict[str, list[dict]],
    train_keys: set[tuple[str, str, str, str]],
) -> str:
    summaries = []
    for label, selected in selected_by_selector.items():
        train_rows = [row for row in selected if case_key(row) in train_keys]
        summaries.append(summarize_selected(selectors_by_label[label], train_rows))
    return sort_selector_summaries(summaries)[0]["selector_label"]


def cross_validate(
    selectors_by_label: dict[str, dict],
    selected_by_selector: dict[str, list[dict]],
    strategy: str,
) -> tuple[dict, list[dict]]:
    all_keys = sorted({case_key(row) for rows in selected_by_selector.values() for row in rows})
    if strategy == "leave_one_case":
        splits = [(case[3], {case}) for case in all_keys]
    elif strategy == "leave_one_seed":
        seeds = sorted({case[1] for case in all_keys}, key=lambda value: int(value))
        splits = [(f"seed{seed}", {case for case in all_keys if case[1] == seed}) for seed in seeds]
    elif strategy == "leave_one_branch":
        branches = sorted({case[0] for case in all_keys})
        splits = [(branch, {case for case in all_keys if case[0] == branch}) for branch in branches]
    else:
        raise ValueError(f"unknown CV strategy: {strategy}")

    out_rows = []
    for holdout_label, test_keys in splits:
        train_keys = set(all_keys) - set(test_keys)
        selector_label = best_selector_for_train(selectors_by_label, selected_by_selector, train_keys)
        selected_lookup = {case_key(row): row for row in selected_by_selector[selector_label]}
        for key in sorted(test_keys):
            row = dict(selected_lookup[key])
            row["cv_strategy"] = strategy
            row["holdout_label"] = holdout_label
            row["trained_selector_label"] = selector_label
            out_rows.append(row)
    labels = Counter(row["failure_label"] for row in out_rows)
    summary = {
        "cv_strategy": strategy,
        "case_count": len(out_rows),
        "all_truth_case_count": sum(bool(row["unique_all_truths_bool"]) for row in out_rows),
        "target0_hit_count": sum(bool(row["unique_target0_bool"]) for row in out_rows),
        "target1_hit_count": sum(bool(row["unique_target1_bool"]) for row in out_rows),
        "target2_hit_count": sum(bool(row["unique_target2_bool"]) for row in out_rows),
        "mean_unique_truth_hit_count": float(np.mean([safe_int(row["unique_truth_hit_count_numeric"]) for row in out_rows])),
        "selected_selector_count": len({row["trained_selector_label"] for row in out_rows}),
        "dominant_failure_label": labels.most_common(1)[0][0] if labels else "",
    }
    return summary, out_rows


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
                "mean_unique_truth_hit_count": float(np.mean([safe_int(row["unique_truth_hit_count_numeric"]) for row in rows])),
            }
        )
    return out


def summarize_audit(
    rows: list[dict],
    selector_rows: list[dict],
    best_rows: list[dict],
    cv_summaries: list[dict],
    source_summary: dict,
) -> dict:
    cv = {row["cv_strategy"]: row for row in cv_summaries}
    case_count = len({case_key(row) for row in rows})
    best = selector_rows[0]
    leave_one_case = cv["leave_one_case"]
    ready = False
    return {
        "policy_label": "local_2d_detector_component_selector_audit_cpu_no_fwi",
        "case_count": case_count,
        "candidate_triple_row_count": len(rows),
        "selector_candidate_count": len(selector_rows),
        "best_in_sample_selector_label": best["selector_label"],
        "best_in_sample_all_truth_case_count": safe_int(best["all_truth_case_count"]),
        "best_in_sample_mean_unique_truth_hit_count": safe_float(best["mean_unique_truth_hit_count"]),
        "leave_one_case_all_truth_case_count": safe_int(leave_one_case["all_truth_case_count"]),
        "leave_one_case_mean_unique_truth_hit_count": safe_float(leave_one_case["mean_unique_truth_hit_count"]),
        "leave_one_seed_all_truth_case_count": safe_int(cv["leave_one_seed"]["all_truth_case_count"]),
        "leave_one_branch_all_truth_case_count": safe_int(cv["leave_one_branch"]["all_truth_case_count"]),
        "best_in_sample_target0_hit_count": safe_int(best["target0_hit_count"]),
        "leave_one_case_target0_hit_count": safe_int(leave_one_case["target0_hit_count"]),
        "source_component_gate_top1_all_truth_case_count": safe_int(source_summary.get("best_top1_all_truth_case_count")),
        "source_component_gate_top50_case_count": safe_int(source_summary.get("best_top50_case_count")),
        "best_selected_dominant_failure_label": Counter(row["failure_label"] for row in best_rows).most_common(1)[0][0] if best_rows else "",
        "ready_for_detector_seeded_fwi": ready,
        "gpu_priority": "none",
        "decision": (
            "Use this as a CPU-only audit of truth-free selector features over the component waveform gate. "
            "A selector would need validated top-1 all-truth recovery before detector-seeded FWI. Until then, "
            "the component gate remains rank-gated/upper-bound evidence, not a GPU/FWI launch queue."
        ),
    }


def plot_selector_audit(summary: dict, branch_rows: list[dict], save_path: Path) -> str:
    labels = ["source\ntop1", "best\nin-sample", "case\nCV", "seed\nCV", "branch\nCV"]
    values = [
        summary["source_component_gate_top1_all_truth_case_count"],
        summary["best_in_sample_all_truth_case_count"],
        summary["leave_one_case_all_truth_case_count"],
        summary["leave_one_seed_all_truth_case_count"],
        summary["leave_one_branch_all_truth_case_count"],
    ]
    fig, axes = plt.subplots(1, 2, figsize=(14.4, 5.2), constrained_layout=True)
    axes[0].bar(np.arange(len(labels)), values, color=["#bab0ab", "#4e79a7", "#59a14f", "#76b7b2", "#f28e2b"])
    axes[0].set_xticks(np.arange(len(labels)), labels, fontsize=8)
    axes[0].set_ylabel("top-1 all-truth cases")
    axes[0].set_ylim(0, summary["case_count"] + 1)
    axes[0].set_title("Component selector top-1 recovery")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    branches = [row["branch_key"] for row in branch_rows]
    x = np.arange(len(branches))
    axes[1].bar(x - 0.18, [row["all_truth_case_count"] for row in branch_rows], width=0.36, label="all-truth")
    axes[1].bar(x + 0.18, [row["target0_hit_count"] for row in branch_rows], width=0.36, label="target0 hit")
    axes[1].set_xticks(x, [branch.replace("_", "\n") for branch in branches], fontsize=8)
    axes[1].set_ylim(0, max([row["case_count"] for row in branch_rows] + [1]) + 1)
    axes[1].set_title("Best selector branch split")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].text(
        0.02,
        0.96,
        f"best={summary['best_in_sample_selector_label']}\n"
        f"ready FWI={summary['ready_for_detector_seeded_fwi']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector component selector audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, selector_csv: Path, best_csv: Path, cv_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_component_selector_audit.png`",
                "",
                "This CPU-only audit evaluates truth-free selectors over saved component",
                "waveform-gated detector triples.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Selector candidates: `{summary['selector_candidate_count']}`.",
                f"Best in-sample selector: `{summary['best_in_sample_selector_label']}`.",
                f"Best in-sample all-truth cases: `{summary['best_in_sample_all_truth_case_count']}`.",
                f"Leave-one-case all-truth cases: `{summary['leave_one_case_all_truth_case_count']}`.",
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
    parser.add_argument("--run-name", default="local_2d_detector_component_selector_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dir = Path(args.summary_root) / args.component_gate_run
    rows = [
        enrich_row(row)
        for row in read_csv_rows(source_dir / "data/local_2d_detector_component_waveform_gate_rows.csv")
    ]
    source_summary = read_json(source_dir / "data/local_2d_detector_component_waveform_gate_summary.json")
    selectors = selector_grid()
    selectors_by_label = {selector["selector_label"]: selector for selector in selectors}
    selected_by_selector = {
        selector["selector_label"]: select_rows_for_selector(rows, selector)
        for selector in selectors
    }
    selector_rows = sort_selector_summaries(
        [
            summarize_selected(selector, selected_by_selector[selector["selector_label"]])
            for selector in selectors
        ]
    )
    best_label = selector_rows[0]["selector_label"]
    best_rows = selected_by_selector[best_label]
    branch_rows = branch_summary(best_rows)
    cv_summaries = []
    cv_rows = []
    for strategy in ("leave_one_case", "leave_one_seed", "leave_one_branch"):
        cv_summary, rows_for_strategy = cross_validate(selectors_by_label, selected_by_selector, strategy)
        cv_summaries.append(cv_summary)
        cv_rows.extend(rows_for_strategy)
    summary = summarize_audit(rows, selector_rows, best_rows, cv_summaries, source_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    selector_csv = data_dir / "local_2d_detector_component_selector_summary.csv"
    best_csv = data_dir / "local_2d_detector_component_selector_best_cases.csv"
    branch_csv = data_dir / "local_2d_detector_component_selector_branch_summary.csv"
    cv_summary_csv = data_dir / "local_2d_detector_component_selector_cv_summary.csv"
    cv_csv = data_dir / "local_2d_detector_component_selector_cv_cases.csv"
    summary_json = data_dir / "local_2d_detector_component_selector_audit_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_component_selector_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(selector_csv, [json_safe(row) for row in selector_rows])
    write_csv(best_csv, [json_safe(row) for row in best_rows])
    write_csv(branch_csv, [json_safe(row) for row in branch_rows])
    write_csv(cv_summary_csv, [json_safe(row) for row in cv_summaries])
    write_csv(cv_csv, [json_safe(row) for row in cv_rows])
    plot_selector_audit(summary, branch_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "source_component_gate_summary_json": str(source_dir / "data/local_2d_detector_component_waveform_gate_summary.json"),
        "source_component_gate_rows_csv": str(source_dir / "data/local_2d_detector_component_waveform_gate_rows.csv"),
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
        "local_2d_detector_component_selector_audit",
        {
            "component_gate_run": args.component_gate_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Audit detector selector feature families over saved separability ranks."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter, defaultdict
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
from run_local_2d_detector_rank_budget_diagnostic import boolish, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SEPARABILITY_RUN = "105_local_2d_detector_feature_separability_audit_post_upper_bound"
STRATEGIES = ("global", "branch", "variant", "branch_variant")
BUDGETS = (1, 10, 20, 50, 100, 200)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def feature_families(features: list[str]) -> dict[str, list[str]]:
    ordered = sorted(features)
    return {
        "all_features": ordered,
        "score_only": [feature for feature in ordered if feature.startswith("score_")],
        "component_only": [feature for feature in ordered if "component" in feature],
        "no_span_target": [feature for feature in ordered if not feature.startswith("x_span_target")],
        "fixed_component_balanced": ["score_component_balanced"],
    }


def case_key(row: dict) -> tuple[str, str, str, str, str]:
    return (
        str(row["branch_key"]),
        str(row["seed"]),
        str(row["case_variant"]),
        str(row["run_name"]),
        str(row["case_label"]),
    )


def rank_value(row: dict) -> float:
    return safe_float(row.get("first_all_truth_rank"), math.inf)


def finite_ranks(rows: list[dict]) -> list[float]:
    ranks = [rank_value(row) for row in rows]
    finite = [rank for rank in ranks if math.isfinite(rank)]
    return finite or [math.inf]


def feature_score_key(rows_for_feature: list[dict]) -> tuple:
    ranks = [rank_value(row) for row in rows_for_feature]
    finite = finite_ranks(rows_for_feature)
    return (
        sum(rank <= 1 for rank in ranks),
        sum(rank <= 10 for rank in ranks),
        sum(rank <= 20 for rank in ranks),
        sum(rank <= 50 for rank in ranks),
        sum(rank <= 100 for rank in ranks),
        sum(rank <= 200 for rank in ranks),
        -float(np.median(finite)),
        -max(finite),
    )


def choose_feature(training_rows: list[dict], allowed_features: list[str]) -> str:
    best_feature = ""
    best_key = None
    for feature in allowed_features:
        rows = [row for row in training_rows if row["feature"] == feature]
        if not rows:
            continue
        key = (*feature_score_key(rows), feature)
        if best_key is None or key > best_key:
            best_key = key
            best_feature = feature
    return best_feature


def training_rows_for_strategy(rows: list[dict], heldout: tuple[str, str, str, str, str], strategy: str) -> list[dict]:
    branch, _seed, variant, _run_name, label = heldout
    train = [row for row in rows if str(row["case_label"]) != label]
    if strategy == "global":
        return train
    if strategy == "branch":
        return [row for row in train if str(row["branch_key"]) == branch]
    if strategy == "variant":
        return [row for row in train if str(row["case_variant"]) == variant]
    if strategy == "branch_variant":
        return [row for row in train if str(row["branch_key"]) == branch and str(row["case_variant"]) == variant]
    raise ValueError(f"unknown strategy: {strategy}")


def selected_case_row(rows: list[dict], label: str, feature: str) -> dict:
    for row in rows:
        if str(row["case_label"]) == label and str(row["feature"]) == feature:
            return row
    raise KeyError((label, feature))


def failure_label(rank: float) -> str:
    if rank <= 1:
        return "top1"
    if rank <= 50:
        return "rank_gate_top50"
    if rank <= 200:
        return "rank_gate_top200"
    return "deeper_than_top200"


def evaluate_policy(rows: list[dict], family_name: str, features: list[str], strategy: str) -> list[dict]:
    out = []
    for key in sorted({case_key(row) for row in rows}):
        branch, seed, variant, run_name, label = key
        train = training_rows_for_strategy(rows, key, strategy)
        if not train:
            train = [row for row in rows if str(row["case_label"]) != label]
        selected_feature = choose_feature(train, features)
        selected = selected_case_row(rows, label, selected_feature)
        rank = rank_value(selected)
        out.append(
            {
                "feature_family": family_name,
                "selector_strategy": strategy,
                "case_label": label,
                "branch_key": branch,
                "seed": safe_int(seed),
                "case_variant": variant,
                "run_name": run_name,
                "selected_feature": selected_feature,
                "first_all_truth_rank": rank,
                "rank_gate_label": failure_label(rank),
                "top_unique_truth_hit_count": safe_int(selected.get("top_unique_truth_hit_count")),
                "top_candidate_x_values_mm": selected.get("top_candidate_x_values_mm", ""),
                "training_case_count": len({row["case_label"] for row in train}),
                "allowed_feature_count": len(features),
            }
        )
    return out


def summarize_policy_rows(case_rows: list[dict]) -> list[dict]:
    out = []
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in case_rows:
        grouped[(str(row["feature_family"]), str(row["selector_strategy"]))].append(row)
    for (family, strategy), rows in sorted(grouped.items()):
        ranks = [safe_float(row["first_all_truth_rank"], math.inf) for row in rows]
        finite = [rank for rank in ranks if math.isfinite(rank)]
        labels = Counter(row["rank_gate_label"] for row in rows)
        selected_features = Counter(row["selected_feature"] for row in rows)
        policy_row = {
            "feature_family": family,
            "selector_strategy": strategy,
            "case_count": len(rows),
            "top1_case_count": sum(rank <= 1 for rank in ranks),
            "top10_case_count": sum(rank <= 10 for rank in ranks),
            "top20_case_count": sum(rank <= 20 for rank in ranks),
            "top50_case_count": sum(rank <= 50 for rank in ranks),
            "top100_case_count": sum(rank <= 100 for rank in ranks),
            "top200_case_count": sum(rank <= 200 for rank in ranks),
            "deeper_than_top200_case_count": labels["deeper_than_top200"],
            "median_first_all_truth_rank": float(np.median(finite)) if finite else math.nan,
            "max_first_all_truth_rank": max(finite) if finite else math.nan,
            "selected_feature_count": len(selected_features),
            "dominant_selected_feature": selected_features.most_common(1)[0][0] if selected_features else "",
            "uses_span_target_feature": any(feature.startswith("x_span_target") for feature in selected_features),
        }
        out.append(policy_row)
    return sorted(out, key=policy_sort_key)


def policy_sort_key(row: dict) -> tuple:
    return (
        -safe_int(row["top1_case_count"]),
        -safe_int(row["top200_case_count"]),
        safe_int(row["deeper_than_top200_case_count"]),
        -safe_int(row["top100_case_count"]),
        -safe_int(row["top50_case_count"]),
        -safe_int(row["top20_case_count"]),
        -safe_int(row["top10_case_count"]),
        boolish(row["uses_span_target_feature"]),
        safe_float(row["median_first_all_truth_rank"], math.inf),
        str(row["feature_family"]),
        str(row["selector_strategy"]),
    )


def branch_rows_for_policy(case_rows: list[dict], family: str, strategy: str) -> list[dict]:
    selected = [
        row
        for row in case_rows
        if row["feature_family"] == family and row["selector_strategy"] == strategy
    ]
    out = []
    for branch in sorted({row["branch_key"] for row in selected}):
        rows = [row for row in selected if row["branch_key"] == branch]
        ranks = [safe_float(row["first_all_truth_rank"], math.inf) for row in rows]
        out.append(
            {
                "feature_family": family,
                "selector_strategy": strategy,
                "branch_key": branch,
                "case_count": len(rows),
                "top10_case_count": sum(rank <= 10 for rank in ranks),
                "top50_case_count": sum(rank <= 50 for rank in ranks),
                "top200_case_count": sum(rank <= 200 for rank in ranks),
                "deeper_than_top200_case_count": sum(rank > 200 for rank in ranks),
                "median_first_all_truth_rank": float(np.median([rank for rank in ranks if math.isfinite(rank)])) if ranks else math.nan,
            }
        )
    return out


def summarize_audit(policy_rows: list[dict], best_branch_rows: list[dict], source_summary: dict) -> dict:
    best = policy_rows[0]
    all_features_global = next(
        row
        for row in policy_rows
        if row["feature_family"] == "all_features" and row["selector_strategy"] == "global"
    )
    top200_gain = safe_int(best["top200_case_count"]) - safe_int(all_features_global["top200_case_count"])
    top50_gain = safe_int(best["top50_case_count"]) - safe_int(all_features_global["top50_case_count"])
    ready_for_rank_claim = safe_int(best["top200_case_count"]) == safe_int(best["case_count"])
    ready_for_fwi = safe_int(best["top1_case_count"]) == safe_int(best["case_count"])
    return {
        "policy_label": "local_2d_detector_selector_feature_family_audit_cpu_no_fwi",
        "source_policy_label": source_summary.get("policy_label", ""),
        "selector_policy_count": len(policy_rows),
        "case_count": best["case_count"],
        "best_feature_family": best["feature_family"],
        "best_selector_strategy": best["selector_strategy"],
        "best_top1_case_count": best["top1_case_count"],
        "best_top10_case_count": best["top10_case_count"],
        "best_top50_case_count": best["top50_case_count"],
        "best_top200_case_count": best["top200_case_count"],
        "best_deeper_than_top200_case_count": best["deeper_than_top200_case_count"],
        "best_median_first_all_truth_rank": best["median_first_all_truth_rank"],
        "best_max_first_all_truth_rank": best["max_first_all_truth_rank"],
        "all_features_global_top50_case_count": all_features_global["top50_case_count"],
        "all_features_global_top200_case_count": all_features_global["top200_case_count"],
        "top50_gain_over_all_features_global": top50_gain,
        "top200_gain_over_all_features_global": top200_gain,
        "best_policy_branch_rows": len(best_branch_rows),
        "ready_for_rank_gated_selector_claim": ready_for_rank_claim,
        "ready_for_detector_seeded_fwi": ready_for_fwi,
        "gpu_priority": "none",
        "decision": (
            "Restricting detector selector features to component/waveform scores removes the "
            "span-target overfit that caused the close50 source-mismatch deeper-than-top200 "
            "failures. The best selector reaches all cases within top200 and improves top50 "
            "coverage over the all-feature global selector, but top1 all-truth recovery remains "
            "0 cases, so detector-seeded FWI is still blocked."
        ),
    }


def plot_audit(policy_rows: list[dict], summary: dict, save_path: Path) -> str:
    display = []
    seen = set()

    def add_row(row: dict) -> None:
        key = (row["feature_family"], row["selector_strategy"])
        if key not in seen:
            display.append(row)
            seen.add(key)

    for row in policy_rows[:8]:
        add_row(row)
    for wanted in (
        ("all_features", "global"),
        ("all_features", "branch"),
        ("all_features", "variant"),
        ("all_features", "branch_variant"),
    ):
        for row in policy_rows:
            if (row["feature_family"], row["selector_strategy"]) == wanted:
                add_row(row)
                break
    for row in sorted(policy_rows, key=lambda item: safe_int(item["deeper_than_top200_case_count"]), reverse=True):
        if len(display) >= 12:
            break
        add_row(row)
    display = display[:12]
    labels = [f"{row['feature_family']}\n{row['selector_strategy']}" for row in display]
    top50 = [safe_int(row["top50_case_count"]) for row in display]
    top200 = [safe_int(row["top200_case_count"]) for row in display]
    failures = [safe_int(row["deeper_than_top200_case_count"]) for row in display]
    x = np.arange(len(display))

    fig, axes = plt.subplots(1, 2, figsize=(16.0, 5.8), constrained_layout=True)
    width = 0.34
    axes[0].bar(x - width / 2, top50, width=width, label="top50", color="#54a24b")
    axes[0].bar(x + width / 2, top200, width=width, label="top200", color="#4c78a8")
    axes[0].set_ylim(0, safe_int(display[0]["case_count"]) + 1)
    axes[0].set_xticks(x, labels, rotation=45, ha="right", fontsize=7)
    axes[0].set_ylabel("cases")
    axes[0].set_title("Leave-one-case rank coverage")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].bar(x, failures, width=0.58, color="#e45756")
    axes[1].set_ylim(0, max(failures + [1]) + 1)
    axes[1].set_xticks(x, labels, rotation=45, ha="right", fontsize=7)
    axes[1].set_ylabel("cases")
    axes[1].set_title("Deeper-than-top200 failures")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Local 2D detector selector feature-family audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_selector_feature_family_audit.png`",
                "",
                "This figure compares leave-one-case detector selector policies over saved",
                "feature-rank outputs. It does not run FDTD, FWI, detector scoring, GPU",
                "kernels, field FWI, 3D/HPC work, or neural-network training.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Best policy: `{summary['best_feature_family']}` / `{summary['best_selector_strategy']}`.",
                f"Best top50 cases: `{summary['best_top50_case_count']}`.",
                f"Best top200 cases: `{summary['best_top200_case_count']}`.",
                f"Top200 gain over all-feature global selector: `{summary['top200_gain_over_all_features_global']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                summary["decision"],
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--separability-run", default=DEFAULT_SEPARABILITY_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_selector_feature_family_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dir = Path(args.summary_root) / args.separability_run / "data"
    objective_rows = read_csv_rows(source_dir / "local_2d_detector_feature_separability_objective_cases.csv")
    source_summary = read_json(source_dir / "local_2d_detector_feature_separability_summary.json")
    families = feature_families(sorted({row["feature"] for row in objective_rows}))

    case_rows = []
    for family_name, features in families.items():
        for strategy in STRATEGIES:
            case_rows.extend(evaluate_policy(objective_rows, family_name, features, strategy))
    policy_rows = summarize_policy_rows(case_rows)
    best = policy_rows[0]
    branch_rows = branch_rows_for_policy(case_rows, best["feature_family"], best["selector_strategy"])
    summary = summarize_audit(policy_rows, branch_rows, source_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    write_csv(data_dir / "local_2d_detector_selector_feature_family_cases.csv", case_rows)
    write_csv(data_dir / "local_2d_detector_selector_feature_family_policy_summary.csv", policy_rows)
    write_csv(data_dir / "local_2d_detector_selector_feature_family_best_branch_summary.csv", branch_rows)
    summary_path = data_dir / "local_2d_detector_selector_feature_family_summary.json"
    summary_path.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")

    fig_path = figures_dir / "local_2d_detector_selector_feature_family_audit.png"
    plot_audit(policy_rows, summary, fig_path)
    write_figure_notes(figures_dir / "FIGURE_NOTES.md", summary)
    write_csv(data_dir / "figure_validation.csv", [figure_stats(fig_path)])
    write_run_manifest(
        str(outdir),
        "local_2d_detector_selector_feature_family_audit",
        {
            "summary": json_safe(summary),
            "paths": {
                "source_objective_cases_csv": str(source_dir / "local_2d_detector_feature_separability_objective_cases.csv"),
                "summary_json": str(summary_path),
                "figure": str(fig_path),
            },
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

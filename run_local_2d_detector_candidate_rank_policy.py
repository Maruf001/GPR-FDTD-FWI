#!/usr/bin/env python3
"""Synthesize top-N candidate-rank policy from saved local 2D detector sensitivity rows."""

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
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SENSITIVITY_RUN = "020_local_2d_detector_parameter_sensitivity_post_rank_depth_metrics"
RANK_CAPS = (3, 5, 10, 20, 40, 80)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def rank_values(value) -> list[int]:
    if value in (None, ""):
        return []
    return [int(part) for part in str(value).split(",") if part.strip()]


def max_rank(row: dict) -> float:
    ranks = rank_values(row.get("assigned_candidate_ranks"))
    return float(max(ranks)) if ranks else math.nan


def row_recovered_within_cap(row: dict, cap: int) -> bool:
    rank = max_rank(row)
    return parse_bool(row.get("unique_all_truths_within_tolerance")) and math.isfinite(rank) and rank <= int(cap)


def summarize_by_config(rows: list[dict], rank_caps: tuple[int, ...] = RANK_CAPS) -> list[dict]:
    case_count = len({(row["branch_key"], row["seed"], row["case_variant"], row["run_name"]) for row in rows})
    out = []
    for config_key in sorted({row["config_key"] for row in rows}):
        cfg_rows = [row for row in rows if row["config_key"] == config_key]
        first = cfg_rows[0]
        full_ranks = [
            max_rank(row)
            for row in cfg_rows
            if parse_bool(row.get("unique_all_truths_within_tolerance")) and math.isfinite(max_rank(row))
        ]
        row = {
            "config_key": config_key,
            "background_mode": first["background_mode"],
            "top_k": int(first["top_k"]),
            "separation_profile": first["separation_profile"],
            "time_offset_family": first["time_offset_family"],
            "case_count": len(cfg_rows),
            "unique_all_truth_case_count": len(full_ranks),
            "mean_max_assigned_rank": float(np.mean(full_ranks)) if full_ranks else math.nan,
            "worst_max_assigned_rank": float(np.max(full_ranks)) if full_ranks else math.nan,
            "min_rank_cap_for_all_cases": "",
        }
        for cap in rank_caps:
            count = sum(row_recovered_within_cap(candidate_row, cap) for candidate_row in cfg_rows)
            row[f"all_truth_within_top{cap}_case_count"] = int(count)
            if count == case_count and row["min_rank_cap_for_all_cases"] == "":
                row["min_rank_cap_for_all_cases"] = int(cap)
        out.append(row)
    return sorted(
        out,
        key=lambda row: (
            row["min_rank_cap_for_all_cases"] == "",
            int(row["min_rank_cap_for_all_cases"] or 10_000),
            -int(row["unique_all_truth_case_count"]),
            float(row["mean_max_assigned_rank"]) if math.isfinite(float(row["mean_max_assigned_rank"])) else 10_000.0,
            str(row["config_key"]),
        ),
    )


def summarize_by_branch(rows: list[dict], rank_caps: tuple[int, ...] = RANK_CAPS) -> list[dict]:
    out = []
    for branch in sorted({row["branch_key"] for row in rows}):
        branch_rows = [row for row in rows if row["branch_key"] == branch]
        case_count = len({(row["seed"], row["case_variant"], row["run_name"]) for row in branch_rows})
        row = {"branch_key": branch, "case_count": case_count}
        for cap in rank_caps:
            best_count = 0
            best_config = ""
            for config_key in sorted({item["config_key"] for item in branch_rows}):
                cfg_rows = [item for item in branch_rows if item["config_key"] == config_key]
                count = sum(row_recovered_within_cap(item, cap) for item in cfg_rows)
                if count > best_count:
                    best_count = int(count)
                    best_config = config_key
            row[f"best_top{cap}_case_count"] = best_count
            row[f"best_top{cap}_config_key"] = best_config
        out.append(row)
    return out


def summarize(rows: list[dict], config_rows: list[dict], branch_rows: list[dict], rank_caps: tuple[int, ...]) -> dict:
    case_count = len({(row["branch_key"], row["seed"], row["case_variant"], row["run_name"]) for row in rows})
    config_count = len(config_rows)
    full_case_configs = [row for row in config_rows if int(row["unique_all_truth_case_count"]) == case_count]
    minimal_full_cap = min(
        (int(row["min_rank_cap_for_all_cases"]) for row in full_case_configs if row["min_rank_cap_for_all_cases"] != ""),
        default=None,
    )
    best_by_cap = {
        f"top{cap}": max((int(row[f"all_truth_within_top{cap}_case_count"]) for row in config_rows), default=0)
        for cap in rank_caps
    }
    config_count_by_cap = {
        f"top{cap}": sum(int(row[f"all_truth_within_top{cap}_case_count"]) == case_count for row in config_rows)
        for cap in rank_caps
    }
    if minimal_full_cap is None:
        decision = (
            "No detector configuration recovers all cases within the tested top-N budgets. "
            "Treat detector candidates as partial seed evidence only."
        )
    elif minimal_full_cap <= 10:
        decision = (
            "All cases are recoverable with a shallow candidate budget. A detector-to-assignment "
            "pilot is a plausible next local 2D step."
        )
    else:
        decision = (
            "All cases are recoverable only with a deeper candidate budget. Use the detector as a "
            "truth-containing candidate generator, and gate any detector-to-FWI pilot by rank/cost."
        )
    return {
        "policy_label": "local_2d_detector_candidate_rank_policy_saved_bscan_cpu",
        "case_count": case_count,
        "config_count": config_count,
        "rank_caps": list(rank_caps),
        "config_with_full_case_recovery_count": len(full_case_configs),
        "minimal_rank_cap_for_full_case_recovery": minimal_full_cap,
        "best_config_key": config_rows[0]["config_key"] if config_rows else "",
        "best_config_min_rank_cap_for_all_cases": config_rows[0]["min_rank_cap_for_all_cases"] if config_rows else "",
        "best_config_mean_max_assigned_rank": config_rows[0]["mean_max_assigned_rank"] if config_rows else math.nan,
        "best_config_worst_max_assigned_rank": config_rows[0]["worst_max_assigned_rank"] if config_rows else math.nan,
        "best_case_count_by_rank_cap": best_by_cap,
        "full_recovery_config_count_by_rank_cap": config_count_by_cap,
        "branch_row_count": len(branch_rows),
        "gpu_used": False,
        "backend": "saved_bscan_cpu_policy_synthesis",
        "decision": decision,
    }


def plot_policy(config_rows: list[dict], branch_rows: list[dict], summary: dict, save_path: Path) -> str:
    rank_caps = summary["rank_caps"]
    best_counts = [summary["best_case_count_by_rank_cap"][f"top{cap}"] for cap in rank_caps]
    full_config_counts = [summary["full_recovery_config_count_by_rank_cap"][f"top{cap}"] for cap in rank_caps]

    fig, axes = plt.subplots(1, 2, figsize=(14.5, 5.2), constrained_layout=True)
    x = np.arange(len(rank_caps))
    axes[0].plot(x, best_counts, marker="o", linewidth=2.0, color="#4c78a8", label="best case count")
    axes[0].bar(x, full_config_counts, width=0.45, color="#72b7b2", alpha=0.65, label="full-recovery configs")
    axes[0].set_xticks(x, [f"top {cap}" for cap in rank_caps])
    axes[0].set_ylim(0, max(summary["case_count"], max(full_config_counts, default=0)) + 1)
    axes[0].set_ylabel("count")
    axes[0].set_title("Candidate-rank budget")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    cap_for_branches = int(summary["minimal_rank_cap_for_full_case_recovery"] or rank_caps[-1])
    branches = [row["branch_key"] for row in branch_rows]
    branch_values = [row[f"best_top{cap_for_branches}_case_count"] for row in branch_rows]
    axes[1].bar(np.arange(len(branches)), branch_values, color="#59a14f", width=0.58)
    axes[1].set_xticks(np.arange(len(branches)), [branch.replace("_", "\n") for branch in branches], fontsize=8)
    axes[1].set_ylim(0, max([row["case_count"] for row in branch_rows] + [1]) + 1)
    axes[1].set_title(f"Branch recovery at top {cap_for_branches}")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Local 2D detector candidate-rank policy", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_candidate_rank_policy.png`",
                "",
                "This figure summarizes top-N candidate-rank requirements from saved",
                "detector sensitivity rows. It does not rerun FDTD, FWI, GPU kernels,",
                "field FWI, or 3D/HPC work.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Cases: `{summary['case_count']}`.",
                f"Configurations: `{summary['config_count']}`.",
                f"Minimal rank cap for full recovery: `{summary['minimal_rank_cap_for_full_case_recovery']}`.",
                f"Best config: `{summary['best_config_key']}`.",
                f"Best-config mean max assigned rank: `{summary['best_config_mean_max_assigned_rank']}`.",
                f"Best-config worst max assigned rank: `{summary['best_config_worst_max_assigned_rank']}`.",
                f"GPU used: `{summary['gpu_used']}`.",
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
    parser.add_argument("--sensitivity-run", default=DEFAULT_SENSITIVITY_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_candidate_rank_policy")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sensitivity_dir = Path(args.summary_root) / args.sensitivity_run
    rows = read_csv_rows(sensitivity_dir / "data/local_2d_detector_parameter_sensitivity_rows.csv")
    config_summary = summarize_by_config(rows)
    branch_summary = summarize_by_branch(rows)
    summary = summarize(rows, config_summary, branch_summary, RANK_CAPS)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    config_csv = data_dir / "local_2d_detector_candidate_rank_policy_config_summary.csv"
    branch_csv = data_dir / "local_2d_detector_candidate_rank_policy_branch_summary.csv"
    summary_json = data_dir / "local_2d_detector_candidate_rank_policy_summary.json"
    figure_path = figures_dir / "local_2d_detector_candidate_rank_policy.png"
    validation_csv = data_dir / "figure_validation.csv"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(config_csv, [json_safe(row) for row in config_summary])
    write_csv(branch_csv, [json_safe(row) for row in branch_summary])
    plot_policy(config_summary, branch_summary, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "config_csv": str(config_csv),
        "branch_csv": str(branch_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_candidate_rank_policy",
        {
            "sensitivity_run": args.sensitivity_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

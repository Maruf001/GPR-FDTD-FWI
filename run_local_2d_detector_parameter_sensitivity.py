#!/usr/bin/env python3
"""Run CPU-only parameter sensitivity on saved local 2D detector B-scans."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
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
from inversion.rebar_detection import detect_rebar_candidates  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_baseline_synthesis import unique_truth_assignment  # noqa: E402
from run_rebar_detection_pipeline import parse_mm_range, truth_match_metrics  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_COMMAND_PLAN_RUN = "017_local_2d_detector_baseline_command_plan_post_interface_patch"

BACKGROUND_MODES = ("none", "mean", "median")
TOP_K_VALUES = (20, 40, 80)
SEPARATION_PROFILES = (
    ("dense4", 4.0, 4.0),
    ("moderate12", 12.0, 8.0),
    ("distinct20", 20.0, 10.0),
)
TIME_OFFSET_FAMILIES = (
    ("single667", (667.0,)),
    ("baseline", (500.0, 550.0, 600.0, 650.0, 667.0, 700.0, 750.0)),
    ("wide", (350.0, 400.0, 450.0, 500.0, 550.0, 600.0, 650.0, 700.0, 750.0, 800.0, 850.0)),
)


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value in (None, ""):
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def assigned_rank_values(value) -> list[int]:
    if value in (None, ""):
        return []
    if isinstance(value, (list, tuple)):
        return [int(rank) for rank in value]
    return [int(part) for part in str(value).split(",") if part.strip()]


def max_assigned_rank(row: dict) -> float:
    ranks = assigned_rank_values(row.get("assigned_candidate_ranks"))
    return float(max(ranks)) if ranks else math.nan


def assigned_rank_preference(row: dict) -> float:
    rank = max_assigned_rank(row)
    return -rank if math.isfinite(rank) else -1_000_000.0


def config_rows() -> list[dict]:
    rows = []
    for background_mode in BACKGROUND_MODES:
        for top_k in TOP_K_VALUES:
            for sep_label, x_sep, z_sep in SEPARATION_PROFILES:
                for offset_label, offsets_ps in TIME_OFFSET_FAMILIES:
                    rows.append({
                        "config_key": f"{background_mode}_top{top_k}_{sep_label}_{offset_label}",
                        "background_mode": background_mode,
                        "top_k": int(top_k),
                        "separation_profile": sep_label,
                        "x_min_separation_mm": float(x_sep),
                        "z_min_separation_mm": float(z_sep),
                        "time_offset_family": offset_label,
                        "time_offsets_ps": ",".join(f"{value:g}" for value in offsets_ps),
                        "time_offsets_s": [float(value) * 1e-12 for value in offsets_ps],
                    })
    return rows


def detection_npz_path(plan_row: dict) -> Path:
    return Path(plan_row["existing_output_dir"]) / "data" / "detection_bscan.npz"


def run_loaded_case_config(
    plan_row: dict,
    config: dict,
    observed: np.ndarray,
    scan_x: np.ndarray,
    time_values: np.ndarray,
    truth_x: list[float],
    truth_z: list[float],
) -> dict:
    started = time.time()
    candidates = detect_rebar_candidates(
        observed,
        scan_x,
        time_values,
        x_values_mm=parse_mm_range(plan_row["detector_x_values_mm"]),
        z_values_mm=parse_mm_range(plan_row["detector_z_values_mm"]),
        top_k=int(config["top_k"]),
        background_mode=config["background_mode"],
        x_min_separation_mm=float(config["x_min_separation_mm"]),
        z_min_separation_mm=float(config["z_min_separation_mm"]),
        tx_rx_offset=float(plan_row["tx_rx_offset_mm"]) / 1000.0,
        time_offsets_s=config["time_offsets_s"],
    )
    metrics = truth_match_metrics(
        candidates,
        truth_x,
        truth_z,
        safe_float(plan_row["truth_tolerance_mm"], 8.0),
        safe_float(plan_row["truth_tolerance_mm"], 8.0),
    )
    truth_hits = [bool(metric["within_tolerance"]) for metric in metrics]
    unique_assignment = unique_truth_assignment(candidates, metrics)
    unique_hits = unique_assignment["unique_truth_hits"]
    best = candidates[0].as_mm() if candidates else {}
    return {
        "branch_key": plan_row["branch_key"],
        "seed": int(plan_row["seed"]),
        "case_variant": plan_row["case_variant"],
        "run_name": plan_row["run_name"],
        "config_key": config["config_key"],
        "background_mode": config["background_mode"],
        "top_k": int(config["top_k"]),
        "separation_profile": config["separation_profile"],
        "time_offset_family": config["time_offset_family"],
        "x_min_separation_mm": float(config["x_min_separation_mm"]),
        "z_min_separation_mm": float(config["z_min_separation_mm"]),
        "detected_candidate_count": len(candidates),
        "all_truths_within_tolerance": all(truth_hits),
        "truth_hit_count": sum(truth_hits),
        "target0_hit": truth_hits[0] if len(truth_hits) > 0 else False,
        "target1_hit": truth_hits[1] if len(truth_hits) > 1 else False,
        "target2_hit": truth_hits[2] if len(truth_hits) > 2 else False,
        "unique_truth_hit_count": unique_assignment["unique_truth_hit_count"],
        "unique_all_truths_within_tolerance": unique_assignment["unique_truth_hit_count"] == len(metrics),
        "unique_target0_hit": unique_hits[0] if len(unique_hits) > 0 else False,
        "unique_target1_hit": unique_hits[1] if len(unique_hits) > 1 else False,
        "unique_target2_hit": unique_hits[2] if len(unique_hits) > 2 else False,
        "assigned_candidate_ranks": ",".join(str(rank) for rank in unique_assignment["assigned_candidate_ranks"]),
        "best_candidate_x_mm": safe_float(best.get("x_mm")),
        "best_candidate_z_mm": safe_float(best.get("z_mm")),
        "best_candidate_score": safe_float(best.get("normalized_score")),
        "elapsed_time_s": float(time.time() - started),
    }


def run_case_config(plan_row: dict, config: dict) -> dict:
    with np.load(detection_npz_path(plan_row)) as npz:
        observed = np.asarray(npz["observed_bscan"], dtype=np.float64)
        scan_x = np.asarray(npz["scan_x"], dtype=np.float64)
        time_values = np.asarray(npz["time"], dtype=np.float64)
        truth_x = [float(value) for value in npz["truth_x_values_mm"]]
        truth_z = [float(value) for value in npz["truth_z_values_mm"]]
    return run_loaded_case_config(plan_row, config, observed, scan_x, time_values, truth_x, truth_z)


def run_case_configs(plan_row: dict, configs: list[dict]) -> list[dict]:
    with np.load(detection_npz_path(plan_row)) as npz:
        observed = np.asarray(npz["observed_bscan"], dtype=np.float64)
        scan_x = np.asarray(npz["scan_x"], dtype=np.float64)
        time_values = np.asarray(npz["time"], dtype=np.float64)
        truth_x = [float(value) for value in npz["truth_x_values_mm"]]
        truth_z = [float(value) for value in npz["truth_z_values_mm"]]
    return [
        run_loaded_case_config(plan_row, config, observed, scan_x, time_values, truth_x, truth_z)
        for config in configs
    ]


def sort_rows(rows: list[dict]) -> list[dict]:
    return sorted(
        rows,
        key=lambda row: (
            str(row["branch_key"]),
            int(row["seed"]),
            str(row["case_variant"]),
            str(row["run_name"]),
            str(row["config_key"]),
        ),
    )


def summarize_by_config(rows: list[dict]) -> list[dict]:
    out = []
    for config_key in sorted({row["config_key"] for row in rows}):
        cfg_rows = [row for row in rows if row["config_key"] == config_key]
        first = cfg_rows[0]
        assigned_rank_maxima = []
        for row in cfg_rows:
            rank = max_assigned_rank(row)
            if bool(row["unique_all_truths_within_tolerance"]) and math.isfinite(rank):
                assigned_rank_maxima.append(rank)
        out.append({
            "config_key": config_key,
            "background_mode": first["background_mode"],
            "top_k": first["top_k"],
            "separation_profile": first["separation_profile"],
            "time_offset_family": first["time_offset_family"],
            "case_count": len(cfg_rows),
            "all_truth_case_count": sum(bool(row["all_truths_within_tolerance"]) for row in cfg_rows),
            "unique_all_truth_case_count": sum(bool(row["unique_all_truths_within_tolerance"]) for row in cfg_rows),
            "target0_hit_count": sum(bool(row["target0_hit"]) for row in cfg_rows),
            "target1_hit_count": sum(bool(row["target1_hit"]) for row in cfg_rows),
            "target2_hit_count": sum(bool(row["target2_hit"]) for row in cfg_rows),
            "unique_target0_hit_count": sum(bool(row["unique_target0_hit"]) for row in cfg_rows),
            "unique_target1_hit_count": sum(bool(row["unique_target1_hit"]) for row in cfg_rows),
            "unique_target2_hit_count": sum(bool(row["unique_target2_hit"]) for row in cfg_rows),
            "mean_unique_truth_hit_count": float(np.mean([row["unique_truth_hit_count"] for row in cfg_rows])),
            "mean_max_assigned_rank": float(np.mean(assigned_rank_maxima)) if assigned_rank_maxima else math.nan,
            "max_assigned_rank": float(np.max(assigned_rank_maxima)) if assigned_rank_maxima else math.nan,
            "mean_elapsed_time_s": float(np.mean([row["elapsed_time_s"] for row in cfg_rows])),
        })
    return sorted(
        out,
        key=lambda row: (
            -int(row["unique_all_truth_case_count"]),
            -float(row["mean_unique_truth_hit_count"]),
            -int(row["unique_target0_hit_count"]),
            str(row["config_key"]),
        ),
    )


def summarize_by_case(rows: list[dict]) -> list[dict]:
    out = []
    for case_key in sorted({(row["branch_key"], row["seed"], row["case_variant"], row["run_name"]) for row in rows}):
        branch, seed, case_variant, run_name = case_key
        case_rows = [
            row
            for row in rows
            if row["branch_key"] == branch and row["seed"] == seed and row["case_variant"] == case_variant
            and row["run_name"] == run_name
        ]
        best = max(
            case_rows,
            key=lambda row: (
                int(row["unique_all_truths_within_tolerance"]),
                int(row["unique_truth_hit_count"]),
                int(row["unique_target0_hit"]),
                int(row["unique_target2_hit"]),
                assigned_rank_preference(row),
                float(row["best_candidate_score"]),
            ),
        )
        out.append({
            "branch_key": branch,
            "seed": int(seed),
            "case_variant": case_variant,
            "run_name": run_name,
            "best_config_key": best["config_key"],
            "best_unique_truth_hit_count": best["unique_truth_hit_count"],
            "best_unique_all_truths_within_tolerance": best["unique_all_truths_within_tolerance"],
            "best_unique_target0_hit": best["unique_target0_hit"],
            "best_unique_target1_hit": best["unique_target1_hit"],
            "best_unique_target2_hit": best["unique_target2_hit"],
            "best_assigned_candidate_ranks": best["assigned_candidate_ranks"],
            "best_max_assigned_rank": max_assigned_rank(best),
        })
    return out


def summarize(rows: list[dict], config_summary: list[dict], case_summary: list[dict]) -> dict:
    case_count = len(case_summary)
    rescued_cases = sum(bool(row["best_unique_all_truths_within_tolerance"]) for row in case_summary)
    best_config = config_summary[0] if config_summary else {}
    if rescued_cases == case_count and case_count:
        decision = (
            "Saved-B-scan detector sensitivity recovered all truths in every case for at least one "
            "configuration, so the earlier negative detector baseline is a parameter-setting artifact. "
            "Because some recoveries require deeper candidate ranks, this is candidate-list recoverability, "
            "not yet a clean standalone top-pick detector result."
        )
    elif rescued_cases:
        decision = (
            "Saved-B-scan detector sensitivity recovered a subset of cases. The detector family has useful "
            "candidate-list signal, but unresolved cases still need either a better scorer or FWI refinement."
        )
    else:
        decision = (
            "Saved-B-scan detector sensitivity did not rescue any cases, so the simple-detector baseline "
            "should remain framed as weak and under-resolving."
        )
    return {
        "policy_label": "local_2d_detector_parameter_sensitivity_saved_bscan_cpu",
        "config_count": len(config_summary),
        "case_count": case_count,
        "case_config_row_count": len(rows),
        "rescued_case_count": rescued_cases,
        "rescued_case_fraction": rescued_cases / case_count if case_count else 0.0,
        "best_config_key": best_config.get("config_key", ""),
        "best_config_unique_all_truth_case_count": best_config.get("unique_all_truth_case_count", 0),
        "best_config_mean_unique_truth_hit_count": best_config.get("mean_unique_truth_hit_count", 0.0),
        "best_config_mean_max_assigned_rank": best_config.get("mean_max_assigned_rank", math.nan),
        "best_config_max_assigned_rank": best_config.get("max_assigned_rank", math.nan),
        "any_config_target0_case_count": sum(bool(row["best_unique_target0_hit"]) for row in case_summary),
        "any_config_target2_case_count": sum(bool(row["best_unique_target2_hit"]) for row in case_summary),
        "gpu_used": False,
        "backend": "saved_bscan_cpu_rescore",
        "decision": decision,
    }


def plot_sensitivity(config_summary: list[dict], case_summary: list[dict], summary: dict, save_path: Path) -> str:
    top = config_summary[:12]
    labels = [row["config_key"].replace("_", "\n") for row in top]
    values = [row["mean_unique_truth_hit_count"] for row in top]

    fig, axes = plt.subplots(1, 2, figsize=(15.5, 5.2), constrained_layout=True)
    x = np.arange(len(top))
    axes[0].bar(x, values, color="#4c78a8", edgecolor="#333333", linewidth=0.5)
    axes[0].set_xticks(x, labels, fontsize=7)
    axes[0].set_ylabel("mean unique truth hits per case")
    axes[0].set_title("Best detector parameter configurations")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    branches = sorted({row["branch_key"] for row in case_summary})
    rescued = [
        sum(row["branch_key"] == branch and bool(row["best_unique_all_truths_within_tolerance"]) for row in case_summary)
        for branch in branches
    ]
    target0 = [
        sum(row["branch_key"] == branch and bool(row["best_unique_target0_hit"]) for row in case_summary)
        for branch in branches
    ]
    target2 = [
        sum(row["branch_key"] == branch and bool(row["best_unique_target2_hit"]) for row in case_summary)
        for branch in branches
    ]
    bx = np.arange(len(branches))
    width = 0.24
    axes[1].bar(bx - width, rescued, width=width, label="all truth")
    axes[1].bar(bx, target0, width=width, label="target0")
    axes[1].bar(bx + width, target2, width=width, label="target2")
    axes[1].set_xticks(bx, [branch.replace("_", "\n") for branch in branches], fontsize=8)
    axes[1].set_title("Best available case recovery across configs")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)

    fig.suptitle("Local 2D detector parameter sensitivity: saved-B-scan CPU rescore", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, config_csv: Path, case_csv: Path, summary_json: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_parameter_sensitivity.png`",
                "",
                "This figure summarizes CPU-only detector rescoring over saved B-scans from",
                "the same-case close14/close50 detector baseline. It does not rerun FDTD, FWI,",
                "GPU kernels, field FWI, or 3D/HPC work.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Configurations: `{summary['config_count']}`.",
                f"Case/config rows: `{summary['case_config_row_count']}`.",
                f"Rescued cases: `{summary['rescued_case_count']}`.",
                f"Best config: `{summary['best_config_key']}`.",
                f"Best-config mean max assigned rank: `{summary['best_config_mean_max_assigned_rank']}`.",
                f"Best-config worst max assigned rank: `{summary['best_config_max_assigned_rank']}`.",
                f"GPU used: `{summary['gpu_used']}`.",
                "",
                summary["decision"],
                "",
                "Outputs:",
                "",
                f"- Case/config rows: `{rows_csv.name}`.",
                f"- Config summary: `{config_csv.name}`.",
                f"- Case summary: `{case_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--command-plan-run", default=DEFAULT_COMMAND_PLAN_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_parameter_sensitivity")
    parser.add_argument("--outdir", default=None)
    parser.add_argument("--workers", type=int, default=4)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    plan_dir = summary_root / args.command_plan_run
    plan_rows = read_csv_rows(plan_dir / "data/local_2d_detector_baseline_command_plan_rows.csv")
    missing = [row["run_name"] for row in plan_rows if not parse_bool(row.get("skip_existing"))]
    if missing:
        raise RuntimeError(f"saved detector B-scans are missing: {missing}")

    configs = config_rows()
    rows = []
    started = time.time()
    if int(args.workers) <= 1:
        for plan_row in plan_rows:
            rows.extend(run_case_configs(plan_row, configs))
    else:
        with ProcessPoolExecutor(max_workers=int(args.workers)) as executor:
            futures = [executor.submit(run_case_configs, plan_row, configs) for plan_row in plan_rows]
            for future in as_completed(futures):
                rows.extend(future.result())
    rows = sort_rows(rows)

    config_summary = summarize_by_config(rows)
    case_summary = summarize_by_case(rows)
    summary = summarize(rows, config_summary, case_summary)
    summary["elapsed_time_s"] = float(time.time() - started)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_detector_parameter_sensitivity_rows.csv"
    config_csv = data_dir / "local_2d_detector_parameter_sensitivity_config_summary.csv"
    case_csv = data_dir / "local_2d_detector_parameter_sensitivity_case_summary.csv"
    summary_json = data_dir / "local_2d_detector_parameter_sensitivity_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_parameter_sensitivity.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(config_csv, [json_safe(row) for row in config_summary])
    write_csv(case_csv, [json_safe(row) for row in case_summary])
    plot_sensitivity(config_summary, case_summary, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "config_csv": str(config_csv),
        "case_csv": str(case_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, rows_csv, config_csv, case_csv, summary_json)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_parameter_sensitivity",
        {
            "command_plan_run": args.command_plan_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

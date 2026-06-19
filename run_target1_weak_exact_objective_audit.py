#!/usr/bin/env python3
"""Audit target1 weak-but-exact rows against diagnostic objective variants."""

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
from run_coordinate_objective_policy_matrix import figure_stats, objective_sort_key, safe_float  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


OBJECTIVE_LABELS = ("base", "early_high", "highband", "late", "late_high", "veryhigh")
TARGET1_TRUTH = (250.0, 100.0, 6.0)
DEFAULT_SUMMARY_ROOT = Path("outputs/summary_tables/wk03_experiment_700_1259_holistic_evaluation/data")


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def canonical_target1_weak_exact_rows(rows: list[dict]) -> list[dict]:
    out = []
    for row in rows:
        if int(safe_float(row.get("target"), -1)) != 1:
            continue
        if not boolish(row.get("exact_geometry")):
            continue
        if not boolish(row.get("base_margin_is_canonical")):
            continue
        if str(row.get("confidence_label")) != "weak":
            continue
        out.append(row)
    return sorted(out, key=lambda row: int(safe_float(row.get("run_id"), -1)))


def objective_rows_for_runs(rows: list[dict], run_ids: set[int]) -> list[dict]:
    return [
        row for row in rows
        if int(safe_float(row.get("run_id"), -1)) in run_ids
    ]


def objective_is_truth(row: dict) -> bool:
    return (
        math.isclose(safe_float(row.get("best_x_mm")), TARGET1_TRUTH[0], abs_tol=1.0e-9)
        and math.isclose(safe_float(row.get("best_z_mm")), TARGET1_TRUTH[1], abs_tol=1.0e-9)
        and math.isclose(safe_float(row.get("best_radius_mm")), TARGET1_TRUTH[2], abs_tol=1.0e-9)
    )


def base_margin_by_run(weak_rows: list[dict]) -> dict[int, float]:
    return {
        int(safe_float(row["run_id"])): safe_float(row.get("base_margin"))
        for row in weak_rows
    }


def summarize_objectives(weak_rows: list[dict], objective_rows: list[dict], cutoff: float) -> list[dict]:
    base_margins = base_margin_by_run(weak_rows)
    by_objective: dict[str, list[dict]] = defaultdict(list)
    for row in objective_rows:
        by_objective[str(row.get("objective_label", ""))].append(row)

    summaries = []
    for objective in sorted(by_objective, key=objective_sort_key):
        rows = by_objective[objective]
        margins = [safe_float(row.get("objective_margin")) for row in rows]
        finite_margins = [value for value in margins if math.isfinite(value)]
        ratios = []
        for row, margin in zip(rows, margins):
            base = base_margins.get(int(safe_float(row.get("run_id"), -1)), math.nan)
            if math.isfinite(base) and base != 0 and math.isfinite(margin):
                ratios.append(margin / base)
        summaries.append({
            "objective_label": objective,
            "row_count": len(rows),
            "truth_geometry_count": sum(1 for row in rows if objective_is_truth(row)),
            "accepted_count": sum(1 for value in finite_margins if value >= cutoff),
            "accepted_fraction": (
                sum(1 for value in finite_margins if value >= cutoff) / len(rows)
                if rows else math.nan
            ),
            "min_margin": min(finite_margins) if finite_margins else math.nan,
            "mean_margin": float(np.mean(finite_margins)) if finite_margins else math.nan,
            "median_ratio_to_base": float(np.median(ratios)) if ratios else math.nan,
        })
    return summaries


def per_run_objective_rows(weak_rows: list[dict], objective_rows: list[dict], cutoff: float) -> list[dict]:
    by_run_objective: dict[int, dict[str, float]] = defaultdict(dict)
    for row in objective_rows:
        run_id = int(safe_float(row.get("run_id"), -1))
        by_run_objective[run_id][str(row.get("objective_label", ""))] = safe_float(row.get("objective_margin"))

    out = []
    for weak in sorted(weak_rows, key=lambda row: safe_float(row.get("base_margin"))):
        run_id = int(safe_float(weak.get("run_id"), -1))
        margins = by_run_objective.get(run_id, {})
        secondary = {
            label: margins.get(label, math.nan)
            for label in OBJECTIVE_LABELS
            if label != "base"
        }
        best_secondary = max(
            secondary,
            key=lambda label: (
                safe_float(secondary[label], -math.inf),
                -objective_sort_key(label)[0],
            ),
        )
        base = safe_float(weak.get("base_margin"))
        late_high = margins.get("late_high", math.nan)
        out.append({
            "run_id": run_id,
            "seed": int(safe_float(weak.get("seed"), -1)),
            "sources": int(safe_float(weak.get("sources"), -1)),
            "tx_rx_offset_mm": safe_float(weak.get("tx_rx_offset_mm")),
            "ringdown_value": safe_float(weak.get("ringdown_value")),
            "base_margin": base,
            "late_high_margin": late_high,
            "highband_margin": margins.get("highband", math.nan),
            "late_margin": margins.get("late", math.nan),
            "veryhigh_margin": margins.get("veryhigh", math.nan),
            "best_secondary_objective": best_secondary,
            "best_secondary_margin": secondary[best_secondary],
            "late_high_ratio_to_base": late_high / base if math.isfinite(base) and base else math.nan,
            "late_high_clears_cutoff": late_high >= cutoff if math.isfinite(late_high) else False,
            "run_name": weak.get("run_name", ""),
        })
    return out


def _selected_subset(name: str, rows: list[dict]) -> list[dict]:
    if name == "all":
        return rows
    if name == "ringdown050":
        return [row for row in rows if math.isclose(safe_float(row.get("ringdown_value")), 0.5)]
    if name == "ringdown025":
        return [row for row in rows if math.isclose(safe_float(row.get("ringdown_value")), 0.25)]
    if name == "modern_seed610_552":
        return [
            row for row in rows
            if int(safe_float(row.get("seed"), -1)) in {610, 5527939710754757}
        ]
    raise ValueError(f"unknown subset {name!r}")


def subset_policy_rows(per_run_rows: list[dict], cutoff: float) -> list[dict]:
    rows = []
    for subset_name in ("all", "ringdown050", "ringdown025", "modern_seed610_552"):
        subset = _selected_subset(subset_name, per_run_rows)
        row = {
            "subset": subset_name,
            "weak_exact_row_count": len(subset),
        }
        for label in ("base", "highband", "late", "late_high", "veryhigh"):
            margin_key = "base_margin" if label == "base" else f"{label}_margin"
            margins = [safe_float(item.get(margin_key)) for item in subset]
            finite = [value for value in margins if math.isfinite(value)]
            row[f"{label}_accepted_count"] = sum(1 for value in finite if value >= cutoff)
            row[f"{label}_min_margin"] = min(finite) if finite else math.nan
        ratios = [safe_float(item.get("late_high_ratio_to_base")) for item in subset]
        finite_ratios = [value for value in ratios if math.isfinite(value)]
        nonaccepted = [
            str(item["run_id"]) for item in subset
            if not boolish(item.get("late_high_clears_cutoff"))
        ]
        row["late_high_mean_ratio_to_base"] = float(np.mean(finite_ratios)) if finite_ratios else math.nan
        row["late_high_nonaccepted_run_ids"] = ", ".join(nonaccepted) if nonaccepted else ""
        rows.append(row)
    return rows


def audit_decision(subset_rows: list[dict]) -> dict:
    by_subset = {row["subset"]: row for row in subset_rows}
    all_row = by_subset["all"]
    ringdown050 = by_subset["ringdown050"]
    if (
        ringdown050["weak_exact_row_count"] > 0
        and ringdown050["late_high_accepted_count"] == ringdown050["weak_exact_row_count"]
    ):
        label = "target1_ringdown050_latehigh_secondary_confirmed"
    elif all_row["late_high_accepted_count"] == all_row["weak_exact_row_count"]:
        label = "target1_latehigh_secondary_confirmed_all_archive"
    else:
        label = "target1_latehigh_secondary_with_archive_exception"
    return {
        "policy_label": label,
        "decision": (
            "For canonical weak-but-exact target1 rows, late_high is a secondary "
            "confirmation objective, not a replacement for the base production gate. "
            "The ringdown050 subset is fully confirmed by late_high; the full archive "
            "has one legacy ringdown025 exception."
        ),
        "all_weak_exact_rows": all_row["weak_exact_row_count"],
        "all_late_high_accepted_count": all_row["late_high_accepted_count"],
        "ringdown050_weak_exact_rows": ringdown050["weak_exact_row_count"],
        "ringdown050_late_high_accepted_count": ringdown050["late_high_accepted_count"],
        "archive_late_high_exception_run_ids": all_row["late_high_nonaccepted_run_ids"],
    }


def plot_audit(objective_rows: list[dict], per_run_rows: list[dict], save_path: Path) -> str:
    objectives = [row["objective_label"] for row in objective_rows]
    accepted = [safe_float(row["accepted_count"], 0.0) for row in objective_rows]
    total = [safe_float(row["row_count"], 1.0) for row in objective_rows]
    fractions = [acc / max(1.0, count) for acc, count in zip(accepted, total)]

    base = np.asarray([safe_float(row.get("base_margin")) for row in per_run_rows], dtype=np.float64)
    late_high = np.asarray([safe_float(row.get("late_high_margin")) for row in per_run_rows], dtype=np.float64)
    ringdown = np.asarray([safe_float(row.get("ringdown_value")) for row in per_run_rows], dtype=np.float64)
    colors = np.where(np.isclose(ringdown, 0.5), "#4c78a8", "#f58518")

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8), constrained_layout=True)
    x = np.arange(len(objectives))
    axes[0].bar(x, fractions, color="#4c78a8", width=0.6)
    axes[0].set_xticks(x, objectives, rotation=35, ha="right")
    axes[0].set_ylim(0, 1.05)
    axes[0].set_ylabel("accepted fraction")
    axes[0].set_title("Target1 weak-exact rows clearing 5e-4 cutoff")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    for idx, (acc, count) in enumerate(zip(accepted, total)):
        axes[0].text(idx, min(1.02, fractions[idx] + 0.03), f"{int(acc)}/{int(count)}", ha="center", fontsize=8)

    axes[1].scatter(base, late_high, c=colors, s=34, edgecolor="#222222", linewidth=0.3)
    lower = min(float(np.nanmin(base)), float(np.nanmin(late_high)), 3.4e-4)
    upper = max(float(np.nanmax(base)), float(np.nanmax(late_high)), 9.5e-4)
    axes[1].plot([lower, upper], [lower, upper], color="#666666", linestyle="--", linewidth=0.9)
    axes[1].axhline(5.0e-4, color="#c7302b", linestyle=":", linewidth=1.0)
    axes[1].axvline(5.0e-4, color="#c7302b", linestyle=":", linewidth=1.0)
    axes[1].set_xlim(lower, upper)
    axes[1].set_ylim(lower, upper)
    axes[1].set_xlabel("canonical base margin")
    axes[1].set_ylabel("late_high margin")
    axes[1].set_title("Late_high lifts modern weak target1 rows")
    axes[1].grid(color="#dddddd", linewidth=0.6)

    fig.suptitle("Target1 weak-but-exact objective audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--coordinate-run-summary-csv",
        default=str(DEFAULT_SUMMARY_ROOT / "coordinate_run_summary_700_1259.csv"),
    )
    parser.add_argument(
        "--objective-variant-summary-csv",
        default=str(DEFAULT_SUMMARY_ROOT / "objective_variant_summary_700_1259.csv"),
    )
    parser.add_argument("--cutoff", type=float, default=5.0e-4)
    parser.add_argument("--run-name", default="target1_weak_exact_objective_audit_700_1259")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    coordinate_rows = read_csv_rows(Path(args.coordinate_run_summary_csv))
    objective_rows = read_csv_rows(Path(args.objective_variant_summary_csv))
    weak_rows = canonical_target1_weak_exact_rows(coordinate_rows)
    run_ids = {int(safe_float(row["run_id"])) for row in weak_rows}
    weak_objectives = objective_rows_for_runs(objective_rows, run_ids)
    objective_summaries = summarize_objectives(weak_rows, weak_objectives, args.cutoff)
    per_run_rows = per_run_objective_rows(weak_rows, weak_objectives, args.cutoff)
    subset_rows = subset_policy_rows(per_run_rows, args.cutoff)
    decision = audit_decision(subset_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    weak_rows_csv = data_dir / "target1_weak_exact_runs.csv"
    per_run_csv = data_dir / "target1_weak_exact_objective_per_run.csv"
    objective_csv = data_dir / "target1_weak_exact_objective_summary.csv"
    subset_csv = data_dir / "target1_weak_exact_subset_policy.csv"
    summary_json = data_dir / "target1_weak_exact_objective_audit_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_audit(objective_summaries, per_run_rows, figures_dir / "target1_weak_exact_objective_audit.png"))

    write_csv(weak_rows_csv, [json_safe(row) for row in weak_rows])
    write_csv(per_run_csv, [json_safe(row) for row in per_run_rows])
    write_csv(objective_csv, [json_safe(row) for row in objective_summaries])
    write_csv(subset_csv, [json_safe(row) for row in subset_rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])

    summary = {
        "coordinate_run_summary_csv": args.coordinate_run_summary_csv,
        "objective_variant_summary_csv": args.objective_variant_summary_csv,
        "cutoff": args.cutoff,
        **decision,
        "objective_summary_rows": objective_summaries,
        "subset_policy_rows": subset_rows,
        "paths": {
            "weak_rows_csv": str(weak_rows_csv),
            "per_run_csv": str(per_run_csv),
            "objective_summary_csv": str(objective_csv),
            "subset_policy_csv": str(subset_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "target1_weak_exact_objective_audit",
        {
            "summary_json": str(summary_json),
            "weak_rows_csv": str(weak_rows_csv),
            "per_run_csv": str(per_run_csv),
            "objective_summary_csv": str(objective_csv),
            "subset_policy_csv": str(subset_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

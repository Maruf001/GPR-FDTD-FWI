#!/usr/bin/env python3
"""Build a CPU-only target1 acquisition-confidence surface from archive tables."""

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


DEFAULT_SUMMARY_ROOT = Path("outputs/summary_tables/wk03_experiment_700_1259_holistic_evaluation")
DEFAULT_EXPERIMENT_ROOT = Path("outputs/experiments")
TARGET1_TRUTH = {"x_mm": 250.0, "z_mm": 100.0, "radius_mm": 6.0}
BASE_CUTOFF = 5.0e-4


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def safe_float(value: object, default: float = math.nan) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value: object, default: int = 0) -> int:
    number = safe_float(value)
    if not math.isfinite(number):
        return default
    return int(number)


def is_true(value: object) -> bool:
    return str(value).strip().lower() == "true"


def quantile(values: list[float], q: float) -> float:
    finite = sorted(value for value in values if math.isfinite(value))
    if not finite:
        return math.nan
    return float(np.quantile(finite, q))


def is_target1_truth_objective(row: dict | None) -> bool:
    if row is None:
        return False
    return (
        math.isclose(safe_float(row.get("best_x_mm")), TARGET1_TRUTH["x_mm"], abs_tol=1.0e-9)
        and math.isclose(safe_float(row.get("best_z_mm")), TARGET1_TRUTH["z_mm"], abs_tol=1.0e-9)
        and math.isclose(safe_float(row.get("best_radius_mm")), TARGET1_TRUTH["radius_mm"], abs_tol=1.0e-9)
    )


def canonical_target1_rows(coordinate_rows: list[dict]) -> list[dict]:
    rows = []
    for row in coordinate_rows:
        if safe_int(row.get("target"), -1) != 1:
            continue
        if not is_true(row.get("base_margin_is_canonical")):
            continue
        if not math.isfinite(safe_float(row.get("base_margin"))):
            continue
        rows.append(row)
    return rows


def objective_lookup(objective_rows: list[dict]) -> dict[tuple[int, str], dict]:
    lookup = {}
    for row in objective_rows:
        run_id = safe_int(row.get("run_id"), -1)
        label = str(row.get("objective_label", ""))
        if run_id >= 0 and label:
            lookup[(run_id, label)] = row
    return lookup


def surface_status(row_count: int, accepted_count: int, late_high_accepted_count: int, exact_count: int) -> str:
    if row_count <= 0:
        return "empty"
    if exact_count < row_count:
        return "geometry_failure_present"
    if accepted_count == row_count:
        return "base_accepted_all_exact"
    if late_high_accepted_count == row_count and accepted_count > 0:
        return "mixed_base_secondary_confirms_all"
    if late_high_accepted_count == row_count:
        return "base_weak_secondary_confirms_all"
    return "secondary_exception_present"


def build_surface_rows(
    coordinate_rows: list[dict],
    objective_rows: list[dict],
    group_field: str,
    group_type: str,
) -> list[dict]:
    lookup = objective_lookup(objective_rows)
    grouped: dict[float, list[dict]] = {}
    for row in canonical_target1_rows(coordinate_rows):
        setting = safe_float(row.get(group_field))
        if not math.isfinite(setting):
            continue
        grouped.setdefault(setting, []).append(row)

    out = []
    for setting, rows in sorted(grouped.items()):
        margins = [safe_float(row.get("base_margin")) for row in rows]
        accepted_count = sum(1 for row in rows if safe_float(row.get("base_margin")) >= BASE_CUTOFF)
        weak_exact_count = sum(
            1
            for row in rows
            if safe_float(row.get("base_margin")) < BASE_CUTOFF and is_true(row.get("exact_geometry"))
        )
        exact_count = sum(1 for row in rows if is_true(row.get("exact_geometry")))
        late_high_truth_count = 0
        late_high_accepted_count = 0
        for row in rows:
            objective = lookup.get((safe_int(row.get("run_id"), -1), "late_high"))
            if is_target1_truth_objective(objective):
                late_high_truth_count += 1
                if safe_float(objective.get("objective_margin")) >= BASE_CUTOFF:
                    late_high_accepted_count += 1
        row_count = len(rows)
        out.append({
            "surface_key": f"{group_type}_{setting:g}",
            "group_type": group_type,
            "setting": setting,
            "row_count": row_count,
            "accepted_count": accepted_count,
            "weak_exact_count": weak_exact_count,
            "exact_count": exact_count,
            "accepted_fraction": accepted_count / row_count,
            "weak_exact_fraction": weak_exact_count / row_count,
            "exact_fraction": exact_count / row_count,
            "median_base_margin": quantile(margins, 0.50),
            "q25_base_margin": quantile(margins, 0.25),
            "q75_base_margin": quantile(margins, 0.75),
            "min_base_margin": min(margins),
            "max_base_margin": max(margins),
            "late_high_truth_count": late_high_truth_count,
            "late_high_accepted_count": late_high_accepted_count,
            "late_high_accepted_fraction": late_high_accepted_count / row_count,
            "status": surface_status(row_count, accepted_count, late_high_accepted_count, exact_count),
        })
    return out


def build_source_series_policy_rows(source_series_rows: list[dict]) -> list[dict]:
    out = []
    for row in sorted(source_series_rows, key=lambda item: safe_int(item.get("first_run"))):
        n_runs = safe_int(row.get("n_runs"))
        n_accepted = safe_int(row.get("n_accepted"))
        first_margin = safe_float(row.get("first_margin"))
        last_margin = safe_float(row.get("last_margin"))
        best_margin = safe_float(row.get("best_margin"))
        best_minus_first = safe_float(row.get("best_minus_first_margin"))
        first_setting = safe_float(row.get("first_setting"))
        last_setting = safe_float(row.get("last_setting"))
        best_setting = safe_float(row.get("best_setting"))
        if n_accepted == n_runs:
            status = "all_base_accepted"
        elif n_accepted == 0:
            status = "all_base_weak"
        elif best_minus_first > 0.0:
            status = "source_escalation_helped_one_branch"
        else:
            status = "lower_source_count_was_best"
        out.append({
            "series_id": row.get("series_id", ""),
            "seed": row.get("seed", ""),
            "run_ids": row.get("run_ids", ""),
            "first_run": safe_int(row.get("first_run")),
            "last_run": safe_int(row.get("last_run")),
            "n_runs": n_runs,
            "n_accepted": n_accepted,
            "n_weak": safe_int(row.get("n_weak")),
            "first_setting": first_setting,
            "last_setting": last_setting,
            "best_setting": best_setting,
            "worst_setting": safe_float(row.get("worst_setting")),
            "first_margin": first_margin,
            "last_margin": last_margin,
            "best_margin": best_margin,
            "worst_margin": safe_float(row.get("worst_margin")),
            "best_minus_first_margin": best_minus_first,
            "last_minus_first_margin": last_margin - first_margin,
            "last_worse_than_first": bool(math.isfinite(last_margin) and math.isfinite(first_margin) and last_margin < first_margin),
            "all_exact_geometry": is_true(row.get("all_exact_geometry")),
            "outcome_category": row.get("outcome_category", ""),
            "status": status,
        })
    return out


def best_setting(rows: list[dict], min_run_count: int) -> dict:
    eligible = [row for row in rows if row["row_count"] >= min_run_count]
    if not eligible:
        return {}
    return max(
        eligible,
        key=lambda row: (
            row["accepted_fraction"],
            row["median_base_margin"],
            row["row_count"],
        ),
    )


def summarize(
    surface_rows: list[dict],
    source_series_policy_rows: list[dict],
    coordinate_rows: list[dict],
    objective_rows: list[dict],
) -> dict:
    target_rows = canonical_target1_rows(coordinate_rows)
    lookup = objective_lookup(objective_rows)
    late_high_truth = 0
    late_high_accepted = 0
    for row in target_rows:
        objective = lookup.get((safe_int(row.get("run_id"), -1), "late_high"))
        if is_target1_truth_objective(objective):
            late_high_truth += 1
            if safe_float(objective.get("objective_margin")) >= BASE_CUTOFF:
                late_high_accepted += 1

    source_rows = [row for row in surface_rows if row["group_type"] == "source_count"]
    txrx_rows = [row for row in surface_rows if row["group_type"] == "txrx_offset"]
    source_best = best_setting(source_rows, min_run_count=5)
    txrx_best = best_setting(txrx_rows, min_run_count=3)
    best_source_counts: dict[str, int] = {}
    for row in source_series_policy_rows:
        key = f"{row['best_setting']:g}"
        best_source_counts[key] = best_source_counts.get(key, 0) + 1

    all_weak = sum(1 for row in source_series_policy_rows if row["status"] == "all_base_weak")
    all_accepted = sum(1 for row in source_series_policy_rows if row["status"] == "all_base_accepted")
    escalation_helped = sum(1 for row in source_series_policy_rows if row["best_minus_first_margin"] > 0.0)
    lower_best = sum(1 for row in source_series_policy_rows if row["best_minus_first_margin"] <= 0.0)
    last_worse = sum(1 for row in source_series_policy_rows if row["last_worse_than_first"])
    source11_terminal = sum(1 for row in source_series_policy_rows if math.isclose(row["last_setting"], 11.0))
    source11_terminal_worse = sum(
        1
        for row in source_series_policy_rows
        if math.isclose(row["last_setting"], 11.0) and row["last_worse_than_first"]
    )

    target_row_count = len(target_rows)
    exact_count = sum(1 for row in target_rows if is_true(row.get("exact_geometry")))
    base_accepted = sum(1 for row in target_rows if safe_float(row.get("base_margin")) >= BASE_CUTOFF)
    weak_exact = sum(
        1
        for row in target_rows
        if safe_float(row.get("base_margin")) < BASE_CUTOFF and is_true(row.get("exact_geometry"))
    )
    return {
        "policy_label": "target1_acquisition_confidence_surface_exact_but_nonmonotonic_cpu_no_gpu",
        "target1_canonical_row_count": target_row_count,
        "target1_exact_geometry_count": exact_count,
        "target1_base_accepted_count": base_accepted,
        "target1_base_weak_exact_count": weak_exact,
        "target1_late_high_truth_count": late_high_truth,
        "target1_late_high_accepted_count": late_high_accepted,
        "source_count_setting_count": len(source_rows),
        "txrx_setting_count": len(txrx_rows),
        "best_source_count_setting_min5": source_best.get("setting", math.nan),
        "best_source_count_accepted_fraction_min5": source_best.get("accepted_fraction", math.nan),
        "best_txrx_setting_min3": txrx_best.get("setting", math.nan),
        "best_txrx_accepted_fraction_min3": txrx_best.get("accepted_fraction", math.nan),
        "source_density_series_count": len(source_series_policy_rows),
        "source_density_all_accepted_series_count": all_accepted,
        "source_density_all_weak_series_count": all_weak,
        "source_density_escalation_helped_count": escalation_helped,
        "source_density_lower_count_best_count": lower_best,
        "source_density_last_worse_than_first_count": last_worse,
        "source_density_terminal_11_count": source11_terminal,
        "source_density_terminal_11_worse_count": source11_terminal_worse,
        "source_density_best_setting_counts": best_source_counts,
        "gpu_priority": "none_now",
        "ready_for_manuscript_target1_acquisition_table": True,
        "decision": (
            "Target1 archive rows preserve exact x/z/r geometry, but canonical "
            "base-margin confidence is acquisition-sensitive and source-density "
            "escalation is nonmonotonic. Late_high remains a diagnostic secondary "
            "confirmation for nearly all target1 rows, not a replacement for the "
            "base gate. No broad target1 GPU sweep is justified by this archive "
            "surface."
        ),
    }


def plot_surface(surface_rows: list[dict], source_series_rows: list[dict], save_path: Path) -> None:
    source_rows = [row for row in surface_rows if row["group_type"] == "source_count"]
    txrx_rows = [row for row in surface_rows if row["group_type"] == "txrx_offset"]
    fig, axes = plt.subplots(2, 2, figsize=(15.5, 8.6), constrained_layout=True)

    def grouped_bars(ax, rows, title, xlabel):
        x = np.arange(len(rows))
        width = 0.36
        ax.bar(
            x - width / 2,
            [row["accepted_fraction"] for row in rows],
            width=width,
            color="#4c78a8",
            edgecolor="#333333",
            label="base accepted",
        )
        ax.bar(
            x + width / 2,
            [row["late_high_accepted_fraction"] for row in rows],
            width=width,
            color="#d99a19",
            edgecolor="#333333",
            label="late_high accepted",
        )
        ax.set_xticks(x, [f"{row['setting']:g}" for row in rows])
        ax.set_ylim(0.0, 1.05)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("fraction of target1 rows")
        ax.grid(axis="y", color="#dddddd", linewidth=0.6)
        for idx, row in enumerate(rows):
            ax.text(idx, 1.02, f"n={row['row_count']}", ha="center", va="bottom", fontsize=8)
        ax.legend(loc="lower right", fontsize=8)

    grouped_bars(axes[0, 0], source_rows, "Target1 confidence by source count", "sources")
    grouped_bars(axes[0, 1], txrx_rows, "Target1 confidence by Tx/Rx offset", "Tx/Rx offset (mm)")

    x = np.arange(len(source_rows))
    axes[1, 0].plot(
        x,
        [row["median_base_margin"] for row in source_rows],
        marker="o",
        color="#2f9d55",
        linewidth=2.0,
    )
    axes[1, 0].fill_between(
        x,
        [row["q25_base_margin"] for row in source_rows],
        [row["q75_base_margin"] for row in source_rows],
        color="#2f9d55",
        alpha=0.18,
    )
    axes[1, 0].axhline(BASE_CUTOFF, color="#b23b3b", linestyle="--", linewidth=1.2)
    axes[1, 0].set_xticks(x, [f"{row['setting']:g}" for row in source_rows])
    axes[1, 0].set_title("Median base margin by source count")
    axes[1, 0].set_xlabel("sources")
    axes[1, 0].set_ylabel("canonical base margin")
    axes[1, 0].grid(axis="y", color="#dddddd", linewidth=0.6)

    best_counts: dict[float, int] = {}
    status_counts: dict[str, int] = {}
    for row in source_series_rows:
        best_counts[row["best_setting"]] = best_counts.get(row["best_setting"], 0) + 1
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
    labels = sorted(best_counts)
    axes[1, 1].bar(
        np.arange(len(labels)),
        [best_counts[label] for label in labels],
        color=["#4c78a8" if math.isclose(label, 5.0) else "#d99a19" for label in labels],
        edgecolor="#333333",
    )
    axes[1, 1].set_xticks(np.arange(len(labels)), [f"{label:g} sources" for label in labels])
    axes[1, 1].set_title("Best source setting by target1 branch")
    axes[1, 1].set_ylabel("source-density series")
    axes[1, 1].grid(axis="y", color="#dddddd", linewidth=0.6)
    note = (
        f"all weak: {status_counts.get('all_base_weak', 0)}\n"
        f"all accepted: {status_counts.get('all_base_accepted', 0)}\n"
        f"last source worse: {sum(1 for row in source_series_rows if row['last_worse_than_first'])}"
    )
    axes[1, 1].text(
        0.98,
        0.95,
        note,
        transform=axes[1, 1].transAxes,
        ha="right",
        va="top",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#bbbbbb"},
    )

    fig.suptitle("Target1 acquisition-confidence surface from existing 2D archive", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def load_inputs(summary_root: Path) -> tuple[list[dict], list[dict], list[dict]]:
    data_dir = summary_root / "data"
    return (
        read_csv_rows(data_dir / "coordinate_run_summary_700_1259.csv"),
        read_csv_rows(data_dir / "objective_variant_summary_700_1259.csv"),
        read_csv_rows(data_dir / "target1_source_density_policy_700_1259.csv"),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default=str(DEFAULT_SUMMARY_ROOT))
    parser.add_argument("--experiment-root", default=str(DEFAULT_EXPERIMENT_ROOT))
    parser.add_argument("--run-name", default="target1_acquisition_confidence_surface")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    summary_root = Path(args.summary_root)
    experiment_root = Path(args.experiment_root)
    coordinate_rows, objective_rows, source_series_rows = load_inputs(summary_root)

    surface_rows = (
        build_surface_rows(coordinate_rows, objective_rows, "sources", "source_count")
        + build_surface_rows(coordinate_rows, objective_rows, "tx_rx_offset_mm", "txrx_offset")
    )
    source_policy_rows = build_source_series_policy_rows(source_series_rows)
    summary = summarize(surface_rows, source_policy_rows, coordinate_rows, objective_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(experiment_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    surface_csv = data_dir / "target1_acquisition_confidence_surface.csv"
    source_policy_csv = data_dir / "target1_source_density_branch_policy.csv"
    summary_json = data_dir / "target1_acquisition_confidence_surface_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "target1_acquisition_confidence_surface.png"

    plot_surface(surface_rows, source_policy_rows, figure_path)
    write_csv(surface_csv, [json_safe(row) for row in surface_rows])
    write_csv(source_policy_csv, [json_safe(row) for row in source_policy_rows])
    write_csv(validation_csv, [figure_stats(figure_path)])
    summary["paths"] = {
        "surface_csv": str(surface_csv),
        "source_policy_csv": str(source_policy_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "target1_acquisition_confidence_surface",
        {
            "summary_json": str(summary_json),
            "surface_csv": str(surface_csv),
            "source_policy_csv": str(source_policy_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

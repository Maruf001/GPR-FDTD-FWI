#!/usr/bin/env python3
"""Archive-level objective-policy summary from holistic CSV tables."""

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
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_coordinate_objective_policy_matrix import objective_sort_key, safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_TRUTH = {
    0: (150.0, 80.0, 5.0),
    1: (250.0, 100.0, 6.0),
    2: (350.0, 120.0, 8.0),
}


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def run_is_canonical_primary(row: dict) -> bool:
    value = row.get("base_margin_is_canonical")
    if value in (None, ""):
        return True
    return str(value).strip().lower() not in {"0", "false", "no"}


def filter_noncanonical_primary_rows(
    run_rows: list[dict],
    objective_rows: list[dict],
) -> tuple[list[dict], list[dict], int, int]:
    noncanonical_run_ids = {
        str(row.get("run_id"))
        for row in run_rows
        if not run_is_canonical_primary(row)
    }
    if not noncanonical_run_ids:
        return list(run_rows), list(objective_rows), 0, 0
    canonical_run_rows = [
        row for row in run_rows
        if str(row.get("run_id")) not in noncanonical_run_ids
    ]
    canonical_objective_rows = [
        row for row in objective_rows
        if str(row.get("run_id")) not in noncanonical_run_ids
    ]
    return (
        canonical_run_rows,
        canonical_objective_rows,
        len(run_rows) - len(canonical_run_rows),
        len(objective_rows) - len(canonical_objective_rows),
    )


def geometry_tuple(row: dict) -> tuple[float, float, float]:
    return (
        float(row["best_x_mm"]),
        float(row["best_z_mm"]),
        float(row["best_radius_mm"]),
    )


def target_from_geometry(values: tuple[float, float, float], truth=DEFAULT_TRUTH) -> int | None:
    for target, target_truth in truth.items():
        if all(abs(float(a) - float(b)) <= 1.0e-9 for a, b in zip(values, target_truth)):
            return int(target)
    return None


def assign_objective_rows(run_rows: list[dict], objective_rows: list[dict]) -> list[dict]:
    runs_by_id: dict[str, list[dict]] = defaultdict(list)
    for row in run_rows:
        runs_by_id[str(row["run_id"])].append(row)
    by_run_objective: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in objective_rows:
        by_run_objective[(str(row["run_id"]), str(row["objective_label"]))].append(row)

    assigned: list[dict] = []
    for row in objective_rows:
        run_id = str(row["run_id"])
        base_count = len(by_run_objective[(run_id, "base")])
        run_candidates = runs_by_id.get(run_id, [])
        assigned_target = None
        assignment_method = "unassigned"
        if base_count == 1 and run_candidates:
            assigned_target = int(float(run_candidates[0]["target"]))
            assignment_method = "single_target_run_summary"
        elif base_count > 1:
            assigned_target = target_from_geometry(geometry_tuple(row))
            assignment_method = "multi_target_geometry"
        truth_target = target_from_geometry(geometry_tuple(row))
        assigned.append({
            **row,
            "assigned_target": assigned_target,
            "truth_geometry_target": truth_target,
            "is_truth_geometry_for_assigned_target": (
                bool(assigned_target is not None and truth_target == assigned_target)
            ),
            "assignment_method": assignment_method,
            "base_row_count_for_run": base_count,
        })
    return assigned


def summarize_archive_policy(assigned_rows: list[dict], cutoff: float) -> list[dict]:
    base_by_run_target = {
        (str(row["run_id"]), int(row["assigned_target"])): safe_float(row["objective_margin"])
        for row in assigned_rows
        if row.get("objective_label") == "base" and row.get("assigned_target") is not None
    }
    grouped: dict[tuple[int, str], list[dict]] = defaultdict(list)
    for row in assigned_rows:
        if row.get("assigned_target") is None:
            continue
        grouped[(int(row["assigned_target"]), str(row["objective_label"]))].append(row)

    out: list[dict] = []
    for (target, objective), rows in sorted(grouped.items(), key=lambda item: (item[0][0], objective_sort_key(item[0][1]))):
        margins = [safe_float(row["objective_margin"]) for row in rows]
        finite_margins = [value for value in margins if math.isfinite(value)]
        ratios = []
        for row in rows:
            base = base_by_run_target.get((str(row["run_id"]), target), math.nan)
            margin = safe_float(row["objective_margin"])
            if math.isfinite(base) and base > 0.0 and math.isfinite(margin):
                ratios.append(margin / base)
        out.append({
            "target_label": f"target{target}",
            "target_index": target,
            "objective_label": objective,
            "row_count": len(rows),
            "truth_geometry_count": sum(1 for row in rows if row["is_truth_geometry_for_assigned_target"]),
            "accepted_count": sum(1 for value in finite_margins if value >= cutoff),
            "accepted_fraction": (
                sum(1 for value in finite_margins if value >= cutoff) / len(rows)
                if rows else math.nan
            ),
            "radius_margin_abs_min": min(finite_margins) if finite_margins else math.nan,
            "radius_margin_abs_mean": sum(finite_margins) / len(finite_margins) if finite_margins else math.nan,
            "radius_margin_abs_max": max(finite_margins) if finite_margins else math.nan,
            "margin_ratio_mean": sum(ratios) / len(ratios) if ratios else math.nan,
        })
    return out


def policy_rows(summary_rows: list[dict]) -> list[dict]:
    by_target: dict[str, list[dict]] = defaultdict(list)
    for row in summary_rows:
        by_target[row["target_label"]].append(row)
    policies = []
    for target, rows in sorted(by_target.items()):
        base = next(row for row in rows if row["objective_label"] == "base")
        nonbase = [row for row in rows if row["objective_label"] != "base"]
        strong = [
            row for row in nonbase
            if safe_float(row["accepted_fraction"]) >= 0.95
            and int(row["truth_geometry_count"]) == int(row["row_count"])
        ]
        strongest = max(
            strong or nonbase,
            key=lambda row: (
                safe_float(row["accepted_fraction"], -1.0),
                safe_float(row["margin_ratio_mean"], -1.0),
                safe_float(row["radius_margin_abs_mean"], -1.0),
            ),
        )
        policies.append({
            "target_label": target,
            "base_accepted_fraction": base["accepted_fraction"],
            "archive_scale_confirmation_objectives": (
                ", ".join(row["objective_label"] for row in sorted(strong, key=lambda row: objective_sort_key(row["objective_label"])))
                or "none"
            ),
            "strongest_archive_secondary_objective": strongest["objective_label"],
            "strongest_archive_accepted_fraction": strongest["accepted_fraction"],
            "strongest_archive_margin_ratio_mean": strongest["margin_ratio_mean"],
        })
    return policies


def figure_stats(path: Path) -> dict:
    with Image.open(path) as image:
        arr = np.asarray(image.convert("RGB"))
        gray = np.asarray(image.convert("L"))
    sample = arr.reshape(-1, 3)[:: max(1, arr.reshape(-1, 3).shape[0] // 10000)]
    return {
        "path": str(path),
        "width": int(arr.shape[1]),
        "height": int(arr.shape[0]),
        "sampled_unique_colors": int(np.unique(sample, axis=0).shape[0]),
        "nonwhite_fraction": float(np.mean(np.any(arr < 250, axis=2))),
        "dynamic_range": int(gray.max()) - int(gray.min()),
    }


def plot_archive_matrix(rows: list[dict], save_path: Path) -> str:
    targets = sorted({row["target_label"] for row in rows})
    objectives = sorted({row["objective_label"] for row in rows}, key=objective_sort_key)
    frac = np.full((len(targets), len(objectives)), np.nan)
    ratio = np.full((len(targets), len(objectives)), np.nan)
    lookup = {(row["target_label"], row["objective_label"]): row for row in rows}
    for i, target in enumerate(targets):
        for j, objective in enumerate(objectives):
            row = lookup[(target, objective)]
            frac[i, j] = safe_float(row["accepted_fraction"])
            ratio[i, j] = safe_float(row["margin_ratio_mean"])
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 4.8), constrained_layout=True)
    im0 = axes[0].imshow(frac, vmin=0.0, vmax=1.0, cmap="viridis")
    im1 = axes[1].imshow(ratio, vmin=0.5, vmax=max(1.8, float(np.nanmax(ratio))), cmap="magma")
    axes[0].set_title("Archive rows clearing cutoff")
    axes[1].set_title("Archive mean margin ratio to base")
    for ax in axes:
        ax.set_xticks(np.arange(len(objectives)))
        ax.set_xticklabels(objectives, rotation=35, ha="right")
        ax.set_yticks(np.arange(len(targets)))
        ax.set_yticklabels(targets)
    for i in range(len(targets)):
        for j in range(len(objectives)):
            axes[0].text(j, i, f"{frac[i, j]:.2g}", ha="center", va="center", color="white", fontsize=8)
            axes[1].text(j, i, f"{ratio[i, j]:.2g}", ha="center", va="center", color="white", fontsize=8)
    fig.colorbar(im0, ax=axes[0], shrink=0.85)
    fig.colorbar(im1, ax=axes[1], shrink=0.85)
    fig.suptitle("Archive-level diagnostic objective policy, runs 700-1218", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coordinate-run-summary-csv", required=True)
    parser.add_argument("--objective-variant-summary-csv", required=True)
    parser.add_argument("--cutoff", type=float, default=5.0e-4)
    parser.add_argument("--run-name", default="archive_objective_policy_summary")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    input_run_rows = read_csv_rows(Path(args.coordinate_run_summary_csv))
    input_objective_rows = read_csv_rows(Path(args.objective_variant_summary_csv))
    (
        run_rows,
        objective_rows,
        excluded_noncanonical_runs,
        excluded_noncanonical_objective_rows,
    ) = filter_noncanonical_primary_rows(input_run_rows, input_objective_rows)
    assigned_rows = assign_objective_rows(run_rows, objective_rows)
    summary_rows = summarize_archive_policy(assigned_rows, args.cutoff)
    policies = policy_rows(summary_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    assignment_csv = data_dir / "archive_objective_assignment_rows.csv"
    matrix_csv = data_dir / "archive_objective_policy_matrix.csv"
    policy_csv = data_dir / "archive_objective_policy_recommendations.csv"
    summary_json = data_dir / "archive_objective_policy_summary.json"
    plot_path = Path(plot_archive_matrix(summary_rows, figures_dir / "archive_objective_policy_matrix.png"))
    validation_csv = data_dir / "figure_validation.csv"
    write_csv(assignment_csv, [json_safe(row) for row in assigned_rows])
    write_csv(matrix_csv, [json_safe(row) for row in summary_rows])
    write_csv(policy_csv, [json_safe(row) for row in policies])
    write_csv(validation_csv, [figure_stats(plot_path)])
    summary = {
        "cutoff": args.cutoff,
        "coordinate_run_rows": len(run_rows),
        "objective_variant_rows": len(objective_rows),
        "input_coordinate_run_rows": len(input_run_rows),
        "input_objective_variant_rows": len(input_objective_rows),
        "excluded_noncanonical_primary_runs": excluded_noncanonical_runs,
        "excluded_noncanonical_objective_rows": excluded_noncanonical_objective_rows,
        "assigned_objective_rows": sum(1 for row in assigned_rows if row.get("assigned_target") is not None),
        "unassigned_objective_rows": sum(1 for row in assigned_rows if row.get("assigned_target") is None),
        "policy_rows": policies,
        "paths": {
            "assignment_csv": str(assignment_csv),
            "matrix_csv": str(matrix_csv),
            "policy_csv": str(policy_csv),
            "summary_json": str(summary_json),
            "plot": str(plot_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "archive_objective_policy_summary",
        {
            "summary_json": str(summary_json),
            "matrix_csv": str(matrix_csv),
            "policy_csv": str(policy_csv),
            "plot": str(plot_path),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

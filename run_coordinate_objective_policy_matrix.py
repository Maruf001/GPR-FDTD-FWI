#!/usr/bin/env python3
"""Build a cross-target policy matrix from objective diagnostic reports."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
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
from visualization.plot_style import save_validated_figure  # noqa: E402


def parse_labelled_report(text: str) -> tuple[str, Path]:
    if "=" not in text:
        raise argparse.ArgumentTypeError("report must use label=path")
    label, path = text.split("=", 1)
    label = label.strip()
    if not label:
        raise argparse.ArgumentTypeError("report label cannot be empty")
    report_path = Path(path.strip())
    if not report_path.exists():
        raise argparse.ArgumentTypeError(f"report path does not exist: {report_path}")
    return label, report_path


def safe_float(value, default=math.nan) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return float(default)
    return out if math.isfinite(out) else float(default)


def objective_sort_key(label: str) -> tuple[int, str]:
    order = {
        "base": 0,
        "early_high": 1,
        "highband": 2,
        "late": 3,
        "late_high": 4,
        "veryhigh": 5,
    }
    return order.get(str(label), 99), str(label)


def summarize_report(label: str, path: Path, cutoff: float) -> list[dict]:
    report = json.loads(path.read_text(encoding="utf-8"))
    ratio_summary = report.get("aggregate", {}).get("by_objective", {})
    confidence_rows = report.get("objective_confidence_rows", [])
    rows: list[dict] = []
    objectives = sorted({row.get("objective_label", "") for row in confidence_rows}, key=objective_sort_key)
    for objective in objectives:
        subset = [row for row in confidence_rows if row.get("objective_label") == objective]
        margins = [safe_float(row.get("radius_margin_abs")) for row in subset]
        finite_margins = [value for value in margins if math.isfinite(value)]
        truth_count = sum(1 for row in subset if row.get("is_truth_geometry") is True)
        accepted_count = sum(1 for value in finite_margins if value >= cutoff)
        weak_count = sum(1 for row in subset if row.get("confidence_label") == "weak")
        ratio_data = ratio_summary.get(objective, {})
        rows.append({
            "target_label": label,
            "objective_label": objective,
            "row_count": len(subset),
            "truth_geometry_count": truth_count,
            "accepted_count": accepted_count,
            "accepted_fraction": accepted_count / len(subset) if subset else math.nan,
            "weak_count": weak_count,
            "radius_margin_abs_min": min(finite_margins) if finite_margins else math.nan,
            "radius_margin_abs_mean": sum(finite_margins) / len(finite_margins) if finite_margins else math.nan,
            "radius_margin_abs_max": max(finite_margins) if finite_margins else math.nan,
            "margin_ratio_mean": ratio_data.get("margin_ratio_mean") if objective != "base" else 1.0,
            "geometry_change_count": ratio_data.get("geometry_change_count") if objective != "base" else 0,
            "source_report_json": str(path),
        })
    return rows


def policy_rows(matrix_rows: list[dict]) -> list[dict]:
    by_target: dict[str, list[dict]] = {}
    for row in matrix_rows:
        by_target.setdefault(str(row["target_label"]), []).append(row)
    out = []
    for target, rows in sorted(by_target.items()):
        nonbase = [row for row in rows if row["objective_label"] != "base"]
        full_accept = [
            row for row in nonbase
            if safe_float(row.get("accepted_fraction")) >= 1.0
            and int(row.get("geometry_change_count") or 0) == 0
        ]
        strongest_candidates = [
            row for row in nonbase
            if int(row.get("geometry_change_count") or 0) == 0
        ] or nonbase
        strongest = max(
            strongest_candidates,
            key=lambda row: (
                safe_float(row.get("accepted_fraction"), -1.0),
                safe_float(row.get("margin_ratio_mean"), -1.0),
                safe_float(row.get("radius_margin_abs_mean"), -1.0),
            ),
        )
        recommended = ", ".join(row["objective_label"] for row in sorted(full_accept, key=lambda row: objective_sort_key(row["objective_label"])))
        out.append({
            "target_label": target,
            "base_accepted_fraction": next(
                safe_float(row.get("accepted_fraction"))
                for row in rows
                if row["objective_label"] == "base"
            ),
            "full_acceptance_objectives": recommended or "none",
            "strongest_secondary_objective": strongest["objective_label"],
            "strongest_secondary_accepted_fraction": strongest["accepted_fraction"],
            "strongest_secondary_margin_ratio_mean": strongest["margin_ratio_mean"],
            "policy_note": (
                "Use listed full-acceptance objectives as secondary confirmation only; "
                "do not replace the base production gate."
            ),
        })
    return out


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


def plot_policy_matrix(rows: list[dict], save_path: Path) -> str:
    targets = sorted({row["target_label"] for row in rows})
    objectives = sorted({row["objective_label"] for row in rows}, key=objective_sort_key)
    frac = np.full((len(targets), len(objectives)), np.nan)
    ratio = np.full((len(targets), len(objectives)), np.nan)
    lookup = {(row["target_label"], row["objective_label"]): row for row in rows}
    for i, target in enumerate(targets):
        for j, objective in enumerate(objectives):
            row = lookup.get((target, objective))
            if row is None:
                continue
            frac[i, j] = safe_float(row.get("accepted_fraction"))
            ratio[i, j] = safe_float(row.get("margin_ratio_mean"))

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 4.8), constrained_layout=True)
    im0 = axes[0].imshow(frac, vmin=0.0, vmax=1.0, cmap="viridis")
    axes[0].set_title("Rows clearing base cutoff")
    im1 = axes[1].imshow(ratio, vmin=0.5, vmax=max(1.8, float(np.nanmax(ratio))), cmap="magma")
    axes[1].set_title("Mean margin ratio to base")
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
    fig.suptitle("Cross-target diagnostic objective policy matrix", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", nargs="+", type=parse_labelled_report)
    parser.add_argument("--cutoff", type=float, default=5.0e-4)
    parser.add_argument("--run-name", default="coordinate_objective_policy_matrix")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    matrix_rows: list[dict] = []
    for label, report_path in args.report:
        matrix_rows.extend(summarize_report(label, report_path, args.cutoff))
    policies = policy_rows(matrix_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    matrix_csv = data_dir / "objective_policy_matrix.csv"
    policy_csv = data_dir / "objective_policy_recommendations.csv"
    summary_json = data_dir / "objective_policy_matrix_summary.json"
    plot_path = Path(plot_policy_matrix(matrix_rows, figures_dir / "objective_policy_matrix.png"))
    validation_csv = data_dir / "figure_validation.csv"
    write_csv(matrix_csv, [json_safe(row) for row in matrix_rows])
    write_csv(policy_csv, [json_safe(row) for row in policies])
    write_csv(validation_csv, [figure_stats(plot_path)])
    summary = {
        "cutoff": args.cutoff,
        "report_count": len(args.report),
        "matrix_row_count": len(matrix_rows),
        "policy_rows": policies,
        "paths": {
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
        "coordinate_objective_policy_matrix",
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

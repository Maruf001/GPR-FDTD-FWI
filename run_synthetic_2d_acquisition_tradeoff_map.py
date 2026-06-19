#!/usr/bin/env python3
"""Synthesize current synthetic 2D acquisition tradeoffs without GPU work."""

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
from run_gssi_field_profile_repeatability_policy import safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_EXPERIMENT_ROOT = Path("outputs/experiments")
DEFAULT_SUMMARY_ROOT = Path("outputs/summary_tables/wk03_experiment_700_1259_holistic_evaluation")


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def clean_fraction(row: dict) -> float:
    clean_count = safe_float(row.get("clean_spacing_count", row.get("clean_row_count")))
    total_count = safe_float(row.get("tested_spacing_count", row.get("row_count")))
    if total_count <= 0.0:
        return math.nan
    return float(clean_count / total_count)


def best_target_txrx_rows(txrx_rows: list[dict], min_run_count: int = 3) -> list[dict]:
    grouped: dict[int, list[dict]] = {}
    for row in txrx_rows:
        target = int(safe_float(row.get("target"), -1))
        if target < 0 or safe_float(row.get("run_count")) < min_run_count:
            continue
        grouped.setdefault(target, []).append(row)
    best_rows = []
    for target, rows in sorted(grouped.items()):
        best = max(
            rows,
            key=lambda row: (
                safe_float(row.get("accepted_fraction")),
                safe_float(row.get("run_count")),
                safe_float(row.get("median_margin")),
            ),
        )
        best_rows.append({
            "target": target,
            "target_label": f"target{target}",
            "best_tx_rx_offset_mm": safe_float(best.get("tx_rx_offset_mm")),
            "accepted_fraction": safe_float(best.get("accepted_fraction")),
            "run_count": int(safe_float(best.get("run_count"))),
            "median_margin": safe_float(best.get("median_margin")),
            "status": "archive_best_txrx_not_universal_rule",
        })
    return best_rows


def best_target_source_rows(source_rows: list[dict], min_run_count: int = 2) -> list[dict]:
    grouped: dict[int, list[dict]] = {}
    for row in source_rows:
        target = int(safe_float(row.get("target"), -1))
        if target < 0 or safe_float(row.get("run_count")) < min_run_count:
            continue
        grouped.setdefault(target, []).append(row)
    best_rows = []
    for target, rows in sorted(grouped.items()):
        ordered = sorted(rows, key=lambda row: safe_float(row.get("sources")))
        accepted = [safe_float(row.get("accepted_fraction")) for row in ordered]
        nonmonotonic = any(
            math.isfinite(accepted[idx])
            and math.isfinite(accepted[idx + 1])
            and accepted[idx + 1] + 1.0e-12 < accepted[idx]
            for idx in range(len(accepted) - 1)
        )
        best = max(
            rows,
            key=lambda row: (
                safe_float(row.get("accepted_fraction")),
                safe_float(row.get("run_count")),
                safe_float(row.get("median_margin")),
            ),
        )
        best_rows.append({
            "target": target,
            "target_label": f"target{target}",
            "best_source_count": int(safe_float(best.get("sources"))),
            "accepted_fraction": safe_float(best.get("accepted_fraction")),
            "run_count": int(safe_float(best.get("run_count"))),
            "median_margin": safe_float(best.get("median_margin")),
            "is_nonmonotonic": bool(nonmonotonic),
            "status": "source_density_nonmonotonic" if nonmonotonic else "source_density_monotonic_in_archive",
        })
    return best_rows


def resolution_txrx_tradeoff_rows(by_txrx_rows: list[dict]) -> list[dict]:
    out = []
    for row in sorted(by_txrx_rows, key=lambda item: safe_float(item.get("tx_rx_offset_mm"))):
        txrx = safe_float(row.get("tx_rx_offset_mm"))
        fraction = clean_fraction(row)
        closest = safe_float(row.get("closest_clean_spacing_mm"))
        tested = int(safe_float(row.get("tested_spacing_count")))
        clean = int(safe_float(row.get("clean_spacing_count")))
        if math.isfinite(closest) and closest <= 14.0 and clean == tested:
            status = "tight_spacing_reference"
        elif clean > 0 and fraction >= 0.75:
            status = "mid_spacing_reference"
        elif clean > 0:
            status = "limited_clean_support"
        else:
            status = "not_clean_in_tested_grid"
        out.append({
            "tradeoff_key": f"resolution_txrx_{txrx:g}",
            "category": "close_spacing_resolution",
            "acquisition_setting": f"Tx/Rx={txrx:g} mm",
            "evidence_source": "1239_coordinate_resolution_policy_synthesis",
            "primary_metric_label": "clean_spacing_fraction",
            "primary_metric_value": fraction,
            "support_count": clean,
            "total_count": tested,
            "risk_score": 1.0 - fraction if math.isfinite(fraction) else 1.0,
            "status": status,
            "recommendation": (
                "Use as the current tight-spacing reference branch."
                if status == "tight_spacing_reference"
                else "Use only within the tested spacing range; do not extrapolate as a universal rule."
            ),
        })
    return out


def build_tradeoff_rows(
    by_txrx_rows: list[dict],
    target_txrx_rows: list[dict],
    source_count_rows: list[dict],
    next_matrix: dict,
) -> list[dict]:
    rows = resolution_txrx_tradeoff_rows(by_txrx_rows)
    for row in best_target_txrx_rows(target_txrx_rows):
        rows.append({
            "tradeoff_key": f"{row['target_label']}_archive_txrx",
            "category": "archive_txrx_acceptance",
            "acquisition_setting": f"{row['target_label']} Tx/Rx={row['best_tx_rx_offset_mm']:g} mm",
            "evidence_source": "txrx_target_policy_700_1259",
            "primary_metric_label": "accepted_fraction",
            "primary_metric_value": row["accepted_fraction"],
            "support_count": row["run_count"],
            "total_count": row["run_count"],
            "risk_score": 1.0 - row["accepted_fraction"],
            "status": row["status"],
            "recommendation": (
                "Treat as target-specific archive context, not a universal "
                "Tx/Rx prescription."
            ),
        })
    for row in best_target_source_rows(source_count_rows):
        rows.append({
            "tradeoff_key": f"{row['target_label']}_source_density",
            "category": "archive_source_count_acceptance",
            "acquisition_setting": f"{row['target_label']} sources={row['best_source_count']}",
            "evidence_source": "source_count_target_policy_700_1259",
            "primary_metric_label": "accepted_fraction",
            "primary_metric_value": row["accepted_fraction"],
            "support_count": row["run_count"],
            "total_count": row["run_count"],
            "risk_score": 1.0 - row["accepted_fraction"],
            "status": row["status"],
            "recommendation": (
                "Do not use source-count escalation alone as a monotonic rescue "
                "policy; archive results are target and seed dependent."
            ),
        })
    rows.append({
        "tradeoff_key": "current_gpu_queue",
        "category": "execution_policy",
        "acquisition_setting": "current local 2D queue",
        "evidence_source": "1310_synthetic_2d_next_question_matrix_post_publication_bundle_refresh",
        "primary_metric_label": "conditional_gpu_candidate_count",
        "primary_metric_value": safe_float(next_matrix.get("conditional_gpu_candidate_count")),
        "support_count": 0,
        "total_count": int(safe_float(next_matrix.get("candidate_count"))),
        "risk_score": 0.0,
        "status": "no_current_gpu_candidate",
        "recommendation": (
            "Do not launch broad GPU sweeps. New GPU work needs a new objective, "
            "geometry, acquisition hypothesis, or narrow exception probe."
        ),
    })
    return rows


def summarize_tradeoffs(rows: list[dict], by_spacing_rows: list[dict], next_matrix: dict) -> dict:
    tight = [
        row for row in rows
        if row["category"] == "close_spacing_resolution" and row["status"] == "tight_spacing_reference"
    ]
    tight_txrx = math.nan
    if tight:
        tight_txrx = safe_float(tight[0]["acquisition_setting"].replace("Tx/Rx=", "").replace(" mm", ""))
    spacing14 = next((row for row in by_spacing_rows if safe_float(row.get("close_spacing_mm")) == 14.0), {})
    target1_source = next((row for row in rows if row["tradeoff_key"] == "target1_source_density"), {})
    target2_txrx = next((row for row in rows if row["tradeoff_key"] == "target2_archive_txrx"), {})
    nonmonotonic_sources = sum(
        1 for row in rows
        if row["category"] == "archive_source_count_acceptance" and row["status"] == "source_density_nonmonotonic"
    )
    conditional_gpu = safe_float(next_matrix.get("conditional_gpu_candidate_count"))
    return {
        "policy_label": "synthetic_2d_acquisition_tradeoff_cpu_no_gpu",
        "tradeoff_row_count": len(rows),
        "tight_spacing_reference_txrx_mm": tight_txrx,
        "close14_minimum_clean_txrx_mm": safe_float(spacing14.get("minimum_clean_tx_rx_offset_mm")),
        "target1_source_density_best_setting": target1_source.get("acquisition_setting", ""),
        "target1_source_density_status": target1_source.get("status", ""),
        "target2_archive_best_txrx_setting": target2_txrx.get("acquisition_setting", ""),
        "source_density_nonmonotonic_target_count": nonmonotonic_sources,
        "conditional_gpu_candidate_count": conditional_gpu,
        "gpu_priority": "none_now",
        "ready_for_manuscript_acquisition_table": True,
        "decision": (
            "Existing synthetic evidence supports acquisition-specific wording, "
            "not a universal acquisition law. Tx/Rx=45 mm is the current "
            "tight-spacing reference in the close-spacing grid, Tx/Rx=35 mm "
            "supports mid-spacing branches, and archive source-density effects "
            "are nonmonotonic across targets. No broad or immediate GPU run is "
            "justified by this synthesis."
        ),
    }


def plot_tradeoffs(rows: list[dict], save_path: Path) -> None:
    resolution_rows = [row for row in rows if row["category"] == "close_spacing_resolution"]
    target_txrx_rows = [row for row in rows if row["category"] == "archive_txrx_acceptance"]
    source_rows = [row for row in rows if row["category"] == "archive_source_count_acceptance"]

    fig, axes = plt.subplots(1, 3, figsize=(16.0, 5.0), constrained_layout=True)
    x0 = np.arange(len(resolution_rows))
    axes[0].bar(
        x0,
        [row["primary_metric_value"] for row in resolution_rows],
        color="#4c78a8",
        edgecolor="#333333",
    )
    axes[0].set_xticks(x0, [row["acquisition_setting"].replace("=", "\n") for row in resolution_rows])
    axes[0].set_ylim(0.0, 1.05)
    axes[0].set_title("Close-spacing clean fraction")
    axes[0].set_ylabel("clean / tested spacings")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    x1 = np.arange(len(target_txrx_rows))
    axes[1].bar(
        x1,
        [row["primary_metric_value"] for row in target_txrx_rows],
        color="#2f9d55",
        edgecolor="#333333",
    )
    axes[1].set_xticks(x1, [row["acquisition_setting"].replace(" ", "\n", 1) for row in target_txrx_rows])
    axes[1].set_ylim(0.0, 1.05)
    axes[1].set_title("Best archive Tx/Rx by target")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    x2 = np.arange(len(source_rows))
    colors = ["#d99a19" if row["status"] == "source_density_nonmonotonic" else "#2f9d55" for row in source_rows]
    axes[2].bar(
        x2,
        [row["primary_metric_value"] for row in source_rows],
        color=colors,
        edgecolor="#333333",
    )
    axes[2].set_xticks(x2, [row["acquisition_setting"].replace(" ", "\n", 1) for row in source_rows])
    axes[2].set_ylim(0.0, 1.05)
    axes[2].set_title("Best source-count acceptance by target")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)
    fig.suptitle("Synthetic 2D acquisition tradeoff map from existing evidence", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def load_inputs(experiment_root: Path, summary_root: Path) -> tuple[list[dict], list[dict], list[dict], list[dict], dict]:
    by_txrx = read_csv_rows(
        experiment_root
        / "1239_coordinate_resolution_policy_synthesis/data/coordinate_resolution_policy_by_txrx.csv"
    )
    by_spacing = read_csv_rows(
        experiment_root
        / "1239_coordinate_resolution_policy_synthesis/data/coordinate_resolution_policy_by_spacing.csv"
    )
    txrx_target = read_csv_rows(summary_root / "data/txrx_target_policy_700_1259.csv")
    source_count = read_csv_rows(summary_root / "data/source_count_target_policy_700_1259.csv")
    next_matrix = read_json(
        experiment_root
        / "1310_synthetic_2d_next_question_matrix_post_publication_bundle_refresh/data/"
        "synthetic_2d_next_question_matrix_summary.json"
    )
    return by_txrx, by_spacing, txrx_target, source_count, next_matrix


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default=str(DEFAULT_EXPERIMENT_ROOT))
    parser.add_argument("--summary-root", default=str(DEFAULT_SUMMARY_ROOT))
    parser.add_argument("--run-name", default="synthetic_2d_acquisition_tradeoff_map_current")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    experiment_root = Path(args.experiment_root)
    summary_root = Path(args.summary_root)
    by_txrx, by_spacing, txrx_target, source_count, next_matrix = load_inputs(experiment_root, summary_root)
    rows = build_tradeoff_rows(by_txrx, txrx_target, source_count, next_matrix)
    summary = summarize_tradeoffs(rows, by_spacing, next_matrix)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(experiment_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "synthetic_2d_acquisition_tradeoff_rows.csv"
    summary_json = data_dir / "synthetic_2d_acquisition_tradeoff_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "synthetic_2d_acquisition_tradeoff_map.png"

    plot_tradeoffs(rows, figure_path)
    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [figure_stats(figure_path)])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "synthetic_2d_acquisition_tradeoff_map",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

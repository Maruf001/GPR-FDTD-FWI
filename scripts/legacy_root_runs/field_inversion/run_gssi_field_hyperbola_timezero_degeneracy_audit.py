#!/usr/bin/env python3
"""Audit field hyperbola/time-zero degeneracy from existing GSSI score surfaces."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_corrected_profile_stack import safe_float  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_HYPERBOLA_RUN = "003_gssi51600s_hyperbola_calibration_qc"
DEFAULT_COMMON_OFFSET_RUN = "004_gssi51600s_common_offset_sweep"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def is_true(value: object) -> bool:
    return str(value).strip().lower() == "true"


def finite_span(values: list[float]) -> float:
    finite = [value for value in values if math.isfinite(value)]
    if not finite:
        return math.nan
    return float(max(finite) - min(finite))


def grouped_rows(rows: list[dict], key: str) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for row in rows:
        out.setdefault(str(row.get(key, "")), []).append(row)
    return out


def best_score(rows: list[dict]) -> float:
    scores = [safe_float(row.get("profile_score")) for row in rows]
    return max(score for score in scores if math.isfinite(score))


def near_top_rows(rows: list[dict], fractional_drop: float = 0.01) -> list[dict]:
    top = best_score(rows)
    threshold = top - abs(top) * fractional_drop
    return [row for row in rows if safe_float(row.get("profile_score")) >= threshold]


def summarize_near_surface(
    *,
    file_name: str,
    surface_type: str,
    rows: list[dict],
    summary_row: dict,
    fractional_drop: float,
) -> dict:
    near = near_top_rows(rows, fractional_drop=fractional_drop)
    top = best_score(rows)
    epsr_values = [safe_float(row.get("epsr")) for row in near]
    velocity_values = [safe_float(row.get("velocity_m_per_ns")) for row in near]
    time_zero_values = [safe_float(row.get("time_zero_ns")) for row in near]
    median_depth_values = [safe_float(row.get("median_depth_m")) * 1000.0 for row in near]
    txrx_values = [safe_float(row.get("tx_rx_offset_mm")) for row in near if "tx_rx_offset_mm" in row]
    return {
        "file": file_name,
        "surface_type": surface_type,
        "total_surface_rows": len(rows),
        "top_score": top,
        "near_top_fractional_drop": fractional_drop,
        "near_top_row_count": len(near),
        "near_top_fraction": len(near) / len(rows) if rows else math.nan,
        "top_minus_p95_or_reported_margin": safe_float(summary_row.get("score_margin_vs_p95")),
        "best_on_grid_boundary": is_true(summary_row.get("best_on_grid_boundary")),
        "best_epsr": safe_float(summary_row.get("best_epsr", summary_row.get("epsr"))),
        "best_velocity_m_per_ns": safe_float(
            summary_row.get("best_velocity_m_per_ns", summary_row.get("velocity_m_per_ns"))
        ),
        "best_time_zero_ns": safe_float(summary_row.get("best_time_zero_ns", summary_row.get("time_zero_ns"))),
        "best_tx_rx_offset_mm": safe_float(summary_row.get("tx_rx_offset_mm")),
        "near_top_epsr_min": min(epsr_values),
        "near_top_epsr_max": max(epsr_values),
        "near_top_epsr_span": finite_span(epsr_values),
        "near_top_velocity_span_m_per_ns": finite_span(velocity_values),
        "near_top_time_zero_span_ns": finite_span(time_zero_values),
        "near_top_median_depth_span_mm": finite_span(median_depth_values),
        "near_top_txrx_span_mm": finite_span(txrx_values) if txrx_values else math.nan,
        "claim_status": "near_top_degenerate_not_calibrated_depth",
    }


def summarize_offset_rows(best_by_offset_rows: list[dict], fractional_drop: float = 0.05) -> list[dict]:
    out = []
    for file_name, rows in sorted(grouped_rows(best_by_offset_rows, "file").items()):
        top = best_score(rows)
        threshold = top - abs(top) * fractional_drop
        near = [row for row in rows if safe_float(row.get("profile_score")) >= threshold]
        offsets = [safe_float(row.get("tx_rx_offset_mm")) for row in near]
        epsrs = [safe_float(row.get("epsr")) for row in near]
        depths = [1000.0 * safe_float(row.get("median_depth_m")) for row in near]
        best = max(rows, key=lambda row: safe_float(row.get("profile_score")))
        out.append({
            "file": file_name,
            "surface_type": "common_offset_best_by_offset",
            "tested_offset_count": len(rows),
            "top_score": top,
            "near_top_fractional_drop": fractional_drop,
            "near_top_offset_count": len(near),
            "near_top_offsets_mm": ";".join(f"{value:g}" for value in sorted(offsets)),
            "near_top_offset_span_mm": finite_span(offsets),
            "near_top_epsr_span": finite_span(epsrs),
            "near_top_median_depth_span_mm": finite_span(depths),
            "best_tx_rx_offset_mm": safe_float(best.get("tx_rx_offset_mm")),
            "best_epsr": safe_float(best.get("epsr")),
            "best_time_zero_ns": safe_float(best.get("time_zero_ns")),
            "claim_status": "txrx_offset_score_ambiguous_not_calibrated_geometry",
        })
    return out


def build_degeneracy_rows(
    hyperbola_surface_rows: list[dict],
    hyperbola_summary_rows: list[dict],
    common_surface_rows: list[dict],
    common_profile_rows: list[dict],
    best_by_offset_rows: list[dict],
) -> tuple[list[dict], list[dict]]:
    hyperbola_summary = {str(row.get("file", "")): row for row in hyperbola_summary_rows}
    common_summary = {str(row.get("file", "")): row for row in common_profile_rows}
    rows = []
    for file_name, file_rows in sorted(grouped_rows(hyperbola_surface_rows, "file").items()):
        rows.append(summarize_near_surface(
            file_name=file_name,
            surface_type="zero_offset_hyperbola_template",
            rows=file_rows,
            summary_row=hyperbola_summary.get(file_name, {}),
            fractional_drop=0.01,
        ))
    for file_name, file_rows in sorted(grouped_rows(common_surface_rows, "file").items()):
        rows.append(summarize_near_surface(
            file_name=file_name,
            surface_type="common_offset_hyperbola_sweep",
            rows=file_rows,
            summary_row=common_summary.get(file_name, {}),
            fractional_drop=0.01,
        ))
    return rows, summarize_offset_rows(best_by_offset_rows, fractional_drop=0.05)


def summarize_degeneracy(rows: list[dict], offset_rows: list[dict]) -> dict:
    boundary_count = sum(1 for row in rows if row["best_on_grid_boundary"])
    epsr_spans = [safe_float(row.get("near_top_epsr_span")) for row in rows]
    time_zero_spans = [safe_float(row.get("near_top_time_zero_span_ns")) for row in rows]
    txrx_spans = [safe_float(row.get("near_top_txrx_span_mm")) for row in rows]
    offset_counts = [safe_float(row.get("near_top_offset_count")) for row in offset_rows]
    return {
        "policy_label": "field_hyperbola_timezero_degeneracy_not_calibrated_inversion",
        "surface_summary_row_count": len(rows),
        "offset_summary_row_count": len(offset_rows),
        "boundary_best_surface_count": boundary_count,
        "max_near_top_epsr_span": max(value for value in epsr_spans if math.isfinite(value)),
        "max_near_top_time_zero_span_ns": max(value for value in time_zero_spans if math.isfinite(value)),
        "max_near_top_txrx_span_mm": max([value for value in txrx_spans if math.isfinite(value)] or [math.nan]),
        "max_near_top_offset_count_5pct": int(max(offset_counts)) if offset_counts else 0,
        "any_surface_best_on_boundary": boundary_count > 0,
        "cover_depth_claim_ready": False,
        "radius_claim_ready": False,
        "field_fwi_ready": False,
        "gpu_priority": "none",
        "decision": (
            "Existing field hyperbola/offset score surfaces are useful QC overlays, "
            "but they are not calibrated inversion evidence. Near-top score regions "
            "span multiple dielectric/time-zero choices, common-offset scores keep "
            "several offsets plausible, and multiple best fits sit on grid boundaries."
        ),
    }


def plot_degeneracy(rows: list[dict], offset_rows: list[dict], summary: dict, save_path: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(16.0, 8.8), constrained_layout=True)
    labels = [
        f"{row['file'].split('__')[-1].replace('.DZT', '')}\n{row['surface_type'].replace('_', ' ')[:18]}"
        for row in rows
    ]
    x = np.arange(len(rows))
    axes[0, 0].bar(
        x,
        [row["near_top_epsr_span"] for row in rows],
        color="#4c78a8",
        edgecolor="#333333",
    )
    axes[0, 0].set_xticks(x, labels)
    axes[0, 0].set_ylabel("epsr span inside 1% top score")
    axes[0, 0].set_title("Near-top dielectric degeneracy")
    axes[0, 0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[0, 1].bar(
        x,
        [row["near_top_time_zero_span_ns"] for row in rows],
        color="#d99a19",
        edgecolor="#333333",
    )
    axes[0, 1].set_xticks(x, labels)
    axes[0, 1].set_ylabel("time-zero span inside 1% top score (ns)")
    axes[0, 1].set_title("Near-top time-zero degeneracy")
    axes[0, 1].grid(axis="y", color="#dddddd", linewidth=0.6)

    offset_labels = [row["file"].split("__")[-1].replace(".DZT", "") for row in offset_rows]
    ox = np.arange(len(offset_rows))
    axes[1, 0].bar(
        ox - 0.18,
        [row["near_top_offset_count"] for row in offset_rows],
        width=0.36,
        color="#2f9d55",
        edgecolor="#333333",
        label="near-top offsets",
    )
    axes[1, 0].bar(
        ox + 0.18,
        [row["near_top_offset_span_mm"] for row in offset_rows],
        width=0.36,
        color="#9b5de5",
        edgecolor="#333333",
        label="offset span mm",
    )
    axes[1, 0].set_xticks(ox, offset_labels)
    axes[1, 0].set_title("Common-offset ambiguity within 5% score")
    axes[1, 0].legend(loc="upper right", fontsize=8)
    axes[1, 0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1, 1].axis("off")
    text = (
        f"surface rows: {summary['surface_summary_row_count']}\n"
        f"boundary best fits: {summary['boundary_best_surface_count']}\n"
        f"max epsr span near top: {summary['max_near_top_epsr_span']:.2f}\n"
        f"max time-zero span near top: {summary['max_near_top_time_zero_span_ns']:.3f} ns\n"
        f"max near-top offset count: {summary['max_near_top_offset_count_5pct']}\n\n"
        "Conclusion: QC overlay only.\nNo calibrated cover-depth, radius, 3D, or field-FWI claim."
    )
    axes[1, 1].text(
        0.02,
        0.95,
        text,
        transform=axes[1, 1].transAxes,
        ha="left",
        va="top",
        fontsize=12,
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "white", "edgecolor": "#bbbbbb"},
    )

    fig.suptitle("Field hyperbola/time-zero degeneracy audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def load_inputs(dataset_root: Path, runs: dict[str, str]) -> tuple[list[dict], list[dict], list[dict], list[dict], list[dict]]:
    hyperbola_root = dataset_root / runs["hyperbola"] / "data"
    common_root = dataset_root / runs["common_offset"] / "data"
    return (
        read_csv_rows(hyperbola_root / "field_hyperbola_score_surface.csv"),
        read_csv_rows(hyperbola_root / "field_hyperbola_calibration_summary.csv"),
        read_csv_rows(common_root / "field_common_offset_score_surface.csv"),
        read_csv_rows(common_root / "field_common_offset_profile_summary.csv"),
        read_csv_rows(common_root / "field_common_offset_best_by_offset.csv"),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--run-name", default="gssi51600s_field_hyperbola_timezero_degeneracy_audit")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    runs = {
        "hyperbola": DEFAULT_HYPERBOLA_RUN,
        "common_offset": DEFAULT_COMMON_OFFSET_RUN,
    }
    (
        hyperbola_surface,
        hyperbola_summary,
        common_surface,
        common_profile,
        best_by_offset,
    ) = load_inputs(dataset_root, runs)
    degeneracy_rows, offset_rows = build_degeneracy_rows(
        hyperbola_surface,
        hyperbola_summary,
        common_surface,
        common_profile,
        best_by_offset,
    )
    summary = summarize_degeneracy(degeneracy_rows, offset_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_hyperbola_timezero_degeneracy_rows.csv"
    offset_csv = data_dir / "field_common_offset_ambiguity_rows.csv"
    summary_json = data_dir / "field_hyperbola_timezero_degeneracy_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_hyperbola_timezero_degeneracy.png"

    plot_degeneracy(degeneracy_rows, offset_rows, summary, figure_path)
    write_csv(rows_csv, [json_safe(row) for row in degeneracy_rows])
    write_csv(offset_csv, [json_safe(row) for row in offset_rows])
    write_csv(validation_csv, [figure_stats(figure_path)])
    summary["readgssi_version"] = readgssi_version()
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "offset_csv": str(offset_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_hyperbola_timezero_degeneracy_audit",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "offset_csv": str(offset_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

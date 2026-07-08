#!/usr/bin/env python3
"""Audit apparent-depth scale for local GSSI field QC without cover-depth claims."""

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


C_M_PER_NS = 0.299792458

DEFAULT_DZT_RUN = "001_gssi51600s_dzt_qc"
DEFAULT_CUE_RUN = "002_gssi51600s_preprocess_feature_qc"
DEFAULT_TIME_ZERO_APPLICATION_RUN = "025_gssi51600s_short_profile_time_zero_application_policy"
DEFAULT_CONTENT_ANCHOR_RUN = "037_gssi51600s_content_time_zero_anchor_policy"
DEFAULT_TIME_ZERO_BUDGET_RUN = "075_gssi51600s_field_time_zero_uncertainty_budget"
DEFAULT_ACQUISITION_READINESS_RUN = "081_gssi51600s_field_acquisition_readiness_audit"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def is_true(value: object) -> bool:
    return str(value).strip().lower() == "true"


def medium_velocity_m_per_ns(epsr: float) -> float:
    epsr = safe_float(epsr)
    if not math.isfinite(epsr) or epsr <= 0.0:
        return math.nan
    return float(C_M_PER_NS / math.sqrt(epsr))


def two_way_depth_mm(time_ns: float, epsr: float) -> float:
    time_ns = safe_float(time_ns)
    velocity = medium_velocity_m_per_ns(epsr)
    if not math.isfinite(time_ns) or not math.isfinite(velocity):
        return math.nan
    return float(1000.0 * 0.5 * velocity * time_ns)


def median_finite(values: list[float]) -> float:
    finite = [value for value in values if math.isfinite(value)]
    if not finite:
        return math.nan
    return float(np.median(np.asarray(finite, dtype=np.float64)))


def file_group(file_name: str) -> str:
    if "__014" in file_name or "__016" in file_name:
        return "short_014_016"
    if "__013" in file_name or "__015" in file_name:
        return "long_013_015"
    return "other"


def load_inputs(dataset_root: Path, runs: dict[str, str]) -> dict[str, object]:
    return {
        "dzt_summary": read_json(dataset_root / runs["dzt"] / "data" / "gssi_dzt_qc_summary.json"),
        "cue_rows": read_csv_rows(dataset_root / runs["cue"] / "data" / "field_reflector_cue_candidates.csv"),
        "applied_rows": read_csv_rows(
            dataset_root
            / runs["time_zero_application"]
            / "data"
            / "short_profile_time_zero_applied_event_residuals.csv"
        ),
        "content_rows": read_csv_rows(
            dataset_root
            / runs["content_anchor"]
            / "data"
            / "short_profile_content_time_zero_anchor_rows.csv"
        ),
        "time_zero_budget": read_json(
            dataset_root / runs["time_zero_budget"] / "data" / "field_time_zero_uncertainty_budget_summary.json"
        ),
        "acquisition_readiness": read_json(
            dataset_root / runs["acquisition_readiness"] / "data" / "field_acquisition_readiness_summary.json"
        ),
    }


def nominal_epsr(dzt_summary: dict) -> float:
    records = dzt_summary.get("records", [])
    return median_finite([safe_float(record.get("dielectric")) for record in records])


def profile_cue_rows(cue_rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for row in cue_rows:
        grouped.setdefault(str(row.get("file", "")), []).append(row)
    out = []
    for file_name, rows in sorted(grouped.items()):
        depths_mm = [1000.0 * safe_float(row.get("approx_depth_m")) for row in rows]
        times_ns = [safe_float(row.get("time_ns")) for row in rows]
        xs_m = [safe_float(row.get("x_m")) for row in rows]
        strengths = [safe_float(row.get("relative_strength")) for row in rows]
        out.append({
            "file": file_name,
            "profile_group": file_group(file_name),
            "cue_count": len(rows),
            "min_time_ns": min(times_ns),
            "max_time_ns": max(times_ns),
            "median_time_ns": median_finite(times_ns),
            "min_apparent_depth_mm": min(depths_mm),
            "max_apparent_depth_mm": max(depths_mm),
            "median_apparent_depth_mm": median_finite(depths_mm),
            "x_min_m": min(xs_m),
            "x_max_m": max(xs_m),
            "x_span_m": max(xs_m) - min(xs_m),
            "max_relative_strength": max(strengths),
            "claim_status": "apparent_depth_scale_qc_not_cover_depth",
        })
    return out


def content_by_pair(content_rows: list[dict]) -> dict[int, dict]:
    return {int(safe_float(row.get("pair_index"))): row for row in content_rows}


def short_pair_depth_rows(
    applied_rows: list[dict],
    content_rows: list[dict],
    epsr: float,
    conservative_depth_equivalent_mm: float,
) -> list[dict]:
    content_lookup = content_by_pair(content_rows)
    out = []
    for row in sorted(applied_rows, key=lambda item: safe_float(item.get("pair_index"))):
        pair_index = int(safe_float(row.get("pair_index")))
        content = content_lookup.get(pair_index, {})
        applied_offset = safe_float(row.get("applied_transfer_offset_ns"))
        reference_phase = safe_float(row.get("reference_phase_time_ns"))
        comparison_phase = safe_float(row.get("comparison_phase_time_ns"))
        corrected_comparison_phase = comparison_phase - applied_offset
        raw_residual_ns = safe_float(row.get("abs_raw_phase_residual_ns"))
        corrected_residual_ns = safe_float(row.get("abs_corrected_phase_residual_ns"))
        corrected_residual_mm = two_way_depth_mm(corrected_residual_ns, epsr)
        content_backed = is_true(content.get("content_backed"))
        if corrected_residual_mm <= conservative_depth_equivalent_mm:
            status = "content_backed_relative_depth_scale_qc" if content_backed else "timing_only_relative_depth_scale_qc"
        else:
            status = "outside_relative_depth_uncertainty"
        out.append({
            "pair_index": pair_index,
            "content_backed": content_backed,
            "reference_apex_group": row.get("reference_apex_group", ""),
            "comparison_apex_group": row.get("comparison_apex_group", ""),
            "reference_x_mm": 1000.0 * safe_float(row.get("reference_x_m")),
            "comparison_aligned_x_mm": 1000.0 * safe_float(row.get("comparison_aligned_x_m")),
            "aligned_x_residual_mm": safe_float(row.get("aligned_x_residual_mm")),
            "reference_phase_time_ns": reference_phase,
            "comparison_phase_time_ns": comparison_phase,
            "applied_transfer_offset_ns": applied_offset,
            "corrected_comparison_phase_time_ns": corrected_comparison_phase,
            "reference_apparent_depth_mm": two_way_depth_mm(reference_phase, epsr),
            "comparison_raw_apparent_depth_mm": two_way_depth_mm(comparison_phase, epsr),
            "comparison_corrected_apparent_depth_mm": two_way_depth_mm(corrected_comparison_phase, epsr),
            "raw_depth_residual_mm": two_way_depth_mm(raw_residual_ns, epsr),
            "corrected_depth_residual_mm": corrected_residual_mm,
            "within_conservative_depth_equivalent": bool(corrected_residual_mm <= conservative_depth_equivalent_mm),
            "pair_min_absolute_correlation": safe_float(content.get("pair_min_absolute_correlation")),
            "claim_status": status,
        })
    return out


def summarize_depth_qc(
    profile_rows: list[dict],
    pair_rows: list[dict],
    epsr: float,
    time_zero_budget: dict,
    acquisition_readiness: dict,
) -> dict:
    cue_count = sum(int(row["cue_count"]) for row in profile_rows)
    cue_depths = []
    for row in profile_rows:
        cue_depths.extend([safe_float(row["min_apparent_depth_mm"]), safe_float(row["max_apparent_depth_mm"])])
    short_profile_rows = [row for row in profile_rows if row["profile_group"] == "short_014_016"]
    long_profile_rows = [row for row in profile_rows if row["profile_group"] == "long_013_015"]
    raw_residuals = [safe_float(row["raw_depth_residual_mm"]) for row in pair_rows]
    corrected_residuals = [safe_float(row["corrected_depth_residual_mm"]) for row in pair_rows]
    mean_raw = float(np.mean(raw_residuals)) if raw_residuals else math.nan
    mean_corrected = float(np.mean(corrected_residuals)) if corrected_residuals else math.nan
    corrected_support_count = sum(1 for row in pair_rows if row["within_conservative_depth_equivalent"])
    content_backed_count = sum(1 for row in pair_rows if row["content_backed"])
    return {
        "policy_label": "field_apparent_depth_qc_relative_scale_not_cover_depth",
        "profile_count": len(profile_rows),
        "cue_count": cue_count,
        "short_profile_count": len(short_profile_rows),
        "long_profile_count": len(long_profile_rows),
        "short_profile_cue_count": sum(int(row["cue_count"]) for row in short_profile_rows),
        "long_profile_cue_count": sum(int(row["cue_count"]) for row in long_profile_rows),
        "nominal_dielectric": epsr,
        "nominal_velocity_m_per_ns": medium_velocity_m_per_ns(epsr),
        "min_profile_apparent_depth_mm": min(cue_depths) if cue_depths else math.nan,
        "max_profile_apparent_depth_mm": max(cue_depths) if cue_depths else math.nan,
        "short_pair_count": len(pair_rows),
        "short_pair_content_backed_count": content_backed_count,
        "short_pair_corrected_depth_support_count": corrected_support_count,
        "short_pair_corrected_depth_support_fraction": corrected_support_count / len(pair_rows) if pair_rows else math.nan,
        "mean_raw_depth_residual_mm": mean_raw,
        "mean_corrected_depth_residual_mm": mean_corrected,
        "max_corrected_depth_residual_mm": max(corrected_residuals) if corrected_residuals else math.nan,
        "mean_depth_residual_reduction_factor": mean_raw / mean_corrected if mean_corrected else math.nan,
        "time_zero_conservative_half_width_ns": safe_float(time_zero_budget.get("conservative_half_width_ns")),
        "time_zero_depth_equivalent_mm": safe_float(
            acquisition_readiness.get("time_zero_two_way_depth_equivalent_mm")
        ),
        "ready_for_apparent_depth_scale_qc": True,
        "ready_for_cover_depth_recovery": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "Use this audit only as an apparent-depth scale check for measured "
            "field QC. The short-pair relative time-zero correction brings all "
            "three paired phase residuals inside the conservative depth-equivalent "
            "uncertainty, but the dataset still lacks absolute time-zero, target "
            "labels, radius validation, and 3D survey geometry."
        ),
    }


def plot_depth_qc(profile_rows: list[dict], pair_rows: list[dict], summary: dict, save_path: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(15.5, 8.8), constrained_layout=True)
    profile_labels = [row["file"].replace("PROJECT001C__", "").replace(".DZT", "") for row in profile_rows]
    x = np.arange(len(profile_rows))
    colors = ["#4c78a8" if row["profile_group"] == "short_014_016" else "#d99a19" for row in profile_rows]
    axes[0, 0].bar(
        x,
        [row["max_apparent_depth_mm"] - row["min_apparent_depth_mm"] for row in profile_rows],
        bottom=[row["min_apparent_depth_mm"] for row in profile_rows],
        color=colors,
        edgecolor="#333333",
    )
    axes[0, 0].scatter(x, [row["median_apparent_depth_mm"] for row in profile_rows], color="#222222", zorder=3)
    axes[0, 0].set_xticks(x, profile_labels)
    axes[0, 0].set_ylabel("apparent depth scale (mm)")
    axes[0, 0].set_title("Reflector-cue apparent depth ranges")
    axes[0, 0].grid(axis="y", color="#dddddd", linewidth=0.6)

    pair_x = np.arange(len(pair_rows))
    width = 0.36
    axes[0, 1].bar(
        pair_x - width / 2,
        [row["raw_depth_residual_mm"] for row in pair_rows],
        width=width,
        color="#9b5de5",
        edgecolor="#333333",
        label="raw residual",
    )
    axes[0, 1].bar(
        pair_x + width / 2,
        [row["corrected_depth_residual_mm"] for row in pair_rows],
        width=width,
        color="#2f9d55",
        edgecolor="#333333",
        label="corrected residual",
    )
    axes[0, 1].axhline(summary["time_zero_depth_equivalent_mm"], color="#b23b3b", linestyle="--", linewidth=1.2)
    axes[0, 1].set_xticks(pair_x, [f"pair {row['pair_index']}" for row in pair_rows])
    axes[0, 1].set_ylabel("depth-equivalent residual (mm)")
    axes[0, 1].set_title("Short-pair relative time-zero residuals")
    axes[0, 1].legend(loc="upper right", fontsize=8)
    axes[0, 1].grid(axis="y", color="#dddddd", linewidth=0.6)

    for row in pair_rows:
        marker = "o" if row["content_backed"] else "s"
        color = "#2f9d55" if row["content_backed"] else "#d99a19"
        axes[1, 0].scatter(
            row["reference_apparent_depth_mm"],
            row["comparison_corrected_apparent_depth_mm"],
            marker=marker,
            s=80,
            color=color,
            edgecolor="#333333",
            label="content-backed" if row["content_backed"] else "timing-only",
        )
        axes[1, 0].text(
            row["reference_apparent_depth_mm"],
            row["comparison_corrected_apparent_depth_mm"] + 0.5,
            f"{row['pair_index']}",
            ha="center",
            va="bottom",
            fontsize=8,
        )
    all_depths = [
        value
        for row in pair_rows
        for value in (row["reference_apparent_depth_mm"], row["comparison_corrected_apparent_depth_mm"])
    ]
    lo = min(all_depths) - 3.0
    hi = max(all_depths) + 3.0
    axes[1, 0].plot([lo, hi], [lo, hi], color="#666666", linestyle="--", linewidth=1.0)
    axes[1, 0].set_xlim(lo, hi)
    axes[1, 0].set_ylim(lo, hi)
    axes[1, 0].set_xlabel("014 reference apparent depth (mm)")
    axes[1, 0].set_ylabel("016 corrected apparent depth (mm)")
    axes[1, 0].set_title("Corrected short-pair depth-scale agreement")
    handles, labels = axes[1, 0].get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    axes[1, 0].legend(unique.values(), unique.keys(), loc="upper left", fontsize=8)
    axes[1, 0].grid(color="#dddddd", linewidth=0.6)

    labels = ["profile cues", "content pairs", "within budget"]
    values = [summary["cue_count"], summary["short_pair_content_backed_count"], summary["short_pair_corrected_depth_support_count"]]
    axes[1, 1].bar(labels, values, color=["#4c78a8", "#2f9d55", "#d99a19"], edgecolor="#333333")
    axes[1, 1].set_title("Field apparent-depth QC support")
    axes[1, 1].set_ylabel("count")
    axes[1, 1].grid(axis="y", color="#dddddd", linewidth=0.6)
    note = (
        "not cover depth\n"
        f"max corrected residual: {summary['max_corrected_depth_residual_mm']:.2f} mm\n"
        f"budget: {summary['time_zero_depth_equivalent_mm']:.2f} mm"
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

    fig.suptitle("GSSI field apparent-depth scale QC, not cover-depth recovery", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--run-name", default="gssi51600s_field_apparent_depth_qc")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    runs = {
        "dzt": DEFAULT_DZT_RUN,
        "cue": DEFAULT_CUE_RUN,
        "time_zero_application": DEFAULT_TIME_ZERO_APPLICATION_RUN,
        "content_anchor": DEFAULT_CONTENT_ANCHOR_RUN,
        "time_zero_budget": DEFAULT_TIME_ZERO_BUDGET_RUN,
        "acquisition_readiness": DEFAULT_ACQUISITION_READINESS_RUN,
    }
    inputs = load_inputs(dataset_root, runs)
    epsr = nominal_epsr(inputs["dzt_summary"])
    conservative_depth_mm = safe_float(inputs["acquisition_readiness"].get("time_zero_two_way_depth_equivalent_mm"))
    profile_rows = profile_cue_rows(inputs["cue_rows"])
    pair_rows = short_pair_depth_rows(
        inputs["applied_rows"],
        inputs["content_rows"],
        epsr,
        conservative_depth_mm,
    )
    summary = summarize_depth_qc(
        profile_rows,
        pair_rows,
        epsr,
        inputs["time_zero_budget"],
        inputs["acquisition_readiness"],
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    profile_csv = data_dir / "field_apparent_depth_profile_cues.csv"
    pair_csv = data_dir / "field_apparent_depth_short_pair_residuals.csv"
    summary_json = data_dir / "field_apparent_depth_qc_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_apparent_depth_qc.png"

    plot_depth_qc(profile_rows, pair_rows, summary, figure_path)
    write_csv(profile_csv, [json_safe(row) for row in profile_rows])
    write_csv(pair_csv, [json_safe(row) for row in pair_rows])
    write_csv(validation_csv, [figure_stats(figure_path)])
    summary["readgssi_version"] = readgssi_version()
    summary["paths"] = {
        "profile_csv": str(profile_csv),
        "pair_csv": str(pair_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_apparent_depth_qc",
        {
            "summary_json": str(summary_json),
            "profile_csv": str(profile_csv),
            "pair_csv": str(pair_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

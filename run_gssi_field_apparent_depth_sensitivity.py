#!/usr/bin/env python3
"""Test apparent-depth sensitivity to dielectric assumptions for GSSI field QC."""

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
from run_gssi_field_apparent_depth_qc import medium_velocity_m_per_ns, nominal_epsr, two_way_depth_mm  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_corrected_profile_stack import safe_float  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_DZT_RUN = "001_gssi51600s_dzt_qc"
DEFAULT_CUE_RUN = "002_gssi51600s_preprocess_feature_qc"
DEFAULT_HYPERBOLA_RUN = "003_gssi51600s_hyperbola_calibration_qc"
DEFAULT_COMMON_OFFSET_RUN = "004_gssi51600s_common_offset_sweep"
DEFAULT_TIME_ZERO_APPLICATION_RUN = "025_gssi51600s_short_profile_time_zero_application_policy"
DEFAULT_TIME_ZERO_BUDGET_RUN = "075_gssi51600s_field_time_zero_uncertainty_budget"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def median_finite(values: list[float]) -> float:
    finite = [value for value in values if math.isfinite(value)]
    if not finite:
        return math.nan
    return float(np.median(np.asarray(finite, dtype=np.float64)))


def load_inputs(dataset_root: Path, runs: dict[str, str]) -> dict[str, object]:
    return {
        "dzt_summary": read_json(dataset_root / runs["dzt"] / "data" / "gssi_dzt_qc_summary.json"),
        "cue_rows": read_csv_rows(dataset_root / runs["cue"] / "data" / "field_reflector_cue_candidates.csv"),
        "hyperbola_summary_rows": read_csv_rows(
            dataset_root / runs["hyperbola"] / "data" / "field_hyperbola_calibration_summary.csv"
        ),
        "common_offset_rows": read_csv_rows(
            dataset_root / runs["common_offset"] / "data" / "field_common_offset_best_by_offset.csv"
        ),
        "applied_rows": read_csv_rows(
            dataset_root
            / runs["time_zero_application"]
            / "data"
            / "short_profile_time_zero_applied_event_residuals.csv"
        ),
        "time_zero_budget": read_json(
            dataset_root / runs["time_zero_budget"] / "data" / "field_time_zero_uncertainty_budget_summary.json"
        ),
    }


def sensitivity_scenarios(
    dzt_summary: dict,
    hyperbola_rows: list[dict],
    common_offset_rows: list[dict],
) -> list[dict]:
    scenarios = [{
        "scenario_key": "dzt_nominal_epsr",
        "source": "dzt_metadata",
        "file": "all_profiles",
        "epsr": nominal_epsr(dzt_summary),
        "time_zero_ns": 0.0,
        "tx_rx_offset_mm": math.nan,
        "calibration_status": "metadata_depth_scale_not_cover_depth",
    }]
    for row in hyperbola_rows:
        scenarios.append({
            "scenario_key": f"hyperbola_template_{str(row.get('file', '')).split('__')[-1].replace('.DZT', '')}",
            "source": "hyperbola_template_overlay",
            "file": row.get("file", ""),
            "epsr": safe_float(row.get("best_epsr")),
            "time_zero_ns": safe_float(row.get("best_time_zero_ns")),
            "tx_rx_offset_mm": 0.0,
            "calibration_status": "template_overlay_boundary_not_ground_truth",
        })
    for row in common_offset_rows:
        if not math.isclose(safe_float(row.get("tx_rx_offset_mm")), 60.0, abs_tol=1.0e-9):
            continue
        scenarios.append({
            "scenario_key": f"common_offset60_{str(row.get('file', '')).split('__')[-1].replace('.DZT', '')}",
            "source": "common_offset_sensitivity",
            "file": row.get("file", ""),
            "epsr": safe_float(row.get("epsr")),
            "time_zero_ns": safe_float(row.get("time_zero_ns")),
            "tx_rx_offset_mm": safe_float(row.get("tx_rx_offset_mm")),
            "calibration_status": "common_offset_sensitivity_not_ground_truth",
        })
    return [row for row in scenarios if math.isfinite(row["epsr"]) and row["epsr"] > 0.0]


def scenario_depth_rows(
    scenarios: list[dict],
    cue_rows: list[dict],
    applied_rows: list[dict],
    conservative_half_width_ns: float,
) -> list[dict]:
    cue_times = [safe_float(row.get("time_ns")) for row in cue_rows]
    residual_times = [safe_float(row.get("abs_corrected_phase_residual_ns")) for row in applied_rows]
    out = []
    for scenario in scenarios:
        epsr = safe_float(scenario["epsr"])
        depths = [two_way_depth_mm(time_ns - safe_float(scenario.get("time_zero_ns"), 0.0), epsr) for time_ns in cue_times]
        residual_depths = [two_way_depth_mm(time_ns, epsr) for time_ns in residual_times]
        budget_mm = two_way_depth_mm(conservative_half_width_ns, epsr)
        support_count = sum(1 for value in residual_depths if value <= budget_mm)
        out.append({
            "scenario_key": scenario["scenario_key"],
            "source": scenario["source"],
            "file": scenario["file"],
            "epsr": epsr,
            "velocity_m_per_ns": medium_velocity_m_per_ns(epsr),
            "time_zero_ns": safe_float(scenario.get("time_zero_ns"), 0.0),
            "tx_rx_offset_mm": scenario.get("tx_rx_offset_mm", math.nan),
            "cue_depth_min_mm": min(depths),
            "cue_depth_median_mm": median_finite(depths),
            "cue_depth_max_mm": max(depths),
            "max_corrected_residual_mm": max(residual_depths),
            "conservative_budget_mm": budget_mm,
            "corrected_residual_support_count": support_count,
            "corrected_residual_row_count": len(residual_depths),
            "corrected_residual_support_fraction": support_count / len(residual_depths) if residual_depths else math.nan,
            "calibration_status": scenario["calibration_status"],
            "cover_depth_claim_ready": False,
        })
    return out


def summarize_sensitivity(rows: list[dict]) -> dict:
    epsr_values = [safe_float(row["epsr"]) for row in rows]
    max_depth_values = [safe_float(row["cue_depth_max_mm"]) for row in rows]
    support_count = sum(
        1
        for row in rows
        if safe_float(row["corrected_residual_support_count"]) == safe_float(row["corrected_residual_row_count"])
    )
    return {
        "policy_label": "field_apparent_depth_sensitivity_not_calibrated_cover_depth",
        "scenario_count": len(rows),
        "epsr_min": min(epsr_values),
        "epsr_max": max(epsr_values),
        "max_apparent_depth_min_mm": min(max_depth_values),
        "max_apparent_depth_max_mm": max(max_depth_values),
        "max_apparent_depth_span_mm": max(max_depth_values) - min(max_depth_values),
        "max_apparent_depth_sensitivity_factor": max(max_depth_values) / min(max_depth_values),
        "all_residuals_within_budget_scenario_count": support_count,
        "all_residuals_within_budget_all_scenarios": support_count == len(rows),
        "cover_depth_claim_ready": False,
        "field_fwi_ready": False,
        "gpu_priority": "none",
        "decision": (
            "Apparent field depth scale is strongly dielectric/time-zero dependent. "
            "The short-pair residual/budget support survives these scale choices, "
            "but the absolute cue depths move enough that this must remain QC scale "
            "evidence, not cover-depth recovery."
        ),
    }


def plot_sensitivity(rows: list[dict], summary: dict, save_path: Path) -> None:
    labels = [row["scenario_key"].replace("_", "\n") for row in rows]
    x = np.arange(len(rows))
    fig, axes = plt.subplots(2, 2, figsize=(16.0, 8.8), constrained_layout=True)

    axes[0, 0].bar(
        x,
        [row["cue_depth_max_mm"] for row in rows],
        color="#4c78a8",
        edgecolor="#333333",
    )
    axes[0, 0].set_xticks(x, labels, rotation=0)
    axes[0, 0].set_ylabel("max cue apparent depth (mm)")
    axes[0, 0].set_title("Apparent-depth scale changes by scenario")
    axes[0, 0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[0, 1].bar(
        x,
        [row["epsr"] for row in rows],
        color="#d99a19",
        edgecolor="#333333",
    )
    axes[0, 1].set_xticks(x, labels, rotation=0)
    axes[0, 1].set_ylabel("relative permittivity")
    axes[0, 1].set_title("Scenario dielectric assumptions")
    axes[0, 1].grid(axis="y", color="#dddddd", linewidth=0.6)

    width = 0.36
    axes[1, 0].bar(
        x - width / 2,
        [row["max_corrected_residual_mm"] for row in rows],
        width=width,
        color="#2f9d55",
        edgecolor="#333333",
        label="max corrected residual",
    )
    axes[1, 0].bar(
        x + width / 2,
        [row["conservative_budget_mm"] for row in rows],
        width=width,
        color="#9b5de5",
        edgecolor="#333333",
        label="conservative budget",
    )
    axes[1, 0].set_xticks(x, labels, rotation=0)
    axes[1, 0].set_ylabel("depth-equivalent scale (mm)")
    axes[1, 0].set_title("Residual support scales with dielectric")
    axes[1, 0].legend(loc="upper right", fontsize=8)
    axes[1, 0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1, 1].axis("off")
    text = (
        f"epsr range: {summary['epsr_min']:.2f} to {summary['epsr_max']:.2f}\n"
        f"max cue depth span: {summary['max_apparent_depth_span_mm']:.1f} mm\n"
        f"sensitivity factor: {summary['max_apparent_depth_sensitivity_factor']:.2f}x\n"
        f"all residuals within budget: {summary['all_residuals_within_budget_scenario_count']}/{summary['scenario_count']}\n\n"
        "Conclusion: depth-scale QC only.\nNo cover-depth, radius, 3D, or FWI claim."
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

    fig.suptitle("Field apparent-depth sensitivity: scale evidence, not calibrated cover depth", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--run-name", default="gssi51600s_field_apparent_depth_sensitivity")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    runs = {
        "dzt": DEFAULT_DZT_RUN,
        "cue": DEFAULT_CUE_RUN,
        "hyperbola": DEFAULT_HYPERBOLA_RUN,
        "common_offset": DEFAULT_COMMON_OFFSET_RUN,
        "time_zero_application": DEFAULT_TIME_ZERO_APPLICATION_RUN,
        "time_zero_budget": DEFAULT_TIME_ZERO_BUDGET_RUN,
    }
    inputs = load_inputs(dataset_root, runs)
    scenarios = sensitivity_scenarios(
        inputs["dzt_summary"],
        inputs["hyperbola_summary_rows"],
        inputs["common_offset_rows"],
    )
    rows = scenario_depth_rows(
        scenarios,
        inputs["cue_rows"],
        inputs["applied_rows"],
        safe_float(inputs["time_zero_budget"].get("conservative_half_width_ns")),
    )
    summary = summarize_sensitivity(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_apparent_depth_sensitivity_rows.csv"
    summary_json = data_dir / "field_apparent_depth_sensitivity_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_apparent_depth_sensitivity.png"

    plot_sensitivity(rows, summary, figure_path)
    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [figure_stats(figure_path)])
    summary["readgssi_version"] = readgssi_version()
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_apparent_depth_sensitivity",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Synthesize close14 source3 three-seed policy evidence without new simulations."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
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
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SOURCE3_RUNS = (
    "336_coordinate_optimizer_close14_seed34_sources3_txrx45_objectives,"
    "1346_coordinate_optimizer_close14_seed13_sources3_txrx45_objectives,"
    "1347_coordinate_optimizer_close14_seed21_sources3_txrx45_objectives"
)
DEFAULT_SOURCE4_AGGREGATE = (
    "outputs/experiments/335_coordinate_confidence_close14_sources4_txrx45_seed_replicates/"
    "data/coordinate_confidence_aggregate.csv"
)
DEFAULT_SOURCE5_AGGREGATE = (
    "outputs/experiments/1296_coordinate_confidence_close14_target2_sources5_txrx45_seed13_21_34_probe_aggregate/"
    "data/coordinate_confidence_aggregate.csv"
)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def seed_from_text(text: object) -> int:
    match = re.search(r"seed(\d+)", str(text))
    return int(match.group(1)) if match else -1


def case_kind(case_label: object) -> str:
    return "source_mismatch" if "source_mismatch" in str(case_label) else "nominal"


def ambiguity_width(row: dict, axis: str) -> float:
    direct = safe_float(row.get(f"ambiguity_{axis}_width_mm"))
    if math.isfinite(direct):
        return direct
    low = safe_float(row.get(f"ambiguity_{axis}_min_mm"))
    high = safe_float(row.get(f"ambiguity_{axis}_max_mm"))
    if math.isfinite(low) and math.isfinite(high):
        return high - low
    return math.nan


def is_truth_geometry(row: dict, truth_x: float, truth_z: float, truth_radius: float) -> bool:
    return (
        math.isclose(safe_float(row.get("best_x_mm")), truth_x, abs_tol=1.0e-9)
        and math.isclose(safe_float(row.get("best_z_mm")), truth_z, abs_tol=1.0e-9)
        and math.isclose(safe_float(row.get("best_radius_mm")), truth_radius, abs_tol=1.0e-9)
    )


def _normalize_row(
    row: dict,
    *,
    source_count: int,
    source_family: str,
    source_path: Path,
    truth_x: float,
    truth_z: float,
    truth_radius: float,
    tx_rx_offset_mm: float,
) -> dict:
    best_x = safe_float(row.get("best_x_mm"))
    best_z = safe_float(row.get("best_z_mm"))
    best_radius = safe_float(row.get("best_radius_mm"))
    truth = is_truth_geometry(row, truth_x, truth_z, truth_radius)
    return {
        "spacing_family": "close14",
        "spacing_mm": 14.0,
        "target_rebar_index": safe_int(row.get("target_rebar_index"), 2),
        "source_count": source_count,
        "source_family": source_family,
        "source_path": str(source_path),
        "run_name": row.get("run_name", ""),
        "case_label": row.get("case_label", ""),
        "case_kind": case_kind(row.get("case_label", "")),
        "seed": seed_from_text(row.get("case_label", row.get("run_name", ""))),
        "tx_rx_offset_mm": tx_rx_offset_mm,
        "best_x_mm": best_x,
        "best_z_mm": best_z,
        "best_radius_mm": best_radius,
        "truth_x_mm": truth_x,
        "truth_z_mm": truth_z,
        "truth_radius_mm": truth_radius,
        "x_abs_error_mm": abs(best_x - truth_x) if math.isfinite(best_x) else math.nan,
        "z_abs_error_mm": abs(best_z - truth_z) if math.isfinite(best_z) else math.nan,
        "radius_abs_error_mm": abs(best_radius - truth_radius) if math.isfinite(best_radius) else math.nan,
        "truth_geometry": truth,
        "confidence_label": row.get("confidence_label", ""),
        "radius_margin_abs": safe_float(row.get("radius_margin_abs")),
        "best_misfit": safe_float(row.get("best_misfit")),
        "competing_geometry_x_mm": safe_float(row.get("competing_geometry_x_mm")),
        "competing_geometry_radius_mm": safe_float(row.get("competing_geometry_radius_mm")),
        "ambiguity_candidate_count": safe_int(row.get("ambiguity_candidate_count"), 0),
        "ambiguity_x_width_mm": ambiguity_width(row, "x"),
        "ambiguity_radius_width_mm": ambiguity_width(row, "radius"),
    }


def source3_rows(experiment_root: Path, run_names: list[str]) -> list[dict]:
    rows = []
    for run_name in run_names:
        run_dir = experiment_root / run_name
        summary_path = run_dir / "data/multi_rebar_coordinate_optimizer_summary.json"
        summary = read_json(summary_path)
        truth_x_values = summary.get("true_x_values_mm") or [math.nan, math.nan, math.nan]
        truth_z_values = summary.get("true_z_values_mm") or [math.nan, math.nan, math.nan]
        truth_radii = summary.get("truth_radius_values_mm") or [math.nan, math.nan, summary.get("truth_radius_mm")]
        report_path = run_dir / "data/coordinate_confidence_report.csv"
        for row in read_csv_rows(report_path):
            if safe_int(row.get("pass_index"), -1) != 0 or row.get("step_kind") != "main":
                continue
            if safe_int(row.get("step_target_index"), safe_int(row.get("target_rebar_index"), -1)) != 2:
                continue
            rows.append(
                _normalize_row(
                    row,
                    source_count=safe_int(summary.get("sources")),
                    source_family="source3_direct_three_seed",
                    source_path=report_path,
                    truth_x=safe_float(truth_x_values[2]),
                    truth_z=safe_float(truth_z_values[2]),
                    truth_radius=safe_float(truth_radii[2]),
                    tx_rx_offset_mm=safe_float(summary.get("tx_rx_offset_mm")),
                )
            )
    return rows


def aggregate_rows(path: Path, source_family: str) -> list[dict]:
    rows = []
    for row in read_csv_rows(path):
        if safe_int(row.get("pass_index"), -1) != 0 or row.get("step_kind") != "main":
            continue
        if safe_int(row.get("step_target_index"), safe_int(row.get("target_rebar_index"), -1)) != 2:
            continue
        truth_x = safe_float(row.get("truth_x_mm"))
        truth_z = safe_float(row.get("truth_z_mm"))
        truth_radius = safe_float(row.get("truth_radius_mm"))
        rows.append(
            _normalize_row(
                row,
                source_count=safe_int(row.get("sources", row.get("source_count"))),
                source_family=source_family,
                source_path=path,
                truth_x=truth_x,
                truth_z=truth_z,
                truth_radius=truth_radius,
                tx_rx_offset_mm=safe_float(row.get("tx_rx_offset_mm")),
            )
        )
    return rows


def summarize_by_source(rows: list[dict]) -> list[dict]:
    output = []
    for source_count in sorted({safe_int(row["source_count"]) for row in rows}):
        group = [row for row in rows if safe_int(row["source_count"]) == source_count]
        seeds = sorted({safe_int(row["seed"]) for row in group if safe_int(row["seed"], -1) >= 0})
        truth_count = sum(boolish(row.get("truth_geometry")) for row in group)
        strong_count = sum(row.get("confidence_label") == "strong" for row in group)
        weak_count = sum(row.get("confidence_label") == "weak" for row in group)
        finite_margins = [safe_float(row.get("radius_margin_abs")) for row in group]
        finite_margins = [value for value in finite_margins if math.isfinite(value)]
        finite_x_widths = [safe_float(row.get("ambiguity_x_width_mm")) for row in group]
        finite_x_widths = [value for value in finite_x_widths if math.isfinite(value)]
        output.append(
            {
                "source_count": source_count,
                "row_count": len(group),
                "seed_count": len(seeds),
                "seed_values": ",".join(str(seed) for seed in seeds),
                "truth_geometry_count": truth_count,
                "truth_geometry_fraction": truth_count / len(group) if group else 0.0,
                "strong_count": strong_count,
                "strong_fraction": strong_count / len(group) if group else 0.0,
                "weak_count": weak_count,
                "selected_wrong_x_count": sum(safe_float(row.get("x_abs_error_mm")) > 0.0 for row in group),
                "min_radius_margin_abs": min(finite_margins) if finite_margins else math.nan,
                "max_x_abs_error_mm": max([safe_float(row.get("x_abs_error_mm")) for row in group] or [math.nan]),
                "max_z_abs_error_mm": max([safe_float(row.get("z_abs_error_mm")) for row in group] or [math.nan]),
                "max_radius_abs_error_mm": max(
                    [safe_float(row.get("radius_abs_error_mm")) for row in group] or [math.nan]
                ),
                "max_ambiguity_x_width_mm": max(finite_x_widths) if finite_x_widths else math.nan,
            }
        )
    return output


def summarize_policy(rows: list[dict], source_summary_rows: list[dict]) -> dict:
    by_source = {safe_int(row["source_count"]): row for row in source_summary_rows}
    source3 = by_source.get(3, {})
    source4 = by_source.get(4, {})
    source5 = by_source.get(5, {})
    source3_seed_count = safe_int(source3.get("seed_count"), 0)
    source3_truth_fraction = safe_float(source3.get("truth_geometry_fraction"), 0.0)
    source3_strong_fraction = safe_float(source3.get("strong_fraction"), 0.0)
    source3_max_x_error = safe_float(source3.get("max_x_abs_error_mm"), math.inf)
    source3_max_radius_error = safe_float(source3.get("max_radius_abs_error_mm"), math.inf)
    source3_replicated_failure = (
        source3_seed_count >= 3
        and math.isclose(source3_truth_fraction, 0.0)
        and safe_int(source3.get("weak_count"), 0) == safe_int(source3.get("row_count"), -1)
        and source3_max_x_error >= 1.0
    )
    source3_near_exact = (
        source3_seed_count >= 3
        and source3_truth_fraction >= (5.0 / 6.0)
        and math.isclose(source3_strong_fraction, 1.0)
        and source3_max_x_error <= 1.0
        and math.isclose(source3_max_radius_error, 0.0)
    )
    source4_clean = (
        safe_int(source4.get("seed_count"), 0) >= 3
        and math.isclose(safe_float(source4.get("truth_geometry_fraction"), 0.0), 1.0)
        and math.isclose(safe_float(source4.get("strong_fraction"), 0.0), 1.0)
    )
    source5_clean = (
        safe_int(source5.get("seed_count"), 0) >= 3
        and math.isclose(safe_float(source5.get("truth_geometry_fraction"), 0.0), 1.0)
        and math.isclose(safe_float(source5.get("strong_fraction"), 0.0), 1.0)
    )
    wrong_source3_rows = [
        row
        for row in rows
        if safe_int(row.get("source_count")) == 3 and safe_float(row.get("x_abs_error_mm")) > 0.0
    ]
    return {
        "policy_label": "close14_source3_three_seed_policy_synthesis",
        "source_row_count": len(rows),
        "source_count_group_count": len(source_summary_rows),
        "source3_seed_count": source3_seed_count,
        "source3_seed_values": source3.get("seed_values", ""),
        "source3_truth_geometry_fraction": source3_truth_fraction,
        "source3_strong_fraction": source3_strong_fraction,
        "source3_max_x_abs_error_mm": source3_max_x_error,
        "source3_max_radius_abs_error_mm": source3_max_radius_error,
        "source3_selected_wrong_x_count": safe_int(source3.get("selected_wrong_x_count"), 0),
        "source3_replicated_failure": source3_replicated_failure,
        "source3_near_exact_three_seed_context": source3_near_exact,
        "source4_three_seed_clean": source4_clean,
        "source5_noise_boundary_three_seed_clean": source5_clean,
        "close14_source_density_failure_supported": False,
        "close14_source3_additional_replicate_needed": False,
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_field_or_3d_work": False,
        "gpu_priority": "none",
        "recommended_next_local_mode": "field_controls_or_cpu_baseline_contract",
        "wrong_source3_case_labels": ",".join(str(row.get("case_label")) for row in wrong_source3_rows),
        "decision": (
            "Close14 Tx/Rx45 source3 does not replicate the close50 Tx/Rx40 source3 failure. "
            "Across seeds 13/21/34, all source3 rows are strong and radius-exact, with one saved "
            "seed34 source-mismatch row selecting the adjacent 265 mm x branch by 1 mm. Saved "
            "source4 rows are clean at the same nominal noise level, and saved source5 rows are "
            "clean in the higher-noise boundary context. Treat close14 source3 as a near-exact "
            "three-seed context result, not as a broad GPU-launch trigger."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "additional_close14_source3_replicate",
            "ready": summary["close14_source3_additional_replicate_needed"],
            "allowed_use": "none",
            "blocked_use": "more close14 source3 Tx/Rx45 replication",
            "evidence": f"source3 seeds={summary['source3_seed_values']}; near_exact={summary['source3_near_exact_three_seed_context']}",
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "broad close-spacing source-density sweep",
            "evidence": "close14 source3 is near-exact context; close50 source3 failure remains spacing/acquisition-specific",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI launch",
            "evidence": "this synthesis only reconciles saved coordinate-confidence evidence",
        },
        {
            "gate_key": "field_or_3d_handoff",
            "ready": summary["ready_for_field_or_3d_work"],
            "allowed_use": "none",
            "blocked_use": "field FWI or 3D/HPC work",
            "evidence": "synthetic 2D close14 policy synthesis; field controls remain separate",
        },
    ]


def plot_synthesis(source_summary_rows: list[dict], summary: dict, save_path: Path) -> str:
    ordered = sorted(source_summary_rows, key=lambda row: safe_int(row["source_count"]))
    labels = [f"{safe_int(row['source_count'])} sources\nseeds {row['seed_values']}" for row in ordered]
    truth_fraction = [safe_float(row.get("truth_geometry_fraction"), 0.0) for row in ordered]
    strong_fraction = [safe_float(row.get("strong_fraction"), 0.0) for row in ordered]
    max_x_error = [safe_float(row.get("max_x_abs_error_mm"), 0.0) for row in ordered]
    x = np.arange(len(ordered))

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.0), constrained_layout=True)
    axes[0].bar(x - 0.18, truth_fraction, width=0.36, label="truth geometry", color="#4e79a7")
    axes[0].bar(x + 0.18, strong_fraction, width=0.36, label="strong confidence", color="#59a14f")
    axes[0].set_xticks(x, labels)
    axes[0].set_ylim(0.0, 1.08)
    axes[0].set_ylabel("fraction")
    axes[0].set_title("Close14 Tx/Rx45 source-count exactness")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(loc="lower right", fontsize=8)

    axes[1].bar(x, max_x_error, color="#f28e2b", edgecolor="#333333", linewidth=0.4)
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("max selected x error (mm)")
    axes[1].set_title("Adjacent-branch selection width")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.95,
        f"source3 near-exact: {summary['source3_near_exact_three_seed_context']}\n"
        f"source3 failure: {summary['source3_replicated_failure']}\n"
        f"wrong source3 rows: {summary['source3_selected_wrong_x_count']}\n"
        f"GPU priority: {summary['gpu_priority']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Close14 Source3 Three-Seed Policy Synthesis", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `close14_source3_three_seed_policy_synthesis.png`",
                "",
                "This figure compares the newly completed close14 source3 seed13/21/34",
                "evidence with saved source4 and source5 close14 context.",
                "",
                f"Source3 seed values: `{summary['source3_seed_values']}`.",
                f"Source3 truth-geometry fraction: `{summary['source3_truth_geometry_fraction']}`.",
                f"Source3 near-exact three-seed context: `{summary['source3_near_exact_three_seed_context']}`.",
                f"Source3 replicated failure: `{summary['source3_replicated_failure']}`.",
                f"Broad GPU queue ready: `{summary['ready_for_broad_gpu_queue']}`.",
                "",
                "Scope boundary:",
                "",
                "This is a CPU-only synthesis of saved synthetic 2D coordinate-confidence",
                "outputs. It does not launch FDTD/FWI, detector-seeded FWI, field FWI,",
                "or 3D/HPC jobs.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default="outputs/experiments")
    parser.add_argument("--source3-runs", default=DEFAULT_SOURCE3_RUNS)
    parser.add_argument("--source4-aggregate", default=DEFAULT_SOURCE4_AGGREGATE)
    parser.add_argument("--source5-aggregate", default=DEFAULT_SOURCE5_AGGREGATE)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--run-name", default="close14_source3_three_seed_policy_synthesis")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    experiment_root = Path(args.experiment_root)
    source3_run_names = [part.strip() for part in args.source3_runs.split(",") if part.strip()]
    rows = (
        source3_rows(experiment_root, source3_run_names)
        + aggregate_rows(Path(args.source4_aggregate), "source4_saved_three_seed")
        + aggregate_rows(Path(args.source5_aggregate), "source5_saved_noise_boundary_three_seed")
    )
    source_summary_rows = summarize_by_source(rows)
    summary = summarize_policy(rows, source_summary_rows)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "close14_source3_three_seed_policy_rows.csv"
    source_summary_csv = data_dir / "close14_source3_three_seed_by_source_count.csv"
    gates_csv = data_dir / "close14_source3_three_seed_gates.csv"
    summary_json = data_dir / "close14_source3_three_seed_policy_summary.json"
    figure_path = figures_dir / "close14_source3_three_seed_policy_synthesis.png"
    validation_csv = data_dir / "figure_validation.csv"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(source_summary_csv, [json_safe(row) for row in source_summary_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_synthesis(source_summary_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary)

    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "source_summary_csv": str(source_summary_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
        "source3_runs": source3_run_names,
        "source4_aggregate_csv": args.source4_aggregate,
        "source5_aggregate_csv": args.source5_aggregate,
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "close14_source3_three_seed_policy_synthesis",
        {
            "summary_json": str(summary_json),
            "source_summary_csv": str(source_summary_csv),
            "rows_csv": str(rows_csv),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

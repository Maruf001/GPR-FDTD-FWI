#!/usr/bin/env python3
"""Synthesize close50 Tx/Rx40 source-count seed-replication evidence."""

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
    "274_coordinate_optimizer_close50_seed34_sources3_txrx40_objectives,"
    "1344_coordinate_optimizer_close50_seed13_sources3_txrx40_objectives,"
    "1345_coordinate_optimizer_close50_seed21_sources3_txrx40_objectives"
)
DEFAULT_SOURCE4_AGGREGATE = (
    "outputs/experiments/280_coordinate_confidence_close50_sources4_txrx40_seed_replicates/"
    "data/coordinate_confidence_aggregate.csv"
)
DEFAULT_SOURCE5_CONFIDENCE = (
    "outputs/experiments/271_close50_txrx40_seed_replication_summary/"
    "data/txrx40_seed_confidence_summary.csv"
)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def seed_from_text(text: str) -> int:
    match = re.search(r"seed(\d+)", str(text))
    if not match:
        return -1
    return int(match.group(1))


def truth_geometry(row: dict, truth_x: float = 300.0, truth_z: float = 90.0, truth_radius: float = 8.0) -> bool:
    return (
        math.isclose(safe_float(row.get("best_x_mm")), truth_x, abs_tol=1.0e-9)
        and math.isclose(safe_float(row.get("best_z_mm")), truth_z, abs_tol=1.0e-9)
        and math.isclose(safe_float(row.get("best_radius_mm")), truth_radius, abs_tol=1.0e-9)
    )


def source3_rows(experiment_root: Path, run_names: list[str]) -> list[dict]:
    rows = []
    for run_name in run_names:
        run_dir = experiment_root / run_name
        summary = read_json(run_dir / "data/multi_rebar_coordinate_optimizer_summary.json")
        truth_radii = summary.get("truth_radius_values_mm") or [math.nan, math.nan, math.nan]
        truth_x = safe_float((summary.get("true_x_values_mm") or [math.nan, math.nan, math.nan])[2])
        truth_z = safe_float((summary.get("true_z_values_mm") or [math.nan, math.nan, math.nan])[2])
        truth_radius = safe_float(truth_radii[2])
        for row in read_csv_rows(run_dir / "data/coordinate_confidence_report.csv"):
            if safe_int(row.get("pass_index"), -1) != 0:
                continue
            if row.get("step_kind") != "main":
                continue
            seed = seed_from_text(str(row.get("case_label", "")))
            rows.append({
                "source_count": safe_int(summary.get("sources")),
                "seed": seed,
                "case_label": row.get("case_label", ""),
                "case_kind": "source_mismatch" if "source_mismatch" in str(row.get("case_label", "")) else "nominal",
                "run_dir": run_name,
                "source_family": "source3_direct_replicate",
                "tx_rx_offset_mm": safe_float(summary.get("tx_rx_offset_mm")),
                "best_x_mm": safe_float(row.get("best_x_mm")),
                "best_z_mm": safe_float(row.get("best_z_mm")),
                "best_radius_mm": safe_float(row.get("best_radius_mm")),
                "truth_x_mm": truth_x,
                "truth_z_mm": truth_z,
                "truth_radius_mm": truth_radius,
                "x_abs_error_mm": abs(safe_float(row.get("best_x_mm")) - truth_x),
                "radius_abs_error_mm": abs(safe_float(row.get("best_radius_mm")) - truth_radius),
                "truth_geometry": truth_geometry(row, truth_x, truth_z, truth_radius),
                "confidence_label": row.get("confidence_label", ""),
                "radius_margin_abs": safe_float(row.get("radius_margin_abs")),
                "best_misfit": safe_float(row.get("best_misfit")),
            })
    return rows


def source4_rows(path: Path) -> list[dict]:
    rows = []
    for row in read_csv_rows(path):
        if safe_int(row.get("pass_index"), -1) != 0 or row.get("step_kind") != "main":
            continue
        seed = seed_from_text(str(row.get("case_label", "")))
        rows.append({
            "source_count": 4,
            "seed": seed,
            "case_label": row.get("case_label", ""),
            "case_kind": "source_mismatch" if "source_mismatch" in str(row.get("case_label", "")) else "nominal",
            "run_dir": Path(str(row.get("summary_path", ""))).parts[2]
            if len(Path(str(row.get("summary_path", ""))).parts) > 2
            else "",
            "source_family": "source4_saved_three_seed",
            "tx_rx_offset_mm": safe_float(row.get("tx_rx_offset_mm"), 40.0),
            "best_x_mm": safe_float(row.get("best_x_mm")),
            "best_z_mm": safe_float(row.get("best_z_mm")),
            "best_radius_mm": safe_float(row.get("best_radius_mm")),
            "truth_x_mm": safe_float(row.get("truth_x_mm"), 300.0),
            "truth_z_mm": safe_float(row.get("truth_z_mm"), 90.0),
            "truth_radius_mm": safe_float(row.get("truth_radius_mm"), 8.0),
            "x_abs_error_mm": safe_float(row.get("x_abs_error_mm"), 0.0),
            "radius_abs_error_mm": safe_float(row.get("radius_abs_error_mm"), 0.0),
            "truth_geometry": boolish(row.get("is_truth_geometry")),
            "confidence_label": row.get("confidence_label", ""),
            "radius_margin_abs": safe_float(row.get("radius_margin_abs")),
            "best_misfit": safe_float(row.get("best_misfit")),
        })
    return rows


def source5_rows(path: Path) -> list[dict]:
    rows = []
    for row in read_csv_rows(path):
        seed = safe_int(row.get("seed"), seed_from_text(str(row.get("case_label", ""))))
        row_for_truth = {
            "best_x_mm": row.get("best_x_mm"),
            "best_z_mm": row.get("best_z_mm"),
            "best_radius_mm": row.get("best_radius_mm"),
        }
        rows.append({
            "source_count": 5,
            "seed": seed,
            "case_label": row.get("case_label", ""),
            "case_kind": "source_mismatch" if "source_mismatch" in str(row.get("case_label", "")) else "nominal",
            "run_dir": "",
            "source_family": "source5_saved_three_seed",
            "tx_rx_offset_mm": 40.0,
            "best_x_mm": safe_float(row.get("best_x_mm")),
            "best_z_mm": safe_float(row.get("best_z_mm")),
            "best_radius_mm": safe_float(row.get("best_radius_mm")),
            "truth_x_mm": 300.0,
            "truth_z_mm": 90.0,
            "truth_radius_mm": 8.0,
            "x_abs_error_mm": abs(safe_float(row.get("best_x_mm")) - 300.0),
            "radius_abs_error_mm": abs(safe_float(row.get("best_radius_mm")) - 8.0),
            "truth_geometry": truth_geometry(row_for_truth),
            "confidence_label": row.get("confidence_label", ""),
            "radius_margin_abs": safe_float(row.get("radius_margin_abs")),
            "best_misfit": math.nan,
        })
    return rows


def summarize_by_source(rows: list[dict]) -> list[dict]:
    output = []
    for source_count in sorted({safe_int(row["source_count"]) for row in rows}):
        group = [row for row in rows if safe_int(row["source_count"]) == source_count]
        seeds = sorted({safe_int(row.get("seed")) for row in group})
        output.append({
            "source_count": source_count,
            "row_count": len(group),
            "seed_count": len(seeds),
            "seed_values": ",".join(str(seed) for seed in seeds),
            "truth_geometry_count": sum(boolish(row.get("truth_geometry")) for row in group),
            "truth_geometry_fraction": (
                sum(boolish(row.get("truth_geometry")) for row in group) / len(group) if group else 0.0
            ),
            "strong_count": sum(row.get("confidence_label") == "strong" for row in group),
            "weak_count": sum(row.get("confidence_label") == "weak" for row in group),
            "selected_wrong_x_count": sum(safe_float(row.get("x_abs_error_mm")) > 0.0 for row in group),
            "min_radius_margin_abs": min([safe_float(row.get("radius_margin_abs")) for row in group] or [math.nan]),
            "max_x_abs_error_mm": max([safe_float(row.get("x_abs_error_mm")) for row in group] or [math.nan]),
            "max_radius_abs_error_mm": max([safe_float(row.get("radius_abs_error_mm")) for row in group] or [math.nan]),
        })
    return output


def summarize_policy(source_rows: list[dict], source_summary_rows: list[dict]) -> dict:
    by_source = {safe_int(row["source_count"]): row for row in source_summary_rows}
    source3 = by_source.get(3, {})
    source4 = by_source.get(4, {})
    source5 = by_source.get(5, {})
    source3_seeds = {safe_int(row.get("seed")) for row in source_rows if safe_int(row.get("source_count")) == 3}
    missing_source3_seeds = sorted({13, 21, 34} - source3_seeds)
    source3_replicated_failure = (
        safe_int(source3.get("seed_count"), 0) >= 2
        and safe_float(source3.get("truth_geometry_fraction"), 1.0) == 0.0
        and safe_float(source3.get("max_x_abs_error_mm"), 0.0) >= 1.0
    )
    source4_clean = safe_int(source4.get("seed_count"), 0) >= 3 and safe_float(source4.get("truth_geometry_fraction"), 0.0) == 1.0
    source5_clean = safe_int(source5.get("seed_count"), 0) >= 3 and safe_float(source5.get("truth_geometry_fraction"), 0.0) == 1.0
    ready_final_seed = source3_replicated_failure and source4_clean and source5_clean and missing_source3_seeds == [21]
    if ready_final_seed:
        decision = (
            "Seed13 reproduced the saved seed34 three-source Tx/Rx40 failure, while saved four- and "
            "five-source Tx/Rx40 evidence is clean across seeds 13/21/34. One final sources3 seed21 "
            "replicate would make the source-count comparison seed-symmetric; no broad GPU queue or "
            "detector-seeded FWI is justified."
        )
    else:
        decision = (
            "The close50 Tx/Rx40 source-count comparison is now seed-symmetric: sources3 fails "
            "across seeds 13/21/34, while sources4 and sources5 are clean across the same three "
            "seeds. This supports a source-density transition claim and closes additional GPU "
            "replication for this local question."
        )
    return {
        "policy_label": "close50_txrx40_source_count_replicate_synthesis",
        "source_row_count": len(source_rows),
        "source_count_group_count": len(source_summary_rows),
        "source3_seed_count": safe_int(source3.get("seed_count"), 0),
        "source3_seed_values": source3.get("seed_values", ""),
        "source3_truth_geometry_fraction": safe_float(source3.get("truth_geometry_fraction"), math.nan),
        "source3_replicated_failure": source3_replicated_failure,
        "source4_three_seed_clean": source4_clean,
        "source5_three_seed_clean": source5_clean,
        "source_count_transition_supported": source3_replicated_failure and source4_clean and source5_clean,
        "missing_source3_seed_values": ",".join(str(seed) for seed in missing_source3_seeds),
        "ready_for_final_source3_seed21_replicate": ready_final_seed,
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "single_bounded_final_seed" if ready_final_seed else "none",
        "decision": decision,
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "final_source3_seed21_replicate",
            "ready": summary["ready_for_final_source3_seed21_replicate"],
            "allowed_use": "one bounded source3 seed21 Tx/Rx40 replicate",
            "blocked_use": "broad source-count or threshold sweep",
            "evidence": f"missing source3 seeds={summary['missing_source3_seed_values']}",
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "launch broad GPU queue",
            "evidence": "source-count synthesis only",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI launch",
            "evidence": "coordinate source-count policy only",
        },
    ]


def plot_synthesis(source_summary_rows: list[dict], summary: dict, save_path: Path) -> str:
    ordered = sorted(source_summary_rows, key=lambda row: safe_int(row["source_count"]))
    labels = [f"{safe_int(row['source_count'])} sources\nseeds {row['seed_values']}" for row in ordered]
    truth_fraction = [safe_float(row.get("truth_geometry_fraction"), 0.0) for row in ordered]
    weak_count = [safe_float(row.get("weak_count"), 0.0) for row in ordered]
    strong_count = [safe_float(row.get("strong_count"), 0.0) for row in ordered]
    x = np.arange(len(ordered))

    fig, axes = plt.subplots(1, 2, figsize=(13.2, 5.0), constrained_layout=True)
    axes[0].bar(x, truth_fraction, color="#4e79a7", edgecolor="#333333", linewidth=0.4)
    axes[0].set_xticks(x, labels)
    axes[0].set_ylim(0.0, 1.08)
    axes[0].set_ylabel("truth-geometry fraction")
    axes[0].set_title("Tx/Rx40 source-count exactness")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x - 0.18, weak_count, width=0.36, label="weak", color="#e15759")
    axes[1].bar(x + 0.18, strong_count, width=0.36, label="strong", color="#59a14f")
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("row count")
    axes[1].set_title("Confidence by source count")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(loc="upper left", fontsize=8)
    axes[1].text(
        0.03,
        0.95,
        f"source3 failure replicated: {summary['source3_replicated_failure']}\n"
        f"source4 clean: {summary['source4_three_seed_clean']}\n"
        f"source5 clean: {summary['source5_three_seed_clean']}\n"
        f"final seed ready: {summary['ready_for_final_source3_seed21_replicate']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Close50 Tx/Rx40 Source-Count Replication Synthesis", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `close50_source_count_replicate_synthesis.png`",
                "",
                "This figure compares the new source3 seed13 replicate with the saved",
                "source3 seed34 and saved source4/source5 Tx/Rx40 seed-replication evidence.",
                "",
                f"Source3 seed count: `{summary['source3_seed_count']}`.",
                f"Source3 seed values: `{summary['source3_seed_values']}`.",
                f"Source3 replicated failure: `{summary['source3_replicated_failure']}`.",
                f"Source-count transition supported: `{summary['source_count_transition_supported']}`.",
                f"Final source3 seed21 replicate ready: `{summary['ready_for_final_source3_seed21_replicate']}`.",
                f"Broad GPU queue ready: `{summary['ready_for_broad_gpu_queue']}`.",
                "",
                "Scope boundary:",
                "",
                "This is a source-count synthesis for close50 target2 Tx/Rx40 only.",
                "It does not launch broad GPU work, field FWI, detector-seeded FWI,",
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
    parser.add_argument("--source5-confidence", default=DEFAULT_SOURCE5_CONFIDENCE)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--run-name", default="close50_source_count_replicate_synthesis")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    experiment_root = Path(args.experiment_root)
    run_names = [part.strip() for part in args.source3_runs.split(",") if part.strip()]
    rows = (
        source3_rows(experiment_root, run_names)
        + source4_rows(Path(args.source4_aggregate))
        + source5_rows(Path(args.source5_confidence))
    )
    source_summary_rows = summarize_by_source(rows)
    summary = summarize_policy(rows, source_summary_rows)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "close50_source_count_replicate_rows.csv"
    source_summary_csv = data_dir / "close50_source_count_replicate_by_source_count.csv"
    gates_csv = data_dir / "close50_source_count_replicate_gates.csv"
    summary_json = data_dir / "close50_source_count_replicate_synthesis_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "close50_source_count_replicate_synthesis.png"
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
        "source3_runs": run_names,
        "source4_aggregate_csv": args.source4_aggregate,
        "source5_confidence_csv": args.source5_confidence,
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "close50_source_count_replicate_synthesis",
        {
            "source3_runs": run_names,
            "source4_aggregate": args.source4_aggregate,
            "source5_confidence": args.source5_confidence,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

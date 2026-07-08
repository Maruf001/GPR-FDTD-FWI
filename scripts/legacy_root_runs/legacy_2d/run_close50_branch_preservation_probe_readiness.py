#!/usr/bin/env python3
"""Score close50 branch-preservation cases for a bounded GPU follow-up."""

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


DEFAULT_ACTIONABILITY_ROWS = (
    "outputs/summary_tables/095_local_2d_branch_preservation_actionability/"
    "data/local_2d_branch_preservation_actionability_rows.csv"
)
DEFAULT_THRESHOLD_SUMMARY = (
    "outputs/summary_tables/096_local_2d_branch_preservation_threshold_sensitivity/"
    "data/local_2d_branch_preservation_threshold_sensitivity_summary.json"
)
DEFAULT_BOUNDARY_ROWS = (
    "outputs/experiments/1338_close50_sampling_boundary_synthesis/"
    "data/close50_sampling_boundary_rows.csv"
)
DEFAULT_BOUNDARY_SUMMARY = (
    "outputs/experiments/1338_close50_sampling_boundary_synthesis/"
    "data/close50_sampling_boundary_synthesis_summary.json"
)
DEFAULT_SOURCE_COUNT_AGGREGATE = (
    "outputs/experiments/277_coordinate_confidence_aggregate_close50_txrx40_sources3_4_5_seed34/"
    "data/coordinate_confidence_aggregate.csv"
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


def candidate_rows(path: Path, case_label: str) -> list[dict]:
    rows = [row for row in read_csv_rows(path) if not case_label or row.get("case_label") == case_label]
    for row in rows:
        row["misfit"] = safe_float(row.get("misfit"))
        row["x_mm"] = safe_float(row.get("x_mm"))
        row["z_mm"] = safe_float(row.get("z_mm"))
        row["radius_mm"] = safe_float(row.get("radius_mm"))
    return sorted(rows, key=lambda row: row["misfit"])


def best_row_for_x(rows: list[dict], x_mm: float) -> dict:
    matches = [row for row in rows if math.isclose(safe_float(row.get("x_mm")), x_mm, abs_tol=1.0e-9)]
    if not matches:
        return {}
    return min(matches, key=lambda row: safe_float(row.get("misfit"), math.inf))


def boundary_by_offset(boundary_rows: list[dict]) -> dict[float, dict]:
    indexed: dict[float, dict] = {}
    for row in boundary_rows:
        if row.get("sampling_family") != "nearest_receiver":
            continue
        offset = safe_float(row.get("tx_rx_offset_mm"))
        if math.isfinite(offset):
            indexed[offset] = row
    return indexed


def source_count_rows(path: Path) -> list[dict]:
    if not Path(path).exists():
        return []
    rows = read_csv_rows(Path(path))
    output = []
    for row in rows:
        if safe_int(row.get("pass_index"), -1) != 0:
            continue
        if str(row.get("step_kind", "")) != "main":
            continue
        output.append(row)
    return output


def source_count_context(rows: list[dict]) -> dict[int, dict]:
    grouped: dict[int, list[dict]] = {}
    for row in rows:
        sources = safe_int(row.get("sources"), -1)
        if sources > 0:
            grouped.setdefault(sources, []).append(row)
    context = {}
    for sources, group in sorted(grouped.items()):
        truth_geometry = sum(boolish(row.get("is_truth_geometry")) for row in group)
        strong = sum(str(row.get("confidence_label", "")) == "strong" for row in group)
        weak = sum(str(row.get("confidence_label", "")) == "weak" for row in group)
        context[sources] = {
            "source_count": sources,
            "row_count": len(group),
            "truth_geometry_count": truth_geometry,
            "truth_geometry_fraction": truth_geometry / len(group) if group else 0.0,
            "strong_count": strong,
            "weak_count": weak,
            "seed_values": ",".join(
                str(value)
                for value in sorted(
                    {
                        seed_from_text(str(row.get("case_label", "")))
                        for row in group
                        if seed_from_text(str(row.get("case_label", ""))) >= 0
                    }
                )
            ),
        }
    return context


def recommend_action(row: dict, summary: dict, boundary_summary: dict, source_context: dict[int, dict]) -> tuple[str, str]:
    offset = safe_float(row.get("tx_rx_offset_mm"))
    sources = safe_int(row.get("sources"), -1)
    boundary_status = str(row.get("boundary_status", ""))
    if sources == 3 and math.isclose(offset, 40.0, abs_tol=1.0e-9):
        context3 = source_context.get(3, {})
        context4 = source_context.get(4, {})
        if safe_int(context3.get("row_count"), 0) <= 2 and safe_float(context4.get("truth_geometry_fraction"), 0.0) >= 1.0:
            return (
                "single_gpu_source_count_seed_replicate",
                (
                    "Only one saved three-source seed exists at Tx/Rx 40 mm, and it retains "
                    "the exact branch without selecting it. A single seed13 or seed21 replicate "
                    "would test whether the three-source fragility is seed-specific while keeping "
                    "the already clean four-source boundary intact."
                ),
            )
    if offset < safe_float(boundary_summary.get("nearest_first_clean_replicated_tx_rx_mm"), math.inf):
        return (
            "no_gpu_archive_boundary_caveat",
            (
                f"Tx/Rx {offset:g} mm is already below the paper-safe clean threshold and has "
                f"nearest boundary status `{boundary_status}`; another run would not move the "
                "30 mm clean-threshold claim without a new acquisition hypothesis."
            ),
        )
    return (
        "no_gpu_saved_evidence_sufficient",
        (
            "Saved evidence already answers this branch-preservation row for the current manuscript "
            "claim; do not launch GPU work from this row alone."
        ),
    )


def build_probe_rows(
    actionability_rows: list[dict],
    boundary_rows: list[dict],
    boundary_summary: dict,
    threshold_summary: dict,
    source_context: dict[int, dict],
) -> list[dict]:
    boundaries = boundary_by_offset(boundary_rows)
    rows = []
    for action_row in actionability_rows:
        if action_row.get("actionability_label") != "candidate_for_narrow_coupled_probe":
            continue
        if "close50" not in str(action_row.get("run_dir", "")):
            continue
        if safe_int(action_row.get("target_index"), -1) != 2:
            continue
        source_summary = read_json(Path(str(action_row["source_summary_json"])))
        candidate_csv = Path(str(action_row["candidate_csv"]))
        case_label = str(action_row.get("case_label", ""))
        candidates = candidate_rows(candidate_csv, case_label)
        best = candidates[0] if candidates else {}
        truth_lateral = best_row_for_x(candidates, safe_float(action_row.get("truth_lateral_x_mm")))
        offset = safe_float(source_summary.get("tx_rx_offset_mm"))
        sources = safe_int(source_summary.get("sources"), -1)
        boundary = boundaries.get(offset, {})
        output_row = {
            "run_dir": action_row.get("run_dir", ""),
            "run_name": action_row.get("run_name", ""),
            "seed": seed_from_text(case_label),
            "case_label": case_label,
            "sources": sources,
            "tx_rx_offset_mm": offset,
            "receiver_sampling": source_summary.get("receiver_sampling", "nearest"),
            "target_index": safe_int(action_row.get("target_index"), -1),
            "best_x_mm": safe_float(action_row.get("best_x_mm")),
            "truth_lateral_x_mm": safe_float(action_row.get("truth_lateral_x_mm")),
            "best_radius_mm": safe_float(best.get("radius_mm")),
            "truth_lateral_radius_mm": safe_float(truth_lateral.get("radius_mm")),
            "truth_radius_mm": safe_float(source_summary.get("truth_radius_values_mm", [math.nan] * 3)[2]),
            "truth_lateral_gap_abs": safe_float(action_row.get("truth_lateral_gap_abs")),
            "truth_lateral_gap_rel": safe_float(action_row.get("truth_lateral_gap_rel")),
            "candidate_linf_improvement_mm": safe_float(action_row.get("candidate_linf_improvement_mm")),
            "boundary_status": boundary.get("boundary_status", "not_in_boundary_table"),
            "boundary_truth_geometry_fraction": safe_float(boundary.get("truth_geometry_fraction"), math.nan),
            "boundary_strict_clean_row_count": safe_float(boundary.get("strict_clean_row_count"), math.nan),
            "boundary_x_ambiguity_row_count": safe_float(boundary.get("x_ambiguity_row_count"), math.nan),
            "threshold_default_recovered_count": safe_int(threshold_summary.get("default_recovered_count"), -1),
            "threshold_default_mean_extra_candidates_per_step": safe_float(
                threshold_summary.get("default_mean_extra_candidates_per_step")
            ),
            "source_count_context_rows": safe_int(source_context.get(sources, {}).get("row_count"), 0),
            "source_count_context_truth_fraction": safe_float(
                source_context.get(sources, {}).get("truth_geometry_fraction"), math.nan
            ),
            "source_count_context_strong_count": safe_int(source_context.get(sources, {}).get("strong_count"), 0),
            "source_count_context_weak_count": safe_int(source_context.get(sources, {}).get("weak_count"), 0),
            "source_count_context_seed_values": source_context.get(sources, {}).get("seed_values", ""),
        }
        action, reason = recommend_action(output_row, {}, boundary_summary, source_context)
        output_row["recommended_action"] = action
        output_row["recommendation_reason"] = reason
        rows.append(output_row)
    return sorted(
        rows,
        key=lambda row: (
            row["recommended_action"] != "single_gpu_source_count_seed_replicate",
            -safe_float(row.get("candidate_linf_improvement_mm"), 0.0),
            safe_float(row.get("tx_rx_offset_mm"), 0.0),
            safe_int(row.get("seed"), 999),
        ),
    )


def summarize_probe_readiness(rows: list[dict], source_context: dict[int, dict]) -> tuple[list[dict], dict]:
    action_labels = sorted({str(row["recommended_action"]) for row in rows})
    action_rows = []
    for label in action_labels:
        group = [row for row in rows if row["recommended_action"] == label]
        action_rows.append({
            "recommended_action": label,
            "row_count": len(group),
            "max_linf_improvement_mm": max(
                [safe_float(row.get("candidate_linf_improvement_mm")) for row in group] or [math.nan]
            ),
            "source_counts": ",".join(str(value) for value in sorted({safe_int(row.get("sources")) for row in group})),
            "tx_rx_offsets_mm": ",".join(
                f"{value:g}" for value in sorted({safe_float(row.get("tx_rx_offset_mm")) for row in group})
            ),
        })
    gpu_rows = [row for row in rows if row["recommended_action"] == "single_gpu_source_count_seed_replicate"]
    source_context_rows = [
        {
            "source_count": value,
            **context,
        }
        for value, context in sorted(source_context.items())
    ]
    summary = {
        "policy_label": "close50_branch_preservation_probe_readiness_cpu",
        "candidate_row_count": len(rows),
        "single_gpu_source_count_seed_replicate_count": len(gpu_rows),
        "no_gpu_archive_boundary_caveat_count": sum(
            row["recommended_action"] == "no_gpu_archive_boundary_caveat" for row in rows
        ),
        "max_candidate_linf_improvement_mm": max(
            [safe_float(row.get("candidate_linf_improvement_mm")) for row in rows] or [math.nan]
        ),
        "ready_for_single_gpu_source_count_seed_replicate": len(gpu_rows) == 1,
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "single_bounded" if len(gpu_rows) == 1 else "none",
        "recommended_gpu_case": gpu_rows[0]["run_dir"] if gpu_rows else "",
        "recommended_new_seed_options": "13,21" if len(gpu_rows) == 1 else "",
        "source_count_context_row_count": len(source_context_rows),
        "decision": (
            "Do not repeat the below-threshold Tx/Rx 25 mm branch rows. If GPU is used, run one "
            "three-source Tx/Rx 40 mm close50 target2 seed replicate to test whether the saved "
            "sources3 seed34 failure is seed-specific; keep this separate from broad close50 "
            "threshold sweeps and detector-seeded FWI."
        ),
    }
    return action_rows, source_context_rows, summary


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "single_gpu_source_count_seed_replicate",
            "ready": summary["ready_for_single_gpu_source_count_seed_replicate"],
            "allowed_use": "one bounded close50 Tx/Rx40 sources3 seed replicate",
            "blocked_use": "broad close50 threshold sweep",
            "evidence": f"recommended case={summary['recommended_gpu_case']}",
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "launch broad GPU queue",
            "evidence": "saved archive already defines the close50 clean threshold boundary",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI launch",
            "evidence": "this scorecard concerns coordinate branch preservation only",
        },
    ]


def plot_probe_readiness(rows: list[dict], source_context_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.1), constrained_layout=True)

    labels = [
        f"{safe_int(row.get('sources'))} src\n{safe_float(row.get('tx_rx_offset_mm')):g} mm\nseed {safe_int(row.get('seed'))}"
        for row in rows
    ]
    gains = [safe_float(row.get("candidate_linf_improvement_mm")) for row in rows]
    colors = [
        "#d87a28" if row["recommended_action"] == "single_gpu_source_count_seed_replicate" else "#6c8ebf"
        for row in rows
    ]
    axes[0].bar(np.arange(len(rows)), gains, color=colors, edgecolor="#333333", linewidth=0.4)
    axes[0].set_xticks(np.arange(len(rows)), labels)
    axes[0].set_ylabel("truth-lateral L-inf gain [mm]")
    axes[0].set_title("Branch-preservation candidates")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    context_labels = [f"{safe_int(row.get('source_count'))} sources" for row in source_context_rows]
    truth_frac = [safe_float(row.get("truth_geometry_fraction"), 0.0) for row in source_context_rows]
    strong_counts = [safe_float(row.get("strong_count"), 0.0) for row in source_context_rows]
    x = np.arange(len(source_context_rows))
    axes[1].bar(x - 0.18, truth_frac, width=0.36, label="truth fraction", color="#59a14f")
    axes[1].bar(x + 0.18, strong_counts, width=0.36, label="strong rows", color="#4e79a7")
    axes[1].set_xticks(x, context_labels)
    axes[1].set_ylim(0.0, max([1.1] + [value + 0.5 for value in strong_counts]))
    axes[1].set_title("Saved Tx/Rx40 source-count context")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(loc="upper left", fontsize=8)
    axes[1].text(
        0.03,
        0.95,
        f"single GPU ready: {summary['ready_for_single_gpu_source_count_seed_replicate']}\n"
        f"broad GPU ready: {summary['ready_for_broad_gpu_queue']}\n"
        f"gpu priority: {summary['gpu_priority']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Close50 branch-preservation GPU-probe readiness", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `close50_branch_preservation_probe_readiness.png`",
                "",
                "This CPU-only figure scores the close50 rows from the branch-preservation",
                "actionability table against the saved close50 sampling-boundary and",
                "source-count evidence.",
                "",
                f"Candidate rows: `{summary['candidate_row_count']}`.",
                f"Single bounded GPU replicate ready: `{summary['ready_for_single_gpu_source_count_seed_replicate']}`.",
                f"Recommended case: `{summary['recommended_gpu_case']}`.",
                f"Recommended new seed options: `{summary['recommended_new_seed_options']}`.",
                f"Broad GPU queue ready: `{summary['ready_for_broad_gpu_queue']}`.",
                "",
                "Scope boundary:",
                "",
                "This scorecard reads saved outputs only. It does not launch FDTD/FWI,",
                "detector-seeded FWI, broad close50 sweeps, field FWI, or 3D/HPC jobs.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--actionability-rows", default=DEFAULT_ACTIONABILITY_ROWS)
    parser.add_argument("--threshold-summary", default=DEFAULT_THRESHOLD_SUMMARY)
    parser.add_argument("--boundary-rows", default=DEFAULT_BOUNDARY_ROWS)
    parser.add_argument("--boundary-summary", default=DEFAULT_BOUNDARY_SUMMARY)
    parser.add_argument("--source-count-aggregate", default=DEFAULT_SOURCE_COUNT_AGGREGATE)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--run-name", default="close50_branch_preservation_probe_readiness")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    actionability_rows = read_csv_rows(Path(args.actionability_rows))
    threshold_summary = read_json(Path(args.threshold_summary))
    boundary_rows = read_csv_rows(Path(args.boundary_rows))
    boundary_summary = read_json(Path(args.boundary_summary))
    source_context = source_count_context(source_count_rows(Path(args.source_count_aggregate)))

    rows = build_probe_rows(
        actionability_rows,
        boundary_rows,
        boundary_summary,
        threshold_summary,
        source_context,
    )
    action_rows, source_context_rows, summary = summarize_probe_readiness(rows, source_context)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "close50_branch_preservation_probe_readiness_rows.csv"
    action_csv = data_dir / "close50_branch_preservation_probe_readiness_actions.csv"
    source_context_csv = data_dir / "close50_branch_preservation_probe_readiness_source_context.csv"
    gates_csv = data_dir / "close50_branch_preservation_probe_readiness_gates.csv"
    summary_json = data_dir / "close50_branch_preservation_probe_readiness_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "close50_branch_preservation_probe_readiness.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(action_csv, [json_safe(row) for row in action_rows])
    write_csv(source_context_csv, [json_safe(row) for row in source_context_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_probe_readiness(rows, source_context_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary)

    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "action_rows_csv": str(action_csv),
        "source_context_csv": str(source_context_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
        "source_actionability_rows": args.actionability_rows,
        "source_threshold_summary": args.threshold_summary,
        "source_boundary_rows": args.boundary_rows,
        "source_boundary_summary": args.boundary_summary,
        "source_count_aggregate": args.source_count_aggregate,
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "close50_branch_preservation_probe_readiness",
        {
            "actionability_rows": args.actionability_rows,
            "boundary_rows": args.boundary_rows,
            "source_count_aggregate": args.source_count_aggregate,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

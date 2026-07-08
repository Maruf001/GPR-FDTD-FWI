#!/usr/bin/env python3
"""Evaluate a branch-preserving middle/right search for a repaired detector seed."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
import time
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

import config as cfg  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from core.source import generate_time_array  # noqa: E402
from inversion.adjoint import _build_mute_window  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from run_multi_rebar_common_radius_profile import build_observed_cases, build_scan_positions  # noqa: E402
from run_multi_rebar_coordinate_optimizer import truth_radius_values_for_run  # noqa: E402
from run_multi_rebar_local_geometry_profile import (  # noqa: E402
    build_variable_geometry_model,
    evaluate_local_geometry_grid,
    rank_case,
)
from run_single_rebar_frequency_weight_matrix import parse_values_mm  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_source_profiled_replication import parse_replication_cases  # noqa: E402
from run_single_rebar_wavelet_mismatch import parse_positive_values, parse_shift_values_ps  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_GREEDY_RUN = (
    "outputs/experiments/"
    "1341_local2d_repaired_exact_radius_seed_refine_target2_close14_seed21_nominal_gpu"
)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def step_for_target(summary: dict, target_index: int) -> dict:
    for step in summary.get("steps", []):
        if int(step.get("target_index", -1)) == int(target_index):
            return step
    raise ValueError(f"missing target {target_index} step")


def candidate_surface(path: Path, case_label: str) -> list[dict]:
    rows = [row for row in read_csv_rows(path) if row.get("case_label") == case_label]
    for row in rows:
        row["misfit"] = safe_float(row.get("misfit"))
        row["x_mm"] = safe_float(row.get("x_mm"))
        row["z_mm"] = safe_float(row.get("z_mm"))
        row["radius_mm"] = safe_float(row.get("radius_mm"))
    return sorted(rows, key=lambda item: item["misfit"])


def retained_target_branches(
    rows: list[dict],
    *,
    abs_gap_cutoff: float,
    rel_gap_cutoff: float,
    max_branches: int,
) -> list[dict]:
    if not rows:
        return []
    best = safe_float(rows[0].get("misfit"))
    retained = []
    for rank, row in enumerate(rows, start=1):
        misfit = safe_float(row.get("misfit"))
        gap_abs = misfit - best
        gap_rel = gap_abs / best if best else math.inf
        keep = rank == 1 or (gap_abs <= abs_gap_cutoff and gap_rel <= rel_gap_cutoff)
        if keep:
            retained.append(
                {
                    "branch_rank": rank,
                    "target1_x_mm": safe_float(row.get("x_mm")),
                    "target1_z_mm": safe_float(row.get("z_mm")),
                    "target1_radius_mm": safe_float(row.get("radius_mm")),
                    "target1_misfit": misfit,
                    "target1_gap_abs": gap_abs,
                    "target1_gap_rel": gap_rel,
                }
            )
        if len(retained) >= int(max_branches):
            break
    return retained


def linf_error_mm(truth_x: list[float], truth_z: list[float], x_values: list[float], z_values: list[float]) -> float:
    truth_x_arr = np.asarray(truth_x, dtype=float)
    truth_z_arr = np.asarray(truth_z, dtype=float)
    x_arr = np.asarray(x_values, dtype=float)
    z_arr = np.asarray(z_values, dtype=float)
    return float(max(np.max(np.abs(x_arr - truth_x_arr)), np.max(np.abs(z_arr - truth_z_arr))))


def target_values_from_offsets(center: float, offsets: list[float]) -> list[float]:
    return [float(center) + float(offset) for offset in offsets]


def flatten_branch_candidates(
    branch: dict,
    candidates: list[dict],
    case_label: str,
    truth_x: list[float],
    truth_z: list[float],
) -> list[dict]:
    rows = []
    ranked = rank_case(candidates, case_label)
    for rank, candidate in enumerate(ranked, start=1):
        params = candidate["params"]
        rows.append(
            {
                "branch_rank": int(branch["branch_rank"]),
                "candidate_rank": rank,
                "target1_x_mm": safe_float(branch["target1_x_mm"]),
                "target1_z_mm": safe_float(branch["target1_z_mm"]),
                "target1_misfit": safe_float(branch["target1_misfit"]),
                "target1_gap_abs": safe_float(branch["target1_gap_abs"]),
                "target1_gap_rel": safe_float(branch["target1_gap_rel"]),
                "target2_x_mm": safe_float(params.get("x_mm")),
                "target2_z_mm": safe_float(params.get("z_mm")),
                "target2_radius_mm": safe_float(params.get("radius_mm")),
                "coupled_misfit": safe_float(candidate.get("misfit")),
                "final_linf_error_mm": linf_error_mm(
                    truth_x,
                    truth_z,
                    params["x_values_mm"],
                    params["z_values_mm"],
                ),
                "x_values_mm": ",".join(f"{value:g}" for value in params["x_values_mm"]),
                "z_values_mm": ",".join(f"{value:g}" for value in params["z_values_mm"]),
                "radii_mm": ",".join(f"{value:g}" for value in params["radii_mm"]),
                "source_frequency_scale": candidate["source_profile"].get("frequency_scale"),
                "source_time_shift_ps": candidate["source_profile"].get("time_shift_ps"),
                "source_amplitude_scale": candidate["source_profile"].get("amplitude_scale"),
            }
        )
    return rows


def summarize_search(branch_rows: list[dict], candidate_rows: list[dict], greedy_summary: dict) -> dict:
    objective_best = min(candidate_rows, key=lambda row: safe_float(row.get("coupled_misfit"))) if candidate_rows else {}
    oracle_best = (
        min(
            candidate_rows,
            key=lambda row: (
                safe_float(row.get("final_linf_error_mm")),
                safe_float(row.get("coupled_misfit")),
            ),
        )
        if candidate_rows
        else {}
    )
    greedy_linf = linf_error_mm(
        greedy_summary["true_x_values_mm"],
        greedy_summary["true_z_values_mm"],
        greedy_summary["final_state"]["x_values_mm"],
        greedy_summary["final_state"]["z_values_mm"],
    )
    objective_linf = safe_float(objective_best.get("final_linf_error_mm"), math.nan)
    oracle_linf = safe_float(oracle_best.get("final_linf_error_mm"), math.nan)
    truth_target2_x = safe_float(greedy_summary["true_x_values_mm"][2], math.nan)
    return {
        "policy_label": "local2d_coupled_middle_right_branch_preserving_search",
        "source_greedy_run_name": greedy_summary.get("run_name", ""),
        "retained_target1_branch_count": len(branch_rows),
        "candidate_count": len(candidate_rows),
        "objective_best_branch_rank": safe_int(objective_best.get("branch_rank"), 0),
        "objective_best_target1_x_mm": safe_float(objective_best.get("target1_x_mm"), math.nan),
        "objective_best_target1_z_mm": safe_float(objective_best.get("target1_z_mm"), math.nan),
        "objective_best_target2_x_mm": safe_float(objective_best.get("target2_x_mm"), math.nan),
        "objective_best_target2_z_mm": safe_float(objective_best.get("target2_z_mm"), math.nan),
        "objective_best_coupled_misfit": safe_float(objective_best.get("coupled_misfit"), math.nan),
        "objective_best_final_linf_error_mm": objective_linf,
        "oracle_best_branch_rank": safe_int(oracle_best.get("branch_rank"), 0),
        "oracle_best_target1_x_mm": safe_float(oracle_best.get("target1_x_mm"), math.nan),
        "oracle_best_target1_z_mm": safe_float(oracle_best.get("target1_z_mm"), math.nan),
        "oracle_best_target2_x_mm": safe_float(oracle_best.get("target2_x_mm"), math.nan),
        "oracle_best_target2_z_mm": safe_float(oracle_best.get("target2_z_mm"), math.nan),
        "oracle_best_coupled_misfit": safe_float(oracle_best.get("coupled_misfit"), math.nan),
        "oracle_best_final_linf_error_mm": oracle_linf,
        "greedy_final_linf_error_mm": greedy_linf,
        "objective_linf_improvement_mm": greedy_linf - objective_linf if math.isfinite(objective_linf) else math.nan,
        "oracle_linf_improvement_mm": greedy_linf - oracle_linf if math.isfinite(oracle_linf) else math.nan,
        "target2_true_lateral_selected_by_objective": math.isclose(
            safe_float(objective_best.get("target2_x_mm"), math.nan),
            truth_target2_x,
            abs_tol=1.0e-9,
        ),
        "target2_true_lateral_available_in_oracle": math.isclose(
            safe_float(oracle_best.get("target2_x_mm"), math.nan),
            truth_target2_x,
            abs_tol=1.0e-9,
        ),
        "ready_for_branch_preserving_selector_evaluation": bool(candidate_rows),
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "Use this as a narrow branch-preserving coupled-search diagnostic. "
            "It does not authorize a broad GPU queue or detector-seeded FWI."
        ),
    }


def branch_summary_rows(branches: list[dict], candidate_rows: list[dict]) -> list[dict]:
    rows = []
    for branch in branches:
        branch_candidates = [
            row for row in candidate_rows if safe_int(row.get("branch_rank"), -1) == int(branch["branch_rank"])
        ]
        best = min(branch_candidates, key=lambda row: safe_float(row.get("coupled_misfit"))) if branch_candidates else {}
        rows.append(
            {
                **branch,
                "candidate_count": len(branch_candidates),
                "best_target2_x_mm": safe_float(best.get("target2_x_mm"), math.nan),
                "best_target2_z_mm": safe_float(best.get("target2_z_mm"), math.nan),
                "best_coupled_misfit": safe_float(best.get("coupled_misfit"), math.nan),
                "best_final_linf_error_mm": safe_float(best.get("final_linf_error_mm"), math.nan),
            }
        )
    return rows


def plot_search(branch_rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [f"b{safe_int(row['branch_rank'])}\nx={safe_float(row['target1_x_mm']):g}" for row in branch_rows]
    target1_misfit = [safe_float(row.get("target1_misfit")) for row in branch_rows]
    best_linf = [safe_float(row.get("best_final_linf_error_mm")) for row in branch_rows]
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 4.5), constrained_layout=True)
    axes[0].bar(labels, target1_misfit, color="#607d8b")
    axes[0].set_title("Retained Middle Branches")
    axes[0].set_ylabel("target1 local misfit")
    axes[0].grid(axis="y", alpha=0.25)
    axes[1].bar(labels, best_linf, color=["#2f9d55" if value <= 1.0 else "#d8a03d" for value in best_linf])
    axes[1].axhline(summary["greedy_final_linf_error_mm"], color="#d6453d", linestyle="--", linewidth=1.2)
    axes[1].set_title("Best Coupled Final Error")
    axes[1].set_ylabel("L-infinity x/z error [mm]")
    axes[1].grid(axis="y", alpha=0.25)
    axes[1].text(
        0.02,
        0.92,
        f"objective={summary['objective_best_final_linf_error_mm']:.1f} mm\n"
        f"oracle={summary['oracle_best_final_linf_error_mm']:.1f} mm\n"
        f"greedy={summary['greedy_final_linf_error_mm']:.1f} mm\n"
        f"gpu={summary['gpu_priority']}",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Branch-Preserving Middle/Right Coupled Search", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `coupled_middle_right_branch_preserving_search.png`",
                "",
                "This figure summarizes a branch-preserving coupled search over retained",
                "middle-bar branches and local target2 candidates for the repaired",
                "target2_close14 seed21 nominal case.",
                "",
                f"Retained middle branches: `{summary['retained_target1_branch_count']}`.",
                f"Evaluated candidates: `{summary['candidate_count']}`.",
                f"Greedy/objective/oracle L-infinity error: `{summary['greedy_final_linf_error_mm']:.1f}` / `{summary['objective_best_final_linf_error_mm']:.1f}` / `{summary['oracle_best_final_linf_error_mm']:.1f}` mm.",
                f"Broad GPU queue ready: `{summary['ready_for_broad_gpu_queue']}`.",
                f"Detector-seeded FWI ready: `{summary['ready_for_detector_seeded_fwi']}`.",
                "",
                "Scope boundary:",
                "",
                "This is a single narrow synthetic diagnostic. It is not a field",
                "transfer, radius/material inference, broad GPU queue, or FWI launch.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--greedy-run", default=DEFAULT_GREEDY_RUN)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--x-offsets-mm", type=parse_values_mm, default=parse_values_mm("-4:4:2"))
    parser.add_argument("--z-offsets-mm", type=parse_values_mm, default=parse_values_mm("-4:4:2"))
    parser.add_argument("--source-frequency-scales", type=parse_positive_values, default=parse_positive_values("1.0"))
    parser.add_argument("--source-time-shift-ps-values", type=parse_shift_values_ps, default=parse_shift_values_ps("0"))
    parser.add_argument("--abs-gap-cutoff", type=float, default=0.01)
    parser.add_argument("--rel-gap-cutoff", type=float, default=0.10)
    parser.add_argument("--max-branches", type=int, default=4)
    parser.add_argument("--top-k", type=int, default=12)
    parser.add_argument("--progress-every", type=int, default=5)
    parser.add_argument("--run-name", default="local2d_coupled_middle_right_branch_preserving_search")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    _override_grid(args.grid_step_mm)
    greedy_run = Path(args.greedy_run)
    greedy_summary = read_json(greedy_run / "data/multi_rebar_coordinate_optimizer_summary.json")
    update_case_label = greedy_summary.get("update_case_label", "nominal")
    target1_step = step_for_target(greedy_summary, 1)
    target1_rows = candidate_surface(Path(target1_step["candidate_csv"]), update_case_label)
    retained = retained_target_branches(
        target1_rows,
        abs_gap_cutoff=args.abs_gap_cutoff,
        rel_gap_cutoff=args.rel_gap_cutoff,
        max_branches=args.max_branches,
    )
    if not retained:
        raise ValueError("no target1 branches retained")

    true_radii = truth_radius_values_for_run(
        greedy_summary.get("truth_radius_mm", cfg.REBAR_RADIUS * 1000.0),
        greedy_summary.get("truth_radius_values_mm"),
        len(greedy_summary["true_x_values_mm"]),
    )
    true_model = build_variable_geometry_model(
        greedy_summary["true_x_values_mm"],
        greedy_summary["true_z_values_mm"],
        true_radii,
        geometry_mode="hard",
    )
    frequency_hz = safe_float(greedy_summary.get("frequency_ghz"), 1.5) * 1e9
    time_values = generate_time_array(cfg.NT, cfg.DT)
    mute = _build_mute_window(cfg.NT, cfg.DT)
    scan_positions, _ = build_scan_positions(
        cfg.INVERSION_SCAN_STEP,
        safe_int(greedy_summary.get("sources"), 5),
        tx_rx_offset_m=safe_float(greedy_summary.get("tx_rx_offset_mm"), 45.0) / 1000.0,
        receiver_sampling=greedy_summary.get("receiver_sampling", "nearest"),
    )
    observed_by_case, case_metadata = build_observed_cases(
        true_model,
        time_values,
        frequency_hz,
        scan_positions,
        args.backend,
        greedy_summary.get("replication_cases") or parse_replication_cases("nominal:1.0,0.0,1.0,0.153613,21"),
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {outdir}")

    started = time.time()
    all_candidate_rows: list[dict] = []
    branch_candidate_files = []
    target2_start_x = safe_float(target1_step["state_after"]["x_values_mm"][2])
    target2_start_z = safe_float(target1_step["state_after"]["z_values_mm"][2])
    target2_radius = safe_float(target1_step["state_after"]["radii_mm"][2])
    for branch in retained:
        base_x = [safe_float(value) for value in target1_step["state_before"]["x_values_mm"]]
        base_z = [safe_float(value) for value in target1_step["state_before"]["z_values_mm"]]
        base_radii = [safe_float(value) for value in target1_step["state_before"]["radii_mm"]]
        base_x[1] = safe_float(branch["target1_x_mm"])
        base_z[1] = safe_float(branch["target1_z_mm"])
        print(
            "Coupled branch "
            f"rank={branch['branch_rank']}, target1=({base_x[1]:g},{base_z[1]:g}), "
            f"target2 center=({target2_start_x:g},{target2_start_z:g})"
        )
        candidates = evaluate_local_geometry_grid(
            observed_by_case,
            base_x,
            base_z,
            target2_radius,
            2,
            target_values_from_offsets(target2_start_x, list(args.x_offsets_mm)),
            target_values_from_offsets(target2_start_z, list(args.z_offsets_mm)),
            [target2_radius],
            base_radii,
            frequency_hz,
            list(args.source_frequency_scales),
            [value * 1e-12 for value in args.source_time_shift_ps_values],
            scan_positions,
            time_values,
            mute,
            args.backend,
            geometry_mode="hard",
            fit_amplitude=True,
            enforce_nonoverlap_candidates=True,
            progress_every=args.progress_every,
        )
        branch_file = data_dir / f"branch_{safe_int(branch['branch_rank']):02d}_target2_candidates.csv"
        branch_candidate_files.append(str(branch_file))
        rows = flatten_branch_candidates(
            branch,
            candidates,
            update_case_label,
            greedy_summary["true_x_values_mm"],
            greedy_summary["true_z_values_mm"],
        )
        write_csv(branch_file, [json_safe(row) for row in rows])
        all_candidate_rows.extend(rows)

    summary = summarize_search(retained, all_candidate_rows, greedy_summary)
    branches = branch_summary_rows(retained, all_candidate_rows)
    candidate_csv = data_dir / "coupled_middle_right_candidates.csv"
    branch_csv = data_dir / "coupled_middle_right_branch_rows.csv"
    gates_csv = data_dir / "coupled_middle_right_gates.csv"
    summary_json = data_dir / "coupled_middle_right_summary.json"
    figure_path = figures_dir / "coupled_middle_right_branch_preserving_search.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"
    validation_csv = data_dir / "figure_validation.csv"

    gates = [
        {
            "gate_key": "branch_preserving_selector_evaluation",
            "ready": summary["ready_for_branch_preserving_selector_evaluation"],
            "allowed_use": "single-case branch-preserving synthetic selector diagnostic",
            "blocked_use": "deployable detector policy",
            "evidence": f"retained branches={summary['retained_target1_branch_count']}; candidates={summary['candidate_count']}",
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "launch broad branch-preserving queue",
            "evidence": "single repaired-seed case only",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI launch",
            "evidence": "no validated general detector-to-FWI contract",
        },
    ]
    plot_search(branches, summary, figure_path)
    write_csv(candidate_csv, [json_safe(row) for row in all_candidate_rows])
    write_csv(branch_csv, [json_safe(row) for row in branches])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["elapsed_time_s"] = time.time() - started
    summary["case_metadata"] = case_metadata
    summary["paths"] = {
        "candidate_csv": str(candidate_csv),
        "branch_csv": str(branch_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
        "branch_candidate_files": branch_candidate_files,
        "source_greedy_summary_json": str(greedy_run / "data/multi_rebar_coordinate_optimizer_summary.json"),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_coupled_middle_right_search",
        {
            "greedy_run": str(greedy_run),
            "backend": args.backend,
            "grid_step_mm": args.grid_step_mm,
            "abs_gap_cutoff": args.abs_gap_cutoff,
            "rel_gap_cutoff": args.rel_gap_cutoff,
            "summary_json": str(summary_json),
            "candidate_csv": str(candidate_csv),
            "branch_csv": str(branch_csv),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

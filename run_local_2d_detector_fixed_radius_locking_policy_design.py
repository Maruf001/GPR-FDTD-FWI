#!/usr/bin/env python3
"""Design a fixed-radius update-order/locking policy after residual audit."""

from __future__ import annotations

import argparse
import ast
import csv
import json
import math
import os
import sys
from pathlib import Path

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
from run_local_2d_detector_fixed_radius_pilot_outcome_synthesis import format_values, parse_values  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_PILOT_RUN = "1357_local2d_fixed_radius_second_pass_target2_close14_seed21_nominal_gpu"
DEFAULT_RESIDUAL_AUDIT_RUN = "128_local_2d_detector_fixed_radius_residual_ambiguity_audit_post_second_pass"
DEFAULT_NEAR_TIE_REL = 0.05
DEFAULT_MAX_RAM_PERCENT = 80.0
DEFAULT_MAX_GPU_UTIL_PERCENT = 90.0


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_vector(value: object) -> list[float]:
    if isinstance(value, list):
        return [float(item) for item in value]
    text = str(value or "").strip()
    if not text:
        return []
    if text.startswith("["):
        return [float(item) for item in ast.literal_eval(text)]
    return parse_values(text)


def clearance_mm(first_x: float, first_z: float, first_r: float, second_x: float, second_z: float, second_r: float) -> float:
    return math.hypot(float(first_x) - float(second_x), float(first_z) - float(second_z)) - (
        float(first_r) + float(second_r)
    )


def _ranked_candidates(rows: list[dict]) -> list[dict]:
    ranked = sorted(rows, key=lambda row: safe_float(row.get("misfit"), math.inf))
    outputs: list[dict] = []
    for rank, row in enumerate(ranked, start=1):
        enriched = dict(row)
        enriched["rank"] = rank
        outputs.append(enriched)
    return outputs


def _target_step(summary: dict, target_index: int) -> dict:
    for step in summary.get("steps", []):
        if safe_int(step.get("target_index"), -1) == int(target_index):
            return step
    raise ValueError(f"target step {target_index} not found")


def _candidate_tuple(row: dict) -> tuple[float, float, float]:
    return (
        safe_float(row.get("x_mm"), math.nan),
        safe_float(row.get("z_mm"), math.nan),
        safe_float(row.get("radius_mm"), math.nan),
    )


def _same_candidate(row: dict, x_mm: float, z_mm: float, radius_mm: float) -> bool:
    x_value, z_value, radius_value = _candidate_tuple(row)
    return (
        abs(x_value - float(x_mm)) <= 1.0e-9
        and abs(z_value - float(z_mm)) <= 1.0e-9
        and abs(radius_value - float(radius_mm)) <= 1.0e-9
    )


def _candidate_errors(row: dict, truth_x: list[float], truth_z: list[float], target_index: int) -> tuple[float, float, float]:
    x_error = safe_float(row.get("x_mm"), math.nan) - float(truth_x[target_index])
    z_error = safe_float(row.get("z_mm"), math.nan) - float(truth_z[target_index])
    return x_error, z_error, max(abs(x_error), abs(z_error))


def build_lock_candidate_rows(
    optimizer_summary: dict,
    residual_rows: list[dict],
    *,
    near_tie_rel: float = DEFAULT_NEAR_TIE_REL,
) -> list[dict]:
    truth_x = parse_vector(optimizer_summary.get("true_x_values_mm"))
    truth_z = parse_vector(optimizer_summary.get("true_z_values_mm"))
    truth_radii = parse_vector(optimizer_summary.get("truth_radius_values_mm") or optimizer_summary.get("truth_radius_mm"))
    outputs: list[dict] = []
    residual_by_target = {safe_int(row.get("target_index"), -1): row for row in residual_rows}
    target_count = len(truth_x)
    for target_index in range(target_count):
        step = _target_step(optimizer_summary, target_index)
        candidate_csv = Path(step["candidate_csv"])
        ranked = _ranked_candidates(read_csv_rows(candidate_csv))
        best = ranked[0]
        best_misfit = safe_float(best.get("misfit"), math.inf)
        near_rows = [
            row for row in ranked
            if safe_float(row.get("misfit"), math.inf) <= best_misfit * (1.0 + float(near_tie_rel))
        ]
        state_before = step.get("state_before", {})
        state_x = parse_vector(state_before.get("x_values_mm"))
        state_z = parse_vector(state_before.get("z_values_mm"))
        state_radii = parse_vector(state_before.get("radii_mm"))
        has_downstream = target_index + 1 < target_count
        if has_downstream:
            neighbor_index = target_index + 1
            neighbor_x = state_x[neighbor_index]
            neighbor_z = state_z[neighbor_index]
            neighbor_r = state_radii[neighbor_index]

            def downstream_clearance(row: dict) -> float:
                return clearance_mm(
                    safe_float(row.get("x_mm")),
                    safe_float(row.get("z_mm")),
                    safe_float(row.get("radius_mm")),
                    neighbor_x,
                    neighbor_z,
                    neighbor_r,
                )

            lock = sorted(
                near_rows,
                key=lambda row: (
                    -downstream_clearance(row),
                    safe_float(row.get("misfit"), math.inf),
                    safe_float(row.get("x_mm"), math.inf),
                    safe_float(row.get("z_mm"), math.inf),
                ),
            )[0]
            best_clearance_to_next_seed = downstream_clearance(best)
            lock_clearance_to_next_seed = downstream_clearance(lock)
            downstream_truth_clearance_best = clearance_mm(
                safe_float(best.get("x_mm")),
                safe_float(best.get("z_mm")),
                safe_float(best.get("radius_mm")),
                truth_x[neighbor_index],
                truth_z[neighbor_index],
                truth_radii[neighbor_index],
            )
            downstream_truth_clearance_lock = clearance_mm(
                safe_float(lock.get("x_mm")),
                safe_float(lock.get("z_mm")),
                safe_float(lock.get("radius_mm")),
                truth_x[neighbor_index],
                truth_z[neighbor_index],
                truth_radii[neighbor_index],
            )
        else:
            neighbor_index = None
            lock = best
            best_clearance_to_next_seed = math.nan
            lock_clearance_to_next_seed = math.nan
            downstream_truth_clearance_best = math.nan
            downstream_truth_clearance_lock = math.nan

        lock_misfit = safe_float(lock.get("misfit"), math.inf)
        lock_x_error, lock_z_error, lock_linf_error = _candidate_errors(lock, truth_x, truth_z, target_index)
        best_x_error, best_z_error, best_linf_error = _candidate_errors(best, truth_x, truth_z, target_index)
        residual = residual_by_target.get(target_index, {})
        lock_is_truth = _same_candidate(lock, truth_x[target_index], truth_z[target_index], truth_radii[target_index])
        best_is_truth = _same_candidate(best, truth_x[target_index], truth_z[target_index], truth_radii[target_index])
        objective_penalty = lock_misfit - best_misfit
        objective_penalty_rel = objective_penalty / best_misfit if best_misfit else math.nan
        action_ready = (
            has_downstream
            and lock["rank"] != best["rank"]
            and objective_penalty_rel <= near_tie_rel
            and lock_clearance_to_next_seed > best_clearance_to_next_seed
            and downstream_truth_clearance_best < -1.0e-9
            and downstream_truth_clearance_lock >= -1.0e-9
        )
        outputs.append(
            {
                "target_index": target_index,
                "residual_mode": residual.get("residual_mode", ""),
                "candidate_count": len(ranked),
                "near_tie_rel_threshold": float(near_tie_rel),
                "near_tie_candidate_count": len(near_rows),
                "best_rank": safe_int(best.get("rank"), 0),
                "best_x_mm": safe_float(best.get("x_mm"), math.nan),
                "best_z_mm": safe_float(best.get("z_mm"), math.nan),
                "best_radius_mm": safe_float(best.get("radius_mm"), math.nan),
                "best_misfit": best_misfit,
                "best_is_truth": best_is_truth,
                "best_x_error_mm": best_x_error,
                "best_z_error_mm": best_z_error,
                "best_linf_error_mm": best_linf_error,
                "lock_rank": safe_int(lock.get("rank"), 0),
                "lock_x_mm": safe_float(lock.get("x_mm"), math.nan),
                "lock_z_mm": safe_float(lock.get("z_mm"), math.nan),
                "lock_radius_mm": safe_float(lock.get("radius_mm"), math.nan),
                "lock_misfit": lock_misfit,
                "lock_is_truth": lock_is_truth,
                "lock_x_error_mm": lock_x_error,
                "lock_z_error_mm": lock_z_error,
                "lock_linf_error_mm": lock_linf_error,
                "lock_objective_penalty_abs": objective_penalty,
                "lock_objective_penalty_rel": objective_penalty_rel,
                "downstream_neighbor_index": "" if neighbor_index is None else neighbor_index,
                "best_clearance_to_next_seed_mm": best_clearance_to_next_seed,
                "lock_clearance_to_next_seed_mm": lock_clearance_to_next_seed,
                "lock_clearance_gain_to_next_seed_mm": (
                    lock_clearance_to_next_seed - best_clearance_to_next_seed
                    if has_downstream else math.nan
                ),
                "downstream_truth_clearance_with_best_mm": downstream_truth_clearance_best,
                "downstream_truth_clearance_with_lock_mm": downstream_truth_clearance_lock,
                "lock_unblocks_downstream_truth_geometry": action_ready,
                "ready_for_single_guarded_unlock_probe": action_ready,
                "allowed_use": "truth-free near-tie downstream-clearance lock design",
                "blocked_use": "broad GPU queue, detector-seeded FWI, field transfer",
            }
        )
    return outputs


def build_policy_rows(lock_rows: list[dict], residual_summary: dict, optimizer_summary: dict) -> list[dict]:
    selected_rows = [row for row in lock_rows if boolish(row.get("ready_for_single_guarded_unlock_probe"))]
    selected = selected_rows[0] if selected_rows else {}
    rows = [
        {
            "policy_key": "current_greedy_sequential",
            "truth_free": True,
            "deployable_now": True,
            "uses_oracle_truth": False,
            "final_linf_error_mm": safe_float(residual_summary.get("final_linf_error_mm"), math.nan),
            "expected_effect": "baseline observed in run 1357",
            "ready_for_gpu_validation": False,
            "ready_for_broad_gpu_queue": False,
            "ready_for_detector_seeded_fwi": False,
            "selected_target_index": "",
            "selected_lock_x_mm": "",
            "selected_lock_z_mm": "",
            "selected_objective_penalty_rel": "",
        },
        {
            "policy_key": "oracle_truth_lock_diagnostic",
            "truth_free": False,
            "deployable_now": False,
            "uses_oracle_truth": True,
            "final_linf_error_mm": 0.0 if selected else math.nan,
            "expected_effect": "diagnostic only: truth lock would make downstream truth non-overlap-feasible",
            "ready_for_gpu_validation": False,
            "ready_for_broad_gpu_queue": False,
            "ready_for_detector_seeded_fwi": False,
            "selected_target_index": selected.get("target_index", ""),
            "selected_lock_x_mm": selected.get("lock_x_mm", ""),
            "selected_lock_z_mm": selected.get("lock_z_mm", ""),
            "selected_objective_penalty_rel": selected.get("lock_objective_penalty_rel", ""),
        },
        {
            "policy_key": "near_tie_downstream_clearance_lock",
            "truth_free": True,
            "deployable_now": bool(selected),
            "uses_oracle_truth": False,
            "final_linf_error_mm": math.nan,
            "expected_effect": (
                "select a near-tie candidate that preserves more downstream clearance "
                "before updating the next target"
            ),
            "ready_for_gpu_validation": bool(selected),
            "ready_for_broad_gpu_queue": False,
            "ready_for_detector_seeded_fwi": False,
            "selected_target_index": selected.get("target_index", ""),
            "selected_lock_x_mm": selected.get("lock_x_mm", ""),
            "selected_lock_z_mm": selected.get("lock_z_mm", ""),
            "selected_objective_penalty_rel": selected.get("lock_objective_penalty_rel", ""),
        },
    ]
    return rows


def guarded_unlock_command(summary: dict) -> str:
    if not summary.get("ready_for_single_guarded_unlock_probe", False):
        return ""
    run_name = "local2d_fixed_radius_locking_target2_unlock_probe_target2_close14_seed21_nominal_gpu"
    command = [
        "conda", "run", "-n", "gpr-fdtd-fwi", "python", "run_resource_guarded_command.py",
        "--max-ram-percent", f"{DEFAULT_MAX_RAM_PERCENT:g}",
        "--max-gpu-util-percent", f"{DEFAULT_MAX_GPU_UTIL_PERCENT:g}",
        "--poll-interval-s", "5",
        "--summary-json", f"outputs/resource_guards/{run_name}_guard_summary.json",
        "--log-jsonl", f"outputs/resource_guards/{run_name}_guard_samples.jsonl",
        "--",
        "conda", "run", "-n", "gpr-fdtd-fwi", "python", "run_multi_rebar_coordinate_optimizer.py",
        "--backend", "gpu-cpml",
        "--grid-step-mm", "1",
        "--sources", "5",
        "--tx-rx-offset-mm", "45",
        "--receiver-sampling", "nearest",
        "--frequency-ghz", "1.5",
        "--true-x-values-mm", "190,250,264",
        "--true-z-values-mm", "90,90,90",
        "--truth-radius-values-mm", "5,6,8",
        "--initial-x-values-mm", summary["unlock_probe_initial_x_values_mm"],
        "--initial-z-values-mm", summary["unlock_probe_initial_z_values_mm"],
        "--initial-radius-values-mm", "5,6,8",
        "--target-indices", str(summary["unlock_probe_target_index"]),
        "--passes", "1",
        "--x-offsets-mm=-2,-1,0,1,2",
        "--z-offsets-mm=-2,-1,0,1,2",
        "--radius-offsets-mm", "0",
        "--replication-cases", "nominal:1.0,0.0,1.0,0.153613,21",
        "--update-case-label", "nominal",
        "--source-frequency-scales", "1.0",
        "--source-time-shift-ps-values=0",
        "--top-k", "12",
        "--progress-every", "5",
        "--geometry-mode", "hard",
        "--enforce-nonoverlap-candidates",
        "--run-name", run_name,
    ]
    return " ".join(command)


def summarize_design(
    optimizer_summary: dict,
    residual_summary: dict,
    lock_rows: list[dict],
    policy_rows: list[dict],
    *,
    near_tie_rel: float,
) -> dict:
    selected_rows = [row for row in lock_rows if boolish(row.get("ready_for_single_guarded_unlock_probe"))]
    selected = selected_rows[0] if selected_rows else {}
    initial_x = parse_vector(optimizer_summary.get("final_state", {}).get("x_values_mm"))
    initial_z = parse_vector(optimizer_summary.get("final_state", {}).get("z_values_mm"))
    unlock_target = ""
    if selected:
        lock_target = safe_int(selected.get("target_index"), -1)
        unlock_target = lock_target + 1
        if unlock_target < len(initial_x):
            unlock_step = _target_step(optimizer_summary, unlock_target)
            initial_x = parse_vector(unlock_step.get("state_before", {}).get("x_values_mm"))
            initial_z = parse_vector(unlock_step.get("state_before", {}).get("z_values_mm"))
        initial_x[lock_target] = safe_float(selected.get("lock_x_mm"))
        initial_z[lock_target] = safe_float(selected.get("lock_z_mm"))
    ready = bool(selected)
    return {
        "policy_label": "local_2d_detector_fixed_radius_locking_policy_design_cpu_selector",
        "source_pilot_run": optimizer_summary.get("run_name", ""),
        "source_residual_policy_label": residual_summary.get("policy_label", ""),
        "near_tie_rel_threshold": float(near_tie_rel),
        "target_count": len(lock_rows),
        "candidate_lock_ready_count": len(selected_rows),
        "selected_lock_target_index": selected.get("target_index", ""),
        "selected_lock_x_mm": selected.get("lock_x_mm", ""),
        "selected_lock_z_mm": selected.get("lock_z_mm", ""),
        "selected_lock_radius_mm": selected.get("lock_radius_mm", ""),
        "selected_lock_rank": selected.get("lock_rank", ""),
        "selected_lock_objective_penalty_abs": selected.get("lock_objective_penalty_abs", ""),
        "selected_lock_objective_penalty_rel": selected.get("lock_objective_penalty_rel", ""),
        "selected_lock_clearance_gain_to_next_seed_mm": selected.get("lock_clearance_gain_to_next_seed_mm", ""),
        "selected_lock_downstream_truth_clearance_before_mm": selected.get(
            "downstream_truth_clearance_with_best_mm", ""
        ),
        "selected_lock_downstream_truth_clearance_after_mm": selected.get(
            "downstream_truth_clearance_with_lock_mm", ""
        ),
        "ready_for_single_guarded_unlock_probe": ready,
        "unlock_probe_target_index": unlock_target,
        "unlock_probe_initial_x_values_mm": format_values(initial_x) if selected else "",
        "unlock_probe_initial_z_values_mm": format_values(initial_z) if selected else "",
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_field_transfer": False,
        "ready_for_detector_inferred_radius_material": False,
        "max_ram_percent": DEFAULT_MAX_RAM_PERCENT,
        "max_gpu_util_percent": DEFAULT_MAX_GPU_UTIL_PERCENT,
        "gpu_priority": "single_guarded_unlock_probe_candidate" if ready else "none",
        "decision": (
            "A truth-free near-tie downstream-clearance lock has one actionable candidate: "
            "lock target1 at [250,90] instead of the greedy [251,89], then validate target2 "
            "with one guarded unlock probe. This is a single falsification probe, not a "
            "broad GPU queue or detector-seeded FWI launch."
            if ready
            else "No truth-free lock candidate is strong enough to justify GPU validation."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "single_guarded_unlock_probe",
            "ready": summary["ready_for_single_guarded_unlock_probe"],
            "allowed_use": "one guarded target2 unlock validation probe",
            "blocked_use": "multi-case queue",
            "evidence": (
                f"lock target={summary['selected_lock_target_index']}; "
                f"penalty_rel={summary['selected_lock_objective_penalty_rel']}; "
                f"clearance_after={summary['selected_lock_downstream_truth_clearance_after_mm']}"
            ),
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "broad detector-refinement queue",
            "evidence": "only one lock candidate has been designed",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "FWI launch",
            "evidence": "fixed radii remain controlled priors and one coordinate residual remains unresolved",
        },
    ]


def plot_design(summary: dict, lock_rows: list[dict], save_path: Path) -> str:
    labels = [f"T{safe_int(row['target_index'], 0)}" for row in lock_rows]
    penalties = [safe_float(row.get("lock_objective_penalty_rel"), 0.0) for row in lock_rows]
    clearance_gains = [
        safe_float(row.get("lock_clearance_gain_to_next_seed_mm"), 0.0)
        if str(row.get("lock_clearance_gain_to_next_seed_mm", "")) else 0.0
        for row in lock_rows
    ]
    unlocks = [1 if boolish(row.get("lock_unblocks_downstream_truth_geometry")) else 0 for row in lock_rows]
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.5), constrained_layout=True)
    axes[0].bar(labels, penalties, color="#4e79a7")
    axes[0].axhline(summary["near_tie_rel_threshold"], color="#e15759", linewidth=1.0, linestyle="--")
    axes[0].set_ylabel("relative objective penalty")
    axes[0].set_title("Near-tie cost")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(labels, clearance_gains, color="#59a14f")
    axes[1].set_ylabel("clearance gain (mm)")
    axes[1].set_title("Downstream clearance")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[2].bar(labels, unlocks, color=["#59a14f" if value else "#bab0ac" for value in unlocks])
    axes[2].set_yticks([0, 1], ["no", "yes"])
    axes[2].set_ylim(0, 1.15)
    axes[2].set_title("Unlocks downstream truth geometry")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[2].text(
        0.04,
        0.08,
        f"ready={summary['ready_for_single_guarded_unlock_probe']}\n"
        f"probe target={summary['unlock_probe_target_index']}\n"
        f"gpu={summary['gpu_priority']}",
        transform=axes[2].transAxes,
        ha="left",
        va="bottom",
        fontsize=8.3,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Fixed-radius near-tie locking policy design", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_fixed_radius_locking_policy_design.png`",
                "",
                "This CPU-only figure designs a truth-free near-tie downstream-clearance",
                "lock after the fixed-radius second-pass residual audit.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Near-tie relative threshold: `{summary['near_tie_rel_threshold']}`.",
                f"Selected lock target: `{summary['selected_lock_target_index']}`.",
                f"Selected lock coordinate: `[{summary['selected_lock_x_mm']},{summary['selected_lock_z_mm']}]` mm.",
                f"Ready for one guarded unlock probe: `{summary['ready_for_single_guarded_unlock_probe']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Scope boundary:",
                "",
                "This design can justify at most one guarded validation probe. It does",
                "not authorize a broad GPU queue, detector-seeded FWI, field transfer,",
                "3D/HPC work, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot-run", default=DEFAULT_PILOT_RUN)
    parser.add_argument("--residual-audit-run", default=DEFAULT_RESIDUAL_AUDIT_RUN)
    parser.add_argument("--near-tie-rel", type=float, default=DEFAULT_NEAR_TIE_REL)
    parser.add_argument("--run-name", default="local_2d_detector_fixed_radius_locking_policy_design")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pilot_dir = Path("outputs/experiments") / args.pilot_run
    residual_dir = Path("outputs/summary_tables") / args.residual_audit_run
    optimizer_summary = read_json(pilot_dir / "data/multi_rebar_coordinate_optimizer_summary.json")
    residual_rows = read_csv_rows(
        residual_dir / "data/local_2d_detector_fixed_radius_residual_ambiguity_rows.csv"
    )
    residual_summary = read_json(
        residual_dir / "data/local_2d_detector_fixed_radius_residual_ambiguity_summary.json"
    )
    lock_rows = build_lock_candidate_rows(
        optimizer_summary,
        residual_rows,
        near_tie_rel=args.near_tie_rel,
    )
    policy_rows = build_policy_rows(lock_rows, residual_summary, optimizer_summary)
    summary = summarize_design(
        optimizer_summary,
        residual_summary,
        lock_rows,
        policy_rows,
        near_tie_rel=args.near_tie_rel,
    )
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root="outputs/summary_tables"))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    lock_csv = data_dir / "local_2d_detector_fixed_radius_lock_candidates.csv"
    policy_csv = data_dir / "local_2d_detector_fixed_radius_lock_policy_variants.csv"
    gates_csv = data_dir / "local_2d_detector_fixed_radius_locking_policy_gates.csv"
    summary_json = data_dir / "local_2d_detector_fixed_radius_locking_policy_summary.json"
    command_txt = data_dir / "recommended_guarded_unlock_probe_command.txt"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_fixed_radius_locking_policy_design.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(lock_csv, [json_safe(row) for row in lock_rows])
    write_csv(policy_csv, [json_safe(row) for row in policy_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_design(summary, lock_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary)
    command_txt.write_text(guarded_unlock_command(summary) + "\n", encoding="utf-8")

    output_summary = {
        **summary,
        "paths": {
            "lock_candidates_csv": str(lock_csv),
            "policy_variants_csv": str(policy_csv),
            "gates_csv": str(gates_csv),
            "summary_json": str(summary_json),
            "recommended_guarded_unlock_probe_command_txt": str(command_txt),
            "source_optimizer_summary_json": str(pilot_dir / "data/multi_rebar_coordinate_optimizer_summary.json"),
            "source_residual_summary_json": str(
                residual_dir / "data/local_2d_detector_fixed_radius_residual_ambiguity_summary.json"
            ),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_fixed_radius_locking_policy_design",
        {
            "summary_json": str(summary_json),
            "lock_candidates_csv": str(lock_csv),
            "policy_variants_csv": str(policy_csv),
            "gates_csv": str(gates_csv),
            "figure_validation_csv": str(validation_csv),
            "recommended_guarded_unlock_probe_command_txt": str(command_txt),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

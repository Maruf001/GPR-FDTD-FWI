#!/usr/bin/env python3
"""Synthesize fixed-radius detector pilot outcomes and pick one next probe."""

from __future__ import annotations

import argparse
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
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from run_local_2d_detector_radius_material_prior_scope_audit import parse_float_list  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_PREFLIGHT_RUN = "091_local_2d_detector_exact_radius_seed_nonoverlap_preflight"
DEFAULT_REPAIR_RUN = "092_local_2d_detector_exact_radius_seed_repair_design"
DEFAULT_PILOT_RUNS = [
    "1340_local2d_controlled_fixed_radius_seed_refine_target2_close14_seed21_source_mismatch_gpu",
    "1341_local2d_repaired_exact_radius_seed_refine_target2_close14_seed21_nominal_gpu",
    "1357_local2d_fixed_radius_second_pass_target2_close14_seed21_nominal_gpu",
]
DEFAULT_MAX_RAM_PERCENT = 80.0
DEFAULT_MAX_GPU_UTIL_PERCENT = 90.0


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def format_values(values: list[float]) -> str:
    return ",".join(f"{float(value):g}" for value in values)


def parse_values(value: object) -> list[float]:
    if isinstance(value, list):
        return [float(item) for item in value]
    text = str(value or "").strip()
    if not text:
        return []
    if text.startswith("["):
        return [float(item) for item in json.loads(text)]
    return parse_float_list(text)


def vector_errors(values: list[float], truth: list[float]) -> list[float]:
    if len(values) != len(truth):
        raise ValueError(f"vector length mismatch: {values!r} vs {truth!r}")
    return [round(float(value) - float(expected), 10) for value, expected in zip(values, truth)]


def linf(values: list[float]) -> float:
    return max((abs(float(value)) for value in values), default=0.0)


def vectors_close(first: list[float], second: list[float], tolerance: float = 1.0e-9) -> bool:
    return len(first) == len(second) and all(abs(a - b) <= tolerance for a, b in zip(first, second))


def infer_case_label(summary: dict, known_branch_keys: list[str]) -> tuple[str, str, int, str]:
    run_name = str(summary.get("run_name", ""))
    branch_key = ""
    for candidate in sorted(known_branch_keys, key=len, reverse=True):
        if candidate and candidate in run_name:
            branch_key = candidate
            break
    if not branch_key:
        branch_key = str(summary.get("branch_key", "unknown"))
    case_variant = str(summary.get("update_case_label") or "")
    replication_cases = summary.get("replication_cases") or []
    seed = 0
    if replication_cases:
        seed = safe_int(replication_cases[0].get("noise_seed"), 0)
        case_variant = case_variant or str(replication_cases[0].get("label") or "")
    return f"{branch_key}|seed{seed}|{case_variant}", branch_key, seed, case_variant


def seed_source_kind(case_label: str, summary: dict, preflight_by_case: dict[str, dict], repair_by_case: dict[str, dict]) -> str:
    initial_x = parse_values(summary.get("initial_state", {}).get("x_values_mm", []))
    initial_z = parse_values(summary.get("initial_state", {}).get("z_values_mm", []))
    repair = repair_by_case.get(case_label)
    if repair:
        repaired_x = parse_values(repair.get("repaired_x_values_mm"))
        repaired_z = parse_values(repair.get("repaired_z_values_mm"))
        if vectors_close(initial_x, repaired_x) and vectors_close(initial_z, repaired_z):
            return "repaired_seed"
    preflight = preflight_by_case.get(case_label)
    if preflight:
        seed_x = parse_values(preflight.get("x_seed_values_mm"))
        seed_z = parse_values(preflight.get("z_seed_values_mm"))
        if boolish(preflight.get("direct_fixed_radius_pilot_ready")) and vectors_close(initial_x, seed_x) and vectors_close(initial_z, seed_z):
            return "direct_preflight_seed"
        if vectors_close(initial_x, seed_x) and vectors_close(initial_z, seed_z):
            return "raw_preflight_seed"
    return "unmatched_seed"


def pilot_row_from_summary(
    summary: dict,
    *,
    preflight_by_case: dict[str, dict],
    repair_by_case: dict[str, dict],
    known_branch_keys: list[str],
) -> dict:
    case_label, branch_key, seed, case_variant = infer_case_label(summary, known_branch_keys)
    true_x = parse_values(summary.get("true_x_values_mm", []))
    true_z = parse_values(summary.get("true_z_values_mm", []))
    truth_radii = parse_values(summary.get("truth_radius_values_mm") or summary.get("truth_radius_mm"))
    initial = summary.get("initial_state", {})
    final = summary.get("final_state", {})
    initial_x = parse_values(initial.get("x_values_mm", []))
    initial_z = parse_values(initial.get("z_values_mm", []))
    final_x = parse_values(final.get("x_values_mm", []))
    final_z = parse_values(final.get("z_values_mm", []))
    final_radii = parse_values(final.get("radii_mm", []))

    initial_x_errors = vector_errors(initial_x, true_x)
    initial_z_errors = vector_errors(initial_z, true_z)
    final_x_errors = vector_errors(final_x, true_x)
    final_z_errors = vector_errors(final_z, true_z)
    initial_linf = max(linf(initial_x_errors), linf(initial_z_errors))
    final_linf = max(linf(final_x_errors), linf(final_z_errors))
    confidence_rows = summary.get("confidence_rows", [])
    candidate_counts = [safe_int(row.get("candidate_count"), 0) for row in confidence_rows]
    radius_missing = [
        row for row in confidence_rows
        if str(row.get("confidence_label", "")).strip().lower() == "missing"
    ]
    final_exact = final_linf <= 1.0e-9
    if final_exact:
        outcome = "exact_recovery"
        followup = "none"
    elif final_linf <= 1.0:
        outcome = "within_one_mm_residual"
        followup = "cpu_interpretation_before_more_gpu"
    elif final_linf <= 2.0:
        outcome = "near_residual"
        followup = "single_guarded_second_pass_probe"
    elif final_linf < initial_linf:
        outcome = "improved_not_close"
        followup = "defer_until_second_pass_policy_is_resolved"
    else:
        outcome = "no_improvement"
        followup = "defer"

    return {
        "run_name": summary.get("run_name", ""),
        "case_label": case_label,
        "branch_key": branch_key,
        "seed": seed,
        "case_variant": case_variant,
        "backend": summary.get("backend", ""),
        "sources": safe_int(summary.get("sources"), 0),
        "tx_rx_offset_mm": safe_float(summary.get("tx_rx_offset_mm"), math.nan),
        "receiver_sampling": summary.get("receiver_sampling", ""),
        "frequency_ghz": safe_float(summary.get("frequency_ghz"), math.nan),
        "seed_source_kind": seed_source_kind(case_label, summary, preflight_by_case, repair_by_case),
        "initial_x_values_mm": format_values(initial_x),
        "initial_z_values_mm": format_values(initial_z),
        "final_x_values_mm": format_values(final_x),
        "final_z_values_mm": format_values(final_z),
        "truth_x_values_mm": format_values(true_x),
        "truth_z_values_mm": format_values(true_z),
        "truth_radius_values_mm": format_values(truth_radii),
        "final_radius_values_mm": format_values(final_radii),
        "initial_x_errors_mm": format_values(initial_x_errors),
        "initial_z_errors_mm": format_values(initial_z_errors),
        "final_x_errors_mm": format_values(final_x_errors),
        "final_z_errors_mm": format_values(final_z_errors),
        "initial_x_linf_mm": linf(initial_x_errors),
        "initial_z_linf_mm": linf(initial_z_errors),
        "initial_linf_mm": initial_linf,
        "final_x_linf_mm": linf(final_x_errors),
        "final_z_linf_mm": linf(final_z_errors),
        "final_linf_mm": final_linf,
        "linf_improvement_mm": initial_linf - final_linf,
        "final_exact_truth": final_exact,
        "final_within_1mm": final_linf <= 1.0,
        "final_within_2mm": final_linf <= 2.0,
        "outcome_label": outcome,
        "recommended_followup": followup,
        "candidate_count_min": min(candidate_counts) if candidate_counts else 0,
        "candidate_count_by_target": format_values([float(value) for value in candidate_counts]),
        "radius_confidence_missing_count": len(radius_missing),
        "elapsed_time_s": safe_float(summary.get("elapsed_time_s"), math.nan),
        "gpu_guard_required_for_followup": followup == "single_guarded_second_pass_probe",
        "allowed_use": "fixed-radius detector-seed refinement outcome synthesis",
        "blocked_use": "broad GPU queue, detector-inferred radius/material, field transfer, FWI launch",
    }


def build_pilot_rows(pilot_summaries: list[dict], preflight_rows: list[dict], repair_rows: list[dict]) -> list[dict]:
    preflight_by_case = {str(row.get("case_label", "")): row for row in preflight_rows}
    repair_by_case = {str(row.get("case_label", "")): row for row in repair_rows}
    branch_keys = sorted({str(row.get("branch_key", "")) for row in preflight_rows if row.get("branch_key")})
    return [
        pilot_row_from_summary(
            summary,
            preflight_by_case=preflight_by_case,
            repair_by_case=repair_by_case,
            known_branch_keys=branch_keys,
        )
        for summary in pilot_summaries
    ]


def build_candidate_coverage_rows(preflight_rows: list[dict], repair_rows: list[dict], pilot_rows: list[dict]) -> list[dict]:
    repairs = {str(row.get("case_label", "")): row for row in repair_rows}
    pilots_by_case: dict[str, list[dict]] = {}
    for row in pilot_rows:
        pilots_by_case.setdefault(str(row.get("case_label", "")), []).append(row)

    rows: list[dict] = []
    for preflight in sorted(preflight_rows, key=lambda item: str(item.get("case_label", ""))):
        case_label = str(preflight.get("case_label", ""))
        direct_ready = boolish(preflight.get("direct_fixed_radius_pilot_ready"))
        repair = repairs.get(case_label)
        repair_ready = boolish(repair.get("ready_for_repaired_fixed_radius_pilot")) if repair else False
        pilots = pilots_by_case.get(case_label, [])
        best_linf = min((safe_float(row.get("final_linf_mm"), math.inf) for row in pilots), default=math.inf)
        if pilots:
            coverage_status = "tested"
        elif direct_ready:
            coverage_status = "untested_direct_ready"
        elif repair_ready:
            coverage_status = "untested_repaired_ready"
        else:
            coverage_status = "blocked"

        launch_x = parse_values(preflight.get("x_seed_values_mm"))
        launch_z = parse_values(preflight.get("z_seed_values_mm"))
        seed_kind = "direct_preflight_seed" if direct_ready else "blocked"
        if repair_ready:
            launch_x = parse_values(repair.get("repaired_x_values_mm"))
            launch_z = parse_values(repair.get("repaired_z_values_mm"))
            seed_kind = "repaired_seed"

        rows.append(
            {
                "case_label": case_label,
                "branch_key": preflight.get("branch_key", ""),
                "seed": safe_int(preflight.get("seed"), 0),
                "case_variant": preflight.get("case_variant", ""),
                "seed_source_kind": seed_kind,
                "coverage_status": coverage_status,
                "direct_fixed_radius_pilot_ready": direct_ready,
                "ready_for_repaired_fixed_radius_pilot": repair_ready,
                "tested_pilot_count": len(pilots),
                "tested_pilot_run_names": ";".join(str(row.get("run_name", "")) for row in pilots),
                "best_observed_final_linf_mm": None if not math.isfinite(best_linf) else best_linf,
                "best_observed_outcome_label": min(
                    (str(row.get("outcome_label", "")) for row in pilots),
                    default="",
                ),
                "launch_seed_x_values_mm": format_values(launch_x),
                "launch_seed_z_values_mm": format_values(launch_z),
                "min_pair_clearance_mm": safe_float(preflight.get("min_pair_clearance_mm"), math.nan),
                "min_pair_clearance_after_repair_mm": (
                    safe_float(repair.get("min_pair_clearance_after_repair_mm"), math.nan)
                    if repair else None
                ),
                "eligible_for_one_case_backlog": (not pilots) and (direct_ready or repair_ready),
                "ready_for_broad_gpu_queue": False,
                "ready_for_detector_seeded_fwi": False,
                "allowed_use": "one-case-at-a-time fixed-radius pilot backlog"
                if (direct_ready or repair_ready) else "preflight blocker",
                "blocked_use": "broad GPU queue, field transfer, detector-inferred radius/material, FWI launch",
            }
        )
    return rows


def best_observed_pilot(pilot_rows: list[dict]) -> dict | None:
    if not pilot_rows:
        return None
    return sorted(
        pilot_rows,
        key=lambda row: (
            safe_float(row.get("final_linf_mm"), math.inf),
            -safe_float(row.get("linf_improvement_mm"), -math.inf),
            str(row.get("run_name", "")),
        ),
    )[0]


def select_best_second_pass(pilot_rows: list[dict]) -> dict | None:
    if any(
        row.get("outcome_label") in {"exact_recovery", "within_one_mm_residual"}
        for row in pilot_rows
    ):
        return None
    candidates = [
        row for row in pilot_rows
        if row["recommended_followup"] == "single_guarded_second_pass_probe"
    ]
    if not candidates:
        return None
    return sorted(
        candidates,
        key=lambda row: (
            safe_float(row.get("final_linf_mm"), math.inf),
            -safe_float(row.get("linf_improvement_mm"), -math.inf),
            str(row.get("run_name", "")),
        ),
    )[0]


def build_selector_rows(
    pilot_rows: list[dict],
    coverage_rows: list[dict],
    *,
    max_ram_percent: float = DEFAULT_MAX_RAM_PERCENT,
    max_gpu_util_percent: float = DEFAULT_MAX_GPU_UTIL_PERCENT,
) -> list[dict]:
    rows: list[dict] = []
    best = select_best_second_pass(pilot_rows)
    if best:
        rows.append(
            {
                "selector_rank": 1,
                "action_key": "single_guarded_second_pass_probe",
                "case_label": best["case_label"],
                "branch_key": best["branch_key"],
                "seed": best["seed"],
                "case_variant": best["case_variant"],
                "seed_source_kind": best["seed_source_kind"],
                "initial_x_values_mm": best["final_x_values_mm"],
                "initial_z_values_mm": best["final_z_values_mm"],
                "initial_radius_values_mm": best["final_radius_values_mm"],
                "x_offsets_mm": "-2,-1,0,1,2",
                "z_offsets_mm": "-2,-1,0,1,2",
                "radius_offsets_mm": "0",
                "target_indices": "0,1,2",
                "passes": 1,
                "expected_candidates_per_target": 25,
                "ready_now": True,
                "requires_gpu_guard": True,
                "max_ram_percent": float(max_ram_percent),
                "max_gpu_util_percent": float(max_gpu_util_percent),
                "rationale": (
                    "Best completed fixed-radius pilot is within 2 mm but has persistent "
                    "lateral residuals; a one-case second pass tests whether the residual "
                    "is optimizer-policy limited before spending on fresh cases."
                ),
                "allowed_use": "single guarded local GPU probe under resource caps",
                "blocked_use": "broad detector queue, FWI, field transfer",
            }
        )

    backlog = [
        row for row in coverage_rows
        if boolish(row.get("eligible_for_one_case_backlog"))
    ]
    def backlog_key(row: dict) -> tuple[int, int, float, str]:
        branch = str(row.get("branch_key", ""))
        status = str(row.get("coverage_status", ""))
        close14_rank = 0 if branch == "target2_close14" else 1
        direct_rank = 0 if status == "untested_direct_ready" else 1
        clearance = safe_float(row.get("min_pair_clearance_mm"), -math.inf)
        return close14_rank, direct_rank, -clearance, str(row.get("case_label", ""))

    for idx, row in enumerate(sorted(backlog, key=backlog_key)[:4], start=len(rows) + 1):
        rows.append(
            {
                "selector_rank": idx,
                "action_key": "fresh_one_case_backlog_after_second_pass_decision",
                "case_label": row["case_label"],
                "branch_key": row["branch_key"],
                "seed": row["seed"],
                "case_variant": row["case_variant"],
                "seed_source_kind": row["seed_source_kind"],
                "initial_x_values_mm": row["launch_seed_x_values_mm"],
                "initial_z_values_mm": row["launch_seed_z_values_mm"],
                "initial_radius_values_mm": "5,6,8",
                "x_offsets_mm": "-4,-2,0,2,4",
                "z_offsets_mm": "-4,-2,0,2,4",
                "radius_offsets_mm": "0",
                "target_indices": "0,1,2",
                "passes": 1,
                "expected_candidates_per_target": 25,
                "ready_now": False,
                "requires_gpu_guard": True,
                "max_ram_percent": float(max_ram_percent),
                "max_gpu_util_percent": float(max_gpu_util_percent),
                "rationale": (
                    "Eligible one-case backlog only after the second-pass policy question "
                    "is resolved; do not launch as a queue."
                ),
                "allowed_use": "future one-case guarded pilot candidate",
                "blocked_use": "broad detector queue, FWI, field transfer",
            }
        )
    return rows


def summarize(
    preflight_summary: dict,
    repair_summary: dict,
    pilot_rows: list[dict],
    coverage_rows: list[dict],
    selector_rows: list[dict],
) -> dict:
    tested = [row for row in coverage_rows if row["coverage_status"] == "tested"]
    untested_direct = [row for row in coverage_rows if row["coverage_status"] == "untested_direct_ready"]
    untested_repaired = [row for row in coverage_rows if row["coverage_status"] == "untested_repaired_ready"]
    exact = [row for row in pilot_rows if boolish(row.get("final_exact_truth"))]
    within_one = [row for row in pilot_rows if row.get("outcome_label") == "within_one_mm_residual"]
    near = [row for row in pilot_rows if row.get("outcome_label") == "near_residual"]
    improved = [row for row in pilot_rows if row.get("outcome_label") == "improved_not_close"]
    best = best_observed_pilot(pilot_rows)
    selected = next((row for row in selector_rows if boolish(row.get("ready_now"))), None)
    if within_one:
        decision = (
            "The guarded second-pass fixed-radius detector pilot reduced the best repaired "
            "case to a 1 mm residual but did not reach exact recovery. Stop immediate GPU "
            "iteration and synthesize the remaining near-competitor ambiguity before any "
            "fresh detector-seed coverage. Keep broad GPU queues, field transfer, "
            "detector-inferred radius/material, and FWI blocked."
        )
    else:
        decision = (
            "The completed fixed-radius detector pilots are useful but not clean recoveries. "
            "Run at most one guarded second-pass probe from the repaired seed21 nominal final "
            "state before spending GPU time on fresh detector-seed coverage. Keep broad GPU "
            "queues, field transfer, detector-inferred radius/material, and FWI blocked."
        )
    return {
        "policy_label": "local_2d_detector_fixed_radius_pilot_outcome_synthesis_cpu_selector",
        "source_preflight_policy_label": preflight_summary.get("policy_label", ""),
        "source_repair_policy_label": repair_summary.get("policy_label", ""),
        "stable_seed_case_count": safe_int(preflight_summary.get("stable_seed_case_count"), len(coverage_rows)),
        "direct_fixed_radius_pilot_ready_count": safe_int(preflight_summary.get("direct_fixed_radius_pilot_ready_count"), 0),
        "repair_ready_count": safe_int(repair_summary.get("repair_found_count"), 0),
        "pilot_run_count": len(pilot_rows),
        "tested_case_count": len(tested),
        "untested_direct_ready_count": len(untested_direct),
        "untested_repaired_ready_count": len(untested_repaired),
        "exact_recovery_pilot_count": len(exact),
        "within_one_mm_residual_pilot_count": len(within_one),
        "near_residual_pilot_count": len(near),
        "improved_not_close_pilot_count": len(improved),
        "best_pilot_run_name": "" if best is None else best["run_name"],
        "best_case_label": "" if best is None else best["case_label"],
        "best_final_linf_mm": None if best is None else best["final_linf_mm"],
        "best_final_x_linf_mm": None if best is None else best["final_x_linf_mm"],
        "best_final_z_linf_mm": None if best is None else best["final_z_linf_mm"],
        "best_linf_improvement_mm": None if best is None else best["linf_improvement_mm"],
        "selected_next_action": "" if selected is None else selected["action_key"],
        "selected_next_case_label": "" if selected is None else selected["case_label"],
        "selected_next_seed_source_kind": "" if selected is None else selected["seed_source_kind"],
        "selected_next_initial_x_values_mm": "" if selected is None else selected["initial_x_values_mm"],
        "selected_next_initial_z_values_mm": "" if selected is None else selected["initial_z_values_mm"],
        "selected_next_x_offsets_mm": "" if selected is None else selected["x_offsets_mm"],
        "selected_next_z_offsets_mm": "" if selected is None else selected["z_offsets_mm"],
        "ready_for_single_guarded_second_pass_probe": selected is not None,
        "ready_for_fresh_one_case_probe_now": False,
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_field_transfer": False,
        "ready_for_detector_inferred_radius_material": False,
        "max_ram_percent": DEFAULT_MAX_RAM_PERCENT,
        "max_gpu_util_percent": DEFAULT_MAX_GPU_UTIL_PERCENT,
        "gpu_priority": "single_guarded_second_pass_candidate" if selected is not None else "none",
        "decision": decision,
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "single_guarded_second_pass_probe",
            "ready": summary["ready_for_single_guarded_second_pass_probe"],
            "allowed_use": "one guarded local GPU probe under caps",
            "blocked_use": "multi-case queue",
            "evidence": (
                f"best final Linf={summary['best_final_linf_mm']} mm; "
                f"case={summary['best_case_label']}"
            ),
        },
        {
            "gate_key": "fresh_one_case_probe_now",
            "ready": summary["ready_for_fresh_one_case_probe_now"],
            "allowed_use": "none until residual ambiguity is interpreted",
            "blocked_use": "fresh detector-seed coverage before residual synthesis",
            "evidence": (
                f"untested direct={summary['untested_direct_ready_count']}; "
                f"untested repaired={summary['untested_repaired_ready_count']}"
            ),
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "broad fixed-radius detector-seed GPU queue",
            "evidence": (
                f"pilot outcomes={summary['pilot_run_count']}; "
                f"exact={summary['exact_recovery_pilot_count']}; "
                f"best Linf={summary['best_final_linf_mm']} mm"
            ),
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "FWI launch",
            "evidence": "fixed-radius local coordinate pilots are not FWI readiness evidence",
        },
    ]


def plot_synthesis(summary: dict, pilot_rows: list[dict], coverage_rows: list[dict], save_path: Path) -> str:
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.7), constrained_layout=True)

    labels = [str(row["case_label"]).replace("|", "\n") for row in pilot_rows]
    initial = [safe_float(row.get("initial_linf_mm"), 0.0) for row in pilot_rows]
    final = [safe_float(row.get("final_linf_mm"), 0.0) for row in pilot_rows]
    xs = list(range(len(pilot_rows)))
    width = 0.36
    axes[0].bar([x - width / 2 for x in xs], initial, width=width, label="initial", color="#4e79a7")
    axes[0].bar([x + width / 2 for x in xs], final, width=width, label="final", color="#59a14f")
    axes[0].set_xticks(xs, labels, fontsize=7.5)
    axes[0].set_ylabel("L-infinity coordinate error (mm)")
    axes[0].set_title("Completed pilots")
    axes[0].legend(frameon=False)
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    coverage_order = ["tested", "untested_direct_ready", "untested_repaired_ready", "blocked"]
    coverage_counts = [
        sum(1 for row in coverage_rows if row["coverage_status"] == key)
        for key in coverage_order
    ]
    axes[1].bar(
        ["tested", "direct\nbacklog", "repaired\nbacklog", "blocked"],
        coverage_counts,
        color=["#59a14f", "#f28e2b", "#edc948", "#bab0ac"],
    )
    axes[1].set_ylabel("case count")
    axes[1].set_title("Stable seed coverage")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    gate_labels = ["second\npass", "fresh\nnow", "broad\nGPU", "FWI"]
    gate_values = [
        summary["ready_for_single_guarded_second_pass_probe"],
        summary["ready_for_fresh_one_case_probe_now"],
        summary["ready_for_broad_gpu_queue"],
        summary["ready_for_detector_seeded_fwi"],
    ]
    axes[2].bar(
        gate_labels,
        [1 if value else 0 for value in gate_values],
        color=["#59a14f" if value else "#bab0ac" for value in gate_values],
    )
    axes[2].set_yticks([0, 1], ["blocked", "ready"])
    axes[2].set_ylim(0, 1.15)
    axes[2].set_title("Next-action gates")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[2].text(
        0.04,
        0.08,
        f"selected={summary['selected_next_case_label']}\n"
        f"best Linf={summary['best_final_linf_mm']} mm\n"
        f"GPU cap={summary['max_gpu_util_percent']:.0f}%\n"
        f"RAM cap={summary['max_ram_percent']:.0f}%",
        transform=axes[2].transAxes,
        ha="left",
        va="bottom",
        fontsize=8.3,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )

    fig.suptitle("Fixed-radius detector pilot outcome synthesis", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_fixed_radius_pilot_outcome_synthesis.png`",
                "",
                "This CPU-only figure synthesizes the completed fixed-radius detector",
                "seed pilots against the exact-radius non-overlap preflight and repair",
                "design. It is a selector, not a launch queue.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Pilot runs included: `{summary['pilot_run_count']}`.",
                f"Best case: `{summary['best_case_label']}`.",
                f"Best final L-infinity error: `{summary['best_final_linf_mm']}` mm.",
                f"Selected next action: `{summary['selected_next_action']}`.",
                f"GPU cap for any selected probe: `{summary['max_gpu_util_percent']}` percent.",
                f"RAM cap for any selected probe: `{summary['max_ram_percent']}` percent.",
                "",
                "Scope boundary:",
                "",
                "The artifact authorizes at most one guarded second-pass probe. It does",
                "not authorize broad GPU queues, detector-inferred radius/material claims,",
                "field transfer, 3D/HPC work, neural-network training, or FWI.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def guarded_command_text(selector_row: dict) -> str:
    if not selector_row:
        return ""
    run_name = "local2d_fixed_radius_second_pass_target2_close14_seed21_nominal_gpu"
    if selector_row["case_label"] != "target2_close14|seed21|nominal":
        suffix = str(selector_row["case_label"]).replace("|", "_").replace("seed", "seed")
        run_name = f"local2d_fixed_radius_second_pass_{suffix}_gpu"
    command = [
        "conda", "run", "-n", "gpr-fdtd-fwi", "python", "run_resource_guarded_command.py",
        "--max-ram-percent", f"{selector_row['max_ram_percent']:g}",
        "--max-gpu-util-percent", f"{selector_row['max_gpu_util_percent']:g}",
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
        "--truth-radius-values-mm", selector_row["initial_radius_values_mm"],
        "--initial-x-values-mm", selector_row["initial_x_values_mm"],
        "--initial-z-values-mm", selector_row["initial_z_values_mm"],
        "--initial-radius-values-mm", selector_row["initial_radius_values_mm"],
        "--target-indices", selector_row["target_indices"],
        "--passes", str(selector_row["passes"]),
        f"--x-offsets-mm={selector_row['x_offsets_mm']}",
        f"--z-offsets-mm={selector_row['z_offsets_mm']}",
        "--radius-offsets-mm", selector_row["radius_offsets_mm"],
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight-run", default=DEFAULT_PREFLIGHT_RUN)
    parser.add_argument("--repair-run", default=DEFAULT_REPAIR_RUN)
    parser.add_argument("--pilot-runs", default=",".join(DEFAULT_PILOT_RUNS))
    parser.add_argument("--run-name", default="local_2d_detector_fixed_radius_pilot_outcome_synthesis")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path("outputs/summary_tables")
    experiment_root = Path("outputs/experiments")
    preflight_dir = summary_root / args.preflight_run
    repair_dir = summary_root / args.repair_run

    preflight_rows = read_csv_rows(
        preflight_dir / "data/local_2d_detector_exact_radius_seed_nonoverlap_preflight_cases.csv"
    )
    preflight_summary = read_json(
        preflight_dir / "data/local_2d_detector_exact_radius_seed_nonoverlap_preflight_summary.json"
    )
    repair_rows = read_csv_rows(
        repair_dir / "data/local_2d_detector_exact_radius_seed_repair_design_rows.csv"
    )
    repair_summary = read_json(
        repair_dir / "data/local_2d_detector_exact_radius_seed_repair_design_summary.json"
    )
    pilot_run_names = [part.strip() for part in str(args.pilot_runs).split(",") if part.strip()]
    pilot_summaries = [
        read_json(experiment_root / run / "data/multi_rebar_coordinate_optimizer_summary.json")
        for run in pilot_run_names
    ]

    pilot_rows = build_pilot_rows(pilot_summaries, preflight_rows, repair_rows)
    coverage_rows = build_candidate_coverage_rows(preflight_rows, repair_rows, pilot_rows)
    selector_rows = build_selector_rows(coverage_rows=coverage_rows, pilot_rows=pilot_rows)
    summary = summarize(preflight_summary, repair_summary, pilot_rows, coverage_rows, selector_rows)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root="outputs/summary_tables"))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    pilot_csv = data_dir / "local_2d_detector_fixed_radius_pilot_outcomes.csv"
    coverage_csv = data_dir / "local_2d_detector_fixed_radius_candidate_coverage.csv"
    selector_csv = data_dir / "local_2d_detector_fixed_radius_next_pilot_selector.csv"
    gates_csv = data_dir / "local_2d_detector_fixed_radius_pilot_outcome_gates.csv"
    summary_json = data_dir / "local_2d_detector_fixed_radius_pilot_outcome_synthesis_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    command_txt = data_dir / "recommended_guarded_command.txt"
    figure_path = figures_dir / "local_2d_detector_fixed_radius_pilot_outcome_synthesis.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(pilot_csv, [json_safe(row) for row in pilot_rows])
    write_csv(coverage_csv, [json_safe(row) for row in coverage_rows])
    write_csv(selector_csv, [json_safe(row) for row in selector_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_synthesis(summary, pilot_rows, coverage_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary)
    ready_selector = next((row for row in selector_rows if boolish(row.get("ready_now"))), {})
    command_txt.write_text(guarded_command_text(ready_selector) + "\n", encoding="utf-8")

    output_summary = {
        **summary,
        "paths": {
            "pilot_outcomes_csv": str(pilot_csv),
            "candidate_coverage_csv": str(coverage_csv),
            "next_pilot_selector_csv": str(selector_csv),
            "gates_csv": str(gates_csv),
            "summary_json": str(summary_json),
            "recommended_guarded_command_txt": str(command_txt),
            "source_preflight_summary_json": str(
                preflight_dir / "data/local_2d_detector_exact_radius_seed_nonoverlap_preflight_summary.json"
            ),
            "source_repair_summary_json": str(
                repair_dir / "data/local_2d_detector_exact_radius_seed_repair_design_summary.json"
            ),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_fixed_radius_pilot_outcome_synthesis",
        {
            "summary_json": str(summary_json),
            "pilot_outcomes_csv": str(pilot_csv),
            "candidate_coverage_csv": str(coverage_csv),
            "next_pilot_selector_csv": str(selector_csv),
            "gates_csv": str(gates_csv),
            "figure_validation_csv": str(validation_csv),
            "recommended_guarded_command_txt": str(command_txt),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

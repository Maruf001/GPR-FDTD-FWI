#!/usr/bin/env python3
"""Close the seed2504730781961 target0 weak-exact exception from existing runs."""

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
from run_coordinate_objective_policy_matrix import figure_stats, safe_float  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_RUN_IDS = (1136, 1137, 1138, 1139, 1140)
RUN_DIR_RE = re.compile(r"^(\d{3,})_")
SEED_RE = re.compile(r"seed(\d+)")


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_union_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        write_csv(path, [])
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    write_csv(path, [{key: row.get(key, "") for key in fieldnames} for row in rows])


def find_run_dir(run_id: int, experiments_root: Path = Path("outputs/experiments")) -> Path:
    matches = sorted(path for path in experiments_root.glob(f"{run_id}_*") if path.is_dir())
    if not matches:
        raise FileNotFoundError(f"could not find output directory for run {run_id}")
    return matches[0]


def run_id_from_dir(run_dir: Path) -> int:
    match = RUN_DIR_RE.match(run_dir.name)
    if not match:
        raise ValueError(f"run directory is not numbered: {run_dir}")
    return int(match.group(1))


def parse_seed(case_label: str) -> int | None:
    match = SEED_RE.search(case_label)
    return int(match.group(1)) if match else None


def close_enough(left: float, right: float, *, tol: float = 1.0e-9) -> bool:
    return math.isfinite(left) and math.isfinite(right) and math.isclose(left, right, abs_tol=tol)


def sequence_close(left: list[float], right: list[float], *, tol: float = 1.0e-9) -> bool:
    return len(left) == len(right) and all(close_enough(a, b, tol=tol) for a, b in zip(left, right))


def row_target_exact(row: dict, summary: dict) -> bool:
    target = int(safe_float(row.get("target_rebar_index"), -1))
    if target < 0:
        return False
    true_x = summary.get("true_x_values_mm", [])
    true_z = summary.get("true_z_values_mm", [])
    true_r = summary.get("truth_radius_values_mm", summary.get("truth_radius_mm", []))
    if target >= min(len(true_x), len(true_z), len(true_r)):
        return False
    return (
        close_enough(safe_float(row.get("best_x_mm")), safe_float(true_x[target]))
        and close_enough(safe_float(row.get("best_z_mm")), safe_float(true_z[target]))
        and close_enough(safe_float(row.get("best_radius_mm")), safe_float(true_r[target]))
    )


def final_state_exact(summary: dict) -> bool:
    final_state = summary.get("final_state", {})
    return (
        sequence_close(
            [safe_float(value) for value in final_state.get("x_values_mm", [])],
            [safe_float(value) for value in summary.get("true_x_values_mm", [])],
        )
        and sequence_close(
            [safe_float(value) for value in final_state.get("z_values_mm", [])],
            [safe_float(value) for value in summary.get("true_z_values_mm", [])],
        )
        and sequence_close(
            [safe_float(value) for value in final_state.get("radii_mm", [])],
            [safe_float(value) for value in summary.get("truth_radius_values_mm", [])],
        )
    )


def followup_kind(*, sources: int, tx_rx_offset_mm: float, baseline_tx_rx_mm: float = 60.0) -> str:
    if sources > 8:
        return "source_density_probe"
    if not close_enough(tx_rx_offset_mm, baseline_tx_rx_mm):
        return "spacing_probe"
    return "baseline_control"


def collect_run_row(run_dir: Path, *, cutoff: float) -> dict:
    data_dir = run_dir / "data"
    summary_path = data_dir / "multi_rebar_coordinate_optimizer_summary.json"
    confidence_path = data_dir / "coordinate_confidence_report.csv"
    objective_path = data_dir / "coordinate_objective_diagnostics.csv"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    confidence_rows = read_csv_rows(confidence_path)
    objective_rows = read_csv_rows(objective_path)
    if not confidence_rows:
        raise ValueError(f"missing confidence row in {confidence_path}")

    confidence = confidence_rows[0]
    run_id = run_id_from_dir(run_dir)
    sources = int(safe_float(summary.get("sources"), safe_float(confidence.get("sources"), -1)))
    tx_rx = safe_float(summary.get("tx_rx_offset_mm"), safe_float(confidence.get("tx_rx_offset_mm")))
    target = int(safe_float(confidence.get("target_rebar_index"), -1))
    base_margin = safe_float(confidence.get("radius_margin_abs"))
    exact_target = row_target_exact(confidence, summary)
    exact_objective_labels = [
        str(row.get("objective_label", ""))
        for row in objective_rows
        if row_target_exact(row, summary)
    ]
    objective_margins = [
        (str(row.get("objective_label", "")), safe_float(row.get("radius_margin_abs")))
        for row in objective_rows
    ]
    above_cutoff = [label for label, margin in objective_margins if margin >= cutoff]
    below_cutoff = [label for label, margin in objective_margins if margin < cutoff]
    strongest_label, strongest_margin = max(
        objective_margins,
        key=lambda item: item[1] if math.isfinite(item[1]) else -math.inf,
    )
    kind = followup_kind(sources=sources, tx_rx_offset_mm=tx_rx)
    accepted = bool(exact_target and base_margin >= cutoff)
    if accepted and kind == "source_density_probe":
        decision = "accepted_source_density_rescue"
    elif accepted:
        decision = "accepted_existing_probe"
    elif exact_target:
        decision = "weak_truth_preserved"
    else:
        decision = "not_accepted_geometry_mismatch"

    return {
        "run_id": run_id,
        "seed": parse_seed(str(confidence.get("case_label", ""))),
        "target": target,
        "target_label": f"target{target}",
        "sources": sources,
        "tx_rx_offset_mm": tx_rx,
        "followup_kind": kind,
        "base_margin": base_margin,
        "margin_deficit": cutoff - base_margin,
        "confidence_label": confidence.get("confidence_label", ""),
        "fallback_warning": confidence.get("fallback_warning", ""),
        "best_x_mm": safe_float(confidence.get("best_x_mm")),
        "best_z_mm": safe_float(confidence.get("best_z_mm")),
        "best_radius_mm": safe_float(confidence.get("best_radius_mm")),
        "next_radius_mm": safe_float(confidence.get("next_radius_mm")),
        "exact_target_geometry": exact_target,
        "exact_final_geometry": final_state_exact(summary),
        "all_objective_variants_truth_exact": len(exact_objective_labels) == len(objective_rows),
        "objective_count": len(objective_rows),
        "objectives_above_cutoff_count": len(above_cutoff),
        "objectives_above_cutoff": ",".join(above_cutoff),
        "objectives_below_cutoff": ",".join(below_cutoff),
        "strongest_objective": strongest_label,
        "strongest_margin": strongest_margin,
        "decision": decision,
        "run_dir": str(run_dir),
    }


def synthesize_closure(rows: list[dict], *, cutoff: float) -> dict:
    ordered = sorted(rows, key=lambda row: int(row["run_id"]))
    accepted = [
        row for row in ordered
        if row["decision"].startswith("accepted") and row["exact_target_geometry"]
    ]
    source_density_accepts = [
        row for row in accepted
        if row["followup_kind"] == "source_density_probe"
    ]
    spacing_rows = [row for row in ordered if row["followup_kind"] == "spacing_probe"]
    baseline = next((row for row in ordered if row["followup_kind"] == "baseline_control"), ordered[0])
    best_spacing = max(spacing_rows, key=lambda row: safe_float(row["base_margin"]), default=None)
    best_overall = max(ordered, key=lambda row: safe_float(row["base_margin"]))

    if source_density_accepts:
        policy_label = "target0_exception_closed_by_source_density"
        gpu_priority = "none"
        decision = (
            "Do not run more target0 GPU work for this exception. Existing follow-ups "
            "show truth-preserving spacing probes that remain weak, followed by a "
            "9-source Tx/Rx=60 source-density rescue that clears the base confidence rule."
        )
    elif accepted:
        policy_label = "target0_exception_closed_by_existing_followup"
        gpu_priority = "none"
        decision = "Do not run more target0 GPU work for this exception; an existing follow-up clears the base rule."
    elif all(row["exact_target_geometry"] for row in ordered):
        policy_label = "target0_exception_truth_preserved_but_unclosed"
        gpu_priority = "candidate_narrow_probe"
        decision = "Truth is preserved, but no existing follow-up clears the base rule; only a narrow probe would be defensible."
    else:
        policy_label = "target0_exception_unresolved_geometry_mismatch"
        gpu_priority = "candidate_narrow_probe"
        decision = "At least one follow-up does not preserve target0 geometry; inspect before any broader sweep."

    return {
        "policy_label": policy_label,
        "cutoff": cutoff,
        "run_count": len(ordered),
        "run_ids": ",".join(str(row["run_id"]) for row in ordered),
        "baseline_run_id": baseline["run_id"],
        "baseline_base_margin": baseline["base_margin"],
        "best_spacing_run_id": best_spacing["run_id"] if best_spacing else "",
        "best_spacing_base_margin": best_spacing["base_margin"] if best_spacing else math.nan,
        "accepted_run_ids": ",".join(str(row["run_id"]) for row in accepted),
        "source_density_accept_run_ids": ",".join(str(row["run_id"]) for row in source_density_accepts),
        "best_overall_run_id": best_overall["run_id"],
        "best_overall_base_margin": best_overall["base_margin"],
        "best_overall_followup_kind": best_overall["followup_kind"],
        "baseline_to_best_spacing_margin_delta": (
            best_spacing["base_margin"] - baseline["base_margin"] if best_spacing else math.nan
        ),
        "baseline_to_best_overall_margin_delta": best_overall["base_margin"] - baseline["base_margin"],
        "best_overall_minus_best_spacing_margin": (
            best_overall["base_margin"] - best_spacing["base_margin"] if best_spacing else math.nan
        ),
        "all_runs_truth_exact": all(row["exact_target_geometry"] for row in ordered),
        "all_objective_variants_truth_exact": all(row["all_objective_variants_truth_exact"] for row in ordered),
        "late_window_caveat": any(
            "late" in str(row.get("objectives_below_cutoff", "")).split(",")
            or "late_high" in str(row.get("objectives_below_cutoff", "")).split(",")
            for row in ordered
        ),
        "gpu_priority": gpu_priority,
        "decision": decision,
    }


def plot_closure(rows: list[dict], summary: dict, save_path: Path) -> str:
    ordered = sorted(rows, key=lambda row: int(row["run_id"]))
    labels = [
        f"{row['run_id']}\n{row['sources']}src/{row['tx_rx_offset_mm']:g}mm"
        for row in ordered
    ]
    margins = [safe_float(row["base_margin"]) for row in ordered]
    colors = [
        "#2f9d55" if str(row["decision"]).startswith("accepted") else "#4c78a8"
        for row in ordered
    ]
    x = np.arange(len(ordered))

    fig, ax = plt.subplots(figsize=(10.5, 4.8), constrained_layout=True)
    ax.bar(x, margins, color=colors, width=0.62)
    ax.axhline(safe_float(summary["cutoff"]), color="#c7302b", linestyle="--", linewidth=1.1, label="5e-4 cutoff")
    ax.set_xticks(x, labels)
    ax.set_ylabel("base radius margin")
    ax.set_title("Target0 weak-exact exception closes under source-density rescue")
    ax.grid(axis="y", color="#dddddd", linewidth=0.6)
    ax.legend(frameon=False, fontsize=8)
    for xpos, margin, row in zip(x, margins, ordered):
        marker = "accepted" if str(row["decision"]).startswith("accepted") else "weak"
        ax.text(xpos, margin + 1.5e-5, marker, ha="center", va="bottom", fontsize=8)
    fig.suptitle(summary["policy_label"], fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-ids", default=",".join(str(value) for value in DEFAULT_RUN_IDS))
    parser.add_argument("--experiments-root", default="outputs/experiments")
    parser.add_argument("--cutoff", type=float, default=5.0e-4)
    parser.add_argument("--run-name", default="target0_exception_closure_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    experiments_root = Path(args.experiments_root)
    run_ids = [int(value.strip()) for value in args.run_ids.split(",") if value.strip()]
    rows = [
        collect_run_row(find_run_dir(run_id, experiments_root), cutoff=args.cutoff)
        for run_id in run_ids
    ]
    summary = synthesize_closure(rows, cutoff=args.cutoff)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "target0_exception_closure_rows.csv"
    summary_json = data_dir / "target0_exception_closure_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_closure(rows, summary, figures_dir / "target0_exception_closure_policy.png"))

    write_union_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        **summary,
        "paths": {
            "rows_csv": str(rows_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "target0_exception_closure_policy",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

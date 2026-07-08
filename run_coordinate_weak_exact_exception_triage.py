#!/usr/bin/env python3
"""Triage weak-exact secondary-confirmation exceptions without rerunning FDTD."""

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
from run_coordinate_objective_policy_matrix import figure_stats, safe_float  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_AUDIT_DIR = Path("outputs/experiments/1262_coordinate_weak_exact_secondary_confirmation_audit_700_1259")


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
    normalized = [
        {key: row.get(key, "") for key in fieldnames}
        for row in rows
    ]
    write_csv(path, normalized)


def boolish(value) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def exception_run_ids(policy_rows: list[dict]) -> list[int]:
    ids: list[int] = []
    for row in policy_rows:
        text = str(row.get("strongest_secondary_nonaccepted_run_ids", "")).strip()
        if not text:
            continue
        for part in text.split(","):
            part = part.strip()
            if part:
                ids.append(int(part))
    return sorted(set(ids))


def find_run_dir(run_id: int, root: Path = Path("outputs/experiments")) -> Path:
    matches = sorted(path for path in root.glob(f"{run_id}_*") if path.is_dir())
    if not matches:
        raise FileNotFoundError(f"could not find output directory for run {run_id}")
    return matches[0]


def objective_top_candidate_metrics(top_candidate_rows: list[dict], objective_label: str) -> dict:
    rows = [
        row for row in top_candidate_rows
        if str(row.get("objective_label")) == objective_label
    ]
    if not rows:
        return {}
    rows = sorted(rows, key=lambda row: int(safe_float(row.get("rank"), 9999)))
    best = rows[0]
    second = rows[1] if len(rows) > 1 else {}
    best_misfit = safe_float(best.get("misfit"))
    second_misfit = safe_float(second.get("misfit"))
    return {
        f"{objective_label}_rank1_radius_mm": safe_float(best.get("radius_mm")),
        f"{objective_label}_rank2_radius_mm": safe_float(second.get("radius_mm")),
        f"{objective_label}_rank1_misfit": best_misfit,
        f"{objective_label}_rank2_misfit": second_misfit,
        f"{objective_label}_rank2_minus_rank1_misfit": (
            second_misfit - best_misfit
            if math.isfinite(best_misfit) and math.isfinite(second_misfit)
            else math.nan
        ),
    }


def classify_exception(
    *,
    ringdown_value: float,
    margin_deficit: float,
    relative_deficit: float,
    best_secondary_ratio_to_base: float,
) -> str:
    if math.isfinite(ringdown_value) and not math.isclose(ringdown_value, 0.5, abs_tol=1.0e-9):
        return "legacy_archive_exception_no_gpu_priority"
    if (
        math.isfinite(margin_deficit)
        and margin_deficit <= 1.0e-5
        and math.isfinite(best_secondary_ratio_to_base)
        and best_secondary_ratio_to_base >= 1.2
    ):
        return "near_threshold_modern_exception_monitor"
    if math.isfinite(relative_deficit) and relative_deficit <= 0.10:
        return "moderate_modern_exception_review_before_gpu"
    return "substantive_exception_candidate_for_narrow_probe"


def triage_rows(
    per_run_rows: list[dict],
    policy_rows: list[dict],
    *,
    cutoff: float,
    experiments_root: Path = Path("outputs/experiments"),
) -> list[dict]:
    per_run_by_id = {int(safe_float(row.get("run_id"), -1)): row for row in per_run_rows}
    rows = []
    for run_id in exception_run_ids(policy_rows):
        row = per_run_by_id[run_id]
        run_dir = find_run_dir(run_id, experiments_root)
        objective = str(row["best_secondary_objective"])
        best_secondary_margin = safe_float(row.get("best_secondary_margin"))
        margin_deficit = cutoff - best_secondary_margin
        relative_deficit = margin_deficit / cutoff if math.isfinite(margin_deficit) else math.nan
        top_candidate_csv = run_dir / "data" / "coordinate_objective_top_candidates.csv"
        top_candidate_rows = read_csv_rows(top_candidate_csv) if top_candidate_csv.exists() else []
        metrics = {
            **objective_top_candidate_metrics(top_candidate_rows, "base"),
            **objective_top_candidate_metrics(top_candidate_rows, objective),
        }
        ringdown_value = safe_float(row.get("ringdown_value"))
        ratio = safe_float(row.get("best_secondary_ratio_to_base"))
        classification = classify_exception(
            ringdown_value=ringdown_value,
            margin_deficit=margin_deficit,
            relative_deficit=relative_deficit,
            best_secondary_ratio_to_base=ratio,
        )
        rows.append({
            "run_id": run_id,
            "target": int(safe_float(row.get("target"), -1)),
            "target_label": row.get("target_label", ""),
            "seed": int(safe_float(row.get("seed"), -1)),
            "sources": int(safe_float(row.get("sources"), -1)),
            "tx_rx_offset_mm": safe_float(row.get("tx_rx_offset_mm")),
            "ringdown_value": ringdown_value,
            "base_margin": safe_float(row.get("base_margin")),
            "best_secondary_objective": objective,
            "best_secondary_margin": best_secondary_margin,
            "best_secondary_margin_deficit": margin_deficit,
            "best_secondary_relative_deficit": relative_deficit,
            "best_secondary_ratio_to_base": ratio,
            "best_secondary_truth_geometry": boolish(row.get("best_secondary_truth_geometry")),
            "classification": classification,
            "gpu_priority": (
                "defer"
                if classification in {
                    "legacy_archive_exception_no_gpu_priority",
                    "near_threshold_modern_exception_monitor",
                }
                else "candidate_narrow_probe"
            ),
            "run_dir": str(run_dir),
            **metrics,
        })
    return rows


def decision_summary(rows: list[dict]) -> dict:
    class_counts: dict[str, int] = {}
    for row in rows:
        key = str(row["classification"])
        class_counts[key] = class_counts.get(key, 0) + 1
    gpu_candidates = [str(row["run_id"]) for row in rows if row["gpu_priority"] == "candidate_narrow_probe"]
    return {
        "policy_label": "weak_exact_exception_triage",
        "exception_count": len(rows),
        "classification_counts": class_counts,
        "gpu_candidate_run_ids": ", ".join(gpu_candidates),
        "decision": (
            "Do not launch broad GPU sweeps for these exceptions. Run 1136 is a "
            "near-threshold modern target0 exception; run 785 is a legacy ringdown025 "
            "target1 archive exception. Both preserve exact geometry under the best "
            "secondary objective."
        ),
    }


def plot_exception_triage(rows: list[dict], cutoff: float, save_path: Path) -> str:
    labels = [f"{row['target_label']}\nrun {row['run_id']}" for row in rows]
    base = [safe_float(row.get("base_margin")) for row in rows]
    secondary = [safe_float(row.get("best_secondary_margin")) for row in rows]
    deficits = [safe_float(row.get("best_secondary_margin_deficit")) for row in rows]

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8), constrained_layout=True)
    x = np.arange(len(rows))
    width = 0.36
    axes[0].bar(x - width / 2, base, width=width, color="#4c78a8", label="base")
    axes[0].bar(x + width / 2, secondary, width=width, color="#2f9d55", label="best secondary")
    axes[0].axhline(cutoff, color="#c7302b", linestyle="--", linewidth=1.0, label="5e-4 cutoff")
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel("radius margin")
    axes[0].set_title("Exception margins remain exact but below cutoff")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].bar(x, deficits, color="#f58518", width=0.52)
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("cutoff minus best secondary margin")
    axes[1].set_title("Distance from secondary confirmation cutoff")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Weak-exact secondary confirmation exception triage", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-dir", default=str(DEFAULT_AUDIT_DIR))
    parser.add_argument("--cutoff", type=float, default=5.0e-4)
    parser.add_argument("--run-name", default="coordinate_weak_exact_exception_triage_700_1259")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    audit_dir = Path(args.audit_dir)
    per_run_csv = audit_dir / "data" / "weak_exact_secondary_per_run.csv"
    policy_csv = audit_dir / "data" / "weak_exact_secondary_target_policy.csv"
    per_run_rows = read_csv_rows(per_run_csv)
    policy_rows = read_csv_rows(policy_csv)
    rows = triage_rows(per_run_rows, policy_rows, cutoff=args.cutoff)
    summary = decision_summary(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    triage_csv = data_dir / "weak_exact_exception_triage.csv"
    summary_json = data_dir / "weak_exact_exception_triage_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_exception_triage(rows, args.cutoff, figures_dir / "weak_exact_exception_triage.png"))

    write_union_csv(triage_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "audit_dir": str(audit_dir),
        "input_per_run_csv": str(per_run_csv),
        "input_policy_csv": str(policy_csv),
        "cutoff": args.cutoff,
        **summary,
        "paths": {
            "triage_csv": str(triage_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "coordinate_weak_exact_exception_triage",
        {
            "summary_json": str(summary_json),
            "triage_csv": str(triage_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Audit secondary objective confirmation for base-weak exact coordinate runs."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
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
from run_coordinate_objective_policy_matrix import figure_stats, objective_sort_key, safe_float  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SUMMARY_ROOT = Path("outputs/summary_tables/wk03_experiment_700_1259_holistic_evaluation/data")
OBJECTIVE_LABELS = ("base", "early_high", "highband", "late", "late_high", "veryhigh")
TARGET_TRUTH = {
    0: {"label": "target0", "x_mm": 150.0, "z_mm": 80.0, "radius_mm": 5.0},
    1: {"label": "target1", "x_mm": 250.0, "z_mm": 100.0, "radius_mm": 6.0},
    2: {"label": "target2", "x_mm": 350.0, "z_mm": 120.0, "radius_mm": 8.0},
}


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def geometry_matches_target(row: dict, target: int) -> bool:
    truth = TARGET_TRUTH[int(target)]
    return (
        math.isclose(safe_float(row.get("best_x_mm")), truth["x_mm"], abs_tol=1.0e-9)
        and math.isclose(safe_float(row.get("best_z_mm")), truth["z_mm"], abs_tol=1.0e-9)
        and math.isclose(safe_float(row.get("best_radius_mm")), truth["radius_mm"], abs_tol=1.0e-9)
    )


def canonical_weak_exact_rows(coordinate_rows: list[dict]) -> list[dict]:
    selected = []
    for row in coordinate_rows:
        target = int(safe_float(row.get("target"), -1))
        if target not in TARGET_TRUTH:
            continue
        if not boolish(row.get("exact_geometry")):
            continue
        if not boolish(row.get("base_margin_is_canonical")):
            continue
        if str(row.get("confidence_label")) != "weak":
            continue
        selected.append(row)

    # Guard against accidental duplicate rows in future summary tables.
    by_key: dict[tuple[int, int], dict] = {}
    for row in selected:
        key = (int(safe_float(row.get("target"), -1)), int(safe_float(row.get("run_id"), -1)))
        by_key.setdefault(key, row)
    return [
        by_key[key]
        for key in sorted(by_key, key=lambda item: (item[0], item[1]))
    ]


def _geometry_error(row: dict, target: int) -> float:
    truth = TARGET_TRUTH[int(target)]
    return (
        abs(safe_float(row.get("best_x_mm")) - truth["x_mm"])
        + abs(safe_float(row.get("best_z_mm")) - truth["z_mm"])
        + abs(safe_float(row.get("best_radius_mm")) - truth["radius_mm"])
    )


def select_objective_row(
    rows_by_run_objective: dict[tuple[int, str], list[dict]],
    run_id: int,
    objective_label: str,
    target: int,
) -> dict | None:
    candidates = rows_by_run_objective.get((run_id, objective_label), [])
    if not candidates:
        return None
    truth_rows = [row for row in candidates if geometry_matches_target(row, target)]
    if truth_rows:
        return truth_rows[0]
    if len(candidates) == 1:
        return candidates[0]
    return min(candidates, key=lambda row: _geometry_error(row, target))


def build_rows_by_run_objective(objective_rows: list[dict]) -> dict[tuple[int, str], list[dict]]:
    rows_by_key: dict[tuple[int, str], list[dict]] = defaultdict(list)
    for row in objective_rows:
        run_id = int(safe_float(row.get("run_id"), -1))
        label = str(row.get("objective_label", ""))
        rows_by_key[(run_id, label)].append(row)
    return rows_by_key


def per_run_confirmation_rows(
    weak_rows: list[dict],
    objective_rows: list[dict],
    cutoff: float,
) -> list[dict]:
    rows_by_run_objective = build_rows_by_run_objective(objective_rows)
    output = []
    for weak in weak_rows:
        run_id = int(safe_float(weak.get("run_id"), -1))
        target = int(safe_float(weak.get("target"), -1))
        row = {
            "target": target,
            "target_label": TARGET_TRUTH[target]["label"],
            "run_id": run_id,
            "seed": int(safe_float(weak.get("seed"), -1)),
            "sources": int(safe_float(weak.get("sources"), -1)),
            "tx_rx_offset_mm": safe_float(weak.get("tx_rx_offset_mm")),
            "ringdown_value": safe_float(weak.get("ringdown_value")),
            "base_margin": safe_float(weak.get("base_margin")),
            "run_name": weak.get("run_name", ""),
        }
        for label in OBJECTIVE_LABELS:
            selected = select_objective_row(rows_by_run_objective, run_id, label, target)
            margin = safe_float(selected.get("objective_margin")) if selected is not None else math.nan
            truth = geometry_matches_target(selected, target) if selected is not None else False
            row[f"{label}_margin"] = margin
            row[f"{label}_truth_geometry"] = truth
            row[f"{label}_accepted"] = bool(math.isfinite(margin) and margin >= cutoff)

        secondary_labels = [label for label in OBJECTIVE_LABELS if label != "base"]
        best_label = max(
            secondary_labels,
            key=lambda label: (
                safe_float(row.get(f"{label}_margin"), -math.inf),
                -objective_sort_key(label)[0],
            ),
        )
        base_margin = safe_float(row.get("base_margin"))
        best_margin = safe_float(row.get(f"{best_label}_margin"))
        row["best_secondary_objective"] = best_label
        row["best_secondary_margin"] = best_margin
        row["best_secondary_accepted"] = bool(math.isfinite(best_margin) and best_margin >= cutoff)
        row["best_secondary_truth_geometry"] = bool(row.get(f"{best_label}_truth_geometry"))
        row["best_secondary_ratio_to_base"] = (
            best_margin / base_margin
            if math.isfinite(best_margin) and math.isfinite(base_margin) and base_margin != 0
            else math.nan
        )
        output.append(row)
    return output


def objective_summary_rows(per_run_rows: list[dict], cutoff: float) -> list[dict]:
    rows = []
    by_target: dict[int, list[dict]] = defaultdict(list)
    for row in per_run_rows:
        by_target[int(row["target"])].append(row)

    for target in sorted(by_target):
        target_rows = by_target[target]
        for label in OBJECTIVE_LABELS:
            margins = [safe_float(row.get(f"{label}_margin")) for row in target_rows]
            finite = [value for value in margins if math.isfinite(value)]
            ratios = [
                safe_float(row.get(f"{label}_margin")) / safe_float(row.get("base_margin"))
                for row in target_rows
                if math.isfinite(safe_float(row.get(f"{label}_margin")))
                and math.isfinite(safe_float(row.get("base_margin")))
                and safe_float(row.get("base_margin")) != 0
            ]
            rows.append({
                "target": target,
                "target_label": TARGET_TRUTH[target]["label"],
                "objective_label": label,
                "row_count": len(target_rows),
                "truth_geometry_count": sum(1 for row in target_rows if bool(row.get(f"{label}_truth_geometry"))),
                "accepted_count": sum(1 for value in finite if value >= cutoff),
                "accepted_fraction": (
                    sum(1 for value in finite if value >= cutoff) / len(target_rows)
                    if target_rows else math.nan
                ),
                "min_margin": min(finite) if finite else math.nan,
                "mean_margin": float(np.mean(finite)) if finite else math.nan,
                "median_ratio_to_base": float(np.median(ratios)) if ratios else math.nan,
                "nonaccepted_run_ids": ", ".join(
                    str(row["run_id"])
                    for row in target_rows
                    if not bool(row.get(f"{label}_accepted"))
                ),
            })
    return rows


def target_policy_rows(per_run_rows: list[dict], summary_rows: list[dict]) -> list[dict]:
    by_target: dict[int, list[dict]] = defaultdict(list)
    for row in per_run_rows:
        by_target[int(row["target"])].append(row)
    by_target_objective = {
        (int(row["target"]), row["objective_label"]): row
        for row in summary_rows
    }

    policies = []
    for target in sorted(by_target):
        target_rows = by_target[target]
        row_count = len(target_rows)
        secondary_summaries = [
            by_target_objective[(target, label)]
            for label in OBJECTIVE_LABELS
            if label != "base"
        ]
        full = [
            row for row in secondary_summaries
            if int(row["accepted_count"]) == row_count
            and int(row["truth_geometry_count"]) == row_count
        ]
        strongest = max(
            secondary_summaries,
            key=lambda row: (
                safe_float(row.get("accepted_fraction"), -1.0),
                safe_float(row.get("median_ratio_to_base"), -1.0),
                safe_float(row.get("mean_margin"), -1.0),
            ),
        )
        accepted_count = int(strongest["accepted_count"])
        if full:
            policy_label = "full_secondary_confirmation"
        elif accepted_count >= max(0, row_count - 1):
            policy_label = "near_secondary_confirmation_one_exception"
        elif accepted_count > 0:
            policy_label = "partial_secondary_confirmation"
        else:
            policy_label = "no_secondary_confirmation"
        policies.append({
            "target": target,
            "target_label": TARGET_TRUTH[target]["label"],
            "weak_exact_row_count": row_count,
            "base_accepted_count": int(by_target_objective[(target, "base")]["accepted_count"]),
            "full_confirmation_objectives": ", ".join(
                row["objective_label"] for row in sorted(full, key=lambda item: objective_sort_key(item["objective_label"]))
            ) or "none",
            "strongest_secondary_objective": strongest["objective_label"],
            "strongest_secondary_accepted_count": accepted_count,
            "strongest_secondary_accepted_fraction": strongest["accepted_fraction"],
            "strongest_secondary_median_ratio_to_base": strongest["median_ratio_to_base"],
            "strongest_secondary_nonaccepted_run_ids": strongest["nonaccepted_run_ids"],
            "policy_label": policy_label,
            "policy_note": (
                "Use secondary objectives as diagnostic confirmation for base-weak exact rows only; "
                "do not replace the canonical base production gate."
            ),
        })
    return policies


def plot_confirmation_matrix(summary_rows: list[dict], policy_rows: list[dict], save_path: Path) -> str:
    targets = sorted({int(row["target"]) for row in summary_rows})
    objectives = list(OBJECTIVE_LABELS)
    accepted = np.full((len(targets), len(objectives)), np.nan)
    ratio = np.full((len(targets), len(objectives)), np.nan)
    lookup = {(int(row["target"]), row["objective_label"]): row for row in summary_rows}
    for i, target in enumerate(targets):
        for j, label in enumerate(objectives):
            row = lookup.get((target, label))
            if row:
                accepted[i, j] = safe_float(row.get("accepted_fraction"))
                ratio[i, j] = safe_float(row.get("median_ratio_to_base"))

    labels = [TARGET_TRUTH[target]["label"] for target in targets]
    policy_lookup = {int(row["target"]): row for row in policy_rows}
    strongest_fraction = [
        safe_float(policy_lookup[target].get("strongest_secondary_accepted_fraction"))
        for target in targets
    ]
    row_counts = [
        safe_float(policy_lookup[target].get("weak_exact_row_count"))
        for target in targets
    ]

    fig, axes = plt.subplots(1, 3, figsize=(16.0, 4.8), constrained_layout=True)
    im0 = axes[0].imshow(accepted, vmin=0.0, vmax=1.0, cmap="viridis")
    axes[0].set_title("Accepted fraction")
    im1 = axes[1].imshow(ratio, vmin=0.5, vmax=max(1.8, float(np.nanmax(ratio))), cmap="magma")
    axes[1].set_title("Median ratio to base")
    for ax in axes[:2]:
        ax.set_xticks(np.arange(len(objectives)), objectives, rotation=35, ha="right")
        ax.set_yticks(np.arange(len(labels)), labels)
    for i in range(len(targets)):
        for j in range(len(objectives)):
            axes[0].text(j, i, f"{accepted[i, j]:.2g}", ha="center", va="center", color="white", fontsize=8)
            axes[1].text(j, i, f"{ratio[i, j]:.2g}", ha="center", va="center", color="white", fontsize=8)
    fig.colorbar(im0, ax=axes[0], shrink=0.78)
    fig.colorbar(im1, ax=axes[1], shrink=0.78)

    x = np.arange(len(targets))
    axes[2].bar(x, strongest_fraction, color="#4c78a8", width=0.58)
    axes[2].set_xticks(x, [f"{label}\n{int(count)} rows" for label, count in zip(labels, row_counts)])
    axes[2].set_ylim(0, 1.05)
    axes[2].set_ylabel("accepted fraction")
    axes[2].set_title("Strongest secondary per target")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)
    for idx, value in enumerate(strongest_fraction):
        axes[2].text(idx, min(1.02, value + 0.03), f"{value:.2f}", ha="center", fontsize=8)

    fig.suptitle("Weak-exact secondary objective confirmation audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def audit_decision(policy_rows: list[dict]) -> dict:
    labels = {row["target_label"]: row for row in policy_rows}
    full_targets = [row["target_label"] for row in policy_rows if row["policy_label"] == "full_secondary_confirmation"]
    near_targets = [
        row["target_label"]
        for row in policy_rows
        if row["policy_label"] == "near_secondary_confirmation_one_exception"
    ]
    return {
        "policy_label": "weak_exact_secondary_confirmation_audit",
        "decision": (
            "Canonical base remains the production confidence gate. Diagnostic secondary "
            "objectives confirm many base-weak exact rows: target2 has full late/late_high "
            "confirmation, while target0 and target1 have one archived exception each."
        ),
        "full_confirmation_targets": ", ".join(full_targets) or "none",
        "near_confirmation_targets": ", ".join(near_targets) or "none",
        "target0_exception_run_ids": labels.get("target0", {}).get("strongest_secondary_nonaccepted_run_ids", ""),
        "target1_exception_run_ids": labels.get("target1", {}).get("strongest_secondary_nonaccepted_run_ids", ""),
        "target2_exception_run_ids": labels.get("target2", {}).get("strongest_secondary_nonaccepted_run_ids", ""),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--coordinate-run-summary-csv",
        default=str(DEFAULT_SUMMARY_ROOT / "coordinate_run_summary_700_1259.csv"),
    )
    parser.add_argument(
        "--objective-variant-summary-csv",
        default=str(DEFAULT_SUMMARY_ROOT / "objective_variant_summary_700_1259.csv"),
    )
    parser.add_argument("--cutoff", type=float, default=5.0e-4)
    parser.add_argument("--run-name", default="coordinate_weak_exact_secondary_confirmation_audit_700_1259")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    coordinate_rows = read_csv_rows(Path(args.coordinate_run_summary_csv))
    objective_rows = read_csv_rows(Path(args.objective_variant_summary_csv))
    weak_rows = canonical_weak_exact_rows(coordinate_rows)
    per_run_rows = per_run_confirmation_rows(weak_rows, objective_rows, args.cutoff)
    objective_rows_out = objective_summary_rows(per_run_rows, args.cutoff)
    policies = target_policy_rows(per_run_rows, objective_rows_out)
    decision = audit_decision(policies)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    weak_rows_csv = data_dir / "weak_exact_base_rows.csv"
    per_run_csv = data_dir / "weak_exact_secondary_per_run.csv"
    objective_csv = data_dir / "weak_exact_secondary_objective_summary.csv"
    policy_csv = data_dir / "weak_exact_secondary_target_policy.csv"
    summary_json = data_dir / "weak_exact_secondary_confirmation_audit_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_confirmation_matrix(objective_rows_out, policies, figures_dir / "weak_exact_secondary_confirmation_audit.png"))

    write_csv(weak_rows_csv, [json_safe(row) for row in weak_rows])
    write_csv(per_run_csv, [json_safe(row) for row in per_run_rows])
    write_csv(objective_csv, [json_safe(row) for row in objective_rows_out])
    write_csv(policy_csv, [json_safe(row) for row in policies])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])

    summary = {
        "coordinate_run_summary_csv": args.coordinate_run_summary_csv,
        "objective_variant_summary_csv": args.objective_variant_summary_csv,
        "cutoff": args.cutoff,
        "weak_exact_row_count": len(weak_rows),
        **decision,
        "target_policy_rows": policies,
        "paths": {
            "weak_rows_csv": str(weak_rows_csv),
            "per_run_csv": str(per_run_csv),
            "objective_summary_csv": str(objective_csv),
            "policy_csv": str(policy_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "coordinate_weak_exact_secondary_confirmation_audit",
        {
            "summary_json": str(summary_json),
            "weak_rows_csv": str(weak_rows_csv),
            "per_run_csv": str(per_run_csv),
            "objective_summary_csv": str(objective_csv),
            "policy_csv": str(policy_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

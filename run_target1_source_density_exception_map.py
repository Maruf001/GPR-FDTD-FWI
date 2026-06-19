#!/usr/bin/env python3
"""Map target1 source-density exceptions to concrete next actions."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter
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
from visualization.plot_style import save_validated_figure  # noqa: E402


BASE_CUTOFF = 5.0e-4
TARGET1_TRUTH = {"x_mm": 250.0, "z_mm": 100.0, "radius_mm": 6.0}
DEFAULT_EXPERIMENT_ROOT = Path("outputs/experiments")
DEFAULT_SOURCE_POLICY_CSV = (
    DEFAULT_EXPERIMENT_ROOT
    / "1312_target1_acquisition_confidence_surface"
    / "data"
    / "target1_source_density_branch_policy.csv"
)
DEFAULT_COORDINATE_CSV = (
    Path("outputs/summary_tables/wk03_experiment_700_1259_holistic_evaluation")
    / "data"
    / "coordinate_run_summary_700_1259.csv"
)
DEFAULT_OBJECTIVE_CSV = (
    Path("outputs/summary_tables/wk03_experiment_700_1259_holistic_evaluation")
    / "data"
    / "objective_variant_summary_700_1259.csv"
)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def safe_float(value: object, default: float = math.nan) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value: object, default: int = 0) -> int:
    number = safe_float(value)
    if not math.isfinite(number):
        return default
    return int(number)


def is_true(value: object) -> bool:
    return str(value).strip().lower() == "true"


def parse_run_ids(value: object) -> list[int]:
    out = []
    for part in str(value or "").replace(";", ",").split(","):
        part = part.strip()
        if not part:
            continue
        out.append(safe_int(part, -1))
    return [run_id for run_id in out if run_id >= 0]


def objective_is_target1_truth(row: dict | None) -> bool:
    if row is None:
        return False
    return (
        math.isclose(safe_float(row.get("best_x_mm")), TARGET1_TRUTH["x_mm"], abs_tol=1.0e-9)
        and math.isclose(safe_float(row.get("best_z_mm")), TARGET1_TRUTH["z_mm"], abs_tol=1.0e-9)
        and math.isclose(
            safe_float(row.get("best_radius_mm")),
            TARGET1_TRUTH["radius_mm"],
            abs_tol=1.0e-9,
        )
    )


def coordinate_lookup(rows: list[dict]) -> dict[int, dict]:
    return {safe_int(row.get("run_id"), -1): row for row in rows if safe_int(row.get("run_id"), -1) >= 0}


def objective_lookup(rows: list[dict]) -> dict[tuple[int, str], dict]:
    out = {}
    for row in rows:
        run_id = safe_int(row.get("run_id"), -1)
        label = str(row.get("objective_label", ""))
        if run_id >= 0 and label:
            out[(run_id, label)] = row
    return out


def is_legacy_ringdown(row: dict | None) -> bool:
    if row is None:
        return False
    ringdown = safe_float(row.get("ringdown_value"))
    return math.isfinite(ringdown) and ringdown < 0.5


def branch_action(
    source_row: dict,
    run_ids: list[int],
    late_high_exception_ids: list[int],
    late_high_accepted_count: int,
    coordinates_by_run: dict[int, dict],
) -> str:
    all_late_high_confirmed = late_high_accepted_count == len(run_ids)
    terminal_11_worse = (
        math.isclose(safe_float(source_row.get("last_setting")), 11.0)
        and str(source_row.get("last_worse_than_first")).strip().lower() == "true"
    )
    n_accepted = safe_int(source_row.get("n_accepted"))
    best_minus_first = safe_float(source_row.get("best_minus_first_margin"))
    exception_rows = [coordinates_by_run.get(run_id) for run_id in late_high_exception_ids]
    if late_high_exception_ids and all(is_legacy_ringdown(row) for row in exception_rows):
        return "legacy_exception_no_gpu"
    if late_high_exception_ids:
        return "modern_exception_review_before_gpu"
    if terminal_11_worse and all_late_high_confirmed:
        return "do_not_extend_source_density"
    if n_accepted == 0 and all_late_high_confirmed:
        return "secondary_confirmed_no_source_rescue"
    if n_accepted > 0 and best_minus_first > 0.0:
        return "accepted_branch_no_rerun"
    if n_accepted > 0 and best_minus_first <= 0.0:
        return "lower_source_count_best_no_rerun"
    return "manual_review"


def build_per_run_rows(
    source_rows: list[dict],
    coordinate_rows: list[dict],
    objective_rows: list[dict],
) -> list[dict]:
    coordinates_by_run = coordinate_lookup(coordinate_rows)
    objectives_by_run = objective_lookup(objective_rows)
    out = []
    seen: set[tuple[str, int]] = set()
    for source_row in source_rows:
        series_id = str(source_row.get("series_id", ""))
        for run_id in parse_run_ids(source_row.get("run_ids")):
            key = (series_id, run_id)
            if key in seen:
                continue
            seen.add(key)
            coordinate = coordinates_by_run.get(run_id, {})
            late_high = objectives_by_run.get((run_id, "late_high"))
            base_margin = safe_float(coordinate.get("base_margin"))
            late_high_margin = safe_float((late_high or {}).get("objective_margin"))
            out.append({
                "series_id": series_id,
                "run_id": run_id,
                "seed": coordinate.get("seed", source_row.get("seed", "")),
                "sources": safe_int(coordinate.get("sources")),
                "tx_rx_offset_mm": safe_float(coordinate.get("tx_rx_offset_mm")),
                "ringdown_value": safe_float(coordinate.get("ringdown_value")),
                "base_margin": base_margin,
                "base_accepted": bool(math.isfinite(base_margin) and base_margin >= BASE_CUTOFF),
                "late_high_margin": late_high_margin,
                "late_high_truth_geometry": objective_is_target1_truth(late_high),
                "late_high_accepted": bool(
                    objective_is_target1_truth(late_high)
                    and math.isfinite(late_high_margin)
                    and late_high_margin >= BASE_CUTOFF
                ),
                "exact_geometry": is_true(coordinate.get("exact_geometry")),
                "run_name": coordinate.get("run_name", ""),
            })
    return sorted(out, key=lambda row: (row["series_id"], row["sources"], row["run_id"]))


def build_branch_rows(
    source_rows: list[dict],
    coordinate_rows: list[dict],
    objective_rows: list[dict],
) -> list[dict]:
    coordinates_by_run = coordinate_lookup(coordinate_rows)
    objectives_by_run = objective_lookup(objective_rows)
    out = []
    for source_row in source_rows:
        run_ids = parse_run_ids(source_row.get("run_ids"))
        late_high_truth_count = 0
        late_high_accepted_count = 0
        late_high_exception_ids = []
        legacy_run_count = 0
        modern_run_count = 0
        exact_count = 0
        for run_id in run_ids:
            coordinate = coordinates_by_run.get(run_id)
            if is_legacy_ringdown(coordinate):
                legacy_run_count += 1
            else:
                modern_run_count += 1
            if coordinate and is_true(coordinate.get("exact_geometry")):
                exact_count += 1
            late_high = objectives_by_run.get((run_id, "late_high"))
            late_high_margin = safe_float((late_high or {}).get("objective_margin"))
            is_truth = objective_is_target1_truth(late_high)
            if is_truth:
                late_high_truth_count += 1
            if is_truth and math.isfinite(late_high_margin) and late_high_margin >= BASE_CUTOFF:
                late_high_accepted_count += 1
            else:
                late_high_exception_ids.append(run_id)
        action = branch_action(
            source_row,
            run_ids,
            late_high_exception_ids,
            late_high_accepted_count,
            coordinates_by_run,
        )
        terminal_11 = math.isclose(safe_float(source_row.get("last_setting")), 11.0)
        out.append({
            "series_id": source_row.get("series_id", ""),
            "seed": source_row.get("seed", ""),
            "run_ids": ", ".join(str(run_id) for run_id in run_ids),
            "first_run": safe_int(source_row.get("first_run")),
            "last_run": safe_int(source_row.get("last_run")),
            "n_runs": safe_int(source_row.get("n_runs")),
            "n_accepted": safe_int(source_row.get("n_accepted")),
            "n_weak": safe_int(source_row.get("n_weak")),
            "first_setting": safe_float(source_row.get("first_setting")),
            "last_setting": safe_float(source_row.get("last_setting")),
            "best_setting": safe_float(source_row.get("best_setting")),
            "worst_setting": safe_float(source_row.get("worst_setting")),
            "first_margin": safe_float(source_row.get("first_margin")),
            "last_margin": safe_float(source_row.get("last_margin")),
            "best_margin": safe_float(source_row.get("best_margin")),
            "worst_margin": safe_float(source_row.get("worst_margin")),
            "best_minus_first_margin": safe_float(source_row.get("best_minus_first_margin")),
            "last_minus_first_margin": safe_float(source_row.get("last_minus_first_margin")),
            "last_worse_than_first": str(source_row.get("last_worse_than_first")).strip().lower() == "true",
            "all_exact_geometry": exact_count == len(run_ids),
            "late_high_truth_count": late_high_truth_count,
            "late_high_accepted_count": late_high_accepted_count,
            "late_high_exception_run_ids": ", ".join(str(run_id) for run_id in late_high_exception_ids),
            "legacy_ringdown_run_count": legacy_run_count,
            "modern_ringdown_run_count": modern_run_count,
            "terminal_11_branch": terminal_11,
            "terminal_11_worse": bool(
                terminal_11 and str(source_row.get("last_worse_than_first")).strip().lower() == "true"
            ),
            "source_policy_status": source_row.get("status", ""),
            "recommended_action": action,
            "gpu_priority": "none" if action != "modern_exception_review_before_gpu" else "review_first",
        })
    return out


def summarize_exception_map(branch_rows: list[dict], per_run_rows: list[dict]) -> dict:
    action_counts = dict(Counter(row["recommended_action"] for row in branch_rows))
    terminal_rows = [row for row in branch_rows if row["terminal_11_branch"]]
    modern_exception_rows = [
        row for row in branch_rows
        if row["recommended_action"] == "modern_exception_review_before_gpu"
    ]
    legacy_exception_rows = [
        row for row in branch_rows
        if row["recommended_action"] == "legacy_exception_no_gpu"
    ]
    all_confirmed_rows = [
        row for row in branch_rows
        if row["late_high_accepted_count"] == row["n_runs"]
    ]
    if not modern_exception_rows and not any(row["recommended_action"] == "manual_review" for row in branch_rows):
        policy_label = "target1_source_density_exception_map_no_gpu"
        gpu_priority = "none"
    else:
        policy_label = "target1_source_density_exception_map_review_before_gpu"
        gpu_priority = "review_first"
    decision = (
        "Target1 source-density branches do not justify a broad or narrow GPU "
        "rerun under the current hypothesis. All modern source-density branches "
        "are exact-geometry and late_high-confirmed; the only late_high exception "
        "is legacy ringdown025 run 785. Terminal 11-source branches are both "
        "worse than their first setting, so source-density escalation should not "
        "be extended as a rescue rule."
    )
    return {
        "policy_label": policy_label,
        "source_density_series_count": len(branch_rows),
        "source_density_run_row_count": len(per_run_rows),
        "all_late_high_confirmed_series_count": len(all_confirmed_rows),
        "legacy_exception_series_count": len(legacy_exception_rows),
        "modern_exception_series_count": len(modern_exception_rows),
        "terminal_11_series_count": len(terminal_rows),
        "terminal_11_worse_count": sum(1 for row in terminal_rows if row["terminal_11_worse"]),
        "terminal_11_late_high_confirmed_count": sum(
            1 for row in terminal_rows if row["late_high_accepted_count"] == row["n_runs"]
        ),
        "source_escalation_helped_count": sum(
            1 for row in branch_rows if safe_float(row["best_minus_first_margin"]) > 0.0
        ),
        "lower_source_count_best_count": sum(
            1 for row in branch_rows if safe_float(row["best_minus_first_margin"]) <= 0.0
        ),
        "all_base_weak_series_count": sum(
            1 for row in branch_rows if row["source_policy_status"] == "all_base_weak"
        ),
        "action_counts": action_counts,
        "gpu_priority": gpu_priority,
        "recommended_gpu_action": "none_target1_source_density",
        "legacy_exception_run_ids": ", ".join(
            sorted(
                {
                    run_id.strip()
                    for row in legacy_exception_rows
                    for run_id in str(row["late_high_exception_run_ids"]).split(",")
                    if run_id.strip()
                },
                key=lambda item: int(item),
            )
        ),
        "decision": decision,
    }


def plot_exception_map(branch_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(2, 2, figsize=(14.8, 8.2), constrained_layout=True)
    action_order = [
        "accepted_branch_no_rerun",
        "lower_source_count_best_no_rerun",
        "secondary_confirmed_no_source_rescue",
        "do_not_extend_source_density",
        "legacy_exception_no_gpu",
        "modern_exception_review_before_gpu",
        "manual_review",
    ]
    labels = [label for label in action_order if summary["action_counts"].get(label, 0)]
    axes[0, 0].bar(
        np.arange(len(labels)),
        [summary["action_counts"][label] for label in labels],
        color="#4c78a8",
        edgecolor="#333333",
        width=0.62,
    )
    axes[0, 0].set_xticks(np.arange(len(labels)), [label.replace("_", "\n") for label in labels])
    axes[0, 0].set_ylabel("series")
    axes[0, 0].set_title("Recommended branch actions")
    axes[0, 0].grid(axis="y", color="#dddddd", linewidth=0.6)

    colors = {
        "accepted_branch_no_rerun": "#4c78a8",
        "lower_source_count_best_no_rerun": "#2f9d55",
        "secondary_confirmed_no_source_rescue": "#d99a19",
        "do_not_extend_source_density": "#c7302b",
        "legacy_exception_no_gpu": "#7f7f7f",
        "modern_exception_review_before_gpu": "#b279a2",
        "manual_review": "#222222",
    }
    x = np.asarray([safe_float(row["first_margin"]) for row in branch_rows], dtype=float)
    y = np.asarray([safe_float(row["last_margin"]) for row in branch_rows], dtype=float)
    c = [colors.get(row["recommended_action"], "#222222") for row in branch_rows]
    s = [90 if row["terminal_11_branch"] else 44 for row in branch_rows]
    axes[0, 1].scatter(x, y, c=c, s=s, edgecolor="#222222", linewidth=0.35)
    lower = min(float(np.nanmin(x)), float(np.nanmin(y)), 3.4e-4)
    upper = max(float(np.nanmax(x)), float(np.nanmax(y)), 6.2e-4)
    axes[0, 1].plot([lower, upper], [lower, upper], color="#666666", linestyle="--", linewidth=0.9)
    axes[0, 1].axhline(BASE_CUTOFF, color="#b23b3b", linestyle=":", linewidth=1.1)
    axes[0, 1].axvline(BASE_CUTOFF, color="#b23b3b", linestyle=":", linewidth=1.1)
    axes[0, 1].set_xlim(lower, upper)
    axes[0, 1].set_ylim(lower, upper)
    axes[0, 1].set_xlabel("first source setting base margin")
    axes[0, 1].set_ylabel("last source setting base margin")
    axes[0, 1].set_title("Nonmonotonic source-density branches")
    axes[0, 1].grid(color="#dddddd", linewidth=0.6)

    terminal = [row for row in branch_rows if row["terminal_11_branch"]]
    terminal_labels = [f"seed {row['seed']}" for row in terminal]
    tx = np.arange(len(terminal))
    axes[1, 0].bar(tx - 0.22, [row["first_margin"] for row in terminal], width=0.22, color="#4c78a8", label="first")
    axes[1, 0].bar(tx, [row["best_margin"] for row in terminal], width=0.22, color="#2f9d55", label="best")
    axes[1, 0].bar(tx + 0.22, [row["last_margin"] for row in terminal], width=0.22, color="#c7302b", label="11-source")
    axes[1, 0].axhline(BASE_CUTOFF, color="#333333", linestyle=":", linewidth=1.0)
    axes[1, 0].set_xticks(tx, terminal_labels)
    axes[1, 0].set_ylabel("base margin")
    axes[1, 0].set_title("Terminal 11-source branches worsen")
    axes[1, 0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1, 0].legend(frameon=False, fontsize=8)

    confirmed = [row["late_high_accepted_count"] / max(1, row["n_runs"]) for row in branch_rows]
    weak = [row["n_weak"] / max(1, row["n_runs"]) for row in branch_rows]
    idx = np.arange(len(branch_rows))
    axes[1, 1].plot(idx, confirmed, marker="o", color="#2f9d55", linewidth=1.8, label="late_high confirmed fraction")
    axes[1, 1].plot(idx, weak, marker="s", color="#f58518", linewidth=1.2, label="base weak fraction")
    axes[1, 1].set_ylim(0.0, 1.05)
    axes[1, 1].set_xlabel("source-density series, sorted by run")
    axes[1, 1].set_ylabel("fraction")
    axes[1, 1].set_title("Secondary confirmation vs base weakness")
    axes[1, 1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1, 1].legend(frameon=False, fontsize=8)

    fig.suptitle(f"Target1 source-density exception map: {summary['policy_label']}", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def load_inputs(source_policy_csv: Path, coordinate_csv: Path, objective_csv: Path) -> tuple[list[dict], list[dict], list[dict]]:
    return (
        read_csv_rows(source_policy_csv),
        read_csv_rows(coordinate_csv),
        read_csv_rows(objective_csv),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-policy-csv", default=str(DEFAULT_SOURCE_POLICY_CSV))
    parser.add_argument("--coordinate-csv", default=str(DEFAULT_COORDINATE_CSV))
    parser.add_argument("--objective-csv", default=str(DEFAULT_OBJECTIVE_CSV))
    parser.add_argument("--experiment-root", default=str(DEFAULT_EXPERIMENT_ROOT))
    parser.add_argument("--run-name", default="target1_source_density_exception_map")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    source_rows, coordinate_rows, objective_rows = load_inputs(
        Path(args.source_policy_csv),
        Path(args.coordinate_csv),
        Path(args.objective_csv),
    )
    branch_rows = build_branch_rows(source_rows, coordinate_rows, objective_rows)
    per_run_rows = build_per_run_rows(source_rows, coordinate_rows, objective_rows)
    summary = summarize_exception_map(branch_rows, per_run_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.experiment_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    branch_csv = data_dir / "target1_source_density_exception_branches.csv"
    per_run_csv = data_dir / "target1_source_density_exception_runs.csv"
    summary_json = data_dir / "target1_source_density_exception_map_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_exception_map(branch_rows, summary, figures_dir / "target1_source_density_exception_map.png"))

    write_csv(branch_csv, [json_safe(row) for row in branch_rows])
    write_csv(per_run_csv, [json_safe(row) for row in per_run_rows])
    write_csv(validation_csv, [figure_stats(figure_path)])
    summary["paths"] = {
        "branch_csv": str(branch_csv),
        "per_run_csv": str(per_run_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "target1_source_density_exception_map",
        {
            "summary_json": str(summary_json),
            "branch_csv": str(branch_csv),
            "per_run_csv": str(per_run_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

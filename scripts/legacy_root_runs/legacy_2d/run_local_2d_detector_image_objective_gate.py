#!/usr/bin/env python3
"""Evaluate a saved-B-scan image objective gate for detector assignment rows."""

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
from inversion.rebar_detection import background_removed_bscan, envelope_bscan, hyperbola_times  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_assignment_failure_taxonomy import failure_label, parse_bool, parse_float_list, parse_int_list  # noqa: E402
from run_local_2d_detector_baseline_synthesis import safe_float  # noqa: E402
from run_local_2d_detector_parameter_sensitivity import DEFAULT_COMMAND_PLAN_RUN, detection_npz_path  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_ASSIGNMENT_RUN = "023_local_2d_detector_blind_assignment_policy_with_span_bonus"
DEFAULT_SELECTOR_RUN = "026_local_2d_detector_assignment_selector_truth_free_feature_grid"
DEFAULT_ORACLE_RUN = "025_local_2d_detector_assignment_failure_taxonomy_policy_oracle"
CASE_FIELDS = ("branch_key", "seed", "case_variant", "run_name")
TIME_OFFSET_FAMILIES_PS = {
    "single667": (667.0,),
    "baseline": (500.0, 550.0, 600.0, 650.0, 667.0, 700.0, 750.0),
    "wide": (350.0, 400.0, 450.0, 500.0, 550.0, 600.0, 650.0, 700.0, 750.0, 800.0, 850.0),
}
OBJECTIVE_VARIANTS = (
    {"objective_label": "row_background_sigma60", "background_mode": "row", "sigma_ps": 60.0},
    {"objective_label": "median_sigma60", "background_mode": "median", "sigma_ps": 60.0},
    {"objective_label": "row_background_sigma100", "background_mode": "row", "sigma_ps": 100.0},
)
PRIMARY_OBJECTIVE_LABEL = "row_background_sigma60"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def case_key(row: dict) -> tuple[str, str, str, str]:
    return tuple(str(row[field]) for field in CASE_FIELDS)


def case_label(row: dict) -> str:
    branch, seed, variant, _run_name = case_key(row)
    return f"{branch}|seed{seed}|{variant}"


def assigned_rank_sum(row: dict) -> int:
    ranks = parse_int_list(row.get("assigned_detection_ranks"))
    return sum(ranks) if ranks else 100_000


def assigned_max_rank(row: dict) -> int:
    ranks = parse_int_list(row.get("assigned_detection_ranks"))
    return max(ranks) if ranks else 100_000


def row_background_mode(row: dict, variant: dict) -> str:
    if variant["background_mode"] == "row":
        return str(row.get("background_mode", "median"))
    return str(variant["background_mode"])


def time_offsets_s(family: str) -> list[float]:
    values_ps = TIME_OFFSET_FAMILIES_PS.get(str(family), TIME_OFFSET_FAMILIES_PS["baseline"])
    return [float(value) * 1.0e-12 for value in values_ps]


def normalized_envelope(observed: np.ndarray, background_mode: str) -> np.ndarray:
    image = envelope_bscan(background_removed_bscan(observed, mode=background_mode))
    finite = image[np.isfinite(image)]
    scale = float(np.percentile(finite, 95.0)) if finite.size else 1.0
    scale = max(scale, 1.0e-30)
    return image / scale


def hyperbola_mask(
    scan_x: np.ndarray,
    time_values: np.ndarray,
    xs_mm: list[float],
    zs_mm: list[float],
    tx_rx_offset_m: float,
    time_offset_s: float,
    sigma_ps: float,
) -> np.ndarray:
    sigma_s = max(float(sigma_ps) * 1.0e-12, 1.0e-15)
    mask = np.zeros((time_values.size, scan_x.size), dtype=np.float64)
    time_column = time_values[:, None]
    for x_mm, z_mm in zip(xs_mm, zs_mm):
        curve = hyperbola_times(
            scan_x,
            float(x_mm) / 1000.0,
            float(z_mm) / 1000.0,
            tx_rx_offset=float(tx_rx_offset_m),
            time_offset_s=float(time_offset_s),
        )
        mask += np.exp(-0.5 * ((time_column - curve[None, :]) / sigma_s) ** 2)
    return np.minimum(mask, 1.0)


def image_objective_score(
    image: np.ndarray,
    scan_x: np.ndarray,
    time_values: np.ndarray,
    xs_mm: list[float],
    zs_mm: list[float],
    tx_rx_offset_m: float,
    offsets_s: list[float],
    sigma_ps: float,
) -> dict:
    y = np.asarray(image, dtype=np.float64).ravel()
    y_norm = float(np.linalg.norm(y))
    if y_norm <= 0.0:
        return {"image_objective_score": 0.0, "best_time_offset_ps": math.nan, "mask_energy_mean": 0.0}
    best_score = -math.inf
    best_offset = math.nan
    best_energy = 0.0
    for offset_s in offsets_s:
        mask = hyperbola_mask(scan_x, time_values, xs_mm, zs_mm, tx_rx_offset_m, offset_s, sigma_ps)
        m = mask.ravel()
        m_norm = float(np.linalg.norm(m))
        if m_norm <= 0.0:
            continue
        score = float(np.dot(y, m) / (y_norm * m_norm))
        energy = float(np.dot(y, m) / max(float(np.sum(m)), 1.0e-30))
        if score > best_score:
            best_score = score
            best_offset = float(offset_s) * 1.0e12
            best_energy = energy
    if not math.isfinite(best_score):
        best_score = 0.0
    return {
        "image_objective_score": best_score,
        "best_time_offset_ps": best_offset,
        "mask_energy_mean": best_energy,
    }


def geometry_score_key(row: dict, variant: dict) -> tuple:
    return (
        str(row["run_name"]),
        row_background_mode(row, variant),
        str(row.get("time_offset_family", "baseline")),
        float(variant["sigma_ps"]),
        str(row.get("assigned_x_values_mm", "")),
        str(row.get("assigned_z_values_mm", "")),
    )


def load_case_data(plan_rows: list[dict]) -> dict[str, dict]:
    out = {}
    for row in plan_rows:
        with np.load(detection_npz_path(row)) as npz:
            out[row["run_name"]] = {
                "observed": np.asarray(npz["observed_bscan"], dtype=np.float64),
                "scan_x": np.asarray(npz["scan_x"], dtype=np.float64),
                "time": np.asarray(npz["time"], dtype=np.float64),
                "tx_rx_offset_m": safe_float(row["tx_rx_offset_mm"], 0.0) / 1000.0,
            }
    return out


def score_assignment_rows(rows: list[dict], plan_rows: list[dict], variants: tuple[dict, ...] = OBJECTIVE_VARIANTS) -> list[dict]:
    case_data = load_case_data(plan_rows)
    image_cache: dict[tuple[str, str], np.ndarray] = {}
    score_cache: dict[tuple, dict] = {}
    out = []
    for row in rows:
        if row.get("assignment_status") != "assigned":
            continue
        xs = parse_float_list(row.get("assigned_x_values_mm"))
        zs = parse_float_list(row.get("assigned_z_values_mm"))
        if not xs or len(xs) != len(zs):
            continue
        data = case_data[row["run_name"]]
        for variant in variants:
            key = geometry_score_key(row, variant)
            if key not in score_cache:
                background_mode = row_background_mode(row, variant)
                image_key = (row["run_name"], background_mode)
                if image_key not in image_cache:
                    image_cache[image_key] = normalized_envelope(data["observed"], background_mode)
                score_cache[key] = image_objective_score(
                    image_cache[image_key],
                    data["scan_x"],
                    data["time"],
                    xs,
                    zs,
                    data["tx_rx_offset_m"],
                    time_offsets_s(str(row.get("time_offset_family", "baseline"))),
                    float(variant["sigma_ps"]),
                )
            scored = dict(row)
            scored["objective_label"] = variant["objective_label"]
            scored.update(score_cache[key])
            scored["case_label"] = case_label(row)
            scored["failure_label"] = failure_label(row)
            scored["unique_truth_hit_count_numeric"] = int(safe_float(row.get("unique_truth_hit_count"), 0.0))
            scored["unique_all_truths_bool"] = parse_bool(row.get("unique_all_truths_within_tolerance"))
            scored["unique_target0_bool"] = parse_bool(row.get("unique_target0_hit"))
            scored["unique_target1_bool"] = parse_bool(row.get("unique_target1_hit"))
            scored["unique_target2_bool"] = parse_bool(row.get("unique_target2_hit"))
            scored["assigned_rank_sum"] = assigned_rank_sum(row)
            scored["assigned_max_rank"] = assigned_max_rank(row)
            out.append(scored)
    return out


def select_best_rows(scored_rows: list[dict], objective_label: str) -> list[dict]:
    selected = []
    rows = [row for row in scored_rows if row["objective_label"] == objective_label]
    for key in sorted({case_key(row) for row in rows}):
        case_rows = [row for row in rows if case_key(row) == key]
        best = max(
            case_rows,
            key=lambda row: (
                float(row["image_objective_score"]),
                -int(row.get("assigned_max_rank", assigned_max_rank(row))),
                -int(row.get("assigned_rank_sum", assigned_rank_sum(row))),
                -int(safe_float(row.get("candidate_budget"), 0.0)),
                str(row.get("config_key", "")),
                str(row.get("assignment_policy_key", "")),
            ),
        )
        selected.append(best)
    return selected


def summarize_selected(objective_label: str, selected_rows: list[dict]) -> dict:
    labels = Counter(row["failure_label"] for row in selected_rows)
    return {
        "objective_label": objective_label,
        "case_count": len(selected_rows),
        "all_truth_case_count": sum(bool(row["unique_all_truths_bool"]) for row in selected_rows),
        "target0_hit_count": sum(bool(row["unique_target0_bool"]) for row in selected_rows),
        "target1_hit_count": sum(bool(row["unique_target1_bool"]) for row in selected_rows),
        "target2_hit_count": sum(bool(row["unique_target2_bool"]) for row in selected_rows),
        "mean_unique_truth_hit_count": float(np.mean([row["unique_truth_hit_count_numeric"] for row in selected_rows])),
        "mean_image_objective_score": float(np.mean([float(row["image_objective_score"]) for row in selected_rows])),
        "dominant_failure_label": labels.most_common(1)[0][0] if labels else "",
    }


def branch_summary(selected_rows: list[dict]) -> list[dict]:
    out = []
    for branch in sorted({row["branch_key"] for row in selected_rows}):
        rows = [row for row in selected_rows if row["branch_key"] == branch]
        out.append({
            "branch_key": branch,
            "case_count": len(rows),
            "all_truth_case_count": sum(bool(row["unique_all_truths_bool"]) for row in rows),
            "target0_hit_count": sum(bool(row["unique_target0_bool"]) for row in rows),
            "target1_hit_count": sum(bool(row["unique_target1_bool"]) for row in rows),
            "target2_hit_count": sum(bool(row["unique_target2_bool"]) for row in rows),
            "mean_unique_truth_hit_count": float(np.mean([row["unique_truth_hit_count_numeric"] for row in rows])),
        })
    return out


def plot_gate(summary: dict, branch_rows: list[dict], variant_rows: list[dict], save_path: Path) -> str:
    labels = ["shared\npolicy", "rank/span\nselector", "image\nobjective", "policy\noracle"]
    values = [
        summary["shared_policy_all_truth_case_count"],
        summary["rank_span_selector_all_truth_case_count"],
        summary["primary_objective_all_truth_case_count"],
        summary["oracle_all_truth_case_count"],
    ]
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 5.2), constrained_layout=True)
    axes[0].bar(np.arange(len(labels)), values, color=["#bab0ab", "#4e79a7", "#59a14f", "#9c755f"])
    axes[0].set_xticks(np.arange(len(labels)), labels, fontsize=8)
    axes[0].set_ylabel("all-truth cases")
    axes[0].set_ylim(0, summary["case_count"] + 1)
    axes[0].set_title("Detector handoff gates")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    variant_labels = [row["objective_label"].replace("_", "\n") for row in variant_rows]
    variant_values = [row["all_truth_case_count"] for row in variant_rows]
    axes[1].bar(np.arange(len(variant_rows)), variant_values, color="#76b7b2", width=0.58)
    axes[1].set_xticks(np.arange(len(variant_rows)), variant_labels, fontsize=8)
    axes[1].set_ylim(0, summary["case_count"] + 1)
    axes[1].set_title("Image-objective variants")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Local 2D detector image-objective handoff gate", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join([
            "# Figure Notes",
            "",
            "## `local_2d_detector_image_objective_gate.png`",
            "",
            "This figure compares saved-row detector assignment gates. The image",
            "objective scores assigned triples against saved detector B-scans with",
            "Gaussian hyperbola masks and time-offset families. It does not rerun",
            "FDTD, FWI, GPU kernels, field FWI, or 3D/HPC work.",
            "",
            f"Policy label: `{summary['policy_label']}`.",
            f"Primary objective: `{summary['primary_objective_label']}`.",
            f"Primary objective all-truth cases: `{summary['primary_objective_all_truth_case_count']}`.",
            f"Shared-policy all-truth cases: `{summary['shared_policy_all_truth_case_count']}`.",
            f"Rank/span selector all-truth cases: `{summary['rank_span_selector_all_truth_case_count']}`.",
            f"Policy-oracle all-truth cases: `{summary['oracle_all_truth_case_count']}`.",
            f"GPU used: `{summary['gpu_used']}`.",
            "",
            summary["decision"],
            "",
        ])
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--command-plan-run", default=DEFAULT_COMMAND_PLAN_RUN)
    parser.add_argument("--assignment-run", default=DEFAULT_ASSIGNMENT_RUN)
    parser.add_argument("--selector-run", default=DEFAULT_SELECTOR_RUN)
    parser.add_argument("--oracle-run", default=DEFAULT_ORACLE_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_image_objective_gate")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    plan_rows = read_csv_rows(
        summary_root / args.command_plan_run / "data/local_2d_detector_baseline_command_plan_rows.csv"
    )
    assignment_dir = summary_root / args.assignment_run
    assignment_rows = read_csv_rows(assignment_dir / "data/local_2d_detector_blind_assignment_policy_rows.csv")
    shared_summary = read_json(assignment_dir / "data/local_2d_detector_blind_assignment_policy_summary.json")
    selector_summary = read_json(
        summary_root / args.selector_run / "data/local_2d_detector_assignment_selector_summary.json"
    )
    oracle_summary = read_json(
        summary_root / args.oracle_run / "data/local_2d_detector_assignment_failure_taxonomy_summary.json"
    )
    scored_rows = score_assignment_rows(assignment_rows, plan_rows)
    variant_rows = []
    selected_by_variant: dict[str, list[dict]] = {}
    for variant in OBJECTIVE_VARIANTS:
        label = variant["objective_label"]
        selected = select_best_rows(scored_rows, label)
        selected_by_variant[label] = selected
        variant_rows.append(summarize_selected(label, selected))

    primary_rows = selected_by_variant[PRIMARY_OBJECTIVE_LABEL]
    primary_summary = next(row for row in variant_rows if row["objective_label"] == PRIMARY_OBJECTIVE_LABEL)
    primary_branch_rows = branch_summary(primary_rows)
    shared_all_truth = int(shared_summary.get("best_unique_all_truth_case_count", 0))
    selector_all_truth = int(selector_summary.get("leave_one_case_all_truth_case_count", 0))
    oracle_all_truth = int(oracle_summary.get("oracle_all_truth_case_count", oracle_summary.get("all_truth_case_count", 0)))
    primary_all_truth = int(primary_summary["all_truth_case_count"])
    if primary_all_truth > shared_all_truth:
        decision = (
            "The saved-B-scan image objective gate improves on the fixed shared policy. This supports a "
            "narrow downstream objective-gated detector handoff before any broader detector-seeded FWI run."
        )
    else:
        decision = (
            "The saved-B-scan image objective gate does not improve on the fixed shared policy. Treat the "
            "policy-oracle gap as requiring a stronger waveform/objective gate or an explicitly bounded "
            "oracle/rank-gated upper-bound, not as a ready automatic detector handoff."
        )
    summary = {
        "policy_label": "local_2d_detector_image_objective_gate_saved_bscan_cpu",
        "case_count": primary_summary["case_count"],
        "assignment_row_count": len(assignment_rows),
        "scored_row_count": len(scored_rows),
        "objective_variant_count": len(OBJECTIVE_VARIANTS),
        "primary_objective_label": PRIMARY_OBJECTIVE_LABEL,
        "primary_objective_all_truth_case_count": primary_all_truth,
        "primary_objective_mean_unique_truth_hit_count": primary_summary["mean_unique_truth_hit_count"],
        "shared_policy_all_truth_case_count": shared_all_truth,
        "shared_policy_mean_unique_truth_hit_count": shared_summary.get("best_mean_unique_truth_hit_count"),
        "rank_span_selector_all_truth_case_count": selector_all_truth,
        "rank_span_selector_mean_unique_truth_hit_count": selector_summary.get("leave_one_case_mean_unique_truth_hit_count"),
        "oracle_all_truth_case_count": oracle_all_truth,
        "oracle_mean_unique_truth_hit_count": oracle_summary.get("mean_unique_truth_hit_count"),
        "source_assignment_run": args.assignment_run,
        "source_selector_run": args.selector_run,
        "source_oracle_run": args.oracle_run,
        "gpu_used": False,
        "backend": "saved_bscan_cpu_image_objective_gate",
        "decision": decision,
    }

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    scored_csv = data_dir / "local_2d_detector_image_objective_gate_rows.csv"
    selected_csv = data_dir / "local_2d_detector_image_objective_gate_selected_cases.csv"
    branch_csv = data_dir / "local_2d_detector_image_objective_gate_branch_summary.csv"
    variant_csv = data_dir / "local_2d_detector_image_objective_gate_variant_summary.csv"
    summary_json = data_dir / "local_2d_detector_image_objective_gate_summary.json"
    figure_path = figures_dir / "local_2d_detector_image_objective_gate.png"
    validation_csv = data_dir / "figure_validation.csv"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(scored_csv, [json_safe(row) for row in scored_rows])
    write_csv(selected_csv, [json_safe(row) for row in primary_rows])
    write_csv(branch_csv, [json_safe(row) for row in primary_branch_rows])
    write_csv(variant_csv, [json_safe(row) for row in variant_rows])
    plot_gate(summary, primary_branch_rows, variant_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "scored_csv": str(scored_csv),
        "selected_csv": str(selected_csv),
        "branch_csv": str(branch_csv),
        "variant_csv": str(variant_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_image_objective_gate",
        {
            "assignment_run": args.assignment_run,
            "selector_run": args.selector_run,
            "oracle_run": args.oracle_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

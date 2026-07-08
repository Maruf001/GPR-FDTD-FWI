#!/usr/bin/env python3
"""Synthesize close50 target2 linear-receiver 29.5 mm seed evidence."""

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
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SUMMARY_PATHS = [
    (
        "outputs/experiments/1271_coordinate_optimizer_close50_seed21_sources4_"
        "txrx29p5_linear_receiver_objectives/data/"
        "multi_rebar_coordinate_optimizer_summary.json"
    ),
    (
        "outputs/experiments/1272_coordinate_optimizer_close50_seed13_sources4_"
        "txrx29p5_linear_receiver_objectives/data/"
        "multi_rebar_coordinate_optimizer_summary.json"
    ),
]
SEED_RE = re.compile(r"seed\d+")
TRUTH_TOL = 1.0e-9
STRONG_MARGIN_THRESHOLD = 1.0e-3


def read_json(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_csv_rows(path: str | Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv_rows(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_safe(row.get(key, "")) for key in fieldnames})


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def exact_match(value, truth, tol: float = TRUTH_TOL) -> bool:
    lhs = safe_float(value)
    rhs = safe_float(truth)
    return math.isfinite(lhs) and math.isfinite(rhs) and abs(lhs - rhs) <= tol


def truth_radii(summary: dict) -> list[float]:
    radii = list(summary.get("truth_radius_values_mm") or [])
    if radii:
        return radii
    return [summary.get("truth_radius_mm") for _ in summary.get("true_x_values_mm", [])]


def seed_label_from_rows(rows: list[dict], fallback: str) -> str:
    for row in rows:
        for key in ("case_label", "run_name"):
            match = SEED_RE.search(str(row.get(key, "")))
            if match:
                return match.group(0)
    match = SEED_RE.search(str(fallback))
    return match.group(0) if match else fallback


def row_matches_truth(row: dict, summary: dict) -> bool:
    target_index = int(safe_float(row.get("step_target_index"), safe_float(row.get("target_rebar_index"), -1)))
    truth_x = list(summary.get("true_x_values_mm", []))
    truth_z = list(summary.get("true_z_values_mm", []))
    truth_r = truth_radii(summary)
    return (
        0 <= target_index < len(truth_x)
        and exact_match(row.get("best_x_mm"), truth_x[target_index])
        and exact_match(row.get("best_z_mm"), truth_z[target_index])
        and exact_match(row.get("best_radius_mm"), truth_r[target_index])
    )


def ambiguity_widths(row: dict) -> tuple[float, float]:
    x_width = safe_float(row.get("ambiguity_x_max_mm")) - safe_float(row.get("ambiguity_x_min_mm"))
    r_width = safe_float(row.get("ambiguity_radius_max_mm")) - safe_float(row.get("ambiguity_radius_min_mm"))
    if not math.isfinite(x_width):
        x_width = 0.0
    if not math.isfinite(r_width):
        r_width = 0.0
    return x_width, r_width


def diagnostic_csv_for_summary(summary: dict, summary_path: str | Path) -> Path:
    path = summary.get("paths", {}).get("objective_diagnostic_csv")
    if path:
        return Path(path)
    return Path(summary_path).parent / "coordinate_objective_diagnostics.csv"


def confidence_detail_rows(summary: dict, summary_path: str | Path) -> list[dict]:
    rows = list(summary.get("confidence_rows", []))
    seed_label = seed_label_from_rows(rows, str(summary.get("run_name", Path(summary_path).parent.parent.name)))
    out = []
    for row in rows:
        x_width, r_width = ambiguity_widths(row)
        truth_match = row_matches_truth(row, summary)
        strong = row.get("confidence_label") == "strong"
        out.append({
            "seed_label": seed_label,
            "run_name": summary.get("run_name"),
            "case_label": row.get("case_label"),
            "receiver_sampling": summary.get("receiver_sampling"),
            "tx_rx_offset_mm": safe_float(summary.get("tx_rx_offset_mm")),
            "sources": int(safe_float(summary.get("sources"), 0)),
            "target_rebar_index": int(safe_float(row.get("target_rebar_index"), -1)),
            "best_x_mm": safe_float(row.get("best_x_mm")),
            "best_z_mm": safe_float(row.get("best_z_mm")),
            "best_radius_mm": safe_float(row.get("best_radius_mm")),
            "radius_margin_abs": safe_float(row.get("radius_margin_abs")),
            "confidence_label": row.get("confidence_label"),
            "truth_geometry_match": truth_match,
            "strong_confidence": strong,
            "x_ambiguity_width_mm": x_width,
            "radius_ambiguity_width_mm": r_width,
            "strict_clean_row": truth_match and strong and x_width <= 0.0 and r_width <= 0.0,
            "summary_path": str(summary_path),
        })
    return out


def objective_detail_rows(summary: dict, summary_path: str | Path) -> list[dict]:
    csv_path = diagnostic_csv_for_summary(summary, summary_path)
    if not csv_path.exists():
        return []
    seed_label = seed_label_from_rows(summary.get("confidence_rows", []), str(summary.get("run_name", csv_path)))
    out = []
    for row in read_csv_rows(csv_path):
        truth_match = row_matches_truth(row, summary)
        out.append({
            "seed_label": seed_label,
            "run_name": row.get("run_name"),
            "case_label": row.get("case_label"),
            "objective_label": row.get("objective_label"),
            "target_rebar_index": int(safe_float(row.get("target_rebar_index"), -1)),
            "best_x_mm": safe_float(row.get("best_x_mm")),
            "best_z_mm": safe_float(row.get("best_z_mm")),
            "best_radius_mm": safe_float(row.get("best_radius_mm")),
            "next_radius_mm": safe_float(row.get("next_radius_mm")),
            "radius_margin_abs": safe_float(row.get("radius_margin_abs")),
            "truth_geometry_match": truth_match,
            "diagnostic_csv": str(csv_path),
        })
    return out


def classify_run(confidence_rows: list[dict], diagnostic_rows: list[dict]) -> str:
    row_count = len(confidence_rows)
    if row_count == 0:
        return "missing_confidence_rows"
    truth_count = sum(1 for row in confidence_rows if row["truth_geometry_match"])
    strong_count = sum(1 for row in confidence_rows if row["strong_confidence"])
    ambiguity_count = sum(
        1 for row in confidence_rows
        if row["x_ambiguity_width_mm"] > 0.0 or row["radius_ambiguity_width_mm"] > 0.0
    )
    highband_rows = [row for row in diagnostic_rows if row.get("objective_label") == "highband"]
    highband_truth_count = sum(1 for row in highband_rows if row["truth_geometry_match"])
    highband_ok = not highband_rows or highband_truth_count == len(highband_rows)
    if truth_count == row_count and strong_count == row_count and ambiguity_count == 0 and highband_ok:
        return "single_seed_clean"
    if truth_count == row_count and strong_count == row_count and highband_ok:
        return "single_seed_exact_strong_x_ambiguous"
    if truth_count == row_count:
        return "single_seed_exact_but_policy_limited"
    return "single_seed_mixed_or_wrong_branch"


def seed_count_label(seed_count: int) -> str:
    names = {
        1: "one_seed",
        2: "two_seed",
        3: "three_seed",
    }
    return names.get(seed_count, f"{seed_count}_seed")


def summarize_run(summary: dict, summary_path: str | Path) -> dict:
    confidence_rows = confidence_detail_rows(summary, summary_path)
    diagnostic_rows = objective_detail_rows(summary, summary_path)
    margins = [row["radius_margin_abs"] for row in confidence_rows if math.isfinite(row["radius_margin_abs"])]
    highband_rows = [row for row in diagnostic_rows if row.get("objective_label") == "highband"]
    highband_margins = [
        row["radius_margin_abs"] for row in highband_rows if math.isfinite(row["radius_margin_abs"])
    ]
    seed_label = seed_label_from_rows(summary.get("confidence_rows", []), str(summary.get("run_name", summary_path)))
    return {
        "seed_label": seed_label,
        "run_name": summary.get("run_name"),
        "summary_path": str(summary_path),
        "receiver_sampling": summary.get("receiver_sampling"),
        "tx_rx_offset_mm": safe_float(summary.get("tx_rx_offset_mm")),
        "sources": int(safe_float(summary.get("sources"), 0)),
        "elapsed_time_s": safe_float(summary.get("elapsed_time_s")),
        "confidence_row_count": len(confidence_rows),
        "truth_geometry_row_count": sum(1 for row in confidence_rows if row["truth_geometry_match"]),
        "strong_confidence_row_count": sum(1 for row in confidence_rows if row["strong_confidence"]),
        "strict_clean_row_count": sum(1 for row in confidence_rows if row["strict_clean_row"]),
        "x_ambiguity_row_count": sum(1 for row in confidence_rows if row["x_ambiguity_width_mm"] > 0.0),
        "radius_ambiguity_row_count": sum(1 for row in confidence_rows if row["radius_ambiguity_width_mm"] > 0.0),
        "radius_margin_abs_min": min(margins) if margins else math.nan,
        "radius_margin_abs_mean": float(np.mean(margins)) if margins else math.nan,
        "radius_margin_abs_max": max(margins) if margins else math.nan,
        "highband_row_count": len(highband_rows),
        "highband_truth_row_count": sum(1 for row in highband_rows if row["truth_geometry_match"]),
        "highband_margin_abs_min": min(highband_margins) if highband_margins else math.nan,
        "run_policy_label": classify_run(confidence_rows, diagnostic_rows),
    }


def summarize_policy(run_rows: list[dict], confidence_rows: list[dict], diagnostic_rows: list[dict]) -> dict:
    confidence_row_count = len(confidence_rows)
    truth_count = sum(1 for row in confidence_rows if row["truth_geometry_match"])
    strong_count = sum(1 for row in confidence_rows if row["strong_confidence"])
    x_ambiguity_count = sum(1 for row in confidence_rows if row["x_ambiguity_width_mm"] > 0.0)
    radius_ambiguity_count = sum(1 for row in confidence_rows if row["radius_ambiguity_width_mm"] > 0.0)
    margins = [row["radius_margin_abs"] for row in confidence_rows if math.isfinite(row["radius_margin_abs"])]
    highband_rows = [row for row in diagnostic_rows if row.get("objective_label") == "highband"]
    highband_truth_count = sum(1 for row in highband_rows if row["truth_geometry_match"])
    highband_margins = [
        row["radius_margin_abs"] for row in highband_rows if math.isfinite(row["radius_margin_abs"])
    ]
    all_exact_strong = truth_count == confidence_row_count and strong_count == confidence_row_count
    all_highband_truth = highband_truth_count == len(highband_rows) if highband_rows else True
    no_ambiguity = x_ambiguity_count == 0 and radius_ambiguity_count == 0
    seed_values = sorted({row["seed_label"] for row in confidence_rows})
    seed_count = len(seed_values)
    ambiguous_seed_values = sorted({
        row["seed_label"] for row in confidence_rows
        if row["x_ambiguity_width_mm"] > 0.0 or row["radius_ambiguity_width_mm"] > 0.0
    })
    clean_seed_values = sorted({
        seed for seed in seed_values
        if all(row["strict_clean_row"] for row in confidence_rows if row["seed_label"] == seed)
    })
    label_stem = seed_count_label(seed_count)
    if confidence_row_count == 0:
        policy_label = "close50_linear29p5_missing_evidence"
    elif all_exact_strong and all_highband_truth and no_ambiguity:
        policy_label = f"close50_linear29p5_{label_stem}_clean_candidate"
    elif all_exact_strong and all_highband_truth:
        policy_label = f"close50_linear29p5_{label_stem}_exact_strong_not_clean_replicated"
    elif truth_count == confidence_row_count and all_highband_truth:
        policy_label = f"close50_linear29p5_{label_stem}_exact_but_policy_limited"
    else:
        policy_label = f"close50_linear29p5_{label_stem}_mixed_or_wrong_branch"
    if policy_label.endswith("exact_strong_not_clean_replicated"):
        next_action = (
            "Do not claim a clean replicated below-30 mm threshold for linear 29.5 mm. "
            f"The evidence is exact and strong across {seed_count} seed(s), but "
            f"x/r ambiguity appears in {len(ambiguous_seed_values)} seed(s): "
            f"{','.join(ambiguous_seed_values)}. Keep the nearest-sampled 30 mm "
            "threshold as the paper-safe clean result unless a new objective or "
            "acquisition question is introduced."
        )
    else:
        next_action = "Use the policy label to choose a narrowly scoped follow-up; avoid broad offset sweeps."
    return {
        "policy_label": policy_label,
        "seed_count": seed_count,
        "seed_values": ",".join(seed_values),
        "strict_clean_seed_count": len(clean_seed_values),
        "strict_clean_seed_values": ",".join(clean_seed_values),
        "ambiguous_seed_count": len(ambiguous_seed_values),
        "ambiguous_seed_values": ",".join(ambiguous_seed_values),
        "run_count": len(run_rows),
        "confidence_row_count": confidence_row_count,
        "truth_geometry_row_count": truth_count,
        "strong_confidence_row_count": strong_count,
        "strict_clean_row_count": sum(1 for row in confidence_rows if row["strict_clean_row"]),
        "x_ambiguity_row_count": x_ambiguity_count,
        "radius_ambiguity_row_count": radius_ambiguity_count,
        "radius_margin_abs_min": min(margins) if margins else math.nan,
        "radius_margin_abs_mean": float(np.mean(margins)) if margins else math.nan,
        "radius_margin_abs_max": max(margins) if margins else math.nan,
        "highband_row_count": len(highband_rows),
        "highband_truth_row_count": highband_truth_count,
        "highband_margin_abs_min": min(highband_margins) if highband_margins else math.nan,
        "highband_margin_abs_mean": float(np.mean(highband_margins)) if highband_margins else math.nan,
        "highband_margin_abs_max": max(highband_margins) if highband_margins else math.nan,
        "receiver_sampling_values": ",".join(sorted({str(row["receiver_sampling"]) for row in run_rows})),
        "tx_rx_offset_values_mm": ",".join(
            f"{safe_float(value):g}"
            for value in sorted({row["tx_rx_offset_mm"] for row in run_rows})
        ),
        "next_action": next_action,
    }


def figure_stats(path: Path) -> dict:
    with Image.open(path) as image:
        arr = np.asarray(image.convert("RGB"))
        gray = np.asarray(image.convert("L"))
    sample = arr.reshape(-1, 3)[:: max(1, arr.reshape(-1, 3).shape[0] // 10000)]
    return {
        "path": str(path),
        "width": int(arr.shape[1]),
        "height": int(arr.shape[0]),
        "sampled_unique_colors": int(np.unique(sample, axis=0).shape[0]),
        "nonwhite_fraction": float(np.mean(np.any(arr < 250, axis=2))),
        "dynamic_range": int(gray.max()) - int(gray.min()),
    }


def plot_policy(run_rows: list[dict], confidence_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), constrained_layout=True)
    ordered_conf = sorted(confidence_rows, key=lambda row: (row["seed_label"], row["case_label"]))
    labels = [
        f"{row['seed_label']}:{'src' if str(row['case_label']).startswith('source') else 'nom'}"
        for row in ordered_conf
    ]
    colors = [
        "#2f9d55" if row["strict_clean_row"] else "#d99a19"
        for row in ordered_conf
    ]
    axes[0].bar(labels, [row["radius_margin_abs"] for row in ordered_conf], color=colors)
    axes[0].axhline(STRONG_MARGIN_THRESHOLD, color="#444444", linestyle="--", linewidth=1.0)
    axes[0].set_ylabel("radius margin abs")
    axes[0].set_title("Primary confidence rows")
    axes[0].tick_params(axis="x", rotation=30, labelsize=8)
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    ordered_runs = sorted(run_rows, key=lambda row: row["seed_label"])
    x = np.arange(len(ordered_runs))
    axes[1].bar(
        x - 0.18,
        [row["strict_clean_row_count"] for row in ordered_runs],
        width=0.36,
        color="#2f9d55",
        label="strict clean rows",
    )
    axes[1].bar(
        x + 0.18,
        [row["x_ambiguity_row_count"] for row in ordered_runs],
        width=0.36,
        color="#d99a19",
        label="x ambiguous rows",
    )
    axes[1].set_xticks(x, [row["seed_label"] for row in ordered_runs])
    axes[1].set_ylabel("row count")
    axes[1].set_title("Clean vs x-ambiguous rows")
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(summary["policy_label"], fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary_json", nargs="*", help="optimizer summary JSON paths")
    parser.add_argument("--run-name", default="close50_linear_receiver_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    summary_paths = [Path(path) for path in (args.summary_json or DEFAULT_SUMMARY_PATHS)]
    for path in summary_paths:
        if not path.exists():
            raise FileNotFoundError(path)

    optimizer_summaries = [(path, read_json(path)) for path in summary_paths]
    confidence_rows: list[dict] = []
    diagnostic_rows: list[dict] = []
    run_rows: list[dict] = []
    for path, summary in optimizer_summaries:
        confidence_rows.extend(confidence_detail_rows(summary, path))
        diagnostic_rows.extend(objective_detail_rows(summary, path))
        run_rows.append(summarize_run(summary, path))

    policy_summary = summarize_policy(run_rows, confidence_rows, diagnostic_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    run_csv = data_dir / "close50_linear_receiver_run_rows.csv"
    confidence_csv = data_dir / "close50_linear_receiver_confidence_rows.csv"
    diagnostic_csv = data_dir / "close50_linear_receiver_objective_diagnostics.csv"
    validation_csv = data_dir / "figure_validation.csv"
    summary_json = data_dir / "close50_linear_receiver_policy_summary.json"
    figure_path = Path(plot_policy(run_rows, confidence_rows, policy_summary, figures_dir / "close50_linear_receiver_policy.png"))

    write_csv_rows(run_csv, run_rows)
    write_csv_rows(confidence_csv, confidence_rows)
    write_csv_rows(diagnostic_csv, diagnostic_rows)
    write_csv_rows(validation_csv, [figure_stats(figure_path)])

    output_summary = {
        **policy_summary,
        "input_summary_jsons": [str(path) for path in summary_paths],
        "paths": {
            "run_csv": str(run_csv),
            "confidence_csv": str(confidence_csv),
            "diagnostic_csv": str(diagnostic_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "close50_linear_receiver_policy",
        {
            "summary_json": str(summary_json),
            "run_csv": str(run_csv),
            "confidence_csv": str(confidence_csv),
            "diagnostic_csv": str(diagnostic_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

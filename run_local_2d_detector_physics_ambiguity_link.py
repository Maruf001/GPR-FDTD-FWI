#!/usr/bin/env python3
"""Link detector reliability review cases to close-spacing physics ambiguity evidence."""

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
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_blind_envelope_robustness_audit import parse_bool  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_RELIABILITY_RUN = "069_local_2d_detector_blind_envelope_reliability_gate"
DEFAULT_THRESHOLD_RUN = "1317_close50_legacy_270_280_policy_audit_post_28p75_seed13_replicate"
DEFAULT_LINEAR29P5_RUN = "1303_close50_linear29p5_three_seed_frequency_policy"
LINEAR29P5_BRANCH = "target2_close50_linear29p5"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def seed_key(value: object) -> str:
    number = safe_int(value, -1)
    return f"seed{number}" if number >= 0 else str(value)


def synthetic_case_label(seed: object, case_variant: object) -> str:
    label = seed_key(seed)
    if str(case_variant) == "source_mismatch":
        return f"source_mismatch_noise10_{label}"
    return f"noise10_{label}"


def linear29p5_confidence_lookup(confidence_rows: list[dict]) -> dict[tuple[str, str], dict]:
    output = {}
    for row in confidence_rows:
        seed = str(row.get("seed_label", ""))
        case_label = str(row.get("case_label", ""))
        if seed and case_label:
            output[(seed, case_label)] = row
    return output


def linear29p5_run_lookup(run_rows: list[dict]) -> dict[str, dict]:
    return {str(row.get("seed_label", "")): row for row in run_rows if row.get("seed_label")}


def build_link_rows(
    reliability_rows: list[dict],
    linear29p5_confidence_rows: list[dict],
    linear29p5_run_rows: list[dict],
    close50_threshold_summary: dict,
) -> list[dict]:
    confidence_by_seed_case = linear29p5_confidence_lookup(linear29p5_confidence_rows)
    run_by_seed = linear29p5_run_lookup(linear29p5_run_rows)
    first_clean = safe_float(close50_threshold_summary.get("first_clean_tx_rx_offset_mm"), math.nan)
    outputs = []

    for row in reliability_rows:
        branch_key = str(row.get("branch_key", ""))
        seed = safe_int(row.get("seed"), -1)
        case_variant = str(row.get("case_variant", ""))
        review = not parse_bool(row.get("truth_free_stable_assignment"))
        tuning_sensitive = parse_bool(row.get("tuning_sensitive_truth_eval"))
        is_linear29p5 = branch_key == LINEAR29P5_BRANCH
        synthetic_label = synthetic_case_label(seed, case_variant)
        synthetic_seed = seed_key(seed)
        confidence = (
            confidence_by_seed_case.get((synthetic_seed, synthetic_label), {})
            if is_linear29p5
            else {}
        )
        run = run_by_seed.get(synthetic_seed, {}) if is_linear29p5 else {}
        txrx = safe_float(confidence.get("tx_rx_offset_mm"), math.nan)
        x_ambiguity = safe_float(confidence.get("x_ambiguity_width_mm"), 0.0)
        strict_clean = parse_bool(confidence.get("strict_clean_row"))
        truth_geometry = parse_bool(confidence.get("truth_geometry_match"))
        strong = parse_bool(confidence.get("strong_confidence"))
        below_first_clean = bool(
            is_linear29p5
            and math.isfinite(txrx)
            and math.isfinite(first_clean)
            and txrx < first_clean
        )
        outputs.append(
            {
                "case_label": row.get("case_label", ""),
                "branch_key": branch_key,
                "seed": seed,
                "case_variant": case_variant,
                "detector_reliability_label": row.get("truth_free_reliability_label", ""),
                "detector_review": review,
                "detector_tuning_sensitive": tuning_sensitive,
                "detector_success_fraction": safe_float(row.get("success_fraction_truth_eval"), math.nan),
                "detector_max_slot_x_range_mm": safe_float(row.get("max_slot_x_range_mm"), math.nan),
                "detector_max_slot_z_range_mm": safe_float(row.get("max_slot_z_range_mm"), math.nan),
                "detector_dominant_selection": row.get("dominant_selection", ""),
                "physics_family": (
                    "close50_linear29p5_below_first_clean_boundary"
                    if is_linear29p5
                    else "close14_detector_reference"
                ),
                "synthetic_case_label": synthetic_label if is_linear29p5 else "",
                "synthetic_confidence_present": bool(confidence),
                "synthetic_tx_rx_offset_mm": txrx if is_linear29p5 else math.nan,
                "synthetic_first_clean_tx_rx_offset_mm": first_clean if is_linear29p5 else math.nan,
                "synthetic_offset_below_first_clean_mm": (
                    first_clean - txrx
                    if is_linear29p5 and math.isfinite(first_clean) and math.isfinite(txrx)
                    else math.nan
                ),
                "synthetic_below_first_clean_threshold": below_first_clean,
                "synthetic_truth_geometry": truth_geometry if is_linear29p5 else False,
                "synthetic_strong_confidence": strong if is_linear29p5 else False,
                "synthetic_strict_clean_row": strict_clean if is_linear29p5 else False,
                "synthetic_x_ambiguity_width_mm": x_ambiguity if is_linear29p5 else math.nan,
                "synthetic_x_ambiguous_row": bool(is_linear29p5 and x_ambiguity > 0.0),
                "synthetic_run_policy_label": run.get("run_policy_label", "") if is_linear29p5 else "",
                "review_near_boundary_nominal": bool(
                    review
                    and is_linear29p5
                    and case_variant == "nominal"
                    and below_first_clean
                ),
            }
        )
    return sorted(outputs, key=lambda item: (item["branch_key"], item["seed"], item["case_variant"]))


def build_group_rows(link_rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in link_rows:
        grouped[(str(row["branch_key"]), str(row["case_variant"]))].append(row)

    outputs = []
    for (branch_key, case_variant), rows in grouped.items():
        review_rows = [row for row in rows if row["detector_review"]]
        near_rows = [row for row in rows if row["synthetic_below_first_clean_threshold"]]
        x_ambiguous_rows = [row for row in rows if row["synthetic_x_ambiguous_row"]]
        outputs.append(
            {
                "branch_key": branch_key,
                "case_variant": case_variant,
                "case_count": len(rows),
                "detector_review_count": len(review_rows),
                "detector_review_fraction": len(review_rows) / len(rows) if rows else 0.0,
                "detector_tuning_sensitive_count": sum(row["detector_tuning_sensitive"] for row in rows),
                "max_detector_slot_x_range_mm": max(
                    [safe_float(row.get("detector_max_slot_x_range_mm"), math.nan) for row in rows]
                    or [math.nan]
                ),
                "median_detector_slot_x_range_mm": float(
                    np.nanmedian([safe_float(row.get("detector_max_slot_x_range_mm"), math.nan) for row in rows])
                )
                if rows
                else math.nan,
                "near_boundary_case_count": len(near_rows),
                "synthetic_x_ambiguous_case_count": len(x_ambiguous_rows),
                "review_case_labels": ";".join(str(row["case_label"]) for row in review_rows),
            }
        )
    return sorted(outputs, key=lambda item: (item["branch_key"], item["case_variant"]))


def summarize_link(
    link_rows: list[dict],
    group_rows: list[dict],
    reliability_summary: dict,
    close50_threshold_summary: dict,
    linear29p5_summary: dict,
) -> dict:
    review_rows = [row for row in link_rows if row["detector_review"]]
    near_review_rows = [row for row in review_rows if row["review_near_boundary_nominal"]]
    linear_rows = [row for row in link_rows if row["branch_key"] == LINEAR29P5_BRANCH]
    linear_nominal_rows = [
        row for row in linear_rows
        if row["case_variant"] == "nominal"
    ]
    linear_source_mismatch_rows = [
        row for row in linear_rows
        if row["case_variant"] == "source_mismatch"
    ]
    review_x_ambiguous = [row for row in review_rows if row["synthetic_x_ambiguous_row"]]
    review_strict_clean = [row for row in review_rows if row["synthetic_strict_clean_row"]]
    all_reviews_near_boundary_nominal = len(review_rows) > 0 and len(near_review_rows) == len(review_rows)
    per_seed_x_explains_all_reviews = len(review_rows) > 0 and len(review_x_ambiguous) == len(review_rows)
    return {
        "policy_label": "local_2d_detector_physics_ambiguity_link_cpu_no_fwi",
        "source_reliability_policy_label": reliability_summary.get("policy_label", ""),
        "source_close50_threshold_policy_label": close50_threshold_summary.get("policy_label", ""),
        "source_linear29p5_policy_label": linear29p5_summary.get("policy_label", ""),
        "case_count": len(link_rows),
        "group_count": len(group_rows),
        "detector_review_case_count": len(review_rows),
        "detector_stable_case_count": len(link_rows) - len(review_rows),
        "review_near_boundary_nominal_count": len(near_review_rows),
        "review_near_boundary_nominal_fraction": (
            len(near_review_rows) / len(review_rows) if review_rows else 0.0
        ),
        "detector_reviews_all_near_boundary_nominal": all_reviews_near_boundary_nominal,
        "close50_linear29p5_case_count": len(linear_rows),
        "close50_linear29p5_nominal_case_count": len(linear_nominal_rows),
        "close50_linear29p5_nominal_review_count": sum(row["detector_review"] for row in linear_nominal_rows),
        "close50_linear29p5_nominal_review_fraction": (
            sum(row["detector_review"] for row in linear_nominal_rows) / len(linear_nominal_rows)
            if linear_nominal_rows
            else 0.0
        ),
        "close50_linear29p5_source_mismatch_case_count": len(linear_source_mismatch_rows),
        "close50_linear29p5_source_mismatch_review_count": sum(
            row["detector_review"] for row in linear_source_mismatch_rows
        ),
        "close50_first_clean_tx_rx_offset_mm": safe_float(
            close50_threshold_summary.get("first_clean_tx_rx_offset_mm"),
            math.nan,
        ),
        "linear29p5_tx_rx_offset_mm": 29.5,
        "linear29p5_offset_below_first_clean_mm": (
            safe_float(close50_threshold_summary.get("first_clean_tx_rx_offset_mm"), math.nan) - 29.5
        ),
        "linear29p5_synthetic_seed_count": safe_int(linear29p5_summary.get("seed_count"), 0),
        "linear29p5_synthetic_strict_clean_seed_count": safe_int(
            linear29p5_summary.get("strict_clean_seed_count"),
            0,
        ),
        "linear29p5_synthetic_ambiguous_seed_count": safe_int(
            linear29p5_summary.get("ambiguous_seed_count"),
            0,
        ),
        "review_cases_with_synthetic_x_ambiguity_count": len(review_x_ambiguous),
        "review_cases_with_synthetic_strict_clean_count": len(review_strict_clean),
        "per_seed_synthetic_x_ambiguity_explains_all_reviews": per_seed_x_explains_all_reviews,
        "ready_for_branch_localization_claim": all_reviews_near_boundary_nominal,
        "ready_for_per_seed_physics_equivalence_claim": per_seed_x_explains_all_reviews,
        "ready_for_global_detector_tuning": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "Detector review cases are localized to the close50 linear-29.5 nominal family, "
            "which sits 0.5 mm below the paper-safe 30 mm clean threshold. However, per-seed "
            "synthetic x-ambiguity explains only part of the review set, so this is a "
            "branch/variant ambiguity-link result, not proof that coordinate objective "
            "ambiguity alone predicts every detector review case."
        ),
    }


def plot_link(link_rows: list[dict], group_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(14.0, 5.3), constrained_layout=True)

    labels = [
        f"{row['branch_key'].replace('target2_', '').replace('_linear29p5', '29.5')}\n"
        f"s{row['seed']} {row['case_variant'].replace('source_mismatch', 'src-mis')}"
        for row in link_rows
    ]
    slot_ranges = [safe_float(row.get("detector_max_slot_x_range_mm"), 0.0) for row in link_rows]
    colors = [
        "#e15759" if row["detector_review"] else "#4e79a7"
        for row in link_rows
    ]
    axes[0].bar(np.arange(len(link_rows)), slot_ranges, color=colors)
    axes[0].axhline(5.0, color="#f28e2b", linestyle="--", linewidth=1.2, label="5 mm gate")
    axes[0].set_xticks(np.arange(len(link_rows)))
    axes[0].set_xticklabels(labels, rotation=55, ha="right", fontsize=7.0)
    axes[0].set_ylabel("max x-slot drift (mm)")
    axes[0].set_title("Truth-free detector reliability gate")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(fontsize=8)

    close50_rows = [row for row in link_rows if row["branch_key"] == LINEAR29P5_BRANCH]
    y_map = {"nominal": 1.0, "source_mismatch": 0.0}
    for row in close50_rows:
        marker = "X" if row["synthetic_x_ambiguous_row"] else "o"
        color = "#e15759" if row["detector_review"] else "#59a14f"
        size = 125 if row["detector_review"] else 90
        axes[1].scatter(
            row["seed"],
            y_map.get(row["case_variant"], 0.5),
            s=size,
            marker=marker,
            color=color,
            edgecolor="#333333",
            linewidth=0.7,
        )
    axes[1].set_yticks([0.0, 1.0])
    axes[1].set_yticklabels(["source mismatch", "nominal"])
    axes[1].set_xticks(sorted({row["seed"] for row in close50_rows}))
    axes[1].set_xlabel("seed")
    axes[1].set_title("Close50 29.5 mm detector/physics link")
    axes[1].grid(color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.95,
        f"review cases: {summary['detector_review_case_count']}\n"
        f"near-boundary nominal reviews: {summary['review_near_boundary_nominal_count']}\n"
        f"synthetic x-ambiguous reviews: {summary['review_cases_with_synthetic_x_ambiguity_count']}\n"
        f"all reviews explained per seed: {summary['per_seed_synthetic_x_ambiguity_explains_all_reviews']}\n"
        f"FWI ready: {summary['ready_for_detector_seeded_fwi']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    axes[1].scatter([], [], color="#e15759", marker="o", label="detector review")
    axes[1].scatter([], [], color="#59a14f", marker="o", label="detector stable")
    axes[1].scatter([], [], color="#999999", marker="X", label="synthetic x ambiguous")
    axes[1].legend(fontsize=8, loc="lower right")

    fig.suptitle("Detector review cases vs close-spacing ambiguity evidence", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, link_csv: Path, group_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_physics_ambiguity_link.png`",
                "",
                "This CPU-only figure links truth-free detector review cases to the",
                "saved close50 29.5 mm synthetic ambiguity evidence.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Detector review cases: `{summary['detector_review_case_count']}`.",
                f"Review near-boundary nominal count: `{summary['review_near_boundary_nominal_count']}`.",
                f"Review cases with synthetic x ambiguity: `{summary['review_cases_with_synthetic_x_ambiguity_count']}`.",
                f"Ready for branch-localization claim: `{summary['ready_for_branch_localization_claim']}`.",
                f"Ready for per-seed physics-equivalence claim: `{summary['ready_for_per_seed_physics_equivalence_claim']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Case link rows: `{link_csv.name}`.",
                f"- Group rows: `{group_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved detector reliability rows and saved close50",
                "coordinate-confidence summaries. It does not run FDTD, FWI, GPU",
                "kernels, field FWI, 3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--experiment-root", default="outputs/experiments")
    parser.add_argument("--reliability-run", default=DEFAULT_RELIABILITY_RUN)
    parser.add_argument("--threshold-run", default=DEFAULT_THRESHOLD_RUN)
    parser.add_argument("--linear29p5-run", default=DEFAULT_LINEAR29P5_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_physics_ambiguity_link")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    experiment_root = Path(args.experiment_root)
    reliability_dir = summary_root / args.reliability_run
    threshold_dir = experiment_root / args.threshold_run
    linear_dir = experiment_root / args.linear29p5_run

    reliability_rows = read_csv_rows(
        reliability_dir / "data/local_2d_detector_blind_envelope_reliability_gate_cases.csv"
    )
    reliability_summary = read_json(
        reliability_dir / "data/local_2d_detector_blind_envelope_reliability_gate_summary.json"
    )
    close50_threshold_summary = read_json(
        threshold_dir / "data/close50_legacy_policy_audit_summary.json"
    )
    linear29p5_summary = read_json(
        linear_dir / "data/close50_linear_receiver_policy_summary.json"
    )
    linear29p5_confidence_rows = read_csv_rows(
        linear_dir / "data/close50_linear_receiver_confidence_rows.csv"
    )
    linear29p5_run_rows = read_csv_rows(
        linear_dir / "data/close50_linear_receiver_run_rows.csv"
    )

    link_rows = build_link_rows(
        reliability_rows,
        linear29p5_confidence_rows,
        linear29p5_run_rows,
        close50_threshold_summary,
    )
    group_rows = build_group_rows(link_rows)
    summary = summarize_link(
        link_rows,
        group_rows,
        reliability_summary,
        close50_threshold_summary,
        linear29p5_summary,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    link_csv = data_dir / "local_2d_detector_physics_ambiguity_link_cases.csv"
    group_csv = data_dir / "local_2d_detector_physics_ambiguity_link_groups.csv"
    summary_json = data_dir / "local_2d_detector_physics_ambiguity_link_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_physics_ambiguity_link.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(link_csv, [json_safe(row) for row in link_rows])
    write_csv(group_csv, [json_safe(row) for row in group_rows])
    plot_link(link_rows, group_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, link_csv, group_csv)
    summary["paths"] = {
        "case_link_csv": str(link_csv),
        "group_csv": str(group_csv),
        "summary_json": str(summary_json),
        "source_reliability_summary_json": str(
            reliability_dir / "data/local_2d_detector_blind_envelope_reliability_gate_summary.json"
        ),
        "source_reliability_cases_csv": str(
            reliability_dir / "data/local_2d_detector_blind_envelope_reliability_gate_cases.csv"
        ),
        "source_close50_threshold_summary_json": str(
            threshold_dir / "data/close50_legacy_policy_audit_summary.json"
        ),
        "source_linear29p5_summary_json": str(
            linear_dir / "data/close50_linear_receiver_policy_summary.json"
        ),
        "source_linear29p5_confidence_csv": str(
            linear_dir / "data/close50_linear_receiver_confidence_rows.csv"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_detector_physics_ambiguity_link",
        {
            "reliability_run": args.reliability_run,
            "threshold_run": args.threshold_run,
            "linear29p5_run": args.linear29p5_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

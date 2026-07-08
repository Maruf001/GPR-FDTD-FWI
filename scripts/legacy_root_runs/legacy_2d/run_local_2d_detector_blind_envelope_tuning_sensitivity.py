#!/usr/bin/env python3
"""Decompose tuning sensitivity for blind-envelope close50 detector cases."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter, defaultdict
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
from run_local_2d_detector_blind_envelope_policy_stability import (  # noqa: E402
    DEFAULT_BLIND_ENVELOPE_RUN,
    read_csv_rows,
)
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_STABILITY_RUN = "063_local_2d_detector_blind_envelope_policy_stability"
KNOB_COLUMNS = [
    "envelope_weight",
    "structural_weight",
    "support_weight",
    "center_weight",
    "span_threshold_mm",
]
FEATURE_COLUMNS = [
    "selection_score",
    "selected_base_sum",
    "edge_envelope_score",
    "support_score",
    "active_structure_score",
    "regular_structure_score",
    "pair_structure_score",
    "regular_center_score",
    "x_span_mm",
    "gap_left_mm",
    "gap_right_mm",
]


def tuning_sensitive_case_labels(case_rows: list[dict], threshold: float = 0.90) -> list[str]:
    return [
        str(row.get("case_label", ""))
        for row in case_rows
        if safe_float(row.get("success_fraction"), 0.0) < threshold
    ]


def knob_value_rows(selected_rows: list[dict], case_labels: list[str]) -> list[dict]:
    rows = []
    case_set = set(case_labels)
    for case_label in case_labels:
        case_rows = [row for row in selected_rows if row.get("case_label") == case_label]
        for knob in KNOB_COLUMNS:
            grouped: dict[str, list[dict]] = defaultdict(list)
            for row in case_rows:
                grouped[str(row.get(knob, ""))].append(row)
            for value, group in sorted(grouped.items(), key=lambda item: safe_float(item[0], 0.0)):
                success_count = sum(parse_bool(row.get("all_target_slots_hit")) for row in group)
                rows.append(
                    {
                        "case_label": case_label,
                        "branch_key": group[0].get("branch_key", "") if group else "",
                        "seed": safe_int(group[0].get("seed"), 0) if group else 0,
                        "case_variant": group[0].get("case_variant", "") if group else "",
                        "knob": knob,
                        "knob_value": safe_float(value),
                        "variant_count": len(group),
                        "success_count": success_count,
                        "failure_count": len(group) - success_count,
                        "success_fraction": success_count / len(group) if group else 0.0,
                    }
                )
    return [row for row in rows if row["case_label"] in case_set]


def knob_effect_rows(value_rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in value_rows:
        grouped[(str(row["case_label"]), str(row["knob"]))].append(row)
    outputs = []
    for (case_label, knob), rows in grouped.items():
        best = max(rows, key=lambda row: (safe_float(row["success_fraction"], 0.0), safe_float(row["knob_value"], 0.0)))
        worst = min(rows, key=lambda row: (safe_float(row["success_fraction"], 0.0), safe_float(row["knob_value"], 0.0)))
        outputs.append(
            {
                "case_label": case_label,
                "branch_key": best.get("branch_key", ""),
                "seed": safe_int(best.get("seed"), 0),
                "case_variant": best.get("case_variant", ""),
                "knob": knob,
                "best_value": safe_float(best.get("knob_value")),
                "best_success_fraction": safe_float(best.get("success_fraction"), 0.0),
                "worst_value": safe_float(worst.get("knob_value")),
                "worst_success_fraction": safe_float(worst.get("success_fraction"), 0.0),
                "success_fraction_effect": safe_float(best.get("success_fraction"), 0.0)
                - safe_float(worst.get("success_fraction"), 0.0),
            }
        )
    return sorted(outputs, key=lambda row: (row["case_label"], -safe_float(row["success_fraction_effect"], 0.0)))


def feature_contrast_rows(selected_rows: list[dict], case_labels: list[str]) -> list[dict]:
    outputs = []
    for case_label in case_labels:
        case_rows = [row for row in selected_rows if row.get("case_label") == case_label]
        success_rows = [row for row in case_rows if parse_bool(row.get("all_target_slots_hit"))]
        failure_rows = [row for row in case_rows if not parse_bool(row.get("all_target_slots_hit"))]
        for feature in FEATURE_COLUMNS:
            success_values = [
                safe_float(row.get(feature))
                for row in success_rows
                if math.isfinite(safe_float(row.get(feature)))
            ]
            failure_values = [
                safe_float(row.get(feature))
                for row in failure_rows
                if math.isfinite(safe_float(row.get(feature)))
            ]
            if not success_values or not failure_values:
                continue
            success_mean = float(np.mean(success_values))
            failure_mean = float(np.mean(failure_values))
            outputs.append(
                {
                    "case_label": case_label,
                    "feature": feature,
                    "success_mean": success_mean,
                    "failure_mean": failure_mean,
                    "delta_success_minus_failure": success_mean - failure_mean,
                    "abs_delta": abs(success_mean - failure_mean),
                }
            )
    return sorted(outputs, key=lambda row: (row["case_label"], -safe_float(row["abs_delta"], 0.0)))


def case_failure_rows(selected_rows: list[dict], case_labels: list[str]) -> list[dict]:
    outputs = []
    for case_label in case_labels:
        case_rows = [row for row in selected_rows if row.get("case_label") == case_label]
        failure_rows = [row for row in case_rows if not parse_bool(row.get("all_target_slots_hit"))]
        failure_counts = Counter(row.get("selected_x_values_mm", "") for row in failure_rows)
        dominant_failure, dominant_count = failure_counts.most_common(1)[0] if failure_counts else ("", 0)
        outputs.append(
            {
                "case_label": case_label,
                "variant_count": len(case_rows),
                "success_count": len(case_rows) - len(failure_rows),
                "failure_count": len(failure_rows),
                "success_fraction": (len(case_rows) - len(failure_rows)) / len(case_rows) if case_rows else 0.0,
                "unique_failure_selection_count": len(failure_counts),
                "dominant_failure_selection": dominant_failure,
                "dominant_failure_count": dominant_count,
            }
        )
    return outputs


def _best_by_case_and_knob(effect_rows: list[dict], knob: str) -> dict[str, float]:
    return {
        str(row["case_label"]): safe_float(row.get("best_value"))
        for row in effect_rows
        if row.get("knob") == knob
    }


def summarize_sensitivity(
    case_rows: list[dict],
    effect_rows: list[dict],
    feature_rows: list[dict],
    failure_rows: list[dict],
    stability_summary: dict,
) -> dict:
    structural_best = _best_by_case_and_knob(effect_rows, "structural_weight")
    support_best = _best_by_case_and_knob(effect_rows, "support_weight")
    structural_values = {value for value in structural_best.values() if math.isfinite(value)}
    support_values = {value for value in support_best.values() if math.isfinite(value)}
    max_effect = max([safe_float(row.get("success_fraction_effect"), 0.0) for row in effect_rows] or [0.0])
    top_effect = max(effect_rows, key=lambda row: safe_float(row.get("success_fraction_effect"), 0.0)) if effect_rows else {}
    span_effect_max = max(
        [
            safe_float(row.get("success_fraction_effect"), 0.0)
            for row in effect_rows
            if row.get("knob") == "span_threshold_mm"
        ]
        or [0.0]
    )
    return {
        "policy_label": "local_2d_detector_blind_envelope_tuning_sensitivity_cpu_no_fwi",
        "source_stability_policy_label": stability_summary.get("policy_label", ""),
        "tuning_sensitive_case_count": len(case_rows),
        "case_labels": ";".join(row["case_label"] for row in case_rows),
        "max_knob_success_fraction_effect": max_effect,
        "top_effect_case_label": top_effect.get("case_label", ""),
        "top_effect_knob": top_effect.get("knob", ""),
        "top_effect_best_value": safe_float(top_effect.get("best_value")),
        "top_effect_worst_value": safe_float(top_effect.get("worst_value")),
        "structural_weight_best_values": ";".join(
            f"{case}={value:g}" for case, value in sorted(structural_best.items())
        ),
        "support_weight_best_values": ";".join(
            f"{case}={value:g}" for case, value in sorted(support_best.items())
        ),
        "structural_weight_direction_conflict": len(structural_values) > 1,
        "support_weight_direction_conflict": len(support_values) > 1,
        "span_threshold_max_effect": span_effect_max,
        "dominant_failure_selection_count": max(
            [safe_int(row.get("dominant_failure_count"), 0) for row in failure_rows] or [0]
        ),
        "feature_contrast_row_count": len(feature_rows),
        "ready_for_global_policy_tuning_fix": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "The close50 nominal fragility is not a simple one-knob tuning problem: "
            "the best structural/support weights point in different directions across the two sensitive seeds. "
            "Use this as a CPU-side detector ambiguity boundary, not as a detector-seeded FWI trigger."
        ),
    }


def plot_sensitivity(effect_rows: list[dict], feature_rows: list[dict], summary: dict, save_path: Path) -> str:
    cases = sorted({row["case_label"] for row in effect_rows})
    knobs = KNOB_COLUMNS
    fig, axes = plt.subplots(1, 2, figsize=(14.8, 5.2), constrained_layout=True)
    width = 0.38
    x = np.arange(len(knobs))
    for idx, case_label in enumerate(cases):
        values = [
            next(
                (
                    safe_float(row["success_fraction_effect"], 0.0)
                    for row in effect_rows
                    if row["case_label"] == case_label and row["knob"] == knob
                ),
                0.0,
            )
            for knob in knobs
        ]
        axes[0].bar(x + (idx - 0.5) * width, values, width=width, label=case_label.replace("|", "\n"))
    axes[0].set_xticks(x, [knob.replace("_", "\n") for knob in knobs], fontsize=8)
    axes[0].set_ylabel("success-fraction effect")
    axes[0].set_title("Policy knob sensitivity")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(fontsize=7, loc="upper left")

    top_features = feature_rows[:8]
    labels = [f"{row['case_label'].split('|')[1]}\n{row['feature']}" for row in top_features]
    deltas = [safe_float(row["delta_success_minus_failure"], 0.0) for row in top_features]
    colors = ["#2f9d55" if value >= 0 else "#c7302b" for value in deltas]
    axes[1].bar(np.arange(len(top_features)), deltas, color=colors, edgecolor="#333333", linewidth=0.5)
    axes[1].set_xticks(np.arange(len(top_features)), labels, rotation=45, ha="right", fontsize=7)
    axes[1].set_ylabel("success mean - failure mean")
    axes[1].set_title("Largest success/failure feature contrasts")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.95,
        f"max knob effect={summary['max_knob_success_fraction_effect']:.3f}\n"
        f"structural conflict={summary['structural_weight_direction_conflict']}\n"
        f"support conflict={summary['support_weight_direction_conflict']}\n"
        f"ready FWI={summary['ready_for_detector_seeded_fwi']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Close50 blind-envelope tuning sensitivity", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, effect_csv: Path, feature_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_blind_envelope_tuning_sensitivity.png`",
                "",
                "This CPU-only figure decomposes why the two close50 nominal cases",
                "are tuning-sensitive under the blind-envelope policy grid.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Tuning-sensitive cases: `{summary['tuning_sensitive_case_count']}`.",
                f"Maximum knob effect: `{summary['max_knob_success_fraction_effect']}`.",
                f"Top-effect knob: `{summary['top_effect_knob']}`.",
                f"Structural-weight direction conflict: `{summary['structural_weight_direction_conflict']}`.",
                f"Support-weight direction conflict: `{summary['support_weight_direction_conflict']}`.",
                f"Ready for global policy tuning fix: `{summary['ready_for_global_policy_tuning_fix']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Knob-effect rows: `{effect_csv.name}`.",
                f"- Feature-contrast rows: `{feature_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved CPU detector summaries only. It does not run FDTD, FWI,",
                "GPU kernels, 3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blind-envelope-run", default=DEFAULT_BLIND_ENVELOPE_RUN)
    parser.add_argument("--stability-run", default=DEFAULT_STABILITY_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_blind_envelope_tuning_sensitivity")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dir = Path("outputs/summary_tables") / args.blind_envelope_run
    stability_dir = Path("outputs/summary_tables") / args.stability_run
    selected_rows = read_csv_rows(
        source_dir / "data/local_2d_detector_blind_component_envelope_assembly_selected_cases.csv"
    )
    stability_cases = read_csv_rows(
        stability_dir / "data/local_2d_detector_blind_envelope_policy_stability_cases.csv"
    )
    stability_summary = read_json(
        stability_dir / "data/local_2d_detector_blind_envelope_policy_stability_summary.json"
    )
    case_labels = tuning_sensitive_case_labels(stability_cases)
    case_rows = [
        row for row in stability_cases
        if row.get("case_label") in set(case_labels)
    ]
    value_rows = knob_value_rows(selected_rows, case_labels)
    effect_rows = knob_effect_rows(value_rows)
    feature_rows = feature_contrast_rows(selected_rows, case_labels)
    failure_rows = case_failure_rows(selected_rows, case_labels)
    summary = summarize_sensitivity(case_rows, effect_rows, feature_rows, failure_rows, stability_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root="outputs/summary_tables"))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    value_csv = data_dir / "local_2d_detector_blind_envelope_tuning_sensitivity_knob_values.csv"
    effect_csv = data_dir / "local_2d_detector_blind_envelope_tuning_sensitivity_knob_effects.csv"
    feature_csv = data_dir / "local_2d_detector_blind_envelope_tuning_sensitivity_features.csv"
    failure_csv = data_dir / "local_2d_detector_blind_envelope_tuning_sensitivity_failures.csv"
    summary_json = data_dir / "local_2d_detector_blind_envelope_tuning_sensitivity_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_blind_envelope_tuning_sensitivity.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(value_csv, [json_safe(row) for row in value_rows])
    write_csv(effect_csv, [json_safe(row) for row in effect_rows])
    write_csv(feature_csv, [json_safe(row) for row in feature_rows])
    write_csv(failure_csv, [json_safe(row) for row in failure_rows])
    plot_sensitivity(effect_rows, feature_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "knob_values_csv": str(value_csv),
        "knob_effects_csv": str(effect_csv),
        "feature_contrasts_csv": str(feature_csv),
        "failure_rows_csv": str(failure_csv),
        "summary_json": str(summary_json),
        "source_selected_cases_csv": str(
            source_dir / "data/local_2d_detector_blind_component_envelope_assembly_selected_cases.csv"
        ),
        "source_stability_cases_csv": str(
            stability_dir / "data/local_2d_detector_blind_envelope_policy_stability_cases.csv"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, effect_csv, feature_csv)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_blind_envelope_tuning_sensitivity",
        {
            "blind_envelope_run": args.blind_envelope_run,
            "stability_run": args.stability_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

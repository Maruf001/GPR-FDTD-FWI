#!/usr/bin/env python3
"""Synthesize close14/close50 source-density evidence across spacing regimes."""

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
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CLOSE50_SOURCE_SUMMARY = (
    "outputs/summary_tables/099_close50_source_count_replicate_synthesis/"
    "data/close50_source_count_replicate_by_source_count.csv"
)
DEFAULT_CLOSE14_SOURCE_SUMMARY = (
    "outputs/summary_tables/102_close14_source3_three_seed_policy_synthesis/"
    "data/close14_source3_three_seed_by_source_count.csv"
)
DEFAULT_ARCHIVE_GROUP_SUMMARY = (
    "outputs/summary_tables/103_close_spacing_source_density_archive_map/"
    "data/close_spacing_source_density_group_summary.csv"
)
DEFAULT_CLOSE50_POLICY = (
    "outputs/summary_tables/099_close50_source_count_replicate_synthesis/"
    "data/close50_source_count_replicate_synthesis_summary.json"
)
DEFAULT_CLOSE14_POLICY = (
    "outputs/summary_tables/102_close14_source3_three_seed_policy_synthesis/"
    "data/close14_source3_three_seed_policy_summary.json"
)
DEFAULT_ARCHIVE_POLICY = (
    "outputs/summary_tables/103_close_spacing_source_density_archive_map/"
    "data/close_spacing_source_density_archive_map_summary.json"
)


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _fraction(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def _archive_lookup(archive_rows: list[dict]) -> dict[tuple[str, int], dict]:
    lookup: dict[tuple[str, int], dict] = {}
    preferred_scopes = {
        ("close14", 3): "three_seed_source3_near_exact_context",
        ("close14", 4): "three_seed_source4_context",
        ("close14", 5): "three_seed_source5_noise_boundary_context",
        ("close50", 3): "matched_source_count_transition",
        ("close50", 4): "matched_source_count_transition",
        ("close50", 5): "matched_source_count_transition",
    }
    for row in archive_rows:
        key = (str(row.get("family")), safe_int(row.get("source_count")))
        if key not in preferred_scopes:
            continue
        if row.get("evidence_scope") == preferred_scopes[key]:
            lookup[key] = row
    return lookup


def _normalize_source_row(
    row: dict,
    *,
    family: str,
    spacing_mm: float,
    tx_rx_offset_mm: float,
    source_csv: Path,
    archive_row: dict | None,
) -> dict:
    source_count = safe_int(row.get("source_count"))
    row_count = safe_int(row.get("row_count"))
    strong_count = safe_int(row.get("strong_count"), 0)
    weak_count = safe_int(row.get("weak_count"), 0)
    truth_fraction = safe_float(row.get("truth_geometry_fraction"), 0.0)
    strong_fraction = safe_float(row.get("strong_fraction"), _fraction(strong_count, row_count))
    weak_fraction = _fraction(weak_count, row_count)
    archive_row = archive_row or {}
    return {
        "family": family,
        "spacing_mm": spacing_mm,
        "source_count": source_count,
        "tx_rx_offset_mm": tx_rx_offset_mm,
        "source_summary_csv": str(source_csv),
        "archive_evidence_scope": archive_row.get("evidence_scope", ""),
        "archive_evidence_role": archive_row.get("evidence_role", ""),
        "row_count": row_count,
        "seed_count": safe_int(row.get("seed_count")),
        "seed_values": row.get("seed_values", ""),
        "truth_geometry_count": safe_int(row.get("truth_geometry_count")),
        "truth_geometry_fraction": truth_fraction,
        "strong_count": strong_count,
        "strong_fraction": strong_fraction,
        "weak_count": weak_count,
        "weak_fraction": weak_fraction,
        "selected_wrong_x_count": safe_int(row.get("selected_wrong_x_count")),
        "min_radius_margin_abs": safe_float(row.get("min_radius_margin_abs")),
        "max_x_abs_error_mm": safe_float(row.get("max_x_abs_error_mm")),
        "max_radius_abs_error_mm": safe_float(row.get("max_radius_abs_error_mm")),
        "max_ambiguity_x_width_mm": safe_float(row.get("max_ambiguity_x_width_mm")),
        "three_seed_exact": boolish(archive_row.get("three_seed_exact")),
        "three_seed_near_exact_context": boolish(archive_row.get("three_seed_near_exact_context")),
        "replicated_failure": boolish(archive_row.get("replicated_failure")),
    }


def load_source_rows(
    close50_source_summary: Path,
    close14_source_summary: Path,
    archive_group_summary: Path,
) -> list[dict]:
    archive_rows = read_csv_rows(archive_group_summary)
    archive_by_key = _archive_lookup(archive_rows)
    rows = []
    for row in read_csv_rows(close50_source_summary):
        source_count = safe_int(row.get("source_count"))
        rows.append(
            _normalize_source_row(
                row,
                family="close50",
                spacing_mm=50.0,
                tx_rx_offset_mm=40.0,
                source_csv=close50_source_summary,
                archive_row=archive_by_key.get(("close50", source_count)),
            )
        )
    for row in read_csv_rows(close14_source_summary):
        source_count = safe_int(row.get("source_count"))
        rows.append(
            _normalize_source_row(
                row,
                family="close14",
                spacing_mm=14.0,
                tx_rx_offset_mm=45.0,
                source_csv=close14_source_summary,
                archive_row=archive_by_key.get(("close14", source_count)),
            )
        )
    return sorted(rows, key=lambda item: (safe_float(item["spacing_mm"]), safe_int(item["source_count"])))


def _row_by_key(rows: list[dict]) -> dict[tuple[str, int], dict]:
    return {(str(row["family"]), safe_int(row["source_count"])): row for row in rows}


def _metric_delta(after: dict, before: dict, metric: str) -> float:
    return safe_float(after.get(metric)) - safe_float(before.get(metric))


def build_comparison_rows(source_rows: list[dict]) -> list[dict]:
    by_key = _row_by_key(source_rows)

    def compare(label: str, kind: str, left_key: tuple[str, int], right_key: tuple[str, int]) -> dict:
        left = by_key[left_key]
        right = by_key[right_key]
        return {
            "comparison_label": label,
            "comparison_kind": kind,
            "left_family": left["family"],
            "left_source_count": left["source_count"],
            "right_family": right["family"],
            "right_source_count": right["source_count"],
            "left_truth_geometry_fraction": left["truth_geometry_fraction"],
            "right_truth_geometry_fraction": right["truth_geometry_fraction"],
            "truth_geometry_fraction_delta": _metric_delta(right, left, "truth_geometry_fraction"),
            "left_strong_fraction": left["strong_fraction"],
            "right_strong_fraction": right["strong_fraction"],
            "strong_fraction_delta": _metric_delta(right, left, "strong_fraction"),
            "left_weak_fraction": left["weak_fraction"],
            "right_weak_fraction": right["weak_fraction"],
            "weak_fraction_delta": _metric_delta(right, left, "weak_fraction"),
            "left_max_x_abs_error_mm": left["max_x_abs_error_mm"],
            "right_max_x_abs_error_mm": right["max_x_abs_error_mm"],
            "max_x_abs_error_delta_mm": _metric_delta(right, left, "max_x_abs_error_mm"),
            "left_replicated_failure": left["replicated_failure"],
            "right_replicated_failure": right["replicated_failure"],
            "left_near_exact": left["three_seed_near_exact_context"],
            "right_near_exact": right["three_seed_near_exact_context"],
        }

    return [
        compare("close50_source3_to_source4", "within_family_source_density", ("close50", 3), ("close50", 4)),
        compare("close50_source4_to_source5", "within_family_source_density", ("close50", 4), ("close50", 5)),
        compare("close14_source3_to_source4", "within_family_source_density", ("close14", 3), ("close14", 4)),
        compare("close14_source4_to_source5", "within_family_source_density", ("close14", 4), ("close14", 5)),
        compare("source3_close50_to_close14", "cross_spacing_source3_contrast", ("close50", 3), ("close14", 3)),
        compare("source4_close50_to_close14", "cross_spacing_source4_contrast", ("close50", 4), ("close14", 4)),
    ]


def synthesize_policy(
    source_rows: list[dict],
    comparison_rows: list[dict],
    close50_policy: dict,
    close14_policy: dict,
    archive_policy: dict,
) -> dict:
    by_key = _row_by_key(source_rows)
    close50_s3 = by_key[("close50", 3)]
    close50_s4 = by_key[("close50", 4)]
    close50_s5 = by_key[("close50", 5)]
    close14_s3 = by_key[("close14", 3)]
    close14_s4 = by_key[("close14", 4)]
    close14_s5 = by_key[("close14", 5)]

    close50_source3_failure = (
        safe_int(close50_s3["seed_count"]) >= 3
        and math.isclose(safe_float(close50_s3["truth_geometry_fraction"]), 0.0)
        and math.isclose(safe_float(close50_s3["weak_fraction"]), 1.0)
        and boolish(close50_s3["replicated_failure"])
    )
    close50_source4_5_exact = (
        math.isclose(safe_float(close50_s4["truth_geometry_fraction"]), 1.0)
        and math.isclose(safe_float(close50_s5["truth_geometry_fraction"]), 1.0)
    )
    close14_source3_near_exact = (
        safe_int(close14_s3["seed_count"]) >= 3
        and safe_float(close14_s3["truth_geometry_fraction"]) >= (5.0 / 6.0)
        and math.isclose(safe_float(close14_s3["strong_fraction"]), 1.0)
        and safe_float(close14_s3["max_x_abs_error_mm"]) <= 1.0
        and math.isclose(safe_float(close14_s3["max_radius_abs_error_mm"]), 0.0)
        and not boolish(close14_s3["replicated_failure"])
    )
    close14_source4_5_exact = (
        math.isclose(safe_float(close14_s4["truth_geometry_fraction"]), 1.0)
        and math.isclose(safe_float(close14_s5["truth_geometry_fraction"]), 1.0)
    )
    source3_spacing_dependent_contrast = close50_source3_failure and close14_source3_near_exact
    close50_source4_rescue = close50_source3_failure and math.isclose(
        safe_float(close50_s4["truth_geometry_fraction"]), 1.0
    )
    close14_source4_incremental_cleanup = (
        close14_source3_near_exact
        and math.isclose(safe_float(close14_s4["truth_geometry_fraction"]), 1.0)
        and safe_float(close14_s3["max_x_abs_error_mm"]) > safe_float(close14_s4["max_x_abs_error_mm"])
    )
    universal_source3_failure_supported = close50_source3_failure and boolish(close14_s3["replicated_failure"])
    manuscript_table_ready = (
        source3_spacing_dependent_contrast
        and close50_source4_5_exact
        and close14_source4_5_exact
        and boolish(close50_policy.get("source_count_transition_supported"))
        and boolish(archive_policy.get("source_count_transition_supported_for_close50_txrx40"))
        and boolish(close14_policy.get("source3_near_exact_three_seed_context"))
    )
    return {
        "policy_label": "close_spacing_source_density_cross_spacing_synthesis",
        "source_row_count": len(source_rows),
        "comparison_row_count": len(comparison_rows),
        "families": "close14,close50",
        "source_counts": "3,4,5",
        "matched_seed_values": "13,21,34",
        "close50_source3_replicated_failure": close50_source3_failure,
        "close50_source4_5_exact_recovery": close50_source4_5_exact,
        "close14_source3_near_exact_context": close14_source3_near_exact,
        "close14_source4_5_exact_recovery": close14_source4_5_exact,
        "source3_spacing_dependent_contrast": source3_spacing_dependent_contrast,
        "close50_source4_rescue_supported": close50_source4_rescue,
        "close14_source4_incremental_cleanup_supported": close14_source4_incremental_cleanup,
        "universal_source3_failure_supported": universal_source3_failure_supported,
        "manuscript_table_ready": manuscript_table_ready,
        "cross_spacing_generalization_ready": False,
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc_handoff": False,
        "gpu_priority": "none",
        "recommended_next_local_mode": "field_controls_or_cpu_same_case_baseline_contract",
        "claim_boundary": (
            "The close50 Tx/Rx40 source-density transition is real in the saved three-seed evidence, "
            "but it is not a universal three-source failure rule: close14 Tx/Rx45 source3 is strong, "
            "radius-exact, and near-exact across the same seeds, with source4 only cleaning up a 1 mm "
            "adjacent-x branch. Frame the manuscript claim as an acquisition/spacing interaction."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "manuscript_source_density_table",
            "ready": summary["manuscript_table_ready"],
            "allowed_use": "synthetic 2D source-density contrast table/figure",
            "blocked_use": "unqualified universal source-count claim",
            "evidence": "close50 source3 failure contrasts with close14 source3 near-exact context",
        },
        {
            "gate_key": "cross_spacing_generalization",
            "ready": summary["cross_spacing_generalization_ready"],
            "allowed_use": "none",
            "blocked_use": "generalize source3 failure to all close spacings",
            "evidence": "close14 source3 does not replicate the close50 source3 failure",
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "broad local GPU source-density sweep",
            "evidence": "saved three-seed evidence already resolves this claim boundary",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI launch",
            "evidence": "this synthesis compares coordinate-confidence summaries only",
        },
        {
            "gate_key": "field_fwi_or_3d_hpc",
            "ready": summary["ready_for_field_fwi"] or summary["ready_for_3d_hpc_handoff"],
            "allowed_use": "none",
            "blocked_use": "field FWI, 3D, or HPC handoff",
            "evidence": "synthetic 2D source-density evidence; field and 3D scopes remain separate",
        },
    ]


def plot_synthesis(source_rows: list[dict], summary: dict, save_path: Path) -> str:
    families = ["close50", "close14"]
    colors = {"close50": "#e15759", "close14": "#4e79a7"}
    source_counts = [3, 4, 5]
    by_key = _row_by_key(source_rows)
    x = np.arange(len(source_counts))

    fig, axes = plt.subplots(1, 2, figsize=(13.8, 5.2), constrained_layout=True)
    width = 0.34
    for offset, family in [(-width / 2, "close50"), (width / 2, "close14")]:
        truth_values = [safe_float(by_key[(family, source)]["truth_geometry_fraction"]) for source in source_counts]
        strong_values = [safe_float(by_key[(family, source)]["strong_fraction"]) for source in source_counts]
        axes[0].bar(
            x + offset,
            truth_values,
            width=width,
            color=colors[family],
            edgecolor="#333333",
            linewidth=0.4,
            label=f"{family} truth",
        )
        axes[0].plot(
            x + offset,
            strong_values,
            marker="o",
            linestyle="none",
            color="#222222",
            markersize=4.5,
            label=f"{family} strong" if family == "close50" else None,
        )
    axes[0].set_xticks(x, [f"{source} sources" for source in source_counts])
    axes[0].set_ylim(0.0, 1.08)
    axes[0].set_ylabel("fraction")
    axes[0].set_title("Truth recovery by spacing and source count")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(loc="lower right", fontsize=8)

    for family in families:
        x_errors = [safe_float(by_key[(family, source)]["max_x_abs_error_mm"]) for source in source_counts]
        axes[1].plot(
            source_counts,
            x_errors,
            marker="o",
            linewidth=2.0,
            color=colors[family],
            label=family,
        )
    axes[1].set_xticks(source_counts)
    axes[1].set_xlabel("source count")
    axes[1].set_ylabel("max selected x error (mm)")
    axes[1].set_title("Residual branch error")
    axes[1].grid(color="#dddddd", linewidth=0.6)
    axes[1].legend(loc="upper right", fontsize=8)
    axes[1].text(
        0.03,
        0.95,
        f"close50 source3 failure: {summary['close50_source3_replicated_failure']}\n"
        f"close14 source3 near-exact: {summary['close14_source3_near_exact_context']}\n"
        f"universal source3 failure: {summary['universal_source3_failure_supported']}\n"
        f"GPU priority: {summary['gpu_priority']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Close-Spacing Source-Density Cross-Spacing Synthesis", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `close_spacing_source_density_cross_spacing_synthesis.png`",
                "",
                "This figure compares saved three-seed close50 Tx/Rx40 and close14 Tx/Rx45",
                "source-density summaries for target2 close-spacing evidence.",
                "",
                f"Close50 source3 replicated failure: `{summary['close50_source3_replicated_failure']}`.",
                f"Close50 source4/5 exact recovery: `{summary['close50_source4_5_exact_recovery']}`.",
                f"Close14 source3 near-exact context: `{summary['close14_source3_near_exact_context']}`.",
                f"Close14 source4/5 exact recovery: `{summary['close14_source4_5_exact_recovery']}`.",
                f"Universal source3 failure supported: `{summary['universal_source3_failure_supported']}`.",
                f"Manuscript table ready: `{summary['manuscript_table_ready']}`.",
                "",
                "Scope boundary:",
                "",
                "This is a CPU-only synthesis of saved synthetic 2D coordinate-confidence",
                "summaries. It does not launch FDTD/FWI, detector-seeded FWI, field FWI,",
                "3D/HPC jobs, broad GPU sweeps, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--close50-source-summary", default=DEFAULT_CLOSE50_SOURCE_SUMMARY)
    parser.add_argument("--close14-source-summary", default=DEFAULT_CLOSE14_SOURCE_SUMMARY)
    parser.add_argument("--archive-group-summary", default=DEFAULT_ARCHIVE_GROUP_SUMMARY)
    parser.add_argument("--close50-policy", default=DEFAULT_CLOSE50_POLICY)
    parser.add_argument("--close14-policy", default=DEFAULT_CLOSE14_POLICY)
    parser.add_argument("--archive-policy", default=DEFAULT_ARCHIVE_POLICY)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--run-name", default="close_spacing_source_density_cross_spacing_synthesis")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_rows = load_source_rows(
        Path(args.close50_source_summary),
        Path(args.close14_source_summary),
        Path(args.archive_group_summary),
    )
    comparison_rows = build_comparison_rows(source_rows)
    summary = synthesize_policy(
        source_rows,
        comparison_rows,
        read_json(Path(args.close50_policy)),
        read_json(Path(args.close14_policy)),
        read_json(Path(args.archive_policy)),
    )
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    source_csv = data_dir / "close_spacing_source_density_cross_spacing_source_rows.csv"
    comparison_csv = data_dir / "close_spacing_source_density_cross_spacing_comparisons.csv"
    gates_csv = data_dir / "close_spacing_source_density_cross_spacing_gates.csv"
    summary_json = data_dir / "close_spacing_source_density_cross_spacing_summary.json"
    figure_path = figures_dir / "close_spacing_source_density_cross_spacing_synthesis.png"
    validation_csv = data_dir / "figure_validation.csv"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(source_csv, [json_safe(row) for row in source_rows])
    write_csv(comparison_csv, [json_safe(row) for row in comparison_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_synthesis(source_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary)

    summary["paths"] = {
        "source_rows_csv": str(source_csv),
        "comparison_csv": str(comparison_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
        "figure_notes": str(figure_notes),
        "close50_source_summary": args.close50_source_summary,
        "close14_source_summary": args.close14_source_summary,
        "archive_group_summary": args.archive_group_summary,
        "close50_policy": args.close50_policy,
        "close14_policy": args.close14_policy,
        "archive_policy": args.archive_policy,
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "close_spacing_source_density_cross_spacing_synthesis",
        {
            "summary_json": str(summary_json),
            "source_rows_csv": str(source_csv),
            "comparison_csv": str(comparison_csv),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

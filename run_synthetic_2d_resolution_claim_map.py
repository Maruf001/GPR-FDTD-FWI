#!/usr/bin/env python3
"""Build a paper-facing synthetic 2D resolution-claim map from policy outputs."""

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
from run_gssi_field_corrected_profile_stack import safe_float  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_EXPERIMENT_ROOT = "outputs/experiments"
DEFAULT_PHYSICAL_SUMMARY = (
    "1256_coordinate_physical_spacing_policy_synthesis_after_close10/data/"
    "coordinate_physical_spacing_policy_summary.json"
)
DEFAULT_PHYSICAL_GROUPS = (
    "1256_coordinate_physical_spacing_policy_synthesis_after_close10/data/"
    "coordinate_physical_spacing_policy_groups.csv"
)
DEFAULT_CLAIM_TIER_SUMMARY = "1288_synthetic_claim_tier_table/data/synthetic_claim_tier_summary.json"
DEFAULT_CLAIM_TIER_ROWS = "1288_synthetic_claim_tier_table/data/synthetic_claim_tier_rows.csv"
DEFAULT_CLOSE14_SUMMARY = (
    "1297_synthetic_target2_close14_three_seed_probe_synthesis/data/"
    "target2_close14_three_seed_probe_summary.json"
)
DEFAULT_CLOSE50_SUMMARY = (
    "1303_close50_linear29p5_three_seed_frequency_policy/data/"
    "close50_linear_receiver_policy_summary.json"
)
DEFAULT_CLAIM_BOUNDARY_SUMMARY = (
    "1305_synthetic_2d_publication_claim_boundary_refresh_post_close50_seed_frequency/data/"
    "synthetic_2d_publication_claim_boundary_refresh_summary.json"
)
DEFAULT_NEXT_MATRIX_SUMMARY = (
    "1306_synthetic_2d_next_question_matrix_post_close50_claim_refresh/data/"
    "synthetic_2d_next_question_matrix_summary.json"
)


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def fraction(numerator: float, denominator: float) -> float:
    if not math.isfinite(denominator) or denominator <= 0:
        return math.nan
    return float(numerator) / float(denominator)


def min_clean_spacing(group_rows: list[dict], *, physical: bool) -> float:
    values = [
        safe_float(row.get("close_spacing_mm"))
        for row in group_rows
        if row.get("policy_label") == "clean_replicated"
        and truthy(row.get("is_physical_nonoverlap")) is physical
        and math.isfinite(safe_float(row.get("close_spacing_mm")))
    ]
    return min(values) if values else math.nan


def resolution_claim_rows(
    physical_summary: dict,
    physical_group_rows: list[dict],
    claim_tier_summary: dict,
    claim_tier_rows: list[dict],
    close14_summary: dict,
    close50_summary: dict,
    claim_boundary_summary: dict,
    next_matrix_summary: dict,
) -> list[dict]:
    rows: list[dict] = []
    clean_nonoverlap_min = min_clean_spacing(physical_group_rows, physical=True)
    clean_overlap_min = min_clean_spacing(physical_group_rows, physical=False)
    group_count = safe_float(physical_summary.get("group_count"))
    clean_nonoverlap_count = safe_float(physical_summary.get("clean_nonoverlap_group_count"))
    rows.append(
        {
            "map_key": "physical_nonoverlap_guardrail",
            "scope": "target1_target2_center_spacing",
            "claim_status": "allowed_physical_spacing_guardrail",
            "primary_metric_label": "closest_clean_nonoverlap_center_spacing_mm",
            "primary_metric_value": clean_nonoverlap_min,
            "support_count": clean_nonoverlap_count,
            "total_count": group_count,
            "support_fraction": fraction(clean_nonoverlap_count, group_count),
            "allowed_claim": (
                "For the current 6 mm + 8 mm radius target1/target2 pair, "
                "close14 is the tangent non-overlap center-spacing guardrail "
                "with clean replicated evidence in existing Tx/Rx branches."
            ),
            "not_allowed": (
                "Do not report close10 or close12 as physical non-overlap "
                "resolution; they are overlapping-cylinder stress tests."
            ),
            "source_policy": physical_summary.get("decision", ""),
        }
    )
    rows.append(
        {
            "map_key": "overlap_stress_test_boundary",
            "scope": "algorithmic_overlap_stress",
            "claim_status": "blocked_for_physical_spacing",
            "primary_metric_label": "closest_clean_overlap_stress_spacing_mm",
            "primary_metric_value": clean_overlap_min,
            "support_count": safe_float(physical_summary.get("clean_overlap_stress_group_count")),
            "total_count": group_count,
            "support_fraction": fraction(
                safe_float(physical_summary.get("clean_overlap_stress_group_count")),
                group_count,
            ),
            "allowed_claim": "Use close10 and close12 only as algorithmic overlap stress tests.",
            "not_allowed": "Do not convert overlap-stress recovery into a physical rebar-spacing claim.",
            "source_policy": physical_summary.get("decision", ""),
        }
    )
    for row in claim_tier_rows:
        target = str(row.get("target_index", ""))
        exact = safe_float(row.get("exact_strong_row_count"))
        objective_unique = safe_float(row.get("objective_unique_row_count"))
        rows.append(
            {
                "map_key": f"target{target}_claim_tier",
                "scope": f"target{target}_archive_claim_tier",
                "claim_status": row.get("claim_tier_label", ""),
                "primary_metric_label": "objective_unique_fraction",
                "primary_metric_value": safe_float(row.get("objective_unique_fraction")),
                "support_count": objective_unique,
                "total_count": exact,
                "support_fraction": fraction(objective_unique, exact),
                "allowed_claim": row.get("recommended_wording", ""),
                "not_allowed": (
                    "Do not collapse exact-strong rows into objective-unique "
                    "wording without checking competitor near ties."
                ),
                "source_policy": claim_tier_summary.get("policy_label", ""),
            }
        )
    rows.append(
        {
            "map_key": "target2_close14_source5_txrx45_objective_limit",
            "scope": "target2_close14_objective_uniqueness",
            "claim_status": "truth_strong_but_objective_near_tie_replicated",
            "primary_metric_label": "near_tie_count_at_scale_0p5",
            "primary_metric_value": safe_float(close14_summary.get("near_tie_count_at_scale_0p5")),
            "support_count": safe_float(close14_summary.get("strong_confidence_count")),
            "total_count": safe_float(close14_summary.get("row_count")),
            "support_fraction": fraction(
                safe_float(close14_summary.get("strong_confidence_count")),
                safe_float(close14_summary.get("row_count")),
            ),
            "allowed_claim": (
                "Truth is selected with strong radius confidence in all close14 "
                "source5/TxRx45 seed/case rows."
            ),
            "not_allowed": (
                "Do not call this branch objective-unique or clean lateral "
                "resolution because the +1 mm x competitor remains inside the "
                "0.5x gate in every row."
            ),
            "source_policy": close14_summary.get("policy_label", ""),
        }
    )
    rows.append(
        {
            "map_key": "target2_close50_linear29p5_seed_frequency",
            "scope": "target2_close50_linear_receiver",
            "claim_status": "exact_strong_not_clean_replicated",
            "primary_metric_label": "strict_clean_seed_fraction",
            "primary_metric_value": fraction(
                safe_float(close50_summary.get("strict_clean_seed_count")),
                safe_float(close50_summary.get("seed_count")),
            ),
            "support_count": safe_float(close50_summary.get("strict_clean_seed_count")),
            "total_count": safe_float(close50_summary.get("seed_count")),
            "support_fraction": fraction(
                safe_float(close50_summary.get("strict_clean_seed_count")),
                safe_float(close50_summary.get("seed_count")),
            ),
            "allowed_claim": (
                "The 29.5 mm linear receiver branch is exact/strong across "
                "three seeds, with strict-clean support in seed21 and seed34."
            ),
            "not_allowed": (
                "Do not promote 29.5 mm to a clean replicated sub-30 mm "
                "threshold because seed13 remains x-ambiguous."
            ),
            "source_policy": close50_summary.get("policy_label", ""),
        }
    )
    rows.append(
        {
            "map_key": "current_synthetic_gpu_queue",
            "scope": "local_2d_next_question_matrix",
            "claim_status": "no_current_gpu_candidate",
            "primary_metric_label": "conditional_gpu_candidate_count",
            "primary_metric_value": safe_float(next_matrix_summary.get("conditional_gpu_candidate_count")),
            "support_count": 0.0,
            "total_count": safe_float(next_matrix_summary.get("candidate_count")),
            "support_fraction": 0.0,
            "allowed_claim": (
                "The refreshed claim-boundary table is current and no "
                "immediate or conditional local synthetic GPU candidate remains."
            ),
            "not_allowed": (
                "Do not launch broad synthetic GPU sweeps without a new "
                "objective, geometry, or acquisition hypothesis."
            ),
            "source_policy": (
                f"{claim_boundary_summary.get('policy_label', '')}; "
                f"{next_matrix_summary.get('policy_label', '')}"
            ),
        }
    )
    return rows


def summarize_map(rows: list[dict], close14_summary: dict, close50_summary: dict, next_matrix_summary: dict) -> dict:
    by_key = {row["map_key"]: row for row in rows}
    blocked = [row for row in rows if "blocked" in str(row.get("claim_status", ""))]
    return {
        "policy_label": "synthetic_2d_resolution_claim_map_close14_close50_current_cpu_no_gpu",
        "row_count": len(rows),
        "blocked_physical_claim_row_count": len(blocked),
        "physical_nonoverlap_guardrail_mm": safe_float(
            by_key["physical_nonoverlap_guardrail"]["primary_metric_value"]
        ),
        "overlap_stress_min_clean_spacing_mm": safe_float(
            by_key["overlap_stress_test_boundary"]["primary_metric_value"]
        ),
        "target2_close14_truth_strong_rows": safe_float(close14_summary.get("strong_confidence_count")),
        "target2_close14_near_tie_rows_at_0p5": safe_float(
            close14_summary.get("near_tie_count_at_scale_0p5")
        ),
        "target2_close50_seed_count": safe_float(close50_summary.get("seed_count")),
        "target2_close50_strict_clean_seed_count": safe_float(
            close50_summary.get("strict_clean_seed_count")
        ),
        "target2_close50_ambiguous_seed_values": close50_summary.get("ambiguous_seed_values", ""),
        "conditional_gpu_candidate_count": safe_float(
            next_matrix_summary.get("conditional_gpu_candidate_count")
        ),
        "gpu_priority": "none_now",
        "ready_for_manuscript_resolution_table": True,
        "decision": (
            "Use this resolution-claim map to separate physical spacing "
            "guardrails, archive claim tiers, objective-uniqueness limits, and "
            "seed-frequency caveats. The current evidence supports a cautious "
            "paper-facing table, not a universal rebar resolution law and not "
            "a new broad GPU sweep."
        ),
    }


def plot_map(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["map_key"].replace("_", "\n") for row in rows]
    values = np.asarray([safe_float(row.get("support_fraction"), 0.0) for row in rows], dtype=np.float64)
    values = np.nan_to_num(values, nan=0.0)
    color_map = {
        "allowed_physical_spacing_guardrail": "#4c78a8",
        "blocked_for_physical_spacing": "#b33a3a",
        "all_objective_unique": "#2f9d55",
        "geometry_clean_but_objective_near_ties": "#d99a19",
        "geometry_and_objective_near_ties": "#f58518",
        "truth_strong_but_objective_near_tie_replicated": "#7f3c8d",
        "exact_strong_not_clean_replicated": "#9467bd",
        "no_current_gpu_candidate": "#6b6b6b",
    }
    colors = [color_map.get(str(row.get("claim_status")), "#999999") for row in rows]
    y = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(13.5, 7.5), constrained_layout=True)
    ax.barh(y, values, color=colors)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0.0, 1.05)
    ax.set_xlabel("support fraction for stated claim")
    ax.set_title("Synthetic 2D resolution-claim map")
    ax.grid(axis="x", color="#dddddd", linewidth=0.6)
    for idx, row in enumerate(rows):
        ax.text(
            min(values[idx] + 0.025, 1.0),
            idx,
            f"{safe_float(row.get('support_count')):.0f}/{safe_float(row.get('total_count')):.0f}",
            va="center",
            ha="left" if values[idx] < 0.92 else "right",
            fontsize=8.5,
        )
    ax.text(
        0.01,
        0.02,
        (
            f"physical guardrail={summary['physical_nonoverlap_guardrail_mm']:.0f} mm | "
            f"close50 ambiguous seed={summary['target2_close50_ambiguous_seed_values']} | "
            f"gpu={summary['gpu_priority']}"
        ),
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
    )
    fig.suptitle(
        "Resolution claims are acquisition/objective-specific, not universal",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default=DEFAULT_EXPERIMENT_ROOT)
    parser.add_argument("--physical-summary", default=DEFAULT_PHYSICAL_SUMMARY)
    parser.add_argument("--physical-groups", default=DEFAULT_PHYSICAL_GROUPS)
    parser.add_argument("--claim-tier-summary", default=DEFAULT_CLAIM_TIER_SUMMARY)
    parser.add_argument("--claim-tier-rows", default=DEFAULT_CLAIM_TIER_ROWS)
    parser.add_argument("--close14-summary", default=DEFAULT_CLOSE14_SUMMARY)
    parser.add_argument("--close50-summary", default=DEFAULT_CLOSE50_SUMMARY)
    parser.add_argument("--claim-boundary-summary", default=DEFAULT_CLAIM_BOUNDARY_SUMMARY)
    parser.add_argument("--next-matrix-summary", default=DEFAULT_NEXT_MATRIX_SUMMARY)
    parser.add_argument("--run-name", default="synthetic_2d_resolution_claim_map")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    root = Path(args.experiment_root)
    physical_summary = read_json(root / args.physical_summary)
    physical_group_rows = read_csv_rows(root / args.physical_groups)
    claim_tier_summary = read_json(root / args.claim_tier_summary)
    claim_tier_rows = read_csv_rows(root / args.claim_tier_rows)
    close14_summary = read_json(root / args.close14_summary)
    close50_summary = read_json(root / args.close50_summary)
    claim_boundary_summary = read_json(root / args.claim_boundary_summary)
    next_matrix_summary = read_json(root / args.next_matrix_summary)

    rows = resolution_claim_rows(
        physical_summary,
        physical_group_rows,
        claim_tier_summary,
        claim_tier_rows,
        close14_summary,
        close50_summary,
        claim_boundary_summary,
        next_matrix_summary,
    )
    summary = summarize_map(rows, close14_summary, close50_summary, next_matrix_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "synthetic_2d_resolution_claim_map_rows.csv"
    summary_json = data_dir / "synthetic_2d_resolution_claim_map_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_map(rows, summary, figures_dir / "synthetic_2d_resolution_claim_map.png"))

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "inputs": {
            "physical_summary": str(root / args.physical_summary),
            "physical_groups": str(root / args.physical_groups),
            "claim_tier_summary": str(root / args.claim_tier_summary),
            "claim_tier_rows": str(root / args.claim_tier_rows),
            "close14_summary": str(root / args.close14_summary),
            "close50_summary": str(root / args.close50_summary),
            "claim_boundary_summary": str(root / args.claim_boundary_summary),
            "next_matrix_summary": str(root / args.next_matrix_summary),
        },
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
        "synthetic_2d_resolution_claim_map",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

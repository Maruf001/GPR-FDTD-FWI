#!/usr/bin/env python3
"""Refresh synthetic 2D publication claim boundaries after reporting-tier audits."""

from __future__ import annotations

import argparse
import csv
import json
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
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_BASE_CLAIMS = (
    "outputs/experiments/1278_synthetic_2d_publication_figure_bundle/data/"
    "synthetic_2d_publication_claim_boundaries.csv"
)
DEFAULT_TIER_SUMMARY = (
    "outputs/experiments/1285_cross_target_objective_reporting_tiers/data/"
    "cross_target_objective_reporting_tiers_summary.json"
)
DEFAULT_TIER_ROWS = (
    "outputs/experiments/1285_cross_target_objective_reporting_tiers/data/"
    "cross_target_objective_reporting_tier_summary_rows.csv"
)
DEFAULT_CLOSE14_PROBE_SUMMARY = (
    "outputs/experiments/1297_synthetic_target2_close14_three_seed_probe_synthesis/data/"
    "target2_close14_three_seed_probe_summary.json"
)
DEFAULT_CLOSE50_POLICY_SUMMARY = (
    "outputs/experiments/1303_close50_linear29p5_three_seed_frequency_policy/data/"
    "close50_linear_receiver_policy_summary.json"
)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_optional_json(path: Path) -> dict:
    if not Path(path).exists():
        return {}
    return read_json(path)


def refreshed_claim_rows(
    base_rows: list[dict],
    tier_summary: dict,
    target_rows: list[dict],
    close14_probe_summary: dict | None = None,
    close50_policy_summary: dict | None = None,
) -> list[dict]:
    retained = [
        row for row in base_rows
        if row.get("claim_area") not in {"gpu_next_step"}
    ]
    target2 = next((row for row in target_rows if str(row.get("target_index")) == "2"), {})
    zero_targets = str(tier_summary.get("zero_width_objective_near_tie_targets", ""))
    geometry_targets = str(tier_summary.get("geometry_ambiguous_targets", ""))
    close14_probe_summary = close14_probe_summary or {}
    close50_policy_summary = close50_policy_summary or {}
    added_rows = [
        {
            "claim_area": "reporting_tiers",
            "allowed_claim": (
                "Report exact-strong, strict location-clean, zero-width objective near-tie, "
                "and geometry-ambiguous near-tie as separate tiers."
            ),
            "not_allowed": (
                "Do not collapse exact-strong rows into paper-clean location claims without "
                "checking geometry ambiguity widths."
            ),
        },
        {
            "claim_area": "objective_uniqueness",
            "allowed_claim": (
                f"Zero-width objective near-ties occur for targets {zero_targets}; they limit "
                "objective-uniqueness wording but not location-clean geometry wording."
            ),
            "not_allowed": (
                "Do not describe zero-width near-tie rows as uniquely isolated objective basins."
            ),
        },
        {
            "claim_area": "target_specificity",
            "allowed_claim": (
                f"Geometry ambiguity in exact-strong archive rows is target-specific to target(s) "
                f"{geometry_targets}; target2 strict location-clean fraction is "
                f"{float(target2.get('strict_location_clean_fraction', 0.0)):.6f}."
            ),
            "not_allowed": "Do not imply target0, target1, and target2 share the same ambiguity profile.",
        },
    ]
    if close14_probe_summary:
        added_rows.append(
            {
                "claim_area": "target2_close14_objective_limit",
                "allowed_claim": (
                    "For target2 close14 source5 / Tx/Rx=45 mm, the three-seed "
                    f"probe selected truth with strong radius confidence in "
                    f"{close14_probe_summary['strong_confidence_count']} / "
                    f"{close14_probe_summary['row_count']} rows, but the +1 mm "
                    f"x competitor remained inside the 0.5x ambiguity gate in "
                    f"{close14_probe_summary['near_tie_count_at_scale_0p5']} / "
                    f"{close14_probe_summary['row_count']} rows."
                ),
                "not_allowed": (
                    "Do not describe this branch as clean lateral resolution or "
                    "as an objective-unique inversion result."
                ),
            }
        )
    if close50_policy_summary:
        added_rows.append(
            {
                "claim_area": "target2_close50_linear29p5_seed_frequency",
                "allowed_claim": (
                    "For target2 close50 linear receiver Tx/Rx=29.5 mm, the "
                    f"three-seed policy selected the true geometry with strong "
                    f"radius confidence in {close50_policy_summary['strong_confidence_row_count']} / "
                    f"{close50_policy_summary['confidence_row_count']} rows. "
                    f"Strict-clean support is {close50_policy_summary['strict_clean_seed_count']} / "
                    f"{close50_policy_summary['seed_count']} seeds; "
                    f"{close50_policy_summary['ambiguous_seed_values']} remains an x-ambiguity caveat."
                ),
                "not_allowed": (
                    "Do not promote 29.5 mm to a clean replicated sub-30 mm "
                    "threshold; keep the nearest-sampled 30 mm result as the "
                    "paper-safe clean threshold."
                ),
            }
        )
    if close14_probe_summary:
        gpu_allowed = (
            "No immediate synthetic GPU-priority run remains for the completed "
            "target2 close14 source5 / Tx/Rx=45 mm probe; future GPU work needs "
            "a different objective, geometry, or acquisition question."
        )
    elif close50_policy_summary:
        gpu_allowed = (
            "No immediate synthetic GPU-priority run remains for the completed "
            "close50 linear 29.5 mm seed-frequency branch; future GPU work needs "
            "a different objective, geometry, or acquisition question."
        )
    else:
        gpu_allowed = (
            "Current synthetic policy still has no immediate GPU-priority run; CPU-side "
            "reporting-tier and objective-margin audits should inform the next hypothesis."
        )
    if close14_probe_summary and close50_policy_summary:
        gpu_allowed = (
            "No immediate synthetic GPU-priority run remains for the completed "
            "close14 objective-limit branch or close50 linear 29.5 mm "
            "seed-frequency branch; future GPU work needs a different objective, "
            "geometry, or acquisition question."
        )
    added_rows.append(
        {
            "claim_area": "gpu_next_step",
            "allowed_claim": gpu_allowed,
            "not_allowed": (
                "Do not launch broad GPU sweeps without a new objective, geometry, or acquisition question."
            ),
        }
    )
    retained.extend(added_rows)
    return retained


def summarize_claims(
    rows: list[dict],
    tier_summary: dict,
    close14_probe_summary: dict | None = None,
    close50_policy_summary: dict | None = None,
) -> dict:
    close14_probe_summary = close14_probe_summary or {}
    close50_policy_summary = close50_policy_summary or {}
    if close14_probe_summary and close50_policy_summary:
        policy_label = "synthetic_2d_publication_claim_boundaries_close14_close50_limits_cpu_no_gpu"
        decision = (
            "Use the refreshed claim-boundary CSV when drafting synthetic 2D "
            "results. It includes the completed close14 objective-uniqueness "
            "limit and close50 linear 29.5 mm seed-frequency caveat, preserving "
            "the no-broad-GPU posture."
        )
    elif close14_probe_summary:
        policy_label = "synthetic_2d_publication_claim_boundaries_close14_limit_cpu_no_gpu"
        decision = (
            "Use the refreshed claim-boundary CSV when drafting synthetic 2D "
            "results. It now includes the completed close14 three-seed probe as "
            "a robust objective-uniqueness limit and preserves the no-broad-GPU posture."
        )
    elif close50_policy_summary:
        policy_label = "synthetic_2d_publication_claim_boundaries_close50_seed_frequency_cpu_no_gpu"
        decision = (
            "Use the refreshed claim-boundary CSV when drafting synthetic 2D "
            "results. It includes the completed close50 linear 29.5 mm "
            "seed-frequency caveat and preserves the no-broad-GPU posture."
        )
    else:
        policy_label = "synthetic_2d_publication_claim_boundaries_refreshed_cpu_no_gpu"
        decision = (
            "Use the refreshed claim-boundary CSV when drafting synthetic 2D "
            "results. It preserves the no-broad-GPU posture while adding "
            "reporting-tier precision."
        )
    return {
        "policy_label": policy_label,
        "claim_boundary_count": len(rows),
        "reporting_tier_policy": tier_summary.get("policy_label", ""),
        "geometry_ambiguous_targets": tier_summary.get("geometry_ambiguous_targets", ""),
        "zero_width_objective_near_tie_targets": tier_summary.get("zero_width_objective_near_tie_targets", ""),
        "close14_probe_included": bool(close14_probe_summary),
        "close14_probe_policy": close14_probe_summary.get("policy_label", ""),
        "close14_probe_near_tie_count_at_scale_0p5": close14_probe_summary.get("near_tie_count_at_scale_0p5", 0),
        "close50_seed_frequency_included": bool(close50_policy_summary),
        "close50_seed_frequency_policy": close50_policy_summary.get("policy_label", ""),
        "close50_seed_count": close50_policy_summary.get("seed_count", 0),
        "close50_ambiguous_seed_count": close50_policy_summary.get("ambiguous_seed_count", 0),
        "close50_ambiguous_seed_values": close50_policy_summary.get("ambiguous_seed_values", ""),
        "gpu_priority": "none",
        "ready_for_manuscript_claim_table": True,
        "decision": decision,
    }


def plot_claim_refresh(rows: list[dict], summary: dict, save_path: Path) -> str:
    areas = [row["claim_area"].replace("_", "\n") for row in rows]
    x = np.arange(len(rows))
    colors = ["#4c78a8" if row["claim_area"] in {"reporting_tiers", "objective_uniqueness", "target_specificity"} else "#6b6b6b" for row in rows]
    fig, ax = plt.subplots(figsize=(12.4, 4.8), constrained_layout=True)
    ax.bar(x, np.ones(len(rows)), color=colors)
    ax.set_xticks(x, areas)
    ax.set_yticks([])
    ax.set_title("Refreshed synthetic 2D manuscript claim-boundary areas")
    ax.text(
        0.01,
        0.92,
        f"claims={summary['claim_boundary_count']} | gpu={summary['gpu_priority']} | tier policy={summary['reporting_tier_policy']}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
    )
    fig.suptitle(
        f"Synthetic 2D claim-boundary refresh: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-claims-csv", default=DEFAULT_BASE_CLAIMS)
    parser.add_argument("--tier-summary-json", default=DEFAULT_TIER_SUMMARY)
    parser.add_argument("--tier-summary-rows-csv", default=DEFAULT_TIER_ROWS)
    parser.add_argument("--close14-probe-summary-json", default=DEFAULT_CLOSE14_PROBE_SUMMARY)
    parser.add_argument("--close50-policy-summary-json", default=DEFAULT_CLOSE50_POLICY_SUMMARY)
    parser.add_argument("--run-name", default="synthetic_2d_publication_claim_boundary_refresh")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    base_rows = read_csv_rows(Path(args.base_claims_csv))
    tier_summary = read_json(Path(args.tier_summary_json))
    target_rows = read_csv_rows(Path(args.tier_summary_rows_csv))
    close14_probe_summary = read_optional_json(Path(args.close14_probe_summary_json))
    close50_policy_summary = read_optional_json(Path(args.close50_policy_summary_json))
    rows = refreshed_claim_rows(
        base_rows,
        tier_summary,
        target_rows,
        close14_probe_summary,
        close50_policy_summary,
    )
    summary = summarize_claims(rows, tier_summary, close14_probe_summary, close50_policy_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    claims_csv = data_dir / "synthetic_2d_publication_claim_boundaries_refreshed.csv"
    summary_json = data_dir / "synthetic_2d_publication_claim_boundary_refresh_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_claim_refresh(rows, summary, figures_dir / "synthetic_2d_publication_claim_boundary_refresh.png"))

    write_csv(claims_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "base_claims_csv": args.base_claims_csv,
        "tier_summary_json": args.tier_summary_json,
        "tier_summary_rows_csv": args.tier_summary_rows_csv,
        "close14_probe_summary_json": args.close14_probe_summary_json,
        "close50_policy_summary_json": args.close50_policy_summary_json,
        **summary,
        "paths": {
            "claims_csv": str(claims_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "synthetic_2d_publication_claim_boundary_refresh",
        {
            "summary_json": str(summary_json),
            "claims_csv": str(claims_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

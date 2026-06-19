#!/usr/bin/env python3
"""Audit the legacy close50 270/280 branch against later threshold evidence."""

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

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import figure_stats  # noqa: E402
from run_gssi_field_profile_repeatability_policy import safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_RUN270_SUMMARY = (
    "outputs/experiments/270_coordinate_optimizer_close50_seed21_sources5_txrx40_objectives/"
    "data/multi_rebar_coordinate_optimizer_summary.json"
)
DEFAULT_RUN280_AGGREGATE = (
    "outputs/experiments/280_coordinate_confidence_close50_sources4_txrx40_seed_replicates/"
    "data/coordinate_confidence_aggregate.json"
)
DEFAULT_THRESHOLD_AGGREGATE = (
    "outputs/experiments/1222_coordinate_confidence_close50_sources4_txrx25_30_35_40_seed_replicates/"
    "data/coordinate_confidence_aggregate.json"
)
DEFAULT_MIDPOINT_SUMMARY = (
    "outputs/experiments/1265_coordinate_optimizer_close50_seed21_sources4_txrx27p5_objectives/"
    "data/multi_rebar_coordinate_optimizer_summary.json"
)
DEFAULT_MIDPOINT_SUMMARIES = (
    DEFAULT_MIDPOINT_SUMMARY,
    "outputs/experiments/1267_coordinate_optimizer_close50_seed21_sources4_txrx28p75_objectives/"
    "data/multi_rebar_coordinate_optimizer_summary.json",
    "outputs/experiments/1316_coordinate_optimizer_close50_seed13_sources4_txrx28p75_objectives/"
    "data/multi_rebar_coordinate_optimizer_summary.json",
)


def load_json(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_union_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        write_csv(path, [])
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    write_csv(path, [{key: row.get(key, "") for key in fieldnames} for row in rows])


def exact_match(value, truth, tol=1.0e-9) -> bool:
    numeric = safe_float(value)
    target = safe_float(truth)
    return math.isfinite(numeric) and math.isfinite(target) and abs(numeric - target) <= tol


def format_offset(value) -> str:
    numeric = safe_float(value)
    if not math.isfinite(numeric):
        return "nan"
    return f"{numeric:g}"


def summarize_optimizer_run(summary: dict, summary_path: str | Path) -> dict:
    rows = list(summary.get("confidence_rows", []))
    truth_x = list(summary.get("true_x_values_mm", []))
    truth_z = list(summary.get("true_z_values_mm", []))
    truth_radii = summary.get("truth_radius_values_mm") or [
        summary.get("truth_radius_mm") for _ in truth_x
    ]
    truth_geometry_count = 0
    target_indices = set()
    for row in rows:
        target_index = int(safe_float(row.get("step_target_index"), -1))
        target_indices.add(target_index)
        if (
            0 <= target_index < len(truth_x)
            and exact_match(row.get("best_x_mm"), truth_x[target_index])
            and exact_match(row.get("best_z_mm"), truth_z[target_index])
            and exact_match(row.get("best_radius_mm"), truth_radii[target_index])
        ):
            truth_geometry_count += 1
    margins = [safe_float(row.get("radius_margin_abs")) for row in rows]
    margins = [value for value in margins if math.isfinite(value)]
    return {
        "evidence": "run270_sources5_txrx40_seed21",
        "summary_path": str(summary_path),
        "run_name": summary.get("run_name"),
        "sources": safe_float(summary.get("sources")),
        "tx_rx_offset_mm": safe_float(summary.get("tx_rx_offset_mm")),
        "target_indices": ",".join(str(idx) for idx in sorted(target_indices)),
        "row_count": len(rows),
        "truth_geometry_count": truth_geometry_count,
        "truth_geometry_fraction": truth_geometry_count / len(rows) if rows else math.nan,
        "confidence_label_counts": dict(sorted({
            label: sum(1 for row in rows if row.get("confidence_label") == label)
            for label in {row.get("confidence_label") for row in rows}
        }.items())),
        "radius_margin_abs_min": min(margins) if margins else math.nan,
        "radius_margin_abs_mean": float(np.mean(margins)) if margins else math.nan,
        "radius_margin_abs_max": max(margins) if margins else math.nan,
        "limitation": "single seed and target2-only; useful sanity check, not a threshold policy",
    }


def confidence_summary_from_optimizer(summary: dict, summary_path: str | Path, evidence_label: str) -> dict:
    rows = list(summary.get("confidence_rows", []))
    truth_x = list(summary.get("true_x_values_mm", []))
    truth_z = list(summary.get("true_z_values_mm", []))
    truth_radii = summary.get("truth_radius_values_mm") or [
        summary.get("truth_radius_mm") for _ in truth_x
    ]
    truth_count = 0
    ambiguity_count = 0
    margins = []
    for row in rows:
        target_index = int(safe_float(row.get("step_target_index"), -1))
        if (
            0 <= target_index < len(truth_x)
            and exact_match(row.get("best_x_mm"), truth_x[target_index])
            and exact_match(row.get("best_z_mm"), truth_z[target_index])
            and exact_match(row.get("best_radius_mm"), truth_radii[target_index])
        ):
            truth_count += 1
        x_width = safe_float(row.get("ambiguity_x_max_mm")) - safe_float(row.get("ambiguity_x_min_mm"))
        radius_width = safe_float(row.get("ambiguity_radius_max_mm")) - safe_float(row.get("ambiguity_radius_min_mm"))
        if (math.isfinite(x_width) and x_width > 0.0) or (math.isfinite(radius_width) and radius_width > 0.0):
            ambiguity_count += 1
        margin = safe_float(row.get("radius_margin_abs"))
        if math.isfinite(margin):
            margins.append(margin)
    row_count = len(rows)
    min_margin = min(margins) if margins else math.nan
    return {
        "evidence": evidence_label,
        "acquisition_key": (
            f"sources={int(safe_float(summary.get('sources')))}|"
            f"tx_rx_offset_mm={format_offset(summary.get('tx_rx_offset_mm'))}|single_seed_pilot"
        ),
        "sources": safe_float(summary.get("sources")),
        "tx_rx_offset_mm": safe_float(summary.get("tx_rx_offset_mm")),
        "row_count": row_count,
        "truth_geometry_count": truth_count,
        "truth_geometry_fraction": truth_count / row_count if row_count else math.nan,
        "x_ambiguity_row_count": ambiguity_count,
        "radius_margin_abs_min": min_margin,
        "radius_margin_abs_mean": float(np.mean(margins)) if margins else math.nan,
        "radius_margin_abs_max": max(margins) if margins else math.nan,
        "branch_policy_label": classify_single_seed_policy(row_count, truth_count, ambiguity_count, min_margin),
        "replication_scope": "single_seed_pilot",
        "summary_path": str(summary_path),
    }


def acquisition_rows_from_aggregate(summary: dict, evidence_label: str) -> list[dict]:
    rows = []
    for key, item in sorted(
        summary.get("aggregate", {}).get("acquisition_summary", {}).items(),
        key=lambda pair: safe_float(pair[1].get("tx_rx_offset_mm")),
    ):
        row_count = int(safe_float(item.get("row_count"), 0))
        truth_count = int(safe_float(item.get("truth_geometry_count"), 0))
        ambiguity_count = int(safe_float(item.get("x_ambiguity_row_count"), 0))
        min_margin = safe_float(item.get("radius_margin_abs_min"))
        rows.append({
            "evidence": evidence_label,
            "acquisition_key": key,
            "sources": safe_float(item.get("sources")),
            "tx_rx_offset_mm": safe_float(item.get("tx_rx_offset_mm")),
            "row_count": row_count,
            "truth_geometry_count": truth_count,
            "truth_geometry_fraction": truth_count / row_count if row_count else math.nan,
            "x_ambiguity_row_count": ambiguity_count,
            "radius_margin_abs_min": min_margin,
            "radius_margin_abs_mean": safe_float(item.get("radius_margin_abs_mean")),
            "radius_margin_abs_max": safe_float(item.get("radius_margin_abs_max")),
            "branch_policy_label": classify_acquisition_policy(row_count, truth_count, ambiguity_count, min_margin),
            "replication_scope": "replicated_aggregate",
            "summary_path": "",
        })
    return rows


def classify_acquisition_policy(
    row_count: int,
    truth_count: int,
    x_ambiguity_count: int,
    min_margin: float,
    *,
    clean_margin_threshold: float = 1.0e-3,
) -> str:
    if row_count <= 0:
        return "missing"
    if truth_count == row_count and x_ambiguity_count == 0 and min_margin >= clean_margin_threshold:
        return "clean_replicated"
    if truth_count == row_count and x_ambiguity_count == 0:
        return "exact_but_low_margin"
    if truth_count > 0:
        return "mixed_or_ambiguous"
    return "not_recovered"


def classify_single_seed_policy(
    row_count: int,
    truth_count: int,
    x_ambiguity_count: int,
    min_margin: float,
    *,
    clean_margin_threshold: float = 1.0e-3,
) -> str:
    if row_count <= 0:
        return "missing"
    if truth_count == row_count and x_ambiguity_count == 0 and min_margin >= clean_margin_threshold:
        return "single_seed_clean_pilot_not_replicated"
    if truth_count == row_count:
        return "single_seed_exact_but_nonclean"
    if truth_count > 0:
        return "single_seed_mixed_or_ambiguous"
    return "single_seed_not_recovered"


def threshold_decision(rows: list[dict]) -> dict:
    clean_rows = [
        row for row in rows
        if row["branch_policy_label"] == "clean_replicated"
        and math.isfinite(safe_float(row.get("tx_rx_offset_mm")))
    ]
    ambiguous_rows = [
        row for row in rows
        if row["branch_policy_label"] in {
            "mixed_or_ambiguous",
            "not_recovered",
            "single_seed_mixed_or_ambiguous",
            "single_seed_not_recovered",
        }
    ]
    non_clean_rows = [
        row for row in rows
        if row["branch_policy_label"] != "clean_replicated"
    ]
    pilot_rows = [
        row for row in rows
        if str(row.get("replication_scope")) == "single_seed_pilot"
    ]
    first_clean = min(clean_rows, key=lambda row: row["tx_rx_offset_mm"]) if clean_rows else None
    ambiguous_offsets = sorted({safe_float(row.get("tx_rx_offset_mm")) for row in ambiguous_rows})
    non_clean_offsets = sorted({safe_float(row.get("tx_rx_offset_mm")) for row in non_clean_rows})
    pilot_offsets = sorted({safe_float(row.get("tx_rx_offset_mm")) for row in pilot_rows})
    pilot_rows_by_offset: dict[float, list[dict]] = {}
    for row in pilot_rows:
        offset = safe_float(row.get("tx_rx_offset_mm"))
        if math.isfinite(offset):
            pilot_rows_by_offset.setdefault(offset, []).append(row)
    replicated_pilot_offsets = sorted(
        offset for offset, offset_rows in pilot_rows_by_offset.items()
        if len(offset_rows) >= 2
    )
    replicated_nonclean_offsets = sorted(
        offset for offset, offset_rows in pilot_rows_by_offset.items()
        if len(offset_rows) >= 2
        and all(
            row["branch_policy_label"] != "single_seed_clean_pilot_not_replicated"
            for row in offset_rows
        )
    )
    pilot_nonclean_offsets = sorted({
        safe_float(row.get("tx_rx_offset_mm"))
        for row in pilot_rows
        if row["branch_policy_label"] != "single_seed_clean_pilot_not_replicated"
    })
    pilot_clean_offsets = sorted({
        safe_float(row.get("tx_rx_offset_mm"))
        for row in pilot_rows
        if row["branch_policy_label"] == "single_seed_clean_pilot_not_replicated"
    })
    pilot_nonclean = any(row["branch_policy_label"] != "single_seed_clean_pilot_not_replicated" for row in pilot_rows)
    if first_clean is None:
        label = "close50_target2_threshold_not_resolved"
    elif replicated_nonclean_offsets:
        label = "close50_target2_threshold_refined_replicated_midpoint_not_clean"
    elif pilot_rows and pilot_nonclean:
        label = "close50_target2_threshold_refined_midpoint_not_clean"
    else:
        label = "close50_target2_threshold_resolved_no_gpu_repeat"
    return {
        "policy_label": label,
        "first_clean_tx_rx_offset_mm": (
            safe_float(first_clean.get("tx_rx_offset_mm")) if first_clean is not None else math.nan
        ),
        "ambiguous_tx_rx_offsets_mm": ",".join(
            format_offset(value) for value in ambiguous_offsets if math.isfinite(value)
        ),
        "non_clean_tx_rx_offsets_mm": ",".join(
            format_offset(value) for value in non_clean_offsets if math.isfinite(value)
        ),
        "clean_tx_rx_offsets_mm": ",".join(
            format_offset(row.get("tx_rx_offset_mm")) for row in clean_rows
        ),
        "single_seed_pilot_tx_rx_offsets_mm": ",".join(
            format_offset(value) for value in pilot_offsets if math.isfinite(value)
        ),
        "replicated_midpoint_pilot_tx_rx_offsets_mm": ",".join(
            format_offset(value) for value in replicated_pilot_offsets if math.isfinite(value)
        ),
        "replicated_nonclean_midpoint_tx_rx_offsets_mm": ",".join(
            format_offset(value) for value in replicated_nonclean_offsets if math.isfinite(value)
        ),
        "single_seed_nonclean_pilot_tx_rx_offsets_mm": ",".join(
            format_offset(value) for value in pilot_nonclean_offsets if math.isfinite(value)
        ),
        "single_seed_clean_pilot_tx_rx_offsets_mm": ",".join(
            format_offset(value) for value in pilot_clean_offsets if math.isfinite(value)
        ),
        "decision": (
            "Do not repeat the old close50 Tx/Rx 40 target2 branch. Later evidence "
            "already resolves the branch-specific target2 threshold: Tx/Rx 25 mm "
            "is ambiguous, midpoint pilots below 30 mm refine the bracket but "
            "remain non-clean under the confidence/ambiguity policy, and 30 mm "
            "and above are clean in the tested three-seed sources4 aggregate. "
            "If a midpoint has replicated non-clean pilot support, use it only "
            "as immediate-below-threshold ambiguity evidence, not as a clean "
            "sub-30 mm threshold."
        ),
    }


def pilot_evidence_label(summary: dict, summary_path: Path) -> str:
    experiment_id = summary_path.parts[-3].split("_", 1)[0] if len(summary_path.parts) >= 3 else "run"
    sources = int(safe_float(summary.get("sources")))
    tx_rx = format_offset(summary.get("tx_rx_offset_mm")).replace(".", "p")
    run_name = str(summary.get("run_name", ""))
    seed_match = re.search(r"seed(\d+)", run_name)
    seed = seed_match.group(1) if seed_match else "unknown"
    return f"run{experiment_id}_sources{sources}_txrx{tx_rx}_seed{seed}_single_seed_pilot"


def tracker_output_alignment_rows(experiment_ids: list[int], docs_root: Path, outputs_root: Path) -> list[dict]:
    rows = []
    for experiment_id in experiment_ids:
        doc_matches = sorted(docs_root.glob(f"{experiment_id}_*.md"))
        output_matches = sorted(outputs_root.glob(f"{experiment_id}_*"))
        doc_name = doc_matches[0].name if doc_matches else ""
        output_name = output_matches[0].name if output_matches else ""
        doc_slug = doc_name.removesuffix(".md").split("_", 1)[1] if "_" in doc_name else ""
        output_slug = output_name.split("_", 1)[1] if "_" in output_name else ""
        rows.append({
            "experiment_id": experiment_id,
            "tracker_file": doc_name,
            "output_dir": output_name,
            "tracker_output_slug_match": bool(doc_slug and output_slug and doc_slug == output_slug),
            "audit_note": (
                "tracker filename does not describe the current output directory"
                if doc_slug and output_slug and doc_slug != output_slug
                else "tracker/output filenames align"
            ),
        })
    return rows


def build_summary(
    run270: dict,
    run280_rows: list[dict],
    threshold_rows: list[dict],
    tracker_rows: list[dict],
) -> dict:
    decision = threshold_decision(threshold_rows)
    return {
        **decision,
        "run270_truth_geometry_fraction": run270["truth_geometry_fraction"],
        "run270_min_margin": run270["radius_margin_abs_min"],
        "run280_txrx40_truth_geometry_fraction": (
            run280_rows[0]["truth_geometry_fraction"] if run280_rows else math.nan
        ),
        "run280_txrx40_min_margin": (
            run280_rows[0]["radius_margin_abs_min"] if run280_rows else math.nan
        ),
        "threshold_row_count": sum(row["row_count"] for row in threshold_rows),
        "threshold_target_scope": "target2 only",
        "coverage_limitation": (
            "The close50 branch is target2-only and should not be sold as an "
            "all-target or field-data result."
        ),
        "tracker_output_mismatch_count": sum(
            1 for row in tracker_rows if not bool(row["tracker_output_slug_match"])
        ),
        "single_seed_midpoint_rows": sum(
            row["row_count"] for row in threshold_rows
            if str(row.get("replication_scope")) == "single_seed_pilot"
        ),
    }


def plot_threshold_rows(rows: list[dict], summary: dict, save_path: Path) -> str:
    ordered = sorted(rows, key=lambda row: safe_float(row.get("tx_rx_offset_mm")))
    offsets = np.asarray([safe_float(row.get("tx_rx_offset_mm")) for row in ordered], dtype=np.float64)
    min_margins = np.asarray([safe_float(row.get("radius_margin_abs_min")) for row in ordered], dtype=np.float64)
    truth_fraction = np.asarray([safe_float(row.get("truth_geometry_fraction")) for row in ordered], dtype=np.float64)
    ambiguity = np.asarray([safe_float(row.get("x_ambiguity_row_count")) for row in ordered], dtype=np.float64)
    colors = ["#2f9d55" if row["branch_policy_label"] == "clean_replicated" else "#c7302b" for row in ordered]

    fig, axes = plt.subplots(1, 3, figsize=(13.8, 4.6), constrained_layout=True)
    axes[0].bar(offsets, min_margins, width=2.6, color=colors)
    axes[0].axhline(1.0e-3, color="#333333", linestyle="--", linewidth=0.9)
    axes[0].set_xlabel("Tx/Rx offset [mm]")
    axes[0].set_ylabel("minimum radius margin")
    axes[0].set_title("Close50 target2 margin threshold")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(offsets, truth_fraction, width=2.6, color=colors)
    axes[1].set_ylim(0, 1.05)
    axes[1].set_xlabel("Tx/Rx offset [mm]")
    axes[1].set_ylabel("truth-geometry fraction")
    axes[1].set_title("Recovery fraction")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[2].bar(offsets, ambiguity, width=2.6, color=colors)
    axes[2].set_xlabel("Tx/Rx offset [mm]")
    axes[2].set_ylabel("x-ambiguity rows")
    axes[2].set_title("Ambiguity count")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"{summary['policy_label']}: first clean Tx/Rx={summary['first_clean_tx_rx_offset_mm']:.0f} mm",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run270-summary", default=DEFAULT_RUN270_SUMMARY)
    parser.add_argument("--run280-aggregate", default=DEFAULT_RUN280_AGGREGATE)
    parser.add_argument("--threshold-aggregate", default=DEFAULT_THRESHOLD_AGGREGATE)
    parser.add_argument(
        "--midpoint-summary",
        action="append",
        default=None,
        help=(
            "Optional single-seed midpoint optimizer summary. May be repeated. "
            "Defaults to the known 27.5 and 28.75 mm pilots when omitted."
        ),
    )
    parser.add_argument("--run-name", default="close50_legacy_270_280_policy_audit")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    run270_summary = load_json(args.run270_summary)
    run280_summary = load_json(args.run280_aggregate)
    threshold_summary = load_json(args.threshold_aggregate)

    run270_row = summarize_optimizer_run(run270_summary, args.run270_summary)
    run280_rows = acquisition_rows_from_aggregate(run280_summary, "run280_sources4_txrx40_seed_replicates")
    threshold_rows = acquisition_rows_from_aggregate(threshold_summary, "run1222_sources4_txrx25_30_35_40_seed_replicates")
    midpoint_paths = [Path(path) for path in (args.midpoint_summary or DEFAULT_MIDPOINT_SUMMARIES)]
    existing_midpoint_paths = []
    for midpoint_path in midpoint_paths:
        if not midpoint_path.exists():
            continue
        existing_midpoint_paths.append(midpoint_path)
        midpoint_summary = load_json(midpoint_path)
        threshold_rows.append(
            confidence_summary_from_optimizer(
                midpoint_summary,
                midpoint_path,
                pilot_evidence_label(midpoint_summary, midpoint_path),
            )
        )
    tracker_rows = tracker_output_alignment_rows(
        [270, 280],
        Path("docs/experiments"),
        Path("outputs/experiments"),
    )
    summary = build_summary(run270_row, run280_rows, threshold_rows, tracker_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    evidence_csv = data_dir / "close50_legacy_branch_evidence.csv"
    threshold_csv = data_dir / "close50_threshold_by_txrx.csv"
    tracker_csv = data_dir / "close50_legacy_tracker_output_alignment.csv"
    summary_json = data_dir / "close50_legacy_policy_audit_summary.json"
    figure_path = Path(plot_threshold_rows(threshold_rows, summary, figures_dir / "close50_legacy_policy_audit.png"))
    validation_csv = data_dir / "figure_validation.csv"

    evidence_rows = [run270_row, *run280_rows]
    write_union_csv(evidence_csv, [json_safe(row) for row in evidence_rows])
    write_csv(threshold_csv, [json_safe(row) for row in threshold_rows])
    write_csv(tracker_csv, [json_safe(row) for row in tracker_rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])

    output_summary = {
        **summary,
        "inputs": {
            "run270_summary": args.run270_summary,
            "run280_aggregate": args.run280_aggregate,
            "threshold_aggregate": args.threshold_aggregate,
            "midpoint_summary": str(existing_midpoint_paths[0]) if existing_midpoint_paths else "",
            "midpoint_summaries": [str(path) for path in existing_midpoint_paths],
        },
        "paths": {
            "evidence_csv": str(evidence_csv),
            "threshold_csv": str(threshold_csv),
            "tracker_alignment_csv": str(tracker_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "close50_legacy_policy_audit",
        {
            "summary_json": str(summary_json),
            "threshold_aggregate": args.threshold_aggregate,
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

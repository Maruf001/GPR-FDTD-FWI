#!/usr/bin/env python3
"""Audit whether the field publication bundle should be refreshed with latest guardrail figures."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_BUNDLE_RUN = "111_gssi51600s_field_publication_claim_bundle_post_event_support_timing_discriminant_hpc"
DEFAULT_CANDIDATES = [
    {
        "figure_key": "field_short_anchor_waveform_coherence_qc",
        "source_run": "124_gssi51600s_field_short_anchor_waveform_coherence_audit",
        "summary_name": "field_short_anchor_waveform_coherence_summary.json",
        "metric_label": "min_corrected_corr",
        "metric_key": "min_corrected_field_trace_abs_correlation",
        "ready_key": "ready_for_waveform_morphology_qc",
        "role": "guardrail_refresh_candidate",
        "allowed_use": "short-anchor waveform morphology QC guardrail",
    },
    {
        "figure_key": "field_short_anchor_radius_degeneracy_guardrail",
        "source_run": "125_gssi51600s_field_short_anchor_radius_degeneracy_audit",
        "summary_name": "field_short_anchor_radius_degeneracy_summary.json",
        "metric_label": "weak_radius_sides",
        "metric_key": "weak_radius_side_count",
        "ready_key": "ready_for_waveform_morphology_qc",
        "role": "guardrail_refresh_candidate",
        "allowed_use": "radius-degeneracy blocker for field morphology QC",
    },
    {
        "figure_key": "field_short_anchor_signed_morphology_qc",
        "source_run": "126_gssi51600s_field_short_anchor_signed_morphology_audit",
        "summary_name": "field_short_anchor_signed_morphology_summary.json",
        "metric_label": "min_signed_corr",
        "metric_key": "min_corrected_signed_correlation",
        "ready_key": "ready_for_signed_waveform_morphology_qc",
        "role": "primary_refresh_candidate",
        "allowed_use": "signed short-anchor waveform morphology QC",
    },
    {
        "figure_key": "field_short_anchor_signed_morphology_threshold_sensitivity",
        "source_run": "127_gssi51600s_field_short_anchor_signed_morphology_sensitivity",
        "summary_name": "field_short_anchor_signed_morphology_sensitivity_summary.json",
        "metric_label": "supported_threshold_combos",
        "metric_key": "all_pairs_supported_threshold_combo_count",
        "ready_key": "ready_for_moderate_threshold_morphology_qc",
        "role": "primary_refresh_candidate",
        "allowed_use": "threshold-margin sensitivity for signed morphology QC",
    },
]


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def build_candidate_rows(dataset_root: Path, bundle_rows: list[dict], candidates: list[dict]) -> list[dict]:
    bundled_keys = {row.get("figure_key", "") for row in bundle_rows}
    bundled_runs = {row.get("source_run", "") for row in bundle_rows}
    rows: list[dict] = []
    for candidate in candidates:
        source_run = candidate["source_run"]
        summary_path = dataset_root / source_run / "data" / candidate["summary_name"]
        summary = read_json(summary_path)
        figure_path = Path(summary.get("paths", {}).get("figure", ""))
        already_in_bundle = candidate["figure_key"] in bundled_keys or source_run in bundled_runs
        field_fwi_ready = boolish(summary.get("ready_for_field_fwi", False))
        ready_for_qc = boolish(summary.get(candidate["ready_key"], False))
        rows.append(
            {
                "figure_key": candidate["figure_key"],
                "source_run": source_run,
                "policy_label": summary.get("policy_label", ""),
                "metric_label": candidate["metric_label"],
                "metric_value": safe_float(summary.get(candidate["metric_key"])),
                "figure_path": str(figure_path),
                "figure_exists": figure_path.is_file(),
                "already_in_current_bundle": already_in_bundle,
                "candidate_role": candidate["role"],
                "ready_for_qc_use": ready_for_qc,
                "ready_for_field_fwi": field_fwi_ready,
                "automatic_bundle_refresh_ready": False,
                "allowed_use": candidate["allowed_use"],
                "blocked_use": "automatic bundle promotion, field FWI, 3D/HPC, radius/geometry/cover-depth recovery",
            }
        )
    return rows


def summarize_freshness(bundle_rows: list[dict], candidate_rows: list[dict], bundle_run: str) -> dict:
    missing = [row for row in candidate_rows if not boolish(row.get("figure_exists"))]
    included = [row for row in candidate_rows if boolish(row.get("already_in_current_bundle"))]
    qc_ready = [row for row in candidate_rows if boolish(row.get("ready_for_qc_use"))]
    fwi_ready = [row for row in candidate_rows if boolish(row.get("ready_for_field_fwi"))]
    primary = [row for row in candidate_rows if row.get("candidate_role") == "primary_refresh_candidate"]
    guardrail = [row for row in candidate_rows if row.get("candidate_role") == "guardrail_refresh_candidate"]
    return {
        "policy_label": "gssi51600s_field_publication_bundle_freshness_audit_curated_refresh_needed_not_automatic",
        "source_bundle_run": bundle_run,
        "current_bundle_figure_count": len(bundle_rows),
        "candidate_figure_count": len(candidate_rows),
        "candidate_already_in_bundle_count": len(included),
        "candidate_missing_figure_count": len(missing),
        "candidate_qc_ready_count": len(qc_ready),
        "primary_refresh_candidate_count": len(primary),
        "guardrail_refresh_candidate_count": len(guardrail),
        "candidate_field_fwi_ready_count": len(fwi_ready),
        "ready_for_curated_bundle_refresh_decision": len(missing) == 0 and len(qc_ready) == len(candidate_rows),
        "automatic_bundle_refresh_ready": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "Keep the current publication bundle curated unless preparing a deliberate field-supplement "
            "refresh. The latest short-anchor morphology chain has four valid QC figures outside the "
            "current bundle; signed morphology and its threshold sensitivity are the primary promotion "
            "candidates, while waveform coherence and radius degeneracy are guardrail candidates. "
            "Do not auto-promote these into field FWI, 3D/HPC, radius, geometry, or cover-depth claims."
        ),
    }


def plot_freshness(candidate_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), constrained_layout=True)
    labels = ["bundle", "candidates", "already\nincluded", "primary", "guardrail"]
    values = [
        summary["current_bundle_figure_count"],
        summary["candidate_figure_count"],
        summary["candidate_already_in_bundle_count"],
        summary["primary_refresh_candidate_count"],
        summary["guardrail_refresh_candidate_count"],
    ]
    axes[0].bar(range(len(labels)), values, color=["#4c72b0", "#55a868", "#bab0ac", "#8172b2", "#c44e52"])
    axes[0].set_xticks(range(len(labels)), labels)
    axes[0].set_ylabel("figure count")
    axes[0].set_title("Field bundle freshness candidates")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    gate_labels = ["curated\nrefresh", "automatic\nrefresh", "field\nFWI", "3D/HPC"]
    gate_values = [
        summary["ready_for_curated_bundle_refresh_decision"],
        summary["automatic_bundle_refresh_ready"],
        summary["ready_for_field_fwi"],
        summary["ready_for_3d_hpc"],
    ]
    colors = ["#59a14f" if value else "#bab0ac" for value in gate_values]
    axes[1].bar(range(len(gate_labels)), [1 if value else 0 for value in gate_values], color=colors)
    axes[1].set_xticks(range(len(gate_labels)), gate_labels)
    axes[1].set_yticks([0, 1], ["blocked", "ready"])
    axes[1].set_ylim(0, 1.15)
    axes[1].set_title("Refresh and launch gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.06,
        f"QC-ready candidates: {summary['candidate_qc_ready_count']}/"
        f"{summary['candidate_figure_count']}\n"
        f"missing figures: {summary['candidate_missing_figure_count']}\n"
        f"already in bundle: {summary['candidate_already_in_bundle_count']}\n"
        f"field FWI candidates: {summary['candidate_field_fwi_ready_count']}",
        transform=axes[1].transAxes,
        va="bottom",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI 51600S field publication bundle freshness audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, candidates_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_publication_bundle_freshness_audit.png`",
                "",
                "This CPU-only figure checks whether the curated field publication",
                "bundle omits the latest short-anchor morphology guardrail figures.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Current bundle figures: `{summary['current_bundle_figure_count']}`.",
                f"Candidate figures: `{summary['candidate_figure_count']}`.",
                f"Already included candidates: `{summary['candidate_already_in_bundle_count']}`.",
                f"Ready for curated refresh decision: `{summary['ready_for_curated_bundle_refresh_decision']}`.",
                f"Automatic bundle refresh ready: `{summary['automatic_bundle_refresh_ready']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Candidate rows: `{candidates_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved field bundle and short-anchor morphology artifacts only. It does not",
                "regenerate the publication bundle, run DZT preprocessing, FDTD, FWI, GPU kernels, 3D/HPC",
                "jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--bundle-run", default=DEFAULT_BUNDLE_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_publication_bundle_freshness_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    bundle_dir = dataset_root / args.bundle_run
    bundle_rows = read_csv_rows(bundle_dir / "data/field_publication_figure_rows.csv")
    candidate_rows = build_candidate_rows(dataset_root, bundle_rows, DEFAULT_CANDIDATES)
    summary = summarize_freshness(bundle_rows, candidate_rows, args.bundle_run)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    candidates_csv = data_dir / "field_publication_bundle_freshness_candidates.csv"
    summary_json = data_dir / "field_publication_bundle_freshness_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_publication_bundle_freshness_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(candidates_csv, [json_safe(row) for row in candidate_rows])
    plot_freshness(candidate_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, candidates_csv)

    summary["paths"] = {
        "candidate_rows_csv": str(candidates_csv),
        "summary_json": str(summary_json),
        "source_bundle_rows_csv": str(bundle_dir / "data/field_publication_figure_rows.csv"),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_publication_bundle_freshness_audit",
        {
            "dataset_id": args.dataset_id,
            "bundle_run": args.bundle_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

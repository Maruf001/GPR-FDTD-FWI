#!/usr/bin/env python3
"""Synthesize close50 nearest-vs-linear sampling boundary evidence."""

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
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_NEAREST_POLICY_RUN = "1317_close50_legacy_270_280_policy_audit_post_28p75_seed13_replicate"
DEFAULT_LINEAR_29P5_RUN = "1303_close50_linear29p5_three_seed_frequency_policy"
DEFAULT_LINEAR_SUB30_RUN = "1275_close50_linear_sub30_bracket_policy"
DEFAULT_CLAIM_REFRESH_RUN = "1305_synthetic_2d_publication_claim_boundary_refresh_post_close50_seed_frequency"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _finite(values: list[float]) -> list[float]:
    return [value for value in values if math.isfinite(value)]


def _fmt_offsets(values: list[float]) -> str:
    return ",".join(f"{value:g}" for value in sorted(set(values)))


def _status_rank(status: str) -> int:
    return {
        "clean_replicated": 4,
        "exact_strong_not_clean": 3,
        "replicated_nonclean": 2,
        "single_seed_nonclean": 1,
        "mixed_or_ambiguous": 0,
    }.get(status, 0)


def nearest_boundary_rows(threshold_rows: list[dict]) -> list[dict]:
    grouped: dict[float, list[dict]] = {}
    for row in threshold_rows:
        offset = safe_float(row.get("tx_rx_offset_mm"))
        if not math.isfinite(offset):
            continue
        grouped.setdefault(offset, []).append(row)

    outputs = []
    for offset, rows in sorted(grouped.items()):
        row_count = sum(int(safe_float(row.get("row_count"), 0)) for row in rows)
        truth_count = sum(int(safe_float(row.get("truth_geometry_count"), 0)) for row in rows)
        x_ambiguity_count = sum(int(safe_float(row.get("x_ambiguity_row_count"), 0)) for row in rows)
        min_margins = _finite([safe_float(row.get("radius_margin_abs_min")) for row in rows])
        scopes = sorted(set(str(row.get("replication_scope", "")) for row in rows))
        policy_labels = sorted(set(str(row.get("branch_policy_label", "")) for row in rows))
        clean_replicated = (
            len(rows) == 1
            and rows[0].get("branch_policy_label") == "clean_replicated"
            and rows[0].get("replication_scope") == "replicated_aggregate"
        )
        replicated_nonclean = len(rows) >= 2 and truth_count == row_count and x_ambiguity_count > 0
        single_seed_nonclean = (
            len(rows) == 1
            and rows[0].get("replication_scope") == "single_seed_pilot"
            and truth_count == row_count
            and x_ambiguity_count > 0
        )
        if clean_replicated:
            status = "clean_replicated"
        elif replicated_nonclean:
            status = "replicated_nonclean"
        elif single_seed_nonclean:
            status = "single_seed_nonclean"
        else:
            status = "mixed_or_ambiguous"
        outputs.append(
            {
                "sampling_family": "nearest_receiver",
                "tx_rx_offset_mm": offset,
                "evidence_row_count": row_count,
                "truth_geometry_count": truth_count,
                "truth_geometry_fraction": truth_count / row_count if row_count else 0.0,
                "strict_clean_row_count": row_count - x_ambiguity_count if truth_count == row_count else 0,
                "x_ambiguity_row_count": x_ambiguity_count,
                "radius_margin_abs_min": min(min_margins) if min_margins else math.nan,
                "seed_or_replication_count": len(rows),
                "replication_scope": ";".join(scopes),
                "source_policy_labels": ";".join(policy_labels),
                "boundary_status": status,
                "clean_threshold_candidate": clean_replicated,
                "paper_role": (
                    "paper_safe_clean_threshold"
                    if clean_replicated and offset == 30.0
                    else "supporting_boundary_evidence"
                ),
            }
        )
    return outputs


def linear_boundary_rows(
    linear29_summary: dict,
    linear29_confidence_rows: list[dict],
    linear_sub30_confidence_rows: list[dict],
) -> list[dict]:
    rows = []
    rows.append(
        {
            "sampling_family": "linear_receiver",
            "tx_rx_offset_mm": 29.5,
            "evidence_row_count": int(safe_float(linear29_summary.get("confidence_row_count"), 0)),
            "truth_geometry_count": int(safe_float(linear29_summary.get("truth_geometry_row_count"), 0)),
            "truth_geometry_fraction": (
                safe_float(linear29_summary.get("truth_geometry_row_count"), 0.0)
                / safe_float(linear29_summary.get("confidence_row_count"), 1.0)
            ),
            "strict_clean_row_count": int(safe_float(linear29_summary.get("strict_clean_row_count"), 0)),
            "x_ambiguity_row_count": int(safe_float(linear29_summary.get("x_ambiguity_row_count"), 0)),
            "radius_margin_abs_min": safe_float(linear29_summary.get("radius_margin_abs_min")),
            "seed_or_replication_count": int(safe_float(linear29_summary.get("seed_count"), 0)),
            "replication_scope": "three_seed_frequency",
            "source_policy_labels": linear29_summary.get("policy_label", ""),
            "boundary_status": "exact_strong_not_clean",
            "clean_threshold_candidate": False,
            "paper_role": "sub30_exact_strong_caveat",
        }
    )

    offset_29p75 = [
        row for row in linear_sub30_confidence_rows
        if abs(safe_float(row.get("tx_rx_offset_mm")) - 29.75) <= 1e-9
    ]
    if offset_29p75:
        row_count = len(offset_29p75)
        truth_count = sum(str(row.get("truth_geometry_match", "")).lower() == "true" for row in offset_29p75)
        strict_clean = sum(str(row.get("strict_clean_row", "")).lower() == "true" for row in offset_29p75)
        x_ambiguity = sum(safe_float(row.get("x_ambiguity_width_mm"), 0.0) > 0.0 for row in offset_29p75)
        margins = _finite([safe_float(row.get("radius_margin_abs")) for row in offset_29p75])
        seeds = sorted(set(str(row.get("seed_label", "")) for row in offset_29p75))
        rows.append(
            {
                "sampling_family": "linear_receiver",
                "tx_rx_offset_mm": 29.75,
                "evidence_row_count": row_count,
                "truth_geometry_count": truth_count,
                "truth_geometry_fraction": truth_count / row_count if row_count else 0.0,
                "strict_clean_row_count": strict_clean,
                "x_ambiguity_row_count": x_ambiguity,
                "radius_margin_abs_min": min(margins) if margins else math.nan,
                "seed_or_replication_count": len(seeds),
                "replication_scope": "single_seed_bracket",
                "source_policy_labels": "close50_linear_sub30_seed13_x_ambiguity_persists",
                "boundary_status": "exact_strong_not_clean",
                "clean_threshold_candidate": False,
                "paper_role": "single_seed_sub30_caveat",
            }
        )
    return rows


def summarize_sampling_boundary(
    rows: list[dict],
    nearest_summary: dict,
    linear29_summary: dict,
    claim_summary: dict,
) -> dict:
    nearest = [row for row in rows if row["sampling_family"] == "nearest_receiver"]
    linear = [row for row in rows if row["sampling_family"] == "linear_receiver"]
    nearest_clean = [
        safe_float(row.get("tx_rx_offset_mm"))
        for row in nearest
        if row["boundary_status"] == "clean_replicated"
    ]
    nearest_nonclean = [
        safe_float(row.get("tx_rx_offset_mm"))
        for row in nearest
        if row["boundary_status"] in {"replicated_nonclean", "single_seed_nonclean", "mixed_or_ambiguous"}
    ]
    linear_exact = [
        safe_float(row.get("tx_rx_offset_mm"))
        for row in linear
        if row["boundary_status"] == "exact_strong_not_clean"
    ]
    first_clean = min(nearest_clean) if nearest_clean else math.nan
    max_nonclean_below_clean = max(
        [value for value in nearest_nonclean if math.isfinite(first_clean) and value < first_clean]
        or [math.nan]
    )
    return {
        "policy_label": "close50_sampling_boundary_synthesis_cpu_no_gpu",
        "boundary_row_count": len(rows),
        "nearest_boundary_row_count": len(nearest),
        "linear_boundary_row_count": len(linear),
        "nearest_first_clean_replicated_tx_rx_mm": first_clean,
        "nearest_nonclean_offsets_mm": _fmt_offsets(nearest_nonclean),
        "nearest_clean_offsets_mm": _fmt_offsets(nearest_clean),
        "nearest_max_nonclean_below_clean_mm": max_nonclean_below_clean,
        "linear_exact_strong_not_clean_offsets_mm": _fmt_offsets(linear_exact),
        "linear29p5_seed_count": safe_float(linear29_summary.get("seed_count"), 0.0),
        "linear29p5_ambiguous_seed_count": safe_float(linear29_summary.get("ambiguous_seed_count"), 0.0),
        "linear29p5_ambiguous_seed_values": linear29_summary.get("ambiguous_seed_values", ""),
        "linear29p5_strict_clean_rows": safe_float(linear29_summary.get("strict_clean_row_count"), 0.0),
        "linear29p5_confidence_rows": safe_float(linear29_summary.get("confidence_row_count"), 0.0),
        "legacy_run270_truth_fraction": safe_float(nearest_summary.get("run270_truth_geometry_fraction"), 0.0),
        "legacy_run280_txrx40_truth_fraction": safe_float(
            nearest_summary.get("run280_txrx40_truth_geometry_fraction"), 0.0
        ),
        "claim_refresh_included": bool(claim_summary.get("ready_for_manuscript_claim_table", False)),
        "ready_for_paper_sampling_boundary": True,
        "ready_for_sub30_clean_threshold_claim": False,
        "ready_for_gpu_probe": False,
        "gpu_priority": "none",
        "decision": (
            "Use 30 mm nearest-sampled Tx/Rx as the paper-safe clean replicated close50 target2 threshold. "
            "Use 28.75 mm nearest-sampled and 29.5 mm linear receiver evidence as sub-30 caveats: exact/strong "
            "or replicated non-clean evidence exists below 30 mm, but not a clean replicated sub-30 threshold. "
            "No additional close50 GPU probe is justified without a new objective or acquisition question."
        ),
    }


def plot_sampling_boundary(rows: list[dict], summary: dict, save_path: Path) -> str:
    ordered = sorted(rows, key=lambda row: (row["sampling_family"], safe_float(row.get("tx_rx_offset_mm"))))
    labels = [
        f"{row['sampling_family'].replace('_receiver', '')}\n{safe_float(row.get('tx_rx_offset_mm')):g} mm"
        for row in ordered
    ]
    ranks = [_status_rank(str(row.get("boundary_status", ""))) for row in ordered]
    colors = {
        "clean_replicated": "#59a14f",
        "exact_strong_not_clean": "#f28e2b",
        "replicated_nonclean": "#e15759",
        "single_seed_nonclean": "#b07aa1",
        "mixed_or_ambiguous": "#9c755f",
    }
    fig, axes = plt.subplots(1, 2, figsize=(14.0, 5.2), constrained_layout=True)
    axes[0].bar(
        np.arange(len(ordered)),
        ranks,
        color=[colors.get(str(row.get("boundary_status", "")), "#bab0ac") for row in ordered],
        edgecolor="#333333",
        linewidth=0.4,
    )
    axes[0].set_xticks(np.arange(len(ordered)), labels, rotation=35, ha="right")
    axes[0].set_yticks(
        [0, 1, 2, 3, 4],
        ["ambiguous", "single\nnonclean", "replicated\nnonclean", "exact\nnot clean", "clean"],
    )
    axes[0].set_title("Close50 target2 boundary status")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    offsets = [safe_float(row.get("tx_rx_offset_mm")) for row in ordered]
    clean_counts = [safe_float(row.get("strict_clean_row_count"), 0.0) for row in ordered]
    row_counts = [safe_float(row.get("evidence_row_count"), 0.0) for row in ordered]
    fractions = [clean / count if count else 0.0 for clean, count in zip(clean_counts, row_counts)]
    axes[1].bar(np.arange(len(ordered)), fractions, color="#4e79a7", edgecolor="#333333", linewidth=0.4)
    axes[1].set_xticks(np.arange(len(ordered)), labels, rotation=35, ha="right")
    axes[1].set_ylim(0.0, 1.08)
    axes[1].set_ylabel("strict-clean row fraction")
    axes[1].set_title("Strict-clean support by sampling family")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.95,
        f"nearest clean threshold: {summary['nearest_first_clean_replicated_tx_rx_mm']:.1f} mm\n"
        f"nearest non-clean: {summary['nearest_nonclean_offsets_mm']} mm\n"
        f"linear caveats: {summary['linear_exact_strong_not_clean_offsets_mm']} mm\n"
        f"linear 29.5 ambiguous seeds: {summary['linear29p5_ambiguous_seed_values']}\n"
        f"GPU probe: {summary['ready_for_gpu_probe']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Close50 target2 nearest-vs-linear sampling boundary synthesis", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `close50_sampling_boundary_synthesis.png`",
                "",
                "This CPU-only figure synthesizes close50 target2 nearest-sampled",
                "and linear-receiver boundary evidence from saved outputs.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Nearest first clean replicated Tx/Rx: `{summary['nearest_first_clean_replicated_tx_rx_mm']}` mm.",
                f"Nearest non-clean offsets: `{summary['nearest_nonclean_offsets_mm']}`.",
                f"Linear exact/strong not-clean offsets: `{summary['linear_exact_strong_not_clean_offsets_mm']}`.",
                f"Linear 29.5 ambiguous seeds: `{summary['linear29p5_ambiguous_seed_values']}`.",
                f"Ready for sub-30 clean threshold claim: `{summary['ready_for_sub30_clean_threshold_claim']}`.",
                f"Ready for GPU probe: `{summary['ready_for_gpu_probe']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Boundary rows: `{rows_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This synthesis reads saved policy outputs only. It does not run FDTD,",
                "FWI, GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default="outputs/experiments")
    parser.add_argument("--nearest-policy-run", default=DEFAULT_NEAREST_POLICY_RUN)
    parser.add_argument("--linear-29p5-run", default=DEFAULT_LINEAR_29P5_RUN)
    parser.add_argument("--linear-sub30-run", default=DEFAULT_LINEAR_SUB30_RUN)
    parser.add_argument("--claim-refresh-run", default=DEFAULT_CLAIM_REFRESH_RUN)
    parser.add_argument("--run-name", default="close50_sampling_boundary_synthesis")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.experiment_root)
    nearest_dir = root / args.nearest_policy_run
    linear29_dir = root / args.linear_29p5_run
    linear_sub30_dir = root / args.linear_sub30_run
    claim_dir = root / args.claim_refresh_run

    nearest_summary = read_json(nearest_dir / "data/close50_legacy_policy_audit_summary.json")
    nearest_rows = read_csv_rows(nearest_dir / "data/close50_threshold_by_txrx.csv")
    linear29_summary = read_json(linear29_dir / "data/close50_linear_receiver_policy_summary.json")
    linear29_confidence_rows = read_csv_rows(linear29_dir / "data/close50_linear_receiver_confidence_rows.csv")
    linear_sub30_confidence_rows = read_csv_rows(
        linear_sub30_dir / "data/close50_linear_sub30_bracket_confidence_rows.csv"
    )
    claim_summary = read_json(claim_dir / "data/synthetic_2d_publication_claim_boundary_refresh_summary.json")

    rows = nearest_boundary_rows(nearest_rows) + linear_boundary_rows(
        linear29_summary,
        linear29_confidence_rows,
        linear_sub30_confidence_rows,
    )
    rows = sorted(rows, key=lambda row: (row["sampling_family"], safe_float(row.get("tx_rx_offset_mm"))))
    summary = summarize_sampling_boundary(rows, nearest_summary, linear29_summary, claim_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.experiment_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "close50_sampling_boundary_rows.csv"
    summary_json = data_dir / "close50_sampling_boundary_synthesis_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "close50_sampling_boundary_synthesis.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    plot_sampling_boundary(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, rows_csv)

    summary["paths"] = {
        "boundary_rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "source_nearest_summary_json": str(nearest_dir / "data/close50_legacy_policy_audit_summary.json"),
        "source_nearest_threshold_csv": str(nearest_dir / "data/close50_threshold_by_txrx.csv"),
        "source_linear29_summary_json": str(linear29_dir / "data/close50_linear_receiver_policy_summary.json"),
        "source_linear29_confidence_csv": str(linear29_dir / "data/close50_linear_receiver_confidence_rows.csv"),
        "source_linear_sub30_confidence_csv": str(
            linear_sub30_dir / "data/close50_linear_sub30_bracket_confidence_rows.csv"
        ),
        "source_claim_refresh_summary_json": str(
            claim_dir / "data/synthetic_2d_publication_claim_boundary_refresh_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "close50_sampling_boundary_synthesis",
        {
            "nearest_policy_run": args.nearest_policy_run,
            "linear_29p5_run": args.linear_29p5_run,
            "linear_sub30_run": args.linear_sub30_run,
            "claim_refresh_run": args.claim_refresh_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

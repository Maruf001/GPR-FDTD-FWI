#!/usr/bin/env python3
"""Build a compact methods-ready card for the synthetic 2D experiment archive."""

from __future__ import annotations

import argparse
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
from run_synthetic_2d_publication_figure_bundle import DEFAULT_EXPERIMENT_ROOT  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_ARCHIVE_HEALTH_RUN = "1324_experiment_archive_health_report_post_field_timing_refresh"
DEFAULT_PUBLICATION_BUNDLE_RUN = "1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation"
DEFAULT_NEXT_MATRIX_RUN = "1323_synthetic_2d_next_question_matrix_post_claim_boundary_reconciliation"
DEFAULT_SOURCE_NOTES_RUN = "1325_synthetic_publication_source_figure_notes_backfill_report"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def no_gpu_value(value) -> bool:
    return str(value).strip().lower() in {"", "none", "none_now", "no_gpu_required"}


def count_fraction(count: float, total: float) -> float:
    total = safe_float(total, 0.0)
    if total <= 0:
        return math.nan
    return safe_float(count, 0.0) / total


def range_rows(archive_summary: dict) -> list[dict]:
    summary = archive_summary.get("summary", archive_summary)
    rows = []
    for range_label, payload in summary.get("by_range", {}).items():
        run_count = safe_float(payload.get("run_count"), 0.0)
        with_images = safe_float(payload.get("with_images"), 0.0)
        with_notes = safe_float(payload.get("with_figure_notes"), 0.0)
        category_counts = payload.get("category_counts", {})
        rows.append(
            {
                "range": range_label,
                "run_count": run_count,
                "physics_or_diagnostic_count": safe_float(
                    category_counts.get("physics_or_diagnostic"), 0.0
                ),
                "analysis_report_count": safe_float(category_counts.get("analysis_report"), 0.0),
                "reporting_audit_checkpoint_count": safe_float(
                    category_counts.get("reporting_audit_checkpoint"), 0.0
                ),
                "unclear_count": safe_float(category_counts.get("unclear"), 0.0),
                "with_data_dir": safe_float(payload.get("with_data_dir"), 0.0),
                "with_figures_dir": safe_float(payload.get("with_figures_dir"), 0.0),
                "with_images": with_images,
                "with_figure_notes": with_notes,
                "figure_note_coverage_fraction": count_fraction(with_notes, with_images),
                "issue_count": safe_float(payload.get("issue_count"), 0.0),
                "warning_count": safe_float(payload.get("warning_count"), 0.0),
            }
        )
    return rows


def summarize_corpus(
    rows: list[dict],
    *,
    archive_summary: dict,
    publication_summary: dict,
    next_matrix_summary: dict,
    source_notes_summary: dict,
) -> dict:
    archive = archive_summary.get("summary", archive_summary)
    category_counts = archive.get("category_counts", {})
    issue_counts = archive.get("issue_counts", {})
    warning_counts = archive.get("warning_counts", {})
    total_images = sum(safe_float(row.get("with_images"), 0.0) for row in rows)
    total_notes = sum(safe_float(row.get("with_figure_notes"), 0.0) for row in rows)
    no_gpu = (
        no_gpu_value(publication_summary.get("gpu_priority", ""))
        and no_gpu_value(next_matrix_summary.get("gpu_priority", ""))
        and no_gpu_value(source_notes_summary.get("gpu_priority", ""))
    )
    current_ready = (
        bool(publication_summary.get("ready_for_manuscript_draft", False))
        and bool(source_notes_summary.get("ready_for_manuscript_handoff", False))
        and safe_float(source_notes_summary.get("notes_present_after_count"), 0.0)
        == safe_float(source_notes_summary.get("source_figure_count"), -1.0)
        and safe_float(next_matrix_summary.get("immediate_gpu_priority_count"), 0.0) == 0.0
        and safe_float(next_matrix_summary.get("conditional_gpu_candidate_count"), 0.0) == 0.0
        and no_gpu
    )
    legacy_issues = sum(safe_float(value, 0.0) for value in issue_counts.values())
    policy = (
        "synthetic_2d_archive_corpus_card_current_ready_legacy_hygiene_caveats"
        if current_ready
        else "synthetic_2d_archive_corpus_card_review_required"
    )
    return {
        "policy_label": policy,
        "archive_run_count": safe_float(archive.get("run_count"), 0.0),
        "physics_or_diagnostic_count": safe_float(category_counts.get("physics_or_diagnostic"), 0.0),
        "analysis_report_count": safe_float(category_counts.get("analysis_report"), 0.0),
        "reporting_audit_checkpoint_count": safe_float(
            category_counts.get("reporting_audit_checkpoint"), 0.0
        ),
        "unclear_run_type_count": safe_float(category_counts.get("unclear"), 0.0),
        "image_bearing_run_count": total_images,
        "figure_notes_run_count": total_notes,
        "archive_figure_note_coverage_fraction": count_fraction(total_notes, total_images),
        "legacy_issue_count": legacy_issues,
        "figure_images_missing_figure_notes_count": safe_float(
            issue_counts.get("figure_images_missing_figure_notes"), 0.0
        ),
        "missing_run_manifest_count": safe_float(issue_counts.get("missing_run_manifest"), 0.0),
        "unclear_run_type_warning_count": safe_float(warning_counts.get("unclear_run_type"), 0.0),
        "current_publication_figure_count": safe_float(publication_summary.get("figure_count"), 0.0),
        "current_publication_validated_figure_count": safe_float(
            publication_summary.get("validated_figure_count"), 0.0
        ),
        "current_publication_claim_boundary_count": safe_float(
            publication_summary.get("claim_boundary_count"), 0.0
        ),
        "current_source_figure_count": safe_float(source_notes_summary.get("source_figure_count"), 0.0),
        "current_source_figure_notes_present": safe_float(
            source_notes_summary.get("notes_present_after_count"), 0.0
        ),
        "synthetic_immediate_gpu_priority_count": safe_float(
            next_matrix_summary.get("immediate_gpu_priority_count"), 0.0
        ),
        "synthetic_conditional_gpu_candidate_count": safe_float(
            next_matrix_summary.get("conditional_gpu_candidate_count"), 0.0
        ),
        "gpu_priority": "none" if no_gpu else "review",
        "ready_for_methods_corpus_card": current_ready,
        "decision": (
            "Use this as a methods-ready synthetic archive/corpus card. The current "
            "publication-facing synthetic endpoint is ready and has complete source-figure "
            "notes; legacy archive hygiene caveats remain historical and should not trigger "
            "broad regeneration or GPU reruns."
        ),
    }


def plot_corpus_card(rows: list[dict], summary: dict, save_path: Path) -> str:
    ranges = [row["range"] for row in rows]
    run_counts = [safe_float(row["run_count"], 0.0) for row in rows]
    note_coverage = [safe_float(row["figure_note_coverage_fraction"], 0.0) for row in rows]
    issues = [safe_float(row["issue_count"], 0.0) for row in rows]

    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.6), constrained_layout=True)
    x = np.arange(len(rows))
    axes[0].bar(x, run_counts, color="#4c78a8", width=0.62)
    axes[0].set_xticks(x, ranges)
    axes[0].set_ylabel("numbered runs")
    axes[0].set_title("Archive runs by range")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, note_coverage, color="#2f9d55", width=0.62)
    axes[1].set_xticks(x, ranges)
    axes[1].set_ylim(0, 1.05)
    axes[1].set_ylabel("fraction")
    axes[1].set_title("Figure-note coverage by range")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    current_values = [
        safe_float(summary.get("current_publication_figure_count"), 0.0),
        safe_float(summary.get("current_publication_claim_boundary_count"), 0.0),
        safe_float(summary.get("current_source_figure_notes_present"), 0.0),
        safe_float(summary.get("synthetic_immediate_gpu_priority_count"), 0.0),
        safe_float(summary.get("synthetic_conditional_gpu_candidate_count"), 0.0),
        sum(issues),
    ]
    labels = ["figures", "claims", "source\nnotes", "immediate\nGPU", "conditional\nGPU", "legacy\nissues"]
    axes[2].bar(np.arange(len(current_values)), current_values, color=["#4c78a8", "#8c564b", "#2f9d55", "#c7302b", "#c7302b", "#6b6b6b"], width=0.62)
    axes[2].set_xticks(np.arange(len(labels)), labels)
    axes[2].set_title("Current endpoint and legacy caveat")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)
    fig.suptitle(f"Synthetic 2D archive corpus card: {summary['policy_label']}", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(
    path: Path,
    summary: dict,
    range_csv: Path,
    summary_json: Path,
    validation_csv: Path,
) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `synthetic_2d_archive_corpus_card.png`",
                "",
                "This is a CPU-only methods card for the existing synthetic 2D",
                "experiment archive. It reads the current archive-health report,",
                "publication bundle, next-question matrix, and source-figure notes",
                "audit; it does not run FDTD, FWI, or GPU kernels.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Archive runs: `{summary['archive_run_count']:.0f}`.",
                f"Physics/diagnostic runs: `{summary['physics_or_diagnostic_count']:.0f}`.",
                f"Current publication figures: `{summary['current_publication_figure_count']:.0f}`.",
                f"Current source notes: `{summary['current_source_figure_notes_present']:.0f}`.",
                f"Legacy issue count: `{summary['legacy_issue_count']:.0f}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Range table: `{range_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                f"- Figure validation: `{validation_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "The card supports methods and corpus description. Legacy archive",
                "hygiene caveats should be reported as historical caveats, not as a",
                "reason to regenerate old runs or launch broad GPU experiments.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default=DEFAULT_EXPERIMENT_ROOT)
    parser.add_argument("--archive-health-run", default=DEFAULT_ARCHIVE_HEALTH_RUN)
    parser.add_argument("--publication-bundle-run", default=DEFAULT_PUBLICATION_BUNDLE_RUN)
    parser.add_argument("--next-matrix-run", default=DEFAULT_NEXT_MATRIX_RUN)
    parser.add_argument("--source-notes-run", default=DEFAULT_SOURCE_NOTES_RUN)
    parser.add_argument("--run-name", default="synthetic_2d_archive_corpus_card")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    experiment_root = Path(args.experiment_root)
    archive_dir = experiment_root / args.archive_health_run
    publication_dir = experiment_root / args.publication_bundle_run
    next_dir = experiment_root / args.next_matrix_run
    source_notes_dir = experiment_root / args.source_notes_run

    archive_summary = read_json(archive_dir / "data/experiment_archive_health_summary.json")
    publication_summary = read_json(
        publication_dir / "data/synthetic_2d_publication_figure_bundle_summary.json"
    )
    next_summary = read_json(next_dir / "data/synthetic_2d_next_question_matrix_summary.json")
    source_notes_summary = read_json(
        source_notes_dir / "data/synthetic_publication_source_figure_notes_backfill_summary.json"
    )

    rows = range_rows(archive_summary)
    summary = summarize_corpus(
        rows,
        archive_summary=archive_summary,
        publication_summary=publication_summary,
        next_matrix_summary=next_summary,
        source_notes_summary=source_notes_summary,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root="outputs/summary_tables"))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    range_csv = data_dir / "synthetic_2d_archive_corpus_ranges.csv"
    summary_json = data_dir / "synthetic_2d_archive_corpus_card_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "synthetic_2d_archive_corpus_card.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(range_csv, [json_safe(row) for row in rows])
    plot_corpus_card(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "range_csv": str(range_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, range_csv, summary_json, validation_csv)
    write_run_manifest(
        str(outdir),
        "synthetic_2d_archive_corpus_card",
        {
            "archive_health_run": args.archive_health_run,
            "publication_bundle_run": args.publication_bundle_run,
            "next_matrix_run": args.next_matrix_run,
            "source_notes_run": args.source_notes_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Backfill figure notes for source figures in the synthetic publication bundle."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe  # noqa: E402
from run_synthetic_2d_publication_figure_bundle import DEFAULT_EXPERIMENT_ROOT  # noqa: E402


DEFAULT_BUNDLE_RUN = "1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def support_metric_text(row: dict) -> str:
    return str(row.get("support_metric") or "not recorded")


def figure_notes_text(row: dict, *, bundle_run: str) -> str:
    figure_path = Path(row.get("figure_path", ""))
    return (
        "\n".join(
            [
                "# Figure Notes",
                "",
                f"## `{figure_path.name}`",
                "",
                "This note was backfilled from the current synthetic 2D publication",
                "bundle so the source figure remains interpretable during manuscript",
                "handoff. The image itself was not regenerated.",
                "",
                f"Source run: `{row.get('source_run', '')}`.",
                f"Bundle run: `{bundle_run}`.",
                f"Figure key: `{row.get('figure_key', '')}`.",
                f"Status: `{row.get('status_label', '')}`.",
                f"Support metric: `{support_metric_text(row)}`.",
                "",
                "Paper use:",
                "",
                str(row.get("paper_use") or "synthetic 2D publication support"),
                "",
                "Allowed claim:",
                "",
                str(row.get("allowed_claim") or "not recorded"),
                "",
                "Scope boundary:",
                "",
                str(row.get("prohibited_claim") or "Do not use this source figure to justify a broad GPU sweep."),
                "",
                "This is controlled known-truth synthetic 2D evidence. It does not",
                "create measured-field, 3D, or universal-resolution claims.",
                "",
            ]
        )
        + "\n"
    )


def backfill_source_notes(
    rows: list[dict],
    *,
    bundle_run: str,
    refresh_existing: bool = False,
) -> tuple[list[dict], dict]:
    audit_rows: list[dict] = []
    for row in rows:
        figure_path = Path(row.get("figure_path", ""))
        notes_path = figure_path.parent / "FIGURE_NOTES.md"
        figure_exists = figure_path.is_file()
        notes_existed_before = notes_path.is_file()
        action = "missing_figure"
        if figure_exists:
            if notes_existed_before and not refresh_existing:
                action = "skipped_existing"
            else:
                notes_path.parent.mkdir(parents=True, exist_ok=True)
                notes_path.write_text(
                    figure_notes_text(row, bundle_run=bundle_run),
                    encoding="utf-8",
                )
                action = "refreshed" if notes_existed_before else "generated"
        audit_rows.append(
            {
                "figure_key": row.get("figure_key", ""),
                "source_run": row.get("source_run", ""),
                "figure_path": str(figure_path),
                "figure_exists": figure_exists,
                "figure_notes_path": str(notes_path),
                "notes_existed_before": notes_existed_before,
                "notes_exists_after": notes_path.is_file(),
                "action": action,
            }
        )

    generated = sum(row["action"] == "generated" for row in audit_rows)
    refreshed = sum(row["action"] == "refreshed" for row in audit_rows)
    skipped = sum(row["action"] == "skipped_existing" for row in audit_rows)
    missing = sum(row["action"] == "missing_figure" for row in audit_rows)
    notes_after = sum(bool(row["notes_exists_after"]) for row in audit_rows)
    complete = missing == 0 and notes_after == len(audit_rows)
    summary = {
        "policy_label": (
            "synthetic_publication_source_figure_notes_backfill_complete_skip_existing"
            if complete
            else "synthetic_publication_source_figure_notes_backfill_review_required"
        ),
        "bundle_run": bundle_run,
        "source_figure_count": len(audit_rows),
        "generated_count": generated,
        "refreshed_count": refreshed,
        "skipped_existing_count": skipped,
        "missing_figure_count": missing,
        "notes_present_after_count": notes_after,
        "refresh_existing": refresh_existing,
        "gpu_priority": "none",
        "ready_for_manuscript_handoff": complete,
        "decision": (
            "Use this as a targeted synthetic source-figure notes backfill for "
            "the current publication bundle only. It does not regenerate figures "
            "or justify any GPU run."
        ),
    }
    return audit_rows, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default=DEFAULT_EXPERIMENT_ROOT)
    parser.add_argument("--bundle-run", default=DEFAULT_BUNDLE_RUN)
    parser.add_argument("--refresh-existing", action="store_true")
    parser.add_argument("--run-name", default="synthetic_publication_source_figure_notes_backfill_report")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    experiment_root = Path(args.experiment_root)
    bundle_dir = experiment_root / args.bundle_run
    figure_rows_csv = bundle_dir / "data/synthetic_2d_publication_figure_rows.csv"
    source_rows = read_csv_rows(figure_rows_csv)
    audit_rows, summary = backfill_source_notes(
        source_rows,
        bundle_run=args.bundle_run,
        refresh_existing=args.refresh_existing,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(experiment_root)))
    data_dir = outdir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    audit_csv = data_dir / "synthetic_publication_source_figure_notes_backfill_rows.csv"
    summary_json = data_dir / "synthetic_publication_source_figure_notes_backfill_summary.json"
    write_csv(audit_csv, [json_safe(row) for row in audit_rows])
    summary["paths"] = {
        "source_figure_rows_csv": str(figure_rows_csv),
        "audit_csv": str(audit_csv),
        "summary_json": str(summary_json),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "synthetic_publication_source_figure_notes_backfill",
        {
            "bundle_run": args.bundle_run,
            "source_figure_rows_csv": str(figure_rows_csv),
            "audit_csv": str(audit_csv),
            "summary_json": str(summary_json),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

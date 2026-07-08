#!/usr/bin/env python3
"""Backfill figure notes for source figures in the current field publication bundle."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe  # noqa: E402


DEFAULT_BUNDLE_RUN = "133_gssi51600s_field_publication_claim_bundle_post_signal_contrast_sensitivity"


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
    if row.get("support_metric"):
        return str(row["support_metric"])
    label = str(row.get("metric_label", "")).strip()
    value = str(row.get("metric_value", "")).strip()
    if label and value:
        return f"{label}={value}"
    return label or value or "not recorded"


def figure_notes_text(row: dict, *, dataset_id: str, bundle_run: str) -> str:
    figure_path = Path(row.get("figure_path", ""))
    return (
        "\n".join(
            [
                "# Figure Notes",
                "",
                f"## `{figure_path.name}`",
                "",
                "This note was backfilled from the current measured-field publication",
                "bundle so the source figure remains interpretable during manuscript",
                "handoff. The image itself was not regenerated.",
                "",
                f"Dataset: `{dataset_id}`.",
                f"Source run: `{row.get('source_run', '')}`.",
                f"Bundle run: `{bundle_run}`.",
                f"Figure key: `{row.get('figure_key', '')}`.",
                f"Policy/status: `{row.get('policy_label') or row.get('status_label') or ''}`.",
                f"Support metric: `{support_metric_text(row)}`.",
                "",
                "Allowed use:",
                "",
                str(row.get("allowed_use") or row.get("paper_use") or "field 2D QC support"),
                "",
                "Scope boundary:",
                "",
                "This is measured GSSI 51600S 2D line-profile QC evidence. It",
                "does not create calibrated cover-depth, radius, 3D, absolute",
                "time-zero, or measured-field FWI claims.",
                "",
            ]
        )
        + "\n"
    )


def backfill_source_notes(
    rows: list[dict],
    *,
    dataset_id: str,
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
                    figure_notes_text(row, dataset_id=dataset_id, bundle_run=bundle_run),
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
            "field_publication_source_figure_notes_backfill_complete_skip_existing"
            if complete
            else "field_publication_source_figure_notes_backfill_review_required"
        ),
        "dataset_id": dataset_id,
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
            "Use this as a targeted field source-figure notes backfill for the "
            "current publication bundle only. It does not regenerate figures or "
            "promote field FWI/3D/depth/radius claims."
        ),
    }
    return audit_rows, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--bundle-run", default=DEFAULT_BUNDLE_RUN)
    parser.add_argument("--refresh-existing", action="store_true")
    parser.add_argument("--run-name", default="gssi51600s_field_publication_source_figure_notes_backfill")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    bundle_dir = dataset_root / args.bundle_run
    figure_rows_csv = bundle_dir / "data/field_publication_figure_rows.csv"
    source_rows = read_csv_rows(figure_rows_csv)
    audit_rows, summary = backfill_source_notes(
        source_rows,
        dataset_id=args.dataset_id,
        bundle_run=args.bundle_run,
        refresh_existing=args.refresh_existing,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    audit_csv = data_dir / "field_publication_source_figure_notes_backfill_rows.csv"
    summary_json = data_dir / "field_publication_source_figure_notes_backfill_summary.json"
    write_csv(audit_csv, [json_safe(row) for row in audit_rows])
    summary["paths"] = {
        "source_figure_rows_csv": str(figure_rows_csv),
        "audit_csv": str(audit_csv),
        "summary_json": str(summary_json),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_publication_source_figure_notes_backfill",
        {
            "dataset_id": args.dataset_id,
            "bundle_run": args.bundle_run,
            "source_figure_rows_csv": str(figure_rows_csv),
            "audit_csv": str(audit_csv),
            "summary_json": str(summary_json),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

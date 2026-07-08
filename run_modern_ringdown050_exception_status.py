#!/usr/bin/env python3
"""Summarize open/closed modern ringdown050 weak-exact exceptions."""

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
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import figure_stats  # noqa: E402
from run_gssi_field_profile_repeatability_policy import safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SECONDARY_SUMMARY = (
    "outputs/experiments/1262_coordinate_weak_exact_secondary_confirmation_audit_700_1259/"
    "data/weak_exact_secondary_confirmation_audit_summary.json"
)
DEFAULT_TRIAGE_CSV = (
    "outputs/experiments/1263_coordinate_weak_exact_exception_triage_700_1259/"
    "data/weak_exact_exception_triage.csv"
)
DEFAULT_CLOSURE_SUMMARY = (
    "outputs/experiments/1276_target0_exception_closure_policy/"
    "data/target0_exception_closure_summary.json"
)


def read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: str | Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_run_ids(text: str) -> list[int]:
    out: list[int] = []
    for part in str(text or "").split(","):
        part = part.strip()
        if part:
            out.append(int(part))
    return out


def classify_exception_status(run_id: int, triage_by_id: dict[int, dict], closure_summary: dict) -> dict:
    triage = triage_by_id.get(run_id, {})
    closure_run_ids = set(parse_run_ids(str(closure_summary.get("run_ids", ""))))
    ringdown_value = safe_float(triage.get("ringdown_value"))
    classification = str(triage.get("classification", "untriaged"))
    if run_id in closure_run_ids and closure_summary.get("policy_label") == "target0_exception_closed_by_source_density":
        status = "closed_by_existing_source_density_followup"
        gpu_priority = "none"
    elif classification.startswith("legacy_archive"):
        status = "legacy_archive_no_gpu_priority"
        gpu_priority = "none"
    elif math.isfinite(ringdown_value) and math.isclose(ringdown_value, 0.5, abs_tol=1.0e-9):
        status = "open_modern_exception_candidate"
        gpu_priority = "candidate_narrow_probe"
    else:
        status = "nonmodern_or_untriaged_defer"
        gpu_priority = "defer"
    return {
        "run_id": run_id,
        "ringdown_value": ringdown_value,
        "triage_classification": classification,
        "exception_status": status,
        "gpu_priority": gpu_priority,
        "closure_policy_label": closure_summary.get("policy_label", ""),
        "closure_run_ids": closure_summary.get("run_ids", ""),
    }


def build_exception_rows(secondary_summary: dict, triage_rows: list[dict], closure_summary: dict) -> list[dict]:
    triage_by_id = {int(safe_float(row.get("run_id"), -1)): row for row in triage_rows}
    rows: list[dict] = []
    for target_row in secondary_summary.get("target_policy_rows", []):
        target = int(safe_float(target_row.get("target"), -1))
        exception_ids = parse_run_ids(str(target_row.get("strongest_secondary_nonaccepted_run_ids", "")))
        if not exception_ids:
            rows.append({
                "target": target,
                "target_label": target_row.get("target_label", f"target{target}"),
                "run_id": "",
                "ringdown_value": "",
                "triage_classification": "none",
                "exception_status": "no_secondary_exception",
                "gpu_priority": "none",
                "strongest_secondary_objective": target_row.get("strongest_secondary_objective", ""),
                "strongest_secondary_accepted_fraction": safe_float(
                    target_row.get("strongest_secondary_accepted_fraction")
                ),
                "closure_policy_label": closure_summary.get("policy_label", ""),
                "closure_run_ids": closure_summary.get("run_ids", ""),
            })
            continue
        for run_id in exception_ids:
            status = classify_exception_status(run_id, triage_by_id, closure_summary)
            rows.append({
                "target": target,
                "target_label": target_row.get("target_label", f"target{target}"),
                "strongest_secondary_objective": target_row.get("strongest_secondary_objective", ""),
                "strongest_secondary_accepted_fraction": safe_float(
                    target_row.get("strongest_secondary_accepted_fraction")
                ),
                **status,
            })
    return rows


def summarize_status(rows: list[dict]) -> dict:
    modern_exception_rows = [
        row for row in rows
        if math.isfinite(safe_float(row.get("ringdown_value")))
        and math.isclose(safe_float(row.get("ringdown_value")), 0.5, abs_tol=1.0e-9)
    ]
    open_modern = [row for row in modern_exception_rows if row.get("exception_status") == "open_modern_exception_candidate"]
    closed_modern = [
        row for row in modern_exception_rows
        if row.get("exception_status") == "closed_by_existing_source_density_followup"
    ]
    legacy = [row for row in rows if row.get("exception_status") == "legacy_archive_no_gpu_priority"]
    if open_modern:
        label = "modern_ringdown050_exception_probe_candidate"
        gpu_priority = "candidate_narrow_probe"
    else:
        label = "modern_ringdown050_no_open_exception_gpu_priority_none"
        gpu_priority = "none"
    return {
        "policy_label": label,
        "exception_row_count": len([row for row in rows if row.get("run_id") != ""]),
        "modern_ringdown050_exception_count": len(modern_exception_rows),
        "modern_ringdown050_closed_count": len(closed_modern),
        "modern_ringdown050_open_count": len(open_modern),
        "legacy_exception_count": len(legacy),
        "gpu_priority": gpu_priority,
        "decision": (
            "No modern ringdown050 weak-exact exception remains open after the "
            "target0 source-density closure. Keep legacy ringdown025 run 785 "
            "as an archive caveat, not a local GPU priority."
            if not open_modern
            else "A modern ringdown050 weak-exact exception remains open; only a narrow probe is defensible."
        ),
    }


def plot_status(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = ["closed\nmodern", "open\nmodern", "legacy", "none"]
    counts = [
        summary["modern_ringdown050_closed_count"],
        summary["modern_ringdown050_open_count"],
        summary["legacy_exception_count"],
        sum(1 for row in rows if row.get("exception_status") == "no_secondary_exception"),
    ]
    colors = ["#2f9d55", "#c7302b", "#f58518", "#4c78a8"]

    fig, ax = plt.subplots(figsize=(8.8, 4.8), constrained_layout=True)
    ax.bar(np.arange(len(labels)), counts, color=colors, width=0.58)
    ax.set_xticks(np.arange(len(labels)), labels)
    ax.set_ylabel("target exception rows")
    ax.set_title("Weak-exact exception status after target0 closure")
    ax.grid(axis="y", color="#dddddd", linewidth=0.6)
    fig.suptitle(summary["policy_label"], fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--secondary-summary-json", default=DEFAULT_SECONDARY_SUMMARY)
    parser.add_argument("--triage-csv", default=DEFAULT_TRIAGE_CSV)
    parser.add_argument("--closure-summary-json", default=DEFAULT_CLOSURE_SUMMARY)
    parser.add_argument("--run-name", default="modern_ringdown050_exception_status")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    secondary_summary = read_json(args.secondary_summary_json)
    triage_rows = read_csv_rows(args.triage_csv)
    closure_summary = read_json(args.closure_summary_json)
    rows = build_exception_rows(secondary_summary, triage_rows, closure_summary)
    summary = summarize_status(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "modern_ringdown050_exception_status_rows.csv"
    summary_json = data_dir / "modern_ringdown050_exception_status_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_status(rows, summary, figures_dir / "modern_ringdown050_exception_status.png"))

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        **summary,
        "input_secondary_summary_json": args.secondary_summary_json,
        "input_triage_csv": args.triage_csv,
        "input_closure_summary_json": args.closure_summary_json,
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
        "modern_ringdown050_exception_status",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

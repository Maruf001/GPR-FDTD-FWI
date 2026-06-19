#!/usr/bin/env python3
"""Close the target1 weak-exact policy question from saved CPU summaries."""

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

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402


DEFAULT_TARGET1_AUDIT = (
    "outputs/experiments/1261_target1_weak_exact_objective_audit_700_1259/"
    "data/target1_weak_exact_objective_audit_summary.json"
)
DEFAULT_SECONDARY_AUDIT = (
    "outputs/experiments/1262_coordinate_weak_exact_secondary_confirmation_audit_700_1259/"
    "data/weak_exact_secondary_confirmation_audit_summary.json"
)
DEFAULT_EXCEPTION_TRIAGE = (
    "outputs/experiments/1263_coordinate_weak_exact_exception_triage_700_1259/"
    "data/weak_exact_exception_triage_summary.json"
)
DEFAULT_EXCEPTION_TRIAGE_CSV = (
    "outputs/experiments/1263_coordinate_weak_exact_exception_triage_700_1259/"
    "data/weak_exact_exception_triage.csv"
)
DEFAULT_ARCHIVE_POLICY = (
    "outputs/experiments/1260_archive_objective_policy_700_1259_guarded/"
    "data/archive_objective_policy_summary.json"
)
DEFAULT_TARGET1_SOURCE_DENSITY = (
    "outputs/summary_tables/wk03_experiment_700_1259_holistic_evaluation/"
    "data/target1_source_density_policy_700_1259.csv"
)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def row_by_value(rows: list[dict], key: str, value: str) -> dict:
    for row in rows:
        if str(row.get(key)) == value:
            return row
    return {}


def source_density_context(rows: list[dict]) -> dict:
    total = len(rows)
    all_weak = [row for row in rows if str(row.get("outcome_category")) == "all weak"]
    mixed = [row for row in rows if str(row.get("outcome_category")).startswith("mixed")]
    all_accepted = [row for row in rows if str(row.get("outcome_category")) == "all accepted"]
    exact = [row for row in rows if boolish(row.get("all_exact_geometry"))]
    return {
        "target1_source_density_series_count": total,
        "target1_source_density_all_exact_geometry_count": len(exact),
        "target1_source_density_all_weak_series_count": len(all_weak),
        "target1_source_density_mixed_series_count": len(mixed),
        "target1_source_density_all_accepted_series_count": len(all_accepted),
        "target1_all_weak_series_ids": ";".join(str(row.get("series_id")) for row in all_weak),
    }


def build_evidence_rows(
    target1_audit: dict,
    secondary_audit: dict,
    exception_summary: dict,
    exception_rows: list[dict],
    archive_policy: dict,
    source_density: dict,
) -> list[dict]:
    subset_rows = target1_audit.get("subset_policy_rows", [])
    target_policy_rows = secondary_audit.get("target_policy_rows", [])
    archive_policy_rows = archive_policy.get("policy_rows", [])
    target1_policy = row_by_value(target_policy_rows, "target_label", "target1")
    target1_archive = row_by_value(archive_policy_rows, "target_label", "target1")
    ringdown050 = row_by_value(subset_rows, "subset", "ringdown050")
    modern = row_by_value(subset_rows, "subset", "modern_seed610_552")
    all_subset = row_by_value(subset_rows, "subset", "all")
    target1_exception = row_by_value(exception_rows, "target_label", "target1")

    return [
        {
            "evidence_key": "target1_all_weak_exact",
            "source": DEFAULT_TARGET1_AUDIT,
            "row_count": safe_int(target1_audit.get("all_weak_exact_rows")),
            "base_accepted_count": safe_int(all_subset.get("base_accepted_count")),
            "secondary_objective": "late_high",
            "secondary_accepted_count": safe_int(all_subset.get("late_high_accepted_count")),
            "secondary_total": safe_int(all_subset.get("weak_exact_row_count")),
            "secondary_fraction": (
                safe_int(all_subset.get("late_high_accepted_count"))
                / safe_int(all_subset.get("weak_exact_row_count"), 1)
            ),
            "exception_run_ids": all_subset.get("late_high_nonaccepted_run_ids", ""),
            "policy_role": "archive_context_near_confirmation",
        },
        {
            "evidence_key": "target1_ringdown050_weak_exact",
            "source": DEFAULT_TARGET1_AUDIT,
            "row_count": safe_int(ringdown050.get("weak_exact_row_count")),
            "base_accepted_count": safe_int(ringdown050.get("base_accepted_count")),
            "secondary_objective": "late_high",
            "secondary_accepted_count": safe_int(ringdown050.get("late_high_accepted_count")),
            "secondary_total": safe_int(ringdown050.get("weak_exact_row_count"), 1),
            "secondary_fraction": (
                safe_int(ringdown050.get("late_high_accepted_count"))
                / safe_int(ringdown050.get("weak_exact_row_count"), 1)
            ),
            "exception_run_ids": ringdown050.get("late_high_nonaccepted_run_ids", ""),
            "policy_role": "modern_ringdown050_full_confirmation",
        },
        {
            "evidence_key": "target1_modern_seed610_552",
            "source": DEFAULT_TARGET1_AUDIT,
            "row_count": safe_int(modern.get("weak_exact_row_count")),
            "base_accepted_count": safe_int(modern.get("base_accepted_count")),
            "secondary_objective": "late_high",
            "secondary_accepted_count": safe_int(modern.get("late_high_accepted_count")),
            "secondary_total": safe_int(modern.get("weak_exact_row_count"), 1),
            "secondary_fraction": (
                safe_int(modern.get("late_high_accepted_count"))
                / safe_int(modern.get("weak_exact_row_count"), 1)
            ),
            "exception_run_ids": modern.get("late_high_nonaccepted_run_ids", ""),
            "policy_role": "current_problem_cases_full_confirmation",
        },
        {
            "evidence_key": "cross_target_secondary_policy",
            "source": DEFAULT_SECONDARY_AUDIT,
            "row_count": safe_int(target1_policy.get("weak_exact_row_count")),
            "base_accepted_count": safe_int(target1_policy.get("base_accepted_count")),
            "secondary_objective": target1_policy.get("strongest_secondary_objective", ""),
            "secondary_accepted_count": safe_int(target1_policy.get("strongest_secondary_accepted_count")),
            "secondary_total": safe_int(target1_policy.get("weak_exact_row_count"), 1),
            "secondary_fraction": safe_float(target1_policy.get("strongest_secondary_accepted_fraction")),
            "exception_run_ids": target1_policy.get("strongest_secondary_nonaccepted_run_ids", ""),
            "policy_role": target1_policy.get("policy_label", ""),
        },
        {
            "evidence_key": "guarded_archive_policy",
            "source": DEFAULT_ARCHIVE_POLICY,
            "row_count": safe_int(archive_policy.get("assigned_objective_rows")),
            "base_accepted_count": math.nan,
            "secondary_objective": target1_archive.get("strongest_archive_secondary_objective", ""),
            "secondary_accepted_count": math.nan,
            "secondary_total": math.nan,
            "secondary_fraction": safe_float(target1_archive.get("strongest_archive_accepted_fraction")),
            "exception_run_ids": "",
            "policy_role": "archive_scale_late_high_confirmation",
        },
        {
            "evidence_key": "target1_exception_triage",
            "source": DEFAULT_EXCEPTION_TRIAGE,
            "row_count": safe_int(exception_summary.get("exception_count")),
            "base_accepted_count": 0,
            "secondary_objective": target1_exception.get("best_secondary_objective", ""),
            "secondary_accepted_count": 0,
            "secondary_total": 1,
            "secondary_fraction": 0.0,
            "exception_run_ids": target1_exception.get("run_id", ""),
            "policy_role": target1_exception.get("classification", ""),
        },
        {
            "evidence_key": "target1_source_density_context",
            "source": DEFAULT_TARGET1_SOURCE_DENSITY,
            "row_count": source_density["target1_source_density_series_count"],
            "base_accepted_count": math.nan,
            "secondary_objective": "not_applicable",
            "secondary_accepted_count": math.nan,
            "secondary_total": math.nan,
            "secondary_fraction": math.nan,
            "exception_run_ids": "",
            "policy_role": (
                "source-density series are exact-geometry context even when base margin is weak"
            ),
        },
    ]


def summarize_policy(evidence_rows: list[dict], source_density: dict) -> dict:
    by_key = {row["evidence_key"]: row for row in evidence_rows}
    ringdown = by_key["target1_ringdown050_weak_exact"]
    modern = by_key["target1_modern_seed610_552"]
    exception = by_key["target1_exception_triage"]
    archive = by_key["guarded_archive_policy"]
    ringdown_full = safe_float(ringdown.get("secondary_fraction")) >= 1.0
    modern_full = safe_float(modern.get("secondary_fraction")) >= 1.0
    legacy_only_exception = str(exception.get("policy_role")) == "legacy_archive_exception_no_gpu_priority"
    return {
        "policy_label": "target1_weak_exact_policy_closure",
        "target1_all_weak_exact_rows": safe_int(by_key["target1_all_weak_exact"].get("row_count")),
        "target1_ringdown050_weak_exact_rows": safe_int(ringdown.get("row_count")),
        "target1_ringdown050_late_high_fraction": safe_float(ringdown.get("secondary_fraction")),
        "target1_modern_seed610_552_rows": safe_int(modern.get("row_count")),
        "target1_modern_seed610_552_late_high_fraction": safe_float(modern.get("secondary_fraction")),
        "target1_archive_late_high_fraction": safe_float(archive.get("secondary_fraction")),
        "target1_exception_run_ids": exception.get("exception_run_ids", ""),
        "target1_exception_policy_role": exception.get("policy_role", ""),
        "target1_source_density_series_count": source_density["target1_source_density_series_count"],
        "target1_source_density_all_exact_geometry_count": source_density[
            "target1_source_density_all_exact_geometry_count"
        ],
        "target1_source_density_all_weak_series_count": source_density[
            "target1_source_density_all_weak_series_count"
        ],
        "target1_source_density_all_weak_series_ids": source_density["target1_all_weak_series_ids"],
        "production_gate": "base_margin",
        "diagnostic_confirmation_objective": "late_high",
        "secondary_confirmation_is_replacement_gate": False,
        "ringdown050_policy_closed": ringdown_full,
        "modern_seed610_552_policy_closed": modern_full,
        "legacy_exception_only": legacy_only_exception,
        "ready_for_broad_gpu_queue": False,
        "ready_for_target1_gpu_exception_probe": False,
        "gpu_priority": "none",
        "decision": (
            "Target1 weak-but-exact rows are a confidence-margin issue, not a geometry "
            "recovery failure. Keep the base objective as the production gate and use "
            "late_high only as diagnostic secondary confirmation. Modern ringdown050 "
            "target1 weak-exact rows, including the seed610/seed552 cases, are fully "
            "confirmed by late_high; the only target1 exception is legacy ringdown025 "
            "run 785 with no GPU priority."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "broad_target1_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "broad target1 weak-exact GPU sweep",
            "evidence": "ringdown050 and modern target1 weak-exact rows are late_high-confirmed",
        },
        {
            "gate_key": "target1_exception_probe",
            "ready": summary["ready_for_target1_gpu_exception_probe"],
            "allowed_use": "none",
            "blocked_use": "GPU probe for legacy target1 run 785",
            "evidence": f"exception role={summary['target1_exception_policy_role']}",
        },
        {
            "gate_key": "secondary_objective_as_production_gate",
            "ready": summary["secondary_confirmation_is_replacement_gate"],
            "allowed_use": "none",
            "blocked_use": "replacing base production confidence gate with late_high",
            "evidence": "late_high is diagnostic confirmation only",
        },
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target1-audit", default=DEFAULT_TARGET1_AUDIT)
    parser.add_argument("--secondary-audit", default=DEFAULT_SECONDARY_AUDIT)
    parser.add_argument("--exception-triage", default=DEFAULT_EXCEPTION_TRIAGE)
    parser.add_argument("--exception-triage-csv", default=DEFAULT_EXCEPTION_TRIAGE_CSV)
    parser.add_argument("--archive-policy", default=DEFAULT_ARCHIVE_POLICY)
    parser.add_argument("--source-density-policy", default=DEFAULT_TARGET1_SOURCE_DENSITY)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--run-name", default="target1_weak_exact_policy_closure")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target1_audit = read_json(Path(args.target1_audit))
    secondary_audit = read_json(Path(args.secondary_audit))
    exception_summary = read_json(Path(args.exception_triage))
    exception_rows = read_csv_rows(Path(args.exception_triage_csv))
    archive_policy = read_json(Path(args.archive_policy))
    source_density_rows = read_csv_rows(Path(args.source_density_policy))
    source_density = source_density_context(source_density_rows)
    evidence_rows = build_evidence_rows(
        target1_audit,
        secondary_audit,
        exception_summary,
        exception_rows,
        archive_policy,
        source_density,
    )
    summary = summarize_policy(evidence_rows, source_density)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    evidence_csv = data_dir / "target1_weak_exact_policy_evidence.csv"
    gates_csv = data_dir / "target1_weak_exact_policy_gates.csv"
    summary_json = data_dir / "target1_weak_exact_policy_closure_summary.json"

    write_csv(evidence_csv, [json_safe(row) for row in evidence_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    summary["paths"] = {
        "evidence_csv": str(evidence_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "target1_audit": args.target1_audit,
        "secondary_audit": args.secondary_audit,
        "exception_triage": args.exception_triage,
        "exception_triage_csv": args.exception_triage_csv,
        "archive_policy": args.archive_policy,
        "source_density_policy": args.source_density_policy,
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "target1_weak_exact_policy_closure",
        {
            "summary_json": str(summary_json),
            "evidence_csv": str(evidence_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

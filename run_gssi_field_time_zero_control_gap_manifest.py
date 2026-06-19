#!/usr/bin/env python3
"""Synthesize field timing evidence against the absolute time-zero control gap."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402


DEFAULT_EARLY_RUN = "090_gssi51600s_field_early_time_anchor_audit"
DEFAULT_SCORECARD_RUN = "105_gssi51600s_field_timing_discriminant_scorecard"
DEFAULT_LADDER_RUN = "121_gssi51600s_field_time_zero_ladder_post_leave_one"
DEFAULT_CONTROL_MANIFEST_RUN = "138_gssi51600s_field_existing_data_control_manifest"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def dataset_paths(
    dataset_root: Path,
    early_run: str,
    scorecard_run: str,
    ladder_run: str,
    control_manifest_run: str,
) -> dict[str, Path]:
    return {
        "early_summary": dataset_root
        / early_run
        / "data/field_early_time_anchor_audit_summary.json",
        "early_lags": dataset_root / early_run / "data/field_early_time_pair_lags.csv",
        "scorecard_summary": dataset_root
        / scorecard_run
        / "data/field_timing_discriminant_scorecard_summary.json",
        "scorecard_rows": dataset_root
        / scorecard_run
        / "data/field_timing_discriminant_scorecard_rows.csv",
        "ladder_rows": dataset_root
        / ladder_run
        / "data/field_time_zero_evidence_ladder_rows.csv",
        "control_manifest_summary": dataset_root
        / control_manifest_run
        / "data/field_existing_data_control_manifest_summary.json",
        "control_manifest_rows": dataset_root
        / control_manifest_run
        / "data/field_existing_data_control_manifest_rows.csv",
    }


def row_lookup(rows: list[dict], key_name: str, value: str) -> dict:
    for row in rows:
        if str(row.get(key_name)) == value:
            return row
    return {}


def build_timing_source_rows(
    early_summary: dict,
    scorecard_summary: dict,
    scorecard_rows: list[dict],
    ladder_rows: list[dict],
    control_rows: list[dict],
    paths: dict[str, Path],
) -> list[dict]:
    early_row = row_lookup(scorecard_rows, "timing_discriminant", "early_common_mode")
    short_row = row_lookup(scorecard_rows, "timing_discriminant", "short_content_relative")
    raw_row = row_lookup(scorecard_rows, "timing_discriminant", "raw_no_correction")
    long_row = row_lookup(scorecard_rows, "timing_discriminant", "long_pattern_only")
    ladder_short = row_lookup(ladder_rows, "gate_key", "short_relative_timing_budget")
    absolute_control = row_lookup(control_rows, "axis_key", "absolute_time_zero")

    return [
        {
            "timing_source": "early_common_mode",
            "source_run": DEFAULT_EARLY_RUN,
            "support_count": safe_int(early_row.get("support_count")),
            "row_count": safe_int(early_row.get("row_count")),
            "support_fraction": safe_float(early_row.get("support_fraction")),
            "representative_offset_ns": safe_float(early_row.get("representative_offset_ns")),
            "strength_metric": safe_float(early_row.get("strength_metric")),
            "status": "negative_control_common_mode",
            "absolute_time_zero_candidate": False,
            "allowed_use": early_row.get("allowed_use", "early/direct-wave common-mode timing QC"),
            "blocked_use": "absolute time-zero calibration",
            "evidence": early_summary.get("decision", ""),
            "source_path": str(paths["early_summary"]),
        },
        {
            "timing_source": "short_content_relative",
            "source_run": DEFAULT_LADDER_RUN,
            "support_count": safe_int(short_row.get("support_count")),
            "row_count": safe_int(short_row.get("row_count")),
            "support_fraction": safe_float(short_row.get("support_fraction")),
            "representative_offset_ns": safe_float(scorecard_summary.get("short_nominal_offset_ns")),
            "strength_metric": safe_float(short_row.get("strength_metric")),
            "status": "relative_timing_supported_not_absolute",
            "absolute_time_zero_candidate": False,
            "allowed_use": ladder_short.get("allowed_use", "short-profile relative timing QC"),
            "blocked_use": ladder_short.get("blocked_use", "absolute time-zero or calibrated depth inversion"),
            "evidence": ladder_short.get("evidence", ""),
            "source_path": str(paths["ladder_rows"]),
        },
        {
            "timing_source": "raw_no_correction",
            "source_run": DEFAULT_SCORECARD_RUN,
            "support_count": safe_int(raw_row.get("support_count")),
            "row_count": safe_int(raw_row.get("row_count")),
            "support_fraction": safe_float(raw_row.get("support_fraction")),
            "representative_offset_ns": safe_float(raw_row.get("representative_offset_ns")),
            "strength_metric": safe_float(raw_row.get("strength_metric")),
            "status": "raw_alignment_rejected",
            "absolute_time_zero_candidate": False,
            "allowed_use": raw_row.get("allowed_use", "negative-control baseline"),
            "blocked_use": raw_row.get("blocked_use", "uncorrected short-pair timing support"),
            "evidence": "raw/no-correction scorecard rejects timing support",
            "source_path": str(paths["scorecard_rows"]),
        },
        {
            "timing_source": "long_pattern_only",
            "source_run": DEFAULT_SCORECARD_RUN,
            "support_count": safe_int(long_row.get("support_count")),
            "row_count": safe_int(long_row.get("row_count")),
            "support_fraction": safe_float(long_row.get("support_fraction")),
            "representative_offset_ns": safe_float(scorecard_summary.get("long_best_offset_median_ns")),
            "strength_metric": safe_float(long_row.get("strength_metric")),
            "status": "pattern_only_rejects_short_transfer",
            "absolute_time_zero_candidate": False,
            "allowed_use": long_row.get("allowed_use", "long-profile pattern-only visual QC"),
            "blocked_use": long_row.get("blocked_use", "phase time-zero or 3D inversion"),
            "evidence": "long profile timing remains pattern-only and rejects short transfer",
            "source_path": str(paths["scorecard_rows"]),
        },
        {
            "timing_source": "absolute_time_zero_control",
            "source_run": DEFAULT_CONTROL_MANIFEST_RUN,
            "support_count": 0,
            "row_count": 1,
            "support_fraction": 0.0,
            "representative_offset_ns": math.nan,
            "strength_metric": math.nan,
            "status": "must_have_control_unsatisfied",
            "absolute_time_zero_candidate": False,
            "allowed_use": absolute_control.get("allowed_current_use", "QC/context only"),
            "blocked_use": "field FWI or calibrated depth inversion",
            "evidence": absolute_control.get("existing_evidence", ""),
            "source_path": str(paths["control_manifest_rows"]),
        },
    ]


def summarize_gap(timing_rows: list[dict], early_summary: dict, scorecard_summary: dict, control_summary: dict) -> dict:
    absolute_candidate_count = sum(boolish(row.get("absolute_time_zero_candidate")) for row in timing_rows)
    short_offset = safe_float(scorecard_summary.get("short_nominal_offset_ns"))
    early_offset = safe_float(early_summary.get("short_pair_early_shift_ns"))
    half_width = safe_float(early_summary.get("short_pair_conservative_half_width_ns"))
    delta = abs(short_offset - early_offset) if math.isfinite(short_offset) and math.isfinite(early_offset) else math.nan
    return {
        "policy_label": "gssi51600s_field_time_zero_control_gap_manifest",
        "timing_source_count": len(timing_rows),
        "absolute_time_zero_candidate_count": absolute_candidate_count,
        "relative_short_timing_supported": any(
            row["timing_source"] == "short_content_relative"
            and safe_float(row.get("support_fraction")) >= 1.0
            for row in timing_rows
        ),
        "early_common_mode_negative_control": any(
            row["timing_source"] == "early_common_mode"
            and row["status"] == "negative_control_common_mode"
            for row in timing_rows
        ),
        "short_content_offset_ns": short_offset,
        "early_common_mode_offset_ns": early_offset,
        "short_vs_early_delta_ns": delta,
        "conservative_half_width_ns": half_width,
        "short_vs_early_exceeds_conservative_half_width": (
            delta > half_width if math.isfinite(delta) and math.isfinite(half_width) else True
        ),
        "must_have_controls_satisfied": safe_int(
            control_summary.get("satisfied_must_have_requirement_count")
        ),
        "must_have_controls_total": safe_int(control_summary.get("must_have_requirement_count")),
        "ready_for_absolute_time_zero": False,
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_field_3d_hpc": False,
        "gpu_priority": "none",
        "recommended_next_measurement": (
            "record a repeatable air/direct-wave or metal-plate timing reference per session "
            "and propagate its uncertainty against the short content-backed relative timing ladder"
        ),
        "decision": (
            "Existing field timing evidence supports relative short-profile timing QC but not "
            "absolute time-zero. The early/direct component is a common-mode negative control, "
            "raw uncorrected timing is rejected, and long profiles remain pattern-only. Current "
            "field FWI, heavy field GPU work, and field 3D/HPC remain blocked until an external "
            "absolute timing reference is collected."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "absolute_time_zero_from_current_archive",
            "ready": summary["ready_for_absolute_time_zero"],
            "allowed_use": "none",
            "blocked_use": "absolute time-zero calibration from current archive",
            "evidence": f"absolute candidates={summary['absolute_time_zero_candidate_count']}",
        },
        {
            "gate_key": "current_archive_field_fwi",
            "ready": summary["ready_for_current_archive_field_fwi"],
            "allowed_use": "none",
            "blocked_use": "field FWI or calibrated depth inversion",
            "evidence": (
                f"must-have controls satisfied={summary['must_have_controls_satisfied']}/"
                f"{summary['must_have_controls_total']}"
            ),
        },
        {
            "gate_key": "new_absolute_timing_reference",
            "ready": True,
            "allowed_use": "controlled 2D acquisition planning",
            "blocked_use": "treating planning as current archive calibration",
            "evidence": summary["recommended_next_measurement"],
        },
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--early-run", default=DEFAULT_EARLY_RUN)
    parser.add_argument("--scorecard-run", default=DEFAULT_SCORECARD_RUN)
    parser.add_argument("--ladder-run", default=DEFAULT_LADDER_RUN)
    parser.add_argument("--control-manifest-run", default=DEFAULT_CONTROL_MANIFEST_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_time_zero_control_gap_manifest")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    paths = dataset_paths(
        dataset_root,
        args.early_run,
        args.scorecard_run,
        args.ladder_run,
        args.control_manifest_run,
    )
    early_summary = read_json(paths["early_summary"])
    scorecard_summary = read_json(paths["scorecard_summary"])
    scorecard_rows = read_csv_rows(paths["scorecard_rows"])
    ladder_rows = read_csv_rows(paths["ladder_rows"])
    control_summary = read_json(paths["control_manifest_summary"])
    control_rows = read_csv_rows(paths["control_manifest_rows"])

    timing_rows = build_timing_source_rows(
        early_summary,
        scorecard_summary,
        scorecard_rows,
        ladder_rows,
        control_rows,
        paths,
    )
    summary = summarize_gap(timing_rows, early_summary, scorecard_summary, control_summary)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    timing_csv = data_dir / "field_time_zero_control_gap_timing_sources.csv"
    gates_csv = data_dir / "field_time_zero_control_gap_gates.csv"
    summary_json = data_dir / "field_time_zero_control_gap_summary.json"

    write_csv(timing_csv, [json_safe(row) for row in timing_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    summary["paths"] = {
        "timing_csv": str(timing_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "source_paths": {key: str(value) for key, value in paths.items()},
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi51600s_field_time_zero_control_gap_manifest",
        {
            "summary_json": str(summary_json),
            "timing_csv": str(timing_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

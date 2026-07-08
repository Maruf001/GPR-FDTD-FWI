#!/usr/bin/env python3
"""Validate controlled-2D GSSI field acquisition packet CSVs."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_controlled_2d_acquisition_protocol import boolish, read_csv_rows  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402


DEFAULT_PACKET_RUN = "141_gssi51600s_controlled_2d_packet_builder"
TABLE_NAMES = (
    "session_log",
    "target_truth",
    "profile_geometry",
    "acquisition_run",
    "reference_measurement",
)
REFERENCE_TYPE_REQUIRED_FIELDS = {
    "measured_time_zero_ns": {"air_direct", "metal_plate_t0"},
    "time_zero_uncertainty_ns": {"air_direct", "metal_plate_t0"},
    "amplitude_metric": {"amplitude_reflector"},
    "amplitude_repeatability_pct": {"amplitude_reflector"},
}


def default_paths(dataset_root: Path, packet_run: str) -> dict[str, Path]:
    packet_root = dataset_root / packet_run
    return {
        "packet_root": packet_root,
        "packet_dir": packet_root / "templates",
        "validation_rules": packet_root / "data/controlled_2d_packet_validation_rules.csv",
        "packet_summary": packet_root / "data/controlled_2d_packet_summary.json",
    }


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_packet_tables(packet_dir: Path, table_names: tuple[str, ...] = TABLE_NAMES) -> dict[str, list[dict]]:
    tables = {}
    for table_name in table_names:
        path = packet_dir / f"{table_name}.csv"
        if path.exists():
            tables[table_name] = read_csv_rows(path)
        else:
            tables[table_name] = []
    return tables


def nonempty(value: object) -> bool:
    return str(value if value is not None else "").strip() != ""


def filled_rows(rows: list[dict]) -> list[dict]:
    return [row for row in rows if any(nonempty(value) for value in row.values())]


def dtype_valid(value: object, dtype: str) -> bool:
    text = str(value).strip()
    if not text:
        return True
    if dtype == "string":
        return True
    if dtype == "float":
        try:
            return math.isfinite(float(text))
        except ValueError:
            return False
    if dtype == "integer":
        try:
            number = float(text)
        except ValueError:
            return False
        return math.isfinite(number) and number.is_integer()
    if dtype == "date":
        try:
            date.fromisoformat(text)
        except ValueError:
            return False
        return True
    return True


def required_reference_types(rule: dict) -> set[str] | None:
    explicit = str(rule.get("required_reference_types", "")).strip()
    if explicit:
        return {part.strip() for part in explicit.split(",") if part.strip()}
    return REFERENCE_TYPE_REQUIRED_FIELDS.get(str(rule.get("field_name")))


def required_rule_applies(rule: dict, row: dict) -> bool:
    if str(rule.get("rule_key")) != "required_nonempty":
        return True
    if str(rule.get("table_name")) != "reference_measurement":
        return True
    required_types = required_reference_types(rule)
    if required_types is None:
        return True
    reference_type = str(row.get("reference_type", "")).strip()
    if not reference_type:
        return True
    return reference_type in required_types


def validate_required_rules(tables: dict[str, list[dict]], rules: list[dict]) -> list[dict]:
    findings = []
    for rule in rules:
        table_name = str(rule["table_name"])
        field_name = str(rule["field_name"])
        rows = tables.get(table_name, [])
        if not rows:
            findings.append(
                {
                    "table_name": table_name,
                    "row_index": "",
                    "field_name": field_name,
                    "check_key": "missing_table_rows",
                    "severity": rule.get("severity", "blocking"),
                    "passed": False,
                    "value": "",
                    "expected": "at least one row",
                    "message": f"{table_name}.{field_name} cannot be validated because the table has no rows",
                }
            )
            continue
        for row_index, row in enumerate(rows, start=1):
            value = row.get(field_name, "")
            if (
                rule["rule_key"] == "required_nonempty"
                and required_rule_applies(rule, row)
                and not nonempty(value)
            ):
                findings.append(
                    {
                        "table_name": table_name,
                        "row_index": row_index,
                        "field_name": field_name,
                        "check_key": "required_nonempty",
                        "severity": rule.get("severity", "blocking"),
                        "passed": False,
                        "value": "",
                        "expected": "non-empty value",
                        "message": f"{table_name}.{field_name} is required",
                    }
                )
                continue
            expected_dtype = str(rule.get("expected_dtype", "string"))
            if not dtype_valid(value, expected_dtype):
                findings.append(
                    {
                        "table_name": table_name,
                        "row_index": row_index,
                        "field_name": field_name,
                        "check_key": "dtype_valid",
                        "severity": rule.get("severity", "blocking"),
                        "passed": False,
                        "value": value,
                        "expected": expected_dtype,
                        "message": f"{table_name}.{field_name} must parse as {expected_dtype}",
                    }
                )
    return findings


def id_set(rows: list[dict], field_name: str) -> set[str]:
    return {str(row.get(field_name, "")).strip() for row in rows if nonempty(row.get(field_name))}


def validate_cross_table_links(tables: dict[str, list[dict]]) -> list[dict]:
    findings = []
    filled = {name: filled_rows(rows) for name, rows in tables.items()}
    session_ids = id_set(filled["session_log"], "session_id")
    target_ids = id_set(filled["target_truth"], "target_id")
    profile_ids = id_set(filled["profile_geometry"], "profile_id")
    reference_ids = id_set(filled["reference_measurement"], "reference_id")
    checks = [
        ("profile_geometry", "session_id", session_ids, "session_log.session_id"),
        ("acquisition_run", "session_id", session_ids, "session_log.session_id"),
        ("reference_measurement", "session_id", session_ids, "session_log.session_id"),
        ("acquisition_run", "target_id", target_ids, "target_truth.target_id"),
        ("acquisition_run", "profile_id", profile_ids, "profile_geometry.profile_id"),
        ("acquisition_run", "reference_id_before", reference_ids, "reference_measurement.reference_id"),
        ("acquisition_run", "reference_id_after", reference_ids, "reference_measurement.reference_id"),
    ]
    for table_name, field_name, valid_ids, expected in checks:
        for row_index, row in enumerate(tables.get(table_name, []), start=1):
            value = str(row.get(field_name, "")).strip()
            if not value:
                continue
            if value not in valid_ids:
                findings.append(
                    {
                        "table_name": table_name,
                        "row_index": row_index,
                        "field_name": field_name,
                        "check_key": "cross_table_link",
                        "severity": "blocking",
                        "passed": False,
                        "value": value,
                        "expected": expected,
                        "message": f"{table_name}.{field_name} references missing {expected}",
                    }
                )
    return findings


def table_status_rows(tables: dict[str, list[dict]], rules: list[dict], findings: list[dict]) -> list[dict]:
    rules_by_table = Counter(str(rule["table_name"]) for rule in rules)
    missing_by_table = Counter(
        str(row["table_name"]) for row in findings if row["check_key"] in {"required_nonempty", "missing_table_rows"}
    )
    dtype_by_table = Counter(str(row["table_name"]) for row in findings if row["check_key"] == "dtype_valid")
    cross_by_table = Counter(str(row["table_name"]) for row in findings if row["check_key"] == "cross_table_link")
    return [
        {
            "table_name": table_name,
            "row_count": len(tables.get(table_name, [])),
            "filled_row_count": len(filled_rows(tables.get(table_name, []))),
            "required_rule_count": rules_by_table[table_name],
            "missing_required_count": missing_by_table[table_name],
            "dtype_failure_count": dtype_by_table[table_name],
            "cross_table_failure_count": cross_by_table[table_name],
        }
        for table_name in TABLE_NAMES
    ]


def reference_count(tables: dict[str, list[dict]], reference_types: set[str]) -> int:
    count = 0
    for row in filled_rows(tables.get("reference_measurement", [])):
        if str(row.get("reference_type", "")).strip() not in reference_types:
            continue
        if nonempty(row.get("measured_time_zero_ns")) and nonempty(row.get("time_zero_uncertainty_ns")):
            count += 1
    return count


def amplitude_reference_count(tables: dict[str, list[dict]]) -> int:
    count = 0
    for row in filled_rows(tables.get("reference_measurement", [])):
        if str(row.get("reference_type", "")).strip() != "amplitude_reflector":
            continue
        if nonempty(row.get("amplitude_metric")) and nonempty(row.get("amplitude_repeatability_pct")):
            count += 1
    return count


def repeat_target_count(tables: dict[str, list[dict]], minimum_repeats: int = 3) -> int:
    repeats: dict[str, set[str]] = defaultdict(set)
    for row in filled_rows(tables.get("acquisition_run", [])):
        target_id = str(row.get("target_id", "")).strip()
        repeat_id = str(row.get("repeat_id", "")).strip()
        if target_id and repeat_id:
            repeats[target_id].add(repeat_id)
    return sum(len(values) >= minimum_repeats for values in repeats.values())


def acceptance_status_rows(tables: dict[str, list[dict]], findings: list[dict]) -> list[dict]:
    missing_required = sum(row["check_key"] in {"required_nonempty", "missing_table_rows"} for row in findings)
    dtype_failures = sum(row["check_key"] == "dtype_valid" for row in findings)
    cross_failures = sum(row["check_key"] == "cross_table_link" for row in findings)
    time_zero_refs = reference_count(tables, {"air_direct", "metal_plate_t0"})
    amplitude_refs = amplitude_reference_count(tables)
    repeat_targets = repeat_target_count(tables)
    target_truth_rows = len(filled_rows(tables.get("target_truth", [])))
    status = [
        {
            "gate_key": "required_metadata_fields",
            "ready": missing_required == 0 and dtype_failures == 0,
            "evidence": f"missing_required={missing_required}; dtype_failures={dtype_failures}",
            "blocks_if_fail": "packet acceptance and calibrated field claims",
        },
        {
            "gate_key": "cross_table_links",
            "ready": cross_failures == 0 and missing_required == 0,
            "evidence": f"cross_table_failures={cross_failures}",
            "blocks_if_fail": "profile/target/reference joins and field FWI",
        },
        {
            "gate_key": "target_truth_controls",
            "ready": target_truth_rows >= 1 and missing_required == 0,
            "evidence": f"filled_target_truth_rows={target_truth_rows}",
            "blocks_if_fail": "radius/depth/known-truth field validation",
        },
        {
            "gate_key": "absolute_time_zero_references",
            "ready": time_zero_refs >= 3 and missing_required == 0,
            "evidence": f"time_zero_reference_count={time_zero_refs}",
            "blocks_if_fail": "absolute time-zero and calibrated depth inversion",
        },
        {
            "gate_key": "amplitude_references",
            "ready": amplitude_refs >= 3 and missing_required == 0,
            "evidence": f"amplitude_reference_count={amplitude_refs}",
            "blocks_if_fail": "amplitude-calibrated inversion",
        },
        {
            "gate_key": "short_repeat_redundancy",
            "ready": repeat_targets >= 1 and missing_required == 0,
            "evidence": f"targets_with_at_least_3_repeats={repeat_targets}",
            "blocks_if_fail": "leave-one repeatability and robust field supplement wording",
        },
    ]
    all_ready = all(boolish(row["ready"]) for row in status)
    status.append(
        {
            "gate_key": "field_fwi_or_heavy_work",
            "ready": all_ready,
            "evidence": f"all_packet_gates_ready={all_ready}",
            "blocks_if_fail": "field FWI, heavy field GPU work, and field 3D/HPC",
        }
    )
    return status


def summarize_validation(
    tables: dict[str, list[dict]],
    rules: list[dict],
    findings: list[dict],
    acceptance_rows: list[dict],
    packet_dir: Path,
) -> dict:
    blocking = [row for row in findings if str(row.get("severity")) == "blocking"]
    missing_required = sum(row["check_key"] in {"required_nonempty", "missing_table_rows"} for row in findings)
    dtype_failures = sum(row["check_key"] == "dtype_valid" for row in findings)
    cross_failures = sum(row["check_key"] == "cross_table_link" for row in findings)
    ready = all(boolish(row["ready"]) for row in acceptance_rows)
    return {
        "policy_label": "gssi51600s_controlled_2d_packet_validator",
        "packet_dir": str(packet_dir),
        "table_count": len(tables),
        "total_row_count": sum(len(rows) for rows in tables.values()),
        "filled_row_count": sum(len(filled_rows(rows)) for rows in tables.values()),
        "validation_rule_count": len(rules),
        "required_field_evaluation_count": sum(
            max(1, len(tables.get(str(rule["table_name"]), []))) for rule in rules
        ),
        "blocking_finding_count": len(blocking),
        "missing_required_value_count": missing_required,
        "dtype_failure_count": dtype_failures,
        "cross_table_failure_count": cross_failures,
        "acceptance_gate_count": len(acceptance_rows),
        "ready_for_packet_acceptance": ready,
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_field_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "The controlled-acquisition packet is not ready for field inversion unless all packet "
            "validation and acceptance gates pass. A blank generated packet should fail by design; "
            "field FWI, heavy field GPU work, and field 3D/HPC stay blocked until a filled packet "
            "passes this validator."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--packet-run", default=DEFAULT_PACKET_RUN)
    parser.add_argument("--packet-dir", default=None)
    parser.add_argument("--validation-rules", default=None)
    parser.add_argument("--run-name", default="gssi51600s_controlled_2d_packet_validator")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    paths = default_paths(dataset_root, args.packet_run)
    packet_dir = Path(args.packet_dir) if args.packet_dir else paths["packet_dir"]
    validation_rules = Path(args.validation_rules) if args.validation_rules else paths["validation_rules"]

    tables = load_packet_tables(packet_dir)
    rules = read_csv_rows(validation_rules)
    findings = validate_required_rules(tables, rules) + validate_cross_table_links(tables)
    table_status = table_status_rows(tables, rules, findings)
    acceptance_rows = acceptance_status_rows(tables, findings)
    summary = summarize_validation(tables, rules, findings, acceptance_rows, packet_dir)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    findings_csv = data_dir / "controlled_2d_packet_validation_findings.csv"
    table_status_csv = data_dir / "controlled_2d_packet_table_status.csv"
    acceptance_csv = data_dir / "controlled_2d_packet_acceptance_status.csv"
    summary_json = data_dir / "controlled_2d_packet_validation_summary.json"

    write_csv(findings_csv, [json_safe(row) for row in findings])
    write_csv(table_status_csv, [json_safe(row) for row in table_status])
    write_csv(acceptance_csv, [json_safe(row) for row in acceptance_rows])
    summary["paths"] = {
        "findings_csv": str(findings_csv),
        "table_status_csv": str(table_status_csv),
        "acceptance_csv": str(acceptance_csv),
        "summary_json": str(summary_json),
        "packet_dir": str(packet_dir),
        "validation_rules": str(validation_rules),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi51600s_controlled_2d_packet_validator",
        {
            "summary_json": str(summary_json),
            "findings_csv": str(findings_csv),
            "table_status_csv": str(table_status_csv),
            "acceptance_csv": str(acceptance_csv),
            "packet_dir": str(packet_dir),
            "validation_rules": str(validation_rules),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build reusable controlled-2D GSSI field acquisition packet templates."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_controlled_2d_acquisition_protocol import boolish, read_csv_rows  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json  # noqa: E402


DEFAULT_PROTOCOL_RUN = "140_gssi51600s_controlled_2d_acquisition_protocol"
DEFAULT_CONTROL_RUN = "138_gssi51600s_field_existing_data_control_manifest"
REFERENCE_REQUIRED_TYPE_RULES = {
    "measured_time_zero_ns": "air_direct,metal_plate_t0",
    "time_zero_uncertainty_ns": "air_direct,metal_plate_t0",
    "amplitude_metric": "amplitude_reflector",
    "amplitude_repeatability_pct": "amplitude_reflector",
}


def field_paths(dataset_root: Path) -> dict[str, Path]:
    return {
        "protocol_steps": dataset_root
        / DEFAULT_PROTOCOL_RUN
        / "data/controlled_2d_acquisition_protocol_steps.csv",
        "metadata_schema": dataset_root
        / DEFAULT_PROTOCOL_RUN
        / "data/controlled_2d_acquisition_metadata_schema.csv",
        "acceptance_gates": dataset_root
        / DEFAULT_PROTOCOL_RUN
        / "data/controlled_2d_acquisition_acceptance_gates.csv",
        "protocol_summary": dataset_root
        / DEFAULT_PROTOCOL_RUN
        / "data/controlled_2d_acquisition_protocol_summary.json",
        "existing_evidence_inventory": dataset_root
        / DEFAULT_CONTROL_RUN
        / "data/field_existing_data_evidence_inventory.csv",
        "existing_control_summary": dataset_root
        / DEFAULT_CONTROL_RUN
        / "data/field_existing_data_control_manifest_summary.json",
    }


def schema_by_table(schema_rows: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for row in schema_rows:
        grouped.setdefault(str(row["table_name"]), []).append(row)
    return grouped


def write_template_csv(path: Path, fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({field: "" for field in fields})


def build_templates(schema_rows: list[dict], template_dir: Path) -> list[dict]:
    rows = []
    for table_name, table_rows in sorted(schema_by_table(schema_rows).items()):
        fields = [str(row["field_name"]) for row in table_rows]
        required_fields = [str(row["field_name"]) for row in table_rows if boolish(row["required"])]
        optional_fields = [str(row["field_name"]) for row in table_rows if not boolish(row["required"])]
        template_path = template_dir / f"{table_name}.csv"
        write_template_csv(template_path, fields)
        rows.append(
            {
                "table_name": table_name,
                "template_path": str(template_path),
                "field_count": len(fields),
                "required_field_count": len(required_fields),
                "optional_field_count": len(optional_fields),
                "required_fields": ",".join(required_fields),
                "optional_fields": ",".join(optional_fields),
            }
        )
    return rows


def validation_rules(schema_rows: list[dict]) -> list[dict]:
    rows = []
    for row in schema_rows:
        if not boolish(row["required"]):
            continue
        rows.append(
            {
                "table_name": row["table_name"],
                "field_name": row["field_name"],
                "rule_key": "required_nonempty",
                "expected_dtype": row["dtype"],
                "units": row["units"],
                "required_reference_types": REFERENCE_REQUIRED_TYPE_RULES.get(str(row["field_name"]), "")
                if row["table_name"] == "reference_measurement"
                else "",
                "severity": "blocking",
                "blocks_if_fail": "calibrated field claims, field FWI, heavy field GPU work, and field 3D/HPC",
                "description": row["description"],
            }
        )
    return rows


def evidence_present_map(evidence_rows: list[dict]) -> dict[str, bool]:
    return {str(row.get("evidence_key")): boolish(row.get("present")) for row in evidence_rows}


def current_archive_prefill_limits(evidence_rows: list[dict]) -> list[dict]:
    present = evidence_present_map(evidence_rows)
    return [
        {
            "table_name": "session_log",
            "current_archive_prefill_status": "partial",
            "source_evidence_keys": "raw_file_inventory,parsed_profile_inventory",
            "source_evidence_present": present.get("raw_file_inventory", False)
            and present.get("parsed_profile_inventory", False),
            "usable_from_current_archive": "dataset family, antenna family, scan spacing/profile metadata context",
            "missing_for_controlled_packet": "session id, operator, exact system/software/gain, dielectric setting, calibrated time range",
            "allowed_use": "archive context and QC provenance",
            "blocked_use": "calibrated inversion session control",
        },
        {
            "table_name": "target_truth",
            "current_archive_prefill_status": "blocked",
            "source_evidence_keys": "radius_degeneracy_gates,inversion_blocker_map",
            "source_evidence_present": present.get("radius_degeneracy_gates", False)
            and present.get("inversion_blocker_map", False),
            "usable_from_current_archive": "none for known target radius/depth truth",
            "missing_for_controlled_packet": "surveyed target coordinates, cover depth, radius/diameter, dielectric/velocity, uncertainty",
            "allowed_use": "radius/depth guardrail caveat",
            "blocked_use": "known-truth field radius/depth recovery or field FWI seed",
        },
        {
            "table_name": "profile_geometry",
            "current_archive_prefill_status": "partial",
            "source_evidence_keys": "survey_geometry_metadata,short_anchor_spatial_consistency",
            "source_evidence_present": present.get("survey_geometry_metadata", False)
            and present.get("short_anchor_spatial_consistency", False),
            "usable_from_current_archive": "trace spacing, approximate profile length, relative short-anchor residual context",
            "missing_for_controlled_packet": "surveyed start/end coordinates, target crossings, one profile-to-target coordinate frame",
            "allowed_use": "2D line-profile QC and spatial guardrails",
            "blocked_use": "profile-to-target geometry seeding or 3D/C-scan interpretation",
        },
        {
            "table_name": "acquisition_run",
            "current_archive_prefill_status": "partial",
            "source_evidence_keys": "raw_file_inventory,parsed_profile_inventory",
            "source_evidence_present": present.get("raw_file_inventory", False)
            and present.get("parsed_profile_inventory", False),
            "usable_from_current_archive": "raw DZT/DZX file names and profile-level metadata",
            "missing_for_controlled_packet": "controlled target id, repeat id, Tx/Rx offset confirmation, before/after references",
            "allowed_use": "existing line-profile QC and repeatability/morphology audits",
            "blocked_use": "controlled repeatability or calibrated field inversion",
        },
        {
            "table_name": "reference_measurement",
            "current_archive_prefill_status": "blocked",
            "source_evidence_keys": "time_zero_ladder,relative_signal_contrast_gates",
            "source_evidence_present": present.get("time_zero_ladder", False)
            and present.get("relative_signal_contrast_gates", False),
            "usable_from_current_archive": "relative short-profile timing and relative signal contrast only",
            "missing_for_controlled_packet": "external air/direct-wave or metal-plate time-zero and amplitude-reference repeats",
            "allowed_use": "relative timing and morphology supplement",
            "blocked_use": "absolute time-zero, amplitude calibration, calibrated depth/radius inversion",
        },
    ]


def summarize_packet(
    template_index: list[dict],
    rules: list[dict],
    prefill_rows: list[dict],
    protocol_summary: dict,
    control_summary: dict,
) -> dict:
    partial_prefill_count = sum(row["current_archive_prefill_status"] == "partial" for row in prefill_rows)
    blocked_prefill_count = sum(row["current_archive_prefill_status"] == "blocked" for row in prefill_rows)
    return {
        "policy_label": "gssi51600s_controlled_2d_packet_builder",
        "template_table_count": len(template_index),
        "template_file_count": len(template_index),
        "validation_rule_count": len(rules),
        "required_metadata_field_count": protocol_summary.get("required_metadata_field_count", len(rules)),
        "acceptance_gate_count": protocol_summary.get("acceptance_gate_count"),
        "partial_current_archive_prefill_table_count": partial_prefill_count,
        "blocked_current_archive_prefill_table_count": blocked_prefill_count,
        "current_archive_must_have_controls_satisfied": control_summary.get(
            "satisfied_must_have_requirement_count"
        ),
        "current_archive_must_have_controls_total": control_summary.get("must_have_requirement_count"),
        "ready_for_new_controlled_2d_acquisition": True,
        "ready_for_packet_validation": True,
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_field_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "Use the generated packet templates for a future controlled 2D GSSI acquisition. "
            "The current archive can partially prefill session/profile/acquisition provenance, "
            "but cannot supply target-truth or external reference-measurement controls. Field FWI, "
            "heavy field GPU work, and field 3D/HPC remain blocked until a filled packet passes "
            "the required metadata and acceptance gates."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--run-name", default="gssi51600s_controlled_2d_packet_builder")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    paths = field_paths(dataset_root)
    schema_rows = read_csv_rows(paths["metadata_schema"])
    protocol_summary = read_json(paths["protocol_summary"])
    control_summary = read_json(paths["existing_control_summary"])
    existing_evidence_rows = read_csv_rows(paths["existing_evidence_inventory"])

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    template_dir = outdir / "templates"
    data_dir.mkdir(parents=True, exist_ok=True)
    template_dir.mkdir(parents=True, exist_ok=True)

    template_index = build_templates(schema_rows, template_dir)
    rules = validation_rules(schema_rows)
    prefill_rows = current_archive_prefill_limits(existing_evidence_rows)
    summary = summarize_packet(template_index, rules, prefill_rows, protocol_summary, control_summary)

    template_index_csv = data_dir / "controlled_2d_packet_template_index.csv"
    rules_csv = data_dir / "controlled_2d_packet_validation_rules.csv"
    prefill_csv = data_dir / "controlled_2d_packet_current_archive_prefill_limits.csv"
    summary_json = data_dir / "controlled_2d_packet_summary.json"

    write_csv(template_index_csv, [json_safe(row) for row in template_index])
    write_csv(rules_csv, [json_safe(row) for row in rules])
    write_csv(prefill_csv, [json_safe(row) for row in prefill_rows])
    summary["paths"] = {
        "template_index_csv": str(template_index_csv),
        "validation_rules_csv": str(rules_csv),
        "current_archive_prefill_limits_csv": str(prefill_csv),
        "summary_json": str(summary_json),
        "template_dir": str(template_dir),
        "source_paths": {key: str(value) for key, value in paths.items()},
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi51600s_controlled_2d_packet_builder",
        {
            "summary_json": str(summary_json),
            "template_index_csv": str(template_index_csv),
            "validation_rules_csv": str(rules_csv),
            "current_archive_prefill_limits_csv": str(prefill_csv),
            "template_dir": str(template_dir),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

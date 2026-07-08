#!/usr/bin/env python3
"""Create a controlled 2D field acquisition protocol from current blockers."""

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
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_int  # noqa: E402


DEFAULT_DESIGN_RUN = "137_gssi51600s_field_controlled_acquisition_design"
DEFAULT_CONTROL_RUN = "138_gssi51600s_field_existing_data_control_manifest"
DEFAULT_TIME_ZERO_RUN = "139_gssi51600s_field_time_zero_control_gap_manifest"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def field_paths(dataset_root: Path) -> dict[str, Path]:
    return {
        "design_rows": dataset_root
        / DEFAULT_DESIGN_RUN
        / "data/field_controlled_acquisition_design_rows.csv",
        "control_rows": dataset_root
        / DEFAULT_CONTROL_RUN
        / "data/field_existing_data_control_manifest_rows.csv",
        "control_summary": dataset_root
        / DEFAULT_CONTROL_RUN
        / "data/field_existing_data_control_manifest_summary.json",
        "time_zero_summary": dataset_root
        / DEFAULT_TIME_ZERO_RUN
        / "data/field_time_zero_control_gap_summary.json",
    }


def row_lookup(rows: list[dict], key: str) -> dict[str, dict]:
    return {str(row.get(key)): row for row in rows}


def protocol_steps(design_rows: list[dict], control_rows: list[dict], time_zero_summary: dict) -> list[dict]:
    design = row_lookup(design_rows, "axis_key")
    control = row_lookup(control_rows, "axis_key")
    rows = [
        {
            "step_id": "P01",
            "phase_order": 1,
            "phase": "session_setup",
            "requirement_axis": "session_metadata",
            "priority": "must_have",
            "action": "record session, antenna, system, gain, dielectric setting, scan spacing, and operator metadata before profiles",
            "minimum_record_count": 1,
            "metadata_table": "session_log",
            "acceptance_gate": "session log exists and every required session field is non-empty",
            "failure_response": "do not promote profiles beyond QC/context",
            "downstream_analysis": "all later validation tables join on session_id",
        },
        {
            "step_id": "P02",
            "phase_order": 2,
            "phase": "target_truth",
            "requirement_axis": "radius_seed_or_recovery",
            "priority": "must_have",
            "action": design["radius_seed_or_recovery"]["required_new_measurement"],
            "minimum_record_count": 1,
            "metadata_table": "target_truth",
            "acceptance_gate": design["radius_seed_or_recovery"]["acceptance_gate"],
            "failure_response": control["radius_seed_or_recovery"]["missing_control"],
            "downstream_analysis": design["radius_seed_or_recovery"]["analysis_after_acquisition"],
        },
        {
            "step_id": "P03",
            "phase_order": 3,
            "phase": "material_depth",
            "requirement_axis": "cover_depth_recovery",
            "priority": "must_have",
            "action": design["cover_depth_recovery"]["required_new_measurement"],
            "minimum_record_count": 1,
            "metadata_table": "target_truth",
            "acceptance_gate": design["cover_depth_recovery"]["acceptance_gate"],
            "failure_response": control["cover_depth_recovery"]["missing_control"],
            "downstream_analysis": design["cover_depth_recovery"]["analysis_after_acquisition"],
        },
        {
            "step_id": "P04",
            "phase_order": 4,
            "phase": "timing_reference",
            "requirement_axis": "absolute_time_zero",
            "priority": "must_have",
            "action": time_zero_summary["recommended_next_measurement"],
            "minimum_record_count": 3,
            "metadata_table": "reference_measurement",
            "acceptance_gate": design["absolute_time_zero"]["acceptance_gate"],
            "failure_response": control["absolute_time_zero"]["missing_control"],
            "downstream_analysis": design["absolute_time_zero"]["analysis_after_acquisition"],
        },
        {
            "step_id": "P05",
            "phase_order": 5,
            "phase": "profile_geometry",
            "requirement_axis": "profile_spatial_calibration",
            "priority": "must_have",
            "action": design["profile_spatial_calibration"]["required_new_measurement"],
            "minimum_record_count": 1,
            "metadata_table": "profile_geometry",
            "acceptance_gate": design["profile_spatial_calibration"]["acceptance_gate"],
            "failure_response": control["profile_spatial_calibration"]["missing_control"],
            "downstream_analysis": design["profile_spatial_calibration"]["analysis_after_acquisition"],
        },
        {
            "step_id": "P06",
            "phase_order": 6,
            "phase": "amplitude_reference",
            "requirement_axis": "absolute_amplitude_calibration",
            "priority": "must_have",
            "action": design["absolute_amplitude_calibration"]["required_new_measurement"],
            "minimum_record_count": 3,
            "metadata_table": "reference_measurement",
            "acceptance_gate": design["absolute_amplitude_calibration"]["acceptance_gate"],
            "failure_response": control["absolute_amplitude_calibration"]["missing_control"],
            "downstream_analysis": design["absolute_amplitude_calibration"]["analysis_after_acquisition"],
        },
        {
            "step_id": "P07",
            "phase_order": 7,
            "phase": "controlled_short_profiles",
            "requirement_axis": "leave_one_content_redundancy",
            "priority": "should_have",
            "action": design["leave_one_content_redundancy"]["required_new_measurement"],
            "minimum_record_count": 3,
            "metadata_table": "acquisition_run",
            "acceptance_gate": design["leave_one_content_redundancy"]["acceptance_gate"],
            "failure_response": control["leave_one_content_redundancy"]["missing_control"],
            "downstream_analysis": design["leave_one_content_redundancy"]["analysis_after_acquisition"],
        },
        {
            "step_id": "P08",
            "phase_order": 8,
            "phase": "optional_long_profiles",
            "requirement_axis": "long_profile_transfer",
            "priority": "optional_scope",
            "action": design["long_profile_transfer"]["required_new_measurement"],
            "minimum_record_count": 0,
            "metadata_table": "profile_geometry",
            "acceptance_gate": design["long_profile_transfer"]["acceptance_gate"],
            "failure_response": control["long_profile_transfer"]["missing_control"],
            "downstream_analysis": design["long_profile_transfer"]["analysis_after_acquisition"],
        },
    ]
    return rows


def schema_rows() -> list[dict]:
    required_fields = {
        "session_log": [
            ("dataset_id", "string", "", "dataset/source-family identifier"),
            ("session_id", "string", "", "unique acquisition session identifier"),
            ("date_utc", "date", "", "acquisition date in UTC"),
            ("operator", "string", "", "operator or team"),
            ("antenna_model", "string", "", "antenna model, for example 51600S"),
            ("antenna_serial", "string", "", "antenna serial number if available"),
            ("system", "string", "", "GPR control unit/system"),
            ("software_version", "string", "", "control software version"),
            ("gain_setting", "string", "", "gain setting or gain table identifier"),
            ("dielectric_setting", "float", "epsr", "instrument dielectric setting"),
            ("scan_spacing_m", "float", "m", "nominal trace spacing"),
            ("time_range_ns", "float", "ns", "recorded time window"),
        ],
        "target_truth": [
            ("target_id", "string", "", "unique target identifier"),
            ("material", "string", "", "target material"),
            ("center_x_mm", "float", "mm", "surveyed target x coordinate"),
            ("center_y_mm", "float", "mm", "surveyed target y/crossline coordinate"),
            ("cover_depth_mm", "float", "mm", "measured cover depth"),
            ("diameter_mm", "float", "mm", "measured target diameter"),
            ("radius_mm", "float", "mm", "measured target radius"),
            ("dielectric_epsr", "float", "epsr", "local dielectric estimate"),
            ("velocity_m_per_ns", "float", "m/ns", "velocity calibration"),
            ("measurement_uncertainty_mm", "float", "mm", "truth measurement uncertainty"),
        ],
        "profile_geometry": [
            ("profile_id", "string", "", "unique profile identifier"),
            ("session_id", "string", "", "foreign key into session_log"),
            ("profile_role", "string", "", "short_repeat, long_context, or reference"),
            ("start_x_mm", "float", "mm", "surveyed profile start x"),
            ("start_y_mm", "float", "mm", "surveyed profile start y"),
            ("end_x_mm", "float", "mm", "surveyed profile end x"),
            ("end_y_mm", "float", "mm", "surveyed profile end y"),
            ("scan_direction", "string", "", "surveyed scan direction"),
            ("trace_spacing_mm", "float", "mm", "trace spacing"),
            ("target_ids_crossed", "string", "", "comma-separated target ids"),
        ],
        "acquisition_run": [
            ("file_name", "string", "", "raw DZT or exported data file"),
            ("session_id", "string", "", "foreign key into session_log"),
            ("profile_id", "string", "", "foreign key into profile_geometry"),
            ("repeat_id", "integer", "", "repeat index for the same profile/target"),
            ("target_id", "string", "", "primary controlled target id"),
            ("tx_rx_offset_mm", "float", "mm", "antenna Tx/Rx offset or configured offset"),
            ("coupling_condition", "string", "", "surface/coupling notes"),
            ("reference_id_before", "string", "", "nearest timing/amplitude reference before profile"),
            ("reference_id_after", "string", "", "nearest timing/amplitude reference after profile"),
        ],
        "reference_measurement": [
            ("reference_id", "string", "", "unique reference measurement id"),
            ("session_id", "string", "", "foreign key into session_log"),
            ("reference_type", "string", "", "air_direct, metal_plate_t0, or amplitude_reflector"),
            ("before_after", "string", "", "before, after, or interleaved"),
            ("file_name", "string", "", "raw reference file"),
            ("repeat_id", "integer", "", "repeat index"),
            ("measured_time_zero_ns", "float", "ns", "measured time-zero reference"),
            ("time_zero_uncertainty_ns", "float", "ns", "reference uncertainty"),
            ("amplitude_metric", "float", "", "reference amplitude coefficient"),
            ("amplitude_repeatability_pct", "float", "percent", "repeatability across references"),
        ],
    }
    optional_fields = {
        "session_log": [("weather", "string", "", "field weather/context"), ("notes", "string", "", "free-form notes")],
        "target_truth": [("truth_source", "string", "", "caliper/survey/spec-sheet source")],
        "profile_geometry": [("survey_method", "string", "", "total station/tape/fixture")],
        "acquisition_run": [("notes", "string", "", "profile-specific notes")],
        "reference_measurement": [("expected_response", "string", "", "expected reference event description")],
    }
    rows = []
    for table_name, fields in required_fields.items():
        for name, dtype, units, description in fields:
            rows.append(
                {
                    "table_name": table_name,
                    "field_name": name,
                    "required": True,
                    "dtype": dtype,
                    "units": units,
                    "description": description,
                }
            )
        for name, dtype, units, description in optional_fields.get(table_name, []):
            rows.append(
                {
                    "table_name": table_name,
                    "field_name": name,
                    "required": False,
                    "dtype": dtype,
                    "units": units,
                    "description": description,
                }
            )
    return rows


def acceptance_gates(protocol_rows: list[dict], schema: list[dict]) -> list[dict]:
    required_schema_fields = sum(boolish(row["required"]) for row in schema)
    return [
        {
            "gate_key": "metadata_completeness",
            "ready": True,
            "required_inputs": "session_log,target_truth,profile_geometry,acquisition_run,reference_measurement",
            "acceptance_threshold": f"{required_schema_fields} required metadata fields populated",
            "blocks_if_fail": "all inversion and calibrated field claims",
            "validation_analysis": "schema completeness check before import/QC",
        },
        {
            "gate_key": "absolute_time_zero_reference",
            "ready": True,
            "required_inputs": "reference_measurement rows with air_direct or metal_plate_t0",
            "acceptance_threshold": "uncertainty <= 0.02 ns or explicitly propagated",
            "blocks_if_fail": "absolute time-zero, depth calibration, field FWI",
            "validation_analysis": "rerun time-zero ladder with reference rows",
        },
        {
            "gate_key": "profile_target_geometry",
            "ready": True,
            "required_inputs": "target_truth plus profile_geometry",
            "acceptance_threshold": "single profile-to-target translation residual range < 5 mm",
            "blocks_if_fail": "geometry seeding and field inversion",
            "validation_analysis": "rerun spatial-consistency audit with surveyed coordinates",
        },
        {
            "gate_key": "target_truth_radius_depth",
            "ready": True,
            "required_inputs": "target_truth radius/diameter, cover_depth, dielectric/velocity",
            "acceptance_threshold": "known radius table and travel-time/depth residual <= 5 mm",
            "blocks_if_fail": "radius/depth recovery claims",
            "validation_analysis": "rerun radius, apparent-depth, and hyperbola degeneracy audits",
        },
        {
            "gate_key": "amplitude_reference",
            "ready": True,
            "required_inputs": "reference_measurement rows with amplitude_reflector",
            "acceptance_threshold": "reference amplitude repeatability within 10 percent",
            "blocks_if_fail": "amplitude-calibrated inversion",
            "validation_analysis": "extend signal-contrast checks with absolute amplitude reference",
        },
        {
            "gate_key": "repeatability_redundancy",
            "ready": True,
            "required_inputs": "at least three acquisition_run repeats per controlled short target",
            "acceptance_threshold": "leave-one content-backed timing interval survives repeat removal",
            "blocks_if_fail": "robust field supplement wording",
            "validation_analysis": "rerun leave-one and time-zero ladder audits",
        },
        {
            "gate_key": "current_archive_field_fwi",
            "ready": False,
            "required_inputs": "new controlled acquisition satisfying all must-have gates",
            "acceptance_threshold": "all must-have gates pass after acquisition",
            "blocks_if_fail": "field FWI, heavy GPU field work, field 3D/HPC",
            "validation_analysis": "only then design small synthetic-to-field inversion pilot",
        },
    ]


def template_rows(schema: list[dict]) -> list[dict]:
    rows = []
    for row in schema:
        if not boolish(row["required"]):
            continue
        rows.append(
            {
                "table_name": row["table_name"],
                "field_name": row["field_name"],
                "required": row["required"],
                "units": row["units"],
                "entry_value": "",
                "field_notes": row["description"],
            }
        )
    return rows


def summarize(protocol: list[dict], schema: list[dict], gates: list[dict], control_summary: dict) -> dict:
    must_have_steps = [row for row in protocol if row["priority"] == "must_have"]
    required_fields = [row for row in schema if boolish(row["required"])]
    return {
        "policy_label": "gssi51600s_controlled_2d_acquisition_protocol",
        "protocol_step_count": len(protocol),
        "must_have_protocol_step_count": len(must_have_steps),
        "metadata_table_count": len({row["table_name"] for row in schema}),
        "required_metadata_field_count": len(required_fields),
        "acceptance_gate_count": len(gates),
        "minimum_short_profile_repeats_per_target": 3,
        "ready_for_new_controlled_2d_acquisition": True,
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_field_3d_hpc": False,
        "current_archive_must_have_controls_satisfied": safe_int(
            control_summary.get("satisfied_must_have_requirement_count")
        ),
        "current_archive_must_have_controls_total": safe_int(
            control_summary.get("must_have_requirement_count")
        ),
        "gpu_priority": "none",
        "decision": (
            "Use this protocol to collect a future controlled 2D field validation dataset. "
            "The current archive remains QC/context only; field FWI and heavy GPU work stay "
            "blocked until the new acquisition satisfies timing, geometry, target truth, "
            "depth/material, amplitude, and repeatability gates."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--run-name", default="gssi51600s_controlled_2d_acquisition_protocol")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    paths = field_paths(dataset_root)
    design_rows = read_csv_rows(paths["design_rows"])
    control_rows = read_csv_rows(paths["control_rows"])
    control_summary = read_json(paths["control_summary"])
    time_zero_summary = read_json(paths["time_zero_summary"])

    protocol = protocol_steps(design_rows, control_rows, time_zero_summary)
    schema = schema_rows()
    gates = acceptance_gates(protocol, schema)
    template = template_rows(schema)
    summary = summarize(protocol, schema, gates, control_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    protocol_csv = data_dir / "controlled_2d_acquisition_protocol_steps.csv"
    schema_csv = data_dir / "controlled_2d_acquisition_metadata_schema.csv"
    gates_csv = data_dir / "controlled_2d_acquisition_acceptance_gates.csv"
    template_csv = data_dir / "controlled_2d_acquisition_field_sheet_template.csv"
    summary_json = data_dir / "controlled_2d_acquisition_protocol_summary.json"

    write_csv(protocol_csv, [json_safe(row) for row in protocol])
    write_csv(schema_csv, [json_safe(row) for row in schema])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    write_csv(template_csv, [json_safe(row) for row in template])
    summary["paths"] = {
        "protocol_csv": str(protocol_csv),
        "schema_csv": str(schema_csv),
        "gates_csv": str(gates_csv),
        "template_csv": str(template_csv),
        "summary_json": str(summary_json),
        "source_paths": {key: str(value) for key, value in paths.items()},
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi51600s_controlled_2d_acquisition_protocol",
        {
            "summary_json": str(summary_json),
            "protocol_csv": str(protocol_csv),
            "schema_csv": str(schema_csv),
            "gates_csv": str(gates_csv),
            "template_csv": str(template_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

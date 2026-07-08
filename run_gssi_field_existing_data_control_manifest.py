#!/usr/bin/env python3
"""Map existing local GSSI field data against controlled-acquisition requirements."""

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
from run_gssi_dzt_qc import (  # noqa: E402
    DEFAULT_DATASET_ID,
    DEFAULT_FIELD_ROOT,
    DEFAULT_INPUT_DIR,
    field_dataset_output_root,
)
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402


DEFAULT_QC_RUN = "001_gssi51600s_dzt_qc"
DEFAULT_GEOMETRY_RUN = "015_gssi51600s_survey_geometry_audit"
DEFAULT_SUPPORT_RUN = "113_gssi51600s_field_cue_support_catalog"
DEFAULT_TIME_ZERO_RUN = "121_gssi51600s_field_time_zero_ladder_post_leave_one"
DEFAULT_SPATIAL_RUN = "122_gssi51600s_field_short_anchor_spatial_consistency_audit"
DEFAULT_RADIUS_RUN = "125_gssi51600s_field_short_anchor_radius_degeneracy_audit"
DEFAULT_CONTRAST_RUN = "135_gssi51600s_field_short_anchor_signal_contrast_regime_synthesis"
DEFAULT_BLOCKER_RUN = "136_gssi51600s_field_inversion_blocker_map_post_contrast"
DEFAULT_DESIGN_RUN = "137_gssi51600s_field_controlled_acquisition_design"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def dataset_paths(dataset_root: Path) -> dict[str, Path]:
    return {
        "inventory_csv": dataset_root / DEFAULT_QC_RUN / "data/gssi_dzt_inventory.csv",
        "inventory_summary_json": dataset_root / DEFAULT_QC_RUN / "data/gssi_dzt_qc_summary.json",
        "survey_geometry_csv": dataset_root
        / DEFAULT_GEOMETRY_RUN
        / "data/survey_geometry_audit.csv",
        "support_catalog_csv": dataset_root
        / DEFAULT_SUPPORT_RUN
        / "data/field_cue_support_catalog.csv",
        "support_anchor_csv": dataset_root
        / DEFAULT_SUPPORT_RUN
        / "data/field_support_anchor_catalog.csv",
        "support_summary_json": dataset_root
        / DEFAULT_SUPPORT_RUN
        / "data/field_cue_support_catalog_summary.json",
        "time_zero_rows_csv": dataset_root
        / DEFAULT_TIME_ZERO_RUN
        / "data/field_time_zero_evidence_ladder_rows.csv",
        "time_zero_summary_json": dataset_root
        / DEFAULT_TIME_ZERO_RUN
        / "data/field_time_zero_evidence_ladder_summary.json",
        "spatial_rows_csv": dataset_root
        / DEFAULT_SPATIAL_RUN
        / "data/field_short_anchor_spatial_consistency_rows.csv",
        "spatial_summary_json": dataset_root
        / DEFAULT_SPATIAL_RUN
        / "data/field_short_anchor_spatial_consistency_summary.json",
        "radius_gates_csv": dataset_root
        / DEFAULT_RADIUS_RUN
        / "data/field_short_anchor_radius_degeneracy_gates.csv",
        "radius_summary_json": dataset_root
        / DEFAULT_RADIUS_RUN
        / "data/field_short_anchor_radius_degeneracy_summary.json",
        "contrast_gates_csv": dataset_root
        / DEFAULT_CONTRAST_RUN
        / "data/field_short_anchor_signal_contrast_regime_gates.csv",
        "contrast_summary_json": dataset_root
        / DEFAULT_CONTRAST_RUN
        / "data/field_short_anchor_signal_contrast_regime_summary.json",
        "blocker_rows_csv": dataset_root
        / DEFAULT_BLOCKER_RUN
        / "data/field_inversion_blocker_map_rows.csv",
        "blocker_summary_json": dataset_root
        / DEFAULT_BLOCKER_RUN
        / "data/field_inversion_blocker_map_summary.json",
        "design_rows_csv": dataset_root
        / DEFAULT_DESIGN_RUN
        / "data/field_controlled_acquisition_design_rows.csv",
        "design_summary_json": dataset_root
        / DEFAULT_DESIGN_RUN
        / "data/field_controlled_acquisition_design_summary.json",
    }


def load_optional_json(path: Path) -> dict:
    return read_json(path) if path.exists() else {}


def file_inventory_rows(input_dir: Path, inventory_rows: list[dict]) -> list[dict]:
    dzt_files = sorted(input_dir.glob("*.DZT"))
    dzx_files = sorted(input_dir.glob("*.DZX"))
    profile_lengths = [safe_float(row.get("profile_length_m")) for row in inventory_rows]
    finite_lengths = [value for value in profile_lengths if math.isfinite(value)]
    trace_counts = [safe_int(row.get("traces")) for row in inventory_rows]
    scan_spacings = {
        round(safe_float(row.get("scan_spacing_m")), 6)
        for row in inventory_rows
        if math.isfinite(safe_float(row.get("scan_spacing_m")))
    }
    antenna_frequencies = {
        round(safe_float(row.get("antenna_frequency_mhz")), 3)
        for row in inventory_rows
        if math.isfinite(safe_float(row.get("antenna_frequency_mhz")))
    }
    return [
        {
            "evidence_key": "raw_file_inventory",
            "present": len(dzt_files) > 0,
            "row_count": len(dzt_files),
            "metric_label": "raw DZT/DZX files",
            "metric_value": f"{len(dzt_files)} DZT, {len(dzx_files)} DZX",
            "allowed_use": "field profile QC and repeatability/morphology audits",
            "blocked_use": "3D survey, absolute time-zero, calibrated depth/radius/amplitude inversion",
            "source_path": str(input_dir),
        },
        {
            "evidence_key": "parsed_profile_inventory",
            "present": len(inventory_rows) > 0,
            "row_count": len(inventory_rows),
            "metric_label": "profile metadata",
            "metric_value": (
                f"profiles={len(inventory_rows)}; traces={sum(trace_counts)}; "
                f"length_m={sum(finite_lengths):.3f}; scan_spacing_m={','.join(map(str, sorted(scan_spacings)))}; "
                f"antenna_mhz={','.join(map(str, sorted(antenna_frequencies)))}"
            ),
            "allowed_use": "2D independent line-profile metadata",
            "blocked_use": "surveyed target geometry or 3D/C-scan geometry claim",
            "source_path": "gssi_dzt_inventory.csv",
        },
    ]


def _gate_lookup(rows: list[dict]) -> dict[str, dict]:
    return {str(row.get("gate_key")): row for row in rows}


def _blocker_lookup(rows: list[dict]) -> dict[str, dict]:
    return {str(row.get("axis_key")): row for row in rows}


def evidence_inventory_rows(paths: dict[str, Path], input_dir: Path, loaded: dict[str, object]) -> list[dict]:
    inventory_rows = loaded["inventory_rows"]
    support_anchor_rows = loaded["support_anchor_rows"]
    support_catalog_rows = loaded["support_catalog_rows"]
    time_zero_rows = loaded["time_zero_rows"]
    spatial_rows = loaded["spatial_rows"]
    radius_gates = _gate_lookup(loaded["radius_gate_rows"])
    contrast_gates = _gate_lookup(loaded["contrast_gate_rows"])
    blocker_rows = loaded["blocker_rows"]

    rows = file_inventory_rows(input_dir, inventory_rows)
    rows.extend(
        [
            {
                "evidence_key": "survey_geometry_metadata",
                "present": paths["survey_geometry_csv"].exists(),
                "row_count": len(loaded["survey_geometry_rows"]),
                "metric_label": "DZX-derived scan spacing/profile length",
                "metric_value": "metadata present, target positions not surveyed",
                "allowed_use": "profile-length and trace-spacing QC",
                "blocked_use": "profile-to-target spatial calibration",
                "source_path": str(paths["survey_geometry_csv"]),
            },
            {
                "evidence_key": "support_anchor_catalog",
                "present": len(support_anchor_rows) > 0,
                "row_count": len(support_anchor_rows),
                "metric_label": "short/long anchor catalog",
                "metric_value": (
                    f"claim_supporting={sum(boolish(row.get('is_claim_supporting')) for row in support_anchor_rows)}; "
                    f"cue_rows={len(support_catalog_rows)}"
                ),
                "allowed_use": "relative timing and morphology support",
                "blocked_use": "absolute time-zero, radius, cover-depth, field FWI, or 3D claim",
                "source_path": str(paths["support_anchor_csv"]),
            },
            {
                "evidence_key": "time_zero_ladder",
                "present": any(str(row.get("status")) == "supported" for row in time_zero_rows),
                "row_count": len(time_zero_rows),
                "metric_label": "relative time-zero ladder",
                "metric_value": "; ".join(
                    str(row.get("evidence"))
                    for row in time_zero_rows
                    if row.get("gate_key") == "short_relative_timing_budget"
                ),
                "allowed_use": "short-profile relative time-zero QC",
                "blocked_use": "absolute time-zero or calibrated depth inversion",
                "source_path": str(paths["time_zero_rows_csv"]),
            },
            {
                "evidence_key": "short_anchor_spatial_consistency",
                "present": len(spatial_rows) > 0,
                "row_count": len(spatial_rows),
                "metric_label": "relative anchor residuals",
                "metric_value": (
                    f"max_abs_residual_mm="
                    f"{max([safe_float(row.get('abs_aligned_x_residual_mm')) for row in spatial_rows] or [math.nan]):.3f}"
                ),
                "allowed_use": "relative short-pair spatial consistency QC",
                "blocked_use": "surveyed profile-to-target geometry",
                "source_path": str(paths["spatial_rows_csv"]),
            },
            {
                "evidence_key": "radius_degeneracy_gates",
                "present": paths["radius_gates_csv"].exists(),
                "row_count": len(loaded["radius_gate_rows"]),
                "metric_label": "radius gates",
                "metric_value": f"radius_seed_ready={boolish(radius_gates.get('radius_seed', {}).get('ready'))}",
                "allowed_use": "radius degeneracy caveat/QC",
                "blocked_use": "field radius seed or recovery",
                "source_path": str(paths["radius_gates_csv"]),
            },
            {
                "evidence_key": "relative_signal_contrast_gates",
                "present": paths["contrast_gates_csv"].exists(),
                "row_count": len(loaded["contrast_gate_rows"]),
                "metric_label": "relative signal contrast gates",
                "metric_value": (
                    f"absolute_amplitude_ready="
                    f"{boolish(contrast_gates.get('absolute_amplitude_calibration', {}).get('ready'))}"
                ),
                "allowed_use": "relative morphology contrast QC",
                "blocked_use": "absolute-amplitude calibrated inversion",
                "source_path": str(paths["contrast_gates_csv"]),
            },
            {
                "evidence_key": "inversion_blocker_map",
                "present": paths["blocker_rows_csv"].exists(),
                "row_count": len(blocker_rows),
                "metric_label": "blocker map rows",
                "metric_value": (
                    f"blockers={sum(str(row.get('axis_family')) == 'blocker' for row in blocker_rows)}"
                ),
                "allowed_use": "scope control for field claims",
                "blocked_use": "heavy field FWI before controls",
                "source_path": str(paths["blocker_rows_csv"]),
            },
        ]
    )
    return rows


def axis_evidence(axis_key: str, evidence_rows: list[dict], loaded: dict[str, object]) -> dict:
    evidence = {row["evidence_key"]: row for row in evidence_rows}
    radius_gates = _gate_lookup(loaded["radius_gate_rows"])
    contrast_gates = _gate_lookup(loaded["contrast_gate_rows"])
    time_zero_rows = loaded["time_zero_rows"]
    spatial_rows = loaded["spatial_rows"]
    blocker_lookup = _blocker_lookup(loaded["blocker_rows"])

    if axis_key == "absolute_time_zero":
        partial = any(str(row.get("gate_key")) == "short_relative_timing_budget" for row in time_zero_rows)
        return {
            "archive_evidence_status": "partial_relative_qc_only" if partial else "missing",
            "archive_has_relevant_evidence": partial,
            "archive_satisfies_control": False,
            "existing_evidence": "short-profile relative timing ladder exists",
            "missing_control": "absolute air/direct-wave or metal-plate timing reference per session",
            "primary_source_path": evidence["time_zero_ladder"]["source_path"],
        }
    if axis_key == "profile_spatial_calibration":
        partial = boolish(evidence["survey_geometry_metadata"]["present"]) and len(spatial_rows) > 0
        return {
            "archive_evidence_status": "partial_relative_geometry_qc_only" if partial else "missing",
            "archive_has_relevant_evidence": partial,
            "archive_satisfies_control": False,
            "existing_evidence": "DZX scan spacing/profile length and short-anchor residual audit exist",
            "missing_control": "surveyed profile starts, directions, target coordinates, and trace-to-target transform",
            "primary_source_path": evidence["survey_geometry_metadata"]["source_path"],
        }
    if axis_key == "radius_seed_or_recovery":
        return {
            "archive_evidence_status": "radius_degeneracy_qc_only",
            "archive_has_relevant_evidence": True,
            "archive_satisfies_control": boolish(radius_gates.get("radius_seed", {}).get("ready")),
            "existing_evidence": "radius degeneracy gates quantify non-uniqueness",
            "missing_control": "measured target radius/diameter table before waveform fitting",
            "primary_source_path": evidence["radius_degeneracy_gates"]["source_path"],
        }
    if axis_key == "cover_depth_recovery":
        blocker = blocker_lookup.get("cover_depth_recovery", {})
        return {
            "archive_evidence_status": "apparent_depth_qc_only",
            "archive_has_relevant_evidence": True,
            "archive_satisfies_control": False,
            "existing_evidence": blocker.get("evidence", "apparent-depth scale sanity checks exist"),
            "missing_control": "measured cover depth plus dielectric/velocity calibration for each target zone",
            "primary_source_path": evidence["inversion_blocker_map"]["source_path"],
        }
    if axis_key == "absolute_amplitude_calibration":
        return {
            "archive_evidence_status": "relative_contrast_qc_only",
            "archive_has_relevant_evidence": True,
            "archive_satisfies_control": boolish(
                contrast_gates.get("absolute_amplitude_calibration", {}).get("ready")
            ),
            "existing_evidence": "relative signal-contrast gates exist",
            "missing_control": "reference reflector, gain/coupling log, and amplitude repeatability reference",
            "primary_source_path": evidence["relative_signal_contrast_gates"]["source_path"],
        }
    if axis_key == "leave_one_content_redundancy":
        blocker = blocker_lookup.get("leave_one_content_redundancy", {})
        return {
            "archive_evidence_status": "repeatability_qc_but_not_robust",
            "archive_has_relevant_evidence": True,
            "archive_satisfies_control": False,
            "existing_evidence": blocker.get("evidence", "leave-one audit exists"),
            "missing_control": "at least three independent short-profile repeats per controlled target",
            "primary_source_path": evidence["inversion_blocker_map"]["source_path"],
        }
    if axis_key == "long_profile_transfer":
        blocker = blocker_lookup.get("long_profile_transfer", {})
        return {
            "archive_evidence_status": "pattern_context_only",
            "archive_has_relevant_evidence": True,
            "archive_satisfies_control": False,
            "existing_evidence": blocker.get("evidence", "long profiles are pattern-only context"),
            "missing_control": "surveyed long/short geometry before transfer",
            "primary_source_path": evidence["inversion_blocker_map"]["source_path"],
        }
    if axis_key == "field_fwi":
        return {
            "archive_evidence_status": "blocked_until_controls",
            "archive_has_relevant_evidence": False,
            "archive_satisfies_control": False,
            "existing_evidence": "no calibrated field inversion evidence",
            "missing_control": "all must-have controls must pass first",
            "primary_source_path": evidence["inversion_blocker_map"]["source_path"],
        }
    if axis_key == "field_3d_hpc":
        return {
            "archive_evidence_status": "not_3d_survey",
            "archive_has_relevant_evidence": False,
            "archive_satisfies_control": False,
            "existing_evidence": "current archive is independent 2D line profiles",
            "missing_control": "3D grid/C-scan acquisition geometry",
            "primary_source_path": evidence["parsed_profile_inventory"]["source_path"],
        }
    return {
        "archive_evidence_status": "unmapped",
        "archive_has_relevant_evidence": False,
        "archive_satisfies_control": False,
        "existing_evidence": "not mapped",
        "missing_control": "not mapped",
        "primary_source_path": "",
    }


def requirement_manifest_rows(design_rows: list[dict], evidence_rows: list[dict], loaded: dict[str, object]) -> list[dict]:
    rows = []
    for design in design_rows:
        axis_key = str(design.get("axis_key"))
        evidence = axis_evidence(axis_key, evidence_rows, loaded)
        rows.append(
            {
                "axis_key": axis_key,
                "priority": design.get("priority", ""),
                "phase": design.get("phase", ""),
                "current_archive_ready_from_design": boolish(design.get("currently_ready")),
                "archive_evidence_status": evidence["archive_evidence_status"],
                "archive_has_relevant_evidence": evidence["archive_has_relevant_evidence"],
                "archive_satisfies_control": evidence["archive_satisfies_control"],
                "existing_evidence": evidence["existing_evidence"],
                "missing_control": evidence["missing_control"],
                "required_new_measurement": design.get("required_new_measurement", ""),
                "acceptance_gate": design.get("acceptance_gate", ""),
                "allowed_current_use": "QC/context only"
                if not evidence["archive_satisfies_control"]
                else "control satisfied",
                "blocked_current_use": design.get("paper_role", ""),
                "primary_source_path": evidence["primary_source_path"],
            }
        )
    return rows


def summarize_manifest(
    requirement_rows: list[dict],
    evidence_rows: list[dict],
    inventory_rows: list[dict],
    design_summary: dict,
) -> dict:
    must_have = [row for row in requirement_rows if row["priority"] == "must_have"]
    satisfied_must_have = [row for row in must_have if boolish(row["archive_satisfies_control"])]
    partial_must_have = [
        row
        for row in must_have
        if boolish(row["archive_has_relevant_evidence"]) and not boolish(row["archive_satisfies_control"])
    ]
    profile_lengths = [safe_float(row.get("profile_length_m")) for row in inventory_rows]
    finite_lengths = [value for value in profile_lengths if math.isfinite(value)]
    raw_inventory = {row["evidence_key"]: row for row in evidence_rows}
    return {
        "policy_label": "gssi51600s_existing_data_control_manifest",
        "raw_dzt_count": safe_int(str(raw_inventory.get("raw_file_inventory", {}).get("row_count", 0))),
        "inventory_profile_count": len(inventory_rows),
        "total_profile_length_m": sum(finite_lengths),
        "current_archive_geometry_type": "independent_2d_line_profiles",
        "current_archive_is_3d_survey": False,
        "requirement_count": len(requirement_rows),
        "must_have_requirement_count": len(must_have),
        "satisfied_must_have_requirement_count": len(satisfied_must_have),
        "partial_qc_must_have_requirement_count": len(partial_must_have),
        "missing_or_unsatisfied_must_have_requirement_count": len(must_have) - len(satisfied_must_have),
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_new_controlled_2d_acquisition_design": boolish(
            design_summary.get("ready_for_new_controlled_2d_acquisition_design", True)
        ),
        "ready_for_field_3d_hpc": False,
        "gpu_priority": "none",
        "recommended_next_field_mode": "controlled_2d_acquisition_protocol_or_metadata_collection_not_fwi",
        "decision": (
            "The existing local GSSI archive has useful 2D line-profile QC evidence "
            "(raw DZT/DZX files, relative short-pair timing, morphology, spatial residual, "
            "and relative contrast audits), but it does not satisfy any must-have inversion "
            "control. Use it for field QC/context only; field FWI, heavy field GPU work, "
            "and 3D/HPC field claims remain blocked until a controlled 2D acquisition records "
            "absolute time zero, surveyed target geometry, target radius/depth truth, "
            "dielectric/velocity calibration, and amplitude reference data."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "current_archive_field_fwi",
            "ready": summary["ready_for_current_archive_field_fwi"],
            "allowed_use": "none",
            "blocked_use": "field FWI on current local GSSI archive",
            "evidence": "must-have controls satisfied="
            f"{summary['satisfied_must_have_requirement_count']}/"
            f"{summary['must_have_requirement_count']}",
        },
        {
            "gate_key": "current_archive_heavy_field_work",
            "ready": summary["ready_for_current_archive_heavy_field_work"],
            "allowed_use": "none",
            "blocked_use": "GPU-heavy field inversion or broad field run",
            "evidence": "archive supports QC/context only",
        },
        {
            "gate_key": "new_controlled_2d_acquisition_design",
            "ready": summary["ready_for_new_controlled_2d_acquisition_design"],
            "allowed_use": "controlled 2D acquisition planning/protocol",
            "blocked_use": "treating current archive as calibrated inversion data",
            "evidence": "run137 controls mapped to existing-data gaps",
        },
        {
            "gate_key": "field_3d_hpc",
            "ready": summary["ready_for_field_3d_hpc"],
            "allowed_use": "none",
            "blocked_use": "3D/HPC field workload from current archive",
            "evidence": "current data are independent 2D line profiles, not a 3D survey",
        },
    ]


def load_inputs(paths: dict[str, Path]) -> dict[str, object]:
    return {
        "inventory_rows": read_csv_rows(paths["inventory_csv"]),
        "inventory_summary": load_optional_json(paths["inventory_summary_json"]),
        "survey_geometry_rows": read_csv_rows(paths["survey_geometry_csv"]),
        "support_catalog_rows": read_csv_rows(paths["support_catalog_csv"]),
        "support_anchor_rows": read_csv_rows(paths["support_anchor_csv"]),
        "support_summary": load_optional_json(paths["support_summary_json"]),
        "time_zero_rows": read_csv_rows(paths["time_zero_rows_csv"]),
        "time_zero_summary": load_optional_json(paths["time_zero_summary_json"]),
        "spatial_rows": read_csv_rows(paths["spatial_rows_csv"]),
        "spatial_summary": load_optional_json(paths["spatial_summary_json"]),
        "radius_gate_rows": read_csv_rows(paths["radius_gates_csv"]),
        "radius_summary": load_optional_json(paths["radius_summary_json"]),
        "contrast_gate_rows": read_csv_rows(paths["contrast_gates_csv"]),
        "contrast_summary": load_optional_json(paths["contrast_summary_json"]),
        "blocker_rows": read_csv_rows(paths["blocker_rows_csv"]),
        "blocker_summary": load_optional_json(paths["blocker_summary_json"]),
        "design_rows": read_csv_rows(paths["design_rows_csv"]),
        "design_summary": load_optional_json(paths["design_summary_json"]),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--run-name", default="gssi51600s_field_existing_data_control_manifest")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    paths = dataset_paths(dataset_root)
    loaded = load_inputs(paths)
    evidence_rows = evidence_inventory_rows(paths, input_dir, loaded)
    requirement_rows = requirement_manifest_rows(loaded["design_rows"], evidence_rows, loaded)
    summary = summarize_manifest(
        requirement_rows,
        evidence_rows,
        loaded["inventory_rows"],
        loaded["design_summary"],
    )
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    evidence_csv = data_dir / "field_existing_data_evidence_inventory.csv"
    requirement_csv = data_dir / "field_existing_data_control_manifest_rows.csv"
    gates_csv = data_dir / "field_existing_data_control_manifest_gates.csv"
    summary_json = data_dir / "field_existing_data_control_manifest_summary.json"

    write_csv(evidence_csv, [json_safe(row) for row in evidence_rows])
    write_csv(requirement_csv, [json_safe(row) for row in requirement_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    summary["paths"] = {
        "evidence_csv": str(evidence_csv),
        "requirement_csv": str(requirement_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "input_dir": str(input_dir),
        "dataset_root": str(dataset_root),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi51600s_field_existing_data_control_manifest",
        {
            "summary_json": str(summary_json),
            "requirement_csv": str(requirement_csv),
            "evidence_csv": str(evidence_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

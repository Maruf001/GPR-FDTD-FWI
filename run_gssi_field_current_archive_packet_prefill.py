#!/usr/bin/env python3
"""Prefill controlled-2D packet provenance from the current local GSSI archive."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_controlled_2d_acquisition_protocol import read_csv_rows  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import safe_float  # noqa: E402


DEFAULT_PACKET_RUN = "141_gssi51600s_controlled_2d_packet_builder"
DEFAULT_INVENTORY_RUN = "001_gssi51600s_dzt_qc"
DEFAULT_SURVEY_RUN = "015_gssi51600s_survey_geometry_audit"
SESSION_ID = "local_gssi_51600s_2026_06_09_archive_prefill"


def field_paths(dataset_root: Path) -> dict[str, Path]:
    return {
        "template_index": dataset_root
        / DEFAULT_PACKET_RUN
        / "data/controlled_2d_packet_template_index.csv",
        "validation_rules": dataset_root
        / DEFAULT_PACKET_RUN
        / "data/controlled_2d_packet_validation_rules.csv",
        "inventory": dataset_root / DEFAULT_INVENTORY_RUN / "data/gssi_dzt_inventory.csv",
        "survey_geometry": dataset_root / DEFAULT_SURVEY_RUN / "data/survey_geometry_audit.csv",
    }


def read_header(path: Path) -> list[str]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        return next(reader)


def template_fields(template_index: list[dict]) -> dict[str, list[str]]:
    fields = {}
    for row in template_index:
        fields[str(row["table_name"])] = read_header(Path(row["template_path"]))
    return fields


def blank_row(fields: list[str]) -> dict:
    return {field: "" for field in fields}


def first_consistent(rows: list[dict], field_name: str) -> str:
    values = {str(row.get(field_name, "")).strip() for row in rows if str(row.get(field_name, "")).strip()}
    return values.pop() if len(values) == 1 else ""


def dataset_date(dataset_id: str) -> str:
    match = re.search(r"(\d{4})_(\d{2})_(\d{2})", dataset_id)
    if not match:
        return ""
    return "-".join(match.groups())


def profile_id_from_file(file_name: str) -> str:
    stem = Path(str(file_name)).stem
    return re.sub(r"[^A-Za-z0-9_]+", "_", stem)


def mm_from_m(value: object) -> str:
    number = safe_float(value)
    if not math.isfinite(number):
        return ""
    return f"{number * 1000.0:.6g}"


def build_session_log(fields: list[str], inventory_rows: list[dict], dataset_id: str) -> list[dict]:
    row = blank_row(fields)
    row.update(
        {
            "dataset_id": dataset_id,
            "session_id": SESSION_ID,
            "date_utc": dataset_date(dataset_id),
            "antenna_model": first_consistent(inventory_rows, "antenna_name"),
            "system": first_consistent(inventory_rows, "dzx_system"),
            "software_version": first_consistent(inventory_rows, "dzx_software_version"),
            "dielectric_setting": first_consistent(inventory_rows, "dielectric"),
            "scan_spacing_m": first_consistent(inventory_rows, "scan_spacing_m"),
            "time_range_ns": first_consistent(inventory_rows, "time_range_ns"),
            "notes": (
                "Prefilled from existing parsed GSSI archive provenance only; "
                "not a controlled acquisition session log."
            ),
        }
    )
    return [row]


def build_profile_geometry(fields: list[str], survey_rows: list[dict]) -> list[dict]:
    rows = []
    for survey in survey_rows:
        row = blank_row(fields)
        row.update(
            {
                "profile_id": profile_id_from_file(str(survey.get("file", ""))),
                "session_id": SESSION_ID,
                "profile_role": "existing_archive_2d_line",
                "trace_spacing_mm": mm_from_m(survey.get("scan_spacing_m")),
                "survey_method": (
                    "DZX trace spacing/profile length only; no surveyed target crossing or "
                    "profile-to-target coordinate frame."
                ),
            }
        )
        rows.append(row)
    return rows


def build_acquisition_run(fields: list[str], inventory_rows: list[dict]) -> list[dict]:
    rows = []
    for repeat_index, inventory in enumerate(inventory_rows, start=1):
        row = blank_row(fields)
        row.update(
            {
                "file_name": inventory.get("file", ""),
                "session_id": SESSION_ID,
                "profile_id": profile_id_from_file(str(inventory.get("file", ""))),
                "repeat_id": repeat_index,
                "notes": (
                    "Existing archive profile provenance. Controlled target id, Tx/Rx offset, "
                    "and timing/amplitude references were not recorded."
                ),
            }
        )
        rows.append(row)
    return rows


def build_packet(fields: dict[str, list[str]], inventory_rows: list[dict], survey_rows: list[dict], dataset_id: str) -> dict[str, list[dict]]:
    return {
        "session_log": build_session_log(fields["session_log"], inventory_rows, dataset_id),
        "target_truth": [blank_row(fields["target_truth"])],
        "profile_geometry": build_profile_geometry(fields["profile_geometry"], survey_rows),
        "acquisition_run": build_acquisition_run(fields["acquisition_run"], inventory_rows),
        "reference_measurement": [blank_row(fields["reference_measurement"])],
    }


def prefill_status_rows(packet: dict[str, list[dict]]) -> list[dict]:
    return [
        {
            "table_name": table_name,
            "row_count": len(rows),
            "filled_row_count": sum(any(str(value).strip() for value in row.values()) for row in rows),
            "prefill_scope": {
                "session_log": "partial archive provenance",
                "target_truth": "left blank: no known target truth in current archive",
                "profile_geometry": "partial DZX trace-spacing/profile identifiers only",
                "acquisition_run": "partial raw-profile provenance only",
                "reference_measurement": "left blank: no external time-zero or amplitude reference",
            }[table_name],
        }
        for table_name, rows in packet.items()
    ]


def summarize(packet: dict[str, list[dict]], validation_rules_path: Path, packet_dir: Path) -> dict:
    status = prefill_status_rows(packet)
    return {
        "policy_label": "gssi51600s_current_archive_packet_prefill",
        "template_table_count": len(packet),
        "total_packet_rows": sum(len(rows) for rows in packet.values()),
        "filled_packet_rows": sum(row["filled_row_count"] for row in status),
        "session_rows_prefilled": status[0]["filled_row_count"],
        "profile_rows_prefilled": next(row["filled_row_count"] for row in status if row["table_name"] == "profile_geometry"),
        "acquisition_rows_prefilled": next(row["filled_row_count"] for row in status if row["table_name"] == "acquisition_run"),
        "target_truth_rows_prefilled": next(row["filled_row_count"] for row in status if row["table_name"] == "target_truth"),
        "reference_rows_prefilled": next(row["filled_row_count"] for row in status if row["table_name"] == "reference_measurement"),
        "ready_for_packet_validation": True,
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_field_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "Current archive provenance can prefill session, profile, and acquisition-run packet rows, "
            "but target-truth and external reference-measurement controls remain blank. Validate this "
            "partially filled packet to quantify remaining blockers; do not treat it as field-FWI ready."
        ),
        "paths": {
            "packet_dir": str(packet_dir),
            "validation_rules": str(validation_rules_path),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--run-name", default="gssi51600s_current_archive_packet_prefill")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    paths = field_paths(dataset_root)
    template_index = read_csv_rows(paths["template_index"])
    inventory_rows = read_csv_rows(paths["inventory"])
    survey_rows = read_csv_rows(paths["survey_geometry"])
    fields = template_fields(template_index)
    packet = build_packet(fields, inventory_rows, survey_rows, args.dataset_id)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    packet_dir = outdir / "packet"
    data_dir = outdir / "data"
    packet_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    for table_name, rows in packet.items():
        write_csv(packet_dir / f"{table_name}.csv", [json_safe(row) for row in rows])

    status = prefill_status_rows(packet)
    status_csv = data_dir / "current_archive_packet_prefill_status.csv"
    summary_json = data_dir / "current_archive_packet_prefill_summary.json"
    write_csv(status_csv, [json_safe(row) for row in status])
    summary = summarize(packet, paths["validation_rules"], packet_dir)
    summary["paths"].update(
        {
            "status_csv": str(status_csv),
            "summary_json": str(summary_json),
            "source_paths": {key: str(value) for key, value in paths.items()},
        }
    )
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi51600s_current_archive_packet_prefill",
        {
            "summary_json": str(summary_json),
            "status_csv": str(status_csv),
            "packet_dir": str(packet_dir),
            "validation_rules": str(paths["validation_rules"]),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

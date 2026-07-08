#!/usr/bin/env python3
"""Build a collection-ready scaffold for the next controlled 2D GSSI packet."""

from __future__ import annotations

import argparse
import csv
import json
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

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import boolish, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_PACKET_TEMPLATE_RUN = "141_gssi51600s_controlled_2d_packet_builder"
DEFAULT_BLOCKER_RUN = "146_gssi51600s_controlled_packet_blocker_prioritization"

TABLE_ORDER = (
    "session_log",
    "target_truth",
    "profile_geometry",
    "acquisition_run",
    "reference_measurement",
)

MEASURED_OR_SESSION_FIELDS = {
    "session_log": {"date_utc", "operator", "antenna_serial", "software_version", "gain_setting", "time_range_ns", "weather"},
    "target_truth": {
        "material",
        "center_x_mm",
        "center_y_mm",
        "cover_depth_mm",
        "diameter_mm",
        "radius_mm",
        "dielectric_epsr",
        "velocity_m_per_ns",
        "measurement_uncertainty_mm",
        "truth_source",
    },
    "profile_geometry": {"start_x_mm", "start_y_mm", "end_x_mm", "end_y_mm", "scan_direction", "trace_spacing_mm", "survey_method"},
    "acquisition_run": {"file_name", "tx_rx_offset_mm", "coupling_condition", "notes"},
    "reference_measurement": {
        "file_name",
        "measured_time_zero_ns",
        "time_zero_uncertainty_ns",
        "amplitude_metric",
        "amplitude_repeatability_pct",
        "expected_response",
    },
}


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def template_fields(template_dir: Path) -> dict[str, list[str]]:
    fields = {}
    for table_name in TABLE_ORDER:
        with (template_dir / f"{table_name}.csv").open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            fields[table_name] = list(reader.fieldnames or [])
    return fields


def blank_row(fields: list[str]) -> dict:
    return {field: "" for field in fields}


def build_scaffold_tables(
    fields_by_table: dict[str, list[str]],
    *,
    dataset_id: str,
    reference_repeat_gate: int,
) -> dict[str, list[dict]]:
    session_id = "planned_controlled_2d_session_001"
    target_id = "T_CONTROL_001"
    profile_id = "P_CONTROL_001"
    time_zero_ids = [f"T0_REF_{idx:03d}" for idx in range(1, reference_repeat_gate + 1)]
    amplitude_ids = [f"AMP_REF_{idx:03d}" for idx in range(1, reference_repeat_gate + 1)]

    session = blank_row(fields_by_table["session_log"])
    session.update(
        {
            "dataset_id": dataset_id,
            "session_id": session_id,
            "antenna_model": "51600S",
            "system": "SIR4K",
            "dielectric_setting": "2.25",
            "scan_spacing_m": "0.003333",
            "notes": "PLANNED SCAFFOLD ONLY: fill measured/session fields during controlled acquisition before validation.",
        }
    )

    target = blank_row(fields_by_table["target_truth"])
    target.update({"target_id": target_id})

    profile = blank_row(fields_by_table["profile_geometry"])
    profile.update(
        {
            "profile_id": profile_id,
            "session_id": session_id,
            "profile_role": "short_repeat_control",
            "target_ids_crossed": target_id,
        }
    )

    acquisition_rows = []
    for idx in range(1, reference_repeat_gate + 1):
        row = blank_row(fields_by_table["acquisition_run"])
        row.update(
            {
                "session_id": session_id,
                "profile_id": profile_id,
                "repeat_id": str(idx),
                "target_id": target_id,
                "reference_id_before": time_zero_ids[(idx - 1) % len(time_zero_ids)],
                "reference_id_after": amplitude_ids[(idx - 1) % len(amplitude_ids)],
            }
        )
        acquisition_rows.append(row)

    reference_rows = []
    for idx, reference_id in enumerate(time_zero_ids, start=1):
        row = blank_row(fields_by_table["reference_measurement"])
        row.update(
            {
                "reference_id": reference_id,
                "session_id": session_id,
                "reference_type": "metal_plate_t0",
                "before_after": "before" if idx == 1 else "interleaved",
                "repeat_id": str(idx),
            }
        )
        reference_rows.append(row)
    for idx, reference_id in enumerate(amplitude_ids, start=1):
        row = blank_row(fields_by_table["reference_measurement"])
        row.update(
            {
                "reference_id": reference_id,
                "session_id": session_id,
                "reference_type": "amplitude_reflector",
                "before_after": "after" if idx == reference_repeat_gate else "interleaved",
                "repeat_id": str(idx),
            }
        )
        reference_rows.append(row)

    return {
        "session_log": [session],
        "target_truth": [target],
        "profile_geometry": [profile],
        "acquisition_run": acquisition_rows,
        "reference_measurement": reference_rows,
    }


def measured_blank_count(table_name: str, rows: list[dict]) -> int:
    measured_fields = MEASURED_OR_SESSION_FIELDS.get(table_name, set())
    return sum(1 for row in rows for field in measured_fields if field in row and str(row.get(field, "")).strip() == "")


def scaffold_status_rows(tables: dict[str, list[dict]]) -> list[dict]:
    rows = []
    for table_name in TABLE_ORDER:
        table_rows = tables[table_name]
        identifier_fields = [
            field
            for field in ("session_id", "target_id", "profile_id", "reference_id", "repeat_id")
            if field in table_rows[0]
        ]
        rows.append(
            {
                "table_name": table_name,
                "row_count": len(table_rows),
                "identifier_fields": ",".join(identifier_fields),
                "planned_identifier_count": sum(
                    1
                    for row in table_rows
                    for field in identifier_fields
                    if str(row.get(field, "")).strip() != ""
                ),
                "measured_or_session_blank_count": measured_blank_count(table_name, table_rows),
                "scaffold_status": "planned_ids_only_not_validated_data",
            }
        )
    return rows


def collection_task_rows(action_rows: list[dict], tables: dict[str, list[dict]]) -> list[dict]:
    rows = []
    id_map = {
        "target_truth_geometry": "T_CONTROL_001",
        "time_zero_reference": ",".join(row["reference_id"] for row in tables["reference_measurement"] if row["reference_type"] == "metal_plate_t0"),
        "amplitude_reference": ",".join(row["reference_id"] for row in tables["reference_measurement"] if row["reference_type"] == "amplitude_reflector"),
        "profile_target_geometry": "P_CONTROL_001",
        "acquisition_control_links": ",".join(row["repeat_id"] for row in tables["acquisition_run"]),
        "session_metadata": "planned_controlled_2d_session_001",
        "reference_registry": ",".join(row["reference_id"] for row in tables["reference_measurement"]),
    }
    for action in action_rows:
        group = str(action["blocker_group"])
        rows.append(
            {
                "priority": safe_int(action["priority"]),
                "blocker_group": group,
                "action_type": action["action_type"],
                "planned_ids_or_repeats": id_map.get(group, ""),
                "minimum_rows_or_repeats": action["minimum_rows_or_repeats"],
                "reference_uncertainty_gate_ns": action.get("reference_uncertainty_gate_ns", ""),
                "reference_depth_equivalent_mm": action.get("reference_depth_equivalent_mm", ""),
                "fields_to_fill": action["field_names"],
                "requires_new_controlled_data": boolish(action["requires_new_controlled_data"]),
                "action": action["action"],
            }
        )
    return sorted(rows, key=lambda row: safe_int(row["priority"]))


def write_packet_tables(packet_dir: Path, tables: dict[str, list[dict]]) -> None:
    packet_dir.mkdir(parents=True, exist_ok=True)
    for table_name in TABLE_ORDER:
        write_csv(packet_dir / f"{table_name}.csv", tables[table_name])


def summarize_scaffold(
    tables: dict[str, list[dict]],
    status_rows: list[dict],
    task_rows: list[dict],
    blocker_summary: dict,
) -> dict:
    t0_refs = [row for row in tables["reference_measurement"] if row["reference_type"] in {"air_direct", "metal_plate_t0"}]
    amp_refs = [row for row in tables["reference_measurement"] if row["reference_type"] == "amplitude_reflector"]
    blank_count = sum(safe_int(row["measured_or_session_blank_count"]) for row in status_rows)
    return {
        "policy_label": "gssi51600s_controlled_collection_scaffold",
        "source_blocker_run": DEFAULT_BLOCKER_RUN,
        "packet_table_count": len(TABLE_ORDER),
        "packet_row_count": sum(len(rows) for rows in tables.values()),
        "planned_session_count": len(tables["session_log"]),
        "planned_target_count": len(tables["target_truth"]),
        "planned_profile_count": len(tables["profile_geometry"]),
        "planned_acquisition_repeat_count": len(tables["acquisition_run"]),
        "planned_time_zero_reference_count": len(t0_refs),
        "planned_amplitude_reference_count": len(amp_refs),
        "reference_repeat_gate": blocker_summary.get("reference_repeat_gate"),
        "reference_uncertainty_gate_ns": blocker_summary.get("reference_uncertainty_gate_ns"),
        "reference_uncertainty_gate_depth_error_mm": blocker_summary.get("reference_uncertainty_gate_depth_error_mm"),
        "action_group_count": len(task_rows),
        "new_controlled_data_action_group_count": sum(boolish(row["requires_new_controlled_data"]) for row in task_rows),
        "measured_or_session_blank_count": blank_count,
        "planned_identifiers_only": True,
        "validator_expected_to_pass": False,
        "ready_for_collection": True,
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_field_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "Use the scaffold as a controlled field collection worksheet only. It proposes stable "
            "session/target/profile/reference IDs and the minimum repeat structure, while leaving "
            "measured target, reference, survey, Tx/Rx, coupling, and session fields blank. Fill the "
            "packet from actual controlled data and rerun the validator before any field inversion."
        ),
    }


def plot_scaffold(status_rows: list[dict], task_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(15.0, 5.4), constrained_layout=True)
    table_names = [row["table_name"] for row in status_rows]
    row_counts = [safe_int(row["row_count"]) for row in status_rows]
    blank_counts = [safe_int(row["measured_or_session_blank_count"]) for row in status_rows]
    x = range(len(table_names))
    axes[0].bar(x, row_counts, width=0.55, color="#4c78a8", label="scaffold rows")
    axes[0].plot(x, blank_counts, marker="o", linewidth=2.0, color="#e45756", label="blank measured/session fields")
    axes[0].set_xticks(list(x), [name.replace("_", "\n") for name in table_names], fontsize=8)
    axes[0].set_title("Packet scaffold structure")
    axes[0].set_ylabel("count")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    groups = [row["blocker_group"] for row in task_rows]
    required_new = [1 if boolish(row["requires_new_controlled_data"]) else 0 for row in task_rows]
    axes[1].bar(
        range(len(groups)),
        required_new,
        width=0.62,
        color=["#e45756" if value else "#4c78a8" for value in required_new],
    )
    axes[1].set_xticks(range(len(groups)), [group.replace("_", "\n") for group in groups], fontsize=8)
    axes[1].set_yticks([0, 1], ["notes", "new data"])
    axes[1].set_ylim(0, 1.2)
    axes[1].set_title("Collection action groups")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("GSSI controlled collection scaffold", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_controlled_collection_scaffold.png`",
                "",
                "This figure summarizes a planned controlled-collection packet scaffold.",
                "It does not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC work, or",
                "neural-network training.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Packet rows: `{summary['packet_row_count']}`.",
                f"Acquisition repeats: `{summary['planned_acquisition_repeat_count']}`.",
                f"Time-zero references: `{summary['planned_time_zero_reference_count']}`.",
                f"Amplitude references: `{summary['planned_amplitude_reference_count']}`.",
                f"Measured/session blanks: `{summary['measured_or_session_blank_count']}`.",
                f"Validator expected to pass: `{summary['validator_expected_to_pass']}`.",
                f"Ready for field FWI: `{summary['ready_for_current_archive_field_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                summary["decision"],
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--packet-template-run", default=DEFAULT_PACKET_TEMPLATE_RUN)
    parser.add_argument("--blocker-run", default=DEFAULT_BLOCKER_RUN)
    parser.add_argument("--run-name", default="gssi51600s_controlled_collection_scaffold")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    template_dir = dataset_root / args.packet_template_run / "templates"
    blocker_dir = dataset_root / args.blocker_run / "data"
    action_rows = read_csv_rows(blocker_dir / "field_controlled_packet_action_groups.csv")
    blocker_summary = read_json(blocker_dir / "field_controlled_packet_blocker_prioritization_summary.json")

    fields_by_table = template_fields(template_dir)
    tables = build_scaffold_tables(
        fields_by_table,
        dataset_id=args.dataset_id,
        reference_repeat_gate=safe_int(blocker_summary.get("reference_repeat_gate"), 3),
    )
    status_rows = scaffold_status_rows(tables)
    task_rows = collection_task_rows(action_rows, tables)
    summary = summarize_scaffold(tables, status_rows, task_rows, blocker_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    packet_dir = outdir / "packet_scaffold"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    write_packet_tables(packet_dir, tables)
    write_csv(data_dir / "field_controlled_collection_scaffold_status.csv", status_rows)
    write_csv(data_dir / "field_controlled_collection_tasks.csv", task_rows)
    summary_path = data_dir / "field_controlled_collection_scaffold_summary.json"
    summary_path.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")

    fig_path = figures_dir / "field_controlled_collection_scaffold.png"
    plot_scaffold(status_rows, task_rows, summary, fig_path)
    write_figure_notes(figures_dir / "FIGURE_NOTES.md", summary)
    write_csv(data_dir / "figure_validation.csv", [figure_stats(fig_path)])
    write_run_manifest(
        str(outdir),
        "gssi51600s_controlled_collection_scaffold",
        {
            "summary": json_safe(summary),
            "paths": {
                "source_action_groups_csv": str(blocker_dir / "field_controlled_packet_action_groups.csv"),
                "packet_scaffold_dir": str(packet_dir),
                "summary_json": str(summary_path),
                "figure": str(fig_path),
            },
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

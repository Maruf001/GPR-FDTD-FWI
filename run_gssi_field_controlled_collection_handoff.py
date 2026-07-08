#!/usr/bin/env python3
"""Create an operational handoff for the next controlled 2D GSSI collection."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_controlled_collection_scaffold import TABLE_ORDER  # noqa: E402
from run_gssi_field_controlled_packet_blocker_prioritization import classify_blocker  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import boolish, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SCAFFOLD_RUN = "151_gssi51600s_recovered_session_collection_scaffold"
DEFAULT_VALIDATION_RUN = "152_gssi51600s_recovered_scaffold_type_aware_validation"
DEFAULT_ACTION_RUN = "153_gssi51600s_recovered_scaffold_type_aware_blocker_prioritization"
DEFAULT_BRIDGE_RUN = "154_gssi51600s_field_qc_to_controlled_collection_bridge"

GROUP_COLLECTION_PHASES = {
    "target_truth_geometry": "target_truth",
    "time_zero_reference": "references",
    "amplitude_reference": "references",
    "profile_target_geometry": "survey_geometry",
    "acquisition_control_links": "controlled_repeats",
    "session_metadata": "session_metadata",
    "reference_registry": "references",
}

GROUP_DONE_WHEN = {
    "target_truth_geometry": (
        "target_truth row has material, center coordinates, cover depth, diameter/radius, "
        "dielectric/velocity, uncertainty, and truth source"
    ),
    "time_zero_reference": (
        "at least three metal-plate or air/direct references have measured time-zero and "
        "uncertainty no larger than the stated gate"
    ),
    "amplitude_reference": (
        "at least three amplitude-reflector references have amplitude metrics and repeatability"
    ),
    "profile_target_geometry": (
        "profile start/end, scan direction, trace spacing, crossed target IDs, and survey "
        "method are recorded in one profile-to-target coordinate frame"
    ),
    "acquisition_control_links": (
        "three controlled repeats have file names, Tx/Rx offset, coupling condition, target/profile "
        "links, and before/after reference IDs"
    ),
    "session_metadata": "session date and operator are verified or recollected",
    "reference_registry": "every reference row has file name, expected response, repeat ID, and session link",
}

GROUP_UNBLOCKS = {
    "target_truth_geometry": "known-truth radius/depth validation and target-geometry checks",
    "time_zero_reference": "absolute time-zero, calibrated depth, and field-inversion preflight",
    "amplitude_reference": "amplitude-calibrated waveform comparison and inversion preflight",
    "profile_target_geometry": "profile spatial calibration and target-crossing interpretation",
    "acquisition_control_links": "repeatability, Tx/Rx-offset confirmation, and packet acceptance",
    "session_metadata": "required metadata gate",
    "reference_registry": "reference traceability and cross-table packet joins",
}


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_packet(packet_dir: Path) -> dict[str, list[dict]]:
    return {table: read_csv_rows(packet_dir / f"{table}.csv") for table in TABLE_ORDER}


def nonempty(value: object) -> bool:
    return str(value if value is not None else "").strip() != ""


def joined(values: list[str]) -> str:
    return ",".join(value for value in values if value)


def unique_join(values: list[object]) -> str:
    return joined(sorted({str(value).strip() for value in values if nonempty(value)}))


def packet_ids_for_group(group: str, packet: dict[str, list[dict]]) -> str:
    if group == "target_truth_geometry":
        return unique_join([row.get("target_id", "") for row in packet["target_truth"]])
    if group == "time_zero_reference":
        return unique_join(
            [
                row.get("reference_id", "")
                for row in packet["reference_measurement"]
                if str(row.get("reference_type", "")) in {"air_direct", "metal_plate_t0"}
            ]
        )
    if group == "amplitude_reference":
        return unique_join(
            [
                row.get("reference_id", "")
                for row in packet["reference_measurement"]
                if str(row.get("reference_type", "")) == "amplitude_reflector"
            ]
        )
    if group == "profile_target_geometry":
        return unique_join(
            [
                f"{row.get('profile_id', '')}:{row.get('target_ids_crossed', '')}"
                for row in packet["profile_geometry"]
            ]
        )
    if group == "acquisition_control_links":
        return unique_join(
            [
                f"{row.get('profile_id', '')}:repeat{row.get('repeat_id', '')}"
                for row in packet["acquisition_run"]
            ]
        )
    if group == "session_metadata":
        return unique_join([row.get("session_id", "") for row in packet["session_log"]])
    if group == "reference_registry":
        return unique_join([row.get("reference_id", "") for row in packet["reference_measurement"]])
    return ""


def gate_lookup(gate_rows: list[dict]) -> dict[str, dict]:
    return {str(row.get("gate_key", "")): row for row in gate_rows}


def gates_for_action(action: dict, gate_rows: list[dict]) -> tuple[str, str, str]:
    lookup = gate_lookup(gate_rows)
    gates = [gate.strip() for gate in str(action.get("acceptance_gates_unblocked", "")).split(",") if gate.strip()]
    statuses = []
    requirements = []
    blockers = []
    for gate in gates:
        gate_row = lookup.get(gate, {})
        statuses.append(f"{gate}={'ready' if boolish(gate_row.get('ready_now')) else 'blocked'}")
        requirement = str(gate_row.get("extra_requirement", "")).strip()
        if requirement:
            requirements.append(f"{gate}: {requirement}")
        blocking = str(gate_row.get("blocking_if_fail", "")).strip()
        if blocking:
            blockers.append(f"{gate}: {blocking}")
    return "; ".join(statuses), "; ".join(requirements), "; ".join(blockers)


def build_handoff_rows(action_rows: list[dict], gate_rows: list[dict], packet: dict[str, list[dict]]) -> list[dict]:
    rows = []
    for action in sorted(action_rows, key=lambda row: safe_int(row.get("priority"), 99)):
        group = str(action.get("blocker_group", ""))
        gate_status, gate_requirements, blocked_claims = gates_for_action(action, gate_rows)
        rows.append(
            {
                "priority": safe_int(action.get("priority"), 99),
                "collection_phase": GROUP_COLLECTION_PHASES.get(group, "review"),
                "blocker_group": group,
                "planned_ids_or_repeats": packet_ids_for_group(group, packet),
                "packet_tables": action.get("table_names", ""),
                "fields_to_fill": action.get("field_names", ""),
                "minimum_rows_or_repeats": action.get("minimum_rows_or_repeats", ""),
                "missing_required_count": safe_int(action.get("missing_required_count"), 0),
                "requires_new_controlled_data": boolish(action.get("requires_new_controlled_data")),
                "current_archive_can_resolve": boolish(action.get("current_archive_can_resolve")),
                "acceptance_gate_status": gate_status,
                "gate_requirements": gate_requirements,
                "blocked_claims_if_unresolved": blocked_claims,
                "done_when": GROUP_DONE_WHEN.get(group, action.get("action", "")),
                "unblocks_after_packet_acceptance": GROUP_UNBLOCKS.get(group, ""),
                "action": action.get("action", ""),
            }
        )
    return rows


def finding_fields_by_row(findings: list[dict]) -> dict[tuple[str, str], list[str]]:
    by_row: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in findings:
        if boolish(row.get("passed")):
            continue
        if str(row.get("severity", "")) != "blocking":
            continue
        if str(row.get("check_key", "")) != "required_nonempty":
            continue
        key = (str(row.get("table_name", "")), str(row.get("row_index", "")))
        by_row[key].append(str(row.get("field_name", "")))
    return by_row


def row_identifier(table_name: str, row: dict) -> str:
    fields = {
        "session_log": ("session_id",),
        "target_truth": ("target_id",),
        "profile_geometry": ("profile_id", "target_ids_crossed"),
        "acquisition_run": ("profile_id", "repeat_id", "target_id"),
        "reference_measurement": ("reference_id", "reference_type", "repeat_id"),
    }.get(table_name, tuple(row.keys()))
    return joined([str(row.get(field, "")).strip() for field in fields])


def build_packet_fill_map(packet: dict[str, list[dict]], findings: list[dict]) -> list[dict]:
    missing = finding_fields_by_row(findings)
    rows = []
    for table_name in TABLE_ORDER:
        for row_index, packet_row in enumerate(packet[table_name], start=1):
            fields = sorted(missing.get((table_name, str(row_index)), []))
            groups = sorted({classify_blocker(table_name, field) for field in fields})
            rows.append(
                {
                    "table_name": table_name,
                    "row_index": row_index,
                    "row_identifier": row_identifier(table_name, packet_row),
                    "missing_required_count": len(fields),
                    "missing_required_fields": ",".join(fields),
                    "blocker_groups": ",".join(groups),
                    "fill_status": "complete_for_required_fields" if not fields else "needs_collection_entry",
                }
            )
    return rows


def build_gate_handoff_rows(gate_rows: list[dict]) -> list[dict]:
    rows = []
    for row in sorted(gate_rows, key=lambda item: safe_int(item.get("highest_priority"), 99)):
        ready = boolish(row.get("ready_now"))
        rows.append(
            {
                "gate_key": row.get("gate_key", ""),
                "ready_now": ready,
                "highest_priority": safe_int(row.get("highest_priority"), 99),
                "required_blocker_groups": row.get("required_blocker_groups", ""),
                "current_evidence": row.get("current_evidence", ""),
                "extra_requirement": row.get("extra_requirement", ""),
                "blocks_if_fail": row.get("blocking_if_fail", ""),
                "handoff_instruction": (
                    "rerun packet validator and blocker prioritization after filling linked rows"
                    if not ready
                    else "gate currently passes"
                ),
            }
        )
    return rows


def summarize_handoff(
    handoff_rows: list[dict],
    packet_rows: list[dict],
    gate_rows: list[dict],
    bridge_summary: dict,
    validation_summary: dict,
) -> dict:
    critical_new = [
        row
        for row in handoff_rows
        if safe_int(row.get("priority"), 99) <= 5 and boolish(row.get("requires_new_controlled_data"))
    ]
    return {
        "policy_label": "gssi51600s_controlled_collection_handoff",
        "source_scaffold_run": DEFAULT_SCAFFOLD_RUN,
        "source_validation_run": DEFAULT_VALIDATION_RUN,
        "source_action_run": DEFAULT_ACTION_RUN,
        "source_bridge_run": DEFAULT_BRIDGE_RUN,
        "handoff_action_count": len(handoff_rows),
        "critical_new_data_action_count": len(critical_new),
        "critical_new_data_action_groups": ";".join(row["blocker_group"] for row in critical_new),
        "packet_row_count": len(packet_rows),
        "packet_rows_needing_entry": sum(row["missing_required_count"] > 0 for row in packet_rows),
        "missing_required_value_count": validation_summary.get("missing_required_value_count"),
        "blocking_finding_count": validation_summary.get("blocking_finding_count"),
        "acceptance_gate_count": len(gate_rows),
        "failed_acceptance_gate_count": sum(not boolish(row.get("ready_now")) for row in gate_rows),
        "reference_repeat_gate": bridge_summary.get("reference_repeat_gate"),
        "reference_uncertainty_gate_ns": bridge_summary.get("reference_uncertainty_gate_ns"),
        "reference_uncertainty_gate_depth_error_mm": bridge_summary.get(
            "reference_uncertainty_gate_depth_error_mm"
        ),
        "field_geometry_type": bridge_summary.get("field_geometry_type", ""),
        "is_3d_survey": boolish(bridge_summary.get("is_3d_survey")),
        "ready_for_collection_day": True,
        "ready_for_packet_acceptance": boolish(validation_summary.get("ready_for_packet_acceptance")),
        "ready_for_current_archive_field_qc_supplement": boolish(
            bridge_summary.get("ready_for_current_archive_field_qc_supplement")
        ),
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_field_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "Use this as the field collection run sheet for the next controlled 2D pass. "
            "The current archive remains useful for scoped 2D field QC only. It is not ready "
            "for field FWI, heavy GPU work, or 3D/HPC until the controlled packet is filled, "
            "validated, and all acceptance gates pass."
        ),
    }


def plot_handoff(
    handoff_rows: list[dict],
    packet_rows: list[dict],
    gate_rows: list[dict],
    summary: dict,
    save_path: Path,
) -> str:
    fig, axes = plt.subplots(2, 2, figsize=(15.8, 9.2), constrained_layout=True)
    ax0, ax1, ax2, ax3 = axes.ravel()

    labels = [row["blocker_group"].replace("_", "\n") for row in handoff_rows]
    missing = [safe_int(row.get("missing_required_count")) for row in handoff_rows]
    colors = [
        "#e15759" if safe_int(row.get("priority"), 99) <= 3 else "#f2cf5b" if safe_int(row.get("priority"), 99) <= 5 else "#4e79a7"
        for row in handoff_rows
    ]
    ax0.bar(np.arange(len(labels)), missing, color=colors, width=0.65)
    ax0.set_xticks(np.arange(len(labels)), labels, fontsize=7.4)
    ax0.set_ylabel("missing required fields")
    ax0.set_title("Collection actions by blocker group")
    ax0.grid(axis="y", color="#dddddd", linewidth=0.6)

    table_names = list(TABLE_ORDER)
    table_missing = [
        sum(safe_int(row["missing_required_count"]) for row in packet_rows if row["table_name"] == table)
        for table in table_names
    ]
    ax1.bar(np.arange(len(table_names)), table_missing, color="#59a14f", width=0.62)
    ax1.set_xticks(np.arange(len(table_names)), [name.replace("_", "\n") for name in table_names], fontsize=8)
    ax1.set_ylabel("missing required fields")
    ax1.set_title("Packet rows to fill")
    ax1.grid(axis="y", color="#dddddd", linewidth=0.6)

    gate_labels = [row["gate_key"].replace("_", "\n") for row in gate_rows]
    gate_values = [1 if boolish(row["ready_now"]) else 0 for row in gate_rows]
    ax2.bar(np.arange(len(gate_labels)), gate_values, color=["#59a14f" if value else "#e15759" for value in gate_values])
    ax2.set_xticks(np.arange(len(gate_labels)), gate_labels, fontsize=7.2)
    ax2.set_yticks([0, 1], ["blocked", "ready"])
    ax2.set_ylim(-0.1, 1.2)
    ax2.set_title("Acceptance gates")
    ax2.grid(axis="y", color="#dddddd", linewidth=0.6)

    ax3.axis("off")
    ax3.text(
        0.02,
        0.98,
        "\n".join(
            [
                "Handoff decision",
                f"ready for collection day: {summary['ready_for_collection_day']}",
                f"packet acceptance: {summary['ready_for_packet_acceptance']}",
                f"field QC supplement: {summary['ready_for_current_archive_field_qc_supplement']}",
                f"field FWI: {summary['ready_for_current_archive_field_fwi']}",
                f"field 3D/HPC: {summary['ready_for_field_3d_hpc']}",
                f"reference gate: {summary['reference_uncertainty_gate_ns']} ns",
                f"missing required values: {summary['missing_required_value_count']}",
                f"failed gates: {summary['failed_acceptance_gate_count']}",
                f"GPU priority: {summary['gpu_priority']}",
            ]
        ),
        transform=ax3.transAxes,
        va="top",
        ha="left",
        fontsize=10,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.45"},
    )

    fig.suptitle("GSSI controlled 2D collection handoff", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_run_sheet(path: Path, handoff_rows: list[dict], gate_rows: list[dict], summary: dict) -> None:
    lines = [
        "# GSSI Controlled 2D Collection Run Sheet",
        "",
        "Use this sheet for the next controlled field pass. It is a collection handoff, not an inversion launch gate.",
        "",
        "## Scope",
        "",
        f"- Current archive geometry: `{summary['field_geometry_type']}`.",
        f"- Ready for scoped field-QC supplement: `{summary['ready_for_current_archive_field_qc_supplement']}`.",
        f"- Ready for packet acceptance: `{summary['ready_for_packet_acceptance']}`.",
        f"- Ready for field FWI/heavy GPU/3D-HPC: `False`.",
        f"- Reference uncertainty gate: `{summary['reference_uncertainty_gate_ns']}` ns.",
        "",
        "## Collection Actions",
        "",
    ]
    for row in handoff_rows:
        lines.extend(
            [
                f"### {row['priority']}. {row['blocker_group']}",
                "",
                f"- Phase: `{row['collection_phase']}`.",
                f"- Planned IDs/repeats: `{row['planned_ids_or_repeats']}`.",
                f"- Packet tables: `{row['packet_tables']}`.",
                f"- Fields to fill: `{row['fields_to_fill']}`.",
                f"- Minimum rows/repeats: `{row['minimum_rows_or_repeats']}`.",
                f"- Gate status: `{row['acceptance_gate_status']}`.",
                f"- Done when: {row['done_when']}.",
                f"- Unblocks after packet acceptance: {row['unblocks_after_packet_acceptance']}.",
                "",
            ]
        )
    lines.extend(["## Acceptance Gates", ""])
    for row in gate_rows:
        lines.append(
            f"- `{row['gate_key']}`: ready=`{row['ready_now']}`, blockers=`{row['required_blocker_groups']}`."
        )
    lines.extend(
        [
            "",
            "## Stop Rule",
            "",
            "Do not run field FWI, heavy local GPU field work, 3D/HPC field jobs, or neural-network training from this field archive until a filled controlled packet passes validation and all acceptance gates pass.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_controlled_collection_handoff.png`",
                "",
                "This CPU-only figure summarizes the operational handoff for the next",
                "controlled 2D GSSI collection pass. It joins the recovered scaffold,",
                "type-aware validation blockers, action priorities, and field-QC bridge.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Handoff actions: `{summary['handoff_action_count']}`.",
                f"Critical new-data actions: `{summary['critical_new_data_action_groups']}`.",
                f"Packet rows needing entry: `{summary['packet_rows_needing_entry']}`.",
                f"Missing required values: `{summary['missing_required_value_count']}`.",
                f"Failed acceptance gates: `{summary['failed_acceptance_gate_count']}`.",
                f"Ready for packet acceptance: `{summary['ready_for_packet_acceptance']}`.",
                f"Ready for field FWI: `{summary['ready_for_current_archive_field_fwi']}`.",
                f"Ready for field 3D/HPC: `{summary['ready_for_field_3d_hpc']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                summary["decision"],
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def source_paths(dataset_root: Path, args: argparse.Namespace) -> dict[str, Path]:
    return {
        "packet_dir": dataset_root / args.scaffold_run / "packet_scaffold_recovered_session",
        "validation_summary": dataset_root / args.validation_run / "data/controlled_2d_packet_validation_summary.json",
        "validation_findings": dataset_root / args.validation_run / "data/controlled_2d_packet_validation_findings.csv",
        "action_rows": dataset_root / args.action_run / "data/field_controlled_packet_action_groups.csv",
        "gate_rows": dataset_root / args.action_run / "data/field_controlled_packet_gate_actions.csv",
        "bridge_summary": dataset_root / args.bridge_run / "data/field_qc_to_controlled_collection_bridge_summary.json",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--scaffold-run", default=DEFAULT_SCAFFOLD_RUN)
    parser.add_argument("--validation-run", default=DEFAULT_VALIDATION_RUN)
    parser.add_argument("--action-run", default=DEFAULT_ACTION_RUN)
    parser.add_argument("--bridge-run", default=DEFAULT_BRIDGE_RUN)
    parser.add_argument("--run-name", default="gssi51600s_controlled_collection_handoff")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    paths = source_paths(dataset_root, args)

    packet = load_packet(paths["packet_dir"])
    validation_summary = read_json(paths["validation_summary"])
    findings = read_csv_rows(paths["validation_findings"])
    source_action_rows = read_csv_rows(paths["action_rows"])
    source_gate_rows = read_csv_rows(paths["gate_rows"])
    bridge_summary = read_json(paths["bridge_summary"])

    handoff_rows = build_handoff_rows(source_action_rows, source_gate_rows, packet)
    packet_rows = build_packet_fill_map(packet, findings)
    gate_rows = build_gate_handoff_rows(source_gate_rows)
    summary = summarize_handoff(handoff_rows, packet_rows, gate_rows, bridge_summary, validation_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    handoff_csv = data_dir / "field_controlled_collection_handoff_rows.csv"
    packet_csv = data_dir / "field_controlled_collection_packet_fill_map.csv"
    gate_csv = data_dir / "field_controlled_collection_gate_handoff.csv"
    summary_json = data_dir / "field_controlled_collection_handoff_summary.json"
    run_sheet = data_dir / "field_controlled_collection_run_sheet.md"
    figure_path = figures_dir / "field_controlled_collection_handoff.png"

    write_csv(handoff_csv, [json_safe(row) for row in handoff_rows])
    write_csv(packet_csv, [json_safe(row) for row in packet_rows])
    write_csv(gate_csv, [json_safe(row) for row in gate_rows])
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_sheet(run_sheet, handoff_rows, gate_rows, summary)
    plot_handoff(handoff_rows, packet_rows, gate_rows, summary, figure_path)
    write_figure_notes(figures_dir / "FIGURE_NOTES.md", summary)
    write_csv(data_dir / "figure_validation.csv", [figure_stats(figure_path)])

    write_run_manifest(
        str(outdir),
        "gssi51600s_controlled_collection_handoff",
        {
            "summary": json_safe(summary),
            "paths": {
                "source_packet_dir": str(paths["packet_dir"]),
                "source_validation_summary": str(paths["validation_summary"]),
                "source_action_rows": str(paths["action_rows"]),
                "source_bridge_summary": str(paths["bridge_summary"]),
                "handoff_csv": str(handoff_csv),
                "packet_fill_map_csv": str(packet_csv),
                "gate_handoff_csv": str(gate_csv),
                "run_sheet": str(run_sheet),
                "summary_json": str(summary_json),
                "figure": str(figure_path),
            },
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

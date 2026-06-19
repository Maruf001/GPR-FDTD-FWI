#!/usr/bin/env python3
"""Audit the critical path from controlled-field handoff to packet acceptance."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
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
from run_local_2d_detector_rank_budget_diagnostic import boolish, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_HANDOFF_RUN = "155_gssi51600s_controlled_collection_handoff"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def split_csv(value: object) -> list[str]:
    return [part.strip() for part in str(value or "").split(",") if part.strip()]


def parse_gate_status(value: object) -> list[str]:
    gates = []
    for part in str(value or "").split(";"):
        gate = part.strip().split("=", maxsplit=1)[0].strip()
        if gate:
            gates.append(gate)
    return gates


def group_rows_by_key(rows: list[dict], key: str) -> dict[str, dict]:
    return {str(row.get(key, "")): row for row in rows}


def build_action_rows(handoff_rows: list[dict]) -> list[dict]:
    rows = []
    for row in sorted(handoff_rows, key=lambda item: safe_int(item.get("priority"), 99)):
        gates = parse_gate_status(row.get("acceptance_gate_status"))
        rows.append(
            {
                "priority": safe_int(row.get("priority"), 99),
                "collection_phase": row.get("collection_phase", ""),
                "blocker_group": row.get("blocker_group", ""),
                "planned_ids_or_repeats": row.get("planned_ids_or_repeats", ""),
                "minimum_rows_or_repeats": safe_int(row.get("minimum_rows_or_repeats"), 0),
                "missing_required_count": safe_int(row.get("missing_required_count"), 0),
                "acceptance_gates_touched": ",".join(gates),
                "gate_touch_count": len(gates),
                "requires_new_controlled_data": boolish(row.get("requires_new_controlled_data")),
                "current_archive_can_resolve": boolish(row.get("current_archive_can_resolve")),
                "documentation_overlay": (
                    row.get("blocker_group") in {"session_metadata", "reference_registry"}
                ),
                "critical_path_role": (
                    "field_inversion_prerequisite"
                    if row.get("blocker_group")
                    in {"target_truth_geometry", "time_zero_reference", "amplitude_reference"}
                    else "packet_acceptance_prerequisite"
                ),
                "done_when": row.get("done_when", ""),
            }
        )
    return rows


def build_gate_rows(gate_rows: list[dict], action_rows: list[dict]) -> list[dict]:
    action_by_group = group_rows_by_key(action_rows, "blocker_group")
    out = []
    for gate in sorted(gate_rows, key=lambda row: safe_int(row.get("highest_priority"), 99)):
        groups = split_csv(gate.get("required_blocker_groups"))
        required_actions = [action_by_group[group] for group in groups if group in action_by_group]
        current_archive_groups = [
            action["blocker_group"]
            for action in required_actions
            if boolish(action.get("current_archive_can_resolve"))
        ]
        new_data_groups = [
            action["blocker_group"]
            for action in required_actions
            if boolish(action.get("requires_new_controlled_data"))
        ]
        out.append(
            {
                "gate_key": gate.get("gate_key", ""),
                "ready_now": boolish(gate.get("ready_now")),
                "highest_priority": safe_int(gate.get("highest_priority"), 99),
                "required_blocker_groups": ",".join(groups),
                "required_action_count": len(required_actions),
                "current_archive_resolvable_action_count": len(current_archive_groups),
                "new_controlled_data_action_count": len(new_data_groups),
                "current_archive_can_unblock": len(required_actions) > 0
                and len(current_archive_groups) == len(required_actions),
                "requires_new_controlled_data": len(new_data_groups) > 0,
                "missing_required_total": sum(
                    safe_int(action.get("missing_required_count"), 0) for action in required_actions
                ),
                "minimum_rows_or_repeats_total": sum(
                    safe_int(action.get("minimum_rows_or_repeats"), 0) for action in required_actions
                ),
                "blocks_if_fail": gate.get("blocks_if_fail", ""),
                "critical_path": " -> ".join(groups),
            }
        )
    return out


def build_phase_rows(action_rows: list[dict]) -> list[dict]:
    by_phase: dict[str, list[dict]] = defaultdict(list)
    for row in action_rows:
        by_phase[str(row.get("collection_phase", "review"))].append(row)
    phase_order = {
        "target_truth": 1,
        "references": 2,
        "survey_geometry": 3,
        "controlled_repeats": 4,
        "session_metadata": 5,
    }
    rows = []
    for phase, actions in sorted(by_phase.items(), key=lambda item: phase_order.get(item[0], 99)):
        gates = sorted({gate for action in actions for gate in split_csv(action.get("acceptance_gates_touched"))})
        rows.append(
            {
                "phase_order": phase_order.get(phase, 99),
                "collection_phase": phase,
                "blocker_groups": ",".join(str(action["blocker_group"]) for action in actions),
                "planned_ids_or_repeats": ";".join(str(action["planned_ids_or_repeats"]) for action in actions),
                "action_count": len(actions),
                "minimum_rows_or_repeats_total": sum(
                    safe_int(action.get("minimum_rows_or_repeats"), 0) for action in actions
                ),
                "missing_required_total": sum(
                    safe_int(action.get("missing_required_count"), 0) for action in actions
                ),
                "acceptance_gates_touched": ",".join(gates),
                "contains_documentation_overlay": any(
                    boolish(action.get("documentation_overlay")) for action in actions
                ),
            }
        )
    return rows


def summarize(
    source_summary: dict,
    action_rows: list[dict],
    gate_rows: list[dict],
    phase_rows: list[dict],
    packet_rows: list[dict],
) -> dict:
    packet_rows_needing_entry = sum(1 for row in packet_rows if row.get("fill_status") == "needs_collection_entry")
    current_archive_unblockable_gates = [
        row for row in gate_rows if boolish(row.get("current_archive_can_unblock"))
    ]
    new_data_actions = [row for row in action_rows if boolish(row.get("requires_new_controlled_data"))]
    inversion_prereqs = [
        row for row in action_rows if row.get("critical_path_role") == "field_inversion_prerequisite"
    ]
    return {
        "policy_label": "gssi51600s_controlled_collection_critical_path",
        "source_handoff_policy_label": source_summary.get("policy_label", ""),
        "action_count": len(action_rows),
        "new_controlled_data_action_count": len(new_data_actions),
        "critical_new_data_action_count": safe_int(source_summary.get("critical_new_data_action_count"), 0),
        "field_inversion_prerequisite_action_count": len(inversion_prereqs),
        "gate_count": len(gate_rows),
        "ready_gate_count": sum(1 for row in gate_rows if boolish(row.get("ready_now"))),
        "current_archive_unblockable_gate_count": len(current_archive_unblockable_gates),
        "phase_count": len(phase_rows),
        "packet_row_count": len(packet_rows),
        "packet_rows_needing_entry": packet_rows_needing_entry,
        "missing_required_value_count": safe_int(source_summary.get("missing_required_value_count"), 0),
        "reference_repeat_gate": safe_int(source_summary.get("reference_repeat_gate"), 0),
        "reference_uncertainty_gate_ns": source_summary.get("reference_uncertainty_gate_ns", ""),
        "field_geometry_type": source_summary.get("field_geometry_type", ""),
        "is_3d_survey": boolish(source_summary.get("is_3d_survey")),
        "ready_for_collection_execution": boolish(source_summary.get("ready_for_collection_day")),
        "ready_for_packet_acceptance": boolish(source_summary.get("ready_for_packet_acceptance")),
        "ready_for_current_archive_field_qc_supplement": boolish(
            source_summary.get("ready_for_current_archive_field_qc_supplement")
        ),
        "ready_for_current_archive_field_fwi": boolish(
            source_summary.get("ready_for_current_archive_field_fwi")
        ),
        "ready_for_current_archive_heavy_field_work": boolish(
            source_summary.get("ready_for_current_archive_heavy_field_work")
        ),
        "ready_for_field_3d_hpc": boolish(source_summary.get("ready_for_field_3d_hpc")),
        "ready_for_gpu_work": False,
        "gpu_priority": "none",
        "decision": (
            "Use this as the critical-path checklist for the next controlled 2D field pass. "
            "The current archive cannot unblock any acceptance gate by itself; real controlled "
            "target truth, references, survey geometry, and repeat acquisitions are required "
            "before packet acceptance, field FWI, heavy GPU work, or 3D/HPC."
        ),
    }


def plot_critical_path(summary: dict, action_rows: list[dict], gate_rows: list[dict], save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8), constrained_layout=True)
    labels = [str(row["blocker_group"]).replace("_", "\n") for row in action_rows]
    missing = [safe_int(row.get("missing_required_count"), 0) for row in action_rows]
    colors = ["#4e79a7" if row.get("critical_path_role") == "field_inversion_prerequisite" else "#9c755f" for row in action_rows]
    axes[0].bar(range(len(labels)), missing, color=colors)
    axes[0].set_xticks(range(len(labels)), labels, rotation=0, fontsize=7.4)
    axes[0].set_ylabel("missing fields")
    axes[0].set_title("Action blockers")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    gate_labels = [str(row["gate_key"]).replace("_", "\n") for row in gate_rows]
    new_data_counts = [safe_int(row.get("new_controlled_data_action_count"), 0) for row in gate_rows]
    axes[1].bar(range(len(gate_labels)), new_data_counts, color="#e15759")
    axes[1].set_xticks(range(len(gate_labels)), gate_labels, rotation=0, fontsize=7.2)
    axes[1].set_ylabel("new-data actions")
    axes[1].set_title("Gate critical path")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.95,
        f"packet rows needing entry={summary['packet_rows_needing_entry']}\n"
        f"ready gates={summary['ready_gate_count']}/{summary['gate_count']}\n"
        f"GPU priority={summary['gpu_priority']}",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        fontsize=8.2,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI controlled 2D collection critical path", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_controlled_collection_critical_path.png`",
                "",
                "This CPU-only figure summarizes the critical path from the current",
                "controlled-collection handoff to a packet that could be accepted.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Action count: `{summary['action_count']}`.",
                f"New controlled-data actions: `{summary['new_controlled_data_action_count']}`.",
                f"Packet rows needing entry: `{summary['packet_rows_needing_entry']}`.",
                f"Ready gates: `{summary['ready_gate_count']}` / `{summary['gate_count']}`.",
                f"Current archive field FWI ready: `{summary['ready_for_current_archive_field_fwi']}`.",
                f"Field 3D/HPC ready: `{summary['ready_for_field_3d_hpc']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "This is a collection-planning artifact. It does not authorize field",
                "FWI, heavy local GPU work, 3D/HPC, or neural-network training.",
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
    parser.add_argument("--handoff-run", default=DEFAULT_HANDOFF_RUN)
    parser.add_argument("--run-name", default="gssi51600s_controlled_collection_critical_path")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    field_root = field_dataset_output_root(args.field_root, args.dataset_id)
    handoff_dir = field_root / args.handoff_run
    data_root = handoff_dir / "data"
    source_summary = read_json(data_root / "field_controlled_collection_handoff_summary.json")
    source_action_rows = read_csv_rows(data_root / "field_controlled_collection_handoff_rows.csv")
    source_gate_rows = read_csv_rows(data_root / "field_controlled_collection_gate_handoff.csv")
    packet_rows = read_csv_rows(data_root / "field_controlled_collection_packet_fill_map.csv")

    action_rows = build_action_rows(source_action_rows)
    gate_rows = build_gate_rows(source_gate_rows, action_rows)
    phase_rows = build_phase_rows(action_rows)
    summary = summarize(source_summary, action_rows, gate_rows, phase_rows, packet_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(field_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    action_csv = data_dir / "field_controlled_collection_critical_actions.csv"
    gate_csv = data_dir / "field_controlled_collection_gate_critical_path.csv"
    phase_csv = data_dir / "field_controlled_collection_phase_plan.csv"
    summary_json = data_dir / "field_controlled_collection_critical_path_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_controlled_collection_critical_path.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(action_csv, [json_safe(row) for row in action_rows])
    write_csv(gate_csv, [json_safe(row) for row in gate_rows])
    write_csv(phase_csv, [json_safe(row) for row in phase_rows])
    plot_critical_path(summary, action_rows, gate_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_notes(figure_notes, summary)

    output_summary = {
        **summary,
        "paths": {
            "actions_csv": str(action_csv),
            "gate_critical_path_csv": str(gate_csv),
            "phase_plan_csv": str(phase_csv),
            "summary_json": str(summary_json),
            "source_handoff_summary_json": str(data_root / "field_controlled_collection_handoff_summary.json"),
            "source_handoff_rows_csv": str(data_root / "field_controlled_collection_handoff_rows.csv"),
            "source_gate_handoff_csv": str(data_root / "field_controlled_collection_gate_handoff.csv"),
            "source_packet_fill_map_csv": str(data_root / "field_controlled_collection_packet_fill_map.csv"),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_controlled_collection_critical_path",
        {
            "handoff_run": args.handoff_run,
            "dataset_id": args.dataset_id,
            "summary_json": str(summary_json),
            "actions_csv": str(action_csv),
            "gate_critical_path_csv": str(gate_csv),
            "phase_plan_csv": str(phase_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

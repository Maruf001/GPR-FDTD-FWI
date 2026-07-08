#!/usr/bin/env python3
"""Prioritize blockers in the current controlled-2D GSSI packet validation."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter, defaultdict
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


DEFAULT_VALIDATION_RUN = "144_gssi51600s_current_archive_packet_prefill_validation"
DEFAULT_REFERENCE_RUN = "145_gssi51600s_field_time_zero_reference_requirement"


GROUP_POLICIES = {
    "target_truth_geometry": {
        "priority": 1,
        "action_type": "new_controlled_measurement",
        "minimum_rows": 1,
        "acceptance_gates": "target_truth_controls,field_fwi_or_heavy_work",
        "action": "Measure and record target material, center coordinates, cover depth, radius/diameter, dielectric/velocity, uncertainty, and truth source.",
    },
    "time_zero_reference": {
        "priority": 2,
        "action_type": "new_reference_measurement",
        "minimum_rows": 3,
        "acceptance_gates": "absolute_time_zero_references,field_fwi_or_heavy_work",
        "action": "Collect at least three air/direct-wave or metal-plate time-zero references before/after the controlled profiles.",
    },
    "amplitude_reference": {
        "priority": 3,
        "action_type": "new_reference_measurement",
        "minimum_rows": 3,
        "acceptance_gates": "amplitude_references,field_fwi_or_heavy_work",
        "action": "Collect at least three amplitude-reference measurements with repeatability metrics.",
    },
    "profile_target_geometry": {
        "priority": 4,
        "action_type": "new_survey_measurement",
        "minimum_rows": 1,
        "acceptance_gates": "required_metadata_fields,cross_table_links,short_repeat_redundancy",
        "action": "Survey profile start/end coordinates, scan direction, trace spacing, crossed target IDs, and survey method in one profile-to-target coordinate frame.",
    },
    "acquisition_control_links": {
        "priority": 5,
        "action_type": "new_controlled_acquisition",
        "minimum_rows": 3,
        "acceptance_gates": "required_metadata_fields,cross_table_links,short_repeat_redundancy",
        "action": "Record controlled profile repeats with target ID, profile ID, Tx/Rx offset, coupling condition, and before/after reference IDs.",
    },
    "session_metadata": {
        "priority": 6,
        "action_type": "recover_or_recollect_metadata",
        "minimum_rows": 1,
        "acceptance_gates": "required_metadata_fields",
        "action": "Recover operator, antenna serial, gain setting, and session metadata from notes or recollect during the controlled session.",
    },
    "reference_registry": {
        "priority": 7,
        "action_type": "new_reference_measurement",
        "minimum_rows": 3,
        "acceptance_gates": "required_metadata_fields,cross_table_links,absolute_time_zero_references,amplitude_references",
        "action": "Assign reference IDs, session links, reference type, before/after role, file name, repeat ID, and expected response for every reference row.",
    },
    "other_required_metadata": {
        "priority": 8,
        "action_type": "metadata_cleanup",
        "minimum_rows": 1,
        "acceptance_gates": "required_metadata_fields",
        "action": "Fill any remaining required fields, then rerun the packet validator.",
    },
}


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def classify_blocker(table_name: str, field_name: str) -> str:
    table = str(table_name)
    field = str(field_name)
    if table == "target_truth":
        return "target_truth_geometry"
    if table == "session_log":
        return "session_metadata"
    if table == "profile_geometry":
        return "profile_target_geometry"
    if table == "acquisition_run":
        return "acquisition_control_links"
    if table == "reference_measurement":
        if field in {"measured_time_zero_ns", "time_zero_uncertainty_ns"}:
            return "time_zero_reference"
        if field in {"amplitude_metric", "amplitude_repeatability_pct"}:
            return "amplitude_reference"
        return "reference_registry"
    return "other_required_metadata"


def enrich_blocker_rows(findings: list[dict]) -> list[dict]:
    rows = []
    for row in findings:
        if boolish(row.get("passed")):
            continue
        if str(row.get("severity", "")) != "blocking":
            continue
        group = classify_blocker(row.get("table_name", ""), row.get("field_name", ""))
        policy = GROUP_POLICIES[group]
        rows.append(
            {
                "blocker_group": group,
                "priority": policy["priority"],
                "action_type": policy["action_type"],
                "table_name": row.get("table_name", ""),
                "row_index": row.get("row_index", ""),
                "field_name": row.get("field_name", ""),
                "check_key": row.get("check_key", ""),
                "expected": row.get("expected", ""),
                "message": row.get("message", ""),
                "current_archive_can_resolve": group == "session_metadata",
                "requires_new_controlled_data": group != "session_metadata",
            }
        )
    return sorted(rows, key=lambda row: (safe_int(row["priority"]), str(row["table_name"]), safe_int(row["row_index"]), str(row["field_name"])))


def action_group_rows(blocker_rows: list[dict], reference_summary: dict) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in blocker_rows:
        grouped[str(row["blocker_group"])].append(row)

    rows = []
    for group, members in grouped.items():
        policy = GROUP_POLICIES[group]
        fields = sorted({str(row["field_name"]) for row in members})
        tables = sorted({str(row["table_name"]) for row in members})
        minimum_rows = policy["minimum_rows"]
        uncertainty_gate_ns = ""
        uncertainty_depth_mm = ""
        if group == "time_zero_reference":
            minimum_rows = safe_int(reference_summary.get("reference_repeat_gate"), minimum_rows)
            uncertainty_gate_ns = reference_summary.get("reference_uncertainty_gate_ns", "")
            uncertainty_depth_mm = reference_summary.get("reference_uncertainty_gate_depth_error_mm", "")
        rows.append(
            {
                "blocker_group": group,
                "priority": policy["priority"],
                "action_type": policy["action_type"],
                "missing_required_count": len(members),
                "table_names": ",".join(tables),
                "field_names": ",".join(fields),
                "minimum_rows_or_repeats": minimum_rows,
                "reference_uncertainty_gate_ns": uncertainty_gate_ns,
                "reference_depth_equivalent_mm": uncertainty_depth_mm,
                "acceptance_gates_unblocked": policy["acceptance_gates"],
                "current_archive_can_resolve": all(boolish(row["current_archive_can_resolve"]) for row in members),
                "requires_new_controlled_data": any(boolish(row["requires_new_controlled_data"]) for row in members),
                "action": policy["action"],
            }
        )
    return sorted(rows, key=lambda row: (safe_int(row["priority"]), str(row["blocker_group"])))


def gate_action_rows(acceptance_rows: list[dict], action_rows: list[dict], reference_summary: dict) -> list[dict]:
    group_by_gate: dict[str, list[dict]] = defaultdict(list)
    for row in action_rows:
        for gate in str(row["acceptance_gates_unblocked"]).split(","):
            if gate:
                group_by_gate[gate].append(row)

    out = []
    for gate in acceptance_rows:
        gate_key = str(gate["gate_key"])
        groups = sorted(group_by_gate.get(gate_key, []), key=lambda row: safe_int(row["priority"]))
        if gate_key == "absolute_time_zero_references":
            extra = (
                f"reference_repeat_gate={reference_summary.get('reference_repeat_gate')}; "
                f"uncertainty_gate_ns={reference_summary.get('reference_uncertainty_gate_ns')}"
            )
        else:
            extra = ""
        out.append(
            {
                "gate_key": gate_key,
                "ready_now": boolish(gate.get("ready")),
                "current_evidence": gate.get("evidence", ""),
                "blocking_if_fail": gate.get("blocks_if_fail", ""),
                "required_blocker_groups": ",".join(row["blocker_group"] for row in groups),
                "highest_priority": min((safe_int(row["priority"]) for row in groups), default=99),
                "extra_requirement": extra,
            }
        )
    return out


def summarize_prioritization(
    blocker_rows: list[dict],
    action_rows: list[dict],
    gate_rows: list[dict],
    validation_summary: dict,
    reference_summary: dict,
    validation_run: str = DEFAULT_VALIDATION_RUN,
    reference_run: str = DEFAULT_REFERENCE_RUN,
) -> dict:
    action_counts = Counter(row["action_type"] for row in action_rows)
    new_data_count = sum(boolish(row["requires_new_controlled_data"]) for row in action_rows)
    archive_resolvable = sum(boolish(row["current_archive_can_resolve"]) for row in action_rows)
    failed_gates = sum(not boolish(row["ready_now"]) for row in gate_rows)
    critical_groups = [
        row["blocker_group"]
        for row in action_rows
        if safe_int(row["priority"]) <= 5 and boolish(row["requires_new_controlled_data"])
    ]
    return {
        "policy_label": "gssi51600s_controlled_packet_blocker_prioritization",
        "source_validation_run": validation_run,
        "source_reference_run": reference_run,
        "blocking_finding_count": len(blocker_rows),
        "validation_blocking_finding_count": validation_summary.get("blocking_finding_count"),
        "missing_required_value_count": validation_summary.get("missing_required_value_count"),
        "action_group_count": len(action_rows),
        "new_controlled_data_action_group_count": new_data_count,
        "archive_or_notes_resolvable_action_group_count": archive_resolvable,
        "failed_acceptance_gate_count": failed_gates,
        "critical_new_data_blocker_groups": critical_groups,
        "action_type_counts": dict(sorted(action_counts.items())),
        "reference_repeat_gate": reference_summary.get("reference_repeat_gate"),
        "reference_uncertainty_gate_ns": reference_summary.get("reference_uncertainty_gate_ns"),
        "reference_uncertainty_gate_depth_error_mm": reference_summary.get("reference_uncertainty_gate_depth_error_mm"),
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_field_3d_hpc": False,
        "ready_for_new_controlled_2d_acquisition": True,
        "gpu_priority": "none",
        "decision": (
            "The current archive packet is not inversion-ready, but the blockers collapse into a "
            "small controlled-acquisition action set. Prioritize target truth, external time-zero "
            "references, amplitude references, surveyed profile geometry, and controlled repeat "
            "acquisition links before any field FWI or heavy compute."
        ),
    }


def plot_prioritization(action_rows: list[dict], gate_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(15.0, 5.4), constrained_layout=True)
    groups = [row["blocker_group"] for row in action_rows]
    counts = [safe_int(row["missing_required_count"]) for row in action_rows]
    colors = ["#e45756" if safe_int(row["priority"]) <= 3 else "#f2cf5b" if safe_int(row["priority"]) <= 5 else "#4c78a8" for row in action_rows]
    axes[0].bar(range(len(groups)), counts, color=colors, width=0.62)
    axes[0].set_xticks(range(len(groups)), [group.replace("_", "\n") for group in groups], rotation=0, fontsize=8)
    axes[0].set_ylabel("missing required fields")
    axes[0].set_title("Packet blocker groups")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    gate_labels = [row["gate_key"] for row in gate_rows]
    gate_blocked = [0 if boolish(row["ready_now"]) else 1 for row in gate_rows]
    axes[1].bar(
        range(len(gate_labels)),
        gate_blocked,
        color=["#54a24b" if value == 0 else "#e45756" for value in gate_blocked],
        width=0.62,
    )
    axes[1].set_xticks(range(len(gate_labels)), [label.replace("_", "\n") for label in gate_labels], rotation=0, fontsize=8)
    axes[1].set_ylim(0, 1.2)
    axes[1].set_yticks([0, 1], ["ready", "blocked"])
    axes[1].set_title("Acceptance gate blockers")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("GSSI controlled packet blocker prioritization", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_controlled_packet_blocker_prioritization.png`",
                "",
                "This figure groups the current packet-validation blockers into acquisition",
                "actions. It does not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC",
                "work, or neural-network training.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Blocking findings: `{summary['blocking_finding_count']}`.",
                f"Action groups: `{summary['action_group_count']}`.",
                f"Failed acceptance gates: `{summary['failed_acceptance_gate_count']}`.",
                f"Reference repeats required: `{summary['reference_repeat_gate']}`.",
                f"Reference uncertainty gate: `{summary['reference_uncertainty_gate_ns']}` ns.",
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
    parser.add_argument("--validation-run", default=DEFAULT_VALIDATION_RUN)
    parser.add_argument("--reference-run", default=DEFAULT_REFERENCE_RUN)
    parser.add_argument("--run-name", default="gssi51600s_controlled_packet_blocker_prioritization")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    validation_dir = dataset_root / args.validation_run / "data"
    reference_dir = dataset_root / args.reference_run / "data"
    findings = read_csv_rows(validation_dir / "controlled_2d_packet_validation_findings.csv")
    acceptance = read_csv_rows(validation_dir / "controlled_2d_packet_acceptance_status.csv")
    validation_summary = read_json(validation_dir / "controlled_2d_packet_validation_summary.json")
    reference_summary = read_json(reference_dir / "field_time_zero_reference_requirement_summary.json")

    blocker_rows = enrich_blocker_rows(findings)
    actions = action_group_rows(blocker_rows, reference_summary)
    gates = gate_action_rows(acceptance, actions, reference_summary)
    summary = summarize_prioritization(
        blocker_rows,
        actions,
        gates,
        validation_summary,
        reference_summary,
        args.validation_run,
        args.reference_run,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    write_csv(data_dir / "field_controlled_packet_blocker_rows.csv", blocker_rows)
    write_csv(data_dir / "field_controlled_packet_action_groups.csv", actions)
    write_csv(data_dir / "field_controlled_packet_gate_actions.csv", gates)
    summary_path = data_dir / "field_controlled_packet_blocker_prioritization_summary.json"
    summary_path.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")

    fig_path = figures_dir / "field_controlled_packet_blocker_prioritization.png"
    plot_prioritization(actions, gates, summary, fig_path)
    write_figure_notes(figures_dir / "FIGURE_NOTES.md", summary)
    write_csv(data_dir / "figure_validation.csv", [figure_stats(fig_path)])
    write_run_manifest(
        str(outdir),
        "gssi51600s_controlled_packet_blocker_prioritization",
        {
            "summary": json_safe(summary),
            "paths": {
                "source_findings_csv": str(validation_dir / "controlled_2d_packet_validation_findings.csv"),
                "source_acceptance_csv": str(validation_dir / "controlled_2d_packet_acceptance_status.csv"),
                "source_reference_summary_json": str(reference_dir / "field_time_zero_reference_requirement_summary.json"),
                "summary_json": str(summary_path),
                "figure": str(fig_path),
            },
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

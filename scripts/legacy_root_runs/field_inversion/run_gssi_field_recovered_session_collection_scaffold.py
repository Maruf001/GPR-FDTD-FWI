#!/usr/bin/env python3
"""Apply recovered GSSI session metadata to the controlled collection scaffold."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from copy import deepcopy
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
from run_gssi_field_controlled_2d_packet_validator import (  # noqa: E402
    TABLE_NAMES,
    acceptance_status_rows,
    default_paths,
    load_packet_tables,
    summarize_validation,
    table_status_rows,
    validate_cross_table_links,
    validate_required_rules,
)
from run_gssi_field_controlled_collection_scaffold import TABLE_ORDER  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import boolish, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SCAFFOLD_RUN = "147_gssi51600s_controlled_collection_scaffold"
DEFAULT_SCAFFOLD_VALIDATION_RUN = "148_gssi51600s_controlled_collection_scaffold_validation"
DEFAULT_RECOVERY_RUN = "150_gssi51600s_current_archive_metadata_recovery"
SESSION_PREFILL_FIELDS = ("antenna_serial", "software_version", "gain_setting", "time_range_ns")


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_packet(packet_dir: Path) -> dict[str, list[dict]]:
    return {
        table_name: read_csv_rows(packet_dir / f"{table_name}.csv")
        for table_name in TABLE_ORDER
    }


def write_packet(packet_dir: Path, packet: dict[str, list[dict]]) -> None:
    packet_dir.mkdir(parents=True, exist_ok=True)
    for table_name in TABLE_ORDER:
        write_csv(packet_dir / f"{table_name}.csv", [json_safe(row) for row in packet[table_name]])


def nonempty(value: object) -> bool:
    return str(value if value is not None else "").strip() != ""


def recoverable_session_values(recovered_packet: dict[str, list[dict]]) -> dict[str, str]:
    session_rows = recovered_packet.get("session_log", [])
    if not session_rows:
        return {}
    session = session_rows[0]
    return {
        field: str(session.get(field, "")).strip()
        for field in SESSION_PREFILL_FIELDS
        if nonempty(session.get(field))
    }


def apply_recovered_session_metadata(
    scaffold_packet: dict[str, list[dict]],
    recovered_packet: dict[str, list[dict]],
) -> tuple[dict[str, list[dict]], list[dict]]:
    output = deepcopy(scaffold_packet)
    values = recoverable_session_values(recovered_packet)
    session_rows = output.get("session_log", [])
    evidence_rows = []
    for row_index, session in enumerate(session_rows, start=1):
        for field in SESSION_PREFILL_FIELDS:
            previous = str(session.get(field, "")).strip()
            recovered = values.get(field, "")
            applied = bool(recovered and not previous)
            if applied:
                session[field] = recovered
            evidence_rows.append(
                {
                    "table_name": "session_log",
                    "row_index": row_index,
                    "field_name": field,
                    "previous_value": previous,
                    "recovered_value": recovered,
                    "applied": applied,
                    "source": "current_archive_recovered_packet",
                    "scope_note": "prefill_for_same_system_controlled_collection_verify_on_collection_day",
                }
            )
        if any(boolish(row["applied"]) for row in evidence_rows):
            note = str(session.get("notes", "")).strip()
            suffix = (
                " Recovered session fields prefilled from current archive DZX metadata; "
                "verify/update during controlled acquisition."
            )
            session["notes"] = f"{note}{suffix}".strip()
    return output, evidence_rows


def validate_packet(packet_dir: Path, validation_rules: Path) -> tuple[dict, list[dict], list[dict], list[dict]]:
    tables = load_packet_tables(packet_dir)
    rules = read_csv_rows(validation_rules)
    findings = validate_required_rules(tables, rules) + validate_cross_table_links(tables)
    table_status = table_status_rows(tables, rules, findings)
    acceptance_rows = acceptance_status_rows(tables, findings)
    summary = summarize_validation(tables, rules, findings, acceptance_rows, packet_dir)
    return summary, findings, table_status, acceptance_rows


def table_status_lookup(rows: list[dict]) -> dict[str, dict]:
    return {str(row["table_name"]): row for row in rows}


def table_delta_rows(before_status: list[dict], after_status: list[dict]) -> list[dict]:
    before = table_status_lookup(before_status)
    after = table_status_lookup(after_status)
    rows = []
    for table_name in TABLE_NAMES:
        b = before.get(table_name, {})
        a = after.get(table_name, {})
        rows.append(
            {
                "table_name": table_name,
                "before_missing_required_count": safe_int(b.get("missing_required_count")),
                "after_missing_required_count": safe_int(a.get("missing_required_count")),
                "missing_required_delta": safe_int(a.get("missing_required_count")) - safe_int(b.get("missing_required_count")),
                "before_dtype_failure_count": safe_int(b.get("dtype_failure_count")),
                "after_dtype_failure_count": safe_int(a.get("dtype_failure_count")),
                "before_cross_table_failure_count": safe_int(b.get("cross_table_failure_count")),
                "after_cross_table_failure_count": safe_int(a.get("cross_table_failure_count")),
            }
        )
    return rows


def summarize_recovered_scaffold(
    evidence_rows: list[dict],
    before_summary: dict,
    after_summary: dict,
    before_status: list[dict],
    after_status: list[dict],
) -> dict:
    deltas = table_delta_rows(before_status, after_status)
    session_delta = next(row for row in deltas if row["table_name"] == "session_log")
    return {
        "policy_label": "gssi51600s_recovered_session_collection_scaffold",
        "source_scaffold_run": DEFAULT_SCAFFOLD_RUN,
        "source_scaffold_validation_run": DEFAULT_SCAFFOLD_VALIDATION_RUN,
        "source_recovery_run": DEFAULT_RECOVERY_RUN,
        "candidate_session_prefill_field_count": len(SESSION_PREFILL_FIELDS),
        "applied_session_prefill_field_count": sum(boolish(row["applied"]) for row in evidence_rows),
        "before_missing_required_value_count": safe_int(before_summary.get("missing_required_value_count")),
        "after_missing_required_value_count": safe_int(after_summary.get("missing_required_value_count")),
        "missing_required_delta": safe_int(after_summary.get("missing_required_value_count")) - safe_int(before_summary.get("missing_required_value_count")),
        "before_session_missing_required_count": safe_int(session_delta["before_missing_required_count"]),
        "after_session_missing_required_count": safe_int(session_delta["after_missing_required_count"]),
        "session_missing_required_delta": safe_int(session_delta["missing_required_delta"]),
        "after_dtype_failure_count": safe_int(after_summary.get("dtype_failure_count")),
        "after_cross_table_failure_count": safe_int(after_summary.get("cross_table_failure_count")),
        "ready_for_collection": True,
        "ready_for_packet_acceptance": boolish(after_summary.get("ready_for_packet_acceptance")),
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_field_3d_hpc": False,
        "gpu_priority": "none",
        "residual_blocker_groups": (
            "date_operator_session_verification, target_truth, surveyed_profile_geometry, "
            "controlled_tx_rx_offset, coupling_condition, measured_time_zero_references, "
            "amplitude_references"
        ),
        "decision": (
            "Recovered current-archive DZX metadata can prefill same-system session fields in the "
            "controlled collection scaffold, reducing worksheet blockers. It remains a collection "
            "worksheet only: measured target, survey, acquisition, time-zero, and amplitude fields "
            "must still be collected before packet acceptance or field inversion."
        ),
    }


def plot_recovered_scaffold(summary: dict, delta_rows: list[dict], evidence_rows: list[dict], save_path: Path) -> str:
    labels = [row["table_name"] for row in delta_rows]
    before = [safe_int(row["before_missing_required_count"]) for row in delta_rows]
    after = [safe_int(row["after_missing_required_count"]) for row in delta_rows]
    x = np.arange(len(labels))

    fig, axes = plt.subplots(1, 2, figsize=(15.0, 5.4), constrained_layout=True)
    width = 0.36
    axes[0].bar(x - width / 2, before, width=width, label="scaffold", color="#bab0ac")
    axes[0].bar(x + width / 2, after, width=width, label="recovered scaffold", color="#4e79a7")
    axes[0].set_xticks(x, [label.replace("_", "\n") for label in labels], fontsize=8)
    axes[0].set_ylabel("missing required fields")
    axes[0].set_title("Scaffold validation blockers")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    field_labels = [row["field_name"].replace("_", "\n") for row in evidence_rows]
    applied = [1 if boolish(row["applied"]) else 0 for row in evidence_rows]
    axes[1].bar(np.arange(len(evidence_rows)), applied, color=["#59a14f" if value else "#e15759" for value in applied])
    axes[1].set_xticks(np.arange(len(evidence_rows)), field_labels, fontsize=8)
    axes[1].set_ylim(0, 1.2)
    axes[1].set_ylabel("applied")
    axes[1].set_title("Recovered session prefill")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.98,
        0.94,
        f"applied={summary['applied_session_prefill_field_count']}\n"
        f"missing delta={summary['missing_required_delta']}\n"
        f"packet ready={summary['ready_for_packet_acceptance']}\n"
        f"GPU={summary['gpu_priority']}",
        transform=axes[1].transAxes,
        va="top",
        ha="right",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI recovered-session collection scaffold", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `gssi51600s_recovered_session_collection_scaffold.png`",
                "",
                "This CPU-only figure shows the validation-blocker reduction from applying",
                "recovered DZX session metadata to the controlled collection scaffold.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Applied session prefill fields: `{summary['applied_session_prefill_field_count']}`.",
                f"Missing required values: `{summary['before_missing_required_value_count']}` -> "
                f"`{summary['after_missing_required_value_count']}`.",
                f"Ready for packet acceptance: `{summary['ready_for_packet_acceptance']}`.",
                f"Ready for field FWI/heavy work/3D: `False`.",
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
    parser.add_argument("--scaffold-run", default=DEFAULT_SCAFFOLD_RUN)
    parser.add_argument("--scaffold-validation-run", default=DEFAULT_SCAFFOLD_VALIDATION_RUN)
    parser.add_argument("--recovery-run", default=DEFAULT_RECOVERY_RUN)
    parser.add_argument("--run-name", default="gssi51600s_recovered_session_collection_scaffold")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    scaffold_packet_dir = dataset_root / args.scaffold_run / "packet_scaffold"
    scaffold_validation_dir = dataset_root / args.scaffold_validation_run / "data"
    recovered_packet_dir = dataset_root / args.recovery_run / "packet_recovered"
    validation_rules = default_paths(dataset_root, "141_gssi51600s_controlled_2d_packet_builder")["validation_rules"]

    scaffold_packet = load_packet(scaffold_packet_dir)
    recovered_packet = load_packet(recovered_packet_dir)
    output_packet, evidence_rows = apply_recovered_session_metadata(scaffold_packet, recovered_packet)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    packet_dir = outdir / "packet_scaffold_recovered_session"
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    write_packet(packet_dir, output_packet)

    after_summary, after_findings, after_status, after_acceptance = validate_packet(packet_dir, validation_rules)
    before_summary = read_json(scaffold_validation_dir / "controlled_2d_packet_validation_summary.json")
    before_status = read_csv_rows(scaffold_validation_dir / "controlled_2d_packet_table_status.csv")
    delta_rows = table_delta_rows(before_status, after_status)
    summary = summarize_recovered_scaffold(evidence_rows, before_summary, after_summary, before_status, after_status)

    evidence_csv = data_dir / "recovered_session_collection_scaffold_evidence.csv"
    delta_csv = data_dir / "recovered_session_collection_scaffold_table_delta.csv"
    findings_csv = data_dir / "controlled_2d_packet_validation_findings.csv"
    table_status_csv = data_dir / "controlled_2d_packet_table_status.csv"
    acceptance_csv = data_dir / "controlled_2d_packet_acceptance_status.csv"
    summary_json = data_dir / "recovered_session_collection_scaffold_summary.json"
    figure_path = figures_dir / "gssi51600s_recovered_session_collection_scaffold.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"
    validation_csv = data_dir / "figure_validation.csv"

    write_csv(evidence_csv, [json_safe(row) for row in evidence_rows])
    write_csv(delta_csv, [json_safe(row) for row in delta_rows])
    write_csv(findings_csv, [json_safe(row) for row in after_findings])
    write_csv(table_status_csv, [json_safe(row) for row in after_status])
    write_csv(acceptance_csv, [json_safe(row) for row in after_acceptance])
    plot_recovered_scaffold(summary, delta_rows, evidence_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "source_scaffold_packet_dir": str(scaffold_packet_dir),
        "source_recovered_packet_dir": str(recovered_packet_dir),
        "recovered_scaffold_packet_dir": str(packet_dir),
        "validation_rules": str(validation_rules),
        "evidence_csv": str(evidence_csv),
        "table_delta_csv": str(delta_csv),
        "findings_csv": str(findings_csv),
        "table_status_csv": str(table_status_csv),
        "acceptance_csv": str(acceptance_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "gssi51600s_recovered_session_collection_scaffold",
        {
            "summary_json": str(summary_json),
            "evidence_csv": str(evidence_csv),
            "table_delta_csv": str(delta_csv),
            "recovered_scaffold_packet_dir": str(packet_dir),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

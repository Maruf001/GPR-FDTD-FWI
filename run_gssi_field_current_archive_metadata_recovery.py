#!/usr/bin/env python3
"""Recover current-archive packet metadata from raw GSSI DZX sidecars."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
import xml.etree.ElementTree as ET
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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, DEFAULT_INPUT_DIR, field_dataset_output_root  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_controlled_2d_acquisition_protocol import read_csv_rows  # noqa: E402
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
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import boolish, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CURRENT_PACKET_RUN = "143_gssi51600s_current_archive_packet_prefill"
DEFAULT_CURRENT_VALIDATION_RUN = "144_gssi51600s_current_archive_packet_prefill_validation"
RECOVERABLE_SESSION_FIELDS = {
    "antenna_serial": "antSerialNumber",
    "gain_setting": "displayGain",
}


def read_csv_dicts(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def first_text(root: ET.Element, tag_name: str) -> str:
    for element in root.iter():
        if local_name(element.tag) == tag_name and element.text is not None:
            text = element.text.strip()
            if text:
                return text
    return ""


def parse_dzx_recovery_metadata(path: Path) -> dict:
    root = ET.parse(path).getroot()
    return {
        "file_name": path.with_suffix(".DZT").name,
        "dzx_path": str(path),
        "antSerialNumber": first_text(root, "antSerialNumber"),
        "displayGain": first_text(root, "displayGain"),
        "antModelNumber": first_text(root, "antModelNumber"),
        "system": first_text(root, "system"),
        "softwareVersion": first_text(root, "softwareVersion"),
    }


def nonempty(value: object) -> bool:
    return str(value if value is not None else "").strip() != ""


def consistent_value(rows: list[dict], field_name: str) -> tuple[str, bool, int]:
    values = {str(row.get(field_name, "")).strip() for row in rows if nonempty(row.get(field_name))}
    if len(values) == 1:
        return next(iter(values)), True, len(rows)
    return "", False, len(rows)


def load_packet(packet_dir: Path) -> dict[str, list[dict]]:
    return {
        table_name: read_csv_dicts(packet_dir / f"{table_name}.csv")
        for table_name in TABLE_NAMES
    }


def write_packet(packet_dir: Path, packet: dict[str, list[dict]]) -> None:
    packet_dir.mkdir(parents=True, exist_ok=True)
    for table_name, rows in packet.items():
        write_csv(packet_dir / f"{table_name}.csv", [json_safe(row) for row in rows])


def dzx_paths_for_packet(packet: dict[str, list[dict]], input_dir: Path) -> list[Path]:
    out = []
    for row in packet.get("acquisition_run", []):
        file_name = str(row.get("file_name", "")).strip()
        if not file_name:
            continue
        out.append(input_dir / Path(file_name).with_suffix(".DZX").name)
    return out


def recover_session_metadata(packet: dict[str, list[dict]], dzx_rows: list[dict]) -> tuple[dict[str, list[dict]], list[dict]]:
    recovered = deepcopy(packet)
    session_rows = recovered.get("session_log", [])
    session = session_rows[0] if session_rows else {}
    evidence_rows = []

    for packet_field, dzx_field in RECOVERABLE_SESSION_FIELDS.items():
        value, consistent, source_count = consistent_value(dzx_rows, dzx_field)
        previous = str(session.get(packet_field, "")).strip()
        applied = bool(value and consistent and not previous)
        if applied:
            session[packet_field] = value
        evidence_rows.append(
            {
                "table_name": "session_log",
                "field_name": packet_field,
                "source_tag": dzx_field,
                "previous_value": previous,
                "recovered_value": value,
                "source_file_count": source_count,
                "consistent_across_sources": consistent,
                "applied": applied,
                "recovery_scope": "raw_dzx_sidecar",
            }
        )

    evidence_rows.append(
        {
            "table_name": "session_log",
            "field_name": "operator",
            "source_tag": "",
            "previous_value": str(session.get("operator", "")).strip(),
            "recovered_value": "",
            "source_file_count": len(dzx_rows),
            "consistent_across_sources": False,
            "applied": False,
            "recovery_scope": "not_present_in_dzx_or_dzt_strings",
        }
    )
    if session_rows and any(boolish(row["applied"]) for row in evidence_rows):
        suffix = " Recovered antenna serial and display gain from consistent raw DZX sidecars."
        session["notes"] = f"{str(session.get('notes', '')).strip()}{suffix}".strip()
    return recovered, evidence_rows


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
    out = []
    for table_name in TABLE_NAMES:
        b = before.get(table_name, {})
        a = after.get(table_name, {})
        out.append(
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
    return out


def summarize_recovery(
    evidence_rows: list[dict],
    before_summary: dict,
    after_summary: dict,
    before_status: list[dict],
    after_status: list[dict],
    dzx_rows: list[dict],
) -> dict:
    deltas = table_delta_rows(before_status, after_status)
    session_delta = next(row for row in deltas if row["table_name"] == "session_log")
    return {
        "policy_label": "gssi51600s_current_archive_metadata_recovery",
        "source_current_packet_run": DEFAULT_CURRENT_PACKET_RUN,
        "source_current_validation_run": DEFAULT_CURRENT_VALIDATION_RUN,
        "dzx_sidecar_count": len(dzx_rows),
        "recoverable_field_count": len([row for row in evidence_rows if row["source_tag"]]),
        "applied_recovered_field_count": sum(boolish(row["applied"]) for row in evidence_rows),
        "before_missing_required_value_count": safe_int(before_summary.get("missing_required_value_count")),
        "after_missing_required_value_count": safe_int(after_summary.get("missing_required_value_count")),
        "missing_required_delta": safe_int(after_summary.get("missing_required_value_count")) - safe_int(before_summary.get("missing_required_value_count")),
        "before_session_missing_required_count": safe_int(session_delta["before_missing_required_count"]),
        "after_session_missing_required_count": safe_int(session_delta["after_missing_required_count"]),
        "session_missing_required_delta": safe_int(session_delta["missing_required_delta"]),
        "after_dtype_failure_count": safe_int(after_summary.get("dtype_failure_count")),
        "after_cross_table_failure_count": safe_int(after_summary.get("cross_table_failure_count")),
        "after_acceptance_gate_count": safe_int(after_summary.get("acceptance_gate_count")),
        "ready_for_packet_acceptance": boolish(after_summary.get("ready_for_packet_acceptance")),
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_field_3d_hpc": False,
        "gpu_priority": "none",
        "unrecovered_blocker_groups": (
            "operator, target_truth, surveyed_profile_endpoints, target_crossings, "
            "controlled_tx_rx_offset, coupling_condition, external_time_zero_references, "
            "amplitude_references"
        ),
        "decision": (
            "Raw DZX sidecars recover antenna serial and display gain for the current archive packet, "
            "reducing session-log blockers only. The packet still lacks operator, known target truth, "
            "surveyed geometry, controlled acquisition links, and external timing/amplitude references; "
            "field FWI, heavy field compute, and field 3D/HPC remain blocked."
        ),
    }


def plot_recovery(summary: dict, delta_rows: list[dict], evidence_rows: list[dict], save_path: Path) -> str:
    labels = [row["table_name"] for row in delta_rows]
    before = [safe_int(row["before_missing_required_count"]) for row in delta_rows]
    after = [safe_int(row["after_missing_required_count"]) for row in delta_rows]
    x = np.arange(len(labels))
    applied = [row for row in evidence_rows if boolish(row["applied"])]

    fig, axes = plt.subplots(1, 2, figsize=(15.0, 5.4), constrained_layout=True)
    width = 0.36
    axes[0].bar(x - width / 2, before, width=width, label="before", color="#bab0ac")
    axes[0].bar(x + width / 2, after, width=width, label="after", color="#4e79a7")
    axes[0].set_xticks(x, [label.replace("_", "\n") for label in labels], fontsize=8)
    axes[0].set_ylabel("missing required fields")
    axes[0].set_title("Validation blockers before/after recovery")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    field_labels = [row["field_name"].replace("_", "\n") for row in evidence_rows]
    field_values = [1 if boolish(row["applied"]) else 0 for row in evidence_rows]
    colors = ["#59a14f" if value else "#e15759" for value in field_values]
    axes[1].bar(np.arange(len(evidence_rows)), field_values, color=colors)
    axes[1].set_xticks(np.arange(len(evidence_rows)), field_labels, fontsize=8)
    axes[1].set_ylim(0, 1.2)
    axes[1].set_ylabel("applied")
    axes[1].set_title("DZX session-field recovery")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.98,
        0.94,
        f"applied={len(applied)}\n"
        f"missing delta={summary['missing_required_delta']}\n"
        f"packet ready={summary['ready_for_packet_acceptance']}\n"
        f"GPU={summary['gpu_priority']}",
        transform=axes[1].transAxes,
        va="top",
        ha="right",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI current archive metadata recovery", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `gssi51600s_current_archive_metadata_recovery.png`",
                "",
                "This CPU-only figure shows how much raw DZX sidecar metadata can recover",
                "from the current archive controlled-acquisition packet.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"DZX sidecars scanned: `{summary['dzx_sidecar_count']}`.",
                f"Applied recovered fields: `{summary['applied_recovered_field_count']}`.",
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
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--current-packet-run", default=DEFAULT_CURRENT_PACKET_RUN)
    parser.add_argument("--current-validation-run", default=DEFAULT_CURRENT_VALIDATION_RUN)
    parser.add_argument("--run-name", default="gssi51600s_current_archive_metadata_recovery")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    current_packet_dir = dataset_root / args.current_packet_run / "packet"
    current_validation_dir = dataset_root / args.current_validation_run / "data"
    validation_rules = default_paths(dataset_root, "141_gssi51600s_controlled_2d_packet_builder")["validation_rules"]
    input_dir = Path(args.input_dir)

    current_packet = load_packet(current_packet_dir)
    dzx_paths = dzx_paths_for_packet(current_packet, input_dir)
    dzx_rows = [parse_dzx_recovery_metadata(path) for path in dzx_paths if path.exists()]
    recovered_packet, evidence_rows = recover_session_metadata(current_packet, dzx_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    packet_dir = outdir / "packet_recovered"
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    write_packet(packet_dir, recovered_packet)

    after_summary, after_findings, after_status, after_acceptance = validate_packet(packet_dir, validation_rules)
    before_summary = read_json(current_validation_dir / "controlled_2d_packet_validation_summary.json")
    before_status = read_csv_dicts(current_validation_dir / "controlled_2d_packet_table_status.csv")
    delta_rows = table_delta_rows(before_status, after_status)
    summary = summarize_recovery(evidence_rows, before_summary, after_summary, before_status, after_status, dzx_rows)

    evidence_csv = data_dir / "current_archive_metadata_recovery_evidence.csv"
    dzx_csv = data_dir / "current_archive_dzx_recovery_metadata.csv"
    delta_csv = data_dir / "current_archive_metadata_recovery_table_delta.csv"
    findings_csv = data_dir / "controlled_2d_packet_validation_findings.csv"
    table_status_csv = data_dir / "controlled_2d_packet_table_status.csv"
    acceptance_csv = data_dir / "controlled_2d_packet_acceptance_status.csv"
    summary_json = data_dir / "current_archive_metadata_recovery_summary.json"
    figure_path = figures_dir / "gssi51600s_current_archive_metadata_recovery.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"
    validation_csv = data_dir / "figure_validation.csv"

    write_csv(evidence_csv, [json_safe(row) for row in evidence_rows])
    write_csv(dzx_csv, [json_safe(row) for row in dzx_rows])
    write_csv(delta_csv, [json_safe(row) for row in delta_rows])
    write_csv(findings_csv, [json_safe(row) for row in after_findings])
    write_csv(table_status_csv, [json_safe(row) for row in after_status])
    write_csv(acceptance_csv, [json_safe(row) for row in after_acceptance])
    plot_recovery(summary, delta_rows, evidence_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "source_packet_dir": str(current_packet_dir),
        "recovered_packet_dir": str(packet_dir),
        "validation_rules": str(validation_rules),
        "evidence_csv": str(evidence_csv),
        "dzx_metadata_csv": str(dzx_csv),
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
        "gssi51600s_current_archive_metadata_recovery",
        {
            "summary_json": str(summary_json),
            "evidence_csv": str(evidence_csv),
            "table_delta_csv": str(delta_csv),
            "recovered_packet_dir": str(packet_dir),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

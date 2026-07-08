#!/usr/bin/env python3
"""Compare current-archive packet validation against the controlled scaffold."""

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
import numpy as np  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import boolish, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CURRENT_VALIDATION_RUN = "144_gssi51600s_current_archive_packet_prefill_validation"
DEFAULT_SCAFFOLD_VALIDATION_RUN = "148_gssi51600s_controlled_collection_scaffold_validation"
DEFAULT_SCAFFOLD_RUN = "147_gssi51600s_controlled_collection_scaffold"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def parse_evidence(text: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for part in str(text).split(";"):
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        out[key.strip()] = safe_int(value.strip())
    return out


def by_key(rows: list[dict], key: str) -> dict[str, dict]:
    return {str(row[key]): row for row in rows}


def table_delta_rows(current_rows: list[dict], scaffold_rows: list[dict]) -> list[dict]:
    current = by_key(current_rows, "table_name")
    scaffold = by_key(scaffold_rows, "table_name")
    rows = []
    for table_name in sorted(set(current) | set(scaffold)):
        c = current.get(table_name, {})
        s = scaffold.get(table_name, {})
        rows.append(
            {
                "table_name": table_name,
                "current_row_count": safe_int(c.get("row_count")),
                "scaffold_row_count": safe_int(s.get("row_count")),
                "row_count_delta": safe_int(s.get("row_count")) - safe_int(c.get("row_count")),
                "current_filled_row_count": safe_int(c.get("filled_row_count")),
                "scaffold_filled_row_count": safe_int(s.get("filled_row_count")),
                "filled_row_delta": safe_int(s.get("filled_row_count")) - safe_int(c.get("filled_row_count")),
                "current_missing_required_count": safe_int(c.get("missing_required_count")),
                "scaffold_missing_required_count": safe_int(s.get("missing_required_count")),
                "missing_required_delta": safe_int(s.get("missing_required_count")) - safe_int(c.get("missing_required_count")),
                "current_cross_table_failure_count": safe_int(c.get("cross_table_failure_count")),
                "scaffold_cross_table_failure_count": safe_int(s.get("cross_table_failure_count")),
            }
        )
    return rows


def gate_delta_rows(current_rows: list[dict], scaffold_rows: list[dict]) -> list[dict]:
    current = by_key(current_rows, "gate_key")
    scaffold = by_key(scaffold_rows, "gate_key")
    rows = []
    for gate_key in sorted(set(current) | set(scaffold)):
        c = current.get(gate_key, {})
        s = scaffold.get(gate_key, {})
        c_evidence = parse_evidence(c.get("evidence", ""))
        s_evidence = parse_evidence(s.get("evidence", ""))
        metric_keys = sorted(set(c_evidence) | set(s_evidence))
        if metric_keys:
            metric_delta = ";".join(
                f"{key}:{c_evidence.get(key, 0)}->{s_evidence.get(key, 0)}"
                for key in metric_keys
            )
        else:
            metric_delta = ""
        rows.append(
            {
                "gate_key": gate_key,
                "current_ready": boolish(c.get("ready")),
                "scaffold_ready": boolish(s.get("ready")),
                "current_evidence": c.get("evidence", ""),
                "scaffold_evidence": s.get("evidence", ""),
                "evidence_delta": metric_delta,
                "ready_state_change": f"{boolish(c.get('ready'))}->{boolish(s.get('ready'))}",
                "blocks_if_fail": s.get("blocks_if_fail") or c.get("blocks_if_fail", ""),
            }
        )
    return rows


def summarize_delta(
    current_summary: dict,
    scaffold_summary: dict,
    scaffold_plan_summary: dict,
    table_rows: list[dict],
    gate_rows: list[dict],
) -> dict:
    current_ready_gates = sum(boolish(row["current_ready"]) for row in gate_rows)
    scaffold_ready_gates = sum(boolish(row["scaffold_ready"]) for row in gate_rows)
    target_gate = next(row for row in gate_rows if row["gate_key"] == "target_truth_controls")
    repeat_gate = next(row for row in gate_rows if row["gate_key"] == "short_repeat_redundancy")
    t0_gate = next(row for row in gate_rows if row["gate_key"] == "absolute_time_zero_references")
    amp_gate = next(row for row in gate_rows if row["gate_key"] == "amplitude_references")
    return {
        "policy_label": "gssi51600s_scaffold_validation_delta",
        "current_validation_run": DEFAULT_CURRENT_VALIDATION_RUN,
        "scaffold_validation_run": DEFAULT_SCAFFOLD_VALIDATION_RUN,
        "current_total_row_count": current_summary.get("total_row_count"),
        "scaffold_total_row_count": scaffold_summary.get("total_row_count"),
        "current_filled_row_count": current_summary.get("filled_row_count"),
        "scaffold_filled_row_count": scaffold_summary.get("filled_row_count"),
        "filled_row_delta": safe_int(scaffold_summary.get("filled_row_count")) - safe_int(current_summary.get("filled_row_count")),
        "current_missing_required_value_count": current_summary.get("missing_required_value_count"),
        "scaffold_missing_required_value_count": scaffold_summary.get("missing_required_value_count"),
        "missing_required_delta": safe_int(scaffold_summary.get("missing_required_value_count")) - safe_int(current_summary.get("missing_required_value_count")),
        "current_cross_table_failure_count": current_summary.get("cross_table_failure_count"),
        "scaffold_cross_table_failure_count": scaffold_summary.get("cross_table_failure_count"),
        "current_ready_gate_count": current_ready_gates,
        "scaffold_ready_gate_count": scaffold_ready_gates,
        "gate_count": len(gate_rows),
        "target_truth_evidence_delta": target_gate["evidence_delta"],
        "short_repeat_evidence_delta": repeat_gate["evidence_delta"],
        "time_zero_reference_evidence_delta": t0_gate["evidence_delta"],
        "amplitude_reference_evidence_delta": amp_gate["evidence_delta"],
        "planned_time_zero_reference_count": scaffold_plan_summary.get("planned_time_zero_reference_count"),
        "planned_amplitude_reference_count": scaffold_plan_summary.get("planned_amplitude_reference_count"),
        "ready_for_collection": scaffold_plan_summary.get("ready_for_collection"),
        "ready_for_packet_acceptance": False,
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_field_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "The scaffold improves structural readiness: it fills all planned rows, removes cross-table "
            "ambiguity, adds target-truth and short-repeat evidence, and reduces required-field blockers "
            "from 67 to 60. It still lacks measured target geometry, time-zero values, amplitude metrics, "
            "survey coordinates, Tx/Rx offsets, coupling, and session details, so all acceptance gates remain "
            "blocked and field inversion/heavy compute remain disallowed."
        ),
    }


def plot_delta(table_rows: list[dict], gate_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 5.6), constrained_layout=True)
    labels = [row["table_name"] for row in table_rows]
    x = np.arange(len(labels))
    width = 0.36
    axes[0].bar(
        x - width / 2,
        [safe_int(row["current_missing_required_count"]) for row in table_rows],
        width=width,
        label="current archive packet",
        color="#9c755f",
    )
    axes[0].bar(
        x + width / 2,
        [safe_int(row["scaffold_missing_required_count"]) for row in table_rows],
        width=width,
        label="collection scaffold",
        color="#4c78a8",
    )
    axes[0].set_xticks(x, [label.replace("_", "\n") for label in labels], fontsize=8)
    axes[0].set_ylabel("missing required fields")
    axes[0].set_title("Validation blockers by table")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    gate_labels = [row["gate_key"] for row in gate_rows]
    scaffold_blocked = [0 if boolish(row["scaffold_ready"]) else 1 for row in gate_rows]
    axes[1].bar(
        range(len(gate_labels)),
        scaffold_blocked,
        color=["#54a24b" if value == 0 else "#e45756" for value in scaffold_blocked],
        width=0.62,
    )
    axes[1].set_xticks(range(len(gate_labels)), [label.replace("_", "\n") for label in gate_labels], fontsize=8)
    axes[1].set_yticks([0, 1], ["ready", "blocked"])
    axes[1].set_ylim(0, 1.2)
    axes[1].set_title("Scaffold acceptance gate blockers")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("GSSI scaffold validation delta", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_scaffold_validation_delta.png`",
                "",
                "This figure compares the current archive prefill validation with the",
                "controlled-collection scaffold validation. It does not run FDTD, FWI,",
                "GPU kernels, field FWI, 3D/HPC work, or neural-network training.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Missing required fields: `{summary['current_missing_required_value_count']}` -> `{summary['scaffold_missing_required_value_count']}`.",
                f"Filled rows: `{summary['current_filled_row_count']}` -> `{summary['scaffold_filled_row_count']}`.",
                f"Ready gates: `{summary['current_ready_gate_count']}` -> `{summary['scaffold_ready_gate_count']}`.",
                f"Ready for packet acceptance: `{summary['ready_for_packet_acceptance']}`.",
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
    parser.add_argument("--current-validation-run", default=DEFAULT_CURRENT_VALIDATION_RUN)
    parser.add_argument("--scaffold-validation-run", default=DEFAULT_SCAFFOLD_VALIDATION_RUN)
    parser.add_argument("--scaffold-run", default=DEFAULT_SCAFFOLD_RUN)
    parser.add_argument("--run-name", default="gssi51600s_scaffold_validation_delta")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    current_dir = dataset_root / args.current_validation_run / "data"
    scaffold_dir = dataset_root / args.scaffold_validation_run / "data"
    scaffold_plan_dir = dataset_root / args.scaffold_run / "data"

    current_summary = read_json(current_dir / "controlled_2d_packet_validation_summary.json")
    scaffold_summary = read_json(scaffold_dir / "controlled_2d_packet_validation_summary.json")
    scaffold_plan_summary = read_json(scaffold_plan_dir / "field_controlled_collection_scaffold_summary.json")
    tables = table_delta_rows(
        read_csv_rows(current_dir / "controlled_2d_packet_table_status.csv"),
        read_csv_rows(scaffold_dir / "controlled_2d_packet_table_status.csv"),
    )
    gates = gate_delta_rows(
        read_csv_rows(current_dir / "controlled_2d_packet_acceptance_status.csv"),
        read_csv_rows(scaffold_dir / "controlled_2d_packet_acceptance_status.csv"),
    )
    summary = summarize_delta(current_summary, scaffold_summary, scaffold_plan_summary, tables, gates)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    write_csv(data_dir / "field_scaffold_validation_table_delta.csv", tables)
    write_csv(data_dir / "field_scaffold_validation_gate_delta.csv", gates)
    summary_path = data_dir / "field_scaffold_validation_delta_summary.json"
    summary_path.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")

    fig_path = figures_dir / "field_scaffold_validation_delta.png"
    plot_delta(tables, gates, summary, fig_path)
    write_figure_notes(figures_dir / "FIGURE_NOTES.md", summary)
    write_csv(data_dir / "figure_validation.csv", [figure_stats(fig_path)])
    write_run_manifest(
        str(outdir),
        "gssi51600s_scaffold_validation_delta",
        {
            "summary": json_safe(summary),
            "paths": {
                "current_validation_summary_json": str(current_dir / "controlled_2d_packet_validation_summary.json"),
                "scaffold_validation_summary_json": str(scaffold_dir / "controlled_2d_packet_validation_summary.json"),
                "summary_json": str(summary_path),
                "figure": str(fig_path),
            },
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

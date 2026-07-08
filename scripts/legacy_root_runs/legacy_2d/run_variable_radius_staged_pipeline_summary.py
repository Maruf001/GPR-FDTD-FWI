#!/usr/bin/env python3
"""Summarize staged variable-radius multi-rebar pipeline runs."""

from __future__ import annotations

import argparse
import csv
import json
import os
import shlex
import sys
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
from run_multi_rebar_joint_radius_profile import read_candidates_csv, rank_joint_radius_candidates  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def load_json(path):
    """Load JSON from disk."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_case_spec(text):
    """Parse label|detection|location|focused|joint[|focused_refinement] case spec."""
    parts = [part.strip() for part in str(text).split("|")]
    if len(parts) not in (5, 6) or any(not part for part in parts):
        raise argparse.ArgumentTypeError(
            "case spec must be label|detection_json|location_json|focused_json|joint_json"
            "[|focused_refinement_json]"
        )
    return {
        "label": parts[0],
        "detection_json": parts[1],
        "location_json": parts[2],
        "focused_json": parts[3],
        "joint_json": parts[4],
        "focused_refinement_json": parts[5] if len(parts) == 6 else None,
    }


def format_case_spec(case_spec):
    """Return the CLI case spec string for a parsed case dictionary."""
    parts = [
        case_spec["label"],
        case_spec["detection_json"],
        case_spec["location_json"],
        case_spec["focused_json"],
        case_spec["joint_json"],
    ]
    if case_spec.get("focused_refinement_json"):
        parts.append(case_spec["focused_refinement_json"])
    return "|".join(str(part) for part in parts)


def vector_abs_errors(values, truth):
    """Return per-value absolute errors."""
    return [abs(float(value) - float(target)) for value, target in zip(values, truth)]


def max_abs_error(values, truth):
    """Return maximum absolute error for same-length vectors."""
    errors = vector_abs_errors(values, truth)
    return max(errors) if errors else np.nan


def _state_vectors(summary):
    state = summary["final_state"]
    return (
        list(state["x_values_mm"]),
        list(state["z_values_mm"]),
        list(state["radii_mm"]),
    )


def _interval_width(row, min_key, max_key):
    lower = row.get(min_key)
    upper = row.get(max_key)
    if lower in (None, "") or upper in (None, ""):
        return None
    return max(0.0, float(upper) - float(lower))


def coordinate_confidence_metrics(summary, truth_x, truth_z, truth_r):
    """Summarize coordinate confidence rows for staged-policy decisions."""
    rows = list(summary.get("confidence_rows") or [])
    acquisition = {
        "sources": summary.get("sources"),
        "tx_rx_offset_mm": summary.get("tx_rx_offset_mm"),
        "frequency_ghz": summary.get("frequency_ghz"),
    }
    if not rows:
        return {
            **acquisition,
            "row_count": 0,
            "truth_geometry_count": 0,
            "x_ambiguity_row_count": 0,
            "x_ambiguity_width_max_mm": np.nan,
        }
    x_widths = []
    truth_count = 0
    for row in rows:
        target_index = int(row["step_target_index"])
        best_x = float(row["best_x_mm"])
        best_z = float(row["best_z_mm"])
        best_radius = float(row["best_radius_mm"])
        if (
            abs(best_x - float(truth_x[target_index])) <= 1.0e-9
            and abs(best_z - float(truth_z[target_index])) <= 1.0e-9
            and abs(best_radius - float(truth_r[target_index])) <= 1.0e-9
        ):
            truth_count += 1
        width = _interval_width(row, "ambiguity_x_min_mm", "ambiguity_x_max_mm")
        if width is not None:
            x_widths.append(width)
    return {
        **acquisition,
        "row_count": len(rows),
        "truth_geometry_count": truth_count,
        "x_ambiguity_row_count": sum(1 for width in x_widths if width > 0.0),
        "x_ambiguity_width_max_mm": max(x_widths) if x_widths else np.nan,
    }


def focus_policy(focused_metrics, refined_metrics=None):
    """Return the packaged focused-polish policy from ambiguity summaries."""
    focused_ambiguous = focused_metrics["x_ambiguity_row_count"] > 0
    if refined_metrics and refined_metrics["x_ambiguity_row_count"] == 0:
        if focused_ambiguous:
            return "use_refined_focus_for_point_x"
        return "refined_focus_confirms_point_x"
    if focused_ambiguous:
        return "report_focused_x_interval"
    return "standard_focus_point_ok"


def _candidate_csv_from_joint_summary(joint_summary, joint_json_path):
    paths = joint_summary.get("paths") or {}
    candidate_csv = paths.get("candidate_csv")
    if not candidate_csv:
        return None
    path = Path(candidate_csv)
    if path.exists():
        return path
    joint_parent = Path(joint_json_path).parent if joint_json_path else None
    if joint_parent is not None:
        fallback = joint_parent / Path(candidate_csv).name
        if fallback.exists():
            return fallback
    return None


def _ranked_rows_for_update_case(joint_summary, joint_json_path=None):
    label = joint_summary.get("update_case_label")
    if label is None:
        label = next(iter(joint_summary["ranked_by_case"]))
    candidate_csv = _candidate_csv_from_joint_summary(joint_summary, joint_json_path)
    if candidate_csv is not None:
        return label, rank_joint_radius_candidates(read_candidates_csv(candidate_csv), label)
    return label, list(joint_summary["ranked_by_case"][label])


def truth_tuple_rank(ranked_rows, truth_radii):
    """Return rank of the truth radius tuple in available ranked rows."""
    truth = [float(value) for value in truth_radii]
    for index, row in enumerate(ranked_rows, start=1):
        if [float(value) for value in row["radii_mm"]] == truth:
            return index
    return None


def summarize_case(case_spec):
    """Summarize one staged pipeline case."""
    detection = load_json(case_spec["detection_json"])
    location = load_json(case_spec["location_json"])
    focused = load_json(case_spec["focused_json"])
    joint = load_json(case_spec["joint_json"])
    refined_focused = (
        load_json(case_spec["focused_refinement_json"])
        if case_spec.get("focused_refinement_json")
        else None
    )
    truth_x = [float(value) for value in detection["truth_x_values_mm"]]
    truth_z = [float(value) for value in detection["truth_z_values_mm"]]
    truth_r = [float(value) for value in detection["truth_radius_values_mm"]]

    loc_x, loc_z, loc_r = _state_vectors(location)
    focus_x, focus_z, focus_r = _state_vectors(focused)
    refined_x, refined_z, refined_r = (
        _state_vectors(refined_focused)
        if refined_focused is not None
        else (None, None, None)
    )
    focused_metrics = coordinate_confidence_metrics(focused, truth_x, truth_z, truth_r)
    refined_metrics = (
        coordinate_confidence_metrics(refined_focused, truth_x, truth_z, truth_r)
        if refined_focused is not None
        else None
    )
    update_case_label, ranked_rows = _ranked_rows_for_update_case(joint, case_spec["joint_json"])
    best_joint = ranked_rows[0]
    next_joint = ranked_rows[1] if len(ranked_rows) > 1 else None
    joint_r = [float(value) for value in best_joint["radii_mm"]]
    next_joint_r = [float(value) for value in next_joint["radii_mm"]] if next_joint else []
    joint_margin_abs = (
        float(next_joint["misfit"]) - float(best_joint["misfit"])
        if next_joint else np.nan
    )
    joint_margin_rel = (
        joint_margin_abs / max(abs(float(best_joint["misfit"])), 1.0e-12)
        if next_joint else np.nan
    )
    joint_x = [float(value) for value in joint.get("candidate_x_values_mm", focus_x)]
    joint_z = [float(value) for value in joint.get("candidate_z_values_mm", focus_z)]

    return {
        "label": case_spec["label"],
        "detection_json": case_spec["detection_json"],
        "location_json": case_spec["location_json"],
        "focused_json": case_spec["focused_json"],
        "focused_refinement_json": case_spec.get("focused_refinement_json"),
        "joint_json": case_spec["joint_json"],
        "truth_x_values_mm": truth_x,
        "truth_z_values_mm": truth_z,
        "truth_radius_values_mm": truth_r,
        "location_final_x_values_mm": [float(value) for value in loc_x],
        "location_final_z_values_mm": [float(value) for value in loc_z],
        "location_final_radius_values_mm": [float(value) for value in loc_r],
        "location_sources": location.get("sources"),
        "location_tx_rx_offset_mm": location.get("tx_rx_offset_mm"),
        "location_frequency_ghz": location.get("frequency_ghz"),
        "focused_final_x_values_mm": [float(value) for value in focus_x],
        "focused_final_z_values_mm": [float(value) for value in focus_z],
        "focused_final_radius_values_mm": [float(value) for value in focus_r],
        "focused_sources": focused_metrics["sources"],
        "focused_tx_rx_offset_mm": focused_metrics["tx_rx_offset_mm"],
        "focused_frequency_ghz": focused_metrics["frequency_ghz"],
        "focused_confidence_row_count": focused_metrics["row_count"],
        "focused_truth_geometry_count": focused_metrics["truth_geometry_count"],
        "focused_x_ambiguity_row_count": focused_metrics["x_ambiguity_row_count"],
        "focused_x_ambiguity_width_max_mm": float(focused_metrics["x_ambiguity_width_max_mm"]),
        "refined_focused_final_x_values_mm": (
            None if refined_x is None else [float(value) for value in refined_x]
        ),
        "refined_focused_final_z_values_mm": (
            None if refined_z is None else [float(value) for value in refined_z]
        ),
        "refined_focused_final_radius_values_mm": (
            None if refined_r is None else [float(value) for value in refined_r]
        ),
        "refined_focused_sources": None if refined_metrics is None else refined_metrics["sources"],
        "refined_focused_tx_rx_offset_mm": (
            None if refined_metrics is None else refined_metrics["tx_rx_offset_mm"]
        ),
        "refined_focused_frequency_ghz": (
            None if refined_metrics is None else refined_metrics["frequency_ghz"]
        ),
        "refined_focused_confidence_row_count": (
            None if refined_metrics is None else refined_metrics["row_count"]
        ),
        "refined_focused_truth_geometry_count": (
            None if refined_metrics is None else refined_metrics["truth_geometry_count"]
        ),
        "refined_focused_x_ambiguity_row_count": (
            None if refined_metrics is None else refined_metrics["x_ambiguity_row_count"]
        ),
        "refined_focused_x_ambiguity_width_max_mm": (
            None if refined_metrics is None else float(refined_metrics["x_ambiguity_width_max_mm"])
        ),
        "focused_policy": focus_policy(focused_metrics, refined_metrics),
        "joint_update_case_label": update_case_label,
        "joint_sources": joint.get("sources"),
        "joint_tx_rx_offset_mm": joint.get("tx_rx_offset_mm"),
        "joint_frequency_ghz": joint.get("frequency_ghz"),
        "joint_best_radius_values_mm": joint_r,
        "joint_best_misfit": float(best_joint["misfit"]),
        "joint_next_radius_values_mm": next_joint_r,
        "joint_next_misfit": float(next_joint["misfit"]) if next_joint else np.nan,
        "joint_margin_abs": float(joint_margin_abs),
        "joint_margin_rel": float(joint_margin_rel),
        "joint_truth_tuple_rank_in_top": truth_tuple_rank(ranked_rows, truth_r),
        "location_max_x_error_mm": max_abs_error(loc_x, truth_x),
        "location_max_z_error_mm": max_abs_error(loc_z, truth_z),
        "location_max_radius_error_mm": max_abs_error(loc_r, truth_r),
        "focused_max_x_error_mm": max_abs_error(focus_x, truth_x),
        "focused_max_z_error_mm": max_abs_error(focus_z, truth_z),
        "focused_max_radius_error_mm": max_abs_error(focus_r, truth_r),
        "refined_focused_max_x_error_mm": (
            None if refined_x is None else max_abs_error(refined_x, truth_x)
        ),
        "refined_focused_max_z_error_mm": (
            None if refined_z is None else max_abs_error(refined_z, truth_z)
        ),
        "refined_focused_max_radius_error_mm": (
            None if refined_r is None else max_abs_error(refined_r, truth_r)
        ),
        "joint_max_x_error_mm": max_abs_error(joint_x, truth_x),
        "joint_max_z_error_mm": max_abs_error(joint_z, truth_z),
        "joint_max_radius_error_mm": max_abs_error(joint_r, truth_r),
    }


def stage_rows(case_summary):
    """Return stage-error rows for plotting/reporting."""
    stages = [
        ("location_only", "location"),
        ("focused_target2", "focused"),
    ]
    rows = []
    for stage_label, prefix in stages:
        rows.append({
            "case": case_summary["label"],
            "stage": stage_label,
            "max_x_error_mm": case_summary[f"{prefix}_max_x_error_mm"],
            "max_z_error_mm": case_summary[f"{prefix}_max_z_error_mm"],
            "max_radius_error_mm": case_summary[f"{prefix}_max_radius_error_mm"],
        })
    if case_summary.get("refined_focused_max_x_error_mm") is not None:
        rows.append({
            "case": case_summary["label"],
            "stage": "focused_target2_refined",
            "max_x_error_mm": case_summary["refined_focused_max_x_error_mm"],
            "max_z_error_mm": case_summary["refined_focused_max_z_error_mm"],
            "max_radius_error_mm": case_summary["refined_focused_max_radius_error_mm"],
        })
    rows.append({
        "case": case_summary["label"],
        "stage": "joint_radius",
        "max_x_error_mm": case_summary["joint_max_x_error_mm"],
        "max_z_error_mm": case_summary["joint_max_z_error_mm"],
        "max_radius_error_mm": case_summary["joint_max_radius_error_mm"],
    })
    return rows


def manifest_path_for_artifact(path):
    """Return the likely run manifest for a data artifact path."""
    artifact = Path(path)
    if artifact.parent.name == "data":
        return artifact.parent.parent / "run_manifest.json"
    return artifact.parent / "run_manifest.json"


def load_manifest_for_artifact(path):
    """Load the run manifest associated with an artifact, if present."""
    manifest_path = manifest_path_for_artifact(path)
    if not manifest_path.exists():
        return str(manifest_path), None
    return str(manifest_path), load_json(manifest_path)


def build_summary_command(run_name, case_specs, outdir=None):
    """Build the staged summary command represented by this report."""
    command = [
        sys.executable,
        "run_variable_radius_staged_pipeline_summary.py",
        "--run-name",
        run_name,
    ]
    if outdir:
        command.extend(["--outdir", str(outdir)])
    for case_spec in case_specs:
        command.extend(["--case", format_case_spec(case_spec)])
    return command


def build_replay_plan(case_summaries, summary_command):
    """Build an ordered dry-run replay plan from stage run manifests."""
    stage_keys = [
        ("detection", "detection_json"),
        ("location_only", "location_json"),
        ("focused_target2", "focused_json"),
        ("focused_target2_refined", "focused_refinement_json"),
        ("joint_radius", "joint_json"),
    ]
    stages = []
    seen_artifacts = set()
    for case_summary in case_summaries:
        for stage_name, artifact_key in stage_keys:
            artifact_json = case_summary.get(artifact_key)
            if not artifact_json or artifact_json in seen_artifacts:
                continue
            seen_artifacts.add(artifact_json)
            manifest_path, manifest = load_manifest_for_artifact(artifact_json)
            command = None if manifest is None else manifest.get("command")
            stages.append({
                "case": case_summary["label"],
                "stage": stage_name,
                "artifact_json": artifact_json,
                "manifest_path": manifest_path,
                "manifest_found": manifest is not None,
                "run_kind": None if manifest is None else manifest.get("run_kind"),
                "command": command,
                "command_available": bool(command),
            })
    return {
        "mode": "dry_run_replay_plan",
        "stage_count": len(stages),
        "command_available_count": sum(1 for stage in stages if stage["command_available"]),
        "stages": stages,
        "summary_command": summary_command,
    }


def write_replay_commands(path, replay_plan):
    """Write shell-quoted replay commands for manual staged rerun planning."""
    lines = [
        "# Staged variable-radius replay command plan.",
        "# This file is intentionally non-executable.",
        "# Review output directory arguments before launching heavy GPU stages.",
        "",
    ]
    for stage in replay_plan["stages"]:
        label = f"{stage['case']} {stage['stage']}"
        lines.append(f"# Stage: {label}")
        if stage.get("command"):
            lines.append(" ".join(shlex.quote(str(part)) for part in stage["command"]))
        else:
            lines.append(f"# Command unavailable; inspect {stage['manifest_path']}")
        lines.append("")
    lines.append("# Summary/report stage")
    lines.append(" ".join(shlex.quote(str(part)) for part in replay_plan["summary_command"]))
    lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def write_rows_csv(path, rows):
    """Write flat rows to CSV."""
    rows = list(rows)
    if not rows:
        raise ValueError("no rows to write")
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_stage_errors(stage_error_rows, save_path):
    """Plot max stage errors for each case."""
    rows = list(stage_error_rows)
    labels = [f"{row['case']}\n{row['stage']}" for row in rows]
    x_errors = [float(row["max_x_error_mm"]) for row in rows]
    z_errors = [float(row["max_z_error_mm"]) for row in rows]
    r_errors = [float(row["max_radius_error_mm"]) for row in rows]
    x = np.arange(len(rows))
    width = 0.25

    fig, ax = plt.subplots(figsize=(max(10.0, 0.85 * len(rows)), 5.6), constrained_layout=True)
    ax.bar(x - width, x_errors, width=width, color="#4C78A8", label="max x error")
    ax.bar(x, z_errors, width=width, color="#F58518", label="max z error")
    ax.bar(x + width, r_errors, width=width, color="#54A24B", label="max radius error")
    ax.set_title("Staged Variable-Radius Pipeline Max Errors")
    ax.set_ylabel("Maximum absolute error [mm]")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(loc="upper right", fontsize=8)
    ymax = max(max(x_errors + z_errors + r_errors) * 1.25, 0.25)
    ax.set_ylim(0.0, ymax)
    if all(error <= 1.0e-12 for error in x_errors + z_errors + r_errors):
        ax.text(
            0.01,
            0.92,
            "All shown stage errors are 0.000 mm",
            transform=ax.transAxes,
            fontsize=9,
            ha="left",
            va="top",
            bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#B0B0B0"},
        )
    return save_validated_figure(fig, save_path)


def _acquisition_text(label, sources, tx_rx_offset_mm, frequency_ghz):
    parts = []
    if sources is not None:
        parts.append(f"sources={sources}")
    if tx_rx_offset_mm is not None:
        parts.append(f"Tx/Rx offset={float(tx_rx_offset_mm):.3g} mm")
    if frequency_ghz is not None:
        parts.append(f"frequency={float(frequency_ghz):.3g} GHz")
    if not parts:
        return f"{label} acquisition=not recorded"
    return f"{label} acquisition=({', '.join(parts)})"


def write_figure_notes(path, case_summaries):
    """Write plain-language figure notes for the staged summary."""
    case_bits = []
    for row in case_summaries:
        acquisition_bits = [
            _acquisition_text(
                "focused",
                row.get("focused_sources"),
                row.get("focused_tx_rx_offset_mm"),
                row.get("focused_frequency_ghz"),
            )
        ]
        if row.get("refined_focused_sources") is not None:
            acquisition_bits.append(
                _acquisition_text(
                    "refined focused",
                    row.get("refined_focused_sources"),
                    row.get("refined_focused_tx_rx_offset_mm"),
                    row.get("refined_focused_frequency_ghz"),
                )
            )
        case_bits.append(
            f"{row['label']}: joint best radii={row['joint_best_radius_values_mm']}, "
            f"truth tuple rank={row['joint_truth_tuple_rank_in_top']}, "
            f"top-2 margin={row['joint_margin_abs']:.5g}, "
            f"focused policy={row['focused_policy']}, "
            f"{' / '.join(acquisition_bits)}"
        )
    text = f"""# Figure Notes

## 1. `staged_variable_radius_pipeline_errors.png` - staged pipeline error reduction

This figure compares maximum absolute geometry error at three stages of the
variable-radius multi-rebar pipeline. The location-only stage corrects x and z
while radius is fixed. The focused-target stage lets the large right bar move
in x, z, and radius. The joint-radius stage holds x/z fixed and estimates all
bar radii together.

Bars show the largest absolute error across the three rebars for x position,
z depth, and radius. A lower bar means that stage is closer to the known
synthetic truth. This plot should be read with the JSON/CSV table because it
compresses per-target errors into a maximum.

Case results: {'; '.join(case_bits)}.
"""
    Path(path).write_text(text, encoding="utf-8")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        action="append",
        required=True,
        type=parse_case_spec,
        help="label|detection_json|location_json|focused_json|joint_json[|focused_refinement_json]",
    )
    parser.add_argument("--run-name", default="variable_radius_staged_pipeline_summary")
    parser.add_argument("--outdir", default=None)
    return parser


def main():
    args = build_parser().parse_args()
    case_summaries = [summarize_case(case_spec) for case_spec in args.case]
    stage_error_rows = [
        row
        for summary in case_summaries
        for row in stage_rows(summary)
    ]

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    case_csv = data_dir / "staged_variable_radius_cases.csv"
    stage_csv = data_dir / "staged_variable_radius_stage_errors.csv"
    json_path = data_dir / "staged_variable_radius_summary.json"
    replay_json_path = data_dir / "staged_variable_radius_replay_plan.json"
    replay_commands_path = data_dir / "staged_variable_radius_replay_commands.txt"
    plot_path = figures_dir / "staged_variable_radius_pipeline_errors.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"
    summary_command = build_summary_command(args.run_name, args.case, args.outdir)
    replay_plan = build_replay_plan(case_summaries, summary_command)
    write_rows_csv(case_csv, case_summaries)
    write_rows_csv(stage_csv, stage_error_rows)
    write_replay_commands(replay_commands_path, replay_plan)
    plot_stage_errors(stage_error_rows, plot_path)
    write_figure_notes(notes_path, case_summaries)
    with replay_json_path.open("w", encoding="utf-8") as handle:
        json.dump(replay_plan, handle, indent=2)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump({
            "case_summaries": case_summaries,
            "stage_error_rows": stage_error_rows,
            "replay_plan": replay_plan,
            "paths": {
                "case_csv": str(case_csv),
                "stage_csv": str(stage_csv),
                "replay_json": str(replay_json_path),
                "replay_commands": str(replay_commands_path),
                "plot": str(plot_path),
                "figure_notes": str(notes_path),
            },
        }, handle, indent=2)
    write_run_manifest(
        str(outdir),
        "variable_radius_staged_pipeline_summary",
        {
            "case_csv": str(case_csv),
            "stage_csv": str(stage_csv),
            "json": str(json_path),
            "replay_json": str(replay_json_path),
            "replay_commands": str(replay_commands_path),
            "plot": str(plot_path),
            "figure_notes": str(notes_path),
        },
    )
    print(json.dumps({"case_summaries": case_summaries}, indent=2))
    print(f"Wrote summary: {json_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()

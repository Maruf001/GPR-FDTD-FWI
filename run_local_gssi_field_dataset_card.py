#!/usr/bin/env python3
"""Build a compact methods-ready data card for the local GSSI field dataset."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_DZT_QC_RUN = "001_gssi51600s_dzt_qc"
DEFAULT_SURVEY_RUN = "015_gssi51600s_survey_geometry_audit"
DEFAULT_ACQUISITION_RUN = "081_gssi51600s_field_acquisition_readiness_audit"
DEFAULT_TIMING_WINDOW_RUN = "101_gssi51600s_field_timing_window_family_classification"
DEFAULT_FIELD_BUNDLE_RUN = "102_gssi51600s_field_publication_claim_bundle_post_timing_window_family"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def safe_int(value, default: int = 0) -> int:
    value_float = safe_float(value, math.nan)
    if not math.isfinite(value_float):
        return default
    return int(round(value_float))


def profile_role(row: dict) -> str:
    stem = str(row.get("file", ""))
    traces = safe_int(row.get("traces"))
    if "__014" in stem or "__016" in stem:
        return "short_repeat_pair_014_016"
    if "__013" in stem or "__015" in stem:
        return "long_pattern_pair_015_013"
    if traces and traces < 400:
        return "short_profile"
    if traces and traces >= 400:
        return "long_profile"
    return "unclassified_profile"


def profile_rows(inventory_rows: list[dict]) -> list[dict]:
    rows = []
    for row in inventory_rows:
        length_m = safe_float(row.get("profile_length_m"))
        scan_spacing_m = safe_float(row.get("scan_spacing_m"))
        rows.append(
            {
                "file": row.get("file", ""),
                "profile_role": profile_role(row),
                "traces": safe_int(row.get("traces")),
                "samples": safe_int(row.get("samples")),
                "scan_spacing_mm": scan_spacing_m * 1000.0,
                "profile_length_m": length_m,
                "time_range_ns": safe_float(row.get("time_range_ns")),
                "dielectric": safe_float(row.get("dielectric")),
                "antenna_name": row.get("antenna_name", ""),
                "antenna_frequency_mhz": safe_float(row.get("antenna_frequency_mhz")),
                "depth_window_m": safe_float(row.get("depth_from_time_m")),
                "dzx_present": str(row.get("dzx_present", "")).lower() == "true",
                "amplitude_std": safe_float(row.get("amplitude_std")),
            }
        )
    return rows


def summarize_card(
    rows: list[dict],
    *,
    dzt_summary: dict,
    survey_summary: dict,
    acquisition_summary: dict,
    timing_window_summary: dict,
    field_bundle_summary: dict,
) -> dict:
    lengths = [safe_float(row.get("profile_length_m")) for row in rows]
    traces = [safe_float(row.get("traces")) for row in rows]
    lengths = [value for value in lengths if math.isfinite(value)]
    traces = [value for value in traces if math.isfinite(value)]
    ready = (
        survey_summary.get("classification") == "independent_2d_line_profiles"
        and bool(acquisition_summary.get("ready_for_2d_qc", False))
        and not bool(acquisition_summary.get("ready_for_3d_hpc", False))
        and not bool(acquisition_summary.get("ready_for_field_fwi", False))
        and not bool(timing_window_summary.get("absolute_time_zero_ready", False))
        and not bool(timing_window_summary.get("field_fwi_ready", False))
    )
    return {
        "policy_label": (
            "local_gssi_field_dataset_card_2d_qc_ready_not_3d_fwi"
            if ready
            else "local_gssi_field_dataset_card_review_required"
        ),
        "dataset_id": dzt_summary.get("dataset_id", ""),
        "input_dir": dzt_summary.get("input_dir", ""),
        "profile_count": len(rows),
        "dzt_file_count": safe_int(dzt_summary.get("dzt_file_count"), len(rows)),
        "trace_count_total": int(sum(traces)) if traces else 0,
        "samples_per_trace": safe_int(rows[0].get("samples") if rows else 0),
        "scan_spacing_mm": safe_float(acquisition_summary.get("scan_spacing_mm")),
        "antenna_frequency_mhz": safe_float(acquisition_summary.get("antenna_frequency_mhz")),
        "dielectric": safe_float(acquisition_summary.get("dielectric")),
        "center_wavelength_mm": safe_float(acquisition_summary.get("center_wavelength_mm")),
        "samples_per_wavelength": safe_float(acquisition_summary.get("samples_per_wavelength")),
        "time_range_ns": safe_float(rows[0].get("time_range_ns") if rows else 0.0),
        "nominal_depth_window_mm": safe_float(acquisition_summary.get("nominal_depth_window_mm")),
        "min_profile_length_m": min(lengths) if lengths else math.nan,
        "max_profile_length_m": max(lengths) if lengths else math.nan,
        "total_trace_derived_length_m": safe_float(
            survey_summary.get("trace_derived_total_length_m"),
            sum(lengths) if lengths else math.nan,
        ),
        "survey_classification": survey_summary.get("classification", ""),
        "no_dzg_file": bool(survey_summary.get("no_dzg_file", False)),
        "has_crossline_file": bool(survey_summary.get("has_crossline_file", False)),
        "ready_for_2d_qc": bool(acquisition_summary.get("ready_for_2d_qc", False)),
        "ready_for_3d_hpc": bool(acquisition_summary.get("ready_for_3d_hpc", False)),
        "ready_for_field_fwi": bool(acquisition_summary.get("ready_for_field_fwi", False)),
        "field_hpc_priority": acquisition_summary.get("field_hpc_priority", "unknown"),
        "timing_window_short_supported_count": safe_float(
            timing_window_summary.get("short_nonraw_supported_count"), 0.0
        ),
        "timing_window_short_row_count": safe_float(timing_window_summary.get("short_nonraw_row_count"), 0.0),
        "timing_window_long_reject_count": safe_float(
            timing_window_summary.get("long_reject_short_transfer_row_count"), 0.0
        ),
        "timing_window_long_row_count": safe_float(timing_window_summary.get("long_row_count"), 0.0),
        "publication_bundle_figure_count": safe_float(field_bundle_summary.get("figure_row_count"), 0.0),
        "publication_bundle_claim_count": safe_float(field_bundle_summary.get("claim_boundary_count"), 0.0),
        "gpu_priority": "none",
        "ready_for_methods_data_card": ready,
        "decision": (
            "Use this as a methods-ready data card for the local GSSI 51600S field dataset. "
            "The dataset is dense along-line 2D QC evidence, not a 3D survey, field FWI "
            "benchmark, cover-depth, radius, or absolute time-zero dataset."
        ),
    }


def plot_dataset_card(rows: list[dict], summary: dict, save_path: Path) -> str:
    files = [row["file"].replace("PROJECT001C__", "").replace(".DZT", "") for row in rows]
    lengths = [safe_float(row["profile_length_m"], 0.0) for row in rows]
    traces = [safe_float(row["traces"], 0.0) for row in rows]

    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.6), constrained_layout=True)
    x = np.arange(len(rows))
    axes[0].bar(x, lengths, color="#4c78a8", width=0.62)
    axes[0].set_xticks(x, files)
    axes[0].set_ylabel("profile length [m]")
    axes[0].set_title("Trace-derived profile lengths")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, traces, color="#2f9d55", width=0.62)
    axes[1].set_xticks(x, files)
    axes[1].set_ylabel("traces")
    axes[1].set_title("Trace counts")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    gate_labels = ["2D QC", "3D HPC", "field FWI", "timing\nabsolute", "methods\ncard"]
    gate_values = [
        1.0 if summary.get("ready_for_2d_qc") else 0.0,
        1.0 if summary.get("ready_for_3d_hpc") else 0.0,
        1.0 if summary.get("ready_for_field_fwi") else 0.0,
        0.0,
        1.0 if summary.get("ready_for_methods_data_card") else 0.0,
    ]
    axes[2].bar(np.arange(len(gate_values)), gate_values, color=["#2f9d55", "#c7302b", "#c7302b", "#c7302b", "#6b6b6b"], width=0.62)
    axes[2].set_xticks(np.arange(len(gate_values)), gate_labels)
    axes[2].set_ylim(0, 1.15)
    axes[2].set_yticks([0, 1], ["blocked", "ready"])
    axes[2].set_title("Use gates")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(f"Local GSSI field dataset card: {summary['policy_label']}", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(
    path: Path,
    summary: dict,
    profile_csv: Path,
    summary_json: Path,
    validation_csv: Path,
) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_gssi_field_dataset_card.png`",
                "",
                "This is a CPU-only methods data card for the local GSSI 51600S",
                "field dataset. It consolidates existing DZT inventory, survey",
                "geometry, acquisition-readiness, timing-window, and publication",
                "bundle summaries.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Profiles: `{summary['profile_count']}`.",
                f"Trace-derived total length: `{summary['total_trace_derived_length_m']:.6f}` m.",
                f"Scan spacing: `{summary['scan_spacing_mm']:.3f}` mm.",
                f"Survey classification: `{summary['survey_classification']}`.",
                f"Ready for 3D/HPC: `{summary['ready_for_3d_hpc']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                "",
                "Outputs:",
                "",
                f"- Profile table: `{profile_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                f"- Figure validation: `{validation_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This card supports field methods and 2D QC description only. It",
                "does not create 3D, field FWI, cover-depth, radius, absolute",
                "time-zero, or synthetic validation claims.",
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
    parser.add_argument("--dzt-qc-run", default=DEFAULT_DZT_QC_RUN)
    parser.add_argument("--survey-run", default=DEFAULT_SURVEY_RUN)
    parser.add_argument("--acquisition-run", default=DEFAULT_ACQUISITION_RUN)
    parser.add_argument("--timing-window-run", default=DEFAULT_TIMING_WINDOW_RUN)
    parser.add_argument("--field-bundle-run", default=DEFAULT_FIELD_BUNDLE_RUN)
    parser.add_argument("--run-name", default="local_gssi_field_dataset_card")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    dzt_dir = dataset_root / args.dzt_qc_run
    survey_dir = dataset_root / args.survey_run
    acquisition_dir = dataset_root / args.acquisition_run
    timing_dir = dataset_root / args.timing_window_run
    bundle_dir = dataset_root / args.field_bundle_run

    dzt_summary = read_json(dzt_dir / "data/gssi_dzt_qc_summary.json")
    inventory_rows = read_csv_rows(dzt_dir / "data/gssi_dzt_inventory.csv")
    survey_summary = read_json(survey_dir / "data/survey_geometry_audit_summary.json")
    acquisition_summary = read_json(acquisition_dir / "data/field_acquisition_readiness_summary.json")
    timing_summary = read_json(timing_dir / "data/field_timing_window_family_classification_summary.json")
    bundle_summary = read_json(bundle_dir / "data/field_publication_claim_bundle_summary.json")

    rows = profile_rows(inventory_rows)
    summary = summarize_card(
        rows,
        dzt_summary=dzt_summary,
        survey_summary=survey_summary,
        acquisition_summary=acquisition_summary,
        timing_window_summary=timing_summary,
        field_bundle_summary=bundle_summary,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root="outputs/summary_tables"))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    profile_csv = data_dir / "local_gssi_field_dataset_card_profiles.csv"
    summary_json = data_dir / "local_gssi_field_dataset_card_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_gssi_field_dataset_card.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(profile_csv, [json_safe(row) for row in rows])
    plot_dataset_card(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "profile_csv": str(profile_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, profile_csv, summary_json, validation_csv)
    write_run_manifest(
        str(outdir),
        "local_gssi_field_dataset_card",
        {
            "dataset_id": args.dataset_id,
            "dzt_qc_run": args.dzt_qc_run,
            "survey_run": args.survey_run,
            "acquisition_run": args.acquisition_run,
            "timing_window_run": args.timing_window_run,
            "field_bundle_run": args.field_bundle_run,
            "readgssi_version": readgssi_version(),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

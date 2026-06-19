#!/usr/bin/env python3
"""Audit measured-field cue spacing context without making inversion claims."""

from __future__ import annotations

import argparse
import csv
import json
import math
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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_PREPROCESS_RUN = "002_gssi51600s_preprocess_feature_qc"
DEFAULT_GEOMETRY_RUN = "015_gssi51600s_survey_geometry_audit"
DEFAULT_APPARENT_DEPTH_RUN = "084_gssi51600s_field_apparent_depth_qc"
DEFAULT_FIELD_POLICY_RUN = "092_gssi51600s_field_dataset_policy_synthesis_post_early_time_anchor_bundle"


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


def profile_group(file_name: str) -> str:
    if "__014" in file_name or "__016" in file_name:
        return "short_014_016"
    if "__013" in file_name or "__015" in file_name:
        return "long_013_015"
    return "unassigned_profile"


def pair_kind(dx_m: float, dt_ns: float, *, same_time_ns: float, duplicate_x_m: float) -> str:
    if dx_m <= duplicate_x_m:
        return "same_x_time_separated_or_vertical"
    if dt_ns <= same_time_ns:
        return "same_time_lateral_spacing"
    return "time_separated_lateral_spacing"


def build_pair_spacing_rows(
    cue_rows: list[dict],
    *,
    same_time_ns: float,
    duplicate_x_m: float,
) -> list[dict]:
    by_file: dict[str, list[dict]] = defaultdict(list)
    for row in cue_rows:
        by_file[str(row.get("file", ""))].append(row)

    out = []
    for file_name, rows in sorted(by_file.items()):
        sorted_rows = sorted(rows, key=lambda row: (safe_float(row.get("x_m")), safe_float(row.get("time_ns"))))
        for left_idx, left in enumerate(sorted_rows):
            for right_idx in range(left_idx + 1, len(sorted_rows)):
                right = sorted_rows[right_idx]
                x_left = safe_float(left.get("x_m"))
                x_right = safe_float(right.get("x_m"))
                t_left = safe_float(left.get("time_ns"))
                t_right = safe_float(right.get("time_ns"))
                if not all(math.isfinite(value) for value in [x_left, x_right, t_left, t_right]):
                    continue
                dx = abs(x_right - x_left)
                dt = abs(t_right - t_left)
                out.append(
                    {
                        "file": file_name,
                        "profile_group": profile_group(file_name),
                        "left_rank": int(safe_float(left.get("rank_in_profile"), left_idx + 1)),
                        "right_rank": int(safe_float(right.get("rank_in_profile"), right_idx + 1)),
                        "left_x_m": x_left,
                        "right_x_m": x_right,
                        "dx_m": dx,
                        "dx_mm": dx * 1000.0,
                        "left_time_ns": t_left,
                        "right_time_ns": t_right,
                        "dt_ns": dt,
                        "pair_kind": pair_kind(dx, dt, same_time_ns=same_time_ns, duplicate_x_m=duplicate_x_m),
                    }
                )
    return out


def _min_or_nan(values: list[float]) -> float:
    finite = [float(value) for value in values if math.isfinite(float(value))]
    return min(finite) if finite else math.nan


def build_profile_context_rows(cue_rows: list[dict], pair_rows: list[dict]) -> list[dict]:
    by_file: dict[str, list[dict]] = defaultdict(list)
    pair_by_file: dict[str, list[dict]] = defaultdict(list)
    for row in cue_rows:
        by_file[str(row.get("file", ""))].append(row)
    for row in pair_rows:
        pair_by_file[str(row.get("file", ""))].append(row)

    out = []
    for file_name, rows in sorted(by_file.items()):
        x_values = [safe_float(row.get("x_m")) for row in rows]
        t_values = [safe_float(row.get("time_ns")) for row in rows]
        strengths = [safe_float(row.get("relative_strength")) for row in rows]
        pairs = pair_by_file[file_name]
        same_time = [safe_float(row.get("dx_m")) for row in pairs if row.get("pair_kind") == "same_time_lateral_spacing"]
        distinct_any = [
            safe_float(row.get("dx_m"))
            for row in pairs
            if row.get("pair_kind") in {"same_time_lateral_spacing", "time_separated_lateral_spacing"}
        ]
        repeated_x = [row for row in pairs if row.get("pair_kind") == "same_x_time_separated_or_vertical"]
        out.append(
            {
                "file": file_name,
                "profile_group": profile_group(file_name),
                "cue_count": len(rows),
                "x_min_m": _min_or_nan(x_values),
                "x_max_m": max([x for x in x_values if math.isfinite(x)], default=math.nan),
                "x_span_m": (
                    max([x for x in x_values if math.isfinite(x)], default=math.nan) - _min_or_nan(x_values)
                    if any(math.isfinite(x) for x in x_values)
                    else math.nan
                ),
                "time_min_ns": _min_or_nan(t_values),
                "time_max_ns": max([t for t in t_values if math.isfinite(t)], default=math.nan),
                "time_span_ns": (
                    max([t for t in t_values if math.isfinite(t)], default=math.nan) - _min_or_nan(t_values)
                    if any(math.isfinite(t) for t in t_values)
                    else math.nan
                ),
                "max_relative_strength": max([s for s in strengths if math.isfinite(s)], default=math.nan),
                "same_time_pair_count": len(same_time),
                "repeated_x_pair_count": len(repeated_x),
                "min_same_time_lateral_spacing_m": _min_or_nan(same_time),
                "min_same_time_lateral_spacing_mm": _min_or_nan(same_time) * 1000.0,
                "min_distinct_x_spacing_any_time_m": _min_or_nan(distinct_any),
                "min_distinct_x_spacing_any_time_mm": _min_or_nan(distinct_any) * 1000.0,
                "claim_status": "field_cue_spacing_context_only_not_resolution_benchmark",
            }
        )
    return out


def summarize_spacing(
    profile_rows: list[dict],
    pair_rows: list[dict],
    *,
    same_time_ns: float,
    geometry: dict,
    apparent_depth: dict,
    field_policy: dict,
) -> dict:
    same_time_pairs = [row for row in pair_rows if row.get("pair_kind") == "same_time_lateral_spacing"]
    distinct_pairs = [
        row
        for row in pair_rows
        if row.get("pair_kind") in {"same_time_lateral_spacing", "time_separated_lateral_spacing"}
    ]
    short_same = [
        safe_float(row.get("dx_m"))
        for row in same_time_pairs
        if row.get("profile_group") == "short_014_016"
    ]
    long_same = [
        safe_float(row.get("dx_m"))
        for row in same_time_pairs
        if row.get("profile_group") == "long_013_015"
    ]
    dataset_same_min_m = _min_or_nan([safe_float(row.get("dx_m")) for row in same_time_pairs])
    dataset_any_min_m = _min_or_nan([safe_float(row.get("dx_m")) for row in distinct_pairs])
    same_time_min_mm = dataset_same_min_m * 1000.0
    close_stress_max_mm = 50.0
    visible_cues_wide = math.isfinite(same_time_min_mm) and same_time_min_mm > close_stress_max_mm
    return {
        "policy_label": "field_cue_spacing_context_not_resolution_benchmark",
        "profile_count": len(profile_rows),
        "cue_count": sum(int(row["cue_count"]) for row in profile_rows),
        "pair_count": len(pair_rows),
        "same_time_threshold_ns": same_time_ns,
        "same_time_lateral_pair_count": len(same_time_pairs),
        "time_separated_lateral_pair_count": sum(
            1 for row in pair_rows if row.get("pair_kind") == "time_separated_lateral_spacing"
        ),
        "same_x_or_vertical_pair_count": sum(
            1 for row in pair_rows if row.get("pair_kind") == "same_x_time_separated_or_vertical"
        ),
        "min_dataset_same_time_lateral_spacing_m": dataset_same_min_m,
        "min_dataset_same_time_lateral_spacing_mm": same_time_min_mm,
        "min_dataset_distinct_x_spacing_any_time_m": dataset_any_min_m,
        "min_dataset_distinct_x_spacing_any_time_mm": dataset_any_min_m * 1000.0,
        "min_short_same_time_lateral_spacing_mm": _min_or_nan(short_same) * 1000.0,
        "min_long_same_time_lateral_spacing_mm": _min_or_nan(long_same) * 1000.0,
        "synthetic_close_spacing_context_max_mm": close_stress_max_mm,
        "same_time_visible_cues_wider_than_synthetic_close_context": visible_cues_wide,
        "geometry_classification": geometry.get("classification", ""),
        "survey_profile_count": geometry.get("profile_count"),
        "apparent_depth_policy": apparent_depth.get("policy_label", ""),
        "field_policy_label": field_policy.get("policy_label", ""),
        "ready_for_field_context": True,
        "ready_for_resolution_benchmark": False,
        "ready_for_cover_depth_recovery": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "Use this as measured-field cue-spacing context only. Similar-time cue separations are much wider "
            "than the synthetic close25-close50 stress scale, while the closest distinct-x field pair is "
            "time-separated. This does not validate or relabel synthetic resolution policy and does not create "
            "field cover-depth, radius, 3D, or FWI readiness."
        ),
    }


def plot_spacing(cue_rows: list[dict], profile_rows: list[dict], summary: dict, save_path: Path) -> str:
    files = [row["file"] for row in profile_rows]
    colors = {
        "PROJECT001C__013.DZT": "#2f6f9f",
        "PROJECT001C__014.DZT": "#4c9f70",
        "PROJECT001C__015.DZT": "#c77d2a",
        "PROJECT001C__016.DZT": "#8f5bb7",
    }
    fig, axes = plt.subplots(1, 2, figsize=(13.8, 4.8), constrained_layout=True)
    for file_name in files:
        rows = [row for row in cue_rows if row.get("file") == file_name]
        axes[0].scatter(
            [safe_float(row.get("x_m")) for row in rows],
            [safe_float(row.get("time_ns")) for row in rows],
            s=[max(28.0, safe_float(row.get("relative_strength"), 1.0) * 5.0) for row in rows],
            label=file_name.replace("PROJECT001C__", "").replace(".DZT", ""),
            color=colors.get(file_name, "#555555"),
            alpha=0.82,
            edgecolor="white",
            linewidth=0.6,
        )
    axes[0].invert_yaxis()
    axes[0].set_xlabel("profile position x [m]")
    axes[0].set_ylabel("cue time [ns]")
    axes[0].set_title("Measured reflector-cue candidates")
    axes[0].grid(color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=9)

    labels = [row["file"].replace("PROJECT001C__", "").replace(".DZT", "") for row in profile_rows]
    values = [safe_float(row.get("min_same_time_lateral_spacing_mm")) for row in profile_rows]
    bar_colors = [colors.get(row["file"], "#555555") for row in profile_rows]
    axes[1].bar(labels, values, color=bar_colors, width=0.62)
    axes[1].axhspan(25.0, 50.0, color="#c7302b", alpha=0.13, label="25-50 mm context")
    axes[1].set_ylabel("min same-time lateral spacing [mm]")
    axes[1].set_title("Cue spacing context only")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=9)
    axes[1].text(
        0.5,
        0.95,
        "Not a known-truth resolution benchmark",
        transform=axes[1].transAxes,
        ha="center",
        va="top",
        fontsize=10,
        color="#333333",
    )

    fig.suptitle(
        f"{summary['policy_label']} | cues={summary['cue_count']} | "
        f"min same-time spacing={summary['min_dataset_same_time_lateral_spacing_mm']:.1f} mm",
        fontsize=12,
    )
    return save_validated_figure(fig, str(save_path))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--preprocess-run", default=DEFAULT_PREPROCESS_RUN)
    parser.add_argument("--geometry-run", default=DEFAULT_GEOMETRY_RUN)
    parser.add_argument("--apparent-depth-run", default=DEFAULT_APPARENT_DEPTH_RUN)
    parser.add_argument("--field-policy-run", default=DEFAULT_FIELD_POLICY_RUN)
    parser.add_argument("--same-time-ns", type=float, default=0.15)
    parser.add_argument("--duplicate-x-m", type=float, default=0.005)
    parser.add_argument("--outdir", default=None)
    parser.add_argument("--run-name", default="gssi51600s_field_cue_spacing_context_audit")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    cue_rows = read_csv_rows(dataset_root / args.preprocess_run / "data/field_reflector_cue_candidates.csv")
    geometry = read_json(dataset_root / args.geometry_run / "data/survey_geometry_audit_summary.json")
    apparent_depth = read_json(dataset_root / args.apparent_depth_run / "data/field_apparent_depth_qc_summary.json")
    field_policy = read_json(dataset_root / args.field_policy_run / "data/field_dataset_policy_summary.json")

    pair_rows = build_pair_spacing_rows(
        cue_rows,
        same_time_ns=args.same_time_ns,
        duplicate_x_m=args.duplicate_x_m,
    )
    profile_rows = build_profile_context_rows(cue_rows, pair_rows)
    summary = summarize_spacing(
        profile_rows,
        pair_rows,
        same_time_ns=args.same_time_ns,
        geometry=geometry,
        apparent_depth=apparent_depth,
        field_policy=field_policy,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    profile_csv = data_dir / "field_cue_spacing_profile_context.csv"
    pair_csv = data_dir / "field_cue_spacing_pair_context.csv"
    summary_json = data_dir / "field_cue_spacing_context_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_cue_spacing_context_audit.png"

    plot_spacing(cue_rows, profile_rows, summary, figure_path)
    write_csv(profile_csv, profile_rows)
    write_csv(pair_csv, pair_rows)
    write_csv(validation_csv, [figure_stats(figure_path)])

    summary["paths"] = {
        "profile_context_csv": str(profile_csv),
        "pair_context_csv": str(pair_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2), encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_cue_spacing_context_audit",
        {
            "dataset_id": args.dataset_id,
            "preprocess_run": args.preprocess_run,
            "geometry_run": args.geometry_run,
            "apparent_depth_run": args.apparent_depth_run,
            "field_policy_run": args.field_policy_run,
            "same_time_ns": args.same_time_ns,
            "duplicate_x_m": args.duplicate_x_m,
            "readgssi_version": readgssi_version(),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

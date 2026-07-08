#!/usr/bin/env python3
"""Survey-geometry audit for local GSSI field DZT/DZX data."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from PIL import Image

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
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def safe_float(value, default=math.nan) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return float(default)
    return out if math.isfinite(out) else float(default)


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _strip_namespace(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _first_text(root: ET.Element, name: str) -> str:
    for elem in root.iter():
        if _strip_namespace(elem.tag) == name and elem.text is not None:
            return elem.text.strip()
    return ""


def _parse_scan_range(text: str) -> tuple[int | None, int | None]:
    parts = [part.strip() for part in str(text).split(",")]
    if len(parts) != 2:
        return None, None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None, None


def _parse_local_coords(text: str) -> tuple[float, float, float] | None:
    parts = [part.strip() for part in str(text).split(",")]
    if len(parts) < 2:
        return None
    try:
        z_value = float(parts[2]) if len(parts) > 2 else 0.0
        return float(parts[0]), float(parts[1]), z_value
    except ValueError:
        return None


def parse_dzx_profile(path: Path) -> dict:
    root = ET.parse(path).getroot()
    waypoints = []
    for waypt in root.iter():
        if _strip_namespace(waypt.tag) != "WayPt":
            continue
        scan = None
        coords = None
        for child in waypt:
            name = _strip_namespace(child.tag)
            if name == "scan" and child.text is not None:
                try:
                    scan = int(child.text.strip())
                except ValueError:
                    scan = None
            if name == "localCoords" and child.text is not None:
                coords = _parse_local_coords(child.text)
        if scan is not None and coords is not None:
            waypoints.append({"scan": scan, "x_m": coords[0], "y_m": coords[1], "z_m": coords[2]})
    scan_start, scan_end = _parse_scan_range(_first_text(root, "scanRange"))
    units_per_scan = safe_float(_first_text(root, "unitsPerScan"))
    scan_per_meters = safe_float(_first_text(root, "scanPerMeters"))
    grid_id = _first_text(root, "gridId")
    endpoint_distance_m = math.nan
    first = None
    last = None
    if len(waypoints) >= 2:
        first = min(waypoints, key=lambda row: row["scan"])
        last = max(waypoints, key=lambda row: row["scan"])
        endpoint_distance_m = math.dist(
            (first["x_m"], first["y_m"], first["z_m"]),
            (last["x_m"], last["y_m"], last["z_m"]),
        )
    return {
        "dzx_path": str(path),
        "dzx_present": True,
        "grid_id": grid_id,
        "units_per_scan_m": units_per_scan,
        "scan_per_meters": scan_per_meters,
        "scan_range_start": scan_start,
        "scan_range_end": scan_end,
        "waypoint_count": len(waypoints),
        "waypoint_start_x_m": first["x_m"] if first is not None else math.nan,
        "waypoint_start_y_m": first["y_m"] if first is not None else math.nan,
        "waypoint_end_x_m": last["x_m"] if last is not None else math.nan,
        "waypoint_end_y_m": last["y_m"] if last is not None else math.nan,
        "waypoint_endpoint_distance_m": endpoint_distance_m,
        "waypoints": waypoints,
    }


def missing_dzg_files(input_dir: Path) -> bool:
    return not any(input_dir.glob("*.DZG")) and not any(input_dir.glob("*.dzg"))


def audit_rows(input_dir: Path, inventory_rows: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for row in inventory_rows:
        file_name = str(row.get("file", ""))
        dzx_path = input_dir / f"{Path(file_name).stem}.DZX"
        dzx = parse_dzx_profile(dzx_path) if dzx_path.exists() else {
            "dzx_path": str(dzx_path),
            "dzx_present": False,
            "grid_id": "",
            "units_per_scan_m": math.nan,
            "scan_per_meters": math.nan,
            "scan_range_start": None,
            "scan_range_end": None,
            "waypoint_count": 0,
            "waypoint_start_x_m": math.nan,
            "waypoint_start_y_m": math.nan,
            "waypoint_end_x_m": math.nan,
            "waypoint_end_y_m": math.nan,
            "waypoint_endpoint_distance_m": math.nan,
            "waypoints": [],
        }
        traces = safe_float(row.get("traces"))
        scan_spacing_m = safe_float(row.get("scan_spacing_m"))
        trace_length_m = safe_float(row.get("profile_length_m"))
        waypoint_distance_m = safe_float(dzx.get("waypoint_endpoint_distance_m"))
        rows.append({
            "file": file_name,
            "channel": row.get("channel", ""),
            "traces": int(traces) if math.isfinite(traces) else "",
            "samples": row.get("samples", ""),
            "antenna_name": row.get("antenna_name", ""),
            "antenna_frequency_mhz": safe_float(row.get("antenna_frequency_mhz")),
            "scan_spacing_m": scan_spacing_m,
            "trace_derived_profile_length_m": trace_length_m,
            "dzx_present": bool(dzx["dzx_present"]),
            "dzx_grid_id": dzx.get("grid_id", ""),
            "dzx_units_per_scan_m": dzx.get("units_per_scan_m"),
            "dzx_scan_per_meters": dzx.get("scan_per_meters"),
            "dzx_scan_range_start": dzx.get("scan_range_start"),
            "dzx_scan_range_end": dzx.get("scan_range_end"),
            "dzx_waypoint_count": dzx.get("waypoint_count"),
            "dzx_waypoint_start_x_m": dzx.get("waypoint_start_x_m"),
            "dzx_waypoint_start_y_m": dzx.get("waypoint_start_y_m"),
            "dzx_waypoint_end_x_m": dzx.get("waypoint_end_x_m"),
            "dzx_waypoint_end_y_m": dzx.get("waypoint_end_y_m"),
            "dzx_waypoint_endpoint_distance_m": waypoint_distance_m,
            "waypoint_length_ratio_to_trace_length": (
                waypoint_distance_m / trace_length_m
                if math.isfinite(waypoint_distance_m) and math.isfinite(trace_length_m) and trace_length_m > 0.0
                else math.nan
            ),
        })
    return rows


def classify_geometry(rows: list[dict], no_dzg: bool) -> dict:
    profile_count = len(rows)
    y_values = {
        round(value, 6)
        for row in rows
        for value in (
            safe_float(row.get("dzx_waypoint_start_y_m")),
            safe_float(row.get("dzx_waypoint_end_y_m")),
        )
        if math.isfinite(value)
    }
    endpoint_distances = []
    for row in rows:
        endpoint = safe_float(row.get("dzx_waypoint_endpoint_distance_m"))
        if math.isfinite(endpoint):
            endpoint_distances.append(endpoint)
    has_crossline_file = not no_dzg
    has_reliable_waypoint_lengths = any(
        safe_float(row.get("waypoint_length_ratio_to_trace_length")) > 0.5
        for row in rows
    )
    has_multiple_profiles = profile_count > 1
    classification = "independent_2d_line_profiles"
    if has_crossline_file and has_reliable_waypoint_lengths and has_multiple_profiles and len(y_values) > 1:
        classification = "candidate_3d_grid"
    reasons = []
    if no_dzg:
        reasons.append("no DZG/GPS/grid position file is present")
    if not has_reliable_waypoint_lengths:
        reasons.append("DZX waypoint endpoints do not encode the trace-derived profile lengths")
    if has_multiple_profiles:
        reasons.append("multiple DZT files are available, but crossline spacing/order is not recoverable")
    return {
        "classification": classification,
        "profile_count": profile_count,
        "no_dzg_file": no_dzg,
        "has_reliable_waypoint_lengths": has_reliable_waypoint_lengths,
        "has_crossline_file": has_crossline_file,
        "trace_derived_total_length_m": float(np.sum([safe_float(row.get("trace_derived_profile_length_m"), 0.0) for row in rows])),
        "reasons": reasons,
        "policy": (
            "Treat this dataset as separate 2D line-profile calibration/QC evidence. "
            "Do not use it as a 3D survey or measured-data FWI benchmark without "
            "external survey layout metadata."
        ),
    }


def figure_stats(path: Path) -> dict:
    with Image.open(path) as image:
        arr = np.asarray(image.convert("RGB"))
        gray = np.asarray(image.convert("L"))
    sample = arr.reshape(-1, 3)[:: max(1, arr.reshape(-1, 3).shape[0] // 10000)]
    return {
        "path": str(path),
        "width": int(arr.shape[1]),
        "height": int(arr.shape[0]),
        "sampled_unique_colors": int(np.unique(sample, axis=0).shape[0]),
        "nonwhite_fraction": float(np.mean(np.any(arr < 250, axis=2))),
        "dynamic_range": int(gray.max()) - int(gray.min()),
    }


def plot_geometry_audit(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [Path(row["file"]).stem.split("__")[-1] for row in rows]
    trace_lengths = [safe_float(row.get("trace_derived_profile_length_m"), 0.0) for row in rows]
    waypoint_lengths = [safe_float(row.get("dzx_waypoint_endpoint_distance_m"), 0.0) for row in rows]
    x = np.arange(len(rows))
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8), constrained_layout=True)
    width = 0.36
    axes[0].bar(x - width / 2, trace_lengths, width=width, label="trace-derived length")
    axes[0].bar(x + width / 2, waypoint_lengths, width=width, label="DZX waypoint endpoint distance")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels)
    axes[0].set_ylabel("length [m]")
    axes[0].set_title("Profile length evidence")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)
    checks = [
        ("DZT profiles", summary["profile_count"]),
        ("DZG present", 0 if summary["no_dzg_file"] else 1),
        ("reliable DZX lengths", 1 if summary["has_reliable_waypoint_lengths"] else 0),
        ("3D classification", 1 if summary["classification"] == "candidate_3d_grid" else 0),
    ]
    axes[1].bar([item[0] for item in checks], [item[1] for item in checks], color=["#4c78a8", "#f58518", "#54a24b", "#b279a2"])
    axes[1].set_title("Survey-geometry classification checks")
    axes[1].set_ylabel("count / boolean")
    axes[1].tick_params(axis="x", labelrotation=25)
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    fig.suptitle(f"Field survey geometry audit: {summary['classification']}", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--inventory-csv", default=None)
    parser.add_argument("--run-name", default="gssi51600s_survey_geometry_audit")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    inventory_csv = (
        Path(args.inventory_csv)
        if args.inventory_csv is not None
        else dataset_root / "001_gssi51600s_dzt_qc" / "data" / "gssi_dzt_inventory.csv"
    )
    rows = audit_rows(input_dir, read_csv_rows(inventory_csv))
    summary = classify_geometry(rows, missing_dzg_files(input_dir))

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    audit_csv = data_dir / "survey_geometry_audit.csv"
    summary_json = data_dir / "survey_geometry_audit_summary.json"
    write_csv(audit_csv, [json_safe(row) for row in rows])
    plot_path = Path(plot_geometry_audit(rows, summary, figures_dir / "survey_geometry_audit.png"))
    validation_csv = data_dir / "figure_validation.csv"
    write_csv(validation_csv, [figure_stats(plot_path)])
    summary["input_dir"] = str(input_dir)
    summary["inventory_csv"] = str(inventory_csv)
    summary["paths"] = {
        "audit_csv": str(audit_csv),
        "summary_json": str(summary_json),
        "plot": str(plot_path),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_survey_geometry_audit",
        {
            "summary_json": str(summary_json),
            "audit_csv": str(audit_csv),
            "plot": str(plot_path),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

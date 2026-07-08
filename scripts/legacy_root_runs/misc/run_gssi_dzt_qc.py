#!/usr/bin/env python3
"""CPU-only import and QC figures for GSSI DZT field profiles."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
import xml.etree.ElementTree as ET
from importlib.metadata import PackageNotFoundError, version
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
from visualization.plot_style import safe_symmetric_limits, save_validated_figure  # noqa: E402


DEFAULT_INPUT_DIR = "data/2026-06-09_GSSI_model_51600S"
DEFAULT_FIELD_ROOT = "outputs/field_experiments"
DEFAULT_DATASET_ID = "local_gssi_51600s_2026_06_09"
C_M_PER_NS = 0.299792458


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _first_text(root: ET.Element, tag_name: str) -> str | None:
    for element in root.iter():
        if _local_name(element.tag) == tag_name and element.text is not None:
            text = element.text.strip()
            if text:
                return text
    return None


def _child_text(parent: ET.Element, tag_name: str) -> str | None:
    for child in parent:
        if _local_name(child.tag) == tag_name and child.text is not None:
            text = child.text.strip()
            if text:
                return text
    return None


def _as_float(value: object) -> float | None:
    if value is None:
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(out):
        return None
    return out


def _as_int(value: object) -> int | None:
    as_float = _as_float(value)
    if as_float is None:
        return None
    return int(as_float)


def _json_safe(value):
    if isinstance(value, dict):
        return {str(key): _json_safe(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(val) for val in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        out = float(value)
        return out if math.isfinite(out) else None
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def field_dataset_output_root(field_root: str | Path, dataset_id: str) -> Path:
    """Return the dataset-specific field experiment output root."""
    dataset_path = Path(dataset_id)
    if (
            not str(dataset_id).strip()
            or dataset_path.is_absolute()
            or ".." in dataset_path.parts):
        raise ValueError(
            "dataset_id must be a non-empty relative name without parent-directory segments"
        )
    return Path(field_root) / dataset_path


def parse_scan_range(text: str | None) -> dict:
    """Parse a GSSI DZX scan range string such as ``0,806``."""
    if not text:
        return {"text": None, "start": None, "end": None, "trace_count": None}
    parts = [part.strip() for part in str(text).split(",") if part.strip()]
    if len(parts) != 2:
        return {"text": text, "start": None, "end": None, "trace_count": None}
    start = _as_int(parts[0])
    end = _as_int(parts[1])
    trace_count = None
    if start is not None and end is not None and end >= start:
        trace_count = end - start + 1
    return {"text": text, "start": start, "end": end, "trace_count": trace_count}


def parse_dzx_metadata(dzx_path: Path) -> dict:
    """Parse the XML DZX sidecar metadata used for DZT import/QC."""
    dzx_path = Path(dzx_path)
    if not dzx_path.exists():
        return {
            "present": False,
            "path": str(dzx_path),
            "warning": "missing_dzx_sidecar",
        }

    root = ET.parse(dzx_path).getroot()
    scan_ranges = []
    for element in root.iter():
        if _local_name(element.tag) == "scanRange" and element.text is not None:
            text = element.text.strip()
            if text and text not in scan_ranges:
                scan_ranges.append(text)

    waypoints = []
    for element in root.iter():
        if _local_name(element.tag) != "WayPt":
            continue
        coords_text = _child_text(element, "localCoords")
        coords = None
        if coords_text:
            coords = [_as_float(part.strip()) for part in coords_text.split(",")]
        waypoints.append({
            "scan": _as_int(_child_text(element, "scan")),
            "local_coords": coords,
        })

    metadata = {
        "present": True,
        "path": str(dzx_path),
        "vertical_unit": _first_text(root, "verticalUnit"),
        "horizontal_unit": _first_text(root, "horizontalUnit"),
        "dielectric": _as_float(_first_text(root, "dielectric")),
        "original_dielectric": _as_float(_first_text(root, "originalDielectric")),
        "units_per_scan_m": _as_float(_first_text(root, "unitsPerScan")),
        "scan_per_meters": _as_float(_first_text(root, "scanPerMeters")),
        "depth_range_m": _as_float(_first_text(root, "depthRange")),
        "samples_per_scan": _as_int(_first_text(root, "samplesPerScan")),
        "system": _first_text(root, "system"),
        "software_version": _first_text(root, "softwareVersion"),
        "grid_id": _first_text(root, "gridId"),
        "antenna_serial_number": _first_text(root, "antSerialNumber"),
        "antenna_model_number": _first_text(root, "antModelNumber"),
        "scan_rate_hz": _as_float(_first_text(root, "scanRate")),
        "transmit_rate_hz": _as_float(_first_text(root, "transmitRate")),
        "surface_pct": _as_float(_first_text(root, "surfacePct")),
        "scan_ranges": [parse_scan_range(text) for text in scan_ranges],
        "waypoints": waypoints,
    }
    metadata["primary_scan_range"] = (
        metadata["scan_ranges"][0]
        if metadata["scan_ranges"]
        else {"text": None, "start": None, "end": None, "trace_count": None}
    )
    return metadata


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _first_list_value(value) -> object | None:
    if isinstance(value, (list, tuple)):
        for item in value:
            if item not in (None, ""):
                return item
        return None
    return value


def antenna_name(header: dict) -> str | None:
    value = _first_list_value(header.get("rh_antname"))
    return None if value is None else str(value).strip()


def antenna_frequency_mhz(header: dict) -> float | None:
    return _as_float(_first_list_value(header.get("antfreq")))


def scan_spacing_m(header: dict, dzx: dict) -> float | None:
    spacing = _as_float(dzx.get("units_per_scan_m"))
    if spacing is not None and spacing > 0.0:
        return spacing
    scans_per_m = _as_float(header.get("rhf_spm"))
    if scans_per_m is not None and scans_per_m > 0.0:
        return 1.0 / scans_per_m
    return None


def dielectric_value(header: dict, dzx: dict) -> float | None:
    value = _as_float(header.get("rhf_epsr"))
    if value is not None and value > 0.0:
        return value
    value = _as_float(dzx.get("dielectric"))
    if value is not None and value > 0.0:
        return value
    return None


def depth_from_time_m(time_ns: float | None, dielectric: float | None) -> float | None:
    if time_ns is None or dielectric is None or dielectric <= 0.0:
        return None
    return C_M_PER_NS * float(time_ns) / (2.0 * math.sqrt(float(dielectric)))


def profile_length_m(trace_count: int, spacing_m: float | None) -> float | None:
    if spacing_m is None or trace_count <= 1:
        return None
    return (trace_count - 1) * spacing_m


def array_stats(values: np.ndarray) -> dict:
    arr = np.asarray(values)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return {
            "min": None,
            "max": None,
            "mean": None,
            "std": None,
            "p01": None,
            "p99": None,
        }
    return {
        "min": float(np.min(finite)),
        "max": float(np.max(finite)),
        "mean": float(np.mean(finite)),
        "std": float(np.std(finite)),
        "p01": float(np.percentile(finite, 1.0)),
        "p99": float(np.percentile(finite, 99.0)),
    }


def background_removed_profile(values: np.ndarray) -> np.ndarray:
    """Remove the median trace-constant component at each time sample."""
    arr = np.asarray(values, dtype=np.float64)
    if arr.ndim != 2:
        raise ValueError("DZT channel array must be two-dimensional")
    return arr - np.nanmedian(arr, axis=1, keepdims=True)


def build_time_axis_ns(header: dict, sample_count: int) -> np.ndarray:
    range_ns = _as_float(header.get("rhf_range"))
    if range_ns is None or range_ns <= 0.0:
        return np.arange(sample_count, dtype=np.float64)
    if sample_count <= 1:
        return np.array([0.0], dtype=np.float64)
    return np.linspace(0.0, range_ns, sample_count, dtype=np.float64)


def build_profile_record(
        dzt_path: Path,
        dzx_metadata: dict,
        header: dict,
        channel: int,
        data: np.ndarray) -> dict:
    arr = np.asarray(data)
    if arr.ndim != 2:
        raise ValueError(f"expected 2D DZT array for {dzt_path}, got shape {arr.shape}")
    sample_count, trace_count = arr.shape
    spacing = scan_spacing_m(header, dzx_metadata)
    range_ns = _as_float(header.get("rhf_range"))
    epsr = dielectric_value(header, dzx_metadata)
    length = profile_length_m(trace_count, spacing)
    depth = depth_from_time_m(range_ns, epsr)
    dzx_trace_count = (
        dzx_metadata.get("primary_scan_range", {}).get("trace_count")
        if dzx_metadata.get("present")
        else None
    )
    warnings = []
    if not dzx_metadata.get("present"):
        warnings.append("missing_dzx_sidecar")
    if dzx_trace_count is not None and dzx_trace_count != trace_count:
        warnings.append("dzx_scan_range_trace_count_mismatch")

    stats = array_stats(arr)
    record = {
        "file": dzt_path.name,
        "stem": dzt_path.stem,
        "dzt_path": str(dzt_path),
        "dzx_path": dzx_metadata.get("path"),
        "dzx_present": bool(dzx_metadata.get("present")),
        "channel": int(channel),
        "samples": int(sample_count),
        "traces": int(trace_count),
        "dtype": str(arr.dtype),
        "file_size_bytes": int(Path(dzt_path).stat().st_size),
        "sha256": sha256_file(dzt_path),
        "header_samples_per_scan": _as_int(header.get("rh_nsamp")),
        "header_bits": _as_int(header.get("rh_bits")),
        "header_channels": _as_int(header.get("rh_nchan")),
        "header_time_zero_samples": _as_int(header.get("rh_zero")),
        "time_range_ns": range_ns,
        "dielectric": epsr,
        "depth_from_time_m": depth,
        "header_depth_m": _as_float(header.get("rhf_depth") or header.get("dzt_depth")),
        "scan_spacing_m": spacing,
        "profile_length_m": length,
        "antenna_name": antenna_name(header),
        "antenna_frequency_mhz": antenna_frequency_mhz(header),
        "header_scans_per_second": _as_float(header.get("rhf_sps")),
        "header_scans_per_meter": _as_float(header.get("rhf_spm")),
        "dzx_system": dzx_metadata.get("system"),
        "dzx_software_version": dzx_metadata.get("software_version"),
        "dzx_depth_range_m": dzx_metadata.get("depth_range_m"),
        "dzx_dielectric": dzx_metadata.get("dielectric"),
        "dzx_units_per_scan_m": dzx_metadata.get("units_per_scan_m"),
        "dzx_scan_per_meters": dzx_metadata.get("scan_per_meters"),
        "dzx_samples_per_scan": dzx_metadata.get("samples_per_scan"),
        "dzx_scan_range": dzx_metadata.get("primary_scan_range", {}).get("text"),
        "dzx_scan_range_trace_count": dzx_trace_count,
        "warnings": warnings,
    }
    record.update({f"amplitude_{key}": value for key, value in stats.items()})
    return _json_safe(record)


def read_dzt_profiles(input_dir: Path) -> list[tuple[dict, np.ndarray]]:
    """Read all DZT profiles under ``input_dir`` using readgssi."""
    try:
        from readgssi.dzt import readdzt
    except ImportError as exc:
        raise RuntimeError(
            "readgssi is required for DZT import. Install it in the active environment first."
        ) from exc

    profiles: list[tuple[dict, np.ndarray]] = []
    for dzt_path in sorted(Path(input_dir).glob("*.DZT")):
        dzx_metadata = parse_dzx_metadata(dzt_path.with_suffix(".DZX"))
        header, data, _gps = readdzt(str(dzt_path), verbose=False)
        if isinstance(data, dict):
            channel_arrays = sorted(data.items(), key=lambda item: int(item[0]))
        else:
            channel_arrays = [(0, data)]
        for channel, arr in channel_arrays:
            record = build_profile_record(
                dzt_path=dzt_path,
                dzx_metadata=dzx_metadata,
                header=header,
                channel=int(channel),
                data=np.asarray(arr),
            )
            profiles.append((record, np.asarray(arr)))
    return profiles


def _x_extent(record: dict) -> tuple[list[float], str]:
    length = _as_float(record.get("profile_length_m"))
    traces = int(record["traces"])
    if length is not None and length > 0.0:
        return [0.0, length, _as_float(record.get("time_range_ns")) or float(record["samples"]), 0.0], "profile distance [m]"
    return [0.0, float(max(1, traces - 1)), _as_float(record.get("time_range_ns")) or float(record["samples"]), 0.0], "trace index"


def plot_bscan_qc(record: dict, data: np.ndarray, save_path: Path) -> str:
    raw = np.asarray(data, dtype=np.float64)
    corrected = background_removed_profile(raw)
    extent, xlabel = _x_extent(record)
    raw_limits = safe_symmetric_limits(raw, percentile=99.0, floor=1.0)
    corrected_limits = safe_symmetric_limits(corrected, percentile=99.0, floor=1.0)

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.2), constrained_layout=True)
    images = [
        axes[0].imshow(
            raw,
            cmap="seismic",
            aspect="auto",
            extent=extent,
            vmin=raw_limits[0],
            vmax=raw_limits[1],
            interpolation="nearest",
        ),
        axes[1].imshow(
            corrected,
            cmap="seismic",
            aspect="auto",
            extent=extent,
            vmin=corrected_limits[0],
            vmax=corrected_limits[1],
            interpolation="nearest",
        ),
    ]
    axes[0].set_title("Raw amplitude")
    axes[1].set_title("Median background removed")
    for ax in axes:
        ax.set_xlabel(xlabel)
        ax.set_ylabel("two-way time [ns]")
        ax.grid(color="#d9d9d9", linewidth=0.4, alpha=0.45)
    for ax, image in zip(axes, images):
        fig.colorbar(image, ax=ax, shrink=0.82, label="amplitude [DZT counts]")

    length_text = record.get("profile_length_m")
    if length_text is None:
        length_label = "unknown distance"
    else:
        length_label = f"{float(length_text):.3f} m"
    fig.suptitle(
        f"{record['file']} ch{record['channel']} | "
        f"{record['traces']} traces x {record['samples']} samples | {length_label}",
        fontsize=12,
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def plot_inventory(records: list[dict], save_path: Path) -> str:
    labels = [f"{record['stem']} ch{record['channel']}" for record in records]
    y = np.arange(len(records))
    traces = [int(record["traces"]) for record in records]
    lengths = [
        0.0 if record.get("profile_length_m") is None else float(record["profile_length_m"])
        for record in records
    ]
    colors = ["#4c78a8" if record.get("dzx_present") else "#e45756" for record in records]

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8), constrained_layout=True)
    axes[0].barh(y, traces, color=colors)
    axes[0].set_yticks(y, labels=labels)
    axes[0].invert_yaxis()
    axes[0].set_xlabel("traces")
    axes[0].set_title("Profile trace count")
    axes[0].grid(axis="x", color="#d9d9d9", linewidth=0.6)

    axes[1].barh(y, lengths, color=colors)
    axes[1].set_yticks(y, labels=[])
    axes[1].invert_yaxis()
    axes[1].set_xlabel("profile length [m]")
    axes[1].set_title("Distance from scan spacing")
    axes[1].grid(axis="x", color="#d9d9d9", linewidth=0.6)
    for idx, record in enumerate(records):
        note = "DZX" if record.get("dzx_present") else "DZT header only"
        axes[1].text(
            lengths[idx] + max(lengths + [1.0]) * 0.015,
            idx,
            note,
            va="center",
            fontsize=8,
            color="#333333",
        )
    fig.suptitle("GSSI 51600S DZT import inventory", fontsize=12, fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def plot_field_context(records: list[dict], save_path: Path) -> str:
    max_length = max(
        [float(record["profile_length_m"]) for record in records if record.get("profile_length_m")]
        or [1.0]
    )
    max_depth = max(
        [float(record["depth_from_time_m"]) for record in records if record.get("depth_from_time_m")]
        or [0.5]
    )
    labels = [f"{record['stem']} ch{record['channel']}" for record in records]

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.4), constrained_layout=True)
    ax = axes[0]
    for idx, record in enumerate(records):
        length = float(record.get("profile_length_m") or 0.0)
        color = "#4c78a8" if record.get("dzx_present") else "#e45756"
        ax.plot([0.0, length], [idx, idx], color=color, linewidth=4.0, solid_capstyle="butt")
        ax.scatter([0.0, length], [idx, idx], color=color, edgecolor="black", linewidth=0.4, zorder=3)
        ax.text(length + max_length * 0.02, idx, f"{record['traces']} traces", va="center", fontsize=8)
    ax.set_yticks(np.arange(len(records)), labels=labels)
    ax.invert_yaxis()
    ax.set_xlabel("profile distance [m]")
    ax.set_ylabel("profile line")
    ax.set_xlim(-0.02 * max_length, 1.18 * max_length)
    ax.set_title("Imported B-scan lines\n(crossline offsets not encoded here)")
    ax.grid(axis="x", color="#d9d9d9", linewidth=0.6)

    ax = axes[1]
    ax.axhspan(0.0, max_depth, facecolor="#f0ece3", edgecolor="#9d9487", linewidth=1.0)
    ax.axhline(0.0, color="#333333", linewidth=1.2, label="survey surface")
    ax.plot([0.0, max_length], [0.0, 0.0], color="#1b7837", linewidth=2.0, label="51600S scan path")
    for fraction in (0.25, 0.5, 0.75):
        ax.scatter(max_length * fraction, 0.0, marker="^", s=45, color="#1b7837",
                   edgecolor="black", linewidth=0.4, zorder=3)
    ax.set_xlim(0.0, max_length)
    ax.set_ylim(max_depth * 1.08, -0.04 * max_depth)
    ax.set_xlabel("profile distance [m]")
    ax.set_ylabel("approximate depth [m]")
    ax.set_title("Profile-level QC model\n(no 3D inversion geometry assumed)")
    ax.grid(color="#d9d9d9", linewidth=0.6)
    ax.legend(loc="lower right", fontsize=8, frameon=True)
    fig.suptitle("GSSI 51600S field-data QC context", fontsize=12, fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_inventory_csv(path: Path, records: list[dict]) -> None:
    fieldnames = [
        "file",
        "channel",
        "dzx_present",
        "samples",
        "traces",
        "dtype",
        "file_size_bytes",
        "sha256",
        "antenna_name",
        "antenna_frequency_mhz",
        "time_range_ns",
        "dielectric",
        "depth_from_time_m",
        "header_depth_m",
        "scan_spacing_m",
        "profile_length_m",
        "dzx_system",
        "dzx_software_version",
        "dzx_depth_range_m",
        "dzx_scan_range",
        "dzx_scan_range_trace_count",
        "amplitude_min",
        "amplitude_max",
        "amplitude_mean",
        "amplitude_std",
        "amplitude_p01",
        "amplitude_p99",
        "warnings",
        "bscan_qc_figure",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            row = {name: record.get(name) for name in fieldnames}
            row["warnings"] = "|".join(record.get("warnings") or [])
            writer.writerow(row)


def write_figure_notes(path: Path, records: list[dict]) -> None:
    bscan_lines = "\n".join(
        f"- `{Path(record['bscan_qc_figure']).name}`: raw and median-background-removed "
        f"B-scan for `{record['file']}` channel {record['channel']}."
        for record in records
    )
    text = f"""# Figure Notes

## `field_profile_qc_context.png`

Profile-level system figure for the GSSI 51600S field data. It shows the
imported B-scan lengths and a generic x-z QC slice. Crossline offsets are not
encoded in the available DZX sidecars, so this is not a reconstructed 3D survey
geometry.

## `gssi_dzt_inventory.png`

Trace-count and distance inventory for each imported DZT channel. Blue bars
have a DZX sidecar; red bars were imported from the DZT header only.

## B-scan QC Figures

{bscan_lines}

These figures are import/QC artifacts. They do not imply that the current 2D
FDTD/FWI model is ready to invert the measured data.
"""
    path.write_text(text, encoding="utf-8")


def write_readme(path: Path, input_dir: Path, records: list[dict]) -> None:
    missing = [record["file"] for record in records if not record.get("dzx_present")]
    text = f"""# GSSI 51600S DZT QC

CPU-only import/QC run for local GSSI DZT profiles under:

```text
{input_dir}
```

Imported {len(records)} DZT channel record(s). Missing DZX sidecars:
{", ".join(sorted(set(missing))) if missing else "none"}.

This run is intentionally limited to reader validation, metadata inventory,
and B-scan QC figures. It is not a 3D FWI run.
"""
    path.write_text(text, encoding="utf-8")


def readgssi_version() -> str | None:
    try:
        return version("readgssi")
    except PackageNotFoundError:
        return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR, help="Directory containing GSSI .DZT files")
    parser.add_argument("--outdir", default=None, help="Optional explicit output directory")
    parser.add_argument("--run-name", default="gssi51600s_dzt_qc", help="Run name for numbered output allocation")
    parser.add_argument(
        "--field-root",
        default=DEFAULT_FIELD_ROOT,
        help="Parent directory for measured/lab/public field-data experiment families",
    )
    parser.add_argument(
        "--dataset-id",
        default=DEFAULT_DATASET_ID,
        help="Relative dataset/source-family name under --field-root",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    input_dir = Path(args.input_dir)
    if not input_dir.is_dir():
        raise FileNotFoundError(f"input directory does not exist: {input_dir}")

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    profile_payloads = read_dzt_profiles(input_dir)
    records: list[dict] = []
    for record, arr in profile_payloads:
        figure_name = f"{record['stem']}_ch{record['channel']}_bscan_qc.png"
        figure_path = figures_dir / figure_name
        record["bscan_qc_figure"] = plot_bscan_qc(record, arr, figure_path)
        records.append(record)

    inventory_figure = plot_inventory(records, figures_dir / "gssi_dzt_inventory.png")
    context_figure = plot_field_context(records, figures_dir / "field_profile_qc_context.png")
    figure_notes = figures_dir / "FIGURE_NOTES.md"
    write_figure_notes(figure_notes, records)
    readme_path = outdir / "README.md"
    write_readme(readme_path, input_dir, records)

    inventory_csv = data_dir / "gssi_dzt_inventory.csv"
    write_inventory_csv(inventory_csv, records)
    summary_json = data_dir / "gssi_dzt_qc_summary.json"
    summary = {
        "run_name": args.run_name,
        "input_dir": str(input_dir),
        "field_root": str(Path(args.field_root)),
        "dataset_id": args.dataset_id,
        "dataset_root": str(dataset_root),
        "outdir": str(outdir),
        "profile_channel_count": len(records),
        "dzt_file_count": len({record["file"] for record in records}),
        "readgssi_version": readgssi_version(),
        "qc_scope": "CPU-only DZT import, metadata inventory, and B-scan QC. No 2D or 3D FWI.",
        "records": records,
        "figures": {
            "inventory": inventory_figure,
            "field_context": context_figure,
            "bscan_qc": [record["bscan_qc_figure"] for record in records],
            "figure_notes": str(figure_notes),
        },
    }
    summary_json.write_text(json.dumps(_json_safe(summary), indent=2) + "\n", encoding="utf-8")
    manifest_path = write_run_manifest(
        str(outdir),
        "gssi51600s_dzt_qc",
        {
            "input_dir": str(input_dir),
            "field_root": str(Path(args.field_root)),
            "dataset_id": args.dataset_id,
            "dataset_root": str(dataset_root),
            "summary_json": str(summary_json),
            "inventory_csv": str(inventory_csv),
            "inventory_figure": inventory_figure,
            "field_context_figure": context_figure,
            "figure_notes": str(figure_notes),
            "readgssi_version": readgssi_version(),
        },
    )

    print(f"Imported {len(records)} DZT channel record(s) from {input_dir}")
    for record in records:
        warning_text = ",".join(record.get("warnings") or []) or "ok"
        length = record.get("profile_length_m")
        length_text = "unknown length" if length is None else f"{float(length):.3f} m"
        print(
            f"{record['file']} ch{record['channel']}: "
            f"{record['traces']} traces x {record['samples']} samples, {length_text}, {warning_text}"
        )
    print(f"Wrote summary: {summary_json}")
    print(f"Wrote manifest: {manifest_path}")


if __name__ == "__main__":
    main()

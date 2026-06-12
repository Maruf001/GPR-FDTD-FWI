#!/usr/bin/env python3
"""CPU-only preprocessing and reflector-cue screening for local GSSI DZT data."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, maximum_filter
from scipy.signal import hilbert

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import (  # noqa: E402
    C_M_PER_NS,
    DEFAULT_DATASET_ID,
    DEFAULT_FIELD_ROOT,
    DEFAULT_INPUT_DIR,
    _as_float,
    background_removed_profile,
    depth_from_time_m,
    field_dataset_output_root,
    read_dzt_profiles,
    readgssi_version,
)
from visualization.plot_style import safe_symmetric_limits, save_validated_figure  # noqa: E402


def json_safe(value):
    if isinstance(value, dict):
        return {str(key): json_safe(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(val) for val in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        out = float(value)
        return out if math.isfinite(out) else None
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def build_axes(record: dict) -> tuple[np.ndarray, np.ndarray]:
    samples = int(record["samples"])
    traces = int(record["traces"])
    time_range_ns = _as_float(record.get("time_range_ns"))
    if time_range_ns is None or time_range_ns <= 0.0:
        time_ns = np.arange(samples, dtype=np.float64)
    else:
        time_ns = np.linspace(0.0, time_range_ns, samples, dtype=np.float64)

    length_m = _as_float(record.get("profile_length_m"))
    if length_m is None or length_m <= 0.0:
        x_m = np.arange(traces, dtype=np.float64)
    else:
        x_m = np.linspace(0.0, length_m, traces, dtype=np.float64)
    return x_m, time_ns


def imshow_extent(x_m: np.ndarray, time_ns: np.ndarray) -> list[float]:
    if x_m.size <= 1:
        x0, x1 = -0.5, 0.5
    else:
        dx = float(np.median(np.diff(x_m)))
        x0 = float(x_m[0] - 0.5 * dx)
        x1 = float(x_m[-1] + 0.5 * dx)
    if time_ns.size <= 1:
        t0, t1 = 0.0, 1.0
    else:
        dt = float(np.median(np.diff(time_ns)))
        t0 = float(time_ns[0] - 0.5 * dt)
        t1 = float(time_ns[-1] + 0.5 * dt)
    return [x0, x1, t1, t0]


def robust_time_zscore(values: np.ndarray) -> np.ndarray:
    """Normalize each time sample across trace position with a robust scale."""
    arr = np.asarray(values, dtype=np.float64)
    median = np.nanmedian(arr, axis=1, keepdims=True)
    mad = np.nanmedian(np.abs(arr - median), axis=1, keepdims=True)
    scale = 1.4826 * mad
    fallback = np.nanpercentile(np.abs(arr - median), 75.0, axis=1, keepdims=True)
    scale = np.where(scale > 1.0e-12, scale, fallback)
    scale = np.where(scale > 1.0e-12, scale, 1.0)
    return (arr - median) / scale


def preprocess_profile(raw: np.ndarray) -> dict[str, np.ndarray]:
    corrected = background_removed_profile(np.asarray(raw, dtype=np.float64))
    envelope = np.abs(hilbert(corrected, axis=0))
    envelope_smooth = gaussian_filter(envelope, sigma=(1.4, 2.2))
    cue = robust_time_zscore(envelope_smooth)
    cue_smooth = gaussian_filter(cue, sigma=(1.0, 1.0))
    return {
        "corrected": corrected,
        "envelope": envelope,
        "envelope_smooth": envelope_smooth,
        "cue": cue_smooth,
    }


def candidate_depth_m(time_ns: float, dielectric: float | None) -> float | None:
    if dielectric is None or dielectric <= 0.0:
        return None
    return depth_from_time_m(time_ns, dielectric)


def pick_reflector_cues(
    record: dict,
    cue: np.ndarray,
    x_m: np.ndarray,
    time_ns: np.ndarray,
    max_candidates: int = 28,
    min_time_ns: float = 0.55,
    max_time_ns: float = 3.40,
    min_x_separation_m: float = 0.055,
    min_t_separation_ns: float = 0.13,
) -> list[dict]:
    """Pick sparse high-envelope cues. These are not confirmed rebars."""
    arr = np.asarray(cue, dtype=np.float64)
    time_mask = (time_ns >= min_time_ns) & (time_ns <= max_time_ns)
    finite = np.isfinite(arr) & time_mask[:, None]
    if not np.any(finite):
        return []
    threshold = max(float(np.nanpercentile(arr[finite], 99.25)), 3.5)
    local_max = arr == maximum_filter(arr, size=(17, 23), mode="nearest")
    rows, cols = np.where(finite & local_max & (arr >= threshold))
    order = np.argsort(arr[rows, cols])[::-1]
    dielectric = _as_float(record.get("dielectric"))

    selected: list[dict] = []
    for idx in order:
        row = int(rows[idx])
        col = int(cols[idx])
        x_val = float(x_m[col])
        t_val = float(time_ns[row])
        if any(
            abs(x_val - cand["x_m"]) < min_x_separation_m
            and abs(t_val - cand["time_ns"]) < min_t_separation_ns
            for cand in selected
        ):
            continue
        selected.append(
            {
                "file": record["file"],
                "channel": int(record["channel"]),
                "x_m": x_val,
                "trace_index": col,
                "time_ns": t_val,
                "sample_index": row,
                "approx_depth_m": candidate_depth_m(t_val, dielectric),
                "relative_strength": float(arr[row, col]),
                "candidate_kind": "reflector_cue_not_confirmed_rebar",
            }
        )
        if len(selected) >= max_candidates:
            break
    return selected


def summarize_profile(record: dict, raw: np.ndarray, processed: dict, candidates: list[dict]) -> dict:
    x_m, time_ns = build_axes(record)
    corrected = processed["corrected"]
    envelope = processed["envelope"]
    cue = processed["cue"]
    early = (time_ns >= 0.55) & (time_ns <= 1.60)
    mid = (time_ns > 1.60) & (time_ns <= 3.40)
    late = time_ns > 3.40
    early_energy = float(np.sqrt(np.mean(corrected[early] ** 2))) if np.any(early) else math.nan
    mid_energy = float(np.sqrt(np.mean(corrected[mid] ** 2))) if np.any(mid) else math.nan
    late_energy = float(np.sqrt(np.mean(corrected[late] ** 2))) if np.any(late) else math.nan
    trace_rms = np.sqrt(np.mean(corrected**2, axis=0))
    time_rms = np.sqrt(np.mean(corrected**2, axis=1))
    candidate_times = [cand["time_ns"] for cand in candidates]
    unique_candidate_x = []
    for x_val in sorted(cand["x_m"] for cand in candidates):
        if not unique_candidate_x or abs(x_val - unique_candidate_x[-1]) >= 0.025:
            unique_candidate_x.append(x_val)
    spacings = (
        np.diff(unique_candidate_x)
        if len(unique_candidate_x) >= 2
        else np.array([], dtype=float)
    )
    return {
        "file": record["file"],
        "channel": int(record["channel"]),
        "samples": int(record["samples"]),
        "traces": int(record["traces"]),
        "profile_length_m": _as_float(record.get("profile_length_m")),
        "scan_spacing_m": _as_float(record.get("scan_spacing_m")),
        "time_range_ns": _as_float(record.get("time_range_ns")),
        "dielectric": _as_float(record.get("dielectric")),
        "approx_depth_range_m": _as_float(record.get("depth_from_time_m")),
        "dzx_present": bool(record.get("dzx_present")),
        "warnings": "|".join(record.get("warnings") or []),
        "corrected_abs_p99": float(np.nanpercentile(np.abs(corrected), 99.0)),
        "envelope_p99": float(np.nanpercentile(envelope, 99.0)),
        "cue_p99": float(np.nanpercentile(cue, 99.0)),
        "early_rms_0p55_1p60ns": early_energy,
        "mid_rms_1p60_3p40ns": mid_energy,
        "late_rms_gt3p40ns": late_energy,
        "early_to_mid_rms_ratio": early_energy / mid_energy if mid_energy > 0.0 else math.nan,
        "trace_rms_min": float(np.min(trace_rms)),
        "trace_rms_max": float(np.max(trace_rms)),
        "time_rms_peak_ns": float(time_ns[int(np.argmax(time_rms))]),
        "candidate_count": len(candidates),
        "candidate_time_min_ns": min(candidate_times) if candidate_times else None,
        "candidate_time_max_ns": max(candidate_times) if candidate_times else None,
        "unique_candidate_x_count": len(unique_candidate_x),
        "median_candidate_spacing_m": float(np.median(spacings)) if spacings.size else None,
    }


def plot_profile_screen(
    record: dict,
    processed: dict,
    candidates: list[dict],
    save_path: Path,
) -> str:
    x_m, time_ns = build_axes(record)
    extent = imshow_extent(x_m, time_ns)
    corrected = processed["corrected"]
    cue = processed["cue"]
    envelope = processed["envelope_smooth"]
    corrected_limits = safe_symmetric_limits(corrected, percentile=99.0, floor=1.0)
    cue_vmax = max(4.0, float(np.nanpercentile(cue[np.isfinite(cue)], 99.5)))
    env_vmax = max(1.0, float(np.nanpercentile(envelope[np.isfinite(envelope)], 99.2)))
    trace_rms = np.sqrt(np.mean(corrected**2, axis=0))
    time_rms = np.sqrt(np.mean(corrected**2, axis=1))

    fig, axes = plt.subplots(2, 2, figsize=(13.5, 8.2), constrained_layout=True)
    ax = axes[0, 0]
    img = ax.imshow(
        corrected,
        cmap="seismic",
        aspect="auto",
        extent=extent,
        vmin=corrected_limits[0],
        vmax=corrected_limits[1],
        interpolation="nearest",
    )
    ax.set_title("Median-background-removed B-scan")
    fig.colorbar(img, ax=ax, shrink=0.82, label="amplitude [DZT counts]")

    ax = axes[0, 1]
    img = ax.imshow(
        cue,
        cmap="magma",
        aspect="auto",
        extent=extent,
        vmin=0.0,
        vmax=cue_vmax,
        interpolation="nearest",
    )
    ax.set_title("Envelope anomaly cue map")
    fig.colorbar(img, ax=ax, shrink=0.82, label="robust relative strength")

    for ax in axes[0, :]:
        if candidates:
            xs = [cand["x_m"] for cand in candidates]
            ts = [cand["time_ns"] for cand in candidates]
            ax.scatter(xs, ts, s=34, facecolors="none", edgecolors="#ffdd55", linewidths=1.2)
        ax.set_xlabel("profile distance [m]")
        ax.set_ylabel("two-way time [ns]")
        ax.grid(color="#d9d9d9", linewidth=0.4, alpha=0.45)

    ax = axes[1, 0]
    ax.plot(x_m, trace_rms, color="#4c78a8", linewidth=1.6)
    for cand in candidates:
        ax.axvline(cand["x_m"], color="#cc6677", alpha=0.22, linewidth=0.9)
    ax.set_xlabel("profile distance [m]")
    ax.set_ylabel("trace RMS after background removal")
    ax.set_title("Lateral energy profile; vertical lines are cue positions")
    ax.grid(color="#d9d9d9", linewidth=0.6)

    ax = axes[1, 1]
    ax.plot(time_rms, time_ns, color="#117733", linewidth=1.6, label="corrected RMS")
    median_env = np.nanmedian(envelope, axis=1)
    ax.plot(median_env / max(float(np.max(median_env)), 1.0) * max(float(np.max(time_rms)), 1.0),
            time_ns, color="#aa4499", linewidth=1.3, label="scaled median envelope")
    ax.invert_yaxis()
    ax.set_xlabel("relative energy")
    ax.set_ylabel("two-way time [ns]")
    ax.set_title("Time-energy profile")
    ax.grid(color="#d9d9d9", linewidth=0.6)
    ax.legend(frameon=False, fontsize=8)

    fig.suptitle(
        f"{record['file']} ch{record['channel']} | {record['traces']} traces | "
        f"{record.get('profile_length_m'):.3f} m | {len(candidates)} reflector cues",
        fontsize=12,
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def plot_preprocess_mosaic(profile_results: list[dict], save_path: Path) -> str:
    fig, axes = plt.subplots(len(profile_results), 1, figsize=(12.5, 2.8 * len(profile_results)), constrained_layout=True)
    axes = np.atleast_1d(axes)
    for ax, item in zip(axes, profile_results):
        record = item["record"]
        x_m, time_ns = item["x_m"], item["time_ns"]
        corrected = item["processed"]["corrected"]
        limits = safe_symmetric_limits(corrected, percentile=99.0, floor=1.0)
        img = ax.imshow(
            corrected,
            cmap="seismic",
            aspect="auto",
            extent=imshow_extent(x_m, time_ns),
            vmin=limits[0],
            vmax=limits[1],
            interpolation="nearest",
        )
        ax.set_title(f"{record['file']} median-background-removed")
        ax.set_xlabel("profile distance [m]")
        ax.set_ylabel("two-way time [ns]")
        ax.grid(color="#d9d9d9", linewidth=0.4, alpha=0.45)
        fig.colorbar(img, ax=ax, shrink=0.86, label="DZT counts")
    fig.suptitle("Field preprocessing mosaic: four imported GSSI 51600S lines", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def plot_candidate_summary(profile_results: list[dict], save_path: Path) -> str:
    fig, axes = plt.subplots(1, len(profile_results), figsize=(4.4 * len(profile_results), 5.2), sharey=True, constrained_layout=True)
    axes = np.atleast_1d(axes)
    for ax, item in zip(axes, profile_results):
        record = item["record"]
        x_m = item["x_m"]
        time_ns = item["time_ns"]
        candidates = item["candidates"]
        ax.set_xlim(float(x_m[0]), float(x_m[-1]) if x_m.size else 1.0)
        ax.set_ylim(float(time_ns[-1]), 0.0)
        if candidates:
            strengths = np.array([cand["relative_strength"] for cand in candidates], dtype=float)
            sizes = 35.0 + 90.0 * (strengths - strengths.min()) / max(float(np.ptp(strengths)), 1.0e-9)
            scatter = ax.scatter(
                [cand["x_m"] for cand in candidates],
                [cand["time_ns"] for cand in candidates],
                s=sizes,
                c=strengths,
                cmap="viridis",
                edgecolor="black",
                linewidth=0.35,
            )
            fig.colorbar(scatter, ax=ax, shrink=0.75, label="relative strength")
        ax.set_title(f"{record['stem']}\n{len(candidates)} cues")
        ax.set_xlabel("profile distance [m]")
        ax.grid(color="#d9d9d9", linewidth=0.6)
    axes[0].set_ylabel("two-way time [ns]")
    fig.suptitle("Sparse reflector-cue candidate map; not confirmed rebar picks", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def plot_energy_summary(profile_metrics: list[dict], save_path: Path) -> str:
    labels = [Path(row["file"]).stem for row in profile_metrics]
    y = np.arange(len(labels))
    candidates = [int(row["candidate_count"]) for row in profile_metrics]
    early_mid = [float(row["early_to_mid_rms_ratio"]) for row in profile_metrics]
    cue_p99 = [float(row["cue_p99"]) for row in profile_metrics]

    fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.8), constrained_layout=True)
    axes[0].barh(y, candidates, color="#4c78a8")
    axes[0].set_yticks(y, labels=labels)
    axes[0].invert_yaxis()
    axes[0].set_xlabel("cue count")
    axes[0].set_title("Sparse reflector cues")

    axes[1].barh(y, early_mid, color="#dd8452")
    axes[1].set_yticks(y, labels=[])
    axes[1].invert_yaxis()
    axes[1].set_xlabel("RMS ratio")
    axes[1].set_title("Early/mid energy ratio")

    axes[2].barh(y, cue_p99, color="#55a868")
    axes[2].set_yticks(y, labels=[])
    axes[2].invert_yaxis()
    axes[2].set_xlabel("99th percentile")
    axes[2].set_title("Cue-map dynamic range")
    for ax in axes:
        ax.grid(axis="x", color="#d9d9d9", linewidth=0.6)
    fig.suptitle("Field profile feature summary", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def validate_figures(paths: list[str | Path]) -> list[dict]:
    rows = []
    for path in paths:
        image = Image.open(path).convert("RGB")
        sample = image.resize((min(image.width, 256), min(image.height, 256)))
        colors = sample.getcolors(maxcolors=1_000_000)
        nonwhite = sum(count for count, color in colors if color != (255, 255, 255)) / (
            sample.width * sample.height
        )
        rows.append(
            {
                "path": str(path),
                "width": image.width,
                "height": image.height,
                "sampled_unique_colors": len(colors),
                "nonwhite_fraction": nonwhite,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(json_safe(row))


def write_readme(path: Path, input_dir: Path, profile_metrics: list[dict], candidate_count: int) -> None:
    text = f"""# GSSI 51600S Preprocessing And Reflector-Cue QC

CPU-only field-data preprocessing run for:

```text
{input_dir}
```

This run applies median background removal, Hilbert-envelope cue mapping, simple
energy summaries, and sparse local-maximum screening. The candidate points are
reflector cues for visual triage. They are not confirmed rebars, not radius
estimates, and not 2D/3D full-waveform inversion results.

Imported {len(profile_metrics)} profile channel record(s) and wrote
{candidate_count} sparse reflector cues.
"""
    path.write_text(text, encoding="utf-8")


def write_figure_notes(path: Path, profile_results: list[dict], figure_paths: dict[str, str]) -> None:
    per_profile = "\n".join(
        f"- `{Path(item['screen_figure']).name}`: four-panel preprocessing, envelope cue, "
        f"lateral energy, and time-energy summary for `{item['record']['file']}`."
        for item in profile_results
    )
    text = f"""# Figure Notes

## `field_preprocessing_mosaic.png`

Ground-penetrating radar (GPR) preprocessing overview for the four imported
GSSI 51600S lines. Each panel shows the median-background-removed B-scan. A
B-scan is a profile image whose horizontal axis is profile distance and whose
vertical axis is two-way travel time.

## `field_candidate_summary.png`

Sparse reflector-cue map. The markers are high-envelope local maxima after
background removal and robust normalization. They are useful places to inspect,
but they are not confirmed rebar detections.

## `field_energy_summary.png`

Profile-level feature summary: number of sparse cue points, early-to-mid time
energy ratio, and cue-map dynamic range. These metrics help decide whether a
line is useful for later calibration or too dominated by ringing/background.

## Per-Profile Screens

{per_profile}

These figures support field-data quality control only. They do not imply that
the current synthetic 2D FDTD/FWI inversion pipeline can already invert this
measured dataset.
"""
    path.write_text(text, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR, help="Directory containing GSSI .DZT files")
    parser.add_argument("--outdir", default=None, help="Optional explicit output directory")
    parser.add_argument(
        "--run-name",
        default="gssi51600s_preprocess_feature_qc",
        help="Run name for numbered output allocation",
    )
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--max-candidates-per-profile", type=int, default=28)
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

    profile_results = []
    candidate_rows: list[dict] = []
    profile_metrics: list[dict] = []
    for record, raw in read_dzt_profiles(input_dir):
        processed = preprocess_profile(raw)
        x_m, time_ns = build_axes(record)
        candidates = pick_reflector_cues(
            record,
            processed["cue"],
            x_m,
            time_ns,
            max_candidates=args.max_candidates_per_profile,
        )
        for rank, cand in enumerate(candidates, start=1):
            cand["rank_in_profile"] = rank
        metrics = summarize_profile(record, raw, processed, candidates)
        screen_figure = plot_profile_screen(
            record,
            processed,
            candidates,
            figures_dir / f"{record['stem']}_ch{record['channel']}_feature_screen.png",
        )
        item = {
            "record": record,
            "raw": raw,
            "processed": processed,
            "x_m": x_m,
            "time_ns": time_ns,
            "candidates": candidates,
            "metrics": metrics,
            "screen_figure": screen_figure,
        }
        profile_results.append(item)
        candidate_rows.extend(candidates)
        profile_metrics.append(metrics)

    figure_paths = {
        "preprocess_mosaic": plot_preprocess_mosaic(
            profile_results,
            figures_dir / "field_preprocessing_mosaic.png",
        ),
        "candidate_summary": plot_candidate_summary(
            profile_results,
            figures_dir / "field_candidate_summary.png",
        ),
        "energy_summary": plot_energy_summary(
            profile_metrics,
            figures_dir / "field_energy_summary.png",
        ),
    }
    figure_paths["profile_screens"] = [item["screen_figure"] for item in profile_results]

    profile_csv = data_dir / "field_profile_feature_summary.csv"
    candidate_csv = data_dir / "field_reflector_cue_candidates.csv"
    figure_validation_csv = data_dir / "figure_validation.csv"
    write_csv(profile_csv, profile_metrics)
    write_csv(candidate_csv, candidate_rows)

    all_figures = (
        [figure_paths["preprocess_mosaic"], figure_paths["candidate_summary"], figure_paths["energy_summary"]]
        + figure_paths["profile_screens"]
    )
    validation_rows = validate_figures(all_figures)
    write_csv(figure_validation_csv, validation_rows)

    figure_notes = figures_dir / "FIGURE_NOTES.md"
    write_figure_notes(figure_notes, profile_results, figure_paths)
    write_readme(outdir / "README.md", input_dir, profile_metrics, len(candidate_rows))

    summary = {
        "run_name": args.run_name,
        "input_dir": str(input_dir),
        "field_root": str(Path(args.field_root)),
        "dataset_id": args.dataset_id,
        "dataset_root": str(dataset_root),
        "outdir": str(outdir),
        "readgssi_version": readgssi_version(),
        "profile_channel_count": len(profile_metrics),
        "reflector_cue_count": len(candidate_rows),
        "qc_scope": (
            "CPU-only preprocessing and reflector-cue screening. "
            "No confirmed rebar labeling, no radius estimate, and no FWI."
        ),
        "profile_summary_csv": str(profile_csv),
        "candidate_csv": str(candidate_csv),
        "figure_validation_csv": str(figure_validation_csv),
        "figures": figure_paths,
    }
    summary_path = data_dir / "field_preprocess_feature_qc_summary.json"
    summary_path.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")

    manifest_path = write_run_manifest(
        str(outdir),
        "gssi51600s_preprocess_feature_qc",
        {
            "input_dir": str(input_dir),
            "field_root": str(Path(args.field_root)),
            "dataset_id": args.dataset_id,
            "summary_json": str(summary_path),
            "profile_summary_csv": str(profile_csv),
            "candidate_csv": str(candidate_csv),
            "figure_notes": str(figure_notes),
            "readgssi_version": readgssi_version(),
        },
    )

    print(f"Wrote field preprocessing QC: {outdir}")
    print(f"Profiles: {len(profile_metrics)}")
    print(f"Reflector cues: {len(candidate_rows)}")
    print(f"Summary: {summary_path}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()

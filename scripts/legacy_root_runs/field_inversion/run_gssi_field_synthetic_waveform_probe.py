#!/usr/bin/env python3
"""Field-to-synthetic waveform probe for selected local GSSI 51600S profiles."""

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
from scipy.signal import hilbert

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

import config as cfg  # noqa: E402
from core.geometry import build_single_rebar_model  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from core.source import generate_time_array, ricker_wavelet  # noqa: E402
from run_gssi_dzt_qc import (  # noqa: E402
    DEFAULT_DATASET_ID,
    DEFAULT_FIELD_ROOT,
    DEFAULT_INPUT_DIR,
    background_removed_profile,
    field_dataset_output_root,
    read_dzt_profiles,
    readgssi_version,
)
from run_gssi_field_preprocess_feature_qc import (  # noqa: E402
    build_axes,
    json_safe,
    preprocess_profile,
    write_csv,
)
from run_multi_rebar_common_radius_profile import (  # noqa: E402
    build_scan_positions,
    simulate_bscan,
)
from visualization.plot_style import safe_symmetric_limits, save_validated_figure  # noqa: E402


DEFAULT_PHASE_CONVENTIONS = "cue_time,top_envelope_35pct"


def parse_csv_text(text: str) -> list[str]:
    values = [item.strip() for item in str(text).split(",") if item.strip()]
    if not values:
        raise argparse.ArgumentTypeError("expected at least one comma-separated value")
    return values


def parse_float_csv(text: str) -> list[float]:
    try:
        values = [float(item.strip()) for item in str(text).split(",") if item.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected comma-separated numeric values") from exc
    if not values:
        raise argparse.ArgumentTypeError("expected at least one value")
    return values


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def safe_float(value, default=math.nan) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return float(default)
    return out if math.isfinite(out) else float(default)


def safe_label(text: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in str(text))


def select_probe_events(
    apex_rows: list[dict],
    phase_conventions: list[str],
    events_per_profile: int,
) -> list[dict]:
    selected: list[dict] = []
    for phase in phase_conventions:
        phase_rows = [row for row in apex_rows if row.get("phase_convention") == phase]
        files = sorted({row.get("file", "") for row in phase_rows})
        for file_name in files:
            subset = [row for row in phase_rows if row.get("file") == file_name]
            subset = sorted(
                subset,
                key=lambda row: safe_float(row.get("template_score"), default=-math.inf),
                reverse=True,
            )
            selected.extend(subset[: int(events_per_profile)])
    return selected


def relative_offsets(count: int, aperture_m: float) -> np.ndarray:
    if count < 1:
        raise ValueError("source count must be positive")
    if count == 1:
        return np.array([0.0], dtype=np.float64)
    return np.linspace(-0.5 * float(aperture_m), 0.5 * float(aperture_m), int(count))


def scan_tx_positions_for_midpoints(
    center_x_m: float,
    midpoint_offsets_m: np.ndarray,
    tx_rx_offset_m: float,
) -> tuple[np.ndarray, np.ndarray]:
    midpoints = float(center_x_m) + np.asarray(midpoint_offsets_m, dtype=np.float64)
    tx_positions = midpoints - 0.5 * float(tx_rx_offset_m)
    lower = cfg.SCAN_START_X
    upper = cfg.SCAN_END_X
    if np.any(tx_positions < lower - 1e-12) or np.any(tx_positions > upper + 1e-12):
        raise ValueError("requested synthetic scan aperture exceeds configured scan domain")
    return tx_positions, midpoints


def interpolate_matrix(
    data: np.ndarray,
    x_values: np.ndarray,
    time_values_ns: np.ndarray,
    target_x_values: np.ndarray,
    target_time_values_ns: np.ndarray,
) -> np.ndarray:
    arr = np.asarray(data, dtype=np.float64)
    x = np.asarray(x_values, dtype=np.float64)
    t = np.asarray(time_values_ns, dtype=np.float64)
    target_x = np.asarray(target_x_values, dtype=np.float64)
    target_t = np.asarray(target_time_values_ns, dtype=np.float64)
    out = np.full((target_t.size, target_x.size), np.nan, dtype=np.float64)
    for col, x_val in enumerate(target_x):
        if x_val < x[0] or x_val > x[-1]:
            continue
        hi = int(np.searchsorted(x, x_val, side="left"))
        if hi <= 0:
            trace = arr[:, 0]
        elif hi >= x.size:
            trace = arr[:, -1]
        else:
            x0 = float(x[hi - 1])
            x1 = float(x[hi])
            weight = 0.0 if x1 == x0 else (float(x_val) - x0) / (x1 - x0)
            trace = (1.0 - weight) * arr[:, hi - 1] + weight * arr[:, hi]
        out[:, col] = np.interp(target_t, t, trace, left=np.nan, right=np.nan)
    return out


def robust_normalize(values: np.ndarray) -> np.ndarray:
    arr = np.asarray(values, dtype=np.float64).copy()
    finite = np.isfinite(arr)
    if not np.any(finite):
        return arr
    med = float(np.nanmedian(arr[finite]))
    arr[finite] -= med
    rms = float(np.sqrt(np.nanmean(arr[finite] ** 2)))
    if not math.isfinite(rms) or rms <= 1.0e-12:
        rms = 1.0
    arr[finite] /= rms
    return arr


def compare_windows(field_window: np.ndarray, synthetic_window: np.ndarray) -> dict:
    field_norm = robust_normalize(field_window)
    synthetic_norm = robust_normalize(synthetic_window)
    mask = np.isfinite(field_norm) & np.isfinite(synthetic_norm)
    if np.count_nonzero(mask) < 8:
        return {
            "valid_sample_count": int(np.count_nonzero(mask)),
            "normalized_correlation": math.nan,
            "absolute_correlation": math.nan,
            "polarity": "insufficient",
            "amplitude_scale": math.nan,
            "normalized_residual_rms": math.nan,
        }
    f = field_norm[mask]
    s = synthetic_norm[mask]
    denom = float(np.linalg.norm(f) * np.linalg.norm(s))
    corr = float(np.dot(f, s) / denom) if denom > 0.0 else math.nan
    dot_ss = float(np.dot(s, s))
    scale = float(np.dot(f, s) / dot_ss) if dot_ss > 0.0 else math.nan
    polarity = "same"
    if math.isfinite(corr) and corr < 0.0:
        polarity = "opposite"
    abs_corr = abs(corr) if math.isfinite(corr) else math.nan
    signed_s = s if polarity == "same" else -s
    signed_scale = abs(scale) if math.isfinite(scale) else math.nan
    residual = f - signed_scale * signed_s if math.isfinite(signed_scale) else f - signed_s
    return {
        "valid_sample_count": int(np.count_nonzero(mask)),
        "normalized_correlation": corr,
        "absolute_correlation": abs_corr,
        "polarity": polarity,
        "amplitude_scale": scale,
        "normalized_residual_rms": float(np.sqrt(np.mean(residual ** 2))),
    }


def shift_window_time(values: np.ndarray, shift_ns: float, dt_ns: float) -> np.ndarray:
    """Shift a window along time, using NaN fill.

    Positive shifts move the synthetic feature later in relative time.
    """
    arr = np.asarray(values, dtype=np.float64)
    shifted = np.full_like(arr, np.nan, dtype=np.float64)
    if not math.isfinite(shift_ns) or not math.isfinite(dt_ns) or dt_ns <= 0.0:
        return shifted
    samples = int(round(float(shift_ns) / float(dt_ns)))
    if samples == 0:
        return arr.copy()
    if abs(samples) >= arr.shape[0]:
        return shifted
    if samples > 0:
        shifted[samples:, :] = arr[:-samples, :]
    else:
        shifted[:samples, :] = arr[-samples:, :]
    return shifted


def shifted_comparisons(
    field_window: np.ndarray,
    synthetic_window: np.ndarray,
    shift_values_ns: list[float],
    dt_ns: float,
) -> list[tuple[dict, np.ndarray]]:
    comparisons: list[tuple[dict, np.ndarray]] = []
    for shift_ns in shift_values_ns:
        shifted = shift_window_time(synthetic_window, float(shift_ns), dt_ns)
        metrics = compare_windows(field_window, shifted)
        metrics["synthetic_time_shift_ns"] = float(shift_ns)
        comparisons.append((metrics, shifted))
    return comparisons


def best_shifted_comparison(
    field_window: np.ndarray,
    synthetic_window: np.ndarray,
    shift_values_ns: list[float],
    dt_ns: float,
) -> tuple[dict, np.ndarray, list[tuple[dict, np.ndarray]]]:
    comparisons = shifted_comparisons(
        field_window,
        synthetic_window,
        shift_values_ns,
        dt_ns,
    )
    best_metrics: dict | None = None
    best_window: np.ndarray | None = None
    for metrics, shifted in comparisons:
        score = metrics.get("absolute_correlation")
        best_score = None if best_metrics is None else best_metrics.get("absolute_correlation")
        if (
                best_metrics is None
                or (math.isfinite(score) and not math.isfinite(best_score))
                or (math.isfinite(score) and math.isfinite(best_score) and score > best_score)):
            best_metrics = metrics
            best_window = shifted
    if best_metrics is None or best_window is None:
        fallback = compare_windows(field_window, synthetic_window)
        fallback["synthetic_time_shift_ns"] = 0.0
        return fallback, synthetic_window, comparisons
    return best_metrics, best_window, comparisons


def estimate_synthetic_peak_time_ns(
    corrected_bscan: np.ndarray,
    time_ns: np.ndarray,
    midpoint_x_m: np.ndarray,
    center_x_m: float,
    min_time_ns: float = 0.20,
    max_time_ns: float = 4.00,
) -> float:
    center_col = int(np.argmin(np.abs(np.asarray(midpoint_x_m) - float(center_x_m))))
    envelope = np.abs(hilbert(np.asarray(corrected_bscan, dtype=np.float64), axis=0))
    mask = (time_ns >= float(min_time_ns)) & (time_ns <= float(max_time_ns))
    rows = np.flatnonzero(mask)
    if rows.size == 0:
        return float(time_ns[int(np.nanargmax(envelope[:, center_col]))])
    local = envelope[rows, center_col]
    return float(time_ns[int(rows[int(np.nanargmax(local))])])


def simulate_single_candidate(
    depth_m: float,
    radius_m: float,
    concrete_epsr: float,
    backend: str,
    frequency_hz: float,
    source_count: int,
    tx_rx_offset_m: float,
    scan_aperture_m: float,
    geometry_mode: str,
    subcell_samples: int,
) -> dict:
    if not math.isfinite(depth_m) or depth_m <= 0.0:
        return {"valid": False, "reason": "nonpositive_depth"}
    if not math.isfinite(radius_m) or radius_m <= 0.0:
        return {"valid": False, "reason": "nonpositive_radius"}
    z_center = cfg.CONCRETE_TOP + float(depth_m)
    if z_center - radius_m <= cfg.CONCRETE_TOP + cfg.DZ:
        return {"valid": False, "reason": "rebar_intersects_surface_or_air"}
    if z_center + radius_m >= cfg.DOMAIN_Z - cfg.DZ:
        return {"valid": False, "reason": "rebar_too_deep_for_domain"}
    if not math.isfinite(concrete_epsr) or concrete_epsr <= 1.0:
        return {"valid": False, "reason": "invalid_concrete_epsr"}

    center_x = 0.25
    offsets = relative_offsets(source_count, scan_aperture_m)
    tx_positions, midpoints = scan_tx_positions_for_midpoints(
        center_x,
        offsets,
        tx_rx_offset_m,
    )
    scan_positions, scan_x = build_scan_positions(
        cfg.INVERSION_SCAN_STEP,
        source_count,
        tx_rx_offset_m=tx_rx_offset_m,
        receiver_sampling="nearest",
        scan_x_values_m=tx_positions,
    )
    old_epsr = cfg.CONCRETE_EPSR
    try:
        cfg.CONCRETE_EPSR = float(concrete_epsr)
        model = build_single_rebar_model(
            center_x,
            z_center,
            radius_m,
            geometry_mode=geometry_mode,
            subcell_samples=subcell_samples,
        )
    finally:
        cfg.CONCRETE_EPSR = old_epsr
    time_s = generate_time_array(cfg.NT, cfg.DT)
    wavelet = ricker_wavelet(time_s, frequency_hz)
    bscan = simulate_bscan(model, wavelet, scan_positions, backend)
    corrected = background_removed_profile(bscan)
    time_ns = time_s * 1.0e9
    peak_time_ns = estimate_synthetic_peak_time_ns(
        corrected,
        time_ns,
        midpoints,
        center_x,
    )
    return {
        "valid": True,
        "reason": "",
        "corrected": corrected,
        "time_ns": time_ns,
        "midpoint_x_m": midpoints,
        "midpoint_offsets_m": midpoints - center_x,
        "synthetic_peak_time_ns": peak_time_ns,
        "scan_x_m": scan_x,
        "z_center_m": z_center,
    }


def figure_stats(path: Path) -> dict:
    with Image.open(path) as image:
        rgb = image.convert("RGB")
        arr = np.asarray(rgb)
        gray = np.asarray(image.convert("L"))
    nonwhite = np.any(arr < 250, axis=2)
    sample = arr.reshape(-1, 3)[:: max(1, arr.reshape(-1, 3).shape[0] // 10000)]
    return {
        "path": str(path),
        "width": int(arr.shape[1]),
        "height": int(arr.shape[0]),
        "sampled_unique_colors": int(np.unique(sample, axis=0).shape[0]),
        "nonwhite_fraction": float(np.mean(nonwhite)),
        "dynamic_range": int(gray.max()) - int(gray.min()),
    }


def plot_summary(rows: list[dict], save_path: Path) -> str:
    valid_rows = [
        row for row in rows
        if row.get("geometry_valid") and math.isfinite(float(row.get("absolute_correlation", math.nan)))
    ]
    fig, ax = plt.subplots(figsize=(12.0, 5.6), constrained_layout=True)
    if valid_rows:
        valid_rows = sorted(valid_rows, key=lambda row: row["absolute_correlation"], reverse=True)
        labels = [
            f"{Path(row['file']).stem.split('__')[-1]} g{row['apex_group']} "
            f"{row['phase_convention']} {row['epsr_source']} r{row['radius_mm']:.0f}"
            for row in valid_rows
        ]
        values = [row["absolute_correlation"] for row in valid_rows]
        colors = ["#2f7f5f" if row["polarity"] == "same" else "#b45f36" for row in valid_rows]
        ax.bar(np.arange(len(values)), values, color=colors)
        ax.set_xticks(np.arange(len(values)))
        ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
        ax.set_ylim(0.0, max(1.0, max(values) * 1.15))
    else:
        ax.text(0.5, 0.5, "No valid synthetic candidates", ha="center", va="center")
        ax.set_xticks([])
    invalid_count = sum(1 for row in rows if not row.get("geometry_valid"))
    ax.set_ylabel("absolute normalized correlation")
    ax.set_title(f"Field-to-synthetic waveform probe ({invalid_count} invalid geometry candidates)")
    ax.grid(axis="y", color="#dddddd", linewidth=0.6)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def plot_best_panel(payload: dict, save_path: Path) -> str:
    field_window = payload["field_norm"]
    synthetic_window = payload["synthetic_norm"]
    residual = payload["residual"]
    rel_x_mm = payload["relative_x_m"] * 1000.0
    rel_t_ns = payload["relative_time_ns"]
    extent = [
        float(rel_x_mm[0]),
        float(rel_x_mm[-1]),
        float(rel_t_ns[-1]),
        float(rel_t_ns[0]),
    ]
    limits = safe_symmetric_limits(
        np.concatenate([
            field_window[np.isfinite(field_window)].ravel(),
            synthetic_window[np.isfinite(synthetic_window)].ravel(),
        ]),
        percentile=98.0,
        floor=1.0,
    )
    fig, axes = plt.subplots(1, 3, figsize=(13.8, 4.8), constrained_layout=True)
    titles = ["field window", "synthetic window", "field - synthetic"]
    arrays = [field_window, synthetic_window, residual]
    for ax, title, arr in zip(axes, titles, arrays):
        im = ax.imshow(
            arr,
            cmap="seismic",
            aspect="auto",
            extent=extent,
            vmin=limits[0],
            vmax=limits[1],
            interpolation="nearest",
        )
        ax.axvline(0.0, color="#111111", linewidth=0.8, linestyle="--")
        ax.axhline(0.0, color="#111111", linewidth=0.8, linestyle="--")
        ax.set_title(title)
        ax.set_xlabel("relative midpoint x [mm]")
        ax.set_ylabel("relative time [ns]")
    fig.colorbar(im, ax=axes, shrink=0.84, label="normalized amplitude")
    row = payload["row"]
    fig.suptitle(
        (
            f"Best waveform probe: {Path(row['file']).name}, "
            f"{row['phase_convention']}, {row['epsr_source']}, "
            f"r={row['radius_mm']:.1f} mm, "
            f"|corr|={row['absolute_correlation']:.3f}"
        ),
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_readme(path: Path, rows: list[dict], output_root: Path) -> None:
    valid_rows = [row for row in rows if row.get("geometry_valid")]
    invalid_rows = [row for row in rows if not row.get("geometry_valid")]
    best = None
    if valid_rows:
        best = max(valid_rows, key=lambda row: row.get("absolute_correlation", -math.inf))
    lines = [
        "# GSSI 51600S Field-to-Synthetic Waveform Probe",
        "",
        "Bounded waveform comparison for phase-anchor field events against simple",
        "single-rebar 2D FDTD snippets. This is not field FWI.",
        "",
        "Output root:",
        "",
        "```text",
        str(output_root),
        "```",
        "",
        f"Candidate rows: {len(rows)}",
        f"Valid synthetic geometries: {len(valid_rows)}",
        f"Invalid geometries: {len(invalid_rows)}",
    ]
    if best is not None:
        lines.extend([
            "",
            "Best valid waveform match:",
            "",
            "```text",
            f"file:       {best['file']}",
            f"phase:      {best['phase_convention']}",
            f"apex group: {best['apex_group']}",
            f"radius:     {best['radius_mm']:.1f} mm",
            f"depth:      {best['fitted_depth_m'] * 1000.0:.1f} mm",
            f"epsr:       {best['concrete_epsr']:.2f}",
            f"|corr|:     {best['absolute_correlation']:.4f}",
            f"polarity:   {best['polarity']}",
            f"time shift: {best.get('synthetic_time_shift_ns', 0.0):.3f} ns",
            "```",
        ])
    lines.extend([
        "",
        "Interpretation boundary:",
        "",
        "```text",
        "This probe checks whether simple synthetic waveform snippets resemble the",
        "field events under the current phase anchors. It does not estimate a final",
        "cover depth, radius, material model, or field inversion result.",
        "```",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--phase-anchor-dir", default=None)
    parser.add_argument("--profile-stems", default="PROJECT001C__014,PROJECT001C__016")
    parser.add_argument("--phase-conventions", type=parse_csv_text, default=parse_csv_text(DEFAULT_PHASE_CONVENTIONS))
    parser.add_argument("--events-per-profile", type=int, default=1)
    parser.add_argument("--radius-values-mm", type=parse_float_csv, default=parse_float_csv("5,6,8"))
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml"], default="gpu-cpml")
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument("--sources", type=int, default=7)
    parser.add_argument("--tx-rx-offset-mm", type=float, default=60.0)
    parser.add_argument("--scan-aperture-mm", type=float, default=320.0)
    parser.add_argument("--window-pre-ns", type=float, default=0.34)
    parser.add_argument("--window-post-ns", type=float, default=0.82)
    parser.add_argument("--synthetic-time-shifts-ns", type=parse_float_csv, default=parse_float_csv("0"))
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--include-config-epsr", action="store_true")
    parser.add_argument("--run-name", default="gssi51600s_field_synthetic_waveform_probe")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    if args.events_per_profile < 1:
        raise ValueError("--events-per-profile must be positive")
    if args.sources < 1:
        raise ValueError("--sources must be positive")
    if args.tx_rx_offset_mm < 0.0:
        raise ValueError("--tx-rx-offset-mm must be non-negative")

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    requested_stems = {item.strip() for item in str(args.profile_stems).split(",") if item.strip()}
    phase_anchor_dir = (
        Path(args.phase_anchor_dir)
        if args.phase_anchor_dir is not None
        else dataset_root / "006_gssi51600s_phase_anchor_qc"
    )
    apex_fit_csv = phase_anchor_dir / "data" / "field_phase_convention_apex_fits.csv"
    if not apex_fit_csv.exists():
        raise FileNotFoundError(f"missing phase-anchor apex CSV: {apex_fit_csv}")

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    processed_by_file: dict[str, dict] = {}
    axes_by_file: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for record, raw in read_dzt_profiles(Path(args.input_dir)):
        if record.get("stem") in requested_stems:
            processed_by_file[record["file"]] = preprocess_profile(raw)
            axes_by_file[record["file"]] = build_axes(record)

    apex_rows = read_csv_rows(apex_fit_csv)
    selected_events = select_probe_events(
        apex_rows,
        args.phase_conventions,
        args.events_per_profile,
    )
    if not selected_events:
        raise SystemExit("No matching phase-anchor events selected")

    frequency_hz = args.frequency_ghz * 1.0e9
    tx_rx_offset_m = args.tx_rx_offset_mm / 1000.0
    scan_aperture_m = args.scan_aperture_mm / 1000.0
    rel_time_ns = np.arange(
        -float(args.window_pre_ns),
        float(args.window_post_ns) + cfg.DT * 1.0e9,
        cfg.DT * 1.0e9,
        dtype=np.float64,
    )

    rows: list[dict] = []
    shift_surface_rows: list[dict] = []
    panel_payloads: dict[str, dict] = {}

    for event in selected_events:
        file_name = event["file"]
        if file_name not in processed_by_file:
            continue
        processed = processed_by_file[file_name]
        x_m, field_time_ns = axes_by_file[file_name]
        center_x = safe_float(event.get("x_m"))
        anchor_time = safe_float(event.get("apex_time_ns"))
        depth_m = safe_float(event.get("fitted_depth_m"))
        fitted_epsr = safe_float(event.get("fitted_epsr"))
        epsr_cases = [("fitted", fitted_epsr)]
        if args.include_config_epsr and not math.isclose(fitted_epsr, cfg.CONCRETE_EPSR, rel_tol=1e-6, abs_tol=1e-6):
            epsr_cases.append(("config", float(cfg.CONCRETE_EPSR)))
        for epsr_label, concrete_epsr in epsr_cases:
            for radius_mm in args.radius_values_mm:
                candidate_id = safe_label(
                    f"{Path(file_name).stem}_{event['phase_convention']}_g{event['apex_group']}_"
                    f"r{radius_mm:g}_{epsr_label}"
                )
                base_row = {
                    "candidate_id": candidate_id,
                    "file": file_name,
                    "phase_convention": event["phase_convention"],
                    "apex_group": int(float(event["apex_group"])),
                    "x_m": center_x,
                    "apex_time_ns": anchor_time,
                    "fitted_depth_m": depth_m,
                    "fitted_velocity_m_per_ns": safe_float(event.get("fitted_velocity_m_per_ns")),
                    "fitted_time_zero_ns": safe_float(event.get("fitted_time_zero_ns")),
                    "template_score": safe_float(event.get("template_score")),
                    "radius_mm": float(radius_mm),
                    "epsr_source": epsr_label,
                    "concrete_epsr": concrete_epsr,
                    "backend": args.backend,
                    "frequency_ghz": args.frequency_ghz,
                    "sources": args.sources,
                    "tx_rx_offset_mm": args.tx_rx_offset_mm,
                    "scan_aperture_mm": args.scan_aperture_mm,
                }
                sim = simulate_single_candidate(
                    depth_m=depth_m,
                    radius_m=float(radius_mm) / 1000.0,
                    concrete_epsr=concrete_epsr,
                    backend=args.backend,
                    frequency_hz=frequency_hz,
                    source_count=args.sources,
                    tx_rx_offset_m=tx_rx_offset_m,
                    scan_aperture_m=scan_aperture_m,
                    geometry_mode=args.geometry_mode,
                    subcell_samples=args.subcell_samples,
                )
                if not sim["valid"]:
                    rows.append({
                        **base_row,
                        "geometry_valid": False,
                        "skip_reason": sim["reason"],
                        "synthetic_peak_time_ns": math.nan,
                        "synthetic_z_center_m": math.nan,
                        "synthetic_time_shift_ns": math.nan,
                        "valid_sample_count": 0,
                        "normalized_correlation": math.nan,
                        "absolute_correlation": math.nan,
                        "polarity": "skipped",
                        "amplitude_scale": math.nan,
                        "normalized_residual_rms": math.nan,
                    })
                    continue

                target_x = center_x + sim["midpoint_offsets_m"]
                field_window = interpolate_matrix(
                    processed["corrected"],
                    x_m,
                    field_time_ns,
                    target_x,
                    anchor_time + rel_time_ns,
                )
                synthetic_window = interpolate_matrix(
                    sim["corrected"],
                    sim["midpoint_x_m"],
                    sim["time_ns"],
                    sim["midpoint_x_m"],
                    sim["synthetic_peak_time_ns"] + rel_time_ns,
                )
                metrics, shifted_synthetic_window, shift_comparisons = best_shifted_comparison(
                    field_window,
                    synthetic_window,
                    args.synthetic_time_shifts_ns,
                    cfg.DT * 1.0e9,
                )
                for shift_metrics, _shifted_window in shift_comparisons:
                    shift_surface_rows.append({
                        **base_row,
                        "geometry_valid": True,
                        "skip_reason": "",
                        "synthetic_peak_time_ns": sim["synthetic_peak_time_ns"],
                        "synthetic_z_center_m": sim["z_center_m"],
                        **shift_metrics,
                    })
                field_norm = robust_normalize(field_window)
                synthetic_norm = robust_normalize(shifted_synthetic_window)
                sign = 1.0 if metrics["polarity"] == "same" else -1.0
                residual = field_norm - sign * synthetic_norm
                row = {
                    **base_row,
                    "geometry_valid": True,
                    "skip_reason": "",
                    "synthetic_peak_time_ns": sim["synthetic_peak_time_ns"],
                    "synthetic_z_center_m": sim["z_center_m"],
                    **metrics,
                }
                rows.append(row)
                panel_payloads[candidate_id] = {
                    "row": row,
                    "field_norm": field_norm,
                    "synthetic_norm": synthetic_norm,
                    "residual": residual,
                    "relative_x_m": sim["midpoint_offsets_m"],
                    "relative_time_ns": rel_time_ns,
                }

    csv_path = data_dir / "field_synthetic_waveform_probe.csv"
    shift_surface_csv = data_dir / "field_synthetic_waveform_shift_surface.csv"
    json_path = data_dir / "field_synthetic_waveform_probe_summary.json"
    summary_plot = figures_dir / "field_synthetic_waveform_probe_summary.png"
    best_panel = figures_dir / "field_synthetic_waveform_best_panel.png"
    validation_csv = data_dir / "figure_validation.csv"

    write_csv(csv_path, [json_safe(row) for row in rows])
    write_csv(shift_surface_csv, [json_safe(row) for row in shift_surface_rows])
    best_payload = None
    valid_rows = [
        row for row in rows
        if row.get("geometry_valid") and math.isfinite(row.get("absolute_correlation", math.nan))
    ]
    if valid_rows:
        best_row = max(valid_rows, key=lambda row: row["absolute_correlation"])
        best_payload = panel_payloads[best_row["candidate_id"]]
    figure_paths = [Path(plot_summary(rows, summary_plot))]
    if best_payload is not None:
        figure_paths.append(Path(plot_best_panel(best_payload, best_panel)))
    validation_rows = [figure_stats(path) for path in figure_paths]
    write_csv(validation_csv, validation_rows)

    summary = {
        "run_name": args.run_name,
        "input_dir": args.input_dir,
        "dataset_id": args.dataset_id,
        "phase_anchor_dir": str(phase_anchor_dir),
        "profile_stems": sorted(requested_stems),
        "selected_event_count": len(selected_events),
        "candidate_count": len(rows),
        "valid_candidate_count": len(valid_rows),
        "invalid_candidate_count": len(rows) - len(valid_rows),
        "best_candidate": None if best_payload is None else json_safe(best_payload["row"]),
        "qc_scope": "field-to-synthetic waveform probe only; no field FWI",
        "paths": {
            "csv": str(csv_path),
            "shift_surface_csv": str(shift_surface_csv),
            "json": str(json_path),
            "summary_plot": str(summary_plot),
            "best_panel": str(best_panel) if best_payload is not None else None,
            "figure_validation_csv": str(validation_csv),
        },
    }
    json_path.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_readme(outdir / "README.md", rows, outdir)
    write_run_manifest(
        str(outdir),
        "gssi_field_synthetic_waveform_probe",
        {
            "summary_json": str(json_path),
            "csv": str(csv_path),
            "shift_surface_csv": str(shift_surface_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate source-pulse and observed-noise context figures for experiments.

This is metadata-only: it reconstructs the configured source wavelet and noise
model from a coordinate-optimizer summary without running FDTD/FWI.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import textwrap
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

import config as cfg  # noqa: E402
from core.source import generate_time_array, ricker_wavelet  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def shift_zero_fill(values, dt, shift_s):
    """Shift a 1D signal in time using interpolation with no wraparound."""
    data = np.asarray(values, dtype=np.float64)
    if data.ndim != 1:
        raise ValueError("values must be one-dimensional")
    time = np.arange(data.size, dtype=np.float64) * float(dt)
    return np.interp(time - float(shift_s), time, data, left=0.0, right=0.0)


def select_replication_case(summary, case_label=None):
    """Return the requested replication case or the first configured case."""
    cases = list(summary.get("replication_cases") or [])
    if not cases:
        raise ValueError("summary has no replication_cases metadata")
    if case_label is None:
        return dict(cases[0])
    for case in cases:
        if case.get("label") == case_label:
            return dict(case)
    raise ValueError(f"case label not found: {case_label}")


def build_source_components(summary, case, nt=None):
    """Build nominal, mismatched, ringdown, and observed source wavelets."""
    frequency_hz = float(summary.get("frequency_ghz", cfg.F_CENTER / 1.0e9)) * 1.0e9
    nt = int(cfg.NT if nt is None else nt)
    time = generate_time_array(nt, cfg.DT)
    frequency_scale = float(case.get("frequency_scale", 1.0))
    time_shift_ps = float(case.get("time_shift_ps", 0.0))
    amplitude_scale = float(case.get("amplitude_scale", 1.0))
    ringdown_scale = float(case.get("ringdown_scale", 0.0))
    ringdown_delay_ps = float(case.get("ringdown_delay_ps", 180.0))
    ringdown_frequency_scale = float(case.get("ringdown_frequency_scale", 0.8))

    nominal = ricker_wavelet(time, frequency_hz)
    primary = ricker_wavelet(time, frequency_hz * frequency_scale)
    if time_shift_ps != 0.0:
        primary = shift_zero_fill(primary, cfg.DT, time_shift_ps * 1.0e-12)
    primary_scaled = amplitude_scale * primary

    ringdown = ricker_wavelet(
        time,
        frequency_hz * frequency_scale * ringdown_frequency_scale,
    )
    ringdown_shift_ps = time_shift_ps + ringdown_delay_ps
    ringdown = shift_zero_fill(ringdown, cfg.DT, ringdown_shift_ps * 1.0e-12)
    ringdown_scaled = amplitude_scale * ringdown_scale * ringdown
    observed_source = primary_scaled + ringdown_scaled
    return {
        "time_s": time,
        "frequency_hz": frequency_hz,
        "nominal": nominal,
        "primary_scaled": primary_scaled,
        "ringdown_scaled": ringdown_scaled,
        "observed_source": observed_source,
    }


def build_noise_proxy(summary, case, source):
    """Build a deterministic 1D Gaussian noise proxy for visualization."""
    fraction = float(case.get("noise_fraction", 0.0))
    seed = int(case.get("noise_seed", 0))
    source = np.asarray(source, dtype=np.float64)
    source_rms = float(np.sqrt(np.mean(source ** 2)))
    noise_std = fraction * source_rms
    rng = np.random.default_rng(seed)
    noise = rng.normal(loc=0.0, scale=noise_std, size=source.shape)
    if noise_std > 0.0:
        standardized_noise = noise / noise_std
    else:
        standardized_noise = np.zeros_like(noise)
    noise_percentiles = np.percentile(noise, [1.0, 5.0, 50.0, 95.0, 99.0])
    standardized_percentiles = np.percentile(
        standardized_noise,
        [1.0, 5.0, 50.0, 95.0, 99.0],
    )
    case_meta = (summary.get("case_metadata") or {}).get(case.get("label"), {})
    observed_noise_stats = case_meta.get("noise", {})
    return {
        "noise": noise,
        "standardized_noise": standardized_noise,
        "combined_proxy": source + noise,
        "stats": {
            "type": "zero-mean Gaussian additive observed-data noise",
            "seed": seed,
            "seed_role": (
                "The seed selects a repeatable Gaussian sample realization; "
                "it does not change the pulse shape or noise distribution."
            ),
            "rms_fraction": fraction,
            "source_proxy_rms": source_rms,
            "noise_proxy_std": noise_std,
            "noise_proxy_rms": float(np.sqrt(np.mean(noise ** 2))),
            "noise_proxy_sample_std": float(np.std(noise)),
            "noise_proxy_mean": float(np.mean(noise)),
            "noise_proxy_min": float(np.min(noise)),
            "noise_proxy_max": float(np.max(noise)),
            "noise_proxy_peak_abs": float(np.max(np.abs(noise))),
            "noise_proxy_percentiles_1_5_50_95_99": [
                float(value) for value in noise_percentiles
            ],
            "standardized_noise_sample_std": float(np.std(standardized_noise)),
            "standardized_noise_min": float(np.min(standardized_noise)),
            "standardized_noise_max": float(np.max(standardized_noise)),
            "standardized_noise_percentiles_1_5_50_95_99": [
                float(value) for value in standardized_percentiles
            ],
            "seed_fingerprint_first16": [
                round(float(value), 4) for value in standardized_noise[:16]
            ],
            "observed_bscan_clean_rms": observed_noise_stats.get("clean_rms"),
            "observed_bscan_noise_std": observed_noise_stats.get("noise_std"),
            "observed_bscan_actual_noise_rms": observed_noise_stats.get("actual_noise_rms"),
        },
    }


def _normalized(values):
    data = np.asarray(values, dtype=np.float64)
    scale = float(np.max(np.abs(data)))
    if scale <= 0.0:
        return data
    return data / scale


def _spectrum(time_s, values):
    dt = float(time_s[1] - time_s[0])
    freq_ghz = np.fft.rfftfreq(len(values), dt) / 1.0e9
    amp = np.abs(np.fft.rfft(values))
    max_amp = float(np.max(amp))
    if max_amp > 0.0:
        amp = amp / max_amp
    return freq_ghz, amp


def _safe_peak_scale(values):
    scale = float(np.max(np.abs(np.asarray(values, dtype=np.float64))))
    if scale <= 0.0:
        return 1.0
    return scale


def validate_png(path, max_sample_pixels=200_000):
    """Return nonblank image metrics for a saved pulse/noise figure."""
    with Image.open(path) as image:
        rgb = image.convert("RGB")
        arr = np.asarray(rgb)
    total_pixels = int(arr.shape[0] * arr.shape[1])
    if total_pixels > int(max_sample_pixels):
        stride = int(np.ceil(np.sqrt(total_pixels / float(max_sample_pixels))))
        sampled = arr[::stride, ::stride]
    else:
        stride = 1
        sampled = arr
    sample_pixels = sampled.reshape(-1, 3)
    unique = len(np.unique(sample_pixels, axis=0))
    nonwhite = float(np.mean(np.any(sample_pixels < 250, axis=1)))
    if unique < 32 or nonwhite < 0.01:
        raise ValueError(f"Saved pulse/noise figure appears degenerate: {path}")
    return {
        "width_px": int(rgb.size[0]),
        "height_px": int(rgb.size[1]),
        "unique_colors": int(unique),
        "nonwhite_fraction": nonwhite,
        "validation_pixel_stride": int(stride),
        "validation_sample_pixels": int(sample_pixels.shape[0]),
    }


def figure_notes_has_pulse_section(figures_dir):
    """Return whether FIGURE_NOTES.md already has the pulse/noise block."""
    notes_path = Path(figures_dir) / "FIGURE_NOTES.md"
    if not notes_path.exists():
        return False
    text = notes_path.read_text(encoding="utf-8")
    return (
        "<!-- source_pulse_noise_context:start -->" in text
        and "<!-- source_pulse_noise_context:end -->" in text
    )


def plot_pulse_noise(summary, case, save_path, title=None):
    """Plot one source pulse/noise context figure."""
    components = build_source_components(summary, case)
    time_ns = components["time_s"] * 1.0e9
    observed = components["observed_source"]
    noise_proxy = build_noise_proxy(summary, case, observed)
    freq_nom, spec_nom = _spectrum(components["time_s"], components["nominal"])
    freq_obs, spec_obs = _spectrum(components["time_s"], observed)

    fig, axes = plt.subplot_mosaic(
        [["wave", "spectrum"], ["combined", "fingerprint"], ["hist", "meta"]],
        figsize=(14.5, 11.0),
        constrained_layout=True,
        gridspec_kw={"height_ratios": [1.0, 1.0, 0.85]},
    )
    max_time_ns = min(4.0, float(time_ns[-1]))
    noise = noise_proxy["noise"]
    standardized_noise = noise_proxy["standardized_noise"]
    combined_proxy = noise_proxy["combined_proxy"]
    stats = noise_proxy["stats"]
    source_peak = _safe_peak_scale(observed)

    ax = axes["wave"]
    ax.plot(time_ns, _normalized(components["nominal"]), label="nominal Ricker", lw=1.8)
    ax.plot(time_ns, _normalized(components["primary_scaled"]), label="mismatched primary", lw=1.5)
    if np.any(np.abs(components["ringdown_scaled"]) > 0.0):
        ax.plot(time_ns, _normalized(components["ringdown_scaled"]), label="delayed ringdown", lw=1.3)
    ax.plot(time_ns, _normalized(observed), label="observed source", lw=2.0, color="#1b7837")
    ax.set_xlim(0.0, max_time_ns)
    ax.set_xlabel("time [ns]")
    ax.set_ylabel("normalized amplitude")
    ax.set_title("Configured Source Pulse")
    ax.grid(alpha=0.35)
    ax.legend(fontsize=8, loc="upper right")

    ax = axes["spectrum"]
    ax.plot(freq_nom, spec_nom, label="nominal Ricker", lw=1.8)
    ax.plot(freq_obs, spec_obs, label="observed source", lw=1.8, color="#1b7837")
    ax.axvline(float(components["frequency_hz"]) / 1.0e9, color="#777777", lw=1.0, ls="--")
    ax.set_xlim(0.0, 6.0)
    ax.set_xlabel("frequency [GHz]")
    ax.set_ylabel("normalized spectrum")
    ax.set_title("Source Spectrum")
    ax.grid(alpha=0.35)
    ax.legend(fontsize=8)

    ax = axes["combined"]
    clean_common = observed / source_peak
    noise_common = noise / source_peak
    combined_common = combined_proxy / source_peak
    common_values = np.concatenate([clean_common, noise_common, combined_common])
    common_ymax = float(np.max(np.abs(common_values)))
    common_ymax = max(1.1, min(3.0, 1.18 * common_ymax))
    ax.plot(time_ns, clean_common, label="clean source proxy", lw=1.8, color="#1b7837")
    ax.plot(time_ns, noise_common, label="Gaussian noise on same scale", lw=1.0, alpha=0.8)
    ax.plot(
        time_ns,
        combined_common,
        label="source + noise proxy",
        lw=1.4,
        color="#d95f02",
    )
    ax.set_xlim(0.0, max_time_ns)
    ax.set_ylim(-common_ymax, common_ymax)
    ax.set_xlabel("time [ns]")
    ax.set_ylabel("amplitude / source peak")
    ax.set_title("Pulse Plus Noise On Common Scale")
    ax.grid(alpha=0.35)
    ax.legend(fontsize=8, loc="upper right")
    ax.text(
        0.02,
        0.05,
        "noise is not separately normalized",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8,
        bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "#dddddd", "alpha": 0.9},
    )

    ax = axes["fingerprint"]
    if stats["noise_proxy_std"] > 0.0:
        ax.plot(time_ns, standardized_noise, lw=0.9, color="#2b6cb0")
    else:
        ax.plot(time_ns, standardized_noise, lw=0.9, color="#2b6cb0")
        ax.text(
            0.5,
            0.5,
            "zero configured noise",
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=10,
        )
    ax.axhline(0.0, color="#444444", lw=0.8)
    ax.axhline(1.0, color="#999999", lw=0.8, ls=":")
    ax.axhline(-1.0, color="#999999", lw=0.8, ls=":")
    ax.set_xlim(0.0, max_time_ns)
    ax.set_ylim(-4.0, 4.0)
    ax.set_xlabel("time [ns]")
    ax.set_ylabel("noise / configured std")
    ax.set_title(f"Seed-Specific Noise Fingerprint (seed {stats['seed']})")
    ax.grid(alpha=0.35)

    ax = axes["hist"]
    if stats["noise_proxy_std"] > 0.0:
        bins = np.linspace(-4.0, 4.0, 41)
        ax.hist(
            standardized_noise,
            bins=bins,
            density=True,
            color="#7fcdbb",
            edgecolor="#2c7fb8",
            linewidth=0.4,
            alpha=0.75,
            label="seed sample",
        )
        x = np.linspace(-4.0, 4.0, 300)
        normal_pdf = np.exp(-0.5 * x ** 2) / np.sqrt(2.0 * np.pi)
        ax.plot(x, normal_pdf, color="#333333", lw=1.4, label="ideal normal")
    else:
        ax.axvline(0.0, color="#2c7fb8", lw=2.0, label="zero noise")
    ax.set_xlim(-4.0, 4.0)
    ax.set_xlabel("noise / configured std")
    ax.set_ylabel("density")
    ax.set_title("Noise Distribution Check")
    ax.grid(alpha=0.35)
    ax.legend(fontsize=8)

    ax = axes["meta"]
    ax.axis("off")
    lines = [
        f"case: {case.get('label', 'unnamed')}",
        "",
        "source condition:",
        "pulse type: Ricker / Mexican hat",
        f"base center frequency: {components['frequency_hz'] / 1.0e9:.3g} GHz",
        f"frequency scale: {float(case.get('frequency_scale', 1.0)):.3g}",
        f"time shift: {float(case.get('time_shift_ps', 0.0)):.3g} ps",
        f"amplitude scale: {float(case.get('amplitude_scale', 1.0)):.3g}",
        f"ringdown scale: {float(case.get('ringdown_scale', 0.0)):.3g}",
        f"ringdown delay: {float(case.get('ringdown_delay_ps', 180.0)):.3g} ps",
        f"ringdown frequency scale: {float(case.get('ringdown_frequency_scale', 0.8)):.3g}",
        "",
        "noise condition:",
        f"noise type: {stats['type']}",
        f"noise RMS fraction: {stats['rms_fraction']:.3g}",
        f"noise seed: {stats['seed']}",
        f"proxy noise std: {stats['noise_proxy_std']:.6g}",
        f"proxy sample RMS: {stats['noise_proxy_rms']:.6g}",
    ]
    if stats.get("observed_bscan_clean_rms") is not None:
        lines.extend([
            "",
            "observed B-scan noise stats from summary:",
            f"clean RMS: {float(stats['observed_bscan_clean_rms']):.6g}",
            f"noise std: {float(stats['observed_bscan_noise_std']):.6g}",
            f"actual noise RMS: {float(stats['observed_bscan_actual_noise_rms']):.6g}",
        ])
    lines.extend([
        "",
        "seed meaning:",
        "Seed changes the repeatable Gaussian sample, not pulse shape.",
        "Use the fingerprint panel to compare seed-only runs.",
        "",
        "Note: Gaussian noise is added to simulated observed B-scans.",
        "The proxy panels use reconstructed metadata, not a new simulation.",
    ])
    ax.text(
        0.02,
        0.98,
        "\n".join(lines),
        va="top",
        ha="left",
        fontsize=7.2,
        family="monospace",
        bbox={"boxstyle": "round,pad=0.45", "fc": "white", "ec": "#dddddd"},
    )

    run_name = title or summary.get("run_name", "Experiment Source Pulse And Noise")
    fig.suptitle(textwrap.fill(str(run_name), width=94), fontsize=14, fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return {
        "components": components,
        "noise_proxy": noise_proxy,
    }


def upsert_figure_notes(figures_dir, figure_name, summary_name):
    """Add or replace the source pulse/noise section in FIGURE_NOTES.md."""
    notes_path = Path(figures_dir) / "FIGURE_NOTES.md"
    start = "<!-- source_pulse_noise_context:start -->"
    end = "<!-- source_pulse_noise_context:end -->"
    section = f"""{start}
## `{figure_name}` - source pulse and noise context

This figure shows the configured Ricker source pulse, source mismatch,
delayed ringdown, additive Gaussian observed-data noise settings, a
common-scale pulse-plus-noise proxy, and a standardized seed fingerprint.
Inspect it when comparing seed-labelled runs so the source/noise condition is
visible before reading objective plots. Seed-only changes should move the
fingerprint while leaving the pulse shape and noise distribution unchanged.

Validation and source/noise metadata are saved in `../data/{summary_name}`.
{end}
"""
    text = notes_path.read_text(encoding="utf-8") if notes_path.exists() else "# Figure Notes\n"
    pattern = re.compile(rf"\n?{re.escape(start)}.*?{re.escape(end)}\n?", flags=re.DOTALL)
    text = pattern.sub("\n", text).rstrip() + "\n\n" + section
    notes_path.write_text(text, encoding="utf-8")
    return str(notes_path)


def infer_outdir(summary_path, outdir):
    if outdir:
        return Path(outdir)
    path = Path(summary_path)
    if path.parent.name == "data":
        return path.parent.parent
    return path.parent


def _run_number(path):
    match = re.match(r"(\d+)_", Path(path).name)
    if match is None:
        return None
    return int(match.group(1))


def numbered_experiment_dirs(experiments_root):
    """Return numbered experiment directories newest first."""
    root = Path(experiments_root)
    dirs = []
    for candidate in root.iterdir():
        if not candidate.is_dir():
            continue
        number = _run_number(candidate)
        if number is None:
            continue
        dirs.append((number, candidate))
    return [path for _, path in sorted(dirs, key=lambda item: item[0], reverse=True)]


def audit_counts(rows):
    counts = {}
    for row in rows:
        status = row.get("status", "")
        counts[status] = counts.get(status, 0) + 1
    return counts


def _audit_row(
        run_dir,
        status,
        reason,
        summary_path=None,
        figure_path=None,
        context_summary_path=None,
        figure_notes_path=None,
        validation=None):
    validation = validation or {}
    return {
        "run_dir": str(run_dir),
        "run_number": _run_number(run_dir),
        "summary_path": "" if summary_path is None else str(summary_path),
        "status": status,
        "reason": reason,
        "figure_path": "" if figure_path is None else str(figure_path),
        "context_summary_path": "" if context_summary_path is None else str(context_summary_path),
        "figure_notes_path": "" if figure_notes_path is None else str(figure_notes_path),
        "width_px": validation.get("width_px", ""),
        "height_px": validation.get("height_px", ""),
        "unique_colors": validation.get("unique_colors", ""),
        "nonwhite_fraction": validation.get("nonwhite_fraction", ""),
        "validation_pixel_stride": validation.get("validation_pixel_stride", ""),
        "validation_sample_pixels": validation.get("validation_sample_pixels", ""),
    }


def _write_audit_json(rows, audit_json):
    path = Path(audit_json)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"rows": rows, "counts": audit_counts(rows)}, indent=2),
        encoding="utf-8",
    )
    return str(path)


def _write_audit_csv(rows, audit_csv):
    path = Path(audit_csv)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "run_number",
        "run_dir",
        "summary_path",
        "status",
        "reason",
        "figure_path",
        "context_summary_path",
        "figure_notes_path",
        "width_px",
        "height_px",
        "unique_colors",
        "nonwhite_fraction",
        "validation_pixel_stride",
        "validation_sample_pixels",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    return str(path)


def process_summary_for_backfill(
        run_dir,
        summary_path,
        case_label=None,
        label="source_pulse_noise_context",
        update_notes=True,
        refresh_existing=False):
    """Generate or skip one pulse/noise context figure with audit metadata."""
    run_dir = Path(run_dir)
    summary_path = Path(summary_path)
    figures_dir = run_dir / "figures"
    data_dir = run_dir / "data"
    figure_path = figures_dir / f"{label}.png"
    context_summary_path = data_dir / f"{label}_summary.json"
    notes_path = figures_dir / "FIGURE_NOTES.md"

    if figure_path.exists() and not refresh_existing:
        try:
            validation = validate_png(figure_path)
        except Exception as exc:
            existing_reason = f"existing figure invalid: {exc}"
        else:
            has_summary = context_summary_path.exists()
            has_notes = (not update_notes) or figure_notes_has_pulse_section(figures_dir)
            if has_summary and has_notes:
                return _audit_row(
                    run_dir,
                    "skipped",
                    "existing valid pulse/noise artifacts",
                    summary_path=summary_path,
                    figure_path=figure_path,
                    context_summary_path=context_summary_path,
                    figure_notes_path=notes_path if notes_path.exists() else None,
                    validation=validation,
                )
            missing = []
            if not has_summary:
                missing.append(context_summary_path.name)
            if not has_notes:
                missing.append(notes_path.name)
            existing_reason = "existing figure missing companion artifacts: " + ", ".join(missing)
    else:
        existing_reason = "refresh requested" if figure_path.exists() else "missing pulse/noise artifacts"

    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        artifacts = write_pulse_noise_artifacts(
            summary,
            run_dir,
            summary_path=summary_path,
            case_label=case_label,
            label=label,
            update_notes=update_notes,
        )
    except Exception as exc:
        return _audit_row(
            run_dir,
            "skipped",
            f"incompatible metadata: {exc}",
            summary_path=summary_path,
            figure_path=figure_path if figure_path.exists() else None,
            context_summary_path=context_summary_path if context_summary_path.exists() else None,
            figure_notes_path=notes_path if notes_path.exists() else None,
        )

    status = "refreshed" if existing_reason != "missing pulse/noise artifacts" else "generated"
    return _audit_row(
        run_dir,
        status,
        existing_reason,
        summary_path=summary_path,
        figure_path=artifacts["figure"],
        context_summary_path=artifacts["summary"],
        figure_notes_path=artifacts["figure_notes"],
        validation=artifacts["validation"],
    )


def backfill_pulse_noise_artifacts(
        experiments_root,
        case_label=None,
        label="source_pulse_noise_context",
        update_notes=True,
        refresh_existing=False,
        min_run_number=None,
        max_run_number=None,
        limit=None,
        audit_json=None,
        audit_csv=None):
    """Backfill pulse/noise context figures newest first."""
    rows = []
    for run_dir in numbered_experiment_dirs(experiments_root):
        run_number = _run_number(run_dir)
        if min_run_number is not None and run_number < int(min_run_number):
            continue
        if max_run_number is not None and run_number > int(max_run_number):
            continue
        if limit is not None and len(rows) >= int(limit):
            break
        summary_path = run_dir / "data" / "multi_rebar_coordinate_optimizer_summary.json"
        if not summary_path.exists():
            rows.append(_audit_row(
                run_dir,
                "skipped",
                "no compatible coordinate optimizer summary",
            ))
            continue
        rows.append(process_summary_for_backfill(
            run_dir,
            summary_path,
            case_label=case_label,
            label=label,
            update_notes=update_notes,
            refresh_existing=refresh_existing,
        ))

    audit_paths = {}
    if audit_json is not None:
        audit_paths["json"] = _write_audit_json(rows, audit_json)
    if audit_csv is not None:
        audit_paths["csv"] = _write_audit_csv(rows, audit_csv)
    return {
        "rows": rows,
        "counts": audit_counts(rows),
        "audit_paths": audit_paths,
    }


def write_pulse_noise_artifacts(
        summary,
        outdir,
        summary_path=None,
        case_label=None,
        label="source_pulse_noise_context",
        update_notes=True):
    """Write pulse/noise figure, metadata summary, and optional notes."""
    outdir = Path(outdir)
    figures_dir = outdir / "figures"
    data_dir = outdir / "data"
    figures_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    case = select_replication_case(summary, case_label=case_label)
    figure_path = figures_dir / f"{label}.png"
    plotted = plot_pulse_noise(summary, case, figure_path)
    validation = validate_png(figure_path)
    stats = plotted["noise_proxy"]["stats"]
    summary_name = f"{label}_summary.json"
    payload = {
        "schema_version": 2,
        "source": "summary",
        "summary_path": None if summary_path is None else str(summary_path),
        "run_name": summary.get("run_name", ""),
        "case": case,
        "source_wavelet": {
            "type": "Ricker / Mexican hat",
            "base_frequency_ghz": float(plotted["components"]["frequency_hz"]) / 1.0e9,
        },
        "noise": stats,
        "visualization": {
            "source_panel_scale": "each source trace is normalized for shape comparison",
            "pulse_plus_noise_scale": "clean source, noise, and combined proxy share source-peak scale",
            "fingerprint_scale": "noise divided by configured Gaussian standard deviation",
            "simulation_policy": "metadata-only reconstruction; no FDTD or FWI run launched",
        },
        "validation": validation,
        "paths": {
            "figure": str(figure_path),
        },
    }
    summary_path_out = data_dir / summary_name
    summary_path_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    notes_path = None
    if update_notes:
        notes_path = upsert_figure_notes(figures_dir, figure_path.name, summary_name)
    return {
        "figure": str(figure_path),
        "summary": str(summary_path_out),
        "figure_notes": notes_path,
        "validation": validation,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, default=None,
                        help="Path to multi_rebar_coordinate_optimizer_summary.json.")
    parser.add_argument("--outdir", default=None)
    parser.add_argument("--case-label", default=None)
    parser.add_argument("--label", default="source_pulse_noise_context")
    parser.add_argument("--skip-figure-notes", action="store_true")
    parser.add_argument("--backfill-root", type=Path, default=None,
                        help="Backfill numbered experiment directories under this root.")
    parser.add_argument("--refresh-existing", action="store_true")
    parser.add_argument("--min-run-number", type=int, default=None)
    parser.add_argument("--max-run-number", type=int, default=None)
    parser.add_argument("--limit", type=int, default=None,
                        help="Maximum numbered experiment directories to audit in backfill mode.")
    parser.add_argument("--audit-json", type=Path, default=None)
    parser.add_argument("--audit-csv", type=Path, default=None)
    args = parser.parse_args()

    if args.backfill_root is not None:
        result = backfill_pulse_noise_artifacts(
            args.backfill_root,
            case_label=args.case_label,
            label=args.label,
            update_notes=not args.skip_figure_notes,
            refresh_existing=args.refresh_existing,
            min_run_number=args.min_run_number,
            max_run_number=args.max_run_number,
            limit=args.limit,
            audit_json=args.audit_json,
            audit_csv=args.audit_csv,
        )
        print("Backfill pulse/noise visualization audit complete.")
        print(json.dumps({
            "counts": result["counts"],
            "audit_paths": result["audit_paths"],
        }, indent=2))
        return

    if args.summary is None:
        raise ValueError("--summary is required unless --backfill-root is supplied")
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    artifacts = write_pulse_noise_artifacts(
        summary,
        infer_outdir(args.summary, args.outdir),
        summary_path=args.summary,
        case_label=args.case_label,
        label=args.label,
        update_notes=not args.skip_figure_notes,
    )
    print(f"Wrote pulse/noise figure: {artifacts['figure']}")
    print(f"Wrote pulse/noise summary: {artifacts['summary']}")
    if artifacts["figure_notes"]:
        print(f"Updated figure notes: {artifacts['figure_notes']}")
    print(json.dumps(artifacts["validation"], indent=2))


if __name__ == "__main__":
    main()

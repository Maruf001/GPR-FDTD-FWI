#!/usr/bin/env python3
"""Audit band-limited repeatability for local GSSI 51600S field profiles."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, DEFAULT_INPUT_DIR, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_corrected_profile_stack import build_profile_windows, compare_matrices, safe_float  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe  # noqa: E402
from run_gssi_field_profile_alignment_policy import load_profile_map  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SHORT_STACK_SUMMARY = (
    "outputs/field_experiments/local_gssi_51600s_2026_06_09/"
    "021_gssi51600s_short_profile_stack_policy/data/"
    "short_profile_stack_policy_summary.json"
)
DEFAULT_SHORT_APPLIED_SUMMARY = (
    "outputs/field_experiments/local_gssi_51600s_2026_06_09/"
    "025_gssi51600s_short_profile_time_zero_application_policy/data/"
    "short_profile_time_zero_application_summary.json"
)
DEFAULT_LONG_STACK_SUMMARY = (
    "outputs/field_experiments/local_gssi_51600s_2026_06_09/"
    "022_gssi51600s_long_profile_stack_policy/data/"
    "long_profile_stack_policy_summary.json"
)
DEFAULT_LONG_SHIFT_SUMMARY = (
    "outputs/field_experiments/local_gssi_51600s_2026_06_09/"
    "053_gssi51600s_long_profile_shift_scan/data/"
    "long_profile_shift_scan_summary.json"
)
DEFAULT_BANDS = "0.4:1.0:low,1.0:1.6:mid_low,1.6:2.4:mid_high,2.4:3.2:high,0.4:3.2:broad"


def read_json(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_csv_rows(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_safe(row.get(key, "")) for key in fieldnames})


def parse_bands(spec: str) -> list[dict]:
    bands: list[dict] = []
    for item in spec.split(","):
        parts = [part.strip() for part in item.split(":")]
        if len(parts) not in {2, 3}:
            raise ValueError(f"bad band spec {item!r}; expected low:high[:label]")
        low = float(parts[0])
        high = float(parts[1])
        if not (math.isfinite(low) and math.isfinite(high) and high > low >= 0.0):
            raise ValueError(f"invalid band limits {item!r}")
        label = parts[2] if len(parts) == 3 and parts[2] else f"{low:g}_{high:g}ghz"
        bands.append({"band_label": label, "low_ghz": low, "high_ghz": high})
    return bands


def stack_lag_samples(stack_summary: dict) -> int:
    summary = stack_summary.get("summary", {})
    lag_mm = safe_float(summary.get("best_lag_mm"))
    dx_m = safe_float(stack_summary.get("dx_m"))
    if not (math.isfinite(lag_mm) and math.isfinite(dx_m) and dx_m > 0.0):
        raise ValueError("stack summary does not contain a finite best_lag_mm and dx_m")
    return int(round(lag_mm / (1000.0 * dx_m)))


def centered_matrix(values: np.ndarray) -> np.ndarray:
    arr = np.asarray(values, dtype=np.float64)
    finite = np.isfinite(arr)
    counts = np.sum(finite, axis=0, keepdims=True)
    sums = np.nansum(arr, axis=0, keepdims=True)
    col_mean = np.divide(sums, counts, out=np.zeros_like(sums), where=counts > 0)
    return arr - col_mean


def bandpass_time_axis(values: np.ndarray, time_ns: np.ndarray, low_ghz: float, high_ghz: float) -> np.ndarray:
    arr = centered_matrix(values)
    finite_mask = np.isfinite(arr)
    filled = np.where(finite_mask, arr, 0.0)
    if filled.shape[0] != len(time_ns):
        raise ValueError("time axis length does not match matrix row count")
    if filled.shape[0] < 4:
        raise ValueError("need at least four time samples for band filtering")
    dt_ns = float(np.median(np.diff(np.asarray(time_ns, dtype=np.float64))))
    if not math.isfinite(dt_ns) or dt_ns <= 0.0:
        raise ValueError("time axis must be strictly increasing")
    freqs_ghz = np.fft.rfftfreq(filled.shape[0], d=dt_ns)
    band_mask = (freqs_ghz >= float(low_ghz)) & (freqs_ghz <= float(high_ghz))
    if not np.any(band_mask):
        closest = int(np.argmin(np.abs(freqs_ghz - 0.5 * (float(low_ghz) + float(high_ghz)))))
        band_mask[closest] = True
    spectrum = np.fft.rfft(filled, axis=0)
    spectrum[~band_mask, :] = 0.0
    filtered = np.fft.irfft(spectrum, n=filled.shape[0], axis=0)
    return np.where(finite_mask, filtered, np.nan)


def matrix_energy(values: np.ndarray) -> float:
    arr = centered_matrix(values)
    finite = arr[np.isfinite(arr)]
    return float(np.sum(finite * finite)) if finite.size else math.nan


def band_energy_fraction(filtered: np.ndarray, broadband: np.ndarray) -> float:
    numerator = matrix_energy(filtered)
    denominator = matrix_energy(broadband)
    if not (math.isfinite(numerator) and math.isfinite(denominator) and denominator > 0.0):
        return math.nan
    return numerator / denominator


def audit_pair_bands(
    *,
    pair_label: str,
    claim_scope: str,
    windows: dict,
    bands: list[dict],
) -> list[dict]:
    rows: list[dict] = []
    reference = windows["reference_window"]
    raw = windows["raw_aligned_comparison"]
    corrected = windows["corrected_aligned_comparison"]
    time_ns = windows["time_ns"]
    raw_full = compare_matrices(reference, raw)
    corrected_full = compare_matrices(reference, corrected)
    rows.append(
        {
            "pair_label": pair_label,
            "claim_scope": claim_scope,
            "band_label": "unfiltered",
            "low_ghz": "",
            "high_ghz": "",
            "reference_energy_fraction": 1.0,
            "comparison_energy_fraction": 1.0,
            "raw_abs_correlation": safe_float(raw_full.get("absolute_correlation")),
            "corrected_abs_correlation": safe_float(corrected_full.get("absolute_correlation")),
            "abs_correlation_gain": (
                safe_float(corrected_full.get("absolute_correlation"))
                - safe_float(raw_full.get("absolute_correlation"))
            ),
            "supported_band": bool(
                safe_float(corrected_full.get("absolute_correlation")) >= 0.60
                and (
                    safe_float(corrected_full.get("absolute_correlation"))
                    - safe_float(raw_full.get("absolute_correlation"))
                )
                > 0.02
            ),
        }
    )
    for band in bands:
        ref_band = bandpass_time_axis(reference, time_ns, band["low_ghz"], band["high_ghz"])
        raw_band = bandpass_time_axis(raw, time_ns, band["low_ghz"], band["high_ghz"])
        corrected_band = bandpass_time_axis(corrected, time_ns, band["low_ghz"], band["high_ghz"])
        raw_metrics = compare_matrices(ref_band, raw_band)
        corrected_metrics = compare_matrices(ref_band, corrected_band)
        raw_abs = safe_float(raw_metrics.get("absolute_correlation"))
        corrected_abs = safe_float(corrected_metrics.get("absolute_correlation"))
        gain = corrected_abs - raw_abs if math.isfinite(raw_abs) and math.isfinite(corrected_abs) else math.nan
        ref_fraction = band_energy_fraction(ref_band, reference)
        cmp_fraction = band_energy_fraction(corrected_band, corrected)
        rows.append(
            {
                "pair_label": pair_label,
                "claim_scope": claim_scope,
                "band_label": band["band_label"],
                "low_ghz": band["low_ghz"],
                "high_ghz": band["high_ghz"],
                "reference_energy_fraction": ref_fraction,
                "comparison_energy_fraction": cmp_fraction,
                "raw_abs_correlation": raw_abs,
                "corrected_abs_correlation": corrected_abs,
                "abs_correlation_gain": gain,
                "supported_band": bool(
                    math.isfinite(gain)
                    and gain > 0.02
                    and corrected_abs >= 0.60
                    and min(ref_fraction, cmp_fraction) >= 0.02
                ),
            }
        )
    return rows


def summarize_band_audit(rows: list[dict]) -> dict:
    short_rows = [row for row in rows if row["pair_label"] == "short_014_016" and row["band_label"] != "unfiltered"]
    long_rows = [row for row in rows if row["pair_label"] == "long_015_013" and row["band_label"] != "unfiltered"]
    short_supported = [row for row in short_rows if bool(row["supported_band"])]
    long_supported = [row for row in long_rows if bool(row["supported_band"])]
    short_unfiltered = next((row for row in rows if row["pair_label"] == "short_014_016" and row["band_label"] == "unfiltered"), {})
    long_unfiltered = next((row for row in rows if row["pair_label"] == "long_015_013" and row["band_label"] == "unfiltered"), {})
    if len(short_supported) >= 3 and safe_float(short_unfiltered.get("abs_correlation_gain")) > 0.05:
        label = "field_bandlimited_repeatability_short_pair_supported_long_pattern_only"
    elif len(short_supported) >= 1:
        label = "field_bandlimited_repeatability_limited_short_pair_support"
    else:
        label = "field_bandlimited_repeatability_not_supported"
    return {
        "policy_label": label,
        "short_supported_band_count": len(short_supported),
        "short_supported_bands": ",".join(row["band_label"] for row in short_supported),
        "long_pattern_supported_band_count": len(long_supported),
        "long_pattern_supported_bands": ",".join(row["band_label"] for row in long_supported),
        "short_unfiltered_raw_abs_correlation": safe_float(short_unfiltered.get("raw_abs_correlation")),
        "short_unfiltered_corrected_abs_correlation": safe_float(short_unfiltered.get("corrected_abs_correlation")),
        "short_unfiltered_abs_correlation_gain": safe_float(short_unfiltered.get("abs_correlation_gain")),
        "long_unfiltered_raw_abs_correlation": safe_float(long_unfiltered.get("raw_abs_correlation")),
        "long_unfiltered_pattern_abs_correlation": safe_float(long_unfiltered.get("corrected_abs_correlation")),
        "long_unfiltered_pattern_gain": safe_float(long_unfiltered.get("abs_correlation_gain")),
        "field_gpu_fwi_priority": "none",
        "decision": (
            "Use band-limited repeatability as measured-field QC only. The short "
            "014/016 branch may guide field figure band choices after the accepted "
            "relative time-zero transfer. The long 015/013 branch remains "
            "pattern-only because profile 013 lacks usable phase-anchor picks."
        ),
    }


def plot_band_audit(rows: list[dict], summary: dict, save_path: Path) -> str:
    plot_rows = [row for row in rows if row["band_label"] != "unfiltered"]
    labels = sorted({row["band_label"] for row in plot_rows}, key=lambda item: [row["band_label"] for row in plot_rows].index(item))
    pairs = ["short_014_016", "long_015_013"]
    x = np.arange(len(labels))
    width = 0.36

    fig, axes = plt.subplots(3, 1, figsize=(12.8, 9.0), constrained_layout=True)
    colors = {"short_014_016": "#4c78a8", "long_015_013": "#f58518"}
    for idx, pair in enumerate(pairs):
        pair_rows = {row["band_label"]: row for row in plot_rows if row["pair_label"] == pair}
        offset = (idx - 0.5) * width
        axes[0].bar(
            x + offset,
            [safe_float(pair_rows[label].get("corrected_abs_correlation")) for label in labels],
            width=width,
            color=colors[pair],
            label=pair,
        )
        axes[1].bar(
            x + offset,
            [safe_float(pair_rows[label].get("abs_correlation_gain")) for label in labels],
            width=width,
            color=colors[pair],
            label=pair,
        )
        axes[2].bar(
            x + offset,
            [
                min(
                    safe_float(pair_rows[label].get("reference_energy_fraction")),
                    safe_float(pair_rows[label].get("comparison_energy_fraction")),
                )
                for label in labels
            ],
            width=width,
            color=colors[pair],
            label=pair,
        )
    axes[0].set_ylabel("aligned |corr|")
    axes[0].set_title("Band-limited aligned profile agreement")
    axes[1].axhline(0.0, color="#555555", linewidth=0.8)
    axes[1].set_ylabel("gain vs raw")
    axes[1].set_title("Band-limited gain after accepted shift")
    axes[2].set_ylabel("min energy fraction")
    axes[2].set_title("Band energy retained in both aligned profiles")
    for ax in axes:
        ax.set_xticks(x, labels)
        ax.grid(axis="y", color="#dddddd", linewidth=0.6)
        ax.legend(frameon=False, fontsize=8)
    fig.suptitle(summary["policy_label"], fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--short-stack-summary", default=DEFAULT_SHORT_STACK_SUMMARY)
    parser.add_argument("--short-applied-summary", default=DEFAULT_SHORT_APPLIED_SUMMARY)
    parser.add_argument("--long-stack-summary", default=DEFAULT_LONG_STACK_SUMMARY)
    parser.add_argument("--long-shift-summary", default=DEFAULT_LONG_SHIFT_SUMMARY)
    parser.add_argument("--time-window-ns", default="0.55,3.40")
    parser.add_argument("--bands-ghz", default=DEFAULT_BANDS)
    parser.add_argument("--run-name", default="gssi51600s_field_bandlimited_repeatability_audit")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    time_min_ns, time_max_ns = [float(part.strip()) for part in args.time_window_ns.split(",", 1)]
    bands = parse_bands(args.bands_ghz)
    short_stack = read_json(args.short_stack_summary)
    short_applied = read_json(args.short_applied_summary)
    long_stack = read_json(args.long_stack_summary)
    long_shift = read_json(args.long_shift_summary)
    profiles = load_profile_map(Path(args.input_dir))

    short_windows = build_profile_windows(
        profiles,
        reference_stem=short_stack["reference_stem"],
        comparison_stem=short_stack["comparison_stem"],
        time_window_ns=(time_min_ns, time_max_ns),
        transfer_offset_ns=safe_float(short_applied.get("summary", {}).get("applied_transfer_offset_ns")),
        orientation=str(short_stack.get("summary", {}).get("best_orientation")),
        lag_samples=stack_lag_samples(short_stack),
    )
    long_windows = build_profile_windows(
        profiles,
        reference_stem=long_stack["reference_stem"],
        comparison_stem=long_stack["comparison_stem"],
        time_window_ns=(time_min_ns, time_max_ns),
        transfer_offset_ns=safe_float(long_shift.get("summary", {}).get("best_matrix_offset_ns")),
        orientation=str(long_stack.get("summary", {}).get("best_orientation")),
        lag_samples=stack_lag_samples(long_stack),
    )

    rows = []
    rows.extend(
        audit_pair_bands(
            pair_label="short_014_016",
            claim_scope="relative_time_zero_qc",
            windows=short_windows,
            bands=bands,
        )
    )
    rows.extend(
        audit_pair_bands(
            pair_label="long_015_013",
            claim_scope="pattern_only_not_time_zero",
            windows=long_windows,
            bands=bands,
        )
    )
    summary = summarize_band_audit(rows)

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_bandlimited_repeatability_rows.csv"
    summary_json = data_dir / "field_bandlimited_repeatability_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_band_audit(rows, summary, figures_dir / "field_bandlimited_repeatability.png"))

    output_summary = {
        **summary,
        "time_window_min_ns": time_min_ns,
        "time_window_max_ns": time_max_ns,
        "bands": bands,
        "input_summaries": {
            "short_stack_summary": args.short_stack_summary,
            "short_applied_summary": args.short_applied_summary,
            "long_stack_summary": args.long_stack_summary,
            "long_shift_summary": args.long_shift_summary,
        },
        "paths": {
            "rows_csv": str(rows_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
        "readgssi_version": readgssi_version(),
    }
    write_csv_rows(rows_csv, rows)
    write_csv_rows(validation_csv, [figure_stats(figure_path)])
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_bandlimited_repeatability_audit",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

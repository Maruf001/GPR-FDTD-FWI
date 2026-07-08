#!/usr/bin/env python3
"""Measure field-trace alignment at supported content time-zero anchors."""

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
    DEFAULT_DATASET_ID,
    DEFAULT_FIELD_ROOT,
    DEFAULT_INPUT_DIR,
    field_dataset_output_root,
    read_dzt_profiles,
    readgssi_version,
)
from run_gssi_field_preprocess_feature_qc import build_axes, json_safe, preprocess_profile  # noqa: E402
from run_gssi_field_synthetic_waveform_probe import interpolate_matrix, robust_normalize  # noqa: E402
from visualization.plot_style import safe_symmetric_limits, save_validated_figure  # noqa: E402


DEFAULT_ANCHOR_RUN = "037_gssi51600s_content_time_zero_anchor_policy"
DEFAULT_APPLIED_RUN = "025_gssi51600s_short_profile_time_zero_application_policy"


def read_csv_rows(path: str | Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def boolish(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def supported_anchor_pairs(anchor_rows: list[dict], applied_rows: list[dict]) -> list[dict]:
    applied_by_pair = {int(safe_float(row.get("pair_index"), -1)): row for row in applied_rows}
    out: list[dict] = []
    for anchor in anchor_rows:
        pair_index = int(safe_float(anchor.get("pair_index"), -1))
        if anchor.get("anchor_policy_label") != "content_time_zero_anchor_supported":
            continue
        applied = applied_by_pair.get(pair_index)
        if applied is None:
            continue
        out.append({**applied, **{f"anchor_{key}": value for key, value in anchor.items()}})
    return sorted(out, key=lambda row: int(safe_float(row.get("pair_index"), 0)))


def load_processed_profiles(input_dir: Path, file_names: set[str]) -> tuple[dict[str, dict], dict[str, tuple[np.ndarray, np.ndarray]]]:
    processed_by_file: dict[str, dict] = {}
    axes_by_file: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for record, raw in read_dzt_profiles(input_dir):
        file_name = str(record.get("file", ""))
        if file_name not in file_names:
            continue
        processed_by_file[file_name] = preprocess_profile(raw)
        axes_by_file[file_name] = build_axes(record)
    return processed_by_file, axes_by_file


def extract_trace(
    processed_by_file: dict[str, dict],
    axes_by_file: dict[str, tuple[np.ndarray, np.ndarray]],
    *,
    file_name: str,
    x_m: float,
    time_ns: np.ndarray,
) -> np.ndarray:
    if file_name not in processed_by_file or file_name not in axes_by_file:
        return np.full(time_ns.shape, np.nan, dtype=np.float64)
    x_values, time_values = axes_by_file[file_name]
    window = interpolate_matrix(
        processed_by_file[file_name]["corrected"],
        x_values,
        time_values,
        np.asarray([float(x_m)], dtype=np.float64),
        np.asarray(time_ns, dtype=np.float64),
    )
    return window[:, 0]


def compare_traces(reference: np.ndarray, comparison: np.ndarray) -> dict:
    ref = robust_normalize(np.asarray(reference, dtype=np.float64).reshape(-1, 1)).ravel()
    cmp = robust_normalize(np.asarray(comparison, dtype=np.float64).reshape(-1, 1)).ravel()
    mask = np.isfinite(ref) & np.isfinite(cmp)
    if int(np.count_nonzero(mask)) < 8:
        return {
            "valid_sample_count": int(np.count_nonzero(mask)),
            "normalized_correlation": math.nan,
            "absolute_correlation": math.nan,
            "polarity": "insufficient",
            "normalized_residual_rms": math.nan,
        }
    r = ref[mask]
    c = cmp[mask]
    denom = float(np.linalg.norm(r) * np.linalg.norm(c))
    corr = float(np.dot(r, c) / denom) if denom > 0.0 else math.nan
    polarity = "same" if math.isfinite(corr) and corr >= 0.0 else "opposite"
    signed = c if polarity == "same" else -c
    residual = r - signed
    return {
        "valid_sample_count": int(np.count_nonzero(mask)),
        "normalized_correlation": corr,
        "absolute_correlation": abs(corr) if math.isfinite(corr) else math.nan,
        "polarity": polarity,
        "normalized_residual_rms": float(np.sqrt(np.mean(residual ** 2))),
    }


def build_alignment_payloads(
    supported_pairs: list[dict],
    processed_by_file: dict[str, dict],
    axes_by_file: dict[str, tuple[np.ndarray, np.ndarray]],
    *,
    window_pre_ns: float,
    window_post_ns: float,
    sample_count: int,
) -> list[dict]:
    rel_time = np.linspace(-float(window_pre_ns), float(window_post_ns), int(sample_count))
    payloads: list[dict] = []
    for row in supported_pairs:
        ref_file = str(row.get("reference_file", ""))
        cmp_file = str(row.get("comparison_file", ""))
        ref_x = safe_float(row.get("reference_x_m"))
        cmp_x = safe_float(row.get("comparison_original_x_m"))
        ref_t = safe_float(row.get("reference_phase_time_ns"))
        cmp_t = safe_float(row.get("comparison_phase_time_ns"))
        transfer = safe_float(row.get("applied_transfer_offset_ns"))
        if not all(math.isfinite(value) for value in [ref_x, cmp_x, ref_t, cmp_t, transfer]):
            continue
        ref_trace = extract_trace(
            processed_by_file,
            axes_by_file,
            file_name=ref_file,
            x_m=ref_x,
            time_ns=ref_t + rel_time,
        )
        raw_trace = extract_trace(
            processed_by_file,
            axes_by_file,
            file_name=cmp_file,
            x_m=cmp_x,
            time_ns=ref_t + rel_time,
        )
        corrected_trace = extract_trace(
            processed_by_file,
            axes_by_file,
            file_name=cmp_file,
            x_m=cmp_x,
            time_ns=ref_t + transfer + rel_time,
        )
        event_local_trace = extract_trace(
            processed_by_file,
            axes_by_file,
            file_name=cmp_file,
            x_m=cmp_x,
            time_ns=cmp_t + rel_time,
        )
        raw_compare = compare_traces(ref_trace, raw_trace)
        corrected_compare = compare_traces(ref_trace, corrected_trace)
        event_compare = compare_traces(ref_trace, event_local_trace)
        raw_abs = safe_float(raw_compare.get("absolute_correlation"))
        corrected_abs = safe_float(corrected_compare.get("absolute_correlation"))
        payloads.append({
            **row,
            "relative_time_ns": rel_time,
            "reference_trace": robust_normalize(ref_trace.reshape(-1, 1)).ravel(),
            "raw_comparison_trace": robust_normalize(raw_trace.reshape(-1, 1)).ravel(),
            "corrected_comparison_trace": robust_normalize(corrected_trace.reshape(-1, 1)).ravel(),
            "event_local_comparison_trace": robust_normalize(event_local_trace.reshape(-1, 1)).ravel(),
            "raw_field_trace_abs_correlation": raw_abs,
            "raw_field_trace_polarity": raw_compare.get("polarity"),
            "raw_field_trace_residual_rms": safe_float(raw_compare.get("normalized_residual_rms")),
            "corrected_field_trace_abs_correlation": corrected_abs,
            "corrected_field_trace_polarity": corrected_compare.get("polarity"),
            "corrected_field_trace_residual_rms": safe_float(corrected_compare.get("normalized_residual_rms")),
            "event_local_field_trace_abs_correlation": safe_float(event_compare.get("absolute_correlation")),
            "field_trace_abs_correlation_improvement": (
                corrected_abs - raw_abs if math.isfinite(corrected_abs) and math.isfinite(raw_abs) else math.nan
            ),
        })
    return payloads


def payload_rows(payloads: list[dict]) -> list[dict]:
    omitted = {
        "relative_time_ns",
        "reference_trace",
        "raw_comparison_trace",
        "corrected_comparison_trace",
        "event_local_comparison_trace",
    }
    return [{key: value for key, value in payload.items() if key not in omitted} for payload in payloads]


def summarize_alignment(rows: list[dict]) -> dict:
    raw_corr = [
        safe_float(row.get("raw_field_trace_abs_correlation"))
        for row in rows
        if math.isfinite(safe_float(row.get("raw_field_trace_abs_correlation")))
    ]
    corrected_corr = [
        safe_float(row.get("corrected_field_trace_abs_correlation"))
        for row in rows
        if math.isfinite(safe_float(row.get("corrected_field_trace_abs_correlation")))
    ]
    improvements = [
        safe_float(row.get("field_trace_abs_correlation_improvement"))
        for row in rows
        if math.isfinite(safe_float(row.get("field_trace_abs_correlation_improvement")))
    ]
    improved_count = sum(1 for value in improvements if value > 0.0)
    if rows and improved_count == len(rows):
        label = "content_anchor_field_trace_alignment_improves_after_time_zero"
    elif improved_count:
        label = "content_anchor_field_trace_alignment_mixed_after_time_zero"
    else:
        label = "content_anchor_field_trace_alignment_not_improved"
    return {
        "policy_label": label,
        "supported_anchor_pair_count": len(rows),
        "field_trace_alignment_improved_count": improved_count,
        "mean_raw_abs_correlation": float(np.mean(raw_corr)) if raw_corr else math.nan,
        "mean_corrected_abs_correlation": float(np.mean(corrected_corr)) if corrected_corr else math.nan,
        "mean_abs_correlation_improvement": float(np.mean(improvements)) if improvements else math.nan,
        "min_abs_correlation_improvement": min(improvements) if improvements else math.nan,
        "max_abs_correlation_improvement": max(improvements) if improvements else math.nan,
        "max_corrected_abs_timing_residual_ns": max(
            (
                abs(safe_float(row.get("corrected_comparison_minus_reference_phase_time_ns")))
                for row in rows
            ),
            default=math.nan,
        ),
        "policy": (
            "Use the field-trace alignment packet as measured-data support for "
            "relative time-zero anchoring and visual QC only. This is not field "
            "radius, cover-depth, geometry, 3D, or FWI evidence."
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


def plot_alignment(payloads: list[dict], summary: dict, save_path: Path) -> str:
    row_count = max(1, len(payloads))
    fig, axes = plt.subplots(row_count, 2, figsize=(13.2, 4.2 * row_count), constrained_layout=True)
    axes = np.asarray(axes).reshape(row_count, 2)
    values = []
    for payload in payloads:
        values.extend(payload["reference_trace"][np.isfinite(payload["reference_trace"])])
        values.extend(payload["raw_comparison_trace"][np.isfinite(payload["raw_comparison_trace"])])
        values.extend(payload["corrected_comparison_trace"][np.isfinite(payload["corrected_comparison_trace"])])
    limits = safe_symmetric_limits(np.asarray(values, dtype=np.float64), percentile=98.0, floor=1.0)

    for row_idx, payload in enumerate(payloads):
        t = payload["relative_time_ns"]
        pair = int(safe_float(payload.get("pair_index"), row_idx + 1))
        axes[row_idx, 0].plot(t, payload["reference_trace"], color="#1f4e79", linewidth=1.4, label="014 reference")
        axes[row_idx, 0].plot(
            t,
            payload["raw_comparison_trace"],
            color="#c7302b",
            linewidth=1.1,
            label="016 before transfer",
        )
        axes[row_idx, 0].axvline(0.0, color="#222222", linestyle=":", linewidth=0.8)
        axes[row_idx, 0].set_ylim(limits)
        axes[row_idx, 0].set_title(
            f"pair {pair} before correction |corr|={payload['raw_field_trace_abs_correlation']:.3f}",
            fontsize=10,
        )
        axes[row_idx, 0].set_xlabel("time relative to 014 anchor [ns]")
        axes[row_idx, 0].set_ylabel("normalized amplitude")
        axes[row_idx, 0].grid(color="#dddddd", linewidth=0.6)

        axes[row_idx, 1].plot(t, payload["reference_trace"], color="#1f4e79", linewidth=1.4, label="014 reference")
        axes[row_idx, 1].plot(
            t,
            payload["corrected_comparison_trace"],
            color="#2f9d55",
            linewidth=1.1,
            label="016 after transfer",
        )
        axes[row_idx, 1].axvline(0.0, color="#222222", linestyle=":", linewidth=0.8)
        axes[row_idx, 1].set_ylim(limits)
        axes[row_idx, 1].set_title(
            f"pair {pair} after correction |corr|={payload['corrected_field_trace_abs_correlation']:.3f}",
            fontsize=10,
        )
        axes[row_idx, 1].set_xlabel("time relative to corrected 016 anchor [ns]")
        axes[row_idx, 1].set_ylabel("normalized amplitude")
        axes[row_idx, 1].grid(color="#dddddd", linewidth=0.6)

    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 1].legend(frameon=False, fontsize=8)
    fig.suptitle(
        (
            "Content-backed field trace alignment: "
            f"{summary['policy_label']}, mean improvement="
            f"{summary['mean_abs_correlation_improvement']:.3f}"
        ),
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--anchor-run", default=DEFAULT_ANCHOR_RUN)
    parser.add_argument("--applied-run", default=DEFAULT_APPLIED_RUN)
    parser.add_argument("--window-pre-ns", type=float, default=0.24)
    parser.add_argument("--window-post-ns", type=float, default=0.36)
    parser.add_argument("--sample-count", type=int, default=121)
    parser.add_argument("--run-name", default="gssi51600s_content_anchor_trace_alignment")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    anchor_csv = dataset_root / args.anchor_run / "data" / "short_profile_content_time_zero_anchor_rows.csv"
    applied_csv = dataset_root / args.applied_run / "data" / "short_profile_time_zero_applied_event_residuals.csv"
    for path in (anchor_csv, applied_csv):
        if not path.exists():
            raise FileNotFoundError(path)
    supported_pairs = supported_anchor_pairs(read_csv_rows(anchor_csv), read_csv_rows(applied_csv))
    file_names = {
        str(row.get("reference_file", ""))
        for row in supported_pairs
        if str(row.get("reference_file", ""))
    } | {
        str(row.get("comparison_file", ""))
        for row in supported_pairs
        if str(row.get("comparison_file", ""))
    }
    processed_by_file, axes_by_file = load_processed_profiles(Path(args.input_dir), file_names)
    missing = sorted(file_names - set(processed_by_file))
    if missing:
        raise FileNotFoundError(f"missing DZT profiles after import: {missing}")

    payloads = build_alignment_payloads(
        supported_pairs,
        processed_by_file,
        axes_by_file,
        window_pre_ns=args.window_pre_ns,
        window_post_ns=args.window_post_ns,
        sample_count=args.sample_count,
    )
    rows = payload_rows(payloads)
    summary = summarize_alignment(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "content_anchor_trace_alignment_rows.csv"
    summary_json = data_dir / "content_anchor_trace_alignment_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_alignment(payloads, summary, figures_dir / "content_anchor_trace_alignment.png"))

    write_csv_rows(rows_csv, rows)
    write_csv_rows(validation_csv, [figure_stats(figure_path)])
    output_summary = {
        **summary,
        "input_anchor_csv": str(anchor_csv),
        "input_applied_csv": str(applied_csv),
        "window_pre_ns": args.window_pre_ns,
        "window_post_ns": args.window_post_ns,
        "sample_count": args.sample_count,
        "paths": {
            "alignment_rows_csv": str(rows_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_content_anchor_trace_alignment",
        {
            "summary_json": str(summary_json),
            "alignment_rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

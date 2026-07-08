#!/usr/bin/env python3
"""Window-sensitivity check for content-anchor field trace alignment."""

from __future__ import annotations

import argparse
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
from run_gssi_dzt_qc import (  # noqa: E402
    DEFAULT_DATASET_ID,
    DEFAULT_FIELD_ROOT,
    DEFAULT_INPUT_DIR,
    field_dataset_output_root,
    readgssi_version,
)
from run_gssi_field_content_anchor_trace_alignment import (  # noqa: E402
    DEFAULT_ANCHOR_RUN,
    DEFAULT_APPLIED_RUN,
    build_alignment_payloads,
    figure_stats,
    load_processed_profiles,
    payload_rows,
    read_csv_rows,
    safe_float,
    summarize_alignment,
    supported_anchor_pairs,
    write_csv_rows,
)
from run_gssi_field_preprocess_feature_qc import json_safe  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_WINDOWS = "0.16:0.24:101,0.24:0.36:121,0.32:0.48:161"


def parse_window_configs(text: str) -> list[dict]:
    configs: list[dict] = []
    for item in str(text).split(","):
        item = item.strip()
        if not item:
            continue
        parts = item.split(":")
        if len(parts) != 3:
            raise argparse.ArgumentTypeError("window configs must be pre:post:samples")
        try:
            pre = float(parts[0])
            post = float(parts[1])
            samples = int(parts[2])
        except ValueError as exc:
            raise argparse.ArgumentTypeError("window configs must be numeric pre:post:samples") from exc
        if pre <= 0.0 or post <= 0.0 or samples < 16:
            raise argparse.ArgumentTypeError("window pre/post must be positive and samples >= 16")
        configs.append({
            "window_label": f"pre{pre:g}_post{post:g}_n{samples}",
            "window_pre_ns": pre,
            "window_post_ns": post,
            "sample_count": samples,
        })
    if not configs:
        raise argparse.ArgumentTypeError("expected at least one window config")
    return configs


def build_sensitivity_rows(
    supported_pairs: list[dict],
    processed_by_file: dict,
    axes_by_file: dict,
    window_configs: list[dict],
) -> tuple[list[dict], list[dict]]:
    pair_rows: list[dict] = []
    window_rows: list[dict] = []
    for config in window_configs:
        payloads = build_alignment_payloads(
            supported_pairs,
            processed_by_file,
            axes_by_file,
            window_pre_ns=config["window_pre_ns"],
            window_post_ns=config["window_post_ns"],
            sample_count=config["sample_count"],
        )
        rows = payload_rows(payloads)
        summary = summarize_alignment(rows)
        window_rows.append({
            **config,
            **summary,
        })
        for row in rows:
            pair_rows.append({
                **config,
                "pair_index": int(safe_float(row.get("pair_index"), -1)),
                "raw_field_trace_abs_correlation": safe_float(row.get("raw_field_trace_abs_correlation")),
                "corrected_field_trace_abs_correlation": safe_float(row.get("corrected_field_trace_abs_correlation")),
                "field_trace_abs_correlation_improvement": safe_float(
                    row.get("field_trace_abs_correlation_improvement")
                ),
                "corrected_comparison_minus_reference_phase_time_ns": safe_float(
                    row.get("corrected_comparison_minus_reference_phase_time_ns")
                ),
            })
    return pair_rows, window_rows


def summarize_sensitivity(window_rows: list[dict], pair_rows: list[dict]) -> dict:
    improved_pairs = [
        row for row in pair_rows
        if safe_float(row.get("field_trace_abs_correlation_improvement")) > 0.0
    ]
    improvements = [
        safe_float(row.get("field_trace_abs_correlation_improvement"))
        for row in pair_rows
        if math.isfinite(safe_float(row.get("field_trace_abs_correlation_improvement")))
    ]
    corrected = [
        safe_float(row.get("corrected_field_trace_abs_correlation"))
        for row in pair_rows
        if math.isfinite(safe_float(row.get("corrected_field_trace_abs_correlation")))
    ]
    all_improved = bool(pair_rows) and len(improved_pairs) == len(pair_rows)
    if all_improved:
        label = "content_anchor_trace_alignment_window_robust"
    elif improved_pairs:
        label = "content_anchor_trace_alignment_window_mixed"
    else:
        label = "content_anchor_trace_alignment_window_not_robust"
    return {
        "policy_label": label,
        "window_count": len(window_rows),
        "pair_window_row_count": len(pair_rows),
        "improved_pair_window_count": len(improved_pairs),
        "all_pair_windows_improved": all_improved,
        "min_abs_correlation_improvement": min(improvements) if improvements else math.nan,
        "mean_abs_correlation_improvement": float(np.mean(improvements)) if improvements else math.nan,
        "max_abs_correlation_improvement": max(improvements) if improvements else math.nan,
        "min_corrected_abs_correlation": min(corrected) if corrected else math.nan,
        "mean_corrected_abs_correlation": float(np.mean(corrected)) if corrected else math.nan,
        "policy": (
            "Use the window-sensitivity result as robustness support for the "
            "measured relative time-zero anchor. This is still field timing and "
            "visual-QC evidence only, not field inversion evidence."
        ),
    }


def plot_sensitivity(window_rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["window_label"].replace("_", "\n") for row in window_rows]
    x = np.arange(len(window_rows))
    raw = [safe_float(row.get("mean_raw_abs_correlation"), 0.0) for row in window_rows]
    corrected = [safe_float(row.get("mean_corrected_abs_correlation"), 0.0) for row in window_rows]
    improvement = [safe_float(row.get("mean_abs_correlation_improvement"), 0.0) for row in window_rows]

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 4.8), constrained_layout=True)
    axes[0].bar(x - 0.18, raw, width=0.36, color="#c7302b", label="raw")
    axes[0].bar(x + 0.18, corrected, width=0.36, color="#2f9d55", label="corrected")
    axes[0].set_xticks(x, labels)
    axes[0].set_ylim(0.0, 1.05)
    axes[0].set_ylabel("mean abs correlation")
    axes[0].set_title("Measured trace agreement by window")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, improvement, color="#4c78a8", width=0.55)
    axes[1].axhline(0.0, color="#222222", linewidth=0.8)
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("mean corrected - raw abs corr")
    axes[1].set_title("Improvement is window-robust")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        (
            "Content-anchor trace alignment sensitivity: "
            f"{summary['policy_label']}"
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
    parser.add_argument("--windows", default=DEFAULT_WINDOWS)
    parser.add_argument("--run-name", default="gssi51600s_content_anchor_trace_alignment_sensitivity")
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

    window_configs = parse_window_configs(args.windows)
    pair_rows, window_rows = build_sensitivity_rows(
        supported_pairs,
        processed_by_file,
        axes_by_file,
        window_configs,
    )
    summary = summarize_sensitivity(window_rows, pair_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    pair_csv = data_dir / "content_anchor_trace_alignment_sensitivity_pairs.csv"
    window_csv = data_dir / "content_anchor_trace_alignment_sensitivity_windows.csv"
    summary_json = data_dir / "content_anchor_trace_alignment_sensitivity_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_sensitivity(window_rows, summary, figures_dir / "content_anchor_trace_alignment_sensitivity.png"))

    write_csv_rows(pair_csv, pair_rows)
    write_csv_rows(window_csv, window_rows)
    write_csv_rows(validation_csv, [figure_stats(figure_path)])
    output_summary = {
        **summary,
        "input_anchor_csv": str(anchor_csv),
        "input_applied_csv": str(applied_csv),
        "window_configs": window_configs,
        "paths": {
            "pair_csv": str(pair_csv),
            "window_csv": str(window_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_content_anchor_trace_alignment_sensitivity",
        {
            "summary_json": str(summary_json),
            "pair_csv": str(pair_csv),
            "window_csv": str(window_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

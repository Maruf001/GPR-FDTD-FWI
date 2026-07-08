#!/usr/bin/env python3
"""Content-aware field-to-synthetic policy for short GSSI profile events."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import figure_stats  # noqa: E402
from run_gssi_field_profile_repeatability_policy import safe_float  # noqa: E402
from run_gssi_field_short_profile_content_window_policy import boolish  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CONTENT_RUN = "031_gssi51600s_short_profile_content_window_policy"
DEFAULT_WAVEFORM_RUN = "011_gssi51600s_field_synthetic_waveform_family_shift_epsr_probe"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def candidate_is_valid(row: dict, phase_convention: str) -> bool:
    return (
        boolish(row.get("geometry_valid"))
        and not str(row.get("skip_reason", "")).strip()
        and str(row.get("phase_convention")) == phase_convention
        and math.isfinite(safe_float(row.get("absolute_correlation")))
    )


def best_waveform_candidate(
    waveform_rows: list[dict],
    *,
    file_name: str,
    apex_group: int,
    phase_convention: str,
) -> dict | None:
    matches = [
        row for row in waveform_rows
        if str(row.get("file")) == file_name
        and int(safe_float(row.get("apex_group"), -1)) == int(apex_group)
        and candidate_is_valid(row, phase_convention)
    ]
    if not matches:
        return None
    return max(
        matches,
        key=lambda row: (
            safe_float(row.get("absolute_correlation")),
            -safe_float(row.get("normalized_residual_rms"), math.inf),
        ),
    )


def _candidate_fields(prefix: str, row: dict | None) -> dict:
    if row is None:
        return {
            f"{prefix}_candidate_id": "",
            f"{prefix}_radius_mm": math.nan,
            f"{prefix}_epsr_source": "",
            f"{prefix}_concrete_epsr": math.nan,
            f"{prefix}_absolute_correlation": math.nan,
            f"{prefix}_normalized_residual_rms": math.nan,
            f"{prefix}_synthetic_time_shift_ns": math.nan,
            f"{prefix}_polarity": "",
        }
    return {
        f"{prefix}_candidate_id": row.get("candidate_id", ""),
        f"{prefix}_radius_mm": safe_float(row.get("radius_mm")),
        f"{prefix}_epsr_source": row.get("epsr_source", ""),
        f"{prefix}_concrete_epsr": safe_float(row.get("concrete_epsr")),
        f"{prefix}_absolute_correlation": safe_float(row.get("absolute_correlation")),
        f"{prefix}_normalized_residual_rms": safe_float(row.get("normalized_residual_rms")),
        f"{prefix}_synthetic_time_shift_ns": safe_float(row.get("synthetic_time_shift_ns")),
        f"{prefix}_polarity": row.get("polarity", ""),
    }


def build_event_waveform_rows(
    event_rows: list[dict],
    waveform_rows: list[dict],
    *,
    reference_file: str,
    comparison_file: str,
    phase_convention: str,
    min_abs_correlation: float,
) -> list[dict]:
    out: list[dict] = []
    for event in sorted(event_rows, key=lambda row: int(safe_float(row.get("pair_index"), 0))):
        ref = best_waveform_candidate(
            waveform_rows,
            file_name=reference_file,
            apex_group=int(safe_float(event.get("reference_apex_group"))),
            phase_convention=phase_convention,
        )
        cmp = best_waveform_candidate(
            waveform_rows,
            file_name=comparison_file,
            apex_group=int(safe_float(event.get("comparison_apex_group"))),
            phase_convention=phase_convention,
        )
        ref_corr = safe_float(ref.get("absolute_correlation")) if ref is not None else math.nan
        cmp_corr = safe_float(cmp.get("absolute_correlation")) if cmp is not None else math.nan
        pair_min_corr = min(ref_corr, cmp_corr) if math.isfinite(ref_corr) and math.isfinite(cmp_corr) else math.nan
        pair_mean_corr = float(np.mean([ref_corr, cmp_corr])) if math.isfinite(pair_min_corr) else math.nan
        content_backed = boolish(event.get("content_backed"))
        waveform_supported = math.isfinite(pair_min_corr) and pair_min_corr >= min_abs_correlation
        if content_backed and waveform_supported:
            label = "content_backed_waveform_supported_qc"
        elif waveform_supported:
            label = "timing_only_waveform_supported_limited"
        else:
            label = "waveform_support_weak_or_missing"
        out.append({
            "pair_index": int(safe_float(event.get("pair_index"))),
            "content_backed": content_backed,
            "content_label": event.get("content_label", ""),
            "reference_apex_group": int(safe_float(event.get("reference_apex_group"))),
            "comparison_apex_group": int(safe_float(event.get("comparison_apex_group"))),
            "reference_x_mm": safe_float(event.get("reference_x_mm")),
            "comparison_aligned_x_mm": safe_float(event.get("comparison_aligned_x_mm")),
            "timing_residual_to_bootstrap_median_ns": safe_float(event.get("timing_residual_to_bootstrap_median_ns")),
            **_candidate_fields("reference", ref),
            **_candidate_fields("comparison", cmp),
            "pair_min_absolute_correlation": pair_min_corr,
            "pair_mean_absolute_correlation": pair_mean_corr,
            "waveform_support_label": label,
        })
    return out


def summarize_policy(rows: list[dict], *, min_abs_correlation: float, min_content_pairs: int) -> dict:
    content_rows = [row for row in rows if bool(row.get("content_backed"))]
    timing_rows = [row for row in rows if not bool(row.get("content_backed"))]
    content_supported = [
        row for row in content_rows
        if row.get("waveform_support_label") == "content_backed_waveform_supported_qc"
    ]
    timing_supported = [
        row for row in timing_rows
        if row.get("waveform_support_label") == "timing_only_waveform_supported_limited"
    ]
    content_corr = [
        safe_float(row.get("pair_min_absolute_correlation"))
        for row in content_rows
        if math.isfinite(safe_float(row.get("pair_min_absolute_correlation")))
    ]
    timing_corr = [
        safe_float(row.get("pair_min_absolute_correlation"))
        for row in timing_rows
        if math.isfinite(safe_float(row.get("pair_min_absolute_correlation")))
    ]
    if len(content_supported) >= min_content_pairs:
        label = "content_backed_field_to_synthetic_qc_supported"
    elif content_supported:
        label = "content_backed_field_to_synthetic_qc_limited"
    else:
        label = "content_backed_field_to_synthetic_qc_not_supported"
    return {
        "policy_label": label,
        "event_pair_count": len(rows),
        "content_backed_event_pair_count": len(content_rows),
        "content_backed_waveform_supported_count": len(content_supported),
        "timing_only_event_pair_count": len(timing_rows),
        "timing_only_waveform_supported_count": len(timing_supported),
        "min_abs_correlation_threshold": min_abs_correlation,
        "min_content_pair_absolute_correlation": min(content_corr) if content_corr else math.nan,
        "min_timing_only_pair_absolute_correlation": min(timing_corr) if timing_corr else math.nan,
        "policy": (
            "Use content-backed field-to-synthetic waveform matches as QC evidence "
            "for later visual comparison only. Timing-only waveform matches are "
            "not repeat-content anchors. This does not support field radius, "
            "cover-depth, geometry, 3D, or FWI claims."
        ),
    }


def plot_policy(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [f"pair {int(row['pair_index'])}" for row in rows]
    x = np.arange(len(rows))
    min_corr = [safe_float(row.get("pair_min_absolute_correlation"), 0.0) for row in rows]
    mean_corr = [safe_float(row.get("pair_mean_absolute_correlation"), 0.0) for row in rows]
    colors = ["#2f9d55" if bool(row.get("content_backed")) else "#c7302b" for row in rows]

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.8), constrained_layout=True)
    axes[0].bar(x, min_corr, color=colors, width=0.62)
    axes[0].axhline(summary["min_abs_correlation_threshold"], color="#222222", linestyle="--", linewidth=0.9)
    axes[0].set_xticks(x, labels)
    axes[0].set_ylim(0, 1.0)
    axes[0].set_ylabel("min(abs corr 014, 016)")
    axes[0].set_title("Pair-level waveform support")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, mean_corr, color=colors, width=0.62)
    axes[1].set_xticks(x, labels)
    axes[1].set_ylim(0, 1.0)
    axes[1].set_ylabel("mean abs correlation")
    axes[1].set_title("Mean waveform correlation")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(summary["policy_label"], fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--content-dir", default=None)
    parser.add_argument("--waveform-dir", default=None)
    parser.add_argument("--reference-file", default="PROJECT001C__014.DZT")
    parser.add_argument("--comparison-file", default="PROJECT001C__016.DZT")
    parser.add_argument("--phase-convention", default="top_envelope_35pct")
    parser.add_argument("--min-abs-correlation", type=float, default=0.80)
    parser.add_argument("--min-content-pairs", type=int, default=2)
    parser.add_argument("--run-name", default="gssi51600s_short_profile_content_synthetic_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    content_dir = Path(args.content_dir) if args.content_dir else dataset_root / DEFAULT_CONTENT_RUN
    waveform_dir = Path(args.waveform_dir) if args.waveform_dir else dataset_root / DEFAULT_WAVEFORM_RUN

    event_rows = read_csv_rows(content_dir / "data" / "short_profile_event_content_classification.csv")
    waveform_rows = read_csv_rows(waveform_dir / "data" / "field_synthetic_waveform_probe.csv")
    rows = build_event_waveform_rows(
        event_rows,
        waveform_rows,
        reference_file=args.reference_file,
        comparison_file=args.comparison_file,
        phase_convention=args.phase_convention,
        min_abs_correlation=args.min_abs_correlation,
    )
    summary = summarize_policy(
        rows,
        min_abs_correlation=args.min_abs_correlation,
        min_content_pairs=args.min_content_pairs,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    event_csv = data_dir / "short_profile_content_synthetic_event_matches.csv"
    summary_json = data_dir / "short_profile_content_synthetic_policy_summary.json"
    figure_path = Path(plot_policy(rows, summary, figures_dir / "short_profile_content_synthetic_policy.png"))
    validation_csv = data_dir / "figure_validation.csv"

    write_csv(event_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])

    output_summary = {
        "content_dir": str(content_dir),
        "waveform_dir": str(waveform_dir),
        "reference_file": args.reference_file,
        "comparison_file": args.comparison_file,
        "phase_convention": args.phase_convention,
        "summary": summary,
        "paths": {
            "event_matches_csv": str(event_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_short_profile_content_synthetic_policy",
        {
            "summary_json": str(summary_json),
            "event_matches_csv": str(event_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

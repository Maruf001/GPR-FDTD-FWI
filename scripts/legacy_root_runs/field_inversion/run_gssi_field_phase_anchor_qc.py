#!/usr/bin/env python3
"""Phase/time-zero anchoring QC for local GSSI 51600S short profiles."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter
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
from run_gssi_field_common_offset_sweep import (  # noqa: E402
    common_offset_hyperbola_time_ns,
    fit_common_offset_profile,
)
from run_gssi_field_hyperbola_calibration import cluster_apex_cues  # noqa: E402
from run_gssi_field_preprocess_feature_qc import (  # noqa: E402
    build_axes,
    imshow_extent,
    json_safe,
    pick_reflector_cues,
    preprocess_profile,
    write_csv,
)
from visualization.plot_style import safe_symmetric_limits, save_validated_figure  # noqa: E402


PHASE_CONVENTIONS = (
    "cue_time",
    "top_envelope_35pct",
    "envelope_max",
    "signed_positive_peak",
    "signed_negative_peak",
    "nearest_zero_crossing",
)


def _nearest_index(values: np.ndarray, target: float) -> int:
    return int(np.argmin(np.abs(np.asarray(values, dtype=np.float64) - float(target))))


def _robust_scale(values: np.ndarray) -> float:
    arr = np.asarray(values, dtype=np.float64)
    med = float(np.nanmedian(arr))
    mad = float(np.nanmedian(np.abs(arr - med)))
    scale = 1.4826 * mad
    if not math.isfinite(scale) or scale <= 1.0e-12:
        scale = float(np.nanstd(arr))
    return scale if math.isfinite(scale) and scale > 1.0e-12 else 1.0


def _first_threshold_time(
    time_ns: np.ndarray,
    envelope_trace: np.ndarray,
    window_rows: np.ndarray,
    peak_row: int,
    fraction: float = 0.35,
) -> tuple[float, int]:
    peak = float(envelope_trace[peak_row])
    if not math.isfinite(peak) or peak <= 0.0:
        return float(time_ns[peak_row]), int(peak_row)
    threshold = fraction * peak
    before = window_rows[window_rows <= peak_row]
    above = before[envelope_trace[before] >= threshold]
    if above.size:
        row = int(above[0])
    else:
        row = int(peak_row)
    return float(time_ns[row]), row


def _nearest_zero_crossing_time(
    time_ns: np.ndarray,
    signed_trace: np.ndarray,
    window_rows: np.ndarray,
    reference_row: int,
) -> tuple[float, int]:
    rows = np.asarray(window_rows, dtype=int)
    if rows.size < 2:
        return float(time_ns[reference_row]), int(reference_row)
    values = signed_trace[rows]
    sign = np.sign(values)
    crossing_pairs = []
    for idx in range(rows.size - 1):
        a = sign[idx]
        b = sign[idx + 1]
        if a == 0:
            crossing_pairs.append((abs(int(rows[idx]) - int(reference_row)), int(rows[idx])))
        elif a * b < 0:
            crossing_pairs.append((abs(int(rows[idx]) - int(reference_row)), int(rows[idx])))
    if not crossing_pairs:
        return float(time_ns[reference_row]), int(reference_row)
    _dist, row = min(crossing_pairs, key=lambda item: item[0])
    return float(time_ns[row]), row


def phase_anchor_for_apex(
    record: dict,
    processed: dict[str, np.ndarray],
    x_m: np.ndarray,
    time_ns: np.ndarray,
    apex: dict,
    trace_half_width: int = 3,
    pre_ns: float = 0.24,
    post_ns: float = 0.42,
) -> dict:
    """Measure multiple local phase conventions around one apex cue."""
    trace_index = _nearest_index(x_m, float(apex["x_m"]))
    col0 = max(0, trace_index - trace_half_width)
    col1 = min(x_m.size, trace_index + trace_half_width + 1)
    cue_time = float(apex["time_ns"])
    row0 = int(np.searchsorted(time_ns, max(0.0, cue_time - pre_ns), side="left"))
    row1 = int(np.searchsorted(time_ns, cue_time + post_ns, side="right"))
    row0 = max(0, min(row0, time_ns.size - 1))
    row1 = max(row0 + 1, min(row1, time_ns.size))
    window_rows = np.arange(row0, row1, dtype=int)

    corrected = processed["corrected"]
    envelope_smooth = processed["envelope_smooth"]
    signed_trace = np.nanmedian(corrected[:, col0:col1], axis=1)
    envelope_trace = np.nanmedian(envelope_smooth[:, col0:col1], axis=1)

    peak_row = int(window_rows[np.nanargmax(envelope_trace[window_rows])])
    top_time, top_row = _first_threshold_time(time_ns, envelope_trace, window_rows, peak_row)
    pos_row = int(window_rows[np.nanargmax(signed_trace[window_rows])])
    neg_row = int(window_rows[np.nanargmin(signed_trace[window_rows])])
    zero_time, zero_row = _nearest_zero_crossing_time(time_ns, signed_trace, window_rows, peak_row)
    cue_row = _nearest_index(time_ns, cue_time)

    local_noise_rows = np.arange(
        max(0, row0 - max(6, window_rows.size)),
        row0,
        dtype=int,
    )
    noise_scale = _robust_scale(signed_trace[local_noise_rows]) if local_noise_rows.size else _robust_scale(signed_trace)
    peak_envelope = float(envelope_trace[peak_row])
    local_signed_span = float(np.nanmax(signed_trace[window_rows]) - np.nanmin(signed_trace[window_rows]))
    local_snr = peak_envelope / noise_scale if noise_scale > 0.0 else math.nan
    quality_flag = "usable"
    if not math.isfinite(local_snr) or local_snr < 4.0:
        quality_flag = "low_snr"
    elif abs(float(time_ns[peak_row]) - cue_time) > 0.18:
        quality_flag = "peak_shift_large"

    return {
        "file": record["file"],
        "channel": int(record["channel"]),
        "apex_group": int(apex["apex_group"]),
        "x_m": float(apex["x_m"]),
        "trace_index": int(trace_index),
        "current_cue_time_ns": cue_time,
        "current_cue_sample_index": int(cue_row),
        "top_envelope_35pct_time_ns": top_time,
        "top_envelope_35pct_sample_index": int(top_row),
        "envelope_max_time_ns": float(time_ns[peak_row]),
        "envelope_max_sample_index": int(peak_row),
        "signed_positive_peak_time_ns": float(time_ns[pos_row]),
        "signed_positive_peak_sample_index": int(pos_row),
        "signed_negative_peak_time_ns": float(time_ns[neg_row]),
        "signed_negative_peak_sample_index": int(neg_row),
        "nearest_zero_crossing_time_ns": zero_time,
        "nearest_zero_crossing_sample_index": int(zero_row),
        "local_snr": float(local_snr),
        "local_signed_span": local_signed_span,
        "phase_quality_flag": quality_flag,
        "trace_window_start": int(col0),
        "trace_window_stop_exclusive": int(col1),
        "time_window_start_ns": float(time_ns[row0]),
        "time_window_stop_ns": float(time_ns[row1 - 1]),
    }


def build_convention_apexes(picks: list[dict], convention: str) -> list[dict]:
    if convention == "cue_time":
        time_key = "current_cue_time_ns"
    else:
        time_key = f"{convention}_time_ns"
    out = []
    for pick in picks:
        row = {
            "file": pick["file"],
            "channel": int(pick["channel"]),
            "apex_group": int(pick["apex_group"]),
            "x_m": float(pick["x_m"]),
            "trace_index": int(pick["trace_index"]),
            "time_ns": float(pick[time_key]),
            "sample_index": int(pick.get(f"{convention}_sample_index", pick["current_cue_sample_index"])),
            "relative_strength": float(pick["local_snr"]),
        }
        out.append(row)
    return out


def fit_phase_conventions(
    processed_by_file: dict[str, dict],
    axes_by_file: dict[str, tuple[np.ndarray, np.ndarray]],
    picks_by_file: dict[str, list[dict]],
    velocity_values: np.ndarray,
    time_zero_values: np.ndarray,
    offset_values: np.ndarray,
) -> tuple[list[dict], list[dict], list[dict]]:
    summary_rows: list[dict] = []
    apex_fit_rows: list[dict] = []
    surface_rows: list[dict] = []
    for file_name, picks in sorted(picks_by_file.items()):
        cue_map = processed_by_file[file_name]["cue"]
        x_m, time_ns = axes_by_file[file_name]
        for convention in PHASE_CONVENTIONS:
            apexes = build_convention_apexes(picks, convention)
            best, apex_rows, surface = fit_common_offset_profile(
                cue_map,
                x_m,
                time_ns,
                apexes,
                velocity_values,
                time_zero_values,
                offset_values,
            )
            summary_rows.append(
                {
                    "file": file_name,
                    "phase_convention": convention,
                    "apex_count": len(apex_rows),
                    **best,
                    "calibration_scope": "field_phase_anchor_sensitivity_not_ground_truth",
                }
            )
            for row in apex_rows:
                row["phase_convention"] = convention
            apex_fit_rows.extend(apex_rows)
            for row in surface:
                row["file"] = file_name
                row["phase_convention"] = convention
            surface_rows.extend(surface)
    return summary_rows, apex_fit_rows, surface_rows


def aggregate_convention_summary(summary_rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for row in summary_rows:
        grouped.setdefault(row["phase_convention"], []).append(row)
    out = []
    for convention, rows in sorted(grouped.items()):
        velocities = [float(row["velocity_m_per_ns"]) for row in rows]
        depths = [float(row["median_depth_m"]) for row in rows if math.isfinite(float(row["median_depth_m"]))]
        scores = [float(row["profile_score"]) for row in rows]
        boundary_count = sum(bool(row.get("best_on_grid_boundary")) for row in rows)
        min_depth = min(depths) if depths else math.nan
        max_depth = max(depths) if depths else math.nan
        median_depth = float(np.median(depths)) if depths else math.nan
        velocity_gap = max(velocities) - min(velocities) if velocities else math.nan
        plausible_depth = bool(depths and min_depth >= 0.015 and max_depth <= 0.120)
        no_boundary = boundary_count == 0
        screen_score = float(np.mean(scores))
        # Penalize conventions that keep boundary solutions or implausibly shallow depths.
        decision_score = screen_score - 0.15 * boundary_count - (0.20 if not plausible_depth else 0.0) - 2.0 * velocity_gap
        out.append(
            {
                "phase_convention": convention,
                "profile_count": len(rows),
                "mean_profile_score": screen_score,
                "velocity_gap_m_per_ns": velocity_gap,
                "median_depth_m": median_depth,
                "min_depth_m": min_depth,
                "max_depth_m": max_depth,
                "boundary_solution_count": boundary_count,
                "plausible_depth_15_to_120mm": plausible_depth,
                "no_boundary_solutions": no_boundary,
                "screening_decision_score": decision_score,
            }
        )
    ranked = sorted(out, key=lambda row: float(row["screening_decision_score"]), reverse=True)
    for idx, row in enumerate(ranked, start=1):
        row["screening_rank"] = idx
        row["screening_recommendation"] = "best_phase_hypothesis" if idx == 1 else "comparison"
    return sorted(ranked, key=lambda row: int(row["screening_rank"]))


def phase_quality_flag_counts(picks: list[dict]) -> dict:
    counts = Counter(str(row.get("phase_quality_flag", "unknown")) for row in picks)
    return {key: int(value) for key, value in sorted(counts.items())}


def plot_phase_anchor_panel(
    record: dict,
    processed: dict[str, np.ndarray],
    x_m: np.ndarray,
    time_ns: np.ndarray,
    picks: list[dict],
    save_path: Path,
) -> str:
    corrected = processed["corrected"]
    limits = safe_symmetric_limits(corrected, percentile=99.0, floor=1.0)
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 5.8), constrained_layout=True)
    for ax, zoom in zip(axes, [False, True]):
        img = ax.imshow(
            corrected,
            cmap="seismic",
            aspect="auto",
            extent=imshow_extent(x_m, time_ns),
            vmin=limits[0],
            vmax=limits[1],
            interpolation="nearest",
        )
        for pick in picks:
            x = pick["x_m"]
            markers = [
                ("current_cue_time_ns", "o", "#111111", "cue"),
                ("top_envelope_35pct_time_ns", "^", "#0072b2", "top35"),
                ("envelope_max_time_ns", "s", "#009e73", "envmax"),
                ("signed_positive_peak_time_ns", "+", "#d55e00", "pos"),
                ("signed_negative_peak_time_ns", "x", "#cc79a7", "neg"),
                ("nearest_zero_crossing_time_ns", "d", "#f0e442", "zero"),
            ]
            for key, marker, color, label in markers:
                ax.scatter(
                    [x],
                    [float(pick[key])],
                    marker=marker,
                    s=42,
                    c=color,
                    edgecolors="black" if marker in {"o", "^", "s", "d"} else None,
                    linewidths=0.45,
                    label=label,
                    zorder=5,
                )
            ax.axvline(x, color="black", linewidth=0.35, alpha=0.35)
        if zoom and picks:
            xs = [float(pick["x_m"]) for pick in picks]
            ts = []
            for pick in picks:
                for key in [
                    "current_cue_time_ns",
                    "top_envelope_35pct_time_ns",
                    "envelope_max_time_ns",
                    "signed_positive_peak_time_ns",
                    "signed_negative_peak_time_ns",
                    "nearest_zero_crossing_time_ns",
                ]:
                    ts.append(float(pick[key]))
            ax.set_xlim(max(float(x_m[0]), min(xs) - 0.10), min(float(x_m[-1]), max(xs) + 0.10))
            ax.set_ylim(max(ts) + 0.20, max(0.0, min(ts) - 0.18))
            ax.set_title("phase-anchor zoom")
        elif zoom:
            ax.text(0.5, 0.5, "No phase-anchor picks", transform=ax.transAxes, ha="center", va="center")
            ax.set_title("phase-anchor zoom")
        else:
            ax.set_title("full profile")
        ax.set_xlabel("profile distance [m]")
        ax.set_ylabel("two-way time [ns]")
        ax.grid(color="#d9d9d9", linewidth=0.35, alpha=0.4)
    handles, labels = axes[1].get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    axes[1].legend(by_label.values(), by_label.keys(), frameon=False, fontsize=8, loc="lower right")
    fig.colorbar(img, ax=axes, shrink=0.82, label="amplitude [DZT counts]")
    fig.suptitle(f"{record['file']} phase/time-zero anchor candidates", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def plot_convention_summary(summary_rows: list[dict], aggregate_rows: list[dict], save_path: Path) -> str:
    conventions = [row["phase_convention"] for row in aggregate_rows]
    files = sorted({row["file"] for row in summary_rows})
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.8), constrained_layout=True)
    x = np.arange(len(conventions), dtype=float)
    width = 0.34
    for idx, file_name in enumerate(files):
        rows = {row["phase_convention"]: row for row in summary_rows if row["file"] == file_name}
        offset = (idx - (len(files) - 1) / 2.0) * width
        axes[0].bar(
            x + offset,
            [float(rows[conv]["profile_score"]) for conv in conventions],
            width=width,
            label=Path(file_name).stem,
        )
        axes[1].bar(
            x + offset,
            [float(rows[conv]["velocity_m_per_ns"]) for conv in conventions],
            width=width,
            label=Path(file_name).stem,
        )
        axes[2].bar(
            x + offset,
            [float(rows[conv]["median_depth_m"]) * 1000.0 for conv in conventions],
            width=width,
            label=Path(file_name).stem,
        )
    axes[0].set_title("best template score")
    axes[0].set_ylabel("score")
    axes[1].set_title("best velocity")
    axes[1].set_ylabel("m/ns")
    axes[2].set_title("median depth")
    axes[2].set_ylabel("mm")
    for ax in axes:
        ax.set_xticks(x)
        ax.set_xticklabels(conventions, rotation=35, ha="right")
        ax.grid(axis="y", color="#d9d9d9", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)
    fig.suptitle("Phase convention sensitivity for local GSSI profiles", fontweight="bold")
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


def write_figure_notes(path: Path, panel_paths: dict[str, str], summary_path: str) -> None:
    panels = "\n".join(
        f"- `{Path(fig_path).name}`: signed B-scan with cue, envelope, signed-peak, and zero-crossing anchors."
        for fig_path in panel_paths.values()
    )
    text = f"""# Figure Notes

## Phase Anchor Panels

{panels}

## `{Path(summary_path).name}`

Compares common-offset fit score, velocity, and median fitted depth under each
phase convention. These are calibration hypotheses for measured GSSI field data,
not confirmed rebar detections, cover-depth estimates, or FWI results.
"""
    path.write_text(text, encoding="utf-8")


def write_readme(path: Path, aggregate_rows: list[dict], output_root: Path) -> None:
    best = aggregate_rows[0] if aggregate_rows else {}
    text = f"""# GSSI 51600S Phase Anchor QC

CPU-only phase/time-zero anchoring sensitivity run for selected local GSSI
profiles.

Output root:

```text
{output_root}
```

Best screening phase hypothesis:

```text
phase convention: {best.get('phase_convention', 'none')}
decision score:   {best.get('screening_decision_score', 'n/a')}
median depth:     {float(best.get('median_depth_m', math.nan)) * 1000.0 if best else math.nan:.1f} mm
velocity gap:     {best.get('velocity_gap_m_per_ns', 'n/a')} m/ns
```

This run does not establish ground-truth cover depth or rebar identity. It
selects a phase convention for the next field-to-synthetic comparison candidate.
"""
    path.write_text(text, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--outdir", default=None)
    parser.add_argument("--run-name", default="gssi51600s_phase_anchor_qc")
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--profile-stems", default="PROJECT001C__014,PROJECT001C__016")
    parser.add_argument("--max-anchor-time-ns", type=float, default=1.25)
    parser.add_argument("--max-candidates", type=int, default=28)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    input_dir = Path(args.input_dir)
    requested_stems = {item.strip() for item in args.profile_stems.split(",") if item.strip()}
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    # Keep the phase-convention sweep light enough for interactive CPU use.
    # The earlier common-offset run already established that the useful offset
    # region is near 40-80 mm, while 0 and 100 mm are retained as controls.
    velocity_values = np.linspace(0.080, 0.220, 29)
    time_zero_values = np.linspace(-0.160, 0.280, 45)
    offset_values = np.array([0.0, 0.04, 0.06, 0.08, 0.10], dtype=np.float64)

    processed_by_file: dict[str, dict] = {}
    axes_by_file: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    picks_by_file: dict[str, list[dict]] = {}
    panel_paths: dict[str, str] = {}
    records_by_file: dict[str, dict] = {}
    skipped_profiles: list[dict] = []

    for record, raw in read_dzt_profiles(input_dir):
        if record["stem"] not in requested_stems:
            continue
        processed = preprocess_profile(raw)
        x_m, time_ns = build_axes(record)
        all_candidates = pick_reflector_cues(
            record,
            processed["cue"],
            x_m,
            time_ns,
            max_candidates=args.max_candidates,
            max_time_ns=3.40,
        )
        candidates = [
            cand
            for cand in all_candidates
            if float(cand["time_ns"]) <= float(args.max_anchor_time_ns)
        ]
        apexes = cluster_apex_cues(candidates)
        picks = [
            phase_anchor_for_apex(record, processed, x_m, time_ns, apex)
            for apex in apexes
        ]
        if not picks:
            skipped_profiles.append({
                "file": record["file"],
                "stem": record["stem"],
                "reason": "no_phase_anchor_picks",
                "candidate_count_before_time_filter": len(all_candidates),
                "candidate_count_after_time_filter": len(candidates),
                "max_anchor_time_ns": float(args.max_anchor_time_ns),
            })
            continue
        processed_by_file[record["file"]] = processed
        axes_by_file[record["file"]] = (x_m, time_ns)
        picks_by_file[record["file"]] = picks
        records_by_file[record["file"]] = record
        panel_paths[record["stem"]] = plot_phase_anchor_panel(
            record,
            processed,
            x_m,
            time_ns,
            picks,
            figures_dir / f"{record['stem']}_phase_anchor_panel.png",
        )

    if not picks_by_file:
        raise RuntimeError(
            f"no requested profiles with phase-anchor picks found: {sorted(requested_stems)}"
        )

    pick_rows = [row for rows in picks_by_file.values() for row in rows]
    summary_rows, apex_fit_rows, surface_rows = fit_phase_conventions(
        processed_by_file,
        axes_by_file,
        picks_by_file,
        velocity_values,
        time_zero_values,
        offset_values,
    )
    aggregate_rows = aggregate_convention_summary(summary_rows)

    picks_csv = data_dir / "field_phase_anchor_picks.csv"
    fit_summary_csv = data_dir / "field_phase_convention_fit_summary.csv"
    aggregate_csv = data_dir / "field_phase_convention_aggregate_summary.csv"
    apex_fit_csv = data_dir / "field_phase_convention_apex_fits.csv"
    surface_csv = data_dir / "field_phase_convention_score_surface.csv"
    write_csv(picks_csv, pick_rows)
    write_csv(fit_summary_csv, summary_rows)
    write_csv(aggregate_csv, aggregate_rows)
    write_csv(apex_fit_csv, apex_fit_rows)
    write_csv(surface_csv, surface_rows)

    convention_summary_figure = plot_convention_summary(
        summary_rows,
        aggregate_rows,
        figures_dir / "phase_convention_depth_velocity_summary.png",
    )
    all_figures = list(panel_paths.values()) + [convention_summary_figure]
    validation_rows = validate_figures(all_figures)
    validation_csv = data_dir / "figure_validation.csv"
    write_csv(validation_csv, validation_rows)

    figure_notes = figures_dir / "FIGURE_NOTES.md"
    write_figure_notes(figure_notes, panel_paths, convention_summary_figure)
    write_readme(outdir / "README.md", aggregate_rows, outdir)

    best = aggregate_rows[0] if aggregate_rows else {}
    summary = {
        "run_name": args.run_name,
        "input_dir": str(input_dir),
        "field_root": str(Path(args.field_root)),
        "dataset_id": args.dataset_id,
        "dataset_root": str(dataset_root),
        "outdir": str(outdir),
        "readgssi_version": readgssi_version(),
        "profile_count": len(picks_by_file),
        "requested_profile_count": len(requested_stems),
        "skipped_profiles": skipped_profiles,
        "phase_anchor_pick_count": len(pick_rows),
        "phase_quality_flag_counts": phase_quality_flag_counts(pick_rows),
        "low_snr_phase_anchor_pick_count": phase_quality_flag_counts(pick_rows).get("low_snr", 0),
        "phase_conventions": list(PHASE_CONVENTIONS),
        "best_phase_hypothesis": best,
        "qc_scope": (
            "CPU-only field phase/time-zero anchoring. "
            "No confirmed rebar labeling, no radius estimate, and no FWI."
        ),
        "picks_csv": str(picks_csv),
        "fit_summary_csv": str(fit_summary_csv),
        "aggregate_csv": str(aggregate_csv),
        "apex_fit_csv": str(apex_fit_csv),
        "score_surface_csv": str(surface_csv),
        "figure_validation_csv": str(validation_csv),
        "figures": {
            "phase_anchor_panels": panel_paths,
            "convention_summary": convention_summary_figure,
            "figure_notes": str(figure_notes),
        },
    }
    summary_path = data_dir / "field_phase_anchor_summary.json"
    summary_path.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")

    manifest_path = write_run_manifest(
        str(outdir),
        "gssi51600s_phase_anchor_qc",
        {
            "input_dir": str(input_dir),
            "field_root": str(Path(args.field_root)),
            "dataset_id": args.dataset_id,
            "summary_json": str(summary_path),
            "readgssi_version": readgssi_version(),
        },
    )
    print(f"Wrote phase-anchor field QC: {outdir}")
    print(f"Profiles: {len(picks_by_file)}")
    print(f"Phase anchor picks: {len(pick_rows)}")
    print(f"Best phase hypothesis: {best.get('phase_convention')}")
    print(f"Summary: {summary_path}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()

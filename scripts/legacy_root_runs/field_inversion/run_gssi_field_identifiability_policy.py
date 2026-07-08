#!/usr/bin/env python3
"""Field identifiability policy for local GSSI waveform-family probes."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter, defaultdict
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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def safe_float(value, default=math.nan) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return float(default)
    return out if math.isfinite(out) else float(default)


def read_shift_surface(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            row["synthetic_time_shift_ns"] = safe_float(row.get("synthetic_time_shift_ns"))
            row["absolute_correlation"] = safe_float(row.get("absolute_correlation"))
            row["normalized_correlation"] = safe_float(row.get("normalized_correlation"))
            row["normalized_residual_rms"] = safe_float(row.get("normalized_residual_rms"))
            row["radius_mm"] = safe_float(row.get("radius_mm"))
            row["concrete_epsr"] = safe_float(row.get("concrete_epsr"))
            row["fitted_depth_m"] = safe_float(row.get("fitted_depth_m"))
            row["template_score"] = safe_float(row.get("template_score"))
            if math.isfinite(row["synthetic_time_shift_ns"]) and math.isfinite(row["absolute_correlation"]):
                rows.append(row)
    if not rows:
        raise ValueError(f"no shift-surface rows in {path}")
    return rows


def filter_policy_rows(rows: list[dict], phase: str, shift_ns: float) -> list[dict]:
    accepted = [
        row for row in rows
        if row.get("geometry_valid") in ("True", True)
        and row.get("phase_convention") == phase
        and math.isclose(float(row["synthetic_time_shift_ns"]), float(shift_ns), abs_tol=1.0e-9)
    ]
    if not accepted:
        raise ValueError(f"no valid rows for phase={phase!r} at shift={shift_ns}")
    return accepted


def event_key(row: dict) -> str:
    return "|".join([
        str(row.get("file", "")),
        str(row.get("phase_convention", "")),
        str(row.get("apex_group", "")),
    ])


def event_label(row: dict) -> str:
    stem = Path(str(row.get("file", ""))).stem
    suffix = stem.split("__")[-1] if "__" in stem else stem
    return f"{suffix} g{row.get('apex_group', '')}"


def _best_and_margin(values: dict[str, float]) -> tuple[str, float, str, float, float]:
    if not values:
        return "", math.nan, "", math.nan, math.nan
    ranked = sorted(values.items(), key=lambda item: (-float(item[1]), str(item[0])))
    best_key, best_value = ranked[0]
    second_key, second_value = (ranked[1] if len(ranked) > 1 else ("", math.nan))
    margin = best_value - second_value if math.isfinite(second_value) else math.nan
    return best_key, best_value, second_key, second_value, margin


def summarize_events(rows: list[dict], margin_threshold: float, correlation_floor: float) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[event_key(row)].append(row)
    out: list[dict] = []
    for _key, subset in sorted(grouped.items()):
        ranked = sorted(subset, key=lambda row: (-float(row["absolute_correlation"]), str(row.get("candidate_id", ""))))
        best = ranked[0]
        second = ranked[1] if len(ranked) > 1 else None
        radius_scores: dict[str, float] = {}
        epsr_scores: dict[str, float] = {}
        for row in subset:
            radius_label = f"{float(row['radius_mm']):.3g}"
            epsr_label = str(row.get("epsr_source", ""))
            score = float(row["absolute_correlation"])
            radius_scores[radius_label] = max(radius_scores.get(radius_label, -math.inf), score)
            epsr_scores[epsr_label] = max(epsr_scores.get(epsr_label, -math.inf), score)
        best_radius, best_radius_score, second_radius, second_radius_score, radius_margin = _best_and_margin(radius_scores)
        best_epsr, best_epsr_score, second_epsr, second_epsr_score, epsr_margin = _best_and_margin(epsr_scores)
        top_margin = (
            float(best["absolute_correlation"]) - float(second["absolute_correlation"])
            if second is not None
            else math.nan
        )
        out.append({
            "event_key": event_key(best),
            "event_label": event_label(best),
            "file": best.get("file", ""),
            "phase_convention": best.get("phase_convention", ""),
            "apex_group": best.get("apex_group", ""),
            "candidate_count": len(subset),
            "best_candidate_id": best.get("candidate_id", ""),
            "best_abs_correlation": best.get("absolute_correlation"),
            "second_abs_correlation": second.get("absolute_correlation") if second is not None else math.nan,
            "top_candidate_margin_abs": top_margin,
            "best_radius_mm": safe_float(best_radius),
            "best_radius_abs_correlation": best_radius_score,
            "second_radius_mm": safe_float(second_radius),
            "second_radius_abs_correlation": second_radius_score,
            "radius_margin_abs": radius_margin,
            "radius_margin_clear": bool(math.isfinite(radius_margin) and radius_margin >= margin_threshold),
            "best_epsr_source": best_epsr,
            "best_epsr_abs_correlation": best_epsr_score,
            "second_epsr_source": second_epsr,
            "second_epsr_abs_correlation": second_epsr_score,
            "epsr_margin_abs": epsr_margin,
            "epsr_margin_clear": bool(math.isfinite(epsr_margin) and epsr_margin >= margin_threshold),
            "best_concrete_epsr": best.get("concrete_epsr"),
            "best_fitted_depth_m": best.get("fitted_depth_m"),
            "best_normalized_residual_rms": best.get("normalized_residual_rms"),
            "best_polarity": best.get("polarity", ""),
            "correlation_floor_pass": bool(float(best["absolute_correlation"]) >= correlation_floor),
        })
    return out


def summarize_profiles(event_rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in event_rows:
        grouped[str(row["file"])].append(row)
    out: list[dict] = []
    for file_name, subset in sorted(grouped.items()):
        radius_counts = Counter(float(row["best_radius_mm"]) for row in subset)
        epsr_counts = Counter(str(row["best_epsr_source"]) for row in subset)
        radius_mode, radius_mode_count = radius_counts.most_common(1)[0]
        epsr_mode, epsr_mode_count = epsr_counts.most_common(1)[0]
        margins = [float(row["radius_margin_abs"]) for row in subset if math.isfinite(float(row["radius_margin_abs"]))]
        epsr_margins = [float(row["epsr_margin_abs"]) for row in subset if math.isfinite(float(row["epsr_margin_abs"]))]
        corrs = [float(row["best_abs_correlation"]) for row in subset]
        depths = [1000.0 * float(row["best_fitted_depth_m"]) for row in subset if math.isfinite(float(row["best_fitted_depth_m"]))]
        out.append({
            "file": file_name,
            "event_count": len(subset),
            "mean_best_abs_correlation": float(np.mean(corrs)),
            "min_best_abs_correlation": float(np.min(corrs)),
            "radius_mode_mm": radius_mode,
            "radius_mode_count": radius_mode_count,
            "radius_consensus_fraction": radius_mode_count / len(subset),
            "min_radius_margin_abs": float(np.min(margins)) if margins else math.nan,
            "mean_radius_margin_abs": float(np.mean(margins)) if margins else math.nan,
            "epsr_mode": epsr_mode,
            "epsr_mode_count": epsr_mode_count,
            "epsr_consensus_fraction": epsr_mode_count / len(subset),
            "min_epsr_margin_abs": float(np.min(epsr_margins)) if epsr_margins else math.nan,
            "mean_epsr_margin_abs": float(np.mean(epsr_margins)) if epsr_margins else math.nan,
            "mean_best_depth_mm": float(np.mean(depths)) if depths else math.nan,
            "min_best_depth_mm": float(np.min(depths)) if depths else math.nan,
            "max_best_depth_mm": float(np.max(depths)) if depths else math.nan,
        })
    return out


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


def plot_identifiability_margins(event_rows: list[dict], margin_threshold: float, save_path: Path) -> str:
    rows = sorted(event_rows, key=lambda row: (row["file"], int(float(row["apex_group"]))))
    labels = [row["event_label"] for row in rows]
    x = np.arange(len(rows))
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8), constrained_layout=True)
    axes[0].bar(x, [row["best_abs_correlation"] for row in rows], color="#4c78a8")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    axes[0].set_ylim(0.0, 1.0)
    axes[0].set_ylabel("best |corr|")
    axes[0].set_title("Accepted timing score")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    width = 0.36
    axes[1].bar(x - width / 2, [row["radius_margin_abs"] for row in rows], width=width, label="radius margin")
    axes[1].bar(x + width / 2, [row["epsr_margin_abs"] for row in rows], width=width, label="epsr-source margin")
    axes[1].axhline(margin_threshold, color="#b22222", linestyle="--", linewidth=1.0, label="clear-margin threshold")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    axes[1].set_ylabel("absolute correlation margin")
    axes[1].set_title("Candidate separability")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)
    fig.suptitle("Field waveform identifiability under accepted timing policy", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def plot_candidate_landscape(rows: list[dict], save_path: Path) -> str:
    event_rows = summarize_events(rows, margin_threshold=0.0, correlation_floor=0.0)
    events = sorted(event_rows, key=lambda row: (row["file"], int(float(row["apex_group"]))))
    radii = sorted({float(row["radius_mm"]) for row in rows})
    epsr_sources = sorted({str(row.get("epsr_source", "")) for row in rows})
    fig, axes = plt.subplots(
        len(epsr_sources),
        1,
        figsize=(10.5, max(3.4, 2.6 * len(epsr_sources))),
        constrained_layout=True,
        squeeze=False,
    )
    colors = plt.cm.tab10(np.linspace(0, 1, max(3, len(radii))))
    for ax, epsr_source in zip(axes[:, 0], epsr_sources):
        for color, radius in zip(colors, radii):
            values = []
            for event in events:
                subset = [
                    row for row in rows
                    if event_key(row) == event["event_key"]
                    and str(row.get("epsr_source", "")) == epsr_source
                    and math.isclose(float(row["radius_mm"]), radius, abs_tol=1.0e-9)
                ]
                values.append(float(subset[0]["absolute_correlation"]) if subset else math.nan)
            ax.plot([event["event_label"] for event in events], values, marker="o", label=f"r={radius:g} mm", color=color)
        ax.set_ylim(0.68, 0.92)
        ax.set_ylabel("|corr|")
        ax.set_title(f"epsr source: {epsr_source}")
        ax.grid(axis="y", color="#dddddd", linewidth=0.6)
        ax.legend(frameon=False, fontsize=8)
        ax.tick_params(axis="x", labelrotation=35)
    axes[-1, 0].set_xlabel("field event")
    fig.suptitle("Accepted-timing field candidate landscape", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def build_policy_summary(
    accepted_rows: list[dict],
    event_rows: list[dict],
    profile_rows: list[dict],
    phase: str,
    shift_ns: float,
    margin_threshold: float,
    correlation_floor: float,
) -> dict:
    radius_clear = sum(1 for row in event_rows if row["radius_margin_clear"])
    epsr_clear = sum(1 for row in event_rows if row["epsr_margin_clear"])
    floor_pass = sum(1 for row in event_rows if row["correlation_floor_pass"])
    radius_margins = [float(row["radius_margin_abs"]) for row in event_rows]
    epsr_margins = [float(row["epsr_margin_abs"]) for row in event_rows]
    return {
        "phase_convention": phase,
        "synthetic_time_shift_ns": shift_ns,
        "accepted_candidate_rows": len(accepted_rows),
        "event_count": len(event_rows),
        "profile_count": len(profile_rows),
        "correlation_floor": correlation_floor,
        "correlation_floor_pass_count": floor_pass,
        "margin_threshold": margin_threshold,
        "radius_margin_clear_count": radius_clear,
        "epsr_margin_clear_count": epsr_clear,
        "mean_radius_margin_abs": float(np.mean(radius_margins)) if radius_margins else math.nan,
        "min_radius_margin_abs": float(np.min(radius_margins)) if radius_margins else math.nan,
        "mean_epsr_margin_abs": float(np.mean(epsr_margins)) if epsr_margins else math.nan,
        "min_epsr_margin_abs": float(np.min(epsr_margins)) if epsr_margins else math.nan,
        "profile_summary": profile_rows,
        "interpretation": (
            "The accepted top-envelope timing policy gives coherent waveform matches, "
            "but radius and epsr should remain calibration hypotheses unless their "
            "margins are externally validated."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--probe-dir", default=None)
    parser.add_argument("--phase-convention", default="top_envelope_35pct")
    parser.add_argument("--synthetic-time-shift-ns", type=float, default=0.2)
    parser.add_argument("--margin-threshold", type=float, default=0.02)
    parser.add_argument("--correlation-floor", type=float, default=0.7)
    parser.add_argument("--run-name", default="gssi51600s_field_identifiability_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    probe_dir = (
        Path(args.probe_dir)
        if args.probe_dir is not None
        else dataset_root / "011_gssi51600s_field_synthetic_waveform_family_shift_epsr_probe"
    )
    shift_surface_csv = probe_dir / "data" / "field_synthetic_waveform_shift_surface.csv"
    rows = read_shift_surface(shift_surface_csv)
    accepted_rows = filter_policy_rows(rows, args.phase_convention, args.synthetic_time_shift_ns)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    event_rows = summarize_events(accepted_rows, args.margin_threshold, args.correlation_floor)
    profile_rows = summarize_profiles(event_rows)
    summary = build_policy_summary(
        accepted_rows,
        event_rows,
        profile_rows,
        args.phase_convention,
        args.synthetic_time_shift_ns,
        args.margin_threshold,
        args.correlation_floor,
    )

    accepted_csv = data_dir / "accepted_timing_candidates.csv"
    event_csv = data_dir / "event_identifiability_summary.csv"
    profile_csv = data_dir / "profile_identifiability_summary.csv"
    write_csv(accepted_csv, [json_safe(row) for row in accepted_rows])
    write_csv(event_csv, [json_safe(row) for row in event_rows])
    write_csv(profile_csv, [json_safe(row) for row in profile_rows])

    margins_plot = Path(plot_identifiability_margins(event_rows, args.margin_threshold, figures_dir / "field_identifiability_margins.png"))
    landscape_plot = Path(plot_candidate_landscape(accepted_rows, figures_dir / "field_candidate_landscape.png"))
    validation_rows = [figure_stats(margins_plot), figure_stats(landscape_plot)]
    validation_csv = data_dir / "figure_validation.csv"
    write_csv(validation_csv, validation_rows)

    summary["paths"] = {
        "accepted_timing_candidates_csv": str(accepted_csv),
        "event_identifiability_summary_csv": str(event_csv),
        "profile_identifiability_summary_csv": str(profile_csv),
        "summary_json": str(data_dir / "field_identifiability_policy_summary.json"),
        "margins_plot": str(margins_plot),
        "landscape_plot": str(landscape_plot),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json = data_dir / "field_identifiability_policy_summary.json"
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_identifiability_policy",
        {
            "summary_json": str(summary_json),
            "shift_surface_csv": str(shift_surface_csv),
            "accepted_csv": str(accepted_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

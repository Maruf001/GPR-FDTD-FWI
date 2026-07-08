#!/usr/bin/env python3
"""CPU-only hyperbola-template calibration overlays for local GSSI field profiles."""

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
    C_M_PER_NS,
    DEFAULT_DATASET_ID,
    DEFAULT_FIELD_ROOT,
    DEFAULT_INPUT_DIR,
    _as_float,
    field_dataset_output_root,
    read_dzt_profiles,
    readgssi_version,
)
from run_gssi_field_preprocess_feature_qc import (  # noqa: E402
    build_axes,
    imshow_extent,
    json_safe,
    pick_reflector_cues,
    preprocess_profile,
    write_csv,
)
from visualization.plot_style import safe_symmetric_limits, save_validated_figure  # noqa: E402


def hyperbola_time_ns(
    x_m: np.ndarray,
    x0_m: float,
    apex_time_ns: float,
    velocity_m_per_ns: float,
    time_zero_ns: float = 0.0,
) -> np.ndarray:
    """Zero-offset point-scatterer hyperbola in two-way time, in ns.

    The model is a field-QC approximation. It does not include the unknown
    51600S transmitter/receiver offset or antenna coupling.
    """
    x = np.asarray(x_m, dtype=np.float64)
    tau_apex = float(apex_time_ns) - float(time_zero_ns)
    if velocity_m_per_ns <= 0.0 or tau_apex <= 0.0:
        return np.full_like(x, np.nan, dtype=np.float64)
    return float(time_zero_ns) + np.sqrt(
        tau_apex**2 + (2.0 * (x - float(x0_m)) / float(velocity_m_per_ns)) ** 2
    )


def depth_from_apex_m(
    apex_time_ns: float,
    velocity_m_per_ns: float,
    time_zero_ns: float = 0.0,
) -> float:
    tau_apex = float(apex_time_ns) - float(time_zero_ns)
    if velocity_m_per_ns <= 0.0 or tau_apex <= 0.0:
        return math.nan
    return 0.5 * float(velocity_m_per_ns) * tau_apex


def epsr_from_velocity(velocity_m_per_ns: float) -> float:
    if velocity_m_per_ns <= 0.0:
        return math.nan
    return (C_M_PER_NS / float(velocity_m_per_ns)) ** 2


def interpolate_curve_values(
    image: np.ndarray,
    time_ns: np.ndarray,
    curve_time_ns: np.ndarray,
    columns: np.ndarray,
) -> np.ndarray:
    values = np.full(columns.size, np.nan, dtype=np.float64)
    for out_idx, col in enumerate(columns):
        values[out_idx] = np.interp(
            curve_time_ns[col],
            time_ns,
            image[:, col],
            left=np.nan,
            right=np.nan,
        )
    return values


def score_hyperbola_template(
    cue_map: np.ndarray,
    x_m: np.ndarray,
    time_ns: np.ndarray,
    x0_m: float,
    apex_time_ns: float,
    velocity_m_per_ns: float,
    time_zero_ns: float,
    half_width_m: float = 0.18,
) -> tuple[float, float]:
    x = np.asarray(x_m, dtype=np.float64)
    columns = np.flatnonzero(np.abs(x - float(x0_m)) <= float(half_width_m))
    if columns.size < 12:
        return math.nan, 0.0
    curve = hyperbola_time_ns(x, x0_m, apex_time_ns, velocity_m_per_ns, time_zero_ns)
    values = interpolate_curve_values(cue_map, time_ns, curve, columns)
    finite = np.isfinite(values)
    support_fraction = float(np.mean(finite)) if values.size else 0.0
    if np.count_nonzero(finite) < max(8, int(0.45 * values.size)):
        return math.nan, support_fraction
    return float(np.nanmean(values[finite])), support_fraction


def cluster_apex_cues(candidates: list[dict], x_cluster_m: float = 0.04) -> list[dict]:
    """Collapse multiple time picks at the same lateral feature into one apex cue."""
    if not candidates:
        return []
    ordered = sorted(candidates, key=lambda row: float(row["x_m"]))
    groups: list[list[dict]] = []
    for cand in ordered:
        if not groups or abs(float(cand["x_m"]) - float(groups[-1][-1]["x_m"])) > x_cluster_m:
            groups.append([cand])
        else:
            groups[-1].append(cand)

    apexes = []
    for idx, group in enumerate(groups, start=1):
        # The earliest strong local maximum is the apex cue. Later maxima at the
        # same x are treated as ringing/multiple-reflection candidates.
        selected = sorted(
            group,
            key=lambda row: (float(row["time_ns"]), -float(row["relative_strength"])),
        )[0]
        apex = dict(selected)
        apex["apex_group"] = idx
        apex["group_size"] = len(group)
        apex["apex_policy"] = "earliest_high_envelope_maximum_in_x_cluster"
        apexes.append(apex)
    return apexes


def fit_profile_grid(
    cue_map: np.ndarray,
    x_m: np.ndarray,
    time_ns: np.ndarray,
    apexes: list[dict],
    velocity_values: np.ndarray,
    time_zero_values: np.ndarray,
    half_width_m: float = 0.18,
) -> tuple[dict, list[dict], list[dict]]:
    """Fit one shared velocity/time-zero pair to all apex cues in a profile."""
    surface_rows: list[dict] = []
    per_cue_rows: list[dict] = []
    best_surface = {
        "score": -math.inf,
        "velocity_m_per_ns": math.nan,
        "time_zero_ns": math.nan,
        "support_fraction": math.nan,
    }

    for velocity in velocity_values:
        for time_zero in time_zero_values:
            cue_scores = []
            cue_supports = []
            for cue in apexes:
                score, support = score_hyperbola_template(
                    cue_map,
                    x_m,
                    time_ns,
                    float(cue["x_m"]),
                    float(cue["time_ns"]),
                    float(velocity),
                    float(time_zero),
                    half_width_m=half_width_m,
                )
                if math.isfinite(score):
                    cue_scores.append(score)
                    cue_supports.append(support)
            profile_score = float(np.mean(cue_scores)) if cue_scores else math.nan
            support_fraction = float(np.mean(cue_supports)) if cue_supports else 0.0
            row = {
                "velocity_m_per_ns": float(velocity),
                "time_zero_ns": float(time_zero),
                "epsr": epsr_from_velocity(float(velocity)),
                "profile_score": profile_score,
                "mean_support_fraction": support_fraction,
                "valid_cue_count": len(cue_scores),
            }
            surface_rows.append(row)
            if math.isfinite(profile_score) and profile_score > best_surface["score"]:
                best_surface = {
                    "score": profile_score,
                    "velocity_m_per_ns": float(velocity),
                    "time_zero_ns": float(time_zero),
                    "support_fraction": support_fraction,
                }

    finite_scores = np.array(
        [row["profile_score"] for row in surface_rows if math.isfinite(row["profile_score"])],
        dtype=np.float64,
    )
    p95 = float(np.percentile(finite_scores, 95.0)) if finite_scores.size else math.nan
    best_surface["score_margin_vs_p95"] = best_surface["score"] - p95 if math.isfinite(p95) else math.nan
    best_surface["epsr"] = epsr_from_velocity(best_surface["velocity_m_per_ns"])
    best_surface["best_on_grid_boundary"] = bool(
        np.isclose(best_surface["velocity_m_per_ns"], np.min(velocity_values))
        or np.isclose(best_surface["velocity_m_per_ns"], np.max(velocity_values))
        or np.isclose(best_surface["time_zero_ns"], np.min(time_zero_values))
        or np.isclose(best_surface["time_zero_ns"], np.max(time_zero_values))
    )

    for cue in apexes:
        score, support = score_hyperbola_template(
            cue_map,
            x_m,
            time_ns,
            float(cue["x_m"]),
            float(cue["time_ns"]),
            best_surface["velocity_m_per_ns"],
            best_surface["time_zero_ns"],
            half_width_m=half_width_m,
        )
        per_cue_rows.append(
            {
                "file": cue["file"],
                "channel": int(cue["channel"]),
                "apex_group": int(cue["apex_group"]),
                "group_size": int(cue["group_size"]),
                "x_m": float(cue["x_m"]),
                "trace_index": int(cue["trace_index"]),
                "apex_time_ns": float(cue["time_ns"]),
                "sample_index": int(cue["sample_index"]),
                "relative_strength": float(cue["relative_strength"]),
                "fitted_velocity_m_per_ns": best_surface["velocity_m_per_ns"],
                "fitted_epsr": best_surface["epsr"],
                "fitted_time_zero_ns": best_surface["time_zero_ns"],
                "fitted_depth_m": depth_from_apex_m(
                    float(cue["time_ns"]),
                    best_surface["velocity_m_per_ns"],
                    best_surface["time_zero_ns"],
                ),
                "template_score": score,
                "support_fraction": support,
                "calibration_scope": "field_template_overlay_not_ground_truth",
            }
        )
    return best_surface, per_cue_rows, surface_rows


def profile_summary_row(file_name: str, per_cue_rows: list[dict], best: dict) -> dict:
    depths = np.array([row["fitted_depth_m"] for row in per_cue_rows], dtype=np.float64)
    x_vals = np.array([row["x_m"] for row in per_cue_rows], dtype=np.float64)
    spacings = np.diff(np.sort(x_vals)) if x_vals.size >= 2 else np.array([], dtype=np.float64)
    return {
        "file": file_name,
        "apex_cue_count": len(per_cue_rows),
        "best_velocity_m_per_ns": best["velocity_m_per_ns"],
        "best_epsr": best["epsr"],
        "best_time_zero_ns": best["time_zero_ns"],
        "profile_score": best["score"],
        "score_margin_vs_p95": best["score_margin_vs_p95"],
        "best_on_grid_boundary": best["best_on_grid_boundary"],
        "mean_support_fraction": best["support_fraction"],
        "median_depth_m": float(np.nanmedian(depths)) if depths.size else None,
        "min_depth_m": float(np.nanmin(depths)) if depths.size else None,
        "max_depth_m": float(np.nanmax(depths)) if depths.size else None,
        "median_apex_spacing_m": float(np.nanmedian(spacings)) if spacings.size else None,
        "calibration_scope": "field_template_overlay_not_ground_truth",
    }


def plot_profile_overlay(
    record: dict,
    processed: dict,
    x_m: np.ndarray,
    time_ns: np.ndarray,
    per_cue_rows: list[dict],
    save_path: Path,
) -> str:
    corrected = processed["corrected"]
    limits = safe_symmetric_limits(corrected, percentile=99.0, floor=1.0)
    fig, ax = plt.subplots(figsize=(11.5, 5.8), constrained_layout=True)
    img = ax.imshow(
        corrected,
        cmap="seismic",
        aspect="auto",
        extent=imshow_extent(x_m, time_ns),
        vmin=limits[0],
        vmax=limits[1],
        interpolation="nearest",
    )
    fig.colorbar(img, ax=ax, shrink=0.86, label="amplitude [DZT counts]")
    colors = ["#ffdd55", "#44aa99", "#cc6677", "#88ccee", "#aa4499"]
    for idx, row in enumerate(per_cue_rows):
        curve = hyperbola_time_ns(
            x_m,
            row["x_m"],
            row["apex_time_ns"],
            row["fitted_velocity_m_per_ns"],
            row["fitted_time_zero_ns"],
        )
        mask = np.abs(x_m - row["x_m"]) <= 0.20
        color = colors[idx % len(colors)]
        ax.plot(x_m[mask], curve[mask], color=color, linewidth=1.8)
        ax.scatter(
            [row["x_m"]],
            [row["apex_time_ns"]],
            s=58,
            facecolors="none",
            edgecolors=color,
            linewidths=1.6,
            zorder=4,
        )
        ax.text(
            row["x_m"],
            row["apex_time_ns"] + 0.14,
            f"{row['fitted_depth_m']*1000:.0f} mm",
            color="black",
            fontsize=8,
            ha="center",
            va="bottom",
            bbox={"facecolor": "white", "alpha": 0.72, "edgecolor": "none", "pad": 1.5},
        )
    if per_cue_rows:
        first = per_cue_rows[0]
        subtitle = (
            f"v={first['fitted_velocity_m_per_ns']:.3f} m/ns, "
            f"epsr={first['fitted_epsr']:.2f}, "
            f"time-zero={first['fitted_time_zero_ns']:.2f} ns"
        )
    else:
        subtitle = "no fitted apex cues"
    ax.set_title(f"{record['file']} hyperbola-template overlay\n{subtitle}")
    ax.set_xlabel("profile distance [m]")
    ax.set_ylabel("two-way time [ns]")
    ax.grid(color="#d9d9d9", linewidth=0.4, alpha=0.45)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def plot_score_surface(
    file_name: str,
    surface_rows: list[dict],
    best: dict,
    save_path: Path,
) -> str:
    velocities = sorted({row["velocity_m_per_ns"] for row in surface_rows})
    zeros = sorted({row["time_zero_ns"] for row in surface_rows})
    matrix = np.full((len(zeros), len(velocities)), np.nan, dtype=np.float64)
    for row in surface_rows:
        i = zeros.index(row["time_zero_ns"])
        j = velocities.index(row["velocity_m_per_ns"])
        matrix[i, j] = row["profile_score"]
    fig, ax = plt.subplots(figsize=(8.2, 5.8), constrained_layout=True)
    image = ax.imshow(
        matrix,
        origin="lower",
        aspect="auto",
        extent=[min(velocities), max(velocities), min(zeros), max(zeros)],
        cmap="viridis",
    )
    ax.scatter(
        [best["velocity_m_per_ns"]],
        [best["time_zero_ns"]],
        marker="x",
        s=85,
        color="white",
        linewidths=2.0,
        label="best grid point",
    )
    ax.set_xlabel("template velocity [m/ns]")
    ax.set_ylabel("time-zero offset [ns]")
    ax.set_title(f"{file_name} profile-level hyperbola score surface")
    ax.legend(frameon=True, loc="upper right")
    fig.colorbar(image, ax=ax, label="mean cue-map score")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def plot_calibration_summary(summary_rows: list[dict], save_path: Path) -> str:
    labels = [Path(row["file"]).stem for row in summary_rows]
    x = np.arange(len(summary_rows))
    velocities = [row["best_velocity_m_per_ns"] for row in summary_rows]
    epsr = [row["best_epsr"] for row in summary_rows]
    depths_mm = [row["median_depth_m"] * 1000.0 for row in summary_rows]
    spacings_mm = [
        math.nan if row["median_apex_spacing_m"] is None else row["median_apex_spacing_m"] * 1000.0
        for row in summary_rows
    ]

    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.2), constrained_layout=True)
    axes[0, 0].bar(x, velocities, color="#4c78a8")
    axes[0, 0].axhline(C_M_PER_NS / math.sqrt(2.25), color="black", linestyle="--", linewidth=1.1)
    axes[0, 0].set_title("Best template velocity")
    axes[0, 0].set_ylabel("m/ns")

    axes[0, 1].bar(x, epsr, color="#dd8452")
    axes[0, 1].axhline(2.25, color="black", linestyle="--", linewidth=1.1)
    axes[0, 1].set_title("Implied dielectric constant")
    axes[0, 1].set_ylabel("epsr")

    axes[1, 0].bar(x, depths_mm, color="#55a868")
    axes[1, 0].set_title("Median fitted display depth")
    axes[1, 0].set_ylabel("mm")

    axes[1, 1].bar(x, spacings_mm, color="#c44e52")
    axes[1, 1].set_title("Median lateral cue spacing")
    axes[1, 1].set_ylabel("mm")

    for ax in axes.ravel():
        ax.set_xticks(x, labels=labels, rotation=20, ha="right")
        ax.grid(axis="y", color="#d9d9d9", linewidth=0.6)
    fig.suptitle("Short-profile field hyperbola calibration summary", fontweight="bold")
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


def write_readme(path: Path, input_dir: Path, summary_rows: list[dict]) -> None:
    rows = "\n".join(
        f"- `{row['file']}`: v={row['best_velocity_m_per_ns']:.3f} m/ns, "
        f"epsr={row['best_epsr']:.2f}, median depth={row['median_depth_m']*1000:.1f} mm, "
        f"boundary warning={bool(row['best_on_grid_boundary'])}"
        for row in summary_rows
    )
    text = f"""# GSSI 51600S Hyperbola Calibration QC

CPU-only field-data calibration run for:

```text
{input_dir}
```

This run fits simple zero-offset hyperbola templates to the short profiles
`PROJECT001C__014.DZT` and `PROJECT001C__016.DZT`. The fitted velocity,
time-zero, dielectric, and depth values are calibration hypotheses for visual
quality control. They are not ground-truth cover measurements and not
full-waveform inversion outputs.

Profile summaries:

{rows}

Boundary warning means the best grid point lies on the edge of the searched
velocity/time-zero grid. In that case, the overlay can still be visually useful,
but the fitted velocity, dielectric, and depth should not be treated as stable
calibration values.
"""
    path.write_text(text, encoding="utf-8")


def write_figure_notes(path: Path, overlay_paths: dict[str, str], surface_paths: dict[str, str]) -> None:
    overlay_lines = "\n".join(
        f"- `{Path(path_str).name}`: median-background-removed B-scan with fitted "
        f"hyperbola templates and approximate display-depth labels."
        for path_str in overlay_paths.values()
    )
    surface_lines = "\n".join(
        f"- `{Path(path_str).name}`: velocity/time-zero score surface; a sharp peak "
        f"would support a more stable calibration than a broad plateau."
        for path_str in surface_paths.values()
    )
    text = f"""# Figure Notes

## `field_hyperbola_calibration_summary.png`

Summary chart for the two short GSSI 51600S profiles. Dashed reference lines
show the metadata dielectric value of 2.25 and its corresponding velocity.
These are not ground-truth values; they are context for the fitted templates.

## Hyperbola Overlay Figures

{overlay_lines}

The overlays use a simple zero-offset point-scatterer formula. They are useful
for visual calibration and velocity/time-zero triage, but they do not include
the actual 51600S transmitter/receiver offset or antenna coupling.

The current fits prefer the lower time-zero grid boundary, so the velocity and
depth numbers should be read as overlay hypotheses rather than calibrated cover
measurements.

## Score Surfaces

{surface_lines}

Ground-penetrating radar (GPR) B-scans are profile images with profile distance
on the horizontal axis and two-way travel time on the vertical axis.
"""
    path.write_text(text, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR, help="Directory containing GSSI .DZT files")
    parser.add_argument("--outdir", default=None, help="Optional explicit output directory")
    parser.add_argument(
        "--run-name",
        default="gssi51600s_hyperbola_calibration_qc",
        help="Run name for numbered output allocation",
    )
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument(
        "--profile-stems",
        default="PROJECT001C__014,PROJECT001C__016",
        help="Comma-separated DZT stems to fit",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    input_dir = Path(args.input_dir)
    if not input_dir.is_dir():
        raise FileNotFoundError(f"input directory does not exist: {input_dir}")

    requested_stems = {item.strip() for item in args.profile_stems.split(",") if item.strip()}
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    velocity_values = np.linspace(0.080, 0.220, 71)
    time_zero_values = np.linspace(-0.050, 0.250, 61)

    summary_rows: list[dict] = []
    apex_rows: list[dict] = []
    surface_rows_all: list[dict] = []
    overlay_paths: dict[str, str] = {}
    surface_paths: dict[str, str] = {}

    for record, raw in read_dzt_profiles(input_dir):
        if record["stem"] not in requested_stems:
            continue
        processed = preprocess_profile(raw)
        x_m, time_ns = build_axes(record)
        candidates_all = pick_reflector_cues(
            record,
            processed["cue"],
            x_m,
            time_ns,
            max_candidates=28,
            max_time_ns=3.40,
        )
        candidates = [cand for cand in candidates_all if float(cand["time_ns"]) <= 1.25]
        apexes = cluster_apex_cues(candidates)
        best, per_cue_rows, surface_rows = fit_profile_grid(
            processed["cue"],
            x_m,
            time_ns,
            apexes,
            velocity_values,
            time_zero_values,
        )
        for row in surface_rows:
            row["file"] = record["file"]
        surface_rows_all.extend(surface_rows)
        apex_rows.extend(per_cue_rows)
        summary_rows.append(profile_summary_row(record["file"], per_cue_rows, best))

        overlay_paths[record["stem"]] = plot_profile_overlay(
            record,
            processed,
            x_m,
            time_ns,
            per_cue_rows,
            figures_dir / f"{record['stem']}_hyperbola_overlay.png",
        )
        surface_paths[record["stem"]] = plot_score_surface(
            record["file"],
            surface_rows,
            best,
            figures_dir / f"{record['stem']}_score_surface.png",
        )

    if not summary_rows:
        raise RuntimeError(f"no requested profiles found: {sorted(requested_stems)}")

    summary_csv = data_dir / "field_hyperbola_calibration_summary.csv"
    apex_csv = data_dir / "field_hyperbola_apex_fits.csv"
    surface_csv = data_dir / "field_hyperbola_score_surface.csv"
    write_csv(summary_csv, summary_rows)
    write_csv(apex_csv, apex_rows)
    write_csv(surface_csv, surface_rows_all)

    summary_figure = plot_calibration_summary(
        summary_rows,
        figures_dir / "field_hyperbola_calibration_summary.png",
    )
    all_figures = [summary_figure] + list(overlay_paths.values()) + list(surface_paths.values())
    validation_rows = validate_figures(all_figures)
    figure_validation_csv = data_dir / "figure_validation.csv"
    write_csv(figure_validation_csv, validation_rows)

    figure_notes = figures_dir / "FIGURE_NOTES.md"
    write_figure_notes(figure_notes, overlay_paths, surface_paths)
    write_readme(outdir / "README.md", input_dir, summary_rows)

    summary_json = {
        "run_name": args.run_name,
        "input_dir": str(input_dir),
        "field_root": str(Path(args.field_root)),
        "dataset_id": args.dataset_id,
        "dataset_root": str(dataset_root),
        "outdir": str(outdir),
        "readgssi_version": readgssi_version(),
        "profile_count": len(summary_rows),
        "apex_fit_count": len(apex_rows),
        "qc_scope": (
            "CPU-only hyperbola-template overlay calibration. "
            "No confirmed rebar labeling, no radius estimate, and no FWI."
        ),
        "summary_csv": str(summary_csv),
        "apex_csv": str(apex_csv),
        "surface_csv": str(surface_csv),
        "figure_validation_csv": str(figure_validation_csv),
        "figures": {
            "summary": summary_figure,
            "overlays": overlay_paths,
            "score_surfaces": surface_paths,
            "figure_notes": str(figure_notes),
        },
    }
    summary_json_path = data_dir / "field_hyperbola_calibration_summary.json"
    summary_json_path.write_text(json.dumps(json_safe(summary_json), indent=2) + "\n", encoding="utf-8")

    manifest_path = write_run_manifest(
        str(outdir),
        "gssi51600s_hyperbola_calibration_qc",
        {
            "input_dir": str(input_dir),
            "field_root": str(Path(args.field_root)),
            "dataset_id": args.dataset_id,
            "summary_json": str(summary_json_path),
            "summary_csv": str(summary_csv),
            "apex_csv": str(apex_csv),
            "figure_notes": str(figure_notes),
            "readgssi_version": readgssi_version(),
        },
    )

    print(f"Wrote field hyperbola calibration QC: {outdir}")
    print(f"Profiles: {len(summary_rows)}")
    print(f"Apex fits: {len(apex_rows)}")
    print(f"Summary: {summary_json_path}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()

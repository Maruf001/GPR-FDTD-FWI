#!/usr/bin/env python3
"""Common-offset hyperbola sensitivity sweep for local GSSI short profiles."""

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
    field_dataset_output_root,
    read_dzt_profiles,
    readgssi_version,
)
from run_gssi_field_hyperbola_calibration import (  # noqa: E402
    cluster_apex_cues,
    epsr_from_velocity,
    interpolate_curve_values,
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


def common_offset_hyperbola_time_ns(
    x_m: np.ndarray,
    x0_m: float,
    apex_time_ns: float,
    velocity_m_per_ns: float,
    time_zero_ns: float,
    tx_rx_offset_m: float,
) -> tuple[np.ndarray, float]:
    """Common-offset hyperbola and inferred depth.

    The trace x-coordinate is treated as the antenna midpoint. This is a QC
    model for sensitivity analysis, not a confirmed instrument geometry.
    """
    x = np.asarray(x_m, dtype=np.float64)
    velocity = float(velocity_m_per_ns)
    tau_apex = float(apex_time_ns) - float(time_zero_ns)
    half_offset = 0.5 * float(tx_rx_offset_m)
    if velocity <= 0.0 or tau_apex <= 0.0 or tx_rx_offset_m < 0.0:
        return np.full_like(x, np.nan), math.nan
    half_path = 0.5 * velocity * tau_apex
    if half_path <= half_offset:
        return np.full_like(x, np.nan), math.nan
    depth = math.sqrt(half_path**2 - half_offset**2)
    tx_dx = x - float(x0_m) - half_offset
    rx_dx = x - float(x0_m) + half_offset
    curve = (
        float(time_zero_ns)
        + (np.sqrt(tx_dx**2 + depth**2) + np.sqrt(rx_dx**2 + depth**2)) / velocity
    )
    return curve, depth


def score_common_offset_template(
    cue_map: np.ndarray,
    x_m: np.ndarray,
    time_ns: np.ndarray,
    cue: dict,
    velocity_m_per_ns: float,
    time_zero_ns: float,
    tx_rx_offset_m: float,
    half_width_m: float = 0.20,
) -> tuple[float, float, float]:
    x = np.asarray(x_m, dtype=np.float64)
    columns = np.flatnonzero(np.abs(x - float(cue["x_m"])) <= float(half_width_m))
    if columns.size < 12:
        return math.nan, 0.0, math.nan
    curve, depth = common_offset_hyperbola_time_ns(
        x,
        float(cue["x_m"]),
        float(cue["time_ns"]),
        float(velocity_m_per_ns),
        float(time_zero_ns),
        float(tx_rx_offset_m),
    )
    if not math.isfinite(depth):
        return math.nan, 0.0, math.nan
    values = interpolate_curve_values(cue_map, time_ns, curve, columns)
    finite = np.isfinite(values)
    support = float(np.mean(finite)) if finite.size else 0.0
    if np.count_nonzero(finite) < max(8, int(0.45 * values.size)):
        return math.nan, support, depth
    return float(np.nanmean(values[finite])), support, depth


def fit_common_offset_profile(
    cue_map: np.ndarray,
    x_m: np.ndarray,
    time_ns: np.ndarray,
    apexes: list[dict],
    velocity_values: np.ndarray,
    time_zero_values: np.ndarray,
    offset_values: np.ndarray,
) -> tuple[dict, list[dict], list[dict]]:
    rows: list[dict] = []
    best = {"profile_score": -math.inf}
    for offset in offset_values:
        for velocity in velocity_values:
            for time_zero in time_zero_values:
                scores = []
                supports = []
                depths = []
                for cue in apexes:
                    score, support, depth = score_common_offset_template(
                        cue_map,
                        x_m,
                        time_ns,
                        cue,
                        float(velocity),
                        float(time_zero),
                        float(offset),
                    )
                    if math.isfinite(score):
                        scores.append(score)
                        supports.append(support)
                        depths.append(depth)
                row = {
                    "tx_rx_offset_m": float(offset),
                    "tx_rx_offset_mm": float(offset) * 1000.0,
                    "velocity_m_per_ns": float(velocity),
                    "time_zero_ns": float(time_zero),
                    "epsr": epsr_from_velocity(float(velocity)),
                    "profile_score": float(np.mean(scores)) if scores else math.nan,
                    "mean_support_fraction": float(np.mean(supports)) if supports else 0.0,
                    "median_depth_m": float(np.median(depths)) if depths else math.nan,
                    "valid_cue_count": len(scores),
                }
                rows.append(row)
                if math.isfinite(row["profile_score"]) and row["profile_score"] > best["profile_score"]:
                    best = dict(row)
    best["best_on_grid_boundary"] = bool(
        np.isclose(best["tx_rx_offset_m"], np.min(offset_values))
        or np.isclose(best["tx_rx_offset_m"], np.max(offset_values))
        or np.isclose(best["velocity_m_per_ns"], np.min(velocity_values))
        or np.isclose(best["velocity_m_per_ns"], np.max(velocity_values))
        or np.isclose(best["time_zero_ns"], np.min(time_zero_values))
        or np.isclose(best["time_zero_ns"], np.max(time_zero_values))
    )

    apex_rows = []
    for cue in apexes:
        score, support, depth = score_common_offset_template(
            cue_map,
            x_m,
            time_ns,
            cue,
            best["velocity_m_per_ns"],
            best["time_zero_ns"],
            best["tx_rx_offset_m"],
        )
        apex_rows.append(
            {
                "file": cue["file"],
                "channel": int(cue["channel"]),
                "apex_group": int(cue["apex_group"]),
                "x_m": float(cue["x_m"]),
                "apex_time_ns": float(cue["time_ns"]),
                "relative_strength": float(cue["relative_strength"]),
                "tx_rx_offset_mm": best["tx_rx_offset_mm"],
                "fitted_velocity_m_per_ns": best["velocity_m_per_ns"],
                "fitted_epsr": best["epsr"],
                "fitted_time_zero_ns": best["time_zero_ns"],
                "fitted_depth_m": depth,
                "template_score": score,
                "support_fraction": support,
                "calibration_scope": "field_common_offset_sensitivity_not_ground_truth",
            }
        )
    return best, apex_rows, rows


def summarize_best_by_offset(file_name: str, rows: list[dict]) -> list[dict]:
    out = []
    offsets = sorted({row["tx_rx_offset_mm"] for row in rows})
    for offset_mm in offsets:
        subset = [row for row in rows if row["tx_rx_offset_mm"] == offset_mm and math.isfinite(row["profile_score"])]
        if not subset:
            continue
        best = max(subset, key=lambda row: row["profile_score"])
        out.append({"file": file_name, **best})
    return out


def plot_offset_sensitivity(rows_by_offset: list[dict], save_path: Path) -> str:
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.8), constrained_layout=True)
    for file_name in sorted({row["file"] for row in rows_by_offset}):
        subset = [row for row in rows_by_offset if row["file"] == file_name]
        subset = sorted(subset, key=lambda row: row["tx_rx_offset_mm"])
        label = Path(file_name).stem
        offsets = [row["tx_rx_offset_mm"] for row in subset]
        axes[0].plot(offsets, [row["profile_score"] for row in subset], marker="o", label=label)
        axes[1].plot(offsets, [row["velocity_m_per_ns"] for row in subset], marker="o", label=label)
        axes[2].plot(offsets, [row["median_depth_m"] * 1000.0 for row in subset], marker="o", label=label)
    axes[0].set_ylabel("best score at offset")
    axes[0].set_title("Template score")
    axes[1].set_ylabel("m/ns")
    axes[1].set_title("Best velocity")
    axes[2].set_ylabel("mm")
    axes[2].set_title("Median fitted depth")
    for ax in axes:
        ax.set_xlabel("assumed Tx/Rx offset [mm]")
        ax.grid(color="#d9d9d9", linewidth=0.6)
        ax.legend(frameon=False, fontsize=8)
    fig.suptitle("Common-offset hyperbola sensitivity", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def plot_common_offset_overlay(
    record: dict,
    processed: dict,
    x_m: np.ndarray,
    time_ns: np.ndarray,
    apex_rows: list[dict],
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
    for idx, row in enumerate(apex_rows):
        curve, _depth = common_offset_hyperbola_time_ns(
            x_m,
            row["x_m"],
            row["apex_time_ns"],
            row["fitted_velocity_m_per_ns"],
            row["fitted_time_zero_ns"],
            row["tx_rx_offset_mm"] / 1000.0,
        )
        mask = np.abs(x_m - row["x_m"]) <= 0.22
        color = colors[idx % len(colors)]
        ax.plot(x_m[mask], curve[mask], color=color, linewidth=1.8)
        ax.scatter([row["x_m"]], [row["apex_time_ns"]], s=58, facecolors="none",
                   edgecolors=color, linewidths=1.6, zorder=4)
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
    if apex_rows:
        first = apex_rows[0]
        subtitle = (
            f"offset={first['tx_rx_offset_mm']:.0f} mm, "
            f"v={first['fitted_velocity_m_per_ns']:.3f} m/ns, "
            f"epsr={first['fitted_epsr']:.2f}, "
            f"time-zero={first['fitted_time_zero_ns']:.2f} ns"
        )
    else:
        subtitle = "no fitted apex cues"
    ax.set_title(f"{record['file']} common-offset overlay\n{subtitle}")
    ax.set_xlabel("profile distance [m]")
    ax.set_ylabel("two-way time [ns]")
    ax.grid(color="#d9d9d9", linewidth=0.4, alpha=0.45)
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


def write_readme(path: Path, input_dir: Path, profile_rows: list[dict]) -> None:
    lines = "\n".join(
        f"- `{row['file']}`: offset={row['tx_rx_offset_mm']:.0f} mm, "
        f"v={row['velocity_m_per_ns']:.3f} m/ns, epsr={row['epsr']:.2f}, "
        f"median depth={row['median_depth_m']*1000:.1f} mm, "
        f"boundary warning={bool(row['best_on_grid_boundary'])}"
        for row in profile_rows
    )
    text = f"""# GSSI 51600S Common-Offset Hyperbola Sweep

CPU-only field-data sensitivity run for:

```text
{input_dir}
```

This run sweeps effective transmitter/receiver offset values from 0 to 120 mm
for the short profiles 014 and 016. It is a model-sensitivity check, not a
confirmed instrument calibration.

Best profile fits:

{lines}
"""
    path.write_text(text, encoding="utf-8")


def write_figure_notes(path: Path, overlay_paths: dict[str, str]) -> None:
    overlays = "\n".join(
        f"- `{Path(path_str).name}`: common-offset hyperbola overlays for one short profile."
        for path_str in overlay_paths.values()
    )
    text = f"""# Figure Notes

## `common_offset_sensitivity.png`

Shows how the best template score, fitted velocity, and median display depth
change as the assumed Tx/Rx offset changes from 0 to 120 mm. A stable
calibration would show a clear preferred offset and consistent velocity across
profiles.

## Common-Offset Overlays

{overlays}

These overlays are calibration hypotheses for measured GSSI field data. They
are not confirmed rebar detections or full-waveform inversion results.
"""
    path.write_text(text, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--outdir", default=None)
    parser.add_argument("--run-name", default="gssi51600s_common_offset_sweep")
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--profile-stems", default="PROJECT001C__014,PROJECT001C__016")
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

    velocity_values = np.linspace(0.080, 0.220, 57)
    time_zero_values = np.linspace(-0.050, 0.250, 41)
    offset_values = np.array([0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12], dtype=np.float64)

    profile_rows: list[dict] = []
    apex_rows_all: list[dict] = []
    surface_rows_all: list[dict] = []
    offset_rows_all: list[dict] = []
    overlay_paths: dict[str, str] = {}

    for record, raw in read_dzt_profiles(input_dir):
        if record["stem"] not in requested_stems:
            continue
        processed = preprocess_profile(raw)
        x_m, time_ns = build_axes(record)
        candidates = [
            cand for cand in pick_reflector_cues(
                record,
                processed["cue"],
                x_m,
                time_ns,
                max_candidates=28,
                max_time_ns=3.40,
            )
            if float(cand["time_ns"]) <= 1.25
        ]
        apexes = cluster_apex_cues(candidates)
        best, apex_rows, surface_rows = fit_common_offset_profile(
            processed["cue"],
            x_m,
            time_ns,
            apexes,
            velocity_values,
            time_zero_values,
            offset_values,
        )
        profile_row = {
            "file": record["file"],
            "apex_cue_count": len(apex_rows),
            **best,
            "calibration_scope": "field_common_offset_sensitivity_not_ground_truth",
        }
        profile_rows.append(profile_row)
        apex_rows_all.extend(apex_rows)
        for row in surface_rows:
            row["file"] = record["file"]
        surface_rows_all.extend(surface_rows)
        offset_rows_all.extend(summarize_best_by_offset(record["file"], surface_rows))
        overlay_paths[record["stem"]] = plot_common_offset_overlay(
            record,
            processed,
            x_m,
            time_ns,
            apex_rows,
            figures_dir / f"{record['stem']}_common_offset_overlay.png",
        )

    if not profile_rows:
        raise RuntimeError(f"no requested profiles found: {sorted(requested_stems)}")

    profile_csv = data_dir / "field_common_offset_profile_summary.csv"
    apex_csv = data_dir / "field_common_offset_apex_fits.csv"
    surface_csv = data_dir / "field_common_offset_score_surface.csv"
    offset_csv = data_dir / "field_common_offset_best_by_offset.csv"
    write_csv(profile_csv, profile_rows)
    write_csv(apex_csv, apex_rows_all)
    write_csv(surface_csv, surface_rows_all)
    write_csv(offset_csv, offset_rows_all)

    sensitivity_figure = plot_offset_sensitivity(
        offset_rows_all,
        figures_dir / "common_offset_sensitivity.png",
    )
    all_figures = [sensitivity_figure] + list(overlay_paths.values())
    validation_rows = validate_figures(all_figures)
    validation_csv = data_dir / "figure_validation.csv"
    write_csv(validation_csv, validation_rows)

    figure_notes = figures_dir / "FIGURE_NOTES.md"
    write_figure_notes(figure_notes, overlay_paths)
    write_readme(outdir / "README.md", input_dir, profile_rows)

    summary = {
        "run_name": args.run_name,
        "input_dir": str(input_dir),
        "field_root": str(Path(args.field_root)),
        "dataset_id": args.dataset_id,
        "dataset_root": str(dataset_root),
        "outdir": str(outdir),
        "readgssi_version": readgssi_version(),
        "profile_count": len(profile_rows),
        "apex_fit_count": len(apex_rows_all),
        "qc_scope": (
            "CPU-only common-offset hyperbola sensitivity. "
            "No confirmed rebar labeling, no radius estimate, and no FWI."
        ),
        "profile_csv": str(profile_csv),
        "offset_csv": str(offset_csv),
        "figure_validation_csv": str(validation_csv),
        "figures": {
            "sensitivity": sensitivity_figure,
            "overlays": overlay_paths,
            "figure_notes": str(figure_notes),
        },
    }
    summary_path = data_dir / "field_common_offset_sweep_summary.json"
    summary_path.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")

    manifest_path = write_run_manifest(
        str(outdir),
        "gssi51600s_common_offset_sweep",
        {
            "input_dir": str(input_dir),
            "field_root": str(Path(args.field_root)),
            "dataset_id": args.dataset_id,
            "summary_json": str(summary_path),
            "profile_csv": str(profile_csv),
            "offset_csv": str(offset_csv),
            "figure_notes": str(figure_notes),
            "readgssi_version": readgssi_version(),
        },
    )
    print(f"Wrote common-offset field sweep: {outdir}")
    print(f"Profiles: {len(profile_rows)}")
    print(f"Apex fits: {len(apex_rows_all)}")
    print(f"Summary: {summary_path}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()

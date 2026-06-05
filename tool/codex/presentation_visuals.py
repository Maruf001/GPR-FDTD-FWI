#!/usr/bin/env python3
"""Generate presentation/context visuals for the GPR-FDTD-FWI experiment archive.

Usage
-----
From the repository root:

    python tool/codex/presentation_visuals.py --all

The script reads experiment summaries and CSV files from ``outputs/experiments``
and writes reusable presentation figures under
``outputs/presentation_figures/2026_06_05_context_figures`` by default.  It does
not run FDTD simulations and does not modify existing experiment outputs.
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import math
import os
import sys
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle  # noqa: E402
from PIL import Image  # noqa: E402


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import config as cfg  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_OUTPUT_ROOT = (
    PROJECT_ROOT / "outputs" / "presentation_figures" / "2026_06_05_context_figures"
)
EXPERIMENT_ROOT = PROJECT_ROOT / "outputs" / "experiments"

STEEL = "#424b57"
STEEL_EDGE = "#111827"
TRUTH = "#111827"
RECOVERED = "#2563eb"
INITIAL = "#dc2626"
COMPETING = "#f59e0b"
CONCRETE = "#f1eee4"
AIR = "#edf6fb"
SURFACE = "#6b7280"
GRID = "#d1d5db"


def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def _experiment_dir(exp_id: int) -> Path:
    matches = sorted(EXPERIMENT_ROOT.glob(f"{int(exp_id):03d}_*"))
    if not matches:
        matches = sorted(EXPERIMENT_ROOT.glob(f"{int(exp_id)}_*"))
    if not matches:
        raise FileNotFoundError(f"No experiment directory found for {exp_id}")
    return matches[0]


def _read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _float(row: dict, key: str, default: float = math.nan) -> float:
    value = row.get(key, "")
    if value in ("", None):
        return float(default)
    return float(value)


def _parse_list(value) -> list[float]:
    if isinstance(value, (list, tuple)):
        return [float(v) for v in value]
    if value in ("", None):
        return []
    parsed = ast.literal_eval(str(value))
    return [float(v) for v in parsed]


def _scan_x_mm(n_sources: int | None, scan_step_mm: float = 8.0) -> np.ndarray:
    all_x = np.arange(
        cfg.SCAN_START_X * 1000.0,
        cfg.SCAN_END_X * 1000.0 + 1e-7,
        float(scan_step_mm),
    )
    if n_sources is not None and int(n_sources) < len(all_x):
        idx = np.linspace(0, len(all_x) - 1, int(n_sources), dtype=int)
        idx = np.unique(idx)
        return all_x[idx]
    return all_x


def _setup_geometry_axis(
    ax,
    *,
    xlim=(0, 500),
    zlim=(20, 140),
    title: str | None = None,
    surface_label: bool = True,
) -> None:
    ax.add_patch(
        Rectangle(
            (0, 0),
            500,
            40,
            facecolor=AIR,
            edgecolor="none",
            zorder=-3,
        )
    )
    ax.add_patch(
        Rectangle(
            (0, 40),
            500,
            260,
            facecolor=CONCRETE,
            edgecolor="none",
            zorder=-3,
        )
    )
    ax.axhline(40, color=SURFACE, linewidth=1.2)
    if surface_label:
        ax.text(
            xlim[0] + 2,
            38,
            "concrete surface (z=40 mm)",
            fontsize=8.5,
            color="#374151",
            va="bottom",
        )
    ax.set_xlim(*xlim)
    ax.set_ylim(*zlim)
    ax.invert_yaxis()
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, color=GRID, linewidth=0.5, alpha=0.7)
    ax.set_xlabel("x position (mm)")
    ax.set_ylabel("z / depth (mm)")
    if title:
        ax.set_title(title, fontsize=11, pad=8)


def _draw_rebars(
    ax,
    xs: list[float],
    zs: list[float],
    rs: list[float],
    *,
    label: str | None = None,
    facecolor: str = STEEL,
    edgecolor: str = STEEL_EDGE,
    alpha: float = 0.95,
    linestyle: str = "-",
    linewidth: float = 1.4,
    labels: bool = True,
    center_marker: bool = True,
    zorder: int = 3,
) -> None:
    for idx, (x, z, r) in enumerate(zip(xs, zs, rs)):
        circle = Circle(
            (x, z),
            r,
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=linewidth,
            linestyle=linestyle,
            alpha=alpha,
            zorder=zorder,
        )
        ax.add_patch(circle)
        if center_marker:
            ax.plot(x, z, marker="+", color=edgecolor, markersize=5, zorder=zorder + 1)
        if labels:
            prefix = "" if label is None else f"{label} "
            ax.text(
                x,
                z + r + 4.5,
                f"{prefix}{idx}: x={x:.0f}, z={z:.0f}, r={r:.1f} mm",
                ha="center",
                va="top",
                fontsize=7.5,
                color=edgecolor,
            )


def _draw_tx_rx_pair(
    ax,
    tx_x: float,
    offset_mm: float,
    *,
    y: float = 32.0,
    color: str = "#1d4ed8",
    alpha: float = 1.0,
    label: bool = False,
) -> None:
    rx_x = min(tx_x + offset_mm, 499.0)
    ax.plot(tx_x, y, marker="^", markersize=7, color=color, alpha=alpha, zorder=6)
    ax.plot(rx_x, y, marker="o", markersize=6, color=color, alpha=alpha, zorder=6)
    ax.plot([tx_x, rx_x], [y, y], color=color, linewidth=1.1, alpha=alpha, zorder=5)
    if label:
        ax.text(tx_x, y - 3.5, "Tx", ha="center", va="top", fontsize=8, color=color)
        ax.text(rx_x, y - 3.5, "Rx", ha="center", va="top", fontsize=8, color=color)
        ax.annotate(
            f"{offset_mm:.0f} mm",
            xy=((tx_x + rx_x) / 2.0, y - 1.0),
            xytext=((tx_x + rx_x) / 2.0, y - 9.0),
            ha="center",
            fontsize=8,
            color=color,
            arrowprops={"arrowstyle": "-", "color": color, "lw": 0.9},
        )


def plot_close_spacing_series(output_root: Path) -> Path:
    outdir = _ensure_dir(output_root / "campaign_close_spacing")
    path = outdir / "close_spacing_geometry_series.png"

    spacings = [50, 40, 30, 28, 14]
    fig, axes = plt.subplots(1, len(spacings), figsize=(14.5, 3.8), constrained_layout=True)
    for ax, spacing in zip(axes, spacings):
        xs = [190.0, 250.0, 250.0 + float(spacing)]
        zs = [90.0, 90.0, 90.0]
        rs = [5.0, 6.0, 8.0]
        _setup_geometry_axis(
            ax,
            xlim=(178, 318),
            zlim=(68, 110),
            title=f"close{spacing}",
            surface_label=False,
        )
        _draw_rebars(ax, xs, zs, rs, labels=False)
        ax.annotate(
            "",
            xy=(xs[1], 74),
            xytext=(xs[2], 74),
            arrowprops={"arrowstyle": "<->", "lw": 1.2, "color": "#374151"},
        )
        ax.text(
            (xs[1] + xs[2]) / 2.0,
            71.5,
            f"{spacing} mm",
            ha="center",
            va="bottom",
            fontsize=8.5,
            color="#374151",
        )
        for x, z, r in zip(xs, zs, rs):
            ax.text(x, z + r + 3.0, f"r={r:.0f}", ha="center", va="top", fontsize=8)
        if spacing == 14:
            ax.text(
                257,
                105,
                "tangent pair\n6+8=14 mm",
                fontsize=8,
                ha="left",
                va="bottom",
                color="#7c2d12",
            )
    fig.suptitle(
        "Variable-radius close-spacing geometries used in the recent coordinate-optimizer campaigns",
        fontsize=12.5,
    )
    return Path(save_validated_figure(fig, path))


def plot_tx_rx_offset_comparison(output_root: Path) -> Path:
    outdir = _ensure_dir(output_root / "common")
    path = outdir / "tx_rx_offset_35_40_45_50mm_comparison.png"

    offsets = [35, 40, 45, 50]
    scan_x = _scan_x_mm(4, scan_step_mm=8.0)
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 6.8), constrained_layout=True)
    for ax, offset in zip(axes.ravel(), offsets):
        _setup_geometry_axis(
            ax,
            xlim=(25, 500),
            zlim=(24, 120),
            title=f"4 scan positions, Tx/Rx offset = {offset} mm",
            surface_label=True,
        )
        _draw_rebars(ax, [190, 250, 264], [90, 90, 90], [5, 6, 8], labels=False, alpha=0.75)
        for i, x in enumerate(scan_x):
            _draw_tx_rx_pair(
                ax,
                float(x),
                float(offset),
                y=32.0,
                color="#2563eb",
                alpha=0.35 if i != 2 else 1.0,
                label=(i == 2),
            )
        ax.add_patch(
            FancyArrowPatch(
                (scan_x[0], 27),
                (scan_x[-1], 27),
                arrowstyle="->",
                mutation_scale=12,
                linewidth=1.2,
                color="#374151",
            )
        )
        ax.text(float(np.mean(scan_x)), 25.5, "scan direction", ha="center", va="bottom", fontsize=8.5)
        ax.text(
            30,
            116,
            f"Tx x = {', '.join(f'{v:.0f}' for v in scan_x)} mm",
            ha="left",
            va="bottom",
            fontsize=8,
            color="#374151",
        )
    fig.suptitle("Common-offset Tx/Rx acquisition geometry for close-spacing campaigns", fontsize=12.5)
    return Path(save_validated_figure(fig, path))


def plot_source_scan_layout(output_root: Path) -> Path:
    outdir = _ensure_dir(output_root / "common")
    path = outdir / "source_scan_layout_ascan_bscan_explanation.png"

    scan_x = _scan_x_mm(5, scan_step_mm=8.0)
    offset = 20.0
    t = np.linspace(0, 8, 400)
    traces = []
    for i, x in enumerate(scan_x):
        center = 2.1 + 0.35 * i + 0.45 * math.sin(x / 70.0)
        trace = np.exp(-((t - center) / 0.38) ** 2) * np.cos(12 * (t - center))
        trace += 0.55 * np.exp(-((t - 4.5 - 0.1 * i) / 0.6) ** 2) * np.cos(8 * (t - 4.5))
        traces.append(trace)
    bscan = np.asarray(traces).T

    fig = plt.figure(figsize=(13.0, 7.4), constrained_layout=True)
    gs = fig.add_gridspec(2, 3, height_ratios=[1.05, 1.0], width_ratios=[1.2, 0.8, 1.0])
    ax_geom = fig.add_subplot(gs[0, :])
    _setup_geometry_axis(ax_geom, xlim=(25, 500), zlim=(24, 125), title="Five source positions form one five-column B-scan")
    _draw_rebars(ax_geom, [150, 250, 350], [90, 90, 90], [6, 6, 6], labels=True, alpha=0.78)
    for i, x in enumerate(scan_x):
        _draw_tx_rx_pair(ax_geom, float(x), offset, y=32, alpha=0.45 + 0.1 * i)
        ax_geom.text(float(x), 28.3, f"{i+1}", ha="center", va="bottom", fontsize=8, color="#1d4ed8")
    ax_geom.add_patch(
        FancyArrowPatch(
            (scan_x[0], 27),
            (scan_x[-1], 27),
            arrowstyle="->",
            mutation_scale=12,
            linewidth=1.2,
            color="#374151",
        )
    )
    ax_geom.text(float(np.mean(scan_x)), 25.5, "scan direction along x", ha="center", va="bottom", fontsize=8.5)

    ax_trace = fig.add_subplot(gs[1, 0])
    for i, trace in enumerate(traces):
        offset_y = i * 1.35
        ax_trace.plot(t, trace + offset_y, color="#2563eb", linewidth=1.0)
        ax_trace.text(8.1, offset_y, f"A-scan {i+1}", va="center", fontsize=8.5)
    ax_trace.set_xlabel("time (ns)")
    ax_trace.set_ylabel("offset trace amplitude")
    ax_trace.set_title("One scan position -> one A-scan trace")
    ax_trace.set_xlim(0, 8.8)
    ax_trace.set_yticks([])
    ax_trace.grid(True, color=GRID, linewidth=0.5)

    ax_arrow = fig.add_subplot(gs[1, 1])
    ax_arrow.axis("off")
    ax_arrow.add_patch(
        FancyArrowPatch(
            (0.12, 0.5),
            (0.88, 0.5),
            arrowstyle="->",
            mutation_scale=28,
            linewidth=2.0,
            color="#374151",
            transform=ax_arrow.transAxes,
        )
    )
    ax_arrow.text(
        0.5,
        0.62,
        "stack columns",
        ha="center",
        va="bottom",
        fontsize=11,
        transform=ax_arrow.transAxes,
    )

    ax_bscan = fig.add_subplot(gs[1, 2])
    im = ax_bscan.imshow(
        bscan,
        extent=[1, len(scan_x), 8, 0],
        aspect="auto",
        cmap="seismic",
        vmin=-1.0,
        vmax=1.0,
    )
    ax_bscan.set_xlabel("source / scan position index")
    ax_bscan.set_ylabel("time (ns)")
    ax_bscan.set_title("B-scan = stack of A-scans")
    ax_bscan.set_xticks(range(1, len(scan_x) + 1))
    fig.colorbar(im, ax=ax_bscan, shrink=0.82, label="relative Ez")
    fig.suptitle("Meaning of 'source' in this repository: one Tx/Rx scan location, one A-scan column", fontsize=12.5)
    return Path(save_validated_figure(fig, path))


def plot_inversion_pipeline(output_root: Path) -> Path:
    outdir = _ensure_dir(output_root / "common")
    path = outdir / "fdtd_fwi_local_geometry_pipeline.png"

    fig, ax = plt.subplots(figsize=(14.0, 5.1), constrained_layout=True)
    ax.axis("off")
    boxes = [
        ("candidate parameters", "x, z, radius\nsource-profile grid"),
        ("geometry builder", "air + concrete\ncircular steel rebars"),
        ("FDTD forward solve", "GPU CPML\none solve per Tx/Rx position"),
        ("predicted B-scan", "stacked A-scans\nshape = time x positions"),
        ("objective comparison", "mute/window/filter\nfit amplitude/source basis"),
        ("rank + report", "best candidate\nconfidence intervals"),
        ("coordinate update", "sequential target update\nor campaign summary"),
    ]
    xs = np.linspace(0.06, 0.94, len(boxes))
    y = 0.56
    width = 0.12
    height = 0.28
    for i, ((title, body), x) in enumerate(zip(boxes, xs)):
        rect = Rectangle(
            (x - width / 2, y - height / 2),
            width,
            height,
            transform=ax.transAxes,
            facecolor="#f9fafb",
            edgecolor="#374151",
            linewidth=1.2,
        )
        ax.add_patch(rect)
        ax.text(x, y + 0.055, title, ha="center", va="center", fontsize=10, fontweight="bold", transform=ax.transAxes)
        ax.text(x, y - 0.055, body, ha="center", va="center", fontsize=8.5, transform=ax.transAxes)
        if i < len(boxes) - 1:
            ax.add_patch(
                FancyArrowPatch(
                    (x + width / 2 + 0.005, y),
                    (xs[i + 1] - width / 2 - 0.005, y),
                    arrowstyle="->",
                    mutation_scale=14,
                    linewidth=1.3,
                    color="#374151",
                    transform=ax.transAxes,
                )
            )
    ax.add_patch(
        FancyArrowPatch(
            (xs[-1], y - height / 2 - 0.02),
            (xs[0], y - height / 2 - 0.02),
            connectionstyle="arc3,rad=-0.22",
            arrowstyle="->",
            mutation_scale=14,
            linewidth=1.2,
            color="#7c3aed",
            transform=ax.transAxes,
        )
    )
    ax.text(
        0.5,
        0.18,
        "Recent experiments use deterministic candidate-grid search and coordinate updates; this is not a neural-network training pipeline.",
        ha="center",
        va="center",
        fontsize=10,
        color="#374151",
        transform=ax.transAxes,
    )
    ax.set_title("Local-geometry FDTD/FWI reporting pipeline", fontsize=13, pad=10)
    return Path(save_validated_figure(fig, path))


def plot_noise_boundary_context(output_root: Path) -> Path:
    exp_dir = _experiment_dir(418)
    outdir = _ensure_dir(output_root / "exp418")
    path = outdir / "exp418_close14_noise_boundary_context.png"
    rows = _read_csv(exp_dir / "data" / "noise_boundary_rows.csv")
    summary = _read_json(exp_dir / "data" / "noise_boundary_summary.json")["summary"]
    rows = sorted(rows, key=lambda row: _float(row, "noise_rms_percent"))

    noise = np.array([_float(row, "noise_rms_percent") for row in rows])
    cutoff_margin = np.array([_float(row, "nominal_competing_margin_to_cutoff") for row in rows])
    x_width = np.array([_float(row, "nominal_ambiguity_x_width_mm") for row in rows])
    clean = np.array([row.get("decision_class") == "clean" for row in rows])

    fig = plt.figure(figsize=(13.2, 6.2), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, height_ratios=[0.9, 1.05])

    ax_geom = fig.add_subplot(gs[:, 0])
    _setup_geometry_axis(
        ax_geom,
        xlim=(180, 276),
        zlim=(68, 108),
        title="close14 geometry at the noise-boundary campaign",
        surface_label=False,
    )
    _draw_rebars(ax_geom, [190, 250, 264], [90, 90, 90], [5, 6, 8], labels=True)
    ax_geom.annotate(
        "",
        xy=(250, 73.5),
        xytext=(264, 73.5),
        arrowprops={"arrowstyle": "<->", "lw": 1.2, "color": "#7c2d12"},
    )
    ax_geom.text(257, 70.7, "14 mm tangent spacing", ha="center", va="bottom", fontsize=9, color="#7c2d12")
    _draw_tx_rx_pair(ax_geom, 178, 50, y=32, color="#2563eb", alpha=1.0, label=True)
    ax_geom.text(182, 34.5, "4-source, 50 mm offset campaign", fontsize=8.5, color="#1d4ed8", va="top")

    ax_margin = fig.add_subplot(gs[0, 1])
    ax_margin.axhline(0.0, color="#111827", linewidth=1.0, linestyle="--")
    ax_margin.plot(noise, cutoff_margin, color="#374151", linewidth=1.2, marker="o", markersize=4)
    ax_margin.scatter(noise[clean], cutoff_margin[clean], color="#16a34a", s=55, label="clean")
    ax_margin.scatter(noise[~clean], cutoff_margin[~clean], color="#ea580c", s=55, label="point-correct but ambiguous")
    ax_margin.set_xlabel("noise RMS (% of clean signal)")
    ax_margin.set_ylabel("competitor margin to ambiguity cutoff")
    ax_margin.set_title("Clean boundary is a near-zero cutoff-margin event")
    ax_margin.grid(True, color=GRID, linewidth=0.5)
    ax_margin.legend(fontsize=8, loc="best")

    ax_width = fig.add_subplot(gs[1, 1])
    ax_width.step(noise, x_width, where="post", color="#7c3aed", linewidth=1.7)
    ax_width.scatter(noise, x_width, color=np.where(clean, "#16a34a", "#ea580c"), s=48)
    ax_width.set_xlabel("noise RMS (% of clean signal)")
    ax_width.set_ylabel("reported x-ambiguity width (mm)")
    ax_width.set_title("Failure mode is lateral x interval widening, not wrong point estimate")
    ax_width.grid(True, color=GRID, linewidth=0.5)
    ax_width.set_yticks([0, 1])
    clean_noise = summary["promoted_clean_noise_rms_percent"]
    upper_noise = summary["final_ambiguous_upper_noise_rms_percent"]
    ax_width.text(
        0.02,
        0.92,
        f"clean endpoint: {clean_noise:.12f}% RMS\nambiguous upper: {upper_noise:.12f}% RMS\nbracket width: {summary['final_bracket_width_percent_rms']:.8f}% RMS",
        transform=ax_width.transAxes,
        ha="left",
        va="top",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#d1d5db", "pad": 4},
    )
    fig.suptitle("Experiment 418 context: close14 noise-boundary result", fontsize=12.5)
    return Path(save_validated_figure(fig, path))


def _noise_boundary_arrays():
    exp_dir = _experiment_dir(418)
    rows = _read_csv(exp_dir / "data" / "noise_boundary_rows.csv")
    summary = _read_json(exp_dir / "data" / "noise_boundary_summary.json")["summary"]
    rows = sorted(rows, key=lambda row: _float(row, "noise_rms_percent"))
    clean_noise = float(summary["promoted_clean_noise_rms_percent"])
    x_micro_pp = np.array([
        (_float(row, "noise_rms_percent") - clean_noise) * 1.0e6
        for row in rows
    ])
    clean = np.array([row.get("decision_class") == "clean" for row in rows])
    return rows, summary, x_micro_pp, clean


def plot_noise_boundary_geometry_v2(output_root: Path) -> Path:
    outdir = _ensure_dir(output_root / "exp418")
    path = outdir / "exp418_close14_geometry_context_v2.png"

    fig, ax = plt.subplots(figsize=(9.4, 5.0), constrained_layout=True)
    _setup_geometry_axis(
        ax,
        xlim=(172, 276),
        zlim=(22, 108),
        title="Experiment 418 geometry: close14 tangent pair with 50 mm Tx/Rx offset",
        surface_label=True,
    )
    _draw_rebars(ax, [190, 250, 264], [90, 90, 90], [5, 6, 8], labels=False, center_marker=False)
    for idx, (x, z) in enumerate(zip([190, 250, 264], [90, 90, 90])):
        ax.text(x, z, str(idx), ha="center", va="center", fontsize=9, color="white", fontweight="bold")
    _draw_tx_rx_pair(ax, 178, 50, y=32, color="#2563eb", alpha=1.0, label=False)
    ax.text(178, 29.0, "Tx", ha="center", va="bottom", fontsize=9, color="#2563eb")
    ax.text(228, 29.0, "Rx", ha="center", va="bottom", fontsize=9, color="#2563eb")
    ax.annotate(
        "50 mm",
        xy=(203, 32.0),
        xytext=(203, 25.6),
        ha="center",
        va="bottom",
        fontsize=9,
        color="#2563eb",
        arrowprops={"arrowstyle": "-", "lw": 1.0, "color": "#2563eb"},
    )
    ax.annotate(
        "",
        xy=(250, 72.8),
        xytext=(264, 72.8),
        arrowprops={"arrowstyle": "<->", "lw": 1.25, "color": "#7c2d12"},
    )
    ax.text(
        257,
        69.8,
        "14 mm center spacing\nmiddle r=6 mm, right r=8 mm",
        ha="center",
        va="bottom",
        fontsize=9,
        color="#7c2d12",
    )
    ax.text(
        173.5,
        102.0,
        "0: x=190, z=90, r=5 mm\n1: x=250, z=90, r=6 mm\n2: x=264, z=90, r=8 mm",
        ha="left",
        va="bottom",
        fontsize=8.5,
        color="#374151",
        bbox={"facecolor": "white", "edgecolor": "#d1d5db", "pad": 4, "alpha": 0.92},
    )
    return Path(save_validated_figure(fig, path))


def plot_noise_boundary_cutoff_margin_v2(output_root: Path) -> Path:
    outdir = _ensure_dir(output_root / "exp418")
    path = outdir / "exp418_noise_boundary_cutoff_margin_v2.png"
    rows, summary, x_micro_pp, clean = _noise_boundary_arrays()
    cutoff_margin = np.array([
        _float(row, "nominal_competing_margin_to_cutoff") * 1.0e8
        for row in rows
    ])

    fig, ax = plt.subplots(figsize=(9.2, 5.1), constrained_layout=True)
    ax.axhline(0.0, color="#111827", linewidth=1.0, linestyle="--", label="ambiguity cutoff")
    ax.plot(x_micro_pp, cutoff_margin, color="#374151", linewidth=1.35, marker="o", markersize=4.2)
    ax.scatter(x_micro_pp[clean], cutoff_margin[clean], color="#16a34a", s=70, label="clean endpoint", zorder=5)
    ax.scatter(x_micro_pp[~clean], cutoff_margin[~clean], color="#ea580c", s=70, label="point-correct but x-ambiguous", zorder=5)
    ax.set_xlabel("noise increase above clean endpoint (micro percentage points)")
    ax.set_ylabel("competitor margin to ambiguity cutoff (x 1e-8)")
    ax.set_title("Experiment 418: the clean boundary is a near-zero cutoff-margin event")
    ax.grid(True, color=GRID, linewidth=0.55)
    ax.legend(fontsize=9, loc="best")
    ax.text(
        0.02,
        0.04,
        f"absolute clean endpoint: {summary['promoted_clean_noise_rms_percent']:.12f}% RMS\n"
        f"ambiguous upper endpoint: {summary['final_ambiguous_upper_noise_rms_percent']:.12f}% RMS",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8.8,
        bbox={"facecolor": "white", "edgecolor": "#d1d5db", "pad": 4},
    )
    return Path(save_validated_figure(fig, path))


def plot_noise_boundary_x_ambiguity_v2(output_root: Path) -> Path:
    outdir = _ensure_dir(output_root / "exp418")
    path = outdir / "exp418_noise_boundary_x_ambiguity_v2.png"
    rows, summary, x_micro_pp, clean = _noise_boundary_arrays()
    x_width = np.array([_float(row, "nominal_ambiguity_x_width_mm") for row in rows])

    fig, ax = plt.subplots(figsize=(9.2, 5.1), constrained_layout=True)
    ax.step(x_micro_pp, x_width, where="post", color="#7c3aed", linewidth=2.0, label="reported x interval width")
    ax.scatter(x_micro_pp[clean], x_width[clean], color="#16a34a", s=70, label="clean endpoint", zorder=5)
    ax.scatter(x_micro_pp[~clean], x_width[~clean], color="#ea580c", s=70, label="point-correct but x-ambiguous", zorder=5)
    ax.set_xlabel("noise increase above clean endpoint (micro percentage points)")
    ax.set_ylabel("reported x-ambiguity width (mm)")
    ax.set_title("Experiment 418: boundary failure is lateral interval widening")
    ax.grid(True, color=GRID, linewidth=0.55)
    ax.set_yticks([0, 1])
    ax.set_ylim(-0.08, 1.12)
    ax.legend(fontsize=9, loc="lower right")
    ax.text(
        0.02,
        0.92,
        "best point remains x=264 mm;\nnear-tied x=263 mm enters the interval",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#d1d5db", "pad": 4},
    )
    ax.text(
        0.02,
        0.08,
        f"bracket width: {summary['final_bracket_width_percent_rms']:.8f}% RMS",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8.8,
        bbox={"facecolor": "white", "edgecolor": "#d1d5db", "pad": 4},
    )
    return Path(save_validated_figure(fig, path))


def plot_source_shape_candidate_landscape(output_root: Path) -> Path:
    outdir = _ensure_dir(output_root / "exp432_434")
    path = outdir / "source_shape_dense_candidate_landscape.png"
    exp_ids = [433, 432, 434]
    titles = ["left target (exp 433)", "center target (exp 432)", "right target (exp 434)"]
    case_label = "source_mismatch_ringdown025_noise10_seed13"

    fig, axes = plt.subplots(1, 3, figsize=(13.8, 4.8), constrained_layout=True)
    for ax, exp_id, title in zip(axes, exp_ids, titles):
        exp_dir = _experiment_dir(exp_id)
        csv_path = exp_dir / "data" / "multi_rebar_local_geometry_objective_candidates.csv"
        rows = [
            row
            for row in _read_csv(csv_path)
            if row.get("case_label") == case_label and row.get("objective_label") == "base"
        ]
        if not rows:
            rows = [
                row
                for row in _read_csv(csv_path)
                if row.get("objective_label") == "base"
            ]
        misfit = np.array([_float(row, "misfit") for row in rows])
        z = np.array([_float(row, "z_mm") for row in rows])
        radius = np.array([_float(row, "radius_mm") for row in rows])
        delta = misfit - float(np.nanmin(misfit))
        order = np.argsort(delta)
        show = order[: min(110, len(order))]
        sc = ax.scatter(
            radius[show],
            z[show],
            c=delta[show],
            cmap="viridis_r",
            s=54,
            edgecolor="#111827",
            linewidth=0.35,
        )
        best = order[0]
        ax.scatter([6.0], [90.0], marker="*", color="#dc2626", s=150, label="true r/z")
        ax.scatter([radius[best]], [z[best]], marker="o", facecolors="none", edgecolors="#2563eb", s=160, linewidth=1.7, label="best")
        for rank, idx in enumerate(order[:5], start=1):
            ax.text(radius[idx] + 0.035, z[idx] + 0.06, str(rank), fontsize=8, color="#111827")
        ax.invert_yaxis()
        ax.set_xlabel("candidate radius (mm)")
        ax.set_ylabel("candidate z (mm)")
        ax.set_title(title)
        ax.grid(True, color=GRID, linewidth=0.5)
        ax.set_xlim(5.25, 7.15)
        ax.set_ylim(92.3, 87.7)
        ax.legend(fontsize=8, loc="lower right")
        fig.colorbar(sc, ax=ax, shrink=0.75, label="misfit above best")
    fig.suptitle(
        "Source-shape Stage 4C dense candidate landscapes: true point and nearby high-radius branches",
        fontsize=12.5,
    )
    return Path(save_validated_figure(fig, path))


def _state_rows(exp_id: int) -> tuple[Path, list[dict[str, str]]]:
    exp_dir = _experiment_dir(exp_id)
    return exp_dir, _read_csv(exp_dir / "data" / "coordinate_state_history.csv")


def plot_coupled_coordinate_evolution(output_root: Path) -> Path:
    outdir = _ensure_dir(output_root / "exp440_444")
    path = outdir / "coupled_coordinate_state_evolution.png"
    exp_ids = [440, 441, 443]
    labels = ["exp 440: all radii high", "exp 441: x/z/r perturbed", "exp 443: reversed order"]
    truth_x = np.array([150.0, 250.0, 350.0])
    truth_z = np.array([90.0, 90.0, 90.0])
    truth_r = np.array([6.0, 6.0, 6.0])

    fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.2), sharey=True, constrained_layout=True)
    for ax, exp_id, label in zip(axes, exp_ids, labels):
        _, rows = _state_rows(exp_id)
        steps = np.array([int(row["step"]) for row in rows])
        x_err = []
        z_err = []
        r_err = []
        total_err = []
        for row in rows:
            xs = np.array(_parse_list(row["x_values_mm"]))
            zs = np.array(_parse_list(row["z_values_mm"]))
            rs = np.array(_parse_list(row["radii_mm"]))
            x_err.append(float(np.max(np.abs(xs - truth_x))))
            z_err.append(float(np.max(np.abs(zs - truth_z))))
            r_err.append(float(np.max(np.abs(rs - truth_r))))
            total_err.append(float(np.sqrt(np.mean((xs - truth_x) ** 2 + (zs - truth_z) ** 2 + (rs - truth_r) ** 2))))
        ax.plot(steps, x_err, marker="o", color="#2563eb", label="max |x error|")
        ax.plot(steps, z_err, marker="s", color="#16a34a", label="max |z error|")
        ax.plot(steps, r_err, marker="^", color="#dc2626", label="max |radius error|")
        ax.plot(steps, total_err, marker="d", color="#7c3aed", linestyle="--", label="RMS geometry error")
        ax.set_xlabel("coordinate step")
        ax.set_title(label, fontsize=10.5)
        ax.grid(True, color=GRID, linewidth=0.5)
        ax.set_xticks(steps)
        ax.set_ylim(-0.05, 2.3)
    axes[0].set_ylabel("error relative to truth (mm)")
    axes[0].legend(fontsize=8, loc="upper right")
    fig.suptitle("Coupled source-shape coordinate runs: geometry error collapses in one pass", fontsize=12.5)
    return Path(save_validated_figure(fig, path))


def plot_coupled_coordinate_percent_error(output_root: Path) -> Path:
    outdir = _ensure_dir(output_root / "exp440_444")
    path = outdir / "coupled_coordinate_percent_error.png"
    exp_ids = [440, 441, 443]
    labels = ["exp 440: all radii high", "exp 441: x/z/r perturbed", "exp 443: reversed order"]
    truth_x = np.array([150.0, 250.0, 350.0])
    truth_z = np.array([90.0, 90.0, 90.0])
    truth_r = np.array([6.0, 6.0, 6.0])

    fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.2), sharey=True, constrained_layout=True)
    for ax, exp_id, label in zip(axes, exp_ids, labels):
        _, rows = _state_rows(exp_id)
        steps = np.array([int(row["step"]) for row in rows])
        x_err = []
        z_err = []
        r_err = []
        rms_err = []
        for row in rows:
            xs = np.array(_parse_list(row["x_values_mm"]))
            zs = np.array(_parse_list(row["z_values_mm"]))
            rs = np.array(_parse_list(row["radii_mm"]))
            x_norm = np.abs(xs - truth_x) / truth_x
            z_norm = np.abs(zs - truth_z) / truth_z
            r_norm = np.abs(rs - truth_r) / truth_r
            x_err.append(float(np.max(x_norm) * 100.0))
            z_err.append(float(np.max(z_norm) * 100.0))
            r_err.append(float(np.max(r_norm) * 100.0))
            rms_err.append(float(np.sqrt(np.mean(np.r_[x_norm, z_norm, r_norm] ** 2)) * 100.0))
        ax.plot(steps, x_err, marker="o", color="#2563eb", label="max x error")
        ax.plot(steps, z_err, marker="s", color="#16a34a", label="max z error")
        ax.plot(steps, r_err, marker="^", color="#dc2626", label="max radius error")
        ax.plot(steps, rms_err, marker="d", color="#7c3aed", linestyle="--", label="RMS normalized error")
        ax.set_xlabel("coordinate step")
        ax.set_title(label, fontsize=10.5)
        ax.grid(True, color=GRID, linewidth=0.5)
        ax.set_xticks(steps)
        ax.set_ylim(-0.08, 3.7)
    axes[0].set_ylabel("error relative to target value (%)")
    axes[0].legend(fontsize=8, loc="upper right")
    fig.suptitle("Coupled coordinate runs: percentage error by parameter family", fontsize=12.5)
    return Path(save_validated_figure(fig, path))


def plot_coupled_target_vs_recovered(output_root: Path) -> Path:
    outdir = _ensure_dir(output_root / "exp440_444")
    path = outdir / "coupled_target_vs_recovered_final_states.png"
    return _plot_coupled_target_vs_recovered(output_root, path)


def plot_coupled_target_vs_recovered_v2(output_root: Path) -> Path:
    outdir = _ensure_dir(output_root / "exp440_444")
    path = outdir / "coupled_target_vs_recovered_final_states_v2.png"
    return _plot_coupled_target_vs_recovered(output_root, path, include_legend=True)


def _plot_coupled_target_vs_recovered(
    output_root: Path,
    path: Path,
    *,
    include_legend: bool = False,
) -> Path:
    exp_ids = [440, 441, 443]
    labels = [
        "exp 440: compact radius-only correction",
        "exp 441: x/z/r-perturbed correction",
        "exp 443: reversed perturbation and target order",
    ]

    fig, axes = plt.subplots(3, 1, figsize=(10.8, 8.0), constrained_layout=True)
    for ax, exp_id, label in zip(axes, exp_ids, labels):
        exp_dir = _experiment_dir(exp_id)
        summary = _read_json(exp_dir / "data" / "multi_rebar_coordinate_optimizer_summary.json")
        truth_x = summary["true_x_values_mm"]
        truth_z = summary["true_z_values_mm"]
        truth_r = summary["truth_radius_values_mm"]
        initial = summary["initial_state"]
        final = summary["final_state"]
        _setup_geometry_axis(ax, xlim=(132, 368), zlim=(76, 106), title=label, surface_label=False)
        _draw_rebars(
            ax,
            initial["x_values_mm"],
            initial["z_values_mm"],
            initial["radii_mm"],
            facecolor="none",
            edgecolor=INITIAL,
            alpha=1.0,
            linestyle="--",
            linewidth=1.4,
            labels=False,
            zorder=3,
        )
        _draw_rebars(
            ax,
            truth_x,
            truth_z,
            truth_r,
            facecolor="#d1d5db",
            edgecolor=TRUTH,
            alpha=0.95,
            labels=False,
            zorder=2,
        )
        _draw_rebars(
            ax,
            final["x_values_mm"],
            final["z_values_mm"],
            final["radii_mm"],
            facecolor="none",
            edgecolor=RECOVERED,
            alpha=1.0,
            linestyle="-",
            linewidth=2.0,
            labels=False,
            zorder=5,
        )
        ax.text(
            362,
            80,
            f"targets {summary['target_indices']}",
            ha="right",
            va="top",
            fontsize=8.2,
            color="#374151",
        )
    if include_legend:
        handles = [
            Line2D(
                [0],
                [0],
                marker="o",
                color=INITIAL,
                markerfacecolor="none",
                markeredgecolor=INITIAL,
                linestyle="--",
                linewidth=1.4,
                markersize=9,
                label="initial state",
            ),
            Line2D(
                [0],
                [0],
                marker="o",
                color=TRUTH,
                markerfacecolor="#d1d5db",
                markeredgecolor=TRUTH,
                linestyle="None",
                markersize=10,
                label="target geometry",
            ),
            Line2D(
                [0],
                [0],
                marker="o",
                color=RECOVERED,
                markerfacecolor="none",
                markeredgecolor=RECOVERED,
                linestyle="-",
                linewidth=2.0,
                markersize=9,
                label="final recovered geometry",
            ),
        ]
        axes[0].legend(
            handles=handles,
            loc="lower center",
            ncol=3,
            frameon=True,
            fontsize=9,
        )
    fig.suptitle("Experiments 440, 441, and 443: coupled coordinate final states recover the target geometry", fontsize=12.5)
    return Path(save_validated_figure(fig, path))


def animate_scan_path(output_root: Path) -> Path:
    outdir = _ensure_dir(output_root / "common")
    path = outdir / "scan_path_5source_txrx20mm.gif"
    scan_x = _scan_x_mm(5, scan_step_mm=8.0)
    offset = 20.0

    fig, ax = plt.subplots(figsize=(8.8, 4.4))
    _setup_geometry_axis(
        ax,
        xlim=(25, 500),
        zlim=(24, 120),
        title="Animated scan path: five source positions, 20 mm Tx/Rx offset",
    )
    _draw_rebars(ax, [150, 250, 350], [90, 90, 90], [6, 6, 6], labels=False, alpha=0.75)
    ax.add_patch(
        FancyArrowPatch(
            (scan_x[0], 27),
            (scan_x[-1], 27),
            arrowstyle="->",
            mutation_scale=12,
            linewidth=1.2,
            color="#374151",
        )
    )
    tx_marker, = ax.plot([], [], marker="^", color="#2563eb", markersize=9, linestyle="None", zorder=6)
    rx_marker, = ax.plot([], [], marker="o", color="#2563eb", markersize=8, linestyle="None", zorder=6)
    link, = ax.plot([], [], color="#2563eb", linewidth=1.5, zorder=5)
    trace_text = ax.text(30, 113, "", fontsize=10, color="#111827", va="bottom")

    def update(frame):
        i = int(frame % len(scan_x))
        tx = float(scan_x[i])
        rx = min(tx + offset, 499.0)
        tx_marker.set_data([tx], [32.0])
        rx_marker.set_data([rx], [32.0])
        link.set_data([tx, rx], [32.0, 32.0])
        trace_text.set_text(f"source position {i + 1}/{len(scan_x)} -> A-scan column {i + 1}")
        return tx_marker, rx_marker, link, trace_text

    anim = FuncAnimation(fig, update, frames=len(scan_x), interval=750, blit=True, repeat=True)
    outdir.mkdir(parents=True, exist_ok=True)
    anim.save(path, writer=PillowWriter(fps=1.4), dpi=140)
    plt.close(fig)
    with Image.open(path) as image:
        if getattr(image, "n_frames", 1) < len(scan_x):
            raise ValueError(f"Saved GIF has too few frames: {path}")
    return path


def write_notes(output_root: Path, paths: list[Path]) -> Path:
    notes = output_root / "PRESENTATION_FIGURE_NOTES.md"
    rel_paths = [path.relative_to(PROJECT_ROOT) for path in paths]
    lines = [
        "# Presentation Figure Notes",
        "",
        "Generated by `tool/codex/presentation_visuals.py`.",
        "",
        "These are presentation/context figures. They do not replace experiment-native diagnostic plots, and no FDTD simulations are run by this script.",
        "",
        "## Generated Files",
        "",
    ]
    descriptions = {
        "close_spacing_geometry_series.png": "Engineering cross-sections for close50, close40, close30, close28, and close14 variable-radius geometries.",
        "tx_rx_offset_35_40_45_50mm_comparison.png": "Common-offset Tx/Rx scan geometry for 35, 40, 45, and 50 mm offsets with four scan positions.",
        "source_scan_layout_ascan_bscan_explanation.png": "Diagram explaining that a source is a Tx/Rx scan location, one location yields one A-scan, and stacked A-scans form a B-scan.",
        "fdtd_fwi_local_geometry_pipeline.png": "Pipeline schematic for the recent local-geometry FDTD/FWI candidate-grid workflow.",
        "exp418_close14_noise_boundary_context.png": "Context figure for the close14 noise boundary around experiments 409-418.",
        "exp418_close14_geometry_context_v2.png": "Cleaner standalone geometry context for the close14 noise-boundary campaign.",
        "exp418_noise_boundary_cutoff_margin_v2.png": "Standalone cutoff-margin chart for the experiment 418 noise boundary.",
        "exp418_noise_boundary_x_ambiguity_v2.png": "Standalone x-ambiguity-width chart for the experiment 418 noise boundary.",
        "source_shape_dense_candidate_landscape.png": "Candidate radius/depth landscapes for the Stage 4C source-shape dense runs 432-434.",
        "coupled_coordinate_state_evolution.png": "Error-versus-step summary for coupled coordinate runs 440, 441, and 443.",
        "coupled_coordinate_percent_error.png": "Percentage-error companion to the coupled coordinate millimeter-error chart.",
        "coupled_target_vs_recovered_final_states.png": "Initial, target, and final geometry overlays for coupled coordinate runs 440, 441, and 443.",
        "coupled_target_vs_recovered_final_states_v2.png": "Improved target-vs-recovered geometry overlay with an explicit legend.",
        "scan_path_5source_txrx20mm.gif": "Simple animation of the five-position 20 mm common-offset scan path.",
    }
    for rel in rel_paths:
        lines.append(f"- `{rel}`: {descriptions.get(rel.name, 'generated presentation figure')}")
    notes.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return notes


def generate_all(output_root: Path) -> list[Path]:
    output_root = _ensure_dir(output_root)
    paths = [
        plot_close_spacing_series(output_root),
        plot_tx_rx_offset_comparison(output_root),
        plot_source_scan_layout(output_root),
        plot_inversion_pipeline(output_root),
        plot_noise_boundary_context(output_root),
        plot_noise_boundary_geometry_v2(output_root),
        plot_noise_boundary_cutoff_margin_v2(output_root),
        plot_noise_boundary_x_ambiguity_v2(output_root),
        plot_source_shape_candidate_landscape(output_root),
        plot_coupled_coordinate_evolution(output_root),
        plot_coupled_coordinate_percent_error(output_root),
        plot_coupled_target_vs_recovered(output_root),
        plot_coupled_target_vs_recovered_v2(output_root),
        animate_scan_path(output_root),
    ]
    write_notes(output_root, paths)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Generate the selected presentation/context figures.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Output directory for generated presentation figures.",
    )
    args = parser.parse_args()
    if not args.all:
        parser.error("Pass --all to generate the selected figure set.")
    paths = generate_all(args.output_root)
    print("Generated presentation/context figures:")
    for path in paths:
        print(f"  {path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()

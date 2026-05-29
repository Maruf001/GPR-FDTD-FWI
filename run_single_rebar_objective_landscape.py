"""Objective landscape diagnostics for the one-rebar pipeline.

This script samples the same muted, normalized B-scan objective used by
``run_single_rebar_inversion.py``. It is intended to answer whether x, z, and
radius are identifiable before expanding from one rebar to multiple rebars.
"""
import argparse
import csv
import json
import os
import sys
import time as timer

import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

import config as cfg  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from inversion.single_rebar_pipeline import (  # noqa: E402
    SingleRebarInversionEngine,
    SingleRebarParams,
    default_single_rebar_initial_guess,
    default_single_rebar_truth,
)


def _parse_frequency_list(text):
    try:
        values = [float(item.strip()) * 1e9 for item in text.split(",") if item.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use comma-separated GHz values, e.g. 1.4,1.5,1.6") from exc
    if not values:
        raise argparse.ArgumentTypeError("At least one frequency is required")
    return values


def _parse_mm_bounds(text):
    try:
        values = [float(item.strip()) for item in text.split(",") if item.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use min,max in millimeters, e.g. 60,130") from exc
    if len(values) != 2 or values[0] >= values[1]:
        raise argparse.ArgumentTypeError("Bounds must be two increasing values: min,max")
    return values


def _params_from_args(prefix, args, default):
    x_mm = getattr(args, f"{prefix}_x_mm")
    z_mm = getattr(args, f"{prefix}_z_mm")
    radius_mm = getattr(args, f"{prefix}_radius_mm")
    return SingleRebarParams(
        x=(x_mm if x_mm is not None else default.x * 1000.0) / 1000.0,
        z=(z_mm if z_mm is not None else default.z * 1000.0) / 1000.0,
        radius=(radius_mm if radius_mm is not None else default.radius * 1000.0) / 1000.0,
    )


def _default_bounds():
    lower = np.array([
        cfg.SCAN_START_X,
        cfg.CONCRETE_TOP + 0.010,
        0.003,
    ], dtype=np.float64)
    upper = np.array([
        cfg.SCAN_END_X,
        min(cfg.DOMAIN_Z - 0.020, cfg.CONCRETE_TOP + 0.160),
        0.015,
    ], dtype=np.float64)
    return lower, upper


def _bounds_from_args(args):
    lower, upper = _default_bounds()
    for index, pair in enumerate((args.x_bounds_mm, args.z_bounds_mm, args.radius_bounds_mm)):
        if pair is not None:
            lower[index] = pair[0] / 1000.0
            upper[index] = pair[1] / 1000.0
    return lower, upper


def _override_grid(grid_step_mm):
    if grid_step_mm is None:
        return
    old_pml_thickness = cfg.NPML * cfg.DX
    step_m = grid_step_mm / 1000.0
    cfg.DX = step_m
    cfg.DZ = step_m
    cfg.DT = cfg.COURANT * cfg.DX / (cfg.C0 * np.sqrt(2.0))
    cfg.NT = int(np.ceil(cfg.T_MAX / cfg.DT))
    cfg.NPML = max(8, int(round(old_pml_thickness / step_m)))
    cfg.NX_INNER = int(np.round(cfg.DOMAIN_X / cfg.DX))
    cfg.NZ_INNER = int(np.round(cfg.DOMAIN_Z / cfg.DZ))
    cfg.NX = cfg.NX_INNER + 2 * cfg.NPML
    cfg.NZ = cfg.NZ_INNER + 2 * cfg.NPML
    print(
        f"Grid override: dx=dz={grid_step_mm:.3f} mm, "
        f"NPML={cfg.NPML}, NX={cfg.NX}, NZ={cfg.NZ}, NT={cfg.NT}"
    )


def _load_compare_params(path):
    if path is None:
        return None
    with open(path, "r", encoding="utf-8") as f:
        summary = json.load(f)
    params = summary.get("recovered") or summary.get("optimizer_final")
    if params is None:
        raise ValueError(f"No recovered/optimizer_final params in {path}")
    return SingleRebarParams(
        x=params["x_mm"] / 1000.0,
        z=params["z_mm"] / 1000.0,
        radius=params["radius_mm"] / 1000.0,
    )


def _axis_around(center_m, half_width_mm, count, lower_m, upper_m):
    center_mm = center_m * 1000.0
    lo_mm = max(lower_m * 1000.0, center_mm - half_width_mm)
    hi_mm = min(upper_m * 1000.0, center_mm + half_width_mm)
    if lo_mm >= hi_mm:
        raise ValueError("Axis bounds collapsed; widen the window or search bounds")
    if count % 2 == 1 and lo_mm <= center_mm <= hi_mm:
        n_each = count // 2
        left = np.linspace(lo_mm, center_mm, n_each + 1)[:-1]
        right = np.linspace(center_mm, hi_mm, n_each + 1)[1:]
        values_mm = np.concatenate([left, np.array([center_mm]), right])
    else:
        values_mm = np.linspace(lo_mm, hi_mm, count)
    return values_mm / 1000.0


def _radius_axis(args, lower_m, upper_m):
    if args.radius_sweep_bounds_mm is not None:
        lo_mm, hi_mm = args.radius_sweep_bounds_mm
        lo_m = max(lower_m, lo_mm / 1000.0)
        hi_m = min(upper_m, hi_mm / 1000.0)
    else:
        lo_m, hi_m = lower_m, upper_m
    if lo_m >= hi_m:
        raise ValueError("Radius sweep bounds collapsed")
    return np.linspace(lo_m, hi_m, args.radius_count)


def _evaluate_point(engine, params, label):
    value = float(engine.objective(params.as_array()))
    print(
        f"  {label}: J={value:.6e}, "
        f"x={params.x * 1000.0:.2f} mm, "
        f"z={params.z * 1000.0:.2f} mm, "
        f"r={params.radius * 1000.0:.2f} mm"
    )
    return value


def _write_long_csv(path, rows, fieldnames):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _sample_xz(engine, x_values, z_values, radius, progress_every):
    values = np.empty((len(z_values), len(x_values)), dtype=np.float64)
    rows = []
    total = len(x_values) * len(z_values)
    count = 0
    started = timer.time()
    for iz, z_value in enumerate(z_values):
        for ix, x_value in enumerate(x_values):
            params = SingleRebarParams(x=x_value, z=z_value, radius=radius)
            value = float(engine.objective(params.as_array()))
            values[iz, ix] = value
            rows.append({
                "x_mm": x_value * 1000.0,
                "z_mm": z_value * 1000.0,
                "radius_mm": radius * 1000.0,
                "objective": value,
            })
            count += 1
            if progress_every and count % progress_every == 0:
                elapsed = timer.time() - started
                print(f"  x-z grid: {count}/{total} evaluations, elapsed={elapsed:.1f} s")
    return values, rows


def _sample_z_radius(engine, z_values, radius_values, x_value, progress_every):
    values = np.empty((len(z_values), len(radius_values)), dtype=np.float64)
    rows = []
    total = len(z_values) * len(radius_values)
    count = 0
    started = timer.time()
    for iz, z_value in enumerate(z_values):
        for ir, radius in enumerate(radius_values):
            params = SingleRebarParams(x=x_value, z=z_value, radius=radius)
            value = float(engine.objective(params.as_array()))
            values[iz, ir] = value
            rows.append({
                "x_mm": x_value * 1000.0,
                "z_mm": z_value * 1000.0,
                "radius_mm": radius * 1000.0,
                "objective": value,
            })
            count += 1
            if progress_every and count % progress_every == 0:
                elapsed = timer.time() - started
                print(f"  z-radius grid: {count}/{total} evaluations, elapsed={elapsed:.1f} s")
    return values, rows


def _sample_radius(engine, radius_values, x_value, z_value):
    values = np.empty(len(radius_values), dtype=np.float64)
    rows = []
    for ir, radius in enumerate(radius_values):
        params = SingleRebarParams(x=x_value, z=z_value, radius=radius)
        value = float(engine.objective(params.as_array()))
        values[ir] = value
        rows.append({
            "x_mm": x_value * 1000.0,
            "z_mm": z_value * 1000.0,
            "radius_mm": radius * 1000.0,
            "objective": value,
        })
    return values, rows


def _log_objective(values):
    finite = values[np.isfinite(values)]
    positive = finite[finite > 0.0]
    floor = 1e-16 if len(positive) == 0 else max(float(np.min(positive)) * 0.1, 1e-16)
    return np.log10(np.maximum(values, floor))


def _plot_heatmap(matrix, x_axis_m, y_axis_m, xlabel, ylabel, title, save_path,
                  point_specs, invert_y=True):
    x_mm = x_axis_m * 1000.0
    y_mm = y_axis_m * 1000.0
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(
        _log_objective(matrix),
        origin="lower",
        extent=[x_mm[0], x_mm[-1], y_mm[0], y_mm[-1]],
        aspect="auto",
        cmap="viridis",
    )
    for spec in point_specs:
        marker = spec.get("marker", "o")
        scatter_kwargs = {
            "marker": marker,
            "s": spec.get("size", 70),
            "color": spec.get("color", "white"),
            "linewidths": 1.0,
            "label": spec["label"],
        }
        if marker not in ("x", "+", "1", "2", "3", "4"):
            scatter_kwargs["edgecolors"] = spec.get("edgecolor", "black")
        ax.scatter(spec["x"], spec["y"], **scatter_kwargs)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if invert_y:
        ax.invert_yaxis()
    ax.legend(loc="best")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("log10 objective")
    fig.tight_layout()
    fig.savefig(save_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def _plot_radius_sweep(radius_values, objective_values, sweep_x, sweep_z,
                       true_params, initial_params, compare_params, save_path):
    fig, ax = plt.subplots(figsize=(8, 5))
    radius_mm = radius_values * 1000.0
    ax.plot(radius_mm, objective_values, marker="o", linewidth=1.8)
    ax.axvline(true_params.radius * 1000.0, color="black", linestyle="--", label="true")
    ax.axvline(initial_params.radius * 1000.0, color="tab:orange", linestyle=":", label="initial")
    if compare_params is not None:
        ax.axvline(compare_params.radius * 1000.0, color="tab:red", linestyle="-.", label="compare")
    ax.set_xlabel("Radius [mm]")
    ax.set_ylabel("Objective")
    ax.set_title(f"Radius sweep at x={sweep_x * 1000.0:.1f} mm, z={sweep_z * 1000.0:.1f} mm")
    ax.set_yscale("symlog", linthresh=1e-8)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(save_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def _min_record_xz(matrix, x_values, z_values, radius):
    iz, ix = np.unravel_index(np.nanargmin(matrix), matrix.shape)
    return {
        "objective": float(matrix[iz, ix]),
        "x_mm": float(x_values[ix] * 1000.0),
        "z_mm": float(z_values[iz] * 1000.0),
        "radius_mm": float(radius * 1000.0),
    }


def _min_record_zr(matrix, z_values, radius_values, x_value):
    iz, ir = np.unravel_index(np.nanargmin(matrix), matrix.shape)
    return {
        "objective": float(matrix[iz, ir]),
        "x_mm": float(x_value * 1000.0),
        "z_mm": float(z_values[iz] * 1000.0),
        "radius_mm": float(radius_values[ir] * 1000.0),
    }


def _min_record_radius(values, radius_values, x_value, z_value):
    ir = int(np.nanargmin(values))
    return {
        "objective": float(values[ir]),
        "x_mm": float(x_value * 1000.0),
        "z_mm": float(z_value * 1000.0),
        "radius_mm": float(radius_values[ir] * 1000.0),
    }


def main():
    truth = default_single_rebar_truth()
    initial = default_single_rebar_initial_guess()

    parser = argparse.ArgumentParser(description="Single-rebar objective landscape diagnostic")
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml", "auto"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=None,
                        help="Temporarily override DX=DZ for diagnostic runs")
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--sources", type=int, default=9)
    parser.add_argument("--scan-step-mm", type=float, default=None)
    parser.add_argument("--frequencies-ghz", type=_parse_frequency_list, default=[1.5e9])
    parser.add_argument("--outdir", default=None,
                        help="Output directory. Defaults to outputs/experiments/NNN_single_rebar_landscape")
    parser.add_argument("--run-name", default="single_rebar_landscape",
                        help="Name used when allocating a numbered output directory")

    parser.add_argument("--xz-count", type=int, default=13)
    parser.add_argument("--zr-count", type=int, default=13)
    parser.add_argument("--radius-count", type=int, default=17)
    parser.add_argument("--x-half-window-mm", type=float, default=70.0)
    parser.add_argument("--z-half-window-mm", type=float, default=45.0)
    parser.add_argument("--xz-center-x-mm", type=float, default=None,
                        help="Center x for x-z landscape; defaults to true x")
    parser.add_argument("--xz-center-z-mm", type=float, default=None,
                        help="Center z for x-z landscape; defaults to true z")
    parser.add_argument("--xz-radius-mm", type=float, default=None,
                        help="Fixed radius for x-z landscape; defaults to true radius")
    parser.add_argument("--zr-x-mm", type=float, default=None,
                        help="Fixed x for z-radius landscape; defaults to true x")
    parser.add_argument("--zr-center-z-mm", type=float, default=None,
                        help="Center z for z-radius landscape; defaults to true z")
    parser.add_argument("--radius-sweep-x-mm", type=float, default=None,
                        help="Fixed x for radius sweep; defaults to true x")
    parser.add_argument("--radius-sweep-z-mm", type=float, default=None,
                        help="Fixed z for radius sweep; defaults to true z")
    parser.add_argument("--radius-sweep-bounds-mm", type=_parse_mm_bounds, default=None)
    parser.add_argument("--progress-every", type=int, default=25)
    parser.add_argument("--log-every", type=int, default=100)

    parser.add_argument("--x-bounds-mm", type=_parse_mm_bounds, default=None)
    parser.add_argument("--z-bounds-mm", type=_parse_mm_bounds, default=None)
    parser.add_argument("--radius-bounds-mm", type=_parse_mm_bounds, default=None)

    parser.add_argument("--true-x-mm", type=float, default=truth.x * 1000.0)
    parser.add_argument("--true-z-mm", type=float, default=truth.z * 1000.0)
    parser.add_argument("--true-radius-mm", type=float, default=truth.radius * 1000.0)
    parser.add_argument("--init-x-mm", type=float, default=initial.x * 1000.0)
    parser.add_argument("--init-z-mm", type=float, default=initial.z * 1000.0)
    parser.add_argument("--init-radius-mm", type=float, default=initial.radius * 1000.0)
    parser.add_argument("--compare-summary-json", default=None)
    parser.add_argument("--compare-x-mm", type=float, default=None)
    parser.add_argument("--compare-z-mm", type=float, default=None)
    parser.add_argument("--compare-radius-mm", type=float, default=None)

    args = parser.parse_args()

    if args.xz_count < 2 or args.zr_count < 2 or args.radius_count < 2:
        raise ValueError("Grid counts must be at least 2")

    _override_grid(args.grid_step_mm)

    true_params = _params_from_args("true", args, truth)
    initial_params = _params_from_args("init", args, initial)
    compare_params = _load_compare_params(args.compare_summary_json)
    if any(value is not None for value in (args.compare_x_mm, args.compare_z_mm, args.compare_radius_mm)):
        if not all(value is not None for value in (args.compare_x_mm, args.compare_z_mm, args.compare_radius_mm)):
            raise ValueError("Set all compare-x-mm, compare-z-mm, and compare-radius-mm")
        compare_params = SingleRebarParams(
            x=args.compare_x_mm / 1000.0,
            z=args.compare_z_mm / 1000.0,
            radius=args.compare_radius_mm / 1000.0,
        )

    lower, upper = _bounds_from_args(args)
    xz_center_x = (args.xz_center_x_mm / 1000.0) if args.xz_center_x_mm is not None else true_params.x
    xz_center_z = (args.xz_center_z_mm / 1000.0) if args.xz_center_z_mm is not None else true_params.z
    xz_radius = (args.xz_radius_mm / 1000.0) if args.xz_radius_mm is not None else true_params.radius
    zr_x = (args.zr_x_mm / 1000.0) if args.zr_x_mm is not None else true_params.x
    zr_center_z = (args.zr_center_z_mm / 1000.0) if args.zr_center_z_mm is not None else true_params.z
    radius_sweep_x = (args.radius_sweep_x_mm / 1000.0) if args.radius_sweep_x_mm is not None else true_params.x
    radius_sweep_z = (args.radius_sweep_z_mm / 1000.0) if args.radius_sweep_z_mm is not None else true_params.z
    scan_step = None if args.scan_step_mm is None else args.scan_step_mm / 1000.0

    outdir = allocate_output_dir(args.outdir, args.run_name)
    print(f"Output directory: {outdir}")
    data_dir = os.path.join(outdir, "data")
    figures_dir = os.path.join(outdir, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    print("Building objective landscape engine...")
    engine = SingleRebarInversionEngine(
        true_params=true_params,
        initial_params=initial_params,
        frequencies=args.frequencies_ghz,
        n_sources=args.sources,
        scan_step=scan_step,
        backend=args.backend,
        parameter_bounds=(lower, upper),
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
        log_every=args.log_every,
    )

    print("\nEvaluating reference points...")
    point_rows = []
    true_j = _evaluate_point(engine, true_params, "true")
    point_rows.append({"label": "true", **true_params.as_mm(), "objective": true_j})
    initial_j = _evaluate_point(engine, initial_params, "initial")
    point_rows.append({"label": "initial", **initial_params.as_mm(), "objective": initial_j})
    compare_j = None
    if compare_params is not None:
        compare_j = _evaluate_point(engine, compare_params, "compare")
        point_rows.append({"label": "compare", **compare_params.as_mm(), "objective": compare_j})

    x_values = _axis_around(xz_center_x, args.x_half_window_mm, args.xz_count, lower[0], upper[0])
    z_values = _axis_around(xz_center_z, args.z_half_window_mm, args.xz_count, lower[1], upper[1])
    zr_z_values = _axis_around(zr_center_z, args.z_half_window_mm, args.zr_count, lower[1], upper[1])
    radius_values = _radius_axis(args, lower[2], upper[2])

    started = timer.time()
    print("\nSampling x-z landscape...")
    xz_objective, xz_rows = _sample_xz(
        engine,
        x_values,
        z_values,
        xz_radius,
        args.progress_every,
    )

    print("\nSampling z-radius landscape...")
    zr_objective, zr_rows = _sample_z_radius(
        engine,
        zr_z_values,
        radius_values,
        zr_x,
        args.progress_every,
    )

    print("\nSampling radius sweep...")
    radius_objective, radius_rows = _sample_radius(
        engine,
        radius_values,
        radius_sweep_x,
        radius_sweep_z,
    )
    elapsed = timer.time() - started

    np.savez(
        os.path.join(data_dir, "objective_landscape.npz"),
        x_values=x_values,
        z_values=z_values,
        zr_z_values=zr_z_values,
        radius_values=radius_values,
        xz_objective=xz_objective,
        zr_objective=zr_objective,
        radius_objective=radius_objective,
        true_params=true_params.as_array(),
        initial_params=initial_params.as_array(),
        compare_params=np.array([] if compare_params is None else compare_params.as_array()),
        slice_params=np.array([xz_center_x, xz_center_z, xz_radius, zr_x, zr_center_z, radius_sweep_x, radius_sweep_z], dtype=np.float64),
        grid=np.array([cfg.DX, cfg.DZ, cfg.NPML, cfg.NX, cfg.NZ, cfg.NT], dtype=np.float64),
        frequencies=np.array(args.frequencies_ghz, dtype=np.float64),
    )
    _write_long_csv(
        os.path.join(data_dir, "xz_landscape.csv"),
        xz_rows,
        ["x_mm", "z_mm", "radius_mm", "objective"],
    )
    _write_long_csv(
        os.path.join(data_dir, "z_radius_landscape.csv"),
        zr_rows,
        ["x_mm", "z_mm", "radius_mm", "objective"],
    )
    _write_long_csv(
        os.path.join(data_dir, "radius_sweep.csv"),
        radius_rows,
        ["x_mm", "z_mm", "radius_mm", "objective"],
    )
    _write_long_csv(
        os.path.join(data_dir, "point_comparison.csv"),
        point_rows,
        ["label", "x_mm", "z_mm", "radius_mm", "objective"],
    )

    xz_points = [
        {"label": "true", "x": true_params.x * 1000.0, "y": true_params.z * 1000.0, "marker": "*", "color": "white", "size": 140},
        {"label": "initial", "x": initial_params.x * 1000.0, "y": initial_params.z * 1000.0, "marker": "o", "color": "tab:orange"},
    ]
    zr_points = [
        {"label": "true", "x": true_params.radius * 1000.0, "y": true_params.z * 1000.0, "marker": "*", "color": "white", "size": 140},
        {"label": "initial", "x": initial_params.radius * 1000.0, "y": initial_params.z * 1000.0, "marker": "o", "color": "tab:orange"},
    ]
    if compare_params is not None:
        xz_points.append({"label": "compare", "x": compare_params.x * 1000.0, "y": compare_params.z * 1000.0, "marker": "x", "color": "tab:red", "size": 95})
        zr_points.append({"label": "compare", "x": compare_params.radius * 1000.0, "y": compare_params.z * 1000.0, "marker": "x", "color": "tab:red", "size": 95})

    _plot_heatmap(
        xz_objective,
        x_values,
        z_values,
        "x center [mm]",
        "z center [mm]",
        f"x-z objective at radius={xz_radius * 1000.0:.1f} mm",
        os.path.join(figures_dir, "xz_landscape.png"),
        xz_points,
        invert_y=True,
    )
    _plot_heatmap(
        zr_objective,
        radius_values,
        zr_z_values,
        "radius [mm]",
        "z center [mm]",
        f"z-radius objective at x={zr_x * 1000.0:.1f} mm",
        os.path.join(figures_dir, "z_radius_landscape.png"),
        zr_points,
        invert_y=True,
    )
    _plot_radius_sweep(
        radius_values,
        radius_objective,
        radius_sweep_x,
        radius_sweep_z,
        true_params,
        initial_params,
        compare_params,
        os.path.join(figures_dir, "radius_sweep.png"),
    )

    summary = {
        "backend": engine.backend,
        "sources": len(engine.scan_positions),
        "frequencies_ghz": [float(value / 1e9) for value in args.frequencies_ghz],
        "geometry_mode": args.geometry_mode,
        "subcell_samples": args.subcell_samples,
        "grid": {
            "dx_mm": cfg.DX * 1000.0,
            "dz_mm": cfg.DZ * 1000.0,
            "npml": cfg.NPML,
            "nx": cfg.NX,
            "nz": cfg.NZ,
            "nt": cfg.NT,
        },
        "elapsed_sampling_s": elapsed,
        "total_objective_evaluations": engine.eval_count,
        "true": {**true_params.as_mm(), "objective": true_j},
        "initial": {**initial_params.as_mm(), "objective": initial_j},
        "compare": None if compare_params is None else {**compare_params.as_mm(), "objective": compare_j},
        "bounds_mm": {
            "lower": SingleRebarParams.from_array(lower).as_mm(),
            "upper": SingleRebarParams.from_array(upper).as_mm(),
        },
        "slice_centers_mm": {
            "xz_center_x_mm": xz_center_x * 1000.0,
            "xz_center_z_mm": xz_center_z * 1000.0,
            "xz_radius_mm": xz_radius * 1000.0,
            "zr_x_mm": zr_x * 1000.0,
            "zr_center_z_mm": zr_center_z * 1000.0,
            "radius_sweep_x_mm": radius_sweep_x * 1000.0,
            "radius_sweep_z_mm": radius_sweep_z * 1000.0,
        },
        "xz_minimum": _min_record_xz(xz_objective, x_values, z_values, xz_radius),
        "z_radius_minimum": _min_record_zr(zr_objective, zr_z_values, radius_values, zr_x),
        "radius_sweep_minimum": _min_record_radius(radius_objective, radius_values, radius_sweep_x, radius_sweep_z),
    }
    with open(os.path.join(data_dir, "objective_landscape_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\nObjective landscape complete.")
    print(f"  Evaluations: {engine.eval_count}")
    print(f"  Sampling runtime: {elapsed:.1f} s")
    print(f"  x-z min: {summary['xz_minimum']}")
    print(f"  z-radius min: {summary['z_radius_minimum']}")
    print(f"  radius sweep min: {summary['radius_sweep_minimum']}")
    write_run_manifest(
        outdir,
        "single_rebar_objective_landscape",
        {
            "backend": engine.backend,
            "sources": len(engine.scan_positions),
            "frequencies_ghz": [float(value / 1e9) for value in args.frequencies_ghz],
            "grid_step_mm": cfg.DX * 1000.0,
            "geometry_mode": args.geometry_mode,
            "subcell_samples": args.subcell_samples,
            "summary_path": os.path.join(data_dir, "objective_landscape_summary.json"),
        },
    )
    print(f"  Saved outputs under {outdir}")


if __name__ == "__main__":
    main()

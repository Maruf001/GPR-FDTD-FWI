"""Radius-focused diagnostics for the one-rebar pipeline.

This is intentionally narrower than ``run_single_rebar_objective_landscape.py``:
it profiles radius at a fixed x/z location, with an optional z-radius grid.
Use it after a coarse-to-fine inversion has already found the rebar location.
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
        raise argparse.ArgumentTypeError("Use min,max in millimeters, e.g. 4,10") from exc
    if len(values) != 2 or values[0] >= values[1]:
        raise argparse.ArgumentTypeError("Bounds must be two increasing values: min,max")
    return values


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


def _params_from_args(prefix, args, default):
    x_mm = getattr(args, f"{prefix}_x_mm")
    z_mm = getattr(args, f"{prefix}_z_mm")
    radius_mm = getattr(args, f"{prefix}_radius_mm")
    return SingleRebarParams(
        x=(x_mm if x_mm is not None else default.x * 1000.0) / 1000.0,
        z=(z_mm if z_mm is not None else default.z * 1000.0) / 1000.0,
        radius=(radius_mm if radius_mm is not None else default.radius * 1000.0) / 1000.0,
    )


def _load_summary_params(path):
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


def _write_csv(path, rows, fieldnames):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _evaluate(engine, params, label):
    value = float(engine.objective(params.as_array()))
    print(
        f"  {label}: J={value:.6e}, "
        f"x={params.x * 1000.0:.3f} mm, "
        f"z={params.z * 1000.0:.3f} mm, "
        f"r={params.radius * 1000.0:.3f} mm"
    )
    return value


def _sample_radius(engine, x_m, z_m, radii_m):
    values = np.empty(len(radii_m), dtype=np.float64)
    rows = []
    started = timer.time()
    for i, radius_m in enumerate(radii_m):
        params = SingleRebarParams(x=x_m, z=z_m, radius=radius_m)
        value = float(engine.objective(params.as_array()))
        values[i] = value
        rows.append({
            "x_mm": x_m * 1000.0,
            "z_mm": z_m * 1000.0,
            "radius_mm": radius_m * 1000.0,
            "objective": value,
        })
        print(
            f"  radius sweep {i + 1}/{len(radii_m)}: "
            f"r={radius_m * 1000.0:.3f} mm, J={value:.6e}, "
            f"elapsed={timer.time() - started:.1f} s"
        )
    return values, rows


def _sample_z_radius(engine, x_m, z_values_m, radii_m, progress_every):
    matrix = np.empty((len(z_values_m), len(radii_m)), dtype=np.float64)
    rows = []
    count = 0
    total = len(z_values_m) * len(radii_m)
    started = timer.time()
    for iz, z_m in enumerate(z_values_m):
        for ir, radius_m in enumerate(radii_m):
            params = SingleRebarParams(x=x_m, z=z_m, radius=radius_m)
            value = float(engine.objective(params.as_array()))
            matrix[iz, ir] = value
            rows.append({
                "x_mm": x_m * 1000.0,
                "z_mm": z_m * 1000.0,
                "radius_mm": radius_m * 1000.0,
                "objective": value,
            })
            count += 1
            if progress_every and count % progress_every == 0:
                print(f"  z-radius grid: {count}/{total}, elapsed={timer.time() - started:.1f} s")
    return matrix, rows


def _minimum_1d(values, radii_m, x_m, z_m):
    index = int(np.nanargmin(values))
    return {
        "objective": float(values[index]),
        "x_mm": x_m * 1000.0,
        "z_mm": z_m * 1000.0,
        "radius_mm": float(radii_m[index] * 1000.0),
        "index": index,
    }


def _minimum_2d(matrix, z_values_m, radii_m, x_m):
    iz, ir = np.unravel_index(np.nanargmin(matrix), matrix.shape)
    return {
        "objective": float(matrix[iz, ir]),
        "x_mm": x_m * 1000.0,
        "z_mm": float(z_values_m[iz] * 1000.0),
        "radius_mm": float(radii_m[ir] * 1000.0),
        "z_index": int(iz),
        "radius_index": int(ir),
    }


def _quadratic_radius_estimate(values, radii_m):
    index = int(np.nanargmin(values))
    if index == 0 or index == len(values) - 1:
        return None
    x = radii_m[index - 1:index + 2] * 1000.0
    y = values[index - 1:index + 2]
    coeffs = np.polyfit(x, y, deg=2)
    a, b, c = coeffs
    if a <= 0:
        return None
    radius_mm = -b / (2.0 * a)
    if radius_mm < x[0] or radius_mm > x[-1]:
        return None
    objective = a * radius_mm**2 + b * radius_mm + c
    return {
        "radius_mm": float(radius_mm),
        "objective": float(objective),
        "quadratic_coefficients": [float(a), float(b), float(c)],
    }


def _plot_radius(path, radii_m, values, true_params, profile_params, compare_params):
    fig, ax = plt.subplots(figsize=(8, 5))
    radii_mm = radii_m * 1000.0
    ax.plot(radii_mm, values, marker="o", linewidth=1.8)
    ax.axvline(true_params.radius * 1000.0, color="black", linestyle="--", label="true")
    ax.axvline(profile_params.radius * 1000.0, color="tab:blue", linestyle=":", label="profile base")
    if compare_params is not None:
        ax.axvline(compare_params.radius * 1000.0, color="tab:red", linestyle="-.", label="compare")
    ax.set_xlabel("Radius [mm]")
    ax.set_ylabel("Objective")
    ax.set_title(
        f"Radius profile at x={profile_params.x * 1000.0:.1f} mm, "
        f"z={profile_params.z * 1000.0:.1f} mm"
    )
    ax.set_yscale("symlog", linthresh=1e-8)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def _plot_z_radius(path, matrix, z_values_m, radii_m, true_params, profile_params, compare_params):
    positive = matrix[np.isfinite(matrix) & (matrix > 0.0)]
    floor = 1e-16 if len(positive) == 0 else max(float(np.min(positive)) * 0.1, 1e-16)
    image = np.log10(np.maximum(matrix, floor))
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(
        image,
        origin="lower",
        extent=[radii_m[0] * 1000.0, radii_m[-1] * 1000.0, z_values_m[0] * 1000.0, z_values_m[-1] * 1000.0],
        aspect="auto",
        cmap="viridis",
    )
    ax.scatter(true_params.radius * 1000.0, true_params.z * 1000.0, marker="*", s=140, color="white", edgecolors="black", label="true")
    ax.scatter(profile_params.radius * 1000.0, profile_params.z * 1000.0, marker="o", s=70, color="tab:blue", edgecolors="black", label="profile base")
    if compare_params is not None:
        ax.scatter(compare_params.radius * 1000.0, compare_params.z * 1000.0, marker="x", s=95, color="tab:red", label="compare")
    ax.set_xlabel("Radius [mm]")
    ax.set_ylabel("z center [mm]")
    ax.set_title(f"z-radius profile at x={profile_params.x * 1000.0:.1f} mm")
    ax.invert_yaxis()
    ax.legend(loc="best")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("log10 objective")
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main():
    truth = default_single_rebar_truth()
    initial = default_single_rebar_initial_guess()

    parser = argparse.ArgumentParser(description="Single-rebar radius profile diagnostic")
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml", "auto"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=None)
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--scan-step-mm", type=float, default=None)
    parser.add_argument("--frequencies-ghz", type=_parse_frequency_list, default=[1.5e9])
    parser.add_argument("--run-name", default="single_rebar_radius_profile")
    parser.add_argument("--outdir", default=None)

    parser.add_argument("--radius-bounds-mm", type=_parse_mm_bounds, default=[4.0, 10.0])
    parser.add_argument("--radius-count", type=int, default=25)
    parser.add_argument("--z-half-window-mm", type=float, default=5.0)
    parser.add_argument("--z-count", type=int, default=0,
                        help="Set >0 to sample a z-radius grid")
    parser.add_argument("--progress-every", type=int, default=25)
    parser.add_argument("--log-every", type=int, default=100)

    parser.add_argument("--profile-x-mm", type=float, default=None)
    parser.add_argument("--profile-z-mm", type=float, default=None)
    parser.add_argument("--profile-radius-mm", type=float, default=None)
    parser.add_argument("--compare-summary-json", default=None)
    parser.add_argument("--x-bounds-mm", type=_parse_mm_bounds, default=None)
    parser.add_argument("--z-bounds-mm", type=_parse_mm_bounds, default=None)

    parser.add_argument("--true-x-mm", type=float, default=truth.x * 1000.0)
    parser.add_argument("--true-z-mm", type=float, default=truth.z * 1000.0)
    parser.add_argument("--true-radius-mm", type=float, default=truth.radius * 1000.0)
    parser.add_argument("--init-x-mm", type=float, default=initial.x * 1000.0)
    parser.add_argument("--init-z-mm", type=float, default=initial.z * 1000.0)
    parser.add_argument("--init-radius-mm", type=float, default=initial.radius * 1000.0)

    args = parser.parse_args()
    if args.radius_count < 2:
        raise ValueError("radius-count must be at least 2")
    if args.z_count < 0:
        raise ValueError("z-count must be >= 0")

    _override_grid(args.grid_step_mm)

    true_params = _params_from_args("true", args, truth)
    initial_params = _params_from_args("init", args, initial)
    compare_params = _load_summary_params(args.compare_summary_json)

    if args.profile_x_mm is not None or args.profile_z_mm is not None or args.profile_radius_mm is not None:
        if not all(value is not None for value in (args.profile_x_mm, args.profile_z_mm, args.profile_radius_mm)):
            raise ValueError("Set profile-x-mm, profile-z-mm, and profile-radius-mm together")
        profile_params = SingleRebarParams(
            x=args.profile_x_mm / 1000.0,
            z=args.profile_z_mm / 1000.0,
            radius=args.profile_radius_mm / 1000.0,
        )
    elif compare_params is not None:
        profile_params = compare_params
    else:
        profile_params = true_params

    lower, upper = _bounds_from_args(args)
    scan_step = None if args.scan_step_mm is None else args.scan_step_mm / 1000.0
    radii_m = np.linspace(args.radius_bounds_mm[0] / 1000.0, args.radius_bounds_mm[1] / 1000.0, args.radius_count)

    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = os.path.join(outdir, "data")
    figures_dir = os.path.join(outdir, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    print(f"Output directory: {outdir}")

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

    point_rows = []
    true_j = _evaluate(engine, true_params, "true")
    point_rows.append({"label": "true", **true_params.as_mm(), "objective": true_j})
    initial_j = _evaluate(engine, initial_params, "initial")
    point_rows.append({"label": "initial", **initial_params.as_mm(), "objective": initial_j})
    profile_j = _evaluate(engine, profile_params, "profile_base")
    point_rows.append({"label": "profile_base", **profile_params.as_mm(), "objective": profile_j})
    compare_j = None
    if compare_params is not None and compare_params != profile_params:
        compare_j = _evaluate(engine, compare_params, "compare")
        point_rows.append({"label": "compare", **compare_params.as_mm(), "objective": compare_j})

    started = timer.time()
    radius_values, radius_rows = _sample_radius(engine, profile_params.x, profile_params.z, radii_m)
    z_values_m = np.array([], dtype=np.float64)
    z_radius_matrix = np.empty((0, len(radii_m)), dtype=np.float64)
    z_radius_rows = []
    if args.z_count > 0:
        z_center_mm = profile_params.z * 1000.0
        z_lo_mm = max(lower[1] * 1000.0, z_center_mm - args.z_half_window_mm)
        z_hi_mm = min(upper[1] * 1000.0, z_center_mm + args.z_half_window_mm)
        z_values_m = np.linspace(z_lo_mm / 1000.0, z_hi_mm / 1000.0, args.z_count)
        z_radius_matrix, z_radius_rows = _sample_z_radius(
            engine,
            profile_params.x,
            z_values_m,
            radii_m,
            args.progress_every,
        )
    elapsed = timer.time() - started

    _write_csv(
        os.path.join(data_dir, "radius_profile.csv"),
        radius_rows,
        ["x_mm", "z_mm", "radius_mm", "objective"],
    )
    _write_csv(
        os.path.join(data_dir, "point_comparison.csv"),
        point_rows,
        ["label", "x_mm", "z_mm", "radius_mm", "objective"],
    )
    if z_radius_rows:
        _write_csv(
            os.path.join(data_dir, "z_radius_profile.csv"),
            z_radius_rows,
            ["x_mm", "z_mm", "radius_mm", "objective"],
        )

    radius_min = _minimum_1d(radius_values, radii_m, profile_params.x, profile_params.z)
    quadratic_min = _quadratic_radius_estimate(radius_values, radii_m)
    z_radius_min = None
    if z_radius_rows:
        z_radius_min = _minimum_2d(z_radius_matrix, z_values_m, radii_m, profile_params.x)

    np.savez(
        os.path.join(data_dir, "radius_profile.npz"),
        radius_values=radii_m,
        radius_objective=radius_values,
        z_values=z_values_m,
        z_radius_objective=z_radius_matrix,
        true_params=true_params.as_array(),
        initial_params=initial_params.as_array(),
        profile_params=profile_params.as_array(),
        compare_params=np.array([] if compare_params is None else compare_params.as_array()),
        grid=np.array([cfg.DX, cfg.DZ, cfg.NPML, cfg.NX, cfg.NZ, cfg.NT], dtype=np.float64),
        frequencies=np.array(args.frequencies_ghz, dtype=np.float64),
    )

    _plot_radius(
        os.path.join(figures_dir, "radius_profile.png"),
        radii_m,
        radius_values,
        true_params,
        profile_params,
        compare_params,
    )
    if z_radius_rows:
        _plot_z_radius(
            os.path.join(figures_dir, "z_radius_profile.png"),
            z_radius_matrix,
            z_values_m,
            radii_m,
            true_params,
            profile_params,
            compare_params,
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
        "profile_base": {**profile_params.as_mm(), "objective": profile_j},
        "compare": None if compare_params is None else {**compare_params.as_mm(), "objective": compare_j if compare_j is not None else profile_j},
        "bounds_mm": {
            "lower": SingleRebarParams.from_array(lower).as_mm(),
            "upper": SingleRebarParams.from_array(upper).as_mm(),
        },
        "radius_profile_minimum": radius_min,
        "quadratic_radius_minimum": quadratic_min,
        "z_radius_minimum": z_radius_min,
    }
    with open(os.path.join(data_dir, "radius_profile_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\nRadius profile complete.")
    print(f"  Evaluations: {engine.eval_count}")
    print(f"  Sampling runtime: {elapsed:.1f} s")
    print(f"  Radius min: {radius_min}")
    print(f"  Quadratic radius min: {quadratic_min}")
    if z_radius_min is not None:
        print(f"  z-radius min: {z_radius_min}")
    write_run_manifest(
        outdir,
        "single_rebar_radius_profile",
        {
            "backend": engine.backend,
            "sources": len(engine.scan_positions),
            "frequencies_ghz": [float(value / 1e9) for value in args.frequencies_ghz],
            "grid_step_mm": cfg.DX * 1000.0,
            "geometry_mode": args.geometry_mode,
            "subcell_samples": args.subcell_samples,
            "summary_path": os.path.join(data_dir, "radius_profile_summary.json"),
        },
    )
    print(f"  Saved outputs under {outdir}")


if __name__ == "__main__":
    main()

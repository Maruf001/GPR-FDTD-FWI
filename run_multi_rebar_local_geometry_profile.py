#!/usr/bin/env python3
"""Profile one target rebar's local x/z/r geometry in a multi-rebar scene."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time

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
from core.materials import MaterialModel  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from core.source import generate_time_array, ricker_wavelet  # noqa: E402
from inversion.adjoint import _build_mute_window  # noqa: E402
from inversion.frequency_weighting import radius_margin_from_ranked  # noqa: E402
from inversion.objective_variants import (  # noqa: E402
    apply_objective_variant,
    objective_variant_window,
    parse_objective_variants,
)
from inversion.source_profile import (  # noqa: E402
    source_profiled_ls,
    source_profiled_ls_over_basis_profiles,
)
from run_multi_rebar_common_radius_profile import (  # noqa: E402
    build_observed_cases,
    build_scan_positions,
    default_rebar_x_values_mm,
    default_rebar_z_values_mm,
    simulate_bscan,
)
from run_single_rebar_frequency_weight_matrix import parse_values_mm  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_source_profiled_polish import (  # noqa: E402
    observed_wavelet,
    ringdown_component_wavelet,
)
from run_single_rebar_source_profiled_replication import parse_replication_cases  # noqa: E402
from run_single_rebar_wavelet_mismatch import parse_positive_values, parse_shift_values_ps  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CASES = (
    "noise10_seed13:1.0,0.0,1.0,0.10,13|"
    "source_mismatch_noise10_seed13:1.1,-50.0,1.1,0.10,13"
)
DEFAULT_OBJECTIVE_VARIANTS = "base:1.0,7.0,0.3,none,none,0.0"


def parse_vector_mm(text):
    """Parse comma values or ranges while preserving vector order/duplicates."""
    values = []
    for item in str(text).split(","):
        item = item.strip()
        if not item:
            continue
        if ":" in item:
            parts = [float(part.strip()) for part in item.split(":") if part.strip()]
            if len(parts) != 3:
                raise argparse.ArgumentTypeError("ranges must use min:max:step")
            start, stop, step = parts
            if step <= 0.0 or start > stop:
                raise argparse.ArgumentTypeError("range requires positive step and start <= stop")
            count = int(np.floor((stop - start) / step + 1e-9)) + 1
            values.extend(round(float(start + step * idx), 10) for idx in range(count))
        else:
            values.append(round(float(item), 10))
    if not values:
        raise argparse.ArgumentTypeError("at least one value is required")
    return values


def truth_radius_values_for_run(common_radius_mm, radius_values_mm, target_count):
    """Resolve common or per-target truth radii for the synthetic observed model."""
    if radius_values_mm is None:
        return [float(common_radius_mm)] * int(target_count)
    values = [float(value) for value in radius_values_mm]
    if len(values) != int(target_count):
        raise ValueError("truth radius values must match truth x/z value count")
    return values


def candidate_rebar_arrays(
        base_x_mm,
        base_z_mm,
        truth_radius_mm,
        target_index,
        target_x_mm,
        target_z_mm,
        target_radius_mm):
    """Return x/z/r arrays for one target-rebar local geometry candidate."""
    base_radii_mm = [float(truth_radius_mm)] * len(base_x_mm)
    return candidate_rebar_arrays_from_base(
        base_x_mm,
        base_z_mm,
        base_radii_mm,
        target_index,
        target_x_mm,
        target_z_mm,
        target_radius_mm,
    )


def candidate_rebar_arrays_from_base(
        base_x_mm,
        base_z_mm,
        base_radii_mm,
        target_index,
        target_x_mm,
        target_z_mm,
        target_radius_mm):
    """Return x/z/r arrays while preserving non-target current radii."""
    if len(base_x_mm) != len(base_z_mm):
        raise ValueError("base x and z lists must have the same length")
    if len(base_x_mm) != len(base_radii_mm):
        raise ValueError("base x, z, and radius lists must have the same length")
    if target_index < 0 or target_index >= len(base_x_mm):
        raise ValueError("target_index must be a valid zero-based rebar index")
    x_values = [float(value) for value in base_x_mm]
    z_values = [float(value) for value in base_z_mm]
    radii = [float(value) for value in base_radii_mm]
    x_values[int(target_index)] = float(target_x_mm)
    z_values[int(target_index)] = float(target_z_mm)
    radii[int(target_index)] = float(target_radius_mm)
    return x_values, z_values, radii


def build_variable_geometry_model(
        x_values_mm,
        z_values_mm,
        radii_mm,
        geometry_mode="hard",
        subcell_samples=5,
        concrete_epsr=cfg.CONCRETE_EPSR,
        concrete_sigma=cfg.CONCRETE_SIGMA,
        rebar_epsr=cfg.REBAR_EPSR,
        rebar_sigma=cfg.REBAR_SIGMA):
    """Build a multi-rebar model from per-rebar geometry and material values."""
    if len(x_values_mm) != len(z_values_mm) or len(x_values_mm) != len(radii_mm):
        raise ValueError("x, z, and radius lists must have the same length")

    model = MaterialModel(
        cfg.NZ,
        cfg.NX,
        eps_r_bg=cfg.AIR_EPSR,
        sigma_bg=cfg.AIR_SIGMA,
        mu_r_bg=cfg.MU_R,
    )
    iz_concrete_top = int(np.round(cfg.CONCRETE_TOP / cfg.DZ)) + cfg.NPML
    model.set_region(
        slice(iz_concrete_top, cfg.NZ),
        slice(0, cfg.NX),
        eps_r=float(concrete_epsr),
        sigma=float(concrete_sigma),
    )

    for x_mm, z_mm, radius_mm in zip(x_values_mm, z_values_mm, radii_mm):
        if geometry_mode == "hard":
            model.add_circle(
                z_center_m=float(z_mm) / 1000.0,
                x_center_m=float(x_mm) / 1000.0,
                radius_m=float(radius_mm) / 1000.0,
                eps_r=float(rebar_epsr),
                sigma=float(rebar_sigma),
                dz=cfg.DZ,
                dx=cfg.DX,
                npml=cfg.NPML,
            )
        elif geometry_mode == "subcell":
            model.add_circle_subcell(
                z_center_m=float(z_mm) / 1000.0,
                x_center_m=float(x_mm) / 1000.0,
                radius_m=float(radius_mm) / 1000.0,
                eps_r=float(rebar_epsr),
                sigma=float(rebar_sigma),
                dz=cfg.DZ,
                dx=cfg.DX,
                npml=cfg.NPML,
                samples=subcell_samples,
            )
        else:
            raise ValueError(f"Unsupported geometry_mode: {geometry_mode}")
    return model


def _candidate_case_result(candidate, case_label, objective_label=None):
    if objective_label is not None and "objective_results" in candidate:
        return candidate["objective_results"][case_label][objective_label]
    return candidate["case_results"][case_label]


def rank_case(candidates, case_label, top_k=None, objective_label=None):
    ranked = []
    for candidate in candidates:
        result = _candidate_case_result(candidate, case_label, objective_label)
        ranked.append({
            "misfit": float(result["misfit"]),
            "params": dict(candidate["params"]),
            "source_profile": dict(result["source_profile"]),
        })
    ranked.sort(key=lambda item: item["misfit"])
    if top_k is None:
        return ranked
    return ranked[:max(0, int(top_k))]


def best_curve_by_radius(candidates, case_label, objective_label=None):
    best = {}
    for candidate in candidates:
        radius = float(candidate["params"]["radius_mm"])
        result = _candidate_case_result(candidate, case_label, objective_label)
        current = best.get(radius)
        if current is None or result["misfit"] < current["misfit"]:
            best[radius] = {
                "radius_mm": radius,
                "misfit": float(result["misfit"]),
                "params": dict(candidate["params"]),
                "source_profile": dict(result["source_profile"]),
            }
    return [best[radius] for radius in sorted(best)]


def evaluate_local_geometry_grid(
        observed_by_case,
        base_x_mm,
        base_z_mm,
        truth_radius_mm,
        target_index,
        target_x_values_mm,
        target_z_values_mm,
        target_radius_values_mm,
        base_radii_mm,
        frequency_hz,
        modeled_frequency_scales,
        time_shift_values_s,
        scan_positions,
        time_values,
        mute,
        backend,
        geometry_mode="hard",
        subcell_samples=5,
        fit_amplitude=True,
        fit_ringdown_coefficient=False,
        source_ringdown_delay_ps=180.0,
        source_ringdown_frequency_scale=0.8,
        concrete_epsr=cfg.CONCRETE_EPSR,
        concrete_sigma=cfg.CONCRETE_SIGMA,
        rebar_epsr=cfg.REBAR_EPSR,
        rebar_sigma=cfg.REBAR_SIGMA,
        objective_variants=None,
        progress_every=25):
    variants = list(objective_variants or [])
    observed_objective_by_case = {}
    variant_mute_by_label = {}
    if variants:
        variant_mute_by_label = {
            variant.label: objective_variant_window(variant, len(time_values), cfg.DT)
            for variant in variants
        }
        for label, observed in observed_by_case.items():
            observed_objective_by_case[label] = {
                variant.label: apply_objective_variant(observed, variant, cfg.DT)
                for variant in variants
            }
    else:
        observed_objective_by_case = {
            label: np.asarray(observed, dtype=np.float64)
            for label, observed in observed_by_case.items()
        }
    if base_radii_mm is None:
        base_radii_mm = [float(truth_radius_mm)] * len(base_x_mm)
    candidates = []
    total = len(target_x_values_mm) * len(target_z_values_mm) * len(target_radius_values_mm)
    started = time.time()
    count = 0
    for x_mm in target_x_values_mm:
        for z_mm in target_z_values_mm:
            for radius_mm in target_radius_values_mm:
                x_values, z_values, radii = candidate_rebar_arrays_from_base(
                    base_x_mm,
                    base_z_mm,
                    base_radii_mm,
                    target_index,
                    x_mm,
                    z_mm,
                    radius_mm,
                )
                model = build_variable_geometry_model(
                    x_values,
                    z_values,
                    radii,
                    geometry_mode=geometry_mode,
                    subcell_samples=subcell_samples,
                    concrete_epsr=concrete_epsr,
                    concrete_sigma=concrete_sigma,
                    rebar_epsr=rebar_epsr,
                    rebar_sigma=rebar_sigma,
                )
                synthetic_by_scale = {}
                basis_by_scale = {}
                for scale in modeled_frequency_scales:
                    if fit_ringdown_coefficient:
                        primary_wavelet = observed_wavelet(
                            time_values,
                            frequency_hz,
                            frequency_scale=float(scale),
                            time_shift_ps=0.0,
                            amplitude_scale=1.0,
                            ringdown_scale=0.0,
                            ringdown_delay_ps=float(source_ringdown_delay_ps),
                            ringdown_frequency_scale=float(source_ringdown_frequency_scale),
                        )
                        ringdown_wavelet = ringdown_component_wavelet(
                            time_values,
                            frequency_hz,
                            frequency_scale=float(scale),
                            time_shift_ps=0.0,
                            ringdown_delay_ps=float(source_ringdown_delay_ps),
                            ringdown_frequency_scale=float(source_ringdown_frequency_scale),
                        )
                        primary = simulate_bscan(
                            model,
                            primary_wavelet,
                            scan_positions,
                            backend,
                        )
                        ringdown = simulate_bscan(
                            model,
                            ringdown_wavelet,
                            scan_positions,
                            backend,
                        )
                        basis_by_scale[float(scale)] = (primary, ringdown)
                    else:
                        wavelet = ricker_wavelet(time_values, frequency_hz * float(scale))
                        synthetic_by_scale[float(scale)] = simulate_bscan(
                            model,
                            wavelet,
                            scan_positions,
                            backend,
                        )

                case_results = {}
                objective_results = {}
                if variants:
                    if fit_ringdown_coefficient:
                        basis_by_variant = {
                            variant.label: [
                                {
                                    "frequency_scale": float(scale),
                                    "ringdown_delay_s": float(source_ringdown_delay_ps) * 1e-12,
                                    "ringdown_frequency_scale": float(source_ringdown_frequency_scale),
                                    "basis_traces": [
                                        apply_objective_variant(primary, variant, cfg.DT),
                                        apply_objective_variant(ringdown, variant, cfg.DT),
                                    ],
                                }
                                for scale, (primary, ringdown) in basis_by_scale.items()
                            ]
                            for variant in variants
                        }
                    else:
                        synthetic_by_variant = {
                            variant.label: {
                                scale: apply_objective_variant(synthetic, variant, cfg.DT)
                                for scale, synthetic in synthetic_by_scale.items()
                            }
                            for variant in variants
                        }
                    primary_label = variants[0].label
                    for label, observed_by_variant in observed_objective_by_case.items():
                        objective_results[label] = {}
                        for variant in variants:
                            if fit_ringdown_coefficient:
                                profile = source_profiled_ls_over_basis_profiles(
                                    observed_by_variant[variant.label],
                                    basis_by_variant[variant.label],
                                    variant_mute_by_label[variant.label],
                                    cfg.DT,
                                    time_shift_values_s=time_shift_values_s,
                                )
                            else:
                                profile = source_profiled_ls(
                                    observed_by_variant[variant.label],
                                    synthetic_by_variant[variant.label],
                                    variant_mute_by_label[variant.label],
                                    cfg.DT,
                                    time_shift_values_s=time_shift_values_s,
                                    fit_amplitude=fit_amplitude,
                                )
                            objective_results[label][variant.label] = {
                                "misfit": float(profile.misfit),
                                "source_profile": profile.as_dict(),
                            }
                        case_results[label] = objective_results[label][primary_label]
                else:
                    for label, observed in observed_objective_by_case.items():
                        if fit_ringdown_coefficient:
                            basis_profiles = [
                                {
                                    "frequency_scale": float(scale),
                                    "ringdown_delay_s": float(source_ringdown_delay_ps) * 1e-12,
                                    "ringdown_frequency_scale": float(source_ringdown_frequency_scale),
                                    "basis_traces": [primary, ringdown],
                                }
                                for scale, (primary, ringdown) in basis_by_scale.items()
                            ]
                            profile = source_profiled_ls_over_basis_profiles(
                                observed,
                                basis_profiles,
                                mute,
                                cfg.DT,
                                time_shift_values_s=time_shift_values_s,
                            )
                        else:
                            profile = source_profiled_ls(
                                observed,
                                synthetic_by_scale,
                                mute,
                                cfg.DT,
                                time_shift_values_s=time_shift_values_s,
                                fit_amplitude=fit_amplitude,
                            )
                        case_results[label] = {
                            "misfit": float(profile.misfit),
                            "source_profile": profile.as_dict(),
                        }

                candidate = {
                    "params": {
                        "x_mm": float(x_mm),
                        "z_mm": float(z_mm),
                        "radius_mm": float(radius_mm),
                        "target_index": int(target_index),
                        "x_values_mm": [float(value) for value in x_values],
                        "z_values_mm": [float(value) for value in z_values],
                        "radii_mm": [float(value) for value in radii],
                    },
                    "case_results": case_results,
                    "material": {
                        "concrete_epsr": float(concrete_epsr),
                        "concrete_sigma": float(concrete_sigma),
                        "rebar_epsr": float(rebar_epsr),
                        "rebar_sigma": float(rebar_sigma),
                        "rebar_log10_sigma": float(np.log10(rebar_sigma)),
                    },
                }
                if variants:
                    candidate["objective_results"] = objective_results
                candidates.append(candidate)
                count += 1
                if progress_every and (count == 1 or count % int(progress_every) == 0):
                    elapsed = time.time() - started
                    print(f"  Multi-rebar local geometry profile: {count}/{total}, elapsed={elapsed:.1f} s")
    return candidates


def build_objective_results(candidates, case_labels, objective_labels, top_k):
    results = {}
    for label in case_labels:
        results[label] = {}
        for objective_label in objective_labels:
            ranked = rank_case(candidates, label, objective_label=objective_label)
            results[label][objective_label] = {
                "margin": radius_margin_from_ranked(ranked),
                "top_candidates": ranked[:top_k],
                "best_curve_by_radius": best_curve_by_radius(
                    candidates,
                    label,
                    objective_label=objective_label,
                ),
            }
    return results


def write_candidate_csv(path, candidates, case_labels):
    fieldnames = [
        "case_label",
        "misfit",
        "target_index",
        "x_mm",
        "z_mm",
        "radius_mm",
        "x_values_mm",
        "z_values_mm",
        "radii_mm",
        "source_frequency_scale",
        "source_time_shift_ps",
        "source_amplitude_scale",
        "source_ringdown_scale",
        "source_ringdown_delay_ps",
        "source_ringdown_frequency_scale",
        "source_primary_coefficient",
        "source_ringdown_coefficient",
    ]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for candidate in candidates:
            params = candidate["params"]
            for label in case_labels:
                result = candidate["case_results"][label]
                profile = result["source_profile"]
                writer.writerow({
                    "case_label": label,
                    "misfit": result["misfit"],
                    "target_index": params["target_index"],
                    "x_mm": params["x_mm"],
                    "z_mm": params["z_mm"],
                    "radius_mm": params["radius_mm"],
                    "x_values_mm": json.dumps(params["x_values_mm"]),
                    "z_values_mm": json.dumps(params["z_values_mm"]),
                    "radii_mm": json.dumps(params["radii_mm"]),
                    "source_frequency_scale": profile["frequency_scale"],
                    "source_time_shift_ps": profile["time_shift_ps"],
                    "source_amplitude_scale": profile["amplitude_scale"],
                    "source_ringdown_scale": profile.get("ringdown_scale", 0.0),
                    "source_ringdown_delay_ps": profile.get("ringdown_delay_ps", 0.0),
                    "source_ringdown_frequency_scale": profile.get("ringdown_frequency_scale", 1.0),
                    "source_primary_coefficient": profile.get("primary_coefficient", profile["amplitude_scale"]),
                    "source_ringdown_coefficient": profile.get("ringdown_coefficient", 0.0),
                })


def write_case_summary_csv(path, results):
    fieldnames = [
        "case_label",
        "best_x_mm",
        "best_z_mm",
        "best_radius_mm",
        "next_radius_mm",
        "radius_margin_abs",
        "best_misfit",
        "best_source_frequency_scale",
        "best_source_time_shift_ps",
        "best_source_amplitude_scale",
        "best_source_ringdown_scale",
        "best_source_ringdown_delay_ps",
        "best_source_ringdown_frequency_scale",
        "best_source_primary_coefficient",
        "best_source_ringdown_coefficient",
    ]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for label, result in results.items():
            best = result["top_candidates"][0]
            params = best["params"]
            profile = best["source_profile"]
            margin = result["margin"]
            writer.writerow({
                "case_label": label,
                "best_x_mm": params["x_mm"],
                "best_z_mm": params["z_mm"],
                "best_radius_mm": margin["best_radius_mm"],
                "next_radius_mm": margin["next_radius_mm"],
                "radius_margin_abs": margin["radius_margin_abs"],
                "best_misfit": margin["best_radius_misfit"],
                "best_source_frequency_scale": profile["frequency_scale"],
                "best_source_time_shift_ps": profile["time_shift_ps"],
                "best_source_amplitude_scale": profile["amplitude_scale"],
                "best_source_ringdown_scale": profile.get("ringdown_scale", 0.0),
                "best_source_ringdown_delay_ps": profile.get("ringdown_delay_ps", 0.0),
                "best_source_ringdown_frequency_scale": profile.get("ringdown_frequency_scale", 1.0),
                "best_source_primary_coefficient": profile.get("primary_coefficient", profile.get("amplitude_scale")),
                "best_source_ringdown_coefficient": profile.get("ringdown_coefficient", 0.0),
            })


def write_objective_summary_csv(path, objective_results):
    fieldnames = [
        "case_label",
        "objective_label",
        "best_x_mm",
        "best_z_mm",
        "best_radius_mm",
        "next_radius_mm",
        "radius_margin_abs",
        "radius_margin_rel",
        "best_misfit",
        "best_source_frequency_scale",
        "best_source_time_shift_ps",
        "best_source_amplitude_scale",
        "best_source_ringdown_scale",
        "best_source_ringdown_delay_ps",
        "best_source_ringdown_frequency_scale",
        "best_source_primary_coefficient",
        "best_source_ringdown_coefficient",
    ]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for case_label, by_objective in objective_results.items():
            for objective_label, result in by_objective.items():
                best = result["top_candidates"][0]
                params = best["params"]
                profile = best["source_profile"]
                margin = result["margin"]
                writer.writerow({
                    "case_label": case_label,
                    "objective_label": objective_label,
                    "best_x_mm": params["x_mm"],
                    "best_z_mm": params["z_mm"],
                    "best_radius_mm": margin["best_radius_mm"],
                    "next_radius_mm": margin["next_radius_mm"],
                    "radius_margin_abs": margin["radius_margin_abs"],
                    "radius_margin_rel": margin["radius_margin_rel"],
                    "best_misfit": margin["best_radius_misfit"],
                    "best_source_frequency_scale": profile["frequency_scale"],
                    "best_source_time_shift_ps": profile["time_shift_ps"],
                    "best_source_amplitude_scale": profile["amplitude_scale"],
                    "best_source_ringdown_scale": profile.get("ringdown_scale", 0.0),
                    "best_source_ringdown_delay_ps": profile.get("ringdown_delay_ps", 0.0),
                    "best_source_ringdown_frequency_scale": profile.get("ringdown_frequency_scale", 1.0),
                    "best_source_primary_coefficient": profile.get("primary_coefficient", profile.get("amplitude_scale")),
                    "best_source_ringdown_coefficient": profile.get("ringdown_coefficient", 0.0),
                })


def write_objective_candidate_csv(path, candidates, case_labels, objective_labels):
    fieldnames = [
        "case_label",
        "objective_label",
        "misfit",
        "target_index",
        "x_mm",
        "z_mm",
        "radius_mm",
        "x_values_mm",
        "z_values_mm",
        "radii_mm",
        "source_frequency_scale",
        "source_time_shift_ps",
        "source_amplitude_scale",
        "source_ringdown_scale",
        "source_ringdown_delay_ps",
        "source_ringdown_frequency_scale",
        "source_primary_coefficient",
        "source_ringdown_coefficient",
    ]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for candidate in candidates:
            params = candidate["params"]
            for case_label in case_labels:
                for objective_label in objective_labels:
                    result = _candidate_case_result(candidate, case_label, objective_label)
                    profile = result["source_profile"]
                    writer.writerow({
                        "case_label": case_label,
                        "objective_label": objective_label,
                        "misfit": result["misfit"],
                        "target_index": params["target_index"],
                        "x_mm": params["x_mm"],
                        "z_mm": params["z_mm"],
                        "radius_mm": params["radius_mm"],
                        "x_values_mm": json.dumps(params["x_values_mm"]),
                        "z_values_mm": json.dumps(params["z_values_mm"]),
                        "radii_mm": json.dumps(params["radii_mm"]),
                        "source_frequency_scale": profile["frequency_scale"],
                        "source_time_shift_ps": profile["time_shift_ps"],
                        "source_amplitude_scale": profile["amplitude_scale"],
                        "source_ringdown_scale": profile.get("ringdown_scale", 0.0),
                        "source_ringdown_delay_ps": profile.get("ringdown_delay_ps", 0.0),
                        "source_ringdown_frequency_scale": profile.get("ringdown_frequency_scale", 1.0),
                        "source_primary_coefficient": profile.get("primary_coefficient", profile["amplitude_scale"]),
                        "source_ringdown_coefficient": profile.get("ringdown_coefficient", 0.0),
                    })


def plot_radius_profiles(results, save_path):
    fig, ax = plt.subplots(figsize=(9.4, 5.3), constrained_layout=True)
    for label, result in results.items():
        curve = result["best_curve_by_radius"]
        radii = [item["radius_mm"] for item in curve]
        values = [item["misfit"] for item in curve]
        ax.plot(radii, values, marker="o", linewidth=1.6, markersize=3.8, label=label)
    ax.set_title("Multi-Rebar Local Geometry Radius Profile")
    ax.set_xlabel("Target rebar radius [mm]")
    ax.set_ylabel("Best objective over target x/z/source profile")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="best", fontsize=8)
    save_validated_figure(fig, save_path)
    plt.close(fig)


def plot_objective_variant_radius_profiles(objective_results, save_path):
    case_labels = list(objective_results)
    if not case_labels:
        return None
    fig, axes = plt.subplots(
        len(case_labels),
        1,
        figsize=(10.8, max(4.0, 3.6 * len(case_labels))),
        constrained_layout=True,
        squeeze=False,
    )
    for row, case_label in enumerate(case_labels):
        ax = axes[row, 0]
        for objective_label, result in objective_results[case_label].items():
            curve = result["best_curve_by_radius"]
            radii = [item["radius_mm"] for item in curve]
            values = [item["misfit"] for item in curve]
            ax.plot(
                radii,
                values,
                marker="o",
                linewidth=1.4,
                markersize=3.4,
                label=objective_label,
            )
        ax.set_title(case_label, fontsize=11, fontweight="bold")
        ax.set_xlabel("Target rebar radius [mm]")
        ax.set_ylabel("Best objective over x/z/source")
        ax.grid(True, alpha=0.25)
        ax.legend(loc="best", fontsize=8, ncols=2)
    fig.suptitle("Radius Evidence By Objective Variant", fontsize=13, fontweight="bold")
    save_validated_figure(fig, save_path)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument("--rebar-x-values-mm", type=parse_vector_mm, default=default_rebar_x_values_mm())
    parser.add_argument("--rebar-z-values-mm", type=parse_vector_mm, default=default_rebar_z_values_mm())
    parser.add_argument("--rebar-radius-values-mm", type=parse_vector_mm, default=None)
    parser.add_argument("--truth-x-values-mm", type=parse_vector_mm, default=None)
    parser.add_argument("--truth-z-values-mm", type=parse_vector_mm, default=None)
    parser.add_argument("--truth-radius-mm", type=float, default=cfg.REBAR_RADIUS * 1000.0)
    parser.add_argument("--truth-radius-values-mm", type=parse_vector_mm, default=None)
    parser.add_argument("--target-rebar-index", type=int, default=0)
    parser.add_argument("--target-x-values-mm", type=parse_values_mm, default=parse_values_mm("148:152:1"))
    parser.add_argument("--target-z-values-mm", type=parse_values_mm, default=parse_values_mm("88:92:1"))
    parser.add_argument("--target-radius-values-mm", type=parse_values_mm, default=parse_values_mm("5.4:7.8:0.2"))
    parser.add_argument("--replication-cases", type=parse_replication_cases, default=parse_replication_cases(DEFAULT_CASES))
    parser.add_argument("--source-frequency-scales", type=parse_positive_values, default=parse_positive_values("0.9,1.0,1.1"))
    parser.add_argument("--source-time-shift-ps-values", type=parse_shift_values_ps, default=parse_shift_values_ps("-80,-50,-25,0,25,50,80"))
    parser.add_argument("--source-ringdown-delay-ps", type=float, default=180.0)
    parser.add_argument("--source-ringdown-frequency-scale", type=float, default=0.8)
    parser.add_argument("--fit-ringdown-coefficient", action="store_true")
    parser.add_argument("--objective-variants", type=parse_objective_variants, default=parse_objective_variants(DEFAULT_OBJECTIVE_VARIANTS))
    parser.set_defaults(fit_amplitude=True)
    parser.add_argument("--no-fit-amplitude", dest="fit_amplitude", action="store_false")
    parser.add_argument("--top-k", type=int, default=12)
    parser.add_argument("--progress-every", type=int, default=25)
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--run-name", default="multi_rebar_local_geometry_profile")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    _override_grid(args.grid_step_mm)
    base_radii_mm = (
        [args.truth_radius_mm] * len(args.rebar_x_values_mm)
        if args.rebar_radius_values_mm is None
        else args.rebar_radius_values_mm
    )
    if len(base_radii_mm) != len(args.rebar_x_values_mm):
        raise ValueError("rebar radius list must match the rebar x/z list length")
    truth_x_values_mm = (
        args.rebar_x_values_mm
        if args.truth_x_values_mm is None
        else args.truth_x_values_mm
    )
    truth_z_values_mm = (
        args.rebar_z_values_mm
        if args.truth_z_values_mm is None
        else args.truth_z_values_mm
    )
    if len(truth_x_values_mm) != len(truth_z_values_mm):
        raise ValueError("truth x and z lists must have the same length")
    if len(truth_x_values_mm) != len(args.rebar_x_values_mm):
        raise ValueError("truth and candidate rebar lists must have the same length")
    candidate_rebar_arrays(
        args.rebar_x_values_mm,
        args.rebar_z_values_mm,
        args.truth_radius_mm,
        args.target_rebar_index,
        args.target_x_values_mm[0],
        args.target_z_values_mm[0],
        args.target_radius_values_mm[0],
    )

    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = os.path.join(outdir, "data")
    figures_dir = os.path.join(outdir, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    print(f"Output directory: {outdir}")

    frequency_hz = args.frequency_ghz * 1e9
    time_values = generate_time_array(cfg.NT, cfg.DT)
    mute = _build_mute_window(cfg.NT, cfg.DT)
    scan_positions, scan_x = build_scan_positions(cfg.INVERSION_SCAN_STEP, args.sources)
    truth_radii = truth_radius_values_for_run(
        args.truth_radius_mm,
        args.truth_radius_values_mm,
        len(truth_x_values_mm),
    )
    true_model = build_variable_geometry_model(
        truth_x_values_mm,
        truth_z_values_mm,
        truth_radii,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
    )
    observed_by_case, case_metadata = build_observed_cases(
        true_model,
        time_values,
        frequency_hz,
        scan_positions,
        args.backend,
        args.replication_cases,
    )

    started = time.time()
    candidates = evaluate_local_geometry_grid(
        observed_by_case,
        args.rebar_x_values_mm,
        args.rebar_z_values_mm,
        args.truth_radius_mm,
        args.target_rebar_index,
        args.target_x_values_mm,
        args.target_z_values_mm,
        args.target_radius_values_mm,
        base_radii_mm,
        frequency_hz,
        args.source_frequency_scales,
        [value * 1e-12 for value in args.source_time_shift_ps_values],
        scan_positions,
        time_values,
        mute,
        args.backend,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
        fit_amplitude=args.fit_amplitude,
        fit_ringdown_coefficient=args.fit_ringdown_coefficient,
        source_ringdown_delay_ps=args.source_ringdown_delay_ps,
        source_ringdown_frequency_scale=args.source_ringdown_frequency_scale,
        objective_variants=args.objective_variants,
        progress_every=args.progress_every,
    )
    elapsed = time.time() - started

    case_labels = [case["label"] for case in args.replication_cases]
    objective_labels = [variant.label for variant in args.objective_variants]
    objective_results = build_objective_results(
        candidates,
        case_labels,
        objective_labels,
        args.top_k,
    )
    results = {}
    for label in case_labels:
        results[label] = objective_results[label][objective_labels[0]]

    candidate_csv = os.path.join(data_dir, "multi_rebar_local_geometry_candidates.csv")
    case_summary_csv = os.path.join(data_dir, "multi_rebar_local_geometry_case_summary.csv")
    objective_candidate_csv = os.path.join(data_dir, "multi_rebar_local_geometry_objective_candidates.csv")
    objective_summary_csv = os.path.join(data_dir, "multi_rebar_local_geometry_objective_summary.csv")
    plot_path = os.path.join(figures_dir, "multi_rebar_local_geometry_radius_profiles.png")
    objective_plot_path = os.path.join(figures_dir, "multi_rebar_objective_variant_radius_profiles.png")
    write_candidate_csv(candidate_csv, candidates, case_labels)
    write_case_summary_csv(case_summary_csv, results)
    write_objective_candidate_csv(
        objective_candidate_csv,
        candidates,
        case_labels,
        objective_labels,
    )
    write_objective_summary_csv(objective_summary_csv, objective_results)
    plot_radius_profiles(results, plot_path)
    plot_objective_variant_radius_profiles(objective_results, objective_plot_path)

    summary = {
        "run_name": args.run_name,
        "backend": args.backend,
        "grid_step_mm": args.grid_step_mm,
        "sources": args.sources,
        "frequency_ghz": args.frequency_ghz,
        "rebar_x_values_mm": args.rebar_x_values_mm,
        "rebar_z_values_mm": args.rebar_z_values_mm,
        "rebar_radius_values_mm": base_radii_mm,
        "truth_x_values_mm": truth_x_values_mm,
        "truth_z_values_mm": truth_z_values_mm,
        "truth_radius_mm": args.truth_radius_mm,
        "truth_radius_values_mm": truth_radii,
        "target_rebar_index": args.target_rebar_index,
        "target_x_values_mm": args.target_x_values_mm,
        "target_z_values_mm": args.target_z_values_mm,
        "target_radius_values_mm": args.target_radius_values_mm,
        "replication_cases": args.replication_cases,
        "case_metadata": case_metadata,
        "source_profile_grid": {
            "frequency_scales": args.source_frequency_scales,
            "time_shift_ps_values": args.source_time_shift_ps_values,
            "fit_amplitude": bool(args.fit_amplitude),
            "fit_ringdown_coefficient": bool(args.fit_ringdown_coefficient),
            "ringdown_delay_ps": float(args.source_ringdown_delay_ps),
            "ringdown_frequency_scale": float(args.source_ringdown_frequency_scale),
        },
        "objective_variants": [variant.as_dict() for variant in args.objective_variants],
        "primary_objective_label": objective_labels[0],
        "elapsed_time_s": float(elapsed),
        "candidate_count": len(candidates),
        "case_count": len(case_labels),
        "results": results,
        "objective_results": objective_results,
        "paths": {
            "candidate_csv": candidate_csv,
            "case_summary_csv": case_summary_csv,
            "objective_candidate_csv": objective_candidate_csv,
            "objective_summary_csv": objective_summary_csv,
            "radius_profiles_plot": plot_path,
            "objective_variant_radius_profiles_plot": objective_plot_path,
        },
    }
    summary_path = os.path.join(data_dir, "multi_rebar_local_geometry_summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    write_run_manifest(
        outdir,
        "multi_rebar_local_geometry_profile",
        {
            "summary_path": summary_path,
            "candidate_csv": candidate_csv,
            "case_summary_csv": case_summary_csv,
            "objective_candidate_csv": objective_candidate_csv,
            "objective_summary_csv": objective_summary_csv,
            "radius_profiles_plot": plot_path,
            "objective_variant_radius_profiles_plot": objective_plot_path,
        },
    )
    for label, result in results.items():
        margin = result["margin"]
        best = result["top_candidates"][0]
        params = best["params"]
        profile = best["source_profile"]
        print(
            f"{label}: best x={params['x_mm']} mm, z={params['z_mm']} mm, "
            f"r={margin['best_radius_mm']} mm, next r={margin['next_radius_mm']} mm, "
            f"margin={margin['radius_margin_abs']}, "
            f"source=({profile['frequency_scale']}, {profile['time_shift_ps']} ps, "
            f"{profile['amplitude_scale']})"
        )
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()

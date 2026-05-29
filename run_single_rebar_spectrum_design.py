#!/usr/bin/env python3
"""Generate spectrum diagnostics for PEBDD band selection."""
import argparse
import csv
import json
import os
import sys

import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import config as cfg  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from inversion.single_rebar_pipeline import (  # noqa: E402
    SingleRebarInversionEngine,
    SingleRebarParams,
    build_model_from_single_params,
    default_single_rebar_truth,
)
from inversion.spectrum_analysis import (  # noqa: E402
    average_amplitude_spectrum,
    band_energy_fraction,
    spectral_energy_band,
)
from run_single_rebar_inversion import _override_grid  # noqa: E402
from visualization.plot_spectrum import plot_average_spectra  # noqa: E402


DEFAULT_CANDIDATES_MM = [
    ("true", 250.0, 90.0, 6.0),
    ("near_radius_6p2", 250.0, 90.0, 6.2),
    ("high_radius_powell", 249.53336048978386, 90.6526482993157, 6.954785109185667),
    ("high_radius_grid", 250.0, 91.0, 6.8),
]


def _parse_candidate(text):
    parts = [item.strip() for item in text.split(":")]
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("Use label:x_mm,z_mm,radius_mm")
    label = parts[0]
    values = [float(item.strip()) for item in parts[1].split(",") if item.strip()]
    if len(values) != 3:
        raise argparse.ArgumentTypeError("Use label:x_mm,z_mm,radius_mm")
    return (label, values[0], values[1], values[2])


def _candidate_params(label, x_mm, z_mm, radius_mm):
    return label, SingleRebarParams(
        x=x_mm / 1000.0,
        z=z_mm / 1000.0,
        radius=radius_mm / 1000.0,
    )


def _spectrum_record(label, traces, dt, mute=None):
    if mute is not None:
        traces = traces * mute[:, None]
    freqs, amplitude = average_amplitude_spectrum(traces, dt)
    band = spectral_energy_band(freqs, amplitude)
    return {
        "label": label,
        "freqs_hz": freqs,
        "amplitude": amplitude,
        "band_5_95": band,
        "energy_fraction_0p2_0p8": band_energy_fraction(freqs, amplitude, 0.2e9, 0.8e9),
        "energy_fraction_0p2_1p1": band_energy_fraction(freqs, amplitude, 0.2e9, 1.1e9),
        "energy_fraction_0p2_1p5": band_energy_fraction(freqs, amplitude, 0.2e9, 1.5e9),
    }


def _write_spectrum_csv(records, path):
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["label", "frequency_hz", "amplitude"])
        for record in records:
            for freq, amp in zip(record["freqs_hz"], record["amplitude"]):
                writer.writerow([record["label"], float(freq), float(amp)])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml", "auto"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--run-name", default="single_rebar_spectrum_design")
    parser.add_argument("--outdir", default=None)
    parser.add_argument("--observed-noise-rms-fraction", type=float, default=0.0)
    parser.add_argument("--noise-seed", type=int, default=13)
    parser.add_argument("--candidate", action="append", type=_parse_candidate,
                        help="Candidate as label:x_mm,z_mm,radius_mm; may repeat")
    parser.add_argument("--no-mute", action="store_true",
                        help="Do not apply the inversion mute to B-scan spectra")
    args = parser.parse_args()

    _override_grid(args.grid_step_mm)
    outdir = allocate_output_dir(args.outdir, args.run_name)
    print(f"Output directory: {outdir}")
    os.makedirs(os.path.join(outdir, "data"), exist_ok=True)
    os.makedirs(os.path.join(outdir, "figures"), exist_ok=True)

    candidates_mm = args.candidate or DEFAULT_CANDIDATES_MM
    candidates = [_candidate_params(*candidate) for candidate in candidates_mm]
    truth = default_single_rebar_truth()
    engine = SingleRebarInversionEngine(
        true_params=truth,
        initial_params=truth,
        frequencies=(cfg.F_CENTER,),
        n_sources=args.sources,
        backend=args.backend,
        observed_noise_rms_fraction=args.observed_noise_rms_fraction,
        noise_seed=args.noise_seed,
        log_every=999,
    )
    mute = None if args.no_mute else engine.mute
    frequency = engine.frequencies[0]
    observed = engine.d_obs_by_frequency[frequency]

    source_freqs, source_amp = average_amplitude_spectrum(engine.wavelets[frequency], cfg.DT)
    source_record = {
        "label": "source_wavelet",
        "freqs_hz": source_freqs,
        "amplitude": source_amp,
        "band_5_95": spectral_energy_band(source_freqs, source_amp),
        "energy_fraction_0p2_0p8": band_energy_fraction(source_freqs, source_amp, 0.2e9, 0.8e9),
        "energy_fraction_0p2_1p1": band_energy_fraction(source_freqs, source_amp, 0.2e9, 1.1e9),
        "energy_fraction_0p2_1p5": band_energy_fraction(source_freqs, source_amp, 0.2e9, 1.5e9),
    }
    signal_records = [_spectrum_record("observed", observed, cfg.DT, mute=mute)]
    residual_records = []
    candidate_summaries = []

    for label, params in candidates:
        model = build_model_from_single_params(
            params.as_array(),
            geometry_mode=engine.geometry_mode,
            subcell_samples=engine.subcell_samples,
        )
        synthetic = engine._simulate_bscan(model, engine.wavelets[frequency])
        residual = synthetic - observed
        signal_records.append(_spectrum_record(f"synthetic_{label}", synthetic, cfg.DT, mute=mute))
        residual_record = _spectrum_record(f"residual_{label}", residual, cfg.DT, mute=mute)
        residual_records.append(residual_record)
        candidate_summaries.append({
            "label": label,
            "params_mm": params.as_mm(),
            "residual_band_5_95": residual_record["band_5_95"],
            "residual_energy_fraction_0p2_0p8": residual_record["energy_fraction_0p2_0p8"],
            "residual_energy_fraction_0p2_1p1": residual_record["energy_fraction_0p2_1p1"],
            "residual_energy_fraction_0p2_1p5": residual_record["energy_fraction_0p2_1p5"],
        })

    all_records = [source_record] + signal_records + residual_records
    _write_spectrum_csv(all_records, os.path.join(outdir, "data", "spectrum_records.csv"))

    plot_average_spectra(
        [source_record],
        save_path=os.path.join(outdir, "figures", "source_spectrum.png"),
        show=False,
        title="Source wavelet spectrum",
    )
    plot_average_spectra(
        signal_records,
        save_path=os.path.join(outdir, "figures", "signal_spectra.png"),
        show=False,
        title="Observed and synthetic B-scan spectra",
    )
    plot_average_spectra(
        residual_records,
        save_path=os.path.join(outdir, "figures", "residual_spectra.png"),
        show=False,
        title="Candidate residual spectra",
    )

    summary = {
        "backend": engine.backend,
        "grid_step_mm": args.grid_step_mm,
        "sources": len(engine.scan_positions),
        "frequency_ghz": float(frequency / 1e9),
        "used_mute": mute is not None,
        "observed_noise_rms_fraction": args.observed_noise_rms_fraction,
        "noise_seed": args.noise_seed,
        "source_band_5_95": source_record["band_5_95"],
        "observed_band_5_95": signal_records[0]["band_5_95"],
        "candidate_residuals": candidate_summaries,
        "candidate_count": len(candidates),
    }
    with open(os.path.join(outdir, "data", "spectrum_design_summary.json"), "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    write_run_manifest(
        outdir,
        "single_rebar_spectrum_design",
        {
            "backend": engine.backend,
            "grid_step_mm": args.grid_step_mm,
            "sources": len(engine.scan_positions),
            "observed_noise_rms_fraction": args.observed_noise_rms_fraction,
            "noise_seed": args.noise_seed,
            "summary_path": os.path.join(outdir, "data", "spectrum_design_summary.json"),
        },
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

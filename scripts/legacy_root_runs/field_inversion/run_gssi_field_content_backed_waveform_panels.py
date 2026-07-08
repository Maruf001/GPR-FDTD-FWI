#!/usr/bin/env python3
"""Build content-backed field/synthetic waveform comparison panels."""

from __future__ import annotations

import argparse
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

import config as cfg  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import (  # noqa: E402
    DEFAULT_DATASET_ID,
    DEFAULT_FIELD_ROOT,
    DEFAULT_INPUT_DIR,
    field_dataset_output_root,
    read_dzt_profiles,
    readgssi_version,
)
from run_gssi_field_preprocess_feature_qc import (  # noqa: E402
    build_axes,
    json_safe,
    preprocess_profile,
    write_csv,
)
from run_gssi_field_short_profile_content_window_policy import boolish  # noqa: E402
from run_gssi_field_synthetic_waveform_probe import (  # noqa: E402
    figure_stats,
    interpolate_matrix,
    read_csv_rows,
    robust_normalize,
    safe_float,
    shift_window_time,
    simulate_single_candidate,
)
from visualization.plot_style import safe_symmetric_limits, save_validated_figure  # noqa: E402


DEFAULT_CONTENT_SYNTHETIC_RUN = "033_gssi51600s_short_profile_content_synthetic_policy"
DEFAULT_WAVEFORM_RUN = "011_gssi51600s_field_synthetic_waveform_family_shift_epsr_probe"


def select_content_backed_candidates(event_rows: list[dict], probe_rows: list[dict]) -> list[dict]:
    """Return reference/comparison candidates for content-backed event pairs."""
    probe_by_id = {row["candidate_id"]: row for row in probe_rows}
    selected: list[dict] = []
    for event in event_rows:
        if not boolish(event.get("content_backed")):
            continue
        for side, prefix in (("reference", "reference"), ("comparison", "comparison")):
            candidate_id = event.get(f"{prefix}_candidate_id", "")
            probe = probe_by_id.get(candidate_id)
            if probe is None:
                selected.append({
                    "pair_index": int(safe_float(event.get("pair_index"), -1)),
                    "side": side,
                    "candidate_id": candidate_id,
                    "available": False,
                    "reason": "candidate_missing_from_waveform_probe",
                })
                continue
            selected.append({
                "pair_index": int(safe_float(event.get("pair_index"), -1)),
                "side": side,
                "candidate_id": candidate_id,
                "available": True,
                "reason": "",
                "pair_min_absolute_correlation": safe_float(event.get("pair_min_absolute_correlation")),
                "pair_mean_absolute_correlation": safe_float(event.get("pair_mean_absolute_correlation")),
                "waveform_support_label": event.get("waveform_support_label", ""),
                "content_label": event.get("content_label", ""),
                "probe": probe,
            })
    return sorted(selected, key=lambda row: (row["pair_index"], row["side"]))


def center_trace(window: np.ndarray) -> np.ndarray:
    """Return the middle aperture trace from a time-by-offset window."""
    arr = np.asarray(window, dtype=np.float64)
    if arr.ndim != 2 or arr.shape[1] == 0:
        raise ValueError("window must be a non-empty 2D array")
    return arr[:, arr.shape[1] // 2]


def summarize_panel_rows(rows: list[dict]) -> dict:
    valid = [row for row in rows if boolish(row.get("simulation_valid"))]
    correlations = [safe_float(row.get("absolute_correlation")) for row in valid]
    correlations = [value for value in correlations if math.isfinite(value)]
    return {
        "policy_label": "content_backed_waveform_visual_qc",
        "panel_count": len(rows),
        "valid_panel_count": len(valid),
        "content_backed_pair_count": len({row.get("pair_index") for row in valid}),
        "min_absolute_correlation": min(correlations) if correlations else math.nan,
        "mean_absolute_correlation": float(np.mean(correlations)) if correlations else math.nan,
        "policy": (
            "Use these panels for visual field-to-synthetic QC of content-backed "
            "short-profile events only. This is no field inversion evidence and "
            "does not support radius, cover-depth, geometry, 3D, or FWI claims."
        ),
    }


def load_processed_profiles(input_dir: Path, file_names: set[str]) -> tuple[dict[str, dict], dict[str, tuple[np.ndarray, np.ndarray]]]:
    processed_by_file: dict[str, dict] = {}
    axes_by_file: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for record, raw in read_dzt_profiles(input_dir):
        if record.get("file") not in file_names:
            continue
        processed_by_file[record["file"]] = preprocess_profile(raw)
        axes_by_file[record["file"]] = build_axes(record)
    return processed_by_file, axes_by_file


def build_panel_payload(
    spec: dict,
    processed_by_file: dict[str, dict],
    axes_by_file: dict[str, tuple[np.ndarray, np.ndarray]],
    *,
    backend: str | None,
    window_pre_ns: float,
    window_post_ns: float,
) -> dict:
    probe = spec["probe"]
    file_name = probe["file"]
    if file_name not in processed_by_file:
        return {**spec, "simulation_valid": False, "reason": "field_profile_missing"}

    center_x = safe_float(probe.get("x_m"))
    anchor_time = safe_float(probe.get("apex_time_ns"))
    depth_m = safe_float(probe.get("fitted_depth_m"))
    radius_m = safe_float(probe.get("radius_mm")) / 1000.0
    concrete_epsr = safe_float(probe.get("concrete_epsr"))
    run_backend = backend or probe.get("backend", "gpu-cpml")
    frequency_hz = safe_float(probe.get("frequency_ghz")) * 1.0e9
    source_count = int(safe_float(probe.get("sources")))
    tx_rx_offset_m = safe_float(probe.get("tx_rx_offset_mm")) / 1000.0
    scan_aperture_m = safe_float(probe.get("scan_aperture_mm")) / 1000.0

    sim = simulate_single_candidate(
        depth_m=depth_m,
        radius_m=radius_m,
        concrete_epsr=concrete_epsr,
        backend=run_backend,
        frequency_hz=frequency_hz,
        source_count=source_count,
        tx_rx_offset_m=tx_rx_offset_m,
        scan_aperture_m=scan_aperture_m,
        geometry_mode="hard",
        subcell_samples=5,
    )
    base = {
        **{key: value for key, value in spec.items() if key != "probe"},
        "file": file_name,
        "phase_convention": probe.get("phase_convention"),
        "apex_group": int(safe_float(probe.get("apex_group"), -1)),
        "radius_mm": safe_float(probe.get("radius_mm")),
        "epsr_source": probe.get("epsr_source"),
        "concrete_epsr": concrete_epsr,
        "absolute_correlation": safe_float(probe.get("absolute_correlation")),
        "normalized_residual_rms": safe_float(probe.get("normalized_residual_rms")),
        "synthetic_time_shift_ns": safe_float(probe.get("synthetic_time_shift_ns"), 0.0),
        "backend": run_backend,
    }
    if not sim["valid"]:
        return {**base, "simulation_valid": False, "reason": sim["reason"]}

    rel_time_ns = np.arange(
        -float(window_pre_ns),
        float(window_post_ns) + cfg.DT * 1.0e9,
        cfg.DT * 1.0e9,
        dtype=np.float64,
    )
    x_m, field_time_ns = axes_by_file[file_name]
    target_x = center_x + sim["midpoint_offsets_m"]
    field_window = interpolate_matrix(
        processed_by_file[file_name]["corrected"],
        x_m,
        field_time_ns,
        target_x,
        anchor_time + rel_time_ns,
    )
    synthetic_window = interpolate_matrix(
        sim["corrected"],
        sim["midpoint_x_m"],
        sim["time_ns"],
        sim["midpoint_x_m"],
        sim["synthetic_peak_time_ns"] + rel_time_ns,
    )
    shifted = shift_window_time(
        synthetic_window,
        safe_float(probe.get("synthetic_time_shift_ns"), 0.0),
        cfg.DT * 1.0e9,
    )
    field_norm = robust_normalize(field_window)
    synthetic_norm = robust_normalize(shifted)
    sign = 1.0 if probe.get("polarity") == "same" else -1.0
    return {
        **base,
        "simulation_valid": True,
        "reason": "",
        "relative_time_ns": rel_time_ns,
        "field_trace": center_trace(field_norm),
        "synthetic_trace": sign * center_trace(synthetic_norm),
    }


def plot_panels(payloads: list[dict], summary: dict, save_path: Path) -> str:
    valid_payloads = [payload for payload in payloads if boolish(payload.get("simulation_valid"))]
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 7.2), constrained_layout=True)
    axes_flat = axes.ravel()
    all_values = []
    for payload in valid_payloads:
        all_values.extend(payload["field_trace"][np.isfinite(payload["field_trace"])])
        all_values.extend(payload["synthetic_trace"][np.isfinite(payload["synthetic_trace"])])
    limits = safe_symmetric_limits(np.asarray(all_values, dtype=np.float64), percentile=98.0, floor=1.0)
    for ax, payload in zip(axes_flat, valid_payloads):
        t = payload["relative_time_ns"]
        ax.plot(t, payload["field_trace"], color="#1f4e79", linewidth=1.4, label="field")
        ax.plot(t, payload["synthetic_trace"], color="#b45f36", linewidth=1.2, linestyle="--", label="synthetic")
        ax.axvline(0.0, color="#222222", linewidth=0.8, linestyle=":")
        ax.set_ylim(limits)
        ax.set_xlabel("relative time [ns]")
        ax.set_ylabel("normalized amplitude")
        ax.set_title(
            (
                f"pair {payload['pair_index']} {payload['side']} "
                f"{Path(payload['file']).stem.split('__')[-1]} g{payload['apex_group']} "
                f"|corr|={payload['absolute_correlation']:.3f}"
            ),
            fontsize=10,
        )
        ax.grid(color="#dddddd", linewidth=0.6)
    for ax in axes_flat[len(valid_payloads):]:
        ax.axis("off")
    axes_flat[0].legend(frameon=False, loc="upper right")
    fig.suptitle(
        (
            "Content-backed field-to-synthetic waveform QC "
            f"(min |corr|={summary['min_absolute_correlation']:.3f})"
        ),
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--content-synthetic-run", default=DEFAULT_CONTENT_SYNTHETIC_RUN)
    parser.add_argument("--waveform-run", default=DEFAULT_WAVEFORM_RUN)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml"], default=None)
    parser.add_argument("--window-pre-ns", type=float, default=0.34)
    parser.add_argument("--window-post-ns", type=float, default=0.82)
    parser.add_argument("--run-name", default="gssi51600s_content_backed_waveform_panels")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    content_csv = (
        dataset_root
        / args.content_synthetic_run
        / "data"
        / "short_profile_content_synthetic_event_matches.csv"
    )
    waveform_csv = dataset_root / args.waveform_run / "data" / "field_synthetic_waveform_probe.csv"
    event_rows = read_csv_rows(content_csv)
    probe_rows = read_csv_rows(waveform_csv)
    specs = select_content_backed_candidates(event_rows, probe_rows)
    available_specs = [spec for spec in specs if boolish(spec.get("available"))]
    file_names = {spec["probe"]["file"] for spec in available_specs}
    processed_by_file, axes_by_file = load_processed_profiles(Path(args.input_dir), file_names)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    payloads = [
        build_panel_payload(
            spec,
            processed_by_file,
            axes_by_file,
            backend=args.backend,
            window_pre_ns=args.window_pre_ns,
            window_post_ns=args.window_post_ns,
        )
        for spec in available_specs
    ]
    panel_rows = [
        {
            key: value
            for key, value in payload.items()
            if key not in {"relative_time_ns", "field_trace", "synthetic_trace"}
        }
        for payload in payloads
    ]
    summary = summarize_panel_rows(panel_rows)

    panel_csv = data_dir / "content_backed_waveform_panel_rows.csv"
    summary_json = data_dir / "content_backed_waveform_panel_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_panels(payloads, summary, figures_dir / "content_backed_waveform_panels.png"))

    write_csv(panel_csv, [json_safe(row) for row in panel_rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        **summary,
        "content_synthetic_csv": str(content_csv),
        "waveform_csv": str(waveform_csv),
        "paths": {
            "panel_csv": str(panel_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_content_backed_waveform_panels",
        {
            "summary_json": str(summary_json),
            "panel_csv": str(panel_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

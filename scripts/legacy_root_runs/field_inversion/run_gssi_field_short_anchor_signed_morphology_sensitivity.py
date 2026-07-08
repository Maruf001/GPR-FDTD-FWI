#!/usr/bin/env python3
"""Sweep signed-morphology thresholds for the GSSI short-anchor field QC."""

from __future__ import annotations

import argparse
import csv
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

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SIGNED_MORPHOLOGY_RUN = "126_gssi51600s_field_short_anchor_signed_morphology_audit"
DEFAULT_CORRECTED_SIGNED_THRESHOLDS = "0.90,0.925,0.95,0.975,0.99"
DEFAULT_EVENT_LOCAL_THRESHOLDS = "0.95,0.975,0.985,0.99"
DEFAULT_IMPROVEMENT_THRESHOLDS = "0.30,0.50,0.60,0.70"
DEFAULT_TIMING_CAPS_NS = "0.05,0.03,0.02,0.01"
MODERATE_CORRECTED_SIGNED_THRESHOLD = 0.925
MODERATE_EVENT_LOCAL_THRESHOLD = 0.985
MODERATE_IMPROVEMENT_THRESHOLD = 0.50
MODERATE_TIMING_CAP_NS = 0.02
STRICT_CORRECTED_SIGNED_THRESHOLD = 0.95
STRICT_IMPROVEMENT_THRESHOLD = 0.60
STRICT_TIMING_CAP_NS = 0.01


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_thresholds(value: str, *, allow_zero: bool = False) -> list[float]:
    thresholds: list[float] = []
    for item in str(value or "").split(","):
        item = item.strip()
        if not item:
            continue
        number = float(item)
        if not math.isfinite(number):
            raise ValueError(f"non-finite threshold: {item}")
        if number < 0.0 or (number == 0.0 and not allow_zero):
            raise ValueError(f"threshold must be positive: {item}")
        thresholds.append(number)
    if not thresholds:
        raise ValueError("at least one threshold is required")
    return sorted(set(thresholds))


def _finite(values: list[float]) -> list[float]:
    return [value for value in values if math.isfinite(value)]


def _row_metrics(row: dict) -> dict[str, float]:
    return {
        "corrected_signed_correlation": safe_float(row.get("corrected_signed_correlation")),
        "event_local_abs_correlation": safe_float(row.get("event_local_field_trace_abs_correlation")),
        "abs_correlation_improvement": safe_float(row.get("field_trace_abs_correlation_improvement")),
        "timing_residual_ns": safe_float(row.get("corrected_abs_timing_residual_ns")),
    }


def _threshold_label(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".").replace(".", "p")


def _pair_supported(
    row: dict,
    *,
    corrected_signed_threshold: float,
    event_local_threshold: float,
    improvement_threshold: float,
    timing_cap_ns: float,
) -> tuple[bool, list[str]]:
    metrics = _row_metrics(row)
    failures = []
    if metrics["corrected_signed_correlation"] < corrected_signed_threshold:
        failures.append("corrected_signed_correlation")
    if metrics["event_local_abs_correlation"] < event_local_threshold:
        failures.append("event_local_abs_correlation")
    if metrics["abs_correlation_improvement"] < improvement_threshold:
        failures.append("abs_correlation_improvement")
    if metrics["timing_residual_ns"] > timing_cap_ns:
        failures.append("timing_residual")
    return len(failures) == 0, failures


def build_threshold_rows(
    signed_rows: list[dict],
    corrected_signed_thresholds: list[float],
    event_local_thresholds: list[float],
    improvement_thresholds: list[float],
    timing_caps_ns: list[float],
) -> list[dict]:
    rows: list[dict] = []
    for corrected_threshold in corrected_signed_thresholds:
        for event_threshold in event_local_thresholds:
            for improvement_threshold in improvement_thresholds:
                for timing_cap in timing_caps_ns:
                    supported_pair_indices = []
                    unsupported_pair_indices = []
                    failures = set()
                    for signed_row in signed_rows:
                        pair_index = int(safe_float(signed_row.get("pair_index"), -1))
                        supported, pair_failures = _pair_supported(
                            signed_row,
                            corrected_signed_threshold=corrected_threshold,
                            event_local_threshold=event_threshold,
                            improvement_threshold=improvement_threshold,
                            timing_cap_ns=timing_cap,
                        )
                        if supported:
                            supported_pair_indices.append(pair_index)
                        else:
                            unsupported_pair_indices.append(pair_index)
                            failures.update(pair_failures)
                    all_supported = len(supported_pair_indices) == len(signed_rows) and len(signed_rows) > 0
                    rows.append(
                        {
                            "threshold_id": (
                                "corr"
                                f"{_threshold_label(corrected_threshold)}_event{_threshold_label(event_threshold)}_"
                                f"improve{_threshold_label(improvement_threshold)}_time{_threshold_label(timing_cap)}ns"
                            ),
                            "corrected_signed_threshold": corrected_threshold,
                            "event_local_threshold": event_threshold,
                            "improvement_threshold": improvement_threshold,
                            "timing_cap_ns": timing_cap,
                            "pair_count": len(signed_rows),
                            "supported_pair_count": len(supported_pair_indices),
                            "supported_pair_indices": ";".join(str(index) for index in supported_pair_indices),
                            "unsupported_pair_indices": ";".join(str(index) for index in unsupported_pair_indices),
                            "all_pairs_supported": all_supported,
                            "binding_failure_metrics": ";".join(sorted(failures)),
                            "allowed_use": "threshold-margin sensitivity for signed field morphology QC",
                            "blocked_use": "amplitude calibration, radius/geometry/cover-depth recovery, field FWI, 3D/HPC",
                        }
                    )
    return rows


def _support_at(
    threshold_rows: list[dict],
    *,
    corrected_signed_threshold: float,
    event_local_threshold: float,
    improvement_threshold: float,
    timing_cap_ns: float,
) -> bool:
    for row in threshold_rows:
        if (
            math.isclose(safe_float(row.get("corrected_signed_threshold")), corrected_signed_threshold)
            and math.isclose(safe_float(row.get("event_local_threshold")), event_local_threshold)
            and math.isclose(safe_float(row.get("improvement_threshold")), improvement_threshold)
            and math.isclose(safe_float(row.get("timing_cap_ns")), timing_cap_ns)
        ):
            return bool(row.get("all_pairs_supported"))
    return False


def summarize_sensitivity(
    signed_rows: list[dict],
    threshold_rows: list[dict],
    signed_summary: dict,
) -> dict:
    corrected = _finite([_row_metrics(row)["corrected_signed_correlation"] for row in signed_rows])
    event = _finite([_row_metrics(row)["event_local_abs_correlation"] for row in signed_rows])
    improvements = _finite([_row_metrics(row)["abs_correlation_improvement"] for row in signed_rows])
    timings = _finite([_row_metrics(row)["timing_residual_ns"] for row in signed_rows])
    supported_rows = [row for row in threshold_rows if bool(row.get("all_pairs_supported"))]
    failure_metrics = sorted(
        {
            metric
            for row in threshold_rows
            for metric in str(row.get("binding_failure_metrics", "")).split(";")
            if metric
        }
    )
    default_supported = _support_at(
        threshold_rows,
        corrected_signed_threshold=0.90,
        event_local_threshold=0.95,
        improvement_threshold=0.30,
        timing_cap_ns=0.05,
    )
    moderate_supported = _support_at(
        threshold_rows,
        corrected_signed_threshold=MODERATE_CORRECTED_SIGNED_THRESHOLD,
        event_local_threshold=MODERATE_EVENT_LOCAL_THRESHOLD,
        improvement_threshold=MODERATE_IMPROVEMENT_THRESHOLD,
        timing_cap_ns=MODERATE_TIMING_CAP_NS,
    )
    strict_corr_supported = _support_at(
        threshold_rows,
        corrected_signed_threshold=STRICT_CORRECTED_SIGNED_THRESHOLD,
        event_local_threshold=MODERATE_EVENT_LOCAL_THRESHOLD,
        improvement_threshold=MODERATE_IMPROVEMENT_THRESHOLD,
        timing_cap_ns=MODERATE_TIMING_CAP_NS,
    )
    strict_all_supported = _support_at(
        threshold_rows,
        corrected_signed_threshold=STRICT_CORRECTED_SIGNED_THRESHOLD,
        event_local_threshold=MODERATE_EVENT_LOCAL_THRESHOLD,
        improvement_threshold=STRICT_IMPROVEMENT_THRESHOLD,
        timing_cap_ns=STRICT_TIMING_CAP_NS,
    )
    return {
        "policy_label": "gssi51600s_field_short_anchor_signed_morphology_threshold_sensitivity_qc_only",
        "source_signed_morphology_policy_label": signed_summary.get("policy_label", ""),
        "content_pair_count": len(signed_rows),
        "threshold_combo_count": len(threshold_rows),
        "all_pairs_supported_threshold_combo_count": len(supported_rows),
        "all_pairs_supported_threshold_fraction": (
            len(supported_rows) / len(threshold_rows) if threshold_rows else math.nan
        ),
        "default_thresholds_supported": default_supported,
        "moderate_tightening_supported": moderate_supported,
        "strict_correlation_supported": strict_corr_supported,
        "strict_all_supported": strict_all_supported,
        "support_limit_corrected_signed_correlation": min(corrected) if corrected else math.nan,
        "support_limit_event_local_abs_correlation": min(event) if event else math.nan,
        "support_limit_abs_correlation_improvement": min(improvements) if improvements else math.nan,
        "support_limit_timing_cap_ns": max(timings) if timings else math.nan,
        "binding_failure_metrics": ";".join(failure_metrics),
        "ready_for_default_signed_morphology_qc": default_supported,
        "ready_for_moderate_threshold_morphology_qc": moderate_supported,
        "ready_for_strict_morphology_claim": False,
        "ready_for_absolute_amplitude_calibration": False,
        "ready_for_radius_seed": False,
        "ready_for_geometry_seed": False,
        "ready_for_cover_depth_recovery": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "ready_for_heavy_field_work": False,
        "gpu_priority": "none",
        "decision": (
            "The signed short-anchor morphology survives the default thresholds and a moderate "
            "tightening envelope, but it does not support stricter morphology or inversion claims. "
            "Use this as field supplement threshold-margin evidence only; keep amplitude calibration, "
            "radius/geometry/cover-depth recovery, field FWI, 3D/HPC, and heavy field work blocked."
        ),
    }


def build_gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "default_signed_morphology_qc",
            "ready": summary["ready_for_default_signed_morphology_qc"],
            "allowed_use": "signed field waveform-morphology QC at default thresholds",
            "blocked_use": "none within default morphology-QC scope",
            "evidence": (
                f"supported combos={summary['all_pairs_supported_threshold_combo_count']}/"
                f"{summary['threshold_combo_count']}"
            ),
        },
        {
            "gate_key": "moderate_threshold_morphology_qc",
            "ready": summary["ready_for_moderate_threshold_morphology_qc"],
            "allowed_use": "threshold-margin robustness statement for field supplement",
            "blocked_use": "strict morphology or inversion claim",
            "evidence": (
                f"limits corr={summary['support_limit_corrected_signed_correlation']:.6f}, "
                f"event={summary['support_limit_event_local_abs_correlation']:.6f}, "
                f"improvement={summary['support_limit_abs_correlation_improvement']:.6f}, "
                f"timing cap={summary['support_limit_timing_cap_ns']:.6f} ns"
            ),
        },
        {
            "gate_key": "strict_morphology_claim",
            "ready": summary["ready_for_strict_morphology_claim"],
            "allowed_use": "none",
            "blocked_use": "strict all-threshold field morphology claim",
            "evidence": (
                f"strict corr supported={summary['strict_correlation_supported']}; "
                f"strict all supported={summary['strict_all_supported']}; "
                f"binding metrics={summary['binding_failure_metrics']}"
            ),
        },
        {
            "gate_key": "field_fwi",
            "ready": summary["ready_for_field_fwi"],
            "allowed_use": "none",
            "blocked_use": "field FWI, 3D/HPC, or heavy field work",
            "evidence": "threshold-margin morphology evidence is not an inversion launch contract",
        },
    ]


def plot_sensitivity(threshold_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), constrained_layout=True)
    grouped: dict[float, list[dict]] = {}
    for row in threshold_rows:
        grouped.setdefault(safe_float(row.get("corrected_signed_threshold")), []).append(row)
    corr_thresholds = sorted(grouped)
    supported_counts = [
        sum(1 for row in grouped[threshold] if bool(row.get("all_pairs_supported")))
        for threshold in corr_thresholds
    ]
    axes[0].bar(
        np.arange(len(corr_thresholds)),
        supported_counts,
        color="#4c72b0",
    )
    axes[0].set_xticks(np.arange(len(corr_thresholds)), [f"{value:.3f}" for value in corr_thresholds])
    axes[0].set_xlabel("corrected signed-correlation threshold")
    axes[0].set_ylabel("all-pair supported combinations")
    axes[0].set_title("Sensitivity grid support by signed-correlation threshold")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    gates = [
        ("default", summary["default_thresholds_supported"]),
        ("moderate", summary["moderate_tightening_supported"]),
        ("strict\ncorr", summary["strict_correlation_supported"]),
        ("strict\nall", summary["strict_all_supported"]),
        ("field\nFWI", summary["ready_for_field_fwi"]),
    ]
    colors = ["#59a14f" if ready else "#bab0ac" for _, ready in gates]
    axes[1].bar(np.arange(len(gates)), [1 if ready else 0 for _, ready in gates], color=colors)
    axes[1].set_xticks(np.arange(len(gates)), [label for label, _ in gates])
    axes[1].set_yticks([0, 1], ["blocked", "ready"])
    axes[1].set_ylim(0, 1.15)
    axes[1].set_title("Claim gates from threshold sweep")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.06,
        f"supported combos: {summary['all_pairs_supported_threshold_combo_count']}/"
        f"{summary['threshold_combo_count']}\n"
        f"corr limit: {summary['support_limit_corrected_signed_correlation']:.3f}\n"
        f"improvement limit: {summary['support_limit_abs_correlation_improvement']:.3f}\n"
        f"timing cap limit: {summary['support_limit_timing_cap_ns']:.3f} ns",
        transform=axes[1].transAxes,
        va="bottom",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI 51600S signed-morphology threshold sensitivity", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, threshold_csv: Path, gates_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_short_anchor_signed_morphology_sensitivity.png`",
                "",
                "This CPU-only figure sweeps signed-morphology thresholds for the two",
                "content-backed GSSI 51600S short-anchor pairs from run 126.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Threshold combinations: `{summary['threshold_combo_count']}`.",
                f"All-pair supported combinations: `{summary['all_pairs_supported_threshold_combo_count']}`.",
                f"Default thresholds supported: `{summary['default_thresholds_supported']}`.",
                f"Moderate tightening supported: `{summary['moderate_tightening_supported']}`.",
                f"Strict morphology claim ready: `{summary['ready_for_strict_morphology_claim']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Threshold rows: `{threshold_csv.name}`.",
                f"- Gate rows: `{gates_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved signed-morphology artifacts only. It does not run DZT preprocessing,",
                "FDTD, FWI, GPU kernels, field inversion, 3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--signed-morphology-run", default=DEFAULT_SIGNED_MORPHOLOGY_RUN)
    parser.add_argument("--corrected-signed-thresholds", default=DEFAULT_CORRECTED_SIGNED_THRESHOLDS)
    parser.add_argument("--event-local-thresholds", default=DEFAULT_EVENT_LOCAL_THRESHOLDS)
    parser.add_argument("--improvement-thresholds", default=DEFAULT_IMPROVEMENT_THRESHOLDS)
    parser.add_argument("--timing-caps-ns", default=DEFAULT_TIMING_CAPS_NS)
    parser.add_argument("--run-name", default="gssi51600s_field_short_anchor_signed_morphology_sensitivity")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    field_root = field_dataset_output_root(args.field_root, args.dataset_id)
    signed_dir = field_root / args.signed_morphology_run
    signed_rows = read_csv_rows(signed_dir / "data/field_short_anchor_signed_morphology_rows.csv")
    signed_summary = read_json(signed_dir / "data/field_short_anchor_signed_morphology_summary.json")

    corrected_thresholds = parse_thresholds(args.corrected_signed_thresholds)
    event_thresholds = parse_thresholds(args.event_local_thresholds)
    improvement_thresholds = parse_thresholds(args.improvement_thresholds)
    timing_caps = parse_thresholds(args.timing_caps_ns)

    threshold_rows = build_threshold_rows(
        signed_rows,
        corrected_thresholds,
        event_thresholds,
        improvement_thresholds,
        timing_caps,
    )
    summary = summarize_sensitivity(signed_rows, threshold_rows, signed_summary)
    gates = build_gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=field_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    threshold_csv = data_dir / "field_short_anchor_signed_morphology_sensitivity_rows.csv"
    gates_csv = data_dir / "field_short_anchor_signed_morphology_sensitivity_gates.csv"
    summary_json = data_dir / "field_short_anchor_signed_morphology_sensitivity_summary.json"
    figure_path = figures_dir / "field_short_anchor_signed_morphology_sensitivity.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"
    validation_csv = data_dir / "figure_validation.csv"

    write_csv(threshold_csv, [json_safe(row) for row in threshold_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_sensitivity(threshold_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, threshold_csv, gates_csv)

    summary["paths"] = {
        "threshold_rows_csv": str(threshold_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "source_signed_morphology_rows_csv": str(
            signed_dir / "data/field_short_anchor_signed_morphology_rows.csv"
        ),
        "source_signed_morphology_summary_json": str(
            signed_dir / "data/field_short_anchor_signed_morphology_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_short_anchor_signed_morphology_sensitivity",
        {
            "signed_morphology_run": args.signed_morphology_run,
            "corrected_signed_thresholds": corrected_thresholds,
            "event_local_thresholds": event_thresholds,
            "improvement_thresholds": improvement_thresholds,
            "timing_caps_ns": timing_caps,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

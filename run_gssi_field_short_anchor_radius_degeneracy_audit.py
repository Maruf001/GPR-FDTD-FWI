#!/usr/bin/env python3
"""Audit short-anchor field radius degeneracy from saved waveform candidates."""

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
from run_gssi_field_short_profile_content_window_policy import boolish  # noqa: E402
from run_gssi_field_synthetic_waveform_probe import safe_float  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CONTENT_SYNTHETIC_RUN = "033_gssi51600s_short_profile_content_synthetic_policy"
DEFAULT_WAVEFORM_RUN = "011_gssi51600s_field_synthetic_waveform_family_shift_epsr_probe"
DEFAULT_WAVEFORM_COHERENCE_RUN = "124_gssi51600s_field_short_anchor_waveform_coherence_audit"
DEFAULT_MIN_RADIUS_CORR_GAP = 0.03
DEFAULT_COMMON_RADIUS_MIN_LOSS_TOL = 0.01
DEFAULT_COMMON_RADIUS_MEAN_LOSS_TOL = 0.03


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def finite(value: object, default: float = math.nan) -> float:
    out = safe_float(value, default)
    return out if math.isfinite(out) else default


def candidate_context(row: dict) -> tuple:
    return (
        row.get("file", ""),
        row.get("phase_convention", ""),
        int(finite(row.get("apex_group"), -1)),
        row.get("epsr_source", ""),
        row.get("backend", ""),
        finite(row.get("frequency_ghz")),
        finite(row.get("sources")),
        finite(row.get("tx_rx_offset_mm")),
        finite(row.get("scan_aperture_mm")),
    )


def valid_waveform_rows(waveform_rows: list[dict]) -> list[dict]:
    rows = []
    for row in waveform_rows:
        if not boolish(row.get("geometry_valid", True)):
            continue
        if not math.isfinite(finite(row.get("absolute_correlation"))):
            continue
        rows.append(row)
    return rows


def rank_radius_family(family_rows: list[dict]) -> list[dict]:
    return sorted(
        family_rows,
        key=lambda row: (
            -finite(row.get("absolute_correlation"), -math.inf),
            finite(row.get("normalized_residual_rms"), math.inf),
            finite(row.get("radius_mm"), math.inf),
        ),
    )


def content_events(event_rows: list[dict]) -> list[dict]:
    return [row for row in event_rows if boolish(row.get("content_backed"))]


def side_selection(event: dict, side: str, selected: dict) -> dict:
    prefix = "reference" if side == "reference" else "comparison"
    return {
        "pair_index": int(finite(event.get("pair_index"), -1)),
        "side": side,
        "content_label": event.get("content_label", ""),
        "selected_candidate_id": event.get(f"{prefix}_candidate_id", ""),
        "selected_radius_mm": finite(event.get(f"{prefix}_radius_mm")),
        "selected_absolute_correlation": finite(event.get(f"{prefix}_absolute_correlation")),
        "selected_normalized_residual_rms": finite(event.get(f"{prefix}_normalized_residual_rms")),
        "file": selected.get("file", ""),
        "phase_convention": selected.get("phase_convention", ""),
        "apex_group": int(finite(selected.get("apex_group"), -1)),
        "epsr_source": selected.get("epsr_source", ""),
        "backend": selected.get("backend", ""),
        "frequency_ghz": finite(selected.get("frequency_ghz")),
        "sources": finite(selected.get("sources")),
        "tx_rx_offset_mm": finite(selected.get("tx_rx_offset_mm")),
        "scan_aperture_mm": finite(selected.get("scan_aperture_mm")),
    }


def build_radius_side_rows(
    event_rows: list[dict],
    waveform_rows: list[dict],
    *,
    min_radius_corr_gap: float = DEFAULT_MIN_RADIUS_CORR_GAP,
) -> list[dict]:
    valid_rows = valid_waveform_rows(waveform_rows)
    by_candidate = {row.get("candidate_id", ""): row for row in valid_rows}
    by_context: dict[tuple, list[dict]] = {}
    for row in valid_rows:
        by_context.setdefault(candidate_context(row), []).append(row)

    outputs: list[dict] = []
    for event in content_events(event_rows):
        for side in ("reference", "comparison"):
            selected_id = event.get(f"{side}_candidate_id", "")
            selected = by_candidate.get(selected_id)
            if selected is None:
                outputs.append(
                    {
                        "pair_index": int(finite(event.get("pair_index"), -1)),
                        "side": side,
                        "selected_candidate_id": selected_id,
                        "available": False,
                        "reason": "selected_candidate_missing_from_waveform_grid",
                        "radius_seed_ready": False,
                    }
                )
                continue
            family = rank_radius_family(by_context.get(candidate_context(selected), []))
            if not family:
                outputs.append(
                    {
                        "pair_index": int(finite(event.get("pair_index"), -1)),
                        "side": side,
                        "selected_candidate_id": selected_id,
                        "available": False,
                        "reason": "radius_family_missing",
                        "radius_seed_ready": False,
                    }
                )
                continue

            best = family[0]
            second = family[1] if len(family) > 1 else None
            correlations = [finite(row.get("absolute_correlation")) for row in family]
            selected_rank = next(
                (
                    index + 1
                    for index, row in enumerate(family)
                    if row.get("candidate_id", "") == selected_id
                ),
                math.nan,
            )
            best_gap = (
                finite(best.get("absolute_correlation")) - finite(second.get("absolute_correlation"))
                if second is not None
                else math.inf
            )
            selected_gap_to_best = finite(best.get("absolute_correlation")) - finite(
                selected.get("absolute_correlation")
            )
            label = "strong_radius_separation" if best_gap >= min_radius_corr_gap else "weak_radius_separation"
            output = side_selection(event, side, selected)
            output.update(
                {
                    "available": True,
                    "reason": "",
                    "valid_radius_count": len(family),
                    "tested_radii_mm": ",".join(f"{finite(row.get('radius_mm')):g}" for row in family),
                    "best_candidate_id": best.get("candidate_id", ""),
                    "best_radius_mm": finite(best.get("radius_mm")),
                    "best_absolute_correlation": finite(best.get("absolute_correlation")),
                    "second_best_radius_mm": finite(second.get("radius_mm")) if second is not None else math.nan,
                    "second_best_absolute_correlation": (
                        finite(second.get("absolute_correlation")) if second is not None else math.nan
                    ),
                    "best_second_abs_correlation_gap": best_gap,
                    "selected_rank_by_correlation": selected_rank,
                    "selected_gap_to_best_abs_correlation": selected_gap_to_best,
                    "radius_absolute_correlation_span": max(correlations) - min(correlations)
                    if correlations
                    else math.nan,
                    "selected_is_best_radius": selected_rank == 1,
                    "radius_resolution_label": label,
                    "radius_seed_ready": selected_rank == 1 and best_gap >= min_radius_corr_gap,
                }
            )
            outputs.append(output)
    return sorted(outputs, key=lambda row: (row.get("pair_index", -1), row.get("side", "")))


def _family_by_radius(waveform_rows: list[dict], selected: dict) -> dict[float, dict]:
    context = candidate_context(selected)
    family = [row for row in waveform_rows if candidate_context(row) == context]
    by_radius: dict[float, dict] = {}
    for row in rank_radius_family(family):
        radius = finite(row.get("radius_mm"))
        if not math.isfinite(radius):
            continue
        by_radius.setdefault(radius, row)
    return by_radius


def build_common_radius_rows(
    event_rows: list[dict],
    waveform_rows: list[dict],
    *,
    min_loss_tolerance: float = DEFAULT_COMMON_RADIUS_MIN_LOSS_TOL,
    mean_loss_tolerance: float = DEFAULT_COMMON_RADIUS_MEAN_LOSS_TOL,
) -> list[dict]:
    valid_rows = valid_waveform_rows(waveform_rows)
    by_candidate = {row.get("candidate_id", ""): row for row in valid_rows}
    outputs: list[dict] = []
    for event in content_events(event_rows):
        pair_index = int(finite(event.get("pair_index"), -1))
        reference = by_candidate.get(event.get("reference_candidate_id", ""))
        comparison = by_candidate.get(event.get("comparison_candidate_id", ""))
        if reference is None or comparison is None:
            continue
        reference_by_radius = _family_by_radius(valid_rows, reference)
        comparison_by_radius = _family_by_radius(valid_rows, comparison)
        common_radii = sorted(set(reference_by_radius) & set(comparison_by_radius))
        selected_pair_min = finite(event.get("pair_min_absolute_correlation"))
        selected_pair_mean = finite(event.get("pair_mean_absolute_correlation"))
        for radius in common_radii:
            ref = reference_by_radius[radius]
            comp = comparison_by_radius[radius]
            ref_corr = finite(ref.get("absolute_correlation"))
            comp_corr = finite(comp.get("absolute_correlation"))
            pair_min = min(ref_corr, comp_corr)
            pair_mean = float(np.mean([ref_corr, comp_corr]))
            min_loss = selected_pair_min - pair_min
            mean_loss = selected_pair_mean - pair_mean
            outputs.append(
                {
                    "pair_index": pair_index,
                    "content_label": event.get("content_label", ""),
                    "common_radius_mm": radius,
                    "reference_candidate_id": ref.get("candidate_id", ""),
                    "comparison_candidate_id": comp.get("candidate_id", ""),
                    "reference_absolute_correlation": ref_corr,
                    "comparison_absolute_correlation": comp_corr,
                    "pair_min_absolute_correlation": pair_min,
                    "pair_mean_absolute_correlation": pair_mean,
                    "selected_reference_radius_mm": finite(event.get("reference_radius_mm")),
                    "selected_comparison_radius_mm": finite(event.get("comparison_radius_mm")),
                    "selected_pair_min_absolute_correlation": selected_pair_min,
                    "selected_pair_mean_absolute_correlation": selected_pair_mean,
                    "pair_min_loss_vs_selected": min_loss,
                    "pair_mean_loss_vs_selected": mean_loss,
                    "common_radius_near_tie": min_loss <= min_loss_tolerance
                    and mean_loss <= mean_loss_tolerance,
                    "same_radius_pair_supports_qc": pair_min >= 0.80,
                }
            )
    return sorted(outputs, key=lambda row: (row.get("pair_index", -1), row.get("common_radius_mm", math.inf)))


def summarize_radius_degeneracy(
    side_rows: list[dict],
    common_radius_rows: list[dict],
    waveform_summary: dict,
    coherence_summary: dict,
    *,
    min_radius_corr_gap: float = DEFAULT_MIN_RADIUS_CORR_GAP,
) -> dict:
    available_side_rows = [row for row in side_rows if boolish(row.get("available", True))]
    selected_best = [row for row in available_side_rows if boolish(row.get("selected_is_best_radius"))]
    weak = [
        row
        for row in available_side_rows
        if finite(row.get("best_second_abs_correlation_gap"), math.inf) < min_radius_corr_gap
    ]
    gaps = [
        finite(row.get("best_second_abs_correlation_gap"))
        for row in available_side_rows
        if math.isfinite(finite(row.get("best_second_abs_correlation_gap")))
    ]
    spans = [
        finite(row.get("radius_absolute_correlation_span"))
        for row in available_side_rows
        if math.isfinite(finite(row.get("radius_absolute_correlation_span")))
    ]
    pair_ids = sorted({int(row["pair_index"]) for row in available_side_rows})
    mismatch_pairs = 0
    for pair_index in pair_ids:
        pair_sides = [row for row in available_side_rows if int(row["pair_index"]) == pair_index]
        radii = {finite(row.get("selected_radius_mm")) for row in pair_sides}
        if len(radii) > 1:
            mismatch_pairs += 1

    common_by_pair: dict[int, list[dict]] = {}
    for row in common_radius_rows:
        common_by_pair.setdefault(int(row["pair_index"]), []).append(row)
    best_common_rows = []
    for rows in common_by_pair.values():
        best_common_rows.append(
            sorted(
                rows,
                key=lambda row: (
                    -finite(row.get("pair_min_absolute_correlation"), -math.inf),
                    -finite(row.get("pair_mean_absolute_correlation"), -math.inf),
                    finite(row.get("common_radius_mm"), math.inf),
                ),
            )[0]
        )
    near_tie_pairs = {
        int(row["pair_index"])
        for row in common_radius_rows
        if boolish(row.get("common_radius_near_tie")) and boolish(row.get("same_radius_pair_supports_qc"))
    }
    min_losses = [
        finite(row.get("pair_min_loss_vs_selected"))
        for row in best_common_rows
        if math.isfinite(finite(row.get("pair_min_loss_vs_selected")))
    ]
    mean_losses = [
        finite(row.get("pair_mean_loss_vs_selected"))
        for row in best_common_rows
        if math.isfinite(finite(row.get("pair_mean_loss_vs_selected")))
    ]

    radius_seed_ready = (
        len(available_side_rows) > 0
        and len(selected_best) == len(available_side_rows)
        and not weak
        and mismatch_pairs == 0
        and not near_tie_pairs
    )
    waveform_ready = bool(coherence_summary.get("ready_for_waveform_morphology_qc", False))
    return {
        "policy_label": "gssi51600s_field_short_anchor_radius_degeneracy_audit_qc_only",
        "content_pair_count": len(pair_ids),
        "content_side_count": len(available_side_rows),
        "selected_best_radius_side_count": len(selected_best),
        "weak_radius_side_count": len(weak),
        "weak_radius_gap_threshold": min_radius_corr_gap,
        "min_best_second_abs_correlation_gap": min(gaps) if gaps else math.nan,
        "max_best_second_abs_correlation_gap": max(gaps) if gaps else math.nan,
        "max_radius_abs_correlation_span": max(spans) if spans else math.nan,
        "selected_radius_mismatch_pair_count": mismatch_pairs,
        "common_radius_row_count": len(common_radius_rows),
        "common_radius_near_tie_pair_count": len(near_tie_pairs),
        "best_common_radius_max_pair_min_loss": max(min_losses) if min_losses else math.nan,
        "best_common_radius_max_pair_mean_loss": max(mean_losses) if mean_losses else math.nan,
        "source_waveform_valid_candidate_count": waveform_summary.get("valid_candidate_count", ""),
        "source_waveform_selected_event_count": waveform_summary.get("selected_event_count", ""),
        "source_waveform_backend": (
            waveform_summary.get("best_candidate", {}).get("backend", "")
            if isinstance(waveform_summary.get("best_candidate"), dict)
            else ""
        ),
        "ready_for_waveform_morphology_qc": waveform_ready,
        "ready_for_radius_seed": radius_seed_ready,
        "ready_for_radius_recovery": False,
        "ready_for_cover_depth_recovery": False,
        "ready_for_geometry_seed": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "ready_for_heavy_field_work": False,
        "gpu_priority": "none",
        "decision": (
            "Saved content-backed short-anchor waveform evidence supports morphology QC, "
            "but radius remains weakly separated. The selected side-wise best radii disagree "
            "between repeat profiles, and forced common-radius alternatives are near-tied at "
            "the pair level. Do not use these field data as a radius seed, radius-recovery "
            "claim, geometry seed, field FWI trigger, or 3D/HPC workload."
        ),
    }


def build_gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "waveform_morphology_qc",
            "ready": summary["ready_for_waveform_morphology_qc"],
            "allowed_use": "field waveform morphology QC",
            "blocked_use": "none within QC scope",
            "evidence": "source coherence audit reports waveform morphology QC support",
        },
        {
            "gate_key": "radius_seed",
            "ready": summary["ready_for_radius_seed"],
            "allowed_use": "none",
            "blocked_use": "field radius seed for inversion",
            "evidence": (
                f"weak radius sides={summary['weak_radius_side_count']}/"
                f"{summary['content_side_count']}; mismatch pairs="
                f"{summary['selected_radius_mismatch_pair_count']}/{summary['content_pair_count']}"
            ),
        },
        {
            "gate_key": "radius_recovery",
            "ready": summary["ready_for_radius_recovery"],
            "allowed_use": "none",
            "blocked_use": "field radius recovery",
            "evidence": (
                f"min best-second radius correlation gap="
                f"{summary['min_best_second_abs_correlation_gap']:.6f}"
            ),
        },
        {
            "gate_key": "common_radius_near_tie",
            "ready": False,
            "allowed_use": "caveat text only",
            "blocked_use": "treating selected radius mismatch as calibrated radius evidence",
            "evidence": (
                f"near-tied common-radius pairs={summary['common_radius_near_tie_pair_count']}/"
                f"{summary['content_pair_count']}"
            ),
        },
        {
            "gate_key": "field_fwi",
            "ready": summary["ready_for_field_fwi"],
            "allowed_use": "none",
            "blocked_use": "field FWI, 3D/HPC, or heavy field work",
            "evidence": "radius/depth/geometry controls remain unavailable",
        },
    ]


def plot_radius_degeneracy(side_rows: list[dict], common_radius_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), constrained_layout=True)
    colors = {
        "reference": "#4e79a7",
        "comparison": "#f28e2b",
    }
    for row in side_rows:
        if not boolish(row.get("available", True)):
            continue
        pair_index = int(row["pair_index"])
        side = row["side"]
        label = f"pair {pair_index} {side}"
        radii = [finite(value) for value in str(row.get("tested_radii_mm", "")).split(",") if value]
        selected_radius = finite(row.get("selected_radius_mm"))
        context_rows = [
            common
            for common in common_radius_rows
            if int(common["pair_index"]) == pair_index
        ]
        # Use side-specific common rows when possible; otherwise show selected/best points only.
        if context_rows:
            if side == "reference":
                y = [finite(item.get("reference_absolute_correlation")) for item in context_rows]
            else:
                y = [finite(item.get("comparison_absolute_correlation")) for item in context_rows]
            x = [finite(item.get("common_radius_mm")) for item in context_rows]
            axes[0].plot(x, y, marker="o", color=colors[side], alpha=0.75, linewidth=1.2, label=label)
            selected_y = next((value for radius, value in zip(x, y) if math.isclose(radius, selected_radius)), math.nan)
            if math.isfinite(selected_y):
                axes[0].scatter([selected_radius], [selected_y], s=70, facecolors="white", edgecolors=colors[side])
        elif radii:
            axes[0].scatter([selected_radius], [finite(row.get("selected_absolute_correlation"))], color=colors[side], label=label)

    axes[0].axhline(0.80, color="#333333", linestyle="--", linewidth=0.8)
    axes[0].set_xlabel("radius [mm]")
    axes[0].set_ylabel("absolute correlation")
    axes[0].set_title("Saved radius sweep around content anchors")
    axes[0].grid(color="#dddddd", linewidth=0.6)
    handles, labels = axes[0].get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    axes[0].legend(unique.values(), unique.keys(), fontsize=8, frameon=False)

    pair_ids = sorted({int(row["pair_index"]) for row in common_radius_rows})
    x = np.arange(len(pair_ids))
    selected_min = []
    best_common_min = []
    selected_mean = []
    best_common_mean = []
    labels = []
    for pair_index in pair_ids:
        rows = [row for row in common_radius_rows if int(row["pair_index"]) == pair_index]
        best = sorted(
            rows,
            key=lambda row: (
                -finite(row.get("pair_min_absolute_correlation"), -math.inf),
                -finite(row.get("pair_mean_absolute_correlation"), -math.inf),
            ),
        )[0]
        selected_min.append(finite(best.get("selected_pair_min_absolute_correlation")))
        selected_mean.append(finite(best.get("selected_pair_mean_absolute_correlation")))
        best_common_min.append(finite(best.get("pair_min_absolute_correlation")))
        best_common_mean.append(finite(best.get("pair_mean_absolute_correlation")))
        labels.append(f"pair {pair_index}")

    width = 0.20
    axes[1].bar(x - 1.5 * width, selected_min, width=width, color="#59a14f", label="selected min")
    axes[1].bar(x - 0.5 * width, best_common_min, width=width, color="#8cd17d", label="best common min")
    axes[1].bar(x + 0.5 * width, selected_mean, width=width, color="#b07aa1", label="selected mean")
    axes[1].bar(x + 1.5 * width, best_common_mean, width=width, color="#d4a6c8", label="best common mean")
    axes[1].set_xticks(x, labels)
    axes[1].set_ylim(0.75, 0.91)
    axes[1].set_ylabel("absolute correlation")
    axes[1].set_title("Forced common-radius near-tie check")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(fontsize=8, frameon=False)
    axes[1].text(
        0.03,
        0.05,
        f"weak radius sides: {summary['weak_radius_side_count']}/{summary['content_side_count']}\n"
        f"radius mismatch pairs: {summary['selected_radius_mismatch_pair_count']}/{summary['content_pair_count']}\n"
        f"common-radius near ties: {summary['common_radius_near_tie_pair_count']}/{summary['content_pair_count']}\n"
        f"radius seed ready: {summary['ready_for_radius_seed']}",
        transform=axes[1].transAxes,
        va="bottom",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI 51600S short-anchor radius degeneracy audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, side_csv: Path, common_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_short_anchor_radius_degeneracy_audit.png`",
                "",
                "This CPU-only figure audits whether saved field-to-synthetic waveform",
                "candidates provide a calibrated radius seed for the two content-backed",
                "short anchors.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Content pairs: `{summary['content_pair_count']}`.",
                f"Weak radius sides: `{summary['weak_radius_side_count']}`.",
                f"Selected radius mismatch pairs: `{summary['selected_radius_mismatch_pair_count']}`.",
                f"Common-radius near-tie pairs: `{summary['common_radius_near_tie_pair_count']}`.",
                f"Ready for radius seed: `{summary['ready_for_radius_seed']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Side-wise radius rows: `{side_csv.name}`.",
                f"- Forced common-radius rows: `{common_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved field waveform candidate grids only. It does",
                "not run DZT preprocessing, FDTD, FWI, GPU kernels, 3D/HPC jobs, or",
                "neural-network training.",
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
    parser.add_argument("--content-synthetic-run", default=DEFAULT_CONTENT_SYNTHETIC_RUN)
    parser.add_argument("--waveform-run", default=DEFAULT_WAVEFORM_RUN)
    parser.add_argument("--waveform-coherence-run", default=DEFAULT_WAVEFORM_COHERENCE_RUN)
    parser.add_argument("--min-radius-corr-gap", type=float, default=DEFAULT_MIN_RADIUS_CORR_GAP)
    parser.add_argument("--common-radius-min-loss-tol", type=float, default=DEFAULT_COMMON_RADIUS_MIN_LOSS_TOL)
    parser.add_argument("--common-radius-mean-loss-tol", type=float, default=DEFAULT_COMMON_RADIUS_MEAN_LOSS_TOL)
    parser.add_argument("--run-name", default="gssi51600s_field_short_anchor_radius_degeneracy_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    field_root = field_dataset_output_root(args.field_root, args.dataset_id)
    content_dir = field_root / args.content_synthetic_run
    waveform_dir = field_root / args.waveform_run
    coherence_dir = field_root / args.waveform_coherence_run

    event_rows = read_csv_rows(content_dir / "data/short_profile_content_synthetic_event_matches.csv")
    waveform_rows = read_csv_rows(waveform_dir / "data/field_synthetic_waveform_probe.csv")
    waveform_summary = read_json(waveform_dir / "data/field_synthetic_waveform_probe_summary.json")
    coherence_summary = read_json(coherence_dir / "data/field_short_anchor_waveform_coherence_summary.json")

    side_rows = build_radius_side_rows(event_rows, waveform_rows, min_radius_corr_gap=args.min_radius_corr_gap)
    common_rows = build_common_radius_rows(
        event_rows,
        waveform_rows,
        min_loss_tolerance=args.common_radius_min_loss_tol,
        mean_loss_tolerance=args.common_radius_mean_loss_tol,
    )
    summary = summarize_radius_degeneracy(
        side_rows,
        common_rows,
        waveform_summary,
        coherence_summary,
        min_radius_corr_gap=args.min_radius_corr_gap,
    )
    gates = build_gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=field_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    side_csv = data_dir / "field_short_anchor_radius_degeneracy_side_rows.csv"
    common_csv = data_dir / "field_short_anchor_common_radius_rows.csv"
    gates_csv = data_dir / "field_short_anchor_radius_degeneracy_gates.csv"
    summary_json = data_dir / "field_short_anchor_radius_degeneracy_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_short_anchor_radius_degeneracy_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(side_csv, [json_safe(row) for row in side_rows])
    write_csv(common_csv, [json_safe(row) for row in common_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_radius_degeneracy(side_rows, common_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, side_csv, common_csv)

    summary["paths"] = {
        "side_rows_csv": str(side_csv),
        "common_radius_rows_csv": str(common_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "source_content_synthetic_rows_csv": str(
            content_dir / "data/short_profile_content_synthetic_event_matches.csv"
        ),
        "source_waveform_probe_csv": str(waveform_dir / "data/field_synthetic_waveform_probe.csv"),
        "source_waveform_summary_json": str(waveform_dir / "data/field_synthetic_waveform_probe_summary.json"),
        "source_waveform_coherence_summary_json": str(
            coherence_dir / "data/field_short_anchor_waveform_coherence_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_short_anchor_radius_degeneracy_audit",
        {
            "content_synthetic_run": args.content_synthetic_run,
            "waveform_run": args.waveform_run,
            "waveform_coherence_run": args.waveform_coherence_run,
            "min_radius_corr_gap": args.min_radius_corr_gap,
            "common_radius_min_loss_tol": args.common_radius_min_loss_tol,
            "common_radius_mean_loss_tol": args.common_radius_mean_loss_tol,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

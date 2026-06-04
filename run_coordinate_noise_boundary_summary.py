#!/usr/bin/env python3
"""Summarize a coordinate-confidence noise boundary bracket."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


NOISE_RE = re.compile(r"noise(?P<noise>\d+(?:p\d+)?)_seed(?P<seed>\d+)")
EXPERIMENT_RE = re.compile(r"^(?P<experiment_id>\d{3,})_")


def _float_or_none(value):
    if value in ("", None):
        return None
    return float(value)


def _interval_width(row, min_key, max_key):
    lower = _float_or_none(row.get(min_key))
    upper = _float_or_none(row.get(max_key))
    if lower is None or upper is None:
        return None
    return max(0.0, upper - lower)


def _exact(value, truth, tol=1.0e-9):
    if value is None or truth is None:
        return False
    return abs(float(value) - float(truth)) <= tol


def parse_noise_seed(text):
    """Return ``(noise_rms_percent, seed)`` from a coordinate case or run label."""
    match = NOISE_RE.search(str(text))
    if not match:
        raise ValueError(f"could not parse noise/seed from {text!r}")
    return float(match.group("noise").replace("p", ".")), int(match.group("seed"))


def experiment_id_from_path(path):
    """Return the numeric experiment id from an output path, when available."""
    for part in Path(path).parts:
        match = EXPERIMENT_RE.match(part)
        if match:
            return int(match.group("experiment_id"))
    return None


def load_json(path):
    """Load JSON from disk."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _truth_for_target(summary, target_index):
    truth_radii = summary.get("truth_radius_values_mm")
    truth_radius = (
        truth_radii[target_index]
        if truth_radii is not None
        else summary.get("truth_radius_mm")
    )
    return (
        float(summary["true_x_values_mm"][target_index]),
        float(summary["true_z_values_mm"][target_index]),
        float(truth_radius),
    )


def _main_confidence_row(summary, source_mismatch):
    rows = summary.get("confidence_rows") or []
    for row in rows:
        label = str(row.get("case_label", ""))
        is_mismatch = label.startswith("source_mismatch_")
        if is_mismatch == source_mismatch and row.get("step_kind", "main") == "main":
            return row
    raise ValueError(f"missing {'source-mismatch' if source_mismatch else 'nominal'} confidence row")


def _diagnostic_row(summary, case_label, objective_label):
    for row in summary.get("objective_diagnostic_rows") or []:
        if row.get("case_label") == case_label and row.get("objective_label") == objective_label:
            return row
    return None


def _row_status(row, truth):
    best_x = _float_or_none(row.get("best_x_mm"))
    best_z = _float_or_none(row.get("best_z_mm"))
    best_radius = _float_or_none(row.get("best_radius_mm"))
    is_truth_geometry = (
        _exact(best_x, truth[0])
        and _exact(best_z, truth[1])
        and _exact(best_radius, truth[2])
    )
    x_width = _interval_width(row, "ambiguity_x_min_mm", "ambiguity_x_max_mm")
    z_width = _interval_width(row, "ambiguity_z_min_mm", "ambiguity_z_max_mm")
    radius_width = _interval_width(
        row,
        "ambiguity_radius_min_mm",
        "ambiguity_radius_max_mm",
    )
    zero_width = (
        (x_width is not None and x_width == 0.0)
        and (z_width is not None and z_width == 0.0)
        and (radius_width is not None and radius_width == 0.0)
    )
    if not is_truth_geometry:
        return "wrong_best_geometry"
    if row.get("fallback_warning"):
        return "fallback_warning"
    if row.get("confidence_label") == "strong" and zero_width:
        return "clean"
    if row.get("confidence_label") == "strong" and x_width and x_width > 0.0:
        return "point_correct_x_ambiguous"
    if row.get("confidence_label") == "strong":
        return "point_correct_other_ambiguity"
    return "point_correct_not_strong"


def _competing_margin_to_cutoff(row):
    competing = _float_or_none(row.get("competing_geometry_misfit"))
    threshold = _float_or_none(row.get("ambiguity_misfit_threshold"))
    if competing is None or threshold is None:
        return None
    return competing - threshold


def _competing_gap(row):
    competing = _float_or_none(row.get("competing_geometry_misfit"))
    best = _float_or_none(row.get("best_misfit"))
    if competing is None or best is None:
        return None, None
    gap = competing - best
    rel = gap / max(abs(best), 1.0e-12)
    return gap, rel


def _case_metrics(prefix, row, truth):
    status = _row_status(row, truth)
    gap, rel_gap = _competing_gap(row)
    margin_to_cutoff = _competing_margin_to_cutoff(row)
    return {
        f"{prefix}_case_label": row.get("case_label"),
        f"{prefix}_status": status,
        f"{prefix}_best_x_mm": _float_or_none(row.get("best_x_mm")),
        f"{prefix}_best_z_mm": _float_or_none(row.get("best_z_mm")),
        f"{prefix}_best_radius_mm": _float_or_none(row.get("best_radius_mm")),
        f"{prefix}_confidence_label": row.get("confidence_label"),
        f"{prefix}_fallback_warning": row.get("fallback_warning") or "",
        f"{prefix}_radius_margin_abs": _float_or_none(row.get("radius_margin_abs")),
        f"{prefix}_radius_margin_rel": _float_or_none(row.get("radius_margin_rel")),
        f"{prefix}_best_misfit": _float_or_none(row.get("best_misfit")),
        f"{prefix}_competing_x_mm": _float_or_none(row.get("competing_geometry_x_mm")),
        f"{prefix}_competing_z_mm": _float_or_none(row.get("competing_geometry_z_mm")),
        f"{prefix}_competing_radius_mm": _float_or_none(row.get("competing_geometry_radius_mm")),
        f"{prefix}_competing_misfit": _float_or_none(row.get("competing_geometry_misfit")),
        f"{prefix}_competing_gap_abs": gap,
        f"{prefix}_competing_gap_rel": rel_gap,
        f"{prefix}_competing_margin_to_cutoff": margin_to_cutoff,
        f"{prefix}_ambiguity_candidate_count": row.get("ambiguity_candidate_count"),
        f"{prefix}_ambiguity_x_width_mm": _interval_width(
            row,
            "ambiguity_x_min_mm",
            "ambiguity_x_max_mm",
        ),
        f"{prefix}_ambiguity_z_width_mm": _interval_width(
            row,
            "ambiguity_z_min_mm",
            "ambiguity_z_max_mm",
        ),
        f"{prefix}_ambiguity_radius_width_mm": _interval_width(
            row,
            "ambiguity_radius_min_mm",
            "ambiguity_radius_max_mm",
        ),
    }


def build_boundary_row(summary, summary_path=None):
    """Build one scalar noise-boundary row from a coordinate optimizer summary."""
    nominal = _main_confidence_row(summary, source_mismatch=False)
    mismatch = _main_confidence_row(summary, source_mismatch=True)
    noise_rms_percent, seed = parse_noise_seed(nominal["case_label"])
    target_index = int(nominal["step_target_index"])
    truth = _truth_for_target(summary, target_index)
    nominal_highband = _diagnostic_row(summary, nominal["case_label"], "highband")
    mismatch_highband = _diagnostic_row(summary, mismatch["case_label"], "highband")
    row = {
        "experiment_id": experiment_id_from_path(summary_path or summary.get("run_name", "")),
        "run_name": summary.get("run_name"),
        "summary_path": summary_path,
        "noise_rms_percent": noise_rms_percent,
        "seed": seed,
        "sources": summary.get("sources"),
        "tx_rx_offset_mm": summary.get("tx_rx_offset_mm"),
        "frequency_ghz": summary.get("frequency_ghz"),
        "target_index": target_index,
        "candidate_count": nominal.get("candidate_count"),
        "truth_x_mm": truth[0],
        "truth_z_mm": truth[1],
        "truth_radius_mm": truth[2],
    }
    row.update(_case_metrics("nominal", nominal, truth))
    row.update(_case_metrics("source_mismatch", mismatch, truth))
    row.update({
        "nominal_highband_radius_margin_abs": (
            None if nominal_highband is None else _float_or_none(nominal_highband.get("radius_margin_abs"))
        ),
        "source_mismatch_highband_radius_margin_abs": (
            None if mismatch_highband is None else _float_or_none(mismatch_highband.get("radius_margin_abs"))
        ),
    })
    clean = row["nominal_status"] == "clean" and row["source_mismatch_status"] == "clean"
    point_correct_not_clean = (
        row["nominal_status"].startswith("point_correct")
        and row["source_mismatch_status"].startswith(("clean", "point_correct"))
    )
    if clean:
        decision_class = "clean"
    elif point_correct_not_clean:
        decision_class = "point_correct_not_clean"
    else:
        decision_class = "failed"
    row.update({
        "clean_for_scalar_bracket": clean,
        "decision_class": decision_class,
    })
    return row


def clean_aggregate_metrics(clean_aggregate_json):
    """Load the replicated-clean aggregate metrics, if supplied."""
    if not clean_aggregate_json:
        return None
    report = load_json(clean_aggregate_json)
    aggregate = report.get("aggregate", report)
    return {
        "path": clean_aggregate_json,
        "row_count": aggregate.get("row_count"),
        "truth_geometry_count": aggregate.get("truth_geometry_count"),
        "x_ambiguity_row_count": aggregate.get("x_ambiguity_row_count"),
        "fallback_warning_count": aggregate.get("fallback_warning_count"),
        "confidence_label_counts": aggregate.get("confidence_label_counts"),
        "radius_margin_abs_min": aggregate.get("radius_margin_abs_min"),
        "radius_margin_abs_mean": aggregate.get("radius_margin_abs_mean"),
        "radius_margin_abs_max": aggregate.get("radius_margin_abs_max"),
    }


def summarize_boundary(rows, promoted_clean_noise_rms_percent=None, clean_aggregate=None, tolerance=1.0e-9):
    """Summarize clean and ambiguous endpoints for a noise bracket."""
    rows = sorted(rows, key=lambda row: float(row["noise_rms_percent"]))
    clean_rows = [row for row in rows if row["clean_for_scalar_bracket"]]
    ambiguous_rows = [row for row in rows if not row["clean_for_scalar_bracket"]]
    if promoted_clean_noise_rms_percent is None:
        if not clean_rows:
            raise ValueError("no clean rows and no promoted clean endpoint supplied")
        promoted_clean_noise_rms_percent = max(float(row["noise_rms_percent"]) for row in clean_rows)
    upper_rows = [
        row for row in ambiguous_rows
        if float(row["noise_rms_percent"]) > float(promoted_clean_noise_rms_percent)
    ]
    final_upper = min(upper_rows, key=lambda row: float(row["noise_rms_percent"])) if upper_rows else None
    smallest_abs_margin = None
    if final_upper and final_upper.get("nominal_competing_margin_to_cutoff") is not None:
        smallest_abs_margin = abs(float(final_upper["nominal_competing_margin_to_cutoff"]))
    return {
        "row_count": len(rows),
        "clean_row_count": len(clean_rows),
        "point_correct_not_clean_row_count": sum(
            1 for row in rows if row["decision_class"] == "point_correct_not_clean"
        ),
        "promoted_clean_noise_rms_percent": float(promoted_clean_noise_rms_percent),
        "single_seed_clean_noise_rms_percent_max": (
            None if not clean_rows else max(float(row["noise_rms_percent"]) for row in clean_rows)
        ),
        "final_ambiguous_upper_noise_rms_percent": (
            None if final_upper is None else float(final_upper["noise_rms_percent"])
        ),
        "final_ambiguous_upper_experiment_id": (
            None if final_upper is None else final_upper["experiment_id"]
        ),
        "final_ambiguous_upper_nominal_margin_to_cutoff": (
            None if final_upper is None else final_upper.get("nominal_competing_margin_to_cutoff")
        ),
        "final_bracket_width_percent_rms": (
            None
            if final_upper is None
            else float(final_upper["noise_rms_percent"]) - float(promoted_clean_noise_rms_percent)
        ),
        "cutoff_margin_stop_tolerance": tolerance,
        "stop_due_to_numerical_edge": (
            False if smallest_abs_margin is None else smallest_abs_margin <= float(tolerance)
        ),
        "clean_aggregate": clean_aggregate,
    }


def write_rows_csv(rows, path):
    """Write boundary rows to CSV."""
    rows = list(rows)
    if not rows:
        raise ValueError("no rows to write")
    fieldnames = list(rows[0].keys())
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _row_label(row):
    exp = row.get("experiment_id")
    exp_text = "exp?" if exp is None else f"exp{int(exp)}"
    return f"{exp_text}\n{float(row['noise_rms_percent']):.15g}%"


def plot_cutoff_margin(rows, save_path, tolerance=1.0e-9):
    """Plot margin between the nearest x competitor and the ambiguity cutoff."""
    rows = sorted(rows, key=lambda row: float(row["noise_rms_percent"]))
    labels = [_row_label(row) for row in rows]
    values = [float(row["nominal_competing_margin_to_cutoff"]) for row in rows]
    colors = [
        "#1b7837" if row["clean_for_scalar_bracket"] else "#d95f02"
        for row in rows
    ]
    fig, ax = plt.subplots(figsize=(10.5, 5.4), constrained_layout=True)
    positions = list(range(len(rows)))
    ax.scatter(positions, values, c=colors, s=70, edgecolor="#222222", linewidth=0.8)
    ax.axhline(0.0, color="#111111", linewidth=1.0, label="ambiguity cutoff")
    ax.axhline(tolerance, color="#555555", linestyle=":", linewidth=0.9, label="+/- stop tolerance")
    ax.axhline(-tolerance, color="#555555", linestyle=":", linewidth=0.9)
    ax.set_yscale("symlog", linthresh=max(float(tolerance), 1.0e-12))
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, rotation=0, fontsize=8)
    ax.set_ylabel("x263/r8 misfit minus ambiguity cutoff")
    ax.set_title("Seed34 Close-14 Target-2 Noise Boundary")
    ax.grid(True, axis="y", alpha=0.25)
    ax.legend(loc="best", frameon=False, fontsize=8)
    for pos, row, value in zip(positions, rows, values):
        text = "clean" if row["clean_for_scalar_bracket"] else "x interval"
        ax.annotate(
            text,
            (pos, value),
            xytext=(0, 9),
            textcoords="offset points",
            ha="center",
            fontsize=7,
        )
    save_validated_figure(fig, save_path)
    plt.close(fig)


def plot_ambiguity_widths(rows, save_path):
    """Plot nominal and source-mismatch x ambiguity interval widths."""
    rows = sorted(rows, key=lambda row: float(row["noise_rms_percent"]))
    labels = [_row_label(row) for row in rows]
    nominal = [float(row["nominal_ambiguity_x_width_mm"]) for row in rows]
    mismatch = [float(row["source_mismatch_ambiguity_x_width_mm"]) for row in rows]
    positions = list(range(len(rows)))
    bar_width = 0.34
    fig, ax = plt.subplots(figsize=(10.5, 5.2), constrained_layout=True)
    ax.bar(
        [pos - bar_width / 2.0 for pos in positions],
        nominal,
        width=bar_width,
        color="#4C78A8",
        label="nominal noise row",
    )
    ax.bar(
        [pos + bar_width / 2.0 for pos in positions],
        mismatch,
        width=bar_width,
        color="#F58518",
        label="source-mismatch row",
    )
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("x ambiguity interval width [mm]")
    ax.set_title("Boundary X Ambiguity Widths")
    ax.set_ylim(0.0, max(1.25, max(nominal + mismatch) * 1.25))
    ax.grid(True, axis="y", alpha=0.25)
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    save_validated_figure(fig, save_path)
    plt.close(fig)


def plot_radius_margins(rows, save_path):
    """Plot base and high-band radius margins across the boundary rows."""
    rows = sorted(rows, key=lambda row: float(row["noise_rms_percent"]))
    labels = [_row_label(row) for row in rows]
    positions = list(range(len(rows)))
    series = [
        ("nominal base", "nominal_radius_margin_abs", "#4C78A8"),
        ("nominal high-band", "nominal_highband_radius_margin_abs", "#72B7B2"),
        ("source-mismatch base", "source_mismatch_radius_margin_abs", "#F58518"),
        ("source-mismatch high-band", "source_mismatch_highband_radius_margin_abs", "#54A24B"),
    ]
    bar_width = 0.18
    fig, ax = plt.subplots(figsize=(11.2, 5.4), constrained_layout=True)
    offsets = [-1.5 * bar_width, -0.5 * bar_width, 0.5 * bar_width, 1.5 * bar_width]
    for offset, (label, key, color) in zip(offsets, series):
        values = [0.0 if row.get(key) is None else float(row[key]) for row in rows]
        ax.bar(
            [pos + offset for pos in positions],
            values,
            width=bar_width,
            color=color,
            label=label,
        )
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Best-vs-next-radius objective gap")
    ax.set_title("Radius Margins Remain Strong Across the Boundary")
    ax.grid(True, axis="y", alpha=0.25)
    ax.legend(loc="upper left", frameon=False, fontsize=8, ncols=2)
    save_validated_figure(fig, save_path)
    plt.close(fig)


def write_figure_notes(path, boundary):
    """Write figure notes for the noise boundary plots."""
    summary = boundary["summary"]
    final_upper = summary.get("final_ambiguous_upper_noise_rms_percent")
    final_margin = summary.get("final_ambiguous_upper_nominal_margin_to_cutoff")
    lines = [
        "# Figure Notes",
        "",
        "## 1. `noise_boundary_cutoff_margin.png` - clean versus ambiguous cutoff",
        "",
        "This figure shows the final close-14 target-2 seed34 noise bracket under",
        "4 sources and 50 mm Tx/Rx offset. Tx/Rx means transmitter/receiver spacing.",
        "RMS means root-mean-square noise level as a percent of the clean signal.",
        "",
        "The y value is the x263/r8 competitor misfit minus the ambiguity cutoff.",
        "Positive means the competitor is outside the near-best set, so the x",
        "interval collapses to the true x264 point. Negative means x263/r8 is still",
        "inside the near-best set, so the reported x interval is 263-264 mm.",
        "",
        f"Promoted clean endpoint: {summary['promoted_clean_noise_rms_percent']}% RMS. "
        f"Final ambiguous upper endpoint: {final_upper}% RMS with margin {final_margin}.",
        "",
        "## 2. `noise_boundary_x_ambiguity_widths.png` - x interval widths",
        "",
        "This figure shows the lateral position interval width for the nominal",
        "noise row and the source-mismatch row. A 0 mm width means the confidence",
        "report has one x location. A 1 mm width means both x263 and x264 remain",
        "inside the ambiguity rule.",
        "",
        "## 3. `noise_boundary_radius_margins.png` - radius evidence",
        "",
        "This figure checks that the boundary failure is lateral x ambiguity, not a",
        "radius failure. The radius margin is the objective gap between the best",
        "radius and the next tested radius. Larger gaps mean stronger radius",
        "separation. High-band is the diagnostic objective that emphasizes higher",
        "frequencies.",
        "",
        "Inspect the cutoff-margin figure first; it carries the stop decision.",
    ]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary_json", nargs="+", help="coordinate optimizer summary JSON paths")
    parser.add_argument("--clean-aggregate-json", default=None)
    parser.add_argument("--promoted-clean-noise-rms-percent", type=float, default=None)
    parser.add_argument("--cutoff-margin-stop-tolerance", type=float, default=1.0e-9)
    parser.add_argument("--run-name", default="coordinate_noise_boundary_summary")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    rows = [
        build_boundary_row(load_json(path), path)
        for path in args.summary_json
    ]
    rows.sort(key=lambda row: float(row["noise_rms_percent"]))
    clean_aggregate = clean_aggregate_metrics(args.clean_aggregate_json)
    summary = summarize_boundary(
        rows,
        promoted_clean_noise_rms_percent=args.promoted_clean_noise_rms_percent,
        clean_aggregate=clean_aggregate,
        tolerance=args.cutoff_margin_stop_tolerance,
    )

    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = Path(outdir) / "data"
    figures_dir = Path(outdir) / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    csv_path = data_dir / "noise_boundary_rows.csv"
    json_path = data_dir / "noise_boundary_summary.json"
    cutoff_plot_path = figures_dir / "noise_boundary_cutoff_margin.png"
    width_plot_path = figures_dir / "noise_boundary_x_ambiguity_widths.png"
    margin_plot_path = figures_dir / "noise_boundary_radius_margins.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"

    write_rows_csv(rows, csv_path)
    plot_cutoff_margin(rows, cutoff_plot_path, tolerance=args.cutoff_margin_stop_tolerance)
    plot_ambiguity_widths(rows, width_plot_path)
    plot_radius_margins(rows, margin_plot_path)

    report = {
        "run_name": args.run_name,
        "input_summary_json": args.summary_json,
        "summary": summary,
        "rows": rows,
        "paths": {
            "csv": str(csv_path),
            "json": str(json_path),
            "cutoff_plot": str(cutoff_plot_path),
            "x_ambiguity_width_plot": str(width_plot_path),
            "radius_margin_plot": str(margin_plot_path),
            "figure_notes": str(notes_path),
        },
    }
    write_figure_notes(notes_path, report)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    manifest_path = write_run_manifest(
        outdir,
        "coordinate_noise_boundary_summary",
        {
            "csv": str(csv_path),
            "json": str(json_path),
            "cutoff_plot": str(cutoff_plot_path),
            "x_ambiguity_width_plot": str(width_plot_path),
            "radius_margin_plot": str(margin_plot_path),
            "figure_notes": str(notes_path),
        },
    )
    print(json.dumps(summary, indent=2))
    print(f"Wrote CSV: {csv_path}")
    print(f"Wrote JSON: {json_path}")
    print(f"Wrote manifest: {manifest_path}")


if __name__ == "__main__":
    main()

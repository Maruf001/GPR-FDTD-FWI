#!/usr/bin/env python3
"""Post-hoc reweight per-frequency source-profiled candidate terms."""

from __future__ import annotations

import argparse
import csv
import json
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
from inversion.frequency_weighting import radius_margin_from_ranked  # noqa: E402
from inversion.radius_confidence import radius_interval_from_curve  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def infer_frequency_keys(fieldnames):
    """Infer frequency keys from candidate CSV fieldnames."""
    prefix = "frequency_misfit_"
    return [
        field[len(prefix):]
        for field in fieldnames
        if field.startswith(prefix)
    ]


def parse_weight_cases(text, frequency_keys):
    """Parse labeled frequency-weight cases."""
    cases = []
    labels = set()
    for item in str(text).split("|"):
        item = item.strip()
        if not item:
            continue
        if ":" not in item:
            raise argparse.ArgumentTypeError("weight cases must be label:w1,w2,...")
        label, values_text = item.split(":", 1)
        label = label.strip()
        if not label or label in labels:
            raise argparse.ArgumentTypeError("weight case labels must be non-empty and unique")
        weights = [float(part.strip()) for part in values_text.split(",") if part.strip()]
        if len(weights) != len(frequency_keys):
            raise argparse.ArgumentTypeError("weight count must match inferred frequency count")
        if any(weight < 0.0 for weight in weights) or not any(weight > 0.0 for weight in weights):
            raise argparse.ArgumentTypeError("weights must be non-negative with at least one positive value")
        labels.add(label)
        cases.append({
            "label": label,
            "weights": {
                key: float(weight)
                for key, weight in zip(frequency_keys, weights)
            },
        })
    if not cases:
        raise argparse.ArgumentTypeError("at least one weight case is required")
    return cases


def read_candidate_rows(path):
    """Read source-profiled candidate CSV rows."""
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [dict(row) for row in reader]
        fieldnames = list(reader.fieldnames or [])
    if not rows:
        raise ValueError("candidate CSV is empty")
    return rows, fieldnames


def weighted_misfit(row, frequency_keys, weights):
    """Compute weighted per-frequency misfit from one candidate row."""
    weight_sum = float(sum(weights.get(key, 0.0) for key in frequency_keys))
    if weight_sum <= 0.0:
        raise ValueError("weight sum must be positive")
    total = 0.0
    for key in frequency_keys:
        total += float(weights.get(key, 0.0)) * float(row[f"frequency_misfit_{key}"])
    return float(total / weight_sum)


def evaluate_weight_cases(rows, frequency_keys, cases):
    """Evaluate all post-hoc weight cases."""
    results = {}
    for case in cases:
        candidates = []
        for row in rows:
            candidates.append({
                "misfit": weighted_misfit(row, frequency_keys, case["weights"]),
                "params": {
                    "x_mm": float(row["x_mm"]),
                    "z_mm": float(row["z_mm"]),
                    "radius_mm": float(row["radius_mm"]),
                },
                "source_profile": {
                    "frequency_scale": float(row["source_frequency_scale"]),
                    "time_shift_ps": float(row["source_time_shift_ps"]),
                    "amplitude_scale": float(row["source_amplitude_scale"]),
                },
            })
        ranked = sorted(candidates, key=lambda item: item["misfit"])
        best_by_radius = {}
        for candidate in candidates:
            radius = candidate["params"]["radius_mm"]
            current = best_by_radius.get(radius)
            if current is None or candidate["misfit"] < current["misfit"]:
                best_by_radius[radius] = candidate
        curve = [best_by_radius[radius] for radius in sorted(best_by_radius)]
        results[case["label"]] = {
            "weights": case["weights"],
            "margin": radius_margin_from_ranked(ranked),
            "exact_tie": radius_interval_from_curve(curve, abs_tolerance=1e-12, rel_tolerance=0.0),
            "weak_interval": radius_interval_from_curve(curve, abs_tolerance=1e-3, rel_tolerance=5e-3),
            "best_curve_by_radius": curve,
        }
    return results


def write_case_summary_csv(path, results):
    """Write one row per frequency-weight case."""
    fieldnames = [
        "case_label",
        "best_radius_mm",
        "next_radius_mm",
        "radius_margin_abs",
        "radius_margin_rel",
        "weak_radius_min_mm",
        "weak_radius_max_mm",
        "weak_radius_count",
    ]
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for label, result in results.items():
            margin = result["margin"]
            weak = result["weak_interval"]
            writer.writerow({
                "case_label": label,
                "best_radius_mm": margin["best_radius_mm"],
                "next_radius_mm": margin["next_radius_mm"],
                "radius_margin_abs": margin["radius_margin_abs"],
                "radius_margin_rel": margin["radius_margin_rel"],
                "weak_radius_min_mm": weak["radius_min_mm"],
                "weak_radius_max_mm": weak["radius_max_mm"],
                "weak_radius_count": weak["radius_count"],
            })


def plot_reweighted_curves(results, save_path):
    """Plot reweighted radius curves."""
    fig, ax = plt.subplots(figsize=(9.4, 5.4), constrained_layout=True)
    for label, result in results.items():
        curve = result["best_curve_by_radius"]
        radii = [item["params"]["radius_mm"] for item in curve]
        values = [item["misfit"] for item in curve]
        ax.plot(radii, values, marker="o", linewidth=1.7, markersize=4.0, label=label)
    ax.set_title("Post-Hoc Frequency Reweighting Diagnostic")
    ax.set_xlabel("Radius [mm]")
    ax.set_ylabel("Weighted per-frequency objective")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="best", fontsize=8, frameon=True)
    return save_validated_figure(fig, save_path)


def write_figure_notes(path, source_csv, frequency_keys, results):
    """Write plain-language notes for the reweighting figure."""
    best_case = max(
        results.items(),
        key=lambda item: float(item[1]["margin"].get("radius_margin_abs", 0.0)),
    )
    label, result = best_case
    margin = result["margin"]
    weak = result["weak_interval"]
    text = f"""# Figure Notes

## 1. `frequency_reweight_radius_profiles.png` - post-hoc frequency weighting

This figure reuses an existing source-profiled candidate CSV and recomputes the
combined objective with different frequency weights. It does not rerun FDTD
and it does not re-optimize the source profile for each new weighting. FDTD
means finite-difference time-domain, the wave solver used to generate the
candidate traces.

The frequency terms came from:

```text
{source_csv}
```

Frequency columns used: `{frequency_keys}`. Lower curves mean better waveform
agreement for that weighted objective.

Main result: the largest post-hoc radius margin is from case `{label}` with
margin `{float(margin['radius_margin_abs']):.6g}`. Its best radius is
`{margin['best_radius_mm']} mm`, and its weak interval is
`{weak['radius_min_mm']}-{weak['radius_max_mm']} mm`. If the weak interval does
not shrink enough, a new weighted GPU run is not justified without a stronger
reason because this cheap diagnostic already shows limited separation.
"""
    Path(path).write_text(text, encoding="utf-8")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-csv", required=True)
    parser.add_argument(
        "--weight-cases",
        default="equal:1,1|hi2:1,2|hi4:1,4|hi8:1,8|hi16:1,16",
        help="Cases as label:w1,w2,... separated by |. Weight order follows inferred frequency columns.",
    )
    parser.add_argument("--run-name", default="source_profiled_frequency_reweight_diagnostic")
    parser.add_argument("--outdir", default=None)
    return parser


def main():
    args = build_parser().parse_args()
    rows, fieldnames = read_candidate_rows(args.candidate_csv)
    frequency_keys = infer_frequency_keys(fieldnames)
    if not frequency_keys:
        raise ValueError("candidate CSV has no frequency_misfit_* columns")
    cases = parse_weight_cases(args.weight_cases, frequency_keys)
    results = evaluate_weight_cases(rows, frequency_keys, cases)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {outdir}")

    summary_csv = data_dir / "frequency_reweight_case_summary.csv"
    summary_json = data_dir / "frequency_reweight_summary.json"
    plot_path = figures_dir / "frequency_reweight_radius_profiles.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"
    write_case_summary_csv(summary_csv, results)
    with summary_json.open("w", encoding="utf-8") as handle:
        json.dump({
            "source_candidate_csv": args.candidate_csv,
            "frequency_keys": frequency_keys,
            "weight_cases": cases,
            "results": results,
        }, handle, indent=2)
    plot_reweighted_curves(results, plot_path)
    plt.close("all")
    write_figure_notes(notes_path, args.candidate_csv, frequency_keys, results)
    write_run_manifest(
        str(outdir),
        "source_profiled_frequency_reweight_diagnostic",
        {
            "summary_csv": str(summary_csv),
            "summary_json": str(summary_json),
            "plot": str(plot_path),
        },
    )
    for label, result in results.items():
        margin = result["margin"]
        weak = result["weak_interval"]
        print(
            f"{label}: best r={margin['best_radius_mm']} mm, "
            f"margin={margin['radius_margin_abs']:.6g}, "
            f"weak={weak['radius_min_mm']}-{weak['radius_max_mm']} mm"
        )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Compare L2 and Softplus/Sinkhorn W2 on shifted Ricker traces."""

from __future__ import annotations

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

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from inversion.trace_distances import least_squares_distance  # noqa: E402
from inversion.trace_wasserstein import softplus_sinkhorn_distance  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def ricker_trace(length=192, center=0.45, width=0.06):
    """Return a normalized Ricker-like pulse on [0, 1]."""
    time = np.linspace(0.0, 1.0, int(length))
    tau = (time - float(center)) / float(width)
    trace = (1.0 - 2.0 * tau ** 2) * np.exp(-tau ** 2)
    return time, trace / max(float(np.max(np.abs(trace))), 1e-12)


def shift_trace_zero_fill(trace, shift_samples):
    """Shift a trace without wraparound."""
    data = np.asarray(trace, dtype=np.float64)
    shifted = np.zeros_like(data)
    shift = int(shift_samples)
    if shift == 0:
        return data.copy()
    if abs(shift) >= data.size:
        return shifted
    if shift > 0:
        shifted[shift:] = data[:-shift]
    else:
        shifted[:shift] = data[-shift:]
    return shifted


def compute_shift_curves(
        shifts,
        length=192,
        beta_values=(4.0, 8.0, 12.0),
        epsilon=0.02,
        downsample=1):
    """Compute L2 and W2 distances over integer sample shifts."""
    _, trace = ricker_trace(length=length)
    rows = []
    for shift in shifts:
        shifted = shift_trace_zero_fill(trace, int(shift))
        row = {
            "shift_samples": int(shift),
            "l2": least_squares_distance(trace, shifted, normalize=True),
        }
        for beta in beta_values:
            row[f"w2_beta_{float(beta):.6g}"] = softplus_sinkhorn_distance(
                trace,
                shifted,
                beta=float(beta),
                epsilon=float(epsilon),
                downsample=int(downsample),
            )
        rows.append(row)
    return rows


def write_csv(path, rows):
    """Write shift curves to CSV."""
    if not rows:
        raise ValueError("no rows to write")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_curves(rows, save_path):
    """Plot distance curves versus shift."""
    shifts = np.array([row["shift_samples"] for row in rows], dtype=np.float64)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.5), constrained_layout=True)

    axes[0].plot(shifts, [row["l2"] for row in rows], color="black", linewidth=2.0)
    axes[0].set_title("Normalized L2")
    axes[0].set_xlabel("Shift [samples]")
    axes[0].set_ylabel("Distance")
    axes[0].grid(True, alpha=0.25)

    w2_keys = [key for key in rows[0] if key.startswith("w2_beta_")]
    for key in w2_keys:
        label = key.replace("w2_beta_", "beta=")
        axes[1].plot(shifts, [row[key] for row in rows], marker="o", markersize=3.2, label=label)
    axes[1].set_title("Softplus Sinkhorn W2")
    axes[1].set_xlabel("Shift [samples]")
    axes[1].set_ylabel("Distance")
    axes[1].grid(True, alpha=0.25)
    axes[1].legend(loc="best", fontsize=8)

    save_validated_figure(fig, save_path)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shift-min", type=int, default=-28)
    parser.add_argument("--shift-max", type=int, default=28)
    parser.add_argument("--length", type=int, default=192)
    parser.add_argument("--beta-values", default="4,8,12")
    parser.add_argument("--epsilon", type=float, default=0.02)
    parser.add_argument("--downsample", type=int, default=1)
    parser.add_argument("--run-name", default="trace_wasserstein_convexity")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    beta_values = [float(part.strip()) for part in args.beta_values.split(",") if part.strip()]
    if not beta_values:
        raise ValueError("at least one beta value is required")
    shifts = list(range(args.shift_min, args.shift_max + 1))

    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = os.path.join(outdir, "data")
    figures_dir = os.path.join(outdir, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    rows = compute_shift_curves(
        shifts,
        length=args.length,
        beta_values=beta_values,
        epsilon=args.epsilon,
        downsample=args.downsample,
    )
    csv_path = os.path.join(data_dir, "trace_w2_convexity.csv")
    plot_path = os.path.join(figures_dir, "trace_w2_convexity.png")
    write_csv(csv_path, rows)
    plot_curves(rows, plot_path)

    zero_row = next(row for row in rows if row["shift_samples"] == 0)
    summary = {
        "run_name": args.run_name,
        "shift_min": args.shift_min,
        "shift_max": args.shift_max,
        "length": args.length,
        "beta_values": beta_values,
        "epsilon": args.epsilon,
        "downsample": args.downsample,
        "zero_shift": zero_row,
        "paths": {
            "csv": csv_path,
            "plot": plot_path,
        },
    }
    summary_path = os.path.join(data_dir, "trace_w2_convexity_summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    write_run_manifest(
        outdir,
        "trace_wasserstein_convexity",
        {
            "summary_path": summary_path,
            "csv": csv_path,
            "plot": plot_path,
        },
    )
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()

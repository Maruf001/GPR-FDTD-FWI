#!/usr/bin/env python3
"""Synthesize close-spacing acquisition policy from confidence aggregates."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_AGGREGATE_CSVS = [
    "outputs/experiments/1222_coordinate_confidence_close50_sources4_txrx25_30_35_40_seed_replicates/data/coordinate_confidence_aggregate.csv",
    "outputs/experiments/293_coordinate_confidence_close45_sources4_txrx35_seed_replicates/data/coordinate_confidence_aggregate.csv",
    "outputs/experiments/297_coordinate_confidence_close40_sources4_txrx35_seed_replicates/data/coordinate_confidence_aggregate.csv",
    "outputs/experiments/301_coordinate_confidence_close35_sources4_txrx35_seed_replicates/data/coordinate_confidence_aggregate.csv",
    "outputs/experiments/305_coordinate_confidence_close30_sources4_txrx35_seed_replicates/data/coordinate_confidence_aggregate.csv",
    "outputs/experiments/314_coordinate_confidence_close28_sources4_txrx35_seed_replicates/data/coordinate_confidence_aggregate.csv",
    "outputs/experiments/310_coordinate_confidence_close25_sources4_txrx40_seed_replicates/data/coordinate_confidence_aggregate.csv",
    "outputs/experiments/319_coordinate_confidence_close28_sources4_txrx45_seed_replicates/data/coordinate_confidence_aggregate.csv",
    "outputs/experiments/323_coordinate_confidence_close25_sources4_txrx45_seed_replicates/data/coordinate_confidence_aggregate.csv",
    "outputs/experiments/327_coordinate_confidence_close20_sources4_txrx45_seed_replicates/data/coordinate_confidence_aggregate.csv",
    "outputs/experiments/331_coordinate_confidence_close15_sources4_txrx45_seed_replicates/data/coordinate_confidence_aggregate.csv",
    "outputs/experiments/335_coordinate_confidence_close14_sources4_txrx45_seed_replicates/data/coordinate_confidence_aggregate.csv",
    "outputs/experiments/1247_coordinate_confidence_close12_sources4_txrx50_seed_replicates/data/coordinate_confidence_aggregate.csv",
    "outputs/experiments/1253_coordinate_confidence_close10_sources4_txrx50_seed_replicates/data/coordinate_confidence_aggregate.csv",
]

POLICY_COLORS = {
    "clean_replicated": "#1B7837",
    "truth_selected_interval": "#D99A19",
    "mixed_or_failed": "#C7302B",
}


def safe_float(value, default=math.nan) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return float(default)
    return out if math.isfinite(out) else float(default)


def truthy(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def finite_values(rows: list[dict], key: str) -> list[float]:
    values = [safe_float(row.get(key)) for row in rows]
    return [value for value in values if math.isfinite(value)]


def positive_count(rows: list[dict], key: str, tol: float = 1.0e-12) -> int:
    return sum(1 for value in finite_values(rows, key) if value > tol)


def parse_close_spacing_mm(text: str) -> float | None:
    match = re.search(r"close(\d+(?:p\d+)?)", str(text))
    if not match:
        return None
    return float(match.group(1).replace("p", "."))


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv_rows(path: Path, rows: list[dict]) -> None:
    rows = [json_safe(row) for row in rows]
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def row_zero_ambiguity(row: dict) -> bool:
    return all(
        abs(safe_float(row.get(key), 0.0)) <= 1.0e-12
        for key in (
            "ambiguity_x_width_mm",
            "ambiguity_z_width_mm",
            "ambiguity_radius_width_mm",
        )
    )


def row_clean(row: dict) -> bool:
    return (
        truthy(row.get("is_truth_geometry"))
        and str(row.get("confidence_label")) in {"moderate", "strong"}
        and row_zero_ambiguity(row)
    )


def policy_label_for_counts(row_count: int, clean_count: int, truth_count: int) -> str:
    if row_count > 0 and clean_count == row_count:
        return "clean_replicated"
    if row_count > 0 and truth_count == row_count:
        return "truth_selected_interval"
    return "mixed_or_failed"


def summarize_group(
    rows: list[dict],
    source_csv: Path,
    close_spacing_mm: float,
    sources: float,
    tx_rx_offset_mm: float,
) -> dict:
    label_counts = Counter(str(row.get("confidence_label", "missing")) for row in rows)
    margins = finite_values(rows, "radius_margin_abs")
    truth_count = sum(1 for row in rows if truthy(row.get("is_truth_geometry")))
    clean_count = sum(1 for row in rows if row_clean(row))
    row_count = len(rows)
    policy_label = policy_label_for_counts(row_count, clean_count, truth_count)
    return {
        "close_spacing_mm": float(close_spacing_mm),
        "sources": float(sources),
        "tx_rx_offset_mm": float(tx_rx_offset_mm),
        "row_count": row_count,
        "truth_geometry_count": truth_count,
        "clean_row_count": clean_count,
        "weak_row_count": label_counts.get("weak", 0),
        "confidence_label_counts": json.dumps(dict(sorted(label_counts.items())), sort_keys=True),
        "x_ambiguity_row_count": positive_count(rows, "ambiguity_x_width_mm"),
        "z_ambiguity_row_count": positive_count(rows, "ambiguity_z_width_mm"),
        "radius_ambiguity_row_count": positive_count(rows, "ambiguity_radius_width_mm"),
        "ambiguity_x_width_max_mm": max(finite_values(rows, "ambiguity_x_width_mm") or [0.0]),
        "ambiguity_z_width_max_mm": max(finite_values(rows, "ambiguity_z_width_mm") or [0.0]),
        "ambiguity_radius_width_max_mm": max(finite_values(rows, "ambiguity_radius_width_mm") or [0.0]),
        "radius_margin_abs_min": min(margins) if margins else math.nan,
        "radius_margin_abs_mean": sum(margins) / len(margins) if margins else math.nan,
        "radius_margin_abs_max": max(margins) if margins else math.nan,
        "truth_geometry_fraction": truth_count / row_count if row_count else math.nan,
        "clean_fraction": clean_count / row_count if row_count else math.nan,
        "policy_label": policy_label,
        "source_aggregate_csv": str(source_csv),
        "source_aggregate_folder": source_csv.parents[1].name,
    }


def load_policy_groups(paths: list[Path]) -> list[dict]:
    grouped: dict[tuple[float, float, float, str], list[dict]] = defaultdict(list)
    source_by_key: dict[tuple[float, float, float, str], Path] = {}
    for path in paths:
        rows = read_csv_rows(path)
        close_spacing = parse_close_spacing_mm(path.parents[1].name)
        if close_spacing is None:
            raise ValueError(f"could not parse close spacing from {path.parents[1].name}")
        for row in rows:
            sources = safe_float(row.get("sources"))
            tx_rx_offset = safe_float(row.get("tx_rx_offset_mm"))
            if not math.isfinite(sources) or not math.isfinite(tx_rx_offset):
                raise ValueError(f"missing sources or tx_rx_offset_mm in {path}")
            key = (float(close_spacing), float(sources), float(tx_rx_offset), str(path))
            grouped[key].append(row)
            source_by_key[key] = path
    out = [
        summarize_group(rows, source_by_key[key], key[0], key[1], key[2])
        for key, rows in grouped.items()
    ]
    return sorted(out, key=lambda row: (row["tx_rx_offset_mm"], -row["close_spacing_mm"], row["source_aggregate_folder"]))


def policy_rank(label: str) -> int:
    return {
        "mixed_or_failed": 0,
        "truth_selected_interval": 1,
        "clean_replicated": 2,
    }.get(label, -1)


def derive_policy_summary(group_rows: list[dict]) -> dict:
    by_txrx: dict[float, list[dict]] = defaultdict(list)
    by_spacing: dict[float, list[dict]] = defaultdict(list)
    for row in group_rows:
        by_txrx[float(row["tx_rx_offset_mm"])].append(row)
        by_spacing[float(row["close_spacing_mm"])].append(row)

    txrx_policy = []
    for txrx, rows in sorted(by_txrx.items()):
        clean = [row for row in rows if row["policy_label"] == "clean_replicated"]
        interval = [row for row in rows if row["policy_label"] == "truth_selected_interval"]
        failed = [row for row in rows if row["policy_label"] == "mixed_or_failed"]
        closest_clean = min((row["close_spacing_mm"] for row in clean), default=None)
        txrx_policy.append({
            "tx_rx_offset_mm": txrx,
            "tested_spacing_count": len(rows),
            "clean_spacing_count": len(clean),
            "interval_spacing_count": len(interval),
            "mixed_or_failed_spacing_count": len(failed),
            "closest_clean_spacing_mm": closest_clean,
            "clean_spacings_mm": ", ".join(str(int(row["close_spacing_mm"])) for row in sorted(clean, key=lambda item: item["close_spacing_mm"])),
            "interval_spacings_mm": ", ".join(str(int(row["close_spacing_mm"])) for row in sorted(interval, key=lambda item: item["close_spacing_mm"])),
            "mixed_or_failed_spacings_mm": ", ".join(str(int(row["close_spacing_mm"])) for row in sorted(failed, key=lambda item: item["close_spacing_mm"])),
        })

    spacing_policy = []
    for spacing, rows in sorted(by_spacing.items()):
        best = max(
            rows,
            key=lambda row: (
                policy_rank(row["policy_label"]),
                -float(row["tx_rx_offset_mm"]),
                safe_float(row.get("radius_margin_abs_min"), -1.0),
            ),
        )
        clean_offsets = sorted(row["tx_rx_offset_mm"] for row in rows if row["policy_label"] == "clean_replicated")
        spacing_policy.append({
            "close_spacing_mm": spacing,
            "tested_tx_rx_offsets_mm": ", ".join(str(int(row["tx_rx_offset_mm"])) for row in sorted(rows, key=lambda item: item["tx_rx_offset_mm"])),
            "best_policy_label": best["policy_label"],
            "minimum_clean_tx_rx_offset_mm": min(clean_offsets) if clean_offsets else None,
            "best_available_tx_rx_offset_mm": best["tx_rx_offset_mm"],
            "best_available_min_margin": best["radius_margin_abs_min"],
        })

    txrx35 = next((row for row in txrx_policy if abs(row["tx_rx_offset_mm"] - 35.0) < 1.0e-9), None)
    txrx45 = next((row for row in txrx_policy if abs(row["tx_rx_offset_mm"] - 45.0) < 1.0e-9), None)
    txrx50 = next((row for row in txrx_policy if abs(row["tx_rx_offset_mm"] - 50.0) < 1.0e-9), None)
    close50_txrx25 = next(
        (
            row for row in group_rows
            if abs(row["close_spacing_mm"] - 50.0) < 1.0e-9
            and abs(row["tx_rx_offset_mm"] - 25.0) < 1.0e-9
        ),
        None,
    )
    close28_txrx35 = next(
        (
            row for row in group_rows
            if abs(row["close_spacing_mm"] - 28.0) < 1.0e-9
            and abs(row["tx_rx_offset_mm"] - 35.0) < 1.0e-9
        ),
        None,
    )
    txrx50_clause = ""
    if txrx50 is not None and txrx50["closest_clean_spacing_mm"] is not None:
        txrx50_clause = (
            f", and 50 mm Tx/Rx reaches close{int(txrx50['closest_clean_spacing_mm'])} "
            "in the tested branch"
        )
    overlap_clause = ""
    if (
        txrx50 is not None
        and txrx50["closest_clean_spacing_mm"] is not None
        and txrx50["closest_clean_spacing_mm"] < 14.0
    ):
        overlap_clause = (
            " The 50 mm Tx/Rx close10/close12 extension is an overlapping-cylinder "
            "algorithmic stress test for the current 6 mm and 8 mm radius pair; "
            "close14 is the non-overlap tangent case."
        )
    decision = (
        "Existing aggregate evidence keeps 35 mm Tx/Rx at close30 as the "
        "standard clean replicated limit, while 45 mm Tx/Rx extends clean "
        f"replication to close14 in the tested branch{txrx50_clause}. "
        "Close50 at Tx/Rx25 is mixed/ambiguous, and close28 at Tx/Rx35 "
        f"remains interval-supported.{overlap_clause}"
    )
    return {
        "group_count": len(group_rows),
        "clean_group_count": sum(1 for row in group_rows if row["policy_label"] == "clean_replicated"),
        "interval_group_count": sum(1 for row in group_rows if row["policy_label"] == "truth_selected_interval"),
        "mixed_or_failed_group_count": sum(1 for row in group_rows if row["policy_label"] == "mixed_or_failed"),
        "tx_rx_policy_rows": txrx_policy,
        "spacing_policy_rows": spacing_policy,
        "standard_35mm_closest_clean_spacing_mm": None if txrx35 is None else txrx35["closest_clean_spacing_mm"],
        "extended_45mm_closest_clean_spacing_mm": None if txrx45 is None else txrx45["closest_clean_spacing_mm"],
        "extended_50mm_closest_clean_spacing_mm": None if txrx50 is None else txrx50["closest_clean_spacing_mm"],
        "close50_txrx25_policy_label": None if close50_txrx25 is None else close50_txrx25["policy_label"],
        "close28_txrx35_policy_label": None if close28_txrx35 is None else close28_txrx35["policy_label"],
        "decision": decision,
    }


def figure_stats(path: Path) -> dict:
    with Image.open(path) as image:
        arr = np.asarray(image.convert("RGB"))
        gray = np.asarray(image.convert("L"))
    sample = arr.reshape(-1, 3)[:: max(1, arr.reshape(-1, 3).shape[0] // 10000)]
    return {
        "path": str(path),
        "width": int(arr.shape[1]),
        "height": int(arr.shape[0]),
        "sampled_unique_colors": int(np.unique(sample, axis=0).shape[0]),
        "nonwhite_fraction": float(np.mean(np.any(arr < 250, axis=2))),
        "dynamic_range": int(gray.max()) - int(gray.min()),
    }


def plot_resolution_policy(group_rows: list[dict], save_path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.2), constrained_layout=True)

    for policy_label, color in POLICY_COLORS.items():
        subset = [row for row in group_rows if row["policy_label"] == policy_label]
        if not subset:
            continue
        sizes = [
            70.0 + min(260.0, 55000.0 * max(0.0, safe_float(row["radius_margin_abs_min"], 0.0)))
            for row in subset
        ]
        axes[0].scatter(
            [row["close_spacing_mm"] for row in subset],
            [row["tx_rx_offset_mm"] for row in subset],
            s=sizes,
            c=color,
            edgecolors="#222222",
            linewidths=0.7,
            label=policy_label.replace("_", " "),
            alpha=0.92,
        )
    for row in group_rows:
        label_offset = (4, -12) if row["close_spacing_mm"] <= 14.5 else (4, 4)
        axes[0].annotate(
            f"{int(row['close_spacing_mm'])}",
            (row["close_spacing_mm"], row["tx_rx_offset_mm"]),
            xytext=label_offset,
            textcoords="offset points",
            fontsize=8,
        )
    axes[0].set_title("Clean vs interval-supported spacing")
    axes[0].set_xlabel("Target spacing [mm]")
    axes[0].set_ylabel("Tx/Rx offset [mm]")
    axes[0].grid(True, alpha=0.25)
    axes[0].legend(loc="lower left", frameon=False, fontsize=8)

    offsets = sorted({row["tx_rx_offset_mm"] for row in group_rows})
    palette = {
        25.0: "#C7302B",
        30.0: "#D99A19",
        35.0: "#1F77B4",
        40.0: "#2CA02C",
        45.0: "#6F4DA8",
        50.0: "#6B6B6B",
    }
    for offset in offsets:
        subset = sorted(
            [row for row in group_rows if row["tx_rx_offset_mm"] == offset],
            key=lambda row: row["close_spacing_mm"],
        )
        axes[1].plot(
            [row["close_spacing_mm"] for row in subset],
            [row["radius_margin_abs_min"] for row in subset],
            marker="o",
            color=palette.get(offset, "#555555"),
            label=f"Tx/Rx {offset:g} mm",
        )
    axes[1].axhline(5.0e-4, color="#333333", linestyle="--", linewidth=1.0, label="5e-4 cutoff")
    axes[1].set_title("Weakest radius margin by acquisition")
    axes[1].set_xlabel("Target spacing [mm]")
    axes[1].set_ylabel("Minimum radius margin")
    axes[1].set_yscale("log")
    axes[1].grid(True, alpha=0.25, which="both")
    axes[1].legend(loc="lower right", frameon=False, fontsize=8)

    fig.suptitle("2D close-spacing acquisition-resolution synthesis", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def write_notes(path: Path, summary: dict) -> None:
    lines = [
        "# Figure Notes",
        "",
        "This CPU-only synthesis reads existing coordinate-confidence aggregate",
        "tables. It does not run FDTD, FWI, or GPU kernels.",
        "",
        "Policy labels:",
        "",
        "- `clean_replicated`: every row selected truth, cleared the confidence label",
        "  as moderate/strong, and had zero x/z/r ambiguity width.",
        "- `truth_selected_interval`: every row selected truth, but at least one row",
        "  retained weak confidence or a nonzero ambiguity interval.",
        "- `mixed_or_failed`: at least one row did not select the exact truth geometry.",
        "",
        "Decision:",
        "",
        summary["decision"],
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_readme(path: Path, group_rows: list[dict], summary: dict) -> None:
    clean = [row for row in group_rows if row["policy_label"] == "clean_replicated"]
    interval = [row for row in group_rows if row["policy_label"] == "truth_selected_interval"]
    failed = [row for row in group_rows if row["policy_label"] == "mixed_or_failed"]
    text = f"""# Coordinate Resolution Policy Synthesis

CPU-only synthesis of existing close-spacing coordinate-confidence aggregates.
No FDTD, FWI, or GPU command was run.

Groups: {len(group_rows)}
Clean replicated groups: {len(clean)}
Truth-selected interval groups: {len(interval)}
Mixed/failed groups: {len(failed)}

Decision:

```text
{summary['decision']}
```
"""
    path.write_text(text, encoding="utf-8")


def existing_default_csvs() -> list[Path]:
    paths = [Path(path) for path in DEFAULT_AGGREGATE_CSVS]
    missing = [path for path in paths if not path.exists()]
    if missing:
        raise FileNotFoundError("missing default aggregate CSVs: " + ", ".join(str(path) for path in missing))
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "aggregate_csv",
        nargs="*",
        help="coordinate_confidence_aggregate.csv paths; defaults to the curated close-spacing policy set",
    )
    parser.add_argument("--run-name", default="coordinate_resolution_policy_synthesis")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    input_paths = [Path(path) for path in args.aggregate_csv] if args.aggregate_csv else existing_default_csvs()
    for path in input_paths:
        if not path.exists():
            raise FileNotFoundError(path)

    group_rows = load_policy_groups(input_paths)
    summary = derive_policy_summary(group_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    group_csv = data_dir / "coordinate_resolution_policy_groups.csv"
    txrx_csv = data_dir / "coordinate_resolution_policy_by_txrx.csv"
    spacing_csv = data_dir / "coordinate_resolution_policy_by_spacing.csv"
    summary_json = data_dir / "coordinate_resolution_policy_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "coordinate_resolution_policy.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"
    readme_path = outdir / "README.md"

    plot_resolution_policy(group_rows, figure_path)
    figure_validation = [figure_stats(figure_path)]
    write_csv_rows(group_csv, group_rows)
    write_csv_rows(txrx_csv, summary["tx_rx_policy_rows"])
    write_csv_rows(spacing_csv, summary["spacing_policy_rows"])
    write_csv_rows(validation_csv, figure_validation)
    summary["input_aggregate_csvs"] = [str(path) for path in input_paths]
    summary["paths"] = {
        "group_csv": str(group_csv),
        "txrx_csv": str(txrx_csv),
        "spacing_csv": str(spacing_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
        "figure_notes": str(notes_path),
        "readme": str(readme_path),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_notes(notes_path, summary)
    write_readme(readme_path, group_rows, summary)
    write_run_manifest(
        str(outdir),
        "coordinate_resolution_policy_synthesis",
        {
            "input_aggregate_csvs": [str(path) for path in input_paths],
            "summary_json": str(summary_json),
            "group_csv": str(group_csv),
            "txrx_csv": str(txrx_csv),
            "spacing_csv": str(spacing_csv),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
            "figure_notes": str(notes_path),
            "readme": str(readme_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

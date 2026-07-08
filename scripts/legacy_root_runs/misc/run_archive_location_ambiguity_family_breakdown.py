#!/usr/bin/env python3
"""Break down exact-strong archive ambiguity rows by experiment family."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
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
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_ROWS_CSV = (
    "outputs/experiments/1281_archive_location_clean_metric_audit/data/"
    "archive_location_clean_metric_rows.csv"
)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def boolish(value) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def compact_values(values: list[float]) -> str:
    finite = sorted({float(value) for value in values if math.isfinite(float(value))})
    return ";".join(f"{value:g}" for value in finite)


def family_label(row: dict) -> str:
    target = str(row.get("target_index", "")).strip() or "unknown"
    text = " ".join([
        str(row.get("aggregate_run", "")),
        str(row.get("run_name", "")),
        str(row.get("case_label", "")),
    ]).lower()
    prefix = f"target{target}"
    if "close14" in text:
        return f"{prefix}_close14"
    if "close50" in text:
        return f"{prefix}_close50"
    if "variable_depth_radius" in text or "xzr_coupled" in text:
        return f"{prefix}_variable_depth_radius"
    if "variable_radius" in text:
        return f"{prefix}_variable_radius_legacy"
    return f"{prefix}_other_archive"


def ambiguity_dimensions(row: dict) -> str:
    dims: list[str] = []
    if boolish(row.get("exact_strong_x_ambiguous")) or safe_float(row.get("x_ambiguity_width_mm"), 0.0) > 0.0:
        dims.append("x")
    if boolish(row.get("exact_strong_z_ambiguous")) or safe_float(row.get("z_ambiguity_width_mm"), 0.0) > 0.0:
        dims.append("z")
    if (
        boolish(row.get("exact_strong_radius_ambiguous"))
        or safe_float(row.get("radius_ambiguity_width_mm"), 0.0) > 0.0
    ):
        dims.append("radius")
    return "+".join(dims)


def normalize_ambiguous_rows(rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    for row in rows:
        exact = boolish(row.get("truth_geometry_match"))
        strong = boolish(row.get("strong_confidence")) or str(row.get("confidence_label")) == "strong"
        dims = ambiguity_dimensions(row)
        if not (exact and strong and dims):
            continue
        case_label = str(row.get("case_label", ""))
        branch_case = "source_mismatch" if case_label.startswith("source_mismatch") else "nominal"
        family = family_label(row)
        out.append({
            "family_label": family,
            "aggregate_run": row.get("aggregate_run", ""),
            "source_csv": row.get("source_csv", ""),
            "run_name": row.get("run_name", ""),
            "case_label": case_label,
            "branch_case": branch_case,
            "target_index": int(safe_float(row.get("target_index"), -1)),
            "sources": safe_float(row.get("sources")),
            "tx_rx_offset_mm": safe_float(row.get("tx_rx_offset_mm")),
            "ambiguity_dimensions": dims,
            "x_ambiguity_width_mm": safe_float(row.get("x_ambiguity_width_mm"), 0.0),
            "z_ambiguity_width_mm": safe_float(row.get("z_ambiguity_width_mm"), 0.0),
            "radius_ambiguity_width_mm": safe_float(row.get("radius_ambiguity_width_mm"), 0.0),
            "publication_action": "exclude_from_strict_location_clean_threshold",
            "gpu_action": "none_now_cpu_reporting_breakdown_only",
        })
    return sorted(out, key=lambda item: (
        item["family_label"],
        item["aggregate_run"],
        item["run_name"],
        item["case_label"],
    ))


def family_breakdown(rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["family_label"]].append(row)

    family_rows: list[dict] = []
    for family, group in sorted(grouped.items()):
        dimension_counts = defaultdict(int)
        for row in group:
            for dim in row["ambiguity_dimensions"].split("+"):
                dimension_counts[dim] += 1
        source_values = [row["sources"] for row in group]
        tx_rx_values = [row["tx_rx_offset_mm"] for row in group]
        target_values = sorted({row["target_index"] for row in group if row["target_index"] >= 0})
        representative_runs = sorted({str(row["aggregate_run"]) for row in group})
        family_rows.append({
            "family_label": family,
            "row_count": len(group),
            "target_indices": ";".join(str(value) for value in target_values),
            "aggregate_run_count": len(representative_runs),
            "representative_aggregate_runs": ";".join(representative_runs[:5]),
            "nominal_row_count": sum(1 for row in group if row["branch_case"] == "nominal"),
            "source_mismatch_row_count": sum(1 for row in group if row["branch_case"] == "source_mismatch"),
            "x_ambiguous_row_count": dimension_counts["x"],
            "z_ambiguous_row_count": dimension_counts["z"],
            "radius_ambiguous_row_count": dimension_counts["radius"],
            "sources_tested": compact_values(source_values),
            "tx_rx_offsets_mm": compact_values(tx_rx_values),
            "max_x_ambiguity_width_mm": max(row["x_ambiguity_width_mm"] for row in group),
            "max_z_ambiguity_width_mm": max(row["z_ambiguity_width_mm"] for row in group),
            "max_radius_ambiguity_width_mm": max(row["radius_ambiguity_width_mm"] for row in group),
            "reporting_action": "treat_as_archive_ambiguity_caveat_not_clean_threshold",
            "gpu_priority": "none_now",
        })
    return family_rows


def summarize_breakdown(ambiguous_rows: list[dict], family_rows: list[dict], total_input_rows: int) -> dict:
    targets = sorted({row["target_index"] for row in ambiguous_rows if row["target_index"] >= 0})
    all_target2 = targets == [2]
    family_count = len(family_rows)
    if ambiguous_rows and all_target2:
        label = "archive_location_ambiguity_target2_family_breakdown_cpu_no_gpu"
    elif ambiguous_rows:
        label = "archive_location_ambiguity_family_breakdown_cpu_no_gpu"
    else:
        label = "archive_location_ambiguity_no_exact_strong_ambiguous_rows"
    return {
        "policy_label": label,
        "input_row_count": total_input_rows,
        "exact_strong_ambiguous_row_count": len(ambiguous_rows),
        "family_count": family_count,
        "target_indices": ";".join(str(value) for value in targets),
        "all_ambiguous_rows_target2": all_target2,
        "x_ambiguous_row_count": sum(1 for row in ambiguous_rows if "x" in row["ambiguity_dimensions"].split("+")),
        "z_ambiguous_row_count": sum(1 for row in ambiguous_rows if "z" in row["ambiguity_dimensions"].split("+")),
        "radius_ambiguous_row_count": sum(
            1 for row in ambiguous_rows if "radius" in row["ambiguity_dimensions"].split("+")
        ),
        "nominal_row_count": sum(1 for row in ambiguous_rows if row["branch_case"] == "nominal"),
        "source_mismatch_row_count": sum(1 for row in ambiguous_rows if row["branch_case"] == "source_mismatch"),
        "max_x_ambiguity_width_mm": max(
            [row["x_ambiguity_width_mm"] for row in ambiguous_rows],
            default=math.nan,
        ),
        "max_z_ambiguity_width_mm": max(
            [row["z_ambiguity_width_mm"] for row in ambiguous_rows],
            default=math.nan,
        ),
        "max_radius_ambiguity_width_mm": max(
            [row["radius_ambiguity_width_mm"] for row in ambiguous_rows],
            default=math.nan,
        ),
        "gpu_priority": "none_now",
        "decision": (
            "The strict-clean exceptions are target2 archive-family caveats. "
            "They support reporting discipline and CPU-side objective design, "
            "not a new broad GPU sweep."
        ),
    }


def plot_breakdown(family_rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["family_label"].replace("target2_", "").replace("_", "\n") for row in family_rows]
    x = np.arange(len(family_rows))
    row_counts = np.asarray([row["row_count"] for row in family_rows], dtype=np.float64)
    x_counts = np.asarray([row["x_ambiguous_row_count"] for row in family_rows], dtype=np.float64)
    z_counts = np.asarray([row["z_ambiguous_row_count"] for row in family_rows], dtype=np.float64)
    radius_counts = np.asarray([row["radius_ambiguous_row_count"] for row in family_rows], dtype=np.float64)

    fig, axes = plt.subplots(1, 2, figsize=(13.4, 4.8), constrained_layout=True)
    axes[0].bar(x, row_counts, color="#4c78a8")
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel("ambiguous exact-strong rows")
    axes[0].set_title("Rows by archive family")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, x_counts, color="#c7302b", label="x")
    axes[1].bar(x, z_counts, bottom=x_counts, color="#f58518", label="z")
    axes[1].bar(x, radius_counts, bottom=x_counts + z_counts, color="#7f3c8d", label="radius")
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("dimension row count")
    axes[1].set_title("Ambiguity dimensions")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)

    fig.suptitle(
        f"Archive ambiguity family breakdown: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows-csv", default=DEFAULT_ROWS_CSV)
    parser.add_argument("--run-name", default="archive_location_ambiguity_family_breakdown")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    input_rows = read_csv_rows(Path(args.rows_csv))
    ambiguous = normalize_ambiguous_rows(input_rows)
    family_rows = family_breakdown(ambiguous)
    summary = summarize_breakdown(ambiguous, family_rows, len(input_rows))

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "archive_location_ambiguity_rows.csv"
    family_csv = data_dir / "archive_location_ambiguity_family_breakdown.csv"
    summary_json = data_dir / "archive_location_ambiguity_family_breakdown_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_breakdown(
        family_rows,
        summary,
        figures_dir / "archive_location_ambiguity_family_breakdown.png",
    ))

    write_csv(rows_csv, [json_safe(row) for row in ambiguous])
    write_csv(family_csv, [json_safe(row) for row in family_rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "input_rows_csv": args.rows_csv,
        **summary,
        "paths": {
            "rows_csv": str(rows_csv),
            "family_breakdown_csv": str(family_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "archive_location_ambiguity_family_breakdown",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "family_breakdown_csv": str(family_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

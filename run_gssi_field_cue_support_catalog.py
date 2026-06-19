#!/usr/bin/env python3
"""Build a measured-field cue/support catalog for the local GSSI 51600S data."""

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
from matplotlib.patches import Patch  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_DATASET_ROOT = field_dataset_output_root(DEFAULT_FIELD_ROOT, DEFAULT_DATASET_ID)
DEFAULT_CUE_CSV = DEFAULT_DATASET_ROOT / "002_gssi51600s_preprocess_feature_qc/data/field_reflector_cue_candidates.csv"
DEFAULT_SHORT_EVENT_CSV = DEFAULT_DATASET_ROOT / "018_gssi51600s_short_profile_repeatability_policy/data/short_profile_event_table.csv"
DEFAULT_SHORT_PAIR_CSV = DEFAULT_DATASET_ROOT / "021_gssi51600s_short_profile_stack_policy/data/short_profile_reversed_event_pairs.csv"
DEFAULT_SHORT_ANCHOR_CSV = DEFAULT_DATASET_ROOT / "037_gssi51600s_content_time_zero_anchor_policy/data/short_profile_content_time_zero_anchor_rows.csv"
DEFAULT_LONG_HOLDOUT_CSV = DEFAULT_DATASET_ROOT / "058_gssi51600s_long_profile_pattern_holdout_qc/data/long_profile_pattern_holdout_qc_rows.csv"
DEFAULT_TIMING_DISCRIMINANT_CSV = DEFAULT_DATASET_ROOT / "105_gssi51600s_field_timing_discriminant_scorecard/data/field_timing_discriminant_scorecard_rows.csv"
DEFAULT_EVENT_SUPPORT_SUMMARY_JSON = DEFAULT_DATASET_ROOT / "110_gssi51600s_field_event_support_tiers_post_timing_discriminant_hpc/data/field_event_support_tiers_summary.json"
DEFAULT_POLICY_SUMMARY_JSON = DEFAULT_DATASET_ROOT / "112_gssi51600s_field_dataset_policy_synthesis_post_event_support_timing_discriminant_hpc_bundle/data/field_dataset_policy_summary.json"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


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


def safe_int(value, default: int = 0) -> int:
    number = safe_float(value)
    if not math.isfinite(number):
        return default
    return int(number)


def boolish(value) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "supported"}


def profile_group(file_name: str) -> str:
    if "__014" in file_name or "__016" in file_name:
        return "short_014_016"
    if "__013" in file_name or "__015" in file_name:
        return "long_015_013"
    return "unknown"


def cue_key(file_name: str, x_m: float, time_ns: float) -> tuple[str, float, float]:
    return (file_name, round(x_m, 6), round(time_ns, 9))


def find_nearest_cue(cues: list[dict], file_name: str, x_m: float, time_ns: float | None = None) -> tuple[int | None, float, float]:
    best_idx = None
    best_distance = math.inf
    best_time_distance = math.inf
    for idx, cue in enumerate(cues):
        if cue.get("file") != file_name:
            continue
        x_distance = abs(safe_float(cue.get("x_m")) - x_m)
        if time_ns is None:
            time_distance = 0.0
        else:
            time_distance = abs(safe_float(cue.get("time_ns")) - time_ns)
        score = x_distance * 1000.0 + time_distance
        if score < best_distance * 1000.0 + best_time_distance:
            best_idx = idx
            best_distance = x_distance
            best_time_distance = time_distance
    return best_idx, best_distance * 1000.0, best_time_distance


def short_event_lookup(rows: list[dict]) -> dict[tuple[str, int], dict]:
    out = {}
    for row in rows:
        file_name = str(row.get("file", ""))
        group = safe_int(row.get("apex_group"), -1)
        if file_name and group >= 0:
            out[(file_name, group)] = row
    return out


def short_anchor_lookup(rows: list[dict]) -> dict[int, dict]:
    return {
        safe_int(row.get("pair_index"), -1): row
        for row in rows
        if safe_int(row.get("pair_index"), -1) >= 0
    }


def annotate_short_cues(
    cue_rows: list[dict],
    short_event_rows: list[dict],
    short_pair_rows: list[dict],
    short_anchor_rows: list[dict],
) -> tuple[list[dict], list[dict]]:
    annotated = [dict(row) for row in cue_rows]
    for row in annotated:
        row["field_profile_group"] = profile_group(str(row.get("file", "")))
        row["support_category"] = "profile_context_only"
        row["support_label"] = "reflector_cue_context_only"
        row["support_pair_index"] = ""
        row["support_role"] = ""
        row["support_match_residual_x_mm"] = math.nan
        row["support_match_residual_time_ns"] = math.nan
        row["allowed_use"] = "measured-profile cue context"
        row["blocked_use"] = "known-truth rebar, cover-depth, radius, field FWI, or 3D claim"

    events = short_event_lookup(short_event_rows)
    anchors = short_anchor_lookup(short_anchor_rows)
    support_rows = []
    for pair in short_pair_rows:
        pair_index = safe_int(pair.get("pair_index"), -1)
        anchor = anchors.get(pair_index, {})
        content_backed = boolish(anchor.get("content_backed"))
        support_category = "short_content_backed_time_zero_anchor" if content_backed else "short_timing_only_limited_cue"
        support_label = str(anchor.get("anchor_policy_label") or anchor.get("content_label") or support_category)
        allowed_use = (
            "short-pair relative time-zero and visual-QC anchor"
            if content_backed else
            "short-pair timing-only limited relative-timing cue"
        )
        blocked_use = (
            "absolute time-zero, cover-depth, radius, field FWI, or 3D claim"
            if content_backed else
            "content-backed event, geometry/radius, cover-depth, field FWI, or 3D claim"
        )
        pair_event_refs = [
            (
                str(pair.get("reference_file", "")),
                safe_int(pair.get("reference_apex_group"), -1),
                "reference",
            ),
            (
                str(pair.get("comparison_file", "")),
                safe_int(pair.get("comparison_apex_group"), -1),
                "comparison",
            ),
        ]
        matched_files = []
        max_x_residual = 0.0
        max_time_residual = 0.0
        for file_name, apex_group, role in pair_event_refs:
            event = events.get((file_name, apex_group), {})
            idx, residual_x_mm, residual_time_ns = find_nearest_cue(
                annotated,
                file_name,
                safe_float(event.get("x_m")),
                safe_float(event.get("current_cue_time_ns")),
            )
            if idx is None:
                continue
            matched_files.append(file_name)
            max_x_residual = max(max_x_residual, residual_x_mm)
            max_time_residual = max(max_time_residual, residual_time_ns)
            annotated[idx]["support_category"] = support_category
            annotated[idx]["support_label"] = support_label
            annotated[idx]["support_pair_index"] = pair_index
            annotated[idx]["support_role"] = role
            annotated[idx]["support_match_residual_x_mm"] = residual_x_mm
            annotated[idx]["support_match_residual_time_ns"] = residual_time_ns
            annotated[idx]["allowed_use"] = allowed_use
            annotated[idx]["blocked_use"] = blocked_use
        support_rows.append({
            "support_anchor_id": f"short_pair_{pair_index}",
            "profile_group": "short_014_016",
            "support_family": "short_relative_timing",
            "support_category": support_category,
            "source_files": ",".join(sorted(set(matched_files))),
            "anchor_x_mm": safe_float(anchor.get("reference_x_mm"), safe_float(pair.get("reference_x_m")) * 1000.0),
            "comparison_aligned_x_mm": safe_float(anchor.get("comparison_aligned_x_mm"), safe_float(pair.get("comparison_aligned_x_m")) * 1000.0),
            "aligned_x_residual_mm": safe_float(anchor.get("aligned_x_residual_mm"), safe_float(pair.get("aligned_x_residual_mm"))),
            "offset_ns": safe_float(anchor.get("comparison_minus_reference_phase_time_ns"), safe_float(pair.get("comparison_minus_reference_phase_time_ns"))),
            "quality_metric_label": "pair_min_absolute_correlation",
            "quality_metric_value": safe_float(anchor.get("pair_min_absolute_correlation")),
            "support_label": support_label,
            "is_claim_supporting": content_backed,
            "allowed_use": allowed_use,
            "blocked_use": blocked_use,
            "max_cue_match_residual_x_mm": max_x_residual,
            "max_cue_match_residual_time_ns": max_time_residual,
        })
    return annotated, support_rows


def nearest_long_anchor_distance_mm(cue: dict, long_rows: list[dict]) -> float:
    if profile_group(str(cue.get("file", ""))) != "long_015_013":
        return math.nan
    x_mm = safe_float(cue.get("x_m")) * 1000.0
    distances = [abs(x_mm - safe_float(row.get("center_x_mm"))) for row in long_rows]
    return min(distances) if distances else math.nan


def build_long_support_rows(long_rows: list[dict]) -> list[dict]:
    out = []
    for row in long_rows:
        stability = str(row.get("stability_label", ""))
        support_label = "long_stable_pattern_only_anchor" if stability == "stable_stack_anchor" else "long_repeat_limited_pattern_only_anchor"
        out.append({
            "support_anchor_id": f"long_anchor_{safe_int(row.get('anchor_index'))}",
            "profile_group": "long_015_013",
            "support_family": "long_pattern_only",
            "support_category": support_label,
            "source_files": "PROJECT001C__015.DZT,PROJECT001C__013.DZT",
            "anchor_x_mm": safe_float(row.get("center_x_mm")),
            "comparison_aligned_x_mm": math.nan,
            "aligned_x_residual_mm": math.nan,
            "offset_ns": 0.060000000000000275,
            "quality_metric_label": "pattern_shift_abs_correlation_gain",
            "quality_metric_value": safe_float(row.get("pattern_shift_abs_correlation_gain")),
            "support_label": str(row.get("support_label", "supported")),
            "is_claim_supporting": boolish(row.get("is_supported")),
            "allowed_use": "long-profile pattern-only visual QC",
            "blocked_use": "phase time-zero, short-transfer timing, cover-depth, radius, field FWI, or 3D claim",
            "max_cue_match_residual_x_mm": math.nan,
            "max_cue_match_residual_time_ns": math.nan,
        })
    return out


def build_catalogs(
    *,
    cue_rows: list[dict],
    short_event_rows: list[dict],
    short_pair_rows: list[dict],
    short_anchor_rows: list[dict],
    long_holdout_rows: list[dict],
) -> tuple[list[dict], list[dict]]:
    cue_catalog, short_support_rows = annotate_short_cues(
        cue_rows,
        short_event_rows,
        short_pair_rows,
        short_anchor_rows,
    )
    for row in cue_catalog:
        nearest = nearest_long_anchor_distance_mm(row, long_holdout_rows)
        row["nearest_long_pattern_anchor_distance_mm"] = nearest
        if row["field_profile_group"] == "long_015_013":
            row["support_category"] = "long_profile_context_cue_only"
            row["support_label"] = "long raw cue; see pattern-only anchor catalog"
            row["allowed_use"] = "long-profile measured cue context"
            row["blocked_use"] = "phase time-zero, cover-depth, radius, field FWI, or 3D claim"
    support_catalog = short_support_rows + build_long_support_rows(long_holdout_rows)
    return cue_catalog, support_catalog


def summarize_catalogs(
    cue_catalog: list[dict],
    support_catalog: list[dict],
    timing_rows: list[dict],
    event_support_summary: dict,
    policy_summary: dict,
) -> dict:
    category_counts: dict[str, int] = {}
    for row in cue_catalog:
        category = str(row.get("support_category", ""))
        category_counts[category] = category_counts.get(category, 0) + 1
    short_content = sum(
        1 for row in support_catalog
        if row["support_category"] == "short_content_backed_time_zero_anchor"
    )
    short_timing = sum(
        1 for row in support_catalog
        if row["support_category"] == "short_timing_only_limited_cue"
    )
    long_stable = sum(
        1 for row in support_catalog
        if row["support_category"] == "long_stable_pattern_only_anchor"
    )
    long_repeat = sum(
        1 for row in support_catalog
        if row["support_category"] == "long_repeat_limited_pattern_only_anchor"
    )
    return {
        "policy_label": "gssi51600s_field_cue_support_catalog_2d_qc_not_inversion",
        "raw_cue_count": len(cue_catalog),
        "raw_profile_count": len({row.get("file") for row in cue_catalog}),
        "support_anchor_count": len(support_catalog),
        "short_content_backed_anchor_count": short_content,
        "short_timing_only_cue_count": short_timing,
        "long_stable_pattern_anchor_count": long_stable,
        "long_repeat_limited_pattern_anchor_count": long_repeat,
        "timing_discriminant_row_count": len(timing_rows),
        "event_support_tier_row_count": safe_int(event_support_summary.get("tier_row_count")),
        "short_content_anchor_support_fraction": safe_float(event_support_summary.get("short_content_anchor_support_fraction")),
        "long_pattern_total_supported_anchor_count": safe_float(event_support_summary.get("long_pattern_total_supported_anchor_count")),
        "field_geometry_type": str(event_support_summary.get("hpc_dimensionality_field_geometry_type", "independent_2d_line_profiles")),
        "ready_for_2d_qc": bool(policy_summary.get("publication_claim_bundle_ready", False)),
        "ready_for_absolute_time_zero": False,
        "ready_for_cover_depth_recovery": False,
        "ready_for_radius_recovery": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
        "cue_category_counts": category_counts,
        "decision": (
            "Use this catalog as measured-field cue/support traceability for manuscript tables "
            "and supplement QA. Raw reflector cues remain context only unless linked to short "
            "content-backed anchors or long pattern-only support anchors. The catalog does not "
            "create known-truth rebar labels, absolute time-zero, cover-depth, radius, field FWI, "
            "3D, or HPC readiness."
        ),
    }


def category_color(category: str) -> str:
    return {
        "short_content_backed_time_zero_anchor": "#2f9d55",
        "short_timing_only_limited_cue": "#d98c20",
        "profile_context_only": "#6b6b6b",
        "long_profile_context_cue_only": "#4c78a8",
        "long_stable_pattern_only_anchor": "#9467bd",
        "long_repeat_limited_pattern_only_anchor": "#b279a2",
    }.get(category, "#6b6b6b")


def plot_catalog(cue_catalog: list[dict], support_catalog: list[dict], summary: dict, save_path: Path) -> str:
    files = sorted({str(row.get("file", "")) for row in cue_catalog})
    file_y = {file_name: idx for idx, file_name in enumerate(files)}
    categories = list(dict.fromkeys(row["support_category"] for row in cue_catalog))
    support_categories = list(dict.fromkeys(row["support_category"] for row in support_catalog))

    fig, axes = plt.subplots(1, 2, figsize=(15.8, 5.8), constrained_layout=True)
    for category in categories:
        rows = [row for row in cue_catalog if row["support_category"] == category]
        axes[0].scatter(
            [safe_float(row.get("x_m")) for row in rows],
            [safe_float(row.get("time_ns")) for row in rows],
            s=48,
            color=category_color(category),
            edgecolor="#222222",
            linewidth=0.3,
            label=category.replace("_", " "),
        )
    axes[0].set_xlabel("profile position x (m)")
    axes[0].set_ylabel("cue time (ns)")
    axes[0].set_title("Raw measured reflector cues")
    axes[0].grid(color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8, loc="best")
    for file_name in files:
        rows = [row for row in cue_catalog if row.get("file") == file_name]
        if not rows:
            continue
        median_x = float(np.median([safe_float(row.get("x_m")) for row in rows]))
        median_t = float(np.median([safe_float(row.get("time_ns")) for row in rows]))
        axes[0].text(median_x, median_t, file_name.replace("PROJECT001C__", "").replace(".DZT", ""), fontsize=8)

    counts = [sum(1 for row in support_catalog if row["support_category"] == category) for category in support_categories]
    x = np.arange(len(support_categories))
    axes[1].bar(x, counts, color=[category_color(category) for category in support_categories], width=0.62)
    axes[1].set_xticks(x, [category.replace("_", "\n") for category in support_categories], fontsize=8)
    axes[1].set_ylabel("support-anchor rows")
    axes[1].set_title("Derived support anchors")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(
        handles=[
            Patch(color=category_color(category), label=category.replace("_", " "))
            for category in support_categories
        ],
        loc="upper right",
        frameon=False,
        fontsize=8,
    )
    axes[1].text(
        0.02,
        0.96,
        (
            f"raw cues: {summary['raw_cue_count']}\n"
            f"support anchors: {summary['support_anchor_count']}\n"
            "field FWI: no"
        ),
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )

    fig.suptitle("GSSI 51600S field cue/support catalog", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, cue_csv: Path, support_csv: Path, summary_json: Path, validation_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_cue_support_catalog.png`",
                "",
                "This CPU-only catalog separates raw measured reflector cues from",
                "derived short-pair timing anchors and long-profile pattern-only anchors.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Raw cue count: `{summary['raw_cue_count']}`.",
                f"Support-anchor count: `{summary['support_anchor_count']}`.",
                f"Short content-backed anchors: `{summary['short_content_backed_anchor_count']}`.",
                f"Short timing-only cues: `{summary['short_timing_only_cue_count']}`.",
                f"Long pattern anchors: `{summary['long_pattern_total_supported_anchor_count']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Cue catalog: `{cue_csv.name}`.",
                f"- Support-anchor catalog: `{support_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                f"- Figure validation: `{validation_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "The catalog reads existing measured-field outputs only. It does not run",
                "FDTD, FWI, GPU, 3D/HPC, neural-network training, or field inversion,",
                "and it does not create known-truth field rebar labels.",
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
    parser.add_argument("--cue-csv", default=str(DEFAULT_CUE_CSV))
    parser.add_argument("--short-event-csv", default=str(DEFAULT_SHORT_EVENT_CSV))
    parser.add_argument("--short-pair-csv", default=str(DEFAULT_SHORT_PAIR_CSV))
    parser.add_argument("--short-anchor-csv", default=str(DEFAULT_SHORT_ANCHOR_CSV))
    parser.add_argument("--long-holdout-csv", default=str(DEFAULT_LONG_HOLDOUT_CSV))
    parser.add_argument("--timing-discriminant-csv", default=str(DEFAULT_TIMING_DISCRIMINANT_CSV))
    parser.add_argument("--event-support-summary-json", default=str(DEFAULT_EVENT_SUPPORT_SUMMARY_JSON))
    parser.add_argument("--policy-summary-json", default=str(DEFAULT_POLICY_SUMMARY_JSON))
    parser.add_argument("--run-name", default="gssi51600s_field_cue_support_catalog")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)

    cue_rows = read_csv_rows(Path(args.cue_csv))
    short_event_rows = read_csv_rows(Path(args.short_event_csv))
    short_pair_rows = read_csv_rows(Path(args.short_pair_csv))
    short_anchor_rows = read_csv_rows(Path(args.short_anchor_csv))
    long_holdout_rows = read_csv_rows(Path(args.long_holdout_csv))
    timing_rows = read_csv_rows(Path(args.timing_discriminant_csv))
    event_support_summary = read_json(Path(args.event_support_summary_json))
    policy_summary = read_json(Path(args.policy_summary_json))

    cue_catalog, support_catalog = build_catalogs(
        cue_rows=cue_rows,
        short_event_rows=short_event_rows,
        short_pair_rows=short_pair_rows,
        short_anchor_rows=short_anchor_rows,
        long_holdout_rows=long_holdout_rows,
    )
    summary = summarize_catalogs(
        cue_catalog,
        support_catalog,
        timing_rows,
        event_support_summary,
        policy_summary,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=dataset_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    cue_csv = data_dir / "field_cue_support_catalog.csv"
    support_csv = data_dir / "field_support_anchor_catalog.csv"
    summary_json = data_dir / "field_cue_support_catalog_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_cue_support_catalog.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(cue_csv, [json_safe(row) for row in cue_catalog])
    write_csv(support_csv, [json_safe(row) for row in support_catalog])
    plot_catalog(cue_catalog, support_catalog, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "cue_catalog_csv": str(cue_csv),
        "support_anchor_catalog_csv": str(support_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, cue_csv, support_csv, summary_json, validation_csv)
    write_run_manifest(
        str(outdir),
        "gssi51600s_field_cue_support_catalog",
        {
            "cue_csv": args.cue_csv,
            "short_event_csv": args.short_event_csv,
            "short_pair_csv": args.short_pair_csv,
            "short_anchor_csv": args.short_anchor_csv,
            "long_holdout_csv": args.long_holdout_csv,
            "timing_discriminant_csv": args.timing_discriminant_csv,
            "event_support_summary_json": args.event_support_summary_json,
            "policy_summary_json": args.policy_summary_json,
            "readgssi_version": readgssi_version(),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

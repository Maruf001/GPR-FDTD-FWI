#!/usr/bin/env python3
"""Audit the morphology of top false geometries from the refreshed detector selector."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter, defaultdict
from itertools import permutations
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
from run_local_2d_detector_rank_budget_diagnostic import boolish, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_COMPONENT_GATE_RUN = "035_local_2d_detector_component_waveform_gate_post_rank_budget"
DEFAULT_REFRESHED_GAP_RUN = "108_local_2d_detector_refreshed_selector_gap_audit_post_feature_family"
TARGETS = ("target0", "target1", "target2")


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def parse_float_list(value: object) -> list[float]:
    out = []
    for part in str(value if value is not None else "").split(","):
        part = part.strip()
        if not part:
            continue
        try:
            number = float(part)
        except ValueError:
            continue
        if math.isfinite(number):
            out.append(number)
    return out


def sorted_x_values(value: object) -> list[float]:
    return sorted(parse_float_list(value))


def case_label(row: dict) -> str:
    return str(row.get("case_label") or f"{row['branch_key']}|seed{row['seed']}|{row['case_variant']}")


def representative_truth_x_by_case(component_rows: list[dict]) -> dict[str, list[float]]:
    grouped: dict[str, list[list[float]]] = defaultdict(list)
    for row in component_rows:
        if not boolish(row.get("unique_all_truths_within_tolerance")):
            continue
        xs = sorted_x_values(row.get("candidate_x_values_mm"))
        if len(xs) == 3:
            grouped[case_label(row)].append(xs)
    representatives = {}
    for label, values in grouped.items():
        arr = np.asarray(values, dtype=np.float64)
        representatives[label] = [float(value) for value in np.median(arr, axis=0)]
    return representatives


def missing_target_list(value: object) -> list[str]:
    text = str(value if value is not None else "").strip()
    if not text or text == "none":
        return []
    return [part.strip() for part in text.split(",") if part.strip()]


def hit_targets_from_missing(missing: list[str]) -> list[str]:
    missing_set = set(missing)
    return [target for target in TARGETS if target not in missing_set]


def false_geometry_mode(missing: list[str]) -> str:
    hits = hit_targets_from_missing(missing)
    if not missing:
        return "all_truth_or_duplicate"
    if len(missing) == 3:
        return "all_targets_missed"
    if len(missing) == 2:
        return f"single_truth_only_{hits[0]}" if hits else "single_truth_only_unknown"
    return f"two_truth_partial_missing_{missing[0]}"


def assignment_errors(selected_xs: list[float], truth_xs: list[float]) -> list[float]:
    if len(selected_xs) != len(truth_xs) or not selected_xs:
        return []
    best_errors = None
    best_sum = math.inf
    for perm in permutations(selected_xs):
        errors = [abs(float(sel) - float(truth)) for sel, truth in zip(perm, truth_xs)]
        total = sum(errors)
        if total < best_sum:
            best_sum = total
            best_errors = errors
    return [float(value) for value in best_errors or []]


def span(values: list[float]) -> float:
    return float(max(values) - min(values)) if values else math.nan


def center(values: list[float]) -> float:
    return float(np.mean(values)) if values else math.nan


def build_morphology_rows(gap_rows: list[dict], component_rows: list[dict]) -> list[dict]:
    truth_by_case = representative_truth_x_by_case(component_rows)
    out = []
    for row in gap_rows:
        label = str(row["case_label"])
        selected_xs = sorted_x_values(row.get("selected_top_candidate_x_values_mm"))
        truth_xs = truth_by_case.get(label, [])
        errors = assignment_errors(selected_xs, truth_xs)
        selected_span = span(selected_xs)
        truth_span = span(truth_xs)
        span_ratio = selected_span / truth_span if math.isfinite(selected_span) and truth_span > 0 else math.nan
        selected_center = center(selected_xs)
        truth_center = center(truth_xs)
        missing = missing_target_list(row.get("selected_top_missing_targets"))
        out.append(
            {
                "case_label": label,
                "branch_key": row["branch_key"],
                "seed": safe_int(row["seed"]),
                "case_variant": row["case_variant"],
                "run_name": row["run_name"],
                "selected_first_all_truth_rank": safe_float(row.get("selected_first_all_truth_rank"), math.inf),
                "selected_rank_gate_label": row.get("selected_rank_gate_label", ""),
                "selected_best_false_minus_truth_score_gap": safe_float(
                    row.get("selected_best_false_minus_truth_score_gap"),
                    math.nan,
                ),
                "selected_positive_false_truth_gap": boolish(row.get("selected_positive_false_truth_gap")),
                "selected_top_unique_truth_hit_count": safe_int(row.get("selected_top_unique_truth_hit_count")),
                "selected_top_missing_targets": ",".join(missing) if missing else "none",
                "false_geometry_mode": false_geometry_mode(missing),
                "selected_top_candidate_x_values_mm": ",".join(f"{value:.6g}" for value in selected_xs),
                "representative_truth_x_values_mm": ",".join(f"{value:.6g}" for value in truth_xs),
                "selected_top_x_span_mm": selected_span,
                "representative_truth_x_span_mm": truth_span,
                "selected_to_truth_x_span_ratio": span_ratio,
                "selected_x_center_mm": selected_center,
                "truth_x_center_mm": truth_center,
                "selected_minus_truth_center_mm": (
                    selected_center - truth_center
                    if math.isfinite(selected_center) and math.isfinite(truth_center)
                    else math.nan
                ),
                "selected_left_edge_minus_truth_left_edge_mm": (
                    selected_xs[0] - truth_xs[0] if selected_xs and truth_xs else math.nan
                ),
                "selected_right_edge_minus_truth_right_edge_mm": (
                    selected_xs[-1] - truth_xs[-1] if selected_xs and truth_xs else math.nan
                ),
                "assignment_abs_errors_mm": ",".join(f"{value:.6g}" for value in errors),
                "max_assignment_abs_error_mm": max(errors) if errors else math.nan,
                "mean_assignment_abs_error_mm": float(np.mean(errors)) if errors else math.nan,
                "compressed_span_under_75pct_truth": span_ratio < 0.75 if math.isfinite(span_ratio) else False,
                "truth_reference_available": len(truth_xs) == 3,
            }
        )
    return out


def summarize_by_branch(rows: list[dict]) -> list[dict]:
    out = []
    for branch in sorted({row["branch_key"] for row in rows}):
        branch_rows = [row for row in rows if row["branch_key"] == branch]
        ratios = [
            safe_float(row["selected_to_truth_x_span_ratio"])
            for row in branch_rows
            if math.isfinite(safe_float(row["selected_to_truth_x_span_ratio"]))
        ]
        errors = [
            safe_float(row["max_assignment_abs_error_mm"])
            for row in branch_rows
            if math.isfinite(safe_float(row["max_assignment_abs_error_mm"]))
        ]
        modes = Counter(row["false_geometry_mode"] for row in branch_rows)
        missing = Counter(row["selected_top_missing_targets"] for row in branch_rows)
        out.append(
            {
                "branch_key": branch,
                "case_count": len(branch_rows),
                "top50_case_count": sum(safe_float(row["selected_first_all_truth_rank"], math.inf) <= 50 for row in branch_rows),
                "top200_case_count": sum(safe_float(row["selected_first_all_truth_rank"], math.inf) <= 200 for row in branch_rows),
                "positive_false_truth_gap_count": sum(boolish(row["selected_positive_false_truth_gap"]) for row in branch_rows),
                "compressed_span_case_count": sum(boolish(row["compressed_span_under_75pct_truth"]) for row in branch_rows),
                "median_selected_to_truth_x_span_ratio": float(np.median(ratios)) if ratios else math.nan,
                "min_selected_to_truth_x_span_ratio": min(ratios) if ratios else math.nan,
                "median_max_assignment_abs_error_mm": float(np.median(errors)) if errors else math.nan,
                "max_assignment_abs_error_mm": max(errors) if errors else math.nan,
                "dominant_false_geometry_mode": modes.most_common(1)[0][0] if modes else "",
                "dominant_missing_targets": missing.most_common(1)[0][0] if missing else "",
            }
        )
    return out


def summarize_audit(rows: list[dict], branch_rows: list[dict], gap_summary: dict) -> dict:
    ratios = [
        safe_float(row["selected_to_truth_x_span_ratio"])
        for row in rows
        if math.isfinite(safe_float(row["selected_to_truth_x_span_ratio"]))
    ]
    errors = [
        safe_float(row["max_assignment_abs_error_mm"])
        for row in rows
        if math.isfinite(safe_float(row["max_assignment_abs_error_mm"]))
    ]
    modes = Counter(row["false_geometry_mode"] for row in rows)
    missing = Counter(row["selected_top_missing_targets"] for row in rows)
    compressed = sum(boolish(row["compressed_span_under_75pct_truth"]) for row in rows)
    return {
        "policy_label": "local_2d_detector_false_geometry_morphology_audit_cpu_no_fwi",
        "source_gap_policy_label": gap_summary.get("policy_label", ""),
        "case_count": len(rows),
        "branch_row_count": len(branch_rows),
        "truth_reference_available_case_count": sum(boolish(row["truth_reference_available"]) for row in rows),
        "top1_all_truth_case_count": sum(safe_float(row["selected_first_all_truth_rank"], math.inf) <= 1 for row in rows),
        "top50_all_truth_case_count": sum(safe_float(row["selected_first_all_truth_rank"], math.inf) <= 50 for row in rows),
        "top200_all_truth_case_count": sum(safe_float(row["selected_first_all_truth_rank"], math.inf) <= 200 for row in rows),
        "positive_false_truth_gap_case_count": sum(boolish(row["selected_positive_false_truth_gap"]) for row in rows),
        "compressed_span_case_count": compressed,
        "compressed_span_case_fraction": compressed / len(rows) if rows else math.nan,
        "median_selected_to_truth_x_span_ratio": float(np.median(ratios)) if ratios else math.nan,
        "min_selected_to_truth_x_span_ratio": min(ratios) if ratios else math.nan,
        "max_selected_to_truth_x_span_ratio": max(ratios) if ratios else math.nan,
        "median_max_assignment_abs_error_mm": float(np.median(errors)) if errors else math.nan,
        "max_assignment_abs_error_mm": max(errors) if errors else math.nan,
        "dominant_false_geometry_mode": modes.most_common(1)[0][0] if modes else "",
        "dominant_missing_targets": missing.most_common(1)[0][0] if missing else "",
        "all_top_false_rows_have_positive_gap": (
            sum(boolish(row["selected_positive_false_truth_gap"]) for row in rows) == len(rows)
            if rows else False
        ),
        "ready_for_false_geometry_morphology_claim": len(rows) > 0 and compressed > 0,
        "ready_for_rank_gated_selector_claim": safe_int(gap_summary.get("selected_top200_case_count")) == len(rows),
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
        "decision": (
            "The refreshed detector selector's top rows are not random misses: they are structured "
            "false geometries, often compressed or partial target subsets, while all-truth triples "
            "remain rank-gated but not top-ranked. This supports a detector ambiguity/morphology "
            "claim and still blocks detector-seeded FWI."
        ),
    }


def plot_audit(summary: dict, rows: list[dict], branch_rows: list[dict], save_path: Path) -> str:
    ordered = sorted(rows, key=lambda row: safe_float(row["selected_to_truth_x_span_ratio"], math.inf))
    labels = [row["case_label"].replace("target2_", "").replace("|", "\n") for row in ordered]
    ratios = [safe_float(row["selected_to_truth_x_span_ratio"], math.nan) for row in ordered]
    colors = ["#e15759" if boolish(row["compressed_span_under_75pct_truth"]) else "#4e79a7" for row in ordered]

    modes = Counter(row["false_geometry_mode"] for row in rows)
    mode_labels = list(modes.keys())
    mode_counts = [modes[label] for label in mode_labels]

    fig, axes = plt.subplots(1, 2, figsize=(16.0, 5.8), constrained_layout=True)
    x = np.arange(len(ordered))
    axes[0].bar(x, ratios, color=colors)
    axes[0].axhline(1.0, color="#555555", linestyle="--", linewidth=0.8)
    axes[0].axhline(0.75, color="#a33b3b", linestyle="--", linewidth=0.8)
    axes[0].set_xticks(x, labels, rotation=45, ha="right", fontsize=7)
    axes[0].set_ylabel("selected top x-span / representative truth x-span")
    axes[0].set_title("Top false x-span morphology")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].barh(
        np.arange(len(mode_labels)),
        mode_counts,
        color=["#59a14f", "#f28e2b", "#e15759", "#76b7b2", "#b07aa1"][: len(mode_labels)],
    )
    axes[1].set_yticks(np.arange(len(mode_labels)), [label.replace("_", "\n") for label in mode_labels], fontsize=8)
    axes[1].invert_yaxis()
    axes[1].set_xlabel("case count")
    axes[1].set_title("Top false geometry modes")
    axes[1].grid(axis="x", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.98,
        0.04,
        f"compressed={summary['compressed_span_case_count']}/{summary['case_count']}\n"
        f"top200 truth={summary['top200_all_truth_case_count']}/{summary['case_count']}\n"
        f"dominant miss={summary['dominant_missing_targets']}\n"
        f"FWI={summary['ready_for_detector_seeded_fwi']}",
        transform=axes[1].transAxes,
        va="bottom",
        ha="right",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local 2D detector false-geometry morphology audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_false_geometry_morphology_audit.png`",
                "",
                "This CPU-only audit compares the refreshed detector selector's top false",
                "x-geometries with representative all-truth candidate triples from the saved",
                "component-gate rows.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Cases: `{summary['case_count']}`.",
                f"Top-200 all-truth cases: `{summary['top200_all_truth_case_count']}`.",
                f"Compressed-span cases: `{summary['compressed_span_case_count']}`.",
                f"Median selected/truth x-span ratio: `{summary['median_selected_to_truth_x_span_ratio']}`.",
                f"Dominant false geometry mode: `{summary['dominant_false_geometry_mode']}`.",
                f"Ready for detector-seeded FWI: `{summary['ready_for_detector_seeded_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                summary["decision"],
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--component-gate-run", default=DEFAULT_COMPONENT_GATE_RUN)
    parser.add_argument("--refreshed-gap-run", default=DEFAULT_REFRESHED_GAP_RUN)
    parser.add_argument("--run-name", default="local_2d_detector_false_geometry_morphology_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    component_dir = summary_root / args.component_gate_run / "data"
    gap_dir = summary_root / args.refreshed_gap_run / "data"
    component_rows = read_csv_rows(component_dir / "local_2d_detector_component_waveform_gate_rows.csv")
    gap_rows = read_csv_rows(gap_dir / "local_2d_detector_refreshed_selector_gap_cases.csv")
    gap_summary = read_json(gap_dir / "local_2d_detector_refreshed_selector_gap_summary.json")

    morphology_rows = build_morphology_rows(gap_rows, component_rows)
    branch_rows = summarize_by_branch(morphology_rows)
    summary = summarize_audit(morphology_rows, branch_rows, gap_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    case_csv = data_dir / "local_2d_detector_false_geometry_morphology_cases.csv"
    branch_csv = data_dir / "local_2d_detector_false_geometry_morphology_branch_summary.csv"
    summary_json = data_dir / "local_2d_detector_false_geometry_morphology_summary.json"
    figure_path = figures_dir / "local_2d_detector_false_geometry_morphology_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"
    validation_csv = data_dir / "figure_validation.csv"

    write_csv(case_csv, [json_safe(row) for row in morphology_rows])
    write_csv(branch_csv, [json_safe(row) for row in branch_rows])
    plot_audit(summary, morphology_rows, branch_rows, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "source_component_gate_rows_csv": str(component_dir / "local_2d_detector_component_waveform_gate_rows.csv"),
        "source_refreshed_gap_cases_csv": str(gap_dir / "local_2d_detector_refreshed_selector_gap_cases.csv"),
        "source_refreshed_gap_summary_json": str(gap_dir / "local_2d_detector_refreshed_selector_gap_summary.json"),
        "case_csv": str(case_csv),
        "branch_summary_csv": str(branch_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_false_geometry_morphology_audit",
        {
            "summary_json": str(summary_json),
            "case_csv": str(case_csv),
            "branch_summary_csv": str(branch_csv),
            "figure": str(figure_path),
            "summary": json_safe(summary),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

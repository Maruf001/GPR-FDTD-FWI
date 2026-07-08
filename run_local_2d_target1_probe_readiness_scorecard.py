#!/usr/bin/env python3
"""Build a CPU-only target1 probe-readiness scorecard from saved 2D outputs."""

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
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_WEAK_SUBSET_CSV = (
    "outputs/experiments/1261_target1_weak_exact_objective_audit_700_1259/"
    "data/target1_weak_exact_subset_policy.csv"
)
DEFAULT_ACQUISITION_SUMMARY_JSON = (
    "outputs/experiments/1312_target1_acquisition_confidence_surface/"
    "data/target1_acquisition_confidence_surface_summary.json"
)
DEFAULT_ACQUISITION_SURFACE_CSV = (
    "outputs/experiments/1312_target1_acquisition_confidence_surface/"
    "data/target1_acquisition_confidence_surface.csv"
)
DEFAULT_SOURCE_BRANCH_CSV = (
    "outputs/experiments/1312_target1_acquisition_confidence_surface/"
    "data/target1_source_density_branch_policy.csv"
)
DEFAULT_EXCEPTION_SUMMARY_JSON = (
    "outputs/experiments/1314_target1_source_density_exception_map/"
    "data/target1_source_density_exception_map_summary.json"
)
DEFAULT_EXCEPTION_BRANCH_CSV = (
    "outputs/experiments/1314_target1_source_density_exception_map/"
    "data/target1_source_density_exception_branches.csv"
)
DEFAULT_NEXT_MATRIX_SUMMARY_JSON = (
    "outputs/experiments/1323_synthetic_2d_next_question_matrix_post_claim_boundary_reconciliation/"
    "data/synthetic_2d_next_question_matrix_summary.json"
)


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


def fraction(numerator: float, denominator: float) -> float:
    denominator = safe_float(denominator, 0.0)
    if denominator <= 0.0:
        return math.nan
    return safe_float(numerator, 0.0) / denominator


def find_surface_row(surface_rows: list[dict], group_type: str, setting: float) -> dict:
    for row in surface_rows:
        if str(row.get("group_type", "")) != group_type:
            continue
        if math.isclose(safe_float(row.get("setting")), setting):
            return row
    return {}


def _gate_status(triggered: bool, no_probe_status: str = "closed_no_probe") -> str:
    return "narrow_probe_candidate" if triggered else no_probe_status


def _gpu_action(triggered: bool) -> str:
    return "define_narrow_probe_contract_before_gpu" if triggered else "none"


def scorecard_row(
    *,
    gate_key: str,
    evidence_source: str,
    current_value: float,
    trigger_threshold: str,
    triggered: bool,
    status: str,
    manuscript_use: str,
    next_action: str,
    gpu_action: str | None = None,
    evidence_count: float = 0.0,
) -> dict:
    return {
        "gate_key": gate_key,
        "evidence_source": evidence_source,
        "current_value": safe_float(current_value, 0.0),
        "evidence_count": safe_float(evidence_count, 0.0),
        "trigger_threshold": trigger_threshold,
        "triggered": bool(triggered),
        "status": status,
        "gpu_action": gpu_action if gpu_action is not None else _gpu_action(triggered),
        "manuscript_use": manuscript_use,
        "next_action": next_action,
    }


def build_probe_rows(
    *,
    acquisition_summary: dict,
    exception_summary: dict,
    next_matrix_summary: dict,
    weak_subset_rows: list[dict],
    surface_rows: list[dict],
    source_branch_rows: list[dict],
    exception_branch_rows: list[dict],
) -> list[dict]:
    target_rows = safe_float(acquisition_summary.get("target1_canonical_row_count"), 0.0)
    exact_rows = safe_float(acquisition_summary.get("target1_exact_geometry_count"), 0.0)
    weak_exact_rows = safe_float(acquisition_summary.get("target1_base_weak_exact_count"), 0.0)
    late_high_accepted = safe_float(acquisition_summary.get("target1_late_high_accepted_count"), 0.0)
    modern_exceptions = safe_float(exception_summary.get("modern_exception_series_count"), 0.0)
    terminal_11 = safe_float(exception_summary.get("terminal_11_series_count"), 0.0)
    terminal_11_worse = safe_float(exception_summary.get("terminal_11_worse_count"), 0.0)
    escalation_helped = safe_float(acquisition_summary.get("source_density_escalation_helped_count"), 0.0)
    lower_best = safe_float(acquisition_summary.get("source_density_lower_count_best_count"), 0.0)
    all_weak_series = safe_float(exception_summary.get("all_base_weak_series_count"), 0.0)
    immediate_gpu = safe_float(next_matrix_summary.get("immediate_gpu_priority_count"), 0.0)
    conditional_gpu = safe_float(next_matrix_summary.get("conditional_gpu_candidate_count"), 0.0)

    txrx60 = find_surface_row(surface_rows, "txrx_offset", 60.0)
    source5 = find_surface_row(surface_rows, "source_count", 5.0)
    ringdown050_subset = next(
        (row for row in weak_subset_rows if row.get("subset") == "ringdown050"),
        {},
    )
    ringdown050_lh = safe_float(ringdown050_subset.get("late_high_accepted_count"), 0.0)
    ringdown050_weak = safe_float(ringdown050_subset.get("weak_exact_row_count"), 0.0)

    geometry_trigger = exact_rows < target_rows
    modern_secondary_trigger = modern_exceptions > 0
    source_monotonic_trigger = terminal_11 > 0 and terminal_11_worse < terminal_11
    txrx_trigger = (
        safe_float(txrx60.get("late_high_accepted_count"), 0.0)
        < safe_float(txrx60.get("row_count"), 0.0)
        and modern_exceptions > 0
    )
    next_matrix_trigger = immediate_gpu > 0 or conditional_gpu > 0

    return [
        scorecard_row(
            gate_key="geometry_stability",
            evidence_source="1312 acquisition surface",
            current_value=fraction(exact_rows, target_rows),
            evidence_count=target_rows,
            trigger_threshold="trigger if any canonical target1 row loses exact x/z/r",
            triggered=geometry_trigger,
            status=_gate_status(geometry_trigger),
            manuscript_use="Target1 is a confidence-policy example, not a localization failure.",
            next_action="Keep target1 in the manuscript as exact geometry with conservative base margins.",
        ),
        scorecard_row(
            gate_key="base_margin_weak_exact",
            evidence_source="1261 weak-exact audit + 1312 surface",
            current_value=fraction(weak_exact_rows, target_rows),
            evidence_count=weak_exact_rows,
            trigger_threshold="weak base rows alone do not trigger GPU if exact and secondary-confirmed",
            triggered=False,
            status="manuscript_confidence_policy",
            gpu_action="none",
            manuscript_use="Use the weak-exact count to separate point recovery from confidence margin.",
            next_action="Do not rerun solely to inflate the canonical base-margin label.",
        ),
        scorecard_row(
            gate_key="ringdown050_secondary_confirmation",
            evidence_source="1261 weak-exact subset policy",
            current_value=fraction(ringdown050_lh, ringdown050_weak),
            evidence_count=ringdown050_weak,
            trigger_threshold="trigger only if modern ringdown050 late_high confirmation fails",
            triggered=ringdown050_lh < ringdown050_weak,
            status=_gate_status(ringdown050_lh < ringdown050_weak),
            manuscript_use="Late_high is a secondary confirmation objective for modern weak-exact target1 rows.",
            next_action="Keep late_high as diagnostic evidence, not as a replacement production gate.",
        ),
        scorecard_row(
            gate_key="modern_secondary_exception",
            evidence_source="1314 source-density exception map",
            current_value=modern_exceptions,
            evidence_count=safe_float(exception_summary.get("source_density_series_count"), 0.0),
            trigger_threshold="trigger if modern source-density exception count is > 0",
            triggered=modern_secondary_trigger,
            status=_gate_status(modern_secondary_trigger),
            manuscript_use="Current modern branches have no secondary-confirmation exception.",
            next_action="No target1 GPU rerun unless a modern exception appears under a new hypothesis.",
        ),
        scorecard_row(
            gate_key="source_density_monotonic_rescue",
            evidence_source="1312 branch policy + 1314 exception map",
            current_value=escalation_helped - lower_best,
            evidence_count=len(source_branch_rows),
            trigger_threshold="trigger only if terminal/high-source branches improve consistently",
            triggered=source_monotonic_trigger,
            status=_gate_status(source_monotonic_trigger, "do_not_extend_source_density"),
            manuscript_use="Source density is nonmonotonic; 11-source endpoints are not a rescue rule.",
            next_action="Do not continue target1 source-count escalation under the current setup.",
        ),
        scorecard_row(
            gate_key="all_base_weak_branches",
            evidence_source="1314 exception branch map",
            current_value=all_weak_series,
            evidence_count=len(exception_branch_rows),
            trigger_threshold="all-base-weak branches trigger GPU only with modern secondary failure",
            triggered=all_weak_series > 0 and modern_exceptions > 0,
            status="secondary_confirmed_no_gpu",
            gpu_action="none",
            manuscript_use="All-base-weak branches are useful negative confidence-policy evidence.",
            next_action="Report them as exact-but-weak branches; do not rerun without new physics/objective.",
        ),
        scorecard_row(
            gate_key="txrx60_boundary",
            evidence_source="1312 acquisition surface",
            current_value=safe_float(txrx60.get("accepted_fraction"), 0.0),
            evidence_count=safe_float(txrx60.get("row_count"), 0.0),
            trigger_threshold="trigger if Tx/Rx boundary contains a modern secondary exception",
            triggered=txrx_trigger,
            status=_gate_status(txrx_trigger, "closed_no_probe"),
            manuscript_use="60 mm has the strongest current target1 Tx/Rx support but is still a confidence-policy surface.",
            next_action="Do not run a target1 Tx/Rx probe unless a new offset hypothesis is defined.",
        ),
        scorecard_row(
            gate_key="source5_reference",
            evidence_source="1312 acquisition surface",
            current_value=safe_float(source5.get("accepted_fraction"), 0.0),
            evidence_count=safe_float(source5.get("row_count"), 0.0),
            trigger_threshold="5-source reference is retained unless geometry failures appear",
            triggered=False,
            status="reference_setting",
            gpu_action="none",
            manuscript_use="Five sources are the best-supported reference setting in the saved target1 archive.",
            next_action="Use as the reference row in target1 acquisition-policy tables.",
        ),
        scorecard_row(
            gate_key="global_next_question_matrix",
            evidence_source="1323 synthetic next-question matrix",
            current_value=immediate_gpu + conditional_gpu,
            evidence_count=safe_float(next_matrix_summary.get("candidate_count"), 0.0),
            trigger_threshold="trigger if immediate or conditional GPU candidate count is > 0",
            triggered=next_matrix_trigger,
            status=_gate_status(next_matrix_trigger),
            manuscript_use="The current synthetic queue has no target1 GPU follow-up.",
            next_action="Move local effort to field QC or a new CPU-first baseline question.",
        ),
        scorecard_row(
            gate_key="legacy_ringdown025_exception",
            evidence_source="1261 weak-exact audit + 1314 exception map",
            current_value=safe_float(exception_summary.get("legacy_exception_series_count"), 0.0),
            evidence_count=safe_float(exception_summary.get("source_density_series_count"), 0.0),
            trigger_threshold="legacy ringdown025 caveat is not a modern target1 GPU trigger",
            triggered=False,
            status="archive_caveat_no_gpu",
            gpu_action="none",
            manuscript_use="Mention run 785 as a legacy caveat if discussing full-archive secondary objectives.",
            next_action="Keep the caveat out of modern target1 probe planning.",
        ),
    ]


def summarize_probe_rows(rows: list[dict], acquisition_summary: dict, exception_summary: dict) -> dict:
    triggered_rows = [row for row in rows if row["triggered"]]
    gpu_actions = [
        row for row in rows
        if str(row.get("gpu_action", "")).lower() not in {"none", ""}
    ]
    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1

    ready_for_probe = bool(gpu_actions)
    return {
        "policy_label": (
            "local_2d_target1_probe_readiness_requires_new_hypothesis"
            if not ready_for_probe
            else "local_2d_target1_probe_readiness_review_required"
        ),
        "scorecard_row_count": len(rows),
        "triggered_gate_count": len(triggered_rows),
        "gpu_action_count": len(gpu_actions),
        "ready_for_target1_gpu_probe": ready_for_probe,
        "target1_canonical_row_count": safe_int(acquisition_summary.get("target1_canonical_row_count")),
        "target1_exact_geometry_count": safe_int(acquisition_summary.get("target1_exact_geometry_count")),
        "target1_base_weak_exact_count": safe_int(acquisition_summary.get("target1_base_weak_exact_count")),
        "target1_late_high_accepted_count": safe_int(acquisition_summary.get("target1_late_high_accepted_count")),
        "modern_exception_series_count": safe_int(exception_summary.get("modern_exception_series_count")),
        "legacy_exception_series_count": safe_int(exception_summary.get("legacy_exception_series_count")),
        "terminal_11_worse_count": safe_int(exception_summary.get("terminal_11_worse_count")),
        "closed_no_probe_count": status_counts.get("closed_no_probe", 0),
        "manuscript_policy_row_count": status_counts.get("manuscript_confidence_policy", 0),
        "do_not_extend_source_density_count": status_counts.get("do_not_extend_source_density", 0),
        "gpu_priority": "none" if not ready_for_probe else "review_before_gpu",
        "ready_for_manuscript_target1_probe_decision": True,
        "decision": (
            "Do not launch a target1 Tx/Rx/source-count GPU probe under the current archived "
            "hypothesis. Target1 canonical rows are exact; weak base margins are secondary-confirmed "
            "for modern ringdown050 rows; source-density escalation is nonmonotonic and terminal "
            "11-source branches are worse. A future GPU run needs a new objective, geometry, "
            "or acquisition hypothesis stated before execution."
        ),
    }


def status_color(status: str) -> str:
    return {
        "closed_no_probe": "#2f9d55",
        "manuscript_confidence_policy": "#4c78a8",
        "do_not_extend_source_density": "#c7302b",
        "secondary_confirmed_no_gpu": "#9467bd",
        "reference_setting": "#6b6b6b",
        "archive_caveat_no_gpu": "#d98c20",
        "narrow_probe_candidate": "#c7302b",
    }.get(status, "#6b6b6b")


def plot_scorecard(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["gate_key"].replace("_", "\n") for row in rows]
    values = [safe_float(row.get("current_value"), 0.0) for row in rows]
    triggered = [1.0 if row["triggered"] else 0.0 for row in rows]
    colors = [status_color(row["status"]) for row in rows]
    statuses = list(dict.fromkeys(row["status"] for row in rows))

    fig, axes = plt.subplots(1, 2, figsize=(16.2, 5.7), constrained_layout=True)
    x = np.arange(len(rows))
    axes[0].bar(x, values, color=colors, width=0.64)
    axes[0].set_xticks(x, labels, fontsize=8)
    axes[0].set_ylabel("current metric value")
    axes[0].set_title("Target1 probe gates")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(
        handles=[Patch(color=status_color(status), label=status.replace("_", " ")) for status in statuses],
        loc="upper right",
        frameon=False,
        fontsize=8,
    )

    axes[1].bar(x, triggered, color=["#c7302b" if item else "#2f9d55" for item in triggered], width=0.64)
    axes[1].set_xticks(x, labels, fontsize=8)
    axes[1].set_ylim(0, 1.05)
    axes[1].set_ylabel("probe trigger")
    axes[1].set_title("GPU-trigger check")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.96,
        f"triggered gates: {summary['triggered_gate_count']}\nGPU actions: {summary['gpu_action_count']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )

    fig.suptitle("Local 2D target1 probe-readiness scorecard", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, summary_json: Path, validation_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_target1_probe_readiness_scorecard.png`",
                "",
                "This CPU-only scorecard consolidates the saved target1 weak-exact,",
                "acquisition-confidence, source-density exception, and next-question",
                "outputs into explicit target1 GPU-probe gates.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Scorecard rows: `{summary['scorecard_row_count']}`.",
                f"Triggered gates: `{summary['triggered_gate_count']}`.",
                f"GPU action count: `{summary['gpu_action_count']}`.",
                f"Ready for target1 GPU probe: `{summary['ready_for_target1_gpu_probe']}`.",
                f"Modern exception series: `{summary['modern_exception_series_count']}`.",
                "",
                "Outputs:",
                "",
                f"- Scorecard rows: `{rows_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                f"- Figure validation: `{validation_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "The scorecard reads existing CSV/JSON artifacts only. It does not run",
                "FDTD, FWI, optimizer, GPU, 3D/HPC, field FWI, or neural-network jobs.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weak-subset-csv", default=DEFAULT_WEAK_SUBSET_CSV)
    parser.add_argument("--acquisition-summary-json", default=DEFAULT_ACQUISITION_SUMMARY_JSON)
    parser.add_argument("--acquisition-surface-csv", default=DEFAULT_ACQUISITION_SURFACE_CSV)
    parser.add_argument("--source-branch-csv", default=DEFAULT_SOURCE_BRANCH_CSV)
    parser.add_argument("--exception-summary-json", default=DEFAULT_EXCEPTION_SUMMARY_JSON)
    parser.add_argument("--exception-branch-csv", default=DEFAULT_EXCEPTION_BRANCH_CSV)
    parser.add_argument("--next-matrix-summary-json", default=DEFAULT_NEXT_MATRIX_SUMMARY_JSON)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--run-name", default="local_2d_target1_probe_readiness_scorecard")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    weak_subset_rows = read_csv_rows(Path(args.weak_subset_csv))
    acquisition_summary = read_json(Path(args.acquisition_summary_json))
    surface_rows = read_csv_rows(Path(args.acquisition_surface_csv))
    source_branch_rows = read_csv_rows(Path(args.source_branch_csv))
    exception_summary = read_json(Path(args.exception_summary_json))
    exception_branch_rows = read_csv_rows(Path(args.exception_branch_csv))
    next_matrix_summary = read_json(Path(args.next_matrix_summary_json))

    rows = build_probe_rows(
        acquisition_summary=acquisition_summary,
        exception_summary=exception_summary,
        next_matrix_summary=next_matrix_summary,
        weak_subset_rows=weak_subset_rows,
        surface_rows=surface_rows,
        source_branch_rows=source_branch_rows,
        exception_branch_rows=exception_branch_rows,
    )
    summary = summarize_probe_rows(rows, acquisition_summary, exception_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_target1_probe_readiness_rows.csv"
    summary_json = data_dir / "local_2d_target1_probe_readiness_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_target1_probe_readiness_scorecard.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    plot_scorecard(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, rows_csv, summary_json, validation_csv)
    write_run_manifest(
        str(outdir),
        "local_2d_target1_probe_readiness_scorecard",
        {
            "weak_subset_csv": args.weak_subset_csv,
            "acquisition_summary_json": args.acquisition_summary_json,
            "acquisition_surface_csv": args.acquisition_surface_csv,
            "source_branch_csv": args.source_branch_csv,
            "exception_summary_json": args.exception_summary_json,
            "exception_branch_csv": args.exception_branch_csv,
            "next_matrix_summary_json": args.next_matrix_summary_json,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

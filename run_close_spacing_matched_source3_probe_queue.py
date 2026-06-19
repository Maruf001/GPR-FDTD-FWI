#!/usr/bin/env python3
"""Build a resource-bounded queue for matched close14/close50 source3 probes."""

from __future__ import annotations

import argparse
import csv
import glob
import json
import math
import os
import shlex
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
from run_local_2d_detector_rank_budget_diagnostic import safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


SEEDS = (13, 21, 34)
REFERENCE_RUNS = (
    "274_coordinate_optimizer_close50_seed34_sources3_txrx40_objectives",
    "1344_coordinate_optimizer_close50_seed13_sources3_txrx40_objectives",
    "1345_coordinate_optimizer_close50_seed21_sources3_txrx40_objectives",
    "336_coordinate_optimizer_close14_seed34_sources3_txrx45_objectives",
    "1346_coordinate_optimizer_close14_seed13_sources3_txrx45_objectives",
    "1347_coordinate_optimizer_close14_seed21_sources3_txrx45_objectives",
)
PROBE_FAMILIES = (
    {
        "probe_family": "close14_source3_txrx40",
        "priority": 1,
        "family": "close14",
        "tx_rx_offset_mm": 40,
        "target2_x_mm": 264,
        "target1_target2_gap_mm": 14,
        "reference_runtime_family": "close14_source3_txrx45",
        "matched_existing_family": "close50_source3_txrx40",
        "claim_value": "matches close50 source3 Tx/Rx40 while retaining close14 spacing",
    },
    {
        "probe_family": "close50_source3_txrx45",
        "priority": 2,
        "family": "close50",
        "tx_rx_offset_mm": 45,
        "target2_x_mm": 300,
        "target1_target2_gap_mm": 50,
        "reference_runtime_family": "close50_source3_txrx40",
        "matched_existing_family": "close14_source3_txrx45",
        "claim_value": "matches close14 source3 Tx/Rx45 while retaining close50 spacing",
    },
)


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def txrx_label(tx_rx_offset_mm: int | float) -> str:
    value = float(tx_rx_offset_mm)
    return str(int(value)) if value.is_integer() else str(value).replace(".", "p")


def run_name(family: str, seed: int, tx_rx_offset_mm: int | float) -> str:
    return f"coordinate_optimizer_{family}_seed{int(seed)}_sources3_txrx{txrx_label(tx_rx_offset_mm)}_objectives"


def replication_cases(seed: int) -> str:
    return (
        f"noise10_seed{seed}:1.0,0.0,1.0,0.1,{seed}|"
        f"source_mismatch_noise10_seed{seed}:1.1,-50,1.1,0.1,{seed}"
    )


def optimizer_command(family: str, seed: int, tx_rx_offset_mm: int | float, target2_x_mm: int | float) -> list[str]:
    true_x_values = f"190,250,{txrx_label(target2_x_mm)}"
    return [
        "conda",
        "run",
        "-n",
        "gpr-fdtd-fwi",
        "python",
        "run_multi_rebar_coordinate_optimizer.py",
        "--backend",
        "gpu-cpml",
        "--grid-step-mm",
        "1",
        "--sources",
        "3",
        "--tx-rx-offset-mm",
        str(tx_rx_offset_mm),
        "--frequency-ghz",
        "1.5",
        "--true-x-values-mm",
        true_x_values,
        "--true-z-values-mm",
        "90,90,90",
        "--truth-radius-values-mm",
        "5,6,8",
        "--initial-x-values-mm",
        true_x_values,
        "--initial-z-values-mm",
        "90,90,85",
        "--initial-radius-values-mm",
        "6,6,6",
        "--target-indices",
        "2",
        "--passes",
        "1",
        "--x-offsets-mm=-2:2:1",
        "--z-offsets-mm=0,5,10",
        "--radius-offsets-mm=-1:2:0.5",
        "--replication-cases",
        replication_cases(seed),
        "--update-case-label",
        f"source_mismatch_noise10_seed{seed}",
        "--source-frequency-scales",
        "0.9,1.0,1.1",
        "--source-time-shift-ps-values=-50,0,50",
        "--diagnostic-objective-variants",
        "base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15",
        "--top-k",
        "20",
        "--revisit-weak-high-radius-targets",
        "--revisit-broad-radius-ambiguity-targets",
        "--revisit-ambiguity-min-width-mm",
        "0.2",
        "--revisit-x-offsets-mm=-1:1:1",
        "--revisit-z-offsets-mm=-2:2:1",
        "--revisit-radius-step-mm",
        "0.5",
        "--progress-every",
        "25",
        "--run-name",
        run_name(family, seed, tx_rx_offset_mm),
    ]


def existing_output_dirs(experiment_root: Path, name: str) -> list[str]:
    matches = sorted(glob.glob(str(experiment_root / f"*_{name}")))
    matches.extend(sorted(glob.glob(str(experiment_root / name))))
    return [path for path in dict.fromkeys(matches) if Path(path).is_dir()]


def completed_result_fields(existing_dir: str) -> dict:
    if not existing_dir:
        return {
            "completed_summary_path": "",
            "completed_elapsed_time_s": "",
            "final_target2_x_mm": "",
            "final_target2_z_mm": "",
            "final_target2_radius_mm": "",
            "truth_selected_all_cases": "",
            "strong_case_count": "",
            "min_radius_margin_abs": "",
            "max_ambiguity_x_width_mm": "",
        }
    summary_path = Path(existing_dir) / "data/multi_rebar_coordinate_optimizer_summary.json"
    if not summary_path.exists():
        return {
            "completed_summary_path": "",
            "completed_elapsed_time_s": "",
            "final_target2_x_mm": "",
            "final_target2_z_mm": "",
            "final_target2_radius_mm": "",
            "truth_selected_all_cases": "",
            "strong_case_count": "",
            "min_radius_margin_abs": "",
            "max_ambiguity_x_width_mm": "",
        }
    summary = read_json(summary_path)
    target_index = 2
    truth_x = safe_float(summary.get("true_x_values_mm", [math.nan, math.nan, math.nan])[target_index])
    truth_z = safe_float(summary.get("true_z_values_mm", [math.nan, math.nan, math.nan])[target_index])
    truth_r = safe_float(summary.get("truth_radius_values_mm", [math.nan, math.nan, math.nan])[target_index])
    final_state = summary.get("final_state", {})
    final_x = safe_float(final_state.get("x_values_mm", [math.nan, math.nan, math.nan])[target_index])
    final_z = safe_float(final_state.get("z_values_mm", [math.nan, math.nan, math.nan])[target_index])
    final_r = safe_float(final_state.get("radii_mm", [math.nan, math.nan, math.nan])[target_index])
    rows = summary.get("confidence_rows", [])
    margins = [safe_float(row.get("radius_margin_abs"), math.nan) for row in rows]
    ambiguity_widths = [
        safe_float(row.get("ambiguity_x_max_mm"), math.nan) - safe_float(row.get("ambiguity_x_min_mm"), math.nan)
        for row in rows
        if math.isfinite(safe_float(row.get("ambiguity_x_max_mm"), math.nan))
        and math.isfinite(safe_float(row.get("ambiguity_x_min_mm"), math.nan))
    ]
    truth_selected_all = (
        math.isfinite(final_x)
        and math.isfinite(final_z)
        and math.isfinite(final_r)
        and final_x == truth_x
        and final_z == truth_z
        and final_r == truth_r
        and all(
            safe_float(row.get("best_x_mm"), math.nan) == truth_x
            and safe_float(row.get("best_z_mm"), math.nan) == truth_z
            and safe_float(row.get("best_radius_mm"), math.nan) == truth_r
            for row in rows
        )
    )
    return {
        "completed_summary_path": str(summary_path),
        "completed_elapsed_time_s": safe_float(summary.get("elapsed_time_s"), math.nan),
        "final_target2_x_mm": final_x,
        "final_target2_z_mm": final_z,
        "final_target2_radius_mm": final_r,
        "truth_selected_all_cases": truth_selected_all,
        "strong_case_count": sum(str(row.get("confidence_label")) == "strong" for row in rows),
        "min_radius_margin_abs": min((value for value in margins if math.isfinite(value)), default=""),
        "max_ambiguity_x_width_mm": max(ambiguity_widths, default=""),
    }


def runtime_reference_rows(experiment_root: Path, reference_runs: tuple[str, ...] = REFERENCE_RUNS) -> list[dict]:
    rows = []
    for reference_run in reference_runs:
        summary_path = experiment_root / reference_run / "data/multi_rebar_coordinate_optimizer_summary.json"
        if not summary_path.exists():
            continue
        summary = read_json(summary_path)
        family = "close14" if "close14" in reference_run else "close50"
        txrx = safe_float(summary.get("tx_rx_offset_mm"), math.nan)
        rows.append(
            {
                "run_name": summary.get("run_name", reference_run),
                "runtime_family": f"{family}_source3_txrx{txrx_label(txrx)}",
                "seed": int(str(reference_run).split("_seed", 1)[1].split("_", 1)[0]),
                "family": family,
                "tx_rx_offset_mm": txrx,
                "target2_x_mm": safe_float(summary.get("true_x_values_mm", [math.nan, math.nan, math.nan])[2]),
                "final_target2_x_mm": safe_float(summary.get("final_state", {}).get("x_values_mm", [math.nan, math.nan, math.nan])[2]),
                "final_target2_radius_mm": safe_float(
                    summary.get("final_state", {}).get("radii_mm", [math.nan, math.nan, math.nan])[2]
                ),
                "elapsed_time_s": safe_float(summary.get("elapsed_time_s")),
                "summary_path": str(summary_path),
            }
        )
    return rows


def mean_runtime_by_family(runtime_rows: list[dict]) -> dict[str, float]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in runtime_rows:
        elapsed = safe_float(row.get("elapsed_time_s"), math.nan)
        if math.isfinite(elapsed):
            grouped[str(row["runtime_family"])].append(elapsed)
    all_values = [value for values in grouped.values() for value in values]
    fallback = float(np.mean(all_values)) if all_values else math.nan
    return {
        **{family: float(np.mean(values)) for family, values in grouped.items() if values},
        "fallback": fallback,
    }


def probe_rows(experiment_root: Path, runtime_rows: list[dict], seeds: tuple[int, ...] = SEEDS) -> list[dict]:
    runtimes = mean_runtime_by_family(runtime_rows)
    rows = []
    for family in PROBE_FAMILIES:
        estimate = runtimes.get(family["reference_runtime_family"], runtimes.get("fallback", math.nan))
        for seed in seeds:
            name = run_name(family["family"], seed, family["tx_rx_offset_mm"])
            existing = existing_output_dirs(experiment_root, name)
            result_fields = completed_result_fields(existing[0] if existing else "")
            command = optimizer_command(family["family"], seed, family["tx_rx_offset_mm"], family["target2_x_mm"])
            rows.append(
                {
                    "probe_family": family["probe_family"],
                    "priority": family["priority"],
                    "seed": seed,
                    "family": family["family"],
                    "sources": 3,
                    "tx_rx_offset_mm": family["tx_rx_offset_mm"],
                    "target2_x_mm": family["target2_x_mm"],
                    "target1_target2_gap_mm": family["target1_target2_gap_mm"],
                    "matched_existing_family": family["matched_existing_family"],
                    "claim_value": family["claim_value"],
                    "run_name": name,
                    "status": "existing" if existing else "missing",
                    "skip_existing": bool(existing),
                    "existing_output_dir": existing[0] if existing else "",
                    "estimated_runtime_s": estimate,
                    "command_text": shlex.join(command),
                    **result_fields,
                }
            )
    return rows


def aggregate_command_for_family(rows: list[dict], probe_family: str) -> str:
    selected = sorted([row for row in rows if row["probe_family"] == probe_family], key=lambda row: safe_int(row["seed"]))
    family = selected[0]["family"]
    txrx = txrx_label(selected[0]["tx_rx_offset_mm"])
    summary_paths = [
        f"outputs/experiments/*_{row['run_name']}/data/multi_rebar_coordinate_optimizer_summary.json"
        for row in selected
    ]
    prefix = [
        "conda",
        "run",
        "-n",
        "gpr-fdtd-fwi",
        "python",
        "run_coordinate_confidence_aggregate.py",
    ]
    suffix = [
        "--run-name",
        f"coordinate_confidence_{family}_sources3_txrx{txrx}_matched_seed_replicates",
    ]
    return " ".join([shlex.join(prefix), *summary_paths, shlex.join(suffix)])


def family_rows(rows: list[dict]) -> list[dict]:
    out = []
    for family in PROBE_FAMILIES:
        selected = [row for row in rows if row["probe_family"] == family["probe_family"]]
        missing = [row for row in selected if row["status"] == "missing"]
        existing = [row for row in selected if row["status"] == "existing"]
        estimate = sum(safe_float(row.get("estimated_runtime_s"), 0.0) for row in missing)
        out.append(
            {
                "probe_family": family["probe_family"],
                "priority": family["priority"],
                "matched_existing_family": family["matched_existing_family"],
                "claim_value": family["claim_value"],
                "seed_count": len(selected),
                "existing_seed_count": len(existing),
                "missing_seed_count": len(missing),
                "missing_seed_values": ",".join(str(row["seed"]) for row in missing),
                "estimated_missing_runtime_s": estimate,
                "estimated_missing_runtime_min": estimate / 60.0,
                "aggregate_command": aggregate_command_for_family(rows, family["probe_family"]),
                "launch_status": "ready_skip_existing" if missing else "already_complete",
            }
        )
    return out


def summarize_queue(rows: list[dict], families: list[dict], runtime_rows: list[dict]) -> dict:
    missing = [row for row in rows if row["status"] == "missing"]
    existing = [row for row in rows if row["status"] == "existing"]
    total_runtime = sum(safe_float(row.get("estimated_runtime_s"), 0.0) for row in missing)
    max_runtime = max((safe_float(row.get("elapsed_time_s"), 0.0) for row in runtime_rows), default=0.0)
    if existing and missing:
        queue_status = "partially_complete_ready_skip_existing"
    elif existing and not missing:
        queue_status = "complete_ready_for_aggregation"
    else:
        queue_status = "ready_but_not_launched"
    return {
        "policy_label": "close_spacing_matched_source3_probe_queue",
        "queue_status": queue_status,
        "probe_family_count": len(families),
        "seed_probe_count": len(rows),
        "existing_seed_probe_count": len(existing),
        "missing_seed_probe_count": len(missing),
        "missing_seed_probe_keys": ";".join(f"{row['probe_family']}:seed{row['seed']}" for row in missing),
        "estimated_missing_gpu_runtime_s": total_runtime,
        "estimated_missing_gpu_runtime_min": total_runtime / 60.0,
        "max_reference_single_seed_runtime_s": max_runtime,
        "ready_for_matched_narrow_probe_queue": True,
        "ready_for_spacing_only_causal_claim_now": False,
        "ready_for_broad_gpu_queue": False,
        "maximum_parallel_gpu_jobs": 1,
        "ram_limit_fraction": 0.80,
        "gpu_utilization_limit_fraction": 0.90,
        "autonomous_gpu_launch_ready": False,
        "gpu_priority": "narrow_conditional_not_launched",
        "decision": (
            "The useful synthetic 2D extension is a matched source3 control, not a repeat of "
            "the old 270/280 branch and not a broad GPU queue. Run close14 source3 Tx/Rx40 "
            "and close50 source3 Tx/Rx45 seeds 13/21/34 only if the manuscript needs a "
            "spacing-only source-density claim. Launch at most one seed at a time and keep "
            "GPU utilization <=90% and RAM <=80%; this CPU contract does not launch them."
        ),
    }


def write_command_file(path: Path, rows: list[dict], families: list[dict]) -> None:
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "# Matched close-spacing source3 probe queue.",
        "# Run only if spacing-only causality is needed for the manuscript.",
        "# Launch at most one optimizer seed at a time; keep GPU <=90% and RAM <=80%.",
        "",
    ]
    for row in rows:
        lines.append(f"# {row['probe_family']} seed {row['seed']}: {row['status']}")
        if row["skip_existing"]:
            lines.append(f"# skip existing: {row['existing_output_dir']}")
        else:
            lines.append(row["command_text"])
        lines.append("")
    lines.append("# Aggregate after all three seeds exist for a family:")
    for row in families:
        lines.append(row["aggregate_command"])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    path.chmod(0o755)


def plot_queue(families: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["probe_family"].replace("_", "\n") for row in families]
    missing = [safe_int(row["missing_seed_count"], 0) for row in families]
    runtime_min = [safe_float(row["estimated_missing_runtime_min"], 0.0) for row in families]
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.9), constrained_layout=True)
    axes[0].bar(np.arange(len(labels)), missing, color="#e15759", width=0.55)
    axes[0].set_xticks(np.arange(len(labels)), labels, fontsize=8)
    axes[0].set_ylabel("missing seed runs")
    axes[0].set_title("Skip-existing matched probe status")
    axes[0].set_ylim(0, max(3.5, max(missing, default=0) + 0.5))
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(np.arange(len(labels)), runtime_min, color="#4e79a7", width=0.55)
    axes[1].set_xticks(np.arange(len(labels)), labels, fontsize=8)
    axes[1].set_ylabel("estimated missing runtime (min)")
    axes[1].set_title("Runtime estimate from prior source3 jobs")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.96,
        f"missing seeds={summary['missing_seed_probe_count']}\n"
        f"total estimate={summary['estimated_missing_gpu_runtime_min']:.1f} min\n"
        f"broad queue={summary['ready_for_broad_gpu_queue']}\n"
        f"auto launch={summary['autonomous_gpu_launch_ready']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Close-spacing matched source3 probe queue", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `close_spacing_matched_source3_probe_queue.png`",
                "",
                "This CPU-only figure summarizes a skip-existing queue for the matched",
                "close14/close50 source3 probe needed only for spacing-only causal wording.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Missing seed probes: `{summary['missing_seed_probe_count']}`.",
                f"Estimated missing runtime: `{summary['estimated_missing_gpu_runtime_min']:.2f}` min.",
                f"Ready for spacing-only causal claim now: `{summary['ready_for_spacing_only_causal_claim_now']}`.",
                f"Ready for broad GPU queue: `{summary['ready_for_broad_gpu_queue']}`.",
                f"Autonomous GPU launch ready: `{summary['autonomous_gpu_launch_ready']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Scope boundary: this run writes queue tables and commands only. It does",
                "not run FDTD, FWI, GPU kernels, field FWI, 3D/HPC, or neural-network",
                "training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default="outputs/experiments")
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--run-name", default="close_spacing_matched_source3_probe_queue")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    experiment_root = Path(args.experiment_root)
    runtime_rows = runtime_reference_rows(experiment_root)
    rows = probe_rows(experiment_root, runtime_rows)
    families = family_rows(rows)
    summary = summarize_queue(rows, families, runtime_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    runtime_csv = data_dir / "close_spacing_matched_source3_reference_runtime_rows.csv"
    probe_csv = data_dir / "close_spacing_matched_source3_probe_rows.csv"
    family_csv = data_dir / "close_spacing_matched_source3_probe_family_rows.csv"
    command_file = data_dir / "close_spacing_matched_source3_probe_commands.sh"
    summary_json = data_dir / "close_spacing_matched_source3_probe_queue_summary.json"
    figure_path = figures_dir / "close_spacing_matched_source3_probe_queue.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"
    validation_csv = data_dir / "figure_validation.csv"

    write_csv(runtime_csv, [json_safe(row) for row in runtime_rows])
    write_csv(probe_csv, [json_safe(row) for row in rows])
    write_csv(family_csv, [json_safe(row) for row in families])
    write_command_file(command_file, rows, families)
    plot_queue(families, summary, figure_path)
    write_figure_notes(figure_notes, summary)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])

    summary["paths"] = {
        "runtime_csv": str(runtime_csv),
        "probe_csv": str(probe_csv),
        "family_csv": str(family_csv),
        "command_file": str(command_file),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "close_spacing_matched_source3_probe_queue",
        {
            "summary_json": str(summary_json),
            "probe_csv": str(probe_csv),
            "family_csv": str(family_csv),
            "command_file": str(command_file),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

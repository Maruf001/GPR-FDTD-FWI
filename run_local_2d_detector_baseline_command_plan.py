#!/usr/bin/env python3
"""Build a CPU-first command plan for same-case 2D detector baselines."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shlex
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
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CONTRACT_RUN = "016_local_2d_baseline_comparison_contract_post_readiness_audit"
DEFAULT_SOURCE_SUMMARIES = (
    "outputs/experiments/1294_coordinate_optimizer_close14_seed13_sources5_txrx45_noise15p361328125_objectives/data/multi_rebar_coordinate_optimizer_summary.json",
    "outputs/experiments/1295_coordinate_optimizer_close14_seed21_sources5_txrx45_noise15p361328125_objectives/data/multi_rebar_coordinate_optimizer_summary.json",
    "outputs/experiments/354_coordinate_optimizer_close14_seed34_sources5_txrx45_noise15p361328125_objectives/data/multi_rebar_coordinate_optimizer_summary.json",
    "outputs/experiments/1272_coordinate_optimizer_close50_seed13_sources4_txrx29p5_linear_receiver_objectives/data/multi_rebar_coordinate_optimizer_summary.json",
    "outputs/experiments/1271_coordinate_optimizer_close50_seed21_sources4_txrx29p5_linear_receiver_objectives/data/multi_rebar_coordinate_optimizer_summary.json",
    "outputs/experiments/1302_coordinate_optimizer_close50_seed34_sources4_txrx29p5_linear_receiver_objectives/data/multi_rebar_coordinate_optimizer_summary.json",
)

SCAN_STEP_MM = 8.0
DETECTOR_TIME_OFFSETS_PS = "500,550,600,650,667,700,750"
DETECTOR_X_PAD_MM = 10.0
DETECTOR_Z_MIN_MM = 75.0
DETECTOR_Z_MAX_MM = 110.0
DETECTOR_GRID_STEP_MM = 1.0
DETECTOR_TOP_K = 20
DETECTOR_MIN_SEPARATION_MM = 4.0
TRUTH_TOLERANCE_MM = 8.0


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def format_float(value: float) -> str:
    value = float(value)
    if math.isclose(value, round(value), abs_tol=1.0e-12):
        return str(int(round(value)))
    return f"{value:g}"


def format_mm_values(values: list[float]) -> str:
    return ",".join(format_float(float(value)) for value in values)


def slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", text.strip().lower()).strip("_")
    return slug or "case"


def branch_key(summary: dict) -> str:
    true_x = [float(value) for value in summary["true_x_values_mm"]]
    target_x = true_x[int(summary.get("target_indices", [len(true_x) - 1])[-1])]
    if math.isclose(target_x, 264.0, abs_tol=0.25):
        return "target2_close14"
    if math.isclose(target_x, 300.0, abs_tol=0.25):
        return "target2_close50_linear29p5"
    return f"target{summary.get('target_indices', ['x'])[-1]}_x{format_float(target_x)}"


def case_variant(label: str) -> str:
    return "source_mismatch" if str(label).startswith("source_mismatch") else "nominal"


def detector_x_range(true_x_values_mm: list[float]) -> str:
    start = min(float(value) for value in true_x_values_mm) - DETECTOR_X_PAD_MM
    stop = max(float(value) for value in true_x_values_mm) + DETECTOR_X_PAD_MM
    return f"{format_float(start)}:{format_float(stop)}:{format_float(DETECTOR_GRID_STEP_MM)}"


def detector_z_range() -> str:
    return f"{format_float(DETECTOR_Z_MIN_MM)}:{format_float(DETECTOR_Z_MAX_MM)}:{format_float(DETECTOR_GRID_STEP_MM)}"


def existing_output_dirs(experiment_root: Path, run_name: str) -> list[str]:
    if not experiment_root.exists():
        return []
    suffix = f"_{run_name}"
    matches = [
        str(path)
        for path in sorted(experiment_root.iterdir())
        if path.is_dir() and path.name.endswith(suffix)
    ]
    return matches


def detector_run_name(branch: str, seed: int, variant: str) -> str:
    return f"local2d_detector_baseline_{slugify(branch)}_seed{int(seed)}_{slugify(variant)}_cpu"


def command_for_case(row: dict) -> list[str]:
    return [
        "conda",
        "run",
        "-n",
        "gpr-fdtd-fwi",
        "python",
        "run_rebar_detection_pipeline.py",
        "--backend",
        "cpu",
        "--grid-step-mm",
        format_float(row["grid_step_mm"]),
        "--scan-step-mm",
        format_float(row["scan_step_mm"]),
        "--sources",
        str(int(row["sources"])),
        "--tx-rx-offset-mm",
        format_float(row["tx_rx_offset_mm"]),
        "--receiver-sampling",
        row["receiver_sampling"],
        "--frequency-ghz",
        format_float(row["frequency_ghz"]),
        "--truth-x-values-mm",
        row["truth_x_values_mm"],
        "--truth-z-values-mm",
        row["truth_z_values_mm"],
        "--truth-radius-values-mm",
        row["truth_radius_values_mm"],
        "--frequency-scale",
        format_float(row["frequency_scale"]),
        "--time-shift-ps",
        format_float(row["time_shift_ps"]),
        "--amplitude-scale",
        format_float(row["amplitude_scale"]),
        "--noise-fraction",
        format_float(row["noise_fraction"]),
        "--noise-seed",
        str(int(row["noise_seed"])),
        "--detector-x-values-mm",
        row["detector_x_values_mm"],
        "--detector-z-values-mm",
        row["detector_z_values_mm"],
        "--detector-time-offset-ps-values",
        row["detector_time_offset_ps_values"],
        "--top-k",
        str(int(row["top_k"])),
        "--x-min-separation-mm",
        format_float(row["detector_min_separation_mm"]),
        "--z-min-separation-mm",
        format_float(row["detector_min_separation_mm"]),
        "--window-half-x-mm",
        "16",
        "--window-half-z-mm",
        "16",
        "--truth-tolerance-x-mm",
        format_float(row["truth_tolerance_mm"]),
        "--truth-tolerance-z-mm",
        format_float(row["truth_tolerance_mm"]),
        "--background-mode",
        "median",
        "--geometry-mode",
        "hard",
        "--run-name",
        row["run_name"],
    ]


def build_plan_rows(
    source_summaries: list[dict],
    *,
    experiment_root: Path,
) -> list[dict]:
    rows: list[dict] = []
    for summary in source_summaries:
        branch = branch_key(summary)
        true_x = [float(value) for value in summary["true_x_values_mm"]]
        true_z = [float(value) for value in summary["true_z_values_mm"]]
        true_r = [float(value) for value in summary["truth_radius_values_mm"]]
        receiver_sampling = str(summary.get("receiver_sampling") or "nearest")
        target_index = int(summary.get("target_indices", [len(true_x) - 1])[-1])
        for case in summary["replication_cases"]:
            seed = int(case["noise_seed"])
            variant = case_variant(str(case["label"]))
            run_name = detector_run_name(branch, seed, variant)
            existing = existing_output_dirs(experiment_root, run_name)
            row = {
                "branch_key": branch,
                "seed": seed,
                "case_label": str(case["label"]),
                "case_variant": variant,
                "source_optimizer_run_name": summary.get("run_name", ""),
                "target_index": target_index,
                "backend": "cpu",
                "gpu_allowed": False,
                "max_parallel_processes": 1,
                "grid_step_mm": float(summary.get("grid_step_mm", 1.0)),
                "scan_step_mm": SCAN_STEP_MM,
                "sources": int(summary["sources"]),
                "tx_rx_offset_mm": float(summary["tx_rx_offset_mm"]),
                "receiver_sampling": receiver_sampling,
                "frequency_ghz": float(summary["frequency_ghz"]),
                "truth_x_values_mm": format_mm_values(true_x),
                "truth_z_values_mm": format_mm_values(true_z),
                "truth_radius_values_mm": format_mm_values(true_r),
                "frequency_scale": float(case["frequency_scale"]),
                "time_shift_ps": float(case["time_shift_ps"]),
                "amplitude_scale": float(case["amplitude_scale"]),
                "noise_fraction": float(case["noise_fraction"]),
                "noise_seed": seed,
                "detector_x_values_mm": detector_x_range(true_x),
                "detector_z_values_mm": detector_z_range(),
                "detector_time_offset_ps_values": DETECTOR_TIME_OFFSETS_PS,
                "top_k": DETECTOR_TOP_K,
                "detector_min_separation_mm": DETECTOR_MIN_SEPARATION_MM,
                "truth_tolerance_mm": TRUTH_TOLERANCE_MM,
                "run_name": run_name,
                "status": "existing" if existing else "planned_cpu",
                "skip_existing": bool(existing),
                "existing_output_dir": existing[0] if existing else "",
                "command_text": "",
                "comparison_question": comparison_question(branch),
            }
            row["command_text"] = shlex.join(command_for_case(row))
            rows.append(row)
    return sorted(rows, key=lambda item: (item["branch_key"], item["seed"], item["case_variant"]))


def comparison_question(branch: str) -> str:
    if branch == "target2_close14":
        return (
            "Does the detector/database baseline merge the close14 250/264 mm pair, "
            "or can it separate the image cues while FWI remains objective-ambiguous?"
        )
    if branch == "target2_close50_linear29p5":
        return (
            "Does detector-only ambiguity track the seed13 x-ambiguity caveat, "
            "or is the 29.5 mm issue specific to the waveform objective?"
        )
    return "Compare detector-only location cues against the existing optimizer branch."


def summarize_plan(rows: list[dict], contract_summary: dict) -> dict:
    branch_counts = {branch: sum(row["branch_key"] == branch for row in rows) for branch in sorted({row["branch_key"] for row in rows})}
    existing_count = sum(bool(row["skip_existing"]) for row in rows)
    planned_count = len(rows) - existing_count
    return {
        "policy_label": "local_2d_same_case_detector_baseline_command_plan_cpu_first_not_launched",
        "source_contract_policy_label": contract_summary.get("policy_label", ""),
        "planned_case_count": len(rows),
        "planned_cpu_case_count": planned_count,
        "existing_case_count": existing_count,
        "branch_counts": branch_counts,
        "nominal_case_count": sum(row["case_variant"] == "nominal" for row in rows),
        "source_mismatch_case_count": sum(row["case_variant"] == "source_mismatch" for row in rows),
        "backend": "cpu",
        "gpu_allowed": False,
        "gpu_priority": "none",
        "max_parallel_processes": 1,
        "ram_ceiling_percent": 80,
        "gpu_utilization_ceiling_percent": 90,
        "scan_step_mm": SCAN_STEP_MM,
        "detector_grid_step_mm": DETECTOR_GRID_STEP_MM,
        "detector_min_separation_mm": DETECTOR_MIN_SEPARATION_MM,
        "ready_for_single_case_cpu_execution": planned_count > 0,
        "decision": (
            "The next meaningful local 2D baseline step is to run these detector cases one at a time, "
            "skip existing outputs, and compare detector cue separation against the close14 objective "
            "near-tie and close50 seed13 x-ambiguity policies. This artifact does not launch them."
        ),
    }


def write_command_file(path: Path, rows: list[dict], summary: dict) -> None:
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "# CPU-first same-case detector-baseline commands.",
        "# Run at most one command at a time; keep RAM <=80% and GPU utilization <=90%.",
        "# These commands intentionally use --backend cpu and preserve existing experiment outputs.",
        "",
        f"# policy_label: {summary['policy_label']}",
        f"# planned_case_count: {summary['planned_case_count']}",
        "",
    ]
    for row in rows:
        lines.append(f"# {row['branch_key']} seed {row['seed']} {row['case_variant']}: {row['status']}")
        lines.append(f"# question: {row['comparison_question']}")
        if row["skip_existing"]:
            lines.append(f"# skip existing: {row['existing_output_dir']}")
            lines.append(f"# {row['command_text']}")
        else:
            lines.append(row["command_text"])
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    path.chmod(0o755)


def plot_plan(rows: list[dict], summary: dict, save_path: Path) -> str:
    branches = sorted(summary["branch_counts"])
    planned_by_branch = [
        sum(row["branch_key"] == branch and not row["skip_existing"] for row in rows)
        for branch in branches
    ]
    existing_by_branch = [
        sum(row["branch_key"] == branch and row["skip_existing"] for row in rows)
        for branch in branches
    ]

    fig, axes = plt.subplots(1, 2, figsize=(13.8, 5.0), constrained_layout=True)
    x = np.arange(len(branches))
    axes[0].bar(x, planned_by_branch, color="#4c78a8", label="planned CPU")
    axes[0].bar(x, existing_by_branch, bottom=planned_by_branch, color="#2f9d55", label="existing")
    axes[0].set_xticks(x, [branch.replace("_", "\n") for branch in branches], fontsize=8)
    axes[0].set_ylabel("same-case detector commands")
    axes[0].set_title("Detector-baseline command plan")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    gate_labels = ["cases", "CPU planned", "existing", "GPU allowed", "parallel"]
    gate_values = [
        summary["planned_case_count"],
        summary["planned_cpu_case_count"],
        summary["existing_case_count"],
        1 if summary["gpu_allowed"] else 0,
        summary["max_parallel_processes"],
    ]
    axes[1].bar(
        np.arange(len(gate_values)),
        gate_values,
        color=["#4c78a8", "#4c78a8", "#2f9d55", "#c7302b", "#f58518"],
        width=0.62,
    )
    axes[1].set_xticks(np.arange(len(gate_values)), gate_labels)
    axes[1].set_title("Execution gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Local 2D detector baseline: CPU-first command plan", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, summary_json: Path, commands_path: Path, validation_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_detector_baseline_command_plan.png`",
                "",
                "This figure summarizes the CPU-first same-case detector-baseline command plan",
                "for the existing close14 and close50 target2 optimizer evidence. It is a launch",
                "plan, not a detector result and not a GPU/FWI run.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Planned cases: `{summary['planned_case_count']}`.",
                f"CPU cases still planned: `{summary['planned_cpu_case_count']}`.",
                f"Existing cases: `{summary['existing_case_count']}`.",
                f"GPU allowed: `{summary['gpu_allowed']}`.",
                f"Max parallel processes: `{summary['max_parallel_processes']}`.",
                "",
                "Outputs:",
                "",
                f"- Plan rows: `{rows_csv.name}`.",
                f"- Summary: `{summary_json.name}`.",
                f"- Commands: `{commands_path.name}`.",
                f"- Figure validation: `{validation_csv.name}`.",
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
    parser.add_argument("--contract-run", default=DEFAULT_CONTRACT_RUN)
    parser.add_argument("--source-summary", action="append", default=None)
    parser.add_argument("--run-name", default="local_2d_detector_baseline_command_plan")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_root = Path(args.summary_root)
    experiment_root = Path(args.experiment_root)
    contract_summary = read_json(
        summary_root / args.contract_run / "data/local_2d_baseline_comparison_contract_summary.json"
    )
    source_paths = [Path(path) for path in (args.source_summary or DEFAULT_SOURCE_SUMMARIES)]
    source_summaries = [read_json(path) for path in source_paths]
    rows = build_plan_rows(source_summaries, experiment_root=experiment_root)
    summary = summarize_plan(rows, contract_summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "local_2d_detector_baseline_command_plan_rows.csv"
    summary_json = data_dir / "local_2d_detector_baseline_command_plan_summary.json"
    commands_path = data_dir / "local_2d_detector_baseline_commands.sh"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_detector_baseline_command_plan.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_command_file(commands_path, rows, summary)
    plot_plan(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "commands": str(commands_path),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary["source_summary_paths"] = [str(path) for path in source_paths]
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, rows_csv, summary_json, commands_path, validation_csv)
    write_run_manifest(
        str(outdir),
        "local_2d_detector_baseline_command_plan",
        {
            "contract_run": args.contract_run,
            "summary_json": str(summary_json),
            "commands": str(commands_path),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

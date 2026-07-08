#!/usr/bin/env python3
"""Build a skip-existing contract for the target2 close14 source5 probe."""

from __future__ import annotations

import argparse
import glob
import json
import os
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


DEFAULT_BASE_MANIFEST = (
    "outputs/experiments/354_coordinate_optimizer_close14_seed34_sources5_txrx45_"
    "noise15p361328125_objectives/run_manifest.json"
)
DEFAULT_THRESHOLD_SUMMARY = (
    "outputs/experiments/1291_synthetic_objective_threshold_sensitivity/data/"
    "synthetic_objective_threshold_sensitivity_summary.json"
)
DEFAULT_MATRIX_SUMMARY = (
    "outputs/experiments/1292_synthetic_2d_next_question_matrix/data/"
    "synthetic_2d_next_question_matrix_summary.json"
)
PROBE_SEEDS = (13, 21, 34)
NOISE_FRACTION = 0.15361328125
NOISE_LABEL = "noise15p361328125"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def script_command(command: list[str]) -> list[str]:
    for idx, part in enumerate(command):
        if Path(str(part)).name == "run_multi_rebar_coordinate_optimizer.py":
            return list(command[idx:])
    raise ValueError("base manifest command does not include run_multi_rebar_coordinate_optimizer.py")


def without_outdir(command: list[str]) -> list[str]:
    out: list[str] = []
    skip_next = False
    for part in command:
        if skip_next:
            skip_next = False
            continue
        if part == "--outdir":
            skip_next = True
            continue
        if str(part).startswith("--outdir="):
            continue
        out.append(part)
    return out


def replace_option(command: list[str], option: str, value: str) -> list[str]:
    out: list[str] = []
    idx = 0
    replaced = False
    while idx < len(command):
        part = command[idx]
        if part == option:
            out.extend([part, value])
            idx += 2
            replaced = True
            continue
        if str(part).startswith(f"{option}="):
            out.append(f"{option}={value}")
            idx += 1
            replaced = True
            continue
        out.append(part)
        idx += 1
    if not replaced:
        out.extend([option, value])
    return out


def run_name_for_seed(seed: int) -> str:
    return f"coordinate_optimizer_close14_seed{seed}_sources5_txrx45_noise15p361328125_objectives"


def replication_cases_for_seed(seed: int) -> str:
    return (
        f"{NOISE_LABEL}_seed{seed}:1.0,0.0,1.0,{NOISE_FRACTION},{seed}|"
        f"source_mismatch_{NOISE_LABEL}_seed{seed}:1.1,-50,1.1,{NOISE_FRACTION},{seed}"
    )


def command_for_seed(base_command: list[str], seed: int) -> list[str]:
    command = without_outdir(base_command)
    command = replace_option(command, "--replication-cases", replication_cases_for_seed(seed))
    command = replace_option(command, "--update-case-label", f"source_mismatch_{NOISE_LABEL}_seed{seed}")
    command = replace_option(command, "--run-name", run_name_for_seed(seed))
    return ["conda", "run", "-n", "gpr-fdtd-fwi", "python", *command]


def existing_output_dirs(experiment_root: Path, run_name: str) -> list[str]:
    matches = sorted(glob.glob(str(experiment_root / f"*_{run_name}")))
    return [path for path in matches if Path(path).is_dir()]


def probe_contract_rows(base_manifest: dict, experiment_root: Path, seeds: tuple[int, ...] = PROBE_SEEDS) -> list[dict]:
    base_command = script_command(list(base_manifest["command"]))
    rows = []
    for seed in seeds:
        run_name = run_name_for_seed(seed)
        existing = existing_output_dirs(experiment_root, run_name)
        command = command_for_seed(base_command, seed)
        rows.append({
            "seed": seed,
            "target_index": 2,
            "family_label": "target2_close14",
            "sources": 5,
            "tx_rx_offset_mm": 45.0,
            "noise_fraction": NOISE_FRACTION,
            "run_name": run_name,
            "status": "existing" if existing else "missing",
            "skip_existing": bool(existing),
            "existing_output_dir": existing[0] if existing else "",
            "command_text": shlex.join(command),
        })
    return rows


def aggregate_command(rows: list[dict]) -> str:
    summary_paths = [
        f"outputs/experiments/*_{row['run_name']}/data/multi_rebar_coordinate_optimizer_summary.json"
        for row in rows
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
        "coordinate_confidence_close14_target2_sources5_txrx45_seed13_21_34_probe_aggregate",
    ]
    return " ".join([shlex.join(prefix), *summary_paths, shlex.join(suffix)])


def summarize_contract(rows: list[dict], threshold_summary: dict, matrix_summary: dict) -> dict:
    existing = [row for row in rows if row["status"] == "existing"]
    missing = [row for row in rows if row["status"] == "missing"]
    return {
        "policy_label": "target2_close14_source5_txrx45_probe_contract_skip_existing_cpu_no_gpu",
        "contract_status": "ready_but_not_launched",
        "probe_target": "target2_close14_source5_txrx45",
        "target_index": 2,
        "sources": 5,
        "tx_rx_offset_mm": 45.0,
        "noise_fraction": NOISE_FRACTION,
        "seed_count": len(rows),
        "existing_seed_count": len(existing),
        "missing_seed_count": len(missing),
        "existing_seed_values": ",".join(str(row["seed"]) for row in existing),
        "missing_seed_values": ",".join(str(row["seed"]) for row in missing),
        "threshold_policy_label": threshold_summary.get("policy_label", ""),
        "source5_txrx45_near_tie_count_at_scale_0p5": threshold_summary.get(
            "source5_txrx45_near_tie_count_at_scale_0p5"
        ),
        "source5_txrx45_near_tie_count_at_scale_1p0": threshold_summary.get(
            "source5_txrx45_near_tie_count_at_scale_1p0"
        ),
        "next_question_policy_label": matrix_summary.get("policy_label", ""),
        "next_question_top": matrix_summary.get("top_question_key", ""),
        "gpu_priority": "low_conditional_not_launched",
        "resource_policy": "Run at most one missing seed at a time; keep GPU <=90% and RAM <=80%.",
        "decision_rule": (
            "After missing seeds are run and aggregated, evaluate target2 close14 "
            "source5/TxRx45 x near ties at fixed threshold scales 0.5 and 1.0. "
            "If near ties persist across multiple seeds at 0.5x, report a robust "
            "objective-uniqueness limitation; if they disappear outside seed34, "
            "report a seed-specific caveat."
        ),
        "decision": (
            "This contract defines the only current conditional synthetic GPU "
            "probe. Seed34 already exists, so future work should skip it and run "
            "only missing seeds 13 and 21 if the manuscript requires new evidence."
        ),
    }


def write_command_file(path: Path, rows: list[dict], aggregate: str) -> None:
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "# Contract-generated commands. Run only if the manuscript requires this narrow probe.",
        "# Check existing_output_dir/status in the CSV before launching any command.",
        "",
    ]
    for row in rows:
        lines.append(f"# seed {row['seed']}: {row['status']}")
        if row["skip_existing"]:
            lines.append(f"# skip existing: {row['existing_output_dir']}")
        else:
            lines.append(row["command_text"])
        lines.append("")
    lines.extend([
        "# Run after all missing seed optimizer summaries exist:",
        aggregate,
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")
    path.chmod(0o755)


def plot_contract(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [f"seed {row['seed']}" for row in rows]
    existing = np.asarray([1 if row["status"] == "existing" else 0 for row in rows], dtype=np.float64)
    missing = 1.0 - existing
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8), constrained_layout=True)
    x = np.arange(len(rows))
    axes[0].bar(x - 0.18, existing, width=0.36, color="#2f9d55", label="existing")
    axes[0].bar(x + 0.18, missing, width=0.36, color="#c7302b", label="missing")
    axes[0].set_xticks(x, labels)
    axes[0].set_ylim(0.0, 1.2)
    axes[0].set_title("Skip-existing seed status")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].bar(
        [0, 1],
        [
            float(summary["source5_txrx45_near_tie_count_at_scale_0p5"]),
            float(summary["source5_txrx45_near_tie_count_at_scale_1p0"]),
        ],
        color=["#4c78a8", "#f58518"],
        width=0.55,
    )
    axes[1].set_xticks([0, 1], ["0.5x\nthreshold", "1.0x\nthreshold"])
    axes[1].set_ylabel("existing seed34 near-tie rows")
    axes[1].set_title("Current source5/TxRx45 objective gate")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    fig.suptitle(f"Synthetic probe contract: {summary['policy_label']}", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default="outputs/experiments")
    parser.add_argument("--base-manifest", default=DEFAULT_BASE_MANIFEST)
    parser.add_argument("--threshold-summary", default=DEFAULT_THRESHOLD_SUMMARY)
    parser.add_argument("--matrix-summary", default=DEFAULT_MATRIX_SUMMARY)
    parser.add_argument("--run-name", default="synthetic_target2_close14_probe_contract")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    rows = probe_contract_rows(
        read_json(Path(args.base_manifest)),
        Path(args.experiment_root),
    )
    threshold_summary = read_json(Path(args.threshold_summary))
    matrix_summary = read_json(Path(args.matrix_summary))
    summary = summarize_contract(rows, threshold_summary, matrix_summary)
    aggregate = aggregate_command(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.experiment_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "synthetic_target2_close14_probe_contract_rows.csv"
    summary_json = data_dir / "synthetic_target2_close14_probe_contract_summary.json"
    commands_sh = data_dir / "synthetic_target2_close14_probe_contract_commands.sh"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_contract(rows, summary, figures_dir / "synthetic_target2_close14_probe_contract.png"))

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_command_file(commands_sh, rows, aggregate)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "base_manifest": args.base_manifest,
        "threshold_summary": args.threshold_summary,
        "matrix_summary": args.matrix_summary,
        **summary,
        "aggregate_command_text": aggregate,
        "paths": {
            "rows_csv": str(rows_csv),
            "summary_json": str(summary_json),
            "commands_sh": str(commands_sh),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "synthetic_target2_close14_probe_contract",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "commands_sh": str(commands_sh),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()

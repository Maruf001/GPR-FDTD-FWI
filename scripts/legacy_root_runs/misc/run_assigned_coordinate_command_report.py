#!/usr/bin/env python3
"""Build a coordinate-FWI command from assigned detector candidates."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_detection_assignment_report import (  # noqa: E402
    assign_ranked_candidates,
    load_candidates_csv,
    write_assignment_csv,
)


def _csv(values):
    return ",".join(f"{float(value):g}" for value in values)


def _noise_label(noise_fraction, seed):
    return f"noise{int(round(float(noise_fraction) * 100)):02d}_seed{int(seed)}"


def _source_mismatch_label(noise_fraction, seed):
    return f"source_mismatch_{_noise_label(noise_fraction, seed)}"


def build_coordinate_command(
        summary,
        assigned_rows,
        args,
):
    """Return a coordinate optimizer command list."""
    source = summary.get("source", {})
    noise_label = _noise_label(args.noise_fraction, args.noise_seed)
    mismatch_label = _source_mismatch_label(args.noise_fraction, args.noise_seed)
    replication_cases = (
        f"{noise_label}:1.0,0.0,1.0,{args.noise_fraction:g},{args.noise_seed}|"
        f"{mismatch_label}:"
        f"{float(source.get('frequency_scale', 1.0)):g},"
        f"{float(source.get('time_shift_ps', 0.0)):g},"
        f"{float(source.get('amplitude_scale', 1.0)):g},"
        f"{args.noise_fraction:g},{args.noise_seed}"
    )
    truth_radius_values = [float(value) for value in summary["truth_radius_values_mm"]]
    initial_radii = args.initial_radius_values_mm
    if initial_radii is None:
        initial_radii = [truth_radius_values[0]] * len(assigned_rows)
    if len(initial_radii) != len(assigned_rows):
        raise ValueError("--initial-radius-values-mm length must match assigned count")
    target_indices = getattr(args, "target_indices", None)
    if target_indices is None:
        target_indices = ",".join(str(index) for index in range(len(assigned_rows)))

    command = [
        sys.executable,
        "run_multi_rebar_coordinate_optimizer.py",
        "--backend", args.backend,
        "--grid-step-mm", f"{args.grid_step_mm:g}",
        "--sources", str(args.sources),
        "--frequency-ghz", f"{float(summary.get('frequency_ghz', 1.5)):g}",
        "--true-x-values-mm", _csv(summary["truth_x_values_mm"]),
        "--true-z-values-mm", _csv(summary["truth_z_values_mm"]),
        "--initial-x-values-mm", _csv(row["x_mm"] for row in assigned_rows),
        "--initial-z-values-mm", _csv(row["z_mm"] for row in assigned_rows),
        "--initial-radius-values-mm", _csv(initial_radii),
        "--target-indices", str(target_indices),
        "--passes", "1",
        f"--x-offsets-mm={args.x_offsets_mm}",
        f"--z-offsets-mm={args.z_offsets_mm}",
        f"--radius-offsets-mm={args.radius_offsets_mm}",
        "--replication-cases", replication_cases,
        "--update-case-label", mismatch_label,
        "--source-frequency-scales", args.source_frequency_scales,
        f"--source-time-shift-ps-values={args.source_time_shift_ps_values}",
        "--diagnostic-objective-variants",
        "base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15",
        "--revisit-weak-high-radius-targets",
        "--revisit-broad-radius-ambiguity-targets",
        "--revisit-ambiguity-min-width-mm", f"{args.revisit_ambiguity_min_width_mm:g}",
        f"--revisit-x-offsets-mm={args.revisit_x_offsets_mm}",
        f"--revisit-z-offsets-mm={args.revisit_z_offsets_mm}",
        "--revisit-radius-step-mm", f"{args.revisit_radius_step_mm:g}",
        "--progress-every", str(args.progress_every),
        "--run-name", args.coordinate_run_name,
    ]
    if len(set(truth_radius_values)) == 1:
        insert_at = command.index("--initial-x-values-mm")
        command[insert_at:insert_at] = ["--truth-radius-mm", f"{truth_radius_values[0]:g}"]
    else:
        insert_at = command.index("--initial-x-values-mm")
        command[insert_at:insert_at] = ["--truth-radius-values-mm", _csv(truth_radius_values)]
    coordinate_outdir = getattr(args, "coordinate_outdir", None)
    if coordinate_outdir:
        command.extend(["--outdir", str(coordinate_outdir)])
    return command


def run_coordinate_command(command, cwd=PROJECT_ROOT, runner=subprocess.run):
    """Run the coordinate optimizer command and return captured process data."""
    completed = runner(
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def run_coordinate_command_to_files(
        command,
        stdout_path,
        stderr_path,
        cwd=PROJECT_ROOT,
        popen=subprocess.Popen):
    """Run the coordinate optimizer while writing process logs directly to files."""
    stdout_path = Path(stdout_path)
    stderr_path = Path(stderr_path)
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    with stdout_path.open("w", encoding="utf-8") as stdout_handle:
        with stderr_path.open("w", encoding="utf-8") as stderr_handle:
            process = popen(
                command,
                cwd=cwd,
                stdout=stdout_handle,
                stderr=stderr_handle,
                text=True,
                env=env,
            )
            returncode = process.wait()
    return {
        "returncode": returncode,
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
    }


def parse_float_csv(text):
    """Parse optional comma-separated floats."""
    if text is None:
        return None
    values = [float(part.strip()) for part in str(text).split(",") if part.strip()]
    if not values:
        raise argparse.ArgumentTypeError("at least one value is required")
    return values


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("detection_summary_json")
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--min-x-separation-mm", type=float, default=45.0)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--noise-fraction", type=float, default=0.10)
    parser.add_argument("--noise-seed", type=int, default=13)
    parser.add_argument("--initial-radius-values-mm", type=parse_float_csv, default=None)
    parser.add_argument("--target-indices", default=None)
    parser.add_argument("--x-offsets-mm", default="-2:2:1")
    parser.add_argument("--z-offsets-mm", default="-5:1:1")
    parser.add_argument("--radius-offsets-mm", default="-0.4:0.4:0.2")
    parser.add_argument("--source-frequency-scales", default="0.9,1.0,1.1")
    parser.add_argument("--source-time-shift-ps-values", default="-50,0,50")
    parser.add_argument("--revisit-ambiguity-min-width-mm", type=float, default=0.2)
    parser.add_argument("--revisit-x-offsets-mm", default="-1:1:1")
    parser.add_argument("--revisit-z-offsets-mm", default="-2:2:1")
    parser.add_argument("--revisit-radius-step-mm", type=float, default=0.2)
    parser.add_argument("--progress-every", type=int, default=25)
    parser.add_argument("--coordinate-run-name", default="assigned_coordinate_optimizer")
    parser.add_argument("--coordinate-outdir", default=None)
    parser.add_argument("--run-coordinate-fwi", action="store_true")
    parser.add_argument("--coordinate-log-mode", choices=["capture", "file"], default="capture")
    parser.add_argument("--run-name", default="assigned_coordinate_command_report")
    parser.add_argument("--outdir", default=None)
    return parser


def main():
    args = build_parser().parse_args()
    with Path(args.detection_summary_json).open("r", encoding="utf-8") as handle:
        summary = json.load(handle)
    candidates_csv = summary["paths"]["csv"]
    candidate_rows = load_candidates_csv(candidates_csv)
    assigned_rows = assign_ranked_candidates(
        candidate_rows,
        args.count,
        args.min_x_separation_mm,
    )
    command = build_coordinate_command(summary, assigned_rows, args)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    assignment_csv = data_dir / "assigned_detection_candidates.csv"
    command_json = data_dir / "assigned_coordinate_command.json"
    command_txt = data_dir / "assigned_coordinate_command.txt"
    stdout_path = data_dir / "coordinate_launcher_stdout.txt"
    stderr_path = data_dir / "coordinate_launcher_stderr.txt"
    write_assignment_csv(assignment_csv, assigned_rows)
    launcher_result = {
        "mode": "run" if args.run_coordinate_fwi else "dry_run",
        "ran": False,
        "returncode": None,
        "log_mode": args.coordinate_log_mode,
        "stdout_path": None,
        "stderr_path": None,
    }
    if args.run_coordinate_fwi:
        if args.coordinate_log_mode == "file":
            result = run_coordinate_command_to_files(command, stdout_path, stderr_path)
        else:
            result = run_coordinate_command(command)
            stdout_path.write_text(result["stdout"], encoding="utf-8")
            stderr_path.write_text(result["stderr"], encoding="utf-8")
            result = {
                "returncode": result["returncode"],
                "stdout_path": str(stdout_path),
                "stderr_path": str(stderr_path),
            }
        launcher_result = {
            "mode": "run",
            "ran": True,
            "returncode": result["returncode"],
            "log_mode": args.coordinate_log_mode,
            "stdout_path": result["stdout_path"],
            "stderr_path": result["stderr_path"],
        }
    with command_json.open("w", encoding="utf-8") as handle:
        json.dump({
            "detection_summary_json": args.detection_summary_json,
            "candidates_csv": candidates_csv,
            "assigned_rows": assigned_rows,
            "command": command,
            "launcher": launcher_result,
        }, handle, indent=2)
    command_txt.write_text(" ".join(shlex.quote(part) for part in command) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "assigned_coordinate_command_report",
        {
            "detection_summary_json": args.detection_summary_json,
            "assignment_csv": str(assignment_csv),
            "command_json": str(command_json),
            "command_txt": str(command_txt),
            "launcher": launcher_result,
        },
    )
    print(json.dumps({"assigned_rows": assigned_rows, "command": command, "launcher": launcher_result}, indent=2))
    print(f"Wrote command: {command_txt}")
    if args.run_coordinate_fwi:
        print(f"Wrote launcher stdout: {stdout_path}")
        print(f"Wrote launcher stderr: {stderr_path}")
        if launcher_result["returncode"] != 0:
            raise SystemExit(int(launcher_result["returncode"]))
    else:
        print("Dry run only: pass --run-coordinate-fwi to launch the coordinate optimizer.")


if __name__ == "__main__":
    main()

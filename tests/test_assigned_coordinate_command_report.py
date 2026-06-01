"""Tests for assigned coordinate command reports."""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_assigned_coordinate_command_report import (  # noqa: E402
    build_coordinate_command,
    run_coordinate_command,
    run_coordinate_command_to_files,
)


def test_build_coordinate_command_uses_assigned_seed_vectors():
    summary = {
        "frequency_ghz": 1.5,
        "truth_x_values_mm": [150.0, 250.0, 350.0],
        "truth_z_values_mm": [80.0, 100.0, 120.0],
        "truth_radius_values_mm": [6.0, 6.0, 6.0],
        "source": {
            "frequency_scale": 1.1,
            "time_shift_ps": -50.0,
            "amplitude_scale": 1.1,
        },
    }
    assigned_rows = [
        {"x_mm": 148.0, "z_mm": 85.0},
        {"x_mm": 252.0, "z_mm": 105.0},
        {"x_mm": 352.0, "z_mm": 120.0},
    ]
    args = argparse.Namespace(
        backend="gpu-cpml",
        grid_step_mm=1.0,
        sources=5,
        noise_fraction=0.10,
        noise_seed=13,
        initial_radius_values_mm=[6.4, 5.6, 6.4],
        x_offsets_mm="-2:2:1",
        z_offsets_mm="-5:1:1",
        radius_offsets_mm="-0.4:0.4:0.2",
        source_frequency_scales="0.9,1.0,1.1",
        source_time_shift_ps_values="-50,0,50",
        revisit_ambiguity_min_width_mm=0.2,
        revisit_x_offsets_mm="-1:1:1",
        revisit_z_offsets_mm="-2:2:1",
        revisit_radius_step_mm=0.2,
        progress_every=25,
        coordinate_run_name="coordinate",
    )

    command = build_coordinate_command(summary, assigned_rows, args)

    assert "--initial-x-values-mm" in command
    assert command[command.index("--initial-x-values-mm") + 1] == "148,252,352"
    assert command[command.index("--initial-z-values-mm") + 1] == "85,105,120"
    assert "--z-offsets-mm=-5:1:1" in command
    assert "--source-time-shift-ps-values=-50,0,50" in command
    assert "--revisit-broad-radius-ambiguity-targets" in command
    assert command[command.index("--update-case-label") + 1] == "source_mismatch_noise10_seed13"


def test_build_coordinate_command_can_pin_coordinate_outdir():
    summary = {
        "frequency_ghz": 1.5,
        "truth_x_values_mm": [190.0, 250.0, 310.0],
        "truth_z_values_mm": [90.0, 90.0, 90.0],
        "truth_radius_values_mm": [6.0, 6.0, 6.0],
        "source": {},
    }
    assigned_rows = [
        {"x_mm": 188.0, "z_mm": 90.0},
        {"x_mm": 248.0, "z_mm": 90.0},
        {"x_mm": 312.0, "z_mm": 90.0},
    ]
    args = argparse.Namespace(
        backend="gpu-cpml",
        grid_step_mm=1.0,
        sources=5,
        noise_fraction=0.10,
        noise_seed=13,
        initial_radius_values_mm=None,
        x_offsets_mm="-2:2:1",
        z_offsets_mm="-2:2:1",
        radius_offsets_mm="-0.4:0.4:0.2",
        source_frequency_scales="0.9,1.0,1.1",
        source_time_shift_ps_values="-50,0,50",
        revisit_ambiguity_min_width_mm=0.2,
        revisit_x_offsets_mm="-1:1:1",
        revisit_z_offsets_mm="-1:1:1",
        revisit_radius_step_mm=0.2,
        progress_every=25,
        coordinate_run_name="coordinate",
        coordinate_outdir="outputs/experiments/999_coordinate",
    )

    command = build_coordinate_command(summary, assigned_rows, args)

    assert "--outdir" in command
    assert command[command.index("--outdir") + 1] == "outputs/experiments/999_coordinate"


def test_build_coordinate_command_uses_per_target_truth_radii_when_needed():
    summary = {
        "frequency_ghz": 1.5,
        "truth_x_values_mm": [190.0, 250.0, 310.0],
        "truth_z_values_mm": [90.0, 90.0, 90.0],
        "truth_radius_values_mm": [5.0, 6.0, 8.0],
        "source": {},
    }
    assigned_rows = [
        {"x_mm": 188.0, "z_mm": 90.0},
        {"x_mm": 248.0, "z_mm": 90.0},
        {"x_mm": 312.0, "z_mm": 90.0},
    ]
    args = argparse.Namespace(
        backend="gpu-cpml",
        grid_step_mm=1.0,
        sources=5,
        noise_fraction=0.10,
        noise_seed=13,
        initial_radius_values_mm=[6.0, 6.0, 6.0],
        x_offsets_mm="-2:2:1",
        z_offsets_mm="-2:2:1",
        radius_offsets_mm="-1:1:0.5",
        source_frequency_scales="0.9,1.0,1.1",
        source_time_shift_ps_values="-50,0,50",
        revisit_ambiguity_min_width_mm=0.2,
        revisit_x_offsets_mm="-1:1:1",
        revisit_z_offsets_mm="-1:1:1",
        revisit_radius_step_mm=0.2,
        progress_every=25,
        coordinate_run_name="coordinate",
        coordinate_outdir=None,
    )

    command = build_coordinate_command(summary, assigned_rows, args)

    assert "--truth-radius-mm" not in command
    assert "--truth-radius-values-mm" in command
    assert command[command.index("--truth-radius-values-mm") + 1] == "5,6,8"


def test_build_coordinate_command_accepts_explicit_target_order():
    summary = {
        "frequency_ghz": 1.5,
        "truth_x_values_mm": [190.0, 250.0, 310.0],
        "truth_z_values_mm": [90.0, 90.0, 90.0],
        "truth_radius_values_mm": [5.0, 6.0, 8.0],
        "source": {},
    }
    assigned_rows = [
        {"x_mm": 188.0, "z_mm": 100.0},
        {"x_mm": 248.0, "z_mm": 90.0},
        {"x_mm": 312.0, "z_mm": 95.0},
    ]
    args = argparse.Namespace(
        backend="gpu-cpml",
        grid_step_mm=1.0,
        sources=5,
        noise_fraction=0.10,
        noise_seed=13,
        initial_radius_values_mm=[6.0, 6.0, 6.0],
        target_indices="2,1,0",
        x_offsets_mm="-2:2:1",
        z_offsets_mm="-10,-5,0,5",
        radius_offsets_mm="-1:2:0.5",
        source_frequency_scales="0.9,1.0,1.1",
        source_time_shift_ps_values="-50,0,50",
        revisit_ambiguity_min_width_mm=0.2,
        revisit_x_offsets_mm="-1:1:1",
        revisit_z_offsets_mm="-2:2:1",
        revisit_radius_step_mm=0.5,
        progress_every=25,
        coordinate_run_name="coordinate",
        coordinate_outdir=None,
    )

    command = build_coordinate_command(summary, assigned_rows, args)

    assert command[command.index("--target-indices") + 1] == "2,1,0"


def test_run_coordinate_command_uses_project_cwd_and_captures_result():
    calls = []

    class Completed:
        returncode = 0
        stdout = "Output directory: outputs/experiments/999_coordinate\n"
        stderr = ""

    def fake_runner(command, **kwargs):
        calls.append((command, kwargs))
        return Completed()

    result = run_coordinate_command(["python", "run_multi_rebar_coordinate_optimizer.py"], runner=fake_runner)

    assert result["returncode"] == 0
    assert result["stdout"].startswith("Output directory:")
    assert calls[0][1]["check"] is False
    assert calls[0][1]["capture_output"] is True
    assert calls[0][1]["text"] is True
    assert calls[0][1]["cwd"].endswith("GPR-FDTD-FWI")


def test_run_coordinate_command_to_files_streams_process_logs(tmp_path):
    calls = []

    class Process:
        returncode = 0

        def wait(self):
            return self.returncode

    def fake_popen(command, **kwargs):
        kwargs["stdout"].write("progress line\n")
        kwargs["stderr"].write("warning line\n")
        calls.append((command, kwargs))
        return Process()

    stdout_path = tmp_path / "stdout.txt"
    stderr_path = tmp_path / "stderr.txt"
    result = run_coordinate_command_to_files(
        ["python", "run_multi_rebar_coordinate_optimizer.py"],
        stdout_path,
        stderr_path,
        popen=fake_popen,
    )

    assert result["returncode"] == 0
    assert stdout_path.read_text(encoding="utf-8") == "progress line\n"
    assert stderr_path.read_text(encoding="utf-8") == "warning line\n"
    assert calls[0][1]["cwd"].endswith("GPR-FDTD-FWI")
    assert calls[0][1]["text"] is True
    assert calls[0][1]["env"]["PYTHONUNBUFFERED"] == "1"

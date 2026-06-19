from pathlib import Path

from run_local_2d_detector_baseline_command_plan import (
    build_plan_rows,
    command_for_case,
    summarize_plan,
    write_command_file,
)


def _optimizer_summary(run_name, x_values, sources, txrx, sampling, seed):
    return {
        "run_name": run_name,
        "grid_step_mm": 1.0,
        "sources": sources,
        "tx_rx_offset_mm": txrx,
        "receiver_sampling": sampling,
        "frequency_ghz": 1.5,
        "true_x_values_mm": x_values,
        "true_z_values_mm": [90.0, 90.0, 90.0],
        "truth_radius_values_mm": [5.0, 6.0, 8.0],
        "target_indices": [2],
        "replication_cases": [
            {
                "label": f"noise_seed{seed}",
                "frequency_scale": 1.0,
                "time_shift_ps": 0.0,
                "amplitude_scale": 1.0,
                "noise_fraction": 0.1,
                "noise_seed": seed,
            },
            {
                "label": f"source_mismatch_noise_seed{seed}",
                "frequency_scale": 1.1,
                "time_shift_ps": -50.0,
                "amplitude_scale": 1.1,
                "noise_fraction": 0.1,
                "noise_seed": seed,
            },
        ],
    }


def test_build_plan_rows_uses_same_case_cpu_geometry(tmp_path):
    rows = build_plan_rows(
        [
            _optimizer_summary("close14", [190.0, 250.0, 264.0], 5, 45.0, "nearest", 13),
            _optimizer_summary("close50", [190.0, 250.0, 300.0], 4, 29.5, "linear", 21),
        ],
        experiment_root=tmp_path,
    )

    assert len(rows) == 4
    close14 = [row for row in rows if row["branch_key"] == "target2_close14"][0]
    close50 = [row for row in rows if row["branch_key"] == "target2_close50_linear29p5"][0]

    assert close14["backend"] == "cpu"
    assert close14["gpu_allowed"] is False
    assert close14["scan_step_mm"] == 8.0
    assert close14["sources"] == 5
    assert close14["tx_rx_offset_mm"] == 45.0
    assert close14["receiver_sampling"] == "nearest"
    assert close14["detector_x_values_mm"] == "180:274:1"
    assert close14["detector_min_separation_mm"] == 4.0
    assert close50["sources"] == 4
    assert close50["tx_rx_offset_mm"] == 29.5
    assert close50["receiver_sampling"] == "linear"


def test_command_for_case_is_cpu_only_and_passes_detector_offset(tmp_path):
    row = build_plan_rows(
        [_optimizer_summary("close50", [190.0, 250.0, 300.0], 4, 29.5, "linear", 34)],
        experiment_root=tmp_path,
    )[0]
    command = command_for_case(row)
    command_text = " ".join(command)

    assert "--backend cpu" in command_text
    assert "gpu-cpml" not in command_text
    assert "--tx-rx-offset-mm 29.5" in command_text
    assert "--receiver-sampling linear" in command_text
    assert "--scan-step-mm 8" in command_text
    assert "--detector-time-offset-ps-values 500,550,600,650,667,700,750" in command_text


def test_summarize_plan_reports_no_gpu_and_single_process(tmp_path):
    rows = build_plan_rows(
        [_optimizer_summary("close14", [190.0, 250.0, 264.0], 5, 45.0, "nearest", 13)],
        experiment_root=tmp_path,
    )
    summary = summarize_plan(rows, {"policy_label": "contract"})

    assert summary["policy_label"] == "local_2d_same_case_detector_baseline_command_plan_cpu_first_not_launched"
    assert summary["planned_case_count"] == 2
    assert summary["planned_cpu_case_count"] == 2
    assert summary["existing_case_count"] == 0
    assert summary["gpu_allowed"] is False
    assert summary["gpu_priority"] == "none"
    assert summary["max_parallel_processes"] == 1
    assert summary["ram_ceiling_percent"] == 80
    assert summary["gpu_utilization_ceiling_percent"] == 90


def test_write_command_file_records_resource_policy(tmp_path):
    rows = build_plan_rows(
        [_optimizer_summary("close14", [190.0, 250.0, 264.0], 5, 45.0, "nearest", 13)],
        experiment_root=tmp_path,
    )
    summary = summarize_plan(rows, {"policy_label": "contract"})
    path = tmp_path / "commands.sh"

    write_command_file(path, rows, summary)

    text = path.read_text(encoding="utf-8")
    assert "RAM <=80%" in text
    assert "GPU utilization <=90%" in text
    assert "--backend cpu" in text
    assert "run_rebar_detection_pipeline.py" in text
    assert path.stat().st_mode & 0o111


def test_existing_rows_are_commented_in_command_file(tmp_path):
    existing = tmp_path / "1326_local2d_detector_baseline_target2_close14_seed13_nominal_cpu"
    existing.mkdir()
    rows = build_plan_rows(
        [_optimizer_summary("close14", [190.0, 250.0, 264.0], 5, 45.0, "nearest", 13)],
        experiment_root=tmp_path,
    )
    summary = summarize_plan(rows, {"policy_label": "contract"})
    path = tmp_path / "commands.sh"

    write_command_file(path, rows, summary)

    lines = path.read_text(encoding="utf-8").splitlines()
    skip_index = lines.index(f"# skip existing: {existing}")
    assert lines[skip_index + 1].startswith("# conda run")

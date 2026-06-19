import json

from run_close_spacing_matched_source3_probe_queue import (
    completed_result_fields,
    family_rows,
    mean_runtime_by_family,
    optimizer_command,
    probe_rows,
    runtime_reference_rows,
    run_name,
    summarize_queue,
)


def test_run_name_and_optimizer_command_define_matched_source3_probe():
    name = run_name("close14", 13, 40)
    command = optimizer_command("close14", 13, 40, 264)
    command_text = " ".join(command)

    assert name == "coordinate_optimizer_close14_seed13_sources3_txrx40_objectives"
    assert command[:5] == ["conda", "run", "-n", "gpr-fdtd-fwi", "python"]
    assert "--sources 3" in command_text
    assert "--tx-rx-offset-mm 40" in command_text
    assert "190,250,264" in command_text
    assert "noise10_seed13" in command_text
    assert "source_mismatch_noise10_seed13" in command_text
    assert name in command


def test_probe_rows_mark_existing_outputs_and_estimate_runtime(tmp_path):
    existing = tmp_path / "999_coordinate_optimizer_close14_seed13_sources3_txrx40_objectives"
    data_dir = existing / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "multi_rebar_coordinate_optimizer_summary.json").write_text(
        json.dumps(
            {
                "elapsed_time_s": 1177.5,
                "true_x_values_mm": [190, 250, 264],
                "true_z_values_mm": [90, 90, 90],
                "truth_radius_values_mm": [5, 6, 8],
                "final_state": {"x_values_mm": [190, 250, 264], "z_values_mm": [90, 90, 90], "radii_mm": [6, 6, 8]},
                "confidence_rows": [
                    {
                        "best_x_mm": 264,
                        "best_z_mm": 90,
                        "best_radius_mm": 8,
                        "confidence_label": "strong",
                        "radius_margin_abs": 0.003,
                        "ambiguity_x_min_mm": 263,
                        "ambiguity_x_max_mm": 265,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    runtime_rows = [
        {"runtime_family": "close14_source3_txrx45", "elapsed_time_s": 1200.0},
        {"runtime_family": "close50_source3_txrx40", "elapsed_time_s": 1500.0},
    ]

    rows = probe_rows(tmp_path, runtime_rows, seeds=(13,))
    by_family = {row["probe_family"]: row for row in rows}

    assert by_family["close14_source3_txrx40"]["status"] == "existing"
    assert by_family["close14_source3_txrx40"]["skip_existing"] is True
    assert by_family["close14_source3_txrx40"]["estimated_runtime_s"] == 1200.0
    assert by_family["close14_source3_txrx40"]["truth_selected_all_cases"] is True
    assert by_family["close14_source3_txrx40"]["strong_case_count"] == 1
    assert by_family["close50_source3_txrx45"]["status"] == "missing"
    assert by_family["close50_source3_txrx45"]["estimated_runtime_s"] == 1500.0


def test_completed_result_fields_extracts_truth_and_margin(tmp_path):
    run_dir = tmp_path / "1348_coordinate_optimizer_close14_seed13_sources3_txrx40_objectives"
    data_dir = run_dir / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "multi_rebar_coordinate_optimizer_summary.json").write_text(
        json.dumps(
            {
                "elapsed_time_s": 1177.5,
                "true_x_values_mm": [190, 250, 264],
                "true_z_values_mm": [90, 90, 90],
                "truth_radius_values_mm": [5, 6, 8],
                "final_state": {"x_values_mm": [190, 250, 264], "z_values_mm": [90, 90, 90], "radii_mm": [6, 6, 8]},
                "confidence_rows": [
                    {
                        "best_x_mm": 264,
                        "best_z_mm": 90,
                        "best_radius_mm": 8,
                        "confidence_label": "strong",
                        "radius_margin_abs": 0.0031,
                        "ambiguity_x_min_mm": 263,
                        "ambiguity_x_max_mm": 265,
                    },
                    {
                        "best_x_mm": 264,
                        "best_z_mm": 90,
                        "best_radius_mm": 8,
                        "confidence_label": "strong",
                        "radius_margin_abs": 0.0038,
                        "ambiguity_x_min_mm": 264,
                        "ambiguity_x_max_mm": 265,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    fields = completed_result_fields(str(run_dir))

    assert fields["completed_elapsed_time_s"] == 1177.5
    assert fields["final_target2_x_mm"] == 264.0
    assert fields["final_target2_radius_mm"] == 8.0
    assert fields["truth_selected_all_cases"] is True
    assert fields["strong_case_count"] == 2
    assert fields["min_radius_margin_abs"] == 0.0031
    assert fields["max_ambiguity_x_width_mm"] == 2.0


def test_family_rows_and_summary_block_broad_gpu_queue(tmp_path):
    existing = tmp_path / "1348_coordinate_optimizer_close14_seed13_sources3_txrx40_objectives"
    existing.mkdir()
    runtime_rows = [
        {"runtime_family": "close14_source3_txrx45", "elapsed_time_s": 1100.0},
        {"runtime_family": "close14_source3_txrx45", "elapsed_time_s": 1300.0},
        {"runtime_family": "close50_source3_txrx40", "elapsed_time_s": 1500.0},
    ]
    rows = probe_rows(tmp_path, runtime_rows, seeds=(13, 21, 34))
    families = family_rows(rows)
    summary = summarize_queue(rows, families, runtime_rows)
    by_family = {row["probe_family"]: row for row in families}

    assert mean_runtime_by_family(runtime_rows)["close14_source3_txrx45"] == 1200.0
    assert by_family["close14_source3_txrx40"]["missing_seed_count"] == 2
    assert by_family["close50_source3_txrx45"]["estimated_missing_runtime_s"] == 4500.0
    assert "outputs/experiments/*_coordinate_optimizer_close14_seed13_sources3_txrx40_objectives" in by_family[
        "close14_source3_txrx40"
    ]["aggregate_command"]
    assert summary["queue_status"] == "partially_complete_ready_skip_existing"
    assert summary["existing_seed_probe_count"] == 1
    assert summary["missing_seed_probe_count"] == 5
    assert summary["ready_for_matched_narrow_probe_queue"] is True
    assert summary["ready_for_spacing_only_causal_claim_now"] is False
    assert summary["ready_for_broad_gpu_queue"] is False
    assert summary["autonomous_gpu_launch_ready"] is False
    assert summary["maximum_parallel_gpu_jobs"] == 1
    assert summary["gpu_priority"] == "narrow_conditional_not_launched"


def test_runtime_reference_json_shape_is_compatible(tmp_path):
    run_dir = tmp_path / "1344_coordinate_optimizer_close50_seed13_sources3_txrx40_objectives"
    data_dir = run_dir / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "multi_rebar_coordinate_optimizer_summary.json").write_text(
        json.dumps(
            {
                "run_name": "coordinate_optimizer_close50_seed13_sources3_txrx40_objectives",
                "tx_rx_offset_mm": 40,
                "true_x_values_mm": [190, 250, 300],
                "final_state": {"x_values_mm": [190, 250, 299], "radii_mm": [6, 6, 7.5]},
                "elapsed_time_s": 1500,
            }
        ),
        encoding="utf-8",
    )

    references = runtime_reference_rows(
        tmp_path,
        reference_runs=("1344_coordinate_optimizer_close50_seed13_sources3_txrx40_objectives",),
    )
    rows = probe_rows(tmp_path, references, seeds=(13,))

    assert references[0]["runtime_family"] == "close50_source3_txrx40"
    assert references[0]["final_target2_x_mm"] == 299.0
    assert rows[1]["probe_family"] == "close50_source3_txrx45"
    assert rows[1]["status"] == "missing"

from run_synthetic_target2_close14_probe_contract import (
    aggregate_command,
    command_for_seed,
    probe_contract_rows,
    summarize_contract,
    without_outdir,
)


def _base_manifest():
    return {
        "command": [
            "python",
            "run_multi_rebar_coordinate_optimizer.py",
            "--sources",
            "5",
            "--tx-rx-offset-mm",
            "45",
            "--replication-cases",
            "noise15p361328125_seed34:1.0,0.0,1.0,0.15361328125,34",
            "--update-case-label",
            "source_mismatch_noise15p361328125_seed34",
            "--run-name",
            "coordinate_optimizer_close14_seed34_sources5_txrx45_noise15p361328125_objectives",
            "--outdir",
            "outputs/experiments/354_coordinate_optimizer_close14_seed34_sources5_txrx45_noise15p361328125_objectives",
        ]
    }


def test_without_outdir_removes_split_and_equals_forms():
    assert without_outdir(["--run-name", "a", "--outdir", "old", "--sources", "5"]) == [
        "--run-name",
        "a",
        "--sources",
        "5",
    ]
    assert without_outdir(["--outdir=old", "--run-name", "a"]) == ["--run-name", "a"]


def test_command_for_seed_rewrites_seed_labels_and_keeps_launcher_safe():
    command = command_for_seed(_base_manifest()["command"][1:], 13)
    command_text = " ".join(command)

    assert command[:5] == ["conda", "run", "-n", "gpr-fdtd-fwi", "python"]
    assert "--outdir" not in command
    assert "noise15p361328125_seed13" in command_text
    assert "source_mismatch_noise15p361328125_seed13" in command_text
    assert "coordinate_optimizer_close14_seed13_sources5_txrx45_noise15p361328125_objectives" in command_text
    assert "seed34" not in command_text


def test_probe_contract_rows_marks_existing_seed34_and_missing_new_seeds(tmp_path):
    existing = (
        tmp_path
        / "354_coordinate_optimizer_close14_seed34_sources5_txrx45_noise15p361328125_objectives"
    )
    existing.mkdir()

    rows = probe_contract_rows(_base_manifest(), tmp_path, seeds=(13, 21, 34))
    by_seed = {row["seed"]: row for row in rows}

    assert by_seed[13]["status"] == "missing"
    assert by_seed[21]["skip_existing"] is False
    assert by_seed[34]["status"] == "existing"
    assert by_seed[34]["skip_existing"] is True
    assert by_seed[34]["existing_output_dir"] == str(existing)


def test_aggregate_command_leaves_summary_globs_expandable():
    rows = [
        {"run_name": "coordinate_optimizer_close14_seed13_sources5_txrx45_noise15p361328125_objectives"},
        {"run_name": "coordinate_optimizer_close14_seed21_sources5_txrx45_noise15p361328125_objectives"},
        {"run_name": "coordinate_optimizer_close14_seed34_sources5_txrx45_noise15p361328125_objectives"},
    ]

    command = aggregate_command(rows)

    assert "'outputs/experiments/*_" not in command
    assert "outputs/experiments/*_coordinate_optimizer_close14_seed13" in command
    assert command.startswith("conda run -n gpr-fdtd-fwi python run_coordinate_confidence_aggregate.py")
    assert "--run-name coordinate_confidence_close14_target2_sources5_txrx45_seed13_21_34_probe_aggregate" in command


def test_summarize_contract_keeps_gpu_conditional_and_records_decision_inputs():
    rows = [
        {"seed": 13, "status": "missing"},
        {"seed": 21, "status": "missing"},
        {"seed": 34, "status": "existing"},
    ]
    threshold_summary = {
        "policy_label": "threshold_policy",
        "source5_txrx45_near_tie_count_at_scale_0p5": 2,
        "source5_txrx45_near_tie_count_at_scale_1p0": 2,
    }
    matrix_summary = {
        "policy_label": "matrix_policy",
        "top_question_key": "target2_close14_source5_threshold_gate",
    }

    summary = summarize_contract(rows, threshold_summary, matrix_summary)

    assert summary["contract_status"] == "ready_but_not_launched"
    assert summary["existing_seed_values"] == "34"
    assert summary["missing_seed_values"] == "13,21"
    assert summary["source5_txrx45_near_tie_count_at_scale_0p5"] == 2
    assert summary["next_question_top"] == "target2_close14_source5_threshold_gate"
    assert summary["gpu_priority"] == "low_conditional_not_launched"
    assert "GPU <=90% and RAM <=80%" in summary["resource_policy"]

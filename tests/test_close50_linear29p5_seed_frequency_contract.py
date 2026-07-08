from run_close50_linear29p5_seed_frequency_contract import (
    command_for_seed,
    contract_rows,
    run_name_for_seed,
    summarize_contract,
    without_outdir,
)


def _base_manifest():
    return {
        "command": [
            "python",
            "run_multi_rebar_coordinate_optimizer.py",
            "--sources",
            "4",
            "--tx-rx-offset-mm",
            "29.5",
            "--receiver-sampling",
            "linear",
            "--replication-cases",
            "noise10_seed21:1.0,0.0,1.0,0.1,21",
            "--update-case-label",
            "source_mismatch_noise10_seed21",
            "--run-name",
            "coordinate_optimizer_close50_seed21_sources4_txrx29p5_linear_receiver_objectives",
            "--outdir",
            "outputs/experiments/1271_coordinate_optimizer_close50_seed21_sources4_txrx29p5_linear_receiver_objectives",
        ]
    }


def test_without_outdir_removes_split_and_equals_forms():
    assert without_outdir(["--run-name", "a", "--outdir", "old", "--sources", "4"]) == [
        "--run-name",
        "a",
        "--sources",
        "4",
    ]
    assert without_outdir(["--outdir=old", "--run-name", "a"]) == ["--run-name", "a"]


def test_command_for_seed_rewrites_close50_seed34_and_keeps_linear_receiver():
    command = command_for_seed(_base_manifest()["command"][1:], 34)
    command_text = " ".join(command)

    assert command[:5] == ["conda", "run", "-n", "gpr-fdtd-fwi", "python"]
    assert "--outdir" not in command
    assert "--receiver-sampling linear" in command_text
    assert "noise10_seed34" in command_text
    assert "source_mismatch_noise10_seed34" in command_text
    assert run_name_for_seed(34) in command_text
    assert "seed21" not in command_text


def test_contract_rows_marks_only_seed34_missing(tmp_path):
    for seed in (13, 21):
        (tmp_path / f"127{seed}_{run_name_for_seed(seed)}").mkdir()

    rows = contract_rows(_base_manifest(), tmp_path, seeds=(13, 21, 34))
    by_seed = {row["seed"]: row for row in rows}

    assert by_seed[13]["status"] == "existing"
    assert by_seed[21]["skip_existing"] is True
    assert by_seed[34]["status"] == "missing"
    assert by_seed[34]["skip_existing"] is False
    assert "seed34" in by_seed[34]["command_text"]


def test_summarize_contract_keeps_threshold_promotion_forbidden():
    rows = [
        {"seed": 13, "status": "existing"},
        {"seed": 21, "status": "existing"},
        {"seed": 34, "status": "missing"},
    ]
    sub30_summary = {
        "policy_label": "close50_linear_sub30_seed13_x_ambiguity_persists",
        "truth_geometry_row_count": 6,
        "strong_confidence_row_count": 6,
        "x_ambiguity_row_count": 2,
        "seed13_x_ambiguous_offsets_mm": "29.5,29.75",
    }
    matrix_summary = {
        "policy_label": "synthetic_2d_next_question_matrix_cpu_first_no_gpu",
        "top_question_key": "close50_sub30_seed_frequency_contract",
    }

    summary = summarize_contract(rows, sub30_summary, matrix_summary)

    assert summary["policy_label"] == "close50_linear29p5_seed_frequency_contract_skip_existing_cpu_no_gpu"
    assert summary["existing_seed_values"] == "13,21"
    assert summary["missing_seed_values"] == "34"
    assert summary["gpu_priority"] == "low_conditional_not_launched"
    assert "Run only the missing seed34 job" in summary["resource_policy"]
    assert "do not promote a clean sub-30 threshold" in summary["decision_rule"]

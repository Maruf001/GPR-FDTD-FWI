from pathlib import Path

from run_local_2d_baseline_comparison_contract import (
    build_contract_rows,
    summarize_contract,
    write_figure_notes,
)


def _claims():
    return [
        {
            "claim_area": "target2_close14_objective_limit",
            "allowed_claim": "close14 truth selected 6 / 6 with a +1 mm competitor.",
            "not_allowed": "Do not call close14 objective-unique.",
        },
        {
            "claim_area": "target2_close50_linear29p5_seed_frequency",
            "allowed_claim": "close50 29.5 mm exact and strong in 6 / 6 rows.",
            "not_allowed": "Do not promote 29.5 mm to clean replicated threshold.",
        },
    ]


def test_build_contract_rows_keeps_close_branch_contracts_cpu_first():
    rows = build_contract_rows(
        baseline_summary={
            "immediate_gpu_priority_count": 0,
            "conditional_gpu_candidate_count": 0,
            "decision": "baseline audit ready",
        },
        contribution_summary={
            "synthetic_immediate_gpu_priority_count": 0,
            "synthetic_conditional_gpu_candidate_count": 0,
            "recommended_framing": "controlled identifiability",
        },
        synthetic_claims=_claims(),
    )
    by_key = {row["contract_key"]: row for row in rows}

    assert len(rows) == 5
    assert by_key["target2_close14_same_case_detector_baseline"]["cpu_first"] is True
    assert by_key["target2_close14_same_case_detector_baseline"]["launch_now"] is False
    assert by_key["target2_close14_same_case_detector_baseline"]["gpu_allowed"] is False
    assert "+1 mm competitor" in by_key["target2_close14_same_case_detector_baseline"]["current_evidence"]
    assert by_key["target2_close50_linear29p5_same_case_detector_seed_frequency"]["cpu_first"] is True
    assert by_key["field_hyperbola_not_a_validation_baseline"]["cpu_first"] is False
    assert by_key["neural_network_baseline_deferred"]["gpu_allowed"] is False


def test_summarize_contract_reports_no_launch_or_gpu():
    rows = build_contract_rows(
        baseline_summary={
            "immediate_gpu_priority_count": 0,
            "conditional_gpu_candidate_count": 0,
            "decision": "baseline audit ready",
        },
        contribution_summary={
            "synthetic_immediate_gpu_priority_count": 0,
            "synthetic_conditional_gpu_candidate_count": 0,
            "recommended_framing": "controlled identifiability",
        },
        synthetic_claims=_claims(),
    )
    summary = summarize_contract(rows)

    assert summary["policy_label"] == "local_2d_baseline_comparison_contract_cpu_first_not_launched"
    assert summary["contract_row_count"] == 5
    assert summary["cpu_first_contract_count"] == 3
    assert summary["launch_now_count"] == 0
    assert summary["gpu_allowed_count"] == 0
    assert summary["gpu_priority"] == "none"
    assert summary["ready_for_future_baseline_runner_design"] is True


def test_write_figure_notes_documents_not_launched_scope(tmp_path):
    notes_path = tmp_path / "FIGURE_NOTES.md"
    summary = {
        "policy_label": "contract",
        "contract_row_count": 5,
        "cpu_first_contract_count": 3,
        "launch_now_count": 0,
        "gpu_allowed_count": 0,
        "highest_priority_contract": "target2_close14_same_case_detector_baseline",
    }

    write_figure_notes(
        notes_path,
        summary,
        Path("rows.csv"),
        Path("summary.json"),
        Path("validation.csv"),
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "local_2d_baseline_comparison_contract.png" in text
    assert "No detector" in text
    assert "3D/HPC" in text

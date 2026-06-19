from pathlib import Path

from run_local_2d_detector_handoff_budget import (
    best_case_count_by_rank,
    branch_best_case_count,
    build_handoff_rows,
    n_choose_k,
    summarize_handoff,
    write_figure_notes,
)


def _rank_summary():
    return {
        "case_count": 4,
        "minimal_rank_cap_for_full_case_recovery": 40,
        "best_case_count_by_rank_cap": {
            "top10": 2,
            "top20": 3,
            "top40": 4,
        },
    }


def _branch_rows():
    return [
        {"branch_key": "a", "best_top20_case_count": "2"},
        {"branch_key": "b", "best_top20_case_count": "2"},
    ]


def _assignment_summary():
    return {"best_unique_all_truth_case_count": 1}


def _oracle_summary():
    return {"oracle_all_truth_case_count": 3}


def _selector_summary():
    return {"best_in_sample_all_truth_case_count": 0}


def _image_gate_summary():
    return {"primary_objective_all_truth_case_count": 0}


def test_candidate_count_helpers():
    assert n_choose_k(10, 3) == 120
    assert n_choose_k(2, 3) == 0
    assert best_case_count_by_rank(_rank_summary(), 10) == 2
    assert branch_best_case_count(_branch_rows(), 20) == 4


def test_build_rows_compares_candidate_lists_and_selectors():
    rows = build_handoff_rows(
        rank_summary=_rank_summary(),
        branch_rank_rows=_branch_rows(),
        assignment_summary=_assignment_summary(),
        oracle_summary=_oracle_summary(),
        selector_summary=_selector_summary(),
        image_gate_summary=_image_gate_summary(),
    )
    by_key = {row["strategy_key"]: row for row in rows}

    assert len(rows) == 7
    assert by_key["branch_top20_candidate_list"]["all_truth_case_count"] == 4
    assert by_key["branch_top20_candidate_list"]["candidate_triples_per_case"] == 1140
    assert by_key["shared_top40_candidate_list"]["total_candidate_triples"] == 39520
    assert by_key["shared_blind_assignment"]["all_truth_case_count"] == 1
    assert by_key["per_case_policy_oracle"]["deployability"] == "per_case_oracle_not_deployable"


def test_summary_blocks_detector_seeded_fwi():
    rows = build_handoff_rows(
        rank_summary=_rank_summary(),
        branch_rank_rows=_branch_rows(),
        assignment_summary=_assignment_summary(),
        oracle_summary=_oracle_summary(),
        selector_summary=_selector_summary(),
        image_gate_summary=_image_gate_summary(),
    )

    summary = summarize_handoff(rows, _rank_summary(), _oracle_summary(), _image_gate_summary())

    assert summary["policy_label"] == "local_2d_detector_handoff_budget_cpu_no_fwi"
    assert summary["cheapest_full_candidate_strategy"] == "branch_top20_candidate_list"
    assert summary["cheapest_full_candidate_triples_per_case"] == 1140
    assert summary["best_deployable_strategy"] == "shared_blind_assignment"
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"


def test_write_figure_notes_documents_no_execution_scope(tmp_path):
    notes_path = tmp_path / "FIGURE_NOTES.md"
    summary = {
        "policy_label": "handoff_budget",
        "strategy_count": 7,
        "cheapest_full_candidate_strategy": "branch_top20_candidate_list",
        "cheapest_full_candidate_triples_per_case": 1140,
        "best_deployable_all_truth_case_count": 1,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }

    write_figure_notes(
        notes_path,
        summary,
        Path("rows.csv"),
        Path("summary.json"),
        Path("validation.csv"),
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "detector-to-FWI handoffs" in text
    assert "does not run" in text
    assert "3D/HPC" in text

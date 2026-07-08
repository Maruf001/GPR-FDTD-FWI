from pathlib import Path

from inversion.rebar_detection import RebarDetectionCandidate
from run_local_2d_detector_alltriples_gate_pilot import (
    build_case_objective_summary,
    build_objective_summary,
    candidate_rank_map,
    combo_truth_metrics,
    summarize,
    write_figure_notes,
)


def _candidate(x_mm, z_mm, score):
    return RebarDetectionCandidate(
        x_m=x_mm / 1000.0,
        z_m=z_mm / 1000.0,
        score=score,
        normalized_score=score,
        support_fraction=1.0,
        time_offset_s=0.0,
    )


def _combo_row(case, objective_scores, all_truth, hits=3):
    row = {
        "case_label": case,
        "branch_key": case.split("|")[0],
        "seed": "13",
        "case_variant": "nominal",
        "unique_all_truths_within_tolerance": all_truth,
        "unique_truth_hit_count": hits,
        "candidate_ranks": "1,2,3",
        "candidate_x_values_mm": "190,250,264",
    }
    for label, value in objective_scores.items():
        row[f"score_{label}"] = value
    return row


def test_candidate_rank_map_and_truth_metrics():
    candidates = [_candidate(190, 90, 1.0), _candidate(250, 90, 0.9), _candidate(264, 90, 0.8)]
    ranks = candidate_rank_map(candidates)
    metrics = combo_truth_metrics(tuple(candidates), [190, 250, 264], [90, 90, 90], 8.0)

    assert ranks[candidates[0]] == 1
    assert metrics["unique_all_truths_within_tolerance"] is True
    assert metrics["unique_truth_hit_count"] == 3


def test_case_and_objective_summary_rank_first_truth():
    rows = [
        _combo_row("branch|seed13|nominal", {"sum": 3.0, "span_bonus": 1.0, "min": 1.0, "min_span": 1.0, "balanced": 1.0, "mask": 1.0}, False, 2),
        _combo_row("branch|seed13|nominal", {"sum": 2.0, "span_bonus": 2.0, "min": 2.0, "min_span": 2.0, "balanced": 2.0, "mask": 2.0}, True, 3),
        _combo_row("branch|seed21|nominal", {"sum": 3.0, "span_bonus": 3.0, "min": 3.0, "min_span": 3.0, "balanced": 3.0, "mask": 3.0}, False, 1),
    ]

    case_rows = build_case_objective_summary(rows)
    objective_rows = build_objective_summary(case_rows)
    sum_row = next(row for row in objective_rows if row["objective_label"] == "sum")

    assert len(case_rows) == 12
    assert sum_row["top1_all_truth_case_count"] == 0
    assert sum_row["first_truth_top10_case_count"] == 1
    assert sum_row["first_truth_top50_case_count"] == 1


def test_summary_blocks_detector_seeded_fwi():
    rows = [
        _combo_row("branch|seed13|nominal", {"sum": 3.0, "span_bonus": 1.0, "min": 1.0, "min_span": 1.0, "balanced": 1.0, "mask": 1.0}, False, 2),
        _combo_row("branch|seed13|nominal", {"sum": 2.0, "span_bonus": 0.5, "min": 0.5, "min_span": 0.5, "balanced": 0.5, "mask": 0.5}, True, 3),
    ]
    case_rows = build_case_objective_summary(rows)
    objective_rows = build_objective_summary(case_rows)
    summary = summarize(rows, case_rows, objective_rows)

    assert summary["policy_label"] == "local_2d_detector_alltriples_gate_pilot_cpu_no_fwi"
    assert summary["best_top1_all_truth_case_count"] == 0
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"


def test_write_figure_notes_documents_scope(tmp_path):
    notes_path = tmp_path / "FIGURE_NOTES.md"
    summary = {
        "policy_label": "alltriples",
        "case_count": 12,
        "combo_row_count": 12180,
        "best_top1_all_truth_case_count": 0,
        "best_top10_objective": "span_bonus",
        "best_top10_case_count": 2,
        "best_top50_objective": "balanced",
        "best_top50_case_count": 8,
        "ready_for_detector_seeded_fwi": False,
    }

    write_figure_notes(
        notes_path,
        summary,
        Path("combo.csv"),
        Path("case.csv"),
        Path("objective.csv"),
        Path("summary.json"),
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "all detector candidate triples" in text
    assert "does not run" in text
    assert "3D/HPC" in text

from pathlib import Path

from run_target2_objective_margin_archive_audit import (
    margin_label,
    objective_margin_rows,
    summarize_margin_audit,
)


def test_margin_label_separates_geometry_and_zero_width_near_ties():
    assert margin_label({
        "geometry_ambiguous": True,
        "competitor_within_ambiguity_threshold": True,
        "ambiguity_candidate_count": 2,
    }) == "geometry_ambiguous_near_tie"
    assert margin_label({
        "geometry_ambiguous": False,
        "competitor_within_ambiguity_threshold": True,
        "ambiguity_candidate_count": 2,
    }) == "zero_width_objective_near_tie"
    assert margin_label({
        "geometry_ambiguous": False,
        "competitor_within_ambiguity_threshold": False,
        "ambiguity_candidate_count": 1,
    }) == "strict_location_clean_margin_separated"


def test_objective_margin_rows_filters_target2_exact_strong(tmp_path: Path):
    csv_path = tmp_path / "236_target2" / "data" / "coordinate_confidence_aggregate.csv"
    csv_path.parent.mkdir(parents=True)
    csv_path.write_text(
        "\n".join([
            "run_name,case_label,confidence_label,is_truth_geometry,step_target_index,best_misfit,competing_geometry_misfit,ambiguity_misfit_threshold,ambiguity_candidate_count,ambiguity_x_width_mm,ambiguity_z_width_mm,ambiguity_radius_width_mm",
            "run_a,noise10_seed21,strong,True,2,0.10,0.101,0.102,2,0,0,0",
            "run_b,noise10_seed21,strong,True,2,0.10,0.101,0.1005,1,0,0,0",
            "run_c,noise10_seed21,weak,True,2,0.10,0.101,0.102,2,1,0,0",
        ])
        + "\n",
        encoding="utf-8",
    )

    rows = objective_margin_rows([csv_path])

    assert len(rows) == 2
    assert {row["margin_label"] for row in rows} == {
        "zero_width_objective_near_tie",
        "strict_location_clean_margin_separated",
    }


def test_summarize_margin_audit_counts_reporting_tiers():
    rows = [
        {
            "strict_location_clean": False,
            "geometry_ambiguous": True,
            "margin_label": "geometry_ambiguous_near_tie",
            "competitor_within_ambiguity_threshold": True,
            "competitor_objective_gap_abs": 0.001,
        },
        {
            "strict_location_clean": True,
            "geometry_ambiguous": False,
            "margin_label": "zero_width_objective_near_tie",
            "competitor_within_ambiguity_threshold": True,
            "competitor_objective_gap_abs": 0.002,
        },
        {
            "strict_location_clean": True,
            "geometry_ambiguous": False,
            "margin_label": "strict_location_clean_margin_separated",
            "competitor_within_ambiguity_threshold": False,
            "competitor_objective_gap_abs": 0.003,
        },
    ]

    summary = summarize_margin_audit(rows)

    assert summary["policy_label"] == "target2_objective_margin_geometry_clean_but_near_ties_present_cpu_no_gpu"
    assert summary["row_count"] == 3
    assert summary["strict_location_clean_count"] == 2
    assert summary["geometry_ambiguous_count"] == 1
    assert summary["zero_width_objective_near_tie_count"] == 1
    assert summary["strict_location_clean_margin_separated_count"] == 1
    assert summary["gpu_priority"] == "none_now"

from pathlib import Path

from run_target2_archive_ambiguity_objective_diagnostic import (
    diagnostic_class,
    diagnostic_rows_from_aggregates,
    summarize_objective_diagnostic,
)


def test_diagnostic_class_marks_one_mm_lateral_near_tie():
    row = {
        "ambiguity_dimensions": "x",
        "x_ambiguity_width_mm": 1.0,
        "z_ambiguity_width_mm": 0.0,
        "radius_ambiguity_width_mm": 0.0,
        "competitor_delta_x_mm": -1.0,
        "competitor_delta_z_mm": 0.0,
        "competitor_delta_radius_mm": 0.0,
        "competitor_within_ambiguity_threshold": True,
    }

    assert diagnostic_class(row) == "one_mm_lateral_near_tie"


def test_diagnostic_class_marks_depth_radius_coupled_near_tie():
    row = {
        "ambiguity_dimensions": "z+radius",
        "x_ambiguity_width_mm": 0.0,
        "z_ambiguity_width_mm": 1.0,
        "radius_ambiguity_width_mm": 0.75,
        "competitor_delta_x_mm": 0.0,
        "competitor_delta_z_mm": -1.0,
        "competitor_delta_radius_mm": -0.75,
        "competitor_within_ambiguity_threshold": True,
    }

    assert diagnostic_class(row) == "depth_radius_coupled_near_tie"


def test_diagnostic_rows_from_aggregates_filters_target2_exact_strong(tmp_path: Path):
    csv_path = tmp_path / "249_target2" / "data" / "coordinate_confidence_aggregate.csv"
    csv_path.parent.mkdir(parents=True)
    csv_path.write_text(
        "\n".join([
            "run_name,case_label,confidence_label,is_truth_geometry,step_target_index,best_x_mm,best_z_mm,best_radius_mm,competing_geometry_x_mm,competing_geometry_z_mm,competing_geometry_radius_mm,best_misfit,competing_geometry_misfit,ambiguity_misfit_threshold,ambiguity_x_width_mm,ambiguity_z_width_mm,ambiguity_radius_width_mm",
            "run_a,noise10_seed34,strong,True,2,300,90,8,299,90,8,0.10,0.101,0.102,1,0,0",
            "run_b,noise10_seed34,weak,True,2,300,90,8,299,90,8,0.10,0.101,0.102,1,0,0",
            "run_c,noise10_seed34,strong,True,1,300,90,8,299,90,8,0.10,0.101,0.102,1,0,0",
        ])
        + "\n",
        encoding="utf-8",
    )

    rows = diagnostic_rows_from_aggregates([csv_path])

    assert len(rows) == 1
    assert rows[0]["target_index"] == 2
    assert rows[0]["diagnostic_class"] == "one_mm_lateral_near_tie"
    assert rows[0]["competitor_within_ambiguity_threshold"] is True


def test_summarize_objective_diagnostic_marks_cpu_no_gpu_near_ties():
    rows = [
        {
            "diagnostic_class": "one_mm_lateral_near_tie",
            "family_label": "target2_close50",
            "competitor_within_ambiguity_threshold": True,
            "competitor_objective_gap_abs": 0.001,
            "competitor_margin_inside_threshold_abs": 0.0002,
            "x_ambiguity_width_mm": 1.0,
            "z_ambiguity_width_mm": 0.0,
            "radius_ambiguity_width_mm": 0.0,
        },
        {
            "diagnostic_class": "depth_radius_coupled_near_tie",
            "family_label": "target2_variable_depth_radius",
            "competitor_within_ambiguity_threshold": True,
            "competitor_objective_gap_abs": 0.002,
            "competitor_margin_inside_threshold_abs": 0.0003,
            "x_ambiguity_width_mm": 0.0,
            "z_ambiguity_width_mm": 1.0,
            "radius_ambiguity_width_mm": 0.75,
        },
    ]

    summary = summarize_objective_diagnostic(rows)

    assert summary["policy_label"] == "target2_archive_ambiguity_near_tie_diagnostic_cpu_no_gpu"
    assert summary["row_count"] == 2
    assert summary["one_mm_lateral_near_tie_count"] == 1
    assert summary["depth_radius_coupled_near_tie_count"] == 1
    assert summary["gpu_priority"] == "none_now"

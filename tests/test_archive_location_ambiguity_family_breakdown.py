from run_archive_location_ambiguity_family_breakdown import (
    family_breakdown,
    family_label,
    normalize_ambiguous_rows,
    summarize_breakdown,
)


def test_family_label_recognizes_close_and_variable_depth_families():
    assert family_label({
        "target_index": "2",
        "aggregate_run": "356_coordinate_confidence_close14_seed34",
        "run_name": "coordinate_optimizer_close14_sources4",
    }) == "target2_close14"
    assert family_label({
        "target_index": "2",
        "aggregate_run": "480_variable_depth_radius_seed55",
        "run_name": "coordinate_optimizer_variable_depth_radius_seed55_target2_xzr_coupled",
    }) == "target2_variable_depth_radius"


def test_normalize_ambiguous_rows_filters_to_exact_strong_ambiguity():
    rows = normalize_ambiguous_rows([
        {
            "aggregate_run": "260_coordinate_confidence_aggregate_close50",
            "run_name": "coordinate_optimizer_variable_radius_target2_close50_seed34_sources7",
            "case_label": "noise10_seed34",
            "target_index": "2",
            "sources": "7",
            "tx_rx_offset_mm": "",
            "confidence_label": "strong",
            "truth_geometry_match": "True",
            "strong_confidence": "True",
            "x_ambiguity_width_mm": "1",
            "z_ambiguity_width_mm": "0",
            "radius_ambiguity_width_mm": "0",
        },
        {
            "aggregate_run": "260_coordinate_confidence_aggregate_close50",
            "run_name": "coordinate_optimizer_variable_radius_target2_close50_seed34_sources7",
            "case_label": "noise10_seed34",
            "target_index": "2",
            "confidence_label": "weak",
            "truth_geometry_match": "True",
            "strong_confidence": "False",
            "x_ambiguity_width_mm": "1",
        },
    ])

    assert len(rows) == 1
    assert rows[0]["family_label"] == "target2_close50"
    assert rows[0]["ambiguity_dimensions"] == "x"
    assert rows[0]["publication_action"] == "exclude_from_strict_location_clean_threshold"


def test_family_breakdown_and_summary_mark_target2_cpu_no_gpu():
    rows = normalize_ambiguous_rows([
        {
            "aggregate_run": "356_coordinate_confidence_close14_seed34",
            "run_name": "coordinate_optimizer_close14_sources4",
            "case_label": "noise15p361328125_seed34",
            "target_index": "2",
            "sources": "4",
            "tx_rx_offset_mm": "45",
            "truth_geometry_match": "True",
            "strong_confidence": "True",
            "x_ambiguity_width_mm": "1",
            "z_ambiguity_width_mm": "0",
            "radius_ambiguity_width_mm": "0",
        },
        {
            "aggregate_run": "480_variable_depth_radius_seed55",
            "run_name": "coordinate_optimizer_variable_depth_radius_seed55_target2_xzr_coupled",
            "case_label": "source_mismatch_noise10_seed55",
            "target_index": "2",
            "sources": "5",
            "tx_rx_offset_mm": "20",
            "truth_geometry_match": "True",
            "strong_confidence": "True",
            "x_ambiguity_width_mm": "0",
            "z_ambiguity_width_mm": "1",
            "radius_ambiguity_width_mm": "0.75",
        },
    ])
    family_rows = family_breakdown(rows)
    summary = summarize_breakdown(rows, family_rows, total_input_rows=10)

    assert summary["policy_label"] == "archive_location_ambiguity_target2_family_breakdown_cpu_no_gpu"
    assert summary["exact_strong_ambiguous_row_count"] == 2
    assert summary["family_count"] == 2
    assert summary["x_ambiguous_row_count"] == 1
    assert summary["z_ambiguous_row_count"] == 1
    assert summary["radius_ambiguous_row_count"] == 1
    assert summary["gpu_priority"] == "none_now"
    assert family_rows[0]["reporting_action"] == "treat_as_archive_ambiguity_caveat_not_clean_threshold"

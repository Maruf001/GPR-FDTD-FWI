from run_close50_x_ambiguity_metric_design import metric_rows, summarize_metric


def test_metric_rows_separates_exact_strong_location_clean_from_x_ambiguous():
    rows = metric_rows([
        {
            "seed_label": "seed21",
            "case_label": "noise10_seed21",
            "tx_rx_offset_mm": "29.5",
            "truth_geometry_match": "True",
            "strong_confidence": "True",
            "x_ambiguity_width_mm": "0",
            "radius_ambiguity_width_mm": "0",
            "radius_margin_abs": "0.001",
        },
        {
            "seed_label": "seed13",
            "case_label": "noise10_seed13",
            "tx_rx_offset_mm": "29.5",
            "truth_geometry_match": "True",
            "strong_confidence": "True",
            "x_ambiguity_width_mm": "1",
            "radius_ambiguity_width_mm": "0",
            "radius_margin_abs": "0.002",
        },
    ])

    assert rows[0]["ambiguity_metric_label"] == "exact_strong_location_clean"
    assert rows[0]["paper_clean_candidate"] is True
    assert rows[1]["ambiguity_metric_label"] == "exact_strong_x_ambiguous"
    assert rows[1]["paper_clean_candidate"] is False


def test_summarize_metric_marks_x_ambiguity_reporting_ready_without_gpu():
    rows = [
        {
            "truth_geometry_match": True,
            "strong_confidence": True,
            "paper_clean_candidate": True,
            "x_ambiguity_width_mm": 0.0,
            "radius_ambiguity_width_mm": 0.0,
            "case_label": "source_mismatch_noise10_seed21",
        },
        {
            "truth_geometry_match": True,
            "strong_confidence": True,
            "paper_clean_candidate": False,
            "x_ambiguity_width_mm": 1.0,
            "radius_ambiguity_width_mm": 0.0,
            "case_label": "noise10_seed13",
        },
    ]

    summary = summarize_metric(rows)

    assert summary["policy_label"] == "close50_sub30_x_ambiguity_reporting_metric_ready_cpu_no_gpu"
    assert summary["x_ambiguous_row_count"] == 1
    assert summary["radius_ambiguous_row_count"] == 0
    assert summary["nominal_x_ambiguous_row_count"] == 1
    assert summary["source_mismatch_x_ambiguous_row_count"] == 0
    assert summary["gpu_priority"] == "none_now"
    assert "x_ambiguity_width_mm == 0" in summary["recommended_reporting_metric"]


def test_summarize_metric_marks_clean_when_all_rows_are_location_clean():
    rows = [
        {
            "truth_geometry_match": True,
            "strong_confidence": True,
            "paper_clean_candidate": True,
            "x_ambiguity_width_mm": 0.0,
            "radius_ambiguity_width_mm": 0.0,
            "case_label": "noise10_seed21",
        }
    ]

    summary = summarize_metric(rows)

    assert summary["policy_label"] == "close50_sub30_location_clean_under_reporting_metric"

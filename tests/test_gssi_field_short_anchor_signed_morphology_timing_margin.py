from run_gssi_field_short_anchor_signed_morphology_timing_margin import (
    build_gate_rows,
    build_timing_margin_rows,
    summarize_timing_margin,
)


def _signed_rows():
    return [
        {
            "pair_index": "2",
            "reference_file": "a.DZT",
            "comparison_file": "b.DZT",
            "corrected_abs_timing_residual_ns": "0.01964636542239684",
            "signed_morphology_supported": "True",
        },
        {
            "pair_index": "3",
            "reference_file": "a.DZT",
            "comparison_file": "b.DZT",
            "corrected_abs_timing_residual_ns": "0.0",
            "signed_morphology_supported": "True",
        },
    ]


def _ladder_summary():
    return {
        "policy_label": "ladder",
        "content_only_offset_half_range_ns": 0.00982318271119842,
        "short_conservative_half_width_ns": 0.058939096267190516,
    }


def test_timing_margin_rows_compare_default_and_moderate_slack_to_ladder_uncertainty():
    rows = build_timing_margin_rows(_signed_rows(), _ladder_summary())
    by_pair = {row["pair_index"]: row for row in rows}

    assert by_pair[2]["default_timing_slack_ns"] == 0.05 - 0.01964636542239684
    assert by_pair[2]["default_slack_covers_content_uncertainty"]
    assert not by_pair[2]["default_slack_covers_conservative_uncertainty"]
    assert not by_pair[2]["moderate_slack_covers_content_uncertainty"]
    assert by_pair[3]["moderate_slack_covers_content_uncertainty"]


def test_timing_margin_summary_supports_content_only_qc_but_blocks_conservative_timing_and_fwi():
    rows = build_timing_margin_rows(_signed_rows(), _ladder_summary())
    summary = summarize_timing_margin(
        rows,
        _ladder_summary(),
        {"policy_label": "signed"},
        {"policy_label": "sensitivity", "support_limit_timing_cap_ns": 0.01964636542239684},
    )
    gates = {row["gate_key"]: row for row in build_gate_rows(summary)}

    assert summary["policy_label"] == "gssi51600s_field_short_anchor_signed_morphology_timing_margin_qc_only"
    assert summary["content_pair_count"] == 2
    assert summary["signed_morphology_supported_pair_count"] == 2
    assert summary["min_default_timing_slack_ns"] == 0.05 - 0.01964636542239684
    assert summary["content_only_offset_half_range_ns"] == 0.00982318271119842
    assert summary["short_conservative_half_width_ns"] == 0.058939096267190516
    assert summary["default_slack_content_covered_pair_count"] == 2
    assert summary["default_slack_conservative_covered_pair_count"] == 0
    assert summary["moderate_slack_content_covered_pair_count"] == 1
    assert summary["ready_for_content_only_morphology_timing_qc"]
    assert not summary["ready_for_conservative_timing_morphology_claim"]
    assert not summary["ready_for_moderate_timing_morphology_margin"]
    assert not summary["ready_for_absolute_time_zero"]
    assert not summary["ready_for_field_fwi"]
    assert gates["content_only_morphology_timing_qc"]["ready"]
    assert not gates["conservative_timing_morphology_claim"]["ready"]
    assert not gates["field_fwi"]["ready"]

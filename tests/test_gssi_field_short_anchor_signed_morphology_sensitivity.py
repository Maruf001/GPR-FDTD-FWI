import pytest

from run_gssi_field_short_anchor_signed_morphology_sensitivity import (
    DEFAULT_CORRECTED_SIGNED_THRESHOLDS,
    DEFAULT_EVENT_LOCAL_THRESHOLDS,
    DEFAULT_IMPROVEMENT_THRESHOLDS,
    DEFAULT_TIMING_CAPS_NS,
    build_gate_rows,
    build_threshold_rows,
    parse_thresholds,
    summarize_sensitivity,
)


def _signed_rows():
    return [
        {
            "pair_index": "2",
            "corrected_signed_correlation": "0.9394685644349674",
            "event_local_field_trace_abs_correlation": "0.988858176059292",
            "field_trace_abs_correlation_improvement": "0.5856373978215583",
            "corrected_abs_timing_residual_ns": "0.01964636542239684",
        },
        {
            "pair_index": "3",
            "corrected_signed_correlation": "0.9881379963559919",
            "event_local_field_trace_abs_correlation": "0.9881379963559919",
            "field_trace_abs_correlation_improvement": "0.7393017130535231",
            "corrected_abs_timing_residual_ns": "0.0",
        },
    ]


def _default_threshold_rows():
    return build_threshold_rows(
        _signed_rows(),
        parse_thresholds(DEFAULT_CORRECTED_SIGNED_THRESHOLDS),
        parse_thresholds(DEFAULT_EVENT_LOCAL_THRESHOLDS),
        parse_thresholds(DEFAULT_IMPROVEMENT_THRESHOLDS),
        parse_thresholds(DEFAULT_TIMING_CAPS_NS),
    )


def test_parse_thresholds_sorts_deduplicates_and_rejects_invalid_values():
    assert parse_thresholds("0.95,0.90,0.95") == [0.90, 0.95]
    with pytest.raises(ValueError):
        parse_thresholds("0.95,0")
    with pytest.raises(ValueError):
        parse_thresholds("")


def test_threshold_grid_identifies_supported_and_binding_failure_regions():
    rows = _default_threshold_rows()
    supported = [row for row in rows if row["all_pairs_supported"]]
    failed = [row for row in rows if not row["all_pairs_supported"]]

    assert len(rows) == 320
    assert len(supported) == 36
    assert any("corrected_signed_correlation" in row["binding_failure_metrics"] for row in failed)
    assert any("abs_correlation_improvement" in row["binding_failure_metrics"] for row in failed)
    assert any("timing_residual" in row["binding_failure_metrics"] for row in failed)


def test_summary_keeps_moderate_morphology_qc_but_blocks_strict_claims_and_fwi():
    rows = _default_threshold_rows()
    summary = summarize_sensitivity(
        _signed_rows(),
        rows,
        {"policy_label": "signed_morphology"},
    )
    gates = {row["gate_key"]: row for row in build_gate_rows(summary)}

    assert summary["policy_label"] == (
        "gssi51600s_field_short_anchor_signed_morphology_threshold_sensitivity_qc_only"
    )
    assert summary["content_pair_count"] == 2
    assert summary["threshold_combo_count"] == 320
    assert summary["all_pairs_supported_threshold_combo_count"] == 36
    assert summary["default_thresholds_supported"]
    assert summary["moderate_tightening_supported"]
    assert not summary["strict_correlation_supported"]
    assert not summary["strict_all_supported"]
    assert summary["ready_for_moderate_threshold_morphology_qc"]
    assert not summary["ready_for_strict_morphology_claim"]
    assert not summary["ready_for_field_fwi"]
    assert summary["gpu_priority"] == "none"
    assert gates["moderate_threshold_morphology_qc"]["ready"]
    assert not gates["strict_morphology_claim"]["ready"]
    assert not gates["field_fwi"]["ready"]

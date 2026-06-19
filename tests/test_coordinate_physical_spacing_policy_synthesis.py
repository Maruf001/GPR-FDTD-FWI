from run_coordinate_physical_spacing_policy_synthesis import (
    add_physical_columns,
    physical_regime,
    summarize_physical_policy,
)


def test_physical_regime_classifies_overlap_tangent_and_separated():
    assert physical_regime(-2.0) == "overlap_stress_test"
    assert physical_regime(0.0) == "tangent_nonoverlap_limit"
    assert physical_regime(5.0) == "separated_nonoverlap"


def test_physical_summary_keeps_overlap_out_of_physical_limit():
    rows = add_physical_columns(
        [
            {"close_spacing_mm": 10.0, "tx_rx_offset_mm": 50.0, "policy_label": "clean_replicated"},
            {"close_spacing_mm": 14.0, "tx_rx_offset_mm": 50.0, "policy_label": "clean_replicated"},
            {"close_spacing_mm": 30.0, "tx_rx_offset_mm": 35.0, "policy_label": "clean_replicated"},
        ],
        target_radius_pair_sum_mm=14.0,
    )

    summary = summarize_physical_policy(rows)
    by_txrx = {row["tx_rx_offset_mm"]: row for row in summary["tx_rx_policy_rows"]}

    assert by_txrx[50.0]["closest_clean_physical_spacing_mm"] == 14.0
    assert by_txrx[50.0]["clean_overlap_stress_spacings_mm"] == "10"
    assert summary["clean_overlap_stress_group_count"] == 1
    assert "close10 and close12" in summary["decision"]

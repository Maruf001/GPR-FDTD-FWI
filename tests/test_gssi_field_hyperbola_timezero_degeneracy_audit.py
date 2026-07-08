from run_gssi_field_hyperbola_timezero_degeneracy_audit import (
    build_degeneracy_rows,
    near_top_rows,
    summarize_degeneracy,
    summarize_offset_rows,
)


def test_near_top_rows_use_fractional_score_drop():
    rows = [
        {"profile_score": "100.0"},
        {"profile_score": "99.2"},
        {"profile_score": "98.9"},
    ]

    near = near_top_rows(rows, fractional_drop=0.01)

    assert len(near) == 2


def test_summarize_offset_rows_records_multiple_plausible_offsets():
    rows = [
        {"file": "A.DZT", "tx_rx_offset_mm": "0", "epsr": "2", "time_zero_ns": "0", "median_depth_m": "0.10", "profile_score": "10.0"},
        {"file": "A.DZT", "tx_rx_offset_mm": "20", "epsr": "3", "time_zero_ns": "0.1", "median_depth_m": "0.08", "profile_score": "9.7"},
        {"file": "A.DZT", "tx_rx_offset_mm": "40", "epsr": "5", "time_zero_ns": "0.2", "median_depth_m": "0.04", "profile_score": "8.0"},
    ]

    out = summarize_offset_rows(rows, fractional_drop=0.05)

    assert out[0]["near_top_offset_count"] == 2
    assert out[0]["near_top_offsets_mm"] == "0;20"
    assert out[0]["near_top_offset_span_mm"] == 20.0
    assert out[0]["claim_status"] == "txrx_offset_score_ambiguous_not_calibrated_geometry"


def test_build_degeneracy_rows_summarizes_surfaces_and_boundaries():
    hyperbola_surface = [
        {"file": "A.DZT", "profile_score": "10.0", "epsr": "2", "velocity_m_per_ns": "0.2", "time_zero_ns": "0.0"},
        {"file": "A.DZT", "profile_score": "9.95", "epsr": "4", "velocity_m_per_ns": "0.1", "time_zero_ns": "0.1"},
    ]
    hyperbola_summary = [
        {
            "file": "A.DZT",
            "best_epsr": "2",
            "best_velocity_m_per_ns": "0.2",
            "best_time_zero_ns": "0.0",
            "score_margin_vs_p95": "0.01",
            "best_on_grid_boundary": "True",
        }
    ]
    common_surface = [
        {
            "file": "A.DZT",
            "tx_rx_offset_mm": "0",
            "profile_score": "8.0",
            "epsr": "2",
            "velocity_m_per_ns": "0.2",
            "time_zero_ns": "0.0",
            "median_depth_m": "0.1",
        },
        {
            "file": "A.DZT",
            "tx_rx_offset_mm": "20",
            "profile_score": "7.96",
            "epsr": "5",
            "velocity_m_per_ns": "0.1",
            "time_zero_ns": "0.2",
            "median_depth_m": "0.2",
        },
    ]
    common_profile = [
        {
            "file": "A.DZT",
            "epsr": "2",
            "velocity_m_per_ns": "0.2",
            "time_zero_ns": "0.0",
            "tx_rx_offset_mm": "0",
            "best_on_grid_boundary": "False",
        }
    ]
    offset_rows = [
        {"file": "A.DZT", "tx_rx_offset_mm": "0", "epsr": "2", "time_zero_ns": "0", "median_depth_m": "0.10", "profile_score": "10.0"},
    ]

    degeneracy_rows, offset_summary = build_degeneracy_rows(
        hyperbola_surface,
        hyperbola_summary,
        common_surface,
        common_profile,
        offset_rows,
    )
    summary = summarize_degeneracy(degeneracy_rows, offset_summary)

    assert len(degeneracy_rows) == 2
    assert degeneracy_rows[0]["best_on_grid_boundary"] is True
    assert summary["boundary_best_surface_count"] == 1
    assert summary["cover_depth_claim_ready"] is False
    assert summary["radius_claim_ready"] is False
    assert summary["field_fwi_ready"] is False
    assert summary["gpu_priority"] == "none"

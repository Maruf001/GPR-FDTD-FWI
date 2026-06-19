from pathlib import Path

from run_coordinate_resolution_policy_synthesis import (
    derive_policy_summary,
    load_policy_groups,
    parse_close_spacing_mm,
    policy_label_for_counts,
    row_clean,
    summarize_group,
)


def base_row(**overrides):
    row = {
        "sources": "4",
        "tx_rx_offset_mm": "35",
        "is_truth_geometry": "True",
        "confidence_label": "strong",
        "radius_margin_abs": "0.001",
        "ambiguity_x_width_mm": "0",
        "ambiguity_z_width_mm": "0",
        "ambiguity_radius_width_mm": "0",
    }
    row.update(overrides)
    return row


def test_parse_close_spacing_from_aggregate_name():
    assert parse_close_spacing_mm("305_coordinate_confidence_close30_sources4_txrx35_seed_replicates") == 30.0
    assert parse_close_spacing_mm("noise_close14p5_case") == 14.5
    assert parse_close_spacing_mm("no_spacing") is None


def test_row_clean_requires_truth_label_and_zero_ambiguity():
    assert row_clean(base_row()) is True
    assert row_clean(base_row(confidence_label="weak")) is False
    assert row_clean(base_row(is_truth_geometry="False")) is False
    assert row_clean(base_row(ambiguity_x_width_mm="1.0")) is False


def test_policy_label_for_counts():
    assert policy_label_for_counts(row_count=6, clean_count=6, truth_count=6) == "clean_replicated"
    assert policy_label_for_counts(row_count=6, clean_count=4, truth_count=6) == "truth_selected_interval"
    assert policy_label_for_counts(row_count=6, clean_count=3, truth_count=4) == "mixed_or_failed"


def test_summarize_group_classifies_interval_when_truth_but_weak(tmp_path):
    rows = [
        base_row(confidence_label="strong", radius_margin_abs="0.002"),
        base_row(confidence_label="weak", radius_margin_abs="0.0001"),
    ]
    summary = summarize_group(
        rows,
        tmp_path / "314_coordinate_confidence_close28_sources4_txrx35_seed_replicates" / "data" / "coordinate_confidence_aggregate.csv",
        close_spacing_mm=28.0,
        sources=4.0,
        tx_rx_offset_mm=35.0,
    )

    assert summary["row_count"] == 2
    assert summary["truth_geometry_count"] == 2
    assert summary["clean_row_count"] == 1
    assert summary["policy_label"] == "truth_selected_interval"
    assert summary["radius_margin_abs_min"] == 0.0001


def test_load_policy_groups_splits_multi_offset_aggregate(tmp_path):
    folder = tmp_path / "1222_coordinate_confidence_close50_sources4_txrx25_30_seed_replicates" / "data"
    folder.mkdir(parents=True)
    csv_path = folder / "coordinate_confidence_aggregate.csv"
    csv_path.write_text(
        "sources,tx_rx_offset_mm,is_truth_geometry,confidence_label,radius_margin_abs,"
        "ambiguity_x_width_mm,ambiguity_z_width_mm,ambiguity_radius_width_mm\n"
        "4,25,False,weak,0.0001,1,0,0.5\n"
        "4,30,True,strong,0.002,0,0,0\n",
        encoding="utf-8",
    )

    groups = load_policy_groups([csv_path])

    assert len(groups) == 2
    assert [group["tx_rx_offset_mm"] for group in groups] == [25.0, 30.0]
    assert groups[0]["policy_label"] == "mixed_or_failed"
    assert groups[1]["policy_label"] == "clean_replicated"


def test_derive_policy_summary_reports_clean_limits():
    rows = [
        {
            "close_spacing_mm": 50.0,
            "tx_rx_offset_mm": 35.0,
            "policy_label": "clean_replicated",
            "radius_margin_abs_min": 0.004,
        },
        {
            "close_spacing_mm": 30.0,
            "tx_rx_offset_mm": 35.0,
            "policy_label": "clean_replicated",
            "radius_margin_abs_min": 0.001,
        },
        {
            "close_spacing_mm": 28.0,
            "tx_rx_offset_mm": 35.0,
            "policy_label": "truth_selected_interval",
            "radius_margin_abs_min": 0.0004,
        },
        {
            "close_spacing_mm": 14.0,
            "tx_rx_offset_mm": 45.0,
            "policy_label": "clean_replicated",
            "radius_margin_abs_min": 0.002,
        },
        {
            "close_spacing_mm": 10.0,
            "tx_rx_offset_mm": 50.0,
            "policy_label": "clean_replicated",
            "radius_margin_abs_min": 0.0015,
        },
    ]

    summary = derive_policy_summary(rows)

    assert summary["standard_35mm_closest_clean_spacing_mm"] == 30.0
    assert summary["extended_45mm_closest_clean_spacing_mm"] == 14.0
    assert summary["extended_50mm_closest_clean_spacing_mm"] == 10.0
    assert summary["close28_txrx35_policy_label"] == "truth_selected_interval"
    assert "50 mm Tx/Rx reaches close10" in summary["decision"]
    assert "overlapping-cylinder algorithmic stress test" in summary["decision"]

from pathlib import Path

from run_close14_noise_policy_synthesis import (
    derive_summary,
    parse_noise_percent,
    summarize_aggregate_csv,
)


def test_parse_noise_percent_handles_decimal_p_encoding():
    assert parse_noise_percent("noise19p642333984375_seed34") == 19.642333984375
    assert parse_noise_percent("coordinate_optimizer_close14_noise15_seed13") == 15.0
    assert parse_noise_percent("no_noise_token") is None


def test_summarize_aggregate_csv_classifies_clean_replicated(tmp_path):
    folder = tmp_path / "335_coordinate_confidence_close14_sources4_txrx45_seed_replicates" / "data"
    folder.mkdir(parents=True)
    csv_path = folder / "coordinate_confidence_aggregate.csv"
    csv_path.write_text(
        "run_name,case_label,sources,tx_rx_offset_mm,is_truth_geometry,confidence_label,"
        "radius_margin_abs,ambiguity_x_width_mm,ambiguity_z_width_mm,ambiguity_radius_width_mm\n"
        "r1,noise10_seed34,4,45,True,strong,0.002,0,0,0\n"
        "r1,source_mismatch_noise10_seed34,4,45,True,strong,0.004,0,0,0\n"
        "r2,noise10_seed13,4,45,True,strong,0.003,0,0,0\n"
        "r2,source_mismatch_noise10_seed13,4,45,True,strong,0.005,0,0,0\n"
        "r3,noise10_seed21,4,45,True,strong,0.0025,0,0,0\n"
        "r3,source_mismatch_noise10_seed21,4,45,True,strong,0.0045,0,0,0\n",
        encoding="utf-8",
    )

    row = summarize_aggregate_csv(csv_path)

    assert row["output_id"] == 335
    assert row["noise_rms_percent"] == 10.0
    assert row["seed_count"] == 3
    assert row["is_seed_replicated"] is True
    assert row["policy_label"] == "clean_replicated"
    assert row["radius_margin_abs_min"] == 0.002


def test_summarize_aggregate_csv_marks_interval_when_truth_is_ambiguous(tmp_path):
    folder = tmp_path / "x" / "data"
    folder.mkdir(parents=True)
    csv_path = folder / "coordinate_confidence_aggregate.csv"
    csv_path.write_text(
        "run_name,case_label,sources,tx_rx_offset_mm,is_truth_geometry,confidence_label,"
        "radius_margin_abs,ambiguity_x_width_mm,ambiguity_z_width_mm,ambiguity_radius_width_mm\n"
        "r1,noise15_seed34,4,50,True,strong,0.002,1,0,0\n"
        "r2,noise15_seed13,4,50,True,strong,0.003,0,0,0\n",
        encoding="utf-8",
    )

    row = summarize_aggregate_csv(csv_path)

    assert row["clean_row_count"] == 1
    assert row["truth_geometry_count"] == 2
    assert row["x_ambiguity_row_count"] == 1
    assert row["policy_label"] == "truth_selected_interval"


def test_derive_summary_reports_txrx_limits():
    rows = [
        {
            "tx_rx_offset_mm": "45",
            "noise_rms_percent": 15.3125,
            "policy_label": "clean_replicated",
            "is_seed_replicated": True,
            "radius_margin_abs_min": 0.002,
        },
        {
            "tx_rx_offset_mm": "50",
            "noise_rms_percent": 19.642333984375,
            "policy_label": "clean_replicated",
            "is_seed_replicated": True,
            "radius_margin_abs_min": 0.0019,
        },
        {
            "tx_rx_offset_mm": "50",
            "noise_rms_percent": 19.7,
            "policy_label": "truth_selected_interval",
            "is_seed_replicated": True,
            "radius_margin_abs_min": 0.0018,
        },
    ]
    boundary = {
        "final_ambiguous_upper_noise_rms_percent": 19.642372131347656,
        "final_bracket_width_percent_rms": 0.00003814697265625,
    }

    summary = derive_summary(rows, boundary)

    assert summary["txrx45_replicated_clean_noise_rms_percent"] == 15.3125
    assert summary["txrx50_replicated_clean_noise_rms_percent"] == 19.642333984375
    assert summary["txrx50_single_seed_ambiguous_upper_noise_rms_percent"] == 19.642372131347656
    assert "19.6423339844" in summary["decision"]

from pathlib import Path

from run_local_gssi_field_dataset_card import (
    profile_role,
    profile_rows,
    summarize_card,
    write_figure_notes,
)


def _inventory_rows():
    return [
        {
            "file": "PROJECT001C__013.DZT",
            "traces": "807",
            "samples": "510",
            "scan_spacing_m": "0.003333",
            "profile_length_m": "2.686398",
            "time_range_ns": "5.0",
            "dielectric": "2.25",
            "antenna_name": "51600S",
            "antenna_frequency_mhz": "1600.0",
            "depth_from_time_m": "0.499654",
            "dzx_present": "True",
            "amplitude_std": "2428888.5",
        },
        {
            "file": "PROJECT001C__014.DZT",
            "traces": "274",
            "samples": "510",
            "scan_spacing_m": "0.003333",
            "profile_length_m": "0.909909",
            "time_range_ns": "5.0",
            "dielectric": "2.25",
            "antenna_name": "51600S",
            "antenna_frequency_mhz": "1600.0",
            "depth_from_time_m": "0.499654",
            "dzx_present": "True",
            "amplitude_std": "1762020.9",
        },
    ]


def test_profile_role_uses_known_profile_pair_ids():
    assert profile_role({"file": "PROJECT001C__014.DZT", "traces": "274"}) == (
        "short_repeat_pair_014_016"
    )
    assert profile_role({"file": "PROJECT001C__015.DZT", "traces": "814"}) == (
        "long_pattern_pair_015_013"
    )
    assert profile_role({"file": "unknown.DZT", "traces": "200"}) == "short_profile"


def test_profile_rows_convert_inventory_for_methods_table():
    rows = profile_rows(_inventory_rows())

    assert rows[0]["profile_role"] == "long_pattern_pair_015_013"
    assert rows[0]["scan_spacing_mm"] == 3.333
    assert rows[1]["profile_role"] == "short_repeat_pair_014_016"
    assert rows[1]["traces"] == 274


def test_summarize_card_keeps_dataset_2d_not_fwi():
    rows = profile_rows(_inventory_rows())
    summary = summarize_card(
        rows,
        dzt_summary={"dataset_id": "dataset", "input_dir": "input", "dzt_file_count": 2},
        survey_summary={
            "classification": "independent_2d_line_profiles",
            "trace_derived_total_length_m": 3.596307,
            "no_dzg_file": True,
            "has_crossline_file": False,
        },
        acquisition_summary={
            "ready_for_2d_qc": True,
            "ready_for_3d_hpc": False,
            "ready_for_field_fwi": False,
            "field_hpc_priority": "none",
            "scan_spacing_mm": 3.333,
            "antenna_frequency_mhz": 1600.0,
            "dielectric": 2.25,
            "center_wavelength_mm": 124.9135,
            "samples_per_wavelength": 37.4778,
            "nominal_depth_window_mm": 499.654,
        },
        timing_window_summary={
            "short_nonraw_supported_count": 18,
            "short_nonraw_row_count": 18,
            "long_reject_short_transfer_row_count": 3,
            "long_row_count": 3,
            "absolute_time_zero_ready": False,
            "field_fwi_ready": False,
        },
        field_bundle_summary={"figure_row_count": 20, "claim_boundary_count": 19},
    )

    assert summary["policy_label"] == "local_gssi_field_dataset_card_2d_qc_ready_not_3d_fwi"
    assert summary["profile_count"] == 2
    assert summary["trace_count_total"] == 1081
    assert summary["survey_classification"] == "independent_2d_line_profiles"
    assert summary["ready_for_2d_qc"] is True
    assert summary["ready_for_3d_hpc"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["ready_for_methods_data_card"] is True


def test_write_figure_notes_documents_methods_scope(tmp_path):
    notes_path = tmp_path / "FIGURE_NOTES.md"
    summary = {
        "policy_label": "dataset_card",
        "profile_count": 4,
        "total_trace_derived_length_m": 7.215945,
        "scan_spacing_mm": 3.333,
        "survey_classification": "independent_2d_line_profiles",
        "ready_for_3d_hpc": False,
        "ready_for_field_fwi": False,
    }

    write_figure_notes(
        notes_path,
        summary,
        Path("profiles.csv"),
        Path("summary.json"),
        Path("validation.csv"),
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "local_gssi_field_dataset_card.png" in text
    assert "independent_2d_line_profiles" in text
    assert "does not create 3D" in text

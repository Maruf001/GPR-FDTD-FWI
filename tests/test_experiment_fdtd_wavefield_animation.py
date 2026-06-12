import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_experiment_fdtd_wavefield_animation import (  # noqa: E402
    compact_animation_title,
    geometry_arrays_from_summary,
    representative_pair_from_summary,
    select_replication_case,
    source_receiver_indices_for_pair,
)


def _summary():
    return {
        "run_name": "fdtd_context_demo",
        "grid_step_mm": 1.0,
        "frequency_ghz": 1.5,
        "sources": 5,
        "tx_rx_offset_mm": 60.0,
        "scan_x_values_mm": [50.0, 146.0, 250.0, 346.0, 450.0],
        "true_x_values_mm": [150.0, 250.0, 350.0],
        "true_z_values_mm": [80.0, 100.0, 120.0],
        "truth_radius_values_mm": [5.0, 6.0, 8.0],
        "target_indices": [2],
        "final_state": {
            "x_values_mm": [150.0, 250.0, 350.0],
            "z_values_mm": [80.0, 100.0, 120.0],
            "radii_mm": [5.0, 6.0, 8.0],
        },
        "replication_cases": [
            {
                "label": "source_mismatch_ringdown050_noise10_seed13",
                "frequency_scale": 1.1,
                "time_shift_ps": -50.0,
                "amplitude_scale": 1.1,
                "noise_fraction": 0.1,
                "noise_seed": 13,
                "ringdown_scale": 0.5,
                "ringdown_delay_ps": 180.0,
                "ringdown_frequency_scale": 0.8,
            }
        ],
    }


def test_geometry_arrays_from_summary_truth_and_final():
    truth = geometry_arrays_from_summary(_summary(), model_state="truth")
    final = geometry_arrays_from_summary(_summary(), model_state="final")

    assert truth == ([150.0, 250.0, 350.0], [80.0, 100.0, 120.0], [5.0, 6.0, 8.0])
    assert final == truth


def test_select_replication_case_returns_named_case():
    case = select_replication_case(_summary(), "source_mismatch_ringdown050_noise10_seed13")

    assert case["noise_seed"] == 13
    assert case["ringdown_scale"] == 0.5


def test_representative_pair_uses_target_and_txrx_offset():
    pair = representative_pair_from_summary(_summary(), summary_path="summary.json")

    assert pair["target_rebar_index"] == 2
    assert pair["tx_x_mm"] == 346.0
    assert pair["rx_x_mm"] == 406.0


def test_source_receiver_indices_keep_receiver_right_of_source():
    pair = representative_pair_from_summary(_summary())
    src_iz, src_ix, rec_iz, rec_ix = source_receiver_indices_for_pair(pair)

    assert src_iz == rec_iz
    assert rec_ix > src_ix


def test_compact_animation_title_uses_run_target_and_pair():
    pair = representative_pair_from_summary(_summary())
    title = compact_animation_title(_summary(), "outputs/experiments/123_demo", pair)

    assert "run 123" in title
    assert "target 2" in title
    assert "Tx 346 mm" in title
    assert len(title) < 90


def test_summary_is_json_serializable_fixture():
    assert json.loads(json.dumps(_summary()))["run_name"] == "fdtd_context_demo"

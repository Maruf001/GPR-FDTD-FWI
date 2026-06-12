import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_experiment_pulse_noise_visualization import (  # noqa: E402
    backfill_pulse_noise_artifacts,
    build_noise_proxy,
    build_source_components,
    select_replication_case,
    write_pulse_noise_artifacts,
)
from run_experiment_wave_propagation_animation import (  # noqa: E402
    backfill_wave_animation_artifacts,
    choose_representative_pair,
    travel_time_metadata,
    write_animation_artifacts,
)
from run_experiment_scene_visualization import scene_from_summary  # noqa: E402


def _summary():
    return {
        "run_name": "context_demo",
        "frequency_ghz": 1.5,
        "sources": 3,
        "tx_rx_offset_mm": 60.0,
        "scan_x_values_mm": [50.0, 190.0, 330.0],
        "true_x_values_mm": [150.0, 250.0, 350.0],
        "true_z_values_mm": [80.0, 100.0, 120.0],
        "truth_radius_values_mm": [5.0, 6.0, 8.0],
        "initial_state": {
            "x_values_mm": [150.0, 250.0, 350.0],
            "z_values_mm": [80.0, 100.0, 120.0],
            "radii_mm": [5.0, 6.0, 8.0],
        },
        "final_state": {
            "x_values_mm": [150.0, 250.0, 350.0],
            "z_values_mm": [80.0, 100.0, 120.0],
            "radii_mm": [5.0, 6.0, 8.0],
        },
        "target_indices": [1],
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
        "case_metadata": {
            "source_mismatch_ringdown050_noise10_seed13": {
                "noise": {
                    "clean_rms": 1.0,
                    "noise_std": 0.1,
                    "actual_noise_rms": 0.099,
                }
            }
        },
    }


def test_source_pulse_noise_artifacts_write_valid_png_and_summary(tmp_path):
    summary = _summary()
    artifacts = write_pulse_noise_artifacts(summary, tmp_path, summary_path="summary.json")

    assert artifacts["validation"]["unique_colors"] > 32
    payload = json.loads((tmp_path / "data" / "source_pulse_noise_context_summary.json").read_text())
    assert payload["case"]["label"] == "source_mismatch_ringdown050_noise10_seed13"
    assert payload["noise"]["rms_fraction"] == 0.1
    assert payload["noise"]["seed_fingerprint_first16"]
    assert payload["visualization"]["pulse_plus_noise_scale"].startswith("clean source")
    assert payload["source_wavelet"]["type"] == "Ricker / Mexican hat"
    assert "source_pulse_noise_context:start" in (
        tmp_path / "figures" / "FIGURE_NOTES.md"
    ).read_text()


def test_source_components_and_noise_proxy_are_deterministic():
    summary = _summary()
    case = select_replication_case(summary)
    components = build_source_components(summary, case, nt=64)
    first = build_noise_proxy(summary, case, components["observed_source"])
    second = build_noise_proxy(summary, case, components["observed_source"])

    assert components["observed_source"].shape == (64,)
    assert first["stats"]["seed"] == 13
    assert first["noise"].tolist() == second["noise"].tolist()
    assert first["stats"]["seed_fingerprint_first16"] == second["stats"]["seed_fingerprint_first16"]


def test_noise_proxy_seed_changes_fingerprint_without_changing_source():
    summary = _summary()
    case = select_replication_case(summary)
    changed_seed_case = dict(case)
    changed_seed_case["noise_seed"] = 21
    components = build_source_components(summary, case, nt=64)
    first = build_noise_proxy(summary, case, components["observed_source"])
    second = build_noise_proxy(summary, changed_seed_case, components["observed_source"])

    assert first["stats"]["seed"] == 13
    assert second["stats"]["seed"] == 21
    assert first["stats"]["type"] == second["stats"]["type"]
    assert first["stats"]["rms_fraction"] == second["stats"]["rms_fraction"]
    assert first["stats"]["seed_fingerprint_first16"] != second["stats"]["seed_fingerprint_first16"]


def test_geometric_wave_animation_artifacts_write_valid_gif_and_summary(tmp_path):
    summary = _summary()
    artifacts = write_animation_artifacts(
        summary,
        tmp_path,
        summary_path="summary.json",
        frames=5,
        fps=2,
    )

    assert artifacts["validation"]["frame_count"] >= 5
    payload = json.loads((tmp_path / "data" / "geometric_wave_propagation_summary.json").read_text())
    assert payload["animation_type"] == "geometric travel-time schematic"
    assert payload["metadata"]["pair"]["target_rebar_index"] == 1
    assert "geometric_wave_propagation:start" in (
        tmp_path / "figures" / "FIGURE_NOTES.md"
    ).read_text()


def test_representative_pair_selects_target_midpoint():
    scene = scene_from_summary(_summary(), "summary.json")
    pair = choose_representative_pair(scene)
    travel = travel_time_metadata(scene, pair)

    assert pair["tx_x_mm"] == 190.0
    assert pair["rx_x_mm"] == 250.0
    assert len(travel["rebar_echoes"]) == 3
    assert any(row["is_target"] for row in travel["rebar_echoes"])


def _write_summary(run_dir, summary=None):
    data_dir = run_dir / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "multi_rebar_coordinate_optimizer_summary.json").write_text(
        json.dumps(_summary() if summary is None else summary),
        encoding="utf-8",
    )


def test_pulse_noise_backfill_generates_audit_and_skips_existing(tmp_path):
    root = tmp_path / "experiments"
    root.mkdir()
    (root / "3_field_qc").mkdir()
    run_dir = root / "2_coordinate_optimizer_demo"
    _write_summary(run_dir)

    result = backfill_pulse_noise_artifacts(
        root,
        audit_json=root / "pulse_audit.json",
        audit_csv=root / "pulse_audit.csv",
    )

    assert result["counts"] == {"skipped": 1, "generated": 1}
    assert (run_dir / "figures" / "source_pulse_noise_context.png").exists()
    assert (run_dir / "data" / "source_pulse_noise_context_summary.json").exists()
    assert (root / "pulse_audit.json").exists()

    second = backfill_pulse_noise_artifacts(root)

    assert second["counts"] == {"skipped": 2}
    coordinate_row = next(row for row in second["rows"] if row["run_number"] == 2)
    assert coordinate_row["reason"] == "existing valid pulse/noise artifacts"


def test_wave_animation_backfill_generates_audit_and_skips_existing(tmp_path):
    root = tmp_path / "experiments"
    root.mkdir()
    (root / "3_field_qc").mkdir()
    run_dir = root / "2_coordinate_optimizer_demo"
    _write_summary(run_dir)

    result = backfill_wave_animation_artifacts(
        root,
        frames=5,
        fps=2,
        audit_json=root / "wave_audit.json",
        audit_csv=root / "wave_audit.csv",
    )

    assert result["counts"] == {"skipped": 1, "generated": 1}
    assert (run_dir / "figures" / "geometric_wave_propagation.gif").exists()
    assert (run_dir / "data" / "geometric_wave_propagation_summary.json").exists()
    assert (root / "wave_audit.csv").exists()

    second = backfill_wave_animation_artifacts(root, frames=5, fps=2)

    assert second["counts"] == {"skipped": 2}
    coordinate_row = next(row for row in second["rows"] if row["run_number"] == 2)
    assert coordinate_row["reason"] == "existing valid wave animation artifacts"

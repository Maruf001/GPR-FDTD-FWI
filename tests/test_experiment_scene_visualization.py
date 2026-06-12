import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_experiment_scene_visualization import (  # noqa: E402
    backfill_scene_artifacts,
    explicit_scene,
    parse_indices,
    rebar_specs,
    scene_from_summary,
    specs_are_same,
    upsert_figure_notes,
)


def test_rebar_specs_requires_matching_lengths():
    with pytest.raises(ValueError, match="same length"):
        rebar_specs([150.0], [80.0, 81.0], [5.0])


def test_scene_from_summary_extracts_geometry_and_acquisition():
    summary = {
        "run_name": "demo",
        "true_x_values_mm": [150.0, 250.0],
        "true_z_values_mm": [80.0, 100.0],
        "truth_radius_values_mm": [5.0, 6.0],
        "initial_state": {
            "x_values_mm": [150.0, 250.0],
            "z_values_mm": [80.0, 101.0],
            "radii_mm": [5.0, 6.25],
        },
        "final_state": {
            "x_values_mm": [150.0, 250.0],
            "z_values_mm": [80.0, 100.0],
            "radii_mm": [5.0, 6.0],
        },
        "target_indices": [1],
        "scan_x_values_mm": [50.0, 250.0, 450.0],
        "tx_rx_offset_mm": 60.0,
        "sources": 3,
        "frequency_ghz": 1.5,
    }

    scene = scene_from_summary(summary, "summary.json")

    assert scene["run_name"] == "demo"
    assert scene["truth"][1]["radius_mm"] == 6.0
    assert scene["initial"][1]["z_mm"] == 101.0
    assert scene["final"][1]["z_mm"] == 100.0
    assert scene["target_indices"] == [1]
    assert scene["scan_x_values_mm"] == [50.0, 250.0, 450.0]
    assert scene["tx_rx_offset_mm"] == 60.0


def test_specs_are_same_uses_numeric_values():
    left = rebar_specs([150.0], [80.0], [5.0])
    right = rebar_specs([150], [80], [5])
    changed = rebar_specs([150.0], [81.0], [5.0])

    assert specs_are_same(left, right)
    assert not specs_are_same(left, changed)


def test_parse_indices_allows_empty_and_rejects_negative():
    assert parse_indices("") == []
    assert parse_indices("0,2") == [0, 2]
    with pytest.raises(Exception):
        parse_indices("-1")


def test_upsert_figure_notes_is_idempotent(tmp_path):
    figures_dir = tmp_path / "figures"
    figures_dir.mkdir()
    notes = figures_dir / "FIGURE_NOTES.md"
    notes.write_text("# Figure Notes\n\nExisting text.\n", encoding="utf-8")

    upsert_figure_notes(figures_dir, "system_scene_geometry.png", "system_scene_geometry_summary.json")
    upsert_figure_notes(figures_dir, "system_scene_geometry.png", "system_scene_geometry_summary.json")
    text = notes.read_text(encoding="utf-8")

    assert text.count("<!-- system_scene_geometry:start -->") == 1
    assert "Existing text." in text


def test_explicit_scene_supports_final_overlay():
    class Args:
        x_values_mm = [150.0]
        z_values_mm = [80.0]
        radius_values_mm = [5.0]
        final_x_values_mm = [151.0]
        final_z_values_mm = [81.0]
        final_radius_values_mm = [5.25]
        target_indices = [0]
        scan_x_values_mm = [50.0]
        tx_rx_offset_mm = 60.0
        source_z_mm = 38.0
        receiver_z_mm = 38.0
        concrete_top_mm = 40.0
        domain_x_mm = 500.0
        domain_z_mm = 300.0
        frequency_ghz = 1.5
        run_name = "explicit"

    scene = explicit_scene(Args)

    assert scene["truth"][0]["x_mm"] == 150.0
    assert scene["final"][0]["x_mm"] == 151.0
    assert scene["target_indices"] == [0]


def _write_coordinate_summary(run_dir, run_name):
    data_dir = run_dir / "data"
    data_dir.mkdir(parents=True)
    summary = {
        "run_name": run_name,
        "true_x_values_mm": [150.0, 250.0],
        "true_z_values_mm": [80.0, 100.0],
        "truth_radius_values_mm": [5.0, 6.0],
        "initial_state": {
            "x_values_mm": [150.0, 250.0],
            "z_values_mm": [80.0, 101.0],
            "radii_mm": [5.0, 6.25],
        },
        "final_state": {
            "x_values_mm": [150.0, 250.0],
            "z_values_mm": [80.0, 100.0],
            "radii_mm": [5.0, 6.0],
        },
        "target_indices": [1],
        "scan_x_values_mm": [50.0, 250.0, 450.0],
        "tx_rx_offset_mm": 60.0,
        "sources": 3,
        "frequency_ghz": 1.5,
    }
    (data_dir / "multi_rebar_coordinate_optimizer_summary.json").write_text(
        json.dumps(summary),
        encoding="utf-8",
    )


def test_backfill_scene_artifacts_generates_audit_and_skips_existing(tmp_path):
    root = tmp_path / "experiments"
    root.mkdir()
    missing_summary = root / "3_field_qc"
    missing_summary.mkdir()
    run_dir = root / "2_coordinate_optimizer_demo"
    _write_coordinate_summary(run_dir, "coordinate_optimizer_demo")
    audit_json = root / "scene_backfill_audit.json"
    audit_csv = root / "scene_backfill_audit.csv"

    result = backfill_scene_artifacts(
        root,
        audit_json=audit_json,
        audit_csv=audit_csv,
    )

    assert result["counts"] == {"skipped": 1, "generated": 1}
    assert (run_dir / "figures" / "system_scene_geometry.png").exists()
    assert (run_dir / "data" / "system_scene_geometry_summary.json").exists()
    assert "<!-- system_scene_geometry:start -->" in (
        run_dir / "figures" / "FIGURE_NOTES.md"
    ).read_text(encoding="utf-8")
    assert audit_json.exists()
    assert audit_csv.exists()

    second = backfill_scene_artifacts(root)

    assert second["counts"] == {"skipped": 2}
    coordinate_row = next(row for row in second["rows"] if row["run_number"] == 2)
    assert coordinate_row["reason"] == "existing valid scene artifacts"
    assert coordinate_row["unique_colors"] != ""

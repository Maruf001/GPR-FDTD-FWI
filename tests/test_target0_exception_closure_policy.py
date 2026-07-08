import csv
import json
import math

from run_target0_exception_closure_policy import (
    collect_run_row,
    followup_kind,
    synthesize_closure,
)


def _write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _make_run(tmp_path, run_id, *, sources, tx_rx, margin, confidence_label):
    run_dir = tmp_path / f"{run_id}_coordinate_optimizer_fake"
    data_dir = run_dir / "data"
    data_dir.mkdir(parents=True)
    summary = {
        "sources": sources,
        "tx_rx_offset_mm": tx_rx,
        "true_x_values_mm": [150.0, 250.0, 350.0],
        "true_z_values_mm": [80.0, 100.0, 120.0],
        "truth_radius_values_mm": [5.0, 6.0, 8.0],
        "final_state": {
            "x_values_mm": [150.0, 250.0, 350.0],
            "z_values_mm": [80.0, 100.0, 120.0],
            "radii_mm": [5.0, 6.0, 8.0],
        },
    }
    (data_dir / "multi_rebar_coordinate_optimizer_summary.json").write_text(
        json.dumps(summary),
        encoding="utf-8",
    )
    confidence = {
        "case_label": "source_mismatch_ringdown050_noise10_seed2504730781961",
        "target_rebar_index": "0",
        "best_x_mm": "150.0",
        "best_z_mm": "80.0",
        "best_radius_mm": "5.0",
        "next_radius_mm": "5.25",
        "radius_margin_abs": str(margin),
        "confidence_label": confidence_label,
        "fallback_warning": "" if confidence_label == "moderate" else "radius_weak_confidence",
    }
    objective_rows = [
        {
            "objective_label": "base",
            "target_rebar_index": "0",
            "best_x_mm": "150.0",
            "best_z_mm": "80.0",
            "best_radius_mm": "5.0",
            "radius_margin_abs": str(margin),
        },
        {
            "objective_label": "highband",
            "target_rebar_index": "0",
            "best_x_mm": "150.0",
            "best_z_mm": "80.0",
            "best_radius_mm": "5.0",
            "radius_margin_abs": str(margin * 1.4),
        },
        {
            "objective_label": "late",
            "target_rebar_index": "0",
            "best_x_mm": "150.0",
            "best_z_mm": "80.0",
            "best_radius_mm": "5.0",
            "radius_margin_abs": str(margin * 0.8),
        },
    ]
    _write_csv(data_dir / "coordinate_confidence_report.csv", [confidence])
    _write_csv(data_dir / "coordinate_objective_diagnostics.csv", objective_rows)
    return run_dir


def test_followup_kind_separates_spacing_and_source_density():
    assert followup_kind(sources=8, tx_rx_offset_mm=60.0) == "baseline_control"
    assert followup_kind(sources=8, tx_rx_offset_mm=45.0) == "spacing_probe"
    assert followup_kind(sources=9, tx_rx_offset_mm=60.0) == "source_density_probe"


def test_collect_run_row_reports_truth_preserving_weak_probe(tmp_path):
    run_dir = _make_run(
        tmp_path,
        1139,
        sources=8,
        tx_rx=45.0,
        margin=4.842585e-4,
        confidence_label="weak",
    )

    row = collect_run_row(run_dir, cutoff=5.0e-4)

    assert row["run_id"] == 1139
    assert row["seed"] == 2504730781961
    assert row["followup_kind"] == "spacing_probe"
    assert row["decision"] == "weak_truth_preserved"
    assert row["exact_target_geometry"] is True
    assert row["all_objective_variants_truth_exact"] is True
    assert row["objectives_above_cutoff"] == "highband"
    assert "base" in row["objectives_below_cutoff"]


def test_synthesize_closure_prefers_existing_source_density_rescue(tmp_path):
    rows = [
        collect_run_row(
            _make_run(tmp_path, 1136, sources=8, tx_rx=60.0, margin=3.872998e-4, confidence_label="weak"),
            cutoff=5.0e-4,
        ),
        collect_run_row(
            _make_run(tmp_path, 1139, sources=8, tx_rx=45.0, margin=4.842585e-4, confidence_label="weak"),
            cutoff=5.0e-4,
        ),
        collect_run_row(
            _make_run(tmp_path, 1140, sources=9, tx_rx=60.0, margin=5.296469e-4, confidence_label="moderate"),
            cutoff=5.0e-4,
        ),
    ]

    summary = synthesize_closure(rows, cutoff=5.0e-4)

    assert summary["policy_label"] == "target0_exception_closed_by_source_density"
    assert summary["gpu_priority"] == "none"
    assert summary["accepted_run_ids"] == "1140"
    assert summary["source_density_accept_run_ids"] == "1140"
    assert summary["best_spacing_run_id"] == 1139
    assert math.isclose(
        summary["best_overall_minus_best_spacing_margin"],
        5.296469e-4 - 4.842585e-4,
    )

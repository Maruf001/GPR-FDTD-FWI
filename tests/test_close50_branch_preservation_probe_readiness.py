import csv
import json

from run_close50_branch_preservation_probe_readiness import (
    build_probe_rows,
    gate_rows,
    source_count_context,
    summarize_probe_readiness,
)


def _write_csv(path, rows):
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_candidate_csv(path, best_x, truth_x):
    _write_csv(
        path,
        [
            {
                "case_label": "source_mismatch_noise10_seed34",
                "misfit": "0.028",
                "target_index": "2",
                "x_mm": str(best_x),
                "z_mm": "90.0",
                "radius_mm": "7.5",
                "x_values_mm": f"[190.0, 250.0, {best_x}]",
                "z_values_mm": "[90.0, 90.0, 90.0]",
                "radii_mm": "[6.0, 6.0, 7.5]",
            },
            {
                "case_label": "source_mismatch_noise10_seed34",
                "misfit": "0.030",
                "target_index": "2",
                "x_mm": str(truth_x),
                "z_mm": "90.0",
                "radius_mm": "8.0",
                "x_values_mm": f"[190.0, 250.0, {truth_x}]",
                "z_values_mm": "[90.0, 90.0, 90.0]",
                "radii_mm": "[6.0, 6.0, 8.0]",
            },
        ],
    )


def test_probe_readiness_allows_one_sources3_txrx40_replicate(tmp_path):
    summary_path = tmp_path / "summary.json"
    candidate_path = tmp_path / "candidates.csv"
    _write_candidate_csv(candidate_path, best_x=299.0, truth_x=300.0)
    summary_path.write_text(
        json.dumps(
            {
                "sources": 3,
                "tx_rx_offset_mm": 40.0,
                "receiver_sampling": "nearest",
                "truth_radius_values_mm": [6.0, 6.0, 8.0],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    actionability_rows = [
        {
            "run_dir": "274_coordinate_optimizer_close50_seed34_sources3_txrx40_objectives",
            "run_name": "case",
            "target_index": "2",
            "case_label": "source_mismatch_noise10_seed34",
            "candidate_csv": str(candidate_path),
            "best_x_mm": "299.0",
            "truth_lateral_x_mm": "300.0",
            "truth_lateral_gap_abs": "0.002",
            "truth_lateral_gap_rel": "0.06",
            "candidate_linf_improvement_mm": "1.0",
            "source_summary_json": str(summary_path),
            "actionability_label": "candidate_for_narrow_coupled_probe",
        }
    ]
    boundary_rows = [
        {
            "sampling_family": "nearest_receiver",
            "tx_rx_offset_mm": "40.0",
            "truth_geometry_fraction": "1.0",
            "strict_clean_row_count": "6",
            "x_ambiguity_row_count": "0",
            "boundary_status": "clean_replicated",
        }
    ]
    source_context = source_count_context(
        [
            {
                "sources": "3",
                "pass_index": "0",
                "step_kind": "main",
                "case_label": "noise10_seed34",
                "is_truth_geometry": "False",
                "confidence_label": "weak",
            },
            {
                "sources": "3",
                "pass_index": "0",
                "step_kind": "main",
                "case_label": "source_mismatch_noise10_seed34",
                "is_truth_geometry": "False",
                "confidence_label": "weak",
            },
            {
                "sources": "4",
                "pass_index": "0",
                "step_kind": "main",
                "case_label": "noise10_seed34",
                "is_truth_geometry": "True",
                "confidence_label": "strong",
            },
        ]
    )

    rows = build_probe_rows(
        actionability_rows,
        boundary_rows,
        {"nearest_first_clean_replicated_tx_rx_mm": 30.0},
        {"default_recovered_count": 13, "default_mean_extra_candidates_per_step": 4.6},
        source_context,
    )
    _, _, summary = summarize_probe_readiness(rows, source_context)
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert rows[0]["recommended_action"] == "single_gpu_source_count_seed_replicate"
    assert rows[0]["truth_lateral_radius_mm"] == 8.0
    assert summary["ready_for_single_gpu_source_count_seed_replicate"] is True
    assert summary["ready_for_broad_gpu_queue"] is False
    assert gates["single_gpu_source_count_seed_replicate"]["ready"] is True


def test_probe_readiness_blocks_below_clean_threshold_repeat(tmp_path):
    summary_path = tmp_path / "summary.json"
    candidate_path = tmp_path / "candidates.csv"
    _write_candidate_csv(candidate_path, best_x=301.0, truth_x=300.0)
    summary_path.write_text(
        json.dumps(
            {
                "sources": 4,
                "tx_rx_offset_mm": 25.0,
                "receiver_sampling": "nearest",
                "truth_radius_values_mm": [6.0, 6.0, 8.0],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    rows = build_probe_rows(
        [
            {
                "run_dir": "1221_coordinate_optimizer_close50_seed21_sources4_txrx25_objectives",
                "run_name": "case",
                "target_index": "2",
                "case_label": "source_mismatch_noise10_seed34",
                "candidate_csv": str(candidate_path),
                "best_x_mm": "301.0",
                "truth_lateral_x_mm": "300.0",
                "truth_lateral_gap_abs": "0.0002",
                "truth_lateral_gap_rel": "0.003",
                "candidate_linf_improvement_mm": "1.0",
                "source_summary_json": str(summary_path),
                "actionability_label": "candidate_for_narrow_coupled_probe",
            }
        ],
        [
            {
                "sampling_family": "nearest_receiver",
                "tx_rx_offset_mm": "25.0",
                "truth_geometry_fraction": "0.333",
                "strict_clean_row_count": "0",
                "x_ambiguity_row_count": "12",
                "boundary_status": "mixed_or_ambiguous",
            }
        ],
        {"nearest_first_clean_replicated_tx_rx_mm": 30.0},
        {"default_recovered_count": 13, "default_mean_extra_candidates_per_step": 4.6},
        {},
    )
    _, _, summary = summarize_probe_readiness(rows, {})

    assert rows[0]["recommended_action"] == "no_gpu_archive_boundary_caveat"
    assert summary["ready_for_single_gpu_source_count_seed_replicate"] is False
    assert summary["gpu_priority"] == "none"

import csv

from run_local_2d_detector_fixed_radius_locking_policy_design import (
    build_lock_candidate_rows,
    build_policy_rows,
    gate_rows,
    guarded_unlock_command,
    summarize_design,
)


def _write_candidates(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "case_label",
                "misfit",
                "target_index",
                "x_mm",
                "z_mm",
                "radius_mm",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _row(target, x_mm, z_mm, radius_mm, misfit):
    return {
        "case_label": "nominal",
        "target_index": target,
        "x_mm": x_mm,
        "z_mm": z_mm,
        "radius_mm": radius_mm,
        "misfit": misfit,
    }


def _optimizer_summary(paths):
    return {
        "run_name": "pilot",
        "true_x_values_mm": [190.0, 250.0, 264.0],
        "true_z_values_mm": [90.0, 90.0, 90.0],
        "truth_radius_values_mm": [5.0, 6.0, 8.0],
        "final_state": {
            "x_values_mm": [190.0, 251.0, 265.0],
            "z_values_mm": [90.0, 89.0, 91.0],
            "radii_mm": [5.0, 6.0, 8.0],
        },
        "steps": [
            {
                "target_index": 0,
                "state_before": {
                    "x_values_mm": [191.0, 252.0, 266.0],
                    "z_values_mm": [90.0, 89.0, 91.0],
                    "radii_mm": [5.0, 6.0, 8.0],
                },
                "candidate_csv": str(paths[0]),
            },
            {
                "target_index": 1,
                "state_before": {
                    "x_values_mm": [190.0, 252.0, 266.0],
                    "z_values_mm": [90.0, 89.0, 91.0],
                    "radii_mm": [5.0, 6.0, 8.0],
                },
                "candidate_csv": str(paths[1]),
            },
            {
                "target_index": 2,
                "state_before": {
                    "x_values_mm": [190.0, 251.0, 266.0],
                    "z_values_mm": [90.0, 89.0, 91.0],
                    "radii_mm": [5.0, 6.0, 8.0],
                },
                "candidate_csv": str(paths[2]),
            },
        ],
    }


def _write_fixture(tmp_path):
    paths = [tmp_path / f"step_{idx}.csv" for idx in range(3)]
    _write_candidates(
        paths[0],
        [
            _row(0, 190.0, 90.0, 5.0, 0.10),
            _row(0, 191.0, 90.0, 5.0, 0.101),
        ],
    )
    _write_candidates(
        paths[1],
        [
            _row(1, 251.0, 89.0, 6.0, 0.06295447447945064),
            _row(1, 250.0, 90.0, 6.0, 0.0651040951580757),
            _row(1, 252.0, 89.0, 6.0, 0.06530693489831033),
            _row(1, 251.0, 90.0, 6.0, 0.06609000295554064),
            _row(1, 250.0, 88.0, 6.0, 0.07557983967167514),
        ],
    )
    _write_candidates(
        paths[2],
        [
            _row(2, 265.0, 91.0, 8.0, 0.06122030512371148),
            _row(2, 265.0, 90.0, 8.0, 0.06222749395404279),
            _row(2, 266.0, 91.0, 8.0, 0.06295447447945064),
        ],
    )
    return _optimizer_summary(paths)


def test_lock_design_selects_near_tie_candidate_that_unblocks_downstream_truth(tmp_path):
    optimizer = _write_fixture(tmp_path)
    rows = build_lock_candidate_rows(
        optimizer,
        [
            {"target_index": 0, "residual_mode": "truth_selected_but_ambiguous"},
            {"target_index": 1, "residual_mode": "truth_present_but_objective_prefers_neighbor"},
            {"target_index": 2, "residual_mode": "truth_candidate_absent_after_nonoverlap_filter"},
        ],
        near_tie_rel=0.05,
    )
    target1 = [row for row in rows if row["target_index"] == 1][0]

    assert target1["best_x_mm"] == 251.0
    assert target1["best_z_mm"] == 89.0
    assert target1["lock_x_mm"] == 250.0
    assert target1["lock_z_mm"] == 90.0
    assert round(target1["lock_objective_penalty_rel"], 6) == 0.034146
    assert target1["downstream_truth_clearance_with_best_mm"] < 0.0
    assert target1["downstream_truth_clearance_with_lock_mm"] == 0.0
    assert target1["ready_for_single_guarded_unlock_probe"] is True


def test_summary_emits_one_guarded_unlock_probe_and_blocks_broad_gpu(tmp_path):
    optimizer = _write_fixture(tmp_path)
    residual_summary = {
        "policy_label": "residual",
        "final_linf_error_mm": 1.0,
    }
    lock_rows = build_lock_candidate_rows(optimizer, [], near_tie_rel=0.05)
    policies = build_policy_rows(lock_rows, residual_summary, optimizer)
    summary = summarize_design(
        optimizer,
        residual_summary,
        lock_rows,
        policies,
        near_tie_rel=0.05,
    )
    gates = {row["gate_key"]: row for row in gate_rows(summary)}
    command = guarded_unlock_command(summary)

    assert summary["ready_for_single_guarded_unlock_probe"] is True
    assert summary["unlock_probe_target_index"] == 2
    assert summary["unlock_probe_initial_x_values_mm"] == "190,250,266"
    assert summary["unlock_probe_initial_z_values_mm"] == "90,90,91"
    assert summary["ready_for_broad_gpu_queue"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert gates["single_guarded_unlock_probe"]["ready"] is True
    assert "--max-ram-percent 80" in command
    assert "--max-gpu-util-percent 90" in command
    assert "--target-indices 2" in command

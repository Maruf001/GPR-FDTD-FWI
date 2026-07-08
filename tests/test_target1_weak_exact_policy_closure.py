from run_target1_weak_exact_policy_closure import gate_rows, source_density_context, summarize_policy


def _evidence(key, row_count, fraction, role="", exception=""):
    return {
        "evidence_key": key,
        "source": "test",
        "row_count": row_count,
        "base_accepted_count": 0,
        "secondary_objective": "late_high",
        "secondary_accepted_count": int(row_count * fraction) if row_count else 0,
        "secondary_total": row_count,
        "secondary_fraction": fraction,
        "exception_run_ids": exception,
        "policy_role": role,
    }


def test_policy_closure_blocks_gpu_and_replacement_gate_when_modern_confirmed():
    source_density = {
        "target1_source_density_series_count": 3,
        "target1_source_density_all_exact_geometry_count": 3,
        "target1_source_density_all_weak_series_count": 1,
        "target1_source_density_mixed_series_count": 2,
        "target1_source_density_all_accepted_series_count": 0,
        "target1_all_weak_series_ids": "seed610",
    }
    evidence_rows = [
        _evidence("target1_all_weak_exact", 43, 42 / 43, exception="785"),
        _evidence("target1_ringdown050_weak_exact", 36, 1.0),
        _evidence("target1_modern_seed610_552", 12, 1.0),
        _evidence("guarded_archive_policy", 2610, 0.9925),
        _evidence(
            "target1_exception_triage",
            2,
            0.0,
            role="legacy_archive_exception_no_gpu_priority",
            exception="785",
        ),
    ]

    summary = summarize_policy(evidence_rows, source_density)
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["ringdown050_policy_closed"] is True
    assert summary["modern_seed610_552_policy_closed"] is True
    assert summary["legacy_exception_only"] is True
    assert summary["ready_for_broad_gpu_queue"] is False
    assert summary["ready_for_target1_gpu_exception_probe"] is False
    assert summary["secondary_confirmation_is_replacement_gate"] is False
    assert gates["broad_target1_gpu_queue"]["ready"] is False
    assert gates["secondary_objective_as_production_gate"]["ready"] is False


def test_source_density_context_counts_exact_and_all_weak_series():
    rows = [
        {"series_id": "a", "outcome_category": "all weak", "all_exact_geometry": "True"},
        {"series_id": "b", "outcome_category": "mixed: accepted setting exists", "all_exact_geometry": "True"},
        {"series_id": "c", "outcome_category": "all accepted", "all_exact_geometry": "False"},
    ]

    summary = source_density_context(rows)

    assert summary["target1_source_density_series_count"] == 3
    assert summary["target1_source_density_all_exact_geometry_count"] == 2
    assert summary["target1_source_density_all_weak_series_count"] == 1
    assert summary["target1_source_density_mixed_series_count"] == 1
    assert summary["target1_source_density_all_accepted_series_count"] == 1
    assert summary["target1_all_weak_series_ids"] == "a"

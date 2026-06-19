from run_close_spacing_source_density_archive_map import summarize_groups, synthesize_policy


def _row(
    family,
    spacing,
    source_count,
    seed,
    truth_geometry,
    confidence_label,
    x_error=0.0,
    radius_error=None,
    evidence_scope=None,
):
    if radius_error is None:
        radius_error = 0.0 if truth_geometry else -0.5
    return {
        "source_label": "test",
        "source_path": "test.csv",
        "evidence_scope": evidence_scope
        or ("matched_source_count_transition" if family == "close50" else "single_seed_source3_context"),
        "family": family,
        "spacing_mm": spacing,
        "source_count": source_count,
        "tx_rx_offset_mm": 40.0 if family == "close50" else 45.0,
        "seed": seed,
        "case_label": f"noise10_seed{seed}",
        "case_kind": "nominal",
        "run_name": "test_run",
        "best_x_mm": 300.0 - x_error,
        "best_z_mm": 90.0,
        "best_radius_mm": 8.0 + radius_error,
        "truth_x_mm": 300.0,
        "truth_z_mm": 90.0,
        "truth_radius_mm": 8.0,
        "x_abs_error_mm": x_error,
        "radius_abs_error_mm": abs(radius_error),
        "truth_geometry": truth_geometry,
        "confidence_label": confidence_label,
        "radius_margin_abs": 0.003 if confidence_label == "strong" else 0.0001,
        "best_misfit": 0.04,
        "ambiguity_x_width_mm": 0.0 if truth_geometry else 1.0,
        "ambiguity_radius_width_mm": 0.0 if truth_geometry else 0.5,
    }


def test_close50_three_seed_source_density_transition_supported():
    rows = []
    for seed in [13, 21, 34]:
        for _ in range(2):
            rows.append(_row("close50", 50.0, 3, seed, False, "weak", x_error=1.0))
            rows.append(_row("close50", 50.0, 4, seed, True, "strong"))
            rows.append(_row("close50", 50.0, 5, seed, True, "strong"))

    group_rows = summarize_groups(rows)
    summary = synthesize_policy(group_rows)

    assert summary["source_count_transition_supported_for_close50_txrx40"] is True
    assert summary["close50_source3_three_seed_failure"] is True
    assert summary["close50_source4_three_seed_exact"] is True
    assert summary["close50_source5_three_seed_exact"] is True
    assert summary["ready_for_broad_gpu_queue"] is False
    assert summary["gpu_priority"] == "none"


def test_nonclose50_single_seed_source3_stays_context_only():
    rows = [
        _row("close14", 14.0, 3, 34, True, "strong"),
        _row("close14", 14.0, 3, 34, True, "strong"),
    ]

    group_rows = summarize_groups(rows)
    summary = synthesize_policy(group_rows)

    assert group_rows[0]["evidence_role"] == "single_seed_context_only"
    assert summary["source_count_transition_supported_for_close50_txrx40"] is False
    assert summary["incomplete_nonclose50_source3_families"] == "close14"
    assert summary["ready_for_broad_gpu_queue"] is False


def test_close14_three_seed_near_exact_source3_is_not_failure_or_incomplete():
    rows = []
    for seed in [13, 21]:
        rows.append(
            _row(
                "close14",
                14.0,
                3,
                seed,
                True,
                "strong",
                evidence_scope="three_seed_source3_near_exact_context",
            )
        )
        rows.append(
            _row(
                "close14",
                14.0,
                3,
                seed,
                True,
                "strong",
                evidence_scope="three_seed_source3_near_exact_context",
            )
        )
    rows.append(
        _row(
            "close14",
            14.0,
            3,
            34,
            True,
            "strong",
            evidence_scope="three_seed_source3_near_exact_context",
        )
    )
    rows.append(
        _row(
            "close14",
            14.0,
            3,
            34,
            False,
            "strong",
            x_error=1.0,
            radius_error=0.0,
            evidence_scope="three_seed_source3_near_exact_context",
        )
    )

    group_rows = summarize_groups(rows)
    summary = synthesize_policy(group_rows)

    assert group_rows[0]["evidence_role"] == "three_seed_near_exact_context"
    assert group_rows[0]["truth_geometry_fraction"] == 5 / 6
    assert group_rows[0]["three_seed_near_exact_context"] is True
    assert group_rows[0]["replicated_failure"] is False
    assert summary["near_exact_nonclose50_source3_families"] == "close14"
    assert summary["incomplete_nonclose50_source3_families"] == ""
    assert summary["ready_for_broad_gpu_queue"] is False

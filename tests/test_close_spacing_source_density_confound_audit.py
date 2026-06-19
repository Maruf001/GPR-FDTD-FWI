from run_close_spacing_source_density_confound_audit import (
    build_claim_rows,
    build_factor_rows,
    gate_rows,
    synthesize_policy,
)


def _family(
    family,
    *,
    txrx,
    target2_x,
    target_gap,
    truth_fraction,
    weak_fraction,
    source5_scope,
):
    return {
        "family": family,
        "source3_seed_values": "13,21,34",
        "source3_source_count": "3",
        "source3_tx_rx_offset_mm": str(txrx),
        "source3_receiver_sampling": "missing,nearest",
        "source3_backend": "gpu-cpml",
        "target0_target1_gap_mm": "60",
        "target1_target2_gap_mm": str(target_gap),
        "target2_x_mm": str(target2_x),
        "true_z_values_mm": "90,90,90",
        "truth_radius_values_mm": "5,6,8",
        "source3_replication_signature": "noise10|freq=1|shift_ps=0|amp=1|noise=0.1",
        "source3_truth_fraction": truth_fraction,
        "source3_strong_fraction": 1.0 - weak_fraction,
        "source3_weak_fraction": weak_fraction,
        "source3_evidence_role": "matched_three_seed_failure" if weak_fraction == 1.0 else "three_seed_near_exact_context",
        "source4_evidence_role": "three_seed_exact_recovery",
        "source5_evidence_scope": source5_scope,
        "source5_evidence_role": "three_seed_exact_recovery",
    }


def test_confound_audit_blocks_spacing_only_causal_generalization():
    close50 = _family(
        "close50",
        txrx=40,
        target2_x=300,
        target_gap=50,
        truth_fraction=0.0,
        weak_fraction=1.0,
        source5_scope="matched_source_count_transition",
    )
    close14 = _family(
        "close14",
        txrx=45,
        target2_x=264,
        target_gap=14,
        truth_fraction=5 / 6,
        weak_fraction=0.0,
        source5_scope="three_seed_source5_noise_boundary_context",
    )
    factors = build_factor_rows(close50, close14)
    claims = build_claim_rows(
        factors,
        {
            "close50_source3_replicated_failure": True,
            "close50_source4_5_exact_recovery": True,
            "close14_source3_near_exact_context": True,
            "source3_spacing_dependent_contrast": True,
        },
    )
    summary = synthesize_policy(factors, claims)
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["close50_within_family_transition_ready"] is True
    assert summary["guarded_cross_spacing_contrast_ready"] is True
    assert summary["spacing_only_causal_generalization_ready"] is False
    assert summary["ready_for_broad_gpu_queue"] is False
    assert summary["acquisition_confound_count"] == 1
    assert summary["geometry_confound_count"] == 1
    assert gates["spacing_only_causal_generalization"]["ready"] is False
    assert gates["broad_gpu_queue"]["ready"] is False


def test_factor_rows_mark_source5_as_context_only_when_noise_scope_differs():
    close50 = _family(
        "close50",
        txrx=40,
        target2_x=300,
        target_gap=50,
        truth_fraction=0.0,
        weak_fraction=1.0,
        source5_scope="matched_source_count_transition",
    )
    close14 = _family(
        "close14",
        txrx=40,
        target2_x=300,
        target_gap=14,
        truth_fraction=1.0,
        weak_fraction=0.0,
        source5_scope="three_seed_source5_noise_boundary_context",
    )

    factors = {row["factor_key"]: row for row in build_factor_rows(close50, close14)}

    assert factors["source5_context_scope"]["factor_type"] == "context_only"
    assert factors["source5_context_scope"]["matched_or_intended"] is False
    assert factors["tx_rx_offset_mm"]["matched_or_intended"] is True
    assert factors["target2_absolute_x_mm"]["matched_or_intended"] is True

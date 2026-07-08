from run_gssi_field_short_anchor_radius_degeneracy_audit import (
    build_common_radius_rows,
    build_radius_side_rows,
    summarize_radius_degeneracy,
)


def _waveform_candidate(file_name, group, radius, corr, residual=0.5):
    return {
        "candidate_id": f"{file_name}_g{group}_r{radius}",
        "file": file_name,
        "phase_convention": "top",
        "apex_group": str(group),
        "epsr_source": "fitted",
        "backend": "cpu",
        "frequency_ghz": "1.5",
        "sources": "5",
        "tx_rx_offset_mm": "60",
        "scan_aperture_mm": "320",
        "radius_mm": str(radius),
        "geometry_valid": "True",
        "absolute_correlation": str(corr),
        "normalized_residual_rms": str(residual),
    }


def _event_rows():
    return [
        {
            "pair_index": "1",
            "content_backed": "False",
            "reference_candidate_id": "ignored",
            "comparison_candidate_id": "ignored",
        },
        {
            "pair_index": "2",
            "content_backed": "True",
            "content_label": "repeat_content_anchor",
            "reference_candidate_id": "ref_g2_r8",
            "reference_radius_mm": "8",
            "reference_absolute_correlation": "0.89",
            "reference_normalized_residual_rms": "0.50",
            "comparison_candidate_id": "cmp_g2_r5",
            "comparison_radius_mm": "5",
            "comparison_absolute_correlation": "0.82",
            "comparison_normalized_residual_rms": "0.62",
            "pair_min_absolute_correlation": "0.82",
            "pair_mean_absolute_correlation": "0.855",
        },
    ]


def _waveform_rows():
    return [
        _waveform_candidate("ref", 2, 5, 0.854),
        _waveform_candidate("ref", 2, 6, 0.871),
        _waveform_candidate("ref", 2, 8, 0.890),
        _waveform_candidate("cmp", 2, 5, 0.820),
        _waveform_candidate("cmp", 2, 6, 0.814),
        _waveform_candidate("cmp", 2, 8, 0.810),
    ]


def test_radius_side_rows_flag_weak_sidewise_radius_separation():
    rows = build_radius_side_rows(_event_rows(), _waveform_rows(), min_radius_corr_gap=0.03)

    assert len(rows) == 2
    assert all(row["selected_is_best_radius"] for row in rows)
    assert all(row["radius_resolution_label"] == "weak_radius_separation" for row in rows)
    assert not any(row["radius_seed_ready"] for row in rows)


def test_common_radius_rows_find_near_tied_common_radius_candidate():
    rows = build_common_radius_rows(_event_rows(), _waveform_rows())

    radius5 = next(row for row in rows if row["common_radius_mm"] == 5.0)
    assert radius5["pair_min_absolute_correlation"] == 0.82
    assert radius5["common_radius_near_tie"]
    assert radius5["same_radius_pair_supports_qc"]


def test_summary_blocks_radius_seed_and_field_fwi_despite_waveform_qc():
    side_rows = build_radius_side_rows(_event_rows(), _waveform_rows(), min_radius_corr_gap=0.03)
    common_rows = build_common_radius_rows(_event_rows(), _waveform_rows())

    summary = summarize_radius_degeneracy(
        side_rows,
        common_rows,
        {"valid_candidate_count": 6, "selected_event_count": 1, "best_candidate": {"backend": "cpu"}},
        {"ready_for_waveform_morphology_qc": True},
        min_radius_corr_gap=0.03,
    )

    assert summary["content_pair_count"] == 1
    assert summary["selected_radius_mismatch_pair_count"] == 1
    assert summary["weak_radius_side_count"] == 2
    assert summary["common_radius_near_tie_pair_count"] == 1
    assert summary["ready_for_waveform_morphology_qc"]
    assert not summary["ready_for_radius_seed"]
    assert not summary["ready_for_field_fwi"]
    assert summary["gpu_priority"] == "none"

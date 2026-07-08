from run_local_2d_detector_sampling_boundary_integration import (
    build_category_rows,
    build_integration_rows,
    summarize_integration,
)


def _reliability_rows():
    return [
        {
            "case_label": "target2_close14|seed13|nominal",
            "branch_key": "target2_close14",
            "seed": "13",
            "case_variant": "nominal",
            "detector_reliability_label": "stable_truth_free_assignment",
            "detector_review": "False",
            "detector_success_fraction": "1.0",
            "detector_max_slot_x_range_mm": "1.0",
        },
        {
            "case_label": "target2_close50_linear29p5|seed13|nominal",
            "branch_key": "target2_close50_linear29p5",
            "seed": "13",
            "case_variant": "nominal",
            "detector_reliability_label": "review_policy_grid_position_drift",
            "detector_review": "True",
            "detector_success_fraction": "0.875",
            "detector_max_slot_x_range_mm": "21.0",
        },
        {
            "case_label": "target2_close50_linear29p5|seed13|source_mismatch",
            "branch_key": "target2_close50_linear29p5",
            "seed": "13",
            "case_variant": "source_mismatch",
            "detector_reliability_label": "stable_truth_free_assignment",
            "detector_review": "False",
            "detector_success_fraction": "1.0",
            "detector_max_slot_x_range_mm": "5.0",
        },
    ]


def _boundary_rows():
    return [
        {
            "sampling_family": "linear_receiver",
            "tx_rx_offset_mm": "29.5",
            "boundary_status": "exact_strong_not_clean",
            "paper_role": "sub30_exact_strong_caveat",
        }
    ]


def test_detector_reviews_are_labeled_as_sub30_nominal_caveats():
    rows = build_integration_rows(
        _reliability_rows(),
        [{"case_label": row["case_label"], "success_fraction": row["detector_success_fraction"]} for row in _reliability_rows()],
        [{"split_field": "branch_key", "heldout_failed_case_labels": "target2_close50_linear29p5|seed13|nominal"}],
        [{"case_label": row["case_label"], "candidate_component_seed_ready": "True"} for row in _reliability_rows()],
        [
            {
                "case_label": "target2_close50_linear29p5|seed13|nominal",
                "synthetic_x_ambiguous_row": "True",
                "synthetic_strict_clean_row": "False",
                "review_near_boundary_nominal": "True",
            }
        ],
        _boundary_rows(),
    )
    by_label = {row["case_label"]: row for row in rows}

    review = by_label["target2_close50_linear29p5|seed13|nominal"]
    assert review["sampling_below_clean_threshold"]
    assert review["detector_review"]
    assert review["branch_transfer_failure"]
    assert review["integration_label"] == "review_localized_to_sub30_nominal_caveat"


def test_summary_allows_branch_local_claim_but_blocks_fwi():
    rows = build_integration_rows(
        _reliability_rows(),
        [{"case_label": row["case_label"], "success_fraction": row["detector_success_fraction"]} for row in _reliability_rows()],
        [{"split_field": "branch_key", "heldout_failed_case_labels": "target2_close50_linear29p5|seed13|nominal"}],
        [{"case_label": row["case_label"], "candidate_component_seed_ready": "True"} for row in _reliability_rows()],
        [
            {
                "case_label": "target2_close50_linear29p5|seed13|nominal",
                "synthetic_x_ambiguous_row": "True",
                "synthetic_strict_clean_row": "False",
                "review_near_boundary_nominal": "True",
            }
        ],
        _boundary_rows(),
    )
    categories = build_category_rows(rows)
    summary = summarize_integration(
        rows,
        categories,
        {
            "nearest_first_clean_replicated_tx_rx_mm": 30.0,
            "ready_for_sub30_clean_threshold_claim": False,
        },
    )

    assert summary["detector_review_case_count"] == 1
    assert summary["review_below_clean_case_count"] == 1
    assert summary["branch_localized_detector_boundary_claim_ready"]
    assert summary["per_seed_physics_equivalence_ready"]
    assert not summary["ready_for_detector_seeded_fwi"]
    assert summary["gpu_priority"] == "none"

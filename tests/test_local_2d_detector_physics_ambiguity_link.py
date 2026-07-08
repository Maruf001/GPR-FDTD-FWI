from run_local_2d_detector_physics_ambiguity_link import (
    build_group_rows,
    build_link_rows,
    summarize_link,
    synthetic_case_label,
)


def _reliability(branch, seed, variant, review, success=1.0):
    return {
        "case_label": f"{branch}|seed{seed}|{variant}",
        "branch_key": branch,
        "seed": str(seed),
        "case_variant": variant,
        "truth_free_stable_assignment": str(not review),
        "truth_free_reliability_label": "review" if review else "stable",
        "tuning_sensitive_truth_eval": str(review),
        "success_fraction_truth_eval": str(success),
        "max_slot_x_range_mm": "20.0" if review else "2.0",
        "max_slot_z_range_mm": "10.0",
        "dominant_selection": "180,250,300",
    }


def _confidence(seed, variant, x_width, strict_clean):
    case_label = synthetic_case_label(seed, variant)
    return {
        "seed_label": f"seed{seed}",
        "case_label": case_label,
        "tx_rx_offset_mm": "29.5",
        "truth_geometry_match": "True",
        "strong_confidence": "True",
        "strict_clean_row": str(strict_clean),
        "x_ambiguity_width_mm": str(x_width),
    }


def test_link_rows_map_review_cases_to_close50_nominal_boundary():
    reliability = [
        _reliability("target2_close14", 13, "nominal", False),
        _reliability("target2_close50_linear29p5", 13, "nominal", True, success=0.875),
        _reliability("target2_close50_linear29p5", 13, "source_mismatch", False),
        _reliability("target2_close50_linear29p5", 34, "nominal", True, success=0.53125),
    ]
    confidence = [
        _confidence(13, "nominal", 1.0, False),
        _confidence(13, "source_mismatch", 0.0, True),
        _confidence(34, "nominal", 0.0, True),
    ]
    run_rows = [
        {"seed_label": "seed13", "run_policy_label": "x_ambiguous"},
        {"seed_label": "seed34", "run_policy_label": "single_seed_clean"},
    ]

    rows = build_link_rows(
        reliability,
        confidence,
        run_rows,
        {"first_clean_tx_rx_offset_mm": 30.0},
    )

    close14 = [row for row in rows if row["branch_key"] == "target2_close14"][0]
    assert close14["synthetic_confidence_present"] is False
    assert close14["synthetic_case_label"] == ""

    reviews = [row for row in rows if row["detector_review"]]
    assert len(reviews) == 2
    assert all(row["review_near_boundary_nominal"] for row in reviews)
    assert sum(row["synthetic_x_ambiguous_row"] for row in reviews) == 1
    assert sum(row["synthetic_strict_clean_row"] for row in reviews) == 1


def test_summary_is_branch_localization_not_per_seed_equivalence_or_fwi():
    reliability = [
        _reliability("target2_close50_linear29p5", 13, "nominal", True, success=0.875),
        _reliability("target2_close50_linear29p5", 13, "source_mismatch", False),
        _reliability("target2_close50_linear29p5", 34, "nominal", True, success=0.53125),
    ]
    confidence = [
        _confidence(13, "nominal", 1.0, False),
        _confidence(13, "source_mismatch", 0.0, True),
        _confidence(34, "nominal", 0.0, True),
    ]
    rows = build_link_rows(
        reliability,
        confidence,
        [
            {"seed_label": "seed13", "run_policy_label": "x_ambiguous"},
            {"seed_label": "seed34", "run_policy_label": "single_seed_clean"},
        ],
        {"first_clean_tx_rx_offset_mm": 30.0},
    )
    groups = build_group_rows(rows)
    summary = summarize_link(
        rows,
        groups,
        {"policy_label": "reliability"},
        {"policy_label": "threshold", "first_clean_tx_rx_offset_mm": 30.0},
        {
            "policy_label": "linear29p5",
            "seed_count": 3,
            "strict_clean_seed_count": 2,
            "ambiguous_seed_count": 1,
        },
    )

    assert summary["review_near_boundary_nominal_count"] == 2
    assert summary["detector_reviews_all_near_boundary_nominal"] is True
    assert summary["review_cases_with_synthetic_x_ambiguity_count"] == 1
    assert summary["review_cases_with_synthetic_strict_clean_count"] == 1
    assert summary["ready_for_branch_localization_claim"] is True
    assert summary["ready_for_per_seed_physics_equivalence_claim"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"

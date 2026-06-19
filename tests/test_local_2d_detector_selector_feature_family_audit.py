from run_local_2d_detector_selector_feature_family_audit import (
    choose_feature,
    evaluate_policy,
    feature_families,
    summarize_audit,
    summarize_policy_rows,
)


def _row(case_label, branch, variant, seed, feature, rank):
    return {
        "case_label": case_label,
        "branch_key": branch,
        "seed": str(seed),
        "case_variant": variant,
        "run_name": f"{branch}_{seed}_{variant}",
        "feature": feature,
        "first_all_truth_rank": str(rank),
        "top_unique_truth_hit_count": "1",
        "top_candidate_x_values_mm": "1,2,3",
    }


def test_feature_families_separate_span_targets_from_component_scores():
    families = feature_families(
        [
            "score_component_balanced",
            "score_span_bonus",
            "x_span_target80_inverse",
            "rank_sum_inverse",
        ]
    )

    assert "x_span_target80_inverse" in families["all_features"]
    assert "x_span_target80_inverse" not in families["score_only"]
    assert "x_span_target80_inverse" not in families["no_span_target"]
    assert families["fixed_component_balanced"] == ["score_component_balanced"]


def test_choose_feature_prefers_shallow_rank_coverage():
    rows = [
        _row("a", "b", "nominal", 1, "feature_a", 10),
        _row("b", "b", "nominal", 2, "feature_a", 80),
        _row("a", "b", "nominal", 1, "feature_b", 20),
        _row("b", "b", "nominal", 2, "feature_b", 30),
    ]

    assert choose_feature(rows, ["feature_a", "feature_b"]) == "feature_a"


def test_component_family_removes_deep_failure_but_keeps_fwi_blocked():
    rows = []
    for seed in (1, 2, 3):
        label = f"close50|seed{seed}|source_mismatch"
        rows.extend(
            [
                _row(label, "close50", "source_mismatch", seed, "x_span_target80_inverse", 500),
                _row(label, "close50", "source_mismatch", seed, "score_component_balanced", 15),
            ]
        )
    for seed in (1, 2, 3):
        label = f"close14|seed{seed}|nominal"
        rows.extend(
            [
                _row(label, "close14", "nominal", seed, "x_span_target80_inverse", 20),
                _row(label, "close14", "nominal", seed, "score_component_balanced", 150),
            ]
        )

    all_cases = evaluate_policy(rows, "all_features", ["x_span_target80_inverse", "score_component_balanced"], "global")
    component_cases = evaluate_policy(rows, "component_only", ["score_component_balanced"], "global")
    policies = summarize_policy_rows(all_cases + component_cases)
    summary = summarize_audit(policies, [], {"policy_label": "source"})

    by_policy = {(row["feature_family"], row["selector_strategy"]): row for row in policies}
    assert by_policy[("all_features", "global")]["deeper_than_top200_case_count"] == 3
    assert by_policy[("component_only", "global")]["deeper_than_top200_case_count"] == 0
    assert summary["ready_for_rank_gated_selector_claim"] is True
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"

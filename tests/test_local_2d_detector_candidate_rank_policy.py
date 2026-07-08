from run_local_2d_detector_candidate_rank_policy import (
    rank_values,
    row_recovered_within_cap,
    summarize,
    summarize_by_branch,
    summarize_by_config,
)


def _row(config_key, branch, seed, variant, ranks, recovered=True):
    return {
        "config_key": config_key,
        "background_mode": config_key.split("_")[0],
        "top_k": "40",
        "separation_profile": "moderate12",
        "time_offset_family": "single667",
        "branch_key": branch,
        "seed": str(seed),
        "case_variant": variant,
        "run_name": f"{branch}_{seed}_{variant}",
        "unique_all_truths_within_tolerance": recovered,
        "assigned_candidate_ranks": ",".join(str(rank) for rank in ranks),
    }


def test_rank_values_and_cap_recovery():
    row = _row("median_top40_moderate12_single667", "close14", 13, "nominal", [2, 8, 11])

    assert rank_values("2,8,11") == [2, 8, 11]
    assert row_recovered_within_cap(row, 10) is False
    assert row_recovered_within_cap(row, 20) is True


def test_candidate_rank_policy_finds_minimal_full_recovery_cap():
    rows = [
        _row("median_top40_moderate12_single667", "close14", 13, "nominal", [2, 8, 11]),
        _row("median_top40_moderate12_single667", "close14", 13, "source_mismatch", [5, 7, 18]),
        _row("none_top20_distinct20_baseline", "close14", 13, "nominal", [2, 3, 6]),
        _row("none_top20_distinct20_baseline", "close14", 13, "source_mismatch", [4, 12, 35]),
    ]

    config_rows = summarize_by_config(rows, rank_caps=(5, 10, 20, 40))
    branch_rows = summarize_by_branch(rows, rank_caps=(5, 10, 20, 40))
    summary = summarize(rows, config_rows, branch_rows, (5, 10, 20, 40))

    assert config_rows[0]["config_key"] == "median_top40_moderate12_single667"
    assert config_rows[0]["min_rank_cap_for_all_cases"] == 20
    assert summary["minimal_rank_cap_for_full_case_recovery"] == 20
    assert summary["best_case_count_by_rank_cap"]["top10"] == 1
    assert summary["best_case_count_by_rank_cap"]["top20"] == 2
    assert summary["gpu_used"] is False

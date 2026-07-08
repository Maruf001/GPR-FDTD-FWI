from run_local_2d_detector_parameter_sensitivity import (
    config_rows,
    summarize,
    summarize_by_case,
    summarize_by_config,
)


def _row(config_key, branch, seed, case_variant, unique_hits, all_truth=False):
    return {
        "config_key": config_key,
        "background_mode": config_key.split("_")[0],
        "top_k": 20,
        "separation_profile": "dense4",
        "time_offset_family": "baseline",
        "branch_key": branch,
        "seed": seed,
        "case_variant": case_variant,
        "run_name": f"{branch}_{seed}_{case_variant}",
        "unique_truth_hit_count": unique_hits,
        "unique_all_truths_within_tolerance": all_truth,
        "unique_target0_hit": unique_hits >= 1,
        "unique_target1_hit": unique_hits >= 2,
        "unique_target2_hit": unique_hits >= 3,
        "all_truths_within_tolerance": all_truth,
        "target0_hit": unique_hits >= 1,
        "target1_hit": unique_hits >= 2,
        "target2_hit": unique_hits >= 3,
        "best_candidate_score": 1.0,
        "assigned_candidate_ranks": ",".join(str(rank) for rank in range(1, unique_hits + 1)),
        "elapsed_time_s": 0.01,
    }


def test_config_rows_cover_background_topk_separation_and_offsets():
    rows = config_rows()

    assert len(rows) == 81
    assert {row["background_mode"] for row in rows} == {"none", "mean", "median"}
    assert {row["top_k"] for row in rows} == {20, 40, 80}
    assert {row["separation_profile"] for row in rows} == {"dense4", "moderate12", "distinct20"}
    assert {row["time_offset_family"] for row in rows} == {"single667", "baseline", "wide"}


def test_summaries_rank_configs_and_cases_by_unique_truth_hits():
    rows = [
        _row("none_top20_dense4_baseline", "target2_close14", 13, "nominal", 2),
        _row("median_top80_dense4_wide", "target2_close14", 13, "nominal", 3, True),
        _row("none_top20_dense4_baseline", "target2_close50_linear29p5", 13, "nominal", 1),
        _row("median_top80_dense4_wide", "target2_close50_linear29p5", 13, "nominal", 2),
    ]

    config_summary = summarize_by_config(rows)
    case_summary = summarize_by_case(rows)
    summary = summarize(rows, config_summary, case_summary)

    assert config_summary[0]["config_key"] == "median_top80_dense4_wide"
    assert len(case_summary) == 2
    assert summary["config_count"] == 2
    assert summary["case_count"] == 2
    assert summary["rescued_case_count"] == 1
    assert summary["best_config_key"] == "median_top80_dense4_wide"
    assert summary["best_config_mean_max_assigned_rank"] == 3.0
    assert summary["gpu_used"] is False

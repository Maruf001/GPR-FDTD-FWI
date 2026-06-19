from run_local_2d_detector_radius_material_prior_scope_audit import (
    build_case_rows,
    gate_rows,
    material_prior_rows,
    summarize_scope,
)


def _plan_rows():
    return [
        {
            "case_label": "plan-close14",
            "branch_key": "target2_close14",
            "seed": "13",
            "case_variant": "nominal",
            "truth_radius_values_mm": "5,6,8",
        },
        {
            "case_label": "plan-close50-review",
            "branch_key": "target2_close50_linear29p5",
            "seed": "21",
            "case_variant": "nominal",
            "truth_radius_values_mm": "5,6,8",
        },
    ]


def _launch_rows():
    return [
        {
            "branch_key": "target2_close14",
            "seed": "13",
            "case_variant": "nominal",
            "review_assignment": "False",
            "radius_seed_available": "False",
            "material_seed_available": "False",
        },
        {
            "branch_key": "target2_close50_linear29p5",
            "seed": "21",
            "case_variant": "nominal",
            "review_assignment": "True",
            "radius_seed_available": "False",
            "material_seed_available": "False",
        },
    ]


def _xz_rows():
    return [
        {
            "branch_key": "target2_close14",
            "seed": "13",
            "case_variant": "nominal",
            "case_contract_status": "stable_in_contract",
            "review_assignment": "False",
        },
        {
            "branch_key": "target2_close50_linear29p5",
            "seed": "21",
            "case_variant": "nominal",
            "case_contract_status": "review_excluded",
            "review_assignment": "True",
        },
    ]


def test_material_prior_rows_expose_fixed_synthetic_config_values():
    rows = material_prior_rows()
    by_parameter = {row["parameter"]: row for row in rows}

    assert len(rows) == 4
    assert by_parameter["concrete_epsr"]["value"] == 6.0
    assert by_parameter["concrete_sigma_s_per_m"]["value"] == 0.01
    assert by_parameter["rebar_epsr"]["value"] == 1.0
    assert by_parameter["rebar_sigma_s_per_m"]["value"] == 1.0e7
    assert all(row["role"] == "controlled synthetic material prior" for row in rows)


def test_case_rows_separate_controlled_priors_from_detector_inferred_seeds():
    rows = build_case_rows(_plan_rows(), _launch_rows(), _xz_rows())
    by_branch = {row["branch_key"]: row for row in rows}

    close14 = by_branch["target2_close14"]
    assert close14["truth_radius_pattern_key"] == "5,6,8"
    assert close14["controlled_synthetic_prior_contract_ready"] is True
    assert close14["detector_radius_seed_available"] is False
    assert close14["detector_material_seed_available"] is False
    assert close14["detector_inferred_radius_material_contract_ready"] is False

    review = by_branch["target2_close50_linear29p5"]
    assert review["review_assignment"] is True
    assert review["controlled_synthetic_prior_contract_ready"] is False
    assert review["blocked_use"] == "detector-inferred radius/material claims, field transfer, GPU/FWI launch"


def test_summary_allows_controlled_prior_scope_but_keeps_gpu_and_fwi_blocked():
    cases = build_case_rows(_plan_rows(), _launch_rows(), _xz_rows())
    materials = material_prior_rows()
    summary = summarize_scope(
        cases,
        materials,
        {
            "policy_label": "launch-contract",
            "active_blocker_keys": "radius_material_contract_missing;review_cases_present",
        },
        {
            "policy_label": "xz-contract",
            "ready_for_branch_specific_xz_seed_neighborhood_contract": True,
        },
    )
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["source_case_count"] == 2
    assert summary["stable_controlled_prior_case_count"] == 1
    assert summary["review_case_excluded_count"] == 1
    assert summary["radius_patterns_mm"] == "5,6,8"
    assert summary["ready_for_controlled_synthetic_prior_contract"] is True
    assert summary["ready_for_detector_inferred_radius_material_contract"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["ready_for_gpu_work"] is False
    assert gates["controlled_synthetic_prior_contract"]["ready"] is True
    assert gates["detector_inferred_radius_material_contract"]["ready"] is False
    assert gates["detector_seeded_fwi"]["ready"] is False

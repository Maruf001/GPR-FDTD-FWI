from run_local_2d_detector_slot_component_assembly_probe import (
    assemble_slot_components,
    component_rows_for_case,
    evaluate_slot_assembly,
    slot_hit_flags,
    summarize_slot_assembly,
)


def _triple_row(
    *,
    xs="190,250,264",
    zs="90,88,92",
    ranks="1,2,3",
    scores="0.8,0.7,0.6",
    branch="target2_close14",
    seed="13",
    run_name="run_a",
):
    return {
        "case_label": f"{branch}|seed{seed}|nominal",
        "branch_key": branch,
        "seed": seed,
        "case_variant": "nominal",
        "run_name": run_name,
        "combo_index": xs.replace(",", "_"),
        "candidate_x_values_mm": xs,
        "candidate_z_values_mm": zs,
        "candidate_ranks": ranks,
        "component_score_values": scores,
        "score_component_min": "0.2",
    }


def test_component_rows_for_case_decomposes_triples_and_keeps_best_duplicate_score():
    rows = [
        _triple_row(xs="190,250,264", scores="0.8,0.7,0.6"),
        _triple_row(xs="190,251,264", scores="0.9,0.5,0.4"),
    ]

    components = component_rows_for_case(rows)
    by_x = {component["x_mm"]: component for component in components}

    assert len(components) == 4
    assert by_x[190.0]["component_score"] == 0.9
    assert by_x[251.0]["rank"] == 2.0


def test_assemble_slot_components_recovers_expected_slots():
    components = component_rows_for_case(
        [
            _triple_row(xs="188,249,266", zs="86,88,90", scores="0.6,0.7,0.6"),
            _triple_row(xs="220,250,265", zs="86,88,90", scores="0.9,0.7,0.6"),
        ]
    )

    selected = assemble_slot_components(
        components,
        (190.0, 250.0, 264.0),
        slot_weight=4.0,
        depth_weight=1.0,
        score_weight=1.0,
        rank_weight=0.02,
    )

    assert [round(component["x_mm"]) for component in selected] == [188, 250, 265]
    assert slot_hit_flags(selected) == [True, True, True]


def test_slot_assembly_summary_marks_upper_bound_not_fwi_ready():
    rows = [
        _triple_row(xs="188,249,266", zs="86,88,90", scores="0.6,0.7,0.6"),
        _triple_row(xs="220,250,265", zs="86,88,90", scores="0.9,0.7,0.6"),
    ]

    variant_rows, selected_rows = evaluate_slot_assembly(
        rows,
        slot_weights=(4.0,),
        depth_weights=(1.0,),
        score_weights=(1.0,),
        rank_weights=(0.02,),
    )
    summary = summarize_slot_assembly(
        variant_rows,
        candidate_row_count=len(rows),
        comparison_summary={"base_all_truth_case_count": 0, "best_all_truth_case_count": 0},
    )

    assert len(selected_rows) == 1
    assert summary["policy_label"] == "local_2d_detector_slot_component_assembly_probe_cpu_no_fwi"
    assert summary["best_all_target_slot_case_count"] == 1
    assert summary["best_mean_target_slot_hit_count"] == 3.0
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"

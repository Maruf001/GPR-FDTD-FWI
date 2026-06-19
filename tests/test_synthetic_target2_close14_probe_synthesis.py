from pathlib import Path

from run_synthetic_target2_close14_probe_synthesis import (
    confidence_paths,
    seed_from_text,
    summarize_probe,
    synthesize_rows,
)


def test_seed_from_text_reads_seed_suffix():
    assert seed_from_text("noise15p361328125_seed21") == 21
    assert seed_from_text("coordinate_optimizer_close14_seed34_sources5") == 34
    assert seed_from_text("missing") is None


def test_confidence_paths_filters_probe_seeds(tmp_path):
    kept = tmp_path / "1294_coordinate_optimizer_close14_seed13_sources5_txrx45_noise15p361328125_objectives/data"
    kept.mkdir(parents=True)
    (kept / "coordinate_confidence_report.csv").write_text("x\n", encoding="utf-8")
    skipped = tmp_path / "999_coordinate_optimizer_close14_seed99_sources5_txrx45_noise15p361328125_objectives/data"
    skipped.mkdir(parents=True)
    (skipped / "coordinate_confidence_report.csv").write_text("x\n", encoding="utf-8")

    paths = confidence_paths([str(tmp_path / "*/data/coordinate_confidence_report.csv")])

    assert paths == [kept / "coordinate_confidence_report.csv"]


def test_synthesize_rows_marks_half_threshold_near_tie(tmp_path):
    path = tmp_path / "coordinate_confidence_report.csv"
    path.write_text(
        "\n".join(
            [
                "run_name,case_label,best_x_mm,best_z_mm,best_radius_mm,competing_geometry_x_mm,"
                "competing_geometry_z_mm,competing_geometry_radius_mm,radius_margin_abs,best_misfit,"
                "competing_geometry_misfit,ambiguity_misfit_threshold,ambiguity_x_min_mm,"
                "ambiguity_x_max_mm,confidence_label",
                "run_seed13,noise_seed13,264,90,8,265,90,8,0.002,1.0,1.03,1.08,264,265,strong",
                "run_seed21,noise_seed21,264,90,8,265,90,8,0.002,1.0,1.05,1.08,264,265,strong",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    rows = synthesize_rows([Path(path)])

    assert rows[0]["near_tie_at_scale_0p5"] is True
    assert rows[1]["near_tie_at_scale_0p5"] is False
    assert rows[1]["near_tie_at_scale_1p0"] is True


def test_summarize_probe_labels_persistent_truth_strong_near_ties():
    rows = [
        {
            "seed": 13,
            "confidence_label": "strong",
            "is_truth_geometry": True,
            "ambiguity_x_width_mm": 1.0,
            "near_tie_at_scale_0p5": True,
            "near_tie_at_scale_1p0": True,
            "competing_geometry_x_mm": 265.0,
            "radius_margin_abs": 0.002,
        },
        {
            "seed": 21,
            "confidence_label": "strong",
            "is_truth_geometry": True,
            "ambiguity_x_width_mm": 1.0,
            "near_tie_at_scale_0p5": True,
            "near_tie_at_scale_1p0": True,
            "competing_geometry_x_mm": 265.0,
            "radius_margin_abs": 0.001,
        },
    ]

    summary = summarize_probe(rows)

    assert summary["policy_label"] == "target2_close14_source5_txrx45_three_seed_persistent_x_near_tie"
    assert summary["truth_geometry_count"] == 2
    assert summary["near_tie_count_at_scale_0p5"] == 2
    assert summary["competing_geometry_x_values_mm"] == "265.0"

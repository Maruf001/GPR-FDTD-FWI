from run_seed21_fitted_ringdown_summary import (
    best_truth_preserving_diagnostics,
    normalize_label,
    summarize_seed21_package,
    target_summary_rows,
    write_figure_notes,
)


def test_best_truth_preserving_diagnostics_ignores_wrong_geometry():
    rows = [
        {
            "target_index": 0,
            "objective_label": "late_high",
            "variant_is_truth_geometry": False,
            "margin_ratio_to_base": 3.0,
        },
        {
            "target_index": 0,
            "objective_label": "veryhigh",
            "variant_is_truth_geometry": True,
            "margin_ratio_to_base": 1.25,
        },
    ]

    winners = best_truth_preserving_diagnostics(rows)

    assert winners[0]["objective_label"] == "veryhigh"


def test_target_summary_rows_attach_best_truth_preserving_objective():
    base_rows = [
        {
            "target_index": 1,
            "case_label": "case",
            "best_x_mm": 250.0,
            "best_z_mm": 100.0,
            "best_radius_mm": 6.0,
            "truth_x_mm": 250.0,
            "truth_z_mm": 100.0,
            "truth_radius_mm": 6.0,
            "is_truth_geometry": True,
            "confidence_label": "moderate",
            "radius_margin_abs": 7.0e-4,
            "radius_margin_rel": 0.02,
        }
    ]
    ratio_rows = [
        {
            "target_index": 1,
            "objective_label": "veryhigh",
            "variant_is_truth_geometry": True,
            "variant_margin_abs": 7.2e-4,
            "margin_ratio_to_base": 1.02,
        },
        {
            "target_index": 1,
            "objective_label": "late_high",
            "variant_is_truth_geometry": True,
            "variant_margin_abs": 9.0e-4,
            "margin_ratio_to_base": 1.28,
        },
    ]

    rows = target_summary_rows(base_rows, ratio_rows)

    assert rows[0]["base_is_truth_geometry"] is True
    assert rows[0]["best_truth_preserving_objective"] == "late_high"
    assert rows[0]["best_truth_preserving_ratio_to_base"] == 1.28


def test_summarize_seed21_package_counts_base_truth_and_objectives():
    target_rows = [
        {
            "base_is_truth_geometry": True,
            "base_confidence_label": "moderate",
            "best_truth_preserving_objective": "veryhigh",
        },
        {
            "base_is_truth_geometry": True,
            "base_confidence_label": "moderate",
            "best_truth_preserving_objective": "late_high",
        },
    ]
    ratio_rows = [
        {
            "objective_label": "veryhigh",
            "variant_is_truth_geometry": True,
            "base_is_truth_geometry": True,
            "variant_changes_geometry": False,
            "margin_ratio_to_base": 1.1,
        }
    ]
    confidence_rows = [
        {
            "objective_label": "base",
            "is_truth_geometry": True,
            "confidence_label": "moderate",
            "ambiguity_x_min_mm": 1.0,
            "ambiguity_x_max_mm": 1.0,
            "ambiguity_z_min_mm": 2.0,
            "ambiguity_z_max_mm": 2.0,
            "ambiguity_radius_min_mm": 3.0,
            "ambiguity_radius_max_mm": 3.0,
            "radius_margin_abs": 0.001,
        }
    ]

    summary = summarize_seed21_package(target_rows, ratio_rows, confidence_rows)

    assert summary["target_count"] == 2
    assert summary["base_truth_count"] == 2
    assert summary["base_confidence_label_counts"] == {"moderate": 2}
    assert summary["best_truth_preserving_objective_counts"] == {
        "veryhigh": 1,
        "late_high": 1,
    }


def test_normalize_label_rejects_path_separators():
    assert normalize_label("seed89") == "seed89"

    try:
        normalize_label("../seed89")
    except ValueError as exc:
        assert "unsupported" in str(exc)
    else:
        raise AssertionError("expected label validation to reject path separators")


def test_write_figure_notes_uses_labelled_filenames(tmp_path):
    summary = {
        "base_truth_count": 3,
        "target_count": 3,
        "base_confidence_label_counts": {"moderate": 3},
        "best_truth_preserving_objective_counts": {"veryhigh": 1, "late_high": 2},
    }
    path = tmp_path / "FIGURE_NOTES.md"

    write_figure_notes(path, summary, label="seed89")

    text = path.read_text(encoding="utf-8")
    assert "`seed89_base_margins_by_target.png`" in text
    assert "`seed89_objective_ratios_by_target.png`" in text
    assert "seed89 source-mismatch/ringdown stress" in text

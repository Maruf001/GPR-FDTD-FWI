from pathlib import Path

import pytest

import run_experiment_700_1218_holistic_report as report


def test_configure_report_scope_sets_range_specific_paths(tmp_path):
    original = (
        report.RUN_MIN,
        report.RUN_MAX,
        report.CUTOFF,
        report.REPORT_DATE,
        report.REPORT_STEM,
        report.REPORT_DIR,
        report.NOTEBOOK_PATH,
    )
    try:
        report.configure_report_scope(
            run_min=700,
            run_max=1257,
            cutoff=6.0e-4,
            report_date="2026-06-17",
            report_dir=tmp_path / "summary",
            notebook_path=tmp_path / "report.ipynb",
        )

        assert report.RUN_RANGE_LABEL == "700_1257"
        assert report.CUTOFF == 6.0e-4
        assert report.DATA_DIR == tmp_path / "summary" / "data"
        assert report.FIG_DIR == tmp_path / "summary" / "figures"
        assert report.SERIES_FIG_DIR == tmp_path / "summary" / "figures" / "series_charts"
        assert report.NOTEBOOK_PATH == tmp_path / "report.ipynb"
        assert report.ranged_csv_name("coordinate_run_summary") == (
            "coordinate_run_summary_700_1257.csv"
        )
    finally:
        (
            run_min,
            run_max,
            cutoff,
            report_date,
            report_stem,
            report_dir,
            notebook_path,
        ) = original
        report.configure_report_scope(
            run_min=run_min,
            run_max=run_max,
            cutoff=cutoff,
            report_date=report_date,
            report_stem=report_stem,
            report_dir=report_dir,
            notebook_path=notebook_path,
        )


def test_configure_report_scope_rejects_inverted_range():
    with pytest.raises(ValueError, match="run_min must be <= run_max"):
        report.configure_report_scope(run_min=1257, run_max=700)


def test_primary_objective_metadata_detects_late_high_primary():
    summary = {
        "diagnostic_objective_variants": [
            {
                "label": "base",
                "t_start_ns": 1.5,
                "t_end_ns": 5.5,
                "taper_ns": 0.2,
                "low_ghz": 1.1,
                "high_ghz": 3.4,
                "band_taper_ghz": 0.15,
            }
        ]
    }

    meta = report.primary_objective_metadata(summary)

    assert meta["primary_objective_label"] == "base"
    assert meta["primary_objective_family"] == "late_high_primary"
    assert meta["base_margin_is_canonical"] is False


def test_canonical_base_policy_runs_excludes_noncanonical_primary():
    df = report.pd.DataFrame(
        [
            {"run_id": 1, "base_margin_is_canonical": True},
            {"run_id": 2, "base_margin_is_canonical": False},
        ]
    )

    filtered = report.canonical_base_policy_runs(df)

    assert filtered["run_id"].tolist() == [1]

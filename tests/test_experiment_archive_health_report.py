from pathlib import Path

from run_experiment_archive_health_report import (
    classify_run_name,
    collect_runs,
    inspect_run,
    range_label,
    summarize_runs,
)


def _run_dir(root: Path, name: str, *, data=False, figures=False, notes=False, image=False):
    path = root / name
    path.mkdir()
    (path / "run_manifest.json").write_text("{}\n", encoding="utf-8")
    if data:
        (path / "data").mkdir()
        (path / "data" / "summary.json").write_text("{}\n", encoding="utf-8")
    if figures:
        (path / "figures").mkdir()
        if notes:
            (path / "figures" / "FIGURE_NOTES.md").write_text("# Notes\n", encoding="utf-8")
        if image:
            (path / "figures" / "plot.png").write_bytes(b"not a real png")
    return path


def test_classify_run_name_separates_physics_from_checkpoint():
    assert classify_run_name("coordinate_optimizer_variable_depth_radius") == "physics_or_diagnostic"
    assert classify_run_name("current_archive_coverage_refresh_state_audit") == "reporting_audit_checkpoint"
    assert classify_run_name("variable_depth_radius_seed_summary") == "analysis_report"


def test_range_label_uses_pace_change_bins():
    assert range_label(430) == "001-430"
    assert range_label(431) == "431-534"
    assert range_label(535) == "535-730"
    assert range_label(731) == "731+"


def test_inspect_run_flags_physics_without_data_and_missing_figure_notes(tmp_path):
    run = _run_dir(
        tmp_path,
        "001_coordinate_optimizer_test",
        data=False,
        figures=True,
        notes=False,
        image=True,
    )

    row = inspect_run(run)

    assert row["category"] == "physics_or_diagnostic"
    assert "physics_or_diagnostic_missing_data_dir" in row["issues"]
    assert "figure_images_missing_figure_notes" in row["issues"]


def test_collect_and_summarize_runs_counts_artifact_coverage(tmp_path):
    _run_dir(tmp_path, "001_coordinate_optimizer_test", data=True, figures=True, notes=True, image=True)
    _run_dir(tmp_path, "535_next_action_queue_test", data=False)
    _run_dir(tmp_path, "731_commit_pr_summary_test", data=True)

    rows = collect_runs(tmp_path)
    summary = summarize_runs(rows)

    assert [row["run_number"] for row in rows] == [1, 535, 731]
    assert summary["by_range"]["001-430"]["run_count"] == 1
    assert summary["by_range"]["535-730"]["run_count"] == 1
    assert summary["by_range"]["731+"]["run_count"] == 1
    assert summary["by_range"]["001-430"]["with_figure_notes"] == 1

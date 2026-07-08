from pathlib import Path

from run_archive_location_clean_metric_audit import (
    aggregate_csv_paths,
    metric_rows_from_aggregates,
    summarize_archive_metric,
)


def test_aggregate_csv_paths_excludes_smoke_by_default(tmp_path):
    real = tmp_path / "123_real" / "data"
    smoke = tmp_path / "456_smoke" / "data"
    real.mkdir(parents=True)
    smoke.mkdir(parents=True)
    (real / "coordinate_confidence_aggregate.csv").write_text("a\n", encoding="utf-8")
    (smoke / "coordinate_confidence_aggregate.csv").write_text("a\n", encoding="utf-8")

    paths = aggregate_csv_paths(tmp_path)

    assert paths == [real / "coordinate_confidence_aggregate.csv"]
    assert len(aggregate_csv_paths(tmp_path, include_smoke=True)) == 2


def test_metric_rows_from_aggregates_marks_exact_strong_ambiguities(tmp_path):
    csv_path = tmp_path / "100_metric" / "data" / "coordinate_confidence_aggregate.csv"
    csv_path.parent.mkdir(parents=True)
    csv_path.write_text(
        "\n".join([
            "run_name,case_label,step_target_index,sources,tx_rx_offset_mm,confidence_label,is_truth_geometry,ambiguity_x_width_mm,ambiguity_z_width_mm,ambiguity_radius_width_mm",
            "run_a,case_a,2,4,29.5,strong,True,1,0,0",
            "run_b,case_b,2,4,29.5,strong,True,0,0,0",
        ])
        + "\n",
        encoding="utf-8",
    )

    rows = metric_rows_from_aggregates([csv_path])

    assert rows[0]["exact_strong_x_ambiguous"] is True
    assert rows[0]["strict_location_clean_strong"] is False
    assert rows[1]["strict_location_clean_strong"] is True


def test_summarize_archive_metric_counts_location_clean_fraction():
    rows = [
        {
            "truth_geometry_match": True,
            "strong_confidence": True,
            "strict_location_clean_strong": True,
            "exact_strong_x_ambiguous": False,
            "exact_strong_z_ambiguous": False,
            "exact_strong_radius_ambiguous": False,
            "x_ambiguity_width_mm": 0.0,
        },
        {
            "truth_geometry_match": True,
            "strong_confidence": True,
            "strict_location_clean_strong": False,
            "exact_strong_x_ambiguous": True,
            "exact_strong_z_ambiguous": False,
            "exact_strong_radius_ambiguous": False,
            "x_ambiguity_width_mm": 1.0,
        },
    ]

    summary = summarize_archive_metric(rows, aggregate_file_count=1, include_smoke=False)

    assert summary["policy_label"] == "archive_location_clean_metric_x_ambiguity_present_cpu_no_gpu"
    assert summary["exact_strong_row_count"] == 2
    assert summary["strict_location_clean_strong_count"] == 1
    assert summary["exact_strong_x_ambiguous_count"] == 1
    assert summary["exact_strong_location_clean_fraction"] == 0.5
    assert summary["gpu_priority"] == "none_now"

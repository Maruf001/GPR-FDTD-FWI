import json

from run_gssi_field_publication_bundle_freshness_audit import (
    build_candidate_rows,
    summarize_freshness,
)


def _write_summary(root, run, name, summary):
    data_dir = root / run / "data"
    data_dir.mkdir(parents=True)
    (data_dir / name).write_text(json.dumps(summary), encoding="utf-8")


def test_bundle_freshness_identifies_current_candidates_outside_curated_bundle(tmp_path):
    figure_a = tmp_path / "124" / "figures" / "a.png"
    figure_b = tmp_path / "126" / "figures" / "b.png"
    figure_a.parent.mkdir(parents=True)
    figure_b.parent.mkdir(parents=True)
    figure_a.write_bytes(b"png")
    figure_b.write_bytes(b"png")

    _write_summary(
        tmp_path,
        "124_run",
        "waveform.json",
        {
            "policy_label": "waveform",
            "min_corr": 0.94,
            "ready_for_waveform_morphology_qc": True,
            "ready_for_field_fwi": False,
            "paths": {"figure": str(figure_a)},
        },
    )
    _write_summary(
        tmp_path,
        "126_run",
        "signed.json",
        {
            "policy_label": "signed",
            "min_signed": 0.93,
            "ready_for_signed_waveform_morphology_qc": True,
            "ready_for_field_fwi": False,
            "paths": {"figure": str(figure_b)},
        },
    )
    candidates = [
        {
            "figure_key": "waveform",
            "source_run": "124_run",
            "summary_name": "waveform.json",
            "metric_label": "min_corr",
            "metric_key": "min_corr",
            "ready_key": "ready_for_waveform_morphology_qc",
            "role": "guardrail_refresh_candidate",
            "allowed_use": "waveform QC",
        },
        {
            "figure_key": "signed",
            "source_run": "126_run",
            "summary_name": "signed.json",
            "metric_label": "min_signed",
            "metric_key": "min_signed",
            "ready_key": "ready_for_signed_waveform_morphology_qc",
            "role": "primary_refresh_candidate",
            "allowed_use": "signed QC",
        },
    ]
    bundle_rows = [{"figure_key": "old", "source_run": "old_run"}]

    rows = build_candidate_rows(tmp_path, bundle_rows, candidates)
    summary = summarize_freshness(bundle_rows, rows, "bundle")

    assert [row["figure_key"] for row in rows] == ["waveform", "signed"]
    assert all(row["figure_exists"] for row in rows)
    assert not any(row["already_in_current_bundle"] for row in rows)
    assert summary["current_bundle_figure_count"] == 1
    assert summary["candidate_figure_count"] == 2
    assert summary["candidate_already_in_bundle_count"] == 0
    assert summary["candidate_missing_figure_count"] == 0
    assert summary["candidate_qc_ready_count"] == 2
    assert summary["primary_refresh_candidate_count"] == 1
    assert summary["guardrail_refresh_candidate_count"] == 1
    assert summary["ready_for_curated_bundle_refresh_decision"]
    assert not summary["automatic_bundle_refresh_ready"]
    assert not summary["ready_for_field_fwi"]
    assert summary["gpu_priority"] == "none"


def test_bundle_freshness_detects_existing_bundle_membership_by_source_run(tmp_path):
    figure = tmp_path / "126" / "figures" / "b.png"
    figure.parent.mkdir(parents=True)
    figure.write_bytes(b"png")
    _write_summary(
        tmp_path,
        "126_run",
        "signed.json",
        {
            "policy_label": "signed",
            "min_signed": 0.93,
            "ready_for_signed_waveform_morphology_qc": True,
            "ready_for_field_fwi": False,
            "paths": {"figure": str(figure)},
        },
    )
    rows = build_candidate_rows(
        tmp_path,
        [{"figure_key": "different_key", "source_run": "126_run"}],
        [
            {
                "figure_key": "signed",
                "source_run": "126_run",
                "summary_name": "signed.json",
                "metric_label": "min_signed",
                "metric_key": "min_signed",
                "ready_key": "ready_for_signed_waveform_morphology_qc",
                "role": "primary_refresh_candidate",
                "allowed_use": "signed QC",
            }
        ],
    )

    assert rows[0]["already_in_current_bundle"]

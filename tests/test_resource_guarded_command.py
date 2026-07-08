import json
import math

from run_resource_guarded_command import (
    PREFLIGHT_EXIT_CODE,
    ResourceSample,
    cap_violation,
    parse_nvidia_smi_csv,
    ram_used_percent_from_meminfo,
    run_guarded,
    summarize_samples,
)


def test_ram_used_percent_uses_memavailable():
    meminfo = "\n".join(
        [
            "MemTotal:       1000000 kB",
            "MemFree:         100000 kB",
            "MemAvailable:    250000 kB",
        ]
    )

    assert ram_used_percent_from_meminfo(meminfo) == 75.0


def test_parse_nvidia_smi_csv_accepts_na_memory_on_gb10():
    util, used, total = parse_nvidia_smi_csv("6, [N/A], [N/A]\n")

    assert util == 6.0
    assert used is None
    assert total is None


def test_cap_violation_reports_ram_and_gpu_limits():
    ram_sample = ResourceSample(
        timestamp_s=0.0,
        elapsed_s=0.0,
        ram_used_percent=81.0,
        gpu_util_percent=50.0,
        gpu_memory_used_mib=None,
        gpu_memory_total_mib=None,
    )
    gpu_sample = ResourceSample(
        timestamp_s=0.0,
        elapsed_s=0.0,
        ram_used_percent=20.0,
        gpu_util_percent=91.0,
        gpu_memory_used_mib=None,
        gpu_memory_total_mib=None,
    )

    assert "ram_used_percent" in cap_violation(ram_sample, 80.0, 90.0)
    assert "gpu_util_percent" in cap_violation(gpu_sample, 80.0, 90.0)


def test_summarize_samples_records_peaks_and_abort_reason():
    samples = [
        ResourceSample(10.0, 0.0, 12.5, 6.0, None, None),
        ResourceSample(11.0, 1.0, 13.5, 87.0, None, None, "gpu_util_percent=91.00 > 90.00"),
    ]

    summary = summarize_samples(samples, ["echo", "ok"], 124, True)

    assert summary["aborted"] is True
    assert summary["sample_count"] == 2
    assert summary["max_ram_used_percent"] == 13.5
    assert summary["max_gpu_util_percent"] == 87.0
    assert summary["abort_reasons"] == ["gpu_util_percent=91.00 > 90.00"]


def test_run_guarded_preflight_violation_writes_summary(monkeypatch, tmp_path):
    def fake_sample(_start):
        return ResourceSample(
            timestamp_s=1.0,
            elapsed_s=0.0,
            ram_used_percent=90.0,
            gpu_util_percent=6.0,
            gpu_memory_used_mib=None,
            gpu_memory_total_mib=None,
        )

    monkeypatch.setattr("run_resource_guarded_command.sample_resources", fake_sample)
    summary_path = tmp_path / "summary.json"
    log_path = tmp_path / "monitor.jsonl"

    returncode = run_guarded(
        ["python", "-c", "print('should not run')"],
        max_ram_percent=80.0,
        max_gpu_util_percent=90.0,
        poll_interval_s=0.1,
        terminate_grace_s=0.1,
        log_jsonl=log_path,
        summary_json=summary_path,
    )

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    log_rows = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]

    assert returncode == PREFLIGHT_EXIT_CODE
    assert summary["aborted"] is True
    assert math.isclose(summary["max_ram_used_percent"], 90.0)
    assert log_rows[0]["abort_reason"].startswith("preflight:")

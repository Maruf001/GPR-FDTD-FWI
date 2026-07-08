#!/usr/bin/env python3
"""Run a command while enforcing host RAM and GPU-utilization ceilings."""

from __future__ import annotations

import argparse
import json
import math
import os
import signal
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path


ABORT_EXIT_CODE = 124
PREFLIGHT_EXIT_CODE = 99


@dataclass
class ResourceSample:
    timestamp_s: float
    elapsed_s: float
    ram_used_percent: float
    gpu_util_percent: float | None
    gpu_memory_used_mib: float | None
    gpu_memory_total_mib: float | None
    abort_reason: str = ""


def parse_meminfo(text: str) -> tuple[float, float]:
    values: dict[str, float] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, rest = line.split(":", 1)
        parts = rest.strip().split()
        if not parts:
            continue
        try:
            values[key] = float(parts[0])
        except ValueError:
            continue
    total = values.get("MemTotal", math.nan)
    available = values.get("MemAvailable", values.get("MemFree", math.nan))
    return total, available


def ram_used_percent_from_meminfo(text: str) -> float:
    total_kib, available_kib = parse_meminfo(text)
    if not math.isfinite(total_kib) or total_kib <= 0.0:
        return math.nan
    if not math.isfinite(available_kib):
        return math.nan
    used = max(0.0, total_kib - available_kib)
    return 100.0 * used / total_kib


def parse_optional_float(value: str) -> float | None:
    text = str(value).strip()
    if not text or text.upper() == "N/A" or text.startswith("[N/A]"):
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def parse_nvidia_smi_csv(text: str) -> tuple[float | None, float | None, float | None]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return None, None, None
    parts = [part.strip() for part in lines[0].split(",")]
    util = parse_optional_float(parts[0]) if len(parts) > 0 else None
    memory_used = parse_optional_float(parts[1]) if len(parts) > 1 else None
    memory_total = parse_optional_float(parts[2]) if len(parts) > 2 else None
    return util, memory_used, memory_total


def query_gpu() -> tuple[float | None, float | None, float | None]:
    try:
        completed = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=utilization.gpu,memory.used,memory.total",
                "--format=csv,noheader,nounits",
            ],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=5.0,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None, None, None
    if completed.returncode != 0:
        return None, None, None
    return parse_nvidia_smi_csv(completed.stdout)


def sample_resources(start_time_s: float) -> ResourceSample:
    meminfo = Path("/proc/meminfo").read_text(encoding="utf-8")
    gpu_util, gpu_memory_used, gpu_memory_total = query_gpu()
    now = time.time()
    return ResourceSample(
        timestamp_s=now,
        elapsed_s=now - start_time_s,
        ram_used_percent=ram_used_percent_from_meminfo(meminfo),
        gpu_util_percent=gpu_util,
        gpu_memory_used_mib=gpu_memory_used,
        gpu_memory_total_mib=gpu_memory_total,
    )


def cap_violation(sample: ResourceSample, max_ram_percent: float, max_gpu_util_percent: float | None) -> str:
    if math.isfinite(sample.ram_used_percent) and sample.ram_used_percent > max_ram_percent:
        return f"ram_used_percent={sample.ram_used_percent:.2f} > {max_ram_percent:.2f}"
    if (
        max_gpu_util_percent is not None
        and sample.gpu_util_percent is not None
        and sample.gpu_util_percent > max_gpu_util_percent
    ):
        return f"gpu_util_percent={sample.gpu_util_percent:.2f} > {max_gpu_util_percent:.2f}"
    return ""


def terminate_process_group(process: subprocess.Popen, grace_s: float) -> None:
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    deadline = time.time() + grace_s
    while time.time() < deadline:
        if process.poll() is not None:
            return
        time.sleep(0.1)
    if process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            return


def write_jsonl(path: Path | None, sample: ResourceSample) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(sample), sort_keys=True) + "\n")


def summarize_samples(samples: list[ResourceSample], command: list[str], returncode: int, aborted: bool) -> dict:
    return {
        "command": command,
        "returncode": returncode,
        "aborted": aborted,
        "sample_count": len(samples),
        "elapsed_s": samples[-1].elapsed_s if samples else 0.0,
        "max_ram_used_percent": max((sample.ram_used_percent for sample in samples), default=math.nan),
        "max_gpu_util_percent": max(
            (sample.gpu_util_percent for sample in samples if sample.gpu_util_percent is not None),
            default=None,
        ),
        "max_gpu_memory_used_mib": max(
            (sample.gpu_memory_used_mib for sample in samples if sample.gpu_memory_used_mib is not None),
            default=None,
        ),
        "abort_reasons": [sample.abort_reason for sample in samples if sample.abort_reason],
    }


def run_guarded(
    command: list[str],
    *,
    max_ram_percent: float,
    max_gpu_util_percent: float | None,
    poll_interval_s: float,
    terminate_grace_s: float,
    log_jsonl: Path | None,
    summary_json: Path | None,
) -> int:
    start = time.time()
    samples: list[ResourceSample] = []
    preflight = sample_resources(start)
    reason = cap_violation(preflight, max_ram_percent, max_gpu_util_percent)
    if reason:
        preflight.abort_reason = f"preflight: {reason}"
        samples.append(preflight)
        write_jsonl(log_jsonl, preflight)
        summary = summarize_samples(samples, command, PREFLIGHT_EXIT_CODE, True)
        if summary_json is not None:
            summary_json.parent.mkdir(parents=True, exist_ok=True)
            summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return PREFLIGHT_EXIT_CODE

    process = subprocess.Popen(command, preexec_fn=os.setsid)
    aborted = False
    returncode = 0
    while True:
        sample = sample_resources(start)
        reason = cap_violation(sample, max_ram_percent, max_gpu_util_percent)
        if reason:
            sample.abort_reason = reason
            aborted = True
            samples.append(sample)
            write_jsonl(log_jsonl, sample)
            terminate_process_group(process, terminate_grace_s)
            returncode = ABORT_EXIT_CODE
            break
        samples.append(sample)
        write_jsonl(log_jsonl, sample)
        child_returncode = process.poll()
        if child_returncode is not None:
            returncode = child_returncode
            break
        time.sleep(max(0.1, poll_interval_s))

    summary = summarize_samples(samples, command, returncode, aborted)
    if summary_json is not None:
        summary_json.parent.mkdir(parents=True, exist_ok=True)
        summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-ram-percent", type=float, default=80.0)
    parser.add_argument("--max-gpu-util-percent", type=float, default=90.0)
    parser.add_argument("--no-gpu-util-cap", action="store_true")
    parser.add_argument("--poll-interval-s", type=float, default=5.0)
    parser.add_argument("--terminate-grace-s", type=float, default=10.0)
    parser.add_argument("--log-jsonl", default=None)
    parser.add_argument("--summary-json", default=None)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command:
        parser.error("command is required after --")
    return args


def main() -> None:
    args = parse_args()
    max_gpu_util_percent = None if args.no_gpu_util_cap else args.max_gpu_util_percent
    returncode = run_guarded(
        args.command,
        max_ram_percent=args.max_ram_percent,
        max_gpu_util_percent=max_gpu_util_percent,
        poll_interval_s=args.poll_interval_s,
        terminate_grace_s=args.terminate_grace_s,
        log_jsonl=None if args.log_jsonl is None else Path(args.log_jsonl),
        summary_json=None if args.summary_json is None else Path(args.summary_json),
    )
    raise SystemExit(returncode)


if __name__ == "__main__":
    main()

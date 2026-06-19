#!/usr/bin/env python3
"""Map saved close-spacing source-density evidence without launching simulations."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import (  # noqa: E402
    read_json,
    safe_float,
    safe_int,
)


DEFAULT_SOURCE_SPECS = (
    {
        "label": "close50_txrx40_source3_4_5_three_seed_synthesis",
        "kind": "replicate_rows",
        "path": (
            "outputs/summary_tables/099_close50_source_count_replicate_synthesis/"
            "data/close50_source_count_replicate_rows.csv"
        ),
        "spacing_mm": 50.0,
        "evidence_scope": "matched_source_count_transition",
    },
    {
        "label": "close25_sources4_txrx40_three_seed",
        "kind": "aggregate",
        "path": (
            "outputs/experiments/310_coordinate_confidence_close25_sources4_txrx40_seed_replicates/"
            "data/coordinate_confidence_aggregate.csv"
        ),
        "spacing_mm": 25.0,
        "evidence_scope": "three_seed_source4_context",
    },
    {
        "label": "close25_sources4_txrx45_three_seed",
        "kind": "aggregate",
        "path": (
            "outputs/experiments/323_coordinate_confidence_close25_sources4_txrx45_seed_replicates/"
            "data/coordinate_confidence_aggregate.csv"
        ),
        "spacing_mm": 25.0,
        "evidence_scope": "three_seed_source4_context",
    },
    {
        "label": "close28_sources4_txrx35_three_seed",
        "kind": "aggregate",
        "path": (
            "outputs/experiments/314_coordinate_confidence_close28_sources4_txrx35_seed_replicates/"
            "data/coordinate_confidence_aggregate.csv"
        ),
        "spacing_mm": 28.0,
        "evidence_scope": "three_seed_source4_context",
    },
    {
        "label": "close28_sources4_txrx45_three_seed",
        "kind": "aggregate",
        "path": (
            "outputs/experiments/319_coordinate_confidence_close28_sources4_txrx45_seed_replicates/"
            "data/coordinate_confidence_aggregate.csv"
        ),
        "spacing_mm": 28.0,
        "evidence_scope": "three_seed_source4_context",
    },
    {
        "label": "close14_sources4_txrx45_three_seed",
        "kind": "aggregate",
        "path": (
            "outputs/experiments/335_coordinate_confidence_close14_sources4_txrx45_seed_replicates/"
            "data/coordinate_confidence_aggregate.csv"
        ),
        "spacing_mm": 14.0,
        "evidence_scope": "three_seed_source4_context",
    },
    {
        "label": "close14_sources3_txrx45_seed34",
        "kind": "optimizer_summary",
        "path": (
            "outputs/experiments/336_coordinate_optimizer_close14_seed34_sources3_txrx45_objectives/"
            "data/multi_rebar_coordinate_optimizer_summary.json"
        ),
        "spacing_mm": 14.0,
        "evidence_scope": "three_seed_source3_near_exact_context",
    },
    {
        "label": "close14_sources3_txrx45_seed13",
        "kind": "optimizer_summary",
        "path": (
            "outputs/experiments/1346_coordinate_optimizer_close14_seed13_sources3_txrx45_objectives/"
            "data/multi_rebar_coordinate_optimizer_summary.json"
        ),
        "spacing_mm": 14.0,
        "evidence_scope": "three_seed_source3_near_exact_context",
    },
    {
        "label": "close14_sources3_txrx45_seed21",
        "kind": "optimizer_summary",
        "path": (
            "outputs/experiments/1347_coordinate_optimizer_close14_seed21_sources3_txrx45_objectives/"
            "data/multi_rebar_coordinate_optimizer_summary.json"
        ),
        "spacing_mm": 14.0,
        "evidence_scope": "three_seed_source3_near_exact_context",
    },
    {
        "label": "close14_sources4_5_7_txrx45_seed34_noise_boundary",
        "kind": "aggregate",
        "path": (
            "outputs/experiments/356_coordinate_confidence_close14_seed34_noise15p361328125_sources4_5_7_aggregate/"
            "data/coordinate_confidence_aggregate.csv"
        ),
        "spacing_mm": 14.0,
        "evidence_scope": "single_seed_source_count_noise_boundary_context",
    },
    {
        "label": "close14_sources5_txrx45_three_seed_noise_boundary",
        "kind": "aggregate",
        "path": (
            "outputs/experiments/1296_coordinate_confidence_close14_target2_sources5_txrx45_seed13_21_34_probe_aggregate/"
            "data/coordinate_confidence_aggregate.csv"
        ),
        "spacing_mm": 14.0,
        "evidence_scope": "three_seed_source5_noise_boundary_context",
    },
)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def seed_from_text(text: object) -> int:
    match = re.search(r"seed(\d+)", str(text))
    return int(match.group(1)) if match else -1


def case_kind(case_label: object) -> str:
    return "source_mismatch" if "source_mismatch" in str(case_label) else "nominal"


def truth_geometry(row: dict) -> bool:
    if "truth_geometry" in row:
        return boolish(row.get("truth_geometry"))
    if "is_truth_geometry" in row:
        return boolish(row.get("is_truth_geometry"))
    best_x = safe_float(row.get("best_x_mm"))
    best_z = safe_float(row.get("best_z_mm"))
    best_radius = safe_float(row.get("best_radius_mm"))
    truth_x = safe_float(row.get("truth_x_mm"))
    truth_z = safe_float(row.get("truth_z_mm"))
    truth_radius = safe_float(row.get("truth_radius_mm"))
    return (
        math.isfinite(best_x)
        and math.isfinite(best_z)
        and math.isfinite(best_radius)
        and math.isclose(best_x, truth_x, abs_tol=1.0e-9)
        and math.isclose(best_z, truth_z, abs_tol=1.0e-9)
        and math.isclose(best_radius, truth_radius, abs_tol=1.0e-9)
    )


def family_label(spacing_mm: float) -> str:
    return f"close{int(round(spacing_mm))}"


def _target2_aggregate_rows(rows: list[dict]) -> list[dict]:
    filtered = []
    for row in rows:
        if safe_int(row.get("pass_index"), -1) != 0:
            continue
        if row.get("step_kind") != "main":
            continue
        if safe_int(row.get("step_target_index"), safe_int(row.get("target_rebar_index"), -1)) != 2:
            continue
        filtered.append(row)
    return filtered


def _normalize_common(row: dict, spec: dict, source_path: Path) -> dict:
    spacing = safe_float(spec["spacing_mm"])
    truth = truth_geometry(row)
    truth_x = safe_float(row.get("truth_x_mm"))
    truth_radius = safe_float(row.get("truth_radius_mm"))
    best_x = safe_float(row.get("best_x_mm"))
    best_radius = safe_float(row.get("best_radius_mm"))
    source_count = safe_int(row.get("source_count", row.get("sources")), -1)
    return {
        "source_label": spec["label"],
        "source_path": str(source_path),
        "evidence_scope": spec["evidence_scope"],
        "family": family_label(spacing),
        "spacing_mm": spacing,
        "source_count": source_count,
        "tx_rx_offset_mm": safe_float(row.get("tx_rx_offset_mm")),
        "seed": safe_int(row.get("seed"), seed_from_text(row.get("case_label", row.get("run_name", "")))),
        "case_label": row.get("case_label", ""),
        "case_kind": case_kind(row.get("case_label", "")),
        "run_name": row.get("run_name", row.get("run_dir", "")),
        "best_x_mm": best_x,
        "best_z_mm": safe_float(row.get("best_z_mm")),
        "best_radius_mm": best_radius,
        "truth_x_mm": truth_x,
        "truth_z_mm": safe_float(row.get("truth_z_mm")),
        "truth_radius_mm": truth_radius,
        "x_abs_error_mm": safe_float(
            row.get("x_abs_error_mm"),
            abs(best_x - truth_x) if math.isfinite(best_x) and math.isfinite(truth_x) else math.nan,
        ),
        "radius_abs_error_mm": safe_float(
            row.get("radius_abs_error_mm"),
            abs(best_radius - truth_radius)
            if math.isfinite(best_radius) and math.isfinite(truth_radius)
            else math.nan,
        ),
        "truth_geometry": truth,
        "confidence_label": row.get("confidence_label", ""),
        "radius_margin_abs": safe_float(row.get("radius_margin_abs")),
        "best_misfit": safe_float(row.get("best_misfit")),
        "ambiguity_x_width_mm": ambiguity_width(row, "x"),
        "ambiguity_radius_width_mm": ambiguity_width(row, "radius"),
    }


def ambiguity_width(row: dict, axis: str) -> float:
    width = safe_float(row.get(f"ambiguity_{axis}_width_mm"))
    if math.isfinite(width):
        return width
    low = safe_float(row.get(f"ambiguity_{axis}_min_mm"))
    high = safe_float(row.get(f"ambiguity_{axis}_max_mm"))
    if math.isfinite(low) and math.isfinite(high):
        return high - low
    return math.nan


def load_replicate_rows(spec: dict) -> list[dict]:
    source_path = Path(spec["path"])
    return [_normalize_common(row, spec, source_path) for row in read_csv_rows(source_path)]


def load_aggregate_rows(spec: dict) -> list[dict]:
    source_path = Path(spec["path"])
    rows = _target2_aggregate_rows(read_csv_rows(source_path))
    return [_normalize_common(row, spec, source_path) for row in rows]


def load_optimizer_summary_rows(spec: dict) -> list[dict]:
    source_path = Path(spec["path"])
    summary = read_json(source_path)
    truth_x = float((summary.get("true_x_values_mm") or [math.nan, math.nan, math.nan])[2])
    truth_z = float((summary.get("true_z_values_mm") or [math.nan, math.nan, math.nan])[2])
    truth_radii = summary.get("truth_radius_values_mm") or [math.nan, math.nan, summary.get("truth_radius_mm")]
    truth_radius = float(truth_radii[2])
    report_path = source_path.with_name("coordinate_confidence_report.csv")
    rows = []
    for row in _target2_aggregate_rows(read_csv_rows(report_path)):
        enriched = dict(row)
        enriched.update(
            {
                "sources": summary.get("sources"),
                "tx_rx_offset_mm": summary.get("tx_rx_offset_mm"),
                "truth_x_mm": truth_x,
                "truth_z_mm": truth_z,
                "truth_radius_mm": truth_radius,
                "x_abs_error_mm": abs(safe_float(row.get("best_x_mm")) - truth_x),
                "radius_abs_error_mm": abs(safe_float(row.get("best_radius_mm")) - truth_radius),
            }
        )
        rows.append(_normalize_common(enriched, spec, report_path))
    return rows


def load_source_rows(specs: list[dict]) -> list[dict]:
    loaders = {
        "replicate_rows": load_replicate_rows,
        "aggregate": load_aggregate_rows,
        "optimizer_summary": load_optimizer_summary_rows,
    }
    rows: list[dict] = []
    for spec in specs:
        loader = loaders.get(str(spec["kind"]))
        if loader is None:
            raise ValueError(f"Unsupported source spec kind: {spec['kind']}")
        rows.extend(loader(spec))
    return rows


def summarize_groups(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        key = (
            row["family"],
            safe_float(row["spacing_mm"]),
            safe_int(row["source_count"]),
            safe_float(row["tx_rx_offset_mm"]),
            row["evidence_scope"],
        )
        grouped[key].append(row)

    summary_rows = []
    for key in sorted(grouped):
        family, spacing, source_count, tx_rx_offset, evidence_scope = key
        group = grouped[key]
        seeds = sorted({safe_int(row.get("seed")) for row in group if safe_int(row.get("seed"), -1) >= 0})
        label_counts = Counter(str(row.get("confidence_label", "")) for row in group)
        truth_count = sum(boolish(row.get("truth_geometry")) for row in group)
        wrong_x_count = sum(safe_float(row.get("x_abs_error_mm")) > 0.0 for row in group)
        margins = [safe_float(row.get("radius_margin_abs")) for row in group]
        finite_margins = [value for value in margins if math.isfinite(value)]
        x_widths = [safe_float(row.get("ambiguity_x_width_mm")) for row in group]
        finite_x_widths = [value for value in x_widths if math.isfinite(value)]
        max_x_error = max([safe_float(row.get("x_abs_error_mm")) for row in group] or [math.nan])
        max_radius_error = max([safe_float(row.get("radius_abs_error_mm")) for row in group] or [math.nan])
        truth_fraction = truth_count / len(group) if group else 0.0
        three_seed_exact = len(seeds) >= 3 and math.isclose(truth_fraction, 1.0)
        replicated_failure = (
            len(seeds) >= 3
            and math.isclose(truth_fraction, 0.0)
            and label_counts.get("weak", 0) == len(group)
            and max_x_error >= 1.0
        )
        near_exact_three_seed_context = (
            len(seeds) >= 3
            and truth_fraction >= (5.0 / 6.0)
            and label_counts.get("strong", 0) == len(group)
            and max_x_error <= 1.0
            and math.isclose(max_radius_error, 0.0)
        )
        if replicated_failure:
            evidence_role = "matched_three_seed_failure"
        elif three_seed_exact:
            evidence_role = "three_seed_exact_recovery"
        elif near_exact_three_seed_context:
            evidence_role = "three_seed_near_exact_context"
        elif len(seeds) == 1:
            evidence_role = "single_seed_context_only"
        else:
            evidence_role = "mixed_or_incomplete_context"

        summary_rows.append(
            {
                "family": family,
                "spacing_mm": spacing,
                "source_count": source_count,
                "tx_rx_offset_mm": tx_rx_offset,
                "evidence_scope": evidence_scope,
                "row_count": len(group),
                "seed_count": len(seeds),
                "seed_values": ",".join(str(seed) for seed in seeds),
                "truth_geometry_count": truth_count,
                "truth_geometry_fraction": truth_fraction,
                "strong_count": label_counts.get("strong", 0),
                "moderate_count": label_counts.get("moderate", 0),
                "weak_count": label_counts.get("weak", 0),
                "selected_wrong_x_count": wrong_x_count,
                "min_radius_margin_abs": min(finite_margins) if finite_margins else math.nan,
                "max_x_abs_error_mm": max_x_error,
                "max_radius_abs_error_mm": max_radius_error,
                "max_ambiguity_x_width_mm": max(finite_x_widths) if finite_x_widths else math.nan,
                "three_seed_exact": three_seed_exact,
                "three_seed_strong_exact": three_seed_exact and label_counts.get("strong", 0) == len(group),
                "three_seed_near_exact_context": near_exact_three_seed_context,
                "replicated_failure": replicated_failure,
                "evidence_role": evidence_role,
            }
        )
    return summary_rows


def synthesize_policy(group_rows: list[dict]) -> dict:
    by_key = {
        (
            row["family"],
            safe_int(row["source_count"]),
            safe_float(row["tx_rx_offset_mm"]),
            row["evidence_scope"],
        ): row
        for row in group_rows
    }
    close50_source3_failure = any(
        row["family"] == "close50" and safe_int(row["source_count"]) == 3 and boolish(row["replicated_failure"])
        for row in group_rows
    )
    close50_source4_exact = any(
        row["family"] == "close50" and safe_int(row["source_count"]) == 4 and boolish(row["three_seed_exact"])
        for row in group_rows
    )
    close50_source5_exact = any(
        row["family"] == "close50" and safe_int(row["source_count"]) == 5 and boolish(row["three_seed_exact"])
        for row in group_rows
    )
    context_source3_rows = [
        row
        for row in group_rows
        if row["family"] != "close50" and safe_int(row["source_count"]) == 3
    ]
    incomplete_source3_families = sorted(
        {
            row["family"]
            for row in context_source3_rows
            if safe_int(row.get("seed_count")) < 3
        }
    )
    three_seed_context_exact_count = sum(
        boolish(row.get("three_seed_exact")) and row["family"] != "close50" for row in group_rows
    )
    near_exact_source3_context_families = sorted(
        {
            row["family"]
            for row in context_source3_rows
            if boolish(row.get("three_seed_near_exact_context"))
        }
    )
    source_count_transition_supported = (
        close50_source3_failure and close50_source4_exact and close50_source5_exact
    )
    return {
        "policy_label": "close_spacing_source_density_archive_map",
        "group_count": len(group_rows),
        "source_count_transition_supported_for_close50_txrx40": source_count_transition_supported,
        "close50_source3_three_seed_failure": close50_source3_failure,
        "close50_source4_three_seed_exact": close50_source4_exact,
        "close50_source5_three_seed_exact": close50_source5_exact,
        "three_seed_context_exact_group_count_outside_close50": three_seed_context_exact_count,
        "near_exact_nonclose50_source3_families": ",".join(near_exact_source3_context_families),
        "incomplete_nonclose50_source3_families": ",".join(incomplete_source3_families),
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_field_or_3d_work": False,
        "gpu_priority": "none",
        "recommended_next_local_mode": "field_packet_validation_or_cpu_baseline_contract",
        "decision": (
            "Saved close-spacing evidence supports a close50 Tx/Rx40 source-density transition: "
            "sources3 fails across seeds 13/21/34 while sources4 and sources5 recover the truth geometry. "
            "Close14 Tx/Rx45 source3 is now a three-seed near-exact context result, with strong radius-exact "
            "rows and only one 1 mm adjacent x-branch selection. Other close-spacing families provide "
            "source4/source5 exact-recovery context, but not a matched three-seed source3 failure transition. "
            "Do not launch a broad GPU queue from this map; treat the close50 source3 failure as "
            "spacing/acquisition-specific unless the manuscript needs cross-spacing generalization."
        ),
        "debug_key_count": len(by_key),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "broad source-density GPU sweep",
            "evidence": "close50 transition already closed; close14 source3 is near-exact context, not failure",
        },
        {
            "gate_key": "detector_seeded_fwi",
            "ready": summary["ready_for_detector_seeded_fwi"],
            "allowed_use": "none",
            "blocked_use": "detector-seeded FWI",
            "evidence": "archive map is coordinate source-density synthesis only",
        },
        {
            "gate_key": "field_or_3d_handoff",
            "ready": summary["ready_for_field_or_3d_work"],
            "allowed_use": "none",
            "blocked_use": "field FWI or 3D/HPC work",
            "evidence": "synthetic 2D archive map; field controls are separate",
        },
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--run-name", default="close_spacing_source_density_archive_map")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    specs = [dict(spec) for spec in DEFAULT_SOURCE_SPECS]
    evidence_rows = load_source_rows(specs)
    group_rows = summarize_groups(evidence_rows)
    summary = synthesize_policy(group_rows)
    gates = gate_rows(summary)

    evidence_csv = data_dir / "close_spacing_source_density_evidence_rows.csv"
    groups_csv = data_dir / "close_spacing_source_density_group_summary.csv"
    gates_csv = data_dir / "close_spacing_source_density_gates.csv"
    summary_json = data_dir / "close_spacing_source_density_archive_map_summary.json"

    write_csv(evidence_csv, [json_safe(row) for row in evidence_rows])
    write_csv(groups_csv, [json_safe(row) for row in group_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    summary["paths"] = {
        "evidence_csv": str(evidence_csv),
        "groups_csv": str(groups_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "source_specs": specs,
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "close_spacing_source_density_archive_map",
        {
            "summary_json": str(summary_json),
            "groups_csv": str(groups_csv),
            "evidence_csv": str(evidence_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

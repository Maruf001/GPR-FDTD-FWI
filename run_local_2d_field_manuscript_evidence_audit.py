#!/usr/bin/env python3
"""Audit current local synthetic 2D and field publication evidence bundles."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_synthetic_2d_publication_figure_bundle import DEFAULT_EXPERIMENT_ROOT  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SYNTHETIC_BUNDLE_RUN = "1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation"
DEFAULT_SYNTHETIC_NEXT_MATRIX_RUN = "1356_synthetic_2d_next_question_matrix_post_matched_source3_policy"
DEFAULT_FIELD_BUNDLE_RUN = "111_gssi51600s_field_publication_claim_bundle_post_event_support_timing_discriminant_hpc"
DEFAULT_FIELD_POLICY_RUN = "112_gssi51600s_field_dataset_policy_synthesis_post_event_support_timing_discriminant_hpc_bundle"

REQUIRED_SYNTHETIC_CLAIMS = {
    "resolution_limit",
    "close50_legacy_branch",
    "confidence_policy",
    "reporting_tiers",
    "objective_uniqueness",
    "target_specificity",
    "target1_acquisition_confidence",
    "target2_close14_objective_limit",
    "target2_close50_linear29p5_seed_frequency",
    "gpu_next_step",
    "field_separation",
}
REQUIRED_FIELD_CLAIMS = {
    "field_geometry",
    "short_profile_timing",
    "long_profile_pattern",
    "synthetic_separation",
    "gpu_next_step",
    "field_time_zero_uncertainty_budget",
    "field_early_time_anchor_negative_qc",
    "field_timing_anchor_conflict",
    "field_timing_window_family_classification",
    "field_cue_spacing_context",
    "field_acquisition_readiness",
    "field_hyperbola_timezero_degeneracy",
}


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def boolish(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def no_gpu_value(value) -> bool:
    return str(value).strip().lower() in {"", "none", "none_now", "no_gpu_required"}


def resolve_project_path(path_text: str, project_root: Path) -> Path:
    path = Path(str(path_text))
    return path if path.is_absolute() else project_root / path


def figure_validated(stats: dict) -> bool:
    return (
        safe_float(stats.get("nonwhite_fraction"), 0.0) > 0.02
        and safe_float(stats.get("dynamic_range"), 0.0) > 10.0
        and safe_float(stats.get("width"), 0.0) >= 50.0
        and safe_float(stats.get("height"), 0.0) >= 50.0
    )


def collect_figure_stats(path_text: str, project_root: Path) -> dict:
    if not path_text:
        return {
            "path": "",
            "file_exists": False,
            "figure_validated": False,
            "figure_issue": "missing_path",
        }
    path = resolve_project_path(path_text, project_root)
    if not path.exists():
        return {
            "path": str(path),
            "file_exists": False,
            "figure_validated": False,
            "figure_issue": "missing_file",
        }
    try:
        stats = figure_stats(path)
    except Exception as exc:  # pragma: no cover - defensive reporting path
        return {
            "path": str(path),
            "file_exists": True,
            "figure_validated": False,
            "figure_issue": f"stats_failed:{type(exc).__name__}",
        }
    stats["file_exists"] = True
    stats["figure_validated"] = figure_validated(stats)
    stats["figure_issue"] = "" if stats["figure_validated"] else "low_dynamic_or_blank"
    return stats


def audit_figure_rows(domain: str, rows: list[dict], project_root: Path) -> list[dict]:
    out = []
    for row in rows:
        stats = collect_figure_stats(row.get("figure_path", ""), project_root)
        use_text = row.get("paper_use") or row.get("allowed_use") or ""
        metric = row.get("support_metric") or (
            f"{row.get('metric_label', '')}={row.get('metric_value', '')}".strip("=")
        )
        policy_or_status = row.get("status_label") or row.get("policy_label") or ""
        out.append(
            {
                "domain": domain,
                "figure_key": row.get("figure_key", ""),
                "source_run": row.get("source_run", ""),
                "policy_or_status": policy_or_status,
                "use_summary": use_text,
                "metric_summary": metric,
                "figure_path": row.get("figure_path", ""),
                "file_exists": bool(stats.get("file_exists")),
                "figure_validated": bool(stats.get("figure_validated")),
                "figure_issue": stats.get("figure_issue", ""),
                "figure_nonwhite_fraction": safe_float(stats.get("nonwhite_fraction")),
                "figure_dynamic_range": safe_float(stats.get("dynamic_range")),
                "figure_width": safe_float(stats.get("width")),
                "figure_height": safe_float(stats.get("height")),
                "declared_validation_status": row.get("figure_validation_status", ""),
                "allowed_claim": row.get("allowed_claim", ""),
                "prohibited_claim": row.get("prohibited_claim", ""),
            }
        )
    return out


def audit_claim_rows(domain: str, rows: list[dict]) -> list[dict]:
    required = REQUIRED_SYNTHETIC_CLAIMS if domain == "synthetic_2d" else REQUIRED_FIELD_CLAIMS
    out = []
    for row in rows:
        claim_area = row.get("claim_area", "")
        allowed = row.get("allowed_claim", "")
        blocked = row.get("not_allowed", "")
        out.append(
            {
                "domain": domain,
                "claim_area": claim_area,
                "required_for_current_package": claim_area in required,
                "has_allowed_claim": bool(allowed.strip()),
                "has_not_allowed_boundary": bool(blocked.strip()),
                "boundary_complete": bool(allowed.strip() and blocked.strip()),
                "allowed_claim": allowed,
                "not_allowed": blocked,
            }
        )
    return out


def required_claims_present(domain: str, claim_rows: list[dict]) -> bool:
    required = REQUIRED_SYNTHETIC_CLAIMS if domain == "synthetic_2d" else REQUIRED_FIELD_CLAIMS
    present = {row.get("claim_area", "") for row in claim_rows}
    return required.issubset(present)


def bundle_figure_status(summary: dict, project_root: Path) -> dict:
    figure_path = summary.get("paths", {}).get("figure", "")
    stats = collect_figure_stats(figure_path, project_root)
    return {
        "bundle_figure_path": figure_path,
        "bundle_figure_exists": bool(stats.get("file_exists")),
        "bundle_figure_validated": bool(stats.get("figure_validated")),
        "bundle_figure_issue": stats.get("figure_issue", ""),
        "bundle_figure_nonwhite_fraction": safe_float(stats.get("nonwhite_fraction")),
        "bundle_figure_dynamic_range": safe_float(stats.get("dynamic_range")),
    }


def build_domain_summary(
    *,
    domain: str,
    bundle_run: str,
    endpoint_run: str,
    bundle_summary: dict,
    endpoint_summary: dict,
    figure_rows: list[dict],
    figure_audit_rows: list[dict],
    claim_rows: list[dict],
    claim_audit_rows: list[dict],
    project_root: Path,
) -> dict:
    if domain == "synthetic_2d":
        ready_key = "ready_for_manuscript_draft"
        expected_figure_count = int(bundle_summary.get("figure_count", 0))
        expected_claim_count = int(bundle_summary.get("claim_boundary_count", 0))
    else:
        ready_key = "ready_for_manuscript_field_supplement"
        expected_figure_count = int(bundle_summary.get("figure_row_count", 0))
        expected_claim_count = int(bundle_summary.get("claim_boundary_count", 0))

    bundle_status = bundle_figure_status(bundle_summary, project_root)
    validated_count = sum(1 for row in figure_audit_rows if boolish(row.get("figure_validated")))
    figure_count_matches = len(figure_rows) == expected_figure_count
    claim_count_matches = len(claim_rows) == expected_claim_count
    all_figures_valid = validated_count == len(figure_audit_rows) and len(figure_audit_rows) > 0
    all_claims_complete = all(boolish(row.get("boundary_complete")) for row in claim_audit_rows)
    required_present = required_claims_present(domain, claim_rows)
    gpu_priority = bundle_summary.get("gpu_priority", endpoint_summary.get("gpu_priority", ""))
    endpoint_gpu = endpoint_summary.get("gpu_priority", endpoint_summary.get("publication_claim_bundle_gpu_priority", ""))

    if domain == "synthetic_2d":
        allowed_scope = "Known-truth synthetic 2D acquisition and ambiguity policy figures."
        blocked_scope = "No field-data relabeling and no broad GPU sweep without a new hypothesis."
    else:
        allowed_scope = "Measured local GSSI 2D line-profile QC and timing/repeatability supplement."
        blocked_scope = "No 3D survey, cover-depth, radius, absolute time-zero, field FWI, or HPC claim."

    ready = (
        boolish(bundle_summary.get(ready_key))
        and all_figures_valid
        and boolish(bundle_status["bundle_figure_validated"])
        and figure_count_matches
        and claim_count_matches
        and all_claims_complete
        and required_present
        and no_gpu_value(gpu_priority)
        and no_gpu_value(endpoint_gpu)
    )

    return {
        "domain": domain,
        "bundle_run": bundle_run,
        "endpoint_run": endpoint_run,
        "bundle_policy_label": bundle_summary.get("policy_label", ""),
        "endpoint_policy_label": endpoint_summary.get("policy_label", ""),
        "figure_row_count": len(figure_rows),
        "expected_figure_row_count": expected_figure_count,
        "validated_figure_file_count": validated_count,
        "all_constituent_figures_validated": all_figures_valid,
        "bundle_figure_validated": bool(bundle_status["bundle_figure_validated"]),
        "claim_boundary_count": len(claim_rows),
        "expected_claim_boundary_count": expected_claim_count,
        "claim_count_matches_summary": claim_count_matches,
        "figure_count_matches_summary": figure_count_matches,
        "all_claim_boundaries_complete": all_claims_complete,
        "required_claim_boundaries_present": required_present,
        "gpu_priority": gpu_priority,
        "endpoint_gpu_priority": endpoint_gpu,
        "manuscript_ready": ready,
        "allowed_scope": allowed_scope,
        "blocked_scope": blocked_scope,
        **bundle_status,
    }


def summarize_audit(domain_rows: list[dict], figure_rows: list[dict], claim_rows: list[dict]) -> dict:
    synthetic = next(row for row in domain_rows if row["domain"] == "synthetic_2d")
    field = next(row for row in domain_rows if row["domain"] == "field_2d")
    all_ready = all(boolish(row["manuscript_ready"]) for row in domain_rows)
    no_gpu = all(no_gpu_value(row["gpu_priority"]) and no_gpu_value(row["endpoint_gpu_priority"]) for row in domain_rows)
    all_figures = all(boolish(row["figure_validated"]) for row in figure_rows) and boolish(
        synthetic["bundle_figure_validated"]
    ) and boolish(field["bundle_figure_validated"])
    all_claims = all(boolish(row["boundary_complete"]) for row in claim_rows)
    cross_domain_guards = (
        any(row["domain"] == "synthetic_2d" and row["claim_area"] == "field_separation" for row in claim_rows)
        and any(row["domain"] == "field_2d" and row["claim_area"] == "synthetic_separation" for row in claim_rows)
    )
    policy_label = (
        "local_2d_field_manuscript_evidence_ready_no_gpu"
        if all_ready and no_gpu and all_figures and all_claims and cross_domain_guards
        else "local_2d_field_manuscript_evidence_review_required"
    )
    return {
        "policy_label": policy_label,
        "domain_count": len(domain_rows),
        "figure_audit_row_count": len(figure_rows),
        "validated_figure_file_count": sum(1 for row in figure_rows if boolish(row["figure_validated"])),
        "claim_boundary_row_count": len(claim_rows),
        "synthetic_ready": boolish(synthetic["manuscript_ready"]),
        "field_ready": boolish(field["manuscript_ready"]),
        "all_domain_figures_validated": all_figures,
        "all_claim_boundaries_complete": all_claims,
        "cross_domain_guards_present": cross_domain_guards,
        "gpu_priority": "none" if no_gpu else "review",
        "ready_for_manuscript_planning": policy_label == "local_2d_field_manuscript_evidence_ready_no_gpu",
        "decision": (
            "Use the current synthetic 2D and measured-field bundles together as a manuscript evidence package, "
            "while keeping their claim scopes separate. No local synthetic GPU run or field FWI/3D run follows "
            "from this audit; the next heavy run needs a new objective, geometry, or calibrated acquisition question."
        ),
    }


def plot_audit(domain_rows: list[dict], summary: dict, save_path: Path) -> str:
    domains = [row["domain"] for row in domain_rows]
    figure_counts = [int(row["figure_row_count"]) for row in domain_rows]
    validated_counts = [int(row["validated_figure_file_count"]) for row in domain_rows]
    claim_counts = [int(row["claim_boundary_count"]) for row in domain_rows]
    ready = [1 if boolish(row["manuscript_ready"]) else 0 for row in domain_rows]
    x = np.arange(len(domains), dtype=float)

    fig, axes = plt.subplots(1, 2, figsize=(13.8, 4.6), constrained_layout=True)
    width = 0.24
    axes[0].bar(x - width, figure_counts, width=width, color="#2f6f9f", label="figure rows")
    axes[0].bar(x, validated_counts, width=width, color="#4c9f70", label="validated files")
    axes[0].bar(x + width, claim_counts, width=width, color="#c77d2a", label="claim boundaries")
    axes[0].set_xticks(x, ["synthetic 2D", "field 2D"])
    axes[0].set_ylabel("count")
    axes[0].set_title("Current paper evidence package")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=9)

    axes[1].bar(x, ready, color=["#4c9f70" if value else "#c7302b" for value in ready], width=0.45)
    axes[1].set_ylim(0.0, 1.15)
    axes[1].set_yticks([0, 1], ["review", "ready"])
    axes[1].set_xticks(x, ["synthetic 2D", "field 2D"])
    axes[1].set_title("Readiness and GPU posture")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    for idx, row in enumerate(domain_rows):
        text = f"gpu={row['gpu_priority']}\nclaims={row['claim_boundary_count']}"
        axes[1].text(idx, 0.08 if ready[idx] else 0.18, text, ha="center", va="bottom", fontsize=9)

    fig.suptitle(
        f"{summary['policy_label']} | figures={summary['validated_figure_file_count']}/"
        f"{summary['figure_audit_row_count']} | claims={summary['claim_boundary_row_count']}",
        fontsize=12,
    )
    return save_validated_figure(fig, str(save_path))


def write_figure_notes(
    path: Path,
    summary: dict,
    domain_csv: Path,
    figure_csv: Path,
    claim_csv: Path,
    validation_csv: Path,
) -> None:
    """Write notes for the cross-domain manuscript evidence audit figure."""
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_field_manuscript_evidence_audit.png`",
                "",
                "This figure audits whether the current synthetic 2D and measured-field",
                "2D evidence bundles are internally ready for manuscript planning while",
                "keeping their claim scopes separate.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Validated figure files: `{summary['validated_figure_file_count']}` of `{summary['figure_audit_row_count']}`.",
                f"Claim-boundary rows: `{summary['claim_boundary_row_count']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "This audit does not create new physics evidence. Domain summaries,",
                f"figure checks, and claim boundaries are stored in `{domain_csv.name}`,",
                f"`{figure_csv.name}`, and `{claim_csv.name}`. Image-validation metrics",
                f"for this audit figure are stored in `{validation_csv.name}`.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default=DEFAULT_EXPERIMENT_ROOT)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--synthetic-bundle-run", default=DEFAULT_SYNTHETIC_BUNDLE_RUN)
    parser.add_argument("--synthetic-next-matrix-run", default=DEFAULT_SYNTHETIC_NEXT_MATRIX_RUN)
    parser.add_argument("--field-bundle-run", default=DEFAULT_FIELD_BUNDLE_RUN)
    parser.add_argument("--field-policy-run", default=DEFAULT_FIELD_POLICY_RUN)
    parser.add_argument("--outdir", default=None)
    parser.add_argument("--run-name", default="local_2d_field_manuscript_evidence_audit")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = Path(PROJECT_ROOT)
    experiment_root = Path(args.experiment_root)
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)

    synthetic_bundle_dir = experiment_root / args.synthetic_bundle_run
    synthetic_next_dir = experiment_root / args.synthetic_next_matrix_run
    field_bundle_dir = dataset_root / args.field_bundle_run
    field_policy_dir = dataset_root / args.field_policy_run

    synthetic_summary = read_json(synthetic_bundle_dir / "data/synthetic_2d_publication_figure_bundle_summary.json")
    synthetic_next = read_json(synthetic_next_dir / "data/synthetic_2d_next_question_matrix_summary.json")
    synthetic_figures = read_csv_rows(synthetic_bundle_dir / "data/synthetic_2d_publication_figure_rows.csv")
    synthetic_claims = read_csv_rows(synthetic_bundle_dir / "data/synthetic_2d_publication_claim_boundaries.csv")

    field_summary = read_json(field_bundle_dir / "data/field_publication_claim_bundle_summary.json")
    field_policy = read_json(field_policy_dir / "data/field_dataset_policy_summary.json")
    field_figures = read_csv_rows(field_bundle_dir / "data/field_publication_figure_rows.csv")
    field_claims = read_csv_rows(field_bundle_dir / "data/field_publication_claim_boundaries.csv")

    synthetic_figure_audit = audit_figure_rows("synthetic_2d", synthetic_figures, project_root)
    field_figure_audit = audit_figure_rows("field_2d", field_figures, project_root)
    synthetic_claim_audit = audit_claim_rows("synthetic_2d", synthetic_claims)
    field_claim_audit = audit_claim_rows("field_2d", field_claims)

    domain_rows = [
        build_domain_summary(
            domain="synthetic_2d",
            bundle_run=args.synthetic_bundle_run,
            endpoint_run=args.synthetic_next_matrix_run,
            bundle_summary=synthetic_summary,
            endpoint_summary=synthetic_next,
            figure_rows=synthetic_figures,
            figure_audit_rows=synthetic_figure_audit,
            claim_rows=synthetic_claims,
            claim_audit_rows=synthetic_claim_audit,
            project_root=project_root,
        ),
        build_domain_summary(
            domain="field_2d",
            bundle_run=args.field_bundle_run,
            endpoint_run=args.field_policy_run,
            bundle_summary=field_summary,
            endpoint_summary=field_policy,
            figure_rows=field_figures,
            figure_audit_rows=field_figure_audit,
            claim_rows=field_claims,
            claim_audit_rows=field_claim_audit,
            project_root=project_root,
        ),
    ]
    figure_audit_rows = synthetic_figure_audit + field_figure_audit
    claim_audit_rows = synthetic_claim_audit + field_claim_audit
    summary = summarize_audit(domain_rows, figure_audit_rows, claim_audit_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root="outputs/summary_tables"))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    domain_csv = data_dir / "local_2d_field_manuscript_domain_summary.csv"
    figure_csv = data_dir / "local_2d_field_manuscript_figure_audit.csv"
    claim_csv = data_dir / "local_2d_field_manuscript_claim_boundary_audit.csv"
    summary_json = data_dir / "local_2d_field_manuscript_evidence_audit_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_field_manuscript_evidence_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(domain_csv, domain_rows)
    write_csv(figure_csv, figure_audit_rows)
    write_csv(claim_csv, claim_audit_rows)
    plot_audit(domain_rows, summary, figure_path)
    write_csv(validation_csv, [figure_stats(figure_path)])
    write_figure_notes(figure_notes, summary, domain_csv, figure_csv, claim_csv, validation_csv)

    summary["paths"] = {
        "domain_summary_csv": str(domain_csv),
        "figure_audit_csv": str(figure_csv),
        "claim_boundary_audit_csv": str(claim_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2), encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_field_manuscript_evidence_audit",
        {
            "synthetic_bundle_run": args.synthetic_bundle_run,
            "synthetic_next_matrix_run": args.synthetic_next_matrix_run,
            "field_bundle_run": args.field_bundle_run,
            "field_policy_run": args.field_policy_run,
            "dataset_id": args.dataset_id,
            "readgssi_version": readgssi_version(),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )

    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()

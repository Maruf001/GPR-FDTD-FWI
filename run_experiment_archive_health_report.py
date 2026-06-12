#!/usr/bin/env python3
"""Audit numbered experiment outputs for artifact hygiene and run type drift."""

from __future__ import annotations

import argparse
import csv
import json
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

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


RUN_DIR_RE = re.compile(r"^(\d{3,})_(.+)$")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

PHYSICS_TERMS = (
    "coordinate_optimizer",
    "detection_",
    "source_shape",
    "single_rebar",
    "multi_rebar",
    "material_radius",
    "radius_profile",
    "radius_tradeoff",
    "w2",
    "wasserstein",
    "wavefield",
    "forward",
    "landscape",
    "geometry",
    "frequency",
    "spectrum",
    "bscan",
)

INFRA_TERMS = (
    "queue",
    "commit",
    "archive",
    "checkpoint",
    "validation",
    "state_audit",
    "lint",
    "manuscript",
    "inventory",
    "handoff",
    "reproducibility",
    "reporting_bundle",
    "caption_package",
    "claim_consistency",
    "editorial",
)

REPORT_TERMS = (
    "summary",
    "aggregate",
    "report",
    "synthesis",
    "figure_map",
    "figure_readiness",
    "objective_confidence",
    "diagnostic_report",
)


def parse_run_dir(path: Path) -> tuple[int, str] | None:
    """Return run number and slug for a numbered output directory."""
    match = RUN_DIR_RE.match(path.name)
    if not match:
        return None
    return int(match.group(1)), match.group(2)


def classify_run_name(slug: str) -> str:
    """Classify a run slug by likely purpose."""
    text = slug.lower()
    if any(term in text for term in INFRA_TERMS):
        return "reporting_audit_checkpoint"
    if any(term in text for term in REPORT_TERMS):
        return "analysis_report"
    if any(term in text for term in PHYSICS_TERMS):
        return "physics_or_diagnostic"
    return "unclear"


def range_label(run_number: int) -> str:
    """Use stable bins that expose the reported pace change."""
    if run_number <= 430:
        return "001-430"
    if run_number <= 534:
        return "431-534"
    if run_number <= 730:
        return "535-730"
    return "731+"


def _iter_files(path: Path) -> list[Path]:
    return [item for item in path.rglob("*") if item.is_file() and not item.is_symlink()]


def inspect_run(path: Path) -> dict:
    """Inspect one numbered experiment output directory."""
    parsed = parse_run_dir(path)
    if parsed is None:
        raise ValueError(f"not a numbered run directory: {path}")
    run_number, slug = parsed
    files = _iter_files(path)
    figure_dir = path / "figures"
    data_dir = path / "data"
    image_files = [item for item in files if item.suffix.lower() in IMAGE_SUFFIXES]
    figure_image_files = [
        item for item in image_files
        if figure_dir in item.parents or item.parent == figure_dir
    ]
    category = classify_run_name(slug)
    has_figure_notes = (figure_dir / "FIGURE_NOTES.md").is_file()
    issues: list[str] = []
    warnings: list[str] = []

    if not (path / "run_manifest.json").is_file():
        issues.append("missing_run_manifest")
    if category == "physics_or_diagnostic" and not data_dir.is_dir():
        issues.append("physics_or_diagnostic_missing_data_dir")
    if figure_image_files and not has_figure_notes:
        issues.append("figure_images_missing_figure_notes")
    if category == "physics_or_diagnostic" and not figure_dir.is_dir():
        warnings.append("physics_or_diagnostic_without_figures_dir")
    if category == "unclear":
        warnings.append("unclear_run_type")
    if category == "reporting_audit_checkpoint" and not data_dir.is_dir():
        warnings.append("checkpoint_without_machine_readable_data")

    return {
        "run_number": run_number,
        "slug": slug,
        "range": range_label(run_number),
        "category": category,
        "has_data_dir": data_dir.is_dir(),
        "has_figures_dir": figure_dir.is_dir(),
        "has_figure_notes": has_figure_notes,
        "has_manifest": (path / "run_manifest.json").is_file(),
        "has_readme": (path / "README.md").is_file(),
        "image_file_count": len(image_files),
        "figure_image_count": len(figure_image_files),
        "file_count": len(files),
        "total_size_bytes": sum(item.stat().st_size for item in files),
        "issues": issues,
        "warnings": warnings,
    }


def collect_runs(outputs_root: Path) -> list[dict]:
    """Collect all numbered output run inspections."""
    rows = []
    for path in outputs_root.iterdir():
        if not path.is_dir() or path.is_symlink():
            continue
        if parse_run_dir(path) is None:
            continue
        rows.append(inspect_run(path))
    rows.sort(key=lambda row: row["run_number"])
    return rows


def summarize_runs(rows: list[dict]) -> dict:
    """Summarize run health by range and category."""
    by_range: dict[str, dict] = {}
    for label in ("001-430", "431-534", "535-730", "731+"):
        group = [row for row in rows if row["range"] == label]
        categories = Counter(row["category"] for row in group)
        by_range[label] = {
            "run_count": len(group),
            "category_counts": dict(categories),
            "with_data_dir": sum(bool(row["has_data_dir"]) for row in group),
            "with_figures_dir": sum(bool(row["has_figures_dir"]) for row in group),
            "with_images": sum(row["image_file_count"] > 0 for row in group),
            "with_figure_notes": sum(bool(row["has_figure_notes"]) for row in group),
            "issue_count": sum(len(row["issues"]) for row in group),
            "warning_count": sum(len(row["warnings"]) for row in group),
        }
    issue_counts = Counter(issue for row in rows for issue in row["issues"])
    warning_counts = Counter(warning for row in rows for warning in row["warnings"])
    return {
        "run_count": len(rows),
        "by_range": by_range,
        "category_counts": dict(Counter(row["category"] for row in rows)),
        "issue_counts": dict(issue_counts),
        "warning_counts": dict(warning_counts),
        "runs_with_issues": [row["run_number"] for row in rows if row["issues"]],
        "runs_with_warnings": [row["run_number"] for row in rows if row["warnings"]],
    }


def write_rows_csv(path: Path, rows: list[dict]) -> None:
    """Write per-run rows to CSV."""
    fieldnames = [
        "run_number",
        "slug",
        "range",
        "category",
        "has_data_dir",
        "has_figures_dir",
        "has_figure_notes",
        "has_manifest",
        "has_readme",
        "image_file_count",
        "figure_image_count",
        "file_count",
        "total_size_bytes",
        "issues",
        "warnings",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out["issues"] = "|".join(row["issues"])
            out["warnings"] = "|".join(row["warnings"])
            writer.writerow(out)


def plot_category_timeline(summary: dict, save_path: Path) -> None:
    """Plot run-category counts by range."""
    labels = list(summary["by_range"])
    categories = sorted(summary["category_counts"])
    bottoms = [0] * len(labels)
    fig, ax = plt.subplots(figsize=(9.2, 5.2), constrained_layout=True)
    for category in categories:
        values = [
            summary["by_range"][label]["category_counts"].get(category, 0)
            for label in labels
        ]
        ax.bar(labels, values, bottom=bottoms, label=category)
        bottoms = [a + b for a, b in zip(bottoms, values)]
    ax.set_title("Numbered Run Type Mix By Archive Range")
    ax.set_xlabel("Run range")
    ax.set_ylabel("Run count")
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.25)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def plot_artifact_coverage(summary: dict, save_path: Path) -> None:
    """Plot artifact coverage rates by range."""
    labels = list(summary["by_range"])
    metrics = [
        ("with_data_dir", "data dir"),
        ("with_figures_dir", "figures dir"),
        ("with_images", "image file"),
        ("with_figure_notes", "figure notes"),
    ]
    width = 0.18
    x_values = list(range(len(labels)))
    fig, ax = plt.subplots(figsize=(9.2, 5.2), constrained_layout=True)
    for offset, (key, label) in enumerate(metrics):
        rates = []
        for range_label_ in labels:
            group = summary["by_range"][range_label_]
            count = group["run_count"]
            rates.append(group[key] / count if count else 0.0)
        positions = [x + (offset - 1.5) * width for x in x_values]
        ax.bar(positions, rates, width=width, label=label)
    ax.set_title("Artifact Coverage Rate By Archive Range")
    ax.set_xlabel("Run range")
    ax.set_ylabel("Fraction of runs")
    ax.set_ylim(0.0, 1.05)
    ax.set_xticks(x_values, labels)
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.25)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def write_figure_notes(path: Path) -> None:
    """Write notes for archive health figures."""
    path.write_text(
        "\n".join([
            "# Figure Notes",
            "",
            "## 1. `run_type_mix_by_range.png` - run type mix",
            "",
            "This stacked bar chart separates numbered outputs into physical or",
            "diagnostic runs, analysis reports, and reporting/audit/checkpoint runs.",
            "It is meant to make run-number inflation visible: a high count of",
            "checkpoint/reporting runs is not the same thing as many new FDTD or FWI",
            "experiments.",
            "",
            "## 2. `artifact_coverage_by_range.png` - artifact coverage",
            "",
            "This grouped bar chart shows how often runs in each archive range contain",
            "`data/`, `figures/`, rendered images, and `figures/FIGURE_NOTES.md`.",
            "Use it as a hygiene check before comparing experiment pace across ranges.",
            "",
            "If a run generated figures or images, figure notes should be present.",
            "Physical or diagnostic runs should normally include a machine-readable",
            "`data/` folder.",
            "",
        ]) + "\n",
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outputs-root", default="outputs/experiments")
    parser.add_argument("--run-name", default="experiment_archive_health_report")
    parser.add_argument("--outdir", default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    outputs_root = Path(args.outputs_root)
    rows = collect_runs(outputs_root)
    summary = summarize_runs(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "experiment_archive_health_rows.csv"
    summary_json = data_dir / "experiment_archive_health_summary.json"
    write_rows_csv(rows_csv, rows)
    summary_json.write_text(
        json.dumps({"summary": summary, "runs": rows}, indent=2) + "\n",
        encoding="utf-8",
    )
    plot_category_timeline(summary, figures_dir / "run_type_mix_by_range.png")
    plot_artifact_coverage(summary, figures_dir / "artifact_coverage_by_range.png")
    write_figure_notes(figures_dir / "FIGURE_NOTES.md")
    write_run_manifest(
        str(outdir),
        "experiment_archive_health_report",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "run_type_figure": str(figures_dir / "run_type_mix_by_range.png"),
            "artifact_coverage_figure": str(figures_dir / "artifact_coverage_by_range.png"),
            "figure_notes": str(figures_dir / "FIGURE_NOTES.md"),
        },
    )
    print(f"Audited {summary['run_count']} runs")
    print(json.dumps(summary["by_range"], indent=2))
    print(f"Wrote summary: {summary_json}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build a baseline matrix from saved single-rebar experiment summaries."""
import argparse
from pathlib import Path

from inversion.single_rebar_result_summary import (
    find_single_rebar_summaries,
    summarize_single_rebar_summary,
    write_summary_csv,
)


def _format_float(value, digits=4):
    if value is None:
        return ""
    return f"{float(value):.{digits}g}"


def _write_markdown(rows, path, csv_path):
    selected = [
        "experiment",
        "noise_fraction",
        "recovered_x_mm",
        "recovered_z_mm",
        "recovered_radius_mm",
        "radius_error_mm",
        "best_misfit",
        "nrms_data_primary",
        "best_radius_mm",
        "next_radius_mm",
        "radius_margin_abs",
        "elapsed_time_s",
    ]
    with Path(path).open("w", encoding="utf-8") as handle:
        handle.write("# Experiment 20: Baseline Result Matrix\n\n")
        handle.write("## Goal\n\n")
        handle.write(
            "Create a machine-readable baseline table for all saved single-rebar "
            "runs before launching more paper-guided experiments.\n\n"
        )
        handle.write("## Outputs\n\n")
        handle.write("```text\n")
        handle.write(f"{csv_path}\n")
        handle.write("```\n\n")
        handle.write("## Summary Table\n\n")
        handle.write("| " + " | ".join(selected) + " |\n")
        handle.write("| " + " | ".join(["---"] * len(selected)) + " |\n")
        for row in rows:
            values = []
            for key in selected:
                value = row.get(key)
                if isinstance(value, float):
                    values.append(_format_float(value))
                else:
                    values.append("" if value is None else str(value))
            handle.write("| " + " | ".join(values) + " |\n")
        handle.write("\n## Current Interpretation\n\n")
        handle.write(
            "This table is an index for comparing future experiments. Use the CSV "
            "for filtering and the top-candidate margin columns for radius "
            "confidence checks.\n"
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="outputs/experiments")
    parser.add_argument(
        "--csv",
        default="outputs/summary_tables/single_rebar_baseline_matrix.csv",
        help="CSV output path",
    )
    parser.add_argument(
        "--markdown",
        default="docs/experiments/20_baseline_result_matrix.md",
        help="Markdown report output path",
    )
    args = parser.parse_args()

    summaries = find_single_rebar_summaries(args.root)
    rows = [summarize_single_rebar_summary(path) for path in summaries]
    rows.sort(key=lambda row: row["experiment"])

    write_summary_csv(rows, args.csv)
    _write_markdown(rows, args.markdown, args.csv)
    print(f"Wrote {len(rows)} rows to {args.csv}")
    print(f"Wrote markdown report to {args.markdown}")


if __name__ == "__main__":
    main()

# Experiment 832: Archive Health After Field Timing Refresh

Date: 2026-06-18

## Purpose

Refresh the numbered-output archive health report after the local 2D/field
evidence refresh. This is an infrastructure audit over existing
`outputs/experiments` folders only. It does not launch FDTD, FWI, optimizer,
field inversion, or GPU work.

## Output

```text
outputs/experiments/1324_experiment_archive_health_report_post_field_timing_refresh
```

Key artifacts:

```text
outputs/experiments/1324_experiment_archive_health_report_post_field_timing_refresh/data/experiment_archive_health_rows.csv
outputs/experiments/1324_experiment_archive_health_report_post_field_timing_refresh/data/experiment_archive_health_summary.json
outputs/experiments/1324_experiment_archive_health_report_post_field_timing_refresh/figures/run_type_mix_by_range.png
outputs/experiments/1324_experiment_archive_health_report_post_field_timing_refresh/figures/artifact_coverage_by_range.png
```

## Result

```text
numbered experiment output dirs audited: 1325
001-430 runs:                         430
431-534 runs:                         104
535-730 runs:                         196
731+ runs:                            595
physics/diagnostic runs:              802
analysis report runs:                 181
reporting/audit/checkpoint runs:      188
unclear run-type warnings:            154
figure-notes issues:                  125
missing run manifests:                5
```

Missing-manifest runs:

```text
263 lateral_gap_threshold_close50_vs_close60_summary
268 close50_txrx_offset_objective_gap_summary
271 close50_txrx40_seed_replication_summary
420 material_source_branch_animation_summary
1220 coordinate_optimizer_close50_seed21_sources4_txrx25_objectives
```

## Interpretation

The current archive has strong machine-readable coverage overall, but the
health report confirms two hygiene gaps that should not be confused with new
research questions: many image-bearing runs lack `figures/FIGURE_NOTES.md`,
and five numbered outputs lack `run_manifest.json`. The latest archive range
is mostly physical/diagnostic or analysis output, while the middle 535-730
range is dominated by reporting/checkpoint runs.

Runs `1322` and `1323` were refreshed in place with generator-written
`figures/FIGURE_NOTES.md`. Run `1325` then backfilled source-figure notes for
the 9 figures referenced by the current synthetic publication bundle, reducing
the refreshed archive's figure-notes issue count from 135 to 125. Current field
and summary-table endpoints were also refreshed with figure notes, although
those folders are outside the synthetic `outputs/experiments` audit stream.

No synthetic GPU or field HPC work follows from this audit. Treat it as a
project-state check that supports later cleanup and manuscript handoff.

## Backfill Decision

Do not backfill these five manifests automatically. Run `420` has a recoverable
command in its tracker, but runs `263`, `268`, and `271` are older summary
artifacts without a clearly recoverable original command invocation, and run
`1220` is an interrupted partial run that was explicitly excluded from the
close50 Tx/Rx 25 mm aggregate and superseded by run `1221`. Leaving these as
audit findings preserves provenance more honestly than writing mixed-quality
synthetic manifests.

## Validation

Validation:

```text
tests/test_experiment_archive_health_report.py
conda run -n gpr-fdtd-fwi python -m pytest -q
663 passed
```

# Experiment 656: Scene Geometry Backfill Audit

## Purpose

Backfill reusable system/scene geometry figures for recent coordinate-optimizer
experiments, then work backward through the numbered archive using only
machine-readable metadata. This was CPU-only plotting and validation; no FDTD,
FWI, or optimizer simulation was launched for this backfill.

## Implementation

Extended the reusable scene visualization entry point:

```text
run_experiment_scene_visualization.py
```

New batch mode audits numbered experiment folders newest-first, skips existing
valid scene artifacts, skips runs without compatible coordinate-optimizer
metadata, writes CSV/JSON audit reports, and can refresh existing scene figures
when annotations improve.

The static scene plot was also refined so close-spacing rebar labels are spread
with callout lines instead of overlapping, and long run-name titles wrap.

Focused test coverage:

```text
tests/test_experiment_scene_visualization.py
```

## Commands

Initial backfill:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_scene_visualization.py \
  --backfill-root outputs/experiments \
  --audit-json outputs/visualization_audits/20260610/scene_geometry_backfill_audit_20260610.json \
  --audit-csv outputs/visualization_audits/20260610/scene_geometry_backfill_audit_20260610.csv
```

Refresh after label-placement improvement:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_scene_visualization.py \
  --backfill-root outputs/experiments \
  --refresh-existing \
  --audit-json outputs/visualization_audits/20260610/scene_geometry_backfill_audit_20260610_final.json \
  --audit-csv outputs/visualization_audits/20260610/scene_geometry_backfill_audit_20260610_final.csv
```

Supplemental latest-run audit after concurrent runs 1120 and 1121 completed:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_scene_visualization.py \
  --backfill-root outputs/experiments \
  --min-run-number 1120 \
  --audit-json outputs/visualization_audits/20260610/scene_geometry_backfill_audit_20260610_latest.json \
  --audit-csv outputs/visualization_audits/20260610/scene_geometry_backfill_audit_20260610_latest.csv
```

## Outputs

Primary audit artifacts:

```text
outputs/visualization_audits/20260610/scene_geometry_backfill_audit_20260610.json
outputs/visualization_audits/20260610/scene_geometry_backfill_audit_20260610.csv
outputs/visualization_audits/20260610/scene_geometry_backfill_audit_20260610_final.json
outputs/visualization_audits/20260610/scene_geometry_backfill_audit_20260610_final.csv
outputs/visualization_audits/20260610/scene_geometry_backfill_audit_20260610_latest.json
outputs/visualization_audits/20260610/scene_geometry_backfill_audit_20260610_latest.csv
```

For each compatible run, the reusable script writes or refreshes:

```text
figures/system_scene_geometry.png
data/system_scene_geometry_summary.json
figures/FIGURE_NOTES.md
```

## Counts

Initial archive-wide pass:

```text
rows: 1119
generated: 484
skipped: 635
```

Refresh pass after improved annotation placement:

```text
rows: 1120
refreshed: 488
skipped: 632
```

Supplemental latest-run audit:

```text
1121: skipped, existing valid scene artifacts
1120: skipped, existing valid scene artifacts
```

Current archive snapshot after the concurrent 1120/1121 runs completed:

```text
coordinate summaries: 526
system_scene_geometry.png files: 490
FIGURE_NOTES.md scene sections: 490
```

A later concurrent GPU optimizer run created output directory 1122 while final
validation was being prepared. At inspection time it had no summary files yet,
so this backfill did not touch it. The current optimizer hook should create its
scene artifacts when that run finishes.

The 36 coordinate summaries without scene figures are older incompatible runs:
19 fail the current truth x/z/radius vector contract, and 17 lack
`scan_x_values_mm` Tx/Rx acquisition metadata. They were skipped rather than
guessing acquisition geometry.

Run 1119 is a GSSI field-data QC output, not a coordinate-optimizer summary, so
it was skipped by this synthetic scene backfill. It already has field QC context
figures from the field-data workflow.

## Validation

Focused tests:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q tests/test_experiment_scene_visualization.py
7 passed
```

Generated/refreshed scene image metrics from the final audit:

```text
metric rows: 488
width_px: 1569 to 2200 before title wrap; refreshed samples now use wrapped titles
height_px: 1030 to 1065
unique_colors: all sampled figures above 1800
nonwhite_fraction: sampled figures 0.54 to 0.73
```

Visual spot checks:

```text
1114 system_scene_geometry.png: wrapped title, Tx/Rx offset callout, target cover, separated labels
1000 system_scene_geometry.png: 8-source geometry, 52.5 mm offset callout, target cover
266 system_scene_geometry.png: close-spacing labels no longer overlap
```

## Interpretation

The compatible synthetic coordinate-optimizer archive now has a reusable
physical scene figure beside the objective plots. The skipped older coordinate
runs should stay skipped unless their summaries are repaired with explicit
scan-position metadata; reconstructing Tx/Rx acquisition geometry from defaults
would be ambiguous.

The current optimizer hook is also writing scene artifacts for new runs, as
shown by runs 1120 and 1121. Run 1122 was still in progress at handoff.

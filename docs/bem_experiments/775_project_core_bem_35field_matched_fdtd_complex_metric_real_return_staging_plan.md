# BEM Experiment 775: Complex Metric Real-Return Staging Plan

Date: 2026-07-01

## Purpose

Create a non-executed staging plan for the five real BEM/FDTD complex metric
CSV files required by the live intake gate.

This run does not create real solver-return files, does not stage files into
the live intake area, does not execute copy commands, does not accept template
files as real returns, and does not promote real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/775_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_file_staging_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_action_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source reconciliation ready:           true
source validation ready:               true
source sensitivity ready:              true
staging files:                         5
required metric rows:                  279
template copy allowed:                 0
real producer files present:           0
live files present:                    0
ready to stage files:                  0
copy commands:                         5
executed commands:                     0
action groups:                         4
ready action groups:                   0
real BEM/FDTD comparison ready:        false
gpu priority:                          none
```

Action groups:

| Order | Action | Files | Rows | Ready now |
| ---: | --- | ---: | ---: | --- |
| 1 | produce real complex metric CSV files | 5 | 279 | false |
| 2 | preflight real CSV files before staging | 5 | 279 | false |
| 3 | stage only real CSV files into live intake paths | 5 | 279 | false |
| 4 | rerun intake and real comparison gates | 5 | 279 | false |

## Interpretation

The real-return handoff is now reduced to five named CSV files. Each planned
copy command uses a producer-file placeholder and an exact live intake path, but
no command is executed in this run.

The plan explicitly disallows copying the blank templates. A real file must
first pass preflight checks: it must not be the template path, it must exist, it
must contain the required columns and row count, it must have no blank required
value cells, it must mark real FDTD export as true, and solver status must be
completed.

## Decision

Use run `775` as the non-executed staging plan for future real BEM/FDTD complex
metric CSV returns. Keep real comparison blocked until all five real CSV files
are staged and pass live intake.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan.py
4 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan.py: pass
```

Figure check:

```text
2212x846, dynamic range=255
```

# BEM Experiment 776: Complex Metric Real-Return Staging Plan Validator

Date: 2026-07-01

## Purpose

Validate the saved run `775` BEM/FDTD complex metric real-return staging plan
from disk.

This run does not create real solver-return files, does not stage files into
the live intake area, does not execute copy commands, does not accept template
files as real returns, and does not promote real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/776_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source staging plan ready:             true
validation checks:                     7
passed validation checks:              7
failed validation checks:              0
staging files:                         5
required metric rows:                  279
copy commands:                         5
executed commands:                     0
real BEM/FDTD comparison ready:        false
gpu priority:                          none
```

Validation checks:

| Check | Result |
| --- | --- |
| source staging plan ready | pass |
| five staging files and 279 rows represented | pass |
| blank templates are non-stageable | pass |
| no real producer or live files are ready | pass |
| commands are present but non-executed | pass |
| action groups and real comparison remain blocked | pass |
| figure and script snapshots are present | pass |

## Interpretation

The saved complex metric staging plan is internally consistent. It contains
five staging targets, 279 required rows, five non-executed copy commands, no
allowed template-copy path, no real producer files, no live files, no ready
action group, and no real-comparison promotion.

## Decision

Use run `776` as the saved-artifact validator for the run `775` non-executed
staging plan.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validator.py
7 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan.py: pass
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validator.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```

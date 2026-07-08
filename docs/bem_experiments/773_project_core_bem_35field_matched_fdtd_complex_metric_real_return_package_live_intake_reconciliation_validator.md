# BEM Experiment 773: Complex Metric Real-Return Package Live Intake Reconciliation Validator

Date: 2026-07-01

## Purpose

Validate the saved run `772` BEM/FDTD complex metric live-intake reconciliation
table from disk.

This run does not create real solver-return files, does not move templates into
the live intake area, does not accept template files as real returns, and does
not promote real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/773_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source reconciliation ready:           true
validation checks:                     7
passed validation checks:              7
failed validation checks:              0
template files:                        5
template rows:                         279
live files present:                    0
accepted files:                        0
accepted as real returns:              0
real BEM/FDTD comparison ready:        false
gpu priority:                          none
```

Validation checks:

| Check | Result |
| --- | --- |
| source reconciliation ready | pass |
| five template files and 279 rows represented | pass |
| templates are present and solver value cells are blank | pass |
| live addendum files remain absent and unaccepted | pass |
| current status split is preserved | pass |
| real comparison remains blocked | pass |
| figure and script snapshots are present | pass |

## Interpretation

The saved BEM/FDTD complex metric reconciliation table is internally
consistent. It preserves the five expected addendum files, 279 expected rows,
3,348 blank solver-value cells, five live parent directories, zero live files,
zero accepted files, and the blocked real-comparison state.

## Decision

Use run `773` as the saved-artifact validator for the run `772` BEM/FDTD
complex metric pre-return reconciliation table.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validator.py
7 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation.py: pass
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validator.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```

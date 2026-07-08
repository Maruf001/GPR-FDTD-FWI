# BEM Experiment 772: Complex Metric Real-Return Package Live Intake Reconciliation

Date: 2026-07-01

## Purpose

Reconcile the run `769` BEM/FDTD complex metric real-return templates against
the run `763` live addendum intake paths.

This run does not create real solver-return files, does not move templates into
the live intake area, does not accept template files as real returns, and does
not promote real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/772_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_reconciliation_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_status_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source template pack ready:             true
source live intake ready:               true
template files:                         5
template rows:                          279
required metric rows:                   279
template files present:                 5
blank required value cells:             3348
live parents present:                   5
live files present:                     0
ready for guarded live intake:          0
accepted files:                         0
accepted as real returns:               0
real BEM/FDTD comparison ready:         false
gpu priority:                           none
```

Current item status:

| Status | Items |
| --- | ---: |
| awaiting real complex metric CSV | 5 |

## Interpretation

The BEM/FDTD complex metric return templates are now connected to the live
addendum intake paths. The five output-local CSV templates exist and contain
279 expected rows, but all solver-produced value fields are blank.

No live addendum file is present. No file is ready for guarded live intake, no
file is accepted as a real return, and real BEM/FDTD comparison remains blocked.

## Decision

Use run `772` as the current BEM/FDTD complex metric pre-return checklist. Keep
real BEM/FDTD comparison blocked until all five real complex metric CSV files
pass live intake.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation.py
4 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation.py: pass
```

Figure check:

```text
2212x852, dynamic range=255
```

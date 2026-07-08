# BEM Experiment 768: Complex Metric Consumer Positive Control Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `767` validator for the complex metric consumer
positive-control block.

This run does not use real FDTD exports, does not accept synthetic files as real
addendum returns, and does not promote real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/768_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:          true
sensitivity scenarios:           11
expected pass scenarios:         1
expected fail scenarios:         10
observed pass scenarios:         1
observed fail scenarios:         10
unexpected outcomes:             0
damaged scenarios:               10
damaged scenarios rejected:      10
gpu priority:                    none
```

Sensitivity scenarios:

| Scenario | Expected | Observed | First failed check |
| --- | --- | --- | --- |
| exact | pass | pass |  |
| source not ready | fail | fail | source positive control ready |
| file count damage | fail | fail | five files and 279 metric rows represented |
| metric row damage | fail | fail | five files and 279 metric rows represented |
| stage shape damage | fail | fail | stage row shape is preserved |
| real export damage | fail | fail | synthetic files preserve schema shape without real export |
| synthetic count damage | fail | fail | synthetic files preserve schema shape without real export |
| metric value damage | fail | fail | metric values are positive and finite |
| real comparison promotion | fail | fail | real comparison remains blocked |
| figure damage | fail | fail | figure and script snapshots are present |
| snapshot damage | fail | fail | figure and script snapshots are present |

## Interpretation

The validator accepts only the exact saved run `766` positive-control state. It
rejects damaged source readiness, file count, metric row count, stage shape,
real-export flags, synthetic-row counts, metric values, false real-comparison
promotion, damaged figure validation, and missing script snapshots.

## Decision

Use runs `766-768` as the guarded BEM/FDTD complex metric consumer mechanics
block. Real comparison remains blocked until real addendum files pass the run
`763-765` intake block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validation_sensitivity.py
10 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control.py: pass
run_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validator.py: pass
run_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validation_sensitivity.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validator.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validation_sensitivity.py: pass
```

Figure check:

```text
2464x861, dynamic range=255
```

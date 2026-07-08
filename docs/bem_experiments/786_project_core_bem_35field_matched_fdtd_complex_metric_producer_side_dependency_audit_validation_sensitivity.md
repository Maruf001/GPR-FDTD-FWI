# BEM Experiment 786: Complex Metric Producer-Side Dependency Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `785` validator.

This run verifies that damaged dependency counts, damaged stage shape, false
producer-file promotion, false preflight promotion, false comparison promotion,
damaged figures, and missing script snapshots are rejected.

## Output

```text
outputs/bem_experiments/786_project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         13
damaged scenarios:                 12
unexpected outcomes:               0
exact saved state passed:          true
producer files present:            0
preflight-passed files:            0
real BEM/FDTD comparison ready:    false
gpu priority:                      none
```

## Interpretation

The validator is fail-closed for the dependency audit. The exact saved state
passes, while damaged or falsely promoted states fail.

## Decision

Keep using run `784` as a partial-producer guide only. Do not weaken the
five-file real-return preflight gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit_validation_sensitivity.py

9 passed
```

Figure check:

```text
2824x840, dynamic range=255
```

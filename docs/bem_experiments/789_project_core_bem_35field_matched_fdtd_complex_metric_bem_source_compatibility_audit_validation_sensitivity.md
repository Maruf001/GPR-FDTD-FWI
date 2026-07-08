# BEM Experiment 789: Complex Metric BEM Source Compatibility Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `788` validator.

This run verifies that false scalar-to-complex promotion, false repackage
promotion, false comparison promotion, damaged source shape, damaged figures,
and missing script snapshots are rejected.

## Output

```text
outputs/bem_experiments/789_project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                                  12
damaged scenarios:                          11
unexpected outcomes:                        0
exact saved state passed:                   true
compatible BEM complex cells:               0
new BEM complex-field exporter required:    true
real BEM/FDTD comparison ready:             false
gpu priority:                               none
```

## Interpretation

The compatibility validator is fail-closed. The exact saved state passes, while
damaged or falsely promoted states fail.

## Decision

Keep the accepted scalar BEM source separate from the required complex-field
BEM exporter.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit_validation_sensitivity.py

9 passed
```

Figure check:

```text
2644x837, dynamic range=255
```

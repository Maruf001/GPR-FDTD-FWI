# BEM Experiment 792: Complex Metric BEM Complex Component Partial Export Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `791` validator.

This run verifies that damaged BEM values, missing rows, false FDTD-field
promotion, false FDTD provenance promotion, false preflight promotion, false
comparison promotion, damaged figures, and missing script snapshots are
rejected.

## Output

```text
outputs/bem_experiments/792_project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                              12
damaged scenarios:                      11
unexpected outcomes:                    0
exact saved state passed:               true
BEM complex value cells:                558
FDTD value cells blank:                 558
FDTD provenance/status cells blank:     1395
partial files passing preflight:        0
real BEM/FDTD comparison ready:         false
gpu priority:                           none
```

## Interpretation

The partial-export validator is fail-closed. The exact saved state passes,
while damaged or falsely promoted states fail.

## Decision

Keep run `790` as a BEM-only partial export until matched FDTD complex values
arrive.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_validation_sensitivity.py

10 passed
```

Figure check:

```text
2644x840, dynamic range=255
```

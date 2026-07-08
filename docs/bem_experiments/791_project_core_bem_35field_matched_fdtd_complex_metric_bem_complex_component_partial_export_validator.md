# BEM Experiment 791: Complex Metric BEM Complex Component Partial Export Validator

Date: 2026-07-01

## Purpose

Validate saved run `790` artifacts from disk.

The validator checks that all nine Bempp frequency solves completed, all five
partial stage files exist with the expected row counts, 279 BEM complex rows
are finite, FDTD-dependent fields remain blank, no partial file passes
preflight, and downstream claims remain blocked.

## Output

```text
outputs/bem_experiments/791_project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_validator_validation_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         7
failed checks:                             0
frequencies ready:                         9
partial stage files:                       5
partial metric rows:                       279
BEM complex value cells:                   558
FDTD value cells blank:                    558
FDTD provenance/status cells blank:        1395
partial files passing preflight:           0
real BEM/FDTD comparison ready:            false
gpu priority:                              none
```

## Interpretation

The saved partial export is stable. It validates as a BEM complex-component
export while still blocking real BEM/FDTD comparison.

## Decision

Use run `791` before citing run `790` as BEM-side complex-component evidence.

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
1744x846, dynamic range=255
```

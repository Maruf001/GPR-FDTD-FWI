# BEM Experiment 788: Complex Metric BEM Source Compatibility Audit Validator

Date: 2026-07-01

## Purpose

Validate saved run `787` artifacts from disk.

The validator checks that the accepted BEM source has two scalar-return files
with 279 rows each, has no complex component columns, reuses receiver and
frequency sampling only, requires a new complex-field exporter, and keeps real
BEM/FDTD comparison blocked.

## Output

```text
outputs/bem_experiments/788_project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit_validator_validation_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_bem_source_compatibility_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         7
failed checks:                             0
accepted BEM files:                        2
accepted BEM scalar-norm rows:             279
required BEM complex cells:                558
compatible BEM complex cells:              0
reusable sampling cells:                   558
new BEM complex-field exporter required:   true
real BEM/FDTD comparison ready:            false
gpu priority:                              none
```

## Interpretation

The saved compatibility audit is stable. The accepted scalar BEM source remains
useful for sampling and scalar norm evidence, but it is not compatible with the
complex BEM component fields.

## Decision

Use run `788` before citing run `787` as the current BEM source compatibility
boundary.

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
1744x846, dynamic range=255
```

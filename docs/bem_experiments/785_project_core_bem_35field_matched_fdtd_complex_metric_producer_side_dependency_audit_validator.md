# BEM Experiment 785: Complex Metric Producer-Side Dependency Audit Validator

Date: 2026-07-01

## Purpose

Validate saved run `784` artifacts from disk.

The validator checks the dependency-group shape, required and blank cell counts,
stage coverage, component cell counts, absent producer files, absent preflight
passes, blocked downstream claims, figure output, and script snapshots.

## Output

```text
outputs/bem_experiments/785_project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit_validator_validation_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         8
failed checks:                             0
required cells:                            3627
blank cells:                               3348
BEM value cells required:                  558
FDTD value cells required:                 558
FDTD provenance/status cells required:     1395
producer files present:                    0
preflight-passed files:                    0
real BEM/FDTD comparison ready:            false
gpu priority:                              none
```

## Interpretation

The saved dependency audit is internally consistent. It confirms that the BEM
side can prepare a defined part of the future return packet, while the real
comparison remains blocked by absent producer files and absent FDTD value and
provenance fields.

## Decision

Use run `785` before citing run `784` as the current producer-side dependency
split.

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
1744x846, dynamic range=255
```

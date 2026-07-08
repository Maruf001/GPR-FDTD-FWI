# BEM Experiment 535: Matched FDTD Return Real-Export Preflight Gap Audit Validator

Date: 2026-06-30

## Purpose

Validate run `534` from saved artifacts.

The validator checks that both real-export probes are refused, no FDTD values
or evidence are produced, the four implementation blockers remain, downstream
states stay closed, and the figure and script snapshots are present.

## Output

```text
outputs/bem_experiments/535_project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit_validator_checks.csv
data/project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation passes:                         5
blocking failures:                         0
real-export preflight validation ready:    true
FDTD return file keys:                     2
real-export refusals:                      2
required FDTD return entries:              558
remaining real-export blockers:            4
GPU priority:                              none
```

## Decision

Use run `535` as the artifact validator for the run `534` real-export preflight
gap audit. The matched FDTD return path remains guarded and non-evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit_validator.py
3 passed
```

Figure check:

```text
2285x841, dynamic range=255
```

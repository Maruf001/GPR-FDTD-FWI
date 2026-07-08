# BEM Experiment 536: Matched FDTD Return Real-Export Preflight Gap Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `535` validator.

The exact run `534` artifacts should pass. Damaged source readiness, probe
counts, refusal counts, value export promotion, accepted-file promotion,
evidence promotion, action promotion, downstream promotion, figure damage, and
script-snapshot damage should fail.

## Output

```text
outputs/bem_experiments/536_project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     11
expected pass scenarios:                   1
expected failure scenarios:                10
unexpected scenarios:                      0
real-export preflight sensitivity ready:   true
exact source artifacts pass:               true
probe damage rejected:                     true
value/evidence promotion rejected:         true
action damage rejected:                    true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
GPU priority:                              none
```

## Decision

Use runs `534-536` as the guarded real-export preflight gap block. Real FDTD
return-value export and validation remain the next BEM-side implementation
step before any accepted BEM/FDTD comparison.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit_validation_sensitivity.py
4 passed
```

Figure check:

```text
2645x841, dynamic range=255
```

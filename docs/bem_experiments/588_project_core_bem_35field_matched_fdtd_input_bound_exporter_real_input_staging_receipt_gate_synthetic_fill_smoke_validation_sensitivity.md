# BEM Experiment 588: Matched FDTD Input-Bound Exporter Real-Input Staging Receipt Gate Synthetic Fill Smoke Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `587` validator with controlled damage to the run `586`
synthetic-smoke artifacts.

This run checks that the validator fails when synthetic case counts,
accept/reject counts, accepted-row counts, real-evidence state, external-file
state, downstream state, figure metadata, or script snapshots are damaged.

## Output

```text
outputs/bem_experiments/588_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_gate_synthetic_fill_smoke_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_gate_synthetic_fill_smoke_validation_sensitivity_cases.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_gate_synthetic_fill_smoke_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_gate_synthetic_fill_smoke_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                  true
sensitivity cases:                       13
expected pass cases:                     1
expected fail cases:                     12
actual pass cases:                       1
actual fail cases:                       12
unexpected cases:                        0
damaged cases:                           12
real BEM/FDTD comparison ready:          false
field transfer ready:                    false
field FWI ready:                         false
gpu priority:                            none
```

Damaged states fail for:

```text
source readiness removal
smoke case removal
accepted-count damage
rejected-count damage
unexpected-case promotion
accepted-row count damage
real-evidence promotion
external staged-file promotion
external accepted-file promotion
BEM/FDTD comparison promotion
figure damage
missing script snapshots
```

## Interpretation

The synthetic-smoke validator is sensitive to the intended failure modes. It
does not silently promote synthetic smoke into real evidence or BEM/FDTD
comparison readiness.

## Decision

Use runs `586-588` as the guarded synthetic acceptance-smoke block for the
external receipt gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_gate_synthetic_fill_smoke_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```

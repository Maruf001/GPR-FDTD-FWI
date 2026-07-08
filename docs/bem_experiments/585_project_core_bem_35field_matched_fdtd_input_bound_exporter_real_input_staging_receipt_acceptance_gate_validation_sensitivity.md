# BEM Experiment 585: Matched FDTD Input-Bound Exporter Real-Input Staging Receipt Acceptance Gate Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `584` validator with controlled damage to the run `583`
receipt-gate artifacts.

This run checks that the validator fails when receipt identity, file presence,
file acceptance, validation-error state, readiness state, downstream state,
figure metadata, or script snapshots are damaged.

## Output

```text
outputs/bem_experiments/585_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate_validation_sensitivity_cases.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                  true
sensitivity cases:                       15
expected pass cases:                     1
expected fail cases:                     14
actual pass cases:                       1
actual fail cases:                       14
unexpected cases:                        0
damaged cases:                           14
exporter execution ready:                false
real BEM/FDTD comparison ready:          false
3D validation claim ready:               false
GPU/HPC ready:                           false
field transfer ready:                    false
field FWI ready:                         false
gpu priority:                            none
```

Damaged states fail for:

```text
source readiness removal
receipt row removal
input/return role-count damage
file-key damage
value-field damage
staged-file presence promotion
file-acceptance promotion
validation-error promotion
exporter-readiness promotion
comparison-readiness promotion
action-readiness promotion
downstream comparison promotion
figure damage
missing script snapshots
```

## Interpretation

The receipt-gate validator is sensitive to the intended failure modes. It does
not silently promote staged files, accepted files, exporter readiness, BEM/FDTD
comparison readiness, or downstream readiness.

## Decision

Use runs `583-585` as the guarded external receipt-acceptance block before any
input-bound exporter execution or BEM/FDTD comparison.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```

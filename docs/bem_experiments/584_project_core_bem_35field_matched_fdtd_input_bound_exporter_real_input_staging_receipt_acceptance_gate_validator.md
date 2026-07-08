# BEM Experiment 584: Matched FDTD Input-Bound Exporter Real-Input Staging Receipt Acceptance Gate Validator

Date: 2026-06-30

## Purpose

Validate run `583` from its saved artifacts.

This run checks that the external receipt gate has the expected four-file
shape, preserves zero accepted files, keeps all actions and downstream states
blocked, and includes valid figure and script-snapshot artifacts.

## Output

```text
outputs/bem_experiments/584_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate_validator.png
scripts/
```

## Result

```text
check count:                             5
passed checks:                           5
failed checks:                           0
receipt rows:                            4
present staged files:                    0
accepted files:                          0
validation errors:                       0
actions:                                 4
exporter execution ready:                false
real BEM/FDTD comparison ready:          false
3D validation claim ready:               false
GPU/HPC ready:                           false
field transfer ready:                    false
field FWI ready:                         false
gpu priority:                            none
```

## Interpretation

The receipt-gate artifact is internally consistent. It defines the external
file boundary but does not promote missing files to accepted evidence.

## Decision

Use run `584` as the artifact validator for run `583`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_acceptance_gate_validator.py

3 passed
```

Figure validation:

```text
2285x840, dynamic range=255
```

# BEM Experiment 816: Complex FDTD Adapter Input External Handoff Claim Boundary Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `815` validator with damaged versions of the run `814`
claim boundary.

The damaged scenarios include claim-count drift, missing guarded claims, handoff
metric promotion, sensitivity-count damage, false completed-stage promotion,
false comparison promotion, false field/3D promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/bem_experiments/816_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_handoff_claim_boundary_validation_sensitivity
```

## Result

```text
scenarios:                         18
expected pass scenarios:           1
expected fail scenarios:           17
observed pass scenarios:           1
observed fail scenarios:           17
unexpected outcomes:               0
damaged scenarios:                 17
damaged scenarios rejected:        17
completed stage files ready:       false
real BEM/FDTD comparison ready:    false
field transfer ready:              false
3D/HPC ready:                      false
gpu priority:                      none
```

The exact saved claim boundary passes. All seventeen damaged variants fail.

## Decision

Use runs `814-816` as the current guarded BEM external handoff claim-boundary
block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_handoff_claim_boundary_validation_sensitivity.py

3 passed
```

Figure check:

```text
3401x886, dynamic range=255
```

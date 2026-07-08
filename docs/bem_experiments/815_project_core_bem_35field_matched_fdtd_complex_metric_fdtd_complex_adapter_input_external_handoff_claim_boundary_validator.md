# BEM Experiment 815: Complex FDTD Adapter Input External Handoff Claim Boundary Validator

Date: 2026-07-01

## Purpose

Validate the saved run `814` claim boundary from artifacts.

The validator checks claim counts, guarded claim content, handoff metrics,
sensitivity metrics, blocked downstream states, figure validation, and script
snapshots.

## Output

```text
outputs/bem_experiments/815_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_handoff_claim_boundary_validator
```

## Result

```text
validation checks:                 8
passed checks:                     8
failed checks:                     0
claims:                            5
guarded claims:                    2
blocked claims:                    3
output-local template rows:        279
external input rows:               0
accepted external rows:            0
damaged scenarios rejected:        11
completed stage files ready:       false
real BEM/FDTD comparison ready:    false
field transfer ready:              false
3D/HPC ready:                      false
gpu priority:                      none
```

## Interpretation

The saved claim boundary is internally consistent. It preserves the separation
between the fill-in template and real external FDTD evidence, and it keeps all
comparison and downstream states blocked.

## Decision

Use this validator before promoting any external complex FDTD input or
BEM/FDTD comparison state.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_handoff_claim_boundary_validator.py

3 passed
```

Figure check:

```text
2861x904, dynamic range=255
```

# BEM Experiment 812: Complex FDTD Adapter Input External Handoff Guard Validator

Date: 2026-07-01

## Purpose

Validate the saved run `811` external handoff guard.

Run `811` separated the output-local complex FDTD input template from the real
external filled-input path. This validator checks that the saved guard preserves
that separation and keeps real BEM/FDTD comparison blocked.

## Output

```text
outputs/bem_experiments/812_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_handoff_guard_validator
```

## Result

```text
validation checks:                         7
passed checks:                             7
failed checks:                             0
handoff items:                             2
output-local template present:             true
output-local template rows:                279
template under external return root:       false
external input file present:               false
external input rows:                       0
external input accepted:                   false
real BEM/FDTD comparison ready:            false
3D/HPC ready:                              false
gpu priority:                              none
```

## Interpretation

The saved handoff guard is stable. The template remains output-local, the real
external input file remains absent, and no BEM/FDTD comparison state is
promoted.

## Decision

Use this validator before accepting any update to the complex FDTD external
input handoff.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_handoff_guard_validator.py

3 passed
```

Figure check:

```text
2789x935, dynamic range=255
```

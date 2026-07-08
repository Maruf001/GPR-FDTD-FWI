# BEM Experiment 923: Panel-116 Real Return Intake Gate Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `921` real-return intake gate validator.

This run checks that the validator accepts only the exact fail-closed intake
state and rejects damaged or prematurely promoted states, including false
return acceptance, opened execution/comparison flags, missing gate blockers,
figure damage, and script-snapshot damage.

This is a CPU-only validation-sensitivity run. It does not execute FDTD,
populate FDTD values, complete a BEM/FDTD comparison, transfer to field
evidence, or start 3D/HPC work.

## Output

```text
outputs/bem_experiments/923_scarep_2d_cpu_bem_panel116_project_fdtd_real_return_intake_gate_validation_sensitivity
```

## Result

```text
source validator ready:                true
scenarios:                             25
expected pass scenarios:               1
expected fail scenarios:               24
observed pass scenarios:               1
observed fail scenarios:               24
unexpected outcomes:                   0
damaged scenarios:                     24
damaged scenarios rejected:            24
project FDTD launch packet written:    true
project FDTD execution authorized:     false
project FDTD return values present:    false
project FDTD comparison completed:     false
field transfer ready:                  false
real 3D validation ready:              false
gpu priority:                          none
```

Rejected damage cases include:

```text
intake-contract demotion
launch-packet demotion
return-template demotion
gate removal
gate-name damage
required-gate count damage
passed-gate count damage
receiver-frequency row-count damage
false complex-value rows
false solver-provenance rows
false real-return acceptance
false blank-template acceptance
false complex-value gate pass
false provenance gate pass
blocker-text damage
false execution authorization
false return-value presence
false comparison completion
field-transfer promotion
3D promotion
GPU-priority promotion
figure damage
script-snapshot damage
```

## Interpretation

The real-return intake validator is fail-closed. It accepts the intended
current state, where the intake contract exists but the blank template is not
accepted as a return. It rejects every tested damaged or prematurely promoted
state.

## Decision

Use runs `920-923` as the guarded current intake boundary for the panel-116
BEM/FDTD comparison packet. A real comparison remains blocked until all 325
receiver-frequency rows contain complex FDTD values and solver provenance.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_real_return_intake_gate_validation_sensitivity.py
3 passed
```

Figure check:

```text
3488x888, dynamic range=255
```

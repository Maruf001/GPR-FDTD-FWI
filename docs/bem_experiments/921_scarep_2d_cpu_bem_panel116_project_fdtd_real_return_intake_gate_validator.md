# BEM Experiment 921: Panel-116 Real Return Intake Gate Validator

Date: 2026-07-01

## Purpose

Validate the run `920` real FDTD return intake gate.

This run checks that the intake boundary is correctly defined, that the blank
receiver-frequency template is rejected as non-evidence, and that FDTD
execution, FDTD return-value, BEM/FDTD comparison, field-transfer, GPU, and
3D claims remain blocked.

This is a CPU-only validator run. It does not execute FDTD, populate FDTD
values, complete a BEM/FDTD comparison, transfer to field evidence, or start
3D/HPC work.

## Output

```text
outputs/bem_experiments/921_scarep_2d_cpu_bem_panel116_project_fdtd_real_return_intake_gate_validator
```

## Result

```text
source intake contract ready:          true
validation checks:                     6
passed checks:                         6
failed checks:                         0
receiver-frequency rows:               325
complex FDTD value rows:               0
solver provenance rows:                0
real return accepted:                  false
blank template rejected as return:     true
project FDTD launch packet written:    true
project FDTD execution authorized:     false
project FDTD return values present:    false
project FDTD comparison completed:     false
field transfer ready:                  false
real 3D validation ready:              false
gpu priority:                          none
```

The six validation checks cover:

```text
source intake contract readiness
gate shape and expected pass/fail state
blank template rejection
required return blockers
blocked execution and downstream claims
figure and script-snapshot validity
```

## Interpretation

The intake gate validates as a fail-closed boundary. The packet structure is
usable for a future return, but the current blank template remains non-evidence
because it has no complex FDTD values and no solver provenance.

## Decision

Require a separately accepted real FDTD return before any BEM/FDTD comparison
claim.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_real_return_intake_gate_validator.py
5 passed
```

Figure check:

```text
2465x864, dynamic range=255
```

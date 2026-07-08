# BEM Experiment 920: Panel-116 Project-FDTD Real Return Intake Gate

Date: 2026-07-01

## Purpose

Define the real FDTD return intake gate for the smooth continuous-shift
panel-116 BEM comparison packet.

This run connects the guarded launch/return packet scaffold with the guarded
blank receiver-frequency return template. It answers one practical question:
what must be present before a future FDTD return can be accepted for BEM/FDTD
comparison?

This is a CPU-only gate-definition run. It does not execute FDTD, populate
FDTD values, complete a BEM/FDTD comparison, transfer to field evidence, or
start 3D/HPC work.

## Output

```text
outputs/bem_experiments/920_scarep_2d_cpu_bem_panel116_project_fdtd_real_return_intake_gate
```

## Result

```text
launch packet ready:                   true
return template ready:                 true
intake gates:                          7
required acceptance gates:             5
passed gates now:                      5
failed gates now:                      2
passed required acceptance gates:      3
failed required acceptance gates:      2
receiver-frequency rows:               325
complex FDTD value rows:               0
solver provenance rows:                0
blank value rows:                      325
real return accepted:                  false
blank template rejected as return:     true
project FDTD launch packet written:    true
project FDTD execution authorized:     false
project FDTD executed now:             false
project FDTD return values present:    false
project FDTD comparison completed:     false
field transfer ready:                  false
real 3D validation ready:              false
gpu priority:                          none
```

The current intake gates are:

| Order | Gate | Required for acceptance | Current state |
| ---: | --- | --- | --- |
| 1 | launch packet guarded | yes | pass |
| 2 | return template guarded | yes | pass |
| 3 | receiver-frequency identity complete | yes | pass |
| 4 | complex FDTD values present | yes | fail |
| 5 | solver provenance present | yes | fail |
| 6 | blank template rejected | no | pass |
| 7 | comparison waits for accepted return | no | pass |

## Interpretation

The comparison packet now has a defined intake gate. The structure is in place:
the launch packet is guarded, the blank return template is guarded, and all
325 receiver-frequency row identities are present.

The current template is correctly rejected as non-evidence because it contains
zero complex FDTD value rows and zero solver-provenance rows. A future return
must provide complex real/imaginary FDTD values and solver provenance for all
325 receiver-frequency rows before any BEM/FDTD comparison can be accepted.

## Decision

Do not compare BEM and FDTD from the blank template. The next valid comparison
step is to supply a real return file with all 325 complex FDTD rows and solver
provenance, then run a separate return-acceptance validator.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_real_return_intake_gate.py
4 passed
```

Figure check:

```text
3311x873, dynamic range=255
```

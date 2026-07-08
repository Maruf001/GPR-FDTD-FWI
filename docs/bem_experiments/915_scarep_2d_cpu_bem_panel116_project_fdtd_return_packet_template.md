# BEM Experiment 915: Panel-116 Project-FDTD Return Packet Template

Date: 2026-07-01

## Purpose

Create a fail-closed project-FDTD return packet template for the smooth
continuous-shift BEM comparison design from runs `912-914`.

This run writes the receiver-frequency row identities and blank FDTD
value/provenance fields required for a future comparison. It does not write a
launch packet, execute FDTD, populate FDTD values, complete a BEM/FDTD
comparison, transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/bem_experiments/915_scarep_2d_cpu_bem_panel116_project_fdtd_return_packet_template
```

## Result

```text
source contract ready:                 true
source validation ready:               true
source sensitivity ready:              true
source continuous ready:               true
receivers:                               13
frequencies:                             25
template rows:                          325
blank value columns:                      6
blank value cells:                     1950
FDTD value rows present:                  0
return template written:               true
project FDTD launch packet written:   false
project FDTD execution authorized:    false
project FDTD executed now:            false
project FDTD return values present:   false
project FDTD comparison completed:    false
field transfer ready:                 false
real 3D validation ready:             false
gpu priority:                         none
```

Template columns include receiver identity, frequency identity, continuous
source/receiver shift, row-state flags, blank complex FDTD values, and blank
solver provenance:

```text
fdtd_real
fdtd_imag
solver_run_id
solver_status
solver_log_sha256
input_contract_sha256
```

## Interpretation

The return packet template is ready as a fillable schema. It defines the exact
`13 x 25 = 325` receiver-frequency rows needed for a future project-FDTD
comparison against the smooth continuous-shift BEM model.

It is not evidence yet. Every FDTD value and solver provenance cell is blank.

## Decision

Use this as the fillable return packet template. Do not claim comparison or
launch FDTD from this template run.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_return_packet_template.py
4 passed
```

Figure check:

```text
2465x847, dynamic range=255
```

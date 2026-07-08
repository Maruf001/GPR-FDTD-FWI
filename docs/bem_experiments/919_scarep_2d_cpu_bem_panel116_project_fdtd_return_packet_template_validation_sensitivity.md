# BEM Experiment 919: Panel-116 Return Packet Template Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `918` return-template validator with damaged and
prematurely promoted template states.

This run checks that the validator accepts only the exact blank
receiver-frequency return template and rejects cases where row identity,
blank FDTD value fields, execution flags, comparison flags, downstream claims,
continuous-shift metadata, figures, or script snapshots are damaged.

This is a CPU-only validation-sensitivity run. It does not execute FDTD,
populate FDTD values, complete a BEM/FDTD comparison, transfer to field
evidence, or start 3D/HPC work.

## Output

```text
outputs/bem_experiments/919_scarep_2d_cpu_bem_panel116_project_fdtd_return_packet_template_validation_sensitivity
```

## Result

```text
source validator ready:                true
scenarios:                             24
expected pass scenarios:               1
expected fail scenarios:               23
observed pass scenarios:               1
observed fail scenarios:               23
unexpected outcomes:                   0
damaged scenarios:                     23
damaged scenarios rejected:            23
project FDTD launch packet written:    false
project FDTD execution authorized:     false
project FDTD return values present:    false
project FDTD comparison completed:     false
field transfer ready:                  false
real 3D validation ready:              false
gpu priority:                          none
```

The exact template passes. The damaged cases rejected by the validator include:

```text
template readiness damage
source-contract readiness damage
source-validation readiness damage
source-sensitivity readiness damage
source-continuous readiness damage
template-row removal
receiver-identity damage
frequency-identity damage
row-order damage
nonblank FDTD value cell
FDTD-value-present flag
row-identity flag damage
false launch-packet presence
false execution authorization
false FDTD execution
false return-value presence
false comparison completion
field-transfer promotion
3D promotion
GPU-priority promotion
missing continuous-shift metadata
figure damage
script-snapshot damage
```

## Interpretation

The return-template validator is fail-closed. It accepts the intended blank
template and rejects damaged or prematurely promoted states. This protects the
next FDTD-return intake step from silently treating a filled, malformed, or
overclaimed template as comparison evidence.

## Decision

Use runs `918-919` as the guarded row-level return-template block. A separate
real FDTD return intake gate is still required before any BEM/FDTD comparison
claim.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_return_packet_template_validation_sensitivity.py
3 passed
```

Figure check:

```text
3491x894, dynamic range=255
```

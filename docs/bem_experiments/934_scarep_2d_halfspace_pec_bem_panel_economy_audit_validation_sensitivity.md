# BEM Experiment 934: Half-Space PEC BEM Panel Economy Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `933` half-space PEC BEM panel-economy validator.

This run checks that the validator accepts only the exact saved policy state
and rejects damaged panel counts, error gates, speedup metrics, wall-savings
metrics, policy demotion, project-core FDTD promotion, field-transfer
promotion, 3D promotion, GPU-priority promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/bem_experiments/934_scarep_2d_halfspace_pec_bem_panel_economy_audit_validation_sensitivity
```

## Result

```text
source validator ready:                true
scenarios:                             17
expected pass scenarios:               1
expected fail scenarios:               16
observed pass scenarios:               1
observed fail scenarios:               16
unexpected outcomes:                   0
damaged scenarios:                     16
damaged scenarios rejected:            16
recommended preliminary panels:        16
reference BEM panels:                  32
use preliminary panels for sweeps:     true
keep reference panels for comparison:  true
project-core FDTD matched:             false
field transfer ready:                  false
3D validation ready:                   false
gpu priority:                          none
```

Rejected damaged states include:

```text
audit-not-ready state
row removal
reference-panel damage
recommended-panel damage
error-gate damage
speedup damage
wall-savings damage
error-fraction damage
preliminary-sweep policy demotion
reference-policy demotion
project-core FDTD promotion
field-transfer promotion
3D promotion
GPU-priority promotion
figure damage
script-snapshot damage
```

## Interpretation

The panel-economy validator is fail-closed. It accepts the exact saved
16-panel preliminary-sweep policy and rejects damaged metrics or premature
scope promotion.

## Decision

Use runs `932-934` as the guarded half-space PEC BEM panel-economy policy
block: 16 panels for preliminary sweeps, 32 panels for final comparison
checkpoints.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_panel_economy_audit.py
tests/test_scarep_2d_halfspace_pec_bem_panel_economy_audit_validator.py
tests/test_scarep_2d_halfspace_pec_bem_panel_economy_audit_validation_sensitivity.py
10 passed
```

Figure check:

```text
3185x887, dynamic range=255
```

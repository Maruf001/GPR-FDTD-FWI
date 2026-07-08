# BEM Experiment 933: Half-Space PEC BEM Panel Economy Audit Validator

Date: 2026-07-01

## Purpose

Validate the run `932` half-space PEC BEM panel-economy audit from saved
artifacts.

This run checks that the 16-panel preliminary-sweep recommendation, 32-panel
reference policy, error gate, speedup, wall-time savings, and blocked
downstream states are stable.

## Output

```text
outputs/bem_experiments/933_scarep_2d_halfspace_pec_bem_panel_economy_audit_validator
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
reference BEM panels:                      32
recommended preliminary panels:            16
recommended preliminary relative L2:       0.0004746867074423852
recommended speedup vs reference:          3.2873864069744765
recommended wall-time savings:             0.6958069797093482
recommended error / best FDTD mismatch:    0.015313315458994644
use preliminary panels for sweeps:         true
keep reference panels for final comparison:true
project-core FDTD matched:                 false
field transfer ready:                      false
3D validation ready:                       false
gpu priority:                              none
```

## Interpretation

The 16-panel preliminary-sweep policy validates against the saved half-space
PEC panel data. The policy is scoped to preliminary half-space PEC BEM sweeps;
the 32-panel result remains the final comparison reference.

## Decision

Use 16 panels for preliminary sweeps and 32 panels for final half-space PEC BEM
checkpoints.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_panel_economy_audit.py
tests/test_scarep_2d_halfspace_pec_bem_panel_economy_audit_validator.py
7 passed
```

Figure check:

```text
2609x857, dynamic range=255
```

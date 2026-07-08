# BEM Experiment 946: Half-Space PEC BEM Acquisition-Geometry Lock Policy Validation Sensitivity

Date: 2026-07-02

## Purpose

Stress-test the run `945` acquisition-geometry lock-policy validator.

## Output

```text
outputs/bem_experiments/946_scarep_2d_halfspace_pec_bem_acquisition_geometry_lock_policy_validation_sensitivity
```

## Result

```text
source validator ready:                 true
scenarios:                              23
expected pass scenarios:                1
expected fail scenarios:                22
observed pass scenarios:                1
observed fail scenarios:                22
unexpected outcomes:                    0
damaged scenarios:                      22
damaged scenarios rejected:             22
policy rows:                            8
required lock rows:                     8
geometry/depth-material L2 ratio:       14.0411791425335
offset/depth peak ratio:                141.13523416491688
offset/material peak ratio:             30.46264982845857
preliminary BEM panels:                 16
project-core FDTD matched:              false
field transfer ready:                   false
3D validation ready:                    false
gpu priority:                           none
```

Rejected damaged states include:

```text
policy-not-ready state
depth/material source readiness damage
geometry source readiness damage
row removal
policy-item damage
required-lock damage
row-order damage
Tx/Rx tolerance damage
antenna-z tolerance damage
coordinate-convention tolerance damage
lock-stage damage
panel-count damage
geometry-L2 ratio damage
offset/depth peak-ratio damage
offset/material peak-ratio damage
policy-row-count damage
project-core FDTD promotion
field-transfer promotion
3D promotion
GPU-priority promotion
figure damage
script-snapshot damage
```

## Decision

Use runs `944-946` as the guarded BEM acquisition-geometry lock-policy block.
The policy is fail-closed against damaged lock rows, weakened dominance
metrics, and premature downstream promotion.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_acquisition_geometry_lock_policy.py
tests/test_scarep_2d_halfspace_pec_bem_acquisition_geometry_lock_policy_validator.py
tests/test_scarep_2d_halfspace_pec_bem_acquisition_geometry_lock_policy_validation_sensitivity.py
10 passed
```

Python compile check:

```text
run_scarep_2d_halfspace_pec_bem_acquisition_geometry_lock_policy.py
run_scarep_2d_halfspace_pec_bem_acquisition_geometry_lock_policy_validator.py
run_scarep_2d_halfspace_pec_bem_acquisition_geometry_lock_policy_validation_sensitivity.py
tests/test_scarep_2d_halfspace_pec_bem_acquisition_geometry_lock_policy.py
tests/test_scarep_2d_halfspace_pec_bem_acquisition_geometry_lock_policy_validator.py
tests/test_scarep_2d_halfspace_pec_bem_acquisition_geometry_lock_policy_validation_sensitivity.py
pass
```

Figure check:

```text
3437x885, dynamic range=255
```

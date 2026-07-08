# BEM Acquisition-Geometry Lock Policy Checkpoint

Date: 2026-07-02

## What Changed

Closed the BEM acquisition-geometry lock-policy block:

- Run `944` converts the guarded depth/material and acquisition-geometry
  sensitivity evidence into a machine-readable lock policy.
- Run `945` validates that policy.
- Run `946` sensitivity-hardens the validator.
- Snapshot audit `345` freezes runs `944-946`.
- Cross-track rollup `346` updates the generated checkpoint tail to 55 ready
  milestones.
- Snapshot audit `347` freezes the new rollup.

## Key Numbers

```text
policy rows:                            8
required lock rows:                     8
geometry/depth-material L2 ratio:       14.0411791425335
offset/depth peak ratio:                141.13523416491688
offset/material peak ratio:             30.46264982845857
validation checks:                      6 / 6 passed
sensitivity scenarios:                  23
damaged scenarios rejected:             22
checkpoint tail milestones:             55 / 55 ready
checkpoint promotions:                  0
```

## Decision

Use runs `944-946` as the guarded BEM acquisition-geometry lock-policy block.
Future matched BEM/FDTD comparison packets should explicitly lock Tx/Rx offset,
antenna-z, source/receiver coordinate convention, target depth, material case,
panel policy, sampled trace shape, and downstream claim scope before residuals
are interpreted.

This block does not promote project-core FDTD matching, field transfer, GPU
escalation, or 3D validation.

## Validation

```text
19 focused tests passed
py_compile passed for the six branch/checkpoint scripts
figures 944-946 dynamic range=255
figures 345-347 dynamic range=255
scoped whitespace and diff checks clean
```

## Artifacts

```text
outputs/bem_experiments/944_scarep_2d_halfspace_pec_bem_acquisition_geometry_lock_policy
outputs/bem_experiments/945_scarep_2d_halfspace_pec_bem_acquisition_geometry_lock_policy_validator
outputs/bem_experiments/946_scarep_2d_halfspace_pec_bem_acquisition_geometry_lock_policy_validation_sensitivity
outputs/_generated_checkpoints/snapshot_audits/345_result_milestone_snapshot_audit_bem_geometry_lock_policy_refresh
outputs/_generated_checkpoints/cross_track/346_local_bem_field_2d_checkpoint_tail_post_bem_geometry_lock_policy_rollup
outputs/_generated_checkpoints/snapshot_audits/347_result_milestone_snapshot_audit_checkpoint_tail_post_bem_geometry_lock_policy_rollup_refresh
```

The marathon request remains active; the next defensible task is another
bounded BEM, field, synthetic 2D, reporting, or tooling branch that preserves
the current compute gates.

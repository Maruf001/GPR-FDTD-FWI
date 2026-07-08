# BEM Acquisition-Geometry Sensitivity Checkpoint

Date: 2026-07-02

## What Changed

Closed the preliminary 16-panel half-space PEC BEM acquisition-geometry block:

- Run `941` sweeps Tx/Rx offset and antenna-z placement at the baseline
  depth/material case.
- Run `942` validates the geometry sweep.
- Run `943` sensitivity-hardens the validator.
- Snapshot audit `342` freezes runs `941-943`.
- Cross-track rollup `343` updates the generated checkpoint tail to 54 ready
  milestones.
- Snapshot audit `344` freezes the new rollup.

## Key Numbers

```text
geometry cases:                        9
tx/rx offsets:                         0.04;0.06;0.08 m
antenna z values:                      -0.02;0;0.04 m
preliminary BEM panels:                16
peak offset span at z=0:               2.6214537950832346 dB
peak antenna-z span at offset 0.06:    0.10842371175746399 dB
max relative L2 across offset at z=0:  0.7099232724148534
max relative L2 across antenna z:      0.4171376953084501
max relative L2 across full grid:      0.9115427115447009
sensitivity scenarios:                 25
damaged scenarios rejected:            24
checkpoint tail milestones:            54 / 54 ready
checkpoint promotions:                 0
```

## Decision

Use runs `941-943` as the guarded preliminary 16-panel BEM
acquisition-geometry sensitivity block. Source/receiver geometry has a much
larger effect than the prior depth/material perturbations in this simplified
BEM-only setting, so matched BEM/FDTD comparisons should lock Tx/Rx spacing
and antenna-z placement before interpreting residual disagreement as depth or
material error.

This block does not promote project-core FDTD matching, field transfer, GPU
escalation, or 3D validation.

## Validation

```text
19 focused tests passed
py_compile passed for the six branch/checkpoint scripts
figure 943 dynamic range=255
figures 342-344 dynamic range=255
scoped whitespace and diff checks clean
```

## Artifacts

```text
outputs/bem_experiments/941_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep
outputs/bem_experiments/942_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep_validator
outputs/bem_experiments/943_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep_validation_sensitivity
outputs/_generated_checkpoints/snapshot_audits/342_result_milestone_snapshot_audit_bem_geometry_sensitivity_refresh
outputs/_generated_checkpoints/cross_track/343_local_bem_field_2d_checkpoint_tail_post_bem_geometry_sensitivity_rollup
outputs/_generated_checkpoints/snapshot_audits/344_result_milestone_snapshot_audit_checkpoint_tail_post_bem_geometry_sensitivity_rollup_refresh
```

The marathon request remains active; the next defensible task is another
bounded BEM, field, synthetic 2D, reporting, or tooling branch that preserves
the current compute gates.

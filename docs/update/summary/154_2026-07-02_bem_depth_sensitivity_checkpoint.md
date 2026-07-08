# BEM Depth Sensitivity Checkpoint

Date: 2026-07-02

## What Changed

Closed the preliminary 16-panel half-space PEC BEM depth-sensitivity block:

- Run `937` sensitivity-hardens the run `936` validator for the run `935`
  16-panel depth sweep.
- Snapshot audit `336` freezes runs `935-937`.
- Cross-track rollup `337` updates the generated checkpoint tail to 52 ready
  milestones.
- Snapshot audit `338` freezes the new rollup.

## Key Numbers

```text
depth cases:                           3
depth values:                          0.25;0.35;0.45 m
preliminary panels:                    16
deep peak change vs shallow:           -0.018574056369367674 dB
max relative L2 vs 0.35 m depth:       0.039940245470760076
sensitivity scenarios:                 19
damaged scenarios rejected:            18
checkpoint tail milestones:            52 / 52 ready
checkpoint promotions:                 0
```

## Decision

Use runs `935-937` as the guarded preliminary 16-panel BEM depth-sensitivity
block. The current evidence supports waveform-shape-based screening in the
simplified half-space PEC setup only. It does not promote project-core FDTD
matching, field transfer, GPU escalation, or 3D validation.

## Validation

```text
19 focused tests passed
py_compile passed for the new scripts
figures 336-338 dynamic range=255
scoped whitespace and diff checks clean
```

## Artifacts

```text
outputs/bem_experiments/937_scarep_2d_halfspace_pec_bem_16panel_depth_sweep_validation_sensitivity
outputs/_generated_checkpoints/snapshot_audits/336_result_milestone_snapshot_audit_bem_depth_sensitivity_refresh
outputs/_generated_checkpoints/cross_track/337_local_bem_field_2d_checkpoint_tail_post_bem_depth_sensitivity_rollup
outputs/_generated_checkpoints/snapshot_audits/338_result_milestone_snapshot_audit_checkpoint_tail_post_bem_depth_sensitivity_rollup_refresh
```

The marathon request remains active; the next defensible task is a bounded
BEM, field, synthetic 2D, or reporting branch that preserves current compute
gates.

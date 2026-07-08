# Experiment Archive Next ID Allocation Checkpoint

Date: 2026-07-02

## What Changed

Closed a next-ID allocation guard after the duplicate-ID audit:

- Experiment `1853` uses the prior audit's recommended next safe output ID and
  verifies that the current ID is uniquely allocated.
- Snapshot audit `368` freezes experiment `1853`.
- Cross-track rollup `369` updates the generated checkpoint tail to 64 ready
  milestones.
- Snapshot audit `370` freezes the new rollup.

## Key Numbers

```text
previous next safe output ID:           1853
current numeric ID:                     1853
current output ID entries:              1
current doc ID entries:                 1
next safe output ID after current:      1854
required guards passed:                 5 / 5
checkpoint tail milestones:             64 / 64 ready
checkpoint promotions:                  0
```

## Decision

Use `1854` as the next safe output numeric ID for subsequent experiment
outputs. Any cleanup of older collided IDs should be planned separately; no
renumbering, moving, or deletion was performed in this checkpoint.

## Validation

```text
11 focused tests passed
py_compile passed for the four allocation/checkpoint scripts and tests
figure 1853 dynamic range=255
figures 368-370 dynamic range=255
scoped whitespace and diff checks clean
```

## Artifacts

```text
outputs/experiments/1853_experiment_archive_next_id_allocation_guard
outputs/_generated_checkpoints/snapshot_audits/368_result_milestone_snapshot_audit_experiment_archive_next_id_allocation_guard_refresh
outputs/_generated_checkpoints/cross_track/369_local_bem_field_2d_checkpoint_tail_post_experiment_archive_next_id_allocation_rollup
outputs/_generated_checkpoints/snapshot_audits/370_result_milestone_snapshot_audit_checkpoint_tail_post_experiment_archive_next_id_allocation_rollup_refresh
```

The marathon request remains active; the next defensible task is another
bounded BEM, field, synthetic 2D, reporting, or tooling branch that preserves
the current compute gates.

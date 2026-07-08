# Synthetic Status-V6 Field-Recheck Next-ID Guard Checkpoint

Date: 2026-07-02

## What Changed

Closed the synthetic 2D refresh after the post-status-v6 field live-receipt
recheck:

- Experiment `1870` refreshes the synthetic 2D next-question matrix from
  existing archive evidence only.
- Experiment `1871` verifies that `1870` consumed the advertised next safe ID
  and advances the next safe experiment output ID to `1872`.
- Snapshot audit `474` freezes the `1870` and `1871` scripts.
- Cross-track rollup `475` updates the generated checkpoint tail to 136 ready
  milestones.
- Snapshot audit `476` freezes the new rollup.

## Key Numbers

```text
synthetic candidate questions:       10
top synthetic question:              synthetic_publication_bundle_current
immediate / conditional GPU rows:    0 / 0
archive consumed/current IDs:        1870 / 1871
next safe output ID:                 1872
checkpoint tail milestones:          136 / 136 ready
checkpoint promotions:               0
```

## Artifacts

```text
outputs/experiments/1870_synthetic_2d_next_question_matrix_post_status_v6_field_recheck_refresh
outputs/experiments/1871_experiment_archive_post_synthetic_status_v6_field_recheck_next_id_guard
outputs/_generated_checkpoints/snapshot_audits/474_result_milestone_snapshot_audit_synthetic_status_v6_field_recheck_next_id_guard_refresh
outputs/_generated_checkpoints/cross_track/475_local_bem_field_2d_checkpoint_tail_post_synthetic_status_v6_field_recheck_next_id_guard_rollup
outputs/_generated_checkpoints/snapshot_audits/476_result_milestone_snapshot_audit_checkpoint_tail_post_synthetic_status_v6_field_recheck_next_id_guard_rollup_refresh
```

## Validation

```text
focused tests passed for the synthetic/archive branch
py_compile passed for the 1870-1871 and 474-476 scripts and tests
figures 1870-1871 and 474-476 dynamic ranges verified
scoped whitespace and full diff checks clean
```

The marathon request remains active; the next defensible task is another
bounded BEM, field, synthetic 2D, reporting, or tooling branch that preserves
the current compute gates.

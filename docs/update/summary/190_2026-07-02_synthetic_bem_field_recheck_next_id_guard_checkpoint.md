# Synthetic BEM/Field Recheck Next-ID Guard Checkpoint

Date: 2026-07-02

## What Changed

Closed the synthetic 2D refresh after the post-BEM/archive field recheck:

- Experiment `1866` refreshes the synthetic 2D next-question matrix from
  existing archive evidence only.
- Experiment `1867` verifies that `1866` consumed the advertised next safe ID
  and advances the next safe experiment output ID to `1868`.
- Snapshot audit `460` freezes the `1866` and `1867` scripts.
- Cross-track rollup `461` updates the generated checkpoint tail to 126 ready
  milestones.
- Snapshot audit `462` freezes the new rollup.

## Key Numbers

```text
synthetic candidate questions:       10
top synthetic question:              synthetic_publication_bundle_current
immediate / conditional GPU rows:    0 / 0
archive consumed/current IDs:        1866 / 1867
next safe output ID:                 1868
checkpoint tail milestones:          126 / 126 ready
checkpoint promotions:               0
```

## Artifacts

```text
outputs/experiments/1866_synthetic_2d_next_question_matrix_post_field_bem_archive_guard_refresh
outputs/experiments/1867_experiment_archive_post_synthetic_bem_field_recheck_next_id_guard
outputs/_generated_checkpoints/snapshot_audits/460_result_milestone_snapshot_audit_synthetic_bem_field_recheck_next_id_guard_refresh
outputs/_generated_checkpoints/cross_track/461_local_bem_field_2d_checkpoint_tail_post_synthetic_bem_field_recheck_next_id_guard_rollup
outputs/_generated_checkpoints/snapshot_audits/462_result_milestone_snapshot_audit_checkpoint_tail_post_synthetic_bem_field_recheck_next_id_guard_rollup_refresh
```

## Validation

```text
focused tests passed for the synthetic/archive branch
py_compile passed for the 1866-1867 and 460-462 scripts and tests
figures 1866-1867 and 460-462 dynamic ranges verified
scoped whitespace and full diff checks clean
```

The marathon request remains active; the next defensible task is another
bounded BEM, field, synthetic 2D, reporting, or tooling branch that preserves
the current compute gates.

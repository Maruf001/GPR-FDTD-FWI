# Synthetic Status-V6 Field BEM-Guard Synthetic Next-ID Checkpoint

Date: 2026-07-02

## What Changed

Closed the synthetic 2D refresh after the post-synthetic-status-v6-field BEM
recheck guard:

- Experiment `1874` refreshes the synthetic 2D next-question matrix from
  existing archive evidence only.
- Experiment `1875` verifies that `1874` consumed the advertised next safe ID
  and advances the next safe experiment output ID to `1876`.
- Snapshot audit `480` freezes the `1874` and `1875` scripts.
- Cross-track rollup `481` updates the generated checkpoint tail to 140 ready
  milestones.
- Snapshot audit `482` freezes the new rollup.

## Key Numbers

```text
synthetic candidate questions:       10
top synthetic question:              synthetic_publication_bundle_current
immediate / conditional GPU rows:    0 / 0
archive consumed/current IDs:        1874 / 1875
next safe output ID:                 1876
checkpoint tail milestones:          140 / 140 ready
checkpoint promotions:               0
```

## Artifacts

```text
outputs/experiments/1874_synthetic_2d_next_question_matrix_post_synthetic_status_v6_field_bem_guard_refresh
outputs/experiments/1875_experiment_archive_post_synthetic_status_v6_field_bem_guard_synthetic_next_id_guard
outputs/_generated_checkpoints/snapshot_audits/480_result_milestone_snapshot_audit_synthetic_status_v6_field_bem_guard_synthetic_next_id_refresh
outputs/_generated_checkpoints/cross_track/481_local_bem_field_2d_checkpoint_tail_post_synthetic_status_v6_field_bem_guard_synthetic_next_id_rollup
outputs/_generated_checkpoints/snapshot_audits/482_result_milestone_snapshot_audit_checkpoint_tail_post_synthetic_status_v6_field_bem_guard_synthetic_next_id_rollup_refresh
```

## Validation

```text
focused tests passed for the synthetic/archive branch
py_compile passed for the 1874-1875 and 480-482 scripts and tests
figures 1874-1875 and 480-482 dynamic ranges verified
full diff check clean
```

The next safe experiment output ID is `1876`; 3D FDTD remains deferred.

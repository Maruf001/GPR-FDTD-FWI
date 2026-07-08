# Synthetic Status-V6 Field BEM-Recheck Next-ID Guard Checkpoint

Date: 2026-07-02

## What Changed

Closed the BEM receipt recheck after the synthetic status-v6 field guard:

- Experiment `1872` reruns the BEM stage-1 external artifact receipt sentinel
  after `1871` advertised `1872` as the next safe output ID.
- Experiment `1873` verifies that `1872` consumed the advertised next safe ID
  and advances the next safe experiment output ID to `1874`.
- Snapshot audit `477` freezes the `1872` and `1873` scripts.
- Cross-track rollup `478` updates the generated checkpoint tail to 138 ready
  milestones.
- Snapshot audit `479` freezes the new rollup.

## Key Numbers

```text
BEM live / missing artifacts:       0 / 2
BEM acceptance-ready rows:          0
BEM blocking decisions:             2
archive consumed/current IDs:       1872 / 1873
next safe output ID:                1874
checkpoint tail milestones:         138 / 138 ready
checkpoint promotions:              0
```

## Artifacts

```text
outputs/experiments/1872_local_2d_bem_stage1_complex_fdtd_external_artifact_receipt_recheck_post_synthetic_status_v6_field_guard
outputs/experiments/1873_experiment_archive_post_synthetic_status_v6_field_bem_recheck_next_id_guard
outputs/_generated_checkpoints/snapshot_audits/477_result_milestone_snapshot_audit_synthetic_status_v6_field_bem_recheck_next_id_guard_refresh
outputs/_generated_checkpoints/cross_track/478_local_bem_field_2d_checkpoint_tail_post_synthetic_status_v6_field_bem_recheck_next_id_guard_rollup
outputs/_generated_checkpoints/snapshot_audits/479_result_milestone_snapshot_audit_checkpoint_tail_post_synthetic_status_v6_field_bem_recheck_next_id_guard_rollup_refresh
```

## Validation

```text
focused tests passed for the BEM/archive branch
py_compile passed for the 1872-1873 and 477-479 scripts and tests
figures 1872-1873 and 477-479 dynamic ranges verified
full diff check clean
```

Per the latest user instruction, the marathon pauses after this fully completed
block; the next intended work stream is 3D FDTD.

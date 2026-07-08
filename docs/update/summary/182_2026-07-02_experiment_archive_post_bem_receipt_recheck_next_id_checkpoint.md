# Experiment Archive Post-BEM-Receipt-Recheck Next ID Checkpoint

Date: 2026-07-02

## What Changed

Closed the experiment archive guard after the BEM receipt recheck:

- Experiment `1861` verifies that experiment `1860` consumed the previously
  advertised next safe experiment ID.
- Snapshot audit `432` freezes experiment `1861`.
- Cross-track rollup `433` updates the generated checkpoint tail to 106 ready
  milestones and includes prior rollup audit `431`.
- Snapshot audit `434` freezes the new rollup.

## Key Numbers

```text
previous next safe ID:               1860
consumed numeric ID:                 1860
current guard numeric ID:            1861
consumed output/doc entries:         1 / 1
current output/doc entries:          1 / 1
next safe output ID:                 1862
source live/missing files:           0 / 2
source blocking decisions:           2
checkpoint tail milestones:          106 / 106 ready
checkpoint promotions:               0
```

## Artifacts

```text
outputs/experiments/1861_experiment_archive_post_bem_receipt_recheck_next_id_guard
outputs/_generated_checkpoints/snapshot_audits/432_result_milestone_snapshot_audit_experiment_archive_post_bem_receipt_recheck_next_id_guard_refresh
outputs/_generated_checkpoints/cross_track/433_local_bem_field_2d_checkpoint_tail_post_experiment_archive_post_bem_receipt_recheck_next_id_guard_rollup
outputs/_generated_checkpoints/snapshot_audits/434_result_milestone_snapshot_audit_checkpoint_tail_post_experiment_archive_post_bem_receipt_recheck_next_id_guard_rollup_refresh
```

## Validation

```text
focused tests passed for the post-BEM-receipt next-ID branch
py_compile passed for the 1861 and 432-434 scripts and tests
figure 1861 dynamic range verified
figures 432-434 dynamic range verified
scoped whitespace and diff checks clean
```

The marathon request remains active; the next defensible task is another
bounded BEM, field, synthetic 2D, reporting, or tooling branch that preserves
the current compute gates.

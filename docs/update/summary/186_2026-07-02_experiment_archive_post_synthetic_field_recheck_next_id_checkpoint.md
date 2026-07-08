# Experiment Archive Post-Synthetic-Field-Recheck Next ID Checkpoint

Date: 2026-07-02

## What Changed

Closed the experiment archive guard after the post-field-recheck synthetic
matrix:

- Experiment `1863` verifies that experiment `1862` consumed the previously
  advertised next safe experiment ID.
- Snapshot audit `446` freezes experiment `1863`.
- Cross-track rollup `447` updates the generated checkpoint tail to 116 ready
  milestones and includes prior rollup audit `445`.
- Snapshot audit `448` freezes the new rollup.

## Key Numbers

```text
previous next safe ID:               1862
consumed numeric ID:                 1862
current guard numeric ID:            1863
consumed output/doc entries:         1 / 1
current output/doc entries:          1 / 1
next safe output ID:                 1864
source candidate questions:          10
source GPU candidates:               0 immediate / 0 conditional
checkpoint tail milestones:          116 / 116 ready
checkpoint promotions:               0
```

## Artifacts

```text
outputs/experiments/1863_experiment_archive_post_synthetic_field_recheck_next_id_guard
outputs/_generated_checkpoints/snapshot_audits/446_result_milestone_snapshot_audit_experiment_archive_post_synthetic_field_recheck_next_id_guard_refresh
outputs/_generated_checkpoints/cross_track/447_local_bem_field_2d_checkpoint_tail_post_experiment_archive_post_synthetic_field_recheck_next_id_guard_rollup
outputs/_generated_checkpoints/snapshot_audits/448_result_milestone_snapshot_audit_checkpoint_tail_post_experiment_archive_post_synthetic_field_recheck_next_id_guard_rollup_refresh
```

## Validation

```text
focused tests passed for the post-synthetic-field-recheck next-ID branch
py_compile passed for the 1863 and 446-448 scripts and tests
figure 1863 dynamic range verified
figures 446-448 dynamic range verified
scoped whitespace and diff checks clean
```

The marathon request remains active; the next defensible task is another
bounded BEM, field, synthetic 2D, reporting, or tooling branch that preserves
the current compute gates.

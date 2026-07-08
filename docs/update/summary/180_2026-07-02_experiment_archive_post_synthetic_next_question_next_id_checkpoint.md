# Experiment Archive Post-Synthetic-Next-Question Next ID Checkpoint

Date: 2026-07-02

## What Changed

Closed the experiment archive guard after the synthetic next-question matrix:

- Experiment `1859` verifies that experiment `1858` consumed the previously
  advertised next safe experiment ID.
- Snapshot audit `426` freezes experiment `1859`.
- Cross-track rollup `427` updates the generated checkpoint tail to 102 ready
  milestones and includes prior rollup audit `425`.
- Snapshot audit `428` freezes the new rollup.

## Key Numbers

```text
previous next safe ID:               1858
consumed numeric ID:                 1858
current guard numeric ID:            1859
consumed output/doc entries:         1 / 1
current output/doc entries:          1 / 1
next safe output ID:                 1860
source candidate questions:          10
source GPU candidates:               0 immediate / 0 conditional
checkpoint tail milestones:          102 / 102 ready
checkpoint promotions:               0
```

## Artifacts

```text
outputs/experiments/1859_experiment_archive_post_synthetic_next_question_next_id_guard
outputs/_generated_checkpoints/snapshot_audits/426_result_milestone_snapshot_audit_experiment_archive_post_synthetic_next_question_next_id_guard_refresh
outputs/_generated_checkpoints/cross_track/427_local_bem_field_2d_checkpoint_tail_post_experiment_archive_post_synthetic_next_question_next_id_guard_rollup
outputs/_generated_checkpoints/snapshot_audits/428_result_milestone_snapshot_audit_checkpoint_tail_post_experiment_archive_post_synthetic_next_question_next_id_guard_rollup_refresh
```

## Validation

```text
focused tests passed for the post-synthetic-next-question next-ID branch
py_compile passed for the 1859 and 426-428 scripts and tests
figure 1859 dynamic range verified
figures 426-428 dynamic range verified
scoped whitespace and diff checks clean
```

The marathon request remains active; the next defensible task is another
bounded BEM, field, synthetic 2D, reporting, or tooling branch that preserves
the current compute gates.

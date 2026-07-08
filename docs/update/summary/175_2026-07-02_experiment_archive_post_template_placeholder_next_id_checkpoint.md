# Experiment Archive Post-Template-Placeholder Next ID Checkpoint

Date: 2026-07-02

## What Changed

Closed the archive next-ID guard after the BEM template placeholder validator:

- Experiment `1857` verifies that `1856` consumed the previously advertised
  next safe experiment ID and advances the next safe output ID to `1858`.
- Snapshot audit `408` freezes experiment `1857`.
- Cross-track rollup `409` updates the generated checkpoint tail to 89 ready
  milestones and includes prior rollup audit `407`.
- Snapshot audit `410` freezes the new rollup.

## Key Numbers

```text
previous next safe ID:                1856
consumed experiment ID:               1856
current guard ID:                     1857
next safe output ID:                  1858
consumed output/doc entries:           1 / 1
current output/doc entries:            1 / 1
duplicate collision IDs tracked:       5
checkpoint tail milestones:           89 / 89 ready
checkpoint promotions:                 0
```

## Artifacts

```text
outputs/experiments/1857_experiment_archive_post_template_placeholder_next_id_guard
outputs/_generated_checkpoints/snapshot_audits/408_result_milestone_snapshot_audit_experiment_archive_post_template_placeholder_next_id_guard_refresh
outputs/_generated_checkpoints/cross_track/409_local_bem_field_2d_checkpoint_tail_post_experiment_archive_post_template_placeholder_next_id_guard_rollup
outputs/_generated_checkpoints/snapshot_audits/410_result_milestone_snapshot_audit_checkpoint_tail_post_experiment_archive_post_template_placeholder_next_id_guard_rollup_refresh
```

## Validation

```text
focused tests passed for the post-template-placeholder next-ID guard branch
py_compile passed for the 1857/408-410 scripts and tests
figure 1857 dynamic range verified
figures 408-410 dynamic range verified
scoped whitespace and diff checks clean
```

The marathon request remains active; the next defensible task is another
bounded BEM, field, synthetic 2D, reporting, or tooling branch that preserves
the current compute gates.

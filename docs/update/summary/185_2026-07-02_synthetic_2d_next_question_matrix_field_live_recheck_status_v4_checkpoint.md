# Synthetic 2D Next-Question Matrix Field Live Recheck Status V4 Checkpoint

Date: 2026-07-02

## What Changed

Closed a synthetic 2D next-question refresh after the field live-receipt
recheck:

- Experiment `1862` refreshes the synthetic 2D next-question matrix from
  existing archive evidence only.
- Snapshot audit `443` freezes experiment `1862`.
- Cross-track rollup `444` updates the generated checkpoint tail to 114 ready
  milestones and includes prior rollup audit `442`.
- Snapshot audit `445` freezes the new rollup.

## Key Numbers

```text
candidate questions:                  10
top question:        synthetic_publication_bundle_current
immediate GPU candidates:              0
conditional GPU candidates:            0
target1 acquisition surface included:  true
target1 exception map included:        true
checkpoint tail milestones:          114 / 114 ready
checkpoint promotions:                 0
```

## Artifacts

```text
outputs/experiments/1862_synthetic_2d_next_question_matrix_post_field_live_recheck_status_v4_refresh
outputs/_generated_checkpoints/snapshot_audits/443_result_milestone_snapshot_audit_synthetic_2d_next_question_matrix_post_field_live_recheck_status_v4_refresh
outputs/_generated_checkpoints/cross_track/444_local_bem_field_2d_checkpoint_tail_post_synthetic_2d_next_question_matrix_field_live_recheck_status_v4_rollup
outputs/_generated_checkpoints/snapshot_audits/445_result_milestone_snapshot_audit_checkpoint_tail_post_synthetic_2d_next_question_matrix_field_live_recheck_status_v4_rollup_refresh
```

## Validation

```text
focused tests passed for the synthetic matrix post-field-live-recheck branch
py_compile passed for the 443-445 scripts and tests
figure 1862 dynamic range verified
figures 443-445 dynamic range verified
scoped whitespace and diff checks clean
```

The marathon request remains active; the next defensible task is another
bounded BEM, field, synthetic 2D, reporting, or tooling branch that preserves
the current compute gates.

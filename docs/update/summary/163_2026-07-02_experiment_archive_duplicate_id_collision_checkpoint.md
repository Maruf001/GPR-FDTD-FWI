# Experiment Archive Duplicate ID Collision Checkpoint

Date: 2026-07-02

## What Changed

Closed a non-destructive duplicate-ID audit for the experiment archive:

- Experiment `1852` scans numbered experiment output folders and experiment
  documentation files for numeric ID collisions.
- Snapshot audit `365` freezes experiment `1852`.
- Cross-track rollup `366` updates the generated checkpoint tail to 63 ready
  milestones.
- Snapshot audit `367` freezes the new rollup.

## Key Numbers

```text
output entries:                         1853
output unique numeric IDs:              1852
doc entries:                            1398
doc unique numeric IDs:                 1393
collision IDs:                          5
output duplicate IDs:                   1
doc duplicate IDs:                      5
recent tail collisions:                 1
next safe output ID:                    1853
checkpoint tail milestones:             63 / 63 ready
checkpoint promotions:                  0
```

Current output-archive collision: ID `1848`.

Doc collisions: IDs `13`, `656`, `665`, `672`, and `1848`.

## Decision

Do not reuse collided IDs. Use `1853` as the next safe output numeric ID for
new experiment outputs, and plan any collision cleanup separately. This audit
does not rename, move, or delete existing artifacts.

## Validation

```text
11 focused tests passed
py_compile passed for the four duplicate-ID/checkpoint scripts and tests
figure 1852 dynamic range=255
figures 365-367 dynamic range=255
scoped whitespace and diff checks clean
```

## Artifacts

```text
outputs/experiments/1852_experiment_archive_duplicate_id_collision_audit
outputs/_generated_checkpoints/snapshot_audits/365_result_milestone_snapshot_audit_experiment_archive_duplicate_id_collision_refresh
outputs/_generated_checkpoints/cross_track/366_local_bem_field_2d_checkpoint_tail_post_experiment_archive_duplicate_id_collision_rollup
outputs/_generated_checkpoints/snapshot_audits/367_result_milestone_snapshot_audit_checkpoint_tail_post_experiment_archive_duplicate_id_collision_rollup_refresh
```

The marathon request remains active; the next defensible task is another
bounded BEM, field, synthetic 2D, reporting, or tooling branch that preserves
the current compute gates.

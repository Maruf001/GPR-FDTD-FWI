# wk06 3D FDTD Report Artifact Integrity Checkpoint

Date: 2026-07-01

## Scope

This checkpoint records the integrity audit for the wk06 3D FDTD report
notebook, PDF, and extracted PNG figures, plus the generated-checkpoint rollup
that includes those artifacts.

## Output

```text
outputs/summary_tables/wk06/3d_fdtd
outputs/_generated_checkpoints/team_reporting/325_wk06_3d_fdtd_report_artifact_integrity_audit
outputs/_generated_checkpoints/snapshot_audits/326_result_milestone_snapshot_audit_wk06_3d_fdtd_report_artifact_integrity_refresh
outputs/_generated_checkpoints/cross_track/327_local_bem_field_2d_checkpoint_tail_post_wk06_report_artifacts_rollup
outputs/_generated_checkpoints/snapshot_audits/328_result_milestone_snapshot_audit_checkpoint_tail_post_wk06_report_artifacts_rollup_refresh
```

## Result

```text
notebook present:             true
pdf present:                  true
png figures:                     6
valid png figures:               6
embedded notebook image outputs: 0
pdf size bytes:            1655823
total png bytes:           1410951
artifact rows:                   8
artifact hashes:                 8
snapshot 326 milestones passed:  1/1
snapshot 326 SHA matches:        2/2
checkpoint 327 milestones ready: 48/48
checkpoint 327 promotions:       0
snapshot 328 milestones passed:  1/1
snapshot 328 SHA matches:        2/2
```

## Decision

Use the PDF plus six PNG files in `outputs/summary_tables/wk06/3d_fdtd` for the
wk06 3D FDTD report handoff. Runs `325-328` are the frozen artifact-integrity
and checkpoint-tail record. No FDTD execution, BEM/FDTD comparison, field
transfer, GPU, or 3D claim is promoted by this report artifact audit.

## Validation

Focused tests:

```text
tests/test_wk06_3d_fdtd_report_artifact_integrity_audit.py
tests/test_result_milestone_snapshot_audit_wk06_3d_fdtd_report_artifact_integrity_refresh.py
tests/test_local_bem_field_2d_checkpoint_tail_post_wk06_report_artifacts_rollup.py
tests/test_result_milestone_snapshot_audit_checkpoint_tail_post_wk06_report_artifacts_rollup_refresh.py
13 passed
```

Figure checks:

```text
325 artifact audit: 1528x736, dynamic range=255
326 snapshot audit: 1276x666, dynamic range=255
327 checkpoint rollup: 1672x738, dynamic range=255
328 rollup snapshot audit: 1276x666, dynamic range=255
```

## Marathon State

The requested 30-hour autonomous marathon is still active. This artifact
integrity checkpoint is not a stop condition.

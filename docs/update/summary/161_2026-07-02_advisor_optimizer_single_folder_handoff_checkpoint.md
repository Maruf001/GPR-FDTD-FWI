# Advisor Optimizer Single-Folder Handoff Checkpoint

Date: 2026-07-02

## What Changed

Closed a refreshed advisor-facing optimizer script handoff block:

- Team report `358` copies the existing optimizer bundle into a generated
  single send folder and verifies every copied file by SHA-256.
- Snapshot audit `359` freezes report `358`.
- Cross-track rollup `360` updates the generated checkpoint tail to 61 ready
  milestones.
- Snapshot audit `361` freezes the new rollup.

## Key Numbers

```text
source files:                          58
copied files:                          58
copy hash matches:                     58
missing copies:                        0
copy hash mismatches:                  0
root entrypoints:                      17
inversion modules:                     16
core modules:                          9
source bytes:                          644722
copied bytes:                          644722
zip bytes:                             183205
checkpoint tail milestones:            61 / 61 ready
checkpoint promotions:                 0
```

## Send Folder

```text
outputs/_generated_checkpoints/team_reporting/358_advisor_optimizer_single_folder_handoff_refresh/advisor_send_folder/advisor_optimizer_scripts_2026-07-01
outputs/_generated_checkpoints/team_reporting/358_advisor_optimizer_single_folder_handoff_refresh/advisor_send_folder/advisor_optimizer_scripts_2026-07-01.zip
```

## Decision

Use the generated `advisor_send_folder` copy when the advisor needs the key
optimizer scripts in one folder. The copied folder and zip match the existing
source bundle byte-for-byte and do not alter compute gates.

Project-FDTD execution, field FWI, field transfer, GPU escalation, and 3D/HPC
remain blocked.

## Validation

```text
12 focused tests passed
py_compile passed for the four handoff/checkpoint scripts and tests
figure 358 dynamic range=255
figures 359-361 dynamic range=255
scoped whitespace and diff checks clean
```

## Artifacts

```text
outputs/_generated_checkpoints/team_reporting/358_advisor_optimizer_single_folder_handoff_refresh
outputs/_generated_checkpoints/snapshot_audits/359_result_milestone_snapshot_audit_advisor_optimizer_single_folder_handoff_refresh
outputs/_generated_checkpoints/cross_track/360_local_bem_field_2d_checkpoint_tail_post_advisor_optimizer_handoff_rollup
outputs/_generated_checkpoints/snapshot_audits/361_result_milestone_snapshot_audit_checkpoint_tail_post_advisor_optimizer_handoff_rollup_refresh
```

The marathon request remains active; the next defensible task is another
bounded BEM, field, synthetic 2D, reporting, or tooling branch that preserves
the current compute gates.

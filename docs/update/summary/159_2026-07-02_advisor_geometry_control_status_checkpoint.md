# Advisor Geometry-Control Status Checkpoint

Date: 2026-07-02

## What Changed

Closed the advisor geometry-control status reporting block:

- Team report `351` packages the current sendable artifacts, BEM
  acquisition-geometry lock policy, field acquisition-geometry controls, and
  latest checkpoint tail.
- Snapshot audit `352` freezes report `351`.
- Cross-track rollup `353` updates the generated checkpoint tail to 58 ready
  milestones.
- Snapshot audit `354` freezes the new rollup.

## Key Numbers

```text
advisor delivery items:                 5 / 5 ready
sendable artifacts:                     2
geometry guards:                        2
BEM required geometry locks:            8
BEM geometry/depth-material L2 ratio:   14.0411791425335
field geometry controls satisfied:      0 / 6
field live files:                       0
field missing files:                    18
checkpoint tail milestones:             58 / 58 ready
checkpoint promotions:                  0
```

## Decision

Use report `351` as the current advisor-facing geometry-control status packet.
It is safe to send as a status artifact, with explicit caveats that BEM/FDTD
interpretation requires acquisition-geometry locks and field evidence remains
blocked until first-return DZT files and paired metadata arrive.

Project-FDTD execution, field FWI, field transfer, GPU escalation, and 3D/HPC
remain blocked.

## Validation

```text
13 focused tests passed
py_compile passed for the four packet/checkpoint scripts
figure 351 dynamic range=255
figures 352-354 dynamic range=255
scoped whitespace and diff checks clean
```

## Artifacts

```text
outputs/_generated_checkpoints/team_reporting/351_advisor_geometry_control_status_packet
outputs/_generated_checkpoints/snapshot_audits/352_result_milestone_snapshot_audit_advisor_geometry_control_status_packet_refresh
outputs/_generated_checkpoints/cross_track/353_local_bem_field_2d_checkpoint_tail_post_advisor_geometry_control_status_rollup
outputs/_generated_checkpoints/snapshot_audits/354_result_milestone_snapshot_audit_checkpoint_tail_post_advisor_geometry_control_status_rollup_refresh
```

The marathon request remains active; the next defensible task is another
bounded BEM, field, synthetic 2D, reporting, or tooling branch that preserves
the current compute gates.

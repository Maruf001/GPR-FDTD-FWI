# Field Acquisition-Geometry Control Checkpoint

Date: 2026-07-02

## What Changed

Closed the field acquisition-geometry control block:

- Run `643` converts the guarded BEM acquisition-geometry sensitivity result
  into six collection-day geometry metadata controls.
- Run `644` validates the control audit.
- Run `645` sensitivity-hardens the validator.
- Snapshot audit `348` freezes runs `643-645`.
- Cross-track rollup `349` updates the generated checkpoint tail to 56 ready
  milestones.
- Snapshot audit `350` freezes the new rollup.

## Key Numbers

```text
geometry controls:                      6
metadata-required controls:             6
currently satisfied controls:           0
expected metadata files:                9
expected DZT files:                     9
live files:                             0
missing files:                          18
BEM peak offset span at z=0:            2.6214537950832346 dB
BEM max relative L2 across offset:      0.7099232724148534
BEM max relative L2 across antenna z:   0.4171376953084501
sensitivity scenarios:                  26
damaged scenarios rejected:             25
checkpoint tail milestones:             56 / 56 ready
checkpoint promotions:                  0
```

## Decision

Use runs `643-645` as the guarded field acquisition-geometry control block.
The collection-day packet remains a metadata-control checklist only: field
evidence, field FWI, GPU escalation, and field 3D/HPC stay blocked until the
first-return DZT files and paired geometry metadata are present and pass the
guarded acceptance path.

## Validation

```text
20 focused tests passed
py_compile passed for the six branch/checkpoint scripts
figure 645 dynamic range=255
figures 348-350 dynamic range=255
scoped whitespace and diff checks clean
```

## Artifacts

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/643_gssi51600s_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit
outputs/field_experiments/local_gssi_51600s_2026_06_09/644_gssi51600s_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit_validator
outputs/field_experiments/local_gssi_51600s_2026_06_09/645_gssi51600s_controlled_collection_trace_pairing_collection_day_acquisition_geometry_control_audit_validation_sensitivity
outputs/_generated_checkpoints/snapshot_audits/348_result_milestone_snapshot_audit_field_acquisition_geometry_control_refresh
outputs/_generated_checkpoints/cross_track/349_local_bem_field_2d_checkpoint_tail_post_field_acquisition_geometry_control_rollup
outputs/_generated_checkpoints/snapshot_audits/350_result_milestone_snapshot_audit_checkpoint_tail_post_field_acquisition_geometry_control_rollup_refresh
```

The marathon request remains active; the next defensible task is another
bounded BEM, field, synthetic 2D, reporting, or tooling branch that preserves
the current compute gates.

# Field Acceptance Rerun Decision Checkpoint

Date: 2026-07-02

## What Changed

Added a guarded field first-return acceptance-rerun decision block:

- Field runs `640-642` convert the no-file live-state refresh from runs
  `637-639` into an explicit acceptance-rerun decision gate, validator, and
  sensitivity suite.
- Snapshot audit `329` freezes the scripts for runs `640-642`.
- Cross-track rollup `330` updates the generated checkpoint tail to
  49 ready milestones with zero promotions.
- Snapshot audit `331` freezes the new rollup.

## Key Numbers

```text
expected first-return files:           18
live files found:                      0
missing files:                         18
observed hashes / sizes:               0 / 0
metadata parseable / DZT candidates:   0 / 0
decision checks:                       6
blocking decision checks:              2
acceptance rerun authorized now:        false
decision sensitivity scenarios:        24
damaged scenarios rejected:            23
checkpoint rollup milestones:          49 / 49 ready
checkpoint promotions:                 0
```

## Decision

Do not rerun the first-return acceptance gate until all 18 expected files are
present and preliminary receipt observations are populated. Controlled field
evidence, field FWI, field transfer, field 3D/HPC, and GPU-priority promotion
remain blocked.

## Validation

```text
33 focused tests passed
py_compile passed for the new scripts
new checkpoint figures: dynamic range=255
scoped whitespace and diff checks clean
```

## Artifacts

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/640_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_acceptance_rerun_decision_gate
outputs/field_experiments/local_gssi_51600s_2026_06_09/641_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_acceptance_rerun_decision_gate_validator
outputs/field_experiments/local_gssi_51600s_2026_06_09/642_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_acceptance_rerun_decision_gate_validation_sensitivity
outputs/_generated_checkpoints/snapshot_audits/329_result_milestone_snapshot_audit_field_acceptance_rerun_decision_refresh
outputs/_generated_checkpoints/cross_track/330_local_bem_field_2d_checkpoint_tail_post_field_acceptance_rerun_decision_rollup
outputs/_generated_checkpoints/snapshot_audits/331_result_milestone_snapshot_audit_checkpoint_tail_post_field_acceptance_rerun_decision_rollup_refresh
```

The marathon request remains active; the next defensible task is another
bounded audit or packaging branch that does not promote blocked field compute.

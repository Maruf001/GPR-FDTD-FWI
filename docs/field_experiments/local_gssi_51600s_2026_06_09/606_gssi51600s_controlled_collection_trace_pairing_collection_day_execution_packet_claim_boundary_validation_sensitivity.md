# Field Experiment 606: Collection-Day Execution Packet Claim Boundary Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `605` validator by damaging the saved run `604` field claim
boundary in controlled ways.

The sensitivity set checks source-readiness damage, claim-count damage,
guarded/blocked support damage, live-return promotion, action-acceptance
promotion, field-evidence promotion, field FWI/3D promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/606_gssi51600s_controlled_collection_trace_pairing_collection_day_execution_packet_claim_boundary_validation_sensitivity
```

## Result

```text
scenarios:                         19
expected passes:                    1
expected failures:                 18
observed passes:                    1
observed failures:                 18
unexpected outcomes:                0
damaged scenarios:                 18
damaged scenarios rejected:        18
gpu priority:                    none
```

The exact saved field claim boundary passes. All damaged states fail:

```text
policy-label damage
boundary-readiness damage
source-readiness damage
claim-shape damage
guarded-count damage
blocked-count damage
guarded-support damage
blocked-support promotion
slot-count damage
live-file requirement damage
live-DZT promotion
live-metadata promotion
accepted-action promotion
field-evidence promotion
field-FWI promotion
field-3D/HPC promotion
figure damage
script-snapshot damage
```

## Interpretation

The field claim-boundary validator accepts only the exact saved evidence-blocked
state and rejects controlled damage to source readiness, claim counts, support
state, live returns, action acceptance, field evidence, field FWI/3D promotion,
figure validation, and script snapshots.

## Decision

Use runs `604-606` as the guarded post-execution-packet field claim-boundary
block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_execution_packet_claim_boundary.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_execution_packet_claim_boundary_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_execution_packet_claim_boundary_validation_sensitivity.py
8 passed
```

Figure check:

```text
3581x886, dynamic range=255
```

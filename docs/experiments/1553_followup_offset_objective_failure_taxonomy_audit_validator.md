# Experiment 1553: Follow-Up Offset Objective Failure Taxonomy Audit Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1552` objective-failure taxonomy audit from artifacts.

## Output

```text
outputs/experiments/1553_local_2d_state_consistent_objective_revision_followup_offset_objective_failure_taxonomy_audit_validator
```

## Result

```text
validation checks:                  6
passed checks:                      6
failed checks:                      0
taxonomy audit validation ready:    true
objective count:                    6
model count:                        20
offset count:                       5
objective failure rows:             40
dominant failure pattern:           base;early_high
all models share same pattern:      true
wide-window claim ready:            false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
3D/HPC ready:                       false
```

The validator confirms source identity, objective counts, row counts, the
`base;early_high` failure pattern, blocked downstream states, figure validation,
and script snapshots.

## Decision

Use this validator as the artifact guard for the run `1552` taxonomy audit.
Sensitivity hardening remains required before closing the block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_followup_offset_objective_failure_taxonomy_audit_validator.py
2 passed
```

Figure check:

```text
3041x895, dynamic range=255
```

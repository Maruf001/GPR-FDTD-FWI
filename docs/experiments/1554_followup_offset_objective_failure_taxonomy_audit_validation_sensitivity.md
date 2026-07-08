# Experiment 1554: Follow-Up Offset Objective Failure Taxonomy Audit Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1553` validator for the run `1552` objective-failure
taxonomy audit.

## Output

```text
outputs/experiments/1554_local_2d_state_consistent_objective_revision_followup_offset_objective_failure_taxonomy_audit_validation_sensitivity
```

## Result

```text
scenario count:                     10
expected pass count:                1
observed pass count:                1
expected failure count:             9
observed failure count:             9
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 1552:   true
validator rejects damaged variants: true
dominant failure pattern:           base;early_high
wide-window claim ready:            false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
3D/HPC ready:                       false
```

The exact run `1552` artifacts pass. Nine damaged variants fail as expected for
policy-label drift, objective-count drift, failure-pattern drift, objective-row
drift, model-pattern drift, offset-count drift, downstream promotion, figure
drift, and script-snapshot drift.

## Decision

Use runs `1552-1554` as the guarded 2D objective-failure taxonomy block. The
result explains the failure mechanism of the follow-up offset probe but does
not justify a physical, field, GPU, or 3D/HPC claim.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_followup_offset_objective_failure_taxonomy_audit_validation_sensitivity.py
2 passed
```

Combined focused taxonomy tests:

```text
tests/test_local_2d_state_consistent_objective_revision_followup_offset_objective_failure_taxonomy_audit.py
tests/test_local_2d_state_consistent_objective_revision_followup_offset_objective_failure_taxonomy_audit_validator.py
tests/test_local_2d_state_consistent_objective_revision_followup_offset_objective_failure_taxonomy_audit_validation_sensitivity.py
7 passed
```

Figure check:

```text
3257x891, dynamic range=255
```

# Experiment 1552: Follow-Up Offset Objective Failure Taxonomy Audit

Date: 2026-06-29

## Purpose

Audit the executed run `1546` follow-up offset probe by objective family. The
question is whether the 20 executed follow-up cases fail because every objective
breaks down, or because a smaller set of objectives is consistently responsible.

## Output

```text
outputs/experiments/1552_local_2d_state_consistent_objective_revision_followup_offset_objective_failure_taxonomy_audit
```

## Result

```text
objective count:                    6
model count:                        20
offset count:                       5
objective-selection rows:           120
objective failure rows:             40
objective pass rows:                80
universally failing objectives:     2
universally passing objectives:     4
dominant failure pattern:           base;early_high
dominant pattern model count:       20
all models share same pattern:      true
each model has two failed objectives: true
each offset has same failure count: true
wide-window claim ready:            false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
3D/HPC ready:                       false
```

The two universally failing objectives are `base` and `early_high`. The four
universally passing objectives are `highband`, `late`, `late_high`, and
`veryhigh`. All 20 follow-up models share the same failure pattern.

## Decision

Use this audit to explain why the executed follow-up offset probe remains
blocked: the failure is objective-family specific, not evidence for a broad
suppression window, physical acquisition rule, field transfer, GPU escalation,
or 3D/HPC escalation.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_followup_offset_objective_failure_taxonomy_audit.py
3 passed
```

Figure check:

```text
3761x923, dynamic range=255
```

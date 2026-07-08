# Experiment 1558: Follow-Up Objective Policy Recommendation

Date: 2026-06-29

## Purpose

Convert the guarded objective-failure taxonomy from runs `1552-1554` into a
narrow objective-policy recommendation for the saved follow-up offset probe.

This run does not launch FDTD, GPU work, field transfer, field FWI, or 3D/HPC.

## Output

```text
outputs/experiments/1558_local_2d_state_consistent_objective_revision_followup_objective_policy_recommendation
```

## Result

```text
objective-policy recommendation ready: true
objectives:                            6
candidate objectives:                  4
excluded objectives:                   2
manual-review objectives:              0
candidate objectives:                  highband;late;late_high;veryhigh
excluded objectives:                   base;early_high
candidate selection rows:              80
candidate failures:                    0
excluded selection rows:               40
excluded failures:                     40
models:                                20
dominant failure pattern:              base;early_high
gpu work ready:                        false
field transfer ready:                  false
3D/HPC ready:                          false
```

## Interpretation

For the saved follow-up offset probe only, retain `highband`, `late`,
`late_high`, and `veryhigh` as candidate objectives. Exclude `base` and
`early_high` because they fail universally across the saved objective-selection
rows.

## Validation

```text
tests/test_local_2d_state_consistent_objective_revision_followup_objective_policy_recommendation.py
2 passed
```

Figure validation:

```text
3761x923, dynamic range=255
```

# Experiment 1560: Follow-Up Objective Policy Recommendation Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1559` validator with damaged variants of the run `1558`
objective-policy recommendation.

## Output

```text
outputs/experiments/1560_local_2d_state_consistent_objective_revision_followup_objective_policy_recommendation_validation_sensitivity
```

## Result

```text
scenarios:                           13
expected pass:                       1
observed pass:                       1
expected failures:                   12
observed failures:                   12
unexpected outcomes:                 0
sensitivity ready:                   true
accepts exact run 1558:              true
rejects damaged variants:            true
objectives:                          6
candidate objectives:                4
excluded objectives:                 2
candidate objectives:                highband;late;late_high;veryhigh
excluded objectives:                 base;early_high
gpu work ready:                      false
```

Damaged variants fail for objective-count drift, candidate/excluded-list drift,
policy-row drift, group-count drift, scope drift, downstream promotion, figure
drift, and script-snapshot drift.

## Validation

```text
tests/test_local_2d_state_consistent_objective_revision_followup_objective_policy_recommendation.py
tests/test_local_2d_state_consistent_objective_revision_followup_objective_policy_recommendation_validator.py
tests/test_local_2d_state_consistent_objective_revision_followup_objective_policy_recommendation_validation_sensitivity.py
6 passed
```

Figure validation:

```text
3581x891, dynamic range=255
```

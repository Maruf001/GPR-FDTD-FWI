# Experiment 1563: Post Objective-Policy Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1562` validator with damaged variants of the run `1561`
post-objective-policy claim boundary.

## Output

```text
outputs/experiments/1563_local_2d_state_consistent_objective_revision_post_objective_policy_claim_boundary_validation_sensitivity
```

## Result

```text
scenarios:                            16
expected pass:                        1
observed pass:                        1
expected failures:                    15
observed failures:                    15
unexpected outcomes:                  0
sensitivity ready:                    true
accepts exact run 1561:               true
rejects damaged variants:             true
claims:                               24
candidate objectives:                 highband;late;late_high;veryhigh
excluded objectives:                  base;early_high
policy scope:                         saved_followup_offset_probe_only
gpu work ready:                       false
field transfer ready:                 false
3D/HPC ready:                         false
```

Damaged variants fail for source-label drift, claim-count drift,
base-boundary-count drift, objective-policy support drift, objective-policy
status drift, objective-policy evidence drift, candidate-list drift,
excluded-list drift, selection-row-count drift, policy-scope drift,
readiness demotion, blocked-support drift, downstream promotion, figure drift,
and script-snapshot drift.

## Validation

```text
tests/test_local_2d_state_consistent_objective_revision_post_objective_policy_claim_boundary.py
tests/test_local_2d_state_consistent_objective_revision_post_objective_policy_claim_boundary_validator.py
tests/test_local_2d_state_consistent_objective_revision_post_objective_policy_claim_boundary_validation_sensitivity.py
6 passed
```

Figure validation:

```text
3473x886, dynamic range=255
```

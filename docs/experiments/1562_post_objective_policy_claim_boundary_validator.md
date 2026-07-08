# Experiment 1562: Post Objective-Policy Claim-Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1561` post-objective-policy claim boundary from
artifacts.

## Output

```text
outputs/experiments/1562_local_2d_state_consistent_objective_revision_post_objective_policy_claim_boundary_validator
```

## Result

```text
validation checks:                    8
passed checks:                        8
failed checks:                        0
validation ready:                     true
claims:                               24
guarded claims:                       21
blocked claims:                       3
objectives:                           6
candidate objectives:                 4
excluded objectives:                  2
candidate objectives:                 highband;late;late_high;veryhigh
excluded objectives:                  base;early_high
policy scope:                         saved_followup_offset_probe_only
gpu work ready:                       false
field transfer ready:                 false
3D/HPC ready:                         false
```

The validator confirms the source identity, claim counts, base-boundary
relationship, objective-policy claim row, policy metrics, blocked claim rows,
blocked downstream states, figure validation, and script snapshots.

## Validation

```text
tests/test_local_2d_state_consistent_objective_revision_post_objective_policy_claim_boundary_validator.py
2 passed
```

Figure validation:

```text
3581x891, dynamic range=255
```

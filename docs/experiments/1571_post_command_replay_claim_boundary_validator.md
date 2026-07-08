# Experiment 1571: Post Command-Replay Claim-Boundary Validator

Date: 2026-06-29

## Purpose

Validate run `1570` from saved artifacts.

The validator checks claim counts, insertion of the executed replay claim,
replay metrics, objective-policy scope, blocked downstream states, figure
validation, and script snapshots.

## Output

```text
outputs/experiments/1571_local_2d_state_consistent_objective_revision_post_command_replay_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_command_replay_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_command_replay_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_command_replay_claim_boundary_validator.png
```

## Result

```text
validation checks:                 6
validation passes:                 6
blocking failures:                 0
claim-boundary validation ready:   true
local generalization boundary:     true
aggregate replay executed:         true
claims:                            25
guarded claims:                    22
blocked claims:                    3
grid models:                       20
objective rows:                    120
candidate rows:                    480
any-failure models:                20
all-objective-failure models:      0
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

## Decision

Use this validator as the artifact guard for run `1570`. Sensitivity testing
remains required before closing the post-command-replay claim-boundary block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_command_replay_claim_boundary_validator.py
5 passed as part of the 12-test focused set
```

Figure check:

```text
2645x867, dynamic range=255
```

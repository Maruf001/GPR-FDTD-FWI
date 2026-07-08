# Experiment 1577: Post Command-Replay Runtime-Audit Claim-Boundary Validator

Date: 2026-06-29

## Purpose

Validate run `1576` from saved artifacts.

The validator checks claim counts, runtime-claim support, runtime metrics,
blocked downstream states, figure validation, and script snapshots.

## Output

```text
outputs/experiments/1577_local_2d_state_consistent_objective_revision_post_command_replay_runtime_audit_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_command_replay_runtime_audit_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_command_replay_runtime_audit_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_command_replay_runtime_audit_claim_boundary_validator.png
```

## Result

```text
validation checks:                 5
validation passes:                 5
blocking failures:                 0
runtime-boundary validation ready: true
claims:                            26
guarded claims:                    23
blocked claims:                    3
elapsed seconds:                   782.566
seconds per grid model:            39.1283
seconds per candidate row:         1.63035
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

## Decision

Use this validator as the artifact guard for run `1576`. Sensitivity testing
remains required before closing the post-runtime-audit claim-boundary block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_command_replay_runtime_audit_claim_boundary_validator.py
5 passed as part of the 12-test focused set
```

Figure check:

```text
2645x839, dynamic range=255
```

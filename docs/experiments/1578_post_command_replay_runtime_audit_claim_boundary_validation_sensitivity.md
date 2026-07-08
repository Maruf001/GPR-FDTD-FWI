# Experiment 1578: Post Command-Replay Runtime-Audit Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1577` validator with controlled damaged variants of the
run `1576` claim boundary.

## Output

```text
outputs/experiments/1578_local_2d_state_consistent_objective_revision_post_command_replay_runtime_audit_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_command_replay_runtime_audit_claim_boundary_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_post_command_replay_runtime_audit_claim_boundary_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_command_replay_runtime_audit_claim_boundary_validation_sensitivity.png
```

## Result

```text
scenarios:                         27
expected pass scenarios:           1
expected failure scenarios:        26
observed pass scenarios:           1
observed failure scenarios:        26
unexpected outcomes:               0
runtime-boundary sensitivity ready:true
validator accepts exact run 1576:  true
validator rejects damaged variants:true
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The validator accepts the exact run `1576` boundary and rejects controlled
damage to claim counts, runtime-claim support, runtime metrics, blocked rows,
downstream promotions, figure validation, and script snapshots.

## Decision

Use runs `1576-1578` as the guarded 2D post-runtime-audit claim-boundary block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_command_replay_runtime_audit_claim_boundary_validation_sensitivity.py
3 passed as part of the 12-test focused set
```

Figure check:

```text
3581x879, dynamic range=255
```

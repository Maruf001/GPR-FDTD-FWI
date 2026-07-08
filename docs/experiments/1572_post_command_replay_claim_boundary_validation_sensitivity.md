# Experiment 1572: Post Command-Replay Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1571` validator with controlled damaged variants of the
run `1570` post-command-replay claim boundary.

## Output

```text
outputs/experiments/1572_local_2d_state_consistent_objective_revision_post_command_replay_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_command_replay_claim_boundary_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_post_command_replay_claim_boundary_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_command_replay_claim_boundary_validation_sensitivity.png
```

## Result

```text
scenarios:                         29
expected pass scenarios:           1
expected failure scenarios:        28
observed pass scenarios:           1
observed failure scenarios:        28
unexpected outcomes:               0
claim-boundary sensitivity ready:  true
validator accepts exact run 1570:  true
validator rejects damaged variants:true
aggregate replay executed:         true
local generalization boundary:     true
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The validator accepts the exact run `1570` boundary and rejects controlled
damage to counts, replay state, objective scope, inserted-claim placement,
downstream promotion, figure validation, and script snapshots.

## Decision

Use runs `1570-1572` as the guarded post-command-replay 2D claim-boundary
block. Keep physical, GPU, field-transfer, field-FWI, and 3D/HPC claims
blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_command_replay_claim_boundary_validation_sensitivity.py
3 passed as part of the 12-test focused set
```

Figure check:

```text
3941x886, dynamic range=255
```

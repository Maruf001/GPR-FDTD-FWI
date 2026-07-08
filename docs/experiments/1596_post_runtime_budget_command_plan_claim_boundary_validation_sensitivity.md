# Experiment 1596: Post Runtime-Budget Command Plan Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1595` validator against controlled damage to the
command-plan claim boundary.

## Output

```text
outputs/experiments/1596_local_2d_state_consistent_objective_revision_post_runtime_budget_command_plan_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_runtime_budget_command_plan_claim_boundary_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_post_runtime_budget_command_plan_claim_boundary_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_runtime_budget_command_plan_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       30
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  29
observed failure scenarios:                  29
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 1594:            true
validator rejects damaged variants:          true
new FDTD executed:                           false
GPU work ready:                              false
field transfer ready:                        false
field FWI ready:                             false
3D/HPC ready:                                false
```

The validator accepts the exact run `1594` boundary and rejects damage to
claim counts, command-plan support, budget metrics, hidden command execution,
downstream promotion, figure validation, and script snapshots.

## Decision

Use runs `1594-1596` as the current guarded 2D post-runtime-budget-command-plan
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_runtime_budget_command_plan_claim_boundary_validation_sensitivity.py
4 passed
```

Figure check:

```text
3581x886, dynamic range=255
```

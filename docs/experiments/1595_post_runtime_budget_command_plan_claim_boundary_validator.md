# Experiment 1595: Post Runtime-Budget Command Plan Claim-Boundary Validator

Date: 2026-06-29

## Purpose

Validate the run `1594` claim boundary from saved artifacts.

## Output

```text
outputs/experiments/1595_local_2d_state_consistent_objective_revision_post_runtime_budget_command_plan_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_runtime_budget_command_plan_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_runtime_budget_command_plan_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_runtime_budget_command_plan_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           5
validation checks passed:                    5
blocking failures:                           0
claim-boundary validation ready:             true
claims:                                      29
guarded claims:                              26
blocked claims:                              3
default recommended grid models:             90
two-hour grid models:                        90
large-screen grid models:                    200
command templates emitted:                   0
commands executed:                           false
new FDTD executed:                           false
GPU work ready:                              false
field transfer ready:                        false
field FWI ready:                             false
3D/HPC ready:                                false
```

The validator confirms that the command-plan claim is present, cites
`1591-1593`, records zero executable commands, and keeps downstream readiness
blocked.

## Decision

Use this validator as the artifact guard for run `1594`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_runtime_budget_command_plan_claim_boundary_validator.py
5 passed
```

Figure check:

```text
2645x830, dynamic range=255
```

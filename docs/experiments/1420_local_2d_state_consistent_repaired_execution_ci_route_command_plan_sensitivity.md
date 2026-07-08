# Local 2D Experiment 1420: Repaired Execution CI Route Command Plan Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1419` CI route command-plan validator.

Run `1419` validated the non-executed command plan from a consumer perspective.
This run checks whether that validator fails closed when source readiness,
command counts, executable command shape, blocked-route shape, command-execution
state, fast/full authority, or downstream readiness states are damaged.

It does not run new FDTD/FWI inversions, execute generated commands, launch
GPU/HPC work, compare against field data, or promote physical, field, or 3D
claims.

## Output

```text
outputs/experiments/1420_local_2d_state_consistent_repaired_execution_ci_route_command_plan_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_ci_route_command_plan_sensitivity_scenarios.csv
data/local_2d_state_consistent_repaired_execution_ci_route_command_plan_sensitivity_summary.json
figures/local_2d_state_consistent_repaired_execution_ci_route_command_plan_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CI_ROUTE_COMMAND_PLAN_SENSITIVITY.md
scripts/run_local_2d_state_consistent_repaired_execution_ci_route_command_plan_sensitivity.py
scripts/test_local_2d_state_consistent_repaired_execution_ci_route_command_plan_sensitivity.py
```

## Result

```text
scenarios:                         33
expected pass scenarios:           1
expected failure scenarios:        32
observed pass scenarios:           1
observed failure scenarios:        32
unexpected outcomes:               0
sensitivity ready:                 true
commands executed:                 false
GPU work ready:                    false
ready for 3D/HPC:                  false
```

The exact run `1418` command plan passes. All 32 damaged scenarios fail as
expected, including source-readiness drift, command-count drift, malformed
executable commands, blocked routes with commands, missing blocked reasons,
command-execution drift, fast/full authority drift, and false
physical/GPU/field/FWI/3D promotion.

## Interpretation

The command-plan validator accepts the exact run `1418` plan and rejects
controlled damage to the fields that matter for safe CI use. This guards the
non-executed command plan without promoting it into an executed result.

## Decision

Use runs `1418-1420` as the guarded non-executed CI command-plan package. The
four runnable CPU commands may be used for CI validation. Physical, GPU, field,
field FWI, and 3D/HPC claims remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_repaired_execution_ci_route_command_plan_sensitivity.py
6 passed
```

Figure validation:

```text
figures/local_2d_state_consistent_repaired_execution_ci_route_command_plan_sensitivity.png
3581x879, dynamic range=255
```

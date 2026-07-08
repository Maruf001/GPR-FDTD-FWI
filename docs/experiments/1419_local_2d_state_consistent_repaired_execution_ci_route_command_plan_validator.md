# Local 2D Experiment 1419: Repaired Execution CI Route Command Plan Validator

Date: 2026-06-28

## Purpose

Validate the run `1418` non-executed CI route command plan from a consumer
perspective.

Run `1418` created four runnable CPU pytest commands and two blocked,
non-executable routes. This run checks whether the command plan preserves the
route counts, command shapes, blocked-route behavior, fast/full table authority
boundary, and blocked physical/GPU/field/3D states.

It does not run new FDTD/FWI inversions, execute generated commands, launch
GPU/HPC work, compare against field data, or promote physical, field, or 3D
claims.

## Output

```text
outputs/experiments/1419_local_2d_state_consistent_repaired_execution_ci_route_command_plan_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_ci_route_command_plan_validator_checks.csv
data/local_2d_state_consistent_repaired_execution_ci_route_command_plan_validator_summary.json
figures/local_2d_state_consistent_repaired_execution_ci_route_command_plan_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CI_ROUTE_COMMAND_PLAN_VALIDATOR.md
scripts/run_local_2d_state_consistent_repaired_execution_ci_route_command_plan_validator.py
scripts/test_local_2d_state_consistent_repaired_execution_ci_route_command_plan_validator.py
```

## Result

```text
validation checks:                 5
validation passes:                 5
blocking failures:                 0
validation ready:                  true
source command rows:               6
source executable commands:        4
source blocked commands:           2
commands executed:                 false
full pack remains authoritative:   true
sentinel replaces full pack:       false
GPU work ready:                    false
ready for 3D/HPC:                  false
```

The validator checks:

| Check | Result |
| --- | --- |
| Source guards and command plan are ready | pass |
| Command group counts match route policy | pass |
| Executable and blocked command shapes are valid | pass |
| Fast and full routes preserve table authority | pass |
| Physical/GPU/field/3D claims remain blocked | pass |

## Interpretation

The command plan is internally consistent. Four runnable rows contain CPU
pytest command templates, two blocked rows contain no command and include a
reason, no commands have been executed, and the fast/full authority split is
preserved.

## Decision

Use run `1419` as the positive validator for the CI route command plan.
Sensitivity remains required before treating the command plan as fully guarded.

Physical claims, GPU work, field transfer, field FWI, and 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_repaired_execution_ci_route_command_plan_validator.py
6 passed
```

Figure validation:

```text
figures/local_2d_state_consistent_repaired_execution_ci_route_command_plan_validator.png
2537x839, dynamic range=255
```

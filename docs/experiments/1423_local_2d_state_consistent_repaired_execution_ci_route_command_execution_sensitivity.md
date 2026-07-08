# Local 2D Experiment 1423: Repaired Execution CI Route Command Execution Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1422` execution-smoke validator.

Run `1422` validated the run `1421` CPU command execution smoke under the exact
expected state. This run checks whether the validator fails closed when command
counts, pass/fail fields, blocked-route behavior, authority flags, or
downstream readiness states are damaged.

It does not run new FDTD/FWI inversions, launch GPU/HPC work, compare against
field data, or promote physical, field, or 3D claims.

## Output

```text
outputs/experiments/1423_local_2d_state_consistent_repaired_execution_ci_route_command_execution_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_ci_route_command_execution_sensitivity_scenarios.csv
data/local_2d_state_consistent_repaired_execution_ci_route_command_execution_sensitivity_summary.json
figures/local_2d_state_consistent_repaired_execution_ci_route_command_execution_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CI_ROUTE_COMMAND_EXECUTION_SENSITIVITY.md
scripts/run_local_2d_state_consistent_repaired_execution_ci_route_command_execution_sensitivity.py
scripts/test_local_2d_state_consistent_repaired_execution_ci_route_command_execution_sensitivity.py
```

## Result

```text
scenarios:                         26
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:        25
observed failure scenarios:        25
unexpected outcomes:                0
sensitivity ready:                  true
commands executed:                  true
full pack remains authoritative:    true
sentinel replaces full pack:        false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The exact run `1421` result passes. Twenty-five damaged variants fail as
expected, including count drift, missing rows, command-group drift, failed or
unexecuted runnable commands, nonzero return codes, blocked-route execution,
missing blocked reasons, full-pack authority drift, sentinel/full-pack drift,
and false physical/GPU/field/3D readiness.

## Interpretation

The executed CPU smoke is now guarded from the current consumer side. It proves
the repaired CI route commands run successfully on CPU, but it does not change
the physical or downstream claim boundary.

## Decision

Use runs `1421-1423` as the guarded executed CPU smoke package for the repaired
2D CI route plan.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_repaired_execution_ci_route_command_execution_sensitivity.py
6 passed
```

Figure validation:

```text
figures/local_2d_state_consistent_repaired_execution_ci_route_command_execution_sensitivity.png
3509x890, dynamic range=255
```

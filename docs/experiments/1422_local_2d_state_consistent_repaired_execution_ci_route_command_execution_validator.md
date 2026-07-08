# Local 2D Experiment 1422: Repaired Execution CI Route Command Execution Validator

Date: 2026-06-28

## Purpose

Validate the run `1421` CPU command execution smoke from a consumer
perspective.

Run `1421` executed the four runnable CPU pytest command rows from the repaired
2D CI route plan. This run validates the execution counts, command outcomes,
blocked-route behavior, full-pack authority, and downstream no-go states.

It does not run new FDTD/FWI inversions, launch GPU/HPC work, compare against
field data, or promote physical, field, or 3D claims.

## Output

```text
outputs/experiments/1422_local_2d_state_consistent_repaired_execution_ci_route_command_execution_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_ci_route_command_execution_validator_checks.csv
data/local_2d_state_consistent_repaired_execution_ci_route_command_execution_validator_summary.json
figures/local_2d_state_consistent_repaired_execution_ci_route_command_execution_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CI_ROUTE_COMMAND_EXECUTION_VALIDATOR.md
scripts/run_local_2d_state_consistent_repaired_execution_ci_route_command_execution_validator.py
scripts/test_local_2d_state_consistent_repaired_execution_ci_route_command_execution_validator.py
```

## Result

```text
validation checks:                  5
validation passes:                  5
blocking failures:                  0
validation ready:                   true
source execution rows:              6
source executed commands:           4
commands executed:                  true
full pack remains authoritative:    true
sentinel replaces full pack:        false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The validator checks:

| Check | Result |
| --- | --- |
| Execution summary counts are consistent | pass |
| Command groups and blocked routes match plan | pass |
| Runnable commands passed with zero return code | pass |
| Fast and full authority boundary preserved | pass |
| Physical/GPU/field/3D states blocked | pass |

## Interpretation

The executed CPU smoke is internally consistent: runnable command rows passed,
blocked routes stayed unexecuted, the full pack remains authoritative, and
physical/GPU/field/3D claims remain blocked.

## Decision

Use run `1422` as the positive validator for the executed 2D CI command smoke.
Sensitivity remains required before treating the execution smoke as fully
guarded.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_repaired_execution_ci_route_command_execution_validator.py
5 passed
```

Figure validation:

```text
figures/local_2d_state_consistent_repaired_execution_ci_route_command_execution_validator.png
2645x833, dynamic range=255
```

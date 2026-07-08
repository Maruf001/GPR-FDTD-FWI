# Local 2D Experiment 1416: Repaired Execution CI Route Execution Validator

Date: 2026-06-28

## Purpose

Validate the run `1415` CI route execution manifest from a consumer
perspective.

It does not run new FDTD/FWI inversions, launch GPU/HPC work, compare against
field data, or promote physical, field, or 3D claims.

## Output

```text
outputs/experiments/1416_local_2d_state_consistent_repaired_execution_ci_route_execution_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_ci_route_execution_validator_checks.csv
data/local_2d_state_consistent_repaired_execution_ci_route_execution_validator_summary.json
figures/local_2d_state_consistent_repaired_execution_ci_route_execution_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CI_ROUTE_EXECUTION_VALIDATOR.md
scripts/run_local_2d_state_consistent_repaired_execution_ci_route_execution_validator.py
scripts/test_local_2d_state_consistent_repaired_execution_ci_route_execution_validator.py
```

## Result

```text
validation checks:                         5
validation passes:                         5
blocking failures:                         0
CI route execution validation ready:        true
source CI routes:                          6
source runnable jobs:                      4
source blocked routes:                     2
full pack remains authoritative:           true
sentinel replaces full pack:               false
physical claim ready:                      false
GPU work ready:                            false
field transfer ready:                      false
field FWI ready:                           false
ready for 3D/HPC:                          false
```

## Interpretation

The CI route execution manifest is internally consistent: six routes are
present, four are runnable, two are blocked/design-review routes, fast smoke
uses the 11-row sentinel, and boundary-sensitive routes use the 88-row full
core gate.

## Decision

Use run `1416` as the positive validator for the route execution manifest.
Sensitivity remains required before treating the route execution manifest as
fully guarded.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_repaired_execution_ci_route_execution_validator.py
7 passed
```

Figure validation:

```text
figures/local_2d_state_consistent_repaired_execution_ci_route_execution_validator.png
2537x840, dynamic range=255
```

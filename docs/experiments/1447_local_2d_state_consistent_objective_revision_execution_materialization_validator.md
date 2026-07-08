# Experiment 1447: Objective-Revision Execution Materialization Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1446` local 2D objective-revision execution
materialization from output artifacts.

This run checks the route table, case table, `veryhigh` diagnostic table,
summary flags, figure validation row, and script snapshots. It does not run new
FDTD simulations, launch GPU work, transfer to field data, run field FWI, or
launch 3D/HPC work.

## Output

```text
outputs/experiments/1447_local_2d_state_consistent_objective_revision_execution_materialization_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_execution_materialization_validator_checks.csv
data/local_2d_state_consistent_objective_revision_execution_materialization_validator_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_execution_materialization_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_EXECUTION_MATERIALIZATION_VALIDATOR.md
scripts/run_local_2d_state_consistent_objective_revision_execution_materialization_validator.py
scripts/test_local_2d_state_consistent_objective_revision_execution_materialization_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                                9
passed checks:                        9
failed checks:                        0
validation ready:                     true
source materialization ready:         true
manifest routes:                      6
materialized routes:                  3
materialized case rows:               15
drop-veryhigh truth recovered:        5
majority-vote truth recovered:        5
veryhigh diagnostic truth recovered:  2
veryhigh diagnostic failures:         3
GPU work ready:                       false
field transfer ready:                 false
field FWI ready:                      false
3D/HPC ready:                         false
```

## Interpretation

The saved run `1446` materialization is internally consistent. The
drop-`veryhigh` route is materialized as the local primary policy, majority
vote is materialized as the local cross-check, and `veryhigh` remains a
diagnostic-only route with three saved failures.

The validator also confirms that broad-radius, physical-transfer, GPU,
field-transfer, field-FWI, and 3D/HPC routes remain blocked.

## Decision

Use runs `1446-1447` as the validated local 2D objective-revision execution
materialization. Sensitivity testing remains required before treating this
validator as guarded.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_execution_materialization_validator.py
4 passed
```

Figure validation:

```text
3041x894, dynamic range=255
```

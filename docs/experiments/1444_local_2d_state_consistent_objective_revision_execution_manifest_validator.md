# Experiment 1444: Objective-Revision Execution Manifest Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1443` local 2D objective-revision execution manifest
from output artifacts.

This run checks that primary selection excludes `veryhigh`, majority vote keeps
all six objective labels as a cross-check, `veryhigh` remains diagnostic-only,
blocked routes are not executable, and downstream claims remain blocked.

It does not run new FDTD simulations, launch GPU work, transfer to field data,
run field FWI, or launch 3D/HPC work.

## Output

```text
outputs/experiments/1444_local_2d_state_consistent_objective_revision_execution_manifest_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_execution_manifest_validator_checks.csv
data/local_2d_state_consistent_objective_revision_execution_manifest_validator_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_execution_manifest_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_EXECUTION_MANIFEST_VALIDATOR.md
scripts/run_local_2d_state_consistent_objective_revision_execution_manifest_validator.py
scripts/test_local_2d_state_consistent_objective_revision_execution_manifest_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              9
passed checks:                      9
failed checks:                      0
validation ready:                   true
source manifest ready:              true
manifest routes:                    6
runnable-now routes:                 3
local policy routes:                 2
diagnostic-only routes:              1
primary objectives:                  5
majority cross-check objectives:     6
diagnostic objectives:               1
veryhigh decision objective blocked: true
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The saved run `1443` execution manifest is internally consistent: primary
selection excludes `veryhigh`, majority vote keeps all six objective labels as
a cross-check, `veryhigh` is diagnostic-only, and broad/physical/GPU/field/FWI/
3D routes remain blocked.

## Decision

Use runs `1443-1444` as the validated local 2D objective-revision execution
manifest. Sensitivity testing remains required before treating the validator
itself as guarded.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_execution_manifest_validator.py
3 passed
```

Figure validation:

```text
3005x879, dynamic range=255
```

# Experiment 1777: 84-Grid External Return Live Intake Gate Validator

Date: 2026-07-01

## Purpose

Validate the saved run `1776` live intake gate artifacts from disk.

This run does not materialize observed-by-case data, execute FDTD, launch GPU
work, transfer to field data, run field FWI, or run 3D/HPC.

## Output

```text
outputs/experiments/1777_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source live intake ready:       true
validation checks:              7
passed validation checks:       7
failed validation checks:       0
expected external items:        21
live files present:             0
accepted external items:        0
artifact jobs:                  10
accepted artifact jobs:         0
ready for materialization:      false
new FDTD executed:              false
gpu priority:                   none
```

Validation checks:

| Check | Result |
| --- | --- |
| source live intake ready | pass |
| twenty-one items and ten paired jobs represented | pass |
| current live return remains absent | pass |
| all current intake statuses are missing-file states | pass |
| no artifact job or item is accepted | pass |
| materialization and downstream states remain blocked | pass |
| stage shape, figure, and script snapshots are present | pass |

## Interpretation

The saved live intake artifacts are internally consistent. They represent the
full 21-item return contract and preserve the current zero-acceptance state.

No observed-by-case materialization should be launched from the current archive:
the live-return area still has no accepted approval token, cache array, result
JSON, or paired artifact job.

## Decision

Use run `1777` as the saved-artifact validator for the run `1776` 2D
external-return live intake gate.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validator.py
8 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate.py: pass
run_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```

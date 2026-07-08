# Experiment 1778: 84-Grid External Return Live Intake Gate Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1777` validator for the 84-grid external-return live
intake gate.

This run does not materialize observed-by-case data, execute FDTD, launch GPU
work, transfer to field data, run field FWI, or run 3D/HPC.

## Output

```text
outputs/experiments/1778_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:          true
sensitivity scenarios:           11
expected pass scenarios:         1
expected fail scenarios:         10
observed pass scenarios:         1
observed fail scenarios:         10
unexpected outcomes:             0
damaged scenarios:               10
damaged scenarios rejected:      10
gpu priority:                    none
```

Sensitivity scenarios:

| Scenario | Expected | Observed | First failed check |
| --- | --- | --- | --- |
| exact | pass | pass |  |
| source not ready | fail | fail | source live intake ready |
| item count drift | fail | fail | twenty-one items and ten paired jobs represented |
| file status damage | fail | fail | current live return remains absent |
| intake status damage | fail | fail | all current intake statuses are missing-file states |
| false item acceptance | fail | fail | no artifact job or item is accepted |
| false job acceptance | fail | fail | no artifact job or item is accepted |
| false materialization | fail | fail | materialization and downstream states remain blocked |
| downstream promotion | fail | fail | materialization and downstream states remain blocked |
| figure damage | fail | fail | stage shape, figure, and script snapshots are present |
| snapshot damage | fail | fail | stage shape, figure, and script snapshots are present |

## Interpretation

The live-intake validator accepts only the exact saved run `1776` state. It
rejects damaged source readiness, external-item count drift, file-status drift,
intake-status drift, false item acceptance, false paired-job acceptance, false
materialization, downstream promotion, damaged figure validation, and missing
script snapshots.

## Decision

Use runs `1776-1778` as the guarded 2D external-return live intake block. The
2D branch remains blocked on real external approval and real FDTD materialized
cache/result artifacts.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validation_sensitivity.py
11 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate.py: pass
run_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validator.py: pass
run_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validation_sensitivity.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_validation_sensitivity.py: pass
```

Figure check:

```text
2464x861, dynamic range=255
```

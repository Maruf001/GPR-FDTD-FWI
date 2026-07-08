# Experiment 1787: 84-Grid External Return Staging Plan Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1786` staging-plan validator against controlled damaged
states.

This run does not create a real approval token, does not create cache arrays,
does not create result JSON files, does not stage files into the live external
return area, does not execute copy commands, does not materialize observed-by-
case data, and does not execute FDTD.

## Output

```text
outputs/experiments/1787_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:       true
validation scenarios:         23
expected pass scenarios:      1
expected fail scenarios:      22
observed pass scenarios:      1
observed fail scenarios:      22
unexpected outcomes:          0
damaged scenarios:            22
damaged scenarios rejected:   22
gpu priority:                 none
```

Sensitivity scenarios:

| Scenario | Expected | Observed | Outcome |
| --- | --- | --- | --- |
| exact | pass | pass | expected |
| source not ready | fail | fail | expected |
| item count damage | fail | fail | expected |
| stage count damage | fail | fail | expected |
| approval count damage | fail | fail | expected |
| cache count damage | fail | fail | expected |
| result count damage | fail | fail | expected |
| job count damage | fail | fail | expected |
| template copy allowed | fail | fail | expected |
| real approval promotion | fail | fail | expected |
| real cache promotion | fail | fail | expected |
| real result promotion | fail | fail | expected |
| live file promotion | fail | fail | expected |
| ready-to-stage promotion | fail | fail | expected |
| executed command | fail | fail | expected |
| copy command damage | fail | fail | expected |
| action count damage | fail | fail | expected |
| ready action promotion | fail | fail | expected |
| materialization promotion | fail | fail | expected |
| FDTD promotion | fail | fail | expected |
| downstream promotion | fail | fail | expected |
| figure damage | fail | fail | expected |
| snapshot damage | fail | fail | expected |

## Interpretation

The staging-plan validator accepts the exact non-executed state and rejects
damaged source, count, template-copy, file-promotion, execution, action,
materialization, FDTD, downstream, figure, and script-snapshot states.

This closes the guarded 84-grid external-return staging-plan block. The next
2D state change must come from a real approval token, ten real cache arrays,
and ten real result JSON files that pass guarded intake.

## Decision

Use runs `1785-1787` as the guarded 84-grid external-return staging-plan block.
Keep materialization, new FDTD execution, downstream physical claims, GPU work,
field transfer, and 3D/HPC escalation blocked until real external-return files
pass guarded intake.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validation_sensitivity.py
10 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan.py: pass
run_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validator.py: pass
run_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validation_sensitivity.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validation_sensitivity.py: pass
```

Figure check:

```text
3472x877, dynamic range=255
```

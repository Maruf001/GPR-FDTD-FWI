# Experiment 1784: 84-Grid External Return Package Live Intake Reconciliation Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1783` validator for the 84-grid external-return package
live-intake reconciliation table.

This run does not create fake cache arrays, does not place template files in
the live external-return area, does not accept external evidence, does not
execute FDTD, and does not materialize observed-by-case data.

## Output

```text
outputs/experiments/1784_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:                true
validation scenarios:                  16
expected pass scenarios:               1
expected fail scenarios:               15
observed pass scenarios:               1
observed fail scenarios:               15
unexpected outcomes:                   0
damaged scenarios:                     15
damaged scenarios rejected:            15
gpu priority:                          none
```

Sensitivity scenarios:

| Scenario | Expected | Observed | Result |
| --- | --- | --- | --- |
| exact | pass | pass | expected |
| source not ready | fail | fail | expected |
| item count damage | fail | fail | expected |
| stage count damage | fail | fail | expected |
| template count damage | fail | fail | expected |
| cache template damage | fail | fail | expected |
| live file promotion | fail | fail | expected |
| ready for intake promotion | fail | fail | expected |
| false acceptance | fail | fail | expected |
| status split damage | fail | fail | expected |
| artifact job count damage | fail | fail | expected |
| artifact job promotion | fail | fail | expected |
| materialization promotion | fail | fail | expected |
| FDTD promotion | fail | fail | expected |
| figure damage | fail | fail | expected |
| snapshot damage | fail | fail | expected |

## Interpretation

The reconciliation validator accepts the exact saved pre-return state and
rejects damaged source, count, template, live-file, acceptance, artifact-job,
materialization, FDTD, figure, and snapshot states.

This closes the 84-grid external-return live-intake reconciliation block. The
current physical next step remains external: the real approval token, real cache
arrays, and real result JSON files must arrive and pass intake before
materialization or new FDTD-dependent analysis can proceed.

## Decision

Use runs `1782-1784` as the guarded 84-grid external-return live-intake
reconciliation block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validation_sensitivity.py
10 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation.py: pass
run_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validator.py: pass
run_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validation_sensitivity.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validation_sensitivity.py: pass
```

Figure check:

```text
3040x860, dynamic range=255
```

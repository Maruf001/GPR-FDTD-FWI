# Experiment 1781: 84-Grid External Return Package Template Pack Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the saved run `1780` validator for the 84-grid external-return
package template pack.

This run does not create fake cache arrays, does not place files in the live
external-return area, does not accept external evidence, does not execute FDTD,
and does not materialize observed-by-case data.

## Output

```text
outputs/experiments/1781_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:              true
validation scenarios:                12
expected pass scenarios:             1
expected fail scenarios:             11
observed pass scenarios:             1
observed fail scenarios:             11
unexpected outcomes:                 0
damaged scenarios:                   11
damaged scenarios rejected:          11
gpu priority:                        none
```

Sensitivity scenarios:

| Scenario | Expected | Observed | Result |
| --- | --- | --- | --- |
| exact | pass | pass | expected |
| source not ready | fail | fail | expected |
| item count damage | fail | fail | expected |
| template count damage | fail | fail | expected |
| cache template damage | fail | fail | expected |
| stage shape damage | fail | fail | expected |
| artifact job damage | fail | fail | expected |
| false acceptance | fail | fail | expected |
| false materialization | fail | fail | expected |
| new FDTD promotion | fail | fail | expected |
| figure damage | fail | fail | expected |
| snapshot damage | fail | fail | expected |

## Interpretation

The package-template validator accepts the exact saved run `1779` template pack
and rejects damaged source, count, template, fake-cache, materialization, FDTD,
figure, and snapshot states.

This closes the 84-grid external-return package-template block as a guarded
pre-execution artifact. The current archive still cannot be promoted to
materialized observed-by-case data until real external-return files pass the
live intake gate.

## Decision

Use runs `1779-1781` as the guarded 2D external-return package-template block.
Keep materialization and FDTD blocked until real files pass live intake.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validation_sensitivity.py
11 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack.py: pass
run_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validator.py: pass
run_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validation_sensitivity.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validation_sensitivity.py: pass
```

Figure check:

```text
2572x861, dynamic range=255
```

# Experiment 1780: 84-Grid External Return Package Template Pack Validator

Date: 2026-07-01

## Purpose

Validate the saved run `1779` 84-grid external-return package template pack.

This run does not create fake cache arrays, does not place files in the live
external-return area, does not accept external evidence, does not execute FDTD,
and does not materialize observed-by-case data.

## Output

```text
outputs/experiments/1780_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source template pack ready:          true
validation checks:                   7
passed validation checks:            7
failed validation checks:            0
package items:                       21
JSON templates written:              11
cache array templates written:       0
artifact job template complete:      10
accepted as external return:         0
ready for materialization:           false
new FDTD executed:                   false
gpu priority:                        none
```

Validation checks:

| Check | Result |
| --- | --- |
| source template pack ready | pass |
| twenty-one package items represented | pass |
| JSON templates written without cache templates | pass |
| stage shape is preserved | pass |
| ten artifact jobs are represented | pass |
| materialization remains blocked | pass |
| figure and script snapshots are present | pass |

## Interpretation

The saved 84-grid package template is internally consistent. It represents the
full twenty-one-item external return, writes the one approval template and ten
result JSON templates, writes no cache-array templates, and keeps materialization
blocked.

## Decision

Use run `1780` as the saved-artifact validator for the run `1779` package
template pack.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validator.py
8 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack.py: pass
run_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_template_pack_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```

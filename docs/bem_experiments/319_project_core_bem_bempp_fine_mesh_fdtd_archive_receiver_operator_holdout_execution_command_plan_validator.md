# BEM Experiment 319: Receiver Operator Holdout Execution Command Plan Validator

Date: 2026-06-28

## Purpose

Validate the saved run `318` holdout execution command plan.

This run uses saved artifacts only. It does not run Bempp, FDTD, GPU/HPC,
field transfer, field FWI, or 3D validation.

## Output

```text
outputs/bem_experiments/319_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan_validator_checks.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan_validator_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan_validator.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_RECEIVER_OPERATOR_HOLDOUT_EXECUTION_COMMAND_PLAN_VALIDATOR.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan_validator.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
validation ready:                   true
source command plan ready:          true
command phases:                     7
commands executing now:             0
holdout data present:               false
receiver operator holdout ready:    false
physical claim ready:               false
real BEM/FDTD comparison ready:     false
3D validation claim ready:          false
field transfer ready:               false
GPU/HPC ready:                      false
field FWI ready:                    false
```

Validated checks:

| Check | Result |
| --- | --- |
| source policy and counts | pass |
| phase order and no-refit contract | pass |
| commands are non-executed and non-GPU | pass |
| command script is comment-only plan | pass |
| downstream states blocked | pass |
| figure validation present | pass |
| script snapshots present | pass |

## Interpretation

The run `318` holdout command plan validates as an ordered, non-executed,
no-refit future execution plan with all downstream states blocked.

## Decision

Use run `319` as the guarded validator for the BEM holdout command plan. Do
not execute or promote the holdout branch until independent holdout geometry
and data exist.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan_validator.py
3 passed
```

Figure validation:

```text
2897x875, dynamic range=255
```
